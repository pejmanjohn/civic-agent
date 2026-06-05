# Example Prompts

Worked answers for these Seattle prompts are in `docs/seattle-demo.md`.
Worked answers for King County prompts are in `docs/king-county-demo.md`.
Washington Open Checkbook setup and answer traces are in `docs/washington-checkbook-demo.md`.

## Fresh Agent

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and help me analyze the Seattle budget.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and compare Seattle Police Department, Seattle Fire Department, and Human Services Department from FY2018 to FY2026.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and tell me where Seattle spends the most money in FY2026.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and show the largest King County FY2026 department budgets.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and summarize King County budgeted revenue, budgeted expenditures, and FTE by year.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and show how Washington state operating budgets changed over time.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and compare Washington General Fund estimated and actual revenue by biennium.
```

```text
Read https://raw.githubusercontent.com/pejmanjohn/civic-agent/main/skill.md and show Washington Open Checkbook actual vendor payments by category for 2025-27.
```

## Installed Skill / Slash-Style Host

If the host exposes `skills/civic-agent/SKILL.md` as `/civic-agent`:

```text
/civic-agent compare Seattle Police Department and Seattle Fire Department from FY2018 to FY2026
```

```text
/civic-agent where does Seattle spend the most money in FY2026?
```

```text
/civic-agent show King County FY2026 departments by budgeted expenditure
```

```text
/civic-agent which King County departments have the most budgeted FTE in FY2026?
```

```text
/civic-agent show Washington Open Checkbook vendor payments by category for 2025-27
```

```text
/civic-agent show the top Washington Open Checkbook vendors in 2025-27
```

With a data/charting plugin:

```text
@data-analytics /civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026.
```

```text
@data-analytics /civic-agent make me a chart of King County FY2026 department budgeted expenditures.
```

```text
@data-analytics /civic-agent make me a chart of Washington Open Checkbook monthly vendor payments for 2025-27.
```

Slash command behavior is host-specific. The repo provides the installable router skill; the host decides whether it appears as `/civic-agent`.
