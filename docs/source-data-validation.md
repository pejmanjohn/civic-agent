# Source Data Validation

Civic Agent validation answers one narrow question: is a source ready to support the answer paths its source card claims? Validation does not independently audit every public record, and it does not make normal answers switch to live official endpoints.

Use this workflow for every accepted source tier. It should be possible for a maintainer or agent to connect an answer value back to the source card, public source page, machine retrieval surface, version or data-through boundary, and the checks that made the stored data acceptable.

## Validation Modes

| Mode | Network? | Purpose |
|---|---:|---|
| Offline validation | No | Check source cards, checked-in snapshots, existing local manifests, and existing local databases. This is the default. |
| Refresh check | Yes, source-specific | Compare current official-source metadata or rebuilt temporary evidence to stored artifacts. This classifies source drift and must be requested explicitly. |
| Refresh or rebuild | Yes, source-specific | Update a managed local cache or regenerate a snapshot. This is never part of ordinary answer generation. |

## Common Result Shape

Validation commands should return one compact shape across storage tiers:

```json
{
  "ok": true,
  "command": "validate",
  "source_id": "washington.revenue_by_biennium",
  "storage_tier": "checked_in_snapshot",
  "status": "partial_current_period",
  "normal_answer_source": "repo_snapshot",
  "source_fingerprint": {},
  "checks": [
    {
      "name": "row_counts",
      "status": "passed",
      "evidence": {"expected": 15, "observed": 15},
      "message": "Normalized row count matches summary."
    }
  ],
  "warnings": [],
  "snapshot_path": "jurisdictions/washington/data/revenue-by-biennium/...",
  "data_through": "2026-04"
}
```

Allowed statuses:

- `valid`: source metadata and stored artifacts pass the checks for the declared tier.
- `partial_current_period`: checks pass, and the source card explicitly says the current period is incomplete through a stated date.
- `missing`: required local or repo artifacts are absent.
- `stale`: stored data is internally valid but freshness metadata no longer matches the accepted source surface.
- `value_drift`: recomputed totals or spot checks disagree with stored summaries.
- `metadata_drift`: source, endpoint, report, file, template, or request identity changed.
- `validation_failed`: malformed data, missing required metadata, failed checks, or unsupported source tier.
- `refresh_failed`: optional live refresh or drift check failed.
- `not_applicable`: the requested check does not apply to the source tier.

## Source Fingerprint

Every accepted source should expose a `source_fingerprint` block in its source card. Stored artifacts should carry the same block or an artifact-specific projection of it. The block has a small common core and source-specific detail.

Required common fields:

- `public_inspection_urls`: official pages a user can open.
- `machine_access`: API endpoint, dashboard endpoint, report URL, file URL, or a list of accepted source surfaces.
- `retrieval_context`: dataset id, report id, model id, source-surface id, file identity, request parameters, filters, query-template ids, or export identity.
- `version_boundary`: snapshot version, report refresh timestamp, file last-modified timestamp, fetched timestamp, or data-through boundary.
- `row_counts`: expected rows by table, export, or local database when applicable.
- `checks`: named totals, reconciliation checks, query-template hashes, response/export checksums, file checksums, and representative spot checks.

User-facing answer traces should cite the public source URL, source id, source-surface id when relevant, snapshot/local data version, data-through boundary, and query/filter context. Machine-oriented endpoints and hashes are for reproducibility; include them in answer traces only when they are useful to explain the evidence.

## Tier Expectations

| Tier | Required validation |
|---|---|
| `live` | Source card fingerprint, official public URL, machine endpoint, dataset/report/file identity, known freshness metadata, and at least one cheap validation query or metadata check. |
| `checked_in_snapshot` | Source card fingerprint, `summary.json`, `provenance.json`, normalized rows, row counts, recomputed totals, query-template or export identity, source refresh/fetch timestamp, and named spot checks. |
| `managed_local_db` | Source card fingerprint, local `manifest.json`, database presence, required schema, queryability, source-file metadata, row counts, data-through boundary, and representative aggregates using the same grains as normal answers. |
| `hosted_artifact` | Source card fingerprint, artifact manifest, hosted artifact identity, checksum or signature, freshness metadata, client validation, and fallback behavior. |
| `context_only` | Public source URL, citation scope, unsupported answer claims, and the reason no structured extraction is accepted yet. |
| `watchlist` | Public source URL, reason it is not accepted, and what would need to change. |
| `reject` | Rejection reason and official-source comparison when useful. |

## Spot Checks

Spot checks should cover the answer paths users are likely to ask for:

- high-value totals such as jurisdiction-wide revenue, expenditures, FTE, or line-item count;
- top rows or grouped totals at the supported grain;
- reconciliations between child rows and parent totals;
- overlap checks when multiple source surfaces cover the same period;
- edge cases such as negative amounts, current partial periods, or absent years;
- file/template identity checks that prove the extraction route did not silently change.

Keep spot checks reviewable. A few meaningful checks are better than broad checks nobody understands.

## Drift Classification

Offline validation distinguishes local corruption from local absence. Optional refresh checks may add official-source drift:

- `unchanged`: official metadata and stored checks still match.
- `partial_current_period`: the official source is current through a stated partial period.
- `stale`: official source metadata is newer than the stored artifact.
- `value_drift`: refreshed totals differ from stored totals.
- `metadata_drift`: endpoint, model, report, file, parameter, template, or export identity changed.
- `refresh_failed`: source-specific live check failed.

Normal answer generation must keep using the source card's `storage_policy.normal_answer_source`. Validation results can be cited as evidence, but validation does not reroute answers.

## Generated Reports

Validation reports and refreshed comparison captures are local generated artifacts by default. Durable audit evidence belongs in:

- source cards;
- probe briefs;
- query templates;
- extractor and builder code;
- checked-in normalized snapshots;
- `summary.json` and `provenance.json`;
- managed local manifests;
- tests;
- worked examples and answer traces.

Do not commit large raw downloads, local SQLite databases, or full debug captures unless a specific artifact is deliberately reviewed and small enough to belong in git.
