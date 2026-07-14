---
case: evergreen-schools-cuts
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
Partly. Evergreen Public Schools (Evergreen School District, Clark County) is not getting less money than it did five years ago — total revenues in the 2024‑25 school year were about 17% higher than in 2019‑20. But revenues have fallen from their 2022‑23 peak: the district took in about $36M less in 2023‑24 than the year before and stayed essentially flat in 2024‑25, while its expenditures kept rising every year. So "less money than at the recent peak, while costs keep climbing" is accurate; "less money than it used to get overall" is not. Note: no accepted source here covers teacher staffing/FTE, so this answer addresses only the money side, not whether teacher cuts occurred or were necessary.

**Numbers** (total revenues / total expenditures as filed, school fiscal years ending Aug 31):
- 2020: $419.2M / $362.9M
- 2021: $430.4M / $362.7M
- 2022: $482.6M / $398.1M
- 2023: $524.9M / $404.7M (revenue peak)
- 2024: $489.6M / $410.6M (revenue −$35.4M, −6.7% vs 2023)
- 2025: $488.8M / $431.1M (revenue −0.2% vs 2024; expenditures +5.0%)

From 2020 to 2025: revenues +$69.5M (+16.6%), expenditures +$68.2M (+18.8%).

**How to read this:**
- These are actual revenues and expenditures as filed with OSPI/the State Auditor — not the district's adopted budget, and not a teacher headcount.
- The 2023 peak and 2024 drop largely bracket the wind-down of one-time federal pandemic (ESSER) funding, though this source doesn't break out revenue by type — that pattern would need district budget documents to confirm.
- These are nominal dollars. With 2020–2025 inflation, roughly flat revenues since 2022 mean less purchasing power per dollar, and salaries (the biggest school cost) rise with inflation — which is how a district can face cuts even with revenues above 2020 levels.
- Revenues exceeding expenditures in a given year does not mean spare cash for teachers: totals include restricted funds (capital, bonds, levies) that can't pay classroom salaries.
- Enrollment matters too (per-pupil funding drives district revenue), but this source has no enrollment data.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), school data as reported to OSPI
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- Data-through: school fiscal years 2020–2025 (years ending Aug 31); file: `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/school-district-annual-totals.jsonl`
- Grain: government × school fiscal year
- Measure: `total_revenues`, `total_expenditures` (amount basis: `ospi_modified_accrual_f196`)
- Filters/query logic: `government = "Evergreen School District (Clark County)"` (mcag 1841), all 6 years
- Check: summary.json reports 12 school-district rows (2 districts × 6 years) covering 2020–2025; spot check Seattle SD 2024‑25 revenues = $1,518,641,110.55 matches the skill's documented value
- Caveats: filed actuals, not budgets; OSPI modified accrual basis, school FY ends Aug 31 — not comparable to city/county figures; no revenue-by-source, staffing/FTE, or enrollment detail at this grain; nominal dollars, not inflation-adjusted; teacher-cut claims cannot be verified or refuted from this source

**Answer mode: partial** — the revenue-trend half of the question is answered exactly from an accepted source; the teacher-staffing half has no accepted source (the path there is the district's own budget documents and OSPI's personnel/S-275 reporting).
