---
case: school-levy-household-cost
surface: repo-skills
answer_mode: unsupported_with_path
session: fresh
---

**Conclusion:** I can't give you a dollar figure yet — no accepted source here covers proposed ballot measures, and your household's cost depends on three things I don't have: (1) which school district you live in, (2) the proposed levy rate on the measure itself, and (3) your home's assessed value. But the math is simple once you have those, and I can show you what school levies cost today as a reality check.

**Numbers (the formula, plus accepted context):**
- Your annual cost ≈ (your home's assessed value ÷ $1,000) × the proposed levy rate per $1,000. Example: a $2.50/$1,000 proposed rate on a $600,000 home ≈ $1,500/year. Ballot measures usually state either the rate or a total dollar amount per year — the rate is what drives your bill.
- Illustrative context from certified levies (not your ballot measure): Seattle School District No. 1's enrichment levy for taxes due 2025 is $0.65422 per $1,000 ($194,678,891 district-wide), up from $0.63479 ($190,239,286) in 2024. On an $800,000 home that certified rate is roughly $523/year — labeled illustrative, since it uses a hypothetical assessed value.
- Statewide, school enrichment levies total $2,814,008,373 due in 2025 (up from $2,633,498,229 in 2024).

**How to read this:** A "school levy" on your ballot is usually an enrichment (operations) levy, a capital levy, or a bond — each shows up as its own line on your tax bill, and rates are per $1,000 of *your parcel's* assessed value, not per household generally. The accepted data here is certified levy amounts already due (2024–2025) — it cannot see proposed measures, so I won't guess your measure's rate. Your path to the exact number: (1) the proposed rate and total are in your county voters' pamphlet / county elections office for the measure; (2) your assessed value is on your county assessor's site (King County publishes parcel lookups and rate books); (3) multiply. Also note the levy-lid context: regular levies grow under a 101% (1%) limit, which is why districts go to voters for enrichment levies at all.

**Offer:** Tell me your city or school district and I can pull that district's current certified levy lines (base, enrichment/lid lifts, bonds) from the accepted levy data so you can see exactly what you pay now and compare it to the proposed measure.

**Trace:**
- **Source:** `washington.dor_property_tax_levies` (Local Taxing District Levy Detail), snapshot `levies-due-2025`
- **Public source:** https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- **Data-through:** tax years due 2024 and 2025 (certified levies; no proposed/ballot measures)
- **Grain:** one row per levy per taxing district per year (district_key aggregates a district's lines)
- **Measure:** levy_rate_per_1000, district_levy
- **Filters/query logic:** validation values read from snapshot summary.json checks (Seattle SD enrichment lines; statewide school enrichment totals); no district filter applied because the user's district is unknown
- **Check:** 4,593 rows; 2025 statewide total $18,450,110,007; Seattle SD enrichment 2025 = 0.65422 / $194,678,891 — all reconcile with DOR Tables 8/12/14 (verified 2026-07-13)
- **Caveats:** certified amounts due, not tax bills, collections, or budgets; no ballot-measure metadata (proposed rates need the county voters' pamphlet/elections source); per-household figures require the parcel's assessed value and are labeled illustrative; a district's base levy, lid lifts, and bonds are separate rows — quoting one line alone misleads.
