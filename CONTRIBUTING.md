# Contributing To Civic Agent

Civic Agent turns official government data into agent-readable skills with citations and caveats. The one non-negotiable is source trust: every accepted source declares what it can answer, what it cannot, how to validate it, and where it drifts. This runbook enumerates every artifact a new source touches - written from the additions of `pierce_county.open_budget`, `pierce_county.open_checkbook`, and `washington.fit_filed_actuals` (all 2026-07-13).

An agent-native workflow is expected: point your coding agent at this file and the exemplar source listed in each step.

## Before Writing Anything: The Probe

Every new source family starts with a probe brief - no source card without one.

1. Copy `docs/templates/source-probe-brief.md` into `docs/source-probes/<slug>.md`.
2. Probe the official source LIVE. Record exact URLs, dataset/report ids, field lists, quirks, and 3-5 verified numeric facts with reproduction commands. Unverified claims are worthless; the probe is the evidence base for every later validation check.
3. Decide the storage tier per `docs/source-data-storage.md`: `live` (documented API, cheap aggregates - see Pierce), `checked_in_snapshot` (small reviewed slice of a bigger surface - see FIT), `managed_local_db` (bulk files - see the WA checkbook), or `context_only`/`watchlist`/`reject`.
4. If the source needs a NEW coverage category, follow the taxonomy promotion rule in `docs/coverage-taxonomy.md` (the probe must document owner, access, measures, grains, validation checks, and unsupported claims before a category is promoted).

## The Artifact Checklist

Adding source `<jurisdiction>.<dataset>` touches, in rough order:

| # | Artifact | Exemplar | Enforced by |
|---|---|---|---|
| 1 | Probe brief `docs/source-probes/<slug>.md` | `pierce-county-open-data.md`, `washington-fit-filed-actuals.md` | review |
| 2 | Source card `jurisdictions/<slug>/sources/<dataset>.source.json` | `pierce_county/sources/open-budget.source.json` (live), `washington/sources/fit-filed-actuals.source.json` (snapshot) | `tests/test_source_storage_policy.py` (tier vocab, fingerprint keys), `tests/test_source_coverage.py` (claims, semantics, evidence refs) |
| 3 | Extractor/builder script (snapshot and managed tiers) | `washington/scripts/extract_fit_actuals.py` | validator |
| 4 | Snapshot artifacts under `jurisdictions/<slug>/data/<dataset>/<version>/` - normalized JSONL + `summary.json` + `provenance.json`, BOTH carrying an embedded `source_fingerprint` with `row_counts`, `checks`, `public_inspection_urls` | FIT snapshot dir | `scripts/source_data.py` validator |
| 5 | Validator function + registration in `scripts/source_data.py` `load_validator()` (snapshot/managed tiers; live tier validates generically) | `validate_washington_fit_snapshot` | `tests/test_source_data_validation.py` |
| 6 | Drift decision in `scripts/drift.py`: a `LIVE_CHECKS` entry (fingerprint a CLOSED period so routine current-period growth is not "drift") or a documented `SKIP_REASONS` entry | `check_pierce_open_budget`, `check_fit_filed_actuals` | `tests/test_drift.py` completeness contract |
| 7 | Jurisdiction skill (`jurisdictions/<slug>/skill.md`, new jurisdiction) or a section in an existing skill, with query recipes, validation checks, vocabulary walls, and answer style | `pierce_county/skill.md` | reference-sync tests |
| 8 | Routes in BOTH routers: `skill.md` (hosted) and `skills/civic-agent/SKILL.md` (installable) | Pierce County sections | `tests/test_packaging_hygiene.py` router-consistency test |
| 9 | Marketplace keyword for a new jurisdiction in `.claude-plugin/marketplace.json` | `pierce-county` | `tests/test_packaging_hygiene.py` |
| 10 | Test-constant registrations: `EXPECTED_CURRENT_CLAIMS` (test_source_coverage), `EXPECTED_POLICY_TIERS` (test_source_storage_policy), validate statuses (test_source_data_validation), `EXPECTED_ACTIVE_CATEGORIES` only on category promotion | see 2026-07-13 commits | the tests themselves |
| 11 | Regenerate: `python3 scripts/package_plugin.py` and `python3 scripts/coverage.py` | - | their `--check` modes in CI |
| 12 | Benchmark movement: if a WA-20 case's claims now resolve, ratchet its expectations in `benchmarks/wa-citizen/cases.json` WITH an `expectation-log.md` entry; regenerate `python3 scripts/wa20.py` | expectation-log entries for M3/M6/M7 | `scripts/wa20.py --check` and `--ratchet-check` in CI |

## Definition Of Done

A source PR is mergeable when all of these pass locally (CI runs the same):

```bash
python3 -m unittest discover -s tests
python3 scripts/package_plugin.py --check
python3 scripts/coverage.py --check
python3 scripts/wa20.py --check
python3 scripts/wa20.py --ratchet-check origin/main
python3 scripts/drift.py            # optional but recommended: live fingerprints hold
```

plus one non-mechanical bar: **a WA-20 benchmark case moved or was added**, with its expectation-log entry. A source that moves no benchmark case needs a written reason it exists.

## Source Trust Rules (the short version)

- Official sources only; every card names `human_inspection_urls` a reader can open.
- Claims are source-scoped and reviewed: `unsupported` means "unsupported by this source", never "the jurisdiction lacks this data". Do not imply jurisdiction coverage from one source.
- Vocabulary walls are mandatory: budgeted/approved/adopted vs actual vs filed vs estimated; biennial vs annual; never numerically merge incompatible frames - present side by side or refuse with a path.
- Validation checks pin verified numbers with reproduction commands and their verification date.
- Partial current periods always carry a data-through boundary.
- Edit canonical files under `jurisdictions/` - never the generated `plugins/` copies.

## Cheap Paths For New Jurisdictions

- **Socrata portal** (Tacoma? Everett has one): copy the Pierce pattern - live tier, no extractor, SoQL recipes in the skill, closed-period drift fingerprints. An afternoon.
- **FIT extension** (any WA city/county/school/special district): add the government to `REVIEWED_GOVERNMENTS` (or `REVIEWED_SCHOOL_DISTRICTS`) in `jurisdictions/washington/scripts/extract_fit_actuals.py`, re-run it, add the `coverage_jurisdictions` entry to the FIT card, update the card/validator row counts, and ratchet any benchmark case it unlocks. Under an hour - this is the paved road for the long tail of WA governments.
- **Everything else** starts with a probe brief and an honest tier decision.

## Local Ops (local-first; GitHub is the publish step, not the compute)

- `bash scripts/gates.sh` - every quality gate in one shot. `bash scripts/install-hooks.sh` installs it as a git pre-push hook so nothing leaves the machine without passing.
- `python3 scripts/drift.py --status` - the freshness ledger, run manually whenever you want to check on the sources (exit is always 0 in status mode; plain `python3 scripts/drift.py` exits nonzero on drift/error if you want the alarm form). No scheduled checks anywhere, by choice - staleness is also visible per-source at answer time via the cards' freshness blocks, and the Tier 0 scoreboard fails loudly if a stale source crosses a case's bound.
- `bash scripts/refresh-all.sh` - the deliberate Monday-coffee command: attempts the four cheap snapshot refreshes and prints each review checklist. Refreshes are never scheduled; they change reviewed artifacts.
- The GitHub workflows under `.github/workflows/` are push-triggered CI (`ci.yml`) plus manual-dispatch fallbacks for drift and refresh - no scheduled Actions compute.
