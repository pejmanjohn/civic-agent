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

The installable skill may be exposed by a host as `/civic-agent`, but slash-command behavior is host-specific. The repo's responsibility is to provide a clear router skill and jurisdiction reference files.

The repo also includes `.agents/plugins/marketplace.json` so Codex marketplace installs can discover the plugin:

```bash
codex plugin marketplace add pejmanjohn/civic-agent --ref main
codex plugin add civic-agent@civic-agent
```

## Routing Contract

Root router:

- `skill.md`
- `skills/civic-agent/SKILL.md`
- `plugins/civic-agent/skills/civic-agent/SKILL.md` as the packaged plugin copy

Jurisdiction reference:

- `skills/<jurisdiction>/skill.md`
- `skills/civic-agent/references/<jurisdiction>.md` for the source copy of the installable router
- `plugins/civic-agent/skills/civic-agent/references/<jurisdiction>.md` inside the packaged plugin

Source metadata:

- `sources/<jurisdiction>/<dataset>.source.json`

Optional data snapshots:

- `data/<jurisdiction>/<dataset>/<version>.raw.<csv|xlsx|json>`
- `data/<jurisdiction>/<dataset>/<version>.normalized.jsonl`
- `data/<jurisdiction>/<dataset>/<version>.summary.json`
- `data/<jurisdiction>/<dataset>/<version>.provenance.json`

## Routing Rules

1. Detect jurisdiction.
2. Detect budget family or question type.
3. Read the matching jurisdiction skill.
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

Washington will likely be the messy source: Fiscal WA and OFM pages, ReportViewer exports, Power BI surfaces, XLSX files, and PDFs. That means the repo must support both live queries and curated snapshots.
