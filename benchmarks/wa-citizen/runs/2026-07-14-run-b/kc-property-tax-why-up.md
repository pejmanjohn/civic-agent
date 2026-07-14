---
case: kc-property-tax-why-up
surface: repo-skills
answer_mode: partial
session: fresh
---

Conclusion:
A ~10% jump in your King County property tax bill this year (taxes due 2025) was almost certainly not a countywide phenomenon — total certified levies across all King County taxing districts rose only about 1.6%. A bill increase that large is driven by which taxing districts overlap YOUR parcel, especially new voter-approved measures, plus whether your home's assessed value rose faster than your neighbors'. The biggest 2024→2025 district-level increases in King County were the Seattle transportation levy lid lift, a brand-new countywide hospital levy, a sharply higher flood control levy, several school bond levies, and the Kent Regional Fire Authority.

Numbers (certified levy amounts due, 2024 → 2025):
- All King County districts combined: $7,603,197,998 → $7,724,787,822 (+1.6%)
- Statewide: $17,630,395,363 → $18,450,110,007 (+4.6%)
- City of Seattle (all city levy lines): $709.1M → $798.9M (+12.7%). The base rate fell 1.44409 → 1.05837 per $1,000, but the lid-lift line rose 0.87332 → 1.57835 after the November 2024 transportation levy — combined city rate went about 2.372 → 2.691 per $1,000 (+13.5%)
- New countywide hospital levy: $0 → $86.7M (new in 2025)
- Flood Zone County-wide: $58.5M → $84.6M (+44.6%)
- School bond levies: Northshore #417 +14.5%, Tahoma #409 +15.1%, Issaquah #411 +7.3%, Lake Washington #414 +5.0%
- Port of Seattle G.O. bonds: $34.7M → $45.5M (+31.3%); Kent RFA: $34.9M → $45.2M (+29.7%)

How to read this:
These are certified levy amounts due per taxing district — not your bill. Your bill is the sum of the levy rates of every district stacked on your parcel, times your assessed value. Because the countywide total rose only 1.6%, a ~10% personal increase means either (a) you live where a big levy landed — e.g., Seattle (transportation lid lift), the Kent RFA area, or a school district that passed a bond — and/or (b) your assessed value rose relative to others in your districts (the levy pie is fixed; your slice depends on your relative value). Everyone countywide also picked up the new hospital levy and the larger flood levy. To decompose your exact bill, look up your parcel's tax code area and value history at the King County Assessor (kingcounty.gov, eReal Property / levy rate books) — that parcel-level stack is not in this source, which is why this answer is partial rather than exact.

Trace:
- Source: washington.dor_property_tax_levies — WA Dept. of Revenue Local Taxing District Levy Detail, snapshot levies-due-2025
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Snapshot/data-through: levies-due-2025 (tax years due 2024 and 2025; 4,593 levy rows)
- Grain: one row per levy per taxing district per year_due; district aggregation by district_key
- Measure: district_levy (dollars), levy_rate_per_1000 (dollars per $1,000 assessed value)
- Filters/query logic: county = "King"; sum district_levy by year_due; per-district 2024 vs 2025 deltas grouped by district_key; Seattle city rows summed across regular/lid-lift/bond lines
- Check: computed King County totals $7,603,197,998 (2024) / $7,724,787,822 (2025) and statewide $17.63B/$18.45B match summary.json fingerprint checks exactly (reconciled with DOR Tables, verified 2026-07-13)
- Caveats: certified levies due, not tax bills or collections; a district's base, lid-lift, and bond levies are separate rows (quoting only Seattle's falling base rate would mislead); household math requires the parcel's assessed value — figures here are illustrative; parcel-level district stack requires county assessor tax-code-area data; ballot-measure metadata (dates, approval %) not in this source.
