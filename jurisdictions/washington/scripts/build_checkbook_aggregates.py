#!/usr/bin/env python3
"""Build checked-in hosted aggregates for the Washington Open Checkbook.

The full checkbook is a managed local SQLite (411MB+ of official XLSX);
hosted/fresh agents cannot build it. This script derives small, checked-in
JSONL aggregates - the four named query shapes per biennium - so the hosted
prompt path can give partial checkbook answers instead of a dead end.

Reads the managed local database (build it first with
`python3 scripts/source_data.py ensure washington.open_checkbook`), writes:

    jurisdictions/washington/data/open-checkbook/<version>/
      aggregates/category-breakdown.jsonl
      aggregates/agency-totals.jsonl
      aggregates/vendor-totals.jsonl      (top N vendors per biennium)
      aggregates/monthly-trend.jsonl
      summary.json
      provenance.json

Category, agency, and monthly groupings each partition every payment row, so
their per-biennium totals must reconcile exactly; summary.json records that
check. Vendor totals are truncated to the top N and are the only lossy file.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "open-checkbook.source.json"
DATA_ROOT = ROOT / "jurisdictions" / "washington" / "data" / "open-checkbook"

VENDOR_TOP_N = 100

AGGREGATES = {
    "category-breakdown.jsonl": """
        SELECT biennium, category AS name, SUM(amount) AS amount, COUNT(*) AS payment_rows
        FROM payments
        GROUP BY biennium, category
        ORDER BY biennium, amount DESC
    """,
    "agency-totals.jsonl": """
        SELECT biennium, agency_code, agency_name AS name, SUM(amount) AS amount,
               COUNT(*) AS payment_rows
        FROM payments
        GROUP BY biennium, agency_code, agency_name
        ORDER BY biennium, amount DESC
    """,
    "monthly-trend.jsonl": """
        SELECT biennium, calendar_month AS name, SUM(amount) AS amount,
               COUNT(*) AS payment_rows
        FROM payments
        GROUP BY biennium, calendar_month
        ORDER BY biennium, calendar_month
    """,
}

VENDOR_SQL = f"""
    SELECT biennium, vendor_name AS name, SUM(amount) AS amount, COUNT(*) AS payment_rows
    FROM payments
    WHERE biennium = ?
    GROUP BY vendor_name
    ORDER BY amount DESC
    LIMIT {VENDOR_TOP_N}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build hosted checkbook aggregates.")
    parser.add_argument(
        "--data-home",
        type=Path,
        default=Path(
            os.environ.get("CIVIC_AGENT_DATA_HOME", Path.home() / ".civic-agent" / "data")
        ),
        help="Managed data cache root (matches scripts/source_data.py).",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    args = parse_args()
    manifest_path = (
        args.data_home / "sources" / "washington" / "open_checkbook" / "manifest.json"
    )
    if not manifest_path.is_file():
        sys.exit(
            "Managed checkbook manifest missing. Run "
            "`python3 scripts/source_data.py ensure washington.open_checkbook` first."
        )
    manifest = load_json(manifest_path)
    db_path = Path(manifest["database_path"])
    if not db_path.is_file():
        sys.exit(f"Managed checkbook database missing: {db_path}")

    data_through = manifest.get("data_through")
    current_biennium = manifest.get("current_biennium")
    version = f"{current_biennium}-through-{data_through}"
    out_dir = DATA_ROOT / version
    aggregates_dir = out_dir / "aggregates"
    aggregates_dir.mkdir(parents=True, exist_ok=True)

    file_stats: dict[str, dict] = {}
    totals_by_grouping: dict[str, dict[str, float]] = {}

    with closing(sqlite3.connect(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        biennia = [
            row["biennium"]
            for row in conn.execute("SELECT DISTINCT biennium FROM payments ORDER BY biennium")
        ]

        for filename, sql in AGGREGATES.items():
            rows = [dict(row) for row in conn.execute(sql)]
            write_jsonl(aggregates_dir / filename, rows)
            grouping_totals: dict[str, float] = {}
            for row in rows:
                grouping_totals[row["biennium"]] = (
                    grouping_totals.get(row["biennium"], 0) + row["amount"]
                )
            totals_by_grouping[filename] = {
                biennium: round(total, 2) for biennium, total in grouping_totals.items()
            }
            file_stats[filename] = {"row_count": len(rows)}

        vendor_rows = []
        for biennium in biennia:
            for rank, row in enumerate(conn.execute(VENDOR_SQL, [biennium]), start=1):
                vendor_rows.append({**dict(row), "rank": rank})
        write_jsonl(aggregates_dir / "vendor-totals.jsonl", vendor_rows)
        file_stats["vendor-totals.jsonl"] = {
            "row_count": len(vendor_rows),
            "top_n_per_biennium": VENDOR_TOP_N,
            "truncated": True,
        }

    reference = totals_by_grouping["category-breakdown.jsonl"]
    reconciliation = {
        biennium: {
            "category_total": reference.get(biennium),
            "agency_total": totals_by_grouping["agency-totals.jsonl"].get(biennium),
            "monthly_total": totals_by_grouping["monthly-trend.jsonl"].get(biennium),
            "reconciles": (
                reference.get(biennium)
                == totals_by_grouping["agency-totals.jsonl"].get(biennium)
                == totals_by_grouping["monthly-trend.jsonl"].get(biennium)
            ),
        }
        for biennium in biennia
    }
    if not all(entry["reconciles"] for entry in reconciliation.values()):
        sys.exit(f"Aggregate groupings do not reconcile: {json.dumps(reconciliation, indent=2)}")

    summary = {
        "source_id": "washington.open_checkbook",
        "snapshot_version": version,
        "kind": "hosted_aggregates",
        "current_biennium": current_biennium,
        "data_through": data_through,
        "biennia": biennia,
        "grain": "biennium x (category | agency | top_vendor | calendar_month)",
        "measure": "amount (actual vendor payments, dollars)",
        "vendor_truncation": {
            "top_n_per_biennium": VENDOR_TOP_N,
            "note": (
                "vendor-totals.jsonl keeps the top vendors by total amount per "
                "biennium; full vendor grain requires the managed local database."
            ),
        },
        "files": file_stats,
        "amount_totals_by_biennium": reference,
        "reconciliation": reconciliation,
    }
    write_json(out_dir / "summary.json", summary)

    provenance = {
        "source_id": "washington.open_checkbook",
        "snapshot_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generator": "jurisdictions/washington/scripts/build_checkbook_aggregates.py",
        "database_row_count": manifest.get("row_count"),
        "source_files": [
            {
                key: entry.get(key)
                for key in (
                    "source_surface_id",
                    "biennium",
                    "url",
                    "last_modified",
                    "content_length",
                    "sha256",
                    "row_count",
                )
            }
            for entry in manifest.get("source_files", [])
        ],
    }
    write_json(out_dir / "provenance.json", provenance)

    print(
        json.dumps(
            {
                "ok": True,
                "snapshot_version": version,
                "output_dir": str(out_dir.relative_to(ROOT)),
                "files": file_stats,
                "data_through": data_through,
            },
            indent=2,
            sort_keys=True,
        )
    )


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
