---
case: kc-property-tax-why-up
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** King County's total certified property tax levies rose only about **1.6%** from 2024 to 2025, so a ~10% jump on your bill is not countywide inflation — it almost certainly comes from the specific taxing districts stacked on your parcel plus how your home's assessed value changed relative to your neighbors'. The likeliest district-level culprits: if you live in Seattle, the city's own levy rose ~12.7% after the voter-approved lid lift replacing the expiring transportation levy; countywide, a **new $86.7M hospital levy line** ($0.10 per $1,000) appeared in 2025 and the **flood control levy rose ~45%**; and several suburban school district bond levies jumped (Northshore +14.5%, Tahoma +15.1%).

**Numbers (certified levies due, King County):**
- All King County districts: $7,603,197,998 (2024) → $7,724,787,822 (2025), **+1.6%**
- City of Seattle (all three lines): $709.1M → $798.9M, **+12.7%**. The base rate fell 1.44409 → 1.05837 per $1,000, but the lid-lift line rose 0.87332 → 1.57835 — quoting only the base line misleads.
- New in 2025: "Hospital County" levy, $86.7M at $0.10/$1,000 — countywide.
- Flood Zone County-wide: $58.5M → $84.6M, **+44.6%**
- School bonds up: Northshore #417 $90.1M → $103.2M (+14.5%); Tahoma #409 +15.1%; Issaquah #411 +7.3%; Lake Washington #414 +5.0%
- Pulling the other way: State School Part 1+2 fell $2,080M → $1,943M (**-6.6%**), and King County's own General Fund lines rose only ~2-4%.

**How to read this:** These are certified levy amounts each taxing district is owed — not your bill. Your bill = (your parcel's assessed value / 1,000) × the combined rate of the districts covering your address. Two things this source cannot see: (1) which exact districts stack on *your* parcel (that needs the county assessor's tax-code-area data — King County publishes rate books at kingcounty.gov/assessor), and (2) your assessed value. Because most levy lines are dollar-capped, if your home's value rose faster than the district average, your share rises even when the district's total doesn't — that alone can turn a 1.6% countywide increase into a 10% personal increase. A Seattle homeowner combining the city's +13% levy, the new hospital levy, and the flood increase could plausibly see ~10% even with average value growth.

**Trace:**
- Source: `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Snapshot: `levies-due-2025` (tax years due 2024 and 2025; 4,593 levy rows statewide, 374 King County rows)
- Data-through: certified levies due 2025 (most recent snapshot year)
- Grain: one row per levy line; district-level aggregation via `district_key`
- Measure: `district_levy` (dollars), `levy_rate_per_1000`
- Filters/query logic: `county = "King"`, group by `district_key`, sum `district_levy` per `year_due`, rank 2024→2025 deltas; Seattle city lines read individually
- Check: King County 2025 total $7,724,787,822 and 2024 total $7,603,197,998 match `summary.json` validation checks to the dollar; statewide 2025 $18,450,110,007 reconciles with DOR Table 12 (verified 2026-07-13)
- Caveats: certified levy amounts due, not tax bills or collections; parcel-level answer needs assessor tax-code-area data and your assessed value — any per-household inference here is illustrative; no ballot-measure metadata (lid lifts/bonds identified by levy-type labels only); answer mode is **partial** because the parcel-level denominator is outside this source.
