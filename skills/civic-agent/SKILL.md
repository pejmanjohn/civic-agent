---
name: civic-agent
description: Use when answering civic budget, public finance, government spending, revenue, department, fund, program, or year-over-year comparison questions across supported jurisdictions.
argument-hint: "[a civic budget question, e.g. which Seattle departments grew most from 2018 to 2026]"
---

# Civic Agent

This is the installable router skill for Civic Agent. A host may expose it as `/civic-agent`.

When invoked, identify the jurisdiction and route the user's question to the right jurisdiction skill file.

## Current Routes

### Seattle

Read the Seattle skill before answering City of Seattle operating budget questions.

If Civic Agent is installed as a packaged plugin (Codex or Claude Code), use the bundled reference:

```text
references/seattle.md
```

If working from this source repo outside the packaged plugin, use:

```text
jurisdictions/seattle/skill.md
```

If working from the hosted public repo, use:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/seattle/skill.md
```

Use Seattle for:

- Seattle budget
- City of Seattle operating budget
- Seattle departments, services, programs, or funds
- Seattle Police Department, Fire, Human Services, City Light, or SPU budget questions
- Seattle FY2018-FY2026 year-over-year comparisons

### King County

Read the King County skill before answering King County, Washington Open Budget Dashboard or adopted budget context questions.

If Civic Agent is installed as a packaged plugin (Codex or Claude Code), use the bundled reference:

```text
references/king_county.md
```

If working from this source repo outside the packaged plugin, use:

```text
jurisdictions/king_county/skill.md
```

If working from the hosted public repo, use:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/king_county/skill.md
```

Use King County for:

- King County budget
- King County Open Budget Dashboard
- King County adopted 2026-2027 biennial budget context
- King County budgeted revenue, budgeted expenditures, departments, or FTE
- DCHS, DNRP, Metro Transit, Public Health, or Sheriff's Office budget questions
- King County 2017-2027 countywide budget trend questions

Do not use King County for actual spending, actual revenue collected, payments, procurement, personnel rosters, Seattle budget analysis, Washington state budget analysis, or cross-jurisdiction comparison.

For broad King County budget-size questions, use `king_county.open_budget_dashboard` for annual dashboard budgeted expenditure and `king_county.adopted_budget` for the official 2026-2027 adopted biennial headline. Present those frames side by side; do not add, average, or reconcile annual dashboard values with adopted two-year context.

### Pierce County

Read the Pierce County skill before answering Pierce County, Washington biennial budget, budget-vs-actual, or transaction-level actual spending (checkbook) questions.

If Civic Agent is installed as a packaged plugin (Codex or Claude Code), use the bundled reference:

```text
references/pierce_county.md
```

If working from this source repo outside the packaged plugin, use:

```text
jurisdictions/pierce_county/skill.md
```

If working from the hosted public repo, use:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/pierce_county/skill.md
```

Use Pierce County for:

- Pierce County budget (biennial, 2016-2017 through 2026-2027)
- Pierce County budget-vs-actual questions
- Pierce County spending, checkbook, payments, payees (2017 through partial 2026)
- Pierce County departments, funds, programs

Boundaries: budget data is biennial - never present totals as annual; checkbook answers state the data-through boundary; no Pierce revenue or staffing source exists yet; the City of Tacoma is a separate, not-yet-covered jurisdiction.

### Washington State

Read the Washington skill before answering Washington state operating budget, General Fund revenue, state agency vendor-payment/checkbook, or OFM population-denominator questions.

If Civic Agent is installed as a packaged plugin (Codex or Claude Code), use the bundled reference:

```text
references/washington.md
```

If working from this source repo outside the packaged plugin, use:

```text
jurisdictions/washington/skill.md
```

If working from the hosted public repo, use:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/jurisdictions/washington/skill.md
```

Use Washington for:

- Filed annual actuals for reviewed local governments via washington.fit_filed_actuals (Spokane, Tacoma, Walla Walla, Vancouver, Everett, King/Pierce/Snohomish counties, Sound Transit, King County Regional Homelessness Authority, Seattle School District No. 1, Evergreen School District) - "what does my city actually take in and spend", school district finances, Sound Transit revenues
- Property-tax levies statewide via washington.dor_property_tax_levies (certified district levy amounts and rates, due 2024-2025) - "why did my property tax go up", school levy amounts, levy-lid context; district level only, never parcel bills

- Washington state budget
- Washington operating budget
- Washington state revenue or General Fund revenue
- Washington actual spending
- Washington Open Checkbook
- Washington vendor payments
- Fiscal WA checkbook
- Fiscal WA operating budget
- Washington state agency budget totals
- 2025-27 enacted Washington operating budget
- Washington operating budget over time
- historical Washington operating budget trends
- Washington Total Budgeted or Outlook Funds (NGF-O) questions
- Washington OFM population estimates
- Seattle or King County per-resident budget denominators

Washington has separate source families. Operating budget answers use budgeted/authorized language. Revenue answers use General Fund estimate/actual language. Open Checkbook answers use actual vendor-payment language and require the managed local database for `washington.open_checkbook`. OFM population answers use resident population denominator language.

Do not use Washington for procurement contract terms, invoices, payroll, staffing/FTE, Seattle budget analysis, King County budget analysis, 2026 supplemental changes, pre-2013-15 operating-budget trends, capital budget, transportation budget, or cross-jurisdiction comparison.

## Freshness Posture

Every source card carries a `freshness` block: `data_through` (what the accepted data covers - never rediscover this), `observed_at`, and `cadence` (how often the source publishes and its typical lag). Before answering a current-period question ("is X happening now", "this year so far"):

