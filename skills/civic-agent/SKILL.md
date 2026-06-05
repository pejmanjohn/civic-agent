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

Read the King County skill before answering King County, Washington Open Budget Dashboard questions.

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
- King County budgeted revenue, budgeted expenditures, departments, or FTE
- DCHS, DNRP, Metro Transit, Public Health, or Sheriff's Office budget questions
- King County 2017-2027 countywide budget trend questions

Do not use King County for actual spending, actual revenue collected, payments, procurement, personnel rosters, Seattle budget analysis, Washington state budget analysis, or cross-jurisdiction comparison.

### Washington State

Read the Washington skill before answering Washington state operating budget, General Fund revenue, or state agency vendor-payment/checkbook questions.

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

Washington has separate source families. Operating budget answers use budgeted/authorized language. Revenue answers use General Fund estimate/actual language. Open Checkbook answers use actual vendor-payment language and require the managed local database for `washington.open_checkbook`.

Do not use Washington for procurement contract terms, invoices, payroll, staffing/FTE, Seattle budget analysis, King County budget analysis, 2026 supplemental changes, pre-2013-15 operating-budget trends, capital budget, transportation budget, or cross-jurisdiction comparison.

## Workflow

1. Identify the jurisdiction in the user's question.
2. Identify the budget topic: operating budget, capital budget, transportation budget, spending/checkbook, revenue, staffing, school finance, department comparison, program drill-down, fund analysis, or year-over-year comparison.
3. Read the matching jurisdiction skill file.
4. Use that skill's official data sources, query recipes, validation checks, caveats, and answer style.
5. For managed local database sources such as `washington.open_checkbook`, inspect status first. If setup is missing and the host can run the repo CLI, ensure the source; otherwise report that managed local data is not set up.
6. For source-backed answers, include a compact trace: source, grain, measure, filters/query logic, validation check or row count when useful, and caveats.
7. If the user asks for a chart, compute the data first and then use available chart/data-visualization tools to render it.
8. If no matching jurisdiction exists, say that Civic Agent does not yet include that jurisdiction.

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

## Fresh-Agent Prompt

For agents that do not have this plugin installed:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```
