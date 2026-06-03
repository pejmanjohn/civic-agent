# Plan

## Goal

Build an open-source civic budget agent repository with hosted skill files, source adapters, and data snapshots where necessary.

The first useful experience:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```

## Phase 1: Seattle

- [x] Create root hosted router skill at `skill.md`.
- [x] Create Codex plugin manifest at `plugins/civic-agent/.codex-plugin/plugin.json`.
- [x] Create installable router skill at `skills/civic-agent/SKILL.md` for `/civic-agent` style hosts.
- [x] Create Seattle jurisdiction skill at `skills/seattle/skill.md`.
- [x] Bundle Seattle as a primary-skill reference for Codex plugin installs.
- [x] Add Seattle source metadata at `sources/seattle/operating-budget.source.json`.
- [ ] Dogfood the hosted prompt with 5-6 budget questions.
- [ ] Tighten the Seattle skill where agents stumble.

Dogfood prompts:

- Where does Seattle spend the most money in FY2026?
- Compare Seattle Police Department and Seattle Fire Department from FY2018 to FY2026.
- Compare Seattle Police Department, Seattle Fire Department, and Human Services Department from FY2018 to FY2026.
- What programs inside Seattle Police Department are largest in FY2026?
- What are the biggest negative rows in FY2026?
- How much is labor vs non-labor in FY2026?
- Make me a chart showing which Seattle departments had the largest budget increases from FY2018 to FY2026.

## Phase 2: Washington

- [ ] Treat Fiscal WA as the broad public fiscal portal.
- [ ] Treat OFM as the executive budget and source-document authority.
- [ ] Treat LEAP as a source family inside the Washington adapter, not the top-level dataset.
- [ ] Add `skills/washington/skill.md`.
- [ ] Add source metadata for operating, capital, transportation, revenue, spending/checkbook, staffing, and K-12.
- [ ] Decide which data should be snapshotted because it is slow-changing or awkward to extract live.
- [ ] Build extractor/normalizer scripts for ReportViewer/XLSX/PDF surfaces only where necessary.

## Phase 3: Multi-Jurisdiction

- [ ] Define normalized schema for cross-jurisdiction comparison.
- [ ] Add snapshot provenance format.
- [ ] Add validation checks per source.
- [ ] Add examples for city-to-city and city-to-state comparisons.

## Design Principles

- The public prompt should be short.
- The skill document should carry the complexity.
- Official sources are the source of truth.
- Snapshots are allowed when official public data changes slowly or is painful for agents to retrieve reliably.
- Do not compare jurisdictions until field mappings and caveats are explicit.
