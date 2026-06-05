import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "source_data.py"


spec = importlib.util.spec_from_file_location("civic_source_data", SCRIPT_PATH)
source_data = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = source_data
spec.loader.exec_module(source_data)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class SourceDataTest(unittest.TestCase):
    def tearDown(self):
        source_data.BUILDER_REGISTRY.clear()
        source_data.QUERY_REGISTRY.clear()

    def test_inspect_reports_storage_policy_and_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = source_data.parse_args(
                ["--data-home", tmp, "inspect", "seattle.operating_budget"]
            )
            result = source_data.run_command(args)
            self.assertTrue(result["ok"])
            self.assertEqual(result["source_id"], "seattle.operating_budget")
            self.assertEqual(result["storage_policy"]["tier"], "live")
            self.assertEqual(result["data_home"], tmp)
            self.assertEqual(
                result["source_dir"],
                str(Path(tmp) / "sources" / "seattle" / "operating_budget"),
            )

    def test_status_returns_missing_when_manifest_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = source_data.parse_args(
                ["--data-home", tmp, "status", "seattle.operating_budget"]
            )
            result = source_data.run_command(args)
            self.assertEqual(result["status"], "missing")
            self.assertEqual(result["storage_tier"], "live")
            self.assertIn("manifest.json", result["manifest_path"])

    def test_ensure_non_managed_source_does_not_require_builder(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = source_data.parse_args(
                ["--data-home", tmp, "ensure", "seattle.operating_budget"]
            )
            result = source_data.run_command(args)
            self.assertEqual(result["status"], "not_managed")
            self.assertEqual(result["storage_tier"], "live")

    def test_ensure_managed_source_writes_manifest_via_registered_builder(self):
        source = {
            "id": "example.source",
            "storage_policy": {
                "tier": "managed_local_db",
                "normal_answer_source": "local_db",
            },
        }

        def fake_load_source_card(source_id):
            if source_id != "example.source":
                raise source_data.SourceDataError("wrong source")
            return {**source, "_path": "jurisdictions/example/sources/source.json"}

        def fake_builder(context, force):
            self.assertEqual(context.source_id, "example.source")
            self.assertFalse(force)
            return {
                "status": "current",
                "storage_tier": "managed_local_db",
                "normal_answer_source": "local_db",
                "row_count": 3,
            }

        original = source_data.load_source_card
        source_data.load_source_card = fake_load_source_card
        source_data.BUILDER_REGISTRY["example.source"] = fake_builder
        try:
            with tempfile.TemporaryDirectory() as tmp:
                args = source_data.parse_args(["--data-home", tmp, "ensure", "example.source"])
                result = source_data.run_command(args)
                manifest_path = (
                    Path(tmp) / "sources" / "example" / "source" / "manifest.json"
                )
                self.assertEqual(result["status"], "current")
                self.assertEqual(result["row_count"], 3)
                self.assertTrue(manifest_path.is_file())
                manifest = load_json(manifest_path)
                self.assertEqual(manifest["source_id"], "example.source")
                self.assertEqual(manifest["row_count"], 3)
        finally:
            source_data.load_source_card = original

    def test_status_reports_missing_when_managed_manifest_points_to_missing_database(self):
        source = {
            "id": "example.source",
            "storage_policy": {
                "tier": "managed_local_db",
                "normal_answer_source": "local_db",
            },
        }

        def fake_load_source_card(source_id):
            if source_id != "example.source":
                raise source_data.SourceDataError("wrong source")
            return {**source, "_path": "jurisdictions/example/sources/source.json"}

        original = source_data.load_source_card
        source_data.load_source_card = fake_load_source_card
        try:
            with tempfile.TemporaryDirectory() as tmp:
                manifest_path = (
                    Path(tmp) / "sources" / "example" / "source" / "manifest.json"
                )
                missing_db = Path(tmp) / "sources" / "example" / "source" / "missing.sqlite"
                manifest_path.parent.mkdir(parents=True)
                manifest_path.write_text(
                    json.dumps({"status": "current", "database_path": str(missing_db)}),
                    encoding="utf-8",
                )
                args = source_data.parse_args(["--data-home", tmp, "status", "example.source"])
                result = source_data.run_command(args)

                self.assertEqual(result["status"], "missing")
                self.assertIn("local database is missing", result["message"])
        finally:
            source_data.load_source_card = original

    def test_status_reports_stale_when_managed_manifest_metadata_differs(self):
        source = {
            "id": "example.source",
            "storage_policy": {
                "tier": "managed_local_db",
                "normal_answer_source": "local_db",
            },
            "source_surfaces": {
                "surface_a": {
                    "status": "accepted",
                    "url": "https://example.test/current.xlsx",
                    "last_modified": "Tue, 26 May 2026 23:51:24 GMT",
                    "content_length": 100,
                }
            },
        }

        def fake_load_source_card(source_id):
            if source_id != "example.source":
                raise source_data.SourceDataError("wrong source")
            return {**source, "_path": "jurisdictions/example/sources/source.json"}

        original = source_data.load_source_card
        source_data.load_source_card = fake_load_source_card
        try:
            with tempfile.TemporaryDirectory() as tmp:
                source_dir = Path(tmp) / "sources" / "example" / "source"
                database_path = source_dir / "current.sqlite"
                manifest_path = source_dir / "manifest.json"
                source_dir.mkdir(parents=True)
                database_path.write_text("", encoding="utf-8")
                manifest_path.write_text(
                    json.dumps(
                        {
                            "status": "current",
                            "database_path": str(database_path),
                            "source_files": [
                                {
                                    "source_surface_id": "surface_a",
                                    "url": "https://example.test/current.xlsx",
                                    "last_modified": "Mon, 01 Jan 2024 00:00:00 GMT",
                                    "content_length": 100,
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                args = source_data.parse_args(["--data-home", tmp, "status", "example.source"])
                result = source_data.run_command(args)

                self.assertEqual(result["status"], "stale")
                self.assertIn("last_modified", result["message"])
        finally:
            source_data.load_source_card = original

    def test_managed_source_stale_reason_detects_missing_accepted_surface(self):
        source = {
            "source_surfaces": {
                "surface_a": {
                    "status": "accepted",
                    "url": "https://example.test/a.xlsx",
                },
                "surface_b": {
                    "status": "rejected",
                    "url": "https://example.test/b.xlsx",
                },
            }
        }
        manifest = {"source_files": []}

        reason = source_data.managed_source_stale_reason(source, manifest)
        self.assertEqual(reason, "Local manifest is missing accepted source surface: surface_a")

    def test_parse_params_requires_key_value_shape(self):
        self.assertEqual(source_data.parse_params(["agency=300"]), {"agency": "300"})
        with self.assertRaises(source_data.SourceDataError):
            source_data.parse_params(["agency"])

    def test_data_home_uses_environment_override(self):
        old_value = os.environ.get("CIVIC_AGENT_DATA_HOME")
        try:
            os.environ["CIVIC_AGENT_DATA_HOME"] = "/tmp/civic-agent-test-home"
            self.assertEqual(
                source_data.data_home_from_env(),
                Path("/tmp/civic-agent-test-home"),
            )
        finally:
            if old_value is None:
                os.environ.pop("CIVIC_AGENT_DATA_HOME", None)
            else:
                os.environ["CIVIC_AGENT_DATA_HOME"] = old_value

    def test_unknown_source_id_fails_clearly(self):
        with self.assertRaises(source_data.SourceDataError):
            source_data.source_context("missing.source")


if __name__ == "__main__":
    unittest.main()
