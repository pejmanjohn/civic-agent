---
case: spd-budget-2020-vs-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle Police Department's approved operating budget dipped sharply in 2021–2022, then climbed back and beyond: from $408.6M in 2020 to $488.6M in 2026 — up about $80M (+19.6%) in nominal dollars, with most of the growth arriving in the 2025 and 2026 budgets.

**Numbers** (SPD approved operating budget by fiscal year):

| Fiscal year | Approved budget | Change vs prior year |
|---|---|---|
| 2020 | $408.6M | — |
| 2021 | $363.0M | −$45.6M (−11.2%) |
| 2022 | $355.5M | −$7.5M (−2.1%) |
| 2023 | $374.3M | +$18.8M (+5.3%) |
| 2024 | $384.9M | +$10.6M (+2.8%) |
| 2025 | $457.9M | +$72.9M (+19.0%) |
| 2026 | $488.6M | +$30.7M (+6.7%) |

- 2020 → 2026: **+$80.0M, +19.6%** (nominal, not inflation-adjusted)
- Low point: 2022 ($355.5M); 2022 → 2026: +$133.1M (+37.4%)

**How to read this:** These are approved operating budget amounts (department grain), not actual spending, staffing, or capital dollars. The 2021–2022 decline is not purely a cut to policing: Seattle reorganized public-safety functions in that period — the dataset shows a separate "Community Safety and Communications Center" department appearing in 2021 (~$17.9M–$22.2M/yr through 2024) that took over functions previously budgeted inside SPD, and that department has no 2025–2026 rows, so some of the 2025 jump likewise reflects restructuring rather than pure growth. Attributing exactly which functions moved when requires ordinance/council-action context beyond this budget table. Figures are nominal; a fair "real" trend would need an inflation adjustment this source does not provide. SPD remains the city's largest non-utility department budget in FY2026.

A chart of this series is available on request; the table above carries the full trend.

**Trace:**
- **Source:** `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`)
- **Public URL:** https://data.seattle.gov/resource/8u2j-imqx.json (dashboard: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- **Data-through:** FY2026 (annual publication; FY2027 expected with the fall 2026 budget cycle; card observed 2026-07-13; live Socrata query at answer time)
- **Grain:** department × fiscal_year
- **Measure:** sum(`approved_amount`)
- **Filters:** `department = "Seattle Police Department"` AND `fiscal_year >= 2020`, grouped by fiscal_year
- **Validation:** FY2026 SPD total $488.6M matches the skill's known check (~$489M); FY2020–FY2026 row counts 83/68/69/341/341/355/358 per year
- **Caveats:** approved operating budget, not actual spending; nominal dollars, no inflation adjustment; department reorganizations (e.g., CSCC split out 2021–2024, absent 2025–2026) affect cross-year comparability; excludes capital budget and related-but-separate departments (Community Police Commission, Office of Inspector General for Public Safety, Police Relief and Pension)

Natural next drill-down: which SPD programs drove the 2025–2026 increases.
