---
case: evergreen-schools-cuts
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** No — Evergreen Public Schools' total revenues are not lower than they used to be historically, but they have fallen from their 2023 peak. Filed actuals show revenues grew from $419M (school year ending 2020) to a peak of $524.9M (2023), then dropped to about $489M in 2024 and 2025. Meanwhile expenditures rose every year, so the gap between money coming in and going out has narrowed sharply — from a ~$120M cushion in 2023 to ~$58M in 2025. Whether that explains teacher cuts involves staffing, enrollment, and cost data this repo does not carry.

**Numbers (Evergreen School District, Clark County — total revenues / total expenditures as filed, school fiscal years ending Aug 31):**

| Year | Revenues | Expenditures |
|---|---|---|
| 2020 | $419.2M | $362.9M |
| 2021 | $430.4M | $362.7M |
| 2022 | $482.6M | $398.1M |
| 2023 | $524.9M | $404.7M |
| 2024 | $489.6M | $410.6M |
| 2025 | $488.8M | $431.1M |

- Revenues 2023→2025: −$36.2M (−6.9%). Revenues 2020→2025: +$69.6M (+16.6%).
- Expenditures 2020→2025: +$68.2M (+18.8%), rising every single year.

**How to read this:** These are actual revenues and expenditures as filed with OSPI (modified accrual, F-196), not budgets and not teacher counts. The likely resident-felt story: money in did rise through 2023 (a period that included one-time federal pandemic relief), then fell back, while costs kept climbing — a squeeze even without an absolute historical decline. These are nominal dollars: no inflation or per-pupil adjustment is supported, and with inflation the 2025 figure buys less than the same nominal amount did in 2020. Staffing/FTE, enrollment, and layoff decisions are outside every accepted source here; for those, see the district's budget documents and OSPI's school apportionment/personnel reports.

**Answer mode: `partial`** — the revenue trend is fully source-backed (recipe `budget_scale.trend`), but the teacher-staffing link, per-pupil, and inflation-adjusted views need sources this repo doesn't yet accept.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), school data as reported to OSPI
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT Snapshot 33, published 2026-06-30)
- Data-through: school fiscal year ending 2025-08-31; 2025 is an early-filing-cycle milestone snapshot
- Grain: school district × school fiscal year
- Measure: `total_revenues`, `total_expenditures`
- Filters: `government = "Evergreen School District (Clark County)"` (mcag 1841) in `school-district-annual-totals.jsonl`
- Check: summary.json reports 12 school-district rows (6 Evergreen, 6 Seattle SD); spot check Seattle SD 2025 revenues 1,518,641,110.55 matches
- Caveats: filed actuals, not budgets; OSPI modified accrual, school FY ends Aug 31 — not comparable to city/county rows; no vendor, staffing, or enrollment detail; nominal dollars only
