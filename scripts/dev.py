#!/usr/bin/env python3
"""Agent-run Civic Agent development helpers.

This script is intentionally boring automation behind an agent-facing skill.
Humans should normally ask the maintainer skill to refresh or inspect dev state;
the skill runs this script and relays the result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import package_plugin


ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = ROOT / ".generated" / "civic-agent-dev-marketplace"
DEV_MARKETPLACE_NAME = "civic-agent-dev"
DEV_PLUGIN_NAME = "civic-agent-dev"
DEV_SKILL_NAME = "civic-agent-dev"
DEV_PLUGIN_ROOT = GENERATED_ROOT / "plugins" / DEV_PLUGIN_NAME
DEV_MANIFEST_PATH = DEV_PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
GENERATED_HEADER = "<!-- Generated local development package. Do not edit or commit. -->\n\n"


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Civic Agent development workflow helpers.")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("install", help="Generate and install @civic-agent-dev locally.")
    subcommands.add_parser("status", help="Report canonical, packaged, and installed plugin state.")
    subcommands.add_parser("verify", help="Verify package and installed dev plugin freshness.")
    subcommands.add_parser("smoke", help="Verify dev install and print smoke-test prompts.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "install":
        install_dev_plugin()
    elif args.command == "status":
        print_status()
    elif args.command == "verify":
        verify_or_exit()
    elif args.command == "smoke":
        smoke()


def install_dev_plugin() -> None:
    print("Refreshing production package from canonical jurisdiction files...", flush=True)
    planned = package_plugin.collect_outputs(update_cachebuster=False)
    package_plugin.remove_stale_outputs(planned)
    package_plugin.write_outputs(planned)

    failures = package_plugin.package_check_failures(package_plugin.collect_outputs(update_cachebuster=False))
    if failures:
        print("Production package verification failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    version = generate_dev_package()
    ensure_dev_marketplace_configured()
    run(["codex", "plugin", "add", f"{DEV_PLUGIN_NAME}@{DEV_MARKETPLACE_NAME}"])

    installed = verify_installed_cache(
        marketplace=DEV_MARKETPLACE_NAME,
        plugin=DEV_PLUGIN_NAME,
        skill=DEV_SKILL_NAME,
        expected_version=version,
    )
    print_check(installed)
    if not installed.ok:
        raise SystemExit(1)

    print()
    print("@civic-agent-dev is installed from the current local checkout.")
    print("Open a new Codex thread before testing it, then invoke @civic-agent-dev explicitly.")


def print_status() -> None:
    print("Civic Agent development status")
    print()
    print(f"Branch: {git_output(['branch', '--show-current']) or 'unknown'}")
    print(f"Commit: {git_output(['rev-parse', '--short', 'HEAD']) or 'unknown'}")
    dirty = git_output(["status", "--short"])
    print(f"Working tree: {'dirty' if dirty else 'clean'}")
    if dirty:
        for line in dirty.splitlines():
            print(f"  {line}")
    print()

    jurisdictions = canonical_jurisdiction_names()
    print(f"Canonical jurisdictions: {', '.join(jurisdictions) if jurisdictions else '(none)'}")
    print()

    package_result = verify_production_package()
    print_check(package_result)

    generated_result = verify_generated_dev_package()
    print_check(generated_result)

    production_installed = verify_installed_cache(
        marketplace="civic-agent",
        plugin="civic-agent",
        skill="civic-agent",
        expected_version=None,
    )
    print_check(production_installed)

    dev_installed = verify_installed_cache(
        marketplace=DEV_MARKETPLACE_NAME,
        plugin=DEV_PLUGIN_NAME,
        skill=DEV_SKILL_NAME,
        expected_version=dev_manifest_version(),
    )
    print_check(dev_installed)


def verify_or_exit() -> None:
    checks = [
        verify_production_package(),
        verify_generated_dev_package(),
        verify_installed_cache(
            marketplace=DEV_MARKETPLACE_NAME,
            plugin=DEV_PLUGIN_NAME,
            skill=DEV_SKILL_NAME,
            expected_version=dev_manifest_version(),
        ),
    ]
    for check in checks:
        print_check(check)
    if not all(check.ok for check in checks):
        raise SystemExit(1)


def smoke() -> None:
    check = verify_installed_cache(
        marketplace=DEV_MARKETPLACE_NAME,
        plugin=DEV_PLUGIN_NAME,
        skill=DEV_SKILL_NAME,
        expected_version=dev_manifest_version(),
    )
    print_check(check)
    if not check.ok:
        raise SystemExit(1)

    print()
    print("Open a new Codex thread and run one or more smoke prompts:")
    print("- @civic-agent-dev Where does Seattle spend the most money in FY2026?")
    print("- @civic-agent-dev What are King County's largest FY2026 department expenditures?")
    print("- @civic-agent-dev What are Washington state's largest 2025-27 enacted operating budget agencies?")


def generate_dev_package(generated_root: Path = GENERATED_ROOT, *, quiet: bool = False) -> str:
    if generated_root.exists():
        shutil.rmtree(generated_root)

    dev_plugin_root = generated_root / "plugins" / DEV_PLUGIN_NAME
    dev_skill_root = dev_plugin_root / "skills" / DEV_SKILL_NAME

    write_json(
        generated_root / ".agents" / "plugins" / "marketplace.json",
        dev_marketplace_manifest(),
    )

    version = dev_version()
    write_json(dev_plugin_root / ".codex-plugin" / "plugin.json", dev_manifest(version))
    write_text(dev_skill_root / "SKILL.md", dev_skill_content())
    write_text(dev_skill_root / "agents" / "openai.yaml", dev_agent_metadata())

    icon_path = package_plugin.PLUGIN_ROOT / "assets" / "icon.png"
    if icon_path.is_file():
        target_icon = dev_plugin_root / "assets" / "icon.png"
        target_icon.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(icon_path, target_icon)

    references_root = dev_skill_root / "references"
    for jurisdiction, skill_path in package_plugin.jurisdiction_skill_paths():
        write_text(
            references_root / f"{jurisdiction}.md",
            skill_path.read_text(encoding="utf-8"),
        )

    write_json(dev_plugin_root / "build-info.json", build_info(version))
    if not quiet:
        print(
            f"Generated {DEV_PLUGIN_NAME} package at {relative_display(dev_plugin_root)}.",
            flush=True,
        )
    return version


def verify_production_package() -> CheckResult:
    failures = package_plugin.package_check_failures(
        package_plugin.collect_outputs(update_cachebuster=False)
    )
    return CheckResult(
        name="Production package",
        ok=not failures,
        details=failures or ["plugins/civic-agent is current."],
    )


def verify_generated_dev_package(generated_root: Path = GENERATED_ROOT) -> CheckResult:
    dev_plugin_root = generated_root / "plugins" / DEV_PLUGIN_NAME
    dev_skill_root = dev_plugin_root / "skills" / DEV_SKILL_NAME
    failures: list[str] = []

    manifest_path = dev_plugin_root / ".codex-plugin" / "plugin.json"
    marketplace_path = generated_root / ".agents" / "plugins" / "marketplace.json"
    skill_path = dev_skill_root / "SKILL.md"

    if not marketplace_path.is_file():
        failures.append(f"{relative_display(marketplace_path)} is missing.")
    elif read_json(marketplace_path).get("name") != DEV_MARKETPLACE_NAME:
        failures.append(f"{relative_display(marketplace_path)} has the wrong marketplace name.")

    if not manifest_path.is_file():
        failures.append(f"{relative_display(manifest_path)} is missing.")
    else:
        manifest = read_json(manifest_path)
        if manifest.get("name") != DEV_PLUGIN_NAME:
            failures.append(f"{relative_display(manifest_path)} has the wrong plugin name.")

    if not skill_path.is_file():
        failures.append(f"{relative_display(skill_path)} is missing.")
    else:
        skill_text = skill_path.read_text(encoding="utf-8")
        if not re.search(r"^name: civic-agent-dev$", skill_text, re.MULTILINE):
            failures.append(f"{relative_display(skill_path)} has the wrong skill name.")
        if "/civic-agent-dev" not in skill_text:
            failures.append(f"{relative_display(skill_path)} does not mention /civic-agent-dev.")

    for jurisdiction, canonical_skill_path in package_plugin.jurisdiction_skill_paths():
        reference_path = dev_skill_root / "references" / f"{jurisdiction}.md"
        if not reference_path.is_file():
            failures.append(f"{relative_display(reference_path)} is missing.")
            continue
        if sha256_file(reference_path) != sha256_file(canonical_skill_path):
            failures.append(f"{relative_display(reference_path)} does not match canonical skill.")
    failures.extend(stale_reference_failures(dev_skill_root / "references"))

    if not (dev_plugin_root / "build-info.json").is_file():
        failures.append(f"{relative_display(dev_plugin_root / 'build-info.json')} is missing.")

    return CheckResult(
        name="Generated dev package",
        ok=not failures,
        details=failures or [f"{relative_display(dev_plugin_root)} matches canonical sources."],
    )


def verify_installed_cache(
    *,
    marketplace: str,
    plugin: str,
    skill: str,
    expected_version: str | None,
) -> CheckResult:
    cache_root = Path.home() / ".codex" / "plugins" / "cache" / marketplace / plugin
    if not cache_root.is_dir():
        return CheckResult(
            name=f"Installed {plugin}@{marketplace}",
            ok=False,
            details=[f"{cache_root} does not exist."],
        )

    install_root = installed_version_root(cache_root, expected_version)
    if install_root is None:
        expected = expected_version or "any installed version"
        return CheckResult(
            name=f"Installed {plugin}@{marketplace}",
            ok=False,
            details=[f"No installed cache entry matched {expected} under {cache_root}."],
        )

    failures: list[str] = []
    manifest_path = install_root / ".codex-plugin" / "plugin.json"
    skill_path = install_root / "skills" / skill / "SKILL.md"
    if not manifest_path.is_file():
        failures.append(f"{manifest_path} is missing.")
    if not skill_path.is_file():
        failures.append(f"{skill_path} is missing.")

    for jurisdiction, canonical_skill_path in package_plugin.jurisdiction_skill_paths():
        reference_path = install_root / "skills" / skill / "references" / f"{jurisdiction}.md"
        if not reference_path.is_file():
            failures.append(f"{reference_path} is missing.")
            continue
        if sha256_file(reference_path) != sha256_file(canonical_skill_path):
            failures.append(f"{reference_path} does not match {canonical_skill_path.relative_to(ROOT)}.")
    failures.extend(stale_reference_failures(install_root / "skills" / skill / "references"))

    details = failures or [f"{install_root} matches canonical jurisdiction references."]
    return CheckResult(
        name=f"Installed {plugin}@{marketplace}",
        ok=not failures,
        details=details,
    )


def installed_version_root(cache_root: Path, expected_version: str | None) -> Path | None:
    candidates = [path for path in cache_root.iterdir() if path.is_dir()]
    if expected_version:
        exact = cache_root / expected_version
        if exact.is_dir():
            return exact
        return None
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def ensure_dev_marketplace_configured() -> None:
    configured = marketplace_roots()
    generated_root = str(GENERATED_ROOT.resolve())
    if configured.get(DEV_MARKETPLACE_NAME) == generated_root:
        return
    if DEV_MARKETPLACE_NAME in configured:
        raise SystemExit(
            f"Marketplace {DEV_MARKETPLACE_NAME} already points at "
            f"{configured[DEV_MARKETPLACE_NAME]}, not {generated_root}."
        )
    run(["codex", "plugin", "marketplace", "add", generated_root])


def marketplace_roots() -> dict[str, str]:
    result = run(["codex", "plugin", "marketplace", "list"], capture=True)
    roots: dict[str, str] = {}
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            roots[parts[0]] = parts[-1]
    return roots


def dev_marketplace_manifest() -> dict[str, object]:
    return {
        "name": DEV_MARKETPLACE_NAME,
        "interface": {"displayName": "Civic Agent Dev"},
        "plugins": [
            {
                "name": DEV_PLUGIN_NAME,
                "source": {
                    "source": "local",
                    "path": f"./plugins/{DEV_PLUGIN_NAME}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Analytics",
            }
        ],
    }


def dev_manifest(version: str) -> dict[str, object]:
    manifest = json.loads(package_plugin.MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["name"] = DEV_PLUGIN_NAME
    manifest["version"] = version
    manifest["description"] = "Local development build of Civic Agent from the current checkout."
    manifest["keywords"] = sorted(set(manifest.get("keywords", [])) | {"dev", "local"})
    interface = dict(manifest["interface"])
    interface.update(
        {
            "displayName": "Civic Agent Dev",
            "shortDescription": "Test the local Civic Agent checkout",
            "longDescription": (
                "Local development build of Civic Agent generated from this checkout. "
                "Use it explicitly while developing sources and routing behavior."
            ),
            "defaultPrompt": [
                "Test local Civic Agent",
                "Analyze Seattle budget with civic-agent-dev",
                "Analyze King County budget with civic-agent-dev",
                "Analyze Washington state budget with civic-agent-dev",
            ],
        }
    )
    manifest["interface"] = interface
    return manifest


def dev_skill_content() -> str:
    content = package_plugin.SOURCE_ROUTER.read_text(encoding="utf-8")
    content = re.sub(r"^name: civic-agent$", f"name: {DEV_SKILL_NAME}", content, count=1, flags=re.MULTILINE)
    content = re.sub(
        r"^description: .+$",
        (
            "description: Use only when explicitly invoked as the local development "
            "Civic Agent build for testing plugin packaging, source routing, or "
            "jurisdiction changes from the current checkout."
        ),
        content,
        count=1,
        flags=re.MULTILINE,
    )
    content = content.replace("# Civic Agent\n", "# Civic Agent Dev\n", 1)
    content = content.replace("/civic-agent", "/civic-agent-dev")
    match = re.match(r"(---\n.*?\n---\n)(.*)", content, flags=re.DOTALL)
    if match is None:
        raise ValueError("router skill is missing frontmatter")
    return (
        match.group(1)
        + "\n"
        + GENERATED_HEADER
        + "This generated skill is for local development tests only. Generic civic "
        "budget questions should use the production `@civic-agent` install unless "
        "the user explicitly asks for the dev build.\n\n"
        + match.group(2)
    )


def dev_agent_metadata() -> str:
    return """interface:
  display_name: "Civic Agent Dev"
  short_description: "Test the local Civic Agent checkout"
  brand_color: "#0F766E"
  default_prompt: "Use $civic-agent-dev to test local Civic Agent source changes."
