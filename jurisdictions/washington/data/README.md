# Washington Data

Washington uses checked-in snapshots because the official public source is a Power BI dashboard with replayable but undocumented report endpoints.

Accepted source surfaces:

- `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- `https://app.powerbi.com/view?r=eyJrIjoiYjMzNmE2MDMtMWY2Ni00NjVkLWFmN2YtZWI4YjE3MjhkNTgzIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`
- `https://fiscal.wa.gov/statebudgets/operatingsummarygraphicprior`
- `https://app.powerbi.com/view?r=eyJrIjoiN2QyYmI5Y2EtMjgwZS00OTQ3LTgwMzgtYmY2YzYzMjRlNzIyIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`

Snapshot policy:

- Normal Civic Agent answers should use the checked-in normalized snapshot, not live Power BI calls.
- Query templates are replay artifacts generated for the official dashboard and stored under `operating-budget/query_templates/`.
- Raw Power BI responses are local/debug artifacts by default. Commit only compact sanitized fixtures or reviewed raw payloads.
- Each committed snapshot must include normalized rows, `summary.json`, and `provenance.json`.
- Provenance must record the source surfaces, model refresh times, extraction time, query-template hashes, response checksums, row counts, validation totals, version filters, and fund-view filters.
- Split-time-span snapshots must include row-level `source_surface_id` values and overlap reconciliation when two surfaces cover the same period.

Interpretation policy:

- Amounts are in dollars in normalized files. Fiscal WA report values are returned in thousands.
- The current snapshot includes the 2025-27 enacted biennial operating budget and enacted base Total Budgeted historical trends from 2013-15 through 2025-27.
- It is not the 2026 supplemental budget, not proposal-stage historical comparisons, not pre-2013-15 history, and not actual spending.
- `Outlook Funds (NGF-O)` is narrower than `Total Budgeted`; always state which fund view was used.
