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

If the host exposes `skills/civic/SKILL.md` as `/civic`:

```text
/civic compare Seattle Police Department and Seattle Fire Department from FY2018 to FY2026
```

```text
/civic where does Seattle spend the most money in FY2026?
```

Slash command behavior is host-specific. The repo provides the installable router skill; the host decides whether it appears as `/civic`.
