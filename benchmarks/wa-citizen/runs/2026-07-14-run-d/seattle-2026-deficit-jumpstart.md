---
case: seattle-2026-deficit-jumpstart
surface: repo-skills
answer_mode: partial
session: fresh
---

**Conclusion:** Seattle's accepted budget data shows the *footprint* of the widely reported strategy — leaning on JumpStart payroll-tax money while the General Fund kept growing — but it cannot show the deficit math or prove "diversion." Approved spending out of the Payroll Expense Tax fund jumped from about $309M (FY2024) to about $517M (FY2025), with the single largest line being Finance General transfers out of the fund ($297M in FY2025, $211M in FY2026), while the approved General Fund grew from $1.65B (FY2024) to $2.01B (FY2026). That pattern is consistent with using JumpStart to support the rest of the budget, but the dataset does not label where transfers land or why.

**Numbers** (approved operating budget, fund grain):

- Payroll Expense Tax fund (14500), total approved by year: FY2022 $234M, FY2023 $319M, FY2024 $309M, FY2025 $517M, FY2026 $427M
- General Fund (00100), total approved: FY2024 $1.651B → FY2025 $1.864B → FY2026 $2.011B (+$360M, +21.8% over two years)
- FY2026 Payroll Expense Tax fund by department: Finance General $211.2M (program: "Appropriation to Special Funds" — transfers out of the fund, destination not named in the data), Office of Housing $142.5M, Office of Economic Development $23.9M, Planning & Community Development $23.2M, Sustainability & Environment $12.5M, all others under $2.5M each
- The Finance General transfer line grew from $85.6M (FY2022) and $93.4M (FY2024) to $296.9M (FY2025)

**How to read this:**

Two honesty points, per the deficit and earmark playbooks. First, "the deficit" is not a number in any accepted source: a shortfall figure (the commonly cited ~$250M) depends on modeling choices — forecast vintage, maintenance- vs policy-level growth assumptions, and which funds count. I cite no deficit number because no accepted source here supports one. Second, *allocation* is visible but *attribution* is not: the data shows large and growing transfers out of the JumpStart fund via Finance General, and shows housing remaining the largest direct programmatic use — but whether that constitutes "diversion" from the original 2020 spending plan (housing/EDI/Green New Deal percentages) turns on council ordinance actions (the 2024 revision of the JumpStart spending plan) that are not in this repo's accepted sources. I name that gap rather than infer intent from budget tables. Also note these are approved budget amounts, not actual spending or actual tax collections.

**Path to a fuller answer:** the City Budget Office's budget overview documents and Seattle City Council ordinances (the 2024 JumpStart fund policy legislation) would supply the deficit calculation and the legal reallocation; neither is an accepted source card yet.

**Trace:**

- **Source:** `seattle.operating_budget` (City of Seattle Operating Budget, Socrata `8u2j-imqx`)
- **Public URL:** https://data.seattle.gov/resource/8u2j-imqx.json (dashboard: https://openbudget.seattle.gov/#!/year/2026/operating/0/department)
- **Data-through:** FY2026 (annual publication; source card observed_at 2026-07-13; queried live at answer time)
- **Grain:** fund → department → program, by fiscal_year
- **Measure:** sum(`approved_amount`)
- **Filters:** `fund="14500 - Payroll Expense Tax"` (642 rows all years; 221 in FY2026) and `fund="00100 - General Fund"`, grouped by fiscal_year, department, program
- **Validation check:** FY2026 all-funds total returned matches card check ~$7.312B context; General Fund FY2026 $2.0107B from 2,689 rows — consistent with fund discovery query
- **Caveats:** approved operating budget, not actual spending or actual tax receipts; "Appropriation to Special Funds" rows are transfers whose destination fund is not identified in this dataset; no deficit figure exists in accepted sources; diversion/intent claims require ordinance context not covered here; fund structure changes across years (PET fund first appears FY2022).
