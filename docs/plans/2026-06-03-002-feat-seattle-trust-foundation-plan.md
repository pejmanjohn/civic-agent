---
title: "docs: Publish Seattle demo answer traces"
status: completed
date: 2026-06-03
type: docs
---

# docs: Publish Seattle demo answer traces

## Summary

Make Seattle the credible first demo for Civic Agent by publishing worked, source-backed answers for the existing dogfood prompts, adding explicit safe/unsupported answer boundaries to the Seattle source card, and adding compact answer-trace guidance to the existing skills. This plan intentionally avoids schemas, eval fixtures, validators, snapshots, dashboards, broad concept glossaries, and contributor scaffolding until the project has either a second real source or an actual answer/eval runner.

---

## Problem Frame

Civic Agent is currently a small agent-readable skill/plugin repo with one concrete source: Seattle's operating-budget Socrata dataset. The repo already has the right primitives for this stage: jurisdiction-first files, official-source routing, Seattle query recipes, validation checks, interpretation rules, and Codex/Claude Code packaging.

The missing proof is not a framework. The missing proof is the finished Seattle experience: a reader should be able to see what Civic Agent can answer, what it cannot answer, where the numbers came from, and which caveats constrain them. That should be delivered as a demo and tight source/skill guidance, not as formal schemas or evals that cannot yet evaluate real agent output.

---

## Requirements

**Answer Trace**

- R1. Source-backed answers include a compact trace: source, grain, filters or query logic, validation check or row count when useful, and caveats.
- R2. Router and Seattle skill guidance make the trace expectation visible without turning the skill into a long process document.

**Seattle Source Boundary**

- R3. Seattle's existing `jurisdictions/seattle/sources/operating-budget.source.json` is enriched in place with safe answer patterns and unsupported claims.
- R4. The enriched source card preserves current useful metadata: Socrata ID, official endpoints, known years, primary measure, hierarchy fields, validation checks, and caveats.
- R5. The source card explicitly prevents overclaiming: it should not be used for actual payments, realtime city activity, staffing/headcount, capital budget, or non-Seattle budget analysis.

**Seattle Demo**

- R6. `docs/seattle-demo.md` provides worked, source-backed answers for the current dogfood prompts in `docs/plan.md`.
- R7. Each demo answer includes enough trace detail for auditability without becoming a query-engine spec.
- R8. The demo is legible to a non-developer reader who does not know Socrata, SoQL, or Seattle's budget schema.

**Documentation and Packaging**

- R9. README, examples, architecture, and repo plan point readers to the Seattle demo and do not imply formal evals or validators exist.
- R10. Plugin packaging remains in sync for generated Seattle references after the Seattle skill changes.

---

## Key Technical Decisions

- KTD1. **Demo first, framework later.** The milestone proves Civic Agent's current value by showing trusted Seattle answers, not by building a general trust architecture.
- KTD2. **Use the existing source card.** Add `safe_answer_patterns` and `not_supported_by_this_source` to `jurisdictions/seattle/sources/operating-budget.source.json`; do not introduce schema or eval directories.
- KTD3. **Treat dogfood prompts as demo prompts, not eval fixtures.** Until there is an answer runner, calling prompt cases "evals" would overstate enforcement.
- KTD4. **Keep answer-trace guidance inline and small.** Add the trace expectation to existing router/Seattle skill surfaces rather than creating separate shared references or packaging logic.
- KTD5. **Do not add snapshots for clean live data.** Seattle's live Socrata source and existing validation checks are enough for this milestone; demo traces can include access context and query logic.

---

## Scope Boundaries

### In Scope

- In-place Seattle source-card enrichment.
- Worked Seattle demo answers for the dogfood prompts.
- Compact answer-trace guidance in existing router and Seattle skill docs.
- README, examples, architecture, plan, and generated plugin-reference updates needed to expose the demo.

### Deferred to Follow-Up Work

