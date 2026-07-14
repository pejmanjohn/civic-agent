---
case: seattle-2026-deficit-jumpstart
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Seattle's approved budget data shows the fingerprint of how the city handled its projected General Fund shortfall: instead of shrinking, the General Fund grew sharply in 2025-2026, while appropriations out of the JumpStart Payroll Expense Tax fund — especially transfer-style "Appropriation to Special Funds" lines — roughly tripled in 2025. In plain terms, the budget was balanced largely by leaning on JumpStart payroll-tax money to support general government, not by cutting the General Fund. The deficit's exact size and the policy mechanics, however, live in city budget documents, not in this dataset — so this is a **partial** answer.

**Numbers** (approved operating budget, Socrata `8u2j-imqx`):

- General Fund (00100) appropriations: 2024 $1.651B → 2025 $1.864B (+$213M, +12.9%) → 2026 $2.011B (+$146M, +7.9%). No General Fund contraction appears.
- JumpStart fund (14500 - Payroll Expense Tax) appropriations: 2022 $234M → 2023 $319M → 2024 $309M → **2025 $517M** → 2026 $427M.
- Inside the JumpStart fund, Finance General's "Appropriation to Special Funds" program (transfers out of the fund): 2024 $93.4M → **2025 $296.9M** → 2026 $211.2M. That 2025 spike is the single largest change in the fund.
- JumpStart's original priorities still show up: Office of Housing $132.8M (2025) and $142.5M (2026); Office of Economic Development ~$20-24M; Office of Planning and Community Development ~$23M; Office of Sustainability and Environment ~$12M each year. Department of Education and Early Learning drops from $13.9M (2025) to $0 (2026).
- Citywide operating total: 2024 $6.107B → 2025 $7.003B → 2026 $7.312B.

**How to read this:** These are approved appropriations (spending authority), not revenues or actual spending, so the dataset cannot show the deficit itself ("deficit" is a revenue-vs-cost projection) or name the destination of the JumpStart transfers. What it can show is that JumpStart-fund spending authority surged in 2025, that most of the surge sits in Finance General transfer appropriations rather than program spending, and that the General Fund kept growing — a pattern consistent with the city's publicized 2025-2026 approach of using JumpStart payroll-tax revenue to support the General Fund. For the official narrative (the projected ~$250M gap, position reductions, and the Council's revised JumpStart fund policy), consult the City Budget Office's 2025-2026 Adopted Budget documents at seattle.gov/city-budget-office — that source is not yet in this repo's accepted registry, which is why this answer is partial rather than exact.

**Trace:**
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx` (`https://data.seattle.gov/resource/8u2j-imqx.json`; OpenBudget: `https://openbudget.seattle.gov/#!/year/2026/operating/0/department`)
- Data-through: FY2018-FY2026 approved budgets; metadata refresh "One Time" (annual/static publication, known years as of June 2026)
- Grain: fund x fiscal_year; drill-downs at fund x department and fund x department x program
- Measure: sum(`approved_amount`)
- Filters: `fund="14500 - Payroll Expense Tax"`; `fund="00100 - General Fund"`; Finance General program split within fund 14500; citywide totals ungrouped by year
- Validation: FY2026 citywide total $7.312B on 7,622 rows matches the skill's known check ($7.312B / 7,622 rows); JumpStart fund rows = 642 across all years
- Caveats: approved budget, not actuals or revenue; the dataset has no deficit figure and does not identify transfer destinations — "Appropriation to Special Funds" is inferred to include General Fund support but is not labeled as such; department/program structures change across years (e.g., DEEL's JumpStart line going to $0 in 2026 may reflect fund restructuring, not a program cut); policy interpretation (deficit closure mechanics, Council's JumpStart policy change) is separated from budget facts and requires official budget documents.

**Answer mode: partial** — fund-level budget facts are exact from the accepted source; the deficit-closure narrative and JumpStart policy change need the City Budget Office adopted-budget documents, which are the named path.
