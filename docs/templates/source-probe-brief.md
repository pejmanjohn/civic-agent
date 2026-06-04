# Source Probe Brief: <Source / Jurisdiction>

Status: draft

## Question

What civic-budget or public-finance question should this source help Civic Agent answer?

```text
<one concrete user-facing question>
```

## Source Identity

- Jurisdiction:
- Budget family:
- Official owner:
- Public inspection URL:
- Candidate machine URL:
- Source type: portal | open-data | dashboard | download | document | mixed
- Source priority:

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

If this is an open data portal, include the catalog search terms used and the candidate datasets returned:

| Search term | Candidate dataset | Dataset id | Owner/attribution | Why selected or rejected |
|---|---|---|---|---|
|  |  |  |  |  |

## Surface Classification

Access candidates:

- [ ] Official documented API
- [ ] Official open data portal
- [ ] Official bulk download
- [ ] Official public dashboard
- [ ] Official document/PDF
- [ ] HTML scrape only
- [ ] Unofficial mirror/context source
- [ ] Not usable

Probe methods attempted:

- [ ] Generic HTML/header probe
- [ ] Official API probe
- [ ] Socrata/open data probe
- [ ] CKAN probe
- [ ] ArcGIS probe
- [ ] Bulk file probe
- [ ] Dashboard probe
- [ ] Power BI probe
- [ ] Tableau probe
- [ ] Document/PDF probe
- [ ] HTML table probe

Evidence:

```text
<curl/web/browser observations, dataset ids, report ids, file headers, model ids>
```

Primary access surface:

```text
<documented API | Socrata | CKAN | ArcGIS | file download | Power BI | Tableau | document | HTML table | none>
```

Primary source identifiers:

```text
<domain, dataset id, resource id, report id, file URL, document URL, or none>
```

Companion surfaces:

```text
<official context pages, documents, dashboards, downloads, or none>
```

## Data Model

Fields and dimensions:

| Field | Type | Meaning | Notes |
|---|---|---|---|
|  |  |  |  |

Measures:

| Measure | Meaning | Budgeted or actual? | Notes |
|---|---|---|---|
|  |  |  |  |

Time/version fields:

```text
<fiscal years, biennia, budget versions, publish dates, refresh times>
```

Freshness and publication metadata:

```text
<rows updated, view/report/file modified, refresh frequency, publication stage, owner/contact/license>
```

Hierarchy:

```text
<agency -> program -> fund -> item, or source-specific hierarchy>
```

## Extraction Approach

Recommended access method:

```text
accept-live | accept-snapshot | accept-context-only | watchlist | reject
```

Why:

```text
<short rationale>
```

If snapshot:

- Query/capture templates:
- Normalized tables:
- Summary checks:
- Provenance fields:

If live:

- Endpoint:
- Query parameters:
- Rate/freshness caveats:
- Validation query:

## Supported Questions

- 
- 
- 

## Unsupported Claims

- 
- 
- 

## Validation Checks

| Check | Expected result | How to reproduce |
|---|---:|---|
|  |  |  |

## Worked Answer Trace

Question:

```text
<representative question>
```

Trace:

```text
Source:
Access method:
Snapshot/version:
Grain:
Measure:
Filters/query logic:
Validation:
Caveats:
```

## Risks

- 
- 
- 

## Decision

Decision:

```text
accept-live | accept-snapshot | accept-context-only | watchlist | reject
```

Next artifact:

```text
<source card, extractor, snapshot, demo, or none>
```
