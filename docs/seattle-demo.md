# Seattle Demo Answer Traces

This demo shows the intended Civic Agent answer style for City of Seattle operating budget questions. It uses the official City of Seattle Operating Budget Socrata dataset and focuses on approved operating budget rows, not actual spending.

All examples below use:

- Source: City of Seattle Operating Budget, Socrata dataset `8u2j-imqx`
- Accessed: 2026-06-04
- Measure: sum of `approved_amount`
- Known check: FY2026 has 7,622 rows and totals about $7.312B
- Caveat: this is approved operating budget data, not actual payments, staffing, or capital budget data

## 1. Where does Seattle spend the most money in FY2026?

Conclusion: At the service level, the largest FY2026 operating-budget area is Utilities, Transportation & Environment at about $2.86B. At the department level, Seattle City Light and Seattle Public Utilities are the two largest departments, which is why utility and enterprise-fund caveats matter.

Numbers:

| Grain | Name | FY2026 approved amount |
|---|---:|---:|
| Service | Utilities, Transportation & Environment | $2.86B |
| Service | Administration | $1.71B |
| Service | Public Safety | $1.07B |
| Department | Seattle City Light | $1.30B |
| Department | Seattle Public Utilities | $1.21B |
| Department | Seattle Police Department | $488.6M |
| Department | Seattle Department of Human Resources | $485.7M |
| Department | Finance General | $459.9M |

How to read this: "Where does the money go?" changes depending on the grain. Service totals show broad budget areas; department totals show organizational budgets. Utility budgets can dominate the operating budget and are not the same as discretionary general-government priorities.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: service and department, FY2026
- Measure: sum of `approved_amount`
- Filters/query logic: filter to `fiscal_year = 2026`, group by `service` and separately by `department`, sort by total descending
- Check: FY2026 row count = 7,622; FY2026 total = $7.312B
- Caveats: approved operating budget, not actual spending; utility and enterprise funds can dominate totals

## 2. Compare Seattle Police and Fire from FY2018 to FY2026

Conclusion: Both departments grew in approved operating budget from FY2018 to FY2026. Police remained larger in dollar terms, while Fire had the faster percentage growth.

Numbers:

| Department | FY2018 | FY2026 | Dollar change | Percent change |
|---|---:|---:|---:|---:|
| Seattle Police Department | $331.3M | $488.6M | +$157.3M | +47.5% |
| Seattle Fire Department | $212.2M | $350.7M | +$138.5M | +65.3% |

How to read this: Police's FY2026 approved operating budget is about $137.9M higher than Fire's. Fire grew faster relative to its FY2018 baseline.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: fiscal year by department
- Measure: sum of `approved_amount`
- Filters/query logic: filter to Seattle Police Department and Seattle Fire Department, group by `fiscal_year` and `department`, compare FY2018 with FY2026
- Check: results use known FY2018-FY2026 years from the source card
- Caveats: approved operating budget, not actual spending; department structures and accounting rows can change over time

## 3. Compare Police, Fire, and Human Services from FY2018 to FY2026

Conclusion: Among these three departments, Human Services had the largest absolute increase and the largest percentage increase from FY2018 to FY2026.

Numbers:

| Department | FY2018 | FY2026 | Dollar change | Percent change |
|---|---:|---:|---:|---:|
| Seattle Police Department | $331.3M | $488.6M | +$157.3M | +47.5% |
| Seattle Fire Department | $212.2M | $350.7M | +$138.5M | +65.3% |
| Human Services Department | $176.5M | $421.1M | +$244.5M | +138.5% |

How to read this: Police is still the largest of the three in FY2026, but Human Services grew more from its FY2018 baseline.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: fiscal year by department
- Measure: sum of `approved_amount`
- Filters/query logic: filter to Seattle Police Department, Seattle Fire Department, and Human Services Department; group by `fiscal_year` and `department`; compare FY2018 with FY2026
- Check: FY2026 totals for these departments align with the known largest-department checks in the Seattle skill
- Caveats: approved operating budget, not actual spending; budget growth does not by itself explain policy outcomes or service levels

## 4. What programs inside Seattle Police Department are largest in FY2026?

Conclusion: Seattle Police Department's largest FY2026 program rows are Special Operations and Departmental Indirect Costs, each at about $70M.

Numbers:

| Program | FY2026 approved amount |
|---|---:|
| Special Operations | $73.0M |
| Departmental Indirect Costs | $71.1M |
| Technical Services | $34.2M |
| North Precinct | $34.0M |
| Divisional Indirect Costs | $32.7M |
| West Precinct | $27.4M |
| Patrol Operations | $24.3M |
| South Precinct | $23.6M |
| East Precinct | $23.3M |
| Citywide Indirect Costs | $21.4M |

