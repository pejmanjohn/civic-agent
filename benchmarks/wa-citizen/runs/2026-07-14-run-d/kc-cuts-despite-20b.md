---
case: kc-cuts-despite-20b
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
The "$20 billion" and "cutting services" can both be true at once, for three reasons. First, $20.16 billion is a **two-year** headline — the council-adopted 2026–2027 biennial budget — not one year of money; the annual dashboard budget for 2026 is about $8.6 billion. Second, most of that money is legally restricted: transit taxes and fares, utility rates, voter-approved lid-lift levies (Best Starts for Kids, Crisis Care Centers, Parks, Veterans/Family Services), and state/federal grants can only be spent on their dedicated purposes. Cuts land in the much smaller flexible General Fund that pays for courts, jails, the Sheriff, and elections — a big total budget cannot legally backfill it. Third, the county's main flexible revenue, the base property-tax levy, can grow only ~1% per year (plus new construction) under the state levy lid, while wages and inflation grow faster — a built-in structural squeeze.

**Numbers:**
- Adopted 2026–2027 biennial budget (context headline): **$20.16 billion** (two years).
- FY2026 dashboard budgeted expenditure: **$8.599 billion**; budgeted revenue $8.866 billion; budgeted FTE 18,333. These are different frames — do not add or reconcile them.
- Countywide budgeted expenditure trend: 2025 $8.627B → 2026 $8.599B → 2027 $8.852B — the countywide total is roughly flat-to-rising even as specific funds face cuts.
- Levy-lid evidence (DOR, taxes due 2025): King County government's base "County General" levy grew from $432.4M (2024) to $442.3M (2025) — about +2.3%, consistent with the 101% lid plus new construction; the county's own county-type levy lines in total went from $1.064B to $1.048B (10 lines → 8) as some voted lid lifts rolled off. Restricted lid-lift lines (Best Starts for Kids, Crisis Care Centers, AFIS, Parks, Radio, Vets/Family Services) are separate, purpose-bound levies.

**How to read this:**
The accepted sources answer the *scale and structure* of the question exactly, but two pieces are missing, which is why this is a **partial** answer. (1) No accepted King County source breaks the budget into General Fund vs restricted funds, so I cannot quote the flexible share — the official path is the adopted 2026–2027 budget book's General Fund tables. (2) "Cutting services" is a claim about specific programs; the dashboard shows budgeted (authorized) values only, not actual spending or service outcomes, and cannot confirm which services were cut — that requires the executive's/council's budget documents. Also, per the deficit-why rule: any specific "shortfall" number you have seen depends on modeling choices (forecast vintage, fund scope, maintenance- vs policy-level growth); none of those numbers come from these sources.

**Trace:**
- **Sources:** `king_county.adopted_budget` (context-only biennial headline); `king_county.open_budget_dashboard`, snapshot 2026-04-01; `washington.dor_property_tax_levies`, snapshot levies-due-2025.
- **Public sources:** https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27 ; https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard ; https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- **Snapshot / data-through:** dashboard snapshot 2026-04-01 (model refresh 2026-04-01T21:37:44), years 2017–2027; DOR levy detail covers tax years due 2024–2025; adopted-budget headline is the enacted 2026–2027 biennium.
- **Grain:** countywide dashboard year (overview-by-year.jsonl); taxing-district levy line (levy-detail.jsonl, county = King, district_type = county).
- **Measures:** budgeted_expenditure, budgeted_revenue, budgeted_fte; district_levy, levy_rate_per_1000.
- **Filters/query logic:** read overview-by-year.jsonl for 2025–2027; read levy-detail.jsonl filtered to King County county-type district lines, compared year_due 2024 vs 2025.
- **Checks:** FY2026 budgeted expenditure = $8,598,795,612 and FTE = 18,333 match summary.json fingerprint; overview has 11 rows (2017–2027); DOR King County all-districts 2025 total $7,724,787,822 matches the skill's verified spot check.
- **Caveats:** budgeted/authorized dashboard values, not actual spending — "cuts" cannot be verified from this source; $20.16B (biennial) and $8.6B (annual) are different period and budget frames — never add, average, or reconcile them; DOR rows are certified levy amounts due, not collections or tax bills; the General Fund vs restricted-fund split is not in any accepted source yet — the adopted 2026–2027 budget book is the official path.
