---
name: seattle-budget-analyst
description: Use when answering questions about Seattle operating budget spending, departments, programs, funds, labor/non-labor split, budget line items, accounting offsets, or year-over-year budget changes.
---

# Seattle Budget Analyst

Use this skill for City of Seattle operating budget questions. It supports questions about services, departments, programs, funds, labor/non-labor split, unusual rows, and year-over-year changes from FY2018-FY2026.

Do not use this for realtime city activity, map visualizations, actual payments/checkbook data, staffing headcount, capital budget, or Washington state budget analysis unless the user explicitly asks for broader context.

## Source Of Truth

- Dataset: City of Seattle Operating Budget
- Provider: Socrata / data.seattle.gov
- Socrata ID: `8u2j-imqx`
- JSON endpoint: `https://data.seattle.gov/resource/8u2j-imqx.json`
- CSV endpoint: `https://data.seattle.gov/resource/8u2j-imqx.csv?$limit=50000`
- Metadata endpoint: `https://data.seattle.gov/api/views/8u2j-imqx`
- OpenBudget page: `https://openbudget.seattle.gov/#!/year/2026/operating/0/department`
- Known years: FY2018-FY2026 as of June 2026
- Refresh frequency in metadata: One Time

Treat this as annual/static budget publication data, not realtime data.

## Safe Answer Patterns

This source can safely support:

- Annual approved operating budget totals by fiscal year.
- FY2018-FY2026 comparisons by service, department, program, fund, fund type, or Labor/Non-Labor description.
- FY2026 service, department, program, fund, and Labor/Non-Labor rankings.
- Department drill-downs into programs, funds, fund types, and Labor/Non-Labor rows.
- Inspection of negative, zero, blank, and unusual `approved_amount` rows.
- Chart-ready tables for Seattle operating budget trends and department growth using `approved_amount`.

Do not use this source for actual spending, payments, realtime city activity, staffing/headcount, capital budget, or non-Seattle budget analysis.

For composed Scale questions, defer to the router's Scale recipes before comparing Seattle to another jurisdiction or computing per-capita values. This source can supply Seattle approved operating-budget facts, but it does not supply inflation adjustments or non-operating budget frames. Per-capita answers may compose this source with `washington.ofm_population`; cite both sources, use the OFM April 1 estimate date, and keep service-scope caveats explicit.

## Data Model

Fields:

- `fiscal_year`: numeric fiscal year
- `service`: high-level city service area
- `department`: department or office
- `program`: budget program
- `fund`: fund code/name
- `fund_type`: fund category/name
- `expense_type`: usually `Expenditures`
- `description`: `Labor` or `Non-Labor`
- `approved_amount`: numeric approved budget amount; may be positive, zero, negative, or blank

Canonical hierarchy:

```text
service -> department -> program -> fund -> description
```

Primary measure:

```text
sum(approved_amount)
```

## Retrieval Strategy

1. For simple totals and grouped answers, query Socrata with SoQL.
2. For multi-step analysis, download the CSV once and compute locally.
3. For vague questions, start at `service` or `department`, then drill into `program` and `fund`.
4. For time comparisons, group by `fiscal_year` plus the requested dimension.
5. For surprising results, inspect raw rows before explaining.
6. If a query returns unexpected totals, re-check filters, null handling, and whether the question asked for operating budget only.

Use `curl --get` with `--data-urlencode` for SoQL parameters.

## Query Recipes

### FY2026 operating total

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=sum(approved_amount) as total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year=2026'
```

Expected check as of June 2026:

```text
total ~= 7311905121.57
rows = 7622
```

### Top departments in FY2026

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=department,sum(approved_amount) as total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year=2026' \
  --data-urlencode '$group=department' \
  --data-urlencode '$order=total desc' \
  --data-urlencode '$limit=20'
```

### Service totals in FY2026

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=service,sum(approved_amount) as total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year=2026' \
  --data-urlencode '$group=service' \
  --data-urlencode '$order=total desc'
```

### Department over time

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=fiscal_year,department,sum(approved_amount) as total' \
  --data-urlencode '$where=department="Seattle Police Department"' \
  --data-urlencode '$group=fiscal_year,department' \
  --data-urlencode '$order=fiscal_year'
```

### Compare multiple departments over time

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=fiscal_year,department,sum(approved_amount) as total' \
  --data-urlencode '$where=department in("Seattle Police Department","Seattle Fire Department","Human Services Department")' \
  --data-urlencode '$group=fiscal_year,department' \
  --data-urlencode '$order=fiscal_year,department'
```

### Department growth from FY2018 to FY2026

Use this for chart requests like "which Seattle departments had the largest budget increases from 2018 to 2026." Query both years, then compute `increase = total_2026 - total_2018` locally and sort by `increase desc`.

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=fiscal_year,department,sum(approved_amount) as total' \
  --data-urlencode '$where=fiscal_year in(2018,2026)' \
  --data-urlencode '$group=fiscal_year,department' \
  --data-urlencode '$order=department,fiscal_year'
```

