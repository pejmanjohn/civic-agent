---
case: walla-walla-city-budget
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
This repo does not yet carry the City of Walla Walla's adopted budget document, so I can't quote "the budget" as the city council adopted it. What I can give you, from an accepted official source, is what Walla Walla **actually took in and spent** as filed with the Washington State Auditor: in **2024 the city reported about $117.5 million in total revenues and $96.3 million in total expenditures** (all funds, FIT headline basis). Early 2025 filings show roughly $119.4M revenues / $100.1M expenditures, but 2025 is a partial early-cycle filing. For the adopted budget itself, the official path is the city's own budget documents (wallawallawa.gov) and the State Auditor's Financial Intelligence Tool at https://portal.sao.wa.gov/FIT/.

**Numbers (filed actuals, all city funds):**

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2020 | $93.4M | $76.2M |
| 2021 | $105.7M | $77.2M |
| 2022 | $107.6M | $84.6M |
| 2023 | $109.1M | $90.0M |
| 2024 | $117.5M | $96.3M |
| 2025 (partial) | $119.4M | $100.1M |

Exact 2024 values: revenues $117,546,221; expenditures $96,284,787. For scale context: OFM's official April 1, 2025 resident population estimate for the City of Walla Walla is 34,850. A chart of the full 2015-2025 series is available on request.

**How to read this:**
- These are **filed actual revenues and expenditures**, not an adopted or proposed budget. A budget is a plan the council authorizes in advance; these are the dollars that actually flowed, as the city reported them to the State Auditor.
- Totals cover **all city funds** — general fund plus utilities (water, sewer, etc.), streets, and other restricted funds — on FIT's headline basis, which excludes internal service funds. Much of the total is restricted money the council can't redirect to general services.
- Expenditures running below revenues does not by itself mean "surplus to spend" — capital timing, reserves, and fund restrictions all sit inside these totals.
- The 2025 row comes from the early filing cycle and should be treated as partial until the filing milestone completes.

**Trace:**
- **Source:** `washington.fit_filed_actuals` (FIT Filed Annual Actuals, reviewed governments) — City of Walla Walla, MCAG 0773; population context from `washington.ofm_population`
- **Public source:** https://portal.sao.wa.gov/FIT/ (population: https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/)
- **Snapshot:** `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30); OFM snapshot `2025-04-01`
- **Data-through:** filed years 2015-2024 complete; 2025 partial (early filing cycle)
- **Grain:** government x year (annual totals, all funds)
- **Measure:** `total_revenues`, `total_expenditures` (`amount_basis` = filed actuals excluding internal service funds)
- **Filters:** `government = "City of Walla Walla"` in `government-annual-totals.jsonl` (11 rows, 2015-2025); OFM row `jurisdiction = "Walla Walla"`, `row_type = "city_town"`, estimate date 2025-04-01
- **Check:** snapshot `summary.json` spot checks reconcile (e.g., City of Spokane 2024 revenues $729,876,646; expenditures $648,638,448); file row count 110 matches summary
- **Caveats:** filed actuals, not a budget frame — do not mix numerically with adopted budget figures; totals-only claim, no department/category breakdown is reviewed at this grain; not checkbook/vendor transactions; 2025 partial; per-resident math would use the OFM denominator, never FIT's population field

**Answer mode:** `partial` — the actuals claim is exact and validated, but the adopted-budget frame the question literally asks for is not yet an accepted source; the official path is named above.
