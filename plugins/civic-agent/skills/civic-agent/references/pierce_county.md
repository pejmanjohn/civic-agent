---
name: pierce-county-budget-analyst
description: Use when answering Pierce County, Washington biennial budget, budget-vs-actual, or transaction-level actual spending (checkbook) questions from the county's official Socrata open data portal.
---

# Pierce County Budget Analyst

Use this skill for Pierce County, Washington budget and actual-spending questions that can be answered from the county's official Socrata open data portal (`open.piercecountywa.gov`):

- Open Budget: biennial budgeted expenditure (with budget-line-grain actuals) by department, division, fund, program, activity, and expenditure type, biennia 2016-2017 through 2026-2027.
- Open Checkbook: transaction-level actual spending by fiscal year, department (company), division, fund, service, spend category, and payee, fiscal years 2017 through the partial current year.

Do not mix the two source families. Open Budget rows are biennial budget authority (with a companion actual column at budget-line grain); Open Checkbook rows are annual transaction-level ledger actuals. Budget periods are biennial and checkbook periods are annual - align periods explicitly before any budget-vs-actual statement across the two sources.

Do not use this skill for Pierce County revenue, staffing/FTE, contracts, payroll, Tacoma city budget, other jurisdictions, or cross-jurisdiction comparison unless the router's Scale recipes establish compatible semantics first.

## Open Budget Source Of Truth

- Dataset: Open Budget Expenditure Data
- Provider: Socrata / open.piercecountywa.gov
- Dataset id: `w2wc-2pqu`
- JSON endpoint: `https://open.piercecountywa.gov/resource/w2wc-2pqu.json`
- Source card: `jurisdictions/pierce_county/sources/open-budget.source.json`
- Coverage: biennia `2016-2017` through `2026-2027`
- Measures: `budget` (budgeted expenditure authority) and `actual` (budget-line-grain actuals; partial for the in-progress biennium)

Field quirks that queries MUST respect:

- `fiscal_year` is a biennium label string such as `2026-2027`, not a number.
- Text dimension values are whitespace-padded; trim for display and filter with `like` or `starts_with`.
- The expenditure category field is officially misspelled `exependiture_category`.

## Open Checkbook Source Of Truth

- Dataset: Open Checkbook Data
- Provider: Socrata / open.piercecountywa.gov
- Dataset id: `iwu2-biyj`
- JSON endpoint: `https://open.piercecountywa.gov/resource/iwu2-biyj.json`
- Source card: `jurisdictions/pierce_county/sources/open-checkbook.source.json`
- Coverage: fiscal years `2017` through `2026`; FY2026 partial through `2026-05-29` (verify with a max(accounting_date) query)
- Measure: `ledger_budget_debit_minus` (debit-minus-credit ledger amount; negative rows are credits/reversals)

`company` is the department-level dimension. Some `payee_for_transaction` values are generic descriptors (for example `Banking Services Vendor`), not legal vendor names - say so when ranking payees.

## Query Recipes

Current biennium budgeted total:

```bash
curl -sS --get 'https://open.piercecountywa.gov/resource/w2wc-2pqu.json' \
  --data-urlencode '$select=sum(budget) as budget_total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year="2026-2027"'
```

Department ranking for the current biennium:

```bash
curl -sS --get 'https://open.piercecountywa.gov/resource/w2wc-2pqu.json' \
  --data-urlencode '$select=department,sum(budget) as budget_total' \
  --data-urlencode '$where=fiscal_year="2026-2027"' \
  --data-urlencode '$group=department' \
  --data-urlencode '$order=budget_total DESC'
```

Biennial budget trend:

```bash
curl -sS --get 'https://open.piercecountywa.gov/resource/w2wc-2pqu.json' \
  --data-urlencode '$select=fiscal_year,sum(budget) as budget_total,sum(actual) as actual_total' \
  --data-urlencode '$group=fiscal_year' \
  --data-urlencode '$order=fiscal_year'
```

Budget vs actual within a closed biennium for one department (note the `like` for padded values):

```bash
curl -sS --get 'https://open.piercecountywa.gov/resource/w2wc-2pqu.json' \
  --data-urlencode '$select=department,sum(budget) as budget_total,sum(actual) as actual_total' \
  --data-urlencode '$where=fiscal_year="2024-2025" AND department like "Sheriff%"' \
  --data-urlencode '$group=department'
```

Checkbook: annual totals and current data-through:

```bash
curl -sS --get 'https://open.piercecountywa.gov/resource/iwu2-biyj.json' \
  --data-urlencode '$select=fiscal_year,sum(ledger_budget_debit_minus) as total,count(*) as rows,max(accounting_date) as latest' \
  --data-urlencode '$group=fiscal_year' \
  --data-urlencode '$order=fiscal_year'
```

Checkbook: top payees for a fiscal year:

```bash
curl -sS --get 'https://open.piercecountywa.gov/resource/iwu2-biyj.json' \
  --data-urlencode '$select=payee_for_transaction,sum(ledger_budget_debit_minus) as total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year=2025' \
  --data-urlencode '$group=payee_for_transaction' \
  --data-urlencode '$order=total DESC' \
  --data-urlencode '$limit=15'
```

Checkbook: department (company) or spend-category breakdowns follow the same shape with `company`, `division`, `fund`, `service`, or `spend_category_as_worktag` as the group field.

## Validation Checks

Verified 2026-07-13; rerun the recipes above and compare before relying on live values:

- Open Budget `2026-2027`: budget total `3,500,588,070` over `10,362` rows, `26` departments, `105` funds.
- Open Budget known biennia: `2016-2017`, `2018-2019`, `2020-2021`, `2022-2023`, `2024-2025`, `2026-2027`.
- Open Checkbook FY2025 (closed year): total `974,830,912.90` over `109,954` rows, `27` companies, `87` funds.
- Open Checkbook FY2026: partial through `2026-05-29`.

If live values deviate materially from these checks, treat the answer as `needs_refresh`: say the source moved, show what was retrieved, and flag the card for refresh.

## Interpretation Rules

- Pierce County budgets biennially. Always name the two-year period; never present a biennial total as an annual figure or divide by two without labeling it an approximation.
- `budget` is budgeted expenditure authority; `actual` is expenditure actuals. Never mix the two in one total, and label the in-progress biennium's actuals partial.
- Checkbook amounts net debits and credits; negative rows are credits/reversals. State how negatives are handled in any total.
- Payee rankings must carry the generic-payee caveat.
- Expenditure data only: this jurisdiction currently has no accepted revenue or staffing source. Say so and name the missing source family when asked.
- For comparisons with King County, Seattle, or Washington state, defer to the router's Scale recipes; biennial county budget frames are not directly comparable to annual dashboard or city operating values.

## Answer Style

Lead with a plain-English Conclusion, then Numbers, then How to read this, then a Trace:

```text
Trace
- Source: pierce_county.open_budget (Open Budget Expenditure Data, Socrata w2wc-2pqu)
- Public source: https://open.piercecountywa.gov/resource/w2wc-2pqu
- Grain: biennium x department
- Measure: sum(budget)
- Filters: fiscal_year="2026-2027"
- Check: 2026-2027 total $3,500,588,070 over 10,362 rows (verified 2026-07-13)
- Caveats: biennial budget authority, not annual, not actual spending
```

For checkbook answers, add the data-through boundary (`FY2026 partial through 2026-05-29`) and the negative-row handling statement.