- Formal JSON schemas for source cards, answer traces, or eval suites.
- Eval JSON fixtures or claims that dogfood prompts are machine-checkable.
- Validation harnesses and test fixtures.
- Checked-in FY2026 summary/provenance data artifacts.
- Source-status dashboard or status document.
- Broad shared civic-budget glossary.
- Contributor adapter templates and `new_jurisdiction` scaffolding. The user wants to brainstorm this separately after the Seattle demo is clear.
- Full executable query/adapter CLI such as `civic-agent query`, `inspect`, `snapshot`, or `validate`.
- Mandatory live Socrata validation in CI.
- Claim-checker, resident lens, public-meeting prep, and analysis-mode UX.
- Inflation-adjusted, per-capita, share-of-total, or general-fund-normalized views.
- Washington messy-source adapter and related extractor/normalizer work.
- Cross-jurisdiction normalized budget schema.

### Non-Goals

- Do not redesign plugin distribution or packaging.
- Do not imply Seattle snapshots are the source of truth while the live Socrata source remains clean.
- Do not imply all future jurisdictions will expose Seattle's fields, measures, or question types.

---

## Implementation Units

### U1. Add Seattle source boundaries and answer-trace guidance

- **Goal:** Make the Seattle source's safe answer surface and answer-trace expectation explicit.
- **Requirements:** R1, R2, R3, R4, R5.
- **Dependencies:** none.
- **Files:**
  - `jurisdictions/seattle/sources/operating-budget.source.json` (modify)
  - `jurisdictions/seattle/skill.md` (modify)
  - `skill.md` (modify)
  - `skills/civic-agent/SKILL.md` (modify)
- **Approach:** Add concise safe answer patterns and unsupported claims to the existing source metadata. Add a short answer-trace section to the Seattle skill and a router-level reminder that source-backed answers should include conclusion, numbers, source, grain, query/filter logic, validation check or row count when useful, and caveats.
- **Patterns to follow:** Existing Seattle skill sections for `Validation Checks`, `Interpretation Rules`, and `Answer Style`; existing source metadata style in `jurisdictions/seattle/sources/operating-budget.source.json`.
- **Test scenarios:**
  - Happy path: a Seattle operating-budget answer can cite the source card's safe answer patterns and include the trace fields named by the skill.
  - Edge case: actual payments, staffing/headcount, capital budget, realtime activity, and non-Seattle claims are explicitly unsupported by the Seattle source card.
  - Edge case: policy questions still require separating budget facts from interpretation.
- **Verification:** The Seattle source boundary is clear from the source metadata, and the skill guidance asks for traceable source-backed answers without adding a new framework.

### U2. Publish worked Seattle demo answers

- **Goal:** Show the current Seattle dogfood prompts answered in the style Civic Agent should produce.
- **Requirements:** R6, R7, R8.
- **Dependencies:** U1.
- **Files:**
  - `docs/seattle-demo.md` (create)
  - `docs/plan.md` (modify)
  - `examples/prompts.md` (modify)
- **Approach:** Write worked answers for the existing dogfood prompts: FY2026 top spending, Police vs Fire, Police vs Fire vs Human Services, Police program drill-down, biggest negative rows, labor vs non-labor, and department-growth chart readiness. Each answer should lead with the plain-English conclusion, show the important numbers, and include a compact trace with source, accessed date, grain, measure, filters/query logic, validation checks or row counts, and caveats. Use raw query syntax sparingly; prefer plain-English query logic in the demo.
- **Patterns to follow:** Dogfood prompts in `docs/plan.md`; Seattle query recipes and validation checks in `jurisdictions/seattle/skill.md`; answer style in the Seattle skill.
- **Test scenarios:**
  - Happy path: every dogfood prompt in `docs/plan.md` is represented in `docs/seattle-demo.md`.
  - Edge case: "largest department" examples include the caveat that utility and enterprise fund budgets can dominate totals and are not equivalent to discretionary priorities.
  - Edge case: negative-row examples explain that negative rows are real budget/accounting rows, not automatic data errors.
  - Chart-ready path: the department-growth prompt produces a chart-ready table description without requiring a chart renderer.
