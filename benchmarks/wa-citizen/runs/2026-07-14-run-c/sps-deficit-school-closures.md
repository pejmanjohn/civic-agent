---
case: sps-deficit-school-closures
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

The accepted sources here can show *how much* money flows through Seattle Public Schools (Seattle School District No. 1) and where its local property-tax levies stand — but they cannot answer *why* the district is closing schools, and they cannot break spending down by program. School-closure decisions are policy choices the district has publicly tied to enrollment decline and a projected general-fund operating gap; neither enrollment nor the district's internal budget projections are in this repo's accepted sources, so that part is context, not a sourced claim. What the filed actuals do show: SPS is a roughly $1.2-billion-a-year operation whose spending grew about 23% over five school years.

**Numbers** (OSPI F-196 filed actuals, school fiscal years ending Aug 31)

| School year ending | Total revenues | Total expenditures |
|---|---|---|
| 2020 | $1,218.7M | $968.1M |
| 2021 | $1,301.3M | $973.5M |
| 2022 | $1,358.1M | $1,054.2M |
| 2023 | $1,400.8M | $1,120.0M |
| 2024 | $1,469.8M | $1,131.3M |
| 2025 | $1,518.6M | $1,193.2M |

- Expenditures grew +23.3% (2020→2025); revenues +24.6%.
- Local property-tax levies (DOR certified, due 2025): Enrichment levy $194.7M (rate 0.65422/$1,000 AV, up from $190.2M / 0.63479 in 2024); Capital projects & transportation levy $365.1M (1.22694, up from $363.8M / 1.21404). Seattle homeowners pay roughly 1.88 per $1,000 of assessed value to the school district across these two lines.

**How to read this**

- These are all-fund filed totals, not a budget and not a program breakdown. "Where the money goes" by category (teaching, administration, buildings, transportation) needs the OSPI F-196 detail or SPS's own budget book — that grain is not in this source, which is why this answer is partial.
- Filed totals showing revenues above expenditures do NOT contradict the district's stated general-fund structural deficit: these totals mix operating and capital/restricted money (the $365M capital levy cannot pay teachers), so surplus-looking totals at this grain say nothing about the operating gap driving closure discussions.
- The "why": SPS leadership has publicly framed closures around declining enrollment and per-student state funding that doesn't cover fixed building costs. That is policy interpretation from public statements, not from these datasets. Official path for detail: SPS budget documents (seattleschools.org) and OSPI's F-196 reports; filed financials for any WA district are at https://portal.sao.wa.gov/FIT/.

**Trace**

- Source: `washington.fit_filed_actuals`, snapshot `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33); plus `washington.dor_property_tax_levies` (card: dor-property-tax-levies), snapshot `levies-due-2025`
- Public source: https://portal.sao.wa.gov/FIT/ ; https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Data-through: school years ending Aug 31, 2020–2025 (school data as reported to OSPI); levies certified for tax years due 2024–2025
- Grain: district-year total revenues/expenditures (school-district-annual-totals.jsonl); one row per levy line (levy-detail.jsonl, district_key 1704001)
- Measure: total_revenues, total_expenditures (amount_basis ospi_modified_accrual_f196); district_levy, levy_rate_per_1000
- Filters: government = "Seattle School District No. 1" (mcag 1903); district_name LIKE "Seattle #1%" for levy rows
- Check: snapshot spot check seattle_sd_2025_revenues = 1,518,641,110.55 matches; 12 school-district rows total; enrichment levy 0.65422 / $194,678,891 matches skill spot check (reconciled to DOR tables 2026-07-13)
- Caveats: filed actuals, not budgets; no program/category breakdown at this grain — that gap is why the mode is partial; school fiscal years end Aug 31 on OSPI modified accrual (not comparable to city/county bases); levy rows are certified amounts due, not collections or tax bills; the closure rationale is policy interpretation outside these sources.

**Answer mode: partial**
