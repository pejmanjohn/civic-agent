#!/usr/bin/env python3
"""Snapshot DOR Local Taxing District Levy Detail (statewide property tax).

Downloads the annual All_County_Levy_Detail_{YEAR}.xlsx files from the
Washington Department of Revenue, parses them with the stdlib OOXML pattern
used by the other extractors, decodes the 9-digit TDCODE scheme, and writes a
checked-in snapshot with two years so year-over-year questions are answerable.

Probe brief: docs/source-probes/washington-dor-property-tax-levies.md
Key traps encoded here:
- prior-year column HEADERS embed shifting literal years -> parse positionally,
  gated by a header-shape check on the stable leading columns;
- one row per LEVY (base levy, lid lifts, and bonds are separate rows) ->
  district_key (TDCODE bytes 1-7) is the aggregation key;
- DOR upload directories (/files/YYYY-MM/) move on silent re-uploads -> the
  URLs below were verified 2026-07-13; refresh by re-scraping the landing page.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = ROOT / "jurisdictions" / "washington" / "data" / "dor-property-tax-levies"
VERSION = "levies-due-2025"

LANDING_PAGE = "https://dor.wa.gov/about/statistics-reports/data-statistics/local-taxing-district-levy-detail"
FILE_URLS = {
    2025: "https://dor.wa.gov/sites/default/files/2025-10/All_County_Levy_Detail_2025.xlsx",
    2024: "https://dor.wa.gov/sites/default/files/2025-02/All_County_Levy_Detail_2024.xlsx",
}
SHEET_NAME = "Levy_Detail"
TDCODE_PATTERN = re.compile(r"^\d{9}$")
EXPECTED_LEADING_HEADERS = ["Taxing District Code", "DISTRICT NAME"]

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
PKG_REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

# Washington's 39 counties in alphabetical order = TDCODE county prefix.
COUNTIES = [
    "Adams", "Asotin", "Benton", "Chelan", "Clallam", "Clark", "Columbia",
    "Cowlitz", "Douglas", "Ferry", "Franklin", "Garfield", "Grant",
    "Grays Harbor", "Island", "Jefferson", "King", "Kitsap", "Kittitas",
    "Klickitat", "Lewis", "Lincoln", "Mason", "Okanogan", "Pacific",
    "Pend Oreille", "Pierce", "San Juan", "Skagit", "Skamania", "Snohomish",
    "Spokane", "Stevens", "Thurston", "Wahkiakum", "Walla Walla", "Whatcom",
    "Whitman", "Yakima",
]
COUNTY_BY_CODE = {f"{index:02d}": name for index, name in enumerate(COUNTIES, start=1)}

# TDCODE bytes 3-4 per LevyDetailExplan.pdf (known values; others pass through).
DISTRICT_TYPES = {
    "00": "state_school",
    "01": "county",
    "02": "road",
    "03": "city",
    "04": "local_school",
    "05": "library",
    "06": "hospital",
    "07": "fire",
    "08": "metro_park",
    "09": "port",
    "10": "port",
    "12": "ems",
    "28": "regional_fire_authority",
    "30": "regional_transit_authority",
}

# TDCODE byte 8 levy types (known values; others pass through).
LEVY_TYPES = {
    "0": "regular",
    "1": "school_enrichment",
    "2": "capital_projects_transportation",
    "3": "school_bond",
    "4": "non_school_bond",
}


class LevyExtractError(RuntimeError):
    pass


def parse_xml(payload: bytes) -> ET.Element:
    """Stdlib ET with a DTD guard: XXE and entity-expansion (billion-laughs)
    attacks both require a DOCTYPE, which legitimate OOXML parts never carry.
    The repo is stdlib-only by convention, so guard instead of adding
    defusedxml."""
    if b"<!DOCTYPE" in payload[:4096].upper():
        raise LevyExtractError("XML part contains a DOCTYPE; refusing to parse.")
    return ET.fromstring(payload)


def download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "civic-agent-dor-extractor (+https://github.com/pejmanjohn/civic-agent)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def parse_sheet(xlsx_bytes: bytes, sheet_name: str) -> list[list[str]]:
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes)) as archive:
        shared = read_shared_strings(archive)
        workbook = parse_xml(archive.read("xl/workbook.xml"))
        relationships = parse_xml(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {
            rel.get("Id"): rel.get("Target")
            for rel in relationships.findall("r:Relationship", PKG_REL_NS)
        }
        sheet_path = None
        for sheet in workbook.findall("a:sheets/a:sheet", NS):
            if sheet.get("name") == sheet_name:
                target = targets[sheet.get(REL_NS)]
                sheet_path = target.lstrip("/") if target.startswith("/") else f"xl/{target}"
                break
        if sheet_path is None:
            raise LevyExtractError(f"sheet not found: {sheet_name}")
        root = parse_xml(archive.read(sheet_path))
    rows = []
    for row in root.findall(".//a:sheetData/a:row", NS):
        cells = {}
        for cell in row.findall("a:c", NS):
            cells[column_number(cell.get("r", "A1"))] = cell_text(cell, shared)
        width = max(cells, default=0)
        rows.append([cells.get(index, "") for index in range(1, width + 1)])
    return rows


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = parse_xml(archive.read("xl/sharedStrings.xml"))
    return [
        "".join(text.text or "" for text in item.findall(".//a:t", NS))
        for item in root.findall("a:si", NS)
    ]


def cell_text(cell: ET.Element, shared: list[str]) -> str:
    if cell.get("t") == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//a:is//a:t", NS))
    value = cell.find("a:v", NS)
    text = "" if value is None else value.text or ""
    if cell.get("t") == "s" and text.isdigit():
        return shared[int(text)]
    return text


def column_number(ref: str) -> int:
    number = 0
    for character in "".join(ch for ch in ref if ch.isalpha()).upper():
        number = number * 26 + ord(character) - 64
    return number


def check_header_shape(rows: list[list[str]]) -> None:
    """The prior-year header text shifts every edition; the stable leading
    columns gate positional parsing."""
    for row in rows[:12]:
        leading = [str(cell).strip() for cell in row[:2]]
        if leading and leading[0].startswith(EXPECTED_LEADING_HEADERS[0]):
            if len(leading) > 1 and EXPECTED_LEADING_HEADERS[1] in leading[1].upper().replace("  ", " "):
                return
            if len(leading) > 1 and leading[1].strip().upper().startswith("DISTRICT"):
                return
    raise LevyExtractError(
        "Header shape changed: 'Taxing District Code' / 'DISTRICT NAME' leading "
        "columns not found. Re-probe before parsing positionally."
    )


def parse_number(value: str) -> float | None:
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def normalize_rows(rows: list[list[str]], year: int) -> list[dict]:
    check_header_shape(rows)
    records = []
    for row in rows:
        code = str(row[0]).strip() if row else ""
        if not TDCODE_PATTERN.match(code):
            continue
        county_code = code[0:2]
        district_type_code = code[2:4]
        levy_type_code = code[7]
        records.append(
            {
                "year_due": year,
                "tdcode": code,
                "district_key": code[0:7],
                "county_code": county_code,
                "county": COUNTY_BY_CODE.get(county_code, f"unknown_{county_code}"),
                "district_type_code": district_type_code,
                "district_type": DISTRICT_TYPES.get(
                    district_type_code, f"other_{district_type_code}"
                ),
                "levy_type_code": levy_type_code,
                "levy_type": LEVY_TYPES.get(levy_type_code, f"other_{levy_type_code}"),
                "district_name": str(row[1]).strip() if len(row) > 1 else "",
                "assessed_value": parse_number(row[2]) if len(row) > 2 else None,
                "levy_rate_per_1000": parse_number(row[3]) if len(row) > 3 else None,
                "district_levy": parse_number(row[4]) if len(row) > 4 else None,
                "highest_prior_levy": parse_number(row[5]) if len(row) > 5 else None,
                "statutory_maximum_rate": parse_number(row[14]) if len(row) > 14 else None,
            }
        )
    if not records:
        raise LevyExtractError(f"no levy rows parsed for {year}")
    return records


def levy_sum(records: list[dict], predicate) -> float:
    return round(sum(r["district_levy"] or 0 for r in records if predicate(r)), 2)


def main() -> None:
    all_records: list[dict] = []
    file_provenance = []
    for year in sorted(FILE_URLS):
        url = FILE_URLS[year]
        payload = download(url)
        rows = parse_sheet(payload, SHEET_NAME)
        records = normalize_rows(rows, year)
        all_records.extend(records)
        file_provenance.append(
            {
                "year_due": year,
                "url": url,
                "content_length": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "levy_rows": len(records),
            }
        )

    by_year = {}
    for record in all_records:
        by_year.setdefault(record["year_due"], []).append(record)

    checks = {}
    for year, records in sorted(by_year.items()):
        prefix = f"year_{year}"
        checks[f"{prefix}_rows"] = len(records)
        checks[f"{prefix}_statewide_levy_total"] = levy_sum(records, lambda r: True)
        checks[f"{prefix}_king_county_levy_total"] = levy_sum(
            records, lambda r: r["county_code"] == "17"
        )
        checks[f"{prefix}_school_enrichment_total"] = levy_sum(
            records,
            lambda r: r["district_type_code"] == "04" and r["levy_type_code"] == "1",
        )
        checks[f"{prefix}_distinct_counties"] = len({r["county_code"] for r in records})
    seattle_sd = {
        record["year_due"]: record
        for record in all_records
        if record["tdcode"] == "170400110"
    }
    for year, record in sorted(seattle_sd.items()):
        checks[f"seattle_sd_enrichment_levy_{year}"] = record["district_levy"]
        checks[f"seattle_sd_enrichment_rate_{year}"] = record["levy_rate_per_1000"]

    out_dir = DATA_ROOT / VERSION
    normalized_dir = out_dir / "normalized"
    normalized_dir.mkdir(parents=True, exist_ok=True)
    all_records.sort(key=lambda r: (r["year_due"], r["tdcode"]))
    with (normalized_dir / "levy-detail.jsonl").open("w", encoding="utf-8") as handle:
        for record in all_records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    row_counts = {"levy-detail.jsonl": len(all_records)}
    summary = {
        "source_id": "washington.dor_property_tax_levies",
        "snapshot_version": VERSION,
        "years_due": sorted(by_year),
        "grain": "one row per levy; district_key (TDCODE bytes 1-7) is the district aggregation key",
        "measures": ["district_levy (dollars)", "levy_rate_per_1000 (dollars per $1,000 assessed value)"],
        "row_counts": row_counts,
        "validation_checks": checks,
        "source_fingerprint": {
            "snapshot_version": VERSION,
            "public_inspection_urls": [LANDING_PAGE],
            "row_counts": row_counts,
            "checks": checks,
        },
    }
    write_json(out_dir / "summary.json", summary)

    provenance = {
        "source_id": "washington.dor_property_tax_levies",
        "snapshot_version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generator": "jurisdictions/washington/scripts/extract_dor_levy_detail.py",
        "landing_page": LANDING_PAGE,
        "source_files": file_provenance,
        "code_scheme_reference": "https://dor.wa.gov/sites/default/files/2022-02/LevyDetailExplan.pdf",
        "source_fingerprint": {
            "snapshot_version": VERSION,
            "public_inspection_urls": [LANDING_PAGE],
            "row_counts": row_counts,
            "checks": checks,
        },
    }
    write_json(out_dir / "provenance.json", provenance)

    print(
        json.dumps(
            {
                "ok": True,
                "snapshot_version": VERSION,
                "rows": len(all_records),
                "checks": checks,
                "output_dir": str(out_dir.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )


def write_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