- **Verification:** A reader can open the demo and understand what Civic Agent can answer, how the numbers were obtained, and what the answer does not prove.

### U3. Sync docs and packaged references

- **Goal:** Keep public docs and generated plugin references aligned with the demo-answer-trace milestone.
- **Requirements:** R9, R10.
- **Dependencies:** U1, U2.
- **Files:**
  - `README.md` (modify)
  - `docs/architecture.md` (modify)
  - `docs/plan.md` (modify)
  - `examples/prompts.md` (modify)
  - `plugins/civic-agent/skills/civic-agent/SKILL.md` (generated)
  - `plugins/civic-agent/skills/civic-agent/references/seattle.md` (generated)
- **Approach:** Keep docs focused on what exists now: Seattle source-card boundaries, answer traces, and the worked demo. Do not describe schemas, validators, snapshots, or evals as current behavior. Run the existing packaging script so generated router and Seattle references match canonical files.
- **Patterns to follow:** Existing `scripts/package_plugin.py --check` flow; README plugin install and routing sections.
- **Test scenarios:**
  - Happy path: `python3 scripts/package_plugin.py --check` passes after regeneration.
  - Integration: generated plugin router and Seattle reference match canonical files.
  - Integration: README and examples point users to `docs/seattle-demo.md` for worked examples.
- **Verification:** Hosted repo docs and packaged plugin references present the same answer-trace behavior and Seattle source boundaries.

---

## Acceptance Examples

- AE1. A user asks "Where does Seattle spend the most money in FY2026?" and the demo shows a short answer plus trace with source, grain, query logic, validation checks, and caveats.
- AE2. A user asks whether Civic Agent can answer Seattle staffing or actual-spending questions from the operating-budget source, and the source card makes the unsupported claim clear.
- AE3. A future contributor can understand a source card as a source capability declaration, not a required shared metric model.
- AE4. The packaged `/civic-agent` install has the same answer-trace guidance as the source repo.
- AE5. The repo plan no longer implies that dogfood prompts are machine-checkable evals before an eval runner exists.

---

## Risks & Mitigations

- **Too little enforcement:** Cutting schemas and validators means this milestone relies on prose and review. Mitigation: keep the answer-trace guidance concise enough that agents actually follow it, and revisit executable checks when there is a runner or second source.
- **Demo staleness:** Worked answers can drift if the Seattle source changes. Mitigation: include accessed date and query logic in each trace, and avoid claiming demo numbers are timeless.
- **Under-specifying future contributors:** Without templates, contributors still need judgment. Mitigation: defer contributor templates intentionally and brainstorm them after the Seattle demo is visible.
- **Doc sprawl:** The demo could become too long or query-heavy. Mitigation: keep answers readable, use plain-English query logic, and only include raw query details when they help auditability.

---

## Documentation Notes

- README should introduce the Seattle demo as the best way to understand the project quickly.
- `docs/architecture.md` should mention answer traces as part of routing/answer style, not a separate validation framework.
- `docs/plan.md` should mark dogfooding as represented by the demo and note that formal evals are deferred until there is a runner.
- `examples/prompts.md` should link to `docs/seattle-demo.md` for worked examples.
- Contributor-template work should be named as the next brainstorm target after this plan, not implemented as part of it.

---

## Sources and Research

- Existing router and installable skill: `skill.md`, `skills/civic-agent/SKILL.md`.
- Seattle source instructions and checks: `jurisdictions/seattle/skill.md`.
- Existing source metadata: `jurisdictions/seattle/sources/operating-budget.source.json`.
- Packaging and generated reference pattern: `scripts/package_plugin.py`, `plugins/civic-agent/skills/civic-agent/references/seattle.md`.
- Current dogfood prompt list: `docs/plan.md`, `examples/prompts.md`.
