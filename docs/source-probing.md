# Source Probing Workflow

Use this workflow when evaluating a potential new Civic Agent budget or public-finance source.

The goal is not to build an adapter immediately. The goal is to prove what the official source can answer, how it can be extracted, what validation checks make it trustworthy, and whether it belongs in Civic Agent at all.

This workflow borrows the useful parts of CLI Printing Press source discovery: raw capture over summaries, complementary discovery methods, explicit source priority, provenance artifacts, and behavioral verification before declaring a source usable. It intentionally does not borrow the CLI-generation parts: feature absorption, command generation, MCP surfaces, or broad contributor automation.

Reference inspiration: `https://github.com/mvanhorn/cli-printing-press`

## Output

A completed probe should leave a small public artifact:

```text
docs/source-probes/<jurisdiction-or-source>.md
```

Use `docs/templates/source-probe-brief.md` as the starting shape.

If the source is accepted, the next implementation step is source-specific:

- Clean official API: add a source card and query recipes.
- Official file download: add a source card, normalizer, validation checks, and a reviewed snapshot if needed.
- Official public dashboard: add a source card, reviewed query/capture templates, normalized snapshot, summary, and provenance.
- PDF/document-only source: usually keep as context or a citation source until the extraction need is narrow and validated.

Every accepted source must also choose a storage tier from `docs/source-data-storage.md`. The tier explains where normal answer data lives: live official source, checked-in snapshot, managed local database, hosted artifact, context-only, watchlist, or reject.

## Source Type Matrix

Run the matrix before getting deep into any one extraction path. Power BI is one possible branch, not the default assumption.

| Source type | Common signals | Preferred access | Probe goal | First artifact if accepted |
|---|---|---|---|---|
| Official documented API | API docs, JSON endpoints, auth/rate notes, examples | `accept-live` | Prove stable query parameters, fields, paging, freshness, and one validation query. | Source card plus query recipes. |
| Open data portal | Socrata, CKAN, ArcGIS REST, data catalog dataset ids | `accept-live` or `accept-snapshot` | Discover candidate assets, then validate one canonical dataset id, API field names, row counts, update times, and official owner. | Source card plus live query or snapshot normalizer. |
| Bulk file download | CSV, XLSX, ZIP, XML, JSON, fixed public file URL | `accept-snapshot` | Prove file stability, headers, sample rows, checksum/size, and refresh cadence. | Source card plus parser, normalized snapshot, and provenance. |
| Public BI dashboard | Power BI, Tableau, Looker, ArcGIS Dashboard, embedded iframe | `accept-snapshot` | Prove the dashboard is official, inspectable, refreshable, and queryable or capturable without relying on fragile UI scraping. | Source card plus capture/query templates and normalized snapshot. |
| Document source | PDF, budget book, ordinance, adopted budget document | `accept-context-only` or `accept-snapshot` | Identify whether the document supplies citations/context or a narrow extractable table. | Source note, citation workflow, or narrow parser. |
| HTML tables/pages | Static tables, server-rendered pages, no API/download | `watchlist` or `accept-snapshot` | Prove official ownership, table stability, headers, and a validation total. | Source card plus narrow scraper only if better options do not exist. |
| Unofficial mirror | Third-party API, civic project, media graphic | `reject` or context only | Check whether it points back to an official source. | Usually none. |

## Storage Tier Matrix

Run the storage tier matrix after the source type is understood. Source type describes how to reach official data; storage tier describes where normal Civic Agent answers should read from.

| Storage tier | Use when | Normal answer source | Example |
|---|---|---|---|
| `live` | Official source is fast, structured, stable, and cheaply validated at answer time. | Official API or official query endpoint. | Seattle Socrata operating budget. |
| `checked_in_snapshot` | Normalized data is compact, slow-changing, and useful in git for tests and default answers. | Checked-in normalized rows plus summary and provenance. | King County dashboard, Washington operating budget, Washington revenue. |
| `managed_local_db` | Source data is official but too large, detailed, slow, or awkward for git and repeated answer-time parsing. | Local database under Civic Agent's data cache. | Washington Open Checkbook full vendor-payment history. |
| `hosted_artifact` | Repeated local rebuild cost, bandwidth, or validation burden justifies central publishing. | Hosted artifact or service, cached locally when useful. | Future scale tier. |
| `context_only` | Source is useful for citations or explanation but not accepted for normal answers. | Human inspection or citation only. | Budget documents without narrow extraction. |
| `watchlist` | Source might become useful but access, semantics, or validation are not acceptable yet. | None. | Unstable dashboards. |
| `reject` | Source is unofficial, misleading, unreproducible, or outside scope. | None. | Unofficial mirrors without official backing. |

