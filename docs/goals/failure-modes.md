# Goal Failure Modes

Use these labels in goal briefs, benchmark audits, post-evals, and milestone handoffs. Pick the primary failure mode first, then add secondary modes only when they change the next action.

| Mode | Use when | Usual next action |
|---|---|---|
| `missing_source` | A source-backed answer needs an official source family that is not accepted yet. | Run `docs/source-probing.md`, then add or reject the source path. |
| `missing_denominator` | A ratio, per-capita value, adjustment, or normalized comparison lacks an accepted denominator or context source. | Probe the companion source family and record denominator semantics. |
| `semantic_mismatch` | Available sources answer local facts but differ in period, frame, measure, scope, unit, or geography. | Add compatibility metadata, present side by side, or narrow the question. |
| `missing_recipe` | A resident-facing question has source cards but no composition recipe or answer-mode rule. | Add or update a recipe before changing source behavior. |
| `weak_trace` | The answer gives numbers without enough source id, URL/surface, grain, measure, filters, freshness, row count, or caveat detail. | Tighten router, jurisdiction skill, or answer template trace requirements. |
| `freshness_unclear` | The answer cannot state snapshot date, data-through date, source refresh state, or current package cache state. | Record freshness in the source fingerprint or dev/prod install status. |
| `unsupported_question` | The requested answer is outside accepted Civic Agent coverage or cannot be safely answered from current sources. | Return unsupported with path, or add a source-probe goal if the question is in scope. |
| `packaging_or_install_drift` | Eval results may reflect stale production/dev plugin caches, generated package drift, detached HEAD ambiguity, or wrong install surface. | Run `python3 scripts/dev.py status`, `python3 scripts/dev.py verify`, and record branch/commit/package state. |
| `validation_gap` | Source data exists but lacks offline validation, row-count checks, spot checks, provenance, or source-fingerprint evidence. | Add source validation before relying on score movement. |
| `scorer_gap` | Manual scoring, arithmetic, prompt isolation, or objective checks are too weak to support the claimed improvement. | Add a worksheet, arithmetic check, required-source check, or narrower scorer rubric. |

## Classification Rules

- Use `missing_denominator` instead of `missing_source` when the missing source is specifically needed to compute a denominator or adjusted measure.
- Use `semantic_mismatch` when the facts are individually correct but not comparable.
- Use `packaging_or_install_drift` when the answer quality may be good or bad only because the wrong installed package was tested.
- Use `scorer_gap` when the implementation may be valid but the eval method cannot prove the delta.

