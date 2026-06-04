---
name: washington-budget-analyst
description: Use when answering questions about Washington state 2025-27 enacted operating budget totals by agency or functional area from Fiscal WA.
---

# Washington Budget Analyst

Use this skill for Washington state operating budget questions that can be answered from the checked-in Fiscal WA 2025-27 enacted biennial operating budget snapshot.

Do not use this for actual spending, vendor payments, checkbook transactions, procurement, actual revenue collected, staffing/FTE, capital budget, transportation budget, Seattle budget analysis, King County budget analysis, or cross-jurisdiction comparison unless a separate source explicitly supports that question.

## Source Of Truth

- Dataset: 2025-27 Biennial Omnibus Operating Budget Summary Comparison
- Provider: Fiscal WA / LEAP / Office of Financial Management / Microsoft Power BI
- Official dashboard page: `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- OFM context page: `https://ofm.wa.gov/budget/`
- Power BI report: `https://app.powerbi.com/view?r=eyJrIjoiYjMzNmE2MDMtMWY2Ni00NjVkLWFmN2YtZWI4YjE3MjhkNTgzIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- Source card: `jurisdictions/washington/sources/operating-budget.source.json`
- Snapshot version: `2025-27-enacted-2025-05-20`
- Budget version: `Enacted (05-20-2025)`
- Model refresh time: `2025-07-22T17:18:33.94`
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
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/summary.json
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/provenance.json
```

Treat this as budgeted/authorized operating budget data, not actual spending. Amounts are normalized to dollars; Fiscal WA report values are returned in thousands.

## Safe Answer Patterns

This source can safely support:

- 2025-27 enacted operating budget totals by agency.
- 2025-27 enacted operating budget totals by functional area.
- Comparisons between `Total Budgeted` and `Outlook Funds (NGF-O)` fund views.
- Budget-version summaries for the 2025-27 biennial operating budget report.
- Chart-ready tables for the supported snapshot grains.

Do not use this source for actual spending, vendor payments, procurement, actual revenue, staffing/FTE, capital budget, transportation budget, 2026 supplemental changes, line-item text search, or cross-jurisdiction comparisons.

## Data Model

Snapshot files:

- `agency-by-fund-view.jsonl`: one row per agency and fund view
- `functional-area-by-fund-view.jsonl`: one row per functional area and fund view
- `version-summary.jsonl`: one row per budget version and fund view in the summary report
- `summary.json`: row counts and validation checks
- `provenance.json`: model metadata, query-template hashes, response checksums, and source entities

Fields:

- `biennium`: `2025-27`
- `budget_version`: `Enacted (05-20-2025)`
- `budget_version_filter`: Fiscal WA report filter label
- `fund_view`: `Total Budgeted` or `Outlook Funds (NGF-O)`
- `agency`: Washington state agency label
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

## Analysis Patterns

### Where does Washington budget the most?

Use `agency-by-fund-view.jsonl`, filter to `Total Budgeted`, sort by `budgeted_amount desc`, and state the fund view.

### What is the difference between Total Budgeted and Outlook Funds?

Use the known fund-view totals and explain the accounting boundary. Do not mix the two in one ranking unless the user explicitly asks for a comparison table.

### Functional area questions

Use `functional-area-by-fund-view.jsonl`. This is the closest supported high-level policy grouping in the first Washington snapshot.

### Latest or current questions

Say the current Washington snapshot is the 2025-27 enacted biennial operating budget with model refresh time `2025-07-22T17:18:33.94`. The separate 2026 supplemental report has been probed but is not implemented in this source slice.

## Interpretation Rules

- Use "budgeted amount" or "authorized operating budget," not actual spending.
- State the budget version: `2025-27 enacted`.
- State the fund view, especially when using `Outlook Funds (NGF-O)`.
- Amounts are dollars in the normalized snapshot.
- Do not answer 2026 supplemental changes unless the supplemental snapshot is added.
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
- Caveats: budgeted/authorized operating budget, not actual spending; 2025-27 enacted biennial budget only; not the 2026 supplemental snapshot
```
