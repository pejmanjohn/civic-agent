# Goal Brief: Benchmark-Driven Launch Readiness

Date: 2026-07-13. Commit at time of writing: `ee95ebf`. Scorer type for all evidence in this brief: manual plus multi-agent research review; no automated answer eval exists yet.

## Trigger

Roadmap checkpoint. The maintainer asked two questions: (1) what data should be added or refined so Washington residents can ask thoughtful questions about their city, county, or state and get good answers; (2) how does the contribution experience become paved and validated enough to publish and get traction. A follow-up directive reframed both around measurement: the project should be benchmark-driven, with a trustworthy way to validate whether improvements move the user experience for a Washington citizen, replacing the single 2026-06-06 run (plugin 3.9 vs web 3.6) with something robust enough to hill-climb on.

## Evidence Inputs

- Threads: 2026-07-13 deep-dive session; 13-agent codebase/market research workflow; 3-agent benchmark-design workflow (two independent question-suite generators, one adversarial methodology critic).
- Benchmark files: `benchmarks/scale/cases.json`, `benchmarks/scale/2026-06-06-baseline.md`, `benchmarks/scale/manual-audit-template.md`, `docs/goals/eval-scoring-rubric.md`.
- Repo docs: `docs/plan.md`, `docs/architecture.md`, `docs/coverage-matrix.md`, `docs/recipes/scale.md`, `docs/processes/civic-agent-improvement-loop.md`, `docs/brainstorms/2026-06-04-contribution-workflow-requirements.md`, `docs/source-data-storage.md`, `docs/source-data-validation.md`.
- Source cards: all six accepted cards under `jurisdictions/*/sources/`.
- External/official references, verified live on 2026-07-13 unless noted:
  - SAO Financial Intelligence Tool OData v4 API at `https://portal.sao.wa.gov/FIT/api` — verified directly: `Snapshots(33)` is the 2025 Filing Milestone (published 2026-06-30, data 2015-2025, total revenues $85.49B, 1,701 filers); `Schedule1AggregationsByGovt` returned Tacoma (mcag `0610`) FY2024 totals (~$2.99B). Coverage: 281 cities/towns, 39 counties, 295 school districts, ~2,000 special districts including Sound Transit (mcag `0987`) and Seattle School District No. 1 (mcag `1903`, OSPI-sourced Schools route).
  - Pierce County Socrata: Open Budget `w2wc-2pqu` (FY2016-17+), transaction-level Open Checkbook `iwu2-biyj` (current through 2026) at `open.piercecountywa.gov`.
  - DOR Property Tax Statistics annual Excel levy/assessed-value tables; OSPI SAFS data files (F-196/F-195/S-275/apportionment/enrollment).
  - Seattle: verified via Socrata catalog that no checkbook/vendor-payment dataset exists; Capital Budget `m6va-m4qe` and Wage Data `2khk-5ukd` do.
  - Market: GSA/US Digital Corps MCP pilot (LLM accuracy on USASpending ~0% raw vs 95% with MCP; self-reported — read methodology before quoting); GRASP paper (arXiv 2503.23299, domain-tuned budget agents 78% vs GPT-4o 60%); `npstorey/civic-ai-tools` (all 559 Socrata portals covered, ~33 stars); ClearGov AI citizen budget platform launch (May 2026, secondhand); OpenElections contributor model; Code for America brigade shutdown; `anthropics/claude-plugins-official` civic/gov category nearly empty.

## Raw Observations

Facts, separated from interpretation:

