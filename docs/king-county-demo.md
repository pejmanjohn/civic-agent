# King County Demo Answer Traces

This demo shows the intended Civic Agent answer style for King County Open Budget Dashboard questions. It uses the checked-in snapshot generated from the official Power BI Gov dashboard and focuses on authorized or budgeted values, not actual spending or actual revenue earned.

All examples below use:

- Source: King County Open Budget Dashboard
- Snapshot: `2026-04-01`
- Model refresh time: `2026-04-01T21:37:44.693`
- Accessed: 2026-06-04
- Measures: `budgeted_revenue`, `budgeted_expenditure`, `budgeted_fte`
- Caveat: this is budget dashboard data, not actual spending, payments, actual revenue collected, or personnel roster data

## 1. What does King County's budget look like by year?

Conclusion: In FY2026, the dashboard snapshot shows about $8.87B in budgeted revenue, $8.60B in budgeted expenditures, and 18,333 budgeted FTE. The snapshot includes dashboard years 2017-2027.

Numbers:

| Year | Budgeted revenue | Budgeted expenditure | Budgeted FTE |
|---:|---:|---:|---:|
| 2017 | $4.61B | $4.58B | 13,990 |
| 2024 | $6.92B | $7.44B | 17,006 |
| 2025 | $8.19B | $8.63B | 17,636 |
| 2026 | $8.87B | $8.60B | 18,333 |
| 2027 | $9.11B | $8.85B | 18,490 |

How to read this: These are dashboard budget years. Future-year values are budgeted values, not completed actuals.

Trace:

- Source: King County Open Budget Dashboard
- Snapshot: `2026-04-01`
- Grain: dashboard year
- Measure: budgeted revenue, budgeted expenditure, budgeted FTE
- Filters/query logic: read `overview-by-year.jsonl`, sort by `year`
- Check: 11 year rows; FY2026 budgeted revenue = $8.866B; FY2026 budgeted expenditure = $8.599B
- Caveats: budgeted/authorized dashboard values, not actual spending or actual revenue earned

## 2. Which King County departments have the largest FY2026 budgeted expenditures?

Conclusion: In FY2026, the largest department-level budgeted expenditures in this snapshot are Community and Human Services, Natural Resources and Parks, and Metro Transit.

Numbers:

| Department | Budgeted expenditure | Budgeted revenue |
|---|---:|---:|
| DCHS - Community and Human Services | $1.62B | $1.50B |
| DNRP - Natural Resources and Parks | $1.58B | $2.08B |
| MTD - Metro Transit | $1.50B | $1.54B |
| KCFiduciary - Fiduciary | $733.4M | $1.51B |
| DPH - Public Health | $612.6M | $520.8M |
| DHR - Human Resources | $554.6M | $503.1M |
| DES - Executive Services | $428.1M | $423.3M |
| KCSO - Sheriff's Office | $345.8M | $204.3M |

How to read this: Department budgets are organizational/accounting views. They are not complete policy-area spending totals.

Trace:

- Source: King County Open Budget Dashboard
- Snapshot: `2026-04-01`
- Grain: FY2026 department
- Measure: `budgeted_expenditure`
- Filters/query logic: read `department-revenue-expenditure-by-year.jsonl`, filter `year = 2026`, sort by `budgeted_expenditure desc`
- Check: 22 department rows; FY2026 department expenditure total = $8.599B
- Caveats: budgeted/authorized dashboard values, not actual spending; department budgets are not complete policy-area spending

## 3. Which King County departments have the most FY2026 budgeted FTE?

Conclusion: Metro Transit has the largest FY2026 budgeted FTE in this snapshot, followed by Natural Resources and Parks, Public Health, the Sheriff's Office, and Executive Services.

Numbers:

| Department | Budgeted FTE |
|---|---:|
| MTD - Metro Transit | 6,373 |
| DNRP - Natural Resources and Parks | 2,435 |
| DPH - Public Health | 1,710 |
| KCSO - Sheriff's Office | 1,246 |
| DES - Executive Services | 1,041 |
| DAJD - Adult and Juvenile Detention | 944 |
| DCHS - Community and Human Services | 759 |
| DLS - Local Services | 582 |

How to read this: FTE here is budgeted FTE from the dashboard, not an employee roster, active headcount, vacancy report, or payroll source.

Trace:

- Source: King County Open Budget Dashboard
- Snapshot: `2026-04-01`
- Grain: FY2026 department
- Measure: `budgeted_fte`
- Filters/query logic: read `department-fte-by-year.jsonl`, filter `year = 2026`, sort by `budgeted_fte desc`
- Check: 21 department FTE rows; FY2026 department FTE total = 18,333
- Caveats: budgeted FTE only; not personnel records, vacancies, payroll, or actual staffing

## 4. What does this dashboard not prove?

Conclusion: The snapshot supports budgeted revenue, budgeted expenditure, and budgeted FTE claims at the listed grains. It does not prove actual spending, actual revenue collected, procurement activity, staffing rosters, service quality, or policy outcomes.

Unsupported claims:

- "King County spent $X" when the claim means actual payments or actual expenditures.
- "King County collected $X" when the claim means actual revenue earned.
- Employee rosters, vacancies, payroll, or active headcount.
- Capital project conclusions from the deferred map/project entities.
- Seattle-vs-King-County comparisons without explicit accounting mappings.

Trace:

- Source: King County source card `king_county.open_budget_dashboard`
- Snapshot: `2026-04-01`
- Grain: source scope and caveats
- Measure: supported/unsupported answer patterns
- Filters/query logic: read `open-budget-dashboard.source.json`, `summary.json`, and `provenance.json`
- Check: source card lists unsupported claims and validation checks
- Caveats: narrow dashboard source; not broad King County public-finance coverage
