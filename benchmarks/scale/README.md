# Scale Benchmark

This benchmark is the repo-owned contract for the first Civic Agent composition audit. It is manual by design: each case records the prompt, expected source trace, caveats, scoring dimensions, failure mode, and improvement path, while a human auditor records model answers and scores.

The goal is not to prove that Civic Agent is always better than web search. The goal is to catch whether source-backed answers remain correct, traceable, coverage-aware, and safe about cross-source comparisons as the plugin changes.

## Files

- `cases.json`: Forward-looking benchmark contract. Future source, recipe, and router changes should update this file when they change expected source ids, answer modes, caveats, or improvement paths.
- `manual-audit-template.md`: Copy this template for a new benchmark run and fill in plugin and web-baseline answers.
- `2026-06-06-baseline.md`: Historical baseline from the first Scale audit. Keep it as evidence, not as the live contract.

## Current Cases

The seed cases cover the Scale bucket:

1. Seattle current operating budget total.
2. King County current budget-size framing.
3. Seattle and King County 5-10 year budget trend.
4. Seattle and King County per-resident budget.

These cases intentionally expose recurring national source shapes:

- clean official open-data API;
- official dashboard snapshot;
- annual dashboard values versus adopted biennial public framing;
- budget totals versus population denominators;
- source-covered facts that should be shown side by side rather than compared directly.

## Manual Protocol

1. Record repo and plugin state:
   - current commit;
   - whether the run uses production `@civic-agent` or local `@civic-agent-dev`;
   - `python3 scripts/dev.py status` and `python3 scripts/dev.py verify` output when testing installed plugin behavior.
2. For each case in `cases.json`, run the plugin prompt in an isolated fresh thread or subagent where possible.
3. For the same case, run the web-baseline prompt using official sources where possible and no Civic Agent source-card context.
4. Fill in `manual-audit-template.md` with:
   - answer text;
   - cited source ids or official URLs;
   - measures, grains, filters, snapshot or data-through dates;
   - required caveats observed or missing;
   - scores for each dimension;
   - primary failure mode;
   - recommended source, recipe, or metadata improvement.
5. Keep model judgment separate from contract validation. `tests/test_benchmark_contract.py` checks benchmark metadata only; it does not score answers.

## Improvement Loop

After a benchmark run changes or validates the project direction, run the goal loop in `docs/processes/civic-agent-improvement-loop.md`. Use `docs/goals/templates/civic-agent-goal-brief.md` before implementation to rank goals and expected eval movement, then use `docs/goals/templates/civic-agent-post-eval.md` after implementation to record score deltas, packaging validity, what improved, and what did not.

## Updating Cases

Update `cases.json` when a milestone changes the expected answer contract. Examples:

- Milestone 2 may add semantic compatibility fields that change required caveats.
- Milestone 3 may change expected answer modes through Scale recipes.
- Milestone 4 records the OFM population denominator probe in `docs/source-probes/washington-ofm-population.md`.
- Milestone 5 accepts `washington.ofm_population` and moves the per-capita case from missing-denominator to source-backed partial mode.
- Milestone 6 accepts `king_county.adopted_budget` as context-only and moves the King County current-total case to `side_by_side_only`.

Every accepted source PR after this benchmark should either improve an existing case or add a new benchmark case that names the resident-facing question it unlocks.
