---
case: pierce-county-budget-size
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion**

Pierce County's current budget authorizes about **$3.5 billion in spending over two years (the 2026–2027 biennium)** — Pierce County budgets in two-year cycles, so this is not an annual figure. The biggest single chunk goes to Planning and Public Works (roads, sewers, surface water, permitting), followed by Human Services, the Sheriff, and county finance/internal operations. By type of cost, the largest categories are purchased services, employee salaries and benefits, and capital construction.

**Numbers** (2026–2027 biennial budgeted expenditure, queried live 2026-07-14)

- Total budgeted expenditure: **$3,500,588,070** across 26 departments and 105 funds
- Largest departments:
  - Planning and Public Works — $1,222.4M (~35%)
  - Human Services — $468.5M (~13%)
  - Sheriff — $419.6M (~12%)
  - Finance — $241.7M
  - Facilities Management — $189.1M
  - Pierce County (countywide/non-departmental) — $178.4M
  - Parks and Recreation — $164.9M
  - Tacoma/Pierce County Health Department — $102.9M
  - Prosecuting Attorney — $95.7M
  - Courts and legal system combined (Superior, District, Juvenile Courts, Clerk, Assigned Counsel) — ~$226.3M
- By expenditure category:
  - Other Services and Charges — $1,124.9M
  - Salaries — $870.3M; Benefits — $328.9M (people costs ~$1.2B combined)
  - Capital Outlays — $457.4M
  - Transfers Out — $441.9M
  - Supplies — $105.4M; Intergovernmental Services — $96.9M; Debt Service (principal + interest) — $74.8M

**How to read this**

- These are **two-year (biennial) budget authority** figures, not one year and not actual cash spent. Halving them gives only a rough annual approximation (~$1.75B/year).
- "Transfers Out" moves money between county funds, so summing categories involves some internal double counting at the countywide level.
- This covers county government only — not the City of Tacoma or school districts. It's expenditure only; no accepted revenue or staffing source exists for Pierce County yet (the county's own budget documents and the State Auditor's FIT portal are the path for those).
- For what the county has *actually* paid out, the separate Open Checkbook source covers annual transactions through a partial FY2026.

**Trace**

- Source: pierce_county.open_budget (Open Budget Expenditure Data, Socrata w2wc-2pqu)
- Public source: https://open.piercecountywa.gov/resource/w2wc-2pqu
- Data: live API query 2026-07-14; coverage biennia 2016-2017 through 2026-2027
- Grain: biennium x department; biennium x expenditure category
- Measure: sum(budget) — budgeted expenditure authority
- Filters: fiscal_year="2026-2027"; grouped by department / exependiture_category (field name misspelled at source)
- Check: 2026-2027 total $3,500,588,070 over 10,362 rows, 26 departments — matches the skill's verified 2026-07-13 validation values exactly
- Caveats: biennial budget authority, not annual, not actual spending; Flood Control Zone District returns a null budget for this biennium; transfers-out includes interfund movement; no revenue or staffing source for Pierce County yet
