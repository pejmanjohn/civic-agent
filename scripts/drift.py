#!/usr/bin/env python3
"""Nightly live-drift checks for Civic Agent sources.

Compares cheap live signals (HTTP headers, one Socrata aggregate) against the
expected values recorded in checked-in source-card fingerprints. Exit status:

- 0: every checked source matches its recorded fingerprint.
- 1: at least one source drifted (the official source moved: refresh needed)
  or a check errored (endpoint unreachable, unexpected response).

Drift is a refresh signal, not a data bug: the follow-up is the source's
documented refresh path, then updating the card fingerprint and any dependent
prose or benchmark expectations.

Sources without a cheap live check are reported as skipped so coverage is
explicit rather than silently absent.
"""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "jurisdictions"
TIMEOUT_SECONDS = 60
USER_AGENT = "civic-agent-drift-check (+https://github.com/pejmanjohn/civic-agent)"

# Live totals marked *_approx in cards may restate slightly without meaning
# the dataset moved; treat sub-0.5% movement as matching.
APPROX_RELATIVE_TOLERANCE = 0.005


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Civic Agent live-drift checks.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument(
        "--source",
        action="append",
        help="Limit to one or more source ids (default: all).",
    )
    return parser.parse_args()


def load_source_cards() -> dict[str, dict]:
    cards = {}
    for path in sorted(SOURCE_ROOT.glob("*/sources/*.source.json")):
        with path.open(encoding="utf-8") as handle:
            card = json.load(handle)
        cards[card["id"]] = card
    return cards


def http_head(url: str) -> dict:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        headers = response.headers
        return {
            "status": response.status,
            "etag": (headers.get("ETag") or "").strip(),
            "last_modified": (headers.get("Last-Modified") or "").strip(),
            "content_length": int(headers.get("Content-Length") or 0),
        }


def http_get_json(url: str):
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type:
            # FIT returns SPA HTML with HTTP 200 for malformed routes.
            raise ValueError(f"non-JSON response ({content_type}) from {url}")
        return json.load(response)


def check(name: str, status: str, expected=None, actual=None, detail: str = "") -> dict:
    return {
        "check": name,
        "status": status,
        "expected": expected,
        "actual": actual,
        "detail": detail,
    }


def compare_header_fields(name_prefix: str, expected: dict, actual: dict) -> list[dict]:
    """Compare recorded etag/last-modified/content-length against live HEAD
    values. Only fields the card actually records are compared."""
    checks = []
    field_pairs = [
        ("etag", "etag"),
        ("last_modified", "last_modified"),
        ("content_length", "content_length"),
    ]
    for expected_key, actual_key in field_pairs:
        expected_value = expected.get(expected_key)
        if expected_value in (None, ""):
            continue
        actual_value = actual.get(actual_key)
        if expected_key == "etag":
            matches = str(expected_value).strip('"') == str(actual_value).strip('"')
        else:
            matches = expected_value == actual_value
        checks.append(
            check(
                f"{name_prefix}.{expected_key}",
                "ok" if matches else "drift",
                expected=expected_value,
                actual=actual_value,
            )
        )
    return checks


def check_seattle_operating_budget(card: dict) -> list[dict]:
    endpoint = card["source_fingerprint"]["machine_access"]["json_endpoint"]
    expected = card.get("validation_checks", {})
    query = urllib.parse.urlencode(
        {
            "$select": "count(*) as rows, sum(approved_amount) as total",
            "$where": "fiscal_year=2026",
        }
    )
    payload = http_get_json(f"{endpoint}?{query}")
    if not payload:
        return [check("seattle.fy2026_aggregate", "error", detail="empty SODA response")]
    live_rows = int(payload[0].get("rows", 0))
    live_total = float(payload[0].get("total", 0.0))
    checks = []
    expected_rows = expected.get("fy2026_rows")
    if expected_rows is not None:
        checks.append(
            check(
                "seattle.fy2026_rows",
                "ok" if live_rows == expected_rows else "drift",
                expected=expected_rows,
                actual=live_rows,
            )
        )
    expected_total = expected.get("fy2026_total_approx")
    if expected_total is not None:
        relative = abs(live_total - expected_total) / expected_total
        checks.append(
            check(
                "seattle.fy2026_total_approx",
                "ok" if relative <= APPROX_RELATIVE_TOLERANCE else "drift",
                expected=expected_total,
                actual=live_total,
                detail=f"relative difference {relative:.4%}",
            )
        )
    return checks


