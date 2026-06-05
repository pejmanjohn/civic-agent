import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "open-checkbook.source.json"


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class WashingtonCheckbookSourceTest(unittest.TestCase):
    def test_source_card_is_parseable_and_scoped_to_checkbook(self):
        source = load_json(SOURCE_CARD_PATH)
        self.assertEqual(source["id"], "washington.open_checkbook")
        self.assertEqual(source["budget_family"], "actual_spending_checkbook")
        self.assertEqual(source["access_method"], "official_bulk_download")
        self.assertEqual(source["storage_policy"]["tier"], "managed_local_db")
        self.assertEqual(source["storage_policy"]["normal_answer_source"], "local_db")
        self.assertEqual(source["current_data_through"], "2026-04")
        self.assertIn("vendor payments", " ".join(source["safe_answer_patterns"]).lower())

    def test_source_surfaces_cover_available_historical_xlsx_files(self):
        source = load_json(SOURCE_CARD_PATH)
        accepted_surfaces = [
            surface
            for surface in source["source_surfaces"].values()
            if surface["status"] == "accepted"
        ]
        self.assertEqual(
            [surface["biennium"] for surface in accepted_surfaces],
            ["2013-15", "2015-17", "2017-19", "2019-21", "2021-23", "2023-25", "2025-27"],
        )
        self.assertEqual(
            sum(surface["content_length"] for surface in accepted_surfaces),
            source["validation_checks"]["historical_file_total_content_length"],
        )
        self.assertEqual(
            source["source_surfaces"]["vendor_payments_2025_27_xlsx"]["actual_data_through"],
            "2026-04",
        )

    def test_actual_spending_coverage_claim_is_supported_with_caveats(self):
        source = load_json(SOURCE_CARD_PATH)
        claim = next(
            claim
            for claim in source["coverage_claims"]
            if claim["category"] == "budget_finance.actual_spending_checkbook"
        )
        self.assertEqual(claim["status"], "supported")
        self.assertEqual(claim["measures"], ["amount"])
        self.assertIn("vendor", claim["grains"])
        self.assertIn("2026", claim["time_coverage"])
        self.assertIn("local database", " ".join(claim["caveats"]).lower())

    def test_unsupported_claims_keep_budget_revenue_and_workforce_separate(self):
        source = load_json(SOURCE_CARD_PATH)
        unsupported = {
            claim["category"]: claim
            for claim in source["coverage_claims"]
            if claim["status"] == "unsupported"
        }
        self.assertEqual(
            set(unsupported),
            {
                "budget_finance.operating_budget",
                "budget_finance.revenue_budget",
                "workforce.budgeted_fte",
            },
        )
        joined_reasons = " ".join(
            claim["unsupported_reason"].lower() for claim in unsupported.values()
        )
        self.assertIn("unsupported by this source", joined_reasons)
        self.assertIn("not operating budget authority", joined_reasons)
        self.assertIn("not revenue budget", joined_reasons)
        self.assertIn("staffing", joined_reasons)


if __name__ == "__main__":
    unittest.main()
