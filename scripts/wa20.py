#!/usr/bin/env python3
"""WA-20 Tier 0 coverage scorer.

Deterministically maps each WA-20 benchmark case's required claims onto
checked-in source-card coverage claims and reports, per case, the best answer
mode current coverage can support ("achievable mode"). No LLM, no network.

Modes of operation:

- default: render benchmarks/wa-citizen/scoreboard.md and print a summary.
- --check: verify the scoreboard is current (CI mode). Exits nonzero when the
  scoreboard drifts, when a case expects more than coverage can deliver, or
  when a staleness boundary has been crossed.
- --ratchet-check BASE_REF: compare cases.json against a git base ref and
  enforce the one-way expectation ratchet and question immutability.

Answer-mode semantics follow docs/recipes/scale.md; the ratchet and scoring
rules follow benchmarks/wa-citizen/README.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "wa-citizen" / "cases.json"
CASES_REPO_PATH = "benchmarks/wa-citizen/cases.json"
EXPECTATION_LOG_PATH = ROOT / "benchmarks" / "wa-citizen" / "expectation-log.md"
SCOREBOARD_PATH = ROOT / "benchmarks" / "wa-citizen" / "scoreboard.md"
SOURCE_ROOT = ROOT / "jurisdictions"

ANSWER_MODE_RANK = {
    "unsupported_with_path": 0,
    "needs_refresh": 1,
    "side_by_side_only": 1,
    "partial": 2,
    "exact": 3,
}
MODE_WEIGHT = {
    "exact": 1.0,
    "partial": 0.5,
    "side_by_side_only": 0.5,
    "needs_refresh": 0.25,
    "unsupported_with_path": 0.0,
}
SUPPORTING_CLAIM_STATUSES = {"supported", "partial"}
DATE_PATTERN = re.compile(r"(\d{4})-(\d{2})(?:-(\d{2}))?")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WA-20 Tier 0 coverage scorer.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify benchmarks/wa-citizen/scoreboard.md is current without writing.",
    )
    parser.add_argument(
        "--ratchet-check",
        metavar="BASE_REF",
        help="Enforce the one-way expectation ratchet against a git base ref.",
    )
    parser.add_argument(
        "--as-of",
        metavar="YYYY-MM-DD",
        help="Override the staleness reference date (defaults to today).",
    )
    return parser.parse_args()


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_cases() -> list[dict]:
    return load_json(CASES_PATH)


def load_source_cards() -> list[dict]:
    cards = []
    for path in sorted(SOURCE_ROOT.glob("*/sources/*.source.json")):
        cards.append(load_json(path))
    return cards


def card_jurisdiction_names(card: dict) -> set[str]:
    jurisdictions = card.get("coverage_jurisdictions")
    if jurisdictions:
        return {entry["jurisdiction_name"] for entry in jurisdictions}
    return {card["jurisdiction_name"]}


def parse_dateish(value: str) -> dt.date | None:
    """Best-effort date from strings like 2026-04, 2026-04-01, or
    2025-27-enacted-2025-05-20 (invalid month tokens are skipped)."""
    best = None
    for match in DATE_PATTERN.finditer(value or ""):
        year, month, day = int(match.group(1)), int(match.group(2)), match.group(3)
        if not 1 <= month <= 12:
            continue
        try:
            candidate = dt.date(year, month, int(day) if day else 1)
        except ValueError:
            continue
        if best is None or candidate > best:
            best = candidate
    return best


def card_freshness_date(card: dict) -> dt.date | None:
    """Data-currency date for a card: prefer *_data_through fields in the
    fingerprint version boundary, then snapshot-version-like fields."""
    boundary = card.get("source_fingerprint", {}).get("version_boundary", {})
    through_dates = [
        parse_dateish(value)
        for key, value in boundary.items()
        if isinstance(value, str)
        and "data_through" in key
        and not key.endswith("_label")
    ]
    through_dates = [date for date in through_dates if date]
    if through_dates:
        return max(through_dates)
    for key in ("latest_estimate_date", "snapshot_version"):
        value = boundary.get(key)
        if isinstance(value, str):
            date = parse_dateish(value)
            if date:
                return date
    return None


def supporting_sources(claim: dict, cards: list[dict]) -> list[dict]:
    """Cards whose coverage claims support this case claim."""
    matches = []
    for card in cards:
        if claim["jurisdiction"] not in card_jurisdiction_names(card):
            continue
        for card_claim in card.get("coverage_claims", []):
            if (
                card_claim.get("category") == claim["category"]
                and card_claim.get("status") in SUPPORTING_CLAIM_STATUSES
            ):
                matches.append(
                    {
                        "source_id": card["id"],
                        "status": card_claim["status"],
                        "freshness_date": card_freshness_date(card),
                    }
                )
    return matches


def evaluate_case(case: dict, cards: list[dict], as_of: dt.date) -> dict:
    claims = []
    for claim in case["required_claims"]:
        sources = supporting_sources(claim, cards)
        claims.append({**claim, "supported": bool(sources), "sources": sources})

    core = [claim for claim in claims if claim["role"] == "core"]
    supported_core = [claim for claim in core if claim["supported"]]
    all_supported = all(claim["supported"] for claim in claims)

    if not supported_core:
        computed = "unsupported_with_path"
    elif all_supported:
        computed = case["mode_ceiling"]
    else:
        computed = "partial"
    if ANSWER_MODE_RANK[computed] > ANSWER_MODE_RANK[case["mode_ceiling"]]:
        computed = case["mode_ceiling"]

    stale_sources = []
    unknown_freshness = []
    max_age = case.get("max_data_age_days")
    if max_age and supported_core:
        dated = []
        for claim in supported_core:
            for source in claim["sources"]:
                date = source["freshness_date"]
                if date is None:
                    unknown_freshness.append(source["source_id"])
                    continue
                age = (as_of - date).days
                dated.append((source["source_id"], date, age))
                if age > max_age:
                    # Note stays day-stable (no age-in-days) so --check only
                    # fails when a staleness boundary is crossed, not daily.
                    stale_sources.append(
                        f"{source['source_id']} (data through {date.isoformat()} "
                        f"exceeds the case's {max_age}-day freshness bound)"
                    )
        if dated and all(age > max_age for _, _, age in dated):
            if ANSWER_MODE_RANK[computed] > ANSWER_MODE_RANK["needs_refresh"]:
                computed = "needs_refresh"

    expected = case["expected_answer_mode"]
    expected_rank = ANSWER_MODE_RANK[expected]
    achievable_rank = ANSWER_MODE_RANK[computed]
    error = None
    ratchet_candidate = False
    if expected_rank > achievable_rank:
        error = (
            f"expected {expected} exceeds achievable {computed}: coverage cannot "
            f"deliver what the case promises"
        )
    elif expected_rank < achievable_rank:
        ratchet_candidate = True

    return {
        "id": case["id"],
        "difficulty": case["difficulty"],
        "altitude": case["altitude"],
        "anchor": case.get("anchor", False),
        "expected_mode": expected,
        "achievable_mode": computed,
        "claims": claims,
        "supported_claims": sum(1 for claim in claims if claim["supported"]),
        "total_claims": len(claims),
        "stale_sources": stale_sources,
        "unknown_freshness": sorted(set(unknown_freshness)),
        "error": error,
        "ratchet_candidate": ratchet_candidate,
    }


def evaluate_suite(cases: list[dict], cards: list[dict], as_of: dt.date) -> dict:
    results = [evaluate_case(case, cards, as_of) for case in cases]
    weighted = sum(MODE_WEIGHT[result["achievable_mode"]] for result in results)
    histogram: dict[str, int] = {}
    expected_histogram: dict[str, int] = {}
    for result in results:
        histogram[result["achievable_mode"]] = histogram.get(result["achievable_mode"], 0) + 1
        expected_histogram[result["expected_mode"]] = (
            expected_histogram.get(result["expected_mode"], 0) + 1
        )
    return {
        "results": results,
        "weighted_score": weighted,
        "weighted_pct": 100.0 * weighted / len(results) if results else 0.0,
        "achievable_histogram": histogram,
        "expected_histogram": expected_histogram,
        "errors": [r for r in results if r["error"]],
        "ratchet_candidates": [r for r in results if r["ratchet_candidate"]],
    }


def histogram_line(histogram: dict[str, int]) -> str:
    order = ["exact", "partial", "side_by_side_only", "needs_refresh", "unsupported_with_path"]
    return " | ".join(f"{mode} {histogram.get(mode, 0)}" for mode in order)


def case_notes(result: dict) -> str:
    notes = []
    if result["error"]:
        notes.append(f"ERROR: {result['error']}")
    if result["ratchet_candidate"]:
        notes.append("ratchet candidate: coverage now exceeds expectation")
    notes.extend(f"stale: {entry}" for entry in result["stale_sources"])
    notes.extend(f"freshness unknown: {entry}" for entry in result["unknown_freshness"])
    partial_claims = [
        f"{claim['jurisdiction']} / {claim['category']}"
        for claim in result["claims"]
        if claim["supported"] and all(s["status"] == "partial" for s in claim["sources"])
    ]
    if partial_claims:
        notes.append("partial-status claim: " + "; ".join(partial_claims))
    return " ".join(notes) if notes else "-"


def render_scoreboard(evaluation: dict) -> str:
    lines = [
        "# WA-20 Tier 0 Coverage Scoreboard",
        "",
        "Generated by `python3 scripts/wa20.py` from `benchmarks/wa-citizen/cases.json` and checked-in source cards. Do not hand-edit this file.",
        "",
        "Achievable mode is what current coverage can support, computed from source-card coverage claims; it is not a claim that answers were produced or scored. Tier 1 runs measure actual answers.",
        "",
        "## Headline",
        "",
        f"- Weighted coverage: {evaluation['weighted_pct']:.1f}% ({evaluation['weighted_score']:.2f} / {len(evaluation['results'])})",
        f"- Achievable modes: {histogram_line(evaluation['achievable_histogram'])}",
        f"- Expected modes: {histogram_line(evaluation['expected_histogram'])}",
        f"- Consistency errors: {len(evaluation['errors'])}",
        f"- Ratchet candidates: {len(evaluation['ratchet_candidates'])}",
        "",
        "## Cases",
        "",
        "| Case | Tier | Altitude | Anchor | Expected | Achievable | Claims | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for result in evaluation["results"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result['id']}`",
                    result["difficulty"].split("_")[0],
                    result["altitude"],
                    "yes" if result["anchor"] else "-",
                    f"`{result['expected_mode']}`",
                    f"`{result['achievable_mode']}`",
                    f"{result['supported_claims']}/{result['total_claims']}",
                    case_notes(result).replace("|", "\\|"),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Ratchet Candidates", ""])
    if evaluation["ratchet_candidates"]:
        lines.append(
            "Coverage now exceeds the recorded expectation for these cases. Ratchet the expectation up in cases.json with an expectation-log.md entry:"
        )
        lines.append("")
        for result in evaluation["ratchet_candidates"]:
            lines.append(
                f"- `{result['id']}`: expected `{result['expected_mode']}`, achievable `{result['achievable_mode']}`"
            )
    else:
        lines.append("None.")

    stale = [
        (result["id"], entry)
        for result in evaluation["results"]
        for entry in result["stale_sources"]
    ]
    lines.extend(["", "## Stale Sources", ""])
    if stale:
        for case_id, entry in stale:
            lines.append(f"- `{case_id}`: {entry}")
    else:
        lines.append("None.")

    return "\n".join(lines) + "\n"


def git_show(base_ref: str, repo_path: str) -> str | None:
    """File content at base_ref, or None when the file does not exist there
    (first introduction: the ratchet has no baseline and vacuously passes)."""
    result = subprocess.run(
        ["git", "show", f"{base_ref}:{repo_path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        if "exists on disk, but not in" in stderr or "does not exist" in stderr:
            return None
        raise SystemExit(f"ratchet check: cannot read {repo_path} at {base_ref}: {stderr}")
    return result.stdout


def ratchet_violations(
    base_cases: list[dict], current_cases: list[dict], expectation_log: str
) -> list[str]:
    violations = []
    current_by_id = {case["id"]: case for case in current_cases}
    for base_case in base_cases:
        case_id = base_case["id"]
        current = current_by_id.get(case_id)
        if current is None:
            if case_id not in expectation_log:
                violations.append(
                    f"{case_id}: case removed without an expectation-log.md entry "
                    f"(retire cases by logging the retirement)"
                )
            continue
        if current["question"] != base_case["question"]:
            violations.append(
                f"{case_id}: question text changed; questions are immutable - retire "
                f"the id and add a new case instead"
            )
        base_rank = ANSWER_MODE_RANK[base_case["expected_answer_mode"]]
        current_rank = ANSWER_MODE_RANK[current["expected_answer_mode"]]
        if current_rank < base_rank and case_id not in expectation_log:
            violations.append(
                f"{case_id}: expected_answer_mode downgraded "
                f"{base_case['expected_answer_mode']} -> {current['expected_answer_mode']} "
                f"without an expectation-log.md entry naming the case"
            )
    return violations


def main() -> None:
    args = parse_args()
    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else dt.date.today()

    if args.ratchet_check:
        base_content = git_show(args.ratchet_check, CASES_REPO_PATH)
        if base_content is None:
            print(
                f"Ratchet check passed: no cases.json at {args.ratchet_check} "
                f"(first introduction)."
            )
            return
        base_cases = json.loads(base_content)
        expectation_log = (
            EXPECTATION_LOG_PATH.read_text(encoding="utf-8")
            if EXPECTATION_LOG_PATH.is_file()
            else ""
        )
        violations = ratchet_violations(base_cases, load_cases(), expectation_log)
        if violations:
            print("Ratchet check failed:")
            for violation in violations:
                print(f"- {violation}")
            raise SystemExit(1)
        print("Ratchet check passed.")
        return

    evaluation = evaluate_suite(load_cases(), load_source_cards(), as_of)
    content = render_scoreboard(evaluation)

    if args.check:
        existing = (
            SCOREBOARD_PATH.read_text(encoding="utf-8")
            if SCOREBOARD_PATH.is_file()
            else None
        )
        failed = False
        if existing != content:
            print(
                "Scoreboard is out of date (coverage, expectations, or a staleness "
                "boundary changed). Run `python3 scripts/wa20.py` and review the diff."
            )
            failed = True
        if evaluation["errors"]:
            print("Consistency errors (case expects more than coverage delivers):")
            for result in evaluation["errors"]:
                print(f"- {result['id']}: {result['error']}")
            failed = True
        if failed:
            raise SystemExit(1)
        print("Scoreboard is current.")
        return

    SCOREBOARD_PATH.write_text(content, encoding="utf-8")
    print(
        f"Rendered benchmarks/wa-citizen/scoreboard.md: "
        f"{evaluation['weighted_pct']:.1f}% weighted coverage, "
        f"{len(evaluation['errors'])} consistency errors, "
        f"{len(evaluation['ratchet_candidates'])} ratchet candidates."
    )
    if evaluation["errors"]:
        for result in evaluation["errors"]:
            print(f"- ERROR {result['id']}: {result['error']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
