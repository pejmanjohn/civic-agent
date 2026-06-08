# Washington OFM April 1 Population Source Probe

Status: probe complete, accepted for checked-in snapshot implementation

Date: 2026-06-08

## Question

Can Civic Agent use official Washington population estimates as a denominator source for per-resident budget answers for Seattle and King County?

## Source Identity

- Jurisdiction: Washington State, with city, town, county, and state estimate rows.
- Budget family: companion population denominator for Scale recipes, not a budget source.
- Official owner: Washington Office of Financial Management, Forecasting and Research Division.
- Public inspection URL: `https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/`
- Candidate machine URL: `https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_final.xlsx`
- Source type: official bulk XLSX download plus official inspection page.
- Source priority: primary official denominator source for Washington city, town, county, and state April 1 population estimates.

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
| April 1 official population estimates page | Washington OFM | `https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/` | Official inspection page | Lists the April 1, 2025 release and links final PDF, final XLSX, change/rank XLSX, housing units, archive, technical information, and population trends. |
| April 1, 2025 population final XLSX | Washington OFM | `https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_final.xlsx` | Bulk XLSX download | Best candidate for M5 extraction because it includes counties, incorporated and unincorporated county rows, cities, towns, state totals, and notations. |
| April 1, 2025 population final PDF | Washington OFM | `https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_final.pdf` | PDF | Human-readable companion/citation surface. |
| Population change and rank XLSX | Washington OFM | `https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_change_and_rank.xlsx` | Bulk XLSX download | Useful for ranked change context, but not needed for first per-capita denominator acceptance. |
| Data.WA `9aqx-raft` | WA State OFM attribution on data.wa.gov | `https://data.wa.gov/api/views/9aqx-raft` | Socrata dataset | Official-attributed mirror for population change/rank, but metadata observed `rowsUpdatedAt` and `viewLastModified` in 2020 and sample rows are county-level. Treat as watchlist/context, not the primary 2025 denominator source. |

## Surface Classification

Access candidates:

- [ ] Official documented API
- [ ] Official open data portal
- [x] Official bulk download
- [ ] Official public dashboard
- [x] Official document/PDF
- [ ] HTML scrape only
- [ ] Unofficial mirror/context source
- [ ] Not usable

Probe methods attempted:

- [x] Generic HTML/header probe
- [ ] Official API probe
- [x] Socrata/open data probe for adjacent Data.WA candidate
- [x] Bulk file probe
- [x] Document/PDF probe
- [x] XLSX workbook inspection

Evidence:

```text
OFM page canonical URL: https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
OFM page dateModified metadata observed: 2026-05-12T19:45:07+00:00.
OFM page section observed: April 1, 2025, with final PDF, final Excel, change/rank Excel, housing Excel, archive, technical information, and population trends links.
Final XLSX HEAD observed: content-type application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; content-length 68,267; last-modified Tue, 24 Feb 2026 08:05:27 GMT; etag "699d5bc7-10aab".
Workbook sheets: Population, Notations.
Population sheet size: 456 rows x 10 columns; data rows after header/footer cleanup: 449.
Population headers: Line, Filter, County, Jurisdiction, 2020 Population Census, 2021 Population Estimate, 2022 Population Estimate, 2023 Population Estimate, 2024 Population Estimate, 2025 Population Estimate.
Filter counts: 39 county rows, 39 unincorporated county rows, 39 incorporated county rows, 289 city/town rows, 39 separator rows, and 3 state total rows.
Data.WA candidate id 9aqx-raft observed with attribution WA State Office of Financial Management and provenance official, but rowsUpdatedAt/viewLastModified are 2020-era metadata.
```

Primary access surface:

```text
official bulk XLSX download
```

Primary source identifiers:

```text
https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_final.xlsx
```

Companion surfaces:

```text
final PDF, population change/rank XLSX, technical information page, historical archive, Data.WA 9aqx-raft watchlist candidate
```

## Data Model

Fields and dimensions:

| Field | Type | Meaning | Notes |
|---|---|---|---|
| `Line` | integer | Official row number | Stable enough for spot checks within one release. |
| `Filter` | integer or marker | Row type | Observed values: `1` county, `2` unincorporated county, `3` incorporated county, `4` city/town, `100` state total, `200` unincorporated state total, `300` incorporated state total, `.` separator. |
| `County` | text | County grouping | City/town rows carry their county. |
| `Jurisdiction` | text | County, city, town, or state total label | Examples: `King County`, `Seattle`, `State Total`. |
| `2020 Population Census` | integer | 2020 census baseline | Keep as baseline, not an estimate date. |
| `2021-2025 Population Estimate` | integer | April 1 estimate by year | Normalize to long rows with `estimate_year`. |

Measures:

| Measure | Meaning | Budgeted or actual? | Notes |
|---|---|---|---|
| `population_estimate` | Official April 1 population estimate | Population denominator | Not a budget amount and not actual spending. |
| `population_census` | 2020 census count | Census baseline | Useful for validation/context, not the default current denominator. |

Time/version fields:

```text
release_year = 2025
estimate_date = April 1 of the estimate year
estimate_year = 2021-2025 for estimate columns
census_year = 2020 for census column
file last-modified and etag from HEAD
```

Freshness and publication metadata:

