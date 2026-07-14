---
case: kc-cuts-despite-20b
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

Two things are getting mixed together in that question. First, the "$20 billion" is a **two-year** number: the King County Council adopted a $20.16 billion budget covering both 2026 and 2027, so the county's annual budget is roughly half that headline — FY2026 budgeted expenditure on the county's own dashboard is about $8.6 billion. Second, a big total budget and service cuts can coexist: most county money is legally restricted to specific purposes (transit fares and taxes to transit, sewer rates to wastewater, etc.), so shortfalls in the flexible General Fund can force cuts even while the countywide total grows. My accepted sources can confirm the budget frames and totals, but they contain only **budgeted** values — they cannot verify which specific services are being cut, by how much, or attribute the cause. That part of the "why" needs the county's adopted budget book itself, which is the official path.

**Numbers**

- Adopted 2026–2027 biennial budget (context): **$20.16 billion** for two years combined.
- FY2026 countywide budgeted expenditure (annual dashboard frame): **$8,598,795,612** (~$8.60B).
- FY2026 countywide budgeted revenue: **$8,865,634,686** (~$8.87B).
- Trend, annual budgeted expenditure: 2017 $4.58B → 2024 $7.44B → 2025 $8.63B → 2026 $8.60B (−$27.8M, −0.3% vs 2025) → 2027 $8.85B.
- FY2026 budgeted FTE: 18,333 (up from 17,636 in 2025).

**How to read this**

- The biennial $20.16B and the annual ~$8.6B are **different budget frames**; do not add, average, or reconcile them. Side by side they show the "$20 billion" intuition overstates the annual scale by roughly 2x.
- All dashboard figures are budgeted/authorized amounts, not actual spending. "Cutting services" is a claim about actual service levels, which this source cannot prove or disprove. At the countywide budgeted level, the 2026 total is essentially flat vs 2025 and rises in 2027 — cuts, where they exist, live inside specific funds and programs below this grain.
- The restricted-funds point (why a General Fund gap forces cuts despite a large total) is standard public-finance context, not a number from my accepted sources. To see the county's own explanation and line-item reductions, use the 2026–2027 Adopted Budget Book: https://cdn.kingcounty.gov/-/media/king-county/depts/council/budget/2026/2026-2027-adopted-budget-book.pdf (also the council budget page: https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27).

**Trace**

- Sources: `king_county.open_budget_dashboard` (King County Open Budget Dashboard, snapshot 2026-04-01, model refresh 2026-04-01T21:37) and `king_county.adopted_budget` (context-only, adopted 2026–2027 biennial headline, observed 2026-03-05).
- Public sources: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard ; https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27
- Snapshot/data-through: dashboard snapshot 2026-04-01, years 2017–2027; adopted-budget context data-through biennium 2026–2027 (biennial cadence — within freshness window as of 2026-07-14).
- Grain: countywide by dashboard year (overview-by-year.jsonl); biennial headline (context).
- Measure: sum(budgeted_expenditure), sum(budgeted_revenue), sum(budgeted_fte); adopted_amount = $20,160,000,000.
- Filters/query logic: read overview-by-year.jsonl, all 11 year rows; adopted headline from source-card checks.
- Check: 11 overview rows (2017–2027); FY2026 budgeted expenditure = 8,598,795,612 and revenue = 8,865,634,686 and FTE = 18,333, all matching the skill's known checks; adopted_amount check = 20,160,000,000.
- Caveats: budgeted/authorized values, not actual spending; biennial and annual frames must not be combined; source cannot verify specific service cuts, fund-level gaps, or causes; the restricted-vs-General-Fund explanation is interpretive context, not sourced numbers.

**Answer mode: partial** — the budget-size and frame facts are exact from accepted sources, but no accepted source covers which services are cut or why (General Fund/fund-level detail); the official path is the adopted budget book above.