## Principles

1. Official source first.

   Identify the office of record and the public page a reader can inspect. A clean API from a non-official site is weaker than an awkward official source.

2. Source capability before jurisdiction coverage.

   One source can support a narrow set of questions. Do not imply that a whole jurisdiction is covered because one dataset is useful.

3. Raw capture before summarized browsing.

   Preserve exact dataset ids, field names, dashboard report ids, refresh timestamps, file URLs, row counts, and validation totals. Use summaries for orientation, not source contracts.

4. Extraction path is part of the source contract.

   A source is not "good" until the agent can describe whether it is a live API, bulk file, public dashboard snapshot, document parser, or reject/watchlist source.

5. Validated answers beat source inventory.

   A source is accepted only when at least one useful answer pattern can be backed by a validation check: row count, official total, dashboard cross-check, file checksum, model refresh time, or comparable evidence.

6. Snapshots are normal for report-shaped sources.

   If the official source is slow-changing and awkward to query live, prefer a checked-in normalized snapshot with provenance over a fragile live-only answer path.

7. Checked-in snapshots and managed local databases solve different problems.

   Use checked-in snapshots when normalized data is compact enough to review and keep in git. Use a managed local database when full-detail data is too large or slow for git but still needs fast repeated local analysis. Do not commit raw historical bulk files or local databases unless a payload is deliberately reviewed and small enough to justify repository storage.

8. One source can have multiple official surfaces.

   If a jurisdiction splits the same budget family across current, prior, yearly, or biennial report pages, keep one logical source id when the provider, measures, caveats, and answer contract are the same. Model each official page/report/file as a `source_surface`, normalize rows into shared tables, and include a row-level `source_surface_id`.

## Split Time-Span Sources

Many civic sources are not one neat API. A current dashboard may cover the active budget while a prior-years dashboard, yearly CSV series, or archived report covers older periods. Treat this as a normal source shape, not as an exception.

Use this pattern when the surfaces represent the same official source family and can answer one user-facing trend question:

```text
source_id: washington.operating_budget
source_surfaces:
  current_biennial_summary_powerbi:
    status: accepted
    coverage: current enacted biennium
  prior_summary_powerbi:
    status: accepted
    coverage: prior enacted biennia
  older_reportviewer:
    status: candidate_context_only
    coverage: possible older history, not normalized yet
normalized tables:
  historical-biennium-summary.jsonl
  historical-agency-by-biennium.jsonl
  historical-functional-area-by-biennium.jsonl
row fields:
  source_surface_id
  period fields
  semantic filter fields
  official dimension code and label
  amount fields
```

Acceptance rules:

- Keep one source id only when the normalized row contract is coherent: same measure, compatible period grain, compatible budget state, and shared caveats.
- Declare every official surface in the source card with a status: `accepted`, `candidate_context_only`, `context_only`, or `rejected`.
- Add semantic filter fields such as `budget_state`, `revision_scope`, `session_type`, `budget_version`, `fund_view`, and `period_type`; do not bury those assumptions in prose only.
- Prefer official codes plus labels for dimensions. Labels alone are brittle across historical periods.
- Use `source_surface_id` on every row so answers can cite which official surface supplied each segment.
- Reconcile overlaps when two surfaces cover the same period. If current 2025-27 appears in both a current report and a prior-years report, the totals must match before either surface is accepted for the stitched trend.
- Reconcile grouped totals to the statewide or parent total for every period. If agency or functional-area rows do not sum to the statewide trend, leave that grain unsupported.
- Keep non-reconciled official surfaces visible as context or candidates instead of silently mixing them into normal answers.

When a source is split by year with separate CSV/XLSX files, use the same shape: one source card, one `source_surfaces` entry per file or file family, shared normalized historical tables, row-level provenance, checksums/file metadata for each accepted file, and period-by-period reconciliation checks.

