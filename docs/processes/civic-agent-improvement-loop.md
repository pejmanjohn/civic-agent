# Civic Agent Improvement Loop

Use this process to turn Civic Agent evidence into ranked goals, implementation milestones, and post-implementation eval learning.

The loop is non-mutating until the user explicitly asks to implement a milestone.

## Trigger

Run the loop after any of these events:

- a benchmark run under `benchmarks/`;
- a dogfood session with `@civic-agent` or `@civic-agent-dev`;
- a new source, recipe, router, or validation change;
- a roadmap review;
- a user asks what should improve next.

## Inputs

Collect enough evidence to distinguish facts from interpretation:

- benchmark cases, manual audit notes, and baseline artifacts;
- source cards, source probes, coverage docs, and validation output;
- router, recipe, and jurisdiction skill behavior;
- package state from `python3 scripts/dev.py status`;
- package freshness from `python3 scripts/dev.py verify`;
- official references when source coverage or freshness is in question;
- blind second-read notes when available.

## Workflow

### 1. Record Eval Validity

Before comparing answers, record:

- current commit and branch;
- production or dev plugin package under test;
- dev install verified;
- production install status when relevant;
- stale cache or generated-package drift;
- benchmark artifact and prompt source;
- scorer type: manual, semi-automated, or automated.

Do not claim score movement without this state.

### 2. Compare Plugin vs Baseline

For each case, separate:

- plugin behavior;
- baseline or web behavior;
- source ids or official URLs cited;
- required caveats present and missing;
- answer mode;
- unsupported claims;
- user-facing usefulness.

Use `docs/goals/templates/civic-agent-goal-brief.md` for the table.

### 3. Diagnose Reusable Failure Modes

Classify each gap using `docs/goals/failure-modes.md`.

Prefer reusable labels over local symptoms. For example, a failed per-resident answer is usually `missing_denominator`, not "Seattle math bug", when the missing contract is an accepted population source.

### 4. Get A Blind Second Read

Ask for a skeptical review of the evidence and tentative ranking when possible. The second read should look for:

- false precision;
- source-frame mismatch;
- stale package/install state;
- score arithmetic errors;
- missing source or validation contracts;
- overbroad implementation goals.

Record agreements, disagreements, additional risks, and ranking changes in the goal brief.

### 5. Extract Principles

Turn repeated evidence into project rules. Good principles are reusable across jurisdictions and source families:

- "accepted source plus validation plus coverage claim plus recipe plus benchmark case";
- "show incompatible frames side by side";
- "record denominator semantics before computing ratios";
- "eval validity includes installed package freshness".

### 6. Rank Goals

Rank goals by:

- resident-facing impact;
- benchmark movement expected;
- safety risk removed;
- whether the contract unlocks future sources;
- implementation size;
- whether a narrower milestone can prove the pattern.

Capture what is not being done now.

### 7. Create Milestone Handoff

End the goal brief with a `/ce-plan` handoff prompt. It should name:

- scope;
- top-ranked goal;
- evidence;
- contract changes;
- acceptance checks;
- expected eval movement;
- constraints and non-goals.

Do not start implementation unless the user asks.

### 8. Post-Eval After Implementation

After milestones land, rerun the relevant eval and fill in `docs/goals/templates/civic-agent-post-eval.md`.

The post-eval must answer:

- which cases moved;
- which barely moved;
- which regressed;
- what changed in source, recipe, router, validation, or package behavior;
- what was still manual or subjective;
- what the next highest-value goal is.

## Example Invocation

```text
/goal civic-agent-improvement-loop
source: benchmarks/scale/2026-06-06-baseline.md
scope: Scale source composition
mode: diagnose -> principles -> milestone plan
```

If `/goal` is too global in the host, use the project skill `civic-agent-goal`.

## Post-Eval Validity Checklist

A post-eval cannot claim improvement unless it records:

- current commit;
- branch;
- package check;
- dev plugin install source;
- stale production/dev cache status;
- benchmark artifact used;
- scorer type;
- baseline arithmetic check.

If any item is missing, classify the result as `packaging_or_install_drift` or `scorer_gap` before using the score delta.

## Future Semi-Automated Scorer

Do not jump straight to a full model-judge harness. The first scorer helper should reduce manual sloppiness:

- load benchmark cases;
- read saved answer markdown;
- check expected source ids;
- check answer mode;
- check required caveats;
- check known numeric facts when available;
- compute score averages and deltas;
- produce a worksheet for human civic-usefulness scoring.
