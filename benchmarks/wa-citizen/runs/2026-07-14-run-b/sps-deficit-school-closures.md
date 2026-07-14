---
case: sps-deficit-school-closures
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

I can show you Seattle Public Schools' (Seattle School District No. 1) actual money in and money out, and what Seattle property owners pay it in local levies — but the accepted sources here cannot verify *why* the district is closing or consolidating schools. School closures are a board policy decision the district has publicly tied to enrollment decline and a General Fund operating gap; enrollment counts, per-school costs, and fund-level (General Fund vs. capital) balances are not in this repo's sources, so I present that rationale as the district's stated position, not a verified fact. Notably, on the all-funds filed-actuals basis available here, SPS's total revenues have *exceeded* total expenditures every year since 2019-20 — which shows why the closure debate can't be settled from headline totals alone: those totals mix operating money with restricted capital-levy money that can't legally pay teachers.

**Numbers**

Filed actuals (OSPI F-196, all funds, school fiscal years ending Aug 31):

| School year | Total revenues | Total expenditures |
|---|---|---|
| 2019-20 | $1.219B | $0.968B |
| 2020-21 | $1.301B | $0.974B |
| 2021-22 | $1.358B | $1.054B |
| 2022-23 | $1.401B | $1.120B |
| 2023-24 | $1.470B | $1.131B |
| 2024-25 | $1.519B | $1.193B |

Expenditures grew ~23% over five years; revenues ~25%.

Local property-tax levies certified for SPS (DOR, tax year due 2025): Enrichment (operations) levy $194.7M at $0.65422 per $1,000 assessed value (up from $190.2M in 2024); Capital projects/technology levy $365.1M at $1.22694 (up from $363.8M). Together about $560M/year of local property tax — but the larger capital levy is restricted money that cannot close an operating deficit.

**How to read this**

- These are actual filed revenues/expenditures, not budgets, and not a program- or school-level breakdown. "Where the money goes" by program (teaching, special ed, transportation, administration, individual schools) needs the district's adopted budget and OSPI's F-196 detail — not yet accepted sources here. Official paths: SPS budget documents, OSPI's district financial reporting, and the State Auditor's FIT portal (https://portal.sao.wa.gov/FIT/).
- The all-funds surplus does NOT mean the district's General Fund is healthy: capital-levy and bond receipts sit in revenues but are legally walled off from operations. A fund-level view would be required to confirm or refute a structural operating deficit.
- Levy rows are certified amounts due to the district, not your tax bill; rates are per $1,000 of your parcel's assessed value.
- The closure rationale (enrollment decline, under-enrolled buildings) is policy interpretation attributed to the district, separate from the budget facts above.

**Answer mode: partial** — money-in/money-out and levy facts are exact from accepted sources; the "why closures" causal claim and the program-level "where does it go" breakdown are unsupported here, with official paths named.

**Trace**

- Source 1: `washington.fit_filed_actuals` — FIT Filed Annual Actuals, school district table (OSPI data), snapshot `milestone-2025-published-2026-06-30` (FIT Snapshot 33, published 2026-06-30)
- Public source: https://portal.sao.wa.gov/FIT/
- Data-through: school fiscal years ending Aug 31, 2020-2025 (SY2024-25 filed)
- Grain: school district x school fiscal year, all-funds totals
- Measure: total_revenues, total_expenditures (OSPI modified accrual, F-196 basis)
- Filters: government = "Seattle School District No. 1" (mcag 1903) in `school-district-annual-totals.jsonl`; 6 rows returned
- Check: SY2024-25 revenues = $1,518,641,110.55, matching the source card spot check exactly; snapshot summary.json row count (12 school rows) matches
- Caveats: filed actuals, not budgets; all-funds totals mask fund restrictions; school accounting basis differs from cities/counties — do not compare numerically

- Source 2: `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Data-through: tax years due 2024 and 2025
- Grain: one row per levy (district_key 1704001, levy lines "Seattle #1 Enrichment" and "Seattle #1 Proj.")
- Measure: district_levy, levy_rate_per_1000
- Filters: county = King, district_type = local_school, district name contains "Seattle #1"
- Check: 2025 enrichment $194,678,891 at 0.65422 matches the source card spot check (reconciled to DOR tables, verified 2026-07-13)
- Caveats: certified levy amounts due, not collections, budgets, or household bills; capital levy restricted to capital/technology uses
