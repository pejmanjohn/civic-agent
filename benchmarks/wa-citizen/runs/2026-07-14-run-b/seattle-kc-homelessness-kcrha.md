---
case: seattle-kc-homelessness-kcrha
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** There is no single accepted source that totals "homelessness spending" for Seattle and King County, but the core of the regional system is measurable: the King County Regional Homelessness Authority (KCRHA) — the joint agency Seattle and King County created in 2019 and fund together — actually spent about **$499.8 million from 2021 through 2024**, growing every year to **$191.6M in 2024**. Seattle separately *budgets* homelessness programs inside its Human Services Department (about **$164.8M approved for 2026**, most of it the city's transfer to KCRHA). King County's own homelessness line cannot be isolated from accepted sources; its human-services department budget is far broader than homelessness.

**Numbers:**

KCRHA actual expenditures (filed actuals, as reported to the State Auditor):
- 2021: $3.0M (startup year) | 2022: $132.5M | 2023: $172.6M | 2024: $191.6M
- 2021–2024 cumulative: ~$499.8M. 2024 ran a deficit year: $191.6M spent vs $180.7M revenues. 2025 is not yet filed.

Seattle approved operating budget, homelessness-named programs (all in the Human Services Department; budget, not actual spend):
- 2024: $113.6M | 2025: $126.2M | 2026: $164.8M
- FY2026 split: KCRHA transfer $126.8M; City-Managed Homelessness Programs $38.1M; HOPE outreach team roughly $0 (small negative offset row)

King County: no accepted source isolates actual homelessness spending. Context only: DCHS (Community and Human Services), which houses homelessness work among much else, has a FY2026 *budgeted* expenditure of $1.624B.

**How to read this:** Three different frames are shown and must not be added together. (1) KCRHA filed actuals are real dollars spent by the joint authority — the cleanest "spent" number — but they are government-wide totals: this source cannot break down where inside KCRHA the money went (shelter vs. outreach vs. admin). (2) Seattle's figures are *approved budget*, not spending, and most of it flows into KCRHA — adding Seattle's transfer to KCRHA's spending would double-count. Program-name matching may also miss homelessness dollars booked under other program names, especially before the 2021 reorganization. (3) King County's contribution also flows into KCRHA and is not separately claimable. For KCRHA program-level detail, the paths are KCRHA's own budget documents and the State Auditor's FIT portal (https://portal.sao.wa.gov/FIT/).

This is a **partial** answer: actual spending is supported for KCRHA only; Seattle is budget-frame only; King County's own homelessness line has no accepted source.

**Trace:**
- Source 1: washington.fit_filed_actuals (SAO Financial Intelligence Tool), snapshot milestone-2025-published-2026-06-30 (FIT Snapshot 33). Public URL: https://portal.sao.wa.gov/FIT/. Data-through: filed years 2015–2024 complete; 2025 early-cycle partial (KCRHA 2025 not filed). Grain: government-year. Measure: total_expenditures, total_revenues (FIT headline basis, excludes internal service funds). Filters: government = "King County Regional Homelessness Authority" (MCAG 3268) in government-annual-totals.jsonl. Check: KCRHA 2024 expenditures 191,618,113 matches the skill's spot check. Caveats: filed actuals, not budgets; no vendor/program breakdown at this grain.
- Source 2: City of Seattle Operating Budget, Socrata 8u2j-imqx. Public URL: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov). Data-through: FY2018–FY2026 approved budget (one-time refresh). Grain: fiscal_year x program. Measure: sum(approved_amount). Filters: upper(program) LIKE '%HOMELESS%'; all matches sit in Human Services Department (74 rows FY2026). Check: FY2024–26 department-grouped totals reconcile to program-grouped totals ($113.6M / $126.2M / $164.8M). Caveats: approved budget, not actuals; name-matching may miss homelessness dollars in other programs; program names changed across years (2018–2020 series is not comparable to post-2021).
- Source 3 (context/boundary): King County Open Budget Dashboard, snapshot 2026-04-01. Public URL: https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard. Grain: FY2026 department. Measure: budgeted_expenditure (DCHS $1.624B, per skill known check). Caveats: budgeted, not actual; department is not a homelessness policy-area total; no program grain available — used only to explain why King County's own homelessness spending is not claimable.
