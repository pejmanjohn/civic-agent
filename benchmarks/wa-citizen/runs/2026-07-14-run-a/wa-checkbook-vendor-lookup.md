---
case: wa-checkbook-vendor-lookup
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
The vendors paid the most by Washington state agencies are overwhelmingly Medicaid managed-care health plans and home-care intermediaries. Molina Healthcare of Washington is far and away #1, followed by Consumer Direct Care Network, Community Health Plan of Washington, Coordinated Care, UnitedHealthcare, and Wellpoint. After the health plans come large construction firms and King County.

One honest limitation: this source aggregates vendor payments by two-year budget period (biennium), not by calendar or single fiscal year. The closest window to "last year" is the current 2025-27 biennium, which covers payments from July 2025 through May 2026 — roughly the last 11 months — so this is a partial answer, not an exact calendar-2025 ranking.

**Numbers:**
Top vendors, 2025-27 biennium (payments July 2025 – May 2026, partial):

1. Molina Healthcare of Washington — $5.68B
2. Consumer Direct Care Network WA — $2.80B
3. Community Health Plan of Washington — $2.04B
4. Coordinated Care of Washington — $1.73B
5. UnitedHealthcare of Washington — $1.62B
6. Wellpoint Washington Inc — $1.43B
7. Clark Construction LLC — $475M
8. King County — $421M
9. Public Consulting Group Inc — $303M
10. Skanska USA Civil West — $243M

For context, the last complete two-year period (2023-25 biennium, July 2023 – June 2025) shows the same pattern: Molina #1 at $4.56B, Consumer Direct #2 at $2.38B, Community Health Plan #3 at $1.35B.

**How to read this:**
These are actual vendor payments from the state Open Checkbook — money that actually went out the door, not budgets, contracts, or procurement awards. The dominance of health plans reflects how Medicaid (Apple Health) works: the Health Care Authority pays managed-care organizations per enrollee, and those plans then pay doctors and hospitals. So "Molina got $5.7B" mostly means Molina administered $5.7B of Medicaid care, not that it kept it. This covers state agency payments only — not local governments — and excludes payroll. Note also that vendor name variants (e.g., "Molina Healthcare of WA Inc" appears separately at $226M) are not consolidated.

**Trace:**
- Source: Fiscal WA Open Checkbook, hosted aggregate snapshot for `washington.open_checkbook` (managed local DB unavailable on this host)
- Public source: https://fiscal.wa.gov/Spending/Checkbook.aspx
- Snapshot: `2025-27-through-2026-05`
- Data-through: 2026-05 (2025-27 biennium partial through May 2026)
- Grain: biennium x vendor (top 100 vendors per biennium)
- Measure: amount (actual vendor payments, dollars)
- Filters/query logic: read `jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/vendor-totals.jsonl`, filter biennium = 2025-27, sort by rank
- Check: summary.json reconciliation — agency/category/monthly totals all reconcile per biennium (2025-27 total $38.465B); vendor-totals.jsonl 700 rows, top-100-per-biennium, truncated=true
- Caveats: actual vendor payments, not budget authority, revenue, contracts, invoices, payroll, staffing, or outcomes; biennium grain — no single-calendar-year slice available on the hosted path (annual/fiscal-year vendor slicing requires the managed local database); 2025-27 is partial through May 2026; vendor list truncated to top 100 per biennium; vendor name variants not consolidated
