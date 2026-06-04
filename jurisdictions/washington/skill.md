---
name: washington-budget-analyst
description: Use when answering questions about Washington state operating budget totals, agency or functional area rankings, or enacted budget trends over time from Fiscal WA.
---

# Washington Budget Analyst

Use this skill for Washington state operating budget questions that can be answered from the checked-in Fiscal WA operating budget snapshot, including 2025-27 enacted agency/function totals and enacted base biennial trends from 2013-15 through 2025-27.

Do not use this for actual spending, vendor payments, checkbook transactions, procurement, actual revenue collected, staffing/FTE, capital budget, transportation budget, Seattle budget analysis, King County budget analysis, or cross-jurisdiction comparison unless a separate source explicitly supports that question.

## Source Of Truth

- Dataset: Washington Operating Budget Summary Reports
- Provider: Fiscal WA / LEAP / Office of Financial Management / Microsoft Power BI
- Current official dashboard page: `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- Historical official dashboard page: `https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior`
- OFM context page: `https://ofm.wa.gov/budget/`
- Current Power BI report: `https://app.powerbi.com/view?r=eyJrIjoiYjMzNmE2MDMtMWY2Ni00NjVkLWFmN2YtZWI4YjE3MjhkNTgzIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- Historical Power BI report: `https://app.powerbi.com/view?r=eyJrIjoiN2QyYmI5Y2EtMjgwZS00OTQ3LTgwMzgtYmY2YzYzMjRlNzIyIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- Source card: `jurisdictions/washington/sources/operating-budget.source.json`
- Snapshot version: `2025-27-enacted-2025-05-20`
- Budget version: `Enacted (05-20-2025)`
- Current model refresh time: `2025-07-22T17:18:33.94`
- Historical model refresh time: `2025-12-29T18:08:24.87`
- Snapshot generated from live Power BI replay: see `jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/provenance.json`

For local dev-plugin testing, read snapshot files from this source checkout:

```text
/Users/pejman/code/civic-agent/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/
```

For hosted/fresh-agent use after the source is pushed, checked-in snapshot files will be available under:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/agency-by-fund-view.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/functional-area-by-fund-view.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/version-summary.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-biennium-summary.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-agency-by-biennium.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-functional-area-by-biennium.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/summary.json
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/provenance.json
```

Treat this as budgeted/authorized operating budget data, not actual spending. Amounts are normalized to dollars; Fiscal WA report values are returned in thousands.

## Safe Answer Patterns

This source can safely support:

- 2025-27 enacted operating budget totals by agency.
- 2025-27 enacted operating budget totals by functional area.
- Statewide enacted base operating budget trends by biennium from 2013-15 through 2025-27.
- Agency enacted base operating budget trends by biennium from 2013-15 through 2025-27.
- Functional area enacted base operating budget trends by biennium from 2013-15 through 2025-27.
- Comparisons between `Total Budgeted` and `Outlook Funds (NGF-O)` fund views.
- Budget-version summaries for the 2025-27 biennial operating budget report.
- Chart-ready tables for the supported snapshot grains.

Do not use this source for actual spending, vendor payments, procurement, actual revenue, staffing/FTE, capital budget, transportation budget, 2026 supplemental changes, line-item text search, historical trends before 2013-15, supplemental/proposal historical comparisons, or cross-jurisdiction comparisons.

## Data Model

Snapshot files:

- `agency-by-fund-view.jsonl`: one row per agency and fund view
- `functional-area-by-fund-view.jsonl`: one row per functional area and fund view
- `version-summary.jsonl`: one row per budget version and fund view in the summary report
- `historical-biennium-summary.jsonl`: one row per enacted base biennial operating budget from 2013-15 through 2025-27
- `historical-agency-by-biennium.jsonl`: one row per agency and biennium for enacted base Total Budgeted trends
- `historical-functional-area-by-biennium.jsonl`: one row per functional area and biennium for enacted base Total Budgeted trends
- `summary.json`: row counts and validation checks
- `provenance.json`: model metadata, query-template hashes, response checksums, and source entities

Fields:

- `source_surface_id`: Power BI surface that supplied the row
- `biennium`: `2025-27` for current rows; `2013-15` through `2025-27` for supported historical trend rows
- `period_type`: `biennium`
- `session_type`: Fiscal WA session type; default historical trend uses `R1`
- `budget_state`: `enacted` for supported historical trends
- `revision_scope`: `base` for supported historical trends
- `budget_version`: Fiscal WA budget version label, such as `Enacted (05-20-2025)` for current rows or `Enacted` for historical trend rows
- `budget_version_filter`: Fiscal WA report filter label
- `fund_view`: `Total Budgeted` or `Outlook Funds (NGF-O)`
- `agency_code`: official Fiscal WA agency code
- `agency`: Washington state agency label
- `functional_area_code`: official Fiscal WA functional area code
- `functional_area`: Fiscal WA functional area label
- `amount_thousands`: report amount in thousands of dollars
- `budgeted_amount`: normalized dollar amount

Primary measure:

```text
sum(budgeted_amount)
```

Default fund view:

```text
Total Budgeted
```

Use `Outlook Funds (NGF-O)` only when the user asks for near-general-fund/outlook funds or when explaining the difference between fund views.

Default historical trend filter:

```text
period_type = "biennium"
budget_state = "enacted"
revision_scope = "base"
session_type = "R1"
budget_version = "Enacted"
fund_view = "Total Budgeted"
```

## Retrieval Strategy

1. Use the checked-in snapshot files as the normal answer source.
2. Use `summary.json` for validation checks before trusting totals.
3. Use `provenance.json` when the answer needs model refresh time, query-template hashes, or Power BI source details.
4. Use the live Power BI extractor only when refreshing the snapshot, not during normal answer generation.
5. If a question asks for an unsupported grain, answer with the supported grains and explain the boundary.

## Query Recipes

### Largest agencies in the 2025-27 enacted operating budget

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/agency-by-fund-view.jsonl
```

