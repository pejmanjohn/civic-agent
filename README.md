# civic-agent

Agent-readable civic budget skills and data adapters.

The goal is simple: point a capable agent at one public skill URL, then ask useful budget questions without knowing where the data lives, how the schema works, or what caveats matter.

## First Prompt

For a fresh agent:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```

For a specific first task:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and compare Seattle Police Department, Seattle Fire Department, and Human Services Department from FY2018 to FY2026.
```

## Repo Shape

```text
civic-agent/
  .agents/plugins/
    marketplace.json        # marketplace entry for Codex plugin discovery
  skill.md                 # hosted router skill for fresh-agent prompts
  skills/
    civic-agent/SKILL.md   # installable router skill; hosts may expose this as /civic-agent
    civic/SKILL.md         # short alias
    seattle/skill.md       # Seattle-specific budget analyst skill
  plugins/
    civic-agent/           # packaged Codex plugin install target
      .codex-plugin/plugin.json
      skills/
        civic-agent/SKILL.md
        civic/SKILL.md
        seattle/skill.md
  sources/
    seattle/
      operating-budget.source.json
  data/
    seattle/
      README.md
  docs/
    architecture.md
    plan.md
  examples/
    prompts.md
```

## Routing Model

`skill.md` is the public entry point. It routes the agent to a jurisdiction-specific skill file.

`skills/civic-agent/SKILL.md` is the installable router skill. If a host maps installed skills to slash commands, this is the skill intended to become `/civic-agent`.

`plugins/civic-agent/` is the packaged plugin copy used by the Codex marketplace install flow.

## Codex Plugin Install

For Codex builds that install plugins from marketplaces:

```bash
codex plugin marketplace add pejmanjohn/civic-agent --ref main
codex plugin add civic-agent@civic-agent
```

After install, hosts that expose skill slash commands should route `/civic-agent` to `skills/civic-agent/SKILL.md`.

Example combined with a chart-capable analytics tool:

```text
@data-analytics /civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026.
```

Current production source:

- `seattle.operating_budget`: City of Seattle operating budget, Socrata dataset `8u2j-imqx`

Future sources should follow the same pattern:

- `washington.budget.operating`
- `washington.spending.checkbook`
- `king_county.budget`
- `san_francisco.operating_budget`

## Data Strategy

Use live official APIs when they are clean and stable. Use checked-in snapshots when official public data is slow-changing, awkward to scrape, or report-shaped.

Seattle is the clean example: direct Socrata JSON/CSV plus SoQL.

Washington will likely be the messy example: Fiscal WA / OFM pages, downloadable XLSX files, ReportViewer exports, PDFs, and normalization.