9. Coverage categories are promoted only after probes.

   `docs/coverage-taxonomy.md` carries the full civic coverage map and the currently active source-card categories. A backlog category such as demographics, crime, transportation, housing, procurement, health, service requests, governance, or elections should not appear in `coverage_claims` until this workflow proves what an official source can answer or explicitly cannot answer.

## Workflow

### 1. State The User Question

Write the concrete question the source should help answer.

Good:

```text
Can Civic Agent answer Washington state operating budget questions by agency, fund, program, item, fiscal year, and budget version?
```

Weak:

```text
Add Washington.
```

Record:

- Jurisdiction
- Budget family: operating, capital, transportation, revenue, spending/checkbook, staffing, K-12, grants, debt, procurement
- Coverage target from `docs/coverage-taxonomy.md`: active category for current budget/public-finance work, or backlog family if the source is being investigated for future coverage.
- Desired grain: agency, department, program, fund, project, vendor, fiscal year, biennium, version
- Desired measure: budgeted amount, actual spending, revenue, FTE, contract amount, project appropriation
- Candidate storage tier from `docs/source-data-storage.md`, if already obvious.

### 2. Build The Official Source Inventory

Start from the user-provided URL, then inventory official adjacent sources.

Check:

- Main budget office or finance office
- Open data portal
- Legislative budget office or council data page
- Official dashboard pages
- Download links
- Enacted budget documents, budget books, schedules, LEAP-like documents
- Revenue, spending, staffing, and capital-specific pages

For each candidate, record:

```text
source_name:
official_owner:
url:
source_type: portal | open-data | dashboard | download | document | mixed
budget_family:
human_inspection_url:
machine_access_candidate:
notes:
```

Source priority matters. If the portal page and a dashboard point at the same data family, record which is the public inspection page and which is the machine extraction surface.

### 3. Classify The Surface

Use fast probes before deciding how to integrate.

Start broad, then follow the matching branch from the source type matrix. Record negative findings too, such as "no API docs found" or "download link changes by session"; those findings explain why a source became a snapshot or watchlist candidate.

#### Generic HTML Probe

```bash
curl -sL '<url>' | rg -n 'iframe|powerbi|tableau|socrata|data\\.wa|csv|xlsx|download|api|json|arcgis|pdf|budget|spending'
curl -sIL '<url>'
```

Look for:

- `data-*` catalog links
- Socrata dataset pages or `/resource/<id>.json`
- CKAN package APIs
- ArcGIS REST service URLs
- Power BI `app.powerbi.com/view?r=...`
- Tableau embeds
- CSV/XLSX download links
- JavaScript calls to API endpoints
- PDF-only pages

#### Official API Probe

For documented JSON/REST APIs:

```bash
curl -sS '<api-doc-or-endpoint-url>' | jq
curl -sS -I '<api-endpoint-url>'
```

Record:

- Base URL and documentation URL
- Required parameters
- Pagination shape
- Sort/filter fields
- Date or fiscal-year filters
- Update or cache headers
- Rate limits and auth requirements
- Error behavior for invalid filters

Reject or snapshot if the API is unofficial, requires non-public credentials, lacks stable filters for the needed grain, or returns UI-only denormalized fragments that cannot be validated.

#### Socrata/Open Data Probe

Socrata-style portals need two stages: portal discovery and dataset validation. Treat the portal URL as a catalog, not as the source contract by itself.

Signals:

- Response headers such as `X-Socrata-Region`
- Dataset URLs ending in an eight-character id such as `8u2j-imqx`
- API URLs shaped like `/resource/<id>.json`, `/api/views/<id>`, or `/api/v3/views/<id>/query.json`
- API docs at `https://dev.socrata.com/foundry/<domain>/<id>`

Portal discovery:

```bash
curl -sS 'https://api.us.socrata.com/api/catalog/v1?domains=<domain>&search_context=<domain>&q=<search-term>&limit=10' | \
  jq '{resultSetSize, results: [.results[] | {name: .resource.name, id: .resource.id, type: .resource.type, link: .link, permalink: .permalink, updatedAt: .resource.updatedAt, category: .classification.domain_category, tags: .classification.domain_tags, owner: .owner.display_name, columns: (.resource.columns_field_name // [])}]}'
```

Use `q`, not `search`, for the catalog text query. Record zero-result searches too, because a failed query can explain why the agent used a different discovery path.

For Socrata-like sources:

```bash
curl -sS '<metadata-url>' | jq '{id: .id, name: .name, columns: [.columns[] | {name, fieldName, dataTypeName}], rowsUpdatedAt: .rowsUpdatedAt}'
curl -sS --get '<resource-json-url>' \
  --data-urlencode '$select=count(*) as rows' \
  --data-urlencode '$limit=1'
```

Use API field names, not display labels.

Dataset validation:

```bash
curl -sS 'https://<domain>/api/views/<dataset-id>' | \
  jq '{id, name, assetType, viewType, displayType, publicationStage, provenance, hideFromCatalog, hideFromDataJson, attribution, owner: .owner.displayName, tableAuthor: .tableAuthor.displayName, license, category, tags, rowsUpdatedAt, viewLastModified, metadata: .metadata.custom_fields, columns: [.columns[] | {name, fieldName, dataTypeName, flags}]}'

curl -sS --get 'https://<domain>/resource/<dataset-id>.json' \
  --data-urlencode '$select=count(*) as rows' \
  --data-urlencode '$limit=1' | jq

curl -sS --get 'https://<domain>/resource/<dataset-id>.json' \
  --data-urlencode '$limit=1' | jq
```

SODA 3 probe, when available:

```bash
curl -sS --get 'https://<domain>/api/v3/views/<dataset-id>/query.json' \
  --data-urlencode 'pageNumber=1' \
  --data-urlencode 'pageSize=1' | jq
```

Bulk export probe:

```bash
curl -sS 'https://<domain>/api/views/<dataset-id>/rows.csv?accessType=DOWNLOAD' | head -5
curl -sS 'https://<domain>/resource/<dataset-id>.csv?$limit=1' | head -5
```

Use `GET` probes for Socrata row endpoints. Some Socrata endpoints can answer `GET` correctly while `HEAD` returns misleading 404-style responses.

Record:

- Portal domain
- Dataset id
- Human dataset URL and short permalink
- API docs URL
- Asset type, view type, display type, and publication stage
- Public grants/rights, provenance, and catalog visibility flags
- Attribution, owner, table author, department/contact custom fields, license, category, and tags
- `rowsUpdatedAt`, `viewLastModified`, and refresh-frequency custom fields
- API field names, display labels, data types, and system/computed fields
- Row count and at least one source-specific validation aggregate

Prefer a published, public, official, tabular dataset as the canonical source. Treat filtered views, derived views, maps, charts, and stories as companion surfaces unless they are the only official source that answers the question.

Common Socrata pitfalls:

- Portal search can return related but irrelevant datasets. Confirm the source by name, owner/attribution, fields, tags, and validation totals.
- Display labels are not query fields. Query `fieldName` values such as `fiscal_year`, not labels such as `Fiscal Year`.
- Computed region columns like `:@computed_region_*` are usually not part of budget analysis unless the question is geographic.
- SODA responses often return numbers and dates as strings; normalize types before arithmetic.
- Full extracts need stable paging, usually with an explicit order. Do not assume the default response limit contains the full dataset.
- SODA 2.1 `/resource/<id>.json` and SODA 3 `/api/v3/views/<id>/query.json` can both exist. Record which one the source card uses and whether an app token is required or recommended.

#### CKAN Probe

For CKAN-like catalogs:

```bash
curl -sS '<ckan-base>/api/3/action/package_show?id=<package-id>' | jq
curl -sS '<resource-url>' -I
```

Record package id, resource ids, formats, last-modified fields, organization, and whether the resource is a live datastore API or a file download.

#### ArcGIS Probe

For ArcGIS REST services:

```bash
curl -sS '<service-url>?f=json' | jq '{name, type, fields, maxRecordCount, capabilities}'
curl -sS --get '<layer-url>/query' \
  --data-urlencode 'f=json' \
  --data-urlencode 'where=1=1' \
  --data-urlencode 'returnCountOnly=true'
```

Record service URL, layer ids, fields, geometry needs, record limit, count endpoint, and whether budget measures are attributes or buried in popups.

#### File Download Probe

```bash
curl -sIL '<download-url>'
```

Record content type, size, last-modified, and whether the URL is stable.

For XLSX/CSV, inspect headers and sample rows locally. Prefer structured parsers over ad hoc text parsing.

#### Dashboard Probe

For dashboards, first identify the product and the official inspection page:

