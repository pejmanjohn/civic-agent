---
name: civic-agent
description: Use when answering civic budget, public finance, government spending, revenue, department, fund, program, or year-over-year comparison questions across supported jurisdictions.
---

# Civic Agent

This is the installable router skill for Civic Agent. A host may expose it as `/civic-agent`.

When invoked, identify the jurisdiction and route the user's question to the right jurisdiction skill file.

## Current Routes

### Seattle

Read the Seattle skill before answering City of Seattle operating budget questions.

If Civic Agent is installed as a Codex plugin, use the bundled reference:

```text
references/seattle.md
```

If working from this source repo outside the packaged plugin, use:

```text
skills/seattle/skill.md
```

If working from the hosted public repo, use:

```text
https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skills/seattle/skill.md
```

Use Seattle for:

- Seattle budget
- City of Seattle operating budget
- Seattle departments, services, programs, or funds
- Seattle Police Department, Fire, Human Services, City Light, or SPU budget questions
- Seattle FY2018-FY2026 year-over-year comparisons

## Workflow

1. Identify the jurisdiction in the user's question.
2. Identify the budget topic: operating budget, capital budget, transportation budget, spending/checkbook, revenue, staffing, school finance, department comparison, program drill-down, fund analysis, or year-over-year comparison.
3. Read the matching jurisdiction skill file.
4. Use that skill's official data sources, query recipes, validation checks, caveats, and answer style.
5. If the user asks for a chart, compute the data first and then use available chart/data-visualization tools to render it.
6. If no matching jurisdiction exists, say that Civic Agent does not yet include that jurisdiction.

## Chart Requests

For requests like:

```text
/civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026
```

Route to Seattle, query department totals by year, compute 2026 minus 2018, sort by absolute increase, and chart the largest increases. Include source, grain, and caveats.

If a data visualization or analytics plugin is available, use it after computing the source-backed table. If no chart renderer is available, return a compact table and explain that the data is chart-ready.

## Fresh-Agent Prompt

For agents that do not have this plugin installed:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```
