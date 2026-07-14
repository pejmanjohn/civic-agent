---
case: walla-walla-city-budget
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

There is no adopted-budget source for the City of Walla Walla accepted in this repo yet, so I can't quote the city's official adopted budget number. What I can give you, from an accepted official source, is what Walla Walla **actually took in and spent** as filed with the Washington State Auditor: in 2024 (the most recent complete filed year), the city reported about **$117.5 million in total revenues** and **$96.3 million in total expenditures**. For the city's adopted budget itself, go to the city's own budget documents (wallawallawa.gov) or the State Auditor's Financial Intelligence Tool (https://portal.sao.wa.gov/FIT/).

**Numbers** (filed actuals, FIT headline basis)

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2022 | $107,634,845 | $84,647,347 |
| 2023 | $109,082,502 | $90,001,108 |
| 2024 | $117,546,221 | $96,284,787 |
| 2025 (early filing cycle) | $119,402,111 | $100,136,521 |

Context: Walla Walla's resident population is 34,850 (OFM April 1, 2025 official estimate), so 2024 actual expenditures work out to roughly $2,800 per resident — illustrative only, since the population date and fiscal year don't align exactly.

**How to read this**

- These are **actual revenues and expenditures as filed** with the State Auditor — not the city's adopted or proposed budget. A budget is a plan (spending authority); these are the dollars that actually moved. The two frames should not be mixed numerically.
- Totals are citywide across all funds on the FIT headline basis, which excludes internal service funds. They include enterprise utilities and capital activity, so they run larger than a "general fund" figure you might see in city budget summaries.
- Revenues exceeding expenditures does not mean a "surplus" in a simple sense — capital grants, debt proceeds classified as revenue in some funds, and timing of capital projects all move these totals.
- The 2025 row is from the early filing cycle and should be treated as preliminary.

**Trace**

- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals, reviewed governments (City of Walla Walla, MCAG 0773)
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- Data-through: filed years 2015–2024 complete; 2025 early-cycle partial
- Grain: government × year
- Measure: `total_revenues`, `total_expenditures` (`amount_basis = filed_actuals_excl_internal_service`)
- Filters/query logic: read `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`, filter `government = "City of Walla Walla"`; 11 rows (2015–2025)
- Check: snapshot `summary.json` confirms City of Walla Walla coverage 2015–2025 within 110 government rows; source fingerprint spot checks (e.g., Spokane 2024 revenues 729,876,646) match
- Caveats: filed actuals are NOT a budget — no adopted/proposed budget source is accepted for Walla Walla yet; FIT headline basis excludes internal service funds; 2025 values partial; population denominator from `washington.ofm_population` snapshot `2025-04-01` (Walla Walla city = 34,850, resident basis; https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/); per-resident figure is illustrative, not comparable across governments with different service responsibilities

**Answer mode: partial** — the requested "budget" frame (adopted budget) has no accepted source; the accepted filed-actuals frame is answered exactly, and the official path to the missing frame is named.