```bash
curl -sL '<dashboard-page-url>' | rg -n 'powerbi|tableau|looker|arcgis|iframe|embed|workbook|reportId|dashboard'
```

Record:

- Dashboard product
- Public inspection URL
- Embed URL
- Owner shown on the official page
- Refresh timestamp if shown
- Export/download options
- Whether network metadata exposes fields and measures
- Whether the dashboard can support a reproducible query or only visual inspection

Use a source-specific dashboard probe after that. If the only possible path is browser-clicking visual elements with no stable data capture, keep the source as context or watchlist unless the source is uniquely important and the extract is narrow.

##### Power BI

For `app.powerbi.com/view?r=<base64url>`:

1. Decode the `r` parameter.

   ```bash
   node -e 'console.log(Buffer.from(process.argv[1], "base64url").toString())' '<r-param>'
   ```

   Record:

   - `k`: report resource key
   - `t`: tenant id
   - `c`: config/version hint

2. Open the embed HTML and locate the resolved cluster.

   ```bash
   curl -sL 'https://app.powerbi.com/view?r=<r-param>' | rg -n 'resolvedClusterUri|FixedClusterUri|modelsAndExploration|conceptualschema|querydata'
   ```

3. Fetch metadata.

   ```bash
   curl --compressed -sS \
     -H 'Accept: application/json' \
     -H 'X-PowerBI-ResourceKey: <resource-key>' \
     '<cluster-api>/public/reports/<resource-key>/modelsAndExploration?preferReadOnlySession=true' | jq
   ```

4. Fetch the conceptual schema.

   ```bash
   curl --compressed -sS \
     -H 'Accept: application/json' \
     -H 'X-PowerBI-ResourceKey: <resource-key>' \
     '<cluster-api>/public/reports/<resource-key>/conceptualschema' | jq
   ```

5. Inspect entities, fields, measures, model id, dataset id, and refresh time.

6. Replay one small `querydata` POST only after identifying the model id, dataset id, and a safe aggregate. The goal is not full extraction yet. The goal is to prove that the public report can be queried and that the response shape is parseable.

Treat Power BI public report endpoints as undocumented report internals. If accepted, use a source-specific snapshot extractor with reviewed query templates, not an open-ended live adapter.

##### Tableau

For Tableau public embeds:

```bash
curl -sL '<tableau-page-url>' | rg -n 'tableau|vizql|workbook|sheet|showVizHome|bootstrapSession'
```

Record workbook/view ids, sheet names, parameters, filters, download options, and whether a CSV export is exposed for the relevant sheet. Prefer official export endpoints or a reviewed browser/network capture over scraping rendered marks.

##### Looker, ArcGIS Dashboard, And Other Dashboards

Record product-specific ids, visible field labels, filters, downloads, and refresh metadata. If there is no documented or repeatable data access path, classify the dashboard as `accept-context-only` or `watchlist` until a narrow, validated extraction path exists.

#### Document/PDF Probe

For document-heavy budget sources:

```bash
curl -sIL '<document-url>'
```

Record document URL, title, fiscal period, adoption/proposal status, file size, last-modified date, page count if known, and whether the document contains extractable tables or only narrative/legal text.

Use documents for citations and context by default. Promote them to `accept-snapshot` only when the needed table is narrow, stable, and has a validation total.

#### HTML Table Probe

For official HTML tables with no better source:

```bash
curl -sL '<url>' | rg -n '<table|<th|<td|data-|json|api|download'
```

Record table headers, row count, whether the table is server-rendered or JavaScript-populated, and any official totals on the page. Prefer a narrow snapshot scraper over live scraping unless the page is stable and cheap to validate.

### 4. Map Capabilities

Build a compact capability map:

```text
fields:
measures:
time fields:
budget versions:
hierarchies:
supported grains:
known filters:
refresh/freshness:
```

Separate budgeted/authorized values from actual spending. Separate operating, capital, transportation, and staffing if the source does.

### 5. Define Safe And Unsafe Questions

Translate source capabilities into answer boundaries.

Safe patterns:

- Annual budget totals by year.
- Department rankings for a specific fiscal year.
- Agency/fund/program drill-downs.
- Budgeted FTE trend if FTE exists in the source.
- Vendor payments if the source is actual-spending/checkbook data.

Unsupported claims:

