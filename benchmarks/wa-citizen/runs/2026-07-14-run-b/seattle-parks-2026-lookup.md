---
case: seattle-parks-2026-lookup
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Seattle's approved 2026 operating budget for Seattle Parks and Recreation is about **$272.6 million** — roughly 3.7% of the city's ~$7.31 billion total operating budget. This covers running the parks system (maintenance crews, recreation and community-center programs, pools, golf, zoo/aquarium support); it does not include the separate capital budget that builds and renovates parks, which this source cannot answer.

**Numbers (FY2026, Seattle Parks and Recreation, approved operating budget):**
- Department total: **$272,607,622**
- Largest programs:
  - Maintenance & Repair — Grounds Crews: $62.5M
  - Recreation Programs & Facility Operations: $42.0M
  - Maintenance & Repair — Shops Crews: $36.0M
  - Citywide / Divisional / Departmental indirect costs (combined): $59.7M
  - Golf Course Programs: $18.4M
  - Aquatic & Swimming Programs: $13.2M
  - Zoo and Aquarium Programs: $9.4M
  - Seattle Conservation Corps: $6.5M
- Offsets (negative rows): CIP Cost Recovery Offset −$1.6M and Indirect Cost Recovery Offset −$9.3M — accounting recoveries, not cuts.

**How to read this:** These are approved operating budget amounts (what the City Council authorized Parks to spend on ongoing operations in fiscal year 2026), not actual spending. The total nets out the offset rows above. Roughly $60M of it is indirect/overhead allocation rather than direct park services. Capital projects (new parks, major renovations, funded largely through the Seattle Park District and CIP) live in a separate capital budget that isn't in this dataset — so the city's full "parks" commitment for 2026 is larger than this operating figure.

A natural next question: how has the Parks operating budget changed since 2018?

**Trace:**
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx` (data.seattle.gov)
- Public URL: https://data.seattle.gov/resource/8u2j-imqx.json ; OpenBudget: https://openbudget.seattle.gov/#!/year/2026/operating/0/department
- Data-through: FY2018–FY2026; one-time annual publication (as of June 2026)
- Grain: department (Seattle Parks and Recreation), drill-down by program
- Measure: sum(`approved_amount`)
- Filters: `fiscal_year=2026 AND department="Seattle Parks and Recreation"` (department name confirmed via LIKE '%PARK%' discovery — it is the only match)
- Validation: FY2026 citywide total returned $7,311,905,121.57 across 7,622 rows, matching the skill's known check; Parks rows = 707
- Caveats: approved operating budget, not actual spending; excludes capital budget (a significant share of parks investment), so this is a partial answer to "what does Seattle budget for parks"; includes ~$60M of indirect-cost allocations; negative rows are cost-recovery offsets.

**Answer mode: partial** — the operating-budget figure is exact from an accepted source, but the parks capital budget frame is not covered by any accepted source here, so the total 2026 parks budget cannot be given.
