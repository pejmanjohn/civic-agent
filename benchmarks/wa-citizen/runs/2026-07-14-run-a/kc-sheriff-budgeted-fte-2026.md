---
case: kc-sheriff-budgeted-fte-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** The King County Sheriff's Office (KCSO) has **1,246 budgeted FTEs (full-time equivalents)** in the 2026 budget, per the King County Open Budget Dashboard. That is the county's official staffing measure for the budget; the dashboard publishes budgeted FTE, not a raw "position count."

**Numbers:**
- KCSO budgeted FTE, FY2026: **1,246**
- Countywide budgeted FTE, FY2026: 18,333 (KCSO is about 6.8% of the county total)
- For context, KCSO is the 4th-largest department by budgeted FTE, behind Metro Transit (6,373), Natural Resources and Parks (2,435), and Public Health (1,710)
- KCSO FY2026 budgeted expenditure: $345.8M

**How to read this:**
- "Budgeted FTE" is the authorized staffing level in the adopted budget, expressed as full-time equivalents. It is not an employee roster, active headcount, or vacancy report — actual filled positions on any given day can be lower.
- If you specifically need a count of authorized *positions* (which can exceed FTE when part-time positions exist), that grain lives in the county's adopted budget book, not this dashboard; the FTE figure is the accepted source-backed answer here.
- This is annual FY2026 dashboard data. The council adopted a two-year 2026–2027 budget ($20.16B biennial); do not mix the annual dashboard figures with biennial headlines.

**Trace:**
- Source: `king_county.open_budget_dashboard`, snapshot 2026-04-01 (model refresh 2026-04-01T21:37:44)
- Public source: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
- Data file: `/Users/pejman/code/civic-agent/jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-fte-by-year.jsonl`
- Grain: FY2026 department
- Measure: `budgeted_fte`
- Filters/query logic: filter `year = 2026`, `department = "KCSO - Sheriff's Office"`
- Check: passed — 21 department FTE rows; FY2026 department FTE total = 18,333 (matches skill validation checks)
- Caveats: budgeted/authorized FTE, not filled positions or headcount; "positions" as a distinct count is not in this source; department view is organizational, not complete public-safety spending/staffing
