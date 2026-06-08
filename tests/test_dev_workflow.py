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
            self.assertIn(str(ROOT), skill)
            self.assertIn("Do not inspect the production `@civic-agent` cache", skill)
            self.assertIn("jurisdictions/<jurisdiction>/skill.md", skill)
            self.assertNotIn("raw.githubusercontent.com/pejmanjohn/civic-agent-dev", skill)

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

    def test_washington_checkbook_route_is_documented_for_packaging(self):
        washington_skill = (ROOT / "jurisdictions" / "washington" / "skill.md").read_text(
            encoding="utf-8"
        )
        router = (ROOT / "skills" / "civic-agent" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("washington.open_checkbook", washington_skill)
        self.assertIn("washington.ofm_population", washington_skill)
        self.assertIn(
            "python3 scripts/source_data.py --json ensure washington.open_checkbook",
            washington_skill,
        )
        self.assertIn("Open Checkbook answers use actual vendor-payment language", router)
        self.assertIn("OFM population-denominator questions", router)
        self.assertIn("Washington OFM population estimates", router)
        self.assertIn("OFM population answers use resident population denominator language", router)
        self.assertIn("managed local database", router)

    def test_scale_recipe_guidance_is_packaged_with_router_and_references(self):
        recipe_doc = (ROOT / "docs" / "recipes" / "scale.md").read_text(
            encoding="utf-8"
        )
        recipe_ids = [
            "budget_scale.current_total",
            "budget_scale.trend",
            "budget_scale.per_capita",
            "budget_scale.cross_jurisdiction",
        ]
        answer_modes = [
            "exact",
            "partial",
            "side_by_side_only",
            "unsupported_with_path",
            "needs_refresh",
        ]

        for recipe_id in recipe_ids:
            self.assertIn(recipe_id, recipe_doc)
        self.assertIn(
            "If no accepted denominator source exists, return `unsupported_with_path`",
            recipe_doc,
        )
        self.assertIn(
            "compatible units, period types, amount basis, budget frames, "
            "government scopes, and geography bases",
            recipe_doc,
        )
        self.assertIn("washington.ofm_population", recipe_doc)

        router_paths = [
            ROOT / "skill.md",
            ROOT / "skills" / "civic-agent" / "SKILL.md",
        ]
        for router_path in router_paths:
            router = router_path.read_text(encoding="utf-8")
            self.assertIn("Scale Recipes And Answer Modes", router)
            self.assertIn(
                "question -> recipe -> required claims -> available sources -> "
                "compatibility check -> answer mode",
                router,
            )
            for recipe_id in recipe_ids:
                self.assertIn(recipe_id, router)
            for answer_mode in answer_modes:
                self.assertIn(answer_mode, router)

        planned = package_plugin.collect_outputs(update_cachebuster=False)
        packaged_router = planned[
            package_plugin.PLUGIN_SKILL_ROOT / "SKILL.md"
        ]
        for recipe_id in recipe_ids:
            self.assertIn(recipe_id, packaged_router)
        for answer_mode in answer_modes:
            self.assertIn(answer_mode, packaged_router)
        self.assertIn("washington.ofm_population", packaged_router)

        expected_reference_fragments = {
            "seattle.md": "compose this source with `washington.ofm_population`",
            "king_county.md": "king_county.adopted_budget",
            "washington.md": "Seattle 816,600 and King County 2,411,700",
        }
        for reference_name, fragment in expected_reference_fragments.items():
            reference = planned[
                package_plugin.references_root_path() / reference_name
            ]
            self.assertIn("For composed Scale questions", reference)
            self.assertIn(fragment, reference)


if __name__ == "__main__":
    unittest.main()
