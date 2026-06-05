# Washington State

Washington state budget support for Civic Agent.

## Files

- `skill.md`: Washington state budget and revenue analysis instructions and snapshot recipes.
- `sources/operating-budget.source.json`: source metadata for the Fiscal WA operating budget summary reports and accepted source surfaces.
- `sources/revenue-by-biennium.source.json`: source metadata for the Fiscal WA revenue by biennium ReportViewer reports.
- `data/README.md`: snapshot policy, Power BI replay notes, and ReportViewer export notes.
- `data/operating-budget/`: query templates, normalized snapshots, summary stats, and provenance.
- `data/revenue-by-biennium/`: normalized revenue snapshots, summary stats, and provenance.
- `scripts/extract_operating_budget.py`: source-specific extractor for the Fiscal WA operating budget summary reports.
- `scripts/extract_revenue.py`: source-specific extractor for the Fiscal WA revenue by biennium reports.

## Current Operating Budget Source

- Provider: LEAP and OFM through Fiscal WA / Microsoft Power BI
- Dataset: Washington Operating Budget Summary Reports
- Current Power BI resource key: `b336a603-1f66-465d-af7f-eb8b1728d583`
- Historical Power BI resource key: `7d2bb9ca-280e-4947-8038-bf6c6324e722`
- Current supported slice: 2025-27 enacted operating budget, by agency and functional area
- Historical supported slice: enacted base Total Budgeted operating budget trends from 2013-15 through 2025-27
- Current supported fund views: `Outlook Funds (NGF-O)` and `Total Budgeted`

## Current Revenue Source

- Provider: LEAP and OFM through Fiscal WA / Microsoft ReportViewer
- Dataset: Washington State Revenue by Biennium Reports
- Accepted report page: `https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx`
- Current snapshot version: `2025-27-revenue-through-2026-04`
- Supported slice: General Fund (001) revenue estimate, actual, and actual-minus-estimate rows
- Historical supported slice: General Fund revenue by biennium from 2003-05 through 2025-27
- Current-period boundary: 2025-27 values are partial through April 2026, not full-biennium final or full-biennium forecast values
