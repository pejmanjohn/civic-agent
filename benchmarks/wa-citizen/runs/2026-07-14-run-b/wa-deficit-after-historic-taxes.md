---
case: wa-deficit-after-historic-taxes
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

A "budget shortfall" in Olympia usually means a *projected future gap* — forecast spending commitments growing faster than forecast revenue over the next four years — not that money is missing today. What the accepted sources here can show is the mechanical backdrop: Washington's enacted operating budget keeps growing at a pace that current-law revenue has historically trailed. The 2025-27 enacted operating budget is **$150.4 billion (Total Budgeted)**, up **$16.8 billion (+12.6%)** from 2023-25 and **2.3x** the 2013-15 budget. Meanwhile, General Fund collections so far in 2025-27 are actually running about **$1.0 billion above estimate** (partial, through April 2026) — so the shortfall story is not about current collections missing; it is about the projected cost of continuing commitments outrunning the revenue base even after new taxes. The size of the projected shortfall itself, and the tax package's forecasted yield, are *not* in this repo's accepted sources — that is why this answer is **partial**, not exact.

**Numbers**

- 2025-27 enacted operating budget, Total Budgeted: $150.411B (Outlook Funds NGF-O view: $77.858B)
- 2023-25 enacted: $133.610B → change: +$16.801B (+12.6%)
- Enacted base biennial trend: 2013-15 $66.5B → 2017-19 $88.3B → 2021-23 $121.7B → 2025-27 $150.4B (+126% over six biennia)
- General Fund (001) revenue, 2025-27 partial through April 2026: actual $46.143B vs. estimate $45.099B (+$1.044B above estimate)
- Prior closed biennia mostly came in *below* estimate: 2023-25 −$1.935B; 2021-23 −$2.653B; 2019-21 −$3.933B

**How to read this**

- Budget figures are enacted budget *authority* (permission to spend), not actual spending. Revenue figures are General Fund (001) only — a narrower fund scope than Total Budgeted, so do not subtract one from the other.
- Interpretation, separated from the facts above: a shortfall can persist after a large tax package because (a) maintenance-level costs (caseloads, wages, inflation, new commitments) are projected to grow faster than revenue; (b) one-time fund balances and transfers used to balance 2025-27 fall away in the outlook years; (c) new-revenue estimates are forecasts that phase in over time. None of those projections are in this repo's sources.
- What this repo cannot verify: the dollar size of the projected shortfall, the tax package's estimated yield, the four-year balanced-budget outlook, or any 2026 supplemental changes. Official paths: OFM's budget outlook materials (https://ofm.wa.gov/budget/) and the Economic and Revenue Forecast Council for revenue forecasts; the 2026 supplemental snapshot is not yet implemented in this source.

**Trace**

Operating budget:
- Source: `washington.operating_budget`, Fiscal WA Operating Budget Summary (Power BI), snapshot `2025-27-enacted-2025-05-20`
- Public source: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien (historical: https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior)
- Data-through: 2025-27 enacted (budget version Enacted 05-20-2025); trend = enacted base by biennium, 2013-15 through 2025-27
- Grain: biennium (statewide) | Measure: budgeted_amount | Filters: historical-biennium-summary.jsonl, fund_view = "Total Budgeted", budget_state = enacted, revision_scope = base
- Check: 7 trend rows; 2025-27 overlap total = $150.411B matches current snapshot; NGF-O = $77.858B
- Caveats: budget authority, not actual spending; excludes capital/transportation budgets; not the 2026 supplemental

Revenue:
- Source: `washington.revenue_by_biennium`, Fiscal WA Revenue by Biennium (ReportViewer), snapshot `2025-27-revenue-through-2026-04`
- Public source: https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: Actual Data Through April 2026; 2025-27 status = partial
- Grain: biennium | Measure: estimated_revenue, actual_revenue, actual_minus_estimate | Filters: general-fund-revenue-by-biennium.jsonl, fund = General Fund (001)
- Check: 12 biennium rows, coverage 2003-05 through 2025-27; 2025-27 est $45.099B / actual $46.143B / diff +$1.044B match snapshot validation values
- Caveats: General Fund (001) only, not all budgeted funds; 2025-27 values partial through April 2026, not a full-biennium forecast; estimates here are Fiscal WA report estimates, not the tax package's fiscal note

Answer mode: **partial** — the growth and collections facts are source-backed; the projected shortfall amount and the tax package's yield have no accepted source in this repo yet.
