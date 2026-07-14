---
case: wa-deficit-after-historic-taxes
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

There is no single official "the shortfall" number — any deficit figure you have heard depends on modeling choices: which revenue-forecast vintage it uses, whether future spending is projected at maintenance level (current services, caseload, and inflation) or policy level, and which fund scope it counts (the narrow near-general-fund "Outlook" view vs. all budgeted funds). What the accepted sources do show is the structural mechanics behind why a big tax package didn't close the gap: (1) budgeted spending keeps growing faster than General Fund revenue is coming in, and (2) the new revenue was already baked into balancing the enacted 2025-27 budget — a projected shortfall lives in the *next* outlook window, not in this budget's headline. Note also that the tax package itself (size, contents, phase-in) is not in this repo's accepted sources, so I cannot confirm the "biggest in history" framing or its dollar value; that would come from Legislative fiscal notes and the ERFC forecast.

**Numbers**

- 2025-27 enacted operating budget: **$150.41B** Total Budgeted (all budgeted funds); **$77.86B** on the narrower Outlook Funds (NGF-O) view — the fund-scope choice alone moves the frame by ~$72B.
- Enacted base biennial growth: 2021-23 $121.73B → 2023-25 $133.61B → 2025-27 $150.41B (**+12.6%** over the prior biennium; +$16.8B).
- General Fund (001) revenue, 2025-27 biennium, partial through May 2026: estimated **$51.27B**, actual collected **$50.91B** — running **-$353M below estimate** so far.
- Forecast-vintage sensitivity, demonstrated in this very source: under the same "Actual Data Through April 2026" label, the current-biennium estimate was revised from $45.10B to $51.27B after June 2026 forecast/legislative revisions, flipping the estimate-vs-actual difference from +$1.04B to -$353M. That is exactly why "the deficit number" moves without anything real changing on the ground.

**How to read this**

- Budget figures are budgeted/authorized amounts (enacted 2025-27, base, biennial) — not actual spending. Revenue figures are General Fund (001) only and partial through May 2026; do not treat them as a full-biennium result or forecast.
- Why the shortfall "persists" despite new taxes (context, not a sourced claim): shortfall projections are forward-looking maintenance-level estimates for future biennia. New revenue raises the baseline, but if projected caseload, wage, and inflation-driven costs grow faster than the revised revenue line, the *next* outlook still shows a gap. Whether it does depends on the ERFC forecast vintage and the Outlook's assumptions — sources this repo has not yet accepted.
- Missing pieces for an exact answer: the official four-year Balanced Budget Outlook (OFM/ERFC), the 2025 revenue-package fiscal notes, and the 2026 supplemental budget. Those are the named path to the actual shortfall number.

**Answer mode: partial** — budget growth and revenue estimate-vs-actual are exact from accepted sources; the shortfall figure, tax-package size, and forecast assumptions are out of scope.

**Trace**

- **Source cards:** `washington.operating_budget`; `washington.revenue_by_biennium`
- **Public sources:** https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien ; https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- **Snapshots:** operating `2025-27-enacted-2025-05-20` (budget version Enacted 05-20-2025); revenue `2025-27-revenue-through-2026-05`
- **Data-through:** budget — enacted snapshot, not applicable; revenue — Actual Data Through May 2026 (2025-27 marked partial)
- **Grain:** biennium (statewide)
- **Measures:** `budgeted_amount` (Total Budgeted and NGF-O fund views); `estimated_revenue`, `actual_revenue`, `actual_minus_estimate` (General Fund 001)
- **Filters/query logic:** `historical-biennium-summary.jsonl` filtered to enacted/base/R1/Total Budgeted; `general-fund-revenue-by-biennium.jsonl`, fund = General Fund (001)
- **Checks:** 7 historical trend rows, 2025-27 overlap matches current Total Budgeted total $150.411B; 12 revenue biennium rows, summary.json marks 2025-27 partial and documents the $45.10B→$51.27B estimate revision
- **Caveats:** budget rows are authority, not actuals; revenue is GF(001) only, partial through May 2026; revenue estimates revise within an unchanged data-through label; 2026 supplemental changes, the Outlook, and the tax package are not in accepted sources; no shortfall number is asserted here.
