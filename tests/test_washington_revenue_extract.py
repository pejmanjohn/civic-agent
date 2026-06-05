import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "jurisdictions" / "washington" / "scripts" / "extract_revenue.py"
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "revenue-by-biennium.source.json"
SNAPSHOT_DIR = (
    ROOT
    / "jurisdictions"
    / "washington"
    / "data"
    / "revenue-by-biennium"
    / "2025-27-revenue-through-2026-04"
)


spec = importlib.util.spec_from_file_location("washington_revenue_extract", SCRIPT_PATH)
extract = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = extract
spec.loader.exec_module(extract)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


class WashingtonRevenueExtractTest(unittest.TestCase):
    def test_source_card_is_parseable_and_scoped(self):
        source = load_json(SOURCE_CARD_PATH)
        self.assertEqual(source["id"], "washington.revenue_by_biennium")
        self.assertEqual(source["access_method"], "reportviewer_snapshot")
        self.assertEqual(source["snapshot_version"], "2025-27-revenue-through-2026-04")
        self.assertEqual(source["actual_data_through"], "2026-04")
        self.assertEqual(source["actual_data_through_label"], "Actual Data Through April 2026")
        self.assertEqual(source["actual_data_through_precision"], "month")
        self.assertEqual(source["default_fund"], "General Fund (001)")
        self.assertEqual(
            source["source_surfaces"]["statewide_revenue_reportviewer"]["status"],
            "accepted",
        )
        self.assertEqual(
            source["source_surfaces"]["fund_detail_by_revenue_source_reportviewer"]["status"],
            "context_only",
        )
        revenue_claim = next(
            claim
            for claim in source["coverage_claims"]
            if claim["category"] == "budget_finance.revenue_budget"
        )
        self.assertEqual(revenue_claim["status"], "partial")
        self.assertEqual(revenue_claim["measures"], ["estimated_revenue"])
        self.assertIn("full-biennium forecast", " ".join(revenue_claim["caveats"]))

    def test_snapshot_summary_captures_historical_coverage_and_current_partial_status(self):
        summary = load_json(SNAPSHOT_DIR / "summary.json")
        self.assertEqual(summary["source_id"], "washington.revenue_by_biennium")
        self.assertEqual(summary["source_fingerprint"]["row_counts"], summary["row_counts"])
        self.assertIn("exports", summary["source_fingerprint"]["integrity"])
        self.assertEqual(summary["actual_data_through"], "2026-04")
        self.assertEqual(summary["actual_data_through_label"], "Actual Data Through April 2026")
        self.assertEqual(summary["row_counts"]["general_fund_revenue_by_biennium"], 12)
        self.assertEqual(summary["row_counts"]["general_fund_revenue_by_area_account"], 934)
        self.assertEqual(summary["historical_coverage"]["start_biennium"], "2003-05")
        self.assertEqual(summary["historical_coverage"]["end_biennium"], "2025-27")
        self.assertEqual(
            summary["historical_coverage"]["biennia"],
            [
                "2003-05",
                "2005-07",
                "2007-09",
                "2009-11",
                "2011-13",
                "2013-15",
                "2015-17",
                "2017-19",
                "2019-21",
                "2021-23",
                "2023-25",
                "2025-27",
            ],
        )
        statuses = summary["actual_data_status_by_biennium"]
        self.assertEqual(statuses["2025-27"], "partial")
        self.assertEqual(
            {status for biennium, status in statuses.items() if biennium != "2025-27"},
            {"complete"},
        )
        checks = summary["validation_checks"]
        self.assertTrue(checks["detail_totals_match_statewide_totals"])
        self.assertEqual(checks["current_biennium_estimated_revenue"], 45098726991)
        self.assertEqual(checks["current_biennium_actual_revenue"], 46142570002.15)
        self.assertEqual(checks["current_biennium_actual_minus_estimate"], 1043843011.15)
        self.assertEqual(checks["current_biennium_actual_data_status"], "partial")

    def test_biennium_rows_are_ordered_and_carry_actual_data_boundary(self):
        rows = load_jsonl(
            SNAPSHOT_DIR / "normalized" / "general-fund-revenue-by-biennium.jsonl"
        )
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[0]["biennium"], "2003-05")
        self.assertEqual(rows[-1]["biennium"], "2025-27")
        self.assertEqual({row["fund"] for row in rows}, {"General Fund (001)"})
        self.assertEqual({row["actual_data_through"] for row in rows}, {"2026-04"})
        self.assertEqual(
            {row["actual_data_through_label"] for row in rows},
            {"Actual Data Through April 2026"},
        )
        self.assertEqual(rows[-1]["actual_data_status"], "partial")
        self.assertEqual(rows[-1]["estimated_revenue"], 45098726991)
        self.assertEqual(rows[-1]["actual_revenue"], 46142570002.15)

    def test_detail_rows_reconcile_to_statewide_rows(self):
        statewide_rows = load_jsonl(
            SNAPSHOT_DIR / "normalized" / "general-fund-revenue-by-biennium.jsonl"
        )
        detail_rows = load_jsonl(
            SNAPSHOT_DIR / "normalized" / "general-fund-revenue-by-area-account.jsonl"
        )
        self.assertEqual(len(detail_rows), 934)
        self.assertFalse(
            duplicate_keys(detail_rows, ["biennium", "revenue_area", "account_or_agency"])
        )
        statewide_by_biennium = {row["biennium"]: row for row in statewide_rows}
        for biennium, detail_total in totals_by_biennium(detail_rows).items():
            statewide = statewide_by_biennium[biennium]
            self.assertAlmostEqual(
                detail_total["estimated_revenue"], statewide["estimated_revenue"], delta=1
            )
            self.assertAlmostEqual(
                detail_total["actual_revenue"], statewide["actual_revenue"], delta=1
            )
            self.assertAlmostEqual(
                detail_total["actual_minus_estimate"],
                statewide["actual_minus_estimate"],
                delta=1,
            )

    def test_provenance_records_reportviewer_exports(self):
        provenance = load_json(SNAPSHOT_DIR / "provenance.json")
        self.assertEqual(provenance["access_method"], "reportviewer_snapshot")
        self.assertIn("source_fingerprint", provenance)
        self.assertIn("exports", provenance["source_fingerprint"]["integrity"])
        self.assertEqual(provenance["actual_data_through"], "2026-04")
        self.assertEqual(provenance["actual_data_through_label"], "Actual Data Through April 2026")
        self.assertEqual(provenance["actual_data_through_precision"], "month")
        self.assertEqual(
            provenance["report_parameters"]["biennium_field"],
            "ReportViewer1$ctl08$ctl03$ddValue",
        )
        self.assertEqual(provenance["report_parameters"]["fund"], "General Fund (001)")
        self.assertIn("2025-27", provenance["exports"])
        current_export = provenance["exports"]["2025-27"]
        self.assertEqual(current_export["actual_data_through"], "2026-04")
        self.assertEqual(current_export["actual_data_status"], "partial")
        self.assertRegex(current_export["xml_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(current_export["xlsx_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(current_export["csv_sha256"], r"^[0-9a-f]{64}$")

    def test_parse_revenue_xml_handles_known_report_shape(self):
        xml = b"""<?xml version="1.0" encoding="utf-8"?>
        <Report xmlns="RevenueSW">
          <table1 textbox32="3.00000" textbox33="5.50000" textbox34="2.50000">
            <table1_Group1_Collection>
              <table1_Group1 textbox13="Area A" textbox26="3.00000" textbox27="5.50000" textbox28="2.50000">
                <Detail_Collection>
                  <Detail AgencyTitle="Account One  " Amount1="1.00000" Amount2="2.00000" Amount3="1.00000" />
                  <Detail AgencyTitle="Account Two" Amount1="2.00000" Amount2="3.50000" Amount3="1.50000" />
                </Detail_Collection>
              </table1_Group1>
            </table1_Group1_Collection>
          </table1>
        </Report>
        """
        parsed = extract.parse_revenue_xml(xml)
        self.assertEqual(parsed["totals"]["estimated_revenue_thousands"], 3)
        self.assertEqual(parsed["totals"]["actual_revenue_thousands"], 5.5)
        self.assertEqual(len(parsed["groups"]), 1)
        self.assertEqual(parsed["groups"][0]["revenue_area"], "Area A")
        self.assertEqual(parsed["groups"][0]["details"][0]["account_or_agency"], "Account One")


def duplicate_keys(rows, keys):
    seen = set()
    duplicates = set()
    for row in rows:
        key = tuple(row[field] for field in keys)
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    return duplicates


def totals_by_biennium(rows):
    totals = {}
    for row in rows:
        bucket = totals.setdefault(
            row["biennium"],
            {
                "estimated_revenue": 0,
                "actual_revenue": 0,
                "actual_minus_estimate": 0,
            },
        )
        for key in bucket:
            bucket[key] += row[key]
    return totals


if __name__ == "__main__":
    unittest.main()
