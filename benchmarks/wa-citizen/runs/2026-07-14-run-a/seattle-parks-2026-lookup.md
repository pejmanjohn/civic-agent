---
case: seattle-parks-2026-lookup
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle's approved 2026 operating budget for Seattle Parks and Recreation is about **$272.6 million** — roughly 3.7% of the city's ~$7.31 billion total operating budget. Most of it goes to maintaining parks and grounds and running recreation facilities and programs.

**Numbers (FY2026, Seattle Parks and Recreation, by program):**
- Department total: **$272,607,622**
- M&R Grounds Crews (parks/grounds maintenance): $62.5M
- Rec Programs & Facility Ops: $42.0M
- M&R Shops Crews: $36.0M
- Citywide Indirect Costs: $22.6M
- Divisional Indirect Costs: $19.6M
- Golf Course Programs: $18.4M
- Departmental Indirect Costs: $17.6M
- Aquatic & Swimming Programs: $13.2M
- M&R Specialty Crews: $12.2M
- Zoo and Aquarium Programs: $9.4M
- All other programs (net): ~$18.9M — includes partnerships, Seattle Conservation Corps, pooled benefits, and two negative offset rows (CIP Cost Recovery −$1.6M, Indirect Cost Recovery −$9.3M)

**How to read this:** This is the *approved operating budget* for the department named "Seattle Parks and Recreation" — money authorized to be spent, not actual spending. It excludes the capital budget (new park construction and major renovations live there). Roughly a quarter of the total is indirect/overhead cost allocation rather than direct park services, and the two negative rows are accounting offsets (cost recoveries), not errors. Grain used: department, drilled into programs.

A natural next question: how has the Parks budget changed since 2018?

**Trace:**
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- Data version: live API query at answer time; dataset covers FY2018–FY2026, refresh "One Time" (annual/static publication)
- Grain: department → program
- Measure: sum(`approved_amount`)
- Filters: `fiscal_year=2026 AND department="Seattle Parks and Recreation"` (department name discovered via `upper(department) like '%PARK%'`; single match)
- Validation: FY2026 citywide total returned $7,311,905,121.57 across 7,622 rows, matching the skill's known check (~$7.312B, 7,622 rows). Parks FY2026 = 707 rows.
- Caveats: approved operating budget, not actual spending; capital projects excluded; indirect-cost and offset rows included in the net total; program names/structure can change across years.
