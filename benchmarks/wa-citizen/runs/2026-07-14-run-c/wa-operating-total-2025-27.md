---
case: wa-operating-total-2025-27
surface: repo-skills
answer_mode: exact
session: fresh
---

**Answer mode: exact** (recipe `budget_scale.current_total`; one accepted source matches the requested frame)

## Conclusion
Washington state's current operating budget — the 2025-27 enacted biennial budget, signed May 20, 2025 — authorizes about **$150.4 billion across all budgeted funds** for the two-year period July 2025 through June 2027. That works out to roughly $75 billion per year, though the state budgets by two-year biennium, not by year. Looking only at the narrower "Outlook Funds (NGF-O)" view — the near-general-fund money the Legislature most actively steers — the total is about **$77.9 billion** for the biennium.

## Numbers
- **Total Budgeted (all budgeted funds), 2025-27 enacted: $150,411,096,000**
- Outlook Funds (NGF-O), 2025-27 enacted: $77,857,672,000
- Largest agencies (Total Budgeted): Health Care Authority $38.0B, Public Schools $36.4B, Dept. of Social and Health Services $25.0B, University of Washington $9.5B
- Trend context (enacted base, Total Budgeted, by biennium): 2013-15 $66.5B → 2019-21 $99.7B → 2023-25 $133.6B → 2025-27 $150.4B

## How to read this
- These are **budgeted/authorized amounts** — permission to spend — not actual spending, and not revenue collected.
- The headline is a **two-year (biennial)** figure. Don't compare it directly to annual city or county budgets.
- "Total Budgeted" counts every budgeted fund, including federal and dedicated accounts. "Outlook Funds (NGF-O)" is the narrower frame you'll often see quoted in news about the state's fiscal outlook. Both are official; they answer different questions, so they're shown side by side rather than collapsed into one number.
- This snapshot is the enacted 2025-27 budget; it does **not** reflect any 2026 supplemental budget changes. The operating budget also excludes the separate capital and transportation budgets.

## Trace
- Source: `washington.operating_budget` — Fiscal WA 2025-27 Biennial Omnibus Operating Budget Summary Comparison, snapshot `2025-27-enacted-2025-05-20`
- Public source: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien
- Snapshot / data-through: budget version `Enacted (05-20-2025)`; Power BI model refresh `2025-07-22T17:18:33.94`; enacted-budget snapshot, so no rolling data-through boundary — but it predates and excludes the 2026 supplemental
- Grain: agency by fund view (statewide total = sum over agencies)
- Measure: `sum(budgeted_amount)` (normalized dollars)
- Filters/query logic: read `agency-by-fund-view.jsonl`; `fund_view = "Total Budgeted"` for the headline; `fund_view = "Outlook Funds (NGF-O)"` for the narrower frame; trend from `historical-biennium-summary.jsonl` (enacted base, R1)
- Check: recomputed from snapshot — 102 Total Budgeted agency rows sum to $150,411,096,000 and 85 NGF-O rows sum to $77,857,672,000, matching the skill's validation checks; historical 2025-27 overlap equals the current total
- Caveats: budgeted/authorized operating budget, not actual spending or revenue; biennial (two-year) figure; excludes capital and transportation budgets; 2026 supplemental changes not reflected; not comparable to annual local-government budgets without an explicit compatibility check
