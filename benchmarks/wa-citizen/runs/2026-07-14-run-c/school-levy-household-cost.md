---
case: school-levy-household-cost
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** I can't compute your exact number, because two inputs aren't in any accepted source here: (1) the proposed levy rate for the specific measure on your ballot (my levy data covers *certified* levies already due in 2024-2025, with no ballot-measure metadata), and (2) your home's assessed value. But the math is simple and I can give you the formula, real current school-levy rates as a benchmark, and exactly where to get your two missing inputs.

**Numbers:**

The formula every Washington school levy uses:

> **Annual cost = (levy rate per $1,000) x (your home's assessed value / 1,000)**

Benchmark from certified 2025 levies (what school levies actually cost right now):
- Seattle School District No. 1 enrichment levy: **$0.65422 per $1,000** ($194.7M district-wide, up from $0.63479 / $190.2M in 2024)
- Seattle SD No. 1 capital projects/transportation levy: **$1.22694 per $1,000** ($365.1M district-wide)
- Illustrative only: on a home assessed at $800,000, those two Seattle school lines together cost about **$1,505/year** ($0.65422 + $1.22694 = $1.88116 per $1,000 x 800). Scale to your own assessed value.
- Statewide, voter-approved school enrichment levies totaled **$2.814B due in 2025** (up from $2.633B in 2024).

**How to read this:**
1. **Get the proposed rate** from your ballot measure's text or the county voters' pamphlet — measures state an estimated levy rate per $1,000 of assessed value (and often an "estimated cost for a $X home"). Ballot-measure details (measure numbers, proposed rates, election dates) need an elections source; my data doesn't carry them.
2. **Get your assessed value** from your county assessor's website (it's on your annual valuation notice; note it usually differs from market price). Any per-household figure without your parcel's value is illustrative.
3. **Know the levy type.** "Enrichment" (formerly M&O) levies fund operations; capital/technology levies fund buildings; bonds repay construction debt. Each is a separate line on your tax bill, so a new measure adds to — or replaces — an expiring line rather than the whole school tax.
4. If you tell me your school district (and ideally your assessed value), I can pull that district's current certified levy lines from the statewide file as a baseline for what you pay today.

Official path for the missing pieces: your county elections voters' pamphlet (proposed rate), your county assessor (assessed value and your parcel's full levy-code stack), and DOR's levy detail for certified history.

**Trace:**
- Source: `washington.dor_property_tax_levies` — DOR Local Taxing District Levy Detail, snapshot `levies-due-2025`
- Public source: https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail
- Data-through: certified levies due tax years 2024 and 2025 (snapshot verified against DOR Tables 8/12/14, 2026-07-13)
- Grain: one row per levy per taxing district per year_due (district-level, not parcel-level)
- Measure: `levy_rate_per_1000`, `district_levy`
- Filters/query logic: read `normalized/levy-detail.jsonl`; `district_type = "local_school"`, `district_key = "1704001"` (Seattle SD No. 1), years 2024-2025; statewide `levy_type = "school_enrichment"` totals from `summary.json`
- Check: 4,593 rows; Seattle SD enrichment 2025 = 0.65422 / $194,678,891 and statewide 2025 total $18,450,110,007 match `summary.json` validation checks to the dollar
- Caveats: certified levy amounts due — not tax bills, collections, budgets, or ballot measures; no ballot-measure metadata (proposed rates need an elections/voters'-pamphlet source); rates are district-level — household cost requires your parcel's assessed value, so the $800K example is illustrative only; your parcel's exact district stack needs county tax-code-area data (county assessor)

**Answer mode: partial** — current certified school-levy rates and the cost formula are source-backed; the specific ballot measure's proposed rate and your household's assessed value are missing inputs with a named official path.
