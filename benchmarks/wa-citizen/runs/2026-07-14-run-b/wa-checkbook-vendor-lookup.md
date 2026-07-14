---
case: wa-checkbook-vendor-lookup
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
Washington state's biggest vendor payments overwhelmingly go to Medicaid managed-care health plans. Molina Healthcare of Washington is by far the largest, followed by Consumer Direct Care Network (in-home care payroll agent) and the other Apple Health insurers — Community Health Plan of Washington, Coordinated Care, UnitedHealthcare, and Wellpoint. After healthcare come large construction contractors (Clark Construction, Skanska, Kiewit) and intergovernmental payments to King County.

One honest limit: the source available here reports vendor totals by two-year budget period (biennium), not by single calendar year, so I cannot give an exact "calendar 2025" ranking. The current 2025-27 biennium ranking below covers payments from July 2025 through May 2026 — most of the last year — and the 2023-25 ranking (which covers January–June 2025) shows the same names on top, so the leaderboard is stable.

**Numbers:**
Top vendors, 2025-27 biennium to date (actual payments, July 2025 – May 2026, partial):
1. Molina Healthcare of Washington — $5.68B
2. Consumer Direct Care Network WA — $2.80B
3. Community Health Plan of Washington — $2.04B
4. Coordinated Care of Washington — $1.73B
5. United Health Care of Washington — $1.62B
6. Wellpoint Washington Inc — $1.43B
7. Clark Construction LLC — $474.8M
8. King County — $420.6M
9. Public Consulting Group Inc — $303.2M
10. Skanska USA Civil West CA Dist — $242.7M

For context, the completed 2023-25 biennium (July 2023 – June 2025) top ranking is nearly identical: Molina $4.56B, Consumer Direct $2.38B, Community Health Plan $1.35B, UnitedHealthcare $1.34B, Coordinated Care $1.15B.

**How to read this:**
- These are actual vendor payments from Washington's Open Checkbook — money that went out the door — not budgets, contract values, or procurement awards.
- The dominance of health plans reflects how Apple Health (Medicaid) works: the state pays insurers monthly per-member premiums, and they in turn pay providers. Consumer Direct is the payroll agent for state-funded in-home caregivers.
- "Last year" is approximated: the hosted source only supports biennium totals. An exact calendar-2025 or fiscal-year-2025 cut requires the managed local checkbook database, which is unavailable in this session.
- The vendor list is truncated to the top 100 vendors per biennium; the top 10 shown are well within that.

**Answer mode:** partial (biennium grain available; exact single-year grain not available on this path).

**Trace:**
- Source: Fiscal WA Open Checkbook hosted aggregates, `washington.open_checkbook` (managed local DB unavailable; hosted-aggregate path used per the Washington skill)
- Public source: https://fiscal.wa.gov/Spending/Checkbook.aspx
- Snapshot: `2025-27-through-2026-05`; data_through = 2026-05 (payments through May 2026; 2025-27 biennium partial)
- Grain: biennium x vendor (top-100 vendors per biennium)
- Measure: sum(amount), actual vendor payments in dollars
- Filters/query logic: read `jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/vendor-totals.jsonl`, filter biennium = 2025-27 (context: 2023-25), sort by rank
- Check: `summary.json` reconciliation — category/agency/monthly totals reconcile per biennium (2025-27 total $38.465B, 2023-25 total $34.961B); vendor file 700 rows, top_n_per_biennium = 100, truncated = true
- Caveats: actual payments, not budget authority, contracts, invoices, payroll, or outcomes; 2025-27 partial through May 2026; no annual grain on hosted path — exact "last year" cut needs the managed local database; near-duplicate vendor names (e.g., "Molina Healthcare of WA Inc" rank 11) are not merged
