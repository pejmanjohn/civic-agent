---
name: washington-budget-analyst
description: Use when answering questions about Washington state operating budget totals, enacted budget trends, General Fund revenue estimate-vs-actual trends, state agency vendor-payment/checkbook actual spending from Fiscal WA, or filed annual actuals for reviewed Washington local governments (cities, counties, school districts, special districts) from the State Auditor's FIT.
---

# Washington Budget Analyst

Use this skill for Washington state budget, revenue, and actual vendor-payment questions that can be answered from reviewed Fiscal WA sources:

- Operating budget: 2025-27 enacted agency/function totals and enacted base biennial trends from 2013-15 through 2025-27.
- Revenue by biennium: General Fund (001) estimated revenue, actual revenue, and actual-minus-estimate trends from 2003-05 through 2025-27, with 2025-27 partial through April 2026.
- Open Checkbook: state agency vendor payments from 2013-15 through the current 2025-27 partial biennium, backed by a managed local SQLite database built from official Fiscal WA XLSX files.
- OFM population: April 1 official resident population estimates for counties, cities, towns, and state totals, used only as denominator context for Scale recipes.
- FIT filed actuals: annual total revenues and expenditures as filed with the State Auditor (and OSPI for school districts) for the REVIEWED local governments in `washington.fit_filed_actuals` - currently Spokane, Tacoma, Walla Walla, Vancouver, Everett, King County, Pierce County, Snohomish County, Sound Transit, the King County Regional Homelessness Authority, Seattle School District No. 1, and Evergreen School District (Clark County).
- DOR property tax levies: certified levy amounts and rates for every taxing district statewide, tax years due 2024-2025, used for "who levies property tax and how much did it change" questions at district level.

Do not mix these source families. Operating budget rows are budget authority, revenue rows are General Fund estimate/actual revenue, Open Checkbook rows are actual vendor payments, and OFM population rows are resident denominators. Do not use this skill for procurement contract terms, payroll, staffing/FTE, capital budget, transportation budget, Seattle budget analysis, King County budget analysis, or cross-jurisdiction comparison unless a separate source explicitly supports that question. Do not treat the 2025-27 revenue or checkbook values as full-biennium final actuals.

For composed Scale questions, defer to the router's Scale recipes before comparing Washington state to city or county sources. Washington operating-budget claims are biennial state budget facts and should not be treated as directly comparable to annual city or county dashboard values without an explicit compatibility check.

Population denominator claims are separate from budget claims. `washington.ofm_population` can supply resident population denominators such as Seattle 816,600 and King County 2,411,700 from OFM April 1, 2025 estimates, but it does not supply budget amounts or service-scope comparability.

## Operating Source Of Truth

- Dataset: Washington Operating Budget Summary Reports
- Provider: Fiscal WA / LEAP / Office of Financial Management / Microsoft Power BI
- Current official dashboard page: `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- Historical official dashboard page: `https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior`
- OFM context page: `https://ofm.wa.gov/budget/`
- Current Power BI report: `https://app.powerbi.com/view?r=eyJrIjoiYjMzNmE2MDMtMWY2Ni00NjVkLWFmN2YtZWI4YjE3MjhkNTgzIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- Historical Power BI report: `https://app.powerbi.com/view?r=eyJrIjoiN2QyYmI5Y2EtMjgwZS00OTQ3LTgwMzgtYmY2YzYzMjRlNzIyIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- Source card: `jurisdictions/washington/sources/operating-budget.source.json`
- Snapshot version: `2025-27-enacted-2025-05-20`
- Budget version: `Enacted (05-20-2025)`
- Current model refresh time: `2025-07-22T17:18:33.94`
- Historical model refresh time: `2025-12-29T18:08:24.87`
- Snapshot generated from live Power BI replay: see `jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/provenance.json`

For local dev-plugin testing, read snapshot files from the repo checkout at this relative path:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/
```

For hosted/fresh-agent use after the source is pushed, checked-in snapshot files will be available under:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/agency-by-fund-view.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/functional-area-by-fund-view.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/version-summary.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-biennium-summary.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-agency-by-biennium.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-functional-area-by-biennium.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/summary.json
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/provenance.json
```

Treat this as budgeted/authorized operating budget data, not actual spending. Amounts are normalized to dollars; Fiscal WA report values are returned in thousands.

## Revenue Source Of Truth