```text
The latest release on the official page is April 1, 2025 as observed on 2026-06-08.
The final XLSX last-modified header observed on 2026-06-08 was Tue, 24 Feb 2026 08:05:27 GMT.
```

Hierarchy:

```text
state total -> county -> incorporated/unincorporated county -> city/town rows
```

## Extraction Approach

Recommended access method:

```text
accept-snapshot
```

Why:

```text
The official file is compact, annual, public, and reviewable. Normal answers should not depend on live HTML parsing, and a checked-in normalized snapshot can carry row counts, workbook metadata, checksums, and spot checks.
```

If snapshot:

- Query/capture templates: direct XLSX download from the final population file URL.
- Normalized tables: one long `population-estimates.jsonl` table with `source_row`, `row_type`, `county`, `jurisdiction`, `estimate_year`, `estimate_date`, `population`, `value_kind`, and notation fields when present.
- Summary checks: workbook sheet names, row counts by row type, statewide 2025 population, Seattle 2025 population, King County 2025 population, and King County incorporated/unincorporated reconciliation.
- Provenance fields: public inspection URL, file URL, downloaded_at, content_length, last_modified, etag, sha256, workbook sheet names, row count, extractor version.

## Storage Policy

Recommended storage tier:

```text
checked_in_snapshot
```

Why:

```text
The normalized data should be small enough for git, slow-changing enough for annual refreshes, and important enough that per-capita answers should work offline with reviewed provenance.
```

Normal answer source:

```text
repo snapshot
```

Freshness check:

```text
source file metadata: official release year, file URL, content length, last-modified, etag, checksum, row count, and latest estimate year.
```

Repo artifacts:

```text
source card, extractor, normalized snapshot, summary, provenance, tests, benchmark case update
```

Local or hosted artifacts:

```text
none expected for first slice
```

Partial-period data-through rule:

```text
none. These are point-in-time April 1 estimates, not partial fiscal-year measures.
```

## Supported Questions

- What is the official April 1 population estimate for Seattle?
- What is the official April 1 population estimate for King County?
- What denominator should Civic Agent use for Seattle or King County per-resident budget answers when the caveats are acceptable?
- How do county, incorporated county, unincorporated county, city, town, and state total population estimates reconcile within the OFM release?

## Unsupported Claims

- Budget amounts, spending, revenue, tax base, or fiscal capacity.
- Service population, daytime population, taxpayers, households, or utility customer counts.
- Age, sex, race, ethnicity, income, housing, or demographic composition from this final population workbook.
- Population outside Washington state.
- Claims that city and county budgets are service-comparable merely because resident denominators exist.

## Validation Checks

| Check | Expected result | How to reproduce |
|---|---:|---|
| Final XLSX is reachable | HTTP 200, XLSX content type | `curl -sIL <final-xlsx-url>` |
| Workbook sheets | `Population`, `Notations` | Load workbook and list sheets. |
| Population sheet headers | 10 expected columns from `Line` through `2025 Population Estimate` | Read row 5 of `Population`. |
| Cleaned population rows | 449 | Count rows after header/footer cleanup, preserving separator and total rows for validation. |
| County rows | 39 | Count `Filter == 1`. |
| Seattle 2025 estimate | 816,600 | Find `Jurisdiction == "Seattle"` and `Filter == 4`. |
| King County 2025 estimate | 2,411,700 | Find `Jurisdiction == "King County"` and `Filter == 1`. |
| State total 2025 estimate | 8,115,100 | Find `Jurisdiction == "State Total"` and `Filter == 100`. |
| King County incorporated reconciliation | 2,161,475 | Sum King County city/town rows and compare to `Incorporated King County`. |
| King County full reconciliation | 2,411,700 | Add `Unincorporated King County` 250,225 plus `Incorporated King County` 2,161,475. |

## Source Fingerprint

Citation fields:

```text
source_id: washington.ofm_population
official_owner: Washington Office of Financial Management, Forecasting and Research Division
public_inspection_url: https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
file_url: https://ofm.wa.gov/wp-content/uploads/sites/default/files/public/dataresearch/pop/april1/ofm_april1_population_final.xlsx
release: April 1, 2025 official population estimates
estimate_date: April 1, 2025 for current denominator rows
file_last_modified_observed: Tue, 24 Feb 2026 08:05:27 GMT
file_etag_observed: "699d5bc7-10aab"
content_length_observed: 68267
primary_sheet: Population
notation_sheet: Notations
spot_checks: Seattle 816600; King County 2411700; State Total 8115100
```

## Benchmark Impact

Milestone 5 accepted this source through a source card, extractor, normalized snapshot, summary, provenance, and tests. The Scale per-resident case now includes `washington.ofm_population` as an expected source and moves from missing-denominator to source-backed partial mode.

Per-capita answers still require denominator caveats: OFM source, April 1 estimate date, resident-jurisdiction boundary, fiscal-year mismatch with Seattle and King County budget frames, and the fact that resident population does not make city and county service responsibilities directly comparable.

## Recommendation

Use the final OFM April 1 population workbook as the checked-in snapshot source. Keep the Data.WA `9aqx-raft` dataset as a watchlist/context candidate unless a future probe proves it is current, complete for city/town rows, and preferable to the canonical OFM workbook.
