---
case: kc-actuals-vs-budget-trap
surface: repo-skills
answer_mode: side_by_side_only
session: fresh
---

**Conclusion:** There is no accepted apples-to-apples source that says whether King County spent exactly what it budgeted in 2025. What I can show you, side by side, is what King County *budgeted* for 2025 (about $8.63 billion) and what it *reported actually spending* in its filed 2025 financials (about $5.86 billion). Those two numbers come from different accounting frames and must not be subtracted to get an "underspend" — the gap is mostly definitional, not money left on the table.

**Numbers (side by side, not a variance):**

| Frame | 2024 | 2025 |
|---|---|---|
| Budgeted expenditure (KC Open Budget Dashboard, annual) | $7,441,147,541 | $8,626,613,762 |
| Filed actual expenditures (State Auditor FIT, excludes internal service funds) | $5,312,711,000 | $5,860,085,000 |

Filed actual revenues for 2025 were $6,476,448,000 — the county took in more than it reported spending on this basis, as it has every year in the series.

**How to read this:** The dashboard figure is budget authority — permission to spend across county funds, including appropriations that routinely go unspent or carry over (capital timing, reserves). The FIT figure is what the county actually reported spending, but on the Auditor's headline basis, which excludes internal service funds and uses different fund/accounting scoping than the budget dashboard. Because the two frames count different things, "budgeted $8.63B, spent $5.86B" is NOT evidence of a $2.8B underspend — the same-sized gap appears in every prior year (e.g., 2024: $7.44B budgeted vs $5.31B filed actual), which tells you it is structural. Note also that King County files FIT amounts in round thousands, and 2025 is from the early filing cycle (King County's 2025 filing is present in this milestone snapshot). A true budget-vs-actual variance would need King County's own budget-to-actual report (e.g., its ACFR or biennial budget monitoring reports), which is not yet an accepted source here.

**Trace:**
- Source 1: `king_county.open_budget_dashboard` (King County Open Budget Dashboard), snapshot 2026-04-01, model refresh 2026-04-01T21:37:44.693
  - Public source: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
  - Grain: countywide by dashboard year; Measure: budgeted_expenditure
  - Filters: overview-by-year.jsonl, year in (2024, 2025)
  - Check: 11 overview rows covering 2017–2027; FY2026 budgeted expenditure = $8,598,795,612 matches known check
  - Caveats: budgeted/authorized values only, not actual spending; annual dashboard frame, distinct from the adopted 2026–2027 $20.16B biennial headline
- Source 2: `washington.fit_filed_actuals` (SAO Financial Intelligence Tool, filed annual actuals), snapshot milestone-2025-published-2026-06-30 (FIT Snapshot 33, published 2026-06-30); data-through: filed years 2015–2024 complete, 2025 early-cycle
  - Public source: https://portal.sao.wa.gov/FIT/
  - Grain: government-year (King County, Washington, MCAG 0127); Measures: total_expenditures, total_revenues
  - Filters: government-annual-totals.jsonl, government = "King County, Washington", year in (2024, 2025)
  - Check: KCRHA 2024 expenditures $191,618,113 matches skill spot check; King County present with all years 2015–2025 in summary.json
  - Caveats: FIT headline basis excludes internal service funds; King County files in round thousands; filed actuals are not budgets and were not numerically reconciled with the dashboard frame
- Compatibility check: amount basis, fund scope, and budget frame differ between the two sources; no accepted alignment recipe exists, so no budget-vs-actual variance was computed → answer mode `side_by_side_only`.
