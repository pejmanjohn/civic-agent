import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "source_data.py"


spec = importlib.util.spec_from_file_location("civic_source_data_validation", SCRIPT_PATH)
source_data = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = source_data
spec.loader.exec_module(source_data)


def fingerprint():
    return {
        "public_inspection_urls": ["https://example.test/source"],
        "machine_access": {"type": "fixture"},
        "retrieval_context": {"dataset_id": "fixture"},
        "version_boundary": {"snapshot_version": "fixture"},
        "row_counts": {"rows": 1},
        "checks": {"rows": 1},
    }


class SourceDataValidationTest(unittest.TestCase):
    def tearDown(self):
        source_data.BUILDER_REGISTRY.clear()
        source_data.QUERY_REGISTRY.clear()
        source_data.VALIDATOR_REGISTRY.clear()

    def test_validate_live_source_checks_source_card_contract_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = source_data.parse_args(
                ["--data-home", tmp, "validate", "seattle.operating_budget"]
            )
            result = source_data.run_command(args)
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["storage_tier"], "live")
            self.assertIn("source_fingerprint", result)
            self.assertIn("live_artifact_not_required", check_names(result))

    def test_validate_current_checked_in_snapshots_offline(self):
        expected = {
            "king_county.open_budget_dashboard": "valid",
            "washington.operating_budget": "valid",
            "washington.revenue_by_biennium": "partial_current_period",
            "washington.ofm_population": "valid",
            "washington.fit_filed_actuals": "valid",
        }
        with tempfile.TemporaryDirectory() as tmp:
            for source_id, status in expected.items():
                args = source_data.parse_args(["--data-home", tmp, "validate", source_id])
                result = source_data.run_command(args)
                self.assertTrue(result["ok"], source_id)
                self.assertEqual(result["status"], status, source_id)
                self.assertIn("snapshot_path", result, source_id)
                self.assertIn("summary_source_fingerprint", check_names(result))

    def test_validate_refresh_check_is_explicit_and_non_mutating(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = source_data.parse_args(
                [
                    "--data-home",
                    tmp,
                    "validate",
                    "washington.revenue_by_biennium",
                    "--refresh-check",
                ]
            )
            result = source_data.run_command(args)
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "partial_current_period")
            self.assertIn("refresh_check", check_names(result))
            self.assertTrue(result["warnings"])

    def test_validate_all_uses_registered_validator_and_aggregates_failures(self):
        source = {
            "id": "example.source",
            "storage_policy": {
                "tier": "checked_in_snapshot",
                "normal_answer_source": "repo_snapshot",
            },
            "source_fingerprint": fingerprint(),
            "_path": "jurisdictions/example/sources/source.source.json",
        }

        def fake_load_source_cards():
            return [source]

        def fake_validator(context, refresh_check):
            return {
                "ok": True,
                "status": "valid",
                "source_fingerprint": {"preserved": True},
                "checks": [source_data.passed_check("fake_check")],
            }

        original = source_data.load_source_cards
        source_data.load_source_cards = fake_load_source_cards
        source_data.VALIDATOR_REGISTRY["example.source"] = fake_validator
        try:
            with tempfile.TemporaryDirectory() as tmp:
                args = source_data.parse_args(["--data-home", tmp, "validate", "--all"])
                result = source_data.run_command(args)
                self.assertTrue(result["ok"])
                self.assertEqual(result["source_count"], 1)
                self.assertEqual(result["results"][0]["source_fingerprint"], {"preserved": True})
                self.assertIn("fake_check", check_names(result["results"][0]))
        finally:
            source_data.load_source_cards = original

    def test_validate_unsupported_storage_tier_fails_clearly(self):
        source = {
            "id": "example.source",
            "storage_policy": {
                "tier": "hosted_artifact",
                "normal_answer_source": "hosted_artifact",
            },
            "source_fingerprint": fingerprint(),
            "_path": "jurisdictions/example/sources/source.source.json",
        }

        def fake_load_source_card(source_id):
            return source

        original = source_data.load_source_card
        source_data.load_source_card = fake_load_source_card
        try:
            with tempfile.TemporaryDirectory() as tmp:
                args = source_data.parse_args(["--data-home", tmp, "validate", "example.source"])
                result = source_data.run_command(args)
                self.assertFalse(result["ok"])
                self.assertEqual(result["status"], "validation_failed")
                self.assertIn("validator_registered", check_names(result))
        finally:
            source_data.load_source_card = original

    def test_validate_managed_local_db_checks_manifest_and_sqlite(self):
        source = {
            "id": "example.checkbook",
            "storage_policy": {
                "tier": "managed_local_db",
                "normal_answer_source": "local_db",
            },
            "source_fingerprint": fingerprint(),
            "current_biennium": "2025-27",
            "source_surfaces": {
                "surface_a": {
                    "status": "accepted",
                    "biennium": "2025-27",
                    "url": "https://example.test/current.xlsx",
                    "last_modified": "Tue, 26 May 2026 23:51:24 GMT",
                    "content_length": 123,
                }
            },
            "_path": "jurisdictions/example/sources/checkbook.source.json",
        }

        def fake_load_source_card(source_id):
            return source

        original = source_data.load_source_card
        source_data.load_source_card = fake_load_source_card
        source_data.VALIDATOR_REGISTRY["example.checkbook"] = (
            source_data.validate_washington_open_checkbook
        )
        try:
            with tempfile.TemporaryDirectory() as tmp:
                args = source_data.parse_args(
                    ["--data-home", tmp, "validate", "example.checkbook"]
                )
                context = source_data.source_context("example.checkbook", data_home=Path(tmp))
                context.source_dir.mkdir(parents=True)
                db_path = context.source_dir / "checkbook.sqlite"
                create_checkbook_fixture_db(db_path)
                manifest = {
                    "ok": True,
                    "status": "partial_current_period",
                    "database_path": str(db_path),
                    "row_count": 1,
                    "current_biennium": "2025-27",
                    "data_through": "2026-04",
                    "source_files": [
                        {
                            "source_surface_id": "surface_a",
                            "biennium": "2025-27",
                            "url": "https://example.test/current.xlsx",
                            "last_modified": "Tue, 26 May 2026 23:51:24 GMT",
                            "content_length": 123,
                            "sha256": "a" * 64,
                            "row_count": 1,
                        }
                    ],
                    "source_fingerprint": {
                        "row_counts": {"payments": 1},
                        "checks": {"current_file_data_through": "2026-04"},
                    },
                }
                source_data.write_json(context.manifest_path, manifest)

                result = source_data.run_command(args)
                self.assertTrue(result["ok"])
                self.assertEqual(result["status"], "partial_current_period")
                self.assertIn("local_database_payment_rows", check_names(result))
                self.assertIn("local_database_required_indexes", check_names(result))
        finally:
            source_data.load_source_card = original

    def test_validate_managed_local_db_reports_schema_failure_without_validator_error(self):
        source = {
            "id": "example.checkbook",
            "storage_policy": {
                "tier": "managed_local_db",
                "normal_answer_source": "local_db",
            },
            "source_fingerprint": fingerprint(),
            "current_biennium": "2025-27",
            "source_surfaces": {},
            "_path": "jurisdictions/example/sources/checkbook.source.json",
        }

        def fake_load_source_card(source_id):
            return source

        original = source_data.load_source_card
        source_data.load_source_card = fake_load_source_card
        source_data.VALIDATOR_REGISTRY["example.checkbook"] = (
            source_data.validate_washington_open_checkbook
        )
        try:
            with tempfile.TemporaryDirectory() as tmp:
                args = source_data.parse_args(
                    ["--data-home", tmp, "validate", "example.checkbook"]
                )
                context = source_data.source_context("example.checkbook", data_home=Path(tmp))
                context.source_dir.mkdir(parents=True)
                db_path = context.source_dir / "checkbook.sqlite"
                create_incomplete_checkbook_fixture_db(db_path)
                manifest = {
                    "ok": True,
                    "status": "current",
                    "database_path": str(db_path),
                    "row_count": 1,
                    "current_biennium": "2025-27",
                    "data_through": "2026-04",
                    "source_files": [],
                    "source_fingerprint": {
                        "row_counts": {"payments": 1},
                        "checks": {"current_file_data_through": "2026-04"},
                    },
                }
                source_data.write_json(context.manifest_path, manifest)

                result = source_data.run_command(args)
                self.assertFalse(result["ok"])
                self.assertEqual(result["status"], "validation_failed")
                self.assertIn("local_database_required_tables", check_names(result))
                self.assertNotIn("validator_error", check_names(result))
        finally:
            source_data.load_source_card = original


