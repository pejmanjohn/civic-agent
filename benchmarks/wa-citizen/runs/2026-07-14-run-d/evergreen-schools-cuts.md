---
case: evergreen-schools-cuts
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
Not compared with five years ago — but yes compared with its recent peak. Evergreen Public Schools' filed total revenues climbed through the pandemic years to a peak of about $524.9M in the 2022-23 school year, then dropped roughly $35M in 2023-24 and stayed essentially flat in 2024-25. Meanwhile filed expenditures rose every single year. So the district isn't poorer than it was in 2020 in raw dollars — it's that the money stopped growing (and fell from the peak) while costs kept climbing. That squeeze is the fiscal backdrop for staffing cuts, though this source can't confirm teacher counts or say what caused the cuts.

**Numbers:**
Filed total revenues and expenditures, Evergreen School District (Clark County), OSPI modified accrual, school fiscal years ending Aug 31, nominal dollars:

| School year | Total revenues | Total expenditures |
|---|---|---|
| 2019-20 | $419.2M | $362.9M |
| 2020-21 | $430.4M | $362.7M |
| 2021-22 | $482.6M | $398.1M |
| 2022-23 | $524.9M | $404.7M |
| 2023-24 | $489.6M | $410.6M |
| 2024-25 | $488.8M | $431.1M |

- Revenue from peak (2022-23) to 2024-25: **down $36.2M (−6.9%)**
- Expenditures over the same two years: **up $26.4M (+6.5%)**
- Revenue vs. 2019-20: still **up 16.6%** in nominal dollars

A chart of this series is available on request.

**How to read this:**
- These are filed actual revenues and expenditures as reported to OSPI — not the district's adopted budget, and not teacher headcount. Staffing/FTE is not something this source can answer.
- The numbers are nominal. No inflation or per-student adjustment is available from accepted sources here, so "less money in real terms or per pupil" can't be computed — with 2022-25 inflation, flat-to-falling nominal revenue very likely means declining real purchasing power, but that's framing, not a sourced number.
- Context, not asserted causes: the 2021-23 bump and 2023-24 drop are consistent with the statewide pattern of one-time federal pandemic (ESSER) aid arriving and expiring, and enrollment affects state funding — but attributing the teacher cuts to any specific factor would need district budget documents and enrollment data, which are outside this source.
- Revenues exceeding expenditures at this total-funds grain does not mean the operating fund is comfortable; fund-level breakdowns are not a reviewed claim here.

**Trace:**
- **Source:** `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments); school data as reported to OSPI (F-196)
- **Public source:** https://portal.sao.wa.gov/FIT/
- **Snapshot:** `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- **Data-through:** school fiscal year 2024-25 (ended Aug 31, 2025); freshness within the source's quarterly-milestone cadence as of today
- **Grain:** school district × school fiscal year (totals only)
- **Measure:** `total_revenues`, `total_expenditures` (OSPI modified accrual, `amount_basis = ospi_modified_accrual_f196`)
- **Filters/query logic:** read `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/school-district-annual-totals.jsonl`, filter `government = "Evergreen School District (Clark County)"` (mcag 1841), sort by `school_fiscal_year_ending_aug31`
- **Check:** 12 school-district rows in snapshot per `summary.json`; sibling spot check Seattle SD No. 1 2024-25 revenues = $1,518,641,110.55 matches the source card's validation value
- **Caveats:** filed actuals, not budgets; totals only — no fund/program/staffing breakdown; school fiscal years end Aug 31 on a different basis than city/county filings; nominal dollars, no inflation or per-pupil adjustment; teacher-cut causation not inferable from these totals; milestone snapshots revise quarterly

**Answer mode:** `partial` — the nominal revenue trend is fully source-backed, but the question's real substance ("less money" relative to costs, students, and staffing) is missing accepted inflation, enrollment, and staffing sources; those gaps are named above.
