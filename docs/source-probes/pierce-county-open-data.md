# Source Probe Brief: Pierce County Open Data (Open Budget + Open Checkbook)

Status: accepted (probed live 2026-07-13)

## Question

What civic-budget or public-finance question should this source help Civic Agent answer?

```text
How big is Pierce County's budget and what do they spend it on?
```

## Source Identity

- Jurisdiction: Pierce County, Washington (second-largest WA county, ~959,900 residents per OFM April 1, 2025)
- Budget family: operating (budget dataset) and spending/checkbook (checkbook dataset)
- Official owner: Pierce County Finance / Budget offices
- Public inspection URL: `https://open.piercecountywa.gov/`
- Candidate machine URL: `https://open.piercecountywa.gov/resource/w2wc-2pqu.json`, `https://open.piercecountywa.gov/resource/iwu2-biyj.json`
- Source type: open-data
- Source priority: high - cheapest fourth jurisdiction (identical Socrata/SODA stack to Seattle) and the first local-government transaction-grain actuals source

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
| Open Budget Expenditure Data | Pierce County | `https://open.piercecountywa.gov/resource/w2wc-2pqu` | Socrata dataset | Biennial budget AND budget-line actuals, FY2016-17 through 2026-27 |
| Open Checkbook Data | Pierce County | `https://open.piercecountywa.gov/resource/iwu2-biyj` | Socrata dataset | Transaction-level ledger actuals, FY2017 through partial FY2026 |
| Budget office pages | Pierce County | `https://www.piercecountywa.gov/126/Budget` | document | Adopted biennial budget books (PDF); context only |

## Surface Classification

Access candidates:

- [x] Official documented API
- [x] Official open data portal
- [ ] Official bulk download
- [ ] Official public dashboard
- [x] Official document/PDF
- [ ] HTML scrape only
- [ ] Unofficial mirror/context source
- [ ] Not usable

Probe methods attempted:

- [x] Socrata/open data probe
- [x] Official API probe

Evidence:

```text
GET /resource/w2wc-2pqu.json?$limit=2 -> rows with fiscal_year "2016-2017" biennium labels,
  whitespace-padded text dimensions, misspelled exependiture_category field, budget + actual measures.
GET /api/views/w2wc-2pqu.json -> name "Open Budget Expenditure Data", rowsUpdatedAt 2026-06-13,
  columns: fiscal_year, department, division, fund, program, activity, expenditure_type,
  exependiture_category (text), actual, budget (number).
GET grouped by fiscal_year -> six biennia 2016-2017..2026-2027; 2026-2027: budget 3,500,588,070 /
  actual 491,632,289.3 (in progress) / 10,362 rows. Matches the county's published $3.5B 2026-27 budget.
GET /api/views/iwu2-biyj.json -> "Open Checkbook Data", rowsUpdatedAt 2026-06-22, columns incl.
  fiscal_year, fiscal_period, accounting_date, company, division, fund, service,
  spend_category_as_worktag, payee_for_transaction, ledger_budget_debit_minus.
GET grouped by fiscal_year -> FY2017-FY2026; FY2025 (closed): 974,830,912.90 / 109,954 rows;
  FY2026 partial: 363,935,403.20 / 48,499 rows, max(accounting_date)=2026-05-29.
Sample rows show company as department-level dimension and generic payees like
  "Banking Services Vendor".
```

Primary access surface:

```text
Socrata (SODA API, no auth for modest volumes)
```

Primary source identifiers:

```text
open.piercecountywa.gov; dataset ids w2wc-2pqu (budget), iwu2-biyj (checkbook)
```

Companion surfaces:

```text
Pierce County budget office PDF budget books (context only); SAO FIT filed actuals (separate source family)
```

## Data Model

Fields and dimensions:

| Field | Type | Meaning | Notes |
|---|---|---|---|
| fiscal_year (budget) | text | biennium label, e.g. 2026-2027 | NOT a number; six biennia |
| department/division/fund/program/activity/expenditure_type/exependiture_category | text | budget hierarchy | whitespace-padded; category field misspelled officially |
| fiscal_year (checkbook) | number | annual fiscal year | 2017-2026 |
| fiscal_period / accounting_date | number / date | period within year | FY2026 partial through 2026-05-29 |
| company/division/fund/service/spend_category_as_worktag/payee_for_transaction | text | checkbook hierarchy | company = department level; some payees generic |

Measures:

| Measure | Meaning | Budgeted or actual? | Notes |
|---|---|---|---|
| budget | biennial budgeted expenditure authority | budgeted | never present as annual |
| actual (budget dataset) | budget-line-grain expenditure actuals | actual | partial for in-progress biennium |
| ledger_budget_debit_minus | transaction ledger amount | actual | debits minus credits; negatives are credits/reversals |

Time/version fields:

```text
Budget: biennium labels 2016-2017 .. 2026-2027. Checkbook: fiscal_year 2017-2026,
accounting_date through 2026-05-29 (observed 2026-07-13).
```