Filter:

```text
fund_view = "Total Budgeted"
```

Known checks:

```text
rows = 102
Total Budgeted total = 150411096000
```

Largest Total Budgeted agency rows:

- WA State Health Care Authority: $38.033B
- Public Schools: $36.407B
- Dept of Social and Health Services: $25.021B
- University of Washington: $9.493B
- Children, Youth, and Families: $5.904B
- Community/Technical College System: $4.327B
- Department of Corrections: $3.341B
- Bond Retirement and Interest: $3.306B

### Functional area totals

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/functional-area-by-fund-view.jsonl
```

Filter:

```text
fund_view = "Total Budgeted"
```

Known checks:

```text
rows = 11
Total Budgeted total = 150411096000
```

Largest Total Budgeted functional area rows:

- Other Human Services: $51.743B
- Public Schools: $36.407B
- DSHS: $25.021B
- Higher Education: $18.923B
- Governmental Operations: $8.602B
- Special Appropriations: $4.364B
- Natural Resources: $3.757B
- Judicial: $751.5M

### Fund view comparison

Read either normalized table and group by `fund_view`.

Known checks:

```text
Total Budgeted = 150411096000
Outlook Funds (NGF-O) = 77857672000
```

Explain that `Total Budgeted` includes all budgeted funds in the report, while `Outlook Funds (NGF-O)` is a narrower near-general-fund/outlook view.

### Budget version summary

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/version-summary.jsonl
```

Use this to explain which 2025-27 biennial versions are visible in the summary report: agency request, governor proposal, House/Senate versions, passed legislature, and enacted.

### Statewide operating budget trend

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-biennium-summary.jsonl
```

Use this for questions like "How has the Washington state operating budget changed over time?"

Known checks:

```text
rows = 7
coverage = 2013-15 through 2025-27
historical_current_overlap_total = 150411096000
```

Known enacted base Total Budgeted biennial totals:

- 2013-15: $66.522B
- 2015-17: $78.888B
- 2017-19: $88.274B
- 2019-21: $99.706B
- 2021-23: $121.733B
- 2023-25: $133.610B
- 2025-27: $150.411B

Always state that this is an enacted base biennial Total Budgeted trend, not actual spending and not a supplemental/proposal comparison.

### Agency operating budget trend

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-agency-by-biennium.jsonl
```

Filter by `agency` or `agency_code`, then sort by `biennium`.

Known checks:

