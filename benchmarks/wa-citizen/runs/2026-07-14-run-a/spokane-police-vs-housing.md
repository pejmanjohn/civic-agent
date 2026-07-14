---
case: spokane-police-vs-housing
surface: repo-skills
answer_mode: unsupported_with_path
session: fresh
---

**Conclusion**

I can't give you a source-backed police-versus-housing/homelessness comparison for the City of Spokane yet. The accepted source that covers Spokane — the State Auditor's Financial Intelligence Tool (FIT) filed annual actuals — is checked in at citywide-total grain only (total revenues and total expenditures per year). It has no department, function, or program breakdown, so neither "police spending" nor "housing and homelessness spending" can be quoted from it. Rather than guess, here is the accepted citywide context plus the official path to the department-level numbers.

**Numbers (accepted context, not the answer to your comparison)**

- City of Spokane total actual expenditures, as filed with the State Auditor:
  - 2024: $648,638,448 (complete filing year)
  - 2025: $673,269,718 (early filing cycle — treat as partial)
- City of Spokane total actual revenues: $729,876,646 (2024)
- Spokane resident population: 234,700 (OFM official April 1, 2025 estimate)

Any police or housing figure you find elsewhere can be sanity-checked against that ~$649M citywide 2024 total.

**How to read this**

- FIT figures are actual revenues/expenditures as filed (FIT headline basis, excluding internal service funds) — not budgets, and not transaction-level checkbook data.
- "Housing and homelessness" is also not a single line item in most city accounting: it typically spans community/human services, capital, and pass-through grants, while police is usually a clean department. Definitional choices will drive any comparison, so a careful source matters.
- Official path to the real answer:
  1. FIT portal (https://portal.sao.wa.gov/FIT/) — explore City of Spokane's filed expenditures by BARS function (e.g., Public Safety vs. Housing and Community Development categories).
  2. City of Spokane's own adopted budget documents (my.spokanecity.org, Budget Office) — department-level police and housing/homeless-services budgets and actuals.
- To make this answerable here, the FIT source would need to be extended to the expenditure-by-function/BARS-category grain for reviewed governments.

**Trace**

- Source: `washington.fit_filed_actuals` (FIT Filed Annual Actuals, reviewed governments) + `washington.ofm_population` (denominator context only)
- Public source: https://portal.sao.wa.gov/FIT/ ; https://ofm.wa.gov/data-research/population-demographics/estimates/april-1-official/
- Snapshot: FIT `milestone-2025-published-2026-06-30` (Snapshot 33, MILE2025, published 2026-06-30); OFM `2025-04-01`
- Data-through: FIT filed years 2015–2024 complete, 2025 partial (early filing cycle); OFM April 1, 2025 estimates
- Grain: government × year (citywide totals only — this grain gap is why the question is unsupported); population by jurisdiction × year
- Measure: `total_expenditures`, `total_revenues`; `population`
- Filters/query logic: `government-annual-totals.jsonl` filtered to `government = "City of Spokane"`; `population-estimates.jsonl` filtered to `jurisdiction = "Spokane"`, `row_type = "city_town"`, `estimate_date = "2025-04-01"`
- Check: Spokane 2024 row matches the skill's spot check (revenues $729,876,646 / expenditures $648,638,448); snapshot summary reports 110 government-annual rows with Spokane covering 2015–2025
- Caveats: filed actuals, not budgets; FIT headline basis excludes internal service funds; no department/function/program grain in this snapshot, so no police or housing/homelessness amounts are claimable; 2025 values partial; population is resident-denominator context only. Answer mode: unsupported_with_path.
