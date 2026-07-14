---
case: school-levy-household-cost
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
I can't compute an exact dollar figure for a levy that's still on your ballot — no accepted source here carries proposed ballot-measure rates, and household cost depends on your home's assessed value, which no source here holds. But the math is simple and two lookups away: **annual cost ≈ (levy's estimated rate per $1,000) × (your assessed value ÷ 1,000)**. The proposed rate is printed in your county voters' pamphlet / ballot measure text; your assessed value is on your county assessor's parcel page or your tax statement.

**Numbers (illustrative baseline from certified 2025 levies, not your ballot measure):**
School levies typically run roughly $0.50–$2.50 per $1,000 of assessed value. Example from the certified data — Seattle School District No. 1, taxes due 2025:
- Enrichment (voter-approved operations) levy: **$0.65422 per $1,000** → about **$523/year on a $800,000 home**
- Capital projects/technology levy: **$1.22694 per $1,000** → about **$982/year on a $800,000 home**
- Statewide, school enrichment levies totaled **$2.81B due in 2025** (up from $2.63B in 2024).

These are *currently certified* levies, shown only so you can sanity-check the ballot measure's estimated rate. Your district's rates will differ — I can look up your district's current certified school levy lines if you tell me your school district (the DOR snapshot covers every taxing district statewide).

**How to read this:**
- A ballot measure's official "estimated levy rate" is a projection; the actual certified rate moves with district-wide assessed value (if values rise, the rate falls for the same dollar amount).
- Replacement levies renew an expiring levy — your net bill change may be near zero even though the measure authorizes hundreds of dollars.
- Any per-household figure is illustrative: it assumes a specific assessed value and ignores exemptions (e.g., senior/disabled).
- Enrichment (operations) levies, capital/tech levies, and bonds are separate lines; check which type your measure is.

**Missing pieces and where to get them:**
1. Proposed rate and term → your county elections voters' pamphlet or the resolution text in the measure.
2. Your assessed value → county assessor parcel lookup (King County publishes parcel data and rate books).
3. Once certified, the actual levy will appear in DOR's Local Taxing District Levy Detail.

**Trace:**
- Source: `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Snapshot/data-through: tax years due 2024 and 2025 (certified levies only; no proposed/ballot measures)
- Grain: one row per levy per taxing district per year due
- Measure: `levy_rate_per_1000`, `district_levy`
- Filters: `year_due=2025`, `district_type=local_school`, illustrative rows `district_key=1704001` (Seattle SD #1); statewide `levy_type=school_enrichment` sum
- Check: snapshot `summary.json` validation checks all match the skill's reviewed spot checks — Seattle SD #1 enrichment 2025 rate 0.65422 / $194,678,891; statewide 2025 school enrichment total $2,814,008,373; statewide 2025 total $18,450,110,007; 4,593 rows
- Caveats: certified levy amounts due, not tax bills, collections, or budgets; no ballot-measure metadata (measure numbers, proposed rates, election dates need county elections sources); per-household figures are illustrative and require your parcel's assessed value; parcel-level levy stacks need county assessor tax-code-area data.

**Answer mode: partial** — the cost formula and current certified school-levy baseline are source-backed, but the proposed measure's rate and your household's assessed value are outside the accepted sources.