- Dataset: Washington State Revenue by Biennium Reports
- Provider: Fiscal WA / LEAP / Office of Financial Management / Microsoft ReportViewer
- Official report page: `https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx`
- Context page: `https://fiscal.wa.gov/Revenue/RevenueOverview.aspx`
- Source card: `jurisdictions/washington/sources/revenue-by-biennium.source.json`
- Snapshot version: `2025-27-revenue-through-2026-04`
- Snapshot generated from live ReportViewer exports: see `jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/provenance.json`
- Actual data through: `2026-04` (`Actual Data Through April 2026`)

For local dev-plugin testing, read revenue snapshot files from the repo checkout at this relative path:

```text
jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/
```

For hosted/fresh-agent use after the source is pushed, checked-in revenue snapshot files will be available under:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/normalized/general-fund-revenue-by-biennium.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/normalized/general-fund-revenue-by-area-account.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/summary.json
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/provenance.json
```

Treat revenue `estimated_revenue` as the revenue-budget measure for this source. The same rows include actual revenue collected and actual-minus-estimate. For the in-progress 2025-27 biennium, all three measures are partial through April 2026.

## Open Checkbook Source Of Truth

- Dataset: Washington State Agency Vendor Payments Open Checkbook
- Provider: Fiscal WA / LEAP / Office of Financial Management / Microsoft Power BI
- Official checkbook page: `https://fiscal.wa.gov/Spending/Checkbook.aspx`
- Fiscal WA spending overview: `https://fiscal.wa.gov/Spending/SpendingOverview.aspx`
- Source card: `jurisdictions/washington/sources/open-checkbook.source.json`
- Storage policy: `managed_local_db`
- Normal answer source: local SQLite database built from official XLSX files
- Current official XLSX: `https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx`
- Historical official XLSX coverage: `2013-15` through `2025-27`
- Current actual data through: `2026-05` (`Payments through May 2026`)
- Hosted aggregate snapshot: `jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/`

For source-checking before answering:

```bash
python3 scripts/source_data.py --json inspect washington.open_checkbook
python3 scripts/source_data.py --json status washington.open_checkbook
python3 scripts/source_data.py --json validate washington.open_checkbook
```

If the status is `missing`, `stale`, `refresh_failed`, or the local database path is missing, ensure or refresh the managed source before answering checkbook questions:

```bash
python3 scripts/source_data.py --json ensure washington.open_checkbook
python3 scripts/source_data.py --json refresh washington.open_checkbook
```

Do not parse the XLSX files during normal answer generation. The first ensure/refresh may download large official files and build the local database; repeated answers should query the indexed SQLite database.

If the agent host cannot run this repo's CLI or access the local database (the hosted/fresh-agent path), answer aggregate checkbook questions from the checked-in hosted aggregate snapshot instead of dead-ending:

```text
jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/category-breakdown.jsonl
jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/agency-totals.jsonl
jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/vendor-totals.jsonl
jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/monthly-trend.jsonl
jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/summary.json
jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/provenance.json
```

Hosted equivalents are available under `https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/` plus the same relative paths.

Hosted aggregate answer rules:

- Supported grains: per-biennium totals by category, by agency, by calendar month, and top-100 vendors per biennium. Rows carry `biennium`, `name`, `amount`, `payment_rows` (vendor rows add `rank`).
- `vendor-totals.jsonl` is truncated to the top 100 vendors per biennium by total amount. Say so when answering vendor questions from the hosted path, and route deeper vendor, sub-object, or filtered questions to the managed local database path.
- Label answers with the snapshot version `2025-27-through-2026-05` and the `data_through` boundary from `summary.json`; the in-progress 2025-27 biennium is partial through May 2026.
- `summary.json` records per-biennium totals with a category/agency/monthly reconciliation check; cite it as the validation evidence in traces.

Treat this as actual state agency vendor-payment data, not budget authority, revenue, contracts, invoices, payroll, staffing, or service outcomes.

## Local Government Filed Actuals Source Of Truth (FIT)

- Dataset: FIT Filed Annual Actuals (reviewed governments)
- Provider: Washington State Auditor's Office Financial Intelligence Tool; school data as reported to OSPI
- Official portal: `https://portal.sao.wa.gov/FIT/`
- Source card: `jurisdictions/washington/sources/fit-filed-actuals.source.json`
- Snapshot version: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- Coverage: filed years 2015-2024 complete for reviewed governments, 2025 early-cycle PARTIAL; school districts 2020-2025 (school fiscal years ending August 31)

Checked-in snapshot files (repo-relative; hosted equivalents under `https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/` plus the same paths):

```text
jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl
jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/school-district-annual-totals.jsonl
jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/summary.json
jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/provenance.json
```