How to read this: Programs mix direct operating areas and indirect-cost categories. Indirect-cost rows are budget/accounting structure, not necessarily a direct resident-facing service.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: program within Seattle Police Department, FY2026
- Measure: sum of `approved_amount`
- Filters/query logic: filter to `fiscal_year = 2026` and `department = "Seattle Police Department"`, group by `program`, sort by total descending
- Check: Seattle Police Department FY2026 total = about $488.6M
- Caveats: approved operating budget, not actual spending; program names include indirect-cost and accounting categories

## 5. What are the biggest negative rows in FY2026?

Conclusion: The biggest negative FY2026 rows are mostly indirect cost recovery, pooled benefits, PTO, or similar accounting rows. They should be treated as real budget/accounting entries, not automatic data errors.

Numbers:

| Amount | Department | Program | Fund |
|---:|---|---|---|
| -$99.4M | Seattle Department of Transportation | Indirect Cost Recovery Offset | Transportation Fund |
| -$61.2M | Seattle Department of Transportation | Pooled Benefits and PTO | Transportation Fund |
| -$49.1M | Seattle City Light | Department GA Indirect Recovery | Light Fund |
| -$46.5M | Seattle City Light | PTO and Benefits Indirect Costs | Light Fund |
| -$37.6M | Seattle Department of Construction and Inspections | Indirect Cost Recovery Offset | Construction and Inspections |

How to read this: Negative rows can offset or allocate costs inside the budget. The FY2026 dataset has 345 negative rows totaling about -$567.6M, so net totals should include them unless the question explicitly asks for gross positive rows.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: raw budget rows, FY2026
- Measure: `approved_amount`
- Filters/query logic: filter to `fiscal_year = 2026` and `approved_amount < 0`, sort by `approved_amount` ascending
- Check: 345 FY2026 rows have negative `approved_amount`
- Caveats: negative rows are real budget/accounting rows; labels such as offsets, recoveries, PTO, and benefits should be inspected before interpreting them

## 6. How much is labor vs non-labor in FY2026?

Conclusion: In FY2026, non-labor rows account for about $4.30B and labor rows account for about $3.01B of Seattle's approved operating budget.

Numbers:

| Description | FY2026 approved amount | Share of FY2026 total | Rows |
|---|---:|---:|---:|
| Non-Labor | $4.30B | 58.8% | 4,154 |
| Labor | $3.01B | 41.2% | 3,468 |

How to read this: The `description` field is useful but coarse. It splits rows into Labor and Non-Labor, but it does not explain staffing levels, headcount, vacancies, or actual payroll spending.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: Labor/Non-Labor description, FY2026
- Measure: sum of `approved_amount`
- Filters/query logic: filter to `fiscal_year = 2026`, group by `description`
- Check: FY2026 descriptions are Labor and Non-Labor; FY2026 total = $7.312B
- Caveats: approved operating budget, not actual payroll or staffing data

## 7. Chart-ready department growth from FY2018 to FY2026

Conclusion: Among departments with FY2018 and FY2026 rows, Seattle Public Utilities, Office of Housing, Seattle City Light, Human Services, and Finance General had the largest absolute increases.

Numbers:

| Department | FY2018 | FY2026 | Dollar change | Percent change |
|---|---:|---:|---:|---:|
| Seattle Public Utilities | $872.9M | $1.21B | +$332.1M | +38.1% |
| Office of Housing | $69.0M | $352.4M | +$283.3M | +410.4% |
| Seattle City Light | $1.02B | $1.30B | +$274.8M | +26.9% |
| Human Services Department | $176.5M | $421.1M | +$244.5M | +138.5% |
| Finance General | $226.7M | $459.9M | +$233.2M | +102.9% |
| Seattle Department of Human Resources | $276.7M | $485.7M | +$209.1M | +75.6% |
| Seattle Police Department | $331.3M | $488.6M | +$157.3M | +47.5% |
| Seattle Fire Department | $212.2M | $350.7M | +$138.5M | +65.3% |
| Seattle Parks and Recreation | $161.6M | $272.6M | +$111.0M | +68.7% |
| Department of Finance and Administrative Services | $294.3M | $399.3M | +$105.0M | +35.7% |

Chart-ready table: use `department` as the category and `dollar_change` as the bar value. Include `fy2018`, `fy2026`, and `percent_change` in the table for hover/details.

How to read this: This is nominal approved-budget growth, not inflation-adjusted growth. Departments can appear, disappear, or change structure; for example, Community Assisted Response and Engagement appears in FY2026 without an FY2018 match and should be labeled separately rather than treated as organic growth.

Trace:

- Source: City of Seattle Operating Budget, Socrata `8u2j-imqx`
- Grain: department, FY2018 and FY2026
- Measure: sum of `approved_amount`
- Filters/query logic: filter to `fiscal_year in (2018, 2026)`, group by `fiscal_year` and `department`, compute FY2026 minus FY2018 locally
- Check: FY2018-FY2026 are known source years; FY2026 total = $7.312B
- Caveats: nominal approved budget, not actual spending; no inflation adjustment; department structure can change over time
