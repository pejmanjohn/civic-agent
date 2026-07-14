---
case: pierce-vs-king-per-resident
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion**

Pierce County spends substantially **less** per resident than King County. On actual spending as filed with the Washington State Auditor for 2024 (the latest complete filed year), King County government spent about **$2,234 per resident**, while Pierce County government spent about **$928 per resident** — roughly **2.4x** more per resident in King County.

**Numbers**

| | King County | Pierce County |
|---|---|---|
| 2024 filed actual expenditures | $5,312,711,000 | $883,659,316 |
| OFM April 1, 2024 resident population | 2,378,100 | 952,600 |
| Actual spending per resident | ~$2,234 | ~$928 |

Both counties' current budgeted frames point the same direction: King County's FY2026 dashboard budgeted expenditure is $8.599B (~$3,565/resident on the April 1, 2025 estimate of 2,411,700), while Pierce County's 2026–2027 biennial budget is $3.501B — approximately $1.75B/yr with the biennium halved, a labeled approximation (~$1,823/resident on the April 1, 2025 estimate of 959,900). These budgeted figures come from different frames (annual dashboard vs. biennial adopted authority) and are shown for direction only, not as a precise comparison.

**How to read this**

- The headline comparison uses filed actual expenditures from the same source, same year (2024, complete), and same accounting basis (FIT headline basis, excluding internal service funds) for both counties — the closest apples-to-apples comparison this repo supports.
- "Per resident" uses the counties' total resident populations. But county governments mostly serve unincorporated residents plus regional functions; King County's higher per-resident figure partly reflects broader service responsibilities — it operates Metro Transit and Public Health as county departments, while Pierce County residents get transit from Pierce Transit, a separate district not in these numbers. This is a difference in what the governments do, not only in how much they spend.
- These are actual expenditures as filed, not budgets, and not outcome or efficiency measures.
- King County files FIT values in round thousands; per-resident figures are rounded accordingly. 2025 filed values exist but are early-cycle partial, so 2024 is used.

**Trace**

- **Source:** `washington.fit_filed_actuals` (FIT Filed Annual Actuals, reviewed governments), snapshot `milestone-2025-published-2026-06-30` (FIT Snapshot 33, MILE2025, published 2026-06-30)
- **Public source:** https://portal.sao.wa.gov/FIT/
- **Data-through:** filed years 2015–2024 complete; 2025 partial (early filing cycle) — 2024 used
- **Grain:** government x year; measure: `total_expenditures` (amount basis `filed_actuals_excl_internal_service`)
- **Filters:** `government-annual-totals.jsonl`, gov_type = county, government in {King County (mcag 0127), Pierce County (mcag 0152)}, year = 2024
- **Check:** Spokane 2024 spot check matches skill (revenues 729,876,646 / expenditures 648,638,448); King 2024 = $5,312,711,000; Pierce 2024 = $883,659,316
- **Denominator source:** `washington.ofm_population`, snapshot `2025-04-01`, April 1, 2024 estimates (King 2,378,100; Pierce 952,600), `row_type = county`, geography basis resident_jurisdiction — FIT's own population field not used, per the denominator wall
- **Public source:** https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
- **Context sources (direction only):** `king_county.open_budget_dashboard` snapshot 2026-04-01 (FY2026 budgeted expenditure $8,598,795,612; https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard) and `pierce_county.open_budget` (Socrata w2wc-2pqu, 2026-2027 budget total $3,500,588,070 verified 2026-07-13; https://open.piercecountywa.gov/resource/w2wc-2pqu) with the biennial halving explicitly labeled an approximation
- **Caveats:** filed actual expenditures, not budgets; per-resident uses total county population while counties serve mainly unincorporated residents plus regional functions; King and Pierce county service scopes differ (notably transit and public health); King County files in round thousands; dollar figures are nominal 2024.