def check_open_checkbook(card: dict) -> list[dict]:
    checks = []
    for surface_id, surface in sorted(card.get("source_surfaces", {}).items()):
        if surface.get("status") != "accepted":
            continue
        actual = http_head(surface["url"])
        checks.extend(
            compare_header_fields(f"checkbook.{surface_id}", surface, actual)
        )
    return checks


def check_ofm_population(card: dict) -> list[dict]:
    fingerprint = card["source_fingerprint"]
    url = fingerprint["machine_access"]["file_url"]
    boundary = fingerprint["version_boundary"]
    actual = http_head(url)
    expected = {
        "etag": boundary.get("file_etag"),
        "last_modified": boundary.get("file_last_modified"),
    }
    return compare_header_fields("ofm.april1_file", expected, actual)


def check_king_county_adopted_budget(card: dict) -> list[dict]:
    boundary = card["source_fingerprint"]["version_boundary"]
    url = card["source_surfaces"]["adopted_budget_book_pdf"]["url"]
    actual = http_head(url)
    expected = {
        "etag": boundary.get("pdf_etag"),
        "last_modified": boundary.get("pdf_last_modified"),
        "content_length": boundary.get("pdf_content_length"),
    }
    return compare_header_fields("kc.adopted_budget_pdf", expected, actual)


def check_pierce_open_budget(card: dict) -> list[dict]:
    """Fingerprint the current-biennium budgeted total: stable between
    adopted budgets/supplementals, so movement is a meaningful drift signal."""
    endpoint = card["source_fingerprint"]["machine_access"]["json_endpoint"]
    expected = card.get("validation_checks", {})
    query = urllib.parse.urlencode(
        {
            "$select": "sum(budget) as total, count(*) as rows",
            "$where": 'fiscal_year="2026-2027"',
        }
    )
    payload = http_get_json(f"{endpoint}?{query}")
    if not payload:
        return [check("pierce.budget_2026_2027", "error", detail="empty SODA response")]
    live_total = float(payload[0].get("total", 0.0))
    live_rows = int(payload[0].get("rows", 0))
    checks = []
    expected_total = expected.get("biennium_2026_2027_budget_total")
    if expected_total is not None:
        relative = abs(live_total - expected_total) / expected_total
        checks.append(
            check(
                "pierce.budget_2026_2027_total",
                "ok" if relative <= APPROX_RELATIVE_TOLERANCE else "drift",
                expected=expected_total,
                actual=live_total,
                detail=f"relative difference {relative:.4%}",
            )
        )
    expected_rows = expected.get("biennium_2026_2027_rows")
    if expected_rows is not None:
        checks.append(
            check(
                "pierce.budget_2026_2027_rows",
                "ok" if live_rows == expected_rows else "drift",
                expected=expected_rows,
                actual=live_rows,
            )
        )
    return checks


def check_pierce_open_checkbook(card: dict) -> list[dict]:
    """Fingerprint a CLOSED fiscal year (FY2025) so routine current-year
    growth is not treated as drift; a closed-year change is a restatement."""
    endpoint = card["source_fingerprint"]["machine_access"]["json_endpoint"]
    expected = card.get("validation_checks", {})
    query = urllib.parse.urlencode(
        {
            "$select": "sum(ledger_budget_debit_minus) as total, count(*) as rows",
            "$where": "fiscal_year=2025",
        }
    )
    payload = http_get_json(f"{endpoint}?{query}")
    if not payload:
        return [check("pierce.checkbook_fy2025", "error", detail="empty SODA response")]
    live_total = float(payload[0].get("total", 0.0))
    live_rows = int(payload[0].get("rows", 0))
    checks = []
    expected_total = expected.get("fy2025_total")
    if expected_total is not None:
        relative = abs(live_total - expected_total) / expected_total
        checks.append(
            check(
                "pierce.checkbook_fy2025_total",
                "ok" if relative <= APPROX_RELATIVE_TOLERANCE else "drift",
                expected=expected_total,
                actual=live_total,
                detail=f"relative difference {relative:.4%}",
            )
        )
    expected_rows = expected.get("fy2025_rows")
    if expected_rows is not None:
        checks.append(
            check(
                "pierce.checkbook_fy2025_rows",
                "ok" if live_rows == expected_rows else "drift",
                expected=expected_rows,
                actual=live_rows,
            )
        )
    return checks