Rows carry `government`, `mcag`, year, `total_revenues`, `total_expenditures`, and `amount_basis`. Government rows use the FIT headline basis (excludes internal service funds); school rows are OSPI modified accrual with `school_fiscal_year_ending_aug31`.

Interpretation rules (vocabulary walls):

- Filed actuals are NOT budgets. Never answer a "what is the budget" question with filed actuals without saying these are actual revenues/expenditures as filed, and never mix them numerically with adopted/approved budget frames without an explicit alignment recipe.
- These are NOT checkbook transactions: no vendors, payees, or invoices at this grain.
- Label 2025 values partial (early filing cycle); some filers report in round thousands (Sound Transit, King County).
- School fiscal years end August 31 and use a different accounting basis than cities/counties - never compare school and city/county values without labeling both bases.
- Only the reviewed governments listed in the source card are claimable. For any other WA local government, follow the router's unsupported-jurisdiction protocol and point at `https://portal.sao.wa.gov/FIT/` as the official path.
- Spot checks for traces: City of Spokane 2024 revenues 729,876,646 / expenditures 648,638,448; Sound Transit 2024 revenues 2,599,304,000; KCRHA 2024 expenditures 191,618,113 (against 180,707,326 revenues - a deficit year); Seattle SD No. 1 school year 2024-25 revenues 1,518,641,110.55.

## Property Tax Levies Source Of Truth (DOR)

- Dataset: Local Taxing District Levy Detail (statewide, every taxing district)
- Provider: Washington State Department of Revenue, Research and Fiscal Analysis
- Official landing page: `https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail`
- Source card: `jurisdictions/washington/sources/dor-property-tax-levies.source.json`
- Snapshot version: `levies-due-2025` (tax years due 2024 and 2025; 4,593 levy rows; DOR series reaches back to 2002)

Checked-in snapshot files (repo-relative; hosted equivalents under `https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/` plus the same paths):

```text
jurisdictions/washington/data/dor-property-tax-levies/levies-due-2025/normalized/levy-detail.jsonl
jurisdictions/washington/data/dor-property-tax-levies/levies-due-2025/summary.json
jurisdictions/washington/data/dor-property-tax-levies/levies-due-2025/provenance.json
```

Rows carry `year_due`, `tdcode`, `district_key`, `county`, `district_type`, `levy_type`, `district_name`, `assessed_value`, `levy_rate_per_1000`, `district_levy`, and `statutory_maximum_rate`.

Interpretation rules (vocabulary walls):

- These are CERTIFIED LEVY AMOUNTS DUE per taxing district - not tax bills, not collections, not budgets.
- One row per LEVY: a district's base levy, lid lifts, and bonds are separate rows. District-level statements aggregate `district_key` and name the lines. Verified trap: Seattle city's base rate fell 1.44409 -> 1.05837 from 2024 to 2025 while its lid-lift line rose 0.87332 -> 1.57835 after the November 2024 transportation levy - quoting only the base line misleads.
- Rates are dollars per $1,000 of assessed value, district-level only. Household math requires the parcel's assessed value; any per-household figure must be labeled illustrative. The parcel-level levy stack ("which districts tax MY address") needs county tax-code-area data - point at the county assessor (King County publishes PDF rate books).
- No ballot-measure metadata: voter-approved levies are identifiable by levy-type codes and names ("Temp Lid Lift", "Bond"), but measure numbers, dates, and approval percentages need an elections source.
- The levy-lid story is answerable: rows carry the 101%-limit and statutory-maximum columns.
- Spot checks for traces: statewide 2025 total $18,450,110,007; King County 2025 total $7,724,787,822 (+1.6% from $7,603,197,998); statewide school enrichment levies $2,814,008,373; Seattle SD #1 enrichment 0.65422/$194,678,891 (2025) vs 0.63479/$190,239,286 (2024). All reconcile with DOR Tables 8/12/14 to the dollar (verified 2026-07-13).

## OFM Population Source Of Truth

- Dataset: April 1 Official Population Estimates
- Provider: Washington Office of Financial Management, Forecasting and Research Division
- Official page: `https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/`
- Official XLSX: `https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_final.xlsx`
- Source card: `jurisdictions/washington/sources/ofm-population.source.json`
- Snapshot version: `2025-04-01`
- Latest estimate date: `2025-04-01`
- Snapshot generated from the official XLSX: see `jurisdictions/washington/data/ofm-population/2025-04-01/provenance.json`

