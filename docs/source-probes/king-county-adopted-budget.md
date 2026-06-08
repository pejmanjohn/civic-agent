# King County Adopted Biennial Budget Source Probe

Status: probe complete, accepted as context-only source

Date: 2026-06-08

## Question

Can Civic Agent answer "How big is King County's budget?" with official adopted biennial budget context instead of only the annual Open Budget Dashboard value?

## Source Identity

- Jurisdiction: King County, Washington
- Budget family: adopted biennial budget context
- Official owner: King County Council
- Public inspection URL: `https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27`
- Candidate machine URL: `https://cdn.kingcounty.gov/-/media/king-county/depts/council/budget/2026/2026-2027-adopted-budget-book.pdf?rev=9cbb996d2da046b8a37ff02ff8009e73&hash=A256B6946888EE7A4A6BB3BA3D6A82FA`
- Source type: official web page plus PDF/document source
- Source priority: official adopted budget framing context for broad budget-size questions

## Official Source Inventory

| Candidate | Owner | URL | Type | Notes |
|---|---|---|---|---|
| King County 2026-27 Budget Process page | King County Council | `https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27` | Official page | States the council reviewed and adopted a two-year `$20.16 billion` budget for 2026 and 2027 and links adopted documents. |
| Adopted Budget Book | King County Council | `https://cdn.kingcounty.gov/-/media/king-county/depts/council/budget/2026/2026-2027-adopted-budget-book.pdf?rev=9cbb996d2da046b8a37ff02ff8009e73&hash=A256B6946888EE7A4A6BB3BA3D6A82FA` | PDF | Official adopted budget book; useful as citation/context, not normalized in this milestone. |
| Adopted budget ordinance file 2025-0288 | King County Council Legislation | `https://mkcclegisearch.kingcounty.gov/LegislationDetail.aspx?ID=7680373&GUID=B4E9E09C-A982-4A8C-A0DA-6CC195D69EE0&Options=Advanced&Search=` | Legislation page | Title says it adopts the 2026-2027 Biennial Budget and makes appropriations for county agencies, departments, and capital improvements. |
| King County Open Budget Dashboard | King County / Microsoft Power BI Gov | `https://kingcounty.gov/en/dept/executive/governance-leadership/performance-strategy-budget/budget/budget-dashboard` | Dashboard snapshot | Existing accepted annual dashboard source. Keep separate from adopted biennial context. |

## Surface Classification

Access candidates:

- [ ] Official documented API
- [ ] Official open data portal
- [ ] Official bulk download
- [ ] Official public dashboard
- [x] Official document/PDF
- [x] HTML page context
- [ ] Unofficial mirror/context source
- [ ] Not usable

Probe methods attempted:

- [x] Generic HTML/header probe
- [x] Document/PDF probe
- [x] Legislation page probe
- [ ] PDF table extraction

Evidence:

```text
Council budget page canonical URL observed: https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27
Council page metadata and visible body state that the council reviewed and adopted a two-year $20.16 billion budget for 2026 and 2027.
Council page links the adopted budget ordinance file and the adopted budget book PDF.
Adopted budget book HEAD observed: HTTP 200; content-type application/pdf; content-length 8,833,003; last-modified Thu, 05 Mar 2026 21:03:17 GMT; etag 18a342e254d24a50b6c93d9e5f23e16b.
Legislation page title observed: AN ORDINANCE that adopts the 2026-2027 Biennial Budget and makes appropriations for county agencies, departments, and capital improvements for the biennium beginning January 1, 2026, and ending December 31, 2027.
```

Primary access surface:

```text
official HTML page and adopted budget PDF
```

Primary source identifiers:

```text
king_county.adopted_budget
public page URL
adopted budget book PDF URL
legislation file ID 2025-0288 / ordinance context
```

Companion surfaces:

```text
king_county.open_budget_dashboard remains the accepted annual dashboard source for budgeted revenue, expenditure, and FTE.
```

