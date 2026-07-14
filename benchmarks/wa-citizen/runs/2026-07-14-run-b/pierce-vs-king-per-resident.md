---
case: pierce-vs-king-per-resident
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion**

Pierce County government spends substantially **less** per resident than King County government. In 2024 — the most recent complete filed year — Pierce County spent about **$928 per resident**, while King County spent about **$2,234 per resident**. King County's per-resident spending is roughly **2.4 times** Pierce County's.

**Numbers**

| County | 2024 total expenditures (filed actuals) | Population (April 1, 2024, OFM) | Spending per resident |
|---|---|---|---|
| King County | $5,312,711,000 | 2,378,100 | ~$2,234 |
| Pierce County | $883,659,316 | 952,600 | ~$928 |

Difference: ~$1,306 more per resident in King County (King ≈ 2.4x Pierce). The gap holds across the whole 2015–2024 series, not just 2024. Preliminary 2025 filings (partial early-cycle) show the same pattern: King ~$5.86B vs Pierce ~$935M in expenditures.

**How to read this**

- These are **actual expenditures as filed** with the Washington State Auditor (FIT headline basis, which excludes internal service funds) — not adopted budgets, and not checkbook transactions. Both counties come from the same source with the same accounting basis, so the comparison is apples-to-apples on measurement.
- "Per resident" uses each county's official April 1, 2024 resident population estimate from OFM, matching the 2024 fiscal (calendar) year.
- A higher number does not automatically mean "more wasteful" or "better funded." The two county governments carry **different service responsibilities**: King County directly operates Metro Transit, Harborview-related health functions, and a large regional wastewater utility inside its county budget, while in Pierce County transit is run by a separate agency (Pierce Transit) that does not appear in the county's filed totals. A meaningful chunk of the gap reflects what each county government does, not how efficiently it does it.
- King County files in round thousands, so its figures are slightly less precise than Pierce's.

**Trace**

- Source: `washington.fit_filed_actuals` (SAO Financial Intelligence Tool, filed annual actuals) + `washington.ofm_population` (OFM April 1 official estimates); recipe `budget_scale.cross_jurisdiction` with `budget_scale.per_capita`
- Public sources: https://portal.sao.wa.gov/FIT/ ; https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
- Snapshots: FIT `milestone-2025-published-2026-06-30` (Snapshot 33, published 2026-06-30); OFM `2025-04-01`
- Data-through: filed years 2015–2024 complete; 2025 partial (early filing cycle)
- Grain: government x year (FIT); county x estimate year (OFM)
- Measure: `total_expenditures` (filed actuals, excl. internal service funds) / `population` (resident, April 1, 2024 estimate)
- Filters: `government-annual-totals.jsonl`, government in {King County, Washington; Pierce County, Washington}, year = 2024; `population-estimates.jsonl`, `row_type=county`, `estimate_date=2024-04-01`
- Check: same source, same `amount_basis=filed_actuals_excl_internal_service` for both counties; summary.json confirms both counties have complete 2015–2024 coverage (110 rows total); skill spot-check (KCRHA 2024 expenditures $191,618,113) matches the snapshot; denominator estimate date falls within the 2024 fiscal year
- Caveats: actual expenditures, not budgets; not comparable to King County's adopted biennial budget headline or its Open Budget Dashboard budgeted values; service responsibilities differ (e.g., Metro Transit is inside King County's totals, Pierce Transit is a separate district), so per-resident levels partly reflect scope, not efficiency; King County files in round thousands; resident population, not service or daytime population; 2025 values are partial and excluded from the headline comparison