1. The hosted fresh-agent path cannot answer WA Open Checkbook questions: answers require a managed local SQLite built from a ~411MB XLSX; the hosted path dead-ends with "managed local data is not set up."
2. `jurisdictions/washington/skill.md` embeds an absolute `/Users/pejman/...` path that ships verbatim into the packaged plugin.
3. There is no `.github/` directory: no CI runs the unittest suite, `package_plugin.py --check`, or coverage regeneration.
4. `--refresh-check` is a stub for every source; live-tier Seattle validation never touches the network; drift is invisible until an answer is wrong.
5. Four test files hardcode per-source-id expectations (`test_source_coverage.py`, `test_source_storage_policy.py`, `test_source_data_validation.py`, `test_benchmark_contract.py`), so adding a source edits shared test modules.
6. Exactly one benchmark run exists (2026-06-06, n=4, self-scored, unblinded); `cases.json` has changed since (milestones 5-6) with no rerun. The composite delta (3.9 vs 3.6) is within single-rater noise for n=4.
7. The 2026-06-04 contribution brainstorm deferred all contributor machinery until 2-3 materially different sources existed. Six sources across four shapes (Socrata live, two Power BI snapshot surfaces, XLSX managed DB, XLSX snapshots) now exist; Stage C/D deliverables never shipped.
8. Demand research (2025-26 WA news cycles) ranks the top resident question archetypes: property tax bills (#1), new 2025-26 state taxes, persistent deficits after tax hikes, homelessness spending accountability (KCRHA audit), school district cuts (SPS $104M deficit, ~100 districts cutting). Zero of the top five archetypes are answerable from accepted sources today.
9. The OFM population snapshot already contains every WA city and town — an unused disambiguation asset for unsupported-jurisdiction questions.
10. FIT provides filed annual actuals (BARS Schedule 01, cash and GAAP filers flagged) — not adopted budgets. Its API is undocumented and internal to the FIT SPA.
11. Coverage matrix backlog (12 families x 3 jurisdictions) carries no prioritization signal; there is no user feedback channel of any kind.
12. Marketplace keyword lists are hand-synced and stale (missing `king-county` in `.claude-plugin/marketplace.json`); root `skill.md` is not covered by the reference-sync tests and has drifted in wording from the installable SKILL.md.

## Plugin vs Baseline Gap

From the 2026-06-06 baseline plus this loop's demand research:

| Question | Plugin behavior | Baseline behavior | Gap |
|---|---|---|---|
| Seattle operating budget size | $7.312B FY2026 with trace (4.7) | Official pages, less precise framing (4.2) | Adjacent budget frames missing |
| King County budget size | $8.599B FY2026 dashboard (3.6) | $20.16B biennial framing (4.4) | Frame reconciliation; worst plugin loss was `semantic_mismatch` |
| 5-10 year trend | Reproducible nominal trends (4.2) | No reproducible table (2.5) | Inflation/population adjustment missing |
| Per-resident budget | Unsupported at the time (2.7) | Manual synthesis possible (3.3) | Since addressed by `washington.ofm_population` — unverified by any rerun |
| Top-5 demand archetypes (property tax, new taxes, deficits, homelessness, schools) | Not represented in any benchmark case; mostly unanswerable | Web answers exist but uncited/unreliable | The benchmark does not measure what residents actually ask |

## Failure Modes

- `missing_source`: property tax, schools, all non-Seattle cities, all non-King counties, special districts, Seattle/KC actuals.
- `scorer_gap`: n=4, one run ever, composite averages, no mechanical checks, no noise floor, expensive protocol that was never repeated.
- `packaging_or_install_drift`: no CI; stale marketplace keywords; absolute path shipped in plugin; root router outside sync tests.
- `freshness_unclear`: `--refresh-check` stubs; live tier never validated at answer time; hardcoded validation constants rot silently.
- `validation_gap`: hosted checkbook path unanswerable; `hosted_artifact` tier documented but unimplemented.
- `semantic_mismatch`: the one recorded benchmark loss (KC annual dashboard vs adopted biennial); FIT (filed actuals) multiplies this risk at 2,300-jurisdiction scale if not vocabulary-walled.
- `unsupported_question`: router gives a flat "not yet included" for every WA jurisdiction beyond three, despite OFM containing every city.

## Blind Review Summary

Two adversarial reviews were run: a strategy critique over three competing lens proposals (data-depth-first, contributor-wedge-first, launch-first), and a benchmark-methodology critique over the draft eval design.

- Agreements: launch-first's diagnosis is best supported (one benchmark run, zero known users, breadth-without-users is the documented graveyard); CI plus a contribution runbook is the cheapest high-leverage change; the hosted checkbook dead-end and shipped absolute path are launch blockers; Tier 0 deterministic coverage scoring is the strongest part of the benchmark design.
- Disagreements: FIT sequencing (data-depth wanted it first, launch-first deferred it). Resolution: benchmark first, then FIT, so FIT's impact is measured, not asserted. The critic also rejected several benchmark features the draft included (see Extracted Principles).
- Additional risks surfaced: accuracy liability (a confidently mis-cited government finance number to a journalist is the existential failure; no corrections protocol exists); solo-maintainer refresh arithmetic (7+ sources x annual refresh x hand-copied constants) grows before refresh tooling exists; FIT is an undocumented internal API (pin milestone snapshot IDs, monitor the `Datasets` endpoint, open an SAO relationship); scoring one's own system blind is theater — replace with mechanical asymmetry and an external spot-check.
- Ranking changes: the benchmark moved from a Phase-4 launch artifact to Goal #1, per the maintainer's directive and the critic's cost-realism finding: an eval built after the improvements cannot attribute them.

## Extracted Principles

1. Benchmark before build: record expected case movement before implementation (existing repo rule), which requires the instrument to exist before the next source lands.
2. The always-on metric must be deterministic and free. Human-touched evaluation must fit in 90 minutes or it will not be repeated — the 2026-06-06 protocol died of cost.
3. Never headline a mean score. Report per-case win/tie/loss; claim improvement only when enough cases flip in one direction (sign test discipline, threshold set by a measured noise floor).
4. Expectations ratchet one way. `expected_answer_mode` may only move `unsupported_with_path -> partial -> exact`; any downgrade requires a linked justification and fails CI otherwise. Question text is immutable; expectations are versioned per run.
5. Include questions the system cannot answer. Graceful failure (`unsupported_with_path` with a named path, no fabrication) is a scored behavior, and uncovered questions are what make the benchmark a coverage-growth instrument.
6. A source is done when its benchmark case moves: accepted source + validation + coverage claim + recipe + benchmark case (extends the existing principle).
7. Prefer one source that covers many jurisdictions (FIT, DOR, OSPI) over per-city integrations; vocabulary-wall filed actuals from adopted budgets exactly as checkbook payments are walled today.
8. Point-in-time baselines only. Plugin-vs-web comparisons are a same-day contest, never a longitudinal series — the web, the model, and the scorer all drift.
9. External pressure or it is homework the maintainer grades themselves: fresh annex questions sourced verbatim from real residents; a quarterly 5-case external spot-check with a published agreement rate.

## Ranked Goals

| Rank | Goal | Evidence | Why now | Not now |
|---|---|---|---|---|
| 1 | WA-20 citizen benchmark: cases + Tier 0 coverage scorer in CI + Tier 1 runner with mechanical scoring + noise-floor double-run | Observations 6, 8, 11; methodology critique | Every later goal states expected movement against it; it converts the 12-family backlog into a prioritized surface | No LLM judge (revisit above ~100 cases); no longitudinal web-baseline claims |
| 2 | Launch-blocker fixes: hosted checkbook aggregates, strip absolute path, CI, nightly drift check, OFM-based jurisdiction disambiguation | Observations 1-4, 9, 12 | Cheap (all S); CI and drift checks are also eval-validity prerequisites | Full refresh-tooling suite; `hosted_artifact` SQLite can follow the JSONL aggregates |
| 3 | FIT statewide source: probe brief, card pinned to milestone snapshots, extractor, vocabulary walls, benchmark cases before announcement | FIT verified live; expected to move 6+ WA-20 cases | The single largest coverage move available; makes "is my city covered" answer yes statewide | Peer-comparison recipe ships only after FIT semantics are proven on covered cases |
| 4 | Demand sources: Pierce County Socrata (budget + checkbook), DOR property-tax levy tables | Verified endpoints; demand archetypes #1, #14 | Pierce is the cheapest fourth jurisdiction on the existing stack; property tax is the #1 resident question | OSPI per-pupil depth (FIT Schools route covers district Q&A first); capital/transportation budgets; fiscal notes; salaries; per-city ArcGIS/Questica |
| 5 | Contribution wedge: CONTRIBUTING runbook, source-card JSON Schema, registry-driven tests (additive-only sources), scaffold/intake skill, benchmark-case definition of done | Observations 5, 7; OpenElections model | Stage C/D triggers fired; FIT + Socrata golden paths make an afternoon contribution literally true | Governance docs, issue forms beyond a question-intake template, MCP server |
| 6 | Launch: worked demos (any-WA-city via FIT; checkbook with real numbers), plugin-directory submission, ten named outreach targets, feedback links in the answer contract, point-in-time Tier 2 comparison published | Market research; empty civic category in official directory | Users are the missing input to every loop above | Web demo (only if outreach proves CLI friction); paid infra |

## Contract Changes Needed

- Benchmark cases: new `benchmarks/wa-citizen/` bucket — `cases.json` (20 cases, schema below), `expectations/` versioned per run, `runs/YYYY-MM-DD/`, generated `scoreboard.md`, `annex/` for fresh resident-sourced questions. Case schema adds to the scale-bucket shape: immutable block (id, question, persona, altitude, jurisdiction, archetype, difficulty), versioned block (`expected_answer_mode`, `expected_source_ids`, `expected_facts` as `{value, tolerance, reproduction_ref}`, `required_caveats` as `{id, pattern}`), plus `unlocked_by`. Extend `tests/test_benchmark_contract.py` to validate both buckets and enforce the one-way mode ratchet.
- Source cards: FIT, Pierce County, DOR property tax (each: probe brief first per `docs/source-probing.md`); publish a source-card JSON Schema extracted from existing test assertions.
- Recipes: jurisdiction-disambiguation behavior for unsupported WA jurisdictions (state facts + OFM denominator + named path); a FIT peer-comparison recipe gated on proven semantics.
- Router/skills: strip absolute paths; bring root `skill.md` under sync tests; `unsupported_with_path` protocol references the disambiguation recipe.
- Validation/tests: Tier 0 coverage scorer in CI failing loudly on stale snapshots; nightly live-drift job running existing validation checks; registry-driven test expectations replacing hardcoded per-source constants.
- Packaging/dev workflow: GitHub Actions (unittest, `package_plugin.py --check`, coverage regen check, Tier 0, runner smoke-test on one case); marketplace keyword check in `package_plugin.py`; de-personalize `scripts/dev.py`.
- Eval/scoring: `scripts/eval.py` mechanical scorer per the improvement-loop spec (source ids, answer mode, caveat patterns, numeric facts with tolerance, averages worksheet); human scoring confined to `civic_usefulness` on 5 anchor cases; auto-generated scoreboard.

## Milestone Queue

| Milestone | Goal | Acceptance |
|---|---|---|
| M1: WA-20 cases | 1 | `benchmarks/wa-citizen/cases.json` with 20 cases from the appendix; contract test validates schema and ratchet; CI green |
| M2: Tier 0 coverage scorer | 1 | Script maps cases to required claims against source cards/coverage matrix; emits per-case expected-achievable mode + coverage %; fails loudly on stale snapshots; runs in CI; scoreboard generated |
| M3: Launch-blocker fixes | 2 | Hosted checkbook JSONL aggregates checked in and routed in the WA skill; no absolute paths in packaged plugin (tested); GitHub Actions live; nightly drift job live; marketplace keywords checked |
| M4: Tier 1 runner + noise floor | 1 | Runner captures answers to `runs/`; mechanical scorer works on all 20; two same-config runs recorded; noise floor documented in the run README; human protocol is 5 anchor cases and fits 90 minutes |
| M5: Disambiguation | 2 | Unsupported-WA-jurisdiction questions return state facts + OFM population + named path; the two graceful-failure benchmark cases score full marks mechanically |
| M6: FIT source | 3 | Probe brief, card (milestone-snapshot pinned, actuals vocabulary walls), extractor, snapshot, validation; Tier 0 shows >=5 cases moving to achievable-partial; Tier 1 rerun on affected cases before coverage is announced |
| M7: Pierce + DOR | 4 | Two accepted cards with validation and demo traces; affected cases move per Expected Eval Movement |
| M8: Contribution wedge | 5 | CONTRIBUTING runbook; JSON Schema; registry-driven tests (adding a source touches no shared module); scaffold/intake path documented; a new-source PR checklist requires a benchmark case |
| M9: Launch | 6 | Worked any-WA-city + checkbook demos; directory submission; outreach to ten named targets; feedback links live; one point-in-time Tier 2 comparison published with per-case results |

## Expected Eval Movement

Recorded before implementation, per repo rule. Case ids reference the appendix suite.

| Case | Expected improvement | Why |
|---|---|---|
| `wa-checkbook-vendor-lookup` | Hosted path: dead-end -> partial | M3 checked-in aggregates |
| `walla-walla-city-budget`, `pierce-county-budget-size` | Graceful-failure quality: fabrication-risk -> full-marks `unsupported_with_path` | M5 disambiguation |
| `spokane-police-vs-housing`, `evergreen-schools-cuts`, `sound-transit-car-tabs`, `kc-actuals-vs-budget-trap`, `sps-deficit-school-closures`, `walla-walla-city-budget` | `unsupported_with_path` -> partial (FIT actuals, correctly walled) | M6 |
| `seattle-kc-homelessness-kcrha` | partial -> stronger partial (KCRHA files with SAO) | M6 |
| `pierce-county-budget-size` | partial -> exact; `pierce-vs-king-per-resident` partial -> exact | M7 Pierce |
| `kc-property-tax-why-up`, `school-levy-household-cost`, `kc-cuts-despite-20b` | `unsupported_with_path`/side-by-side -> partial | M7 DOR |
| `wa-new-taxes-actually-collecting` | needs_refresh -> partial | Revenue snapshot refresh discipline (M3 drift job surfaces it) |
| Tier 0 coverage % | ~35% of cases achievable today -> ~75% after M7 | Sum of the above |
| Tier 2 point-in-time | No numeric target; publish per-case win/tie/loss | Baselines are not longitudinal |

## Handoff Prompt For /ce-plan

```text
Use this goal brief to create a repo-scoped implementation plan for Civic Agent.

Scope: benchmarks/wa-citizen/ (new), scripts/eval.py (new), .github/workflows/ (new), plus touched routers/skills/cards named in Contract Changes.

Top-ranked goal: WA-20 citizen benchmark (M1, M2, M4) and launch-blocker fixes (M3, M5), in that order; data sources (M6, M7) only after the instrument exists.

Evidence: docs/goals/2026-07-13-benchmark-driven-launch-goal.md, benchmarks/scale/2026-06-06-baseline.md, docs/processes/civic-agent-improvement-loop.md.

Required contract changes: see Contract Changes Needed section.

Expected eval movement: see Expected Eval Movement section; movement claims require the noise-floor double-run from M4 first.

Constraints:
- Keep implementation milestones reviewable.
- Preserve package/install provenance.
- Do not replace manual civic usefulness scoring with an unvalidated model judge.
- Never headline a mean score; per-case win/tie/loss with the ratchet-checked mode distribution is the headline.
- Human-touched eval work must fit in 90 minutes per run.
- Question text in cases.json is immutable once merged; expectations move only via the one-way ratchet with linked justification.
```

## Appendix A: WA-20 Candidate Suite

Merged from two independently generated suites (persona lens and coverage-grid lens); the full 40-candidate pool is preserved for the fresh-questions annex. Distribution: 6 T1 lookup / 8 T2 composition / 6 T3 interpretation; altitudes 5 city / 5 county / 4 state / 3 school district / 1 special district / 2 multi; 9 jurisdictions including Eastern Washington. Modes are expectations under coverage as of 2026-07-13.

| # | Case id | Question (primary phrasing) | Persona | Altitude | Tier | Mode today | Unlocked by |
|---|---|---|---|---|---|---|---|
| 1 | `seattle-parks-2026-lookup` | What does Seattle budget for parks in 2026? | Green Lake resident | city | T1 | exact | covered (quality anchor) |
| 2 | `kc-sheriff-budgeted-fte-2026` | How many positions does the King County Sheriff's Office have in the 2026 budget? | Council staffer | county | T1 | exact | covered |
| 3 | `wa-operating-total-2025-27` | How big is Washington state's operating budget? | First-time voter | state | T1 | exact | covered; must name fund view and note the 2026 supplemental is out of scope |
| 4 | `wa-checkbook-vendor-lookup` | Which vendors got the most money from Washington state last year? | Journalist | state | T1 | exact locally; dead-end hosted | M3 hosted aggregates |
| 5 | `pierce-county-budget-size` | How big is Pierce County's budget and what do they spend it on? | Tacoma small-business owner | county | T1 | unsupported_with_path | Pierce Socrata; FIT actuals |
| 6 | `walla-walla-city-budget` | What is the City of Walla Walla's budget? | Walla Walla retiree | city | T1 | unsupported_with_path (fabrication trap: small town) | FIT |
| 7 | `spd-budget-2020-vs-2026` | How has Seattle's police budget changed since 2020? | Seattle renter | city | T2 | exact | covered (trend anchor) |
| 8 | `spokane-police-vs-housing` | How much does Spokane spend on police compared to housing and homelessness? | Spokane tenants-union member | city | T2 | unsupported_with_path | FIT (BARS function categories) |
| 9 | `evergreen-schools-cuts` | Evergreen Public Schools keeps cutting teachers — is the district actually getting less money? | Vancouver WA parent | school_district | T2 | unsupported_with_path | FIT Schools; OSPI per-pupil later |
| 10 | `sound-transit-car-tabs` | I pay Sound Transit car tabs — how much does Sound Transit take in and spend? | Tacoma commuter | special_district | T2 | unsupported_with_path | FIT (mcag 0987); ST3 program gap stays out of scope |
| 11 | `kc-actuals-vs-budget-trap` | Did King County actually spend what it budgeted last year? | Auditor-minded resident | county | T2 | unsupported_with_path (fabrication trap: only budgets exist) | FIT actuals enable budget-vs-actual |
| 12 | `pierce-vs-king-per-resident` | Does Pierce County spend more or less per resident than King County? | Regional reporter | multi | T2 | partial | Pierce Socrata + OFM (denominator already accepted) |
| 13 | `wa-new-taxes-actually-collecting` | Are the new 2025 state taxes actually bringing in the money that was projected? | Small-business owner | state | T2 | needs_refresh | Revenue snapshot refresh; ERFC forecast source later |
| 14 | `school-levy-household-cost` | What would the school levy on my ballot cost my household? | School-board voter | school_district | T2 | unsupported_with_path | DOR levy tables + median AV |
| 15 | `sps-deficit-school-closures` | Why is Seattle Public Schools closing schools? Where does their money actually go? | SPS parent | school_district | T3 | unsupported_with_path | FIT (mcag 1903); OSPI F-196 |
| 16 | `kc-property-tax-why-up` | Why did my King County property tax bill go up ~10% this year? | Homeowner | county | T3 | unsupported_with_path | DOR levy tables + assessor levy detail |
| 17 | `kc-cuts-despite-20b` | Why is King County cutting services if its budget is $20 billion? | Skeptical taxpayer | county | T3 | side_by_side_only | DOR levy-lid context; general-fund vs dedicated framing |
| 18 | `seattle-2026-deficit-jumpstart` | How did Seattle close its deficit, and what happened to the JumpStart money? | PubliCola reader | city | T3 | partial | Fund-grain revenue context; ordinance history stays out of scope |
| 19 | `seattle-kc-homelessness-kcrha` | How much have Seattle and King County spent on homelessness, and where did it go? | Journalist | multi | T3 | partial (refusal-discipline heavy) | FIT (KCRHA files with SAO); fragmentation is part of a correct answer |
| 20 | `wa-deficit-after-historic-taxes` | Why does Washington still have a budget shortfall after the biggest tax package in state history? | Statewide voter | state | T3 | partial | Revenue estimate-vs-actual (covered) + four-year outlook source later; must state modeling choices |

Deliberately unrepresented (recorded so exclusion is a decision, not an accident): ferries/electrification (archetype 12), levy-delivery oversight (archetype 15), fiscal notes, state salaries. Candidates for annex rotation.

## Appendix B: Benchmark Architecture

Three tiers; the only always-on tier is deterministic and free.

- Tier 0 — coverage score (CI, every commit, no LLM). Maps each case to required claims and checks them against accepted source cards, coverage claims, and snapshot freshness. Emits per-case expected-achievable answer mode and a repo-wide WA-20 coverage %. Fails loudly on stale snapshots. This is the continuous hill-climb signal and the headline metric alongside the achieved-mode distribution.
- Tier 1 — answer score (per milestone, target under 90 minutes of human time). Runner executes plugin prompts in isolated sessions, saves markdown to `runs/YYYY-MM-DD/`. `scripts/eval.py` mechanically checks expected source ids, answer mode, caveat patterns (`{id, pattern}`), and numeric facts within tolerance for all 20 cases. Humans score `civic_usefulness` on 5 designated anchor cases only (1, 4, 12, 16, 19 — one per stratum), explicitly labeled author-scored and unblinded. Runner smoke-tests in CI on one case so it does not bit-rot between runs.
- Tier 2 — web-baseline contest (annual, and at launch; only after two Tier 1 runs have occurred). Same 20 questions against a plain web-search agent, same day, same model. Per-case win/tie/loss published; no composite headline; no cross-year baseline comparisons ever claimed.

Validity rules (from the adversarial methodology review):

1. Noise floor first: before any improvement claim, run the same config twice and publish the test-retest spread; the observed spread is the significance threshold. Expect single-rater noise around +/-0.5 per case; do not claim a real delta on the 20-case set unless roughly 6+ cases flip the same direction.
2. One-way expectation ratchet, CI-enforced; downgrades require a linked justification issue. The expectation-change log publishes next to the scoreboard.
3. No paraphrase sampling in scored runs. Paraphrase variants run only as a Tier 0-style robustness bit (same answer mode across phrasings: yes/no).
4. No LLM judge below ~100 cases: validating one costs more human scoring than it saves.
5. External pressure: annex questions collected verbatim from real residents (council public comment, community forums, reader questions via the feedback link), not authored by the maintainer; quarterly, one outside person scores 5 cases and the agreement rate is published.
6. Every run records commit, package/install state, and snapshot versions per the existing improvement-loop validity checklist.
