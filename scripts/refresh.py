#!/usr/bin/env python3
"""Orchestrated source refresh for Civic Agent.

`python3 scripts/refresh.py <source_id>` runs the source's refresh path end to
end and then tells you exactly what still needs human judgment:

1. re-runs the source's builder/extractor (checked-in snapshot and managed
   sources; live-tier sources need no refresh),
2. validates the refreshed source via scripts/source_data.py,
3. regenerates the coverage matrix, WA-20 scoreboard, and plugin package,
4. greps skills/docs for the PREVIOUS data-through boundary so stale prose
   can't hide,
5. prints the review checklist (card boundary/check values, benchmark
   expectations, expectation-log entry).

It deliberately does NOT edit source cards or benchmark cases: those are
reviewed artifacts, and refreshes can change semantics, not just numbers (the
2026-07-14 revenue refresh flipped a sign under an unchanged label). The
output is a working-tree diff plus a checklist, reviewed like any change.

`--check <source_id>` only reports the freshness state and the refresh path.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "jurisdictions"

# How each source refreshes. commands run from the repo root.
REFRESH_PLANS = {
    "washington.fit_filed_actuals": {
        "commands": [["python3", "jurisdictions/washington/scripts/extract_fit_actuals.py"]],
        "notes": "Rewrites the pinned-version snapshot in place. If a NEWER FIT milestone exists (drift: refresh_available), first update SNAPSHOT_ID/VERSION in the extractor and the card, then run.",
    },
    "washington.dor_property_tax_levies": {
        "commands": [["python3", "jurisdictions/washington/scripts/extract_dor_levy_detail.py"]],
        "notes": "Re-scrape the DOR landing page for moved file URLs before refreshing; add the new tax year to FILE_URLS when due-2026 tables publish.",
    },
    "washington.ofm_population": {
        "commands": [["python3", "jurisdictions/washington/scripts/extract_ofm_population.py", "--live"]],
        "notes": "A new April 1 vintage changes population numbers embedded in skills, demo docs, and benchmark facts - budget extra review time.",
    },
    "washington.revenue_by_biennium": {
        "commands": [["python3", "jurisdictions/washington/scripts/extract_revenue.py", "--live"]],
        "notes": "CARD-FIRST: the extractor writes to the card's snapshot_version directory and stamps its boundary from the current-biennium export. Values REVISE in place between refreshes; never diff totals across versions without noting revisions.",
    },
    "washington.open_checkbook": {
        "commands": [["python3", "scripts/source_data.py", "refresh", "washington.open_checkbook"]],
        "notes": "Downloads ~411MB of official XLSX and rebuilds the local database, then regenerate hosted aggregates: python3 jurisdictions/washington/scripts/build_checkbook_aggregates.py",
    },
    "washington.operating_budget": {
        "commands": None,
        "notes": "Power BI replay snapshot; refresh is a maintainer procedure (see the extractor and card). The known 2026 supplemental is a new source slice, not a refresh.",
    },
    "king_county.open_budget_dashboard": {
        "commands": None,
        "notes": "Power BI Gov template replay; re-capture is manual (see docs/plans/2026-06-04-001-feat-king-county-powerbi-source-plan.md).",
    },
    "king_county.adopted_budget": {
        "commands": None,
        "notes": "Context-only PDF headline; refresh = verify the new adopted budget book and update the card by hand.",
    },
    "seattle.operating_budget": {
        "commands": [],
        "notes": "Live tier - answers query the official API; refresh means updating card validation checks when a new fiscal year publishes.",
    },
    "pierce_county.open_budget": {
        "commands": [],
        "notes": "Live tier - refresh means updating card validation checks when a new biennium or supplemental publishes.",
    },
    "pierce_county.open_checkbook": {
        "commands": [],
        "notes": "Live tier - update the card's freshness.data_through after verifying max(accounting_date) live.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh a Civic Agent source.")
    parser.add_argument("source_id", help="Source card id, e.g. washington.revenue_by_biennium")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report freshness state and the refresh path without running anything.",
    )
    return parser.parse_args()


def load_card(source_id: str) -> dict:
    for path in SOURCE_ROOT.glob("*/sources/*.source.json"):
        card = json.loads(path.read_text(encoding="utf-8"))
        if card["id"] == source_id:
            return card
    sys.exit(f"Unknown source id: {source_id}")


def run(cmd: list[str], *, allow_fail: bool = False) -> int:
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0 and not allow_fail:
        sys.exit(f"Command failed ({result.returncode}); refresh aborted.")
    return result.returncode


def grep_stale_boundary(boundary: str, source_id: str) -> list[str]:
    result = subprocess.run(
        [
            "grep",
            "-rln",
            boundary,
            "skill.md",
            "skills",
            "jurisdictions",
            "docs",
            "benchmarks/wa-citizen/cases.json",
            "--include=*.md",
            "--include=*.json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    hits = [line for line in result.stdout.splitlines() if "data/" not in line]
    return hits


def main() -> None:
    args = parse_args()
    card = load_card(args.source_id)
    plan = REFRESH_PLANS.get(args.source_id)
    if plan is None:
        sys.exit(
            f"No refresh plan registered for {args.source_id}. Add one to "
            f"REFRESH_PLANS in scripts/refresh.py (see CONTRIBUTING.md)."
        )

    freshness = card.get("freshness", {})
    old_boundary = str(freshness.get("data_through", ""))
    print(f"Source: {args.source_id}")
    print(f"Recorded data_through: {old_boundary} (observed {freshness.get('observed_at')})")
    print(f"Refresh notes: {plan['notes']}")

    print("\nCurrent drift/freshness state:")
    run(["python3", "scripts/drift.py", "--status", "--source", args.source_id], allow_fail=True)

    if args.check:
        return
    if plan["commands"] is None:
        sys.exit("\nThis source's refresh is a manual procedure - see the notes above.")
    if not plan["commands"]:
        print("\nLive-tier source: nothing to extract. Review the card's freshness "
              "block and validation checks against the live endpoints instead.")
        return

    for cmd in plan["commands"]:
        run(cmd)

    print("\nValidating refreshed source:")
    run(["python3", "scripts/source_data.py", "validate", args.source_id], allow_fail=True)

    print("\nRegenerating derived artifacts:")
    run(["python3", "scripts/coverage.py"])
    run(["python3", "scripts/wa20.py"])
    run(["python3", "scripts/package_plugin.py"])

    print("\nFiles still mentioning the previous boundary "
          f"({old_boundary!r}) - review each:")
    for hit in grep_stale_boundary(old_boundary, args.source_id) or ["- none found"]:
        print(f"  {hit}")

    print(
        "\nREVIEW CHECKLIST (refresh.py does not edit these on purpose):\n"
        "  1. Card: freshness.data_through/observed_at, validation_checks, "
        "fingerprint values vs the new summary.json.\n"
        "  2. Skill prose: boundary mentions and any hardcoded totals.\n"
        "  3. Benchmark: ratchet any WA-20 case this refresh moves, with an "
        "expectation-log.md entry.\n"
        "  4. Run the full gates: python3 -m unittest discover -s tests && "
        "scripts checks (--check modes).\n"
        "  5. git diff review - values can REVISE in place; note revisions, "
        "never silently overwrite history."
    )


if __name__ == "__main__":
    main()