def create_checkbook_fixture_db(path):
    with closing(sqlite3.connect(path)) as conn:
        conn.executescript(
            """
            CREATE TABLE source_files (
              file_id INTEGER PRIMARY KEY,
              source_surface_id TEXT NOT NULL,
              biennium TEXT NOT NULL,
              url TEXT NOT NULL,
              fetched_at TEXT NOT NULL,
              last_modified TEXT,
              content_length INTEGER NOT NULL,
              sha256 TEXT NOT NULL,
              row_count INTEGER NOT NULL,
              status TEXT NOT NULL
            );
            CREATE TABLE payments (
              payment_id INTEGER PRIMARY KEY,
              biennium TEXT NOT NULL,
              fiscal_year INTEGER NOT NULL,
              fiscal_month INTEGER NOT NULL,
              calendar_month TEXT NOT NULL,
              agency_code TEXT NOT NULL,
              agency_name TEXT NOT NULL,
              object_code TEXT NOT NULL,
              category TEXT NOT NULL,
              subobject_code TEXT NOT NULL,
              subcategory TEXT NOT NULL,
              vendor_name TEXT NOT NULL,
              amount REAL NOT NULL
            );
            CREATE TABLE refresh_runs (
              run_id TEXT PRIMARY KEY,
              started_at TEXT NOT NULL,
              finished_at TEXT NOT NULL,
              status TEXT NOT NULL,
              message TEXT NOT NULL
            );
            CREATE INDEX idx_payments_biennium ON payments (biennium);
            CREATE INDEX idx_payments_period ON payments (fiscal_year, fiscal_month);
            CREATE INDEX idx_payments_month ON payments (calendar_month);
            CREATE INDEX idx_payments_agency ON payments (agency_code, agency_name);
            CREATE INDEX idx_payments_category ON payments (category, subcategory);
            CREATE INDEX idx_payments_vendor ON payments (vendor_name);
            """
        )
        conn.execute(
            """
            INSERT INTO source_files (
              source_surface_id, biennium, url, fetched_at, last_modified,
              content_length, sha256, row_count, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "surface_a",
                "2025-27",
                "https://example.test/current.xlsx",
                "2026-06-05T00:00:00+00:00",
                "Tue, 26 May 2026 23:51:24 GMT",
                123,
                "a" * 64,
                1,
                "accepted",
            ),
        )
        conn.execute(
            """
            INSERT INTO payments (
              biennium, fiscal_year, fiscal_month, calendar_month, agency_code,
              agency_name, object_code, category, subobject_code, subcategory,
              vendor_name, amount
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "2025-27",
                2026,
                10,
                "2026-04",
                "100",
                "Agency A",
                "C",
                "Goods and Services",
                "01",
                "Office Supplies",
                "Vendor A",
                100.0,
            ),
        )
        conn.execute(
            """
            INSERT INTO refresh_runs (run_id, started_at, finished_at, status, message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "run-1",
                "2026-06-05T00:00:00+00:00",
                "2026-06-05T00:00:01+00:00",
                "current",
                "fixture",
            ),
        )
        conn.commit()


def create_incomplete_checkbook_fixture_db(path):
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            """
            CREATE TABLE refresh_runs (
              run_id TEXT PRIMARY KEY,
              started_at TEXT,
              finished_at TEXT,
              status TEXT,
              message TEXT
            )
            """
        )
        conn.commit()


def check_names(result):
    return {check["name"] for check in result["checks"]}


if __name__ == "__main__":
    unittest.main()
