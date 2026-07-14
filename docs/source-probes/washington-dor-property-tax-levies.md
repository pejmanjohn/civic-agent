# Source Probe Brief: DOR Property Tax Levy Detail (statewide, all taxing districts)

Status: probed live 2026-07-13; recommended accept-snapshot (extractor not yet built)

## Question

```text
Why did my property tax go up - which taxing districts levy on property in my area,
how much did each levy change, and what does the school levy amount to?
```

This is demand archetype #1 for Washington residents (see `docs/goals/2026-07-13-benchmark-driven-launch-goal.md`) and unlocks WA-20 cases `kc-property-tax-why-up`, `school-levy-household-cost`, and the levy-context half of `kc-cuts-despite-20b`.

## Source Identity

- Jurisdiction: Washington State (all 39 counties, every taxing district - 2,288 levy rows in 2025)
- Budget family: property tax levies (proposed category: `budget_finance.property_tax_levies`)
- Official owner: Washington State Department of Revenue, Research and Fiscal Analysis
- Public inspection URL: `https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail`
- Candidate machine URL: `https://dor.wa.gov/sites/default/files/2025-10/All_County_Levy_Detail_2025.xlsx` (285KB)
- Source type: official bulk download (annual XLSX)
- Series depth: 2002-2025 (xls before 2010); publishes October-November of the tax-due year

## Primary Surface: All_County_Levy_Detail_{YEAR}.xlsx

Single clean sheet `Levy_Detail`, header row 6, data from row 10, one row per LEVY (2,288 rows in 2025). Columns: Taxing District Code (TDCODE), District Name, Locally Assessed Value, Levy Rate ($/1,000 AV), District Levy ($), Highest Prior Levy, New Construction AV, prior-year rate/value columns, Maximum Allowable Levy Under 101% Calculation, Statutory Maximum Rate, Levy Limit Percent Increase.

The 9-digit TDCODE decodes everything (scheme: `https://dor.wa.gov/sites/default/files/2022-02/LevyDetailExplan.pdf`):

- bytes 1-2: county (17 = King; 39 prefixes)
- bytes 3-4: district type (00 state school, 01 county, 03 city, 04 local school, 07 fire, 12 EMS, 30 RTA, ...)
- bytes 5-7: district id (schools use the OSPI code)
- bytes 8-9: levy type (0 regular, 1 school enrichment/EP&O, 2 capital projects/transportation, 3 school bond, 4 non-school bond, ...; lid lifts and bonds are SEPARATE rows)

Companion validation tables (same `/sites/default/files/{YYYY-MM}/Table_{N}_{YEAR}.xlsx` pattern): Table_8 (levies by county, YoY), Table_14 (assessed values by county), Table_12 (statewide school enrichment history 1993-2025), Table_30 Pt1-3 (school district levies per county).

## Verified Facts (2026-07-13; cross-file reconciliation exact to the dollar)

| Fact | Value | Reproduction |
|---|---:|---|
| Statewide levies due 2025 | $18,450,110,007 | sum(District Levy) over all 2,288 rows == Table_8 TOTAL x1000 |
| King County levies due 2025 | $7,724,787,822 | sum over 184 rows with TDCODE prefix 17 == Table_8 King row (+1.599% YoY) |
| King County assessed value (due 2025) | $866,805,846,211 | Table_14 King row (+4.733% YoY); statewide $2,067,498,789,907 |
| Statewide school enrichment levies 2025 | $2,814,008,373 (374 levies, rate 1.3734, 15.3% of all levies) | sum where type=04, levy byte=1 == Table_12 2025 row |
| Seattle SD #1 enrichment levy | 2025: 0.65422 / $194,678,891; 2024: 0.63479 / $190,239,286 | TDCODE 170400110 in each year's file |
| King County countywide EMS levy 2025 | 0.22146 / $191,842,786 | TDCODE 171200080 |

## What It Answers / Does Not

Answers, at taxing-district level: which districts levy in a county, per-levy rates AND dollar amounts, year-over-year change (join TDCODE across annual files; 2,237 of 2,288 2025 codes match 2024), school EP&O/capital/bond levies per district (all 20 King County districts verified), the 101%-limit and statutory-maximum context for the levy-lid story.

Does NOT answer: an individual address's levy stack (needs tax-code-area composition - King County publishes that only as PDF rate books: `ratebook26.pdf`, `taxrate26.pdf` series on the assessor site); ballot-measure linkage (no measure numbers/dates/approval percentages - voter-approved levies are identifiable only structurally by levy-type byte and names like "Temp Lid Lift"; connecting to elections needs a separate SoS/county source); parcel-level or exemption-level detail.

## Extraction Approach And Storage Policy

```text
Tier: checked_in_snapshot. Per-year snapshot of All_County_Levy_Detail (285KB) with 2+ years
checked in for YoY, plus Table_8/12/14 named totals as validation anchors. Extractor: openpyxl,
positional column mapping (prior-year header TEXT embeds shifting literal years - a header-shape
check must gate ingestion), accept rows where col A matches ^\d{9}$, decompose TDCODE, aggregate
key = bytes 1-7 for district-level rollups. Discover URLs by scraping the stable landing pages
(the /files/{YYYY-MM}/ directory segment reflects upload month, moves on silent re-uploads, and
gains _0/_1 suffixes - never guess it); pin snapshots by checksum. Effort: low (one-day
extractor including validations).
```

## Interpretation Rules To Encode (vocabulary walls)

- One row per LEVY, not per district: a district's base levy, lid lifts, and bonds are separate lines. Naive single-code YoY misleads - verified example: Seattle city's base rate "fell" 1.44409 -> 1.05837 while its lid-lift line rose 0.87332 -> 1.57835 after the November 2024 transportation levy. District-level statements must aggregate TDCODE bytes 1-7 and surface lid-lift/bond lines explicitly.
- Rates are per $1,000 of assessed value; district-level only - household math requires the parcel's AV and must be labeled illustrative.
- 51 new / 68 dropped codes between 2024 and 2025: handle births/deaths explicitly in trends.

## Risks

- Silent re-uploads months later (2024 levy detail re-uploaded 2025-02) - checksum pinning plus a drift check on the landing pages.
- Header text shifts every edition; positional mapping with a shape gate.
- The "which districts tax MY address" half stays out of scope without county tax-code-area data (PDF-only at King County).
- Ballot-measure linkage requires a second source if demanded.

## Decision

```text
accept-snapshot
```

Next artifact:

```text
Extractor (jurisdictions/washington/scripts/extract_dor_levy_detail.py), source card
washington.dor_property_tax_levies claiming proposed-category promotion
budget_finance.property_tax_levies, validator, drift check (landing-page scrape + checksum),
skill/router routes, benchmark ratchet for kc-property-tax-why-up, school-levy-household-cost,
and kc-cuts-despite-20b (adjunct)
```