Important caveat: departments can appear, disappear, or change structure. If a department has no FY2018 row but a large FY2026 total, show it but label the increase as "new/no FY2018 match" rather than organic growth.

If a department name is uncertain, discover matching department values first:

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=department,count(*) as rows' \
  --data-urlencode "$where=upper(department) like '%POLICE%'" \
  --data-urlencode '$group=department' \
  --data-urlencode '$order=department'
```

### Department drill-down by program

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=program,sum(approved_amount) as total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year=2026 AND department="Seattle Police Department"' \
  --data-urlencode '$group=program' \
  --data-urlencode '$order=total desc'
```

### Labor vs non-labor

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=description,sum(approved_amount) as total,count(*) as rows' \
  --data-urlencode '$where=fiscal_year=2026' \
  --data-urlencode '$group=description' \
  --data-urlencode '$order=total desc'
```

### Biggest negative rows

```bash
curl -sS --get 'https://data.seattle.gov/resource/8u2j-imqx.json' \
  --data-urlencode '$select=fiscal_year,service,department,program,fund,fund_type,description,approved_amount' \
  --data-urlencode '$where=fiscal_year=2026 AND approved_amount < 0' \
  --data-urlencode '$order=approved_amount asc' \
  --data-urlencode '$limit=25'
```

### Full CSV for local analysis

```bash
curl -L -sS 'https://data.seattle.gov/resource/8u2j-imqx.csv?$limit=50000' \
  -o seattle-operating-budget.csv
```

## Analysis Patterns

### Where does the money go?

Start with service totals, then department totals, then largest programs. If the user did not specify a grain, say which grain you used.

### Compare departments

Group by `fiscal_year` and `department`. Report current totals, absolute change, and percent change. Be careful with departments that appear, disappear, or are renamed.

For largest-increase charts, calculate change from the earliest requested year to the latest requested year and chart the top departments by absolute dollar increase. Include departments with missing baseline years separately or mark them clearly.

### Drill into a department

Filter by `department`, then group by `program`. If useful, split by `description` for Labor / Non-Labor or by `fund` / `fund_type`.

### Find growth or decline

Compare the earliest and latest years requested. Exclude blank amounts from numeric sums. Note that zero and negative rows can affect net totals.

### Explain funds

Group by `fund_type` or `fund`. Explain that fund-based views are about financing/accounting structure, not necessarily direct resident-facing services.

### Investigate weird rows

Look for negative, zero, and blank `approved_amount` rows. Treat negative rows as likely accounting offsets, recoveries, transfers, or internal cost allocation unless the raw row shows otherwise.

## Interpretation Rules

- Do not call this realtime data.
- Do not describe every row as direct spending on residents.
- Use `approved_amount` as the default numeric measure.
- Sum at the grain the user asked for.
- If the user asks "where does money go?" and does not specify grain, start with `service` and `department`.
- Negative rows are real budget/accounting rows, not automatic data errors.
- Zero rows may represent configured budget lines with no approved amount.
- Blank `approved_amount` rows should be excluded from numeric sums unless auditing missing data.
- `description` only means Labor or Non-Labor; it is useful but coarse.
- Utility budgets and enterprise funds can dominate totals, so "largest department" is not the same as "largest discretionary priority."
- For policy or political questions, separate budget facts from interpretation.
- For cross-year comparisons, warn that budget structure, program names, and department names may change.

## Validation Checks

Known checks as of June 2026:

- Total rows across FY2018-FY2026: about 35,891
- FY2026 rows: 7,622
- FY2026 operating total: about $7.312B
- FY2026 departments: 44
- FY2026 programs: about 380
- FY2026 funds: about 84
- FY2026 descriptions: Labor and Non-Labor

Known largest FY2026 departments:

- Seattle City Light: about $1.30B
- Seattle Public Utilities: about $1.21B
- Seattle Police Department: about $489M
- Seattle Department of Human Resources: about $486M
- Finance General: about $460M

If a result differs materially, verify the year filter, the dataset ID, and whether blank/null values were handled correctly.

## Answer Style

Lead with the plain-English conclusion, then show the numbers.

Use this shape:

```text
Conclusion: [one sentence]

Numbers:
- [dimension]: $X
- [dimension]: $Y

How to read this:
[brief explanation of grain, caveats, and budget meaning]

Trace:
- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: [service / department / program / fund / description / row]
- Measure: sum(`approved_amount`)
- Filters/query logic: [plain-English description]
- Check: [row count, known total, or validation check when useful]
- Caveats: [approved operating budget, not actual spending; other relevant caveats]
```

Round large dollar amounts to human scale unless exact values matter. For comparisons, include both absolute dollar change and percent change. Mention the dimension used: service, department, program, fund, or Labor/Non-Labor.

When helpful, end with one natural next drill-down question, not a long menu.
