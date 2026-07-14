---
case: spd-budget-2020-vs-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle Police Department's approved operating budget fell sharply after 2020 — bottoming out in 2022 about 13% below the 2020 level — then climbed steadily, and by 2026 sits about $80 million (roughly 20%) above where it was in 2020.

**Numbers** (approved operating budget, sum by fiscal year):
- FY2020: $408.6M
- FY2021: $363.0M (−$45.6M, −11.2% vs 2020)
- FY2022: $355.5M (low point; −$53.1M, −13.0% vs 2020)
- FY2023: $374.3M
- FY2024: $384.9M
- FY2025: $457.9M
- FY2026: $488.6M (+$80.0M, +19.6% vs 2020)

**How to read this:** These are approved (adopted) operating budget amounts, not actual spending, at the department grain. The 2021-2022 dip is not only a cut: functions also moved out of SPD organizationally. Notably, 911 dispatch left SPD for the new Community Safety and Communications Center (FY2021 budget $17.9M), whose successor, Community Assisted Response and Engagement (CARE), has a $68.6M budget in FY2026. Parking enforcement similarly moved out of and later back into SPD during this window. So the "SPD" line covers a somewhat different set of functions in different years, and part of the post-2023 rebound reflects functions returning plus wage settlements, not purely expanded policing. Dollars are nominal — not inflation-adjusted — and about $80M of growth over six inflationary years is modest in real terms.

**Trace:**
- Source: `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`)
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data-through: FY2018-FY2026; live query at answer time (dataset refresh cadence: one-time annual publication; last skill validation June 2026)
- Grain: department x fiscal_year
- Measure: sum(`approved_amount`)
- Filters: `department = "Seattle Police Department" AND fiscal_year >= 2020`, grouped by fiscal_year; supplementary queries on CSCC and CARE departments for scope-change context
- Check: FY2026 SPD total $488.6M matches the skill's known-largest-departments check (~$489M); row counts per year 68-358, consistent with dataset structure change in FY2023
- Caveats: approved operating budget, not actual spending; nominal dollars; department scope changed across years (911 dispatch/CSCC/CARE, parking enforcement moves), so year-over-year totals are not a fully like-for-like comparison; no staffing/headcount data in this source

Natural next drill-down: which SPD programs drove the FY2024-to-FY2026 increase?
