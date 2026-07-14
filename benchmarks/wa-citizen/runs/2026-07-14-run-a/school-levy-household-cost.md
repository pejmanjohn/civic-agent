---
case: school-levy-household-cost
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** I can't compute an exact dollar figure for the specific measure on your ballot, because that needs three things I don't have: (1) which school district you live in, (2) the proposed levy rate or amount in the ballot measure itself (my accepted property-tax source has no ballot-measure metadata — proposed measures aren't in it), and (3) your home's assessed value. What I can do is give you the exact formula and real, certified current school-levy rates so you can see the scale, plus where to get your two missing inputs.

**Numbers:**
- The formula: **annual cost = (levy rate per $1,000) × (your assessed value ÷ 1,000)**. Ballot measures usually state an estimated rate per $1,000 of assessed value.
- Illustrative, using certified 2025 (tax-year-due) rates from the WA Dept. of Revenue for Seattle School District No. 1:
  - Enrichment (operations) levy: **$0.65422 per $1,000** → about **$523/year on a $800,000 home** ($654 per $1M).
  - Capital projects/technology levy: **$1.22694 per $1,000** → about **$982/year on a $800,000 home**.
- Statewide context: voter-approved local school enrichment levies totaled **$2.814 billion** due in 2025, out of **$18.45 billion** in all certified property tax levies statewide.
- Typical school enrichment rates around the state run roughly $0.50–$2.50 per $1,000; your district's actual rate may differ substantially.

**How to read this:** These are certified levy amounts due — what districts were authorized to collect in 2024–2025 — not tax bills, collections, or the proposed measure on your ballot. A new or renewal levy on your ballot replaces or adds to lines like these; renewals often keep your bill roughly flat rather than adding the full amount on top. Any per-household figure here is illustrative: your actual cost depends on your parcel's assessed value (county assessor) and how your district's total assessed value grows. To get your exact answer: (1) find the estimated rate per $1,000 in your county voters' pamphlet or the district's levy resolution; (2) look up your assessed value on your county assessor's site; (3) multiply. If you tell me your school district, I can pull its current certified levy lines from this source as a baseline.

**Trace:**
- Source: `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Snapshot / data-through: tax years due 2024 and 2025; 4,593 levy rows
- Grain: one row per levy line per taxing district per year due
- Measure: `levy_rate_per_1000`, `district_levy`
- Filters: `year_due = 2025`; illustrative rows `district_name` LIKE "Seattle #1" (`levy_type` = school_enrichment, capital_projects_transportation); statewide sums over all rows and over `levy_type = school_enrichment`
- Check: statewide 2025 total recomputed = $18,450,110,007 and school enrichment = $2,814,008,373 — both match the skill's DOR Table 8/12/14 spot checks; Seattle SD #1 enrichment 0.65422 / $194,678,891 matches
- Caveats: certified levies due, not bills or collections; no ballot-measure metadata (proposed rates, measure numbers, election dates need an elections/voters' pamphlet source); household math requires parcel assessed value from the county assessor and is labeled illustrative; parcel-level "which districts tax my address" needs county tax-code-area data
- Answer mode: **partial** — the formula and certified baseline rates are source-backed; the proposed measure's rate and your assessed value are outside accepted sources.
