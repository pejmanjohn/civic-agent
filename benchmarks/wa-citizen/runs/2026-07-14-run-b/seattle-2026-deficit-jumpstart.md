---
case: seattle-2026-deficit-jumpstart
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Seattle's approved budget data shows a pattern consistent with the widely reported deficit fix: instead of cutting the General Fund — which actually grew about $360 million from FY2024 to FY2026 — the city leaned on the JumpStart payroll tax. Appropriations out of the JumpStart fund roughly doubled in FY2025, and the fastest-growing piece was not housing or economic development but a "Finance General – Appropriation to Special Funds" line (interfund transfers), which tripled from about $93M to $297M. That is the budget-data footprint of JumpStart money being redirected to backfill general government, while the fund's original earmarks (housing) held roughly flat rather than growing with the tax.

**Numbers** (approved operating budget, sum of `approved_amount`):

General Fund (00100) appropriations:
- FY2024: $1.651B
- FY2025: $1.864B (+$213M, +12.9%)
- FY2026: $2.011B (+$146M, +7.9%)

JumpStart / Payroll Expense Tax fund (14500) appropriations:
- FY2022: $234M (first year in this dataset)
- FY2023: $319M
- FY2024: $309M
- FY2025: $517M (+67% year over year)
- FY2026: $427M

Inside the JumpStart fund, Finance General "Appropriation to Special Funds" (transfers out to other funds):
- FY2024: $93.4M
- FY2025: $296.9M
- FY2026: $211.2M

Meanwhile, Office of Housing spending from the JumpStart fund stayed essentially flat: $142.3M (FY2024) → $142.5M (FY2026). Other FY2026 JumpStart-funded departments: Economic Development $23.9M, Planning & Community Development $23.2M, Sustainability & Environment $12.5M.

**How to read this:** This is approved operating budget (appropriations), not actual spending or tax collections, at the fund/department/program grain. The dataset shows money appropriated *out of* the JumpStart fund; it labels the big FY2025-FY2026 transfer line only as "Appropriation to Special Funds" and does not name the receiving fund, so I cannot confirm from this source alone that those transfers went specifically to the General Fund — only that large JumpStart transfers-out and General Fund growth happened together. The policy mechanics (the size of the projected General Fund deficit, and the 2024 council legislation loosening JumpStart's spending-plan earmarks) are not in any accepted source in this repo; treat my first sentence's framing as interpretation layered on the fund-level facts. This is why the answer mode is **partial**: the fund-flow numbers are exact and source-backed, but the deficit size and the legal redirection mechanism would need the City Budget Office's adopted-budget documents (seattle.gov/city-budget-office) to be fully sourced.

**Answer mode: partial.**

**Trace:**
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data-through: FY2018-FY2026 approved budget; metadata refresh "One Time" (static annual publication, known years as of June 2026)
- Grain: fund by fiscal_year; department and program drill-downs within fund `14500 - Payroll Expense Tax` and fund `00100 - General Fund`
- Measure: sum(`approved_amount`)
- Filters: `fund="14500 - Payroll Expense Tax"` grouped by fiscal_year/department/program; `fund="00100 - General Fund"` grouped by fiscal_year
- Validation check: FY2026 citywide total $7,311,905,121.57 across 7,622 rows — matches the skill's expected check exactly
- Caveats: approved appropriations, not actual spending or revenue collected; the Payroll Expense Tax fund first appears in FY2022 (the tax began collections in 2021); "Appropriation to Special Funds" destination fund is not identified in this dataset; deficit size and JumpStart-flexibility legislation are outside accepted sources; fund/program names can change across years.
