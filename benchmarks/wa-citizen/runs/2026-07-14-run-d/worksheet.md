# Tier 1 Worksheet - 2026-07-14-run-d

Mechanical results are in results.json. Human judgment is ONLY `civic_usefulness` (0-5 per docs/goals/eval-scoring-rubric.md) on the anchor cases below - author-scored, unblinded, and labeled as such. Do not re-score mechanical dimensions by hand.

| Anchor case | Mechanical | civic_usefulness (0-5) | Notes |
|---|---|---|---|
| `seattle-parks-2026-lookup` | 5/5 |  |  |
| `wa-checkbook-vendor-lookup` | 4/5 |  |  |
| `pierce-vs-king-per-resident` | 7/7 |  |  |
| `kc-property-tax-why-up` | 7/7 |  |  |
| `seattle-kc-homelessness-kcrha` | 7/8 |  |  |

Per-case mechanical failures (fix the capture or record as findings):

- `wa-checkbook-vendor-lookup` / answer_mode: expected 'exact', got 'partial'
- `pierce-county-budget-size` / source:pierce_county.open_checkbook: expected 'cited', got 'absent'
- `school-levy-household-cost` / answer_mode: expected 'partial', got 'unsupported_with_path'
- `seattle-kc-homelessness-kcrha` / caveat:no-outcome-claims: expected 'Refuses to convert spending totals into effectiveness claims.', got 'not found'
