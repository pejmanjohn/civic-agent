---
date: 2026-06-04
topic: contribution-workflow
---

# Contribution Workflow Requirements

## Summary

Civic Agent should not add contributor machinery while the repo has one real source. The next design input should be a second, materially different source. Before that, the only defensible contributor-facing artifact is an optional, provisional source-trust checklist that helps maintainers and agents avoid unsupported civic-budget claims.

---

## Problem Frame

The repo already has the core contribution contract in implicit form: `docs/architecture.md` defines the routing shape, `jurisdictions/seattle/sources/operating-budget.source.json` shows a source card, `jurisdictions/seattle/skill.md` shows the jurisdiction skill pattern, and `scripts/package_plugin.py` refreshes the installable package.

The risk is that a generic "contributor workflow" would turn Seattle's clean Socrata shape into the project standard before Washington or another messy source tests the model. The useful thing to preserve now is narrower: every source-backed answer must have official provenance, explicit scope, supported and unsupported claims, validation checks, caveats, and package freshness.

---

## Key Decisions

- **Source #2 is the primary next move.** The contributor surface should be shaped by at least two real sources, preferably including a source that differs materially from Seattle.
- **The contract is source trust, not external contributor process.** The near-term user is the maintainer or an agent adding sources, not a broad open-source contributor base.
- **Source bar comes before jurisdiction bar.** A jurisdiction can begin with one narrow source, but the repo must not imply broad jurisdiction coverage from that single source.
- **Any pre-source-2 artifact is optional and provisional.** If added, it should say it is derived from one clean Seattle example and should be rewritten after source #2.
- **Gates must be trigger-based.** Templates and scaffolding should appear only after repeated real friction, not because they are easy to generate.

---

## Actors

- A1. Maintainer adding or reviewing a new source.
- A2. Coding agent asked to extend Civic Agent without overgeneralizing from Seattle.
- A3. Future external contributor proposing a civic finance source.
- A4. End user relying on Civic Agent answers to include source, grain, query logic, validation checks, and caveats.

---

## Requirements

**Immediate Direction**

- R1. The requirements must make source #2 the recommended next design input, not a contributor framework.
- R2. The requirements must preserve the option to add no contributor-facing artifact before source #2.
- R3. If a pre-source-2 artifact is added, it must be framed as a source-trust checklist, not a mature external contribution process.
- R4. Any pre-source-2 artifact must be explicitly provisional and must not claim to generalize across all civic finance sources.

**Source Trust Bar**

- R5. Every accepted source must identify its official or clearly justified trusted public source.
- R6. Every accepted source must state the jurisdiction, budget family, access method, primary measure, and answer grain.
- R7. Every accepted source must declare supported answer patterns and unsupported claims.
- R8. Every accepted source must include at least one validation check and visible caveats.
- R9. Every accepted source must include worked answer traces or demo prompts showing source, grain, measure, filters or query logic, validation check, and caveats.
- R10. A new jurisdiction must start with one clearly scoped source unless broader coverage is actually proven.

**Repo Hygiene**

- R11. Contributors must edit canonical jurisdiction files under `jurisdictions/`, not generated plugin references.
- R12. Any change to canonical router or jurisdiction skill files must refresh and check the plugin package with `python3 scripts/package_plugin.py` and `python3 scripts/package_plugin.py --check`.
- R13. The workflow must make router/source registry drift visible as a review concern until a future validator exists.

**Deferred Machinery**

- R14. The project must not add a source-card schema, source-intake template, eval runner, CI validation, issue forms, PR template, adapter framework, or `new_jurisdiction` script as part of the immediate contributor workflow.
- R15. A source-intake template should be considered only after two materially different sources exist and repeated source-evaluation questions are clear.
- R16. Jurisdiction scaffolding should be considered only after manual additions reveal stable repeated mistakes that a checklist or script would prevent.

---

## Recommended Sequence

| Stage | Trigger | Deliverable | Non-Deliverable |
|---|---|---|---|
| 0. Brainstorm | Now | This requirements brief | Any contributor implementation |
| A. Optional pre-source-2 checklist | Real near-term reviewer or agent need before source #2 | One-screen source-trust checklist, preferably near the existing architecture contract | Root contribution handbook, governance, templates, scripts |
| B. Source #2 | Next serious design input | One narrow, materially different source with metadata, caveats, validation checks, and answer traces | Broad jurisdiction promise |
| C. Post-source-2 rewrite | Source #2 merged and lessons are clear | Rewrite the checklist from two examples; decide whether a source-intake template adds value | Automatic template creation |
| D. Scaffolding | At least three additions or the same manual mistake corrected twice | Checklist or script that prevents observed mistakes | Speculative generator based on Seattle alone |

