---
case: wa-deficit-after-historic-taxes
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

Washington's accepted budget sources can't quote you the shortfall itself — the "shortfall" is a projection in the state's four-year budget outlook and revenue forecasts, which aren't accepted sources in this repo yet. But they do show the structural squeeze behind the headlines: the state's enacted spending authority keeps growing faster than its main tax fund. The 2025-27 enacted operating budget is $150.4 billion in total budgeted funds — up $16.8 billion (12.6%) from 2023-25, and more than double 2013-15 — while General Fund revenue in recent completed biennia came in *below* the estimates shown in the state's own revenue report (about $1.9B under in 2023-25, $2.7B under in 2021-23). A "shortfall after a big tax package" isn't a contradiction: new taxes raise the revenue line, but a shortfall is about whether *projected future* revenue covers *already-committed* spending growth (caseloads, salaries, programs carried forward). The tax package was enacted alongside a budget that grew 12.6%, so the gap is about the trajectory, not the current year's cash.

**Numbers**

- Enacted operating budget (Total Budgeted, biennial): 2013-15 $66.52B → 2019-21 $99.71B → 2021-23 $121.73B → 2023-25 $133.61B → 2025-27 $150.41B (+12.6% vs 2023-25; +126% vs 2013-15)
- 2025-27 narrower near-general-fund view (Outlook Funds, NGF-O): $77.86B
- General Fund (001) actual-minus-estimate, recent closed biennia: 2019-21 −$3.93B, 2021-23 −$2.65B, 2023-25 −$1.93B
- 2025-27 so far (partial through April 2026): estimated $45.10B, actual $46.14B — running +$1.04B above estimate to date

**How to read this**

Budget figures are enacted budget *authority* (permission to spend), not actual spending, and are biennial. Revenue figures are General Fund (001) only — one fund, not the whole $150B budget, which draws on many funds. The 2025-27 revenue actuals are partial (through April 2026) and cannot be read as a full-biennium result or forecast. The size of "the biggest tax package in state history" (~the 2025 revenue legislation) and the projected out-biennium shortfall live in ERFC revenue forecasts and the OFM/legislative four-year balanced-budget outlook — not covered here. For those, see https://erfc.wa.gov/ and https://ofm.wa.gov/budget/ (and the 2026 supplemental budget documents, which this snapshot explicitly does not cover). Why-questions ultimately mix facts with policy interpretation; the interpretation above is labeled as such.

**Trace**

- Source 1: Fiscal WA Operating Budget Summary (washington.operating_budget), snapshot 2025-27-enacted-2025-05-20; historical-biennium-summary.jsonl
- Public URL: https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien
- Grain: biennium; Measure: budgeted_amount; Filters: enacted base, fund_view="Total Budgeted", session R1
- Check: 7 rows, 2013-15 through 2025-27; 2025-27 overlap total = $150,411,096,000 matches current snapshot check
- Caveats: enacted budget authority, not actual spending; excludes capital/transportation budgets; does not reflect 2026 supplemental
- Source 2: Fiscal WA Revenue by Biennium (washington.revenue_by_biennium), snapshot 2025-27-revenue-through-2026-04; general-fund-revenue-by-biennium.jsonl
- Public URL: https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: Actual Data Through April 2026; 2025-27 status = partial
- Grain: biennium; Measures: estimated_revenue, actual_revenue, actual_minus_estimate; Filter: fund = General Fund (001)
- Check: 12 biennium rows; 2025-27 estimate $45,098,726,991 and actual $46,142,570,002.15 match skill validation checks
- Caveats: General Fund only; estimate vintage is as-reported by Fiscal WA; not comparable to Total Budgeted spending authority; no forecast or shortfall figure in this source

Answer mode: **partial** — budget-growth and revenue facts are exact from accepted sources, but the shortfall projection and tax-package size have no accepted source; official path named (ERFC forecasts, OFM four-year outlook, 2026 supplemental documents).
