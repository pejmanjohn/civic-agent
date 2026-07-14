# Tier 1 Worksheet - 2026-07-14-run-c

Mechanical results are in results.json. Human judgment is ONLY `civic_usefulness` (0-5 per docs/goals/eval-scoring-rubric.md) on the anchor cases below - author-scored, unblinded, and labeled as such. Do not re-score mechanical dimensions by hand.

| Anchor case | Mechanical | civic_usefulness (0-5) | Notes |
|---|---|---|---|
| `seattle-parks-2026-lookup` | 5/5 | 5 | Trace should include clickable URLs wherever possible so a reader can explore sources. |
| `wa-checkbook-vendor-lookup` | 4/5 | 5 | Good answer; the Trace is hard to read as a human. |
| `pierce-vs-king-per-resident` | 3/9 | 5 |  |
| `kc-property-tax-why-up` | 7/7 | 4 | Should ask which city the resident lives in and offer a levy/bond lookup that could explain the increase. |
| `seattle-kc-homelessness-kcrha` | 6/8 | 4 | Hard to process; a chart would help for changes over time. |

Per-case mechanical failures (fix the capture or record as findings):

- `kc-sheriff-budgeted-fte-2026` / answer_mode: expected 'exact', got 'partial'
- `wa-checkbook-vendor-lookup` / answer_mode: expected 'exact', got 'partial'
- `pierce-county-budget-size` / source:pierce_county.open_checkbook: expected 'cited', got 'absent'
- `spokane-police-vs-housing` / answer_mode: expected 'partial', got 'unsupported_with_path'
- `sound-transit-car-tabs` / answer_mode: expected 'partial', got 'exact'
- `sound-transit-car-tabs` / caveat:st3-gap-out-of-scope: expected 'Separates filed actuals from ST3 capital-program projections.', got 'not found'
- `kc-actuals-vs-budget-trap` / answer_mode: expected 'partial', got 'side_by_side_only'
- `pierce-vs-king-per-resident` / answer_mode: expected 'partial', got 'exact'
- `pierce-vs-king-per-resident` / source:king_county.open_budget_dashboard: expected 'cited', got 'absent'
- `pierce-vs-king-per-resident` / source:pierce_county.open_budget: expected 'cited', got 'absent'
- `pierce-vs-king-per-resident` / caveat:period-mismatch-named: expected 'Names the biennial-vs-annual period mismatch instead of silently annualizing.', got 'not found'
- `pierce-vs-king-per-resident` / fact:king-county-2025-population: expected 2411700, got 'not found'
- `pierce-vs-king-per-resident` / fact:pierce-county-2025-population: expected 959900, got 'not found'
- `kc-cuts-despite-20b` / source:washington.dor_property_tax_levies: expected 'cited', got 'absent'
- `kc-cuts-despite-20b` / caveat:general-vs-dedicated: expected 'Explains the general-fund vs dedicated-funds distinction at the heart of the paradox.', got 'not found'
- `kc-cuts-despite-20b` / caveat:levy-101-context: expected 'Explains the 101% levy-limit mechanics from the DOR levy-limit columns.', got 'not found'
- `seattle-2026-deficit-jumpstart` / caveat:attribution-is-context: expected "Treats 'what happened to the money' attribution as needing ordinance context, not budget-table inference.", got 'not found'
- `seattle-kc-homelessness-kcrha` / caveat:fragmentation-is-the-answer: expected 'States spending is fragmented across city, county, and authority - the fragmentation is part of a correct answer.', got 'not found'
- `seattle-kc-homelessness-kcrha` / caveat:no-outcome-claims: expected 'Refuses to convert spending totals into effectiveness claims.', got 'not found'
- `wa-deficit-after-historic-taxes` / caveat:modeling-choices-explicit: expected "States that 'the deficit number' depends on modeling choices and names them.", got 'not found'

Human pass completed 2026-07-14 by the maintainer (author-scored, unblinded, per benchmark rules). Anchor civic_usefulness: 5, 5, 5, 4, 4 (mean 4.6 - reported per-case, mean shown for the record only).
