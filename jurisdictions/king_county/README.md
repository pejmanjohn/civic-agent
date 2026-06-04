# King County

King County budget-dashboard support for Civic Agent.

## Files

- `skill.md`: King County budget analysis instructions and snapshot recipes.
- `sources/open-budget-dashboard.source.json`: source metadata for the King County Open Budget Dashboard.
- `data/README.md`: snapshot policy and Power BI replay notes.
- `data/open-budget-dashboard/`: query templates, normalized snapshots, summary stats, and provenance.
- `scripts/extract_open_budget.py`: source-specific extractor for the King County Open Budget Dashboard.

## Current Source

- Provider: King County / Microsoft Power BI Gov
- Dataset: King County Open Budget Dashboard
- Power BI resource key: `93fc6001-5c9d-4b9e-8e70-d758dc7082a0`
- Known years: 2017-2027 in the captured dashboard snapshot
- Current supported grains: countywide budgeted revenue/expenditure/FTE by year, FY2026 department budgeted revenue/expenditure, and FY2026 department FTE