1. Compute the boundary age from `data_through` against today.
2. If the age is within `expected_interval_days + expected_lag_days` of the cadence, answer normally and state the boundary with publication-lag language: "latest available; this source publishes <pattern>".
3. If the age exceeds that window, or the card/drift ledger marks the source `refresh_available`, declare `needs_refresh`: still give the bounded numbers, but LEAD with the fact that the snapshot likely lags the official source, and name the refresh path.
4. Warning from live experience: some sources REVISE values within an unchanged data-through boundary (Fiscal WA revenue estimates moved $6B under the same April label). Treat `data_through` as a data boundary, not a version; cite the snapshot version too.

Never present stale current-period data as current, and never refuse to show well-boundaried numbers just because they lag - the mode plus the boundary language carries the honesty.

## Workflow

1. Identify the jurisdiction in the user's question.
2. Identify the budget topic: operating budget, capital budget, transportation budget, spending/checkbook, revenue, staffing, school finance, department comparison, program drill-down, fund analysis, or year-over-year comparison.
3. Read the matching jurisdiction skill file.
4. Use that skill's official data sources, query recipes, validation checks, caveats, and answer style.
5. For managed local database sources such as `washington.open_checkbook`, inspect status first. If setup is missing and the host can run the repo CLI, ensure the source; otherwise report that managed local data is not set up.
6. For composed Scale questions, use the Scale recipe planning sequence before answering: question -> recipe -> required claims -> available sources -> compatibility check -> answer mode.
7. For source-backed answers, include a compact trace: the SOURCE CARD ID verbatim (for example `seattle.operating_budget`; dataset names alone do not satisfy the citation contract, and composed answers name every card used), public source URL or source-surface id when useful, snapshot/local data version or data-through boundary, grain, measure, filters/query logic, validation check or row count when useful, and caveats.
8. If the user asks for a chart, compute the data first and then use available chart/data-visualization tools to render it.
9. If no matching jurisdiction skill exists but the question names a Washington city, town, or county, answer in `unsupported_with_path` mode instead of a bare refusal: say plainly that no accepted budget source covers that jurisdiction yet; offer the jurisdiction's official April 1 resident population from `washington.ofm_population` as accepted context (the snapshot covers every Washington county, city, and town - see the Washington skill's OFM section), naming the estimate date; offer state-level facts only where they genuinely apply, labeled as state facts; and name the official path - the jurisdiction's own budget documents and the State Auditor's Financial Intelligence Tool (`https://portal.sao.wa.gov/FIT/`). Never substitute state or peer-jurisdiction numbers for the requested jurisdiction's budget.
10. If the jurisdiction is outside Washington, say that Civic Agent does not yet include it.

## Scale Recipes And Answer Modes

Use `docs/recipes/scale.md` in the source repo, or the bundled router guidance in this skill when installed, for resident-facing budget-size questions. Current recipe ids are `budget_scale.current_total`, `budget_scale.trend`, `budget_scale.per_capita`, and `budget_scale.cross_jurisdiction`.

Answer modes:

- `exact`: all required source claims exist, semantics are compatible, and freshness is acceptable.
- `partial`: supported pieces can be answered, but a source, denominator, adjustment, or frame is missing.
- `side_by_side_only`: facts are useful but frames, periods, units, or scopes should not be numerically compared.
- `unsupported_with_path`: no safe source-backed answer exists yet, but the missing source family or probe path is clear.
- `needs_refresh`: source exists, but validation or freshness blocks confident use.

Do not compare jurisdictions, periods, or budget frames until source-card semantics show compatible amount basis, budget frame, period type, period status, unit, government scope, and geography basis. If semantics are incompatible, present source-backed facts side by side with caveats or name the missing source path.

## Chart Requests

For requests like:

```text
/civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026
```

Route to Seattle, query department totals by year, compute 2026 minus 2018, sort by absolute increase, and chart the largest increases. Include source, grain, and caveats.

If a data visualization or analytics plugin is available, use it after computing the source-backed table. If no chart renderer is available, return a compact table and explain that the data is chart-ready.

For King County chart requests, use the checked-in snapshot from `jurisdictions/king_county/data/open-budget-dashboard/2026-04-01/`. Current chart-ready grains are countywide year totals, FY2026 department budgeted revenue/expenditure, and FY2026 department budgeted FTE.

For Washington operating-budget chart requests, use the checked-in snapshot from `jurisdictions/washington/data/operating-budget/2025-27-enacted-2025-05-20/`. Current chart-ready grains are 2025-27 enacted agency totals and functional area totals by fund view, plus enacted base historical trends by biennium from 2013-15 through 2025-27. Default to `Total Budgeted` unless the user asks for `Outlook Funds (NGF-O)`.

For Washington revenue chart requests, use the checked-in snapshot from `jurisdictions/washington/data/revenue-by-biennium/2025-27-revenue-through-2026-04/`. State that 2025-27 values are partial through April 2026.

For Washington checkbook chart requests, use `scripts/source_data.py query washington.open_checkbook` after the managed local database exists. Current chart-ready grains are category, agency, vendor, and monthly actual-payment totals.

For per-resident Scale answers involving Seattle or King County, compose the budget source with `washington.ofm_population`. Current checked-in OFM April 1, 2025 population estimates are Seattle = 816,600 and King County = 2,411,700. Cite both sources and state that resident denominators do not make city and county service responsibilities or budget frames directly comparable.

## Fresh-Agent Prompt

For agents that do not have this plugin installed:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```
