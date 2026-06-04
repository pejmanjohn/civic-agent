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

## Local Development Surface

Development is agent-native. The repo includes a local maintainer skill at `.agents/skills/civic-agent-maintainer/SKILL.md` for package refreshes, install status, and smoke-test prompts. A developer can ask the agent to refresh Civic Agent dev; the agent runs the deterministic helper and relays the result.

The helper generates a gitignored Codex dev marketplace under `.generated/civic-agent-dev-marketplace/` with a separate plugin identity:

- `@civic-agent`: production/stable install.
- `@civic-agent-dev`: generated from the current local checkout, explicit testing only.

The dev plugin is generated from the same canonical router and jurisdiction files as the production package. It should never be hand-edited, and it should not be used for generic budget questions unless the user explicitly asks to test the local development build.

After installing or refreshing the dev plugin, open a new Codex thread before testing. Active threads do not reload newly installed plugin skills.

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

Source metadata acts as a source card: it identifies the official source, human inspection URLs, fields, known checks, caveats, safe answer patterns, and claims that source should not support.

Each source card should include `human_inspection_urls`: a short list of public URLs a reader can open to inspect the official source. Keep those separate from machine-oriented API, metadata, and query endpoints.

When one logical source is split across time spans or report pages, keep the source id stable and represent the pieces as `source_surfaces` in the source card. Each accepted surface should carry its official inspection URL, machine endpoint or file metadata, coverage, and status. Normalized rows should include `source_surface_id`, semantic filters such as budget state/fund view/period type, and official dimension codes where available. Snapshot summaries should include overlap reconciliation and period-by-period grouped-total checks before a stitched historical table is treated as answerable.

Before adding a source card for a new source family, write a probe brief using `docs/source-probing.md` and `docs/templates/source-probe-brief.md`. The probe brief should identify the official owner, candidate machine surfaces, access method, supported questions, unsupported claims, validation checks, and whether the source should be accepted live, snapshotted, kept as context only, watched, or rejected.

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

Washington is the second report-shaped source and first split-time-span source: Fiscal WA current and prior Power BI surfaces are stitched into one `washington.operating_budget` snapshot for current 2025-27 rankings and historical enacted base trends from 2013-15 through 2025-27. Fiscal WA also has XLSX files, PDFs, and checkbook surfaces, but those remain separate source families or context until they have their own accepted extraction and validation path.
