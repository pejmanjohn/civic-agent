# Tier 1 Worksheet - 2026-07-14-run-b

Mechanical results are in results.json. Human judgment is ONLY `civic_usefulness` (0-5 per docs/goals/eval-scoring-rubric.md) on the anchor cases below - author-scored, unblinded, and labeled as such. Do not re-score mechanical dimensions by hand.

| Anchor case | Mechanical | civic_usefulness (0-5) | Notes |
|---|---|---|---|
| `seattle-parks-2026-lookup` | 3/5 |  |  |
| `wa-checkbook-vendor-lookup` | 4/5 |  |  |
| `pierce-vs-king-per-resident` | 3/9 |  |  |
| `kc-property-tax-why-up` | 7/7 |  |  |
| `seattle-kc-homelessness-kcrha` | 4/8 |  |  |

Per-case mechanical failures (fix the capture or record as findings):

- `seattle-parks-2026-lookup` / answer_mode: expected 'exact', got 'partial'
- `seattle-parks-2026-lookup` / source:seattle.operating_budget: expected 'cited', got 'absent'
- `kc-sheriff-budgeted-fte-2026` / source:king_county.open_budget_dashboard: expected 'cited', got 'absent'
- `wa-checkbook-vendor-lookup` / answer_mode: expected 'exact', got 'partial'
- `pierce-county-budget-size` / source:pierce_county.open_checkbook: expected 'cited', got 'absent'
- `spd-budget-2020-vs-2026` / source:seattle.operating_budget: expected 'cited', got 'absent'
- `spokane-police-vs-housing` / answer_mode: expected 'partial', got 'unsupported_with_path'
- `evergreen-schools-cuts` / answer_mode: expected 'partial', got 'exact'
- `sound-transit-car-tabs` / answer_mode: expected 'partial', got 'exact'
- `sound-transit-car-tabs` / caveat:st3-gap-out-of-scope: expected 'Separates filed actuals from ST3 capital-program projections.', got 'not found'
- `kc-actuals-vs-budget-trap` / answer_mode: expected 'partial', got 'side_by_side_only'
- `pierce-vs-king-per-resident` / answer_mode: expected 'partial', got 'exact'
- `pierce-vs-king-per-resident` / source:king_county.open_budget_dashboard: expected 'cited', got 'absent'
- `pierce-vs-king-per-resident` / source:pierce_county.open_budget: expected 'cited', got 'absent'
- `pierce-vs-king-per-resident` / caveat:period-mismatch-named: expected 'Names the biennial-vs-annual period mismatch instead of silently annualizing.', got 'not found'
- `pierce-vs-king-per-resident` / fact:king-county-2025-population: expected 2411700, got 'not found'
- `pierce-vs-king-per-resident` / fact:pierce-county-2025-population: expected 959900, got 'not found'
- `wa-new-taxes-actually-collecting` / answer_mode: expected 'needs_refresh', got 'partial'
- `wa-new-taxes-actually-collecting` / caveat:freshness-block: expected 'Flags that a snapshot refresh is needed before a confident current-period claim.', got 'not found'
- `sps-deficit-school-closures` / caveat:causation-is-interpretation: expected 'Separates filed financial facts from causal interpretation of closures.', got 'not found'
- `kc-cuts-despite-20b` / source:king_county.open_budget_dashboard: expected 'cited', got 'absent'
- `kc-cuts-despite-20b` / source:washington.dor_property_tax_levies: expected 'cited', got 'absent'
- `seattle-2026-deficit-jumpstart` / source:seattle.operating_budget: expected 'cited', got 'absent'
- `seattle-2026-deficit-jumpstart` / caveat:attribution-is-context: expected "Treats 'what happened to the money' attribution as needing ordinance context, not budget-table inference.", got 'not found'
- `seattle-kc-homelessness-kcrha` / source:seattle.operating_budget: expected 'cited', got 'absent'
- `seattle-kc-homelessness-kcrha` / source:king_county.open_budget_dashboard: expected 'cited', got 'absent'
- `seattle-kc-homelessness-kcrha` / caveat:fragmentation-is-the-answer: expected 'States spending is fragmented across city, county, and authority - the fragmentation is part of a correct answer.', got 'not found'
- `seattle-kc-homelessness-kcrha` / caveat:no-outcome-claims: expected 'Refuses to convert spending totals into effectiveness claims.', got 'not found'
- `wa-deficit-after-historic-taxes` / caveat:modeling-choices-explicit: expected "States that 'the deficit number' depends on modeling choices and names them.", got 'not found'
