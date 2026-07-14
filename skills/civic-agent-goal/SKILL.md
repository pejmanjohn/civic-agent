---
name: civic-agent-goal
description: Use when turning Civic Agent benchmarks, dogfood evidence, source additions, roadmap work, or post-implementation evals into goal briefs, milestone handoffs, or score-delta reports.
argument-hint: "[source or scope, e.g. Scale source composition post-eval]"
---

# Civic Agent Goal

This project skill is the Civic Agent-specific `/goal` fallback. Use it when the user wants the next goal, a milestone handoff, or a post-eval from Civic Agent evidence.

## Non-mutating Rule

Non-mutating by default: produce a goal brief, post-eval, or handoff prompt. Do not edit source cards, recipes, router skills, package files, or implementation code unless the user explicitly asks to implement the resulting milestone.

## Required References

Read these before producing the artifact:

- `docs/processes/civic-agent-improvement-loop.md`
- `docs/goals/templates/civic-agent-goal-brief.md`
- `docs/goals/templates/civic-agent-post-eval.md`
- `docs/goals/failure-modes.md`
- `docs/goals/eval-scoring-rubric.md`

Use benchmark-specific docs such as `benchmarks/scale/README.md` when the evidence comes from a benchmark bucket.

## Goal Brief Workflow

1. Collect evidence from benchmark files, source cards, source probes, repo docs, user notes, and official references.
2. Record plugin/package validity when an eval result is involved: commit, branch, package surface, dev verification, production install status, and stale cache warnings.
3. Separate raw observations from interpretation.
4. Compare Civic Agent behavior against the baseline.
5. Classify gaps with the shared failure-mode labels.
6. Get or simulate a skeptical second read of the evidence, clearly marking it as a review of the supplied artifacts.
7. Extract reusable principles.
8. Rank goals and explain why lower-ranked goals are not first.
9. End with a `/ce-plan` handoff prompt.

## Post-Eval Workflow

1. Verify the implementation under test: commit, branch, package, install status, and eval date.
2. Rerun or review the benchmark cases using the same scoring dimensions.
3. Record old score, new score, delta, and whether each case actually improved.
4. Compute old written average, old arithmetic average, new average, and both deltas.
5. Separate what improved from what did not improve much.
6. Record regressions, scorer gaps, and next goal recommendations.

## Failure Labels

Use the labels from `docs/goals/failure-modes.md` exactly:

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

## Output Paths

When saving artifacts, use:

```text
docs/goals/YYYY-MM-DD-<scope>-goal.md
docs/goals/YYYY-MM-DD-<scope>-post-eval.md
```