## Extraction Approach

Recommended access method:

```text
accept-context-only
```

Why:

```text
The immediate Scale failure is headline framing, not a need for line-item extraction. The official page supplies a stable adopted two-year total and ordinance/document links. Normal answers should cite it as context beside the existing annual dashboard snapshot rather than parse PDF tables in this milestone.
```

## Storage Policy

Recommended storage tier:

```text
context_only
```

Why:

```text
The source should influence broad budget-size framing and caveats, but the normalized answer data remains the existing Open Budget Dashboard snapshot until a narrow adopted-budget table/parser is justified.
```

Normal answer source:

```text
none; cite official context page/PDF when the adopted biennial frame matters.
```

Freshness check:

```text
manual source-card metadata: official page URL, PDF content length, PDF last-modified, PDF etag, and observed adopted amount.
```

Repo artifacts:

```text
source card, probe, skill guidance, benchmark update
```

## Supported Questions

- What official adopted biennial context should frame a broad King County budget-size answer?
- What is the council-adopted 2026-2027 headline budget amount?
- Why should the annual Open Budget Dashboard FY2026 expenditure value not be treated as the same frame as the adopted two-year budget?

## Unsupported Claims

- Department-level adopted budget rows from the PDF.
- Adopted-budget actual spending, vendor payments, invoices, procurement, or payroll.
- A normalized replacement for the Open Budget Dashboard snapshot.
- Any claim that the 2026 annual dashboard budgeted expenditure and 2026-2027 adopted biennial budget are directly comparable.

## Validation Checks

| Check | Expected result | How to reproduce |
|---|---:|---|
| Council page reachable | HTTP 200 and budget process page title | `curl -sS <page-url> \| rg -i 'King County 2026-27 Budget Process'` |
| Adopted headline amount | `$20.16 billion` | `curl -sS <page-url> \| rg -i '20\\.16'` |
| Adopted budget book reachable | HTTP 200 PDF | `curl -sIL <pdf-url>` |
| Adopted budget book metadata | content-length `8833003`, last-modified `Thu, 05 Mar 2026 21:03:17 GMT` | `curl -sIL <pdf-url>` |
| Legislation page identifies ordinance purpose | adopts the `2026-2027 Biennial Budget` | `curl -sS <legislation-url> \| rg -i '2026-2027 Biennial Budget'` |

## Source Fingerprint

Citation fields:

```text
source_id: king_county.adopted_budget
official_owner: King County Council
public_inspection_url: https://kingcounty.gov/en/dept/council/governance-leadership/county-council/budget-review-2026-27
adopted_budget_book_url: https://cdn.kingcounty.gov/-/media/king-county/depts/council/budget/2026/2026-2027-adopted-budget-book.pdf?rev=9cbb996d2da046b8a37ff02ff8009e73&hash=A256B6946888EE7A4A6BB3BA3D6A82FA
legislation_url: https://mkcclegisearch.kingcounty.gov/LegislationDetail.aspx?ID=7680373&GUID=B4E9E09C-A982-4A8C-A0DA-6CC195D69EE0&Options=Advanced&Search=
adopted_period: 2026-2027
adopted_amount: 20160000000
adopted_amount_label: $20.16 billion
pdf_content_length_observed: 8833003
pdf_last_modified_observed: Thu, 05 Mar 2026 21:03:17 GMT
pdf_etag_observed: 18a342e254d24a50b6c93d9e5f23e16b
```

## Benchmark Impact

The King County current budget-size case should expect `side_by_side_only`: use `king_county.open_budget_dashboard` for annual dashboard budgeted expenditure and `king_county.adopted_budget` for official adopted biennial context. Do not collapse those frames into one headline number.

## Recommendation

Accept `king_county.adopted_budget` as a context-only source. Consider a future narrow PDF/table extraction only if users need adopted budget detail below the headline adopted biennial framing.
