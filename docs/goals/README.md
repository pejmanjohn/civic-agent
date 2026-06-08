# Civic Agent Goals

This directory holds Civic Agent improvement-loop artifacts. Use it after a benchmark run, dogfood session, source addition, review cycle, or roadmap checkpoint when the repo needs a ranked goal brief rather than another one-off plan.

The goal loop is:

```text
collect evidence
-> compare Civic Agent vs baseline
-> diagnose reusable failure modes
-> get a blind second read
-> extract principles
-> rank goals
-> create milestone handoff
-> after implementation: rerun eval
-> compare expected vs actual improvement
-> update next goals
```

## Files

- `templates/civic-agent-goal-brief.md`: Copy this before implementation. It captures evidence, plugin-vs-baseline gaps, failure modes, ranked goals, expected eval movement, and a `/ce-plan` handoff prompt.
- `templates/civic-agent-post-eval.md`: Copy this after implementation. It records package/install validity, score deltas, what improved, what did not, regressions, scorer gaps, and next goals.
- `failure-modes.md`: Shared vocabulary for classifying reusable failures.
- `eval-scoring-rubric.md`: Manual scoring rubric for benchmark and post-eval runs.
- `../processes/civic-agent-improvement-loop.md`: Full process for running the loop.

## Naming

Use stable, dated filenames:

```text
docs/goals/YYYY-MM-DD-<scope>-goal.md
docs/goals/YYYY-MM-DD-<scope>-post-eval.md
```

Examples:

```text
docs/goals/2026-06-08-scale-source-composition-goal.md
docs/goals/2026-06-08-scale-source-composition-post-eval.md
```

## Evidence Inputs

Prefer checked-in or reproducible artifacts over chat memory:

- benchmark cases and manual audit files under `benchmarks/`;
- source cards and source-probe docs under `jurisdictions/` and `docs/source-probes/`;
- coverage docs under `docs/coverage-*`;
- router, recipe, and jurisdiction skills;
- package/install status from `python3 scripts/dev.py status` and `python3 scripts/dev.py verify`;
- official external references when a source is being probed or revalidated.

## Rules

- Keep goal briefs non-mutating: they diagnose, rank, and hand off; they do not start implementation unless the user explicitly asks.
- Record expected eval movement before implementation so post-eval can judge whether the work improved the benchmark case, not just whether milestones landed.
- A post-eval cannot claim score movement without package/install state, scorer type, prompt source, baseline arithmetic, and known limitations.
- Treat scorer gaps as roadmap evidence. A manual benchmark is acceptable, but arithmetic and objective checks should not be silently sloppy.

