# Civic Coverage Taxonomy

This taxonomy describes the civic data coverage Civic Agent wants to understand over time. It is not a promise that every jurisdiction already has every category. It separates three ideas:

1. Full civic coverage map: the broad set of resident-relevant public data families that governments commonly publish.
2. Active source-card categories: the narrow categories that current source cards may claim in `coverage_claims`.
3. Reviewed source coverage: what one official source supports, partially supports, or does not support.

Source cards remain the source of truth for current capabilities. A category appearing here does not make any jurisdiction supported until a reviewed source card says so.

## Status Semantics

| status | Applies to | Meaning |
|---|---|---|
| `supported` | Source card claim | The reviewed source can answer the category at the listed measures, grains, and time or version boundary. |
| `partial` | Source card claim | The reviewed source can answer a constrained slice of the category, but important expected grains, measures, years, or source surfaces are missing. |
| `unsupported` | Source card claim | The reviewed source has been checked and should not be used for the category. Use source-level wording: unsupported by this source. |
| `unsupported-by-reviewed-source` | Derived jurisdiction rollup | Reviewed source cards for the jurisdiction explicitly say the category is unsupported by those sources. This is not a claim that the jurisdiction lacks the data elsewhere. |
| `not-yet-probed` | Derived jurisdiction rollup | No reviewed source card currently carries a claim for the category. Absence of a claim means not evaluated, not unavailable. |

## Active Source-Card Categories

These are the only category keys that may appear in `coverage_claims` for this round.

| category_key | tier | label | Current focus |
|---|---|---|---|
| `budget_finance.operating_budget` | active | Operating budget | Authorized or approved budget amounts by government budget grain. |
| `budget_finance.revenue_budget` | active | Revenue budget | Budgeted or projected revenue amounts, not actual revenue collected. |
| `workforce.budgeted_fte` | active | Budgeted FTE | Authorized or budgeted full-time-equivalent staffing totals. |
| `budget_finance.actual_spending_checkbook` | active | Actual spending/checkbook | Actual spending, vendor payments, invoices, or checkbook-style transactions. |

## Backlog Civic Coverage Families

Backlog families guide source probes and jurisdiction gap views. They must not appear in source-card `coverage_claims` until deliberately promoted to active categories after a probe proves the category can be supported or rejected by a reviewed source.

| family_key | tier | Resident questions | Common source types |
|---|---|---|---|
| `population_demographics` | backlog | Who lives here, how is the population changing, and what demographic context matters? | Census ACS API, local demographic dashboards, planning data portals. |
| `public_safety_crime` | backlog | What crimes, incidents, response patterns, and safety outcomes are reported? | Police open data, 911/CAD datasets, FBI Crime Data API, public safety dashboards. |
| `transportation_infrastructure` | backlog | What streets, transit, traffic, collisions, projects, and infrastructure assets are tracked? | DOT dashboards, ArcGIS services, traffic counts, capital project portals. |
| `housing_permitting_land` | backlog | What permits, housing units, parcels, zoning, inspections, and land records are public? | Planning/permitting portals, assessor data, building inspection data, GIS. |
| `procurement_contracts` | backlog | Who gets public contracts, for what amounts, and under what procurement process? | Contract search portals, procurement systems, vendor payment data. |
| `economic_labor_context` | backlog | What is the local economic and labor-market context? | BLS LAUS, Census, state labor data, economic development dashboards. |
| `health_human_services` | backlog | What health, social-service, homelessness, public-health, or benefit metrics are reported? | Health department dashboards, City Health Dashboard, human-services datasets. |
| `environment_climate_utilities` | backlog | What environmental, energy, climate, utility, and resilience indicators are available? | Environment dashboards, utility open data, energy benchmarking, climate plans. |
| `service_requests_311` | backlog | What residents request or report, where, and how quickly government responds? | 311/service request portals, case-management dashboards, open-data datasets. |
| `performance_outcomes` | backlog | What goals, outcome measures, service levels, and performance trends does government publish? | Performance dashboards, strategic plans, What Works Cities-style reporting. |
| `governance_meetings` | backlog | What elected bodies discussed, voted on, or scheduled? | Meeting agendas, minutes, legislative systems, ordinance databases. |
| `elections_campaigns` | backlog | What election, campaign finance, ethics, or voting data is public? | Election offices, campaign-finance portals, ethics datasets. |

## Promotion Rule

A backlog family becomes an active source-card category only after a source probe documents:

- The official owner and public inspection URL.
- The machine or snapshot access path.
- The exact measures, grains, geography, time coverage, and update cadence.
- At least one validation check or reproducible source fact.
- What the reviewed source does not support.
- Any comparability caveats if the category might be compared across sources or jurisdictions.

Promotion should add the new active category here, update coverage tests, and add source-card claims only for reviewed sources. Do not add unsupported rows just to fill the matrix.

## Comparability Rule

Shared labels are navigation aids, not accounting mappings. `budget_finance.operating_budget` can refer to Seattle `approved_amount`, King County `budgeted_expenditure`, and Washington `budgeted_amount`; those measures are not directly comparable until separate mapping and caveat work exists.

## Research Anchors

The backlog families are grounded in official and civic-data references that emphasize broad public data categories, data inventories, temporal coverage, quality, and resident-facing outcomes:

- Seattle Open Data and DataSF portal categories.
- Data.gov open-government and Catalog API metadata guidance.
- DCAT-US dataset metadata guidance.
- What Works Cities Certification Assessment.
- City Health Dashboard metrics background.
- Census public-sector topics and ACS API documentation.
- DOJ developer resources for the FBI Crime Data API.
- BLS Local Area Unemployment Statistics.
