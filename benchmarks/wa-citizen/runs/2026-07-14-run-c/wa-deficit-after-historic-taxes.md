---
case: wa-deficit-after-historic-taxes
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** The accepted sources can show the two arithmetic halves of the story, but not the shortfall figure itself. Washington's 2025-27 enacted operating budget grew to $150.4 billion — up $16.8 billion (12.6%) from 2023-25, the largest dollar jump in the covered record. Meanwhile, even after the 2025 tax package was folded into the official revenue estimates (the June 2026 revisions raised the current-biennium General Fund estimate from $45.10B to $51.27B), actual collections are running about $353 million *below* those raised estimates so far. In plain terms: spending authority rose faster than revenue, and the new taxes are so far bringing in slightly less than officially expected. The projected multi-year "shortfall" number itself comes from the ERFC forecast and OFM four-year outlook, which are not accepted sources here — so this is a **partial** answer.

**Numbers:**
- Enacted operating budget (Total Budgeted, biennial): 2023-25 $133.610B → 2025-27 $150.411B (+$16.801B, +12.6%).
- General Fund (001), 2025-27, partial through May 2026: estimated $51.268B, actual $50.914B, actual-minus-estimate **-$353.2M**.
- Prior biennium for context: 2023-25 GF actual $103.796B vs estimate $105.730B (**-$1.935B**); actuals have landed below estimates in every biennium since 2005-07.
- Snapshot revision warning: under the same data-through label, the July 2026 refresh raised the 2025-27 estimate $45.10B → $51.27B, flipping the difference from +$1.04B to -$353M.

**How to read this:** These are two different frames — do not net them against each other. The $150.4B is enacted budget authority across all budgeted funds for the biennium, not actual spending; the General Fund figures are one fund's revenue, partial through May 2026 with roughly half the biennium left. "Shortfall" in news coverage usually means the *projected* gap between forecast revenue and the cost of continuing current services over four years — a forecast concept these snapshots do not carry. The budget facts above are consistent with a shortfall persisting (fast spending growth, collections trailing even post-tax-package estimates), but the interpretation of *why* costs grew (caseloads, compensation, Medicaid, forecast downgrades) needs the ERFC revenue forecast (erfc.wa.gov) and OFM's budget outlook (ofm.wa.gov/budget/) — that is the path for the missing piece.

**Trace:**
- Sources: `washington.operating_budget` (Fiscal WA Operating Budget Summary, snapshot 2025-27-enacted-2025-05-20) and `washington.revenue_by_biennium` (Fiscal WA Revenue by Biennium, snapshot 2025-27-revenue-through-2026-05)
- Public sources: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien ; https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: operating = enacted 2025-27 budget (version Enacted 05-20-2025); revenue = Actual Data Through May 2026 (2025-27 partial); monthly cadence, boundary within window as of 2026-07-14
- Grain: biennium (statewide)
- Measures: budgeted_amount (Total Budgeted); estimated_revenue, actual_revenue, actual_minus_estimate (General Fund 001)
- Filters/query logic: historical-biennium-summary.jsonl with period_type=biennium, budget_state=enacted, revision_scope=base, fund_view="Total Budgeted"; general-fund-revenue-by-biennium.jsonl, fund="General Fund (001)"
- Check: 7 historical trend rows, 2025-27 overlap = $150.411B matches current Total Budgeted total; 12 revenue biennium rows, 2025-27 values match skill known checks (est $51.268B / act $50.914B / -$353.2M)
- Caveats: budget figures are enacted authority, not actual spending, and exclude the 2026 supplemental; revenue is General Fund (001) only and partial — not a full-biennium forecast; budget (all funds) and GF revenue are different scopes and must not be subtracted; revenue estimates revise within an unchanged data-through label (cite snapshot version); the shortfall projection itself is unsourced here — ERFC/OFM outlook is the official path.
