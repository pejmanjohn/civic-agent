---
case: sound-transit-car-tabs
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
In 2024, the latest complete filing year, Sound Transit took in about **$2.60 billion** in total revenues and spent about **$1.39 billion** in total expenditures, as filed with the Washington State Auditor. Its early-cycle 2025 filing shows roughly $2.92 billion in and $1.48 billion out. Sound Transit consistently takes in far more than it spends on this basis — by design: it is banking voter-approved taxes (including your car-tab MVET, plus sales tax and property tax) to fund a decades-long capital program of light rail and transit expansion, and much of the capital construction outflow shows up over time.

**Numbers (filed actuals, FIT headline basis):**

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2015 | $910.5M | $354.0M |
| 2018 | $1.99B | $536.9M |
| 2021 | $2.40B | $698.9M |
| 2022 | $2.55B | $762.1M |
| 2023 | $2.62B | $1.22B |
| 2024 | $2.60B | $1.39B |
| 2025 (partial, early filing cycle) | $2.92B | $1.48B |

Revenues have roughly tripled since 2015 (the ST3 measure passed in late 2016); expenditures have roughly quadrupled, accelerating sharply since 2023 as construction ramps up.

**How to read this:**
- These are **actual revenues and expenditures as filed** with the State Auditor — not Sound Transit's adopted budget, and not transaction-level checkbook data. Filed actuals exclude internal service funds.
- Your car tabs (motor vehicle excise tax) are one of several revenue streams; this source reports **totals only** and does not break revenue down by tax type. For the MVET share specifically, Sound Transit's own financial reports are the path.
- The persistent revenue-over-expenditure gap largely reflects money accumulated and bonded for future capital construction, not surplus in the everyday sense.
- Label caution: Sound Transit files in round thousands, and 2025 is an early-cycle partial filing that may be revised.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), Washington State Auditor's Office Financial Intelligence Tool
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- Data-through: filed years 2015–2024 complete; 2025 early-cycle PARTIAL
- Grain: government × year (annual totals)
- Measure: `total_revenues`, `total_expenditures`
- Filters/query logic: read `government-annual-totals.jsonl`, filter `government = "Sound Transit"` (mcag 0987), all years
- Check: 11 Sound Transit rows (2015–2025); spot check passed — Sound Transit 2024 revenues = $2,599,304,000 matches the snapshot's recorded fingerprint; file row count 110 matches summary.json
- Caveats: filed actuals, not budgets and not checkbook transactions; FIT headline basis excludes internal service funds; Sound Transit reports in round thousands; 2025 values partial; no revenue-by-source (e.g., car-tab MVET) breakdown at this grain

**Answer mode: exact** — the question asks what Sound Transit actually takes in and spends, which is precisely what this reviewed filed-actuals source covers, with the 2025 partial-year value labeled as such.
