import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "open-checkbook.source.json"


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            rows.append(json.loads(line))
    return rows


class WashingtonCheckbookHostedAggregatesTest(unittest.TestCase):
    """The checked-in hosted aggregates must stay internally consistent with
    their summary and with the source card that routes agents to them."""

    @classmethod
    def setUpClass(cls):
        cls.card = load_json(CARD_PATH)
        cls.block = cls.card["hosted_aggregates"]
        cls.snapshot_dir = ROOT / cls.block["path"]
        cls.summary = load_json(cls.snapshot_dir / "summary.json")

    def test_card_declares_hosted_aggregates_repo_artifact(self):
        self.assertIn("hosted_aggregates", self.card["storage_policy"]["repo_artifacts"])

    def test_snapshot_version_matches_card_and_data_through(self):
        self.assertEqual(self.block["snapshot_version"], self.summary["snapshot_version"])
        self.assertEqual(self.summary["data_through"], self.card["current_data_through"])
        self.assertIn(self.summary["data_through"], self.block["snapshot_version"])

    def test_all_declared_files_exist(self):
        for name in self.block["files"]:
            self.assertTrue(
                (self.snapshot_dir / name).is_file(), f"missing declared file: {name}"
            )

    def test_row_counts_match_summary(self):
        for filename, stats in self.summary["files"].items():
            rows = load_jsonl(self.snapshot_dir / "aggregates" / filename)
            self.assertEqual(len(rows), stats["row_count"], filename)

    def test_groupings_reconcile_per_biennium(self):
        for biennium, entry in self.summary["reconciliation"].items():
            self.assertTrue(entry["reconciles"], f"{biennium}: {entry}")

    def test_recomputed_category_totals_match_summary(self):
        rows = load_jsonl(self.snapshot_dir / "aggregates" / "category-breakdown.jsonl")
        totals = {}
        for row in rows:
            totals[row["biennium"]] = totals.get(row["biennium"], 0) + row["amount"]
        for biennium, expected in self.summary["amount_totals_by_biennium"].items():
            self.assertAlmostEqual(totals[biennium], expected, places=2, msg=biennium)

    def test_vendor_totals_are_ranked_and_truncated(self):
        rows = load_jsonl(self.snapshot_dir / "aggregates" / "vendor-totals.jsonl")
        top_n = self.summary["vendor_truncation"]["top_n_per_biennium"]
        by_biennium = {}
        for row in rows:
            by_biennium.setdefault(row["biennium"], []).append(row)
        for biennium, vendor_rows in by_biennium.items():
            self.assertLessEqual(len(vendor_rows), top_n, biennium)
            ranks = [row["rank"] for row in vendor_rows]
            self.assertEqual(ranks, sorted(ranks), biennium)
            amounts = [row["amount"] for row in vendor_rows]
            self.assertEqual(amounts, sorted(amounts, reverse=True), biennium)

    def test_every_biennium_is_covered(self):
        rows = load_jsonl(self.snapshot_dir / "aggregates" / "category-breakdown.jsonl")
        self.assertEqual(
            sorted({row["biennium"] for row in rows}), self.summary["biennia"]
        )

    def test_skill_routes_hosted_agents_to_the_aggregates(self):
        skill_text = (ROOT / "jurisdictions" / "washington" / "skill.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(self.block["path"].rstrip("/"), skill_text)
        self.assertIn("top 100 vendors", skill_text)


if __name__ == "__main__":
    unittest.main()