policy:
  allow_implicit_invocation: false
"""


def build_info(version: str) -> dict[str, object]:
    jurisdictions = {}
    for jurisdiction, skill_path in package_plugin.jurisdiction_skill_paths():
        jurisdictions[jurisdiction] = {
            "path": str(skill_path.relative_to(ROOT)),
            "sha256": sha256_file(skill_path),
        }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "source_branch": git_output(["branch", "--show-current"]),
        "source_commit": git_output(["rev-parse", "--short", "HEAD"]),
        "router_sha256": sha256_file(package_plugin.SOURCE_ROUTER),
        "jurisdictions": jurisdictions,
    }


def dev_version() -> str:
    manifest = json.loads(package_plugin.MANIFEST_PATH.read_text(encoding="utf-8"))
    base = package_plugin.strip_build_metadata(str(manifest["version"]))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"{base}-dev+codex.{stamp}"


def dev_manifest_version() -> str | None:
    if not DEV_MANIFEST_PATH.is_file():
        return None
    return str(read_json(DEV_MANIFEST_PATH).get("version"))


def canonical_jurisdiction_names() -> list[str]:
    return [jurisdiction for jurisdiction, _ in package_plugin.jurisdiction_skill_paths()]


def stale_reference_failures(references_root: Path) -> list[str]:
    if not references_root.is_dir():
        return []
    expected = {f"{jurisdiction}.md" for jurisdiction in canonical_jurisdiction_names()}
    return [
        f"{path} is a stale generated reference."
        for path in sorted(references_root.glob("*.md"))
        if path.name not in expected
    ]


def run(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=capture,
    )


def git_output(args: list[str]) -> str:
    try:
        result = run(["git", *args], capture=True)
    except subprocess.CalledProcessError:
        return ""
    return result.stdout.strip()


def read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, object]) -> None:
    write_text(path, json.dumps(value, indent=2) + "\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def print_check(check: CheckResult) -> None:
    status = "ok" if check.ok else "needs attention"
    print(f"{check.name}: {status}")
    for detail in check.details:
        print(f"  - {detail}")
    print()


if __name__ == "__main__":
    main()
