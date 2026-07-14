---
case: wa-checkbook-vendor-lookup
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Health-care companies dominate. Washington state's biggest vendor by far is **Molina Healthcare of Washington**, one of the state's Medicaid managed-care insurers — it received roughly $4.6 billion in the 2023–25 biennium and $5.7 billion so far in 2025–27. The rest of the top tier is the same story: Medicaid managed-care plans and in-home care payroll (Consumer Direct Care Network), followed at a distance by construction firms and King County. One honest limit: the accepted source aggregates vendor payments by two-year biennium, not by single calendar year, so "last year" (2025) is answered here as the two biennial rankings that bracket 2025 — the ranking is essentially identical in both, so the conclusion holds either way.

**Numbers (actual vendor payments, dollars):**

2025–27 biennium (partial — payments July 2025 through May 2026):
1. Molina Healthcare of Washington — $5.68B
2. Consumer Direct Care Network WA — $2.80B
3. Community Health Plan of Washington — $2.04B
4. Coordinated Care of Washington — $1.73B
5. United Health Care of Washington — $1.62B
6. Wellpoint Washington Inc — $1.43B
7. Clark Construction LLC — $474.8M
8. King County — $420.6M
9. Public Consulting Group Inc — $303.2M
10. Skanska USA Civil West — $242.7M

2023–25 biennium (complete — July 2023 through June 2025, includes fiscal year 2025):
1. Molina Healthcare of Washington — $4.56B
2. Consumer Direct Care Network WA — $2.38B
3. Community Health Plan of Washington — $1.35B
4. United Health Care of Washington — $1.34B
5. Coordinated Care of Washington — $1.15B

**How to read this:** These are actual vendor payments from the state's Open Checkbook — money that actually went out the door — not budget authority, contract values, or payroll. The top recipients are mostly insurers the Health Care Authority pays to run Apple Health (Medicaid), so "vendor" here largely means "pass-through to health coverage for residents," not conventional procurement. The 2025–27 biennium is in progress (through May 2026), so its totals will grow. A precise calendar-2025 vendor cut exists in the underlying transaction data but isn't available in this session; the biennial rankings above bracket it and agree on the leaders.

**Trace:**
- **Source:** `washington.open_checkbook` (hosted aggregate snapshot; managed local DB unavailable this session)
- **Public source:** https://fiscal.wa.gov/Spending/Checkbook.aspx
- **Snapshot:** `2025-27-through-2026-05`; **data-through:** 2026-05 (2025–27 biennium partial through May 2026)
- **Grain:** biennium x vendor (top-100 vendors per biennium)
- **Measure:** sum(amount), actual vendor payments in dollars
- **Filters/query logic:** read `jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/vendor-totals.jsonl`, filter biennium in {2023-25, 2025-27}, sort by rank
- **Check:** `summary.json` reconciliation — category/agency/monthly totals reconcile per biennium (2023–25 total $34.96B; 2025–27 partial total $38.47B, all `reconciles: true`); vendor file 700 rows, top-100 per biennium
- **Caveats:** payments, not contracts, invoices, budget authority, or outcomes; vendor list truncated to top 100 per biennium (irrelevant for a top-10 ranking); biennium grain only — no single-year vendor cut in this session, which is why this is `partial` rather than `exact`; a related entity "Molina Healthcare of WA Inc" appears separately at rank 11 in 2025–27 ($225.9M) — vendor names are as recorded, not deduplicated.

**Answer mode:** partial — the top-vendor ranking is fully supported at biennium grain, but the exact "last year" (calendar/fiscal 2025) vendor cut requires the transaction-level database, unavailable here.
