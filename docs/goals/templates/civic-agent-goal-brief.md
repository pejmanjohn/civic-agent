# Goal Brief: <scope>

## Trigger

Why this loop was run.

## Evidence Inputs

- Threads:
- Benchmark files:
- Repo docs:
- Source cards:
- User notes:
- External/official references:

## Raw Observations

Separate facts from interpretation.

## Plugin vs Baseline Gap

| Question | Plugin behavior | Baseline behavior | Gap |
|---|---|---|---|
|  |  |  |  |

## Failure Modes

Use standard labels from `docs/goals/failure-modes.md`:

- `missing_source`
- `missing_denominator`
- `semantic_mismatch`
- `missing_recipe`
- `weak_trace`
- `freshness_unclear`
- `unsupported_question`
- `packaging_or_install_drift`
- `validation_gap`
- `scorer_gap`

## Blind Review Summary

- Agreements:
- Disagreements:
- Additional risks:
- Ranking changes:

## Extracted Principles

Durable project rules learned from the evidence.

## Ranked Goals

| Rank | Goal | Evidence | Why now | Not now |
|---|---|---|---|---|
|  |  |  |  |  |

## Contract Changes Needed

- Benchmark cases:
- Source cards:
- Recipes:
- Router/skills:
- Validation/tests:
- Packaging/dev workflow:
- Eval/scoring:

## Milestone Queue

| Milestone | Goal | Acceptance |
|---|---|---|
|  |  |  |

## Expected Eval Movement

| Case | Expected improvement | Why |
|---|---|---|
|  |  |  |

## Handoff Prompt For /ce-plan

```text
Use this goal brief to create a repo-scoped implementation plan for Civic Agent.

Scope:

Top-ranked goal:

Evidence:

Required contract changes:

Expected eval movement:

Constraints:
- Keep implementation milestones reviewable.
- Preserve package/install provenance.
- Do not replace manual civic usefulness scoring with an unvalidated model judge.
```
