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
- [x] Create Seattle jurisdiction skill at `jurisdictions/seattle/skill.md`.
- [x] Bundle Seattle as a primary-skill reference for Codex plugin installs.
- [x] Add Seattle source metadata at `jurisdictions/seattle/sources/operating-budget.source.json`.
- [x] Publish worked demo answers for the dogfood prompts at `docs/seattle-demo.md`.
- [x] Tighten the Seattle answer style with compact source/grain/query/caveat traces.

Dogfood prompts represented in `docs/seattle-demo.md`:

- Where does Seattle spend the most money in FY2026?
- Compare Seattle Police Department and Seattle Fire Department from FY2018 to FY2026.
- Compare Seattle Police Department, Seattle Fire Department, and Human Services Department from FY2018 to FY2026.
- What programs inside Seattle Police Department are largest in FY2026?
- What are the biggest negative rows in FY2026?
- How much is labor vs non-labor in FY2026?
- Make me a chart showing which Seattle departments had the largest budget increases from FY2018 to FY2026.

Formal eval fixtures are deferred until Civic Agent has an answer runner that can check real outputs.

## Phase 1.5: King County

- [x] Add King County as the second source and first report-shaped source.
- [x] Add `jurisdictions/king_county/skill.md`.
- [x] Add source metadata at `jurisdictions/king_county/sources/open-budget-dashboard.source.json`.
- [x] Add reviewed Power BI query templates and a source-specific extractor.
- [x] Add checked-in normalized snapshot, summary, and provenance for snapshot `2026-04-01`.
- [x] Add fixture-backed extractor tests for the supported Power BI response shapes.
- [x] Publish worked King County demo answers at `docs/king-county-demo.md`.

King County intentionally stays narrow: budgeted revenue, budgeted expenditures, and budgeted FTE from the Open Budget Dashboard. It does not add a generic Power BI adapter, contributor scaffold, or cross-jurisdiction comparison model.

## Phase 2: Washington

- [x] Probe Washington state budget sources and classify Fiscal WA as the primary official data surface.
- [x] Treat Fiscal WA operating budget reports as Power BI-backed snapshot candidates.
- [x] Treat OFM as the executive budget and source-document authority.
- [x] Treat LEAP as a source family inside the Washington adapter, not the top-level dataset.
- [x] Decide the first supported operating budget version/default from Fiscal WA: 2025-27 enacted biennial operating budget.
- [x] Add `jurisdictions/washington/skill.md`.
- [x] Add source metadata for the first Washington operating budget source.
- [x] Add a checked-in normalized snapshot for the first Washington operating budget source.
- [ ] Decide whether spending/checkbook should be a second Washington source based on downloadable XLSX files.
- [ ] Add source metadata for capital, transportation, revenue, staffing, and K-12 only after each source is probed.
- [x] Decide which data should be snapshotted because it is slow-changing or awkward to extract live.
- [x] Build extractor/normalizer scripts for the first operating-budget Power BI surface.

## Phase 3: Multi-Jurisdiction

- [x] Define a civic coverage taxonomy that separates the full aspirational coverage map from the current active budget/public-finance categories.
- [x] Add source-level coverage claims for current production source cards.
- [x] Add a generated coverage matrix and reviewed-source jurisdiction rollup.
- [ ] Define normalized schema for cross-jurisdiction comparison.
- [ ] Add a durable source-fingerprint and validation workflow across live, checked-in snapshot, and managed local data tiers.
- [ ] Add examples for city-to-city and city-to-state comparisons.

## Design Principles

- The public prompt should be short.
- The skill document should carry the complexity.
- Official sources are the source of truth.
- New source families should start with a probe brief before source cards or extractors.
- Coverage claims are source-level review aids, not jurisdiction scores.
- Backlog civic categories should become active only after a source probe proves what an official source can answer.
- Snapshots are allowed when official public data changes slowly or is painful for agents to retrieve reliably.
- Do not compare jurisdictions until field mappings and caveats are explicit.
