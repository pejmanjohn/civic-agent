# Seattle Open Data Portal Source Probe

Status: probe complete, workflow input

Date: 2026-06-04

## Question

How should Civic Agent handle Socrata-style civic open data portals such as Seattle Open Data?

## Initial Answer

Seattle Open Data is an official City of Seattle Socrata/Data & Insights portal. It should be treated as a catalog plus per-dataset API host.

For Civic Agent, the portal itself is not the source contract. A source card should point to one canonical dataset id, with the portal catalog and official Seattle Open Data pages recorded as companion inspection surfaces.

## Source Identity

- Jurisdiction: Seattle
- Source family: open data portal
- Official owner: City of Seattle / Seattle Information Technology Open Data Program
- Public inspection URL: `https://data.seattle.gov/`
- Official context URL: `https://www.seattle.gov/tech/reports-and-data/open-data/about-the-open-data-program`
- Platform: Socrata / Tyler Data & Insights
- Recommended access: `accept-live` for stable tabular datasets; `accept-snapshot` when a dataset is large, fast-changing, or needs repeatable historical extracts.

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
| Seattle Open Data portal | City of Seattle | `https://data.seattle.gov/` | Socrata portal | Official catalog and primary data access surface. |
| Seattle Open Data program | Seattle IT | `https://www.seattle.gov/tech/reports-and-data/open-data/about-the-open-data-program` | official context | Explains the City's open data program and "beyond tabular" strategy. |
| City of Seattle Operating Budget | City of Seattle / Budget Office | `https://data.seattle.gov/City-Administration/City-of-Seattle-Operating-Budget/8u2j-imqx` | Socrata dataset | Existing Civic Agent Seattle operating budget source. |
| Socrata API docs for budget dataset | Socrata / Tyler | `https://dev.socrata.com/foundry/data.seattle.gov/8u2j-imqx` | API docs | Dataset-specific API docs path; discoverable from the dataset id. |

## Portal Organization

The portal can be probed through the Socrata catalog API:

```text
https://api.us.socrata.com/api/catalog/v1?domains=data.seattle.gov&search_context=data.seattle.gov&q=<term>&limit=10
```

Observed broad portal probe:

```json
{
  "resultSetSize": 1004,
  "domain": "data.seattle.gov"
}
```

Observed search for `operating budget`:

| Candidate dataset | Dataset id | Type | Category | Owner | Why it matters |
|---|---|---|---|---|---|
| City of Seattle Operating Budget | `8u2j-imqx` | dataset | City Administration | Nicole Evans | Canonical Seattle operating budget source. |
| Current City Properties | `qhwj-ipk4` | dataset | City Administration | Bond, Alysoun | Related by text search, but not a budget source. |

Observed search for `budget` returned six candidates, including:

- `8u2j-imqx`: City of Seattle Operating Budget
- `m6va-m4qe`: City of Seattle Capital Budget
- `bsgq-948x`: Open Budget - Capital Projects Details
- `uxxb-mmuq`: Seattle Rescue Plan

This is why Socrata probes need catalog discovery plus source selection. Portal search is useful, but it is not enough to decide source fit.

## Surface Classification

Access candidates:

- [x] Official open data portal
- [x] Official documented API
- [x] Official bulk CSV export
- [ ] Official public dashboard
- [ ] Official document/PDF
- [ ] HTML scrape only
- [ ] Not usable

Probe methods used:

- Generic HTML/header probe
- Socrata/open data catalog probe
- Dataset metadata probe
- SoQL validation probe
- Bulk CSV export probe
- SODA 3 query probe

Primary access surface:

```text
Socrata dataset API
```

Primary source identifiers:

```text
domain: data.seattle.gov
dataset id: 8u2j-imqx
resource endpoint: https://data.seattle.gov/resource/8u2j-imqx.json
metadata endpoint: https://data.seattle.gov/api/views/8u2j-imqx
SODA 3 endpoint: https://data.seattle.gov/api/v3/views/8u2j-imqx/query.json
CSV export: https://data.seattle.gov/api/views/8u2j-imqx/rows.csv?accessType=DOWNLOAD
```

Companion surfaces:

```text
Seattle Open Data program page, dataset human inspection page, Socrata API docs, Open Budget site if relevant to the user-facing budget workflow.
```

## Data Model Example: Operating Budget

Dataset metadata observed from `/api/views/8u2j-imqx`:

```json
{
  "id": "8u2j-imqx",
  "name": "City of Seattle Operating Budget",
  "assetType": "dataset",
  "viewType": "tabular",
  "displayType": "table",
  "publicationStage": "published",
  "provenance": "official",
  "attribution": "City of Seattle",
  "category": "City Administration",
  "license": "Public Domain"
}
```

Fields:

| Display label | API field name | Type |
|---|---|---|
| Fiscal Year | `fiscal_year` | number |
| Service | `service` | text |
| Department | `department` | text |
| Program | `program` | text |
| Fund | `fund` | text |
| Fund Type | `fund_type` | text |
| Expense Type | `expense_type` | text |
| Description | `description` | text |
| Approved Amount | `approved_amount` | number |

Freshness and publication metadata:

```text
catalog updatedAt: 2026-03-04T22:47:25Z
rowsUpdatedAt: 2026-03-04T22:47:25Z
viewLastModified: 2026-03-04T22:47:21Z
publicationDate: 2022-09-22T01:17:16Z
custom Department: Budget Office
custom Contact Email: open.data@seattle.gov
custom Refresh Frequency: One Time
```

## Validation Checks

| Check | Observed result | How to reproduce |
|---|---:|---|
| Total rows and fiscal-year range | 35,891 rows, FY2018-FY2026 | SoQL count/min/max query on `/resource/8u2j-imqx.json` |
| FY2026 top department by approved amount | Seattle City Light, about 1.295B | SoQL group-by department with `fiscal_year=2026` |
| API docs path | Dataset docs available by id pattern | `https://dev.socrata.com/foundry/data.seattle.gov/8u2j-imqx` |
| CSV export | GET returns display-label headers | `/api/views/8u2j-imqx/rows.csv?accessType=DOWNLOAD` |

Representative SoQL validation:

```text
https://data.seattle.gov/resource/8u2j-imqx.json?$select=count(*) as rows, max(fiscal_year) as max_fy, min(fiscal_year) as min_fy&$limit=1
```

Observed result:

```json
[
  {
    "rows": "35891",
    "max_fy": "2026",
    "min_fy": "2018"
  }
]
```

## Workflow Lessons

- Add a Socrata portal-discovery step before dataset validation.
- Use catalog API parameter `q`, not `search`, for text search.
- Treat broad portal search results as candidates, not accepted sources.
- Prefer `fieldName` values from `/api/views/<id>` for queries.
- Keep display labels only for human-facing output and CSV export notes.
- Record `assetType`, `viewType`, `publicationStage`, `provenance`, catalog visibility, owner, attribution, license, tags, update times, and custom fields.
- Use `GET` probes for row endpoints; `HEAD` can be misleading on Socrata row/export URLs.
- Ignore computed georegion fields unless the question needs geography.
- Record whether the source card uses SODA 2.1 `/resource/<id>.json` or SODA 3 `/api/v3/views/<id>/query.json`.
- Full extracts need stable paging and normalization because SODA often returns numeric values as strings.

## Decision

Decision:

```text
accept-live
```

Next artifact:

```text
No new Seattle source card needed for the operating budget dataset. Use this probe to improve the general source-probing workflow for Socrata-style open data portals.
```
