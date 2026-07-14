---
case: spokane-police-vs-housing
surface: repo-skills
answer_mode: unsupported_with_path
session: fresh
---

**Conclusion**

I can't give you a source-backed police vs. housing/homelessness comparison for the City of Spokane yet. The one accepted source covering Spokane (`washington.fit_filed_actuals`, the State Auditor's Financial Intelligence Tool) reports the city's filed annual totals — total revenues and total expenditures — but department- and program-level breakdowns (police, housing, homelessness) are explicitly not yet reviewed claims for that source. Rather than guess, here is what the accepted data does say, plus the official path to the split you asked for.

**Numbers (accepted context, not the answer to your split)**

City of Spokane filed annual actuals, FIT headline basis (excludes internal service funds):

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2023 | $713.9M | $631.9M |
| 2024 | $729.9M | $648.6M |
| 2025 (partial, early filing cycle) | $752.8M | $673.3M |

So whatever Spokane spends on police and on housing/homelessness, each is a slice of roughly $649M in total 2024 expenditures.

**How to read this**

- These are actual revenues and expenditures as filed with the State Auditor — not a budget, and not a department breakdown.
- "Housing and homelessness" is also not one department in most city books; it typically spans a community/housing/human-services division plus grant funds (CDBG, HOME, state homelessness dollars), so even the official split requires care.
- Your path to the real answer:
  1. City of Spokane's own adopted budget documents (my.spokanecity.org, Budget Office) — the adopted budget shows Police Department appropriations next to Community, Housing & Human Services appropriations.
  2. The State Auditor's FIT portal (https://portal.sao.wa.gov/FIT/) — explore City of Spokane and drill into expenditures by function (public safety vs. housing/community services, BARS categories) for filed actual years.
- If this repo later promotes FIT function/department detail to a reviewed claim, this question becomes answerable in `partial` or `exact` mode.

**Trace**

- Source: `washington.fit_filed_actuals` (FIT Filed Annual Actuals, reviewed governments)
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- Data-through: filed year 2024 complete; 2025 early-cycle partial
- Grain: government x year (citywide totals only)
- Measure: total_revenues, total_expenditures (filed actuals, headline basis excluding internal service funds)
- Filters: government = "City of Spokane" (MCAG 0724) in `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`
- Check: matches source-card validation values — Spokane 2024 revenues $729,876,646 and expenditures $648,638,448; 110 government-annual rows in snapshot
- Caveats: filed actuals, not budget authority; headline basis can differ up to ~16% from all-funds totals; department/program/fund breakdowns are unsupported by this source card; 2025 values will move in later milestone revisions; no police or housing/homelessness amounts are claimed here.

**Answer mode: unsupported_with_path** — the requested police vs. housing/homelessness comparison has no accepted source; citywide filed totals are provided as labeled context, and the official path (Spokane adopted budget documents and FIT function-level drilldown) is named.
