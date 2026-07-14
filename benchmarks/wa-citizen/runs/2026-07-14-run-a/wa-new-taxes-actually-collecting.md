---
case: wa-new-taxes-actually-collecting
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
So far, yes — and then some, at the all-taxes level. Ten months into the 2025-27 budget period (through April 2026), Washington's General Fund has actually collected about **$1.04 billion more** than was projected for that stretch. But the accepted source tracks revenue by collecting agency, not by individual tax bill, so I can't isolate exactly how much of that came from the *new* 2025 taxes (the B&O surcharges, expanded sales tax on services, capital gains changes, etc.) versus the existing tax base. What I can say: the Department of Revenue — the agency that collects nearly all state taxes, including the new ones — is running **$2.43 billion above** its estimate, which is where any new-tax overperformance would show up.

**Numbers (General Fund 001, 2025-27 biennium, partial through April 2026):**
- Estimated revenue to date: $45.099B
- Actual revenue to date: $46.143B
- Actual minus estimate: **+$1.044B (+2.3%)**
- Department of Revenue line: est $25.331B, actual $27.762B (**+$2.43B**)
- Notable offsets below the line: Health Care Authority −$838M and Public Schools −$318M vs estimate (these are agency receipts/transfers, not taxes)
- For contrast, the last two full biennia both came in *under* estimate: 2023-25 −$1.93B, 2021-23 −$2.65B

**How to read this:**
"Estimated" here is the official revenue estimate built into the budget — the projection the Legislature counted on when it enacted the 2025 tax package. "Actual" is what has actually hit the General Fund through April 2026. The biennium runs through June 2027, so this is a 10-month progress report, not a final verdict — a positive gap now can narrow or widen. Also, the grain is agency, not tax type: the DOR line mixes new 2025 taxes with sales, B&O, property-in-state-fund, and other longstanding taxes. A per-tax answer (e.g., "did the new services sales tax hit its fiscal note?") would need DOR collections-by-tax-source data or ERFC forecast-tracking documents, which aren't yet an accepted source in this repo — that's the path to an exact answer.

**Answer mode:** partial — the aggregate estimate-vs-actual question is fully supported; isolating the specific new 2025 tax lines is not.

**Trace:**
- Source: Fiscal WA Revenue by Biennium, `washington.revenue_by_biennium`, snapshot `2025-27-revenue-through-2026-04`
- Public source: https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx
- Data-through: Actual Data Through April 2026 (2025-27 status: partial)
- Grain: biennium (totals); biennium × revenue area × account/agency (detail)
- Measure: estimated_revenue, actual_revenue, actual_minus_estimate
- Filters/query logic: read `general-fund-revenue-by-biennium.jsonl` for 2025-27 totals; read `general-fund-revenue-by-area-account.jsonl` filtered to biennium = 2025-27, sorted by |actual_minus_estimate|
- Check: 12 biennium rows, 934 detail rows; 2025-27 estimated $45,098,726,991 / actual $46,142,570,002.15 / difference +$1,043,843,011.15 match the skill's known validation values; detail reconciles to statewide totals within rounding
- Caveats: General Fund (001) only — new taxes deposited to other funds aren't visible here; 2025-27 values are partial through April 2026, not a full-biennium result or forecast; detail is by collecting agency, not tax type, so new-2025-tax revenue cannot be separated from the existing base; revenue estimates, not budget authority or spending.
