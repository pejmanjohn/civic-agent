import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "jurisdictions" / "washington" / "scripts" / "extract_operating_budget.py"
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "operating-budget.source.json"
SNAPSHOT_DIR = (
    ROOT
    / "jurisdictions"
    / "washington"
    / "data"
    / "operating-budget"
    / "2025-27-enacted-2025-05-20"
)
TEMPLATE_ROOT = ROOT / "jurisdictions" / "washington" / "data" / "operating-budget" / "query_templates"


spec = importlib.util.spec_from_file_location("washington_extract", SCRIPT_PATH)
extract = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(extract)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


class WashingtonPowerBiExtractTest(unittest.TestCase):
    def test_source_card_is_parseable_and_scoped(self):
        source = load_json(SOURCE_CARD_PATH)
        self.assertEqual(source["id"], "washington.operating_budget")
        self.assertEqual(source["access_method"], "powerbi_snapshot")
        self.assertEqual(source["snapshot_version"], "2025-27-enacted-2025-05-20")
        self.assertIn("safe_answer_patterns", source)
        self.assertIn("not_supported_by_this_source", source)
        self.assertIn("source_surfaces", source)
        self.assertEqual(
            source["source_surfaces"]["current_biennial_summary_powerbi"]["status"],
            "accepted",
        )
        self.assertEqual(source["source_surfaces"]["prior_summary_powerbi"]["status"], "accepted")
        self.assertEqual(source["source_surfaces"]["operating_search_powerbi"]["status"], "context_only")
        self.assertEqual(source["default_trend"]["budget_version"], "Enacted")
        self.assertEqual(source["default_trend"]["session_type"], "R1")
        unsupported = " ".join(source["not_supported_by_this_source"])
        self.assertIn("Actual spending", unsupported)
        self.assertIn("2026 supplemental", unsupported)
        self.assertIn("before 2013-15", unsupported)

    def test_snapshot_summary_has_known_validation_checks(self):
        summary = load_json(SNAPSHOT_DIR / "summary.json")
        checks = summary["validation_checks"]
        self.assertEqual(checks["default_fund_view_total"], 150411096000)
        self.assertEqual(checks["totals_by_fund_view"]["Total Budgeted"], 150411096000)
        self.assertEqual(checks["totals_by_fund_view"]["Outlook Funds (NGF-O)"], 77857672000)
        self.assertEqual(checks["default_fund_view_agency_rows"], 102)
        self.assertEqual(checks["default_fund_view_functional_area_rows"], 11)
        self.assertTrue(checks["agency_function_totals_match"])
        self.assertEqual(summary["row_counts"]["historical_biennium_summary"], 7)
        self.assertEqual(summary["row_counts"]["historical_agency_by_biennium"], 711)
        self.assertEqual(summary["row_counts"]["historical_functional_area_by_biennium"], 77)
        self.assertEqual(summary["historical_coverage"]["start_biennium"], "2013-15")
        self.assertEqual(summary["historical_coverage"]["end_biennium"], "2025-27")
        self.assertTrue(checks["historical_agency_totals_match"])
        self.assertTrue(checks["historical_functional_area_totals_match"])
        self.assertTrue(checks["historical_current_overlap_matches"])
        self.assertEqual(checks["historical_current_overlap_total"], 150411096000)
        self.assertEqual(
            checks["historical_totals_by_biennium"],
            {
                "2013-15": 66522466000,
                "2015-17": 78888305000,
                "2017-19": 88274413000,
                "2019-21": 99705964000,
                "2021-23": 121732757000,
                "2023-25": 133609941000,
                "2025-27": 150411096000,
            },
        )

    def test_agency_snapshot_contains_top_total_budgeted_rows(self):
        rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "agency-by-fund-view.jsonl")
        total_budgeted = [row for row in rows if row["fund_view"] == "Total Budgeted"]
        self.assertEqual(len(total_budgeted), 102)

        hca = next(row for row in total_budgeted if row["agency"] == "WA State Health Care Authority")
        self.assertEqual(hca["budgeted_amount"], 38033098000)

        public_schools = next(row for row in total_budgeted if row["agency"] == "Public Schools")
        self.assertEqual(public_schools["budgeted_amount"], 36406761000)

    def test_functional_area_snapshot_matches_agency_total(self):
        agency_rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "agency-by-fund-view.jsonl")
        function_rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "functional-area-by-fund-view.jsonl")
        agency_total = sum(
            row["budgeted_amount"] for row in agency_rows if row["fund_view"] == "Total Budgeted"
        )
        function_total = sum(
            row["budgeted_amount"] for row in function_rows if row["fund_view"] == "Total Budgeted"
        )
        self.assertEqual(agency_total, 150411096000)
        self.assertEqual(function_total, 150411096000)

    def test_historical_biennium_summary_supports_statewide_trends(self):
        rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "historical-biennium-summary.jsonl")
        self.assertEqual(len(rows), 7)
        self.assertEqual([row["biennium"] for row in rows], [
            "2013-15",
            "2015-17",
            "2017-19",
            "2019-21",
            "2021-23",
            "2023-25",
            "2025-27",
        ])
        self.assertEqual(rows[0]["budgeted_amount"], 66522466000)
        self.assertEqual(rows[-1]["budgeted_amount"], 150411096000)
        self.assertEqual({row["source_surface_id"] for row in rows}, {"prior_summary_powerbi"})
        self.assertEqual({row["budget_state"] for row in rows}, {"enacted"})
        self.assertEqual({row["revision_scope"] for row in rows}, {"base"})
        self.assertEqual({row["fund_view"] for row in rows}, {"Total Budgeted"})

    def test_historical_grouped_trend_tables_reconcile_to_statewide_totals(self):
        summary_rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "historical-biennium-summary.jsonl")
        agency_rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "historical-agency-by-biennium.jsonl")
        function_rows = load_jsonl(
            SNAPSHOT_DIR / "normalized" / "historical-functional-area-by-biennium.jsonl"
        )

        expected_totals = {
            row["biennium"]: row["budgeted_amount"]
            for row in summary_rows
        }
        self.assertEqual(
            budgeted_totals_by(agency_rows, "biennium"),
            expected_totals,
        )
        self.assertEqual(
            budgeted_totals_by(function_rows, "biennium"),
            expected_totals,
        )
        self.assertEqual(len(agency_rows), 711)
        self.assertEqual(len(function_rows), 77)
        self.assertEqual(
            {row["source_surface_id"] for row in agency_rows if row["biennium"] == "2025-27"},
            {"current_biennial_summary_powerbi"},
        )
        self.assertEqual(
            {row["source_surface_id"] for row in agency_rows if row["biennium"] != "2025-27"},
            {"prior_summary_powerbi"},
        )
        self.assertFalse(
            duplicate_keys(agency_rows, ["biennium", "agency_code"]),
            "historical agency rows should be unique by biennium and agency code",
        )
        self.assertFalse(
            duplicate_keys(function_rows, ["biennium", "functional_area_code"]),
            "historical functional area rows should be unique by biennium and functional area code",
        )

    def test_committed_query_templates_match_script_builder(self):
        source = load_json(SOURCE_CARD_PATH)
        generated = extract.build_query_templates(source)
        self.assertEqual(len(generated), 6)
        for key, filename in extract.QUERY_TEMPLATE_FILES.items():
            committed = load_json(TEMPLATE_ROOT / filename)
            self.assertEqual(committed, generated[key])

    def test_provenance_records_multiple_surfaces_and_template_routes(self):
        provenance = load_json(SNAPSHOT_DIR / "provenance.json")
        self.assertIn("source_surfaces", provenance)
        self.assertEqual(
            provenance["source_surfaces"]["current_biennial_summary_powerbi"]["status"],
            "accepted",
        )
        self.assertEqual(provenance["source_surfaces"]["prior_summary_powerbi"]["status"], "accepted")
        self.assertEqual(
            provenance["query_templates"]["historical_biennium_summary"]["source_surface_id"],
            "prior_summary_powerbi",
        )
        self.assertEqual(
            provenance["query_templates"]["agency_by_fund_view"]["source_surface_id"],
            "current_biennial_summary_powerbi",
        )

    def test_parse_rows_handles_value_dicts_and_repeat_masks(self):
        payload = {
            "results": [
                {
                    "result": {
                        "data": {
                            "dsr": {
                                "DS": [
                                    {
                                        "PH": [
                                            {
                                                "DM0": [
                                                    {
                                                        "S": [
                                                            {"N": "G0", "DN": "D0"},
                                                            {"N": "G1", "DN": "D1"},
                                                            {"N": "M0"},
                                                        ],
                                                        "C": [0, 0, 10],
                                                    },
                                                    {"C": [1, 20], "R": 1},
                                                    {"C": [1, 30], "R": 2},
                                                ]
                                            }
                                        ],
                                        "ValueDicts": {
                                            "D0": ["FY1", "FY2"],
                                            "D1": ["Agency A", "Agency B"],
                                        },
                                    }
                                ]
                            }
                        }
                    }
                }
            ]
        }
        rows = extract.parse_rows(payload, ["fy", "agency", "amount"])
        self.assertEqual(
            rows,
            [
                {"fy": "FY1", "agency": "Agency A", "amount": 10},
                {"fy": "FY1", "agency": "Agency B", "amount": 20},
                {"fy": "FY2", "agency": "Agency B", "amount": 30},
            ],
        )


def budgeted_totals_by(rows, key):
    totals = {}
    for row in rows:
        totals[row[key]] = totals.get(row[key], 0) + row["budgeted_amount"]
    return dict(sorted(totals.items()))


def duplicate_keys(rows, keys):
    seen = set()
    duplicates = set()
    for row in rows:
        key = tuple(row[field] for field in keys)
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    return duplicates


if __name__ == "__main__":
    unittest.main()