def check_fit_filed_actuals(card: dict) -> list[dict]:
    """Two signals: (a) a newer FIT milestone snapshot exists (refresh path),
    (b) a pinned-snapshot fact restated (should never happen for a published
    milestone - treat as a loud alarm)."""
    fingerprint = card["source_fingerprint"]
    pinned_id = fingerprint["retrieval_context"]["fit_snapshot_id"]
    api_base = fingerprint["machine_access"]["api_base"]
    latest = http_get_json(
        f"{api_base}/Snapshots?%24orderby=id%20desc&%24top=1"
    )["value"][0]
    checks = [
        check(
            "fit.latest_milestone_id",
            "ok" if latest["id"] == pinned_id else "drift",
            expected=pinned_id,
            actual=latest["id"],
            detail=f"latest snapshot: {latest.get('name', '')}",
        )
    ]
    expected_rev = card.get("validation_checks", {}).get("spokane_2024_revenues")
    if expected_rev is not None:
        query = urllib.parse.quote("mcag eq '0724' and year eq 2024", safe="()',")
        payload = http_get_json(
            f"{api_base}/Snapshots({pinned_id})/GovernmentMetrics?%24filter={query}"
        )
        live_rev = payload["value"][0]["revenues"] if payload.get("value") else None
        checks.append(
            check(
                "fit.spokane_2024_revenues",
                "ok" if live_rev == expected_rev else "drift",
                expected=expected_rev,
                actual=live_rev,
            )
        )
    return checks


LIVE_CHECKS = {
    "seattle.operating_budget": check_seattle_operating_budget,
    "washington.open_checkbook": check_open_checkbook,
    "washington.ofm_population": check_ofm_population,
    "king_county.adopted_budget": check_king_county_adopted_budget,
    "pierce_county.open_budget": check_pierce_open_budget,
    "pierce_county.open_checkbook": check_pierce_open_checkbook,
    "washington.fit_filed_actuals": check_fit_filed_actuals,
}

# Power BI and ReportViewer surfaces have no cheap unauthenticated freshness
# signal; their staleness is tracked by data-through boundaries in wa20.py.
SKIP_REASONS = {
    "king_county.open_budget_dashboard": "Power BI Gov model refresh requires a report session; no cheap HEAD signal.",
    "washington.operating_budget": "Power BI report surfaces; snapshot age is tracked via wa20.py data-through staleness.",
    "washington.revenue_by_biennium": "ReportViewer export; snapshot age is tracked via wa20.py data-through staleness.",
}


def run_checks(source_ids: list[str] | None = None) -> dict:
    cards = load_source_cards()
    selected = source_ids or sorted(cards)
    results = []
    for source_id in selected:
        if source_id not in cards:
            results.append(
                {
                    "source_id": source_id,
                    "status": "error",
                    "checks": [check("source", "error", detail="unknown source id")],
                }
            )
            continue
        runner = LIVE_CHECKS.get(source_id)
        if runner is None:
            results.append(
                {
                    "source_id": source_id,
                    "status": "skipped",
                    "checks": [],
                    "detail": SKIP_REASONS.get(source_id, "no live check implemented"),
                }
            )
            continue
        try:
            checks = runner(cards[source_id])
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, KeyError, ValueError) as exc:
            results.append(
                {
                    "source_id": source_id,
                    "status": "error",
                    "checks": [check("live", "error", detail=f"{type(exc).__name__}: {exc}")],
                }
            )
            continue
        statuses = {entry["status"] for entry in checks}
        if "drift" in statuses:
            status = "drift"
        elif "error" in statuses:
            status = "error"
        else:
            status = "ok"
        results.append({"source_id": source_id, "status": status, "checks": checks})

    summary = {
        "ok": sum(1 for entry in results if entry["status"] == "ok"),
        "drift": sum(1 for entry in results if entry["status"] == "drift"),
        "error": sum(1 for entry in results if entry["status"] == "error"),
        "skipped": sum(1 for entry in results if entry["status"] == "skipped"),
    }
    return {"results": results, "summary": summary}


def main() -> None:
    args = parse_args()
    report = run_checks(args.source)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for entry in report["results"]:
            print(f"[{entry['status'].upper()}] {entry['source_id']}")
            for item in entry["checks"]:
                if item["status"] == "ok":
                    continue
                print(
                    f"  - {item['check']}: {item['status']} "
                    f"(expected {item['expected']!r}, actual {item['actual']!r}) {item['detail']}"
                )
            if entry.get("detail"):
                print(f"  {entry['detail']}")
        summary = report["summary"]
        print(
            f"Summary: {summary['ok']} ok, {summary['drift']} drift, "
            f"{summary['error']} error, {summary['skipped']} skipped."
        )
    if report["summary"]["drift"] or report["summary"]["error"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
