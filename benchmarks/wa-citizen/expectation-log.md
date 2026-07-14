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

## 2026-07-13 - FIT filed actuals accepted (M6)

`budget_finance.filed_annual_actuals` promoted to an active taxonomy category (probe: `docs/source-probes/washington-fit-filed-actuals.md`); all `proposed:` prefixes dropped per the contract test. Ratchets, all upward, all backed by the checked-in FIT snapshot (milestone-2025-published-2026-06-30, verified live 2026-07-13):

- `walla-walla-city-budget`: `unsupported_with_path` -> `partial` (filed actuals now answerable; adopted budget remains the missing half).
- `spokane-police-vs-housing`: `unsupported_with_path` -> `partial` (totals answerable; BARS category breakdown not yet a reviewed claim - the ceiling reason).
- `evergreen-schools-cuts`: `unsupported_with_path` -> `partial` (FIT Schools route; OSPI enrollment remains for per-pupil).
- `sound-transit-car-tabs`: `unsupported_with_path` -> `partial` (filed totals; revenue-stream split and ST3 plan out of scope).
- `kc-actuals-vs-budget-trap`: `unsupported_with_path` -> `partial` (actuals now exist; frames stay side-by-side, never reconciled).
- `sps-deficit-school-closures`: `unsupported_with_path` -> `partial` (filed totals; F-195 budgets and enrollment remain).
- `seattle-kc-homelessness-kcrha`: mode unchanged (`partial`); KCRHA filed actuals added to expected sources with the 2024 deficit-year fact.

## 2026-07-14 - DOR property-tax levies accepted (M7, second half)

`budget_finance.property_tax_levies` promoted (probe: `docs/source-probes/washington-dor-property-tax-levies.md`); `proposed:` prefixes dropped. Snapshot `levies-due-2025` (tax years 2024-2025, 4,593 levy rows) reconciles with DOR Tables 8/12/14 to the dollar.

- `kc-property-tax-why-up`: `unsupported_with_path` -> `partial`. District-level levy amounts, rates, YoY change, and 101%-limit context answerable; the parcel-level stack (assessor tax-code areas, PDF-only) and ballot-measure linkage remain out of scope - the partial ceiling reasons.
- `school-levy-household-cost`: `unsupported_with_path` -> `partial`. District EP&O/bond levy rates and amounts answerable; household math stays illustrative without parcel assessed value.
- `kc-cuts-despite-20b`: mode unchanged (`partial`); the levy-capacity adjunct is now supported, so the caveat flips from naming a missing source to explaining the 101% mechanics.
