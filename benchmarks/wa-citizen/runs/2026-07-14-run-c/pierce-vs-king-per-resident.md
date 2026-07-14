---
case: pierce-vs-king-per-resident
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion**

King County spends substantially more per resident than Pierce County — roughly 2.4 times as much. In 2024, the latest complete filed year, King County government's actual expenditures worked out to about **$2,234 per resident**, versus about **$928 per resident** for Pierce County government. Partial 2025 filings point the same direction (~$2,430 vs ~$974). Much of the gap reflects what each county government *does*, not just how generously it does it: King County runs Metro Transit, a large Public Health department, and a regional wastewater utility — functions Pierce County residents receive from separate agencies (Pierce Transit, the state, cities) whose spending is not in the Pierce County line.

**Numbers (filed year 2024, actual expenditures, FIT headline basis)**

| | Total expenditures | Population (OFM Apr 1, 2024) | Per resident |
|---|---|---|---|
| King County govt | $5,312,711,000 | 2,378,100 | ~$2,234 |
| Pierce County govt | $883,659,316 | 952,600 | ~$928 |

Difference: ~$1,306 more per resident in King County (ratio ~2.41x).

**How to read this**

- These are **actual expenditures as filed** with the State Auditor (FIT headline basis, excluding internal service funds) — not adopted budgets, and not checkbook transactions.
- The denominator is OFM's official April 1, 2024 resident population for each whole county, matching the 2024 filing year.
- King County files in round thousands, so its total is approximate at the dollar level.
- Per-resident spending is not a value-for-money score: the two county governments have different service responsibilities, so a direct "more efficient / less efficient" reading is not supported.
- 2025 filings exist for both counties but are early-cycle partial; 2024 is the safest comparison year.

**Answer mode: exact** — both jurisdictions come from the same source with identical amount basis, period type, period status, unit, government scope, and geography basis, plus a matched-year resident denominator.

**Trace**

- Sources: `washington.fit_filed_actuals` (expenditures, both counties) + `washington.ofm_population` (denominators)
- Public sources: https://portal.sao.wa.gov/FIT/ ; https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
- Snapshots: FIT `milestone-2025-published-2026-06-30` (Snapshot 33, published 2026-06-30; filed years 2015-2024 complete, 2025 partial); OFM `2025-04-01`
- Grain: government x year (county rows, mcag 0127 King, 0152 Pierce); county x estimate year for population
- Measure: `total_expenditures` / `population`; per-resident = expenditures divided by April 1, 2024 estimate
- Filters: `government in ("King County, Washington","Pierce County, Washington")`, `year=2024`; population `row_type="county"`, `estimate_date="2024-04-01"`
- Validation: `amount_basis` identical (`filed_actuals_excl_internal_service`) on both rows; FIT `fit_population` fields (2,378,100 / 952,600) match OFM 2024 rows exactly; KCRHA 2024 spot check ($191,618,113) matches the Washington skill's known value
- Caveats: filed actuals, not budgets; excludes internal service funds; King County files in round thousands; service responsibilities differ (Metro Transit, Public Health, and wastewater are inside King County's total, while Pierce Transit is a separate district); 2025 values partial; per-resident figures are scale context, not efficiency scores
