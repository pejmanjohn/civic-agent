# Washington State

Washington state budget support for Civic Agent.

## Files

- `skill.md`: Washington state budget analysis instructions and snapshot recipes.
- `sources/operating-budget.source.json`: source metadata for the Fiscal WA operating budget summary reports and accepted source surfaces.
- `data/README.md`: snapshot policy and Power BI replay notes.
- `data/operating-budget/`: query templates, normalized snapshots, summary stats, and provenance.
- `scripts/extract_operating_budget.py`: source-specific extractor for the Fiscal WA operating budget summary reports.

## Current Source

- Provider: LEAP and OFM through Fiscal WA / Microsoft Power BI
- Dataset: Washington Operating Budget Summary Reports
- Current Power BI resource key: `b336a603-1f66-465d-af7f-eb8b1728d583`
- Historical Power BI resource key: `7d2bb9ca-280e-4947-8038-bf6c6324e722`
- Current supported slice: 2025-27 enacted operating budget, by agency and functional area
- Historical supported slice: enacted base Total Budgeted operating budget trends from 2013-15 through 2025-27
- Current supported fund views: `Outlook Funds (NGF-O)` and `Total Budgeted`
