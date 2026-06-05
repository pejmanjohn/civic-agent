# Washington State Budget Source Probe

Status: accepted and implemented for operating budget summary snapshots and General Fund revenue by biennium snapshots; additional Fiscal WA surfaces remain candidates/context

Date: 2026-06-04

## Question

Can Civic Agent support Washington state budget questions from official sources, comparable to Seattle and King County?

## Initial Answer

Yes, but not through the OFM budget landing page alone.

The best primary data surface is Washington's Fiscal Information site:

- `https://fiscal.wa.gov/statebudgets/statebudgetsoverview`
- `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- `https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior`

OFM remains an official source for budget proposals, enacted/executive context, agency budget materials, and source documents:

- `https://ofm.wa.gov/budget/`

For budgeted/authorized operating data, Fiscal WA is a Power BI-backed official public dashboard/source family. For revenue estimate-vs-actual data, Fiscal WA also exposes session-based ReportViewer exports. For actual vendor payments, Fiscal WA exposes downloadable XLSX files through Open Checkbook.

Open Checkbook is now tracked as its own actual-spending source because it answers vendor-payment questions, not budget or revenue questions:

```text
docs/source-probes/washington-open-checkbook.md
jurisdictions/washington/sources/open-checkbook.source.json
```

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
| OFM budget hub | Washington Office of Financial Management | `https://ofm.wa.gov/budget/` | portal/documents | Good official entry point, not the best machine data source. |
| Fiscal WA state budgets | LEAP and OFM | `https://fiscal.wa.gov/statebudgets/statebudgetsoverview` | portal/dashboard | Best official budget data hub. Separates operating, capital, transportation, and combined budgets. |
| Fiscal WA biennial operating summary comparison | LEAP and OFM | `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien` | Power BI dashboard | Accepted current 2025-27 operating budget summary surface. |
| Fiscal WA prior operating summary | LEAP and OFM | `https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior` | Power BI dashboard | Accepted historical enacted base trend surface. |
| Fiscal WA revenue by biennium | LEAP and OFM | `https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx` | ReportViewer export | Accepted General Fund revenue estimate-vs-actual surface, with biennia back to 2003-05 and current 2025-27 values partial through April 2026. |
| Fiscal WA fund detail by revenue source | LEAP and OFM | `https://fiscal.wa.gov/Revenue/RevenueBySource.aspx` | ReportViewer export | Context-only companion surface for future selected-source fund detail extraction. |
| Fiscal WA revenue source by fund detail | LEAP and OFM | `https://fiscal.wa.gov/Revenue/RevenueByFund.aspx` | ReportViewer export | Context-only companion surface for future selected-fund revenue source detail extraction. |
| Fiscal WA operating search | LEAP and OFM | `https://fiscal.wa.gov/Search/OperatingDataSearch` | Power BI dashboard | Context-only for this source; useful for line-item search investigation, but not accepted for full historical summary trends because totals did not reconcile to the summary report. |
| Fiscal WA agency information | LEAP and OFM | `https://fiscal.wa.gov/statebudgets/AgencyInfo` | portal/dashboard links | Maps agency-related reports across operating, capital, transportation, budget bills, LEAP docs, and search. |
| Fiscal WA Open Checkbook | LEAP and OFM | `https://fiscal.wa.gov/Spending/Checkbook` | Power BI plus XLSX downloads | Actual vendor payments by biennium, monthly updates. Not a budget source. |

## Surface Classification

Recommended first accepted source:

```text
washington.operating_budget
access_method: powerbi_snapshot
```

Accepted revenue companion source:

```text
washington.revenue_by_biennium
access_method: reportviewer_snapshot
```

Useful companion source:

```text
washington_state.open_checkbook
access_method: official_bulk_download
```

Do not mix these in one source. Operating budget answers, revenue estimate-vs-actual answers, and actual vendor-payment answers have different measures, grains, and caveats.

Probe methods used:

- Generic HTML/header probe
- Dashboard probe
- Power BI probe
- Bulk file probe
- Document/portal context review

Primary operating access surface:

```text
Power BI public report snapshots for Fiscal WA operating budget summary data
```

Primary revenue access surface:

```text
ReportViewer XML/XLSX/CSV exports for Fiscal WA RevenueSW, snapshotted by biennium
```

Companion and candidate surfaces:

```text
OFM budget hub and budget documents for context; ERFC revenue forecast notebooks for forecast context; Fiscal WA Operating Search for line-item investigation; Fiscal WA Open Checkbook XLSX for separate actual-spending questions
```

## How The Site Was Probed

### 1. Start from the user URL

The OFM page was inspected first as the official budget hub:

```text
https://ofm.wa.gov/budget/
```

This is official, but it points more toward proposals, budget documents, instructions, and explanatory material than toward a clean public data API.

### 2. Follow the official budget-data path

Search and page inspection led to Fiscal WA. The state budgets overview describes Washington's operating, capital, and transportation budgets, and the navigation exposes interactive reports and search pages.

The agency information page explicitly lists operating budget reports, agency detail reports, enacted budget bills, LEAP documents, and `Search Operating Budget Data`.

### 3. Inspect interactive report embeds

Fetching the operating search page showed embedded Power BI:

```text
https://fiscal.wa.gov/Search/OperatingDataSearch
```

Embedded report:

```text
https://app.powerbi.com/view?r=eyJrIjoiMTcwMTM0ZGItNmNkZi00ZTgyLWFmZWEtMWZhMDIxNjcyYWExIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9
```

Decoded `r` payload:

```json
{"k":"170134db-6cdf-4e82-afea-1fa021672aa1","t":"b4eb0ccf-0194-4663-a56a-9ed91efd3308","c":6}
```

The Power BI embed resolved to:

```text
https://wabi-west-us-redirect.analysis.windows.net/
```

The API host used for successful metadata calls was:

```text
https://wabi-west-us-api.analysis.windows.net
```

### 4. Verify metadata access

Operating search metadata was accessible with `X-PowerBI-ResourceKey`.

Observed model:

```json
{
  "id": 5094236,
  "displayName": "BudOpSearch",
  "dbName": "7e925de4-07e3-4e72-9766-d127fd3b1d65",
  "LastRefreshTime": "2026-03-17T16:59:06.613",
  "directQueryMode": false,
  "sizeInMBs": 17
}
```

Key entity:

```text
Operating_Search
```

Useful fields observed:

```text
Biennium, SessionType, VersionCode, WebTitle35, Agency, Program,
ItemGroup, Item, ItemTitle, Fund, AppropType, Title35,
DescriptiveText, Amount, FY, Final, AgencyKey, SearchText,
SessionKey, VerType, PublishDate, CreateDate
```

### 5. Inspect a second operating report

The supplemental operating summary comparison page also embeds Power BI:

```text
https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonsupp
```

Embedded report key:

```text
21c1830b-8aa6-4283-bb42-863d2afcc2ba
```

Observed model:

```json
{
  "id": 12425925,
  "displayName": "BudOpSummaryComparisonSupp",
  "dbName": "334e1536-de21-44a6-841d-5ea55741e718",
  "LastRefreshTime": "2026-03-17T16:59:43.863",
  "directQueryMode": false,
  "sizeInMBs": 1
}
```

Useful entities:

```text
Operating_Funding
Operating_VersionInfo
Operating_ActiveFunds
Titles_Agency
Titles_FunctionalArea
```

`Operating_Funding` fields observed:

```text
Biennium, SessionType, VersionCode, Agency, Program, Subprogram,
ItemGroup, Item, OmniFlag, CapitalFlag, FY, Fund, AppropType,
Amount, FundCode, FundTTl, Pct, SessionTitle, TOTB, Supp
```

`Operating_VersionInfo` carries budget version metadata such as:

```text
Biennium, SessionType, VersionCode, IsPublic, Final, BudgetType,
Chamber, VersionOwner, Title10, Title20, Title35, VersionInformation,
CreateDate, PublishDate, WebTitle20, WebTitle35
```

### 6. Replay one safe querydata request

A small aggregate `querydata` POST against `Operating_Funding` returned data, proving the report is queryable through public Power BI internals.

The response used Power BI's compressed `dsr` row format with `ValueDicts`, so it needs a source-specific parser, not casual JSON field access.

This puts Fiscal WA in the same integration class as King County, not Seattle:

```text
Seattle: clean Socrata API
King County: official Power BI dashboard snapshot
Washington: official Fiscal WA Power BI dashboard snapshot
```

### 7. Check actual-spending companion data

Open Checkbook exposes a stable XLSX download for current biennium vendor payments:

```text
https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx
```

Observed headers:

```text
content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
content-length: 22019618
last-modified: Tue, 26 May 2026 23:51:24 GMT
```

The Fiscal WA page states this is state agency vendor payments for the 2025-27 biennium and that data is added monthly with previous month vendor payments.

This is useful for actual spending/payment questions. It is not a budget source.

## Implemented Source

`washington.operating_budget` supports:

- 2025-27 enacted operating budget totals by agency and fund view.
- 2025-27 enacted operating budget totals by functional area and fund view.
- Budget-version summaries for the current 2025-27 biennial operating summary report.
- Statewide enacted base Total Budgeted operating budget trends by biennium from 2013-15 through 2025-27.
- Agency enacted base Total Budgeted trends by biennium from 2013-15 through 2025-27.
- Functional-area enacted base Total Budgeted trends by biennium from 2013-15 through 2025-27.
- Narrow answer traces using official Fiscal WA report metadata, reviewed query templates, row-level `source_surface_id`, and reconciliation checks.

Accepted source surfaces:

- `current_biennial_summary_powerbi`: Fiscal WA biennial operating summary comparison, current 2025-27 agency/function/fund-view rows.
- `prior_summary_powerbi`: Fiscal WA prior operating summary, historical enacted base statewide/agency/function rows.

Context or candidate surfaces:

- `operating_search_powerbi`: context-only for line-item investigation; not accepted for full historical trends because the 2025-27 enacted aggregate did not reconcile to the accepted summary total.
- `prior_single_version_reportviewer`: candidate context-only older surface; not used for normal answers until replay and reconciliation are proven.

## Unsupported Claims

Do not use this first source for:

- Actual spending or vendor payments.
- Staffing/FTE unless a reviewed staffing or FTE source is added.
- Capital or transportation budget questions unless those separate report models are probed and accepted.
- Historical operating budget trends before 2013-15.
- Supplemental, revised, proposal-stage, House, Senate, or Governor historical comparisons unless an explicit normalized table is added.
- Claims that Civic Agent supports all Washington public finance.
- Cross-jurisdiction comparisons with Seattle or King County until accounting definitions are mapped.

## Recommended Decision

Decision:

```text
accept-snapshot
```

Next implementation:

```text
jurisdictions/washington/
  skill.md
  sources/operating-budget.source.json
  scripts/extract_operating_budget.py
  data/operating-budget/query_templates/*.query.json
  data/operating-budget/<snapshot-version>/normalized/*.jsonl
  data/operating-budget/<snapshot-version>/summary.json
  data/operating-budget/<snapshot-version>/provenance.json
```

Use the King County extractor as the pattern, but keep this source-specific. Do not create a generic Power BI adapter yet.

## Remaining Open Questions

- Should a separate Fiscal WA Operating Search source be added for line-item search and fiscal-year detail?
- Can the prior Single Version ReportViewer surface be replayed safely enough to extend selected historical rows before 2013-15?
- Should supplemental/revised historical comparison tables be added as a separate normalized grain?
- Are capital and transportation separate Phase 2 sources or deferred until the operating source proves the workflow?
