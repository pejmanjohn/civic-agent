# Source Probe Brief: SAO Financial Intelligence Tool (FIT) Filed Annual Actuals

Status: accepted (probed live 2026-07-13; every number verified with a reproduction URL)

## Question

```text
What does my Washington city / county / school district / special district actually take in and spend?
```

## Source Identity

- Jurisdiction: all Washington local governments (~2,300 filers: 281 cities/towns, 39 counties, 295 school districts, fire/port/transit/other special districts)
- Budget family: filed annual actuals (revenues and expenditures as filed)
- Official owner: Washington State Auditor's Office (SAO); school data as reported to OSPI
- Public inspection URL: `https://portal.sao.wa.gov/FIT/`
- Candidate machine URL: `https://portal.sao.wa.gov/FIT/api` (OData v4, unauthenticated)
- Source type: dashboard + undocumented internal API + official bulk download
- Source priority: highest - one integration makes every WA local government answerable for filed actuals; the state already did the normalization

## Surface Classification

Primary access surface:

```text
OData v4 API behind the FIT SPA (Microsoft.AspNetCore.OData; odata-version 4.0). Unauthenticated
for published Snapshots and the Schools dataset; the Live singleton (unpublished filings) is 401.
Official bulk XLSX extracts exist at https://portal.sao.wa.gov/FIT/extracts/FullExtract(year=N)
(years 2015-2025; ~41.5MB per year) - the sanctioned fallback if the API shifts.
```

Primary source identifiers:

```text
portal.sao.wa.gov/FIT/api; Snapshots(33) = "2025 Filing Milestone Snapshot" (code MILE2025,
created 2026-06-30, BARS year 2025, includedYears 2015-2025, 1,701 filers with data,
total revenues $85,489,701,170.74). Schools singleton = "2020-2025 Schools Financial Data
(as reported to OSPI)" (created 2026-02-05).
```

## Data Model (probed and decoded live)

- `fsSectionId`: 10 Beginning Balances, **20 Revenues, 30 Expenditures**, 25 Other Increases, 35 Other Decreases, 40 Ending Balances, 80 Balance Sheet (decoded from `Snapshots(33)/detail` -> `financialSummarySections`).
- `acctBasisTypeId`: 1 GAAP, 2 BARS Cash, 3 Schools Modified Accrual, 4 Schools Cash, 5 Special. Cities/counties file calendar-year GAAP or cash; schools file modified accrual with fiscal year ending Aug 31.
- `Schedule1AggregationsByGovt` is a pre-computed grouping-sets cube per (mcag, year); the government grand total per section is the single row where ALL eight dimension fields are null.
- Two measures: `totalAmount` (includes internal service funds) and `totalAmountExclIntlSrvc`. **FIT's headline numbers are the ExclIntlSrvc values** (verified equal to `GovernmentMetrics` for five governments; the difference reaches ~16% for Spokane - citing the wrong one will not match the FIT UI).
- `GovernmentMetrics` is a flat endpoint `{year, mcag, revenues, expenditures, population}` matching the headline totals to the penny - the recipe of choice for totals.
- Schools route: `Schools/financialReportAggregationsByGovt` (singleton, `fundCode` instead of `fund`, no `expenditureObjectId`), same all-dims-null total recipe.

Reproduction recipe (totals for one government-year):

```text
GET https://portal.sao.wa.gov/FIT/api/Snapshots(33)/GovernmentMetrics?$filter=mcag eq '{MCAG}' and year eq {YEAR}
```

## Verified Governments And Facts (2026-07-13, Snapshot 33)

| Government | mcag | 2024 revenues | 2024 expenditures |
|---|---|---:|---:|
| City of Spokane | 0724 | 729,876,646 | 648,638,448 |
| City of Walla Walla | 0773 | 117,546,221 | 96,284,787 |
| City of Tacoma | 0610 | 1,557,523,341 | 1,363,145,339 |
| King County | 0127 | 6,204,971,000 | 5,312,711,000 |
| Pierce County | 0152 | 1,086,328,271 | 883,659,316 |
| Sound Transit | 0987 | 2,599,304,000 | 1,385,233,000 |
| KC Regional Homelessness Authority | 3268 | 180,707,326 | 191,618,113 |

Schools (SY ending Aug 31, 2025): Seattle SD No. 1 (1903) revenues 1,518,641,110.55 / expenditures 1,193,163,295.90; Evergreen SD No. 114 (1841, Clark Co.) revenues 488,762,832.47 / expenditures 431,111,960.53. Multi-year verified back to 2015 (Spokane 2015: 469,879,284.37 / 416,869,114.66).

## Storage Policy

```text
checked_in_snapshot, pinned to FIT Snapshot 33 (MILE2025). The snapshot contains ONLY the
reviewed governments the card claims (10 governments + 2 school districts), not all 2,300 -
claims stay reviewed-source claims. Extractor: jurisdictions/washington/scripts/extract_fit_actuals.py.
Refresh: milestone snapshots publish ~quarterly (next likely id 34 ~2026-09); the drift check
watches Snapshots?$orderby=id desc for a new milestone.
```

## Supported Questions

- Total revenues and expenditures for a reviewed government, 2015-2024 (2025 early-cycle, partial).
- Revenue/expenditure trends and rough revenue-vs-expenditure framing per government.
- School district filed totals (2020-2025, OSPI basis).

## Unsupported Claims

- Budget authority, adopted budgets, or budget-vs-actual verdicts across sources without explicit frame alignment (filed annual actuals vs biennial/annual budget frames).
- Fund, department, program, account, or object breakdowns (cube exists but is not yet a reviewed claim).
- Checkbook/vendor transactions, staffing, or outcomes.
- Any government not in the reviewed list (the snapshot deliberately excludes them; extend and re-run).

## Risks

- Undocumented internal API with no version contract; field names already differ between dataset families (`fund` vs `fundCode`). Mitigations: pinned milestone snapshot ids; content-type validation (malformed routes return SPA HTML with HTTP 200); official bulk XLSX extracts as fallback.
- 2025 values are early-cycle and will change in later milestone revisions; label 2025 partial.
- Some filers report in round thousands (Sound Transit, King County) - source data, not an artifact.
- Basis mixing: GAAP vs cash filers (acctBasisTypeId), calendar vs school fiscal years - never compare across bases without labeling.

## Decision

```text
accept-snapshot
```

Next artifact:

```text
source card washington.fit_filed_actuals, snapshot data, validator, drift check, router/skill
routes, benchmark expectation ratchet (walla-walla, spokane, evergreen, sound-transit,
kc-actuals-trap, sps cases)
```
