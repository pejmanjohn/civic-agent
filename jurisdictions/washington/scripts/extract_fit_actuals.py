#!/usr/bin/env python3
"""Snapshot SAO FIT filed annual actuals for reviewed Washington governments.

Pulls government-level total revenues/expenditures (FIT-headline basis:
excluding internal service funds) from the State Auditor's Financial
Intelligence Tool OData API, pinned to a published milestone snapshot, for the
reviewed governments listed below - plus OSPI-sourced school district totals
from the Schools route. Writes a checked-in snapshot under
jurisdictions/washington/data/fit-filed-actuals/<version>/.

FIT covers ~2,300 WA local governments; this snapshot deliberately contains
only the reviewed governments the source card claims. Extend REVIEWED_* lists
and re-run to promote more.

Probe brief: docs/source-probes/washington-fit-filed-actuals.md
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = ROOT / "jurisdictions" / "washington" / "data" / "fit-filed-actuals"

API = "https://portal.sao.wa.gov/FIT/api"
SNAPSHOT_ID = 33
SNAPSHOT_CODE = "MILE2025"
VERSION = "milestone-2025-published-2026-06-30"

# fsSectionId codes per Snapshots(33)/detail financialSummarySections
SECTION_REVENUES = 20
SECTION_EXPENDITURES = 30

REVIEWED_GOVERNMENTS = [
    {"mcag": "0724", "name": "City of Spokane", "gov_type": "city", "county": "Spokane"},
    {"mcag": "0610", "name": "City of Tacoma", "gov_type": "city", "county": "Pierce"},
    {"mcag": "0773", "name": "City of Walla Walla", "gov_type": "city", "county": "Walla Walla"},
    {"mcag": "0247", "name": "City of Vancouver", "gov_type": "city", "county": "Clark"},
    {"mcag": "0664", "name": "City of Everett", "gov_type": "city", "county": "Snohomish"},
    {"mcag": "0127", "name": "King County, Washington", "gov_type": "county", "county": "King"},
    {"mcag": "0152", "name": "Pierce County, Washington", "gov_type": "county", "county": "Pierce"},
    {"mcag": "0162", "name": "Snohomish County, Washington", "gov_type": "county", "county": "Snohomish"},
    {"mcag": "0987", "name": "Sound Transit", "gov_type": "special_district", "county": "King"},
    {"mcag": "3268", "name": "King County Regional Homelessness Authority", "gov_type": "special_district", "county": "King"},
]

REVIEWED_SCHOOL_DISTRICTS = [
    {"mcag": "1903", "name": "Seattle School District No. 1", "county": "King"},
    {"mcag": "1841", "name": "Evergreen School District (Clark County)", "county": "Clark"},
]


def get_json(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "civic-agent-fit-extractor (+https://github.com/pejmanjohn/civic-agent)",
        },
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type:
            # FIT returns SPA HTML with HTTP 200 for any malformed route.
            raise RuntimeError(f"Non-JSON response ({content_type}) from {url}")
        return json.load(response)


def odata_url(path: str, filter_expr: str) -> str:
    return f"{API}/{path}?$filter=" + urllib.parse.quote(filter_expr, safe="()',")


def fetch_government_metrics() -> list[dict]:
    by_mcag = {gov["mcag"]: gov for gov in REVIEWED_GOVERNMENTS}
    mcag_list = ",".join(f"'{mcag}'" for mcag in sorted(by_mcag))
    url = odata_url(f"Snapshots({SNAPSHOT_ID})/GovernmentMetrics", f"mcag in ({mcag_list})")
    payload = get_json(url)
    rows = []
    for entry in payload.get("value", []):
        gov = by_mcag.get(entry.get("mcag"))
        if gov is None:
            continue
        rows.append(
            {
                "mcag": entry["mcag"],
                "government": gov["name"],
                "gov_type": gov["gov_type"],
                "county": gov["county"],
                "year": entry["year"],
                "total_revenues": entry.get("revenues"),
                "total_expenditures": entry.get("expenditures"),
                "fit_population": entry.get("population"),
                "amount_basis": "filed_actuals_excl_internal_service",
                "source_surface_id": "snapshot_government_metrics",
            }
        )
    rows.sort(key=lambda row: (row["government"], row["year"]))
    return rows


def fetch_school_totals() -> list[dict]:
    rows = []
    for district in REVIEWED_SCHOOL_DISTRICTS:
        filter_expr = (
            f"mcag eq '{district['mcag']}' and "
            f"(fsSectionId eq {SECTION_REVENUES} or fsSectionId eq {SECTION_EXPENDITURES}) "
            "and fundCode eq null and fundCategoryId eq null and fundTypeId eq null "
            "and basicAccountId eq null and subAccountId eq null and elementId eq null "
            "and subElementId eq null"
        )
        url = odata_url("Schools/financialReportAggregationsByGovt", filter_expr)
        payload = get_json(url)
        by_year: dict[int, dict] = {}
        for entry in payload.get("value", []):
            year_row = by_year.setdefault(
                entry["year"],
                {
                    "mcag": district["mcag"],
                    "government": district["name"],
                    "gov_type": "school_district",
                    "county": district["county"],
                    "school_fiscal_year_ending_aug31": entry["year"],
                    "total_revenues": None,
                    "total_expenditures": None,
                    "amount_basis": "ospi_modified_accrual_f196",
                    "source_surface_id": "schools_financial_report",
                },
            )
            if entry["fsSectionId"] == SECTION_REVENUES:
                year_row["total_revenues"] = entry.get("totalAmount")
            elif entry["fsSectionId"] == SECTION_EXPENDITURES:
                year_row["total_expenditures"] = entry.get("totalAmount")
        rows.extend(by_year[year] for year in sorted(by_year))
    rows.sort(key=lambda row: (row["government"], row["school_fiscal_year_ending_aug31"]))
    return rows


def main() -> None:
    snapshot_meta = get_json(odata_url("Snapshots", f"id eq {SNAPSHOT_ID}"))["value"][0]
    if snapshot_meta.get("code") != SNAPSHOT_CODE:
        sys.exit(
            f"Snapshot {SNAPSHOT_ID} code changed: expected {SNAPSHOT_CODE}, "
            f"got {snapshot_meta.get('code')}. Re-verify before snapshotting."
        )

    metrics = fetch_government_metrics()
    schools = fetch_school_totals()
    if not metrics or not schools:
        sys.exit("Empty extraction; refusing to write snapshot.")

    out_dir = DATA_ROOT / VERSION
    normalized = out_dir / "normalized"
    normalized.mkdir(parents=True, exist_ok=True)
    write_jsonl(normalized / "government-annual-totals.jsonl", metrics)
    write_jsonl(normalized / "school-district-annual-totals.jsonl", schools)

    year_coverage = {}
    for row in metrics:
        year_coverage.setdefault(row["government"], []).append(row["year"])
    school_coverage = {}
    for row in schools:
        school_coverage.setdefault(row["government"], []).append(
            row["school_fiscal_year_ending_aug31"]
        )

    summary = {
        "source_id": "washington.fit_filed_actuals",
        "snapshot_version": VERSION,
        "fit_snapshot_id": SNAPSHOT_ID,
        "fit_snapshot_code": SNAPSHOT_CODE,
        "fit_snapshot_name": snapshot_meta.get("name"),
        "fit_snapshot_created": snapshot_meta.get("dateCreated"),
        "bars_year": snapshot_meta.get("barsYearUsed"),
        "row_counts": {
            "government-annual-totals.jsonl": len(metrics),
            "school-district-annual-totals.jsonl": len(schools),
        },
        "governments": {
            gov: {"years": sorted(years)} for gov, years in sorted(year_coverage.items())
        },
        "school_districts": {
            gov: {"years": sorted(years)} for gov, years in sorted(school_coverage.items())
        },
        "measure_basis": {
            "governments": "GovernmentMetrics revenues/expenditures = FIT headline basis (excludes internal service funds); some filers report in round thousands.",
            "school_districts": "OSPI F-196 modified accrual; school fiscal year ends Aug 31; 'year' is the ending calendar year.",
        },
        "spot_checks": build_spot_checks(metrics, schools),
    }
    row_counts = summary["row_counts"]
    summary["source_fingerprint"] = {
        "snapshot_version": VERSION,
        "fit_snapshot_id": SNAPSHOT_ID,
        "public_inspection_urls": ["https://portal.sao.wa.gov/FIT/"],
        "row_counts": row_counts,
        "checks": summary["spot_checks"],
    }
    write_json(out_dir / "summary.json", summary)

    provenance = {
        "source_id": "washington.fit_filed_actuals",
        "snapshot_version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generator": "jurisdictions/washington/scripts/extract_fit_actuals.py",
        "api_base": API,
        "fit_snapshot": {
            "id": SNAPSHOT_ID,
            "code": SNAPSHOT_CODE,
            "name": snapshot_meta.get("name"),
            "created": snapshot_meta.get("dateCreated"),
            "total_revenues_all_filers": snapshot_meta.get("totalRevenues"),
            "filers_with_data": snapshot_meta.get("filersWithData"),
        },
        "queries": {
            "government_metrics": f"{API}/Snapshots({SNAPSHOT_ID})/GovernmentMetrics?$filter=mcag in (...)",
            "school_totals": f"{API}/Schools/financialReportAggregationsByGovt?$filter=mcag eq '<mcag>' and (fsSectionId eq 20 or fsSectionId eq 30) and <all dims> eq null",
        },
        "official_bulk_fallback": "https://portal.sao.wa.gov/FIT/extracts/FullExtract(year=<YYYY>)",
        "source_fingerprint": {
            "snapshot_version": VERSION,
            "fit_snapshot_id": SNAPSHOT_ID,
            "public_inspection_urls": ["https://portal.sao.wa.gov/FIT/"],
            "row_counts": {
                "government-annual-totals.jsonl": len(metrics),
                "school-district-annual-totals.jsonl": len(schools),
            },
            "checks": build_spot_checks(metrics, schools),
        },
    }
    write_json(out_dir / "provenance.json", provenance)

    print(
        json.dumps(
            {
                "ok": True,
                "snapshot_version": VERSION,
                "government_rows": len(metrics),
                "school_rows": len(schools),
                "output_dir": str(out_dir.relative_to(ROOT)),
            },
            indent=2,
        )
    )


def build_spot_checks(metrics: list[dict], schools: list[dict]) -> dict:
    def find(rows, government, year, year_key="year"):
        for row in rows:
            if row["government"] == government and row[year_key] == year:
                return row
        return {}

    spokane = find(metrics, "City of Spokane", 2024)
    sound_transit = find(metrics, "Sound Transit", 2024)
    kcrha = find(metrics, "King County Regional Homelessness Authority", 2024)
    sps = find(schools, "Seattle School District No. 1", 2025,
               year_key="school_fiscal_year_ending_aug31")
    return {
        "spokane_2024_revenues": spokane.get("total_revenues"),
        "spokane_2024_expenditures": spokane.get("total_expenditures"),
        "sound_transit_2024_revenues": sound_transit.get("total_revenues"),
        "kcrha_2024_expenditures": kcrha.get("total_expenditures"),
        "seattle_sd_2025_revenues": sps.get("total_revenues"),
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
