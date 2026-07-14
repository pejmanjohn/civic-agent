---
case: kc-cuts-despite-20b
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

The "$20 billion" and "service cuts" are talking about different things. The $20.16 billion is King County's *two-year* (2026-2027) adopted budget, covering everything the county does — and most of it is legally restricted money (transit fares and taxes, sewer rates, grants) that can't be moved to whatever service is being cut. On an annual basis, the county's budgeted expenditure is about $8.6 billion in 2026 — and it did not grow from 2025 to 2026 (it dipped slightly), even while budgeted FTE rose. The specific "why" behind any given service cut (typically a General Fund gap: costs growing faster than legally capped property-tax revenue) is not something my accepted sources can prove, so I answer that part as a path, not a number.

**Numbers**

- Adopted 2026-2027 biennial budget (context frame): $20.16 billion — a two-year total, not one year's budget.
- Annual dashboard frame, countywide budgeted expenditure: 2025 = $8.627B, 2026 = $8.599B (a ~$28M / -0.3% dip), 2027 = $8.852B.
- Countywide budgeted revenue: 2026 = $8.866B; budgeted FTE: 18,333 in 2026 (up from 17,636 in 2025).
- Largest FY2026 department budgeted expenditures: Community & Human Services $1.624B, Natural Resources & Parks $1.579B, Metro Transit $1.498B — dominated by dedicated/restricted funds, not flexible General Fund dollars.

**How to read this**

- Do not add, average, or reconcile the $20.16B biennial headline with the ~$8.6B annual dashboard values; they are different period and budget frames.
- These are budgeted/authorized values, not actual spending — this source cannot confirm or deny that specific services were "cut," only what was budgeted.
- A big total budget and real service cuts can coexist: most county dollars are restricted by law to specific purposes (transit, wastewater, grants), while discretionary services depend on the General Fund, whose revenue growth is constrained (e.g., Washington's 1% property-tax levy growth cap). That structural explanation is standard budget context, not a number my sources verify — for the official rationale, read the county's own 2026-2027 adopted budget materials: https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27 and the Adopted Budget Book PDF linked there.
- I have no accepted source for King County's General Fund breakdown or restricted-vs-flexible split; that is the missing piece for a fully source-backed "why cuts" answer.

**Trace**

- Source: King County Open Budget Dashboard (snapshot) + context-only source `king_county.adopted_budget`
- Public source: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard ; adopted-budget context: https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27
- Snapshot: dashboard snapshot 2026-04-01 (model refresh 2026-04-01T21:37:44); adopted-budget context fingerprint: legislation file 2025-0288, budget book PDF last-modified 2026-03-05
- Grain: countywide by year (2017-2027) and FY2026 by department
- Measure: budgeted_expenditure, budgeted_revenue, budgeted_fte; biennial adopted_amount ($20,160,000,000) as labeled context
- Filters/query logic: read overview-by-year.jsonl (all years), department-revenue-expenditure-by-year.jsonl (year=2026, sort budgeted_expenditure desc); adopted headline from source card only
- Check: 11 overview rows 2017-2027; FY2026 budgeted expenditure = $8,598,795,612, revenue = $8,865,634,686, FTE = 18,333; 22 FY2026 department rows totaling $8.599B — all match skill validation checks
- Caveats: budgeted/authorized values, not actual spending; biennial and annual frames must not be numerically reconciled; department budgets are organizational views, not policy-area spending; no accepted source covers the General Fund gap or which services were cut — the county's adopted budget book and council budget page are the official path

