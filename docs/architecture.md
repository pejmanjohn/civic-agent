# Architecture

`civic-agent` has two public surfaces:

1. Hosted prompt surface for fresh agents:

   ```text
   Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
   ```

2. Installable skill surface for hosts that expose skills or slash commands:

   ```text
   skills/civic-agent/SKILL.md
   ```

The installable skill may be exposed by a host as `/civic-agent`, but slash-command behavior is host-specific. The repo's responsibility is to provide a clear router skill and canonical jurisdiction files under `jurisdictions/`.

The repo serves two marketplace catalogs from one canonical source, so the same plugin can be installed from either ecosystem:

- Codex discovers the plugin via `.agents/plugins/marketplace.json`:

  ```bash
  codex plugin marketplace add pejmanjohn/civic-agent --ref main
  codex plugin add civic-agent@civic-agent
  ```

- Claude Code discovers it via the repo-root `.claude-plugin/marketplace.json`:

  ```bash
  /plugin marketplace add pejmanjohn/civic-agent
  /plugin install civic-agent@civic-agent
  ```

Each catalog points at its own packaged plugin directory, both generated from the same canonical sources by `scripts/package_plugin.py`:

- Codex installs `plugins/civic-agent/` (hand-authored `.codex-plugin/plugin.json`, router under `skills/civic-agent/SKILL.md`, bundled `references/`). The skill lives under `skills/<name>/`, which Codex exposes as `/civic-agent`.
- Claude Code installs `plugins/civic-agent-cc/` (generated `.claude-plugin/plugin.json`, router as a plugin-root `SKILL.md`, bundled `references/`). The router is the plugin's **root default skill**, so Claude Code exposes it as the bare `/civic-agent` rather than the namespaced `/civic-agent:civic-agent` a `skills/<name>/` layout would produce.

The two ecosystems use separate directories because Claude Code's bare-command default skill requires a plugin-root `SKILL.md` with no sibling `skills/` directory, while Codex's manifest points at `skills/`. The Claude Code manifest is generated from the Codex manifest (dropping the Codex `interface` block and the `+codex.<stamp>` version suffix), so shared metadata is edited once in the Codex manifest; `package_plugin.py --check` fails if any generated file drifts.

## Routing Contract

Root router:

- `skill.md`
- `skills/civic-agent/SKILL.md`
- `plugins/civic-agent/skills/civic-agent/SKILL.md` as the packaged Codex copy
- `plugins/civic-agent-cc/SKILL.md` as the packaged Claude Code copy (plugin-root default skill)

Jurisdiction reference:

- `jurisdictions/<jurisdiction>/skill.md` as the canonical source
- `plugins/civic-agent/skills/civic-agent/references/<jurisdiction>.md` inside the packaged Codex plugin, generated from the canonical source
- `plugins/civic-agent-cc/references/<jurisdiction>.md` inside the packaged Claude Code plugin, generated from the canonical source

Source metadata:

- `jurisdictions/<jurisdiction>/sources/<dataset>.source.json`

Optional data snapshots:

- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.raw.<csv|xlsx|json>`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.normalized.jsonl`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.summary.json`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.provenance.json`

## Routing Rules

1. Detect jurisdiction.
2. Detect budget family or question type.
3. Read the matching jurisdiction skill under `jurisdictions/<jurisdiction>/skill.md`.
4. Use that skill's official sources and validation checks.
5. Explain the grain and caveats in the answer.

For composed prompts such as:

```text
@data-analytics /civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026.
```

`/civic-agent` owns source routing, query planning, validation, and budget interpretation. The analytics/charting plugin owns chart rendering after Civic Agent has produced the source-backed table.

Unsupported jurisdictions should fail clearly. Do not fabricate adapters.

## Why This Shape

Seattle is the clean source: a direct Socrata API with stable fields.

Washington will likely be the messy source: Fiscal WA and OFM pages, ReportViewer exports, Power BI surfaces, XLSX files, and PDFs. That means the repo must support both live queries and curated snapshots while keeping each jurisdiction's instructions, source metadata, and data notes together.
