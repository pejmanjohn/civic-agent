---
case: seattle-kc-homelessness-kcrha
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** There is no single "Seattle + King County homelessness spending" number in the accepted sources, but the closest actual-spending fact is this: most of both governments' homelessness money now flows through their joint agency, the King County Regional Homelessness Authority (KCRHA), whose filed actual expenditures grew from about $3.0M in its 2021 startup year to $191.6M in 2024. Seattle's own approved budget shows roughly $100–165M per year flowing to homelessness programs — the bulk of it as its contribution to KCRHA. A King-County-side homelessness-specific spending line, and a category-level "where did it go" breakdown, are not yet covered by an accepted source.

**Numbers:**

*KCRHA actual expenditures as filed with the State Auditor (the main joint spending channel):*
- 2021: $3.0M (startup year); revenues $3.9M
- 2022: $132.5M; revenues $115.2M
- 2023: $172.6M; revenues $156.1M
- 2024: $191.6M; revenues $180.7M (a deficit year — spending exceeded revenues)
- 2025: not yet filed in this snapshot (early filing cycle)

*Seattle approved operating budget, Human Services Department homelessness programs (budgeted, not actual spending):*
- FY2024: ~$113.6M total (KCRHA contribution $99.7M; City-Managed Homelessness Programs $12.6M; HOPE Team $1.4M)
- FY2025: ~$126.2M total (KCRHA $104.6M; City-Managed $15.8M; HOPE Team $5.8M)
- FY2026: ~$164.8M total (KCRHA $126.8M; City-Managed $38.1M)
- Earlier frame: FY2018–FY2020 "Homelessness Prevention & Support" ran $20–32M/year before the KCRHA consolidation.

*King County:* the accepted county source only supports department-level budgeted values (DCHS — Community and Human Services, FY2026 budgeted expenditure $1.624B), which is far broader than homelessness. No homelessness-specific King County spending claim is supported.

**How to read this:** Three different frames are shown side by side, not added together. KCRHA numbers are actual annual expenditures as filed (FIT headline basis, excludes internal service funds) — the truest "spent" figure available. Seattle numbers are approved budget amounts, not payments, at program grain in one department; homelessness-related spending in other departments (e.g., housing capital, encampment cleanup in Parks/SPU) would not appear under these program names. Seattle's KCRHA contribution is also a large share of KCRHA's revenue, so summing Seattle + KCRHA double-counts. "Where did it go" below the totals (shelter vs. outreach vs. admin, or by vendor) is not answerable from accepted sources; the path is KCRHA's own budget documents and its filings in the State Auditor's Financial Intelligence Tool (https://portal.sao.wa.gov/FIT/), plus King County DCHS budget documents for the county side.

**Answer mode:** partial — KCRHA filed actuals and Seattle approved program budgets are source-backed; a King County homelessness-specific line, a combined deduplicated total, and a category breakdown are missing.

**Trace:**
- Source 1: `washington.fit_filed_actuals` — FIT Filed Annual Actuals, snapshot `milestone-2025-published-2026-06-30` (Snapshot 33, published 2026-06-30)
  - Public source: https://portal.sao.wa.gov/FIT/
  - Data-through: filed years 2015–2024 complete; 2025 partial (KCRHA 2025 not yet filed)
  - Grain: government × year; Measure: total_expenditures, total_revenues
  - Filters: government = "King County Regional Homelessness Authority" (mcag 3268) in `government-annual-totals.jsonl`
  - Check: matches skill spot check — KCRHA 2024 expenditures 191,618,113 vs revenues 180,707,326
  - Caveats: filed actuals, not budgets; FIT headline basis excludes internal service funds; no vendors or spending categories at this grain; KCRHA files in round-ish amounts
- Source 2: City of Seattle Operating Budget, Socrata `8u2j-imqx` (live API query)
  - Public source: https://data.seattle.gov/resource/8u2j-imqx.json (OpenBudget: https://openbudget.seattle.gov)
  - Data-through: FY2018–FY2026 approved budget publication (static)
  - Grain: fiscal_year × department × program; Measure: sum(approved_amount)
  - Filters: upper(program) like '%HOMELESS%', grouped by year/department/program
  - Check: 23 grouped rows returned, all in Human Services Department; FY2026 KCRHA program $126.8M consistent with HSD scale in skill checks
  - Caveats: approved budget, not actual spending; name-based program filter may miss homelessness-related lines elsewhere; program names/structure changed across years (2021 consolidation into KCRHA); small negative row (HOPE Team FY2026, −$4,252) is an accounting offset
- Source 3 (boundary): King County Open Budget Dashboard, snapshot `2026-04-01` — supports only department-grain budgeted values (DCHS $1.624B FY2026 budgeted expenditure); no homelessness program grain; not used for a homelessness claim.
