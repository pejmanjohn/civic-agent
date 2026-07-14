# WA-20 Expectation Change Log

Append-only. Every change to a case's versioned expectation block gets an entry: date, case id, field, old -> new, and justification. `expected_answer_mode` downgrades are invalid without an entry here (enforced by the ratchet check in `scripts/wa20.py --ratchet-check`).

## 2026-07-13 - baseline

Initial expectations for all 20 cases, seeded from `docs/goals/2026-07-13-benchmark-driven-launch-goal.md` Appendix A against coverage as of commit `ee95ebf`.

Mode distribution at baseline: 9 `unsupported_with_path`, 5 `exact`, 5 `partial`, 1 `needs_refresh`.

Deliberate divergence from the goal appendix: `kc-cuts-despite-20b` seeded as `partial` rather than `side_by_side_only` (the covered frame-discipline half supports a partial answer today; the side-by-side discipline is enforced by its `biennial-vs-annual` required caveat).

## 2026-07-13 - M3 hosted checkbook aggregates

- `wa-checkbook-vendor-lookup`: `expected_failure_mode` `validation_gap` -> `none`; `expected_answer_mode` unchanged (`exact`). The hosted/fresh-agent path now answers from checked-in aggregates (`jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/`) instead of dead-ending on the managed local database. Top-100 vendor truncation is disclosed in the case caveats and skill routing.
