import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "civic-agent"
CLAUDE_MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
SOURCE_ROOT = ROOT / "jurisdictions"

CANONICAL_SKILL_PATHS = [
    ROOT / "skill.md",
    ROOT / "skills" / "civic-agent" / "SKILL.md",
]

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt"}

# Machine-local absolute path prefixes that must never ship in skills or the
# packaged plugin. Repo paths in shipped text must be repo-relative.
FORBIDDEN_PATH_PREFIXES = ("/Users/", "/home/", "C:\\Users\\")


def shipped_text_files():
    files = [path for path in CANONICAL_SKILL_PATHS if path.is_file()]
    files.extend(sorted(SOURCE_ROOT.glob("*/skill.md")))
    files.extend(
        path
        for path in sorted(PLUGIN_ROOT.rglob("*"))
        if path.is_file() and path.suffix in TEXT_SUFFIXES
    )
    return files


def jurisdiction_slugs():
    return sorted(
        path.name for path in SOURCE_ROOT.iterdir() if (path / "skill.md").is_file()
    )


class PackagingHygieneTest(unittest.TestCase):
    def test_no_machine_local_absolute_paths_ship(self):
        offenders = []
        for path in shipped_text_files():
            text = path.read_text(encoding="utf-8")
            for prefix in FORBIDDEN_PATH_PREFIXES:
                if prefix in text:
                    offenders.append(f"{path.relative_to(ROOT)} contains {prefix!r}")
        self.assertEqual(offenders, [])

    def test_marketplace_keywords_cover_every_jurisdiction(self):
        marketplace = json.loads(CLAUDE_MARKETPLACE_PATH.read_text(encoding="utf-8"))
        keywords = set()
        for plugin in marketplace.get("plugins", []):
            keywords.update(plugin.get("keywords", []))
        missing = []
        for slug in jurisdiction_slugs():
            keyword = slug.replace("_", "-")
            if keyword not in keywords:
                missing.append(keyword)
        self.assertEqual(
            missing,
            [],
            f"marketplace keywords missing jurisdiction slugs: {missing}; "
            f"update .claude-plugin/marketplace.json when adding a jurisdiction",
        )

    def test_every_jurisdiction_is_routed_in_both_routers(self):
        # Closes brainstorm R13: router/source registry drift must be visible.
        # The root router is hand-maintained prose, so assert the durable
        # invariant - each jurisdiction's canonical skill URL is routed.
        root_router = (ROOT / "skill.md").read_text(encoding="utf-8")
        installable = (ROOT / "skills" / "civic-agent" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        missing = []
        for slug in jurisdiction_slugs():
            skill_url = (
                "https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/"
                f"jurisdictions/{slug}/skill.md"
            )
            if skill_url not in root_router:
                missing.append(f"skill.md missing route for {slug}")
            if skill_url not in installable:
                missing.append(f"skills/civic-agent/SKILL.md missing route for {slug}")
        self.assertEqual(missing, [])

    def test_shipped_file_scan_actually_covers_the_plugin(self):
        files = shipped_text_files()
        self.assertTrue(
            any(PLUGIN_ROOT in path.parents for path in files),
            "plugin files missing from the hygiene scan",
        )
        self.assertTrue(
            any(path.name == "skill.md" and SOURCE_ROOT in path.parents for path in files),
            "jurisdiction skills missing from the hygiene scan",
        )


if __name__ == "__main__":
    unittest.main()
