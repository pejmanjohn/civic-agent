---
case: kc-cuts-despite-20b
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** The "$20 billion" and "cutting services" facts are less contradictory than they sound, mostly because of two framing issues. First, the $20.16 billion is a **two-year** (2026–2027) adopted budget, not one year of money — the annual FY2026 budgeted expenditure on the county's own dashboard is about **$8.6 billion**. Second, a big countywide total does not mean flexible money: most of King County's budget sits in dedicated funds and enterprise operations (transit, wastewater, public health grants, etc.) that legally can't be moved to backfill other services. Service reductions are typically concentrated in the much smaller General Fund, which pays for things like courts, elections, and the Sheriff. My accepted sources can confirm the budget frames and totals, but they contain budgeted values only — they cannot confirm which specific services are being cut or quantify the General Fund gap. For that, the official path is the county's 2026–2027 Adopted Budget Book and budget-review page (linked in the trace).

**Numbers:**
- Adopted 2026–2027 biennial budget (context frame): **$20.16 billion** for two years combined.
- FY2026 annual budgeted expenditure (dashboard frame): **$8,598,795,612** (~$8.6B); FY2026 budgeted revenue: **$8,865,634,686** (~$8.9B); FY2027 budgeted expenditure: ~$8.85B.
- These two frames must not be added, averaged, or reconciled — annual dashboard years and the adopted biennial headline are different accounting views.
- Largest FY2026 department budgeted expenditures: Community & Human Services $1.62B, Natural Resources & Parks $1.58B, Metro Transit $1.50B — illustrating how much of the budget is committed to dedicated-purpose operations.
- Countywide budgeted expenditure has risen every recent dashboard year (2017: $4.58B → 2026: $8.60B), so at the countywide budgeted grain there is no visible "cut" — reductions happen inside specific funds and programs, which this source does not break out.

**How to read this:** "Budgeted" means authorized amounts, not actual spending. A county can have a growing total budget and still cut services where its flexible (General Fund) revenues grow slower than costs, because restricted revenues (fares, sewer rates, grants, dedicated levies) can only be spent on their own purposes. My sources verify the size and frames; the *why* of specific cuts is policy narrative that lives in the adopted budget book, not in these datasets — hence answer mode **partial**.

**Trace:**
- Source 1: King County Open Budget Dashboard (`king_county.open_budget_dashboard`), snapshot 2026-04-01, model refresh 2026-04-01T21:37:44
- Public source: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard
- Grain: countywide by year (2017–2027) from `overview-by-year.jsonl`; FY2026 department rows from `department-revenue-expenditure-by-year.jsonl`
- Measure: budgeted_expenditure, budgeted_revenue
- Filters/query logic: read overview rows for all years; department rows filtered year = 2026, sorted by budgeted_expenditure desc
- Check: 11 overview rows (2017–2027); FY2026 expenditure total = $8,598,795,612 and revenue = $8,865,634,686 match snapshot summary.json checks; 22 department rows sum to the same totals
- Source 2: `king_county.adopted_budget` (context only), adopted period 2026–2027, adopted amount $20.16B
- Public source: https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27 (Adopted Budget Book PDF last modified 2026-03-05)
- Caveats: budgeted/authorized values, not actual spending or actual revenue collected; biennial context and annual dashboard values are different frames and were not combined; department budgets are organizational views, not complete policy-area spending; no accepted source itemizes the General Fund shortfall or the specific service reductions — consult the Adopted Budget Book for that detail
- Answer mode: **partial** (budget-size frames answered exactly; the causal "why cuts" claim is beyond accepted sources, official path named)
