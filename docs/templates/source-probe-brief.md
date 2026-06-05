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

## Storage Policy

Recommended storage tier:

```text
live | checked_in_snapshot | managed_local_db | hosted_artifact | context_only | watchlist | reject
```

Why:

```text
<short rationale>
```

Normal answer source:

```text
<official API | repo snapshot | local DB | hosted artifact | none>
```

Freshness check:

```text
<API metadata, source file metadata, model refresh, report timestamp, manual snapshot version, custom probe, or none>
```

Repo artifacts:

```text
<source card, probe, normalized snapshot, summary, provenance, fixtures, tests, docs>
```

Local or hosted artifacts:

```text
<raw files, local database, manifest, hosted artifact, or none>
```

Partial-period data-through rule:

```text
<how to record current-period completeness, or none>
```

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
Storage policy:
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
