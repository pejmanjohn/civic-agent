---
name: king-county-budget-analyst
description: Use when answering questions about King County, Washington budgeted revenue, budgeted expenditures, departments, FTE, or Open Budget Dashboard year comparisons.
---

# King County Budget Analyst

Use this skill for King County, Washington Open Budget Dashboard questions. It supports questions about budgeted revenue, budgeted expenditures, and budgeted FTE from the checked-in dashboard snapshot.

Do not use this for actual spending, payment/checkbook transactions, actual revenue collected, procurement, personnel rosters, vacancies, realtime county operations, Seattle city budget analysis, Washington state budget analysis, or cross-jurisdiction comparison unless a separate source explicitly supports that question.

## Source Of Truth

- Dataset: King County Open Budget Dashboard
- Provider: King County / Microsoft Power BI Gov
- Official dashboard page: `https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard`
- Power BI report: `https://app.powerbigov.us/view?r=eyJrIjoiOTNmYzYwMDEtNWM5ZC00YjllLThlNzAtZDc1OGRjNzA4MmEwIiwidCI6ImJhZTUwNTlhLTc2ZjAtNDlkNy05OTk2LTcyZGZlOTVkNjljNyJ9`
- Source card: `jurisdictions/king_county/sources/open-budget-dashboard.source.json`
- Snapshot version: `2026-04-01`
- Model refresh time: `2026-04-01T21:37:44.693`
- Snapshot generated from live Power BI replay: see `jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/provenance.json`

