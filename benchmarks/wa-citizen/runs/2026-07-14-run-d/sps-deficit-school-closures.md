---
case: sps-deficit-school-closures
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

Seattle Public Schools' closure debate is about its General Fund operating budget, and no single number "proves" why closures are happening — the factors most often cited (enrollment decline, the expiration of one-time federal COVID relief known as the ESSER cliff, and the state cap on local enrichment levies) are real context, but they are causal claims that the accepted financial sources here cannot themselves adjudicate. What the filed numbers do show: the district is a roughly $1.5B-a-year operation whose total filed expenditures grew about 23% from school year 2019-20 to 2024-25, and whose voter-approved local levies are two of its major local revenue lines. Where the money goes by category (teaching vs. administration vs. buildings) is not yet a reviewed claim in this repo — I can give you audited totals and the official drill-down path, so this is a **partial** answer.

**Numbers** (Seattle School District No. 1, as filed with OSPI/State Auditor; school fiscal years ending Aug 31)

| School year ending | Total revenues | Total expenditures |
|---|---|---|
| 2020 | $1,218,710,222 | $968,088,361 |
| 2021 | $1,301,316,397 | $973,532,276 |
| 2022 | $1,358,142,549 | $1,054,173,545 |
| 2023 | $1,400,752,364 | $1,120,027,429 |
| 2024 | $1,469,813,801 | $1,131,325,593 |
| 2025 | $1,518,641,111 | $1,193,163,296 |

Local property-tax levies (DOR certified, district-wide):
- Seattle #1 Enrichment levy: $194,678,891 in 2025 (rate 0.65422/$1,000) vs $190,239,286 in 2024 — enrichment levies are capped by state law, which limits how much local voters can add for operations.
- Seattle #1 Capital Projects/Technology levy: $365,103,496 in 2025 — larger than the enrichment levy, but restricted to capital/technology, not classroom operations.

**How to read this**

- These are filed all-funds actuals on OSPI's modified-accrual basis — they include restricted capital and debt money, so "revenues exceed expenditures" here does NOT mean the district has an operating surplus. The closure conversation is about the unrestricted General Fund, which these totals do not isolate.
- Filed actuals are not budgets: the deficit figures quoted in closure debates come from the district's budget projections, which depend on modeling choices (forecast vintage, fund scope).
- The levy rows show the structural point concretely: the big capital levy cannot legally backfill operating shortfalls, and the enrichment levy is state-capped.
- Where the money actually goes by category (salaries, special education, transportation, central office) is not a reviewed claim here. Official drill-down path: SPS's own budget book (seattleschools.org), the FIT portal's category views (https://portal.sao.wa.gov/FIT/), and OSPI F-196 reports.
- Enrollment, ESSER expiration, and levy caps are named as context; asserting which one "caused" closures would need enrollment and board-decision sources this repo does not yet accept.

**Trace**

- **Source:** `washington.fit_filed_actuals` — FIT Filed Annual Actuals (school rows as reported to OSPI), snapshot `milestone-2025-published-2026-06-30` (FIT Snapshot 33, published 2026-06-30)
- **Public source:** https://portal.sao.wa.gov/FIT/
- **Data-through:** school fiscal year ending 2025-08-31 (2020-2025 for school districts)
- **Grain:** government x school fiscal year, all-funds totals only
- **Measure:** total_revenues, total_expenditures (OSPI modified accrual, F-196)
- **Filters:** school-district-annual-totals.jsonl, government = "Seattle School District No. 1" (mcag 1903); 6 rows returned of 12 in file
- **Check:** spot check passed — SY2024-25 revenues $1,518,641,110.55 matches summary.json fingerprint
- **Caveats:** filed actuals, not budgets; all-funds basis, does not isolate the General Fund operating picture; category breakdown not a reviewed claim
- **Source:** `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- **Public source:** https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- **Data-through:** tax years due 2024-2025
- **Grain:** one row per levy line, district_key 1704001
- **Measure:** district_levy, levy_rate_per_1000
- **Filters:** levy-detail.jsonl, district_name matches "Seattle #1"; 2 levy lines per year (enrichment, capital projects)
- **Check:** Seattle SD #1 enrichment 2025 = 0.65422 / $194,678,891 matches the skill's documented DOR Table reconciliation (verified 2026-07-13)
- **Caveats:** certified levy amounts due, not collections or tax bills; enrichment-levy cap mechanics cited as statutory context, and ballot-measure details need an elections source
