---
case: seattle-parks-2026-lookup
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle's approved 2026 operating budget for Seattle Parks and Recreation is about **$272.6 million** — roughly 3.7% of the city's $7.31 billion FY2026 operating budget, and up about $13.9 million (+5.4%) from FY2025.

**Numbers:**
- Seattle Parks and Recreation, FY2026 approved operating budget: **$272,607,622**
- FY2025 comparison: $258,737,397 → change of +$13.9M (+5.4%)
- Labor vs Non-Labor split (FY2026): Labor $191.2M, Non-Labor $81.4M
- Largest FY2026 programs within Parks:
  - Maintenance & Repair Grounds Crews: $62.5M
  - Recreation Programs & Facility Ops: $42.0M
  - M&R Shops Crews: $36.0M
  - Citywide Indirect Costs: $22.6M
  - Divisional Indirect Costs: $19.6M
  - Golf Course Programs: $18.4M
  - Aquatic & Swimming Programs: $13.2M

**How to read this:**
This is the approved *operating* budget at the department grain — what the city authorized Seattle Parks and Recreation to spend on day-to-day operations in fiscal year 2026. It is not actual spending, and it excludes the *capital* budget (building or renovating parks facilities is budgeted separately and not covered by this source). About 70% of the parks operating budget is labor. Several "Indirect Costs" programs (~$59.7M combined) are internal cost allocations rather than direct resident-facing park services. Program names and structure can change year to year, so the FY2025→FY2026 comparison is at the department total, which is stable.

**Trace:**
- Source: `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`)
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget view: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data-through: FY2018–FY2026 annual budget publication (static, "One Time" refresh; known years as of June 2026)
- Grain: department (Seattle Parks and Recreation), with program and Labor/Non-Labor drill-downs
- Measure: sum(`approved_amount`)
- Filters: `fiscal_year=2026 AND department="Seattle Parks and Recreation"` (department name discovered via `%PARK%` match — exactly one match); FY2025 queried the same way for comparison
- Validation: FY2026 citywide total returned $7,311,905,121.57 across 7,622 rows, matching the skill's expected check exactly; Parks FY2026 = 707 rows
- Caveats: approved operating budget, not actual spending; excludes capital budget; includes internal cost allocations; labor/non-labor is a coarse split

Natural next question: do you want the capital side too (park construction and major maintenance)? That's budgeted separately and this source can't answer it.
