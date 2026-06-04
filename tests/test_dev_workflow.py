import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEV_SCRIPT_PATH = ROOT / "scripts" / "dev.py"
PACKAGE_SCRIPT_PATH = ROOT / "scripts" / "package_plugin.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


dev = load_module("civic_agent_dev", DEV_SCRIPT_PATH)
package_plugin = load_module("civic_agent_package_plugin", PACKAGE_SCRIPT_PATH)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class DevWorkflowTest(unittest.TestCase):
    def test_generate_dev_package_uses_dev_identity_and_canonical_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            generated_root = Path(tmp) / "marketplace"
            version = dev.generate_dev_package(generated_root, quiet=True)

            marketplace = load_json(
                generated_root / ".agents" / "plugins" / "marketplace.json"
            )
            self.assertEqual(marketplace["name"], "civic-agent-dev")
            self.assertEqual(marketplace["plugins"][0]["name"], "civic-agent-dev")

            manifest = load_json(
                generated_root
                / "plugins"
                / "civic-agent-dev"
                / ".codex-plugin"
                / "plugin.json"
            )
            self.assertEqual(manifest["name"], "civic-agent-dev")
            self.assertEqual(manifest["version"], version)
            self.assertIn("-dev+codex.", version)
            self.assertEqual(manifest["interface"]["displayName"], "Civic Agent Dev")

            skill_path = (
                generated_root
                / "plugins"
                / "civic-agent-dev"
                / "skills"
                / "civic-agent-dev"
                / "SKILL.md"
            )
            skill = skill_path.read_text(encoding="utf-8")
            self.assertTrue(skill.startswith("---\nname: civic-agent-dev\n"))
            self.assertIn("/civic-agent-dev", skill)
            self.assertIn("Generated local development package", skill)

            agent_metadata = (
                generated_root
                / "plugins"
                / "civic-agent-dev"
                / "skills"
                / "civic-agent-dev"
                / "agents"
                / "openai.yaml"
            ).read_text(encoding="utf-8")
            self.assertIn('display_name: "Civic Agent Dev"', agent_metadata)
            self.assertIn("allow_implicit_invocation: false", agent_metadata)

            for jurisdiction, canonical_skill_path in package_plugin.jurisdiction_skill_paths():
                reference_path = (
                    generated_root
                    / "plugins"
                    / "civic-agent-dev"
                    / "skills"
                    / "civic-agent-dev"
                    / "references"
                    / f"{jurisdiction}.md"
                )
                self.assertTrue(reference_path.is_file())
                self.assertEqual(
                    reference_path.read_text(encoding="utf-8"),
                    canonical_skill_path.read_text(encoding="utf-8"),
                )

            build_info = load_json(
                generated_root / "plugins" / "civic-agent-dev" / "build-info.json"
            )
            self.assertEqual(build_info["version"], version)
            self.assertEqual(
                sorted(build_info["jurisdictions"].keys()),
                sorted(dev.canonical_jurisdiction_names()),
            )

            result = dev.verify_generated_dev_package(generated_root)
            self.assertTrue(result.ok, result.details)

    def test_verify_generated_dev_package_detects_reference_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            generated_root = Path(tmp) / "marketplace"
            dev.generate_dev_package(generated_root, quiet=True)
            seattle_reference = (
                generated_root
                / "plugins"
                / "civic-agent-dev"
                / "skills"
                / "civic-agent-dev"
                / "references"
                / "seattle.md"
            )
            seattle_reference.write_text("stale\n", encoding="utf-8")
            old_reference = seattle_reference.parent / "old_jurisdiction.md"
            old_reference.write_text("old\n", encoding="utf-8")

            result = dev.verify_generated_dev_package(generated_root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("seattle.md does not match canonical skill" in detail for detail in result.details)
            )
            self.assertTrue(
                any("old_jurisdiction.md" in detail for detail in result.details)
            )

    def test_package_outputs_cover_all_jurisdiction_references(self):
        planned = package_plugin.collect_outputs(update_cachebuster=False)
        planned_reference_names = {
            path.name
            for path in planned
            if path.parent == package_plugin.references_root_path()
        }
        expected_reference_names = {
            f"{jurisdiction}.md"
            for jurisdiction, _ in package_plugin.jurisdiction_skill_paths()
        }
        self.assertEqual(planned_reference_names, expected_reference_names)


if __name__ == "__main__":
    unittest.main()
