# Washington Data

Washington uses checked-in snapshots because the official public sources are interactive report surfaces with replayable but undocumented or session-scoped endpoints.

Accepted operating budget source surfaces:

- `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- `https://app.powerbi.com/view?r=eyJrIjoiYjMzNmE2MDMtMWY2Ni00NjVkLWFmN2YtZWI4YjE3MjhkNTgzIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- `https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior`
- `https://app.powerbi.com/view?r=eyJrIjoiN2QyYmI5Y2EtMjgwZS00OTQ3LTgwMzgtYmY2YzYzMjRlNzIyIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`

Accepted revenue source surface:

- `https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx`

Accepted Open Checkbook source surface:

- `https://fiscal.wa.gov/Spending/Checkbook.aspx`
- `https://fiscal.wa.gov/Spending/VendorPayments2527.xlsx`

Snapshot policy:

- Normal Civic Agent answers should use the checked-in normalized snapshot, not live Power BI or ReportViewer calls.
- Query templates are replay artifacts generated for the official dashboard and stored under `operating-budget/query_templates/`.
- Raw Power BI responses and ReportViewer exports are local/debug artifacts by default. Commit only compact sanitized fixtures or reviewed raw payloads.
- Each committed snapshot must include normalized rows, `summary.json`, and `provenance.json`.
- Provenance must record the source surfaces, model refresh times, extraction time, query-template hashes, response checksums, row counts, validation totals, version filters, and fund-view filters.
- Split-time-span snapshots must include row-level `source_surface_id` values and overlap reconciliation when two surfaces cover the same period.

Interpretation policy:

- Amounts are in dollars in normalized files. Fiscal WA report values are returned in thousands.
- The current snapshot includes the 2025-27 enacted biennial operating budget and enacted base Total Budgeted historical trends from 2013-15 through 2025-27.
- It is not the 2026 supplemental budget, not proposal-stage historical comparisons, not pre-2013-15 history, and not actual spending.
- `Outlook Funds (NGF-O)` is narrower than `Total Budgeted`; always state which fund view was used.
- The revenue snapshot includes General Fund (001) estimated revenue, actual revenue, and actual-minus-estimate rows from 2003-05 through 2025-27.
- Revenue rows carry `actual_data_through`, `actual_data_through_label`, and `actual_data_status`. For snapshot `2025-27-revenue-through-2026-04`, the 2025-27 values are partial through April 2026 and must not be described as full-biennium final actuals or full-biennium forecasts.
- Fiscal WA Open Checkbook is separate actual-spending/checkbook data. Its full vendor-payment line items are managed through a local database built from official XLSX files because the historical source files are too large for normal git storage.
