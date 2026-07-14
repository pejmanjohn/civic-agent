import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "drift.py"

spec = importlib.util.spec_from_file_location("drift", SCRIPT_PATH)
drift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drift)


class CompareHeaderFieldsTest(unittest.TestCase):
    def test_matching_fields_are_ok(self):
        checks = drift.compare_header_fields(
            "s",
            {"etag": "abc", "last_modified": "Mon, 01 Jun 2026 00:00:00 GMT", "content_length": 10},
            {"etag": "abc", "last_modified": "Mon, 01 Jun 2026 00:00:00 GMT", "content_length": 10},
        )
        self.assertEqual([c["status"] for c in checks], ["ok", "ok", "ok"])

    def test_etag_comparison_ignores_quoting(self):
        checks = drift.compare_header_fields("s", {"etag": '"abc"'}, {"etag": "abc"})
        self.assertEqual(checks[0]["status"], "ok")

    def test_changed_last_modified_is_drift(self):
        checks = drift.compare_header_fields(
            "s",
            {"last_modified": "Tue, 26 May 2026 23:51:24 GMT"},
            {"last_modified": "Tue, 23 Jun 2026 18:52:10 GMT"},
        )
        self.assertEqual(checks[0]["status"], "drift")

    def test_fields_not_recorded_in_card_are_skipped(self):
        checks = drift.compare_header_fields("s", {"etag": None}, {"etag": "abc"})
        self.assertEqual(checks, [])


class CheckCoverageContractTest(unittest.TestCase):
    """Every source card must either have a live drift check or a documented
    skip reason - silent absence of freshness monitoring is not allowed."""

    def test_every_card_has_a_check_or_a_skip_reason(self):
        card_ids = set(drift.load_source_cards())
        covered = set(drift.LIVE_CHECKS) | set(drift.SKIP_REASONS)
        missing = sorted(card_ids - covered)
        self.assertEqual(
            missing,
            [],
            f"sources without drift coverage decision: {missing}; add a live check "
            f"to LIVE_CHECKS or a documented skip to SKIP_REASONS in scripts/drift.py",
        )

    def test_no_stale_entries_for_removed_cards(self):
        card_ids = set(drift.load_source_cards())
        stale = sorted((set(drift.LIVE_CHECKS) | set(drift.SKIP_REASONS)) - card_ids)
        self.assertEqual(stale, [])


class RunChecksTest(unittest.TestCase):
    def test_unknown_source_id_reports_error(self):
        report = drift.run_checks(["nonexistent.source"])
        self.assertEqual(report["results"][0]["status"], "error")
        self.assertEqual(report["summary"]["error"], 1)

    def test_skipped_sources_report_reason(self):
        report = drift.run_checks(["king_county.open_budget_dashboard"])
        entry = report["results"][0]
        self.assertEqual(entry["status"], "skipped")
        self.assertTrue(entry["detail"])


if __name__ == "__main__":
    unittest.main()
