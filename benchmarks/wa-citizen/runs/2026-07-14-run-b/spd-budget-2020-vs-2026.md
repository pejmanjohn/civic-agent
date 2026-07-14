---
case: spd-budget-2020-vs-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle's police budget dipped after 2020 — falling about 13% by 2022 — then climbed steadily, and by FY2026 sits at roughly $489M, about $80M (20%) above its FY2020 level.

**Numbers** (approved operating budget, Seattle Police Department):
- FY2020: $408.6M
- FY2021: $363.0M (−$45.6M, −11.2% vs 2020)
- FY2022: $355.5M (low point; −$53.1M, −13.0% vs 2020)
- FY2023: $374.3M
- FY2024: $384.9M
- FY2025: $457.9M
- FY2026: $488.6M (+$80.0M, +19.6% vs 2020)

**How to read this:**
- These are *approved operating budget* amounts, not actual spending — what the City Council authorized, not what SPD ultimately spent.
- Figures are nominal dollars; no inflation adjustment. In real terms the 2026 figure is closer to flat-to-modest growth versus 2020.
- Department structure changed across these years. Notably, some functions that were inside SPD in 2020 (e.g., 911 dispatch/parking enforcement moves around 2021) were shifted to other city units, so part of the 2021-22 drop reflects reorganization, not only cuts — and program-level row structure changed markedly starting FY2023 (row counts jump from ~70 to ~340).
- Related but separate departments (Community Police Commission, Police Relief and Pension) are excluded; this is SPD only.

**Trace:**
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data-through: FY2018–FY2026; dataset refresh "One Time" annual publication, checks current as of June 2026
- Grain: department × fiscal_year
- Measure: sum(`approved_amount`)
- Filters: `department = "Seattle Police Department" AND fiscal_year >= 2020`, grouped by fiscal_year
- Validation: FY2026 SPD total $488.6M matches skill's known check (~$489M); department-name discovery confirmed exact filter value; row counts per year returned (68–358)
- Caveats: approved budget, not actuals; nominal dollars; department reorganizations (functions moved out of SPD ~2021) affect year-over-year comparability; excludes pension and oversight bodies budgeted separately

Natural next question: how much of SPD's FY2026 budget is sworn-officer labor versus non-labor, by program?