For hosted/fresh-agent use after the source is pushed, checked-in snapshot files will be available under:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/ofm-population/2025-04-01/normalized/population-estimates.jsonl
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/ofm-population/2025-04-01/summary.json
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/data/ofm-population/2025-04-01/provenance.json
```

Known denominator checks:

```text
Seattle 2025 resident population estimate = 816600
King County 2025 resident population estimate = 2411700
State Total 2025 resident population estimate = 8115100
```

Treat this as resident population denominator data, not budget authority, service population, households, taxpayers, or broad demographic composition.

## Safe Answer Patterns

The operating source can safely support:

- 2025-27 enacted operating budget totals by agency.
- 2025-27 enacted operating budget totals by functional area.
- Statewide enacted base operating budget trends by biennium from 2013-15 through 2025-27.
- Agency enacted base operating budget trends by biennium from 2013-15 through 2025-27.
- Functional area enacted base operating budget trends by biennium from 2013-15 through 2025-27.
- Comparisons between `Total Budgeted` and `Outlook Funds (NGF-O)` fund views.
- Budget-version summaries for the 2025-27 biennial operating budget report.
- Chart-ready tables for the supported snapshot grains.

Do not use the operating source for actual spending, vendor payments, procurement, actual revenue, staffing/FTE, capital budget, transportation budget, 2026 supplemental changes, line-item text search, historical trends before 2013-15, supplemental/proposal historical comparisons, or cross-jurisdiction comparisons.

The revenue source can safely support:

- General Fund (001) estimated revenue, actual revenue, and actual-minus-estimate totals by biennium from 2003-05 through 2025-27.
- General Fund revenue rows by biennium, revenue area, and Fiscal WA account/agency label.
- Closed-biennium historical General Fund revenue trends.
- Current-biennium revenue estimates and actuals only when labeled as partial through April 2026.

Do not use the revenue source for funds beyond General Fund (001), selected major-source detail, selected-fund source detail, ERFC forecast assumptions, final 2025-27 actuals, full-biennium 2025-27 forecasts, or expenditure budget questions.

The Open Checkbook source can safely support:

- State agency vendor-payment totals by biennium, fiscal year, fiscal month, calendar month, agency, object category, subobject category, or vendor.
- Category, agency, vendor, and monthly actual-payment rankings for a selected biennium or fiscal period.
- Historical vendor-payment trends from 2013-15 through 2025-27, with the current biennium labeled partial through May 2026 until refreshed.
- Plain-English explanations of how checkbook actual payments differ from budget authority, revenue, contracts, invoices, payroll, staffing, and service outcomes.

Do not use Open Checkbook for budget authority, appropriations, revenue, procurement contract terms, invoices, purchase orders, payroll, employee compensation, FTE, staffing, service quality, program outcomes, or local government spending outside Washington state agency vendor payments.

The OFM population source can safely support:

- April 1 resident population estimates for Washington counties, cities, towns, and state totals.
- Seattle and King County denominator values for per-resident Scale answers.
- County incorporated and unincorporated population splits that reconcile to county totals.

Do not use OFM population for budget amounts, service population, daytime population, households, taxpayers, broad demographic composition, or claims that city and county budgets are service-comparable.

## Data Model

Operating snapshot files:

- `agency-by-fund-view.jsonl`: one row per agency and fund view
- `functional-area-by-fund-view.jsonl`: one row per functional area and fund view
- `version-summary.jsonl`: one row per budget version and fund view in the summary report
- `historical-biennium-summary.jsonl`: one row per enacted base biennial operating budget from 2013-15 through 2025-27
- `historical-agency-by-biennium.jsonl`: one row per agency and biennium for enacted base Total Budgeted trends
- `historical-functional-area-by-biennium.jsonl`: one row per functional area and biennium for enacted base Total Budgeted trends
- `summary.json`: row counts and validation checks
- `provenance.json`: model metadata, query-template hashes, response checksums, and source entities

Fields:

- `source_surface_id`: Power BI surface that supplied the row
- `biennium`: `2025-27` for current rows; `2013-15` through `2025-27` for supported historical trend rows
- `period_type`: `biennium`
- `session_type`: Fiscal WA session type; default historical trend uses `R1`
- `budget_state`: `enacted` for supported historical trends
- `revision_scope`: `base` for supported historical trends
- `budget_version`: Fiscal WA budget version label, such as `Enacted (05-20-2025)` for current rows or `Enacted` for historical trend rows
- `budget_version_filter`: Fiscal WA report filter label
- `fund_view`: `Total Budgeted` or `Outlook Funds (NGF-O)`
- `agency_code`: official Fiscal WA agency code
- `agency`: Washington state agency label
- `functional_area_code`: official Fiscal WA functional area code
- `functional_area`: Fiscal WA functional area label
- `amount_thousands`: report amount in thousands of dollars
- `budgeted_amount`: normalized dollar amount

Primary measure:

```text
sum(budgeted_amount)
```

Default fund view:

```text
Total Budgeted
```

Use `Outlook Funds (NGF-O)` only when the user asks for near-general-fund/outlook funds or when explaining the difference between fund views.

Default historical trend filter:

```text
period_type = "biennium"
budget_state = "enacted"
revision_scope = "base"
session_type = "R1"
budget_version = "Enacted"
fund_view = "Total Budgeted"
```

Revenue snapshot files:

- `general-fund-revenue-by-biennium.jsonl`: one row per biennium for General Fund (001) estimate, actual, and actual-minus-estimate totals
- `general-fund-revenue-by-area-account.jsonl`: one row per biennium, revenue area, and Fiscal WA account/agency label
- `summary.json`: row counts, actual-data-through metadata, historical coverage, and validation checks
- `provenance.json`: ReportViewer surface metadata, report parameters, export checksums, and normalization notes

Revenue fields:

- `source_surface_id`: ReportViewer surface that supplied the row
- `biennium`: `2003-05` through `2025-27`
- `period_type`: `biennium`
- `fund`: `General Fund (001)`
- `fund_code`: `001`
- `revenue_area`: high-level Fiscal WA revenue area, on detail rows
- `account_or_agency`: Fiscal WA detail label, on detail rows
- `estimated_revenue`: normalized estimated revenue dollars
- `actual_revenue`: normalized actual revenue dollars
- `actual_minus_estimate`: normalized actual-minus-estimate dollars
- `estimated_revenue_thousands`, `actual_revenue_thousands`, `actual_minus_estimate_thousands`: report units
- `actual_data_through`: `2026-04`
- `actual_data_through_label`: `Actual Data Through April 2026`
- `actual_data_status`: `complete` for closed biennia; `partial` for 2025-27

Revenue primary measures:

```text
sum(estimated_revenue)
sum(actual_revenue)
sum(actual_minus_estimate)
```

OFM population snapshot files:

- `population-estimates.jsonl`: one row per source geography and year for the 2020 census baseline and April 1 estimates from 2021 through 2025
- `summary.json`: row counts, source file metadata, and validation checks
- `provenance.json`: official page/file identity, workbook sheet names, and source fingerprint

OFM population fields:

- `source_line`: official workbook row number
- `row_type`: `county`, `unincorporated_county`, `incorporated_county`, `city_town`, `state_total`, `unincorporated_state_total`, or `incorporated_state_total`
- `county`: county grouping from the workbook
- `jurisdiction`: county, city, town, or state-total label
- `year`: census or estimate year
- `value_kind`: `census` for 2020 rows or `estimate` for 2021-2025 rows
- `estimate_date`: April 1 estimate date on estimate rows
- `geography_basis`: `resident_jurisdiction`
- `population`: resident population value

OFM population primary measure:

```text
population
```

Default denominator filter:

```text
value_kind = "estimate"
estimate_date = "2025-04-01"
row_type = "city_town" for Seattle
row_type = "county" for King County
```

Open Checkbook local database:

- Managed source id: `washington.open_checkbook`
- Database: `open_checkbook.sqlite` under the configured Civic Agent data cache
- Manifest: `manifest.json` under the same managed source cache
- Raw files: official `VendorPayments*.xlsx` files under the managed source cache, not git

Open Checkbook payment fields:

- `biennium`: `2013-15` through `2025-27`
- `fiscal_year`: official Fiscal WA fiscal year
- `fiscal_month`: official Fiscal WA fiscal month, where fiscal month 1 is July
- `calendar_month`: derived `YYYY-MM`
- `agency_code`, `agency_name`
- `object_code`, `category`
- `subobject_code`, `subcategory`
- `vendor_name`
- `amount`: normalized payment amount in dollars

Open Checkbook primary measure:

```text
sum(amount)
```

Supported named queries through `scripts/source_data.py query washington.open_checkbook`:

- `category_breakdown`: top payment categories by amount
- `agency_totals`: top agencies by payment amount
- `vendor_totals`: top vendors by payment amount
- `monthly_trend`: month-by-month payment totals

Common parameters:

```text
biennium=2025-27
limit=10
agency_code=<optional agency code>
category=<optional exact category label>
```

## Retrieval Strategy

1. Use the checked-in operating, revenue, and OFM population snapshot files as the normal answer source for budget authority, revenue, and resident denominator questions.
2. Use `summary.json` for validation checks before trusting totals.
3. Use `provenance.json` when the answer needs model refresh time, query-template hashes, source fingerprint details, or Power BI/ReportViewer source details.
4. Use the live Power BI or ReportViewer extractors only when refreshing snapshots, not during normal answer generation.
5. For Open Checkbook questions, run `scripts/source_data.py --json status washington.open_checkbook` and `scripts/source_data.py --json validate washington.open_checkbook` first. Use `ensure` or `refresh` when the managed local database is missing or stale, then query the local SQLite database through named queries.
6. If a question asks for an unsupported grain, answer with the supported grains and explain the boundary.

## Query Recipes

### OFM population denominator lookup

Read:

```text
jurisdictions/washington/data/ofm-population/2025-04-01/normalized/population-estimates.jsonl
```

Filter:

```text
value_kind = "estimate"
estimate_date = "2025-04-01"
jurisdiction = "Seattle" and row_type = "city_town"
jurisdiction = "King County" and row_type = "county"
```

Known checks:

```text
Seattle 2025 population estimate = 816600
King County 2025 population estimate = 2411700
State Total 2025 population estimate = 8115100
```

Use these rows only as resident denominators. A per-capita budget answer should cite the budget source and `washington.ofm_population`, then state the estimate date and budget-period mismatch.

### Largest agencies in the 2025-27 enacted operating budget

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/agency-by-fund-view.jsonl
```

