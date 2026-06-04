# civic-agent

<img src="plugins/civic-agent/assets/icon.png" alt="Civic Agent icon" width="120">

Agent-readable civic budget skills, source cards, and plugin packaging.

The goal is simple: point a capable agent at one public skill URL, then ask useful budget questions without knowing where the data lives, how the schema works, or what caveats matter.

## Repo Shape

```text
civic-agent/
  .claude-plugin/
    marketplace.json        # marketplace catalog for Claude Code plugin discovery
  .agents/plugins/
    marketplace.json        # marketplace entry for Codex plugin discovery
  .agents/skills/
    civic-agent-maintainer/ # repo-local maintainer skill for dev refresh/status/smoke
  skill.md                 # hosted router skill for fresh-agent prompts
  jurisdictions/
    seattle/
      README.md
      skill.md
      sources/
        operating-budget.source.json
      data/
        README.md
    king_county/
      README.md
      skill.md
      sources/
        open-budget-dashboard.source.json
      data/
        open-budget-dashboard/
          2026-04-01/
          query_templates/
  skills/
    civic-agent/SKILL.md   # installable router skill; hosts may expose this as /civic-agent
    civic-agent/agents/    # Codex display metadata for the primary skill
  plugins/
    civic-agent/           # packaged plugin install target (Codex + Claude Code)
      .codex-plugin/plugin.json    # Codex manifest (name: civic-agent)
      .claude-plugin/plugin.json   # Claude Code manifest (generated; name: civic-agent)
      assets/icon.png
      skills/
        civic-agent/SKILL.md       # router skill; invoked as /civic-agent in both
        civic-agent/agents/openai.yaml
        civic-agent/references/seattle.md
        civic-agent/references/king_county.md
  scripts/
    package_plugin.py
    dev.py                  # agent-run local dev plugin installer/status helper
  docs/
    architecture.md
    coverage-matrix.md
    coverage-taxonomy.md
    plan.md
    seattle-demo.md
  examples/
    prompts.md
```

## Routing Model

`skill.md` is the public entry point. It routes the agent to a jurisdiction-specific skill file under `jurisdictions/`.

`skills/civic-agent/SKILL.md` is the installable router skill. If a host maps installed skills to slash commands, this is the skill intended to become `/civic-agent`.

`plugins/civic-agent/` is the packaged plugin copy used by the Codex marketplace install flow. It intentionally exposes one Codex-facing skill so the composer label appears as `Civic Agent`; jurisdiction instructions are generated as bundled references from `jurisdictions/<slug>/skill.md`.

`plugins/civic-agent/` carries a manifest for each ecosystem in the same directory: the hand-authored `.codex-plugin/plugin.json` and the generated `.claude-plugin/plugin.json` (both named `civic-agent`). The two share one `skills/civic-agent/` tree, so jurisdiction behavior never diverges. The router `SKILL.md` declares an `argument-hint`, which makes Claude Code treat it as a command and show it in the picker as the bare `/civic-agent` rather than the namespaced `/civic-agent:civic-agent` (skills without `argument-hint` are shown namespaced). The Claude Code manifest is generated from the Codex manifest by `scripts/package_plugin.py`.

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

## Claude Code Plugin Install

For Claude Code:

```text
/plugin marketplace add pejmanjohn/civic-agent
/plugin install civic-agent@civic-agent
```

The `owner/repo` shorthand resolves the repository's default branch (`main`), so no ref pin is needed; append `@main` to pin it explicitly. After install, invoke the router as:

```text
/civic-agent
```

The picker shows the bare `/civic-agent` (not `/civic-agent:civic-agent`) because the skill declares an `argument-hint`, which Claude Code treats as a command. You usually don't type it at all: the skill is model-invoked from its description, so asking a budget question fires it automatically. Validate the marketplace and plugin locally before sharing:

```bash
claude plugin validate .
claude plugin validate ./plugins/civic-agent
```

Current production sources:

