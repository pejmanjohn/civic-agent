---
case: evergreen-schools-cuts
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:** No — Evergreen Public Schools (Evergreen School District, Clark County) is not taking in less money than it used to over the whole period we can see, but its revenues have fallen from their 2023 peak and have essentially flatlined since, while its spending has kept climbing. Total revenues in school year 2024-25 (~$488.8M) were about 17% higher than in 2019-20 (~$419.2M), but about $36M (-6.9%) below the 2022-23 peak (~$524.9M). Meanwhile expenditures rose every year, from ~$362.9M to ~$431.1M. So the squeeze is real: flat-to-declining nominal revenue since 2023 plus rising costs (and inflation) narrows what the district can afford, even though it is not literally "getting less money than it used to" versus five years ago.

**Numbers** (total revenues / total expenditures, as filed; school fiscal years ending Aug 31):

| School year | Total revenues | Total expenditures |
|---|---|---|
| 2019-20 | $419,220,741 | $362,863,508 |
| 2020-21 | $430,396,817 | $362,667,407 |
| 2021-22 | $482,596,596 | $398,118,098 |
| 2022-23 | $524,942,908 (peak) | $404,676,658 |
| 2023-24 | $489,552,365 | $410,645,920 |
| 2024-25 | $488,762,832 | $431,111,961 |

- Revenues 2019-20 → 2024-25: +$69.5M (+16.6%)
- Revenues 2022-23 → 2024-25: -$36.2M (-6.9%)
- Expenditures 2019-20 → 2024-25: +$68.2M (+18.8%)

**How to read this:** These are actual revenues and expenditures as the district reported them to OSPI (F-196, modified accrual) — not budgets, and not staffing data. The 2022-23 peak and subsequent drop likely reflects the wind-down of one-time federal pandemic (ESSER) funds, though this source does not break out revenue by type. Figures are nominal dollars: with inflation, roughly flat revenue since 2023 buys less each year, and per-pupil resources also depend on enrollment, which this source does not cover. Importantly, this source says nothing about teacher counts or FTE — whether cuts were forced by these revenue trends or by other choices (enrollment loss, levy capacity, cost growth) is interpretation beyond the data. For staffing and per-pupil detail, the district's F-196/budget documents and OSPI's school apportionment reports are the official path.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), school district rows as reported to OSPI
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30); file `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/school-district-annual-totals.jsonl`
- Data-through: school fiscal year ending 2025-08-31 (school coverage 2020-2025)
- Grain: government x school fiscal year
- Measure: `total_revenues`, `total_expenditures` (amount basis `ospi_modified_accrual_f196`)
- Filters/query logic: `government = "Evergreen School District (Clark County)"` (mcag 1841), sorted by `school_fiscal_year_ending_aug31`
- Check: 6 of 6 expected Evergreen rows returned; `summary.json` row count for school-district-annual-totals.jsonl = 12 (two districts x 6 years) matches; spot check Seattle SD 2024-25 revenues $1,518,641,110.55 present in summary
- Caveats: filed actuals, not budgets; modified accrual, school FY ends Aug 31; nominal dollars, not inflation- or enrollment-adjusted; no revenue-source or staffing/FTE breakdown at this grain; teacher-cut causation is policy interpretation, not a claim this source supports

**Answer mode: exact** — the revenue-trend question is fully answered from one accepted source with compatible semantics across all years shown; the staffing/causation piece is explicitly flagged as outside the source.
