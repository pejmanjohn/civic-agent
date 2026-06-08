# Eval Scoring Rubric

This rubric keeps Civic Agent benchmark scoring manual but disciplined. Use the same dimensions as `benchmarks/scale/cases.json` so old and new runs can be compared.

Score each dimension from 0 to 5:

- 0: absent, unsafe, or materially wrong.
- 1: recognizes the question but cannot support the answer.
- 2: partially useful, with important unsupported claims or missing caveats.
- 3: usable with visible limitations.
- 4: strong, source-backed, and mostly complete.
- 5: ideal for the current source contract.

## Dimensions

| Dimension | 5 means | Common deductions |
|---|---|---|
| `correctness` | Numbers, frames, periods, and calculations match accepted sources and stated filters. | Wrong total, wrong year/biennium, unsupported arithmetic, source-frame confusion. |
| `traceability` | The answer names source id or official URL/surface, snapshot or data-through boundary, grain, measure, filters/query logic, and useful validation evidence. | Missing source id, vague citation, no row count or freshness boundary when needed. |
| `coverage_awareness` | The answer states what Civic Agent can and cannot answer from accepted sources. | Implies full jurisdiction coverage from one source, hides missing source families. |
| `comparability` | Cross-source comparisons only happen after compatible semantics are established; otherwise facts are shown side by side. | Collapses annual dashboard, adopted biennial, operating, actual-spending, and denominator frames into one headline. |
| `civic_usefulness` | A resident can understand scale, change, caveats, and next question paths without reading repo internals. | Technically correct but not decision-useful, buries the bottom line, or omits useful caveats. |
| `freshness` | The answer states package/install state for evals and source freshness for data claims. | Stale dev/prod install, unknown snapshot, or missing data-through boundary. |
| `improvement_path` | The answer or audit names the smallest source, recipe, validation, or packaging change that would improve the result. | "Needs better data" without a probe/source/contract path. |

## Score Delta Rules

- Score deltas must compare the same case, prompt source, scoring dimensions, and answer surface.
- Record both old written average and old arithmetic average. If they disagree, use both in the post-eval.
- Treat a case as improved only when the new score moves for a capability reason, not because the scoring note changed.
- A small delta can still matter if it removes a safety risk such as unsupported comparison or stale package state.
- A milestone can be complete while the eval does not improve; record that as evidence for the next goal.

## Objective Checks Before Human Judgment

Before assigning civic-usefulness judgment, check the mechanical items:

- required source ids appeared or missing-source behavior was explicit;
- required caveats appeared;
- answer mode matched the benchmark case or recipe;
- arithmetic and averages are correct;
- package/install state is current enough for the claim;
- source validation/fingerprint checks are recorded when data changed.
