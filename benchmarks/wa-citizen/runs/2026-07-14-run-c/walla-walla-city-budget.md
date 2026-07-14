---
case: walla-walla-city-budget
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** No accepted source in this repo carries the City of Walla Walla's *adopted budget* itself, so I can't quote the official budget document's headline number. What I can give you, from an accepted official source, is the closest source-backed measure of the city government's financial size: its **actual revenues and expenditures as filed with the Washington State Auditor**. In 2024 (the latest complete filed year), the City of Walla Walla took in about **$117.5 million** and spent about **$96.3 million**, all funds combined (excluding internal service funds). For a city of roughly 34,850 residents (OFM April 1, 2025 estimate), that's a government operating on the order of $100 million a year.

**Numbers (FIT filed actuals, City of Walla Walla, all funds, excludes internal service funds):**

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2022 | $107,634,845 | $84,647,347 |
| 2023 | $109,082,502 | $90,001,108 |
| 2024 | $117,546,221 | $96,284,787 |
| 2025 (partial, early filing cycle) | $119,402,111 | $100,136,521 |

**How to read this:** These are actuals — money actually received and spent as filed with the State Auditor — **not** the city's adopted budget. A budget is a forward-looking authorization; the two frames should not be mixed numerically. Revenues exceeding expenditures here does not mean a "surplus" in the everyday sense: totals span all fund types (general fund, utilities, capital, grants, debt), and capital/grant timing routinely creates gaps like this. The 2025 row comes from the early filing cycle and may be revised. For the official adopted budget figure, the paths are the city's own budget documents (wallawallawa.gov) and the State Auditor's Financial Intelligence Tool.

**Trace:**
- Source: `washington.fit_filed_actuals` (SAO Financial Intelligence Tool filed annual actuals, reviewed governments)
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, created 2026-06-30)
- Data-through: filed years 2015–2024 complete; 2025 partial (early filing cycle)
- Grain: government × year (City of Walla Walla, MCAG 0773)
- Measure: `total_revenues`, `total_expenditures`; amount basis `filed_actuals_excl_internal_service` (FIT headline basis)
- Filters/query logic: read `government-annual-totals.jsonl`, filter `government = "City of Walla Walla"`; 11 rows returned (2015–2025)
- Check: snapshot `summary.json` fingerprint checks reconcile (e.g., Spokane 2024 revenues $729,876,646; Sound Transit 2024 revenues $2,599,304,000); 110 total government rows as expected
- Caveats: filed actuals, NOT an adopted budget — the adopted-budget frame is the missing source; excludes internal service funds; 2025 partial; population context is `washington.ofm_population` (Walla Walla city = 34,850, April 1, 2025 resident estimate), a denominator only, not a service-scope claim

**Answer mode: `partial`** — an accepted official source covers the jurisdiction (filed actuals), but the specific frame asked about (the adopted budget) has no accepted source yet; the official path is the city's budget documents and the SAO FIT portal.
