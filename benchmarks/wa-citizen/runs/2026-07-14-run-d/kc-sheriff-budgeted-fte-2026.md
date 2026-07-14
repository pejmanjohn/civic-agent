---
case: kc-sheriff-budgeted-fte-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** The King County Sheriff's Office (KCSO) has **1,246 budgeted full-time-equivalent (FTE) positions** in the 2026 budget, per the county's official Open Budget Dashboard. Note the measure: you asked about "positions," and the accepted source answers in budgeted FTE — the county's official staffing measure for the budget. One FTE equals one full-time position's worth of budgeted hours (two half-time positions count as one FTE), so the count of individual people or job slots could differ slightly.

**Numbers:**
- KCSO FY2026 budgeted FTE: **1,246**
- For scale: that is about 6.8% of King County's total FY2026 budgeted FTE of 18,333
- KCSO ranks 4th among county departments by budgeted FTE, behind Metro Transit (6,373), Natural Resources and Parks (2,435), and Public Health (1,710)

**How to read this:** This is the authorized staffing level in the adopted budget — how many FTE the county budgeted for the Sheriff's Office in 2026. It is not an active-employee roster, headcount of people, vacancy report, or payroll record; actual filled positions on any given day can be lower (or occasionally structured differently) than budgeted FTE. It also reflects the annual 2026 dashboard year, not the biennial 2026–2027 adopted budget frame.

**Trace:**
- **Source:** `king_county.open_budget_dashboard` (King County Open Budget Dashboard)
- **Public source:** https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
- **Snapshot:** 2026-04-01 (Power BI model refresh 2026-04-01T21:37:44.693); data through dashboard year 2027
- **Grain:** FY2026 department
- **Measure:** `budgeted_fte`
- **Filters/query logic:** read `jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-fte-by-year.jsonl`, filter year = 2026 and department = "KCSO - Sheriff's Office"
- **Check:** passed — 21 department FTE rows and FY2026 department FTE total = 18,333, both matching the skill's known validation checks; KCSO row (1,246) matches the documented ranking
- **Caveats:** budgeted FTE, not headcount, roster, or vacancies ("positions" answered at the source's official FTE measure, labeled above); annual dashboard-year value, not the biennial adopted-budget frame; department view is an organizational/accounting cut, not complete public-safety spending or staffing
