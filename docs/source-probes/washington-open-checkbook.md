# Washington Open Checkbook Source Probe

Status: probe complete, accepted for managed local database implementation

Date: 2026-06-05

## Question

Can Civic Agent answer Washington state actual-spending/checkbook questions from official vendor-payment data?

## Source Identity

- Jurisdiction: Washington State
- Budget family: actual spending/checkbook
- Official owner: Fiscal WA / LEAP / Office of Financial Management
- Public inspection URL: `https://fiscal.wa.gov/Spending/Checkbook.aspx`
- Candidate machine URL: `https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx`
- Source type: official bulk download plus Power BI inspection page
- Source priority: primary official source for state agency vendor-payment questions

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
| Fiscal WA Open Checkbook | LEAP and OFM | `https://fiscal.wa.gov/Spending/Checkbook.aspx` | Power BI plus XLSX download | State agency vendor payments for the current biennium; page says data is added monthly with previous month vendor payments. |
| Current vendor payments XLSX | LEAP and OFM | `https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx` | XLSX bulk download | Current 2025-27 vendor-payment rows. |
| Object/subobject definitions | LEAP and OFM | `https://fiscal.wa.gov/Spending/ObjectSubObjectDefinitions.pdf` | PDF | Category and subcategory definitions. |
| Open Checkbook disclaimer | LEAP and OFM | `https://fiscal.wa.gov/Spending/DisclaimerWAVendorCB.pdf` | PDF | Source-specific caveats. |
| State agency contracts | data.wa.gov | `https://data.wa.gov/dataset/Agency-Contracts-Fiscal-Year-2025/6fx9-ncas/data_preview` | Socrata dataset | Procurement/contract source, not actual payments. Keep separate from checkbook. |

## Surface Classification

Access candidates:

- [x] Official bulk download
- [x] Official public dashboard
- [ ] Official documented API
- [ ] Official open data portal
- [ ] Official document/PDF only
- [ ] HTML scrape only
- [ ] Unofficial mirror/context source
- [ ] Not usable

Probe methods attempted:

- [x] Generic HTML/header probe
- [x] Bulk file probe
- [x] Dashboard probe
- [x] Power BI probe
- [x] Document/PDF probe
- [x] Socrata/open data probe for adjacent contracts surface

Evidence:

```text
The Open Checkbook page links ../Spending/VendorPayments2527.xlsx, object/subobject definitions, and disclaimer PDFs.
The page states that it contains state agency vendor payments for the 2025-27 biennium and that data is added monthly with previous month vendor payments.
Current XLSX headers: Bien, FY, FMonth, Agy, Agency, Object, Category, Subobj, SubCategory, Vendor, Amount.
Current XLSX row count: 382,783 rows.
Current XLSX latest fiscal period: FY2026 fiscal month 10, which maps to April 2026.
Historical XLSX URL pattern exists from VendorPayments1315.xlsx through VendorPayments2527.xlsx.
```

Primary access surface:

```text
official bulk XLSX download
```

Primary source identifiers:

```text
https://fiscal.wa.gov/Spending/Checkbook.aspx
https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx
```

Companion surfaces:

```text
Fiscal WA Power BI Open Checkbook visual inspection page
ObjectSubObjectDefinitions.pdf
DisclaimerWAVendorCB.pdf
```

## Storage Policy

Recommended storage tier:

```text
managed_local_db
```

Why:

```text
The official XLSX files are stable and valuable but too large for git and too slow to parse during every answer. Current plus historical files total about 411 MB before normalization.
```

Normal answer source:

```text
local DB
```

Freshness check:

```text
source file metadata: URL, content length, last-modified, checksum, row count, and max fiscal year/month.
```

Repo artifacts:

```text
source card, probe, builder, tests, fixtures, docs, optional compact rollups only if reviewably small
```

Local artifacts:

```text
raw XLSX files, SQLite database, manifest
```

Partial-period data-through rule:

```text
Map max FY/FMonth to calendar month for the current biennium. FY2026 month 10 maps to 2026-04.
```

## Data Model

Fields and dimensions:

| Field | Type | Meaning | Notes |
|---|---|---|---|
| `Bien` | text | Biennium | Example: `2025-27`. |
| `FY` | number | Fiscal year | Washington fiscal year starts in July. |
| `FMonth` / `Fiscal Month` | number | Fiscal month | Older `2013-15` file uses `Fiscal Month`; normalize both headers. |
| `Agy` | text | Agency code | Keep as text to preserve leading zeros if they appear. |
| `Agency` | text | Agency name | Official labels include whitespace padding. |
| `Object` | text | Object code | Payment category code. |
| `Category` | text | Object category | Example: Goods and Services. |
| `Subobj` | text | Subobject code | Payment subcategory code. |
| `SubCategory` | text | Subcategory | Example: Other Contractual Services. |
| `Vendor` | text | Vendor name | Official vendor label. |
| `Amount` | number | Vendor-payment amount | Payment amount in dollars. |

Measures:

| Measure | Meaning | Budgeted or actual? | Notes |
|---|---|---|---|
| `amount` | Vendor-payment amount | Actual payment | Not budget authority, contract obligation, invoice detail, or payroll. |

Time/version fields:

```text
Biennium, FY, FMonth, derived calendar_month, official file last-modified, downloaded_at, current_data_through.
```

Freshness and publication metadata:

```text
Current file HEAD observed: content-length 22,019,618; last-modified Tue, 26 May 2026 23:51:24 GMT.
Fiscal WA page states data is added monthly with previous month vendor payments.
```

## Extraction Approach

Recommended access method:

```text
accept-snapshot
```

Why:

```text
The source is an official bulk download with stable public file URLs. It should not be parsed live for every answer; build a managed local database instead.
```

If snapshot:

- Query/capture templates: not needed; use official file URLs from source surfaces.
- Normalized tables: `payments`, `source_files`, `refresh_runs`.
- Summary checks: row counts, file metadata, max fiscal period, agency count, category list.
- Provenance fields: file URL, last-modified, content length, sha256, fetched_at, row count, data-through boundary.

## Supported Questions

- Which agencies had the largest actual vendor payments in a selected biennium or fiscal period?
- What categories or subcategories account for the largest vendor-payment amounts?
- Which vendors received the largest payments from a selected agency or category?
- How did vendor payments trend month by month?
- What does Open Checkbook show, and how does it differ from budget, revenue, contract, payroll, or service-outcome data?

## Unsupported Claims

- Operating, capital, transportation, or revenue budget authority.
- Revenue forecasts, estimated revenue, actual revenue collected, or tax receipts.
- Procurement contract terms, contract obligations, bid processes, or contract amendments.
- Payroll, employee rosters, budgeted FTE, vacancies, or staffing claims.
- Invoices, purchase orders, or deliverables beyond the payment rows.
- Service quality, policy outcomes, program performance, or causal explanations.

## Validation Checks

| Check | Expected result | How to reproduce |
|---|---:|---|
| Current file URL is downloadable | HTTP 200 | `HEAD https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx` |
| Current file content length | 22,019,618 bytes | HEAD response |
| Current file row count | 382,783 payment rows | Parse first worksheet and exclude header row |
| Current file max fiscal period | FY2026 month 10 | Parse `FY` and `FMonth` columns |
| Current data-through | April 2026 | Map FY2026 month 10 to calendar month |
| Historical files available | 2013-15 through 2025-27 | HEAD `VendorPayments{YY}.xlsx` URLs |
| Total historical XLSX size | 411,417,899 bytes | Sum observed content lengths |

## Worked Answer Trace

Question:

```text
Which categories account for the largest Washington state agency vendor payments in the current biennium?
```

Trace:

```text
Source: Fiscal WA Open Checkbook
Access method: official_bulk_download
Storage policy: managed_local_db
Snapshot/version: local database built from VendorPayments2527.xlsx and any selected historical files
Grain: category
Measure: amount
Filters/query logic: biennium = 2025-27; group by Category; sum Amount
Validation: local manifest row count and source file metadata match accepted source surface
Caveats: current biennium is partial through April 2026; vendor payments are not budget authority, contract obligations, payroll, invoices, or service outcomes
```

## Risks

- Official file headers can drift.
- Current biennium is partial and monthly, so data-through must be carried into answers.
- Full historical line items are too large for git.
- Vendor payments can be confused with budget authority, contract obligations, invoices, payroll, or outcomes.

## Decision

Decision:

```text
accept-snapshot
```

Next artifact:

```text
source card, managed local database builder, tests, Washington skill routing, demo
```