Freshness and publication metadata:

```text
Socrata rowsUpdatedAt: budget 2026-06-13, checkbook 2026-06-22. Checkbook appears to update
roughly monthly; budget per biennium/supplemental.
```

Hierarchy:

```text
Budget: department -> division -> fund -> program -> activity -> expenditure_type -> category.
Checkbook: company -> division -> fund -> service -> spend_category -> payee.
```

## Extraction Approach

Recommended access method:

```text
accept-live
```

Why:

```text
Documented Socrata SODA API identical to the accepted Seattle pattern; aggregates are cheap
at answer time; no snapshot needed while the portal stays reliable.
```

If live:

- Endpoint: the two JSON endpoints above
- Query parameters: $select/$where/$group/$order SoQL
- Rate/freshness caveats: unauthenticated SODA throttling applies at high volume; per-answer aggregates are far below it
- Validation query: grouped totals per biennium / fiscal year compared to card validation checks

## Storage Policy

Recommended storage tier:

```text
live
```

Why:

```text
Same rationale as seattle.operating_budget: official API, cheap aggregates, validation
checks pin known totals, nightly drift check watches for restatement.
```

Normal answer source:

```text
official API
```

Freshness check:

```text
API metadata (rowsUpdatedAt) plus scripts/drift.py fingerprints on a CLOSED period
(2026-2027 budget total; FY2025 checkbook total) so routine current-period growth
is not treated as drift.
```

Repo artifacts:

```text
source card, probe, tests, docs
```

Local or hosted artifacts:

```text
none
```

Partial-period data-through rule:

```text
Checkbook FY2026 is partial; answers must state the max(accounting_date) boundary
(2026-05-29 as probed). Budget 2026-2027 actual column is partial until the biennium closes.
```

## Supported Questions

- How big is Pierce County's 2026-2027 budget, and how does it break down by department?
- How has the county's biennial budget changed since 2016-2017?
- Did Pierce County spend what it budgeted in 2024-2025 (within-source budget-vs-actual)?
- Who did Pierce County pay in 2025, by department, fund, category, or payee?

## Unsupported Claims

- Revenue budgets or actual revenue collected (no accepted revenue source).
- Staffing, FTE, payroll, headcount.
- Annual budget totals (budget data is biennial).
- Contract terms or procurement documents.

## Validation Checks

| Check | Expected result | How to reproduce |
|---|---:|---|
| 2026-2027 budget total | 3,500,588,070 | SoQL sum(budget) where fiscal_year="2026-2027" |
| 2026-2027 rows / departments / funds | 10,362 / 26 / 105 | SoQL count + count(distinct) |
| FY2025 checkbook total | 974,830,912.90 | SoQL sum(ledger_budget_debit_minus) where fiscal_year=2025 |
| FY2025 checkbook rows / companies / funds | 109,954 / 27 / 87 | SoQL count + count(distinct) |
| FY2026 checkbook data-through | 2026-05-29 | SoQL max(accounting_date) where fiscal_year=2026 |

## Source Fingerprint

Citation fields:

```text
open.piercecountywa.gov; pierce_county.open_budget (w2wc-2pqu); pierce_county.open_checkbook
(iwu2-biyj); biennium labels; FY2026 data-through 2026-05-29.
```

Retrieval fields:

```text
JSON/CSV/metadata endpoints per card; SoQL filters as in the jurisdiction skill recipes.
```

Integrity fields:

```text
rowsUpdatedAt values; closed-period totals and row counts above.
```

Spot-check candidates:

```text
2026-2027 budget total vs the county's published $3.5B biennial budget; FY2025 closed-year total.
```

## Worked Answer Trace

Question:

```text
How big is Pierce County's budget?
```

Trace:

```text
Source: pierce_county.open_budget (Open Budget Expenditure Data, Socrata w2wc-2pqu)
Access method: socrata (live)
Storage policy: live / official API at answer time
Snapshot/version: n/a (live); rowsUpdatedAt 2026-06-13
Grain: biennium
Measure: sum(budget)
Filters/query logic: fiscal_year="2026-2027"
Validation: $3,500,588,070 over 10,362 rows (verified 2026-07-13); matches the county's published $3.5B 2026-27 budget
Caveats: biennial budgeted expenditure authority, not annual, not actual spending; expenditure side only
```

## Risks

- Portal or dataset retirement/re-keying (live tier has no insulation); the nightly drift check watches closed-period fingerprints.
- Whitespace-padded dimensions and the misspelled category field will break naive queries; recipes encode the workarounds.
- Checkbook payee names are partially generic; payee rankings must carry the caveat.
- Budget dataset is expenditure-only; resident revenue questions stay unsupported until a revenue source is probed.

## Decision

Decision:

```text
accept-live
```

Next artifact:

```text
source cards (pierce_county.open_budget, pierce_county.open_checkbook), jurisdiction skill,
router routes, drift checks, benchmark expectation ratchet for pierce-county-budget-size and
pierce-vs-king-per-resident
```