For hosted/fresh-agent use, the checked-in snapshot files are available under:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/overview-by-year.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-revenue-expenditure-by-year.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-fte-by-year.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/summary.json
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/provenance.json
```

Treat this as authorized or budgeted dashboard data, not actual spending and not actual revenue earned.

## Safe Answer Patterns

This source can safely support:

- Countywide budgeted revenue and budgeted expenditure totals by dashboard year.
- Countywide budgeted FTE totals by dashboard year.
- FY2026 department-level budgeted revenue and budgeted expenditure rankings.
- FY2026 department-level budgeted FTE rankings.
- Explanations of what the King County Open Budget Dashboard supports and does not prove.
- Chart-ready tables for the supported snapshot grains.

Do not use this source for actual spending, actual revenue collected, transactions, procurement, capital project analysis, staff rosters, vacancies, non-King-County budget analysis, or cross-jurisdiction comparisons.

## Data Model

Snapshot files:

- `overview-by-year.jsonl`: one row per dashboard year
- `department-revenue-expenditure-by-year.jsonl`: FY2026 rows by department
- `department-fte-by-year.jsonl`: FY2026 rows by department
- `summary.json`: row counts and validation checks
- `provenance.json`: model metadata, query-template hashes, response checksums, and source entities

Fields:

- `year`: dashboard budget year
- `department`: King County department label
- `budgeted_revenue`: dashboard revenue value
- `budgeted_expenditure`: dashboard expenditure value
- `budgeted_fte`: dashboard full-time employee value

Primary measures:

```text
sum(budgeted_revenue)
sum(budgeted_expenditure)
sum(budgeted_fte)
```

## Retrieval Strategy

1. Use the checked-in snapshot files as the normal answer source.
2. Use `summary.json` for validation checks before trusting totals.
3. Use `provenance.json` when the answer needs model refresh time, query-template hashes, or Power BI source details.
4. Use the live Power BI extractor only when refreshing the snapshot, not during normal answer generation.
5. If a question asks for an unsupported grain, answer with the supported grains and explain the boundary.

## Query Recipes

### Countywide budgeted revenue, expenditure, and FTE by year

Read:

```text
jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/overview-by-year.jsonl
```

Each row has:

```json
{"year": 2026, "budgeted_revenue": 8865634686, "budgeted_expenditure": 8598795612, "budgeted_fte": 18333}
```

Known checks:

```text
years = 2017-2027
FY2026 budgeted revenue = 8865634686
FY2026 budgeted expenditure = 8598795612
FY2026 budgeted FTE = 18333
```

### FY2026 department budgeted revenue and expenditure

Read:

```text
jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-revenue-expenditure-by-year.jsonl
```

Known checks:

```text
rows = 22
FY2026 department revenue total = 8865634686
FY2026 department expenditure total = 8598795612
```

Largest FY2026 budgeted expenditure rows:

- DCHS - Community and Human Services: $1.624B
- DNRP - Natural Resources and Parks: $1.579B
- MTD - Metro Transit: $1.498B
- KCFiduciary - Fiduciary: $733.4M
- DPH - Public Health: $612.6M
- DHR - Human Resources: $554.6M
- DES - Executive Services: $428.1M
- KCSO - Sheriff's Office: $345.8M

Largest FY2026 budgeted revenue rows:

- DNRP - Natural Resources and Parks: $2.083B
- MTD - Metro Transit: $1.540B
- KCFiduciary - Fiduciary: $1.506B
- DCHS - Community and Human Services: $1.496B
- DPH - Public Health: $520.8M

### FY2026 department budgeted FTE

Read:

```text
jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-fte-by-year.jsonl
```

Known checks:

```text
rows = 21
FY2026 department FTE total = 18333
```

Largest FY2026 budgeted FTE rows:

- MTD - Metro Transit: 6,373
- DNRP - Natural Resources and Parks: 2,435
- DPH - Public Health: 1,710
- KCSO - Sheriff's Office: 1,246
- DES - Executive Services: 1,041
- DAJD - Adult and Juvenile Detention: 944
- DCHS - Community and Human Services: 759

## Analysis Patterns

### Where does King County budget the most?

Use department budgeted expenditure rows for FY2026 unless the user asks for revenue or FTE. Say which grain you used.

### Revenue vs expenditure

Use `overview-by-year.jsonl` for countywide year comparisons and `department-revenue-expenditure-by-year.jsonl` for FY2026 department-level comparison.

### FTE questions

Use budgeted FTE language. Do not describe FTE as employee roster, active headcount, vacancies, payroll, or HR records.

### Trend questions

Use `overview-by-year.jsonl` for countywide trends from 2017-2027. Department-level trend is not supported by the initial snapshot because the reviewed department query is FY2026 only.

### Claim checks

Separate budget facts from interpretation. If a claim uses "spent," "collected," "cut," or "increased," clarify whether the source can answer with budgeted/authorized values only.

## Interpretation Rules

- Use "budgeted expenditure" or "dashboard expenditure budget," not actual spending.
- Use "budgeted revenue" or "dashboard revenue budget," not actual revenue collected.
- Future years such as 2027 are budget years, not completed actuals.
- Department budgets are organizational/accounting views, not complete policy-area spending.
- FTE is budgeted FTE, not a personnel roster or active employee count.
- Do not compare King County to Seattle until accounting definitions and normalized dimensions are explicit.
- Do not infer service quality, policy outcomes, or operational performance from budget rows alone.
- For "latest" questions, use the snapshot version and model refresh time unless explicitly refreshing the source.

## Validation Checks

Known checks from snapshot `2026-04-01`:

- Overview years: 11 rows, 2017-2027
- FY2026 countywide budgeted revenue: $8.866B
- FY2026 countywide budgeted expenditure: $8.599B
- FY2026 countywide budgeted FTE: 18,333
- FY2026 department revenue/expenditure rows: 22
- FY2026 department FTE rows: 21
- FY2026 department revenue total: $8.866B
- FY2026 department expenditure total: $8.599B
- FY2026 department FTE total: 18,333

If a result differs materially, verify the snapshot version, year filter, and whether the user asked for budgeted values or actuals.

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

Keep the user-facing answer short, but make the trace inspectable.

Example trace:

```text
Trace:
- Source: King County Open Budget Dashboard, snapshot 2026-04-01
- Grain: FY2026 department
- Measure: budgeted_expenditure
- Filters/query logic: read department-revenue-expenditure-by-year.jsonl, filter year = 2026, sort by budgeted_expenditure desc
- Check: 22 department rows; FY2026 department expenditure total = $8.599B
- Caveats: budgeted/authorized dashboard values, not actual spending; department budgets are not complete policy-area spending
```