- `seattle.operating_budget`: City of Seattle operating budget, Socrata dataset `8u2j-imqx`
- `king_county.open_budget_dashboard`: King County Open Budget Dashboard, Power BI Gov snapshot `2026-04-01`
- `washington.operating_budget`: Washington state operating budget, Fiscal WA Power BI snapshot `2025-27-enacted-2025-05-20`, including 2025-27 enacted agency/function totals and enacted base biennial trends from 2013-15 through 2025-27

Coverage orientation:

- `docs/coverage-taxonomy.md`: full civic coverage map, current active budget/public-finance categories, and rules for promoting backlog categories after source probes.
- `docs/coverage-matrix.md`: generated source and jurisdiction coverage view from checked-in source cards. It is a reviewed-source coverage aid, not a jurisdiction score.

Worked examples:

- `docs/seattle-demo.md`: source-backed answers and compact traces for the current dogfood prompts.
- `docs/king-county-demo.md`: source-backed answers and compact traces for the King County snapshot.
- `docs/coverage-matrix.md`: source-level coverage claims and derived jurisdiction rollups.
- `docs/source-probing.md`: workflow for evaluating new official sources before adding them.
- `docs/source-probes/seattle-open-data-portal.md`: Socrata/open data portal probe and workflow lessons.
- `docs/source-probes/washington-state-budget.md`: current Washington state budget source probe.
- `jurisdictions/washington/skill.md`: source-backed answer recipes for the Washington operating budget snapshot.

## Packaging

Location-specific source files live under `jurisdictions/`. Refresh the checked-in plugin package after editing canonical jurisdiction or router files. The Claude Code manifest (`plugins/civic-agent/.claude-plugin/plugin.json`) is generated from the hand-authored Codex manifest, so shared metadata is edited once in `plugins/civic-agent/.codex-plugin/plugin.json`:

```bash
python3 scripts/package_plugin.py
python3 scripts/package_plugin.py --check
```

`package_plugin.py --check` also fails when a stale generated jurisdiction reference remains in the packaged plugin after a jurisdiction is renamed or removed.

## Agent-Native Development Loop

The preferred development workflow is conversational. Ask the local maintainer skill to refresh or inspect dev state instead of running commands manually:

```text
refresh Civic Agent dev
check Civic Agent dev status
smoke test Civic Agent dev
```

The maintainer skill lives at `.agents/skills/civic-agent-maintainer/SKILL.md`. It runs the deterministic helper script for you and reports the result.

For local Codex testing, the maintainer skill generates and installs a gitignored dev plugin:

```text
@civic-agent      production/stable install
@civic-agent-dev  current local checkout, explicit testing only
```

After a dev refresh, open a new Codex thread and explicitly invoke `@civic-agent-dev`. Active threads do not reload newly installed plugin skills.

The underlying agent-run command is:

```bash
python3 scripts/dev.py install
```

It refreshes the checked-in package, generates `.generated/civic-agent-dev-marketplace/`, installs `civic-agent-dev@civic-agent-dev`, and verifies that the installed cache contains the current jurisdiction references. `.generated/` is ignored and should not be edited or committed.

Future sources should follow the same pattern:

- `washington.spending.checkbook`
- `san_francisco.operating_budget`

Before adding a future source, run the source-probing workflow in `docs/source-probing.md` and capture the result with `docs/templates/source-probe-brief.md`.

## Data Strategy

Use live official APIs when they are clean and stable. Use checked-in snapshots when official public data is slow-changing, awkward to scrape, or report-shaped.

Seattle is the clean example: direct Socrata JSON/CSV plus SoQL.

King County is the first report-shaped example: official Power BI Gov dashboard replayed through reviewed query templates into a checked-in normalized snapshot.

Washington is the second report-shaped example: Fiscal WA Power BI reports replayed through reviewed query templates into a checked-in normalized operating budget snapshot. It also demonstrates the split-time-span pattern: one logical source id with multiple official report surfaces stitched into common historical trend tables and validated by overlap totals. Treat Open Checkbook as a separate actual-spending source.
