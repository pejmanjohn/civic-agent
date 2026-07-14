---
case: wa-new-taxes-actually-collecting
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
Close, but running slightly behind — with an important catch. Washington's official revenue tracking doesn't break out "the new 2025 taxes" as their own line, so no accepted source can say bill-by-bill whether each new tax is hitting its original projection. What the accepted source can say: General Fund revenue for the 2025-27 biennium — which includes the new taxes — is coming in about **$353 million (0.7%) below the current official estimate**, with actuals through May 2026. And "the projection" is a moving target: the estimate itself was revised **up about $6.2 billion** (from ~$45.1B to $51.27B) after the June 2026 forecast folded in legislative changes, which flipped the picture from "ahead of estimate" to "slightly behind."

**Numbers (General Fund 001, 2025-27 biennium, partial through May 2026):**
- Estimated revenue: **$51.27 billion**
- Actual revenue collected: **$50.91 billion**
- Actual minus estimate: **-$353.2 million (-0.7%)**
- Closest proxy for the new taxes: the Department of Revenue line (which collects sales, B&O, and most new 2025 taxes) is **$393M ahead** of estimate ($30.06B actual vs $29.67B estimated); the biggest laggards are the Health Care Authority (-$262M) and Public Schools (-$225M) lines — not tax collections.
- Context: small shortfalls vs estimate are normal — 10 of the last 11 completed biennia finished below estimate (e.g., 2023-25: -$1.93B; 2019-21: -$3.93B).

**How to read this:**
- These are General Fund (001) figures only, and the biennium runs through June 2027 — everything here is partial, roughly 11 months in. Don't treat -0.7% as a final verdict.
- The "estimate" is the current official forecast, not the projection made when the 2025 tax package passed. Fiscal WA revises estimates in place, so this measures tracking against today's forecast. Comparing against the original enactment-time fiscal notes would need the ERFC forecast history and bill fiscal notes — that's the path if you want the strict "did each new tax deliver what was promised in spring 2025" answer.
- The detail data is grained by collecting agency (e.g., "Department of Revenue"), not by tax type or bill, so the new sales-tax-on-services, B&O, and other 2025 changes can't be isolated here. DOR's tax statistics and ERFC's quarterly forecast reviews (https://erfc.wa.gov/forecasts/revenue-forecast) are where per-source performance gets published.
- Revenue tracking is separate from the budget: this says nothing about whether spending is on plan.

**Trace:**
- **Source:** `washington.revenue_by_biennium` — Fiscal WA Statewide Revenue by Biennium (General Fund 001)
- **Public source:** https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- **Snapshot:** `2025-27-revenue-through-2026-05` (fetched 2026-07-14)
- **Data-through:** Actual Data Through May 2026; 2025-27 `actual_data_status = partial`
- **Grain:** biennium (headline); biennium × revenue area × collecting agency (detail)
- **Measure:** `estimated_revenue`, `actual_revenue`, `actual_minus_estimate`
- **Filters/query logic:** read `general-fund-revenue-by-biennium.jsonl` (12 rows) and `general-fund-revenue-by-area-account.jsonl` filtered to `biennium = 2025-27` (70 rows), sorted by absolute estimate gap
- **Check:** summary.json validation — 2025-27 estimated $51,267,621,520 / actual $50,914,382,425.63 / difference -$353,239,094.37; detail totals reconcile to statewide totals
- **Caveats:** partial biennium (through May 2026 of a period ending June 2027); General Fund (001) only — dedicated accounts outside GF are not covered; estimates are revised in place (documented $6.2B upward revision at the June 2026 forecast under an unchanged data label), so this compares against the current forecast, not original 2025 enactment projections; agency-grain detail cannot isolate individual 2025 tax bills.

**Answer mode: partial** — the aggregate is-revenue-tracking-the-forecast question is answered exactly from an accepted source, but the specific "new 2025 taxes vs their original projections" claim needs per-source/fiscal-note data (ERFC forecast reviews, DOR collections statistics) that isn't an accepted source yet.
