# Jurisdiction-First Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move all Seattle-specific source material into `jurisdictions/seattle/` and generate the packaged Codex plugin reference from that canonical location.

**Architecture:** `jurisdictions/<slug>/` becomes the canonical source tree for place-specific skills, source metadata, and data notes. `plugins/civic-agent/` remains checked-in package output for Codex and is refreshed by `scripts/package_plugin.py`. The script copies router files and jurisdiction skill references, supports a `--check` drift check, and has an explicit `--update-cachebuster` flag for local reinstall workflows.

**Tech Stack:** Python 3 standard library, Codex plugin manifest JSON, Markdown skill files, existing plugin-creator validation scripts.

---

### Task 1: Create Canonical Seattle Jurisdiction Tree

**Files:**
- Move: `skills/seattle/skill.md` -> `jurisdictions/seattle/skill.md`
- Move: `sources/seattle/operating-budget.source.json` -> `jurisdictions/seattle/sources/operating-budget.source.json`
- Move: `data/seattle/README.md` -> `jurisdictions/seattle/data/README.md`
- Delete: `skills/civic-agent/references/seattle.md`
- Create: `jurisdictions/seattle/README.md`

- [ ] **Step 1: Move existing files into the jurisdiction folder**

Run:

```bash
mkdir -p jurisdictions/seattle/sources jurisdictions/seattle/data
git mv skills/seattle/skill.md jurisdictions/seattle/skill.md
git mv sources/seattle/operating-budget.source.json jurisdictions/seattle/sources/operating-budget.source.json
git mv data/seattle/README.md jurisdictions/seattle/data/README.md
git rm skills/civic-agent/references/seattle.md
rmdir skills/seattle sources/seattle data/seattle skills/civic-agent/references
```

Expected: `jurisdictions/seattle/` contains `skill.md`, `sources/operating-budget.source.json`, and `data/README.md`.

- [ ] **Step 2: Add a Seattle overview file**

Create `jurisdictions/seattle/README.md`:

```markdown
# Seattle

City of Seattle operating budget support for Civic Agent.

## Files

- `skill.md`: Seattle budget analysis instructions and query recipes.
- `sources/operating-budget.source.json`: source metadata for the City of Seattle Operating Budget dataset.
- `data/README.md`: snapshot policy and live-data notes.

## Current Source

- Provider: Socrata / data.seattle.gov
- Dataset: City of Seattle Operating Budget
- Socrata ID: `8u2j-imqx`
- Known years: FY2018-FY2026
```

- [ ] **Step 3: Confirm no old source folders remain**

Run:

```bash
test ! -d skills/seattle
test ! -d skills/civic-agent/references
test ! -d sources/seattle
test ! -d data/seattle
find jurisdictions/seattle -maxdepth 3 -type f | sort
```

Expected output includes:

```text
jurisdictions/seattle/README.md
jurisdictions/seattle/data/README.md
jurisdictions/seattle/skill.md
jurisdictions/seattle/sources/operating-budget.source.json
```

### Task 2: Add Plugin Packaging Script

**Files:**
- Create: `scripts/package_plugin.py`
- Modify: `plugins/civic-agent/.codex-plugin/plugin.json`
- Modify: `plugins/civic-agent/skills/civic-agent/references/seattle.md`

- [ ] **Step 1: Create the packaging script**

Create `scripts/package_plugin.py`:

