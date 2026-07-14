---
case: kc-actuals-vs-budget-trap
surface: repo-skills
answer_mode: side_by_side_only
session: fresh
---

**Conclusion:** There is no accepted source that directly reconciles King County's budget to its actual spending, so I can't tell you a true "budget vs. actual" variance. What I can show, side by side, is (a) what King County budgeted for 2025 per its official Open Budget Dashboard, and (b) what King County actually spent in 2025 as filed with the Washington State Auditor. These two numbers use different accounting bases and must not be subtracted from each other.

**Numbers (2025, King County government):**
- Budgeted expenditure (Open Budget Dashboard): **$8,626,613,762**
- Filed actual total expenditures (State Auditor FIT): **$5,860,085,000** (King County reports in round thousands; 2025 is an early-filing-cycle year)
- For reference, 2024 (the latest fully complete filed year): budgeted $7,441,147,541 vs. filed actual expenditures $5,312,711,000 — the same non-comparability applies.

**How to read this:** The gap between these numbers is mostly an accounting-frame difference, not evidence of a huge underspend. The dashboard figure is budgeted/authorized expenditure across the county's dashboard view; the FIT figure is the Auditor's headline filed-actuals basis, which **excludes internal service funds** and reflects a different fund/scope treatment. Subtracting them would produce a misleading "unspent" number. A real answer to "did they spend what they budgeted" needs a budget-to-actual source on a single basis — King County's own year-end financial reports (ACFR budget-to-actual schedules) or a future accepted source that maps the dashboard frame to the FIT frame. Both facts here are individually solid and official; they just can't be numerically compared.

**Trace:**
- Source 1: `king_county.open_budget_dashboard`, snapshot 2026-04-01 (model refresh 2026-04-01T21:37:44.693)
  - Public: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
  - Grain: countywide by dashboard year; Measure: budgeted_expenditure; Filter: year = 2025 from overview-by-year.jsonl
  - Check: 11 overview rows (2017–2027); FY2026 budgeted expenditure = $8,598,795,612 matches known check
  - Caveats: budgeted/authorized dashboard values, not actual spending or payments
- Source 2: `washington.fit_filed_actuals`, snapshot milestone-2025-published-2026-06-30 (FIT Snapshot 33, published 2026-06-30)
  - Public: https://portal.sao.wa.gov/FIT/
  - Grain: government × year; Measure: total_expenditures; Filter: government = "King County, Washington" (MCAG 0127), year = 2025 (and 2024 for reference), amount_basis = filed_actuals_excl_internal_service
  - Check: 110 government rows in snapshot; King County years 2015–2025 present; spot check KCRHA 2024 expenditures $191,618,113 matches
  - Caveats: FIT headline basis excludes internal service funds; King County files in round thousands; 2025 is an early-filing-cycle (partial-cycle) milestone year; filed actuals are not budgets and were not numerically compared to the dashboard budget frame
- Answer mode: side_by_side_only — amount basis and budget frame are incompatible; no accepted alignment recipe exists. Checkbook (managed local DB) was not used; it covers Washington state agencies only and was treated as unavailable.
