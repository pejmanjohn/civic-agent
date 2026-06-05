import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "jurisdictions"

EXPECTED_POLICY_TIERS = {
    "seattle.operating_budget": "live",
    "king_county.open_budget_dashboard": "checked_in_snapshot",
    "washington.operating_budget": "checked_in_snapshot",
    "washington.revenue_by_biennium": "checked_in_snapshot",
    "washington.open_checkbook": "managed_local_db",
}
ALLOWED_TIERS = {
    "live",
    "checked_in_snapshot",
    "managed_local_db",
    "hosted_artifact",
    "context_only",
    "watchlist",
    "reject",
}
ALLOWED_NORMAL_ANSWER_SOURCES = {
    "official_api",
    "repo_snapshot",
    "local_db",
    "hosted_artifact",
    "none",
}
ALLOWED_FRESHNESS_CHECKS = {
    "api_metadata",
    "source_file_metadata",
    "model_refresh",
    "report_timestamp",
    "manual_snapshot_version",
    "custom_probe",
    "none",
}
ALLOWED_REPO_ARTIFACTS = {
    "source_card",
    "probe",
    "query_templates",
    "normalized_snapshot",
    "summary",
    "provenance",
    "builder",
    "tests",
    "fixtures",
    "docs",
    "query_recipes",
  }
ALLOWED_LOCAL_ARTIFACTS = {
    "raw_source_file",
    "local_database",
    "manifest",
    "debug_capture",
}


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def source_cards():
    return [load_json(path) for path in sorted(SOURCE_ROOT.glob("*/sources/*.source.json"))]


class SourceStoragePolicyTest(unittest.TestCase):
    def test_current_source_cards_declare_expected_storage_tiers(self):
        cards_by_id = {source["id"]: source for source in source_cards()}
        for source_id, expected_tier in EXPECTED_POLICY_TIERS.items():
            self.assertIn(source_id, cards_by_id)
            self.assertEqual(cards_by_id[source_id]["storage_policy"]["tier"], expected_tier)

    def test_storage_policy_values_use_known_vocabulary(self):
        for source in source_cards():
            policy = source.get("storage_policy")
            if not policy:
                continue
            self.assertIn(policy["tier"], ALLOWED_TIERS, source["id"])
            self.assertIn(
                policy["normal_answer_source"],
                ALLOWED_NORMAL_ANSWER_SOURCES,
                source["id"],
            )
            self.assertIn(policy["freshness_check"], ALLOWED_FRESHNESS_CHECKS, source["id"])
            self.assertIsInstance(policy.get("repo_artifacts"), list, source["id"])
            self.assertIsInstance(policy.get("local_artifacts"), list, source["id"])
            self.assertIsInstance(policy.get("refresh_behavior"), str, source["id"])
            self.assertTrue(policy["refresh_behavior"].strip(), source["id"])
            for artifact in policy["repo_artifacts"]:
                self.assertIn(artifact, ALLOWED_REPO_ARTIFACTS, source["id"])
            for artifact in policy["local_artifacts"]:
                self.assertIn(artifact, ALLOWED_LOCAL_ARTIFACTS, source["id"])

    def test_storage_policy_tier_matches_normal_answer_source(self):
        expected_normal_answer_source = {
            "live": "official_api",
            "checked_in_snapshot": "repo_snapshot",
            "managed_local_db": "local_db",
            "hosted_artifact": "hosted_artifact",
            "context_only": "none",
            "watchlist": "none",
            "reject": "none",
        }
        for source in source_cards():
            policy = source.get("storage_policy")
            if not policy:
                continue
            self.assertEqual(
                policy["normal_answer_source"],
                expected_normal_answer_source[policy["tier"]],
                source["id"],
            )

    def test_managed_local_db_policy_names_freshness_and_local_artifacts(self):
        for source in source_cards():
            policy = source.get("storage_policy")
            if not policy or policy["tier"] != "managed_local_db":
                continue
            self.assertNotEqual(policy["freshness_check"], "none", source["id"])
            self.assertIn("local_database", policy["local_artifacts"], source["id"])
            self.assertTrue(
                {"raw_source_file", "manifest"}.issubset(policy["local_artifacts"]),
                source["id"],
            )

    def test_accepted_source_cards_expose_common_source_fingerprint(self):
        required_keys = {
            "public_inspection_urls",
            "machine_access",
            "retrieval_context",
            "version_boundary",
            "row_counts",
            "checks",
        }
        for source in source_cards():
            if source["id"] not in EXPECTED_POLICY_TIERS:
                continue
            fingerprint = source.get("source_fingerprint")
            self.assertIsInstance(fingerprint, dict, source["id"])
            self.assertTrue(required_keys.issubset(fingerprint), source["id"])
            self.assertTrue(fingerprint["public_inspection_urls"], source["id"])
            self.assertIsInstance(fingerprint["machine_access"], dict, source["id"])
            self.assertIsInstance(fingerprint["retrieval_context"], dict, source["id"])
            self.assertIsInstance(fingerprint["version_boundary"], dict, source["id"])
            self.assertIsInstance(fingerprint["row_counts"], dict, source["id"])
            self.assertIsInstance(fingerprint["checks"], dict, source["id"])

    def test_current_stored_artifacts_expose_source_fingerprint(self):
        artifact_dirs = [
            SOURCE_ROOT / "king_county" / "data" / "open-budget-dashboard" / "2026-04-01",
            SOURCE_ROOT
            / "washington"
            / "data"
            / "operating-budget"
            / "2025-27-enacted-2025-05-20",
            SOURCE_ROOT
            / "washington"
            / "data"
            / "revenue-by-biennium"
            / "2025-27-revenue-through-2026-04",
        ]
        for artifact_dir in artifact_dirs:
            summary = load_json(artifact_dir / "summary.json")
            provenance = load_json(artifact_dir / "provenance.json")
            for artifact in (summary, provenance):
                fingerprint = artifact.get("source_fingerprint")
                self.assertIsInstance(fingerprint, dict, artifact_dir.as_posix())
                self.assertEqual(fingerprint["row_counts"], summary["row_counts"])
                self.assertIn("checks", fingerprint)
                self.assertIn("public_inspection_urls", fingerprint)


if __name__ == "__main__":
    unittest.main()
