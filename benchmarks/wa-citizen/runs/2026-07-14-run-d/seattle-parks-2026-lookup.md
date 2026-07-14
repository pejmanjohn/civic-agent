---
case: seattle-parks-2026-lookup
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** Seattle's approved 2026 operating budget for Seattle Parks and Recreation is about **$272.6 million** — roughly 3.7% of the city's $7.31 billion total operating budget.

**Numbers:**
- Seattle Parks and Recreation, FY2026 approved operating budget: **$272,607,622**
- Citywide FY2026 operating total (for scale): $7,311,905,122
- Largest programs inside Parks (FY2026):
  - M&R Grounds Crews (grounds maintenance): $62.5M
  - Rec Programs & Facility Ops: $42.0M
  - M&R Shops Crews: $36.0M
  - Citywide Indirect Costs: $22.6M
  - Divisional Indirect Costs: $19.6M
  - Golf Course Programs: $18.4M
  - Departmental Indirect Costs: $17.6M
  - Aquatic & Swimming Programs: $13.2M

**How to read this:** This is the approved *operating* budget at the department grain — the money authorized for running parks, recreation centers, pools, golf courses, and related programs in 2026. It is not actual spending, and it excludes the capital budget (building or renovating parks facilities), which lives in a separate budget frame not covered by this source. Roughly $60M of the total sits in "indirect cost" programs (overhead allocations), so not every dollar is direct resident-facing service. Separately funded parks money can also flow through other entities (e.g., the Seattle Park District levy), so the department's operating line is not the city's entire parks story.

**Trace:**
- **Source:** `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`)
- **Public URL:** https://data.seattle.gov/resource/8u2j-imqx.json (browse: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- **Data-through:** FY2018–FY2026 annual budget publication (static, refresh "One Time"); queried live 2026-07-14
- **Grain:** department (drill-down at program)
- **Measure:** sum(`approved_amount`)
- **Filters:** `fiscal_year = 2026 AND department = "Seattle Parks and Recreation"` (707 rows); the only department matching "park" in the dataset
- **Validation check:** citywide FY2026 total returned $7,311,905,121.57 across 7,622 rows — exact match to the skill's expected check
- **Caveats:** approved operating budget, not actual spending; capital budget excluded; indirect-cost programs inflate the "service" reading; Park District and other funds outside this department line are not included

Natural next question: how has the Parks budget changed since 2018?
