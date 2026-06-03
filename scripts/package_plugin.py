#!/usr/bin/env python3
"""Refresh the checked-in Codex and Claude Code plugin packages from canonical source files."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "civic-agent"
PLUGIN_SKILL_ROOT = PLUGIN_ROOT / "skills" / "civic-agent"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
CLAUDE_MANIFEST_PATH = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
SOURCE_ROUTER = ROOT / "skills" / "civic-agent" / "SKILL.md"
SOURCE_AGENT = ROOT / "skills" / "civic-agent" / "agents" / "openai.yaml"
JURISDICTIONS_ROOT = ROOT / "jurisdictions"
SEMVER_WITH_BUILD_RE = re.compile(r"^([^+]+)(?:\+.*)?$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package the Civic Agent Codex plugin.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated files are current without writing changes.",
    )
    parser.add_argument(
        "--update-cachebuster",
        action="store_true",
        help="Update plugin.json version build metadata for local Codex reinstall.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    planned = collect_outputs(update_cachebuster=args.update_cachebuster)
    if args.check:
        failures = [
            str(path.relative_to(ROOT))
            for path, content in planned.items()
            if read_text(path) != content
        ]
        if failures:
            print("Plugin package is out of date:")
            for failure in failures:
                print(f"- {failure}")
            raise SystemExit(1)
        print("Plugin package is current.")
        return
    write_outputs(planned)
    print("Packaged Civic Agent plugin.")


def collect_outputs(*, update_cachebuster: bool) -> dict[Path, str]:
    outputs: dict[Path, str] = {
        PLUGIN_SKILL_ROOT / "SKILL.md": SOURCE_ROUTER.read_text(encoding="utf-8"),
        PLUGIN_SKILL_ROOT / "agents" / "openai.yaml": SOURCE_AGENT.read_text(encoding="utf-8"),
        CLAUDE_MANIFEST_PATH: claude_manifest_content(),
    }
    references_root = PLUGIN_SKILL_ROOT / "references"
    for jurisdiction_dir in sorted(JURISDICTIONS_ROOT.iterdir()):
        if not jurisdiction_dir.is_dir() or jurisdiction_dir.name.startswith("."):
            continue
        skill_path = jurisdiction_dir / "skill.md"
        if not skill_path.is_file():
            continue
        outputs[references_root / f"{jurisdiction_dir.name}.md"] = skill_path.read_text(
            encoding="utf-8"
        )
    if update_cachebuster:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["version"] = cachebusted_version(str(manifest["version"]))
        outputs[MANIFEST_PATH] = json.dumps(manifest, indent=2) + "\n"
    return outputs


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def strip_build_metadata(version: str) -> str:
    match = SEMVER_WITH_BUILD_RE.match(version)
    if match is None:
        raise ValueError(f"unsupported plugin version: {version}")
    return match.group(1)


def claude_manifest_content() -> str:
    """Generate the Claude Code plugin manifest from the canonical Codex manifest.

    The Codex manifest is the hand-authored source of truth for shared metadata.
    The generated Claude manifest drops the Codex-only ``interface`` block and the
    ``skills`` path (Claude Code auto-discovers ``skills/<name>/SKILL.md``), and
    carries the plain base semver with no ``+codex.<stamp>`` build suffix.
    """
    codex = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest = {
        "name": codex["name"],
        "description": codex["description"],
        "version": strip_build_metadata(str(codex["version"])),
        "author": codex["author"],
        "homepage": codex["homepage"],
        "repository": codex["repository"],
        "license": codex["license"],
        "keywords": codex["keywords"],
    }
    return json.dumps(manifest, indent=2) + "\n"


def cachebusted_version(version: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{strip_build_metadata(version)}+codex.{stamp}"


if __name__ == "__main__":
    main()
