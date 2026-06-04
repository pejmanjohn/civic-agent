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

Both catalogs point at the single packaged plugin directory `plugins/civic-agent/`, which carries a manifest for each ecosystem over one shared `skills/civic-agent/` tree:

- The hand-authored `.codex-plugin/plugin.json` is named `civic-agent`; Codex exposes the skill as `/civic-agent`.
- The generated `.claude-plugin/plugin.json` is also named `civic-agent` (install id `civic-agent@civic-agent`). Claude Code namespaces plugin skills as `/<plugin>:<skill>`, but a skill whose `SKILL.md` declares an `argument-hint` is treated as a command and shown in the picker by its bare name. The router declares `argument-hint`, so the picker shows `/civic-agent` rather than `/civic-agent:civic-agent`. (The plugin name does not affect this — a skill without `argument-hint` shows namespaced regardless of the plugin name.)

The Claude Code manifest is generated from the Codex manifest (dropping the Codex `interface` block and stripping the `+codex.<stamp>` version suffix), so shared metadata is edited once in the Codex manifest; `package_plugin.py --check` fails if the generated manifest drifts.

## Routing Contract

Root router:

- `skill.md`
- `skills/civic-agent/SKILL.md`
- `plugins/civic-agent/skills/civic-agent/SKILL.md` as the packaged plugin copy (shared by Codex and Claude Code)

Jurisdiction reference:

- `jurisdictions/<jurisdiction>/skill.md` as the canonical source
- `plugins/civic-agent/skills/civic-agent/references/<jurisdiction>.md` inside the packaged plugin, generated from the canonical source

Source metadata:

- `jurisdictions/<jurisdiction>/sources/<dataset>.source.json`

Source metadata acts as a source card: it identifies the official source, fields, known checks, caveats, safe answer patterns, and claims that source should not support.

Optional data snapshots:

- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.raw.<csv|xlsx|json>`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.normalized.jsonl`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.summary.json`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>.provenance.json`

Report-shaped sources may use a multi-artifact snapshot directory when one official report produces several normalized tables:

- `jurisdictions/<jurisdiction>/data/<dataset>/query_templates/*.query.json`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>/normalized/*.jsonl`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>/summary.json`
- `jurisdictions/<jurisdiction>/data/<dataset>/<version>/provenance.json`

Raw report responses are local/debug artifacts by default unless a specific payload is reviewed and intentionally committed.

## Routing Rules

1. Detect jurisdiction.
2. Detect budget family or question type.
3. Read the matching jurisdiction skill under `jurisdictions/<jurisdiction>/skill.md`.
4. Use that skill's official sources and validation checks.
5. For source-backed answers, include a compact trace: source, grain, measure, filters/query logic, validation check or row count when useful, and caveats.

For composed prompts such as:

```text
@data-analytics /civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026.
```

`/civic-agent` owns source routing, query planning, validation, and budget interpretation. The analytics/charting plugin owns chart rendering after Civic Agent has produced the source-backed table.

Unsupported jurisdictions should fail clearly. Do not fabricate adapters.

## Why This Shape

Seattle is the clean source: a direct Socrata API with stable fields.

King County is the report-shaped source: an official Power BI Gov dashboard replayed through reviewed query templates into a checked-in snapshot.

Washington will likely be the messy source: Fiscal WA and OFM pages, ReportViewer exports, Power BI surfaces, XLSX files, and PDFs. That means the repo must support both live queries and curated snapshots while keeping each jurisdiction's instructions, source metadata, and data notes together.
