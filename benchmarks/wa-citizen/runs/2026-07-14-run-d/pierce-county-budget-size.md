---
case: pierce-county-budget-size
surface: repo-skills
answer_mode: exact
session: fresh
---

## Conclusion

Pierce County budgets in two-year chunks. Its current 2026–2027 biennial budget authorizes about **$3.50 billion in spending over two years** — roughly $1.75B/yr if you halve it, which is only an approximation since the county doesn't split its budget evenly by year. The biggest shares go to Planning and Public Works (roads, sewer, surface water — about a third of the budget), Human Services, and the Sheriff. By type of cost, the largest chunks are payments for services and charges, followed by employee salaries and benefits, capital projects, and internal fund transfers.

## Numbers

**Total budgeted expenditure, 2026–2027 biennium: $3,500,588,070** (across 26 departments and 105 funds)

Largest departments (biennial budget authority):

| Department | 2026–2027 budget |
|---|---|
| Planning and Public Works | $1,222.4M |
| Human Services | $468.5M |
| Sheriff | $419.6M |
| Finance | $241.7M |
| Facilities Management | $189.1M |
| Pierce County (general/countywide) | $178.4M |
| Parks and Recreation | $164.9M |
| Tacoma/Pierce County Health Dept | $102.9M |
| Prosecuting Attorney | $95.7M |
| Courts + Assigned Counsel combined (Juvenile, Superior, District, Clerk, Assigned Counsel) | ~$226.3M |

By expenditure category: Other Services and Charges $1,124.9M; Salaries $870.3M; Capital Outlays $457.4M; Transfers Out $441.9M; Benefits $328.9M; Supplies $105.4M; Intergovernmental Services $96.9M; Debt Service $74.8M. (Categories sum exactly to the $3.50B total.)

## How to read this

- These are **biennial** figures — two years of budget authority, not one year of spending.
- This is **budgeted expenditure authority**, not actual dollars out the door. For actuals: the county's Open Checkbook shows about $974.8M in net ledger payments in FY2025 (a single closed year).
- **Transfers Out (~$442M) are internal fund-to-fund movements**, so the $3.50B total includes some double counting of money that is spent again by the receiving fund.
- Justice-and-safety spending is spread across several departments (Sheriff, Prosecuting Attorney, four court offices, Assigned Counsel, Medical Examiner) — together roughly $755M, comparable in scale to Public Works' non-capital work.
- No accepted **revenue or staffing** source exists for Pierce County yet, so this answers the spending side only; the county's adopted budget book covers revenue.

**Answer mode: exact** (budget-size question answered from the accepted official source at its official frame, biennial budgeted expenditure, with the frame labeled).

## Trace

- **Source:** `pierce_county.open_budget` (Open Budget Expenditure Data, Socrata `w2wc-2pqu`)
- **Public URL:** https://open.piercecountywa.gov/resource/w2wc-2pqu
- **Data-through:** live API queried 2026-07-14; coverage biennia 2016-2017 through 2026-2027
- **Grain:** biennium x department / biennium x expenditure category
- **Measure:** sum(budget) — budgeted expenditure authority
- **Filters:** `fiscal_year="2026-2027"`; grouped by `department` and by `exependiture_category` (field name is officially misspelled)
- **Validation:** live total $3,500,588,070 over 10,362 rows matches the skill's check verified 2026-07-13; category breakdown sums exactly to the total; Flood Control Zone District returns no budget rows this biennium
- **Caveats:** biennial not annual; budget authority not actual spending; totals include ~$442M interfund transfers (double counting); no revenue/staffing source; FY2025 checkbook context figure nets debits minus credits (negative rows are reversals)
