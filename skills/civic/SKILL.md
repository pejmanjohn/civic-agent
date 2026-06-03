---
name: civic
description: Use when answering civic budget, public finance, government spending, revenue, department, fund, program, or year-over-year comparison questions across supported jurisdictions.
---

# Civic

This is the installable router skill for Civic Agent. A host may expose it as `/civic`.

When invoked, route the user's question to the right jurisdiction skill.

## Routing

Current production jurisdiction:

- Seattle: `https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skills/seattle/skill.md`

If the question mentions Seattle, City of Seattle, a Seattle department, or Seattle FY2018-FY2026 budget comparisons, read the Seattle skill before answering.

If the question asks about Washington state, King County, another city, or cross-jurisdiction comparisons, say whether that jurisdiction is supported yet. Do not pretend unsupported sources exist.

## Workflow

1. Identify jurisdiction and budget topic.
2. Read the jurisdiction skill file.
3. Use that skill's official data source, query recipes, validation checks, caveats, and answer style.
4. Answer with the source, grain, numbers, and plain-English interpretation.

## Public Hosted Entry Point

For fresh agents that do not have this installed, use:

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```
