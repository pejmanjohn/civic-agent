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

## 2026-07-14 - SPD fact correction (scorer_gap caught by the first Tier 1 runs)

- `spd-budget-2020-vs-2026`: `expected_facts` corrected. The seeded values ($437.1M FY2020 / $513.6M FY2026) summed every department matching %POLICE% - including the Community Police Commission and Police Relief and Pension - while the question and both captured answers correctly scope to the Seattle Police Department alone ($408,611,750 / $488,586,234.95, verified live 2026-07-14). Both Tier 1 runs failed these facts identically, which is what exposed the benchmark bug. Answer mode unchanged; classic scorer_gap.

## 2026-07-14 - freshness machinery + revenue refresh: wa-new-taxes ratchet

- `wa-new-taxes-actually-collecting`: `expected_answer_mode` `needs_refresh` -> `partial`; `max_data_age_days` 60 -> 120. The original 60-day bound was tighter than the source's real publication cadence (May actuals live in mid-July = ~75-day lag), so the case punished publication lag as if it were our lag. The refreshed snapshot (data through 2026-05) plus the new per-card freshness contract (cadence: 30d interval + 75d lag) make partial-with-boundary-language the honest expectation; needs_refresh now triggers only when the snapshot genuinely falls outside the cadence window. Note for scorers: the refresh also revealed that report values REVISE in place - current-biennium difference flipped from +$1.04B to -$353M after June forecast revisions - so no volatile current-period fact is pinned on this case.

## 2026-07-14 - maintainer calibration batch (decision sheet)

Six mode calibrations decided by the maintainer against three runs of evidence:

- `wa-checkbook-vendor-lookup`: stays `exact`; the skills now state that top-N aggregate answers fully support top-N questions (the 3/3 partial declarations were under-claiming).
- `kc-sheriff-budgeted-fte-2026`: stays `exact`; new router rule - answering at the accepted measure (budgeted FTE) with the distinction labeled stays exact.
- `spokane-police-vs-housing`: stays `partial`; the FIT skill now teaches the expected partial shape - citywide totals plus the named category gap - instead of full refusal.
- `sound-transit-car-tabs`: ceiling and expectation raised `partial` -> `exact` (upgrade): the asked question is fully answered by filed totals; adjacencies stay caveats. 3/3 runs already answered this way.
- `kc-actuals-vs-budget-trap`: `partial` -> `side_by_side_only` (rank downgrade, justified): the scale recipe's own definition fits - the two frames are shown side by side and never reconciled; 3/3 runs applied it.
- `pierce-vs-king-per-resident`: `partial` -> `exact` (upgrade): labeled biennial-to-annual alignment is now a sanctioned comparison (rule added to docs/recipes/scale.md); clears the standing scoreboard ratchet candidate.

## 2026-07-14 - D7 caveat adjudication (maintainer-approved policy)

Per-caveat verdicts against the run C answers:

- LOOSENED (concept clearly expressed, pattern too narrow): `st3-gap-out-of-scope` (capital buildout/bonded-construction framing counts); `general-vs-dedicated` (order-agnostic).
- REWRITTEN: `pierce-vs-king-per-resident` `period-mismatch-named` -> `comparability-basis-named`. Run C used FIT filed actuals for BOTH counties with year-matched OFM denominators - same source, basis, and year, so there was no period mismatch to name; the caveat now accepts either a shared basis or labeled alignment. The two pinned 2025 population facts are REMOVED: they hard-coded one answer path's denominators, and year-matched denominators are methodologically preferable.
- KEPT STRICT (content genuinely missing from answers): `fragmentation-is-the-answer`, `no-outcome-claims`, `modeling-choices-explicit`, `attribution-is-context`, `levy-101-context`. The routers now carry a Hard Questions Playbook teaching those answer shapes; future runs are expected to meet the patterns.
