---
case: seattle-2026-deficit-jumpstart
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Seattle's approved budgets show the city leaned heavily on JumpStart (the payroll expense tax on large employers) to keep the General Fund growing through 2025-2026: appropriations out of the Payroll Expense Tax fund roughly tripled their "transfer-out" line in FY2025, and General Fund spending kept rising instead of shrinking. The budget data shows this money-movement footprint clearly, but it does not contain the deficit figure itself or the council's policy decision — so this is a **partial** answer: exact numbers on the fund flows, context-only on the "why."

**Numbers** (approved operating budget, City of Seattle):
- Payroll Expense Tax fund (14500) appropriations by year: FY2022 $234M -> FY2023 $319M -> FY2024 $309M -> FY2025 $517M -> FY2026 $427M.
- Inside that fund, Finance General's "Appropriation to Special Funds" line — the mechanism that moves JumpStart money out to support other funds — went $93M (FY2024) -> $297M (FY2025) -> $211M (FY2026).
- General Fund (00100) appropriations: $1.65B (FY2024) -> $1.86B (FY2025, +$213M / +12.9%) -> $2.01B (FY2026).
- JumpStart's original dedicated purposes still show up: Office of Housing is the largest direct recipient at $133M (FY2025) and $142M (FY2026).
- Citywide operating total: $6.11B (FY2024) -> $7.00B (FY2025) -> $7.31B (FY2026).

**How to read this:** These are approved appropriations (spending authority), not actual dollars collected or spent, and the dataset is expenditure-side only — it has no revenue rows and no "deficit" field. What it can show: in FY2025, the year Seattle's widely reported ~$250M-per-year General Fund shortfall had to be closed, the JumpStart fund's appropriations nearly doubled, driven almost entirely by a transfer-out line, while the General Fund grew rather than contracted. That pattern is consistent with the adopted policy of using JumpStart revenue to backfill the General Fund — but the deficit size and the council legislation restructuring JumpStart come from budget documents and reporting, not from this dataset, so treat those as context, not source-backed figures. Housing remained JumpStart's largest dedicated line item; the marginal dollars are what moved. Note the "Appropriation to Special Funds" label does not itself name the General Fund as destination.

A natural next drill-down: which departments' General Fund budgets grew most from FY2024 to FY2026.

**Trace:**
- Source: `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`)
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data-through: FY2018-FY2026 approved budgets; dataset marked "One Time" refresh, current as of June 2026 skill validation
- Grain: fund, fund x department, fund x department x program, fiscal_year
- Measure: sum(`approved_amount`)
- Filters: `fund = "14500 - Payroll Expense Tax"`; `fund = "00100 - General Fund"`; Finance General programs within fund 14500; grouped by fiscal_year
- Validation: FY2026 citywide total returned $7,311,905,121.57 on 7,622 rows — matches the skill's expected check exactly
- Caveats: approved operating budget, not actual spending or actual tax collections; no revenue-side or deficit data exists in any accepted source, so the ~$250M deficit figure and the JumpStart policy restructuring are labeled context, not source-backed claims; fund/program structures change across years (the 14500 fund only appears from FY2022); transfer destinations are not named at this grain.
