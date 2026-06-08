import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "king_county" / "sources" / "adopted-budget.source.json"
KING_SKILL_PATH = ROOT / "jurisdictions" / "king_county" / "skill.md"


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class KingCountyAdoptedBudgetSourceTest(unittest.TestCase):
    def test_source_card_is_context_only_and_scoped_to_biennial_framing(self):
        source = load_json(SOURCE_CARD_PATH)
        self.assertEqual(source["id"], "king_county.adopted_budget")
        self.assertEqual(source["storage_policy"]["tier"], "context_only")
        self.assertEqual(source["storage_policy"]["normal_answer_source"], "none")
        self.assertEqual(source["adopted_period"], "2026-2027")
        self.assertEqual(source["adopted_amount"], 20160000000)
        self.assertEqual(source["adopted_amount_label"], "$20.16 billion")
        self.assertEqual(source["coverage_claims"], [])
        unsupported = " ".join(source["not_supported_by_this_source"])
        self.assertIn("Annual dashboard", unsupported)
        self.assertIn("directly comparable", unsupported)

    def test_king_county_skill_presents_dashboard_and_adopted_frames_separately(self):
        skill = KING_SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("adopted budget context", skill)
        self.assertIn("king_county.adopted_budget", skill)
        self.assertIn("$20.16 billion", skill)
        self.assertIn("side by side", skill)
        self.assertIn("do not add, average, or reconcile them", skill)


if __name__ == "__main__":
    unittest.main()
