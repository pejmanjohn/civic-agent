---
case: sound-transit-car-tabs
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
In 2024 — the latest complete filing year — Sound Transit took in about **$2.60 billion** in total revenues and spent about **$1.39 billion** in total expenditures, as filed with the Washington State Auditor. Its 2025 filing (early cycle, treat as preliminary) shows about **$2.92 billion** in and **$1.48 billion** out. Revenues have consistently run well above expenditures in these filings — the agency collects taxes (including your car-tab MVET, plus sales tax, property tax, fares, grants) ahead of the multi-billion-dollar ST3 rail expansion it is building and the debt it carries.

**Numbers (filed actuals, FIT headline basis, rounded):**

| Year | Total revenues | Total expenditures |
|------|---------------:|-------------------:|
| 2015 | $0.910B | $0.354B |
| 2016 | $0.970B | $0.423B |
| 2017 | $1.674B | $0.738B |
| 2018 | $1.987B | $0.537B |
| 2019 | $2.150B | $0.596B |
| 2020 | $2.131B | $0.616B |
| 2021 | $2.399B | $0.699B |
| 2022 | $2.554B | $0.762B |
| 2023 | $2.616B | $1.219B |
| 2024 | $2.599B | $1.385B |
| 2025 | $2.918B (partial/early filing) | $1.482B (partial/early filing) |

A chart of this trend is available on request.

**How to read this:**
- These are **actual revenues and expenditures as filed** with the State Auditor — not Sound Transit's adopted budget, and not checkbook-level payments to vendors.
- The revenue total lumps together all sources. Your car tabs (the motor vehicle excise tax) are one stream among several; **the breakdown by tax source is not a reviewed claim from this source** — for that, use Sound Transit's own annual financial reports or the FIT portal's category views.
- The persistent gap between money in and money out reflects an agency saving for and phasing large capital construction (light rail expansion) and debt service; the FIT headline expenditure basis excludes internal service funds, and Sound Transit files in round thousands.
- 2025 values come from the early filing cycle and may be revised.

**Trace:**
- **Source:** `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), Washington State Auditor's Financial Intelligence Tool
- **Public source:** https://portal.sao.wa.gov/FIT/
- **Snapshot:** `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30); repo file `/Users/pejman/code/civic-agent/jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`
- **Data-through:** filed years 2015–2024 complete; 2025 early-cycle partial
- **Grain:** government × year (annual totals)
- **Measure:** `total_revenues`, `total_expenditures` (amount_basis = `filed_actuals_excl_internal_service`)
- **Filters/query logic:** rows where `government = "Sound Transit"` (mcag 0987), all years, sorted by year
- **Check:** 11 Sound Transit rows returned; Sound Transit 2024 revenues = $2,599,304,000 matches the snapshot's `summary.json` spot check exactly; file total 110 government rows matches summary row count
- **Caveats:** filed actuals, not budget; no vendor/category/tax-source detail at this grain (MVET share needs Sound Transit's own financial reports); Sound Transit reports in round thousands; 2025 partial; FIT headline basis excludes internal service funds
