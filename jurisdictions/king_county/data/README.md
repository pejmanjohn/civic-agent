# King County Data

King County uses checked-in snapshots because the official public source is a Power BI Gov dashboard with replayable but undocumented report endpoints.

Primary source:

- `https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard`
- `https://app.powerbigov.us/view?r=eyJrIjoiOTNmYzYwMDEtNWM5ZC00YjllLThlNzAtZDc1OGRjNzA4MmEwIiwidCI6ImJhZTUwNTlhLTc2ZjAtNDlkNy05OTk2LTcyZGZlOTVkNjljNyJ9`

Snapshot policy:

- Normal Civic Agent answers should use the checked-in normalized snapshot, not live Power BI calls.
- Query templates are replay artifacts captured from the official dashboard and stored under `open-budget-dashboard/query_templates/`.
- Raw Power BI responses are local/debug artifacts by default. Commit only compact sanitized fixtures or reviewed raw payloads.
- Each committed snapshot must include normalized rows, `summary.json`, and `provenance.json`.
- Provenance must record the model refresh time, extraction time, query-template hashes, response checksums, row counts, and validation totals.
