---
case: sound-transit-car-tabs
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
Sound Transit takes in far more than it spends on operations each year — by design. In 2024, the most recent complete filing year, Sound Transit reported about **$2.60 billion in total revenues** and about **$1.39 billion in total expenditures** as filed with the Washington State Auditor. Your car-tab (motor vehicle excise tax) money is part of that revenue stream, alongside sales tax, property tax, fares, and federal grants. The large gap between revenues and expenditures is not "leftover" money — Sound Transit is deliberately collecting ahead of massive multi-year capital projects (light rail expansion under the ST3 program) and debt repayment, so revenue banked in one year funds construction spending in later years.

**Numbers (filed annual actuals, FIT headline basis):**

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2020 | $2.131B | $0.616B |
| 2021 | $2.399B | $0.699B |
| 2022 | $2.554B | $0.762B |
| 2023 | $2.616B | $1.219B |
| 2024 | $2.599B | $1.385B |
| 2025 (partial, early filing cycle) | $2.918B | $1.482B |

Trend: revenues have roughly tripled since 2015 ($910M → $2.6B), largely because ST3 taxes (approved November 2016) took effect in 2017. Expenditures on this basis have grown faster recently — roughly doubling from 2022 to 2024 as construction ramps up.

**How to read this:**
- These are **actual revenues and expenditures as filed** with the State Auditor — not Sound Transit's adopted budget, and not checkbook-level payments to vendors.
- This grain does not break out how much comes specifically from car tabs vs. sales tax, property tax, or fares; for that split, see Sound Transit's own financial reports or the FIT portal.
- The revenue-vs-spending gap reflects saving for capital projects and debt service, not surplus in the everyday sense.
- Sound Transit files in round thousands, so figures are approximate at the last three digits.
- 2025 values come from the early filing cycle and should be treated as partial/preliminary.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), Washington State Auditor's Office Financial Intelligence Tool
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30); file `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`
- Data-through: filed years 2015–2024 complete; 2025 early-cycle partial
- Grain: government × year (Sound Transit, MCAG 0987)
- Measure: `total_revenues`, `total_expenditures` (amount basis: filed actuals excluding internal service funds)
- Filters/query logic: `government = "Sound Transit"`, all years 2015–2025 (11 rows)
- Check: spot check passed — Sound Transit 2024 revenues $2,599,304,000 matches summary.json fingerprint; 110 total government rows as expected
- Caveats: filed actuals, not budget; no vendor/payee detail; no revenue-source split (car tabs not separable at this grain); Sound Transit reports in round thousands; 2025 partial

**Answer mode: exact** — the question asks for actual take-in and spend, which this reviewed filed-actuals source directly supports with passing validation.
