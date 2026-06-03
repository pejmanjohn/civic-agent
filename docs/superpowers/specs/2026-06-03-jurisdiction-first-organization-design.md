# Jurisdiction-First Organization Design

## Summary

Reorganize Civic Agent around a canonical `jurisdictions/<slug>/` source tree so each location is easy to explore in one place. The checked-in Codex plugin package should remain installable, but location-specific plugin references should be generated from the canonical jurisdiction files instead of authored separately.

## Goals

- Make each jurisdiction browsable as a complete unit.
- Keep data notes, source metadata, and jurisdiction instructions colocated.
- Preserve the existing public router and Codex plugin installation flow.
- Reduce drift between canonical jurisdiction files and packaged plugin references.
- Keep the structure simple enough for future contributors adding Washington, King County, or other jurisdictions.

## Non-Goals

- Do not redesign the Civic Agent routing behavior.
- Do not change the Seattle budget analysis content.
- Do not add new jurisdictions as part of this reorganization.
- Do not require consumers to understand plugin packaging internals to browse civic data sources.

## Proposed Source Layout

Canonical location-specific files should live under `jurisdictions/<slug>/`:

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

Root-level files should focus on repo, router, package, and examples:

```text
skill.md
skills/
  civic-agent/
    SKILL.md
    agents/openai.yaml
docs/
examples/
scripts/
plugins/
  civic-agent/
```

## Packaged Plugin Layout

The Codex plugin should keep the shape Codex expects:

```text
plugins/civic-agent/
  .codex-plugin/plugin.json
  assets/icon.png
  skills/
    civic-agent/
      SKILL.md
      agents/openai.yaml
      references/
        seattle.md
```

`plugins/civic-agent/skills/civic-agent/references/seattle.md` should be generated from `jurisdictions/seattle/skill.md`. It should not be manually edited.

## Packaging Flow

Add a small packaging script that:

1. Copies the canonical router skill from `skills/civic-agent/SKILL.md` into the plugin package.
2. Copies `skills/civic-agent/agents/openai.yaml` into the plugin package.
3. Copies each `jurisdictions/<slug>/skill.md` to `plugins/civic-agent/skills/civic-agent/references/<slug>.md`.
4. Leaves plugin-only metadata and assets under `plugins/civic-agent/`.
5. Supports an explicit flag for updating the Codex cachebuster when packaging for local reinstall.

The package output can remain checked in so the repository is still easy to install from Codex marketplaces. The script is responsible for keeping generated package references aligned with canonical jurisdiction files.

## Documentation Updates

Update `README.md` and `docs/architecture.md` to explain:

- `jurisdictions/` is the canonical place to browse or add location-specific content.
- `plugins/civic-agent/` is the packaged Codex plugin output.
- Packaged jurisdiction references are generated from `jurisdictions/<slug>/skill.md`.
- Contributors should edit canonical jurisdiction files, then regenerate and validate the plugin package.

## Validation

The implementation should include these checks:

- Validate the canonical `skills/civic-agent` skill.
- Validate the packaged `plugins/civic-agent` plugin.
- Verify generated plugin references match canonical jurisdiction skill files.
- Confirm `codex plugin add civic-agent@civic-agent` installs the regenerated package locally.

## Migration Plan

1. Create `jurisdictions/seattle/`.
2. Move `skills/seattle/skill.md` to `jurisdictions/seattle/skill.md`.
3. Move `sources/seattle/operating-budget.source.json` to `jurisdictions/seattle/sources/operating-budget.source.json`.
4. Move `data/seattle/README.md` to `jurisdictions/seattle/data/README.md`.
5. Add the packaging script.
6. Regenerate `plugins/civic-agent/skills/civic-agent/references/seattle.md`.
7. Update docs and examples to reference the jurisdiction-first layout.
8. Run validation and local reinstall.

## Implementation Defaults

- The packaging script should not update the plugin cachebuster by default. It should provide an explicit flag for local reinstall workflows.
- Source metadata filenames should keep the `.source.json` suffix. That keeps source manifests distinct from general JSON data files inside each jurisdiction.
