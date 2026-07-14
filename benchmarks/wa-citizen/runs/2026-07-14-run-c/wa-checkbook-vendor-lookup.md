---
case: wa-checkbook-vendor-lookup
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:**
Over roughly the past year (July 2025 through May 2026, the latest available data), the vendors paid the most by Washington state agencies were overwhelmingly Medicaid managed-care health plans. Molina Healthcare of Washington alone received about $5.7 billion, and five other health plans each received $1.4-2.8 billion. After health care, the biggest payees were construction firms and other governments.

**Numbers (actual state agency vendor payments, 2025-27 biennium to date, July 2025 - May 2026):**

| Rank | Vendor | Payments |
|---|---|---|
| 1 | Molina Healthcare of Washington | $5.68B |
| 2 | Consumer Direct Care Network Washington | $2.80B |
| 3 | Community Health Plan of Washington | $2.04B |
| 4 | Coordinated Care of Washington | $1.73B |
| 5 | United Health Care of Washington | $1.62B |
| 6 | Wellpoint Washington Inc | $1.43B |
| 7 | Clark Construction LLC | $475M |
| 8 | King County | $421M |
| 9 | Public Consulting Group Inc | $303M |
| 10 | Skanska USA Civil West CA District | $243M |

Total 2025-27 payments to date across all vendors: $38.47B. Note "Molina Healthcare of WA Inc" also appears separately at rank 11 ($226M) — vendor names are as filed, so the same company can appear under multiple spellings.

**How to read this:**
- These are actual payments state agencies made to vendors — not contracts awarded, not budget authority, and not local-government spending.
- The dominance of health plans reflects Medicaid (Apple Health): the Health Care Authority routes federal and state Medicaid dollars through managed-care insurers, so they show up as the state's biggest "vendors."
- "Last year" here means the current 2025-27 biennium to date: July 2025 through May 2026 (11 months). The available aggregate is biennium-level, so I cannot cut it to exactly calendar year 2025 or a single closed fiscal year — that finer cut needs the managed local checkbook database (fiscal-year grain), which is unavailable in this session. That is why this answer is **partial** rather than exact.
- Data is latest available; this source publishes monthly with a lag, and payments through May 2026 is the current boundary.

**Answer mode:** partial

**Trace:**
- Source: `washington.open_checkbook` — Fiscal WA Open Checkbook, hosted aggregate snapshot (managed local DB unavailable this session)
- Public source: https://fiscal.wa.gov/Spending/Checkbook.aspx
- Snapshot: `2025-27-through-2026-05`; file `jurisdictions/washington/data/open-checkbook/2025-27-through-2026-05/aggregates/vendor-totals.jsonl`
- Data-through: 2026-05 (payments through May 2026; 2025-27 biennium is in progress and partial)
- Grain: biennium x vendor (top 100 vendors per biennium)
- Measure: sum(amount), actual vendor payments in dollars
- Filters/query logic: biennium = "2025-27", sort by rank
- Check: summary.json reconciliation — 2025-27 total $38,465,185,859.87 matches across agency/category/monthly aggregates; 100 vendor rows for 2025-27; monthly-trend confirms coverage 2025-07 through 2026-05
- Caveats: payments, not contract obligations, procurement terms, invoices, payroll, or budget authority; vendor list truncated to top 100 per biennium; vendor names as filed (same entity may appear under multiple names, e.g. two Molina entries); does not cover local governments' own spending
