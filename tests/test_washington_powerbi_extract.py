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
        unsupported = " ".join(source["not_supported_by_this_source"])
        self.assertIn("Actual spending", unsupported)
        self.assertIn("2026 supplemental", unsupported)

    def test_snapshot_summary_has_known_validation_checks(self):
        summary = load_json(SNAPSHOT_DIR / "summary.json")
        checks = summary["validation_checks"]
        self.assertEqual(checks["default_fund_view_total"], 150411096000)
        self.assertEqual(checks["totals_by_fund_view"]["Total Budgeted"], 150411096000)
        self.assertEqual(checks["totals_by_fund_view"]["Outlook Funds (NGF-O)"], 77857672000)
        self.assertEqual(checks["default_fund_view_agency_rows"], 102)
        self.assertEqual(checks["default_fund_view_functional_area_rows"], 11)
        self.assertTrue(checks["agency_function_totals_match"])

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

    def test_committed_query_templates_match_script_builder(self):
        source = load_json(SOURCE_CARD_PATH)
        generated = extract.build_query_templates(source)
        for key, filename in extract.QUERY_TEMPLATE_FILES.items():
            committed = load_json(TEMPLATE_ROOT / filename)
            self.assertEqual(committed, generated[key])

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


if __name__ == "__main__":
    unittest.main()
