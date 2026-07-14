---
case: kc-property-tax-why-up
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** A roughly 10% jump on one King County property tax bill almost never comes from a countywide tax increase — total certified King County levies rose only about 1.6% from 2024 to 2025. Individual bills jump much faster than the countywide total for three reasons: (1) your home's assessed value rose faster than your area's average, so you absorbed a bigger share (the state's 101% lid caps a district's total regular levy, not your bill); (2) voters in your levy stack approved new or renewed lid lifts and bonds, which sit outside that lid; and (3) new levy lines started in 2025. One caveat up front: the certified levy data covers tax years due 2024 and 2025; if "this year" means your 2026 bill, DOR's due-2026 tables publish late 2026, so I can show you the pattern and the mechanics, not your 2026 lines.

**Numbers (certified levies due, 2024 → 2025):**
- King County total, all taxing districts: $7,603,197,998 → $7,724,787,822 (+1.6%)
- Countywide assessed value (county general levy base): ~$824.0B → ~$860.7B (+4.5%), while the county general rate fell 0.5225 → 0.51029 per $1,000 — the lid pushes rates down as values rise
- Biggest district-level dollar increases: Seattle lid-lift lines $709.1M → $798.9M (+12.7%; Seattle's base levy rate fell 1.44409 → 1.05837 while its lid-lift rate rose 0.87332 → 1.57835 after the November 2024 transportation levy); a new countywide hospital levy line of $86.7M appearing in 2025; county flood zone $58.5M → $84.6M (+44.6%); Northshore SD bond +14.5%; Port G.O. bonds +31.3%; Kent Regional Fire Authority +29.7%
- 51 levy lines were new and 68 dropped between 2024 and 2025 — new voter-approved lines land directly on the affected parcels' bills

**How to read this:** Your bill is your parcel's assessed value times the summed rates of every district that taxes your address (state school, county, city, school district, fire/EMS, port, Sound Transit, etc.), so the "why" is parcel-specific. If you're in Seattle, the 2024 transportation levy alone plausibly explains most of a 10% jump. Elsewhere, look for a school bond, RFA, or lid lift that passed in your area, plus your own valuation change. These figures are certified levy amounts due per district — not bills, not collections. To see your exact levy stack and year-over-year lines, use the King County Assessor's eReal Property lookup and its "taxpayer transparency" bill breakdown (the parcel-level tax-code-area data is published by the county, not DOR); the value notice you received shows the assessed-value side.

**Trace:**
- Source: `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Data-through: tax year due 2025 (due-2026 tables expected late 2026; within the source's annual publication cadence, so this is the latest available)
- Grain: one row per levy; aggregated to district (`district_key`) for changes, county for totals
- Measure: `district_levy` (dollars), `levy_rate_per_1000`
- Filters/query logic: read `levy-detail.jsonl`, filter `county = "King"`, group by `district_key` × `year_due`, compare 2024 vs 2025; base/lid-lift/bond lines kept separate
- Check: 4,593 rows total; King County 2025 total $7,724,787,822 and 2024 total $7,603,197,998 match source-card validation checks; statewide/county totals reconcile with DOR Tables 8/12/14 to the dollar (verified 2026-07-13)
- Caveats: certified levies due, not tax bills or collections; parcel-level levy stack not supported (county assessor data required); no ballot-measure metadata, so voter-approval attributions are inferred from levy-type labels; household math is illustrative without your parcel's assessed value; 2026 levies not yet published

**Answer mode: partial** — the district-level 2024→2025 change and the mechanics are fully source-backed, but your specific parcel's bill and the 2026 tax year are outside this source; the parcel path is the King County Assessor.
