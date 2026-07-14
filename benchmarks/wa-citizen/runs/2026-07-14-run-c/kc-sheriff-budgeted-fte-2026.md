---
case: kc-sheriff-budgeted-fte-2026
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
King County's Open Budget Dashboard shows the King County Sheriff's Office (KCSO) with **1,246 budgeted FTE (full-time equivalents) in the 2026 budget**. The accepted source measures staffing in budgeted FTE, not a raw count of authorized positions, so if you need the literal position count (which can exceed FTE when part-time positions are included), that number lives in the adopted budget book itself — hence this is a partial rather than exact answer to "how many positions."

**Numbers:**
- KCSO FY2026 budgeted FTE: **1,246**
- Countywide FY2026 budgeted FTE: 18,333 (KCSO is about 6.8% of the county total)
- For scale: KCSO is the 4th-largest county department by budgeted FTE, behind Metro Transit (6,373), Natural Resources and Parks (2,435), and Public Health (1,710), and its FY2026 budgeted expenditure is about $345.8M.

**How to read this:**
Budgeted FTE is the staffing level the County Council authorized in the budget — it is not an employee roster, active headcount, or vacancy report. One FTE equals one full-time position's worth of hours, so 1,246 FTE could map to slightly more individual positions if any are part-time. Actual filled staffing at any moment will differ from the budgeted figure. Note also that King County adopted a two-year (2026–2027) budget; this FTE figure is the dashboard's annual 2026 view.

**Trace:**
- Source: `king_county.open_budget_dashboard` (King County Open Budget Dashboard)
- Public source: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
- Snapshot: 2026-04-01 (model refresh 2026-04-01T21:37:44.693); data covers dashboard years 2017–2027
- Grain: FY2026 department
- Measure: budgeted_fte
- Filters/query logic: read `jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-fte-by-year.jsonl`, filter year = 2026, department = "KCSO - Sheriff's Office"
- Check: 21 department FTE rows; FY2026 department FTE total = 18,333 — both match the skill's validation checks
- Caveats: budgeted FTE, not authorized position count, roster, or vacancies; annual dashboard frame, not the $20.16B adopted 2026–2027 biennial frame; for a literal position list, consult the adopted 2026–2027 budget documents

Answer mode: **partial** — the source supports FY2026 budgeted FTE exactly (1,246), but "positions" as a distinct count is not a measure the accepted source carries.
