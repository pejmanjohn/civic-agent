---
case: sound-transit-car-tabs
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion:**
Sound Transit takes in far more than it spends in a typical year — by design. In 2024 (the most recent complete filed year), it reported about **$2.60 billion in total revenues** and about **$1.39 billion in total expenditures** as filed with the Washington State Auditor. The gap is not "leftover" money: Sound Transit is in the middle of a voter-approved capital buildout (ST3 light rail expansion), so tax collections — including the car-tab MVET you pay — are banked and bonded against multi-billion-dollar construction that lands in future years. Note these are actual filed revenues and expenditures, not the agency's adopted budget.

**Numbers (FIT filed actuals, in dollars):**

| Year | Total revenues | Total expenditures |
|---|---|---|
| 2015 | 910,463,197 | 353,958,000 |
| 2018 | 1,987,078,000 | 536,949,000 |
| 2020 | 2,131,434,000 | 616,343,000 |
| 2022 | 2,554,058,000 | 762,094,000 |
| 2023 | 2,616,474,000 | 1,219,143,000 |
| 2024 | 2,599,304,000 | 1,385,233,000 |
| 2025 (partial filing cycle) | 2,918,164,000 | 1,481,881,000 |

Revenues roughly tripled from 2015 to 2024 (the big jump in 2017-2018 follows the ST3 tax increases, including the higher car-tab MVET rate). Expenditures nearly quadrupled, with a marked step up in 2023-2024 as expansion projects ramped.

**How to read this:**
- These are **actual revenues and expenditures as filed** with the State Auditor's Financial Intelligence Tool (FIT headline basis, excluding internal service funds) — not Sound Transit's adopted budget, and not transaction-level checkbook data.
- "Revenues" includes all sources — the ST3 taxes (car-tab MVET, sales tax, property tax), fares, grants, and other income — this source does not break out the car-tab share. Your car tabs are one slice of the tax side.
- "Expenditures" on this basis will differ from cash spent on capital construction in a given year; the surplus largely funds the ongoing capital program and debt.
- 2025 is from the early filing cycle and should be treated as partial/preliminary.
- Sound Transit files in round thousands, so figures are rounded at the source.

**Trace:**
- Source: `washington.fit_filed_actuals` (FIT Filed Annual Actuals, reviewed governments)
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33, published 2026-06-30)
- Data-through: filed years 2015-2024 complete; 2025 early-cycle partial
- Grain: government x year (Sound Transit, MCAG 0987, special district, King County)
- Measure: `total_revenues`, `total_expenditures` (amount basis: filed actuals excluding internal service funds)
- Filters/query logic: read `jurisdictions/washington/data/fit-filed-actuals/milestone-2025-published-2026-06-30/normalized/government-annual-totals.jsonl`, filter `government = "Sound Transit"`; 11 rows (2015-2025)
- Check: snapshot spot check `sound_transit_2024_revenues = 2,599,304,000` matches the retrieved row exactly; summary.json row count 110 for government-annual-totals
- Caveats: filed actuals, not budgets and not checkbook transactions; no vendor/payee or revenue-source breakdown at this grain (car-tab share not separable here); Sound Transit reports in round thousands; 2025 partial; FIT headline basis excludes internal service funds

**Answer mode: exact.**