Filter:

```text
fund_view = "Total Budgeted"
```

Known checks:

```text
rows = 102
Total Budgeted total = 150411096000
```

Largest Total Budgeted agency rows:

- WA State Health Care Authority: $38.033B
- Public Schools: $36.407B
- Dept of Social and Health Services: $25.021B
- University of Washington: $9.493B
- Children, Youth, and Families: $5.904B
- Community/Technical College System: $4.327B
- Department of Corrections: $3.341B
- Bond Retirement and Interest: $3.306B

### Functional area totals

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/functional-area-by-fund-view.jsonl
```

Filter:

```text
fund_view = "Total Budgeted"
```

Known checks:

```text
rows = 11
Total Budgeted total = 150411096000
```

Largest Total Budgeted functional area rows:

- Other Human Services: $51.743B
- Public Schools: $36.407B
- DSHS: $25.021B
- Higher Education: $18.923B
- Governmental Operations: $8.602B
- Special Appropriations: $4.364B
- Natural Resources: $3.757B
- Judicial: $751.5M

### Fund view comparison

Read either normalized table and group by `fund_view`.

Known checks:

```text
Total Budgeted = 150411096000
Outlook Funds (NGF-O) = 77857672000
```

Explain that `Total Budgeted` includes all budgeted funds in the report, while `Outlook Funds (NGF-O)` is a narrower near-general-fund/outlook view.

### Budget version summary

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/version-summary.jsonl
```

