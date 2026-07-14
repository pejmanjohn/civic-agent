---
case: wa-new-taxes-actually-collecting
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

Roughly, yes — but with a catch: no accepted source isolates the *new* 2025 taxes as their own line. What the state's official revenue report can say is that total General Fund collections for the 2025-27 budget (which includes the new taxes the Legislature passed in 2025) are running just 0.7% below the official projection so far — a $353 million shortfall on about $51 billion, with roughly 11 of 24 months booked. The Department of Revenue, the agency that collects nearly all the new taxes (B&O changes, expanded sales tax, and similar), is actually running $393 million *above* its estimate. So collections are tracking close to plan overall, but this source cannot tell you whether each specific new tax is hitting its own individual projection.

**Numbers** (General Fund 001, 2025-27 biennium, partial through May 2026)

- Estimated revenue: $51.268 billion
- Actual revenue collected: $50.914 billion
- Actual minus estimate: -$353.2 million (-0.69%)
- Department of Revenue (collects most state taxes, including the new ones): estimated $29.671B, actual $30.064B, +$393.0M above estimate
- Notable laggards, by collecting agency: Health Care Authority -$262M, Public Schools revenues -$225M, Insurance Commissioner -$134M

**How to read this**

- "Projected" here means the official Fiscal WA estimate, which was revised in mid-2026 after the June forecast and 2025 legislative session — so the current estimate already *includes* what the new taxes were expected to raise. Being 0.7% under that revised bar is a near-miss, not a collapse. (Caution: the earlier snapshot of this same report showed estimates $6B lower; estimates revise.)
- The biennium runs July 2025 - June 2027; these figures cover collections through May 2026 only. Do not read them as a full-biennium result or forecast.
- The data's grain is *collecting agency*, not tax type. "New 2025 taxes" flow mostly through the Department of Revenue mixed with all existing taxes, so a tax-by-tax "did the new capital-gains/B&O/sales-tax changes each hit their number" answer needs a source this repo doesn't have yet — the Economic and Revenue Forecast Council's tracking reports (erfc.wa.gov) publish forecast-vs-collections by tax source and are the official path for that.
- General Fund (001) only; new taxes deposited to other accounts (e.g., dedicated funds) are outside this view.

**Trace**

- Source: `washington.revenue_by_biennium` — Fiscal WA Revenue by Biennium, snapshot `2025-27-revenue-through-2026-05` (fetched 2026-07-14)
- Public source: https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: Actual Data Through May 2026; 2025-27 `actual_data_status = partial`
- Grain: biennium (totals); biennium x revenue_area x account_or_agency (detail)
- Measure: estimated_revenue, actual_revenue, actual_minus_estimate
- Filters/query logic: read `general-fund-revenue-by-biennium.jsonl` for 2025-27 totals; read `general-fund-revenue-by-area-account.jsonl` filtered to biennium = 2025-27 (70 rows), sorted by estimate
- Check: 12 biennium rows; 937 detail rows; `detail_totals_match_statewide_totals = true`; 2025-27 totals match summary.json validation checks exactly ($51,267,621,520 est / $50,914,382,425.63 actual / -$353,239,094.37)
- Caveats: partial biennium (through May 2026), not final actuals or a forecast; General Fund (001) only; agency grain cannot attribute revenue to specific new 2025 tax enactments; estimates revise within the same data-through label (prior snapshot showed +$1.04B over a $45.10B estimate before the June 2026 revision); snapshot is one day newer than the skill text's described boundary (May vs April 2026)

**Answer mode: partial** — total collections vs. projection are source-backed and current, but tax-by-tax attribution for the new 2025 taxes is not supported; ERFC collection reports are the named path for that.
