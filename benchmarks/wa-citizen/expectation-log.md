# WA-20 Expectation Change Log

Append-only. Every change to a case's versioned expectation block gets an entry: date, case id, field, old -> new, and justification. `expected_answer_mode` downgrades are invalid without an entry here (enforced by the ratchet check in `scripts/wa20.py --ratchet-check`).

## 2026-07-13 - baseline

Initial expectations for all 20 cases, seeded from `docs/goals/2026-07-13-benchmark-driven-launch-goal.md` Appendix A against coverage as of commit `ee95ebf`.

Mode distribution at baseline: 9 `unsupported_with_path`, 5 `exact`, 5 `partial`, 1 `needs_refresh`.

Deliberate divergence from the goal appendix: `kc-cuts-despite-20b` seeded as `partial` rather than `side_by_side_only` (the covered frame-discipline half supports a partial answer today; the side-by-side discipline is enforced by its `biennial-vs-annual` required caveat).

## 2026-07-13 - M3 hosted checkbook aggregates

- `wa-checkbook-vendor-lookup`: `expected_failure_mode` `validation_gap` -> `none`; `expected_answer_mode` unchanged (`exact`). The hosted/fresh-agent path now answers from checked-in aggregates (`jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/`) instead of dead-ending on the managed local database. Top-100 vendor truncation is disclosed in the case caveats and skill routing.

## 2026-07-13 - Pierce County sources accepted (M7, first half)

- `pierce-county-budget-size`: `expected_answer_mode` `unsupported_with_path` -> `exact`; failure mode `missing_source` -> `none`. `pierce_county.open_budget` (biennial budget + budget-line actuals) and `pierce_county.open_checkbook` (transaction actuals) accepted as live Socrata sources; caveats rewritten from graceful-failure checks to biennial/budget-vs-actual/expenditure-only discipline; budget-total fact added ($3,500,588,070, verified 2026-07-13).
- `pierce-vs-king-per-resident`: `expected_answer_mode` stays `partial` even though Tier 0 now reports achievable `exact` (all four core claims supported). Reason: Pierce budget frames are biennial and King County dashboard values are annual; without a period-alignment recipe the honest answer presents per-resident values side by side without a numeric verdict. The standing ratchet-candidate note on the scoreboard is acknowledged and intentional until the cross_jurisdiction recipe gains an alignment rule.