```python
#!/usr/bin/env python3
"""Refresh the checked-in Codex plugin package from canonical source files."""

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
SOURCE_ROUTER = ROOT / "skills" / "civic-agent" / "SKILL.md"
SOURCE_AGENT = ROOT / "skills" / "civic-agent" / "agents" / "openai.yaml"
JURISDICTIONS_ROOT = ROOT / "jurisdictions"
SEMVER_WITH_BUILD_RE = re.compile(r"^([^+]+)(?:\\+.*)?$")


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
        failures = [str(path.relative_to(ROOT)) for path, content in planned.items() if read_text(path) != content]
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
    }
    references_root = PLUGIN_SKILL_ROOT / "references"
    for jurisdiction_dir in sorted(JURISDICTIONS_ROOT.iterdir()):
        if not jurisdiction_dir.is_dir() or jurisdiction_dir.name.startswith("."):
            continue
        skill_path = jurisdiction_dir / "skill.md"
        if not skill_path.is_file():
            continue
        outputs[references_root / f"{jurisdiction_dir.name}.md"] = skill_path.read_text(encoding="utf-8")
    if update_cachebuster:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        manifest["version"] = cachebusted_version(str(manifest["version"]))
        outputs[MANIFEST_PATH] = json.dumps(manifest, indent=2) + "\\n"
    return outputs


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_outputs(outputs: dict[Path, str]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def cachebusted_version(version: str) -> str:
    match = SEMVER_WITH_BUILD_RE.match(version)
    if match is None:
        raise ValueError(f"unsupported plugin version: {version}")
    base_version = match.group(1)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{base_version}+codex.{stamp}"


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run packaging once**

Run:

```bash
python3 scripts/package_plugin.py
```

Expected: `plugins/civic-agent/skills/civic-agent/references/seattle.md` exactly matches `jurisdictions/seattle/skill.md`.

- [ ] **Step 3: Run drift check**

Run:

```bash
python3 scripts/package_plugin.py --check
```

Expected: `Plugin package is current.`

### Task 3: Update Router and Documentation Paths

**Files:**
- Modify: `skill.md`
- Modify: `skills/civic-agent/SKILL.md`
- Modify: `README.md`
- Modify: `docs/architecture.md`
- Modify: `docs/plan.md`
- Modify: `examples/prompts.md`

- [ ] **Step 1: Update hosted router paths**

In `skill.md`, replace raw Seattle skill URLs with:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/seattle/skill.md
```

Replace local action references from:

```text
skills/seattle/skill.md
```

to:

```text
jurisdictions/seattle/skill.md
```

- [ ] **Step 2: Update installable router source paths**

In `skills/civic-agent/SKILL.md`, keep the bundled plugin reference:

```text
references/seattle.md
```

Replace source-repo fallback references with:

```text
jurisdictions/seattle/skill.md
```

Replace hosted public repo references with:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/seattle/skill.md
```

- [ ] **Step 3: Update README repo shape**

Update the tree in `README.md` to show:

```text
jurisdictions/
  seattle/
    README.md
    skill.md
    sources/
      operating-budget.source.json
    data/
      README.md
```

Remove top-level `data/seattle`, `sources/seattle`, and `skills/seattle` entries from the tree.

- [ ] **Step 4: Update architecture and plan docs**

In `docs/architecture.md`, make `jurisdictions/<jurisdiction>/skill.md` the canonical jurisdiction reference and explain plugin references are generated.

In `docs/plan.md`, replace Seattle file paths with:

```text
jurisdictions/seattle/skill.md
jurisdictions/seattle/sources/operating-budget.source.json
```

- [ ] **Step 5: Update examples**

Run:

```bash
rg -n "skills/seattle|sources/seattle|data/seattle|raw.githubusercontent.com/pejmanjohn/civic-agent/main/skills/seattle" .
```

Replace any remaining stale public or local Seattle paths with the `jurisdictions/seattle` equivalents.

### Task 4: Validate, Reinstall, and Commit

**Files:**
- Modify: `plugins/civic-agent/.codex-plugin/plugin.json`
- Generated: `plugins/civic-agent/skills/civic-agent/SKILL.md`
- Generated: `plugins/civic-agent/skills/civic-agent/agents/openai.yaml`
- Generated: `plugins/civic-agent/skills/civic-agent/references/seattle.md`

- [ ] **Step 1: Refresh package with cachebuster**

Run:

```bash
python3 scripts/package_plugin.py --update-cachebuster
```

Expected: `plugins/civic-agent/.codex-plugin/plugin.json` version changes to `0.1.0+codex.<timestamp>`.

- [ ] **Step 2: Validate package and canonical skill**

Run:

```bash
uv run --with PyYAML python /Users/pejman/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/pejman/code/civic-agent/plugins/civic-agent
uv run --with PyYAML python /Users/pejman/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/pejman/code/civic-agent/skills/civic-agent
python3 scripts/package_plugin.py --check
```

Expected:

```text
Plugin validation passed: /Users/pejman/code/civic-agent/plugins/civic-agent
Skill is valid!
Plugin package is current.
```

- [ ] **Step 3: Reinstall plugin locally**

Run:

```bash
codex plugin add civic-agent@civic-agent
codex plugin list | rg -n 'Marketplace `civic-agent`|civic-agent@civic-agent' -C 1
```

Expected: `civic-agent@civic-agent` is installed from `/Users/pejman/code/civic-agent/plugins/civic-agent`.

- [ ] **Step 4: Commit implementation**

Run:

```bash
git status -sb
git add -A
git commit -m "Organize jurisdiction sources"
```

Expected: commit includes the jurisdiction tree, packaging script, generated plugin reference, and documentation updates.
