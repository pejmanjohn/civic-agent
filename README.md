# civic-agent

<img src="plugins/civic-agent/assets/icon.png" alt="Civic Agent icon" width="120">

Agent-readable civic budget skills and data adapters.

The goal is simple: point a capable agent at one public skill URL, then ask useful budget questions without knowing where the data lives, how the schema works, or what caveats matter.

## Repo Shape

```text
civic-agent/
  .agents/plugins/
    marketplace.json        # marketplace entry for Codex plugin discovery
  skill.md                 # hosted router skill for fresh-agent prompts
  jurisdictions/
    seattle/
      README.md
      skill.md
      sources/
        operating-budget.source.json
      data/
        README.md
  skills/
    civic-agent/SKILL.md   # installable router skill; hosts may expose this as /civic-agent
    civic-agent/agents/    # Codex display metadata for the primary skill
  plugins/
    civic-agent/           # packaged Codex plugin install target
      .codex-plugin/plugin.json
      assets/icon.png
      skills/
        civic-agent/SKILL.md
        civic-agent/agents/openai.yaml
        civic-agent/references/seattle.md
  scripts/
    package_plugin.py
  docs/
    architecture.md
    plan.md
  examples/
    prompts.md
```

## Routing Model

`skill.md` is the public entry point. It routes the agent to a jurisdiction-specific skill file under `jurisdictions/`.

`skills/civic-agent/SKILL.md` is the installable router skill. If a host maps installed skills to slash commands, this is the skill intended to become `/civic-agent`.

`plugins/civic-agent/` is the packaged plugin copy used by the Codex marketplace install flow. It intentionally exposes one Codex-facing skill so the composer label appears as `Civic Agent`; jurisdiction instructions are generated as bundled references from `jurisdictions/<slug>/skill.md`.

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

## Packaging

Location-specific source files live under `jurisdictions/`. Refresh the checked-in Codex plugin package after editing canonical jurisdiction or router files:

```bash
python3 scripts/package_plugin.py
python3 scripts/package_plugin.py --check
```

For local Codex reinstall testing, update the plugin cachebuster explicitly:

```bash
python3 scripts/package_plugin.py --update-cachebuster
codex plugin add civic-agent@civic-agent
```

Future sources should follow the same pattern:

- `washington.budget.operating`
- `washington.spending.checkbook`
- `king_county.budget`
- `san_francisco.operating_budget`

## Data Strategy

Use live official APIs when they are clean and stable. Use checked-in snapshots when official public data is slow-changing, awkward to scrape, or report-shaped.

Seattle is the clean example: direct Socrata JSON/CSV plus SoQL.

Washington will likely be the messy example: Fiscal WA / OFM pages, downloadable XLSX files, ReportViewer exports, PDFs, and normalization.
