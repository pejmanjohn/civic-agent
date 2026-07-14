---
case: spd-budget-2020-vs-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle's approved police operating budget dipped after 2020 — falling to a low of about $355M in 2022 — then climbed steadily, and by 2026 it is about $489M, roughly $80M (about 20%) higher in nominal dollars than the $409M approved for 2020.

**Numbers** (Seattle Police Department, approved operating budget by fiscal year):
- FY2020: $408.6M
- FY2021: $363.0M (−11.2% vs 2020)
- FY2022: $355.5M (low point, −13.0% vs 2020)
- FY2023: $374.3M
- FY2024: $384.9M
- FY2025: $457.9M
- FY2026: $488.6M (+$80.0M, +19.6% vs 2020)

**How to read this:** These are approved operating budget amounts (what the City Council authorized), not actual spending, and they are nominal dollars — no inflation adjustment, because no accepted inflation source is composed here. The 2021-2022 drop partly reflects reorganization, not only cuts: after 2020, Seattle moved functions such as parking enforcement and 911 dispatch out of SPD into other units (e.g., the Community Safety and Communications Center), so SPD's line shrinks even where the city still funds those services elsewhere. The later rebound includes wage settlements and hiring/retention spending. The row-count jump in 2023 (68-69 rows to ~341) signals a budget-structure change in how SPD lines are published, which is another reason to read year-over-year shifts as department-as-labeled, not a constant-scope organization.

**Trace:**
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data-through: annual/static publication covering FY2018-FY2026 (skill snapshot as of June 2026); live API queried at answer time
- Grain: department x fiscal_year
- Measure: sum(`approved_amount`)
- Filters: `department = "Seattle Police Department"` AND `fiscal_year >= 2020`, grouped by fiscal_year
- Validation check: FY2026 SPD total returned $488.6M, matching the skill's known check of "Seattle Police Department: about $489M"; row counts per year 68-358
- Caveats: approved budget, not actuals; nominal dollars, no inflation adjustment; department scope changed after 2020 (functions moved out of SPD), so the trend is not a constant-scope comparison; negative/offset rows are included in net totals
- Recipe/mode: `budget_scale.trend`, answer mode `exact` (nominal single-source trend with stated scope caveats)

Natural next question: which SPD programs drove the 2025-2026 increases?
