---
case: pierce-vs-king-per-resident
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Pierce County government spends substantially LESS per resident than King County government — roughly $900–930 per resident versus roughly $2,200–2,230 in 2024, the latest complete filed year. King County spends about 2.4x more per resident. But this is not a fair "efficiency" comparison: King County runs far more regional services per resident (Metro Transit, regional wastewater treatment, Public Health – Seattle & King County) than Pierce County does, so a large share of the gap is service scope, not spending intensity.

**Numbers (2024 filed actuals, county governments only):**

| | Total expenditures (2024) | Per resident (OFM Apr 1, 2025 pop) | Per resident (FIT year-aligned 2024 pop) |
|---|---|---|---|
| King County | $5,312,711,000 | ~$2,203 (pop 2,411,700) | ~$2,234 (pop 2,378,100) |
| Pierce County | $883,659,316 | ~$921 (pop 959,900) | ~$928 (pop 952,600) |

Per-resident revenues (2024, year-aligned pop): King ~$2,609; Pierce ~$1,140. The gap is stable across recent years — 2025 early-cycle filings (partial) show the same pattern (King ~$2,430/resident, Pierce ~$974).

**How to read this:** These are actual expenditures as filed with the Washington State Auditor (FIT headline basis, excluding internal service funds) — not adopted budgets, and county government only (spending by Tacoma, Seattle, other cities, school districts, and special districts inside each county is excluded). Both counties are measured from the same source with the same accounting basis and the same annual period, so the side-by-side is legitimate; the per-resident denominators are official OFM April 1 resident estimates. The honest takeaway for a resident: King County government simply does more per resident (transit alone is billions), so "spends more" does not mean "wastes more" — and "spends less" does not mean Pierce residents get less government overall, since some equivalent services are delivered by other entities (e.g., Pierce Transit is a separate agency not in these figures).

Answer mode: **partial** — both budget claims and both denominators come from accepted sources with compatible semantics, but the primary OFM denominator (April 1, 2025 estimate) postdates the 2024 fiscal year. The FIT snapshot's own year-aligned 2024 populations confirm the ratio (~2.4x) is insensitive to this mismatch, and the directional conclusion is unambiguous.

**Trace:**
- Source: `washington.fit_filed_actuals` (SAO Financial Intelligence Tool, milestone Snapshot 33), snapshot `milestone-2025-published-2026-06-30`; denominator `washington.ofm_population`, snapshot `2025-04-01`
- Public sources: https://portal.sao.wa.gov/FIT/ ; https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
- Files: `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`; `jurisdictions/washington/data/ofm-population/2025-04-01/normalized/population-estimates.jsonl`
- Data-through: FIT filed years 2015–2024 complete; 2025 early-cycle partial. OFM estimate date 2025-04-01.
- Grain: government x year (annual totals); county x year (population)
- Measure: `total_expenditures` (and `total_revenues`), divided by resident population
- Filters: `government IN ("King County, Washington","Pierce County, Washington")`, `year = 2024`, `amount_basis = filed_actuals_excl_internal_service`; OFM `row_type = county`, `value_kind = estimate`, `estimate_date = 2025-04-01`
- Checks: skill spot checks passed (Spokane 2024 revenues 729,876,646; Sound Transit 2024 revenues 2,599,304,000; KCRHA 2024 expenditures 191,618,113); OFM King 2,411,700 and Pierce 959,900 match skill's known values; FIT 2025 populations reconcile to OFM 2025 estimates exactly
- Caveats: filed actuals, not budgets; excludes internal service funds; King County files in round thousands; county-government scope only — different regional service responsibilities (King runs Metro Transit, wastewater, public health) make per-capita levels non-comparable as efficiency measures; OFM 2025 denominator vs 2024 fiscal year mismatch (year-aligned FIT populations used as robustness check); no vendor/checkbook grain here.
