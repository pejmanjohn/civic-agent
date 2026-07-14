---
case: kc-actuals-vs-budget-trap
surface: repo-skills
answer_mode: side_by_side_only
session: fresh
---

**Conclusion:**
There is no accepted apples-to-apples budget-vs-actual number for King County, so I can't tell you a true "variance." What the accepted sources support is showing the two frames side by side for 2025: King County's dashboard **budgeted** expenditure was about **$8.63 billion**, while its **filed actual** expenditures with the State Auditor were about **$5.86 billion**. The roughly $2.8B gap is mostly an accounting-frame difference, not evidence of massive underspending — the two numbers are built on different bases and must not be subtracted.

**Numbers:**

| 2025 | Amount | Frame |
|---|---|---|
| Budgeted expenditure (Open Budget Dashboard) | $8,626,613,762 | authorized/budgeted, all dashboard appropriations |
| Filed actual expenditures (SAO FIT) | $5,860,085,000 | filed actuals, FIT headline basis (excludes internal service funds; King County files in round thousands) |
| Filed actual revenues (SAO FIT), for context | $6,476,448,000 | same FIT basis — actual revenues exceeded actual expenditures in 2025 |

**How to read this:**
- The dashboard number is what the Council **authorized** King County to spend; the FIT number is what King County **reported actually spending** to the State Auditor — but on a narrower basis (it excludes internal service funds, and the fund/scope definitions differ from the dashboard's). Subtracting them would mix frames and overstate "unspent budget."
- Governments routinely spend less than full authority (contingencies, capital timing, vacancies), so even a clean comparison rarely shows 100% execution — but quantifying King County's true execution rate needs a source that publishes budget and actuals on the same basis (King County's own biennial budget-to-actual reports / ACFR). That source isn't in the accepted registry yet.
- The 2025 FIT values come from the Auditor's 2025 filing-milestone snapshot; King County has filed 2025, but the milestone cycle is early, so figures could be revised.
- If "last year" meant the 2024 fiscal year: budgeted expenditure $7,441,147,541 vs FIT filed actual $5,312,711,000 — same frame caveat applies.

**Trace:**
- **Source 1:** `king_county.open_budget_dashboard` (King County Open Budget Dashboard), snapshot 2026-04-01, model refresh 2026-04-01T21:37:44
- **Public source 1:** https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
- **Grain/measure 1:** countywide year; `budgeted_expenditure` from `overview-by-year.jsonl`, filter year = 2025 (2024 shown for the alternate reading)
- **Check 1:** overview file has 11 rows covering 2017–2027; FY2026 fingerprint checks (expenditure $8,598,795,612; revenue $8,865,634,686) match `summary.json`
- **Source 2:** `washington.fit_filed_actuals` (SAO Financial Intelligence Tool, filed annual actuals for reviewed governments), snapshot milestone-2025-published-2026-06-30 (FIT Snapshot 33, created 2026-06-30)
- **Public source 2:** https://portal.sao.wa.gov/FIT/
- **Data-through 2:** filed years 2015–2024 complete; 2025 filed (early milestone cycle, subject to revision)
- **Grain/measure 2:** government-year; `total_expenditures`, `total_revenues` from `government-annual-totals.jsonl`, filter government = "King County, Washington" (mcag 0127), year = 2025
- **Check 2:** 110 government-annual rows; King County present for all years 2015–2025 in `summary.json`; amount_basis = filed_actuals_excl_internal_service
- **Caveats:** budgeted dashboard values are not actual spending; FIT actuals are not budgets and exclude internal service funds; King County reports FIT values in round thousands; the two frames have incompatible amount bases and scopes, so no numeric variance is computed — a true execution-rate answer needs King County's own budget-to-actual/ACFR reporting on a single basis

**Answer mode:** `side_by_side_only` — both facts are source-backed, but the budget frame and the filed-actuals frame are not numerically comparable.
