---
case: spokane-police-vs-housing
surface: repo-skills
answer_mode: unsupported_with_path
session: fresh
---

**Conclusion:** No accepted source in this system can yet break City of Spokane spending down by department or function, so I can't give you a source-backed police vs. housing-and-homelessness comparison. What I can tell you with confidence is Spokane's citywide filed actuals, and exactly where the official breakdown lives.

**Numbers (supported context only):**
- City of Spokane total expenditures, as filed with the Washington State Auditor: **$648.6M in 2024** (against $729.9M in revenues), and **$673.3M in 2025** (partial, early filing cycle).
- Trend: filed expenditures grew from $416.9M (2015) to $648.6M (2024), roughly +56% over nine years.
- No police, housing, or homelessness line exists in this reviewed source — those are function/department grains the source explicitly does not yet claim.

**How to read this:** These are actual revenues and expenditures as filed with the State Auditor (FIT headline basis, which excludes internal service funds) — not the adopted budget, and not a department breakdown. The comparison you asked for is answerable from official sources, just not from this repo's reviewed snapshot yet. Two official paths:
1. **State Auditor's Financial Intelligence Tool** (https://portal.sao.wa.gov/FIT/) — explore City of Spokane and view expenditures by function (public safety, housing/community services, etc.) for any filed year. This is the missing grain; promoting FIT's function-level rows to a reviewed claim is the clear extension path.
2. **City of Spokane's own adopted budget documents** (my.spokanecity.org) — department-level police and housing/homelessness budget lines, including its Community, Housing and Human Services division.

One caution for when you look it up: "housing and homelessness" spending is usually spread across a division, grant-funded programs (HUD/CDBG), and sometimes capital funds, while "police" is one department — a raw side-by-side can understate housing spending or mix budget frames. Also note police is typically among the largest general-fund lines in any city, so the two categories are rarely on the same funding basis.

**Trace:**
- Source: `washington.fit_filed_actuals` — FIT Filed Annual Actuals (reviewed governments), Washington State Auditor's Office
- Public source: https://portal.sao.wa.gov/FIT/
- Snapshot: `milestone-2025-published-2026-06-30` (FIT milestone Snapshot 33)
- Data-through: filed years 2015–2024 complete; 2025 early-cycle partial
- Grain: government × year (citywide totals only — no department/function grain)
- Measure: total_expenditures, total_revenues (filed actuals, excl. internal service funds)
- Filters/query logic: read `government-annual-totals.jsonl`, filter government = "City of Spokane" (MCAG 0724)
- Check: Spokane 2024 revenues $729,876,646 / expenditures $648,638,448 match the source-card validation checks; 110 government-annual rows total
- Caveats: filed actuals, not budgets; headline basis excludes internal service funds (can differ up to ~16% from all-funds); 2025 partial; department/fund/program breakdowns are explicitly listed as not supported by this source — hence unsupported_with_path for the police-vs-housing split.
