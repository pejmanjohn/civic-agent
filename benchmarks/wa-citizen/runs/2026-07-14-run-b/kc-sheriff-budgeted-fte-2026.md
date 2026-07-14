---
case: kc-sheriff-budgeted-fte-2026
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** The King County Sheriff's Office (KCSO) has 1,246 budgeted full-time-equivalent (FTE) positions in the 2026 budget, according to King County's official Open Budget Dashboard.

**Numbers:**
- KCSO budgeted FTE, FY2026: **1,246**
- That is about 6.8% of the countywide FY2026 budgeted total of 18,333 FTE.
- For context, KCSO is the county's 4th-largest department by budgeted FTE, behind Metro Transit (6,373), Natural Resources and Parks (2,435), and Public Health (1,710).

**How to read this:** This is *budgeted FTE* — the staffing level authorized in the budget — not a personnel roster, active headcount, or vacancy count. "Positions" in budget documents are expressed as FTE, so a mix of full- and part-time roles can add up to 1,246 FTE. It also does not tell you how many deputies versus civilian staff, or how many positions are currently filled. Note this covers the Sheriff's Office as an organizational unit; other public-safety functions (e.g., Adult and Juvenile Detention, at 944 FTE) are budgeted separately.

**Trace:**
- Source: King County Open Budget Dashboard, snapshot 2026-04-01 (model refresh 2026-04-01T21:37:44)
- Public source: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
- Snapshot file: jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/normalized/department-fte-by-year.jsonl
- Grain: FY2026 department
- Measure: budgeted_fte
- Filters/query logic: filter year = 2026, department = "KCSO - Sheriff's Office"
- Check: 21 department FTE rows; FY2026 department FTE total = 18,333 (matches skill validation checks); KCSO row = 1,246 (matches known check)
- Caveats: budgeted/authorized FTE, not filled positions or headcount; annual dashboard frame, not the adopted 2026-2027 biennial budget document; does not break out sworn vs civilian positions

**Answer mode: exact** — the source directly supports FY2026 department-level budgeted FTE for KCSO, with the caveat that "positions" is answered as budgeted FTE.
