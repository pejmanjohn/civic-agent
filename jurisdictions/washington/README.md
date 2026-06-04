# Washington State

Washington state budget support for Civic Agent.

## Files

- `skill.md`: Washington state budget analysis instructions and snapshot recipes.
- `sources/operating-budget.source.json`: source metadata for the Fiscal WA operating budget summary report.
- `data/README.md`: snapshot policy and Power BI replay notes.
- `data/operating-budget/`: query templates, normalized snapshots, summary stats, and provenance.
- `scripts/extract_operating_budget.py`: source-specific extractor for the Fiscal WA operating budget summary report.

## Current Source

- Provider: LEAP and OFM through Fiscal WA / Microsoft Power BI
- Dataset: 2025-27 Biennial Omnibus Operating Budget summary comparison
- Power BI resource key: `b336a603-1f66-465d-af7f-eb8b1728d583`
- Current supported slice: 2025-27 enacted operating budget, by agency and functional area
- Current supported fund views: `Outlook Funds (NGF-O)` and `Total Budgeted`