Use this to explain which 2025-27 biennial versions are visible in the summary report: agency request, governor proposal, House/Senate versions, passed legislature, and enacted.

### Statewide operating budget trend

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-biennium-summary.jsonl
```

Use this for questions like "How has the Washington state operating budget changed over time?"

Known checks:

```text
rows = 7
coverage = 2013-15 through 2025-27
historical_current_overlap_total = 150411096000
```

Known enacted base Total Budgeted biennial totals:

- 2013-15: $66.522B
- 2015-17: $78.888B
- 2017-19: $88.274B
- 2019-21: $99.706B
- 2021-23: $121.733B
- 2023-25: $133.610B
- 2025-27: $150.411B

Always state that this is an enacted base biennial Total Budgeted trend, not actual spending and not a supplemental/proposal comparison.

### Agency operating budget trend

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-agency-by-biennium.jsonl
```

Filter by `agency` or `agency_code`, then sort by `biennium`.

Known checks:

```text
rows = 711
agency totals by biennium match historical-biennium-summary.jsonl
2025-27 rows come from current_biennial_summary_powerbi
2013-15 through 2023-25 rows come from prior_summary_powerbi
```

When interpreting long trends, mention that official agency labels and agency structures can change over time.

### Functional area operating budget trend

Read:

```text
jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/normalized/historical-functional-area-by-biennium.jsonl
```

Filter by `functional_area` or `functional_area_code`, then sort by `biennium`.

Known checks:

```text
rows = 77
functional area totals by biennium match historical-biennium-summary.jsonl
2025-27 rows come from current_biennial_summary_powerbi
2013-15 through 2023-25 rows come from prior_summary_powerbi
```