```text
rows = 711
agency totals by biennium match historical-biennium-summary.jsonl
2025-27 rows come from current_biennial_summary_powerbi
2013-15 through 2023-25 rows come from prior_summary_powerbi
```

When interpreting long trends, mention that official agency labels and agency structures can change over time.

### Functional area operating budget trend

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-functional-area-by-biennium.jsonl
```

Filter by `functional_area` or `functional_area_code`, then sort by `biennium`.

Known checks:

```text
rows = 77
functional area totals by biennium match historical-biennium-summary.jsonl
2025-27 rows come from current_biennial_summary_powerbi
2013-15 through 2023-25 rows come from prior_summary_powerbi
```

Use this as the supported high-level policy grouping for historical Washington operating-budget trends.

## Analysis Patterns

### Where does Washington budget the most?

Use `agency-by-fund-view.jsonl`, filter to `Total Budgeted`, sort by `budgeted_amount desc`, and state the fund view.

### What is the difference between Total Budgeted and Outlook Funds?

Use the known fund-view totals and explain the accounting boundary. Do not mix the two in one ranking unless the user explicitly asks for a comparison table.

### Functional area questions

Use `functional-area-by-fund-view.jsonl`. This is the closest supported high-level policy grouping in the first Washington snapshot.

For historical functional area trends, use `historical-functional-area-by-biennium.jsonl`.

### Budget over time questions

Use `historical-biennium-summary.jsonl` for statewide trends. Use the historical agency or functional-area files only when the user asks for a specific agency or functional-area trend. Default to enacted base Total Budgeted rows and state the supported coverage range.

### Latest or current questions

Say the current Washington snapshot is the 2025-27 enacted biennial operating budget with current model refresh time `2025-07-22T17:18:33.94`. Historical trend rows use the prior summary model with refresh time `2025-12-29T18:08:24.87`. The separate 2026 supplemental report has been probed but is not implemented in this source slice.

## Interpretation Rules

- Use "budgeted amount" or "authorized operating budget," not actual spending.
- State the budget version: `2025-27 enacted`.
- State the fund view, especially when using `Outlook Funds (NGF-O)`.
- Amounts are dollars in the normalized snapshot.
- Historical trend answers default to enacted base biennial Total Budgeted rows from 2013-15 through 2025-27.
- Do not answer 2026 supplemental changes unless the supplemental snapshot is added.
- Do not answer pre-2013-15 Washington operating-budget trends from this snapshot.
- Do not answer proposal-stage, House, Senate, Governor, supplemental, or revised historical comparisons unless a matching normalized table is added.
- Do not infer service quality, policy outcomes, or operational performance from budget rows alone.
- Do not compare Washington to Seattle or King County until accounting definitions and normalized dimensions are explicit.

## Validation Checks

Known checks from snapshot `2025-27-enacted-2025-05-20`:

- Total Budgeted agency rows: 102
- Total Budgeted functional area rows: 11
- Total Budgeted total: $150.411B
- Outlook Funds (NGF-O) total: $77.858B
- Agency and functional area totals match by fund view
- Version summary rows: 28
- Historical statewide trend rows: 7
- Historical agency trend rows: 711
- Historical functional area trend rows: 77
- Historical coverage: 2013-15 through 2025-27
- Historical totals by biennium match agency and functional area totals
- Historical 2025-27 overlap matches the current Total Budgeted total: $150.411B

If a result differs materially, verify the snapshot version, budget version filter, fund view, and whether the user asked for budgeted values or actuals.

## Answer Style

Use this compact structure for source-backed answers:

```text
Conclusion:
Numbers:
How to read this:
Trace:
- Source:
- Snapshot:
- Grain:
- Measure:
- Filters/query logic:
- Check:
- Caveats:
```

Example trace:

```text
Trace:
- Source: Fiscal WA 2025-27 Biennial Omnibus Operating Budget Summary Comparison, snapshot 2025-27-enacted-2025-05-20
- Grain: agency
- Measure: budgeted_amount
- Filters/query logic: read agency-by-fund-view.jsonl, filter fund_view = "Total Budgeted", sort by budgeted_amount desc
- Check: 102 Total Budgeted agency rows; Total Budgeted total = $150.411B
- Caveats: budgeted/authorized operating budget, not actual spending; 2025-27 enacted biennial budget; not the 2026 supplemental snapshot
```
