---
case: pierce-county-budget-size
surface: repo-skills
answer_mode: exact
session: fresh
---

**Conclusion**

Pierce County's current budget is about **$3.5 billion for the two-year 2026–2027 biennium** (Pierce County budgets in two-year cycles, not annually). The biggest share by far goes to **Planning and Public Works** (roads, sewer, surface water, land use) at about $1.22 billion — over a third of the total. After that, the largest areas are **Human Services** (~$469M), the **Sheriff** (~$420M), **Finance** (~$242M), and **Facilities Management** (~$189M). Courts and the broader legal system (Prosecuting Attorney, Superior/District/Juvenile Courts, Assigned Counsel, Clerk) together add roughly $322M more.

**Numbers** (2026–2027 biennial budgeted expenditure authority)

- Total: **$3,500,588,070**
- Top departments:
  1. Planning and Public Works — $1,222,407,850 (~35%)
  2. Human Services — $468,509,930 (~13%)
  3. Sheriff — $419,636,880 (~12%)
  4. Finance — $241,669,350 (~7%)
  5. Facilities Management — $189,058,820 (~5%)
  6. "Pierce County" (countywide/general line) — $178,358,640 (~5%)
  7. Parks and Recreation — $164,884,370 (~5%)
  8. Tacoma/Pierce County Health Department — $102,899,820 (~3%)
  9. Prosecuting Attorney — $95,667,010 (~3%)
  10. Juvenile Court — $57,115,420 (~2%)
- Remaining 16 departments (courts, Assessor/Treasurer, Auditor, Emergency Management, Council, Executive, etc.) make up the rest.

**How to read this**

- These are **two-year (biennial) figures**. Halving them gives only a rough annual approximation.
- This is **budgeted expenditure authority** — what the county is authorized to spend — not actual dollars out the door. (Actual transaction-level spending is a separate Open Checkbook dataset; e.g., closed FY2025 actuals totaled about $975M.)
- Planning and Public Works looks huge partly because it includes large capital and utility-style funds (roads, sewer), not just office staff.
- "Pierce County" and "Finance" lines include countywide/internal-service costs, so they overstate what those offices themselves consume.
- No accepted **revenue** or **staffing** source exists for Pierce County in this system yet — this answer covers spending authority only.

**Trace**

- Source: pierce_county.open_budget (Open Budget Expenditure Data, Socrata w2wc-2pqu)
- Public source: https://open.piercecountywa.gov/resource/w2wc-2pqu
- Queried live at answer time (2026-07-14)
- Grain: biennium x department
- Measure: sum(budget)
- Filters: fiscal_year="2026-2027"; department ranking grouped by department
- Check: 2026–2027 total $3,500,588,070 over 10,362 rows, 26 departments — matches the source card's verified 2026-07-13 values
- Caveats: biennial budget authority, not annual, not actual spending; Flood Control Zone District returned a null budget total in the ranking; some department lines include countywide/internal-service and capital funds

