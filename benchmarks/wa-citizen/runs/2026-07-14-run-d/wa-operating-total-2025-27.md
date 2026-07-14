---
case: wa-operating-total-2025-27
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
Washington state's operating budget, as enacted for the 2025-27 biennium, is about **$150.4 billion in total budgeted funds** over the two-year period (July 2025 through June 2027). If you narrow to the near-general-fund view lawmakers use for balancing ("Outlook Funds," NGF-O), the same enacted budget is about **$77.9 billion**. Both are budget authority — what the Legislature authorized agencies to spend — not actual spending.

**Numbers:**
- 2025-27 enacted operating budget, Total Budgeted (all budgeted funds): **$150,411,096,000** (~$150.4B for the biennium, roughly $75B/year)
- Same budget, Outlook Funds (NGF-O) view: **$77,857,672,000** (~$77.9B)
- For scale context, the prior 2023-25 enacted base was $133.6B, so the enacted operating budget grew about $16.8B (+12.6%) biennium over biennium.
- Largest pieces (Total Budgeted): Health Care Authority ~$38.0B, Public Schools ~$36.4B, Social and Health Services ~$25.0B, University of Washington ~$9.5B.

**How to read this:**
- Washington budgets by **two-year biennium**, so $150.4B covers 24 months — don't compare it directly to a city or county's annual figure.
- "Total Budgeted" counts every budgeted fund (federal funds, dedicated accounts, etc.); "Outlook Funds (NGF-O)" is the narrower state-flexible-money view that dominates deficit debates. News stories quote both, which is why headline numbers differ by nearly 2x.
- This is the operating budget only — the capital and transportation budgets are separate and not included here.
- This reflects the budget as **enacted May 20, 2025**; any 2026 supplemental changes are not in this snapshot.

**Trace:**
- **Source:** `washington.operating_budget` — Fiscal WA 2025-27 Biennial Omnibus Operating Budget Summary Comparison, snapshot `2025-27-enacted-2025-05-20`
- **Public source:** https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien
- **Snapshot / data-through:** budget version `Enacted (05-20-2025)`; Power BI model refresh `2025-07-22T17:18:33.94`; not applicable as a data-through boundary — this is an enacted-budget snapshot, not a flow series
- **Grain:** agency x fund view, biennium 2025-27
- **Measure:** sum(budgeted_amount), normalized dollars
- **Filters:** `agency-by-fund-view.jsonl`, fund_view = "Total Budgeted" (NGF-O reported alongside as labeled second frame)
- **Check:** 102 Total Budgeted agency rows summing to $150,411,096,000 and 85 NGF-O rows summing to $77,857,672,000 — both match the source card's known validation checks; historical 2025-27 overlap also matches $150.411B
- **Caveats:** budgeted/authorized amounts, not actual spending; biennial (two-year) total; operating budget only (excludes capital and transportation budgets); 2026 supplemental changes not reflected; the two fund views must never be added or mixed in one number

**Answer mode:** `exact` (recipe `budget_scale.current_total` — one accepted source matches the requested frame; both official fund views shown side by side with labels).
