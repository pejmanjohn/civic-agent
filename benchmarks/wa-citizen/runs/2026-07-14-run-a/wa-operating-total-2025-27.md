---
case: wa-operating-total-2025-27
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
Washington state's current operating budget — the 2025-27 enacted biennial budget signed May 20, 2025 — authorizes about **$150.4 billion** in spending over the two-year period from July 2025 through June 2027, counting all budgeted funds. On the narrower near-general-fund view legislators use for balancing (Outlook Funds, NGF-O), it is about **$77.9 billion**.

**Numbers:**
- 2025-27 enacted operating budget, Total Budgeted (all funds): **$150,411,096,000**
- 2025-27 enacted operating budget, Outlook Funds (NGF-O): **$77,857,672,000**
- Roughly $75 billion per year on the all-funds view, though the budget is enacted and tracked as a two-year (biennial) total
- For scale, the prior 2023-25 enacted base budget was $133.6 billion Total Budgeted, so 2025-27 is about $16.8 billion (about 12.6%) larger in nominal terms
- Largest pieces (Total Budgeted): Health Care Authority $38.0B, Public Schools $36.4B, Dept. of Social and Health Services $25.0B, University of Washington $9.5B

**How to read this:**
- These are **budgeted/authorized amounts** — permission to spend — not actual spending. Actual payments come from a different source (Open Checkbook).
- Washington budgets by **biennium** (two years). Do not halve the total and call it "the annual budget" in any official sense.
- **Total Budgeted** counts every fund in the budget, including federal and dedicated accounts. **Outlook Funds (NGF-O)** is the near-general-fund slice most policy debates about "the state budget" refer to. Both are official frames; pick the one matching your question.
- This is the **operating** budget only — the capital and transportation budgets are separate and not covered here.
- This snapshot reflects the budget as enacted in May 2025; it does not include any 2026 supplemental changes.

**Answer mode: exact** (recipe `budget_scale.current_total`; the accepted source matches the requested operating-budget frame, both official fund views shown with labels).

**Trace:**
- Source: `washington.operating_budget` — Fiscal WA 2025-27 Biennial Omnibus Operating Budget Summary Comparison, snapshot `2025-27-enacted-2025-05-20`
- Public source: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien (Fiscal WA / LEAP / OFM Power BI)
- Snapshot: `2025-27-enacted-2025-05-20`; budget version `Enacted (05-20-2025)`; model refresh `2025-07-22T17:18:33.94`
- Data-through: not applicable — enacted budget authority, not actuals
- Grain: agency by fund view (statewide sum); historical check at biennium grain
- Measure: sum(budgeted_amount), normalized to dollars (report values are in thousands)
- Filters/query logic: read `agency-by-fund-view.jsonl`, group by `fund_view`, sum `budgeted_amount`; cross-checked 2025-27 row in `historical-biennium-summary.jsonl` (enacted base, Total Budgeted)
- Check: 102 Total Budgeted agency rows summing to $150,411,096,000 and 85 NGF-O rows summing to $77,857,672,000, matching the skill's known validation values; historical 2025-27 overlap matches at $150.411B
- Caveats: budgeted/authorized operating budget, not actual spending; biennial (two-year) total, not annual; operating budget only (capital and transportation budgets excluded); does not reflect 2026 supplemental changes; Total Budgeted and NGF-O are different official frames and must not be mixed in one number

