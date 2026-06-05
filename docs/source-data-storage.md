# Source Data Storage Policy

Civic Agent prefers live official data when the official source is fast, structured, and stable enough to query during an answer. When live access would make answers slow, brittle, or impossible to validate, choose the lightest durable storage tier that preserves trustworthy source-backed answers.

This policy applies during source probing and source-card review. It does not replace source-specific validation, provenance, or answer caveats.

## Storage Tiers

| Tier | Normal answer source | Use when | Git policy | Current examples |
|---|---|---|---|---|
| `live` | Official API or official query endpoint | The source is documented or stable, low-latency, queryable at the needed grain, and easy to validate at answer time. | Commit source card, query recipes, validation notes, and small tests only. | `seattle.operating_budget` |
| `checked_in_snapshot` | Reviewed normalized files in the repo | Normalized data is compact, slow-changing, useful for tests/demo/default answers, and reviewable in git. | Commit normalized rows, summary, provenance, query templates when needed, and compact fixtures. Raw captures are local/debug artifacts unless reviewed and small. | `king_county.open_budget_dashboard`, `washington.operating_budget`, `washington.revenue_by_biennium` |
| `managed_local_db` | Local database under the user's Civic Agent data cache | Official source data is large, slow to parse, awkwardly formatted, or too detailed for git, but can be downloaded and rebuilt locally. | Commit source card, probe, builder, tests, small fixtures, provenance shape, and optional compact rollups. Do not commit full raw files, full line-item dumps, or local databases. | `washington.open_checkbook` |
| `hosted_artifact` | Hosted artifact or service downloaded/queried by the agent | Rebuild cost, bandwidth, validation, or product scale makes every user rebuilding locally wasteful. | Commit manifests, source cards, validation code, and client logic. Raw files and derived artifacts live in managed storage. | Future tier |
| `context_only` | Human-readable official page or document | The source is useful for citations or explanation but does not yet have a validated extraction path. | Commit source notes and citation workflow only. | Document-only budget context |
| `watchlist` | None | The source may become useful but access, semantics, or validation are not acceptable yet. | Commit probe notes if useful. | Unstable dashboards |
| `reject` | None | The source is unofficial, misleading, not reproducible, or outside scope. | Usually no source card. Record rejection in probe when needed. | Unofficial mirrors without official backing |

## Decision Rules

1. Prefer `live` for clean official APIs and open-data portals when validation can run cheaply at answer time.
2. Prefer `checked_in_snapshot` when normalized data is small enough to review, diff, test, and package without making the repo heavy.
3. Prefer `managed_local_db` when the official source is valuable but too large, slow, or awkward for git or answer-time parsing.
4. Promote to `hosted_artifact` only after repeated local rebuild cost, bandwidth, or multi-jurisdiction scale justifies central publishing.
5. Keep `context_only`, `watchlist`, and `reject` explicit. A source is not answerable just because it exists.

## Freshness Contract

Every non-live source must define how freshness is checked:

- Source page URL or official machine URL.
- Last-modified header, API metadata, model refresh time, report timestamp, file checksum, or a source-specific probe.
- `downloaded_at` or `snapshot_fetched_at` time for local or repo artifacts.
- Row counts and validation totals for normalized data.
- Data-through boundary when current-period data is partial.

For managed local databases, status should be reported as one of:

- `missing`: no local artifact exists.
- `current`: local metadata matches the official freshness check.
- `stale`: official source appears newer than local data.
- `partial_current_period`: source is current, but the current fiscal period is incomplete.
- `refresh_failed`: the last refresh failed and prior data may still exist.
- `unknown`: freshness cannot be determined from available metadata.

## Artifact Policy

Git should contain the durable source contract:

- Source cards.
- Probe briefs.
- Extractors and builders.
- Query templates and fixtures when compact.
- Normalized checked-in snapshots when compact.
- Summary and provenance JSON.
- Tests.
- Worked examples and answer traces.

Git should not contain large generated artifacts:

- Full historical raw XLSX/CSV/ZIP files.
- Full line-item dumps when they are large enough to make clone/package size annoying.
- User-local databases.
- Debug captures unless reviewed, small, and intentionally useful.

Managed local data should live outside the repository by default. Use `CIVIC_AGENT_DATA_HOME` to override the location for tests, CI experiments, or developer-specific setups.

## Source Card Fields

Source cards may declare `storage_policy` alongside `access_method`:

```json
{
  "access_method": "official_bulk_download",
  "storage_policy": {
    "tier": "managed_local_db",
    "normal_answer_source": "local_db",
    "freshness_check": "source_file_metadata",
    "repo_artifacts": ["source_card", "probe", "builder", "tests", "fixtures"],
    "local_artifacts": ["raw_source_file", "local_database", "manifest"],
    "refresh_behavior": "download_and_rebuild_local_cache"
  }
}
```

`access_method` describes how the official source is reached. `storage_policy` describes where answer data lives and how it is kept trustworthy.

See `docs/washington-checkbook-demo.md` for the first managed-local database example.
