---
case: wa-new-taxes-actually-collecting
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
So far, yes at the big-picture level — Washington's General Fund is actually running *ahead* of what was projected for the 2025-27 budget period. Through April 2026 (the first ~10 months of the two-year cycle), the state has collected about $46.1 billion against a $45.1 billion estimate, roughly $1.04 billion (+2.3%) above projection. That is notable because in every biennium since 2005-07, actuals came in *below* estimates. But I cannot tell you whether the specific new 2025 tax measures (the 2025 legislature's revenue package — B&O changes, expanded sales tax on services, etc.) are individually hitting their fiscal-note projections: the accepted source tracks revenue by collecting agency, not by individual tax, so this is a **partial** answer.

**Numbers (General Fund 001, 2025-27 biennium, partial through April 2026):**
- Estimated revenue: $45.099B
- Actual revenue: $46.143B
- Actual minus estimate: +$1.044B (+2.3%)
- Largest line, Department of Revenue (which collects most state taxes, including the new ones): $27.76B actual vs $25.33B estimated, +$2.43B
- Notable lines running below estimate: Health Care Authority −$838M; Public Schools −$318M; Insurance Commissioner −$144M
- Recent closed biennia for context: 2023-25 actuals were −$1.93B vs estimate; 2021-23 were −$2.65B; 2019-21 were −$3.93B

**How to read this:**
- These are General Fund (001) figures only — many 2025 revenue changes feed other accounts (e.g., dedicated accounts), which this source does not cover.
- The "estimate" is Fiscal WA's revenue estimate for the biennium, which already incorporates enacted 2025 law changes — so beating it means collections overall are outpacing the official forecast, not just that new taxes exist.
- The detail grain is collecting agency, not tax type. The Department of Revenue line being +$2.43B is consistent with taxes overall over-performing, but it mixes new 2025 taxes with existing sales, B&O, and property taxes — it cannot isolate any single new measure.
- 2025-27 is only partial through April 2026. Revenue is lumpy across a biennium; do not extrapolate the +$1.04B to a full-biennium result.
- To check individual new taxes against their projections, the official path is the Economic and Revenue Forecast Council's quarterly forecasts and collections reports (https://erfc.wa.gov/forecasts/revenue-forecast) and DOR collections detail — that per-measure source is not yet in this repo.

**Trace:**
- Source: Fiscal WA Revenue by Biennium (washington.revenue_by_biennium), snapshot 2025-27-revenue-through-2026-04
- Public source: https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: Actual Data Through April 2026 (2025-27 actual_data_status = partial)
- Grain: biennium (totals); biennium × revenue_area × account_or_agency (detail)
- Measure: estimated_revenue, actual_revenue, actual_minus_estimate
- Filters/query logic: read general-fund-revenue-by-biennium.jsonl, row biennium = 2025-27; detail from general-fund-revenue-by-area-account.jsonl filtered to biennium = 2025-27, sorted by estimated_revenue desc
- Check: 12 biennium rows, 934 detail rows; summary.json validation confirms 2025-27 estimated = $45,098,726,991, actual = $46,142,570,002.15, difference = +$1,043,843,011.15; detail totals reconcile to statewide totals
- Caveats: General Fund (001) only; partial through April 2026 — not a full-biennium actual or forecast; agency-level detail cannot isolate specific new 2025 tax measures; estimates embed enacted law, so this measures forecast accuracy, not new-tax yield per se

**Answer mode: partial** — the overall projection-vs-actual question is answerable from an accepted source, but per-tax-measure performance of the new 2025 taxes requires ERFC/DOR per-source detail not yet in the repo.
