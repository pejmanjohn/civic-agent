# Scale Recipes

Scale recipes define how Civic Agent should answer resident-facing questions about budget size, budget growth, per-capita scale, and cross-jurisdiction comparison. They compose source-card claims; they do not replace source cards, source fingerprints, or jurisdiction skills.

Before answering a composed Scale question, build an internal plan:

```text
question -> recipe -> required claims -> available sources -> compatibility check -> answer mode
```

## Answer Modes

- `exact`: All required source claims exist, the semantic fields are compatible, and freshness is acceptable.
- `partial`: Civic Agent can answer supported pieces, but one or more source claims, denominators, adjustments, or frames are missing.
- `side_by_side_only`: Sources can each answer locally, but their frames, periods, units, or scope should not be numerically compared.
- `unsupported_with_path`: No safe source-backed answer exists yet, but the missing source family or probe path is clear.
- `needs_refresh`: A source exists, but validation or freshness blocks confident use.

## Recipe: `budget_scale.current_total`

Use for questions such as:

```text
How big is Seattle's operating budget?
How big is King County's budget?
```

Required source claims:

- a budget or revenue amount claim at the requested jurisdiction;
- source semantics for amount basis, budget frame, period type, period status, unit, government scope, and geography basis;
- source trace with public URL or source-surface id, version or data-through boundary, grain, measure, filters, validation check, and caveats.

Behavior:

- If one accepted source matches the requested frame, answer from that source and name the frame.
- If the user asks a broad "how big is the budget?" question and multiple accepted official frames exist, show them side by side with labels.
- If another official frame is known but not yet accepted, answer the accepted source as `partial` and name the missing source path.
- Do not collapse annual dashboard values, adopted biennial budgets, operating budgets, General Fund values, and actual spending into one headline number.

## Recipe: `budget_scale.trend`

Use for questions such as:

```text
How has Seattle's budget changed since 2018?
How have Seattle's and King County's budgets changed over the last 5-10 years?
```

Required source claims:

- comparable time series within each source;
- period grain and amount basis;
- semantic caveats for source surfaces, reorganizations, future years, and partial periods.

Behavior:

- Compute nominal trend when the source supports a stable series.
- State the start and end periods, amount basis, and budget frame.
- For cross-jurisdiction trend questions, compare only compatible semantics. Otherwise present source-specific trends side by side.
- Do not present inflation-adjusted or per-capita trend unless accepted companion sources provide those adjustments.

## Recipe: `budget_scale.per_capita`

Use for questions such as:

```text
What is the per-resident budget for Seattle and King County?
```

Required source claims:

- a source-backed budget total;
- accepted population or denominator source;
- denominator semantics: estimate date, geography basis, resident/service population choice, and boundary caveats.

Behavior:

- If no accepted denominator source exists, return `unsupported_with_path` and name the needed source family.
- For Seattle and King County resident denominators, use `washington.ofm_population` unless a narrower accepted source supersedes it.
- If a denominator exists but fiscal year and estimate date differ, answer as `partial` and state the mismatch.
- State whether the denominator is residents, households, taxpayers, service population, or another basis.
- Do not imply per-capita values are comparable when governments have different service responsibilities or budget frames.

## Recipe: `budget_scale.cross_jurisdiction`

Use for questions such as:

```text
Compare Seattle's budget with King County's.
Which government spends more per resident?
```

Required source claims:

- at least two jurisdiction-specific source-backed answers;
- compatible units, period types, amount basis, budget frames, government scopes, and geography bases;
- denominator/context sources when computing adjusted or per-capita values.

Behavior:

- Use `exact` only when source semantics are compatible, including government scope and geography basis.
- Use `side_by_side_only` when the facts are useful but not apples to apples.
- Use `partial` when one jurisdiction has an accepted source and another is missing a matching frame or denominator.
- Preserve source-specific caveats in the final answer trace.

## Benchmark Tie-In

The seed cases in `benchmarks/scale/cases.json` define the current acceptance target for these recipes. Update the benchmark cases when a source or recipe changes the expected answer mode, required caveats, expected source ids, or improvement path.
