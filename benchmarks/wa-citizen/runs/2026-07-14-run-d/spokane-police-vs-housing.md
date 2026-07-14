---
case: spokane-police-vs-housing
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion**

I can't yet give you a source-backed police-vs-housing dollar comparison for the City of Spokane — the accepted source for Spokane covers the city's filed **totals** only, not spending by category. What I can tell you exactly: in 2024 (the latest complete filed year), the City of Spokane reported **$648.6 million in total expenditures** against **$729.9 million in total revenues**, as filed with the Washington State Auditor. Police and housing/homelessness are each slices of that total, but the department/category breakdown is not yet a reviewed claim in this system, and I won't improvise those numbers.

**Numbers** (City of Spokane, filed actuals, FIT headline basis)

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2022 | $636,985,220 | $567,910,781 |
| 2023 | $713,909,072 | $631,933,223 |
| 2024 | $729,876,646 | $648,638,448 |
| 2025 (partial, early filing cycle) | $752,751,790 | $673,269,718 |

**How to read this**

- These are **actual revenues and expenditures as filed** with the State Auditor — not the adopted budget, and not checkbook transactions. Don't mix them with budget-book numbers without an alignment step.
- For the police-vs-housing breakdown you asked about, the official drill-down paths are: (1) the **City of Spokane's own budget documents** (my.spokanecity.org, Office of Management & Budget), which show department-level allocations for the Police Department and for housing/homeless services (CHHS division), and (2) the **State Auditor's Financial Intelligence Tool** (https://portal.sao.wa.gov/FIT/), whose category views break Spokane's filed expenditures into functional groups like Public Safety and Housing & Community Development.
- One framing note from the playbook: budgeted allocations and filed actuals are different frames, and homelessness spending in particular often splits across city, county, and other entities — a single city-budget line understates the public total. Spending totals also say nothing about outcomes.
- 2025 values are from the early filing cycle and may be revised.

**Trace**

- **Source:** `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), snapshot `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- **Public source:** https://portal.sao.wa.gov/FIT/
- **Snapshot/data-through:** filed years 2015–2024 complete; 2025 partial (early filing cycle)
- **Grain:** government × year (City of Spokane, MCAG 0724)
- **Measure:** `total_revenues`, `total_expenditures`
- **Filters/query logic:** read `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`, filter `government = "City of Spokane"`
- **Check:** spot check passed — Spokane 2024 revenues $729,876,646 / expenditures $648,638,448 match the snapshot `summary.json` fingerprint; 110 government-annual rows total
- **Caveats:** filed actuals on the FIT headline basis (excludes internal service funds), not budgets; category breakdown (police vs housing) is not a reviewed claim at this grain — totals only; 2025 partial; no vendor/payee detail

**Answer mode: `partial`** — the government-total pieces are exact and validated, but the category split you asked for requires a source (city budget book or FIT category views) not yet accepted in this system.
