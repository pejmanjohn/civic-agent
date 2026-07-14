---
case: kc-property-tax-why-up
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** A ~10% jump on one household's King County bill almost never comes from "the county raising taxes" — countywide certified property-tax levies rose only about **1.6%** from 2024 to 2025. Individual bills jump when (a) your home's assessed value grew faster than your neighbors' (your *share* of each district's fixed levy rises), and/or (b) voters in your area approved new levies — lid lifts, school bonds, fire-authority or hospital levies — which are the fast-growing lines in the 2025 data. One caveat up front: DOR's district-level tables run through taxes due 2025; if "this year" means your 2026 bill, the due-2026 tables publish late 2026, so the specifics below are the 2024→2025 story.

**Numbers (King County, certified levies due, 2024 → 2025):**
- Countywide total: $7,603.2M → $7,724.8M (**+1.6%**)
- Local school districts: $2,072.9M → $2,121.1M (+2.3%); state school levy: $2,080.4M → $1,942.6M (−6.6%)
- Cities: $1,193.0M → $1,290.7M (**+8.2%**); county government: $1,064.5M → $1,048.3M (−1.5%)
- Fast movers, mostly voter-approved: hospital districts $54.2M → $142.1M (+162%), regional fire authorities $79.4M → $94.6M (+19.2%), flood-zone $58.5M → $84.6M (+44.6%)
- Concrete example of the voter-approved effect: Seattle's base city rate *fell* 1.44409 → 1.05837 per $1,000, but its lid-lift line rose 0.87332 → 1.57835 after the November 2024 transportation levy — the city total still climbed.

**How to read this:** Washington levies are budget-based: each district's regular levy can grow only ~1% a year (the 101% lid) plus new construction, which is why the countywide total moves slowly. Your bill is your parcel's assessed value times the sum of rates for the districts stacked on your address. So a 10% increase usually means your assessed value rose faster than your district's average (shifting share onto you), or a new voter-approved levy landed on your stack — or both. These figures are certified levy amounts due per taxing district, not bills or collections; per-household math needs your parcel's assessed value from the King County Assessor (who also publishes the parcel-level rate stack). If you tell me your city and school district, I can pull exactly which of your district levies changed 2024→2025.

**Trace:**
- **Source:** `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- **Public source:** https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- **Snapshot / data-through:** `levies-due-2025`; data through tax year due 2025 (due-2026 tables expected late 2026 — within the source's annual publication cadence, so not stale)
- **Grain:** one row per levy; aggregated to county, district type, and district (King County filter)
- **Measure:** `district_levy` (certified dollars due), `levy_rate_per_1000`
- **Filters/query logic:** read `levy-detail.jsonl` (4,593 rows), filter `county = "King"`, sum by `year_due` and `district_type`; Seattle city lines pulled by district name and levy type
- **Check:** King County 2025 total $7,724,787,822 and 2024 total $7,603,197,998 match the source card's validation checks to the dollar (reconciled with DOR Tables 8/12/14, verified 2026-07-13)
- **Caveats:** certified levies due, not tax bills or collections; parcel-level bill and levy stack need King County Assessor data; no ballot-measure metadata (voter-approved lines identified by levy-type/name only); 51 new and 68 dropped levy codes 2024→2025; snapshot cannot explain a 2026 bill at district detail until DOR publishes due-2026 tables

**Answer mode: partial** — the mechanism and 2024→2025 district-level facts are source-backed, but your specific ~10% needs your parcel's assessed value (assessor data) and, if you mean the 2026 bill, the not-yet-published due-2026 levy tables.