Use this as the supported high-level policy grouping for historical Washington operating-budget trends.

### General Fund revenue trend

Read:

```text
jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/normalized/general-fund-revenue-by-biennium.jsonl
```

Known checks:

```text
rows = 12
coverage = 2003-05 through 2025-27
2025-27 estimated_revenue = 45098726991
2025-27 actual_revenue = 46142570002.15
2025-27 actual_minus_estimate = 1043843011.15
2025-27 actual_data_status = partial
actual_data_through = 2026-04
```

Use this for General Fund revenue trend questions. For closed biennia, `actual_data_status = complete`. For 2025-27, say the estimate, actual, and difference values are partial through April 2026 and should not be treated as full-biennium final actuals or a full-biennium forecast.

### General Fund revenue detail

Read:

```text
jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/normalized/general-fund-revenue-by-area-account.jsonl
```

Use this only for General Fund (001) revenue rows by biennium, `revenue_area`, and `account_or_agency`. Known check: 934 detail rows, and detail totals reconcile to the statewide biennium totals within rounding tolerance.

### Open Checkbook category breakdown

Ensure the managed local database exists, then run:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook category_breakdown --param biennium=2025-27 --param limit=10
```

Use this for questions like "What categories drive Washington state vendor payments?" State that this is actual vendor-payment data and that 2025-27 is partial through May 2026 unless the manifest reports a newer `data_through`.

### Open Checkbook agency totals

Run:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook agency_totals --param biennium=2025-27 --param limit=10
```

Use this for top agency actual-payment rankings. Do not describe the result as largest agency budgets; use "vendor payments" or "actual payments."

### Open Checkbook vendor totals

Run:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook vendor_totals --param biennium=2025-27 --param limit=10
```

Use this for top vendors by actual payment amount. Caveat that the rows are payments, not contract obligations or procurement terms.

### Open Checkbook monthly trend

Run:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook monthly_trend --param biennium=2025-27
```

Use this for current-biennium or historical payment timing questions. Include the manifest `data_through`, row count, and any current-biennium partial-status caveat.

## Analysis Patterns

### Where does Washington budget the most?

Use `agency-by-fund-view.jsonl`, filter to `Total Budgeted`, sort by `budgeted_amount desc`, and state the fund view.

### What is the difference between Total Budgeted and Outlook Funds?

Use the known fund-view totals and explain the accounting boundary. Do not mix the two in one ranking unless the user explicitly asks for a comparison table.

### Functional area questions

Use `functional-area-by-fund-view.jsonl`. This is the closest supported high-level policy grouping in the first Washington snapshot.

For historical functional area trends, use `historical-functional-area-by-biennium.jsonl`.

### Budget over time questions

Use `historical-biennium-summary.jsonl` for statewide trends. Use the historical agency or functional-area files only when the user asks for a specific agency or functional-area trend. Default to enacted base Total Budgeted rows and state the supported coverage range.

### Latest or current questions

Say the current Washington snapshot is the 2025-27 enacted biennial operating budget with current model refresh time `2025-07-22T17:18:33.94`. Historical trend rows use the prior summary model with refresh time `2025-12-29T18:08:24.87`. The separate 2026 supplemental report has been probed but is not implemented in this source slice.

For current Washington revenue questions, say the current revenue snapshot is `2025-27-revenue-through-2026-04`; 2025-27 revenue values are partial through April 2026.

For current Washington checkbook questions, inspect the managed local manifest. The source card's reviewed current boundary is `Payments through April 2026`; a refreshed local database may report a newer `data_through`. Always use the manifest value when it exists.

## Interpretation Rules

- Use "budgeted amount" or "authorized operating budget," not actual spending.
- State the budget version: `2025-27 enacted`.
- State the fund view, especially when using `Outlook Funds (NGF-O)`.
- Amounts are dollars in the normalized snapshot.
- Historical trend answers default to enacted base biennial Total Budgeted rows from 2013-15 through 2025-27.
- Do not answer 2026 supplemental changes unless the supplemental snapshot is added.
- For revenue answers, state `actual_data_through` whenever using `actual_revenue` or `actual_minus_estimate`, and whenever using the in-progress 2025-27 `estimated_revenue`.
- For checkbook answers, use "actual vendor payments" or "payment amount," not "budget."
- For checkbook answers, state the managed local database status, data-through month, selected biennium, grain, measure, row count or query check, and caveats.
- Do not answer pre-2013-15 Washington operating-budget trends from this snapshot.
- Do not answer proposal-stage, House, Senate, Governor, supplemental, or revised historical comparisons unless a matching normalized table is added.
- Do not infer procurement contract terms, invoice details, payroll, staffing, service quality, policy outcomes, or operational performance from checkbook rows.
- Do not infer service quality, policy outcomes, or operational performance from budget rows alone.
- Do not compare Washington to Seattle or King County until accounting definitions and normalized dimensions are explicit.