The primary path is Stage 0 to Stage B to Stage C. Stage A is allowed only as a small guardrail if someone needs to touch source structure before source #2 lands.

---

## Key Flows

- F1. Add source #2 first
  - **Trigger:** Maintainer decides to expand beyond Seattle.
  - **Actors:** A1, A2
  - **Steps:** Pick one narrow source; add source metadata and jurisdiction instructions; include supported and unsupported claims; add validation checks and worked answer traces; refresh and check the plugin package.
  - **Outcome:** The repo learns whether the Seattle-derived shape holds for a materially different source.
  - **Covered by:** R1, R5-R13

- F2. Optional pre-source-2 checklist
  - **Trigger:** A maintainer, agent, or contributor needs a written review bar before source #2.
  - **Actors:** A1, A2, A3
  - **Steps:** Add a short checklist that points to existing source-card, jurisdiction-skill, architecture, and packaging examples; mark it provisional; avoid onboarding or governance content.
  - **Outcome:** The repo gains a guardrail against unsafe source additions without creating new machinery.
  - **Covered by:** R2-R4, R11-R14

- F3. Revisit after source #2
  - **Trigger:** A second materially different source is merged.
  - **Actors:** A1, A2
  - **Steps:** Compare Seattle and source #2; separate general trust requirements from source-specific details; decide whether a template would reduce real review friction.
  - **Outcome:** Any contributor artifact is rewritten from evidence instead of Seattle-only assumptions.
  - **Covered by:** R15, R16

---

## Acceptance Examples

- AE1. A contributor wants to add a new Socrata city budget before Washington exists.
  - **Covers:** R2-R4, R5-R14
  - **Given:** The repo still has only Seattle.
  - **When:** They ask for a contribution workflow.
  - **Then:** The recommended response is either no new artifact yet or a provisional source-trust checklist; it does not add a scaffold, schema, or generic normalized budget model.

- AE2. A maintainer adds one Washington budget source.
  - **Covers:** R1, R5-R13
  - **Given:** The source is narrower than all Washington public finance.
  - **When:** The maintainer writes source metadata and skill instructions.
  - **Then:** The source declares what it can and cannot answer, includes validation checks and caveats, and does not imply broad Washington coverage.

- AE3. Two materially different sources now exist.
  - **Covers:** R15, R16
  - **Given:** Seattle and a second source have both been merged.
  - **When:** The team revisits contributor workflow.
  - **Then:** The team decides whether a source-intake template or checklist rewrite is justified by the actual differences and repeated questions.

---

## Scope Boundaries

Deferred for later:

- Root `CONTRIBUTING.md` as a broad external contributor handbook.
- Source-intake template.
- `scripts/new_jurisdiction.py`.
- Formal source-card JSON schema.
- Eval runner or CI checks for answer quality.
- GitHub issue forms or PR template.
- Normalized cross-jurisdiction data model.

Outside the immediate contributor-workflow identity:

- Claims that one source means Civic Agent supports an entire jurisdiction.
- Requirements that every jurisdiction support operating, capital, revenue, staffing, spending, and other budget families before being useful.
- Any rule that turns Seattle's fields, hierarchy, or live Socrata access pattern into a universal standard.

---

## Success Criteria

- S1. A maintainer can explain why source #2 is the next design input before contributor machinery.
- S2. A coding agent can add a narrow source without mistaking Seattle's data model for a universal schema.
- S3. A reviewer can reject unsupported civic-budget claims by checking official source, scope, supported patterns, unsupported claims, validation checks, caveats, and answer traces.
- S4. The repo does not gain new process surfaces that must be maintained before there is evidence they prevent real mistakes.

---

## Sources And Research

- Current repo contracts: `README.md`, `docs/architecture.md`, `docs/plan.md`, `skill.md`, `skills/civic-agent/SKILL.md`.
- Seattle exemplar: `jurisdictions/seattle/skill.md`, `jurisdictions/seattle/sources/operating-budget.source.json`, `docs/seattle-demo.md`.
- Packaging invariant: `scripts/package_plugin.py`.
- External reviewer synthesis: two rounds of Claude Companion and Oracle review. Both opposed scaffolding, schemas, evals, and templates now. Claude pushed hardest for source #2 first and a checklist only as an optional guardrail. Oracle agreed source #2 should be the default and reframed the artifact as a source trust contract rather than a contributor workflow.
