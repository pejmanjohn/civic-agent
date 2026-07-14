import datetime as dt
import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "jurisdictions"
DRIFT_PATH = ROOT / "scripts" / "drift.py"
REFRESH_PATH = ROOT / "scripts" / "refresh.py"

spec = importlib.util.spec_from_file_location("drift_for_freshness", DRIFT_PATH)
drift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drift)

refresh_spec = importlib.util.spec_from_file_location("refresh_for_freshness", REFRESH_PATH)
refresh = importlib.util.module_from_spec(refresh_spec)
refresh_spec.loader.exec_module(refresh)

ALLOWED_KINDS = {"date", "month", "fiscal_year", "calendar_year", "biennium"}
DATA_THROUGH_PATTERNS = {
    "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "month": re.compile(r"^\d{4}-\d{2}$"),
    "fiscal_year": re.compile(r"^\d{4}$"),
    "calendar_year": re.compile(r"^\d{4}$"),
    "biennium": re.compile(r"^\d{4}-\d{2,4}$"),
}


def source_cards():
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(SOURCE_ROOT.glob("*/sources/*.source.json"))
    ]


class SourceFreshnessContractTest(unittest.TestCase):
    """Every source card must declare its freshness contract: what the data
    runs through, when that was observed, the source's publication cadence,
    and how (or whether) upstream can be probed for newer data."""

    def test_every_card_declares_freshness(self):
        missing = [
            card["id"] for card in source_cards() if "freshness" not in card
        ]
        self.assertEqual(missing, [])

    def test_freshness_fields_are_well_formed(self):
        for card in source_cards():
            block = card["freshness"]
            with self.subTest(card["id"]):
                self.assertIn(block["data_through_kind"], ALLOWED_KINDS)
                pattern = DATA_THROUGH_PATTERNS[block["data_through_kind"]]
                self.assertRegex(block["data_through"], pattern)
                dt.date.fromisoformat(block["observed_at"])
                cadence = block["cadence"]
                self.assertIsInstance(cadence["expected_interval_days"], int)
                self.assertGreater(cadence["expected_interval_days"], 0)
                self.assertIsInstance(cadence["expected_lag_days"], int)
                self.assertGreaterEqual(cadence["expected_lag_days"], 0)
                self.assertTrue(str(cadence["pattern"]).strip())

    def test_upstream_probe_references_resolve(self):
        """A probe is either drift:<source id registered in LIVE_CHECKS> or
        none:<reason>. Dangling references defeat the whole point."""
        for card in source_cards():
            probe = card["freshness"]["upstream_probe"]
            with self.subTest(card["id"]):
                if probe.startswith("drift:"):
                    target = probe.split(":", 1)[1]
                    self.assertIn(target, drift.LIVE_CHECKS, probe)
                    self.assertEqual(target, card["id"], probe)
                else:
                    self.assertTrue(
                        probe.startswith("none:") and len(probe) > 5,
                        f"{card['id']} upstream_probe must be drift:<id> or "
                        f"none:<reason>, got {probe!r}",
                    )

    def test_snapshot_sources_data_through_matches_card_boundaries(self):
        """Where a card carries a legacy boundary field, the freshness block
        must agree with it - one source of truth, no drift between them."""
        for card in source_cards():
            block = card["freshness"]
            legacy = card.get("current_data_through") or card.get(
                "actual_data_through"
            )
            if legacy:
                with self.subTest(card["id"]):
                    self.assertTrue(
                        block["data_through"].startswith(legacy)
                        or legacy.startswith(block["data_through"]),
                        f"{card['id']}: freshness.data_through "
                        f"{block['data_through']!r} disagrees with legacy "
                        f"boundary {legacy!r}",
                    )


    def test_every_source_has_a_refresh_plan(self):
        card_ids = {card["id"] for card in source_cards()}
        planned = set(refresh.REFRESH_PLANS)
        self.assertEqual(sorted(card_ids - planned), [], "sources without a refresh plan")
        self.assertEqual(sorted(planned - card_ids), [], "refresh plans for removed sources")


if __name__ == "__main__":
    unittest.main()
