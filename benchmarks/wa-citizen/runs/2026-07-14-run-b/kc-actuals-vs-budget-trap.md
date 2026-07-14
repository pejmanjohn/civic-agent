---
case: kc-actuals-vs-budget-trap
surface: repo-skills
answer_mode: side_by_side_only
session: fresh
---

**Conclusion:**
I can show you King County's 2025 budget and King County's 2025 filed actual spending side by side, but I can't honestly tell you "they spent X% of the budget." The two official sources measure spending on different accounting bases, so subtracting one from the other would produce a misleading variance number. What the sources do show: King County budgeted about $8.6 billion in expenditures for 2025, and its annual report filed with the State Auditor shows about $5.9 billion in total expenditures on the Auditor's narrower headline basis. That gap is mostly a difference in what each source counts — not evidence of $2.7 billion in "unspent" money.

**Numbers (side by side, not a variance):**

| Frame | 2025 | 2024 (for context) |
|---|---|---|
| Budgeted expenditure (King County Open Budget Dashboard) | $8,626,613,762 | $7,441,147,541 |
| Filed actual total expenditures (State Auditor FIT, headline basis) | $5,860,085,000 | $5,312,711,000 |

**How to read this:**
- The dashboard number is the county's *authorized/budgeted* expenditure for the year — permission to spend, across the county's own budget presentation.
- The FIT number is what King County *reported actually spending* in its annual filing to the Washington State Auditor — but on FIT's headline basis, which excludes internal service funds and uses the Auditor's fund-accounting presentation, not the county's budget presentation. King County also files these figures in round thousands.
- Because the scopes differ, "budget minus filed actuals" is not an underspend figure. A true budget-vs-actual answer needs a single source that publishes both on the same basis (e.g., King County's own biennial budget-to-actual reports or ACFR); no such source is accepted in this repo yet.
- The 2025 FIT figure comes from the Auditor's early 2025 filing-cycle snapshot; treat it as an early-cycle filing that could be revised.
- One directional fact both frames support: both budget and actual spending grew from 2024 to 2025 (budget +15.9%, filed actuals +10.3% within their own frames).

**Trace:**
- Source 1: `king_county.open_budget_dashboard`, snapshot 2026-04-01 (model refresh 2026-04-01T21:37:44.693)
  - Public: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
  - Grain: countywide by dashboard year; Measure: budgeted_expenditure; Filters: overview-by-year.jsonl, year in (2024, 2025)
  - Check: 11 overview rows covering 2017–2027; FY2026 expenditure total matches summary.json check $8,598,795,612
  - Caveats: budgeted/authorized values, not actual spending
- Source 2: `washington.fit_filed_actuals`, snapshot milestone-2025-published-2026-06-30 (FIT Snapshot 33)
  - Public: https://portal.sao.wa.gov/FIT/
  - Data-through: filed years 2015–2024 complete; 2025 early filing cycle (King County has filed)
  - Grain: government-year; Measure: total_expenditures, amount_basis = filed_actuals_excl_internal_service; Filters: government-annual-totals.jsonl, government = "King County, Washington", year in (2024, 2025)
  - Check: 110 government rows; snapshot spot checks pass (e.g., KCRHA 2024 expenditures $191,618,113)
  - Caveats: FIT headline basis excludes internal service funds; King County files in round thousands; not comparable numerically to the dashboard budget frame — no alignment recipe exists
- Answer mode: side_by_side_only (both facts are source-backed, but frames must not be numerically reconciled)
