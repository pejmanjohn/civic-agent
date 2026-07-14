---
case: pierce-county-budget-size
surface: repo-skills
answer_mode: exact
session: fresh
---

## Conclusion

Pierce County's current budget is about **$3.5 billion for the two-year 2026–2027 biennium** — the county budgets in two-year cycles, so this is not an annual figure (roughly $1.75 billion per year as an unofficial approximation). The biggest share by far goes to **Planning and Public Works** (roads, surface water, sewer — about $1.2B, a third of the whole budget), followed by **Human Services** (~$469M) and the **Sheriff** (~$420M). By type of spending, the largest buckets are contracted/other services (~$1.12B), employee salaries and benefits (~$1.20B combined), and capital projects (~$457M).

## Numbers

**Total budgeted expenditure authority, 2026–2027 biennium: $3,500,588,070** (across 26 departments and 105 funds).

Top departments (biennial budget):

| Department | 2026–2027 budget |
|---|---|
| Planning and Public Works | $1,222,407,850 |
| Human Services | $468,509,930 |
| Sheriff | $419,636,880 |
| Finance | $241,669,350 |
| Facilities Management | $189,058,820 |
| Pierce County (countywide/general) | $178,358,640 |
| Parks and Recreation | $164,884,370 |
| Tacoma/Pierce County Health Department | $102,899,820 |
| Prosecuting Attorney | $95,667,010 |
| Juvenile Court | $57,115,420 |

By expenditure category:

| Category | 2026–2027 budget |
|---|---|
| Other Services and Charges | $1,124,910,110 |
| Salaries | $870,295,830 |
| Capital Outlays | $457,444,770 |
| Transfers Out | $441,944,910 |
| Benefits | $328,881,330 |
| Supplies | $105,436,700 |
| Intergovernmental Services | $96,893,860 |
| Debt Service (principal + interest) | $74,780,560 |

Categories sum exactly to the $3.50B total.

## How to read this

- This is **budgeted spending authority** — what the County Council authorized — not actual dollars spent. Actual spending typically comes in below budget.
- The period is **two years** (2026 and 2027 combined). Never compare it directly to annual budgets of cities or other counties.
- "Transfers Out" (~$442M) moves money between county funds, so there is some double-counting inside the total; the all-funds figure is bigger than net new spending.
- Planning and Public Works looks huge partly because it includes fee- and rate-funded utilities (sewer, surface water) and road capital, not just general-tax spending.
- No accepted **revenue or staffing** source exists for Pierce County yet, so this answer covers spending only; for revenue, the county's budget documents and the State Auditor's FIT portal (https://portal.sao.wa.gov/FIT/) are the official path.

## Trace

```text
- Source: pierce_county.open_budget (Open Budget Expenditure Data, Socrata w2wc-2pqu)
- Public source: https://open.piercecountywa.gov/resource/w2wc-2pqu
- Data-through: biennia 2016-2017 through 2026-2027 (live API queried 2026-07-14)
- Grain: biennium x department; biennium x expenditure category
- Measure: sum(budget) (budgeted expenditure authority)
- Filters: fiscal_year="2026-2027"; grouped by department and by exependiture_category (field name misspelled in source)
- Check: 2026-2027 total $3,500,588,070 over 10,362 rows — matches the skill's verified 2026-07-13 validation check; category breakdown sums exactly to the same total
- Caveats: biennial budget authority, not annual, not actual spending; transfers-out included (internal double-counting); Flood Control Zone District row returned a null budget total in the ranking; no revenue/staffing source for Pierce County
```

Answer mode: **exact** — one accepted official source matches the requested jurisdiction and budget-size frame (`budget_scale.current_total`), live values match validation checks, and the frame is named throughout.
