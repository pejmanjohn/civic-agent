# Washington Data

Washington uses checked-in snapshots because the official public source is a Power BI dashboard with replayable but undocumented report endpoints.

Primary source:

- `https://fiscal.wa.gov/statebudgets/operatingsummarycomparisonbien`
- `https://app.powerbi.com/view?r=eyJrIjoiYjMzNmE2MDMtMWY2Ni00NjVkLWFmN2YtZWI4YjE3MjhkNTgzIiwidCI6ImI0ZWIwY2NmLTAxOTQtNDY2My1hNTZhLTllZDkxZWZkMzMwOCIsImMiOjZ9`

Snapshot policy:

- Normal Civic Agent answers should use the checked-in normalized snapshot, not live Power BI calls.
- Query templates are replay artifacts generated for the official dashboard and stored under `operating-budget/query_templates/`.
- Raw Power BI responses are local/debug artifacts by default. Commit only compact sanitized fixtures or reviewed raw payloads.
- Each committed snapshot must include normalized rows, `summary.json`, and `provenance.json`.
- Provenance must record the model refresh time, extraction time, query-template hashes, response checksums, row counts, validation totals, version filters, and fund-view filters.

Interpretation policy:

- Amounts are in dollars in normalized files. Fiscal WA report values are returned in thousands.
- The current snapshot is the 2025-27 enacted biennial operating budget, not the 2026 supplemental budget and not actual spending.
- `Outlook Funds (NGF-O)` is narrower than `Total Budgeted`; always state which fund view was used.
