---
case: wa-operating-total-2025-27
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
Washington state's current operating budget — the 2025-27 enacted biennial budget signed May 20, 2025 — authorizes about **$150.4 billion** in total budgeted funds over the two-year period (roughly $75 billion per year, though the state budgets by biennium, not by year). The narrower near-general-fund view that budget writers use for sustainability planning, called Outlook Funds (NGF-O), is about **$77.9 billion** of that total.

**Numbers:**
- 2025-27 enacted operating budget, Total Budgeted (all budgeted funds): **$150,411,096,000**
- 2025-27 enacted operating budget, Outlook Funds (NGF-O): **$77,857,672,000**
- Largest agencies within the Total Budgeted view: Health Care Authority $38.03B, Public Schools $36.41B, Dept. of Social and Health Services $25.02B, University of Washington $9.49B
- For scale over time: the enacted base biennial total has grown from $66.5B (2013-15) to $150.4B (2025-27)

**How to read this:**
- This is **budget authority** — what the Legislature authorized agencies to spend — not actual spending, and not revenue collected.
- Washington budgets in **two-year biennia** (July 2025 through June 2027). Don't compare the $150.4B headline directly with annual city or county budget figures.
- "Total Budgeted" counts all budgeted funds, including federal and dedicated accounts. "Outlook Funds (NGF-O)" is the narrower near-general-fund slice most often quoted in Olympia budget debates — both are official frames of the same enacted budget.
- The operating budget excludes the separate capital and transportation budgets.
- This snapshot reflects the budget as enacted; it does not include any 2026 supplemental changes.

**Trace:**
- Source: `washington.operating_budget` — Fiscal WA 2025-27 Biennial Omnibus Operating Budget Summary Comparison, snapshot `2025-27-enacted-2025-05-20` (budget version "Enacted (05-20-2025)", model refresh 2025-07-22T17:18:33.94)
- Public source: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien
- Data-through: not applicable — enacted budget snapshot, not a spending feed
- Grain: agency x fund view (checked-in `agency-by-fund-view.jsonl`)
- Measure: sum(budgeted_amount), normalized to dollars
- Filters/query logic: group by `fund_view`; headline = fund_view "Total Budgeted"; secondary frame = "Outlook Funds (NGF-O)"
- Check: recomputed from the snapshot at answer time — 102 Total Budgeted agency rows summing to $150,411,096,000 and NGF-O $77,857,672,000, matching the skill's validation checks exactly
- Caveats: budgeted/authorized operating budget, not actual spending or revenue; biennial (2025-27), not annual; excludes capital and transportation budgets; does not reflect 2026 supplemental changes; the two fund views are alternative frames and must not be added together

**Answer mode: exact** — one accepted source matches the requested "operating budget" frame, validation checks pass, and both official fund views are presented side by side with labels per the `budget_scale.current_total` recipe.
