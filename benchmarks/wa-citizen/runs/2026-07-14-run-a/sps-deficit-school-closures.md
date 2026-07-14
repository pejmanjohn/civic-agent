---
case: sps-deficit-school-closures
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

I can show you Seattle Public Schools' (Seattle School District No. 1) actual money picture at the total level, but two honest limits up front. First, "why they're closing schools" is a policy decision — the district has publicly framed consolidation around declining enrollment and a general-fund gap, but my accepted sources don't include enrollment or the district's internal deficit math, so I won't present that as verified fact. Second, "where the money goes" by program (teachers vs. administration vs. buildings) needs a breakdown my accepted source doesn't carry — it reports district-wide totals only. What the filed numbers do show: SPS is a roughly $1.2–1.5 billion-a-year operation, its spending grew about 23% from school year 2019–20 to 2024–25, and at the all-funds level its filed revenues exceeded filed expenditures every year — which is not evidence against a general-fund deficit, because these totals mix the day-to-day fund with capital/levy money that legally can't pay teachers.

**Numbers**

Filed actuals, school fiscal years ending Aug 31 (OSPI modified accrual):

| School year ending | Total revenues | Total expenditures |
|---|---|---|
| 2020 | $1,218.7M | $968.1M |
| 2021 | $1,301.3M | $973.5M |
| 2022 | $1,358.1M | $1,054.2M |
| 2023 | $1,400.8M | $1,120.0M |
| 2024 | $1,469.8M | $1,131.3M |
| 2025 | $1,518.6M | $1,193.2M |

Expenditures rose 23.2% and revenues 24.6% over that span. Local property-tax context (certified levies due, Seattle SD #1): enrichment (operations) levy $190.2M in 2024 → $194.7M in 2025; capital projects/transportation levy $363.8M → $365.1M. These levy figures are calendar-year amounts due — context beside the school-year actuals, not addable to them.

**How to read this**

- These are actual revenues/expenditures as filed with OSPI/the State Auditor — not the district's adopted budget, and not transaction-level detail.
- The totals combine all funds. Capital levy dollars (that ~$365M/yr line) fund buildings, not classroom operations, so a surplus in the combined totals can coexist with a general-fund shortfall — which is the frame in which school-closure debates happen.
- For the program-level "where does it go" answer and the closure rationale, the official path is: SPS's own adopted budget documents, OSPI's F-196 detailed financial reporting, and the State Auditor's FIT portal (https://portal.sao.wa.gov/FIT/), which publishes filed financials for every Washington district.

**Trace**

- Source: `washington.fit_filed_actuals` (FIT milestone Snapshot 33 / OSPI school data), snapshot `milestone-2025-published-2026-06-30`; context from `washington.dor_property_tax_levies`, snapshot `levies-due-2025`
- Public source: https://portal.sao.wa.gov/FIT/ ; https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Data-through: school fiscal years 2020–2025 (ending Aug 31); levies due 2024–2025
- Grain: district-year totals (schools file); one row per levy line (DOR file)
- Measure: `total_revenues`, `total_expenditures`; `district_levy`, `levy_rate_per_1000`
- Filters: `government = "Seattle School District No. 1"` (mcag 1903); DOR `district_key = 1704001` (enrichment + capital lines aggregated by year)
- Check: spot checks match skill values — SD 2025 revenues $1,518,641,110.55; enrichment 2025 rate 0.65422 / $194,678,891; 12 school rows in summary.json
- Caveats: filed actuals, not budgets; OSPI modified accrual, all funds combined — no fund or program breakdown at this grain; school fiscal year differs from calendar-year levy amounts (side-by-side only); enrollment and closure-decision rationale are outside accepted sources; answer mode `partial` — program-level spending breakdown is the missing claim, with OSPI F-196 / SPS budget docs / FIT as the path.