## Validation Checks

Known checks from snapshot `2025-27-enacted-2025-05-20`:

- Total Budgeted agency rows: 102
- Total Budgeted functional area rows: 11
- Total Budgeted total: $150.411B
- Outlook Funds (NGF-O) total: $77.858B
- Agency and functional area totals match by fund view
- Version summary rows: 28
- Historical statewide trend rows: 7
- Historical agency trend rows: 711
- Historical functional area trend rows: 77
- Historical coverage: 2013-15 through 2025-27
- Historical totals by biennium match agency and functional area totals
- Historical 2025-27 overlap matches the current Total Budgeted total: $150.411B

If a result differs materially, verify the snapshot version, budget version filter, fund view, and whether the user asked for budgeted values or actuals.

Known revenue checks from snapshot `2025-27-revenue-through-2026-04`:

- General Fund revenue biennium rows: 12
- General Fund revenue detail rows: 934
- Historical coverage: 2003-05 through 2025-27
- Actual data through: April 2026
- 2025-27 actual data status: partial
- 2025-27 estimated revenue: $45.099B
- 2025-27 actual revenue: $46.143B
- Detail totals reconcile to statewide biennium totals within rounding tolerance

Known Open Checkbook checks from source card `washington.open_checkbook`:

- Current official file: `VendorPayments2527.xlsx`
- Current file rows: 382,783
- Current file periods: 10
- Current file fiscal year/month range: `2026-01` through `2026-10`
- Current file data through: April 2026
- Current file agencies: 100
- Current file categories: 9
- Historical XLSX coverage: 2013-15 through 2025-27
- Historical official file total content length: 411,417,899 bytes

When answering from the local database, prefer the manifest and query result over the source-card probe values. If the manifest and source card disagree, report the local manifest as the active answer source and note the source-card probe date may be older.

## Answer Style

Use this compact structure for source-backed answers:

```text
Conclusion:
Numbers:
How to read this:
Trace:
- Source:
- Public source or source surface:
- Snapshot:
- Data-through:
- Grain:
- Measure:
- Filters/query logic:
- Check:
- Caveats:
```

Example trace:

```text
Trace:
- Source: Fiscal WA 2025-27 Biennial Omnibus Operating Budget Summary Comparison, snapshot 2025-27-enacted-2025-05-20
- Public source: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien
- Data-through: not applicable; this is the 2025-27 enacted budget snapshot
- Grain: agency
- Measure: budgeted_amount
- Filters/query logic: read agency-by-fund-view.jsonl, filter fund_view = "Total Budgeted", sort by budgeted_amount desc
- Check: 102 Total Budgeted agency rows; Total Budgeted total = $150.411B
- Caveats: budgeted/authorized operating budget, not actual spending; 2025-27 enacted biennial budget; not the 2026 supplemental snapshot
```

Revenue trace example:

```text
Trace:
- Source: Fiscal WA Revenue by Biennium, snapshot 2025-27-revenue-through-2026-04
- Public source: https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: Actual Data Through April 2026
- Grain: biennium
- Measure: estimated_revenue, actual_revenue, actual_minus_estimate
- Filters/query logic: read general-fund-revenue-by-biennium.jsonl; fund = "General Fund (001)"
- Check: 12 biennium rows; detail totals reconcile to statewide totals
- Caveats: 2025-27 values are partial through April 2026; General Fund (001) only; not operating budget or actual spending
```

Open Checkbook trace example:

```text
Trace:
- Source: Fiscal WA Open Checkbook, managed local DB for washington.open_checkbook
- Public source: https://fiscal.wa.gov/Spending/Checkbook.aspx
- Storage: managed_local_db; manifest data_through = 2026-04
- Data-through: Payments through April 2026, or the newer manifest value after refresh
- Grain: category
- Measure: amount
- Filters/query logic: source_data.py query washington.open_checkbook category_breakdown --param biennium=2025-27 --param limit=10
- Check: local manifest row_count and source_files row counts; current source-card probe observed 382,783 current-file rows
- Caveats: actual vendor payments, not budget authority, revenue, contracts, invoices, payroll, staffing, or outcomes; 2025-27 is partial through May 2026 unless refreshed
```
