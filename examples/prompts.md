# Example Prompts

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

## Installed Skill / Slash-Style Host

If the host exposes `skills/civic-agent/SKILL.md` as `/civic-agent`:

```text
/civic-agent compare Seattle Police Department and Seattle Fire Department from FY2018 to FY2026
```

```text
/civic-agent where does Seattle spend the most money in FY2026?
```

With a data/charting plugin:

```text
@data-analytics /civic-agent make me a chart showing which Seattle departments had the largest budget increases from 2018 to 2026.
```

Slash command behavior is host-specific. The repo provides the installable router skill; the host decides whether it appears as `/civic-agent`.
