# Washington Open Checkbook Demo

Washington Open Checkbook is the first Civic Agent source that uses the managed local database tier. The official Fiscal WA source publishes full vendor-payment XLSX files. Git stores the source card, probe, builder, tests, and docs; the full XLSX files and SQLite database live in the local Civic Agent data cache.

## Source

- Source id: `washington.open_checkbook`
- Official page: `https://fiscal.wa.gov/Spending/Checkbook.aspx`
- Current official file: `VendorPayments2527.xlsx`
- Historical coverage: `2013-15` through `2025-27`
- Current reviewed data-through boundary: `Payments through April 2026`
- Storage tier: `managed_local_db`
- Normal answer source: local SQLite database

## First-Run Setup

Inspect the source contract:

```bash
python3 scripts/source_data.py --json inspect washington.open_checkbook
```

Check whether the local managed database already exists:

```bash
python3 scripts/source_data.py --json status washington.open_checkbook
```

Build the local database when it is missing or stale:

```bash
python3 scripts/source_data.py --json ensure washington.open_checkbook
```

The first run downloads official XLSX files and builds `open_checkbook.sqlite` under the configured Civic Agent data cache. By default that cache is outside the repo at `~/.civic-agent/data`. For local debugging, use `--data-home .civic-agent-data`; that path is gitignored.

Use refresh when the official source metadata or monthly data-through boundary has changed:

```bash
python3 scripts/source_data.py --json refresh washington.open_checkbook
```

## Example Questions

Category breakdown for the current biennium:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook category_breakdown --param biennium=2025-27 --param limit=10
```

Top agencies by actual vendor-payment amount:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook agency_totals --param biennium=2025-27 --param limit=10
```

Top vendors by actual vendor-payment amount:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook vendor_totals --param biennium=2025-27 --param limit=10
```

Monthly payment trend:

```bash
python3 scripts/source_data.py --json query washington.open_checkbook monthly_trend --param biennium=2025-27
```

## Answer Shape

Use this source for actual vendor-payment questions, not budget authority:

```text
Conclusion:
The largest Washington Open Checkbook categories for the selected biennium are actual vendor-payment categories, not agency budgets.

Numbers:
Use the rows returned by the named query, sorted by amount.

How to read this:
These are payments recorded in Fiscal WA Open Checkbook. They do not show appropriations, contract obligations, invoices, payroll, staffing, or service outcomes.

Trace:
- Source: Fiscal WA Open Checkbook, washington.open_checkbook
- Storage: managed_local_db; local manifest data_through = <manifest data_through>
- Grain: category
- Measure: amount
- Filters/query logic: category_breakdown, biennium = 2025-27, limit = 10
- Check: local manifest row_count and source_files row counts
- Caveats: 2025-27 is partial through the manifest data-through month; actual vendor payments are not budget authority or procurement contracts
```

## Source-Card Probe Checks

The reviewed current-file probe found:

- Current file rows: 382,783
- Current file periods: 10
- Current file fiscal year/month range: `2026-01` through `2026-10`
- Current file data through: April 2026
- Current file agencies: 100
- Current file categories: 9
- Historical official XLSX total content length: 411,417,899 bytes

When a local manifest exists, use the manifest as the active answer trace. The probe values are the reviewed source contract; the local manifest is the concrete built artifact.
