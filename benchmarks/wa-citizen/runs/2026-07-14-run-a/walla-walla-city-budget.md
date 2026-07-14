---
case: walla-walla-city-budget
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
There is no adopted-budget source accepted in this system for the City of Walla Walla yet, so I can't quote the city's official budget document number. What I can give you, from an accepted official source, is what Walla Walla actually takes in and spends each year as filed with the Washington State Auditor: in 2024 (the latest complete filed year), the city reported about **$117.5 million in total revenues** and **$96.3 million in total expenditures**. These are actuals, not the adopted budget — a city's adopted budget is typically a somewhat larger appropriation figure across all funds.

**Numbers:**
- 2024 filed actuals: total revenues **$117,546,221**; total expenditures **$96,284,787**
- 2025 filed actuals (early filing cycle — treat as partial/preliminary): revenues $119,402,110.54; expenditures $100,136,521.26
- Recent trend (filed expenditures): 2020 $76.2M → 2022 $84.6M → 2023 $90.0M → 2024 $96.3M
- Context: Walla Walla's official April 1, 2025 resident population is **34,850** (OFM). Illustratively, 2024 expenditures work out to roughly $2,780 per resident — an approximation only, since the fiscal year and estimate date differ.

**How to read this:**
These are **filed annual actuals** on the State Auditor's FIT headline basis (all funds, excluding internal service funds) — they include enterprise utilities and capital activity, which is why revenues exceed expenditures in most years. They are not the adopted budget, not a general-fund figure, and not checkbook transactions. For the city's actual adopted budget (Walla Walla budgets on a two-year cycle), the official path is the city's own budget documents at wallawallawa.gov and the State Auditor's Financial Intelligence Tool at https://portal.sao.wa.gov/FIT/, which publishes filed financials for every Washington local government.

**Answer mode:** `partial` (recipe `budget_scale.current_total`) — the accepted source answers the "how big is the city's finances" question on the filed-actuals frame; the adopted-budget frame is a known official source not yet accepted here.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), snapshot `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30); population context from `washington.ofm_population`, snapshot `2025-04-01`
- Public source: https://portal.sao.wa.gov/FIT/ (FIT); https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/ (OFM)
- Data-through: filed years 2015–2024 complete; 2025 early-cycle partial; OFM estimate date 2025-04-01
- Grain: government × year (annual totals)
- Measure: `total_revenues`, `total_expenditures`
- Filters/query logic: `government-annual-totals.jsonl`, filter `government = "City of Walla Walla"` (mcag 0773); OFM `population-estimates.jsonl`, `jurisdiction = "Walla Walla"`, `row_type = "city_town"`, `estimate_date = "2025-04-01"`
- Check: 110 government-annual rows in snapshot summary; Walla Walla present with years 2015–2025; snapshot spot checks (e.g., Spokane 2024 revenues 729,876,646) match the source card
- Caveats: filed actuals, not an adopted budget; FIT headline basis excludes internal service funds; includes utilities/enterprise and capital funds; 2025 values are partial early-cycle filings; per-resident figure is illustrative (fiscal year vs. April 1 estimate mismatch); do not mix these numerically with the city's adopted budget figures.
