---
case: seattle-kc-homelessness-kcrha
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** There is no single "homelessness budget" here — that fragmentation is part of the answer. Spending splits across three governments: the City of Seattle (which budgets ~$165M for homelessness in 2026, most of it passed through to a regional authority), the King County Regional Homelessness Authority (KCRHA, which actually spent ~$192M in 2024 pooling city and county money), and King County itself (whose homelessness-specific spending has no accepted source-backed number yet — only its ~$1.62B Community and Human Services department budget, which includes much more than homelessness).

**Numbers:**
- Seattle FY2026 approved operating budget, homelessness-named programs (all in the Human Services Department): **$164.8M total** — KCRHA pass-through $126.8M, City-Managed Homelessness Programs $38.1M, HOPE Team ~$0 (a -$4,252 offset row in 2026; it was $5.8M in 2025).
- Seattle trend: the KCRHA program line grew from $96.9M (2023) to $126.8M (2026); pre-KCRHA (2018-2020) the city's "Homelessness Prevention & Support" program ran $20-32M/yr — the structure changed, so this is not one continuous series.
- KCRHA filed actuals (where pooled money actually went out the door): 2022 spent $132.5M, 2023 $172.6M, **2024 $191.6M** (against $180.7M revenues — a deficit year). 2025 is not yet filed.
- King County: FY2026 budgeted expenditure for DCHS (Community and Human Services) is $1.624B, but a homelessness-specific breakdown is not a reviewed claim from any accepted source.

**How to read this:**
1. **Do not add Seattle + KCRHA.** Seattle's $126.8M KCRHA line is city money flowing INTO the authority; KCRHA's $191.6M in expenditures includes that same money plus county and other funds. Adding them double-counts.
2. **Budgets vs. actuals are different frames.** Seattle numbers are approved budget allocations; KCRHA numbers are actual expenditures as filed with the State Auditor. They are kept separate above, not reconciled.
3. **The Seattle figure is a lower bound** — it captures programs literally named for homelessness. Related spending (affordable housing via the Office of Housing, emergency response, behavioral health) sits in other programs and departments.
4. **Spending totals are not outcome claims.** These numbers say nothing about effectiveness; an outcome answer would need shelter/housing placement and point-in-time count data, which no accepted source here provides.

**Answer mode: `partial`** — Seattle allocations and KCRHA actuals are source-backed; King County's homelessness-specific share is missing (its dashboard supports department grain only; FIT supports government totals only). The path: King County's adopted budget book DCHS sections and the FIT portal's category views (https://portal.sao.wa.gov/FIT/).

**Trace:**
- **Source 1:** `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`) — https://data.seattle.gov/resource/8u2j-imqx.json — live API query at answer time; known years FY2018-FY2026 (metadata June 2026)
- **Grain/Measure/Filters (1):** fiscal_year × program; sum(`approved_amount`); `upper(program) like '%HOMELESS%' OR program like '%HOPE%'` — 74 FY2026 rows, all in Human Services Department
- **Check (1):** FY2026 filtered total $164,813,730.59; FY2026 dataset-wide total ~$7.312B / 7,622 rows per skill validation
- **Caveats (1):** approved budget, not actual spending; program-name filter is a lower bound; "Homelessness Prevention and Support" rows sum to $0 from 2023 on (structure moved to KCRHA/City-Managed lines)
- **Source 2:** `washington.fit_filed_actuals` (SAO Financial Intelligence Tool) — https://portal.sao.wa.gov/FIT/ — snapshot `milestone-2025-published-2026-06-30` (FIT Snapshot 33); filed years complete through 2024
- **Grain/Measure/Filters (2):** government × year totals; `total_expenditures`/`total_revenues`, basis `filed_actuals_excl_internal_service`; government = King County Regional Homelessness Authority (MCAG 3268)
- **Check (2):** KCRHA 2024 expenditures 191,618,113 matches the skill's spot check exactly
- **Caveats (2):** filed actuals, not budgets; totals only, no category/vendor detail; 2025 not yet filed for KCRHA
- **Source 3:** `king_county.open_budget_dashboard` — https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard — snapshot `2026-04-01`; department grain, `budgeted_expenditure`; DCHS FY2026 = $1.624B (context only — not a homelessness figure); check: 22 dept rows totaling $8.599B
- **Composition rule:** budgeted allocations and filed actuals presented side by side per the router's homelessness playbook; no cross-source addition; managed local checkbook database unavailable this session (hosted snapshots used instead)