- Actual spending from a budget-only source.
- Service quality or outcomes from budget rows alone.
- Employee rosters from budgeted FTE.
- Cross-jurisdiction comparisons before accounting definitions are normalized.
- Whole-jurisdiction coverage when only one budget family has been reviewed.

### 6. Choose The Access Method

Use this preference order:

1. `socrata` or other official documented API
2. `official_bulk_download`
3. `official_dashboard_snapshot`
4. `official_document_extract`
5. `html_scrape`
6. `watchlist_or_reject`

Prefer `official_dashboard_snapshot` for report-shaped Power BI/Tableau sources unless the provider documents a stable API. The snapshot should carry query templates, normalized rows, summary checks, and provenance.

### 6a. Choose The Storage Tier

Choose the storage tier separately from access method:

```text
live | checked_in_snapshot | managed_local_db | hosted_artifact | context_only | watchlist | reject
```

Record:

- Normal answer source: official API, repo snapshot, local DB, hosted artifact, or none.
- Freshness check: API metadata, source file metadata, model refresh, report timestamp, manual snapshot version, or custom probe.
- Repo artifacts: source card, probe, normalized snapshot, summary, provenance, fixtures, tests, docs.
- Local artifacts: raw source files, local database, manifest, debug captures.
- Data-through rule for partial current-period data.

Use `checked_in_snapshot` for compact reviewed normalized data. Use `managed_local_db` when official full-detail data is too large or slow for git but should be fast after setup.

### 7. Prove One Answer

Before accepting a source, answer one representative question and write the trace.

Trace shape:

```text
Source:
Access method:
Storage policy:
Snapshot/version:
Grain:
Measure:
Filters/query logic:
Validation:
Caveats:
```

The validation should be something a reviewer can re-run or inspect:

- Row count
- Latest fiscal year count
- Official dashboard total
- Download file size and last-modified date
- Power BI model refresh time
- Query-template checksum
- Source page URL

### 8. Decide

Use one of these outcomes:

- `accept-live`: Official API is stable enough for live queries.
- `accept-snapshot`: Official source is useful but should be normalized into a reviewed snapshot.
- `accept-context-only`: Useful official context, but not a reliable answer data source yet.
- `watchlist`: Possible source, needs more evidence or a narrower question.
- `reject`: Not official, not inspectable, too brittle, or unable to support useful questions.

Record why. A rejected source with clear evidence is useful future context.

Also record the reviewed coverage category or backlog family, whether the source should create or update a source-card `coverage_claims` entry, and which evidence references would support that claim. Do not add unsupported rows just to fill a jurisdiction matrix.

## Civic Agent Artifacts

For an accepted source, add only the artifacts the source needs.

Clean API:

```text
jurisdictions/<jurisdiction>/sources/<source>.source.json
jurisdictions/<jurisdiction>/skill.md
docs/<jurisdiction>-demo.md
```

Report-shaped source:

```text
jurisdictions/<jurisdiction>/sources/<source>.source.json
jurisdictions/<jurisdiction>/scripts/extract_<source>.py
jurisdictions/<jurisdiction>/data/<source>/query_templates/*.query.json
jurisdictions/<jurisdiction>/data/<source>/<version>/normalized/*.jsonl
jurisdictions/<jurisdiction>/data/<source>/<version>/summary.json
jurisdictions/<jurisdiction>/data/<source>/<version>/provenance.json
jurisdictions/<jurisdiction>/skill.md
docs/<jurisdiction>-demo.md
```

Avoid a generic adapter until at least two sources of the same type force the same implementation shape.

## Printing Press Practices To Reuse

- One build-driving brief, not many narrative documents.
- Source priority before implementation, especially when a cleaner secondary source could invert the user's intended primary source.
- Complementary discovery modes: official docs, live traffic/dashboard metadata, community/tool references, downloads, documents.
- Raw evidence and provenance artifacts for anything inferred from a dashboard or captured traffic.
- Decision markers/checklists that prevent an agent from silently skipping a discovery method because it looks annoying.
- Validation as a ship gate, not a nice-to-have.
- Retros for systemic misses: after a source takes manual repair, write down what failed and whether it belongs in the future workflow.

## Printing Press Practices To Skip

- Generating a CLI before the source contract is proven.
- Absorbing every feature from every competing tool.
- Transcendence/novel-feature brainstorming.
- Broad scorecards before we have an answer runner.
- Heavy contributor automation before repeated source-addition mistakes are visible.
