#!/usr/bin/env python3
"""Build the Washington OFM April 1 population checked-in snapshot."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "ofm-population.source.json"
NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
PKG_REL_NS = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
EXPECTED_HEADERS = [
    "Line",
    "Filter",
    "County",
    "Jurisdiction",
    "2020 Population Census",
    "2021 Population Estimate",
    "2022 Population Estimate",
    "2023 Population Estimate",
    "2024 Population Estimate",
    "2025 Population Estimate",
]
ROW_TYPES = {
    "1": "county",
    "2": "unincorporated_county",
    "3": "incorporated_county",
    "4": "city_town",
    "100": "state_total",
    "200": "unincorporated_state_total",
    "300": "incorporated_state_total",
}


class PopulationExtractError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Washington OFM population snapshot.")
    parser.add_argument(
        "--source-file",
        type=Path,
        help="Use a local XLSX file instead of downloading the official source.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Snapshot directory. Defaults to the source card snapshot_version path.",
    )
    return parser.parse_args()


def main() -> None:
    source = load_json(SOURCE_CARD_PATH)
    args = parse_args()
    output_dir = args.output_dir or (
        ROOT
        / "jurisdictions"
        / "washington"
        / "data"
        / "ofm-population"
        / source["snapshot_version"]
    )
    if args.source_file:
        xlsx_bytes = args.source_file.read_bytes()
        file_metadata = {
            "url": source["source_file_url"],
            "content_length": len(xlsx_bytes),
            "last_modified": source["source_file_last_modified"],
            "etag": source["source_file_etag"],
            "sha256": sha256_bytes(xlsx_bytes),
            "fetched_at": utc_now(),
            "source": str(args.source_file),
        }
    else:
        xlsx_bytes, file_metadata = download_source(source["source_file_url"])
    build_snapshot(source, xlsx_bytes, file_metadata, output_dir)
    print(f"Wrote Washington OFM population snapshot to {output_dir}")


def build_snapshot(
    source: dict[str, Any],
    xlsx_bytes: bytes,
    file_metadata: dict[str, Any],
    output_dir: Path,
) -> None:
    parsed = parse_population_workbook(xlsx_bytes)
    rows = build_normalized_rows(parsed)
    summary = build_summary(source, parsed, rows, file_metadata)
    provenance = build_provenance(source, parsed, summary, file_metadata)

    normalized_dir = output_dir / "normalized"
    write_jsonl(normalized_dir / "population-estimates.jsonl", rows)
    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "provenance.json", provenance)


def parse_population_workbook(xlsx_bytes: bytes) -> dict[str, Any]:
    sheets = parse_workbook_sheets(xlsx_bytes)
    population_rows = sheets.get("Population")
    notation_rows = sheets.get("Notations")
    if population_rows is None:
        raise PopulationExtractError("Population sheet is missing.")
    if notation_rows is None:
        raise PopulationExtractError("Notations sheet is missing.")

    header_index = find_header_row(population_rows)
    headers = normalize_headers(population_rows[header_index])
    if headers != EXPECTED_HEADERS:
        raise PopulationExtractError(f"unexpected headers: {headers}")

    notation_lookup = parse_notations(notation_rows)
    geography_rows = []
    separator_rows = 0
    for excel_row_number, row in enumerate(population_rows[header_index + 1 :], start=header_index + 2):
        if not row:
            continue
        line = cell_text(row, 0)
        if not line:
            continue
        if not line.isdigit():
            continue
        filter_value = cell_text(row, 1)
        if filter_value == ".":
            separator_rows += 1
            continue
        row_type = ROW_TYPES.get(filter_value)
        if row_type is None:
            raise PopulationExtractError(
                f"unknown row filter {filter_value!r} on Excel row {excel_row_number}"
            )
        values = dict(zip(headers, row))
        source_line = int(line)
        geography_rows.append(
            {
                "source_line": source_line,
                "row_type": row_type,
                "filter": int(filter_value),
                "county": normalize_space(values["County"]),
                "jurisdiction": normalize_space(values["Jurisdiction"]),
                "values": {
                    "2020": parse_int(values["2020 Population Census"]),
                    "2021": parse_int(values["2021 Population Estimate"]),
                    "2022": parse_int(values["2022 Population Estimate"]),
                    "2023": parse_int(values["2023 Population Estimate"]),
                    "2024": parse_int(values["2024 Population Estimate"]),
                    "2025": parse_int(values["2025 Population Estimate"]),
                },
                "notations": notation_lookup.get(source_line, {}),
            }
        )
    return {
        "sheet_names": list(sheets),
        "headers": headers,
        "geography_rows": geography_rows,
        "separator_rows": separator_rows,
    }


def build_normalized_rows(parsed: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in parsed["geography_rows"]:
        for year, population in item["values"].items():
            value_kind = "census" if year == "2020" else "estimate"
            row = {
                "source_line": item["source_line"],
                "row_type": item["row_type"],
                "county": item["county"],
                "jurisdiction": item["jurisdiction"],
                "year": int(year),
                "value_kind": value_kind,
                "population": population,
                "geography_basis": "resident_jurisdiction",
            }
            if value_kind == "estimate":
                row["estimate_date"] = f"{year}-04-01"
            else:
                row["census_year"] = int(year)
            notation = item.get("notations", {}).get(year, "")
            if notation:
                row["notation"] = notation
            rows.append(row)
    return rows


def build_summary(
    source: dict[str, Any],
    parsed: dict[str, Any],
    rows: list[dict[str, Any]],
    file_metadata: dict[str, Any],
) -> dict[str, Any]:
    geography_rows = parsed["geography_rows"]
    row_counts = {
        "geography_rows": len(geography_rows),
        "population_estimates": len(rows),
        "county_rows": count_geographies(geography_rows, "county"),
        "unincorporated_county_rows": count_geographies(geography_rows, "unincorporated_county"),
        "incorporated_county_rows": count_geographies(geography_rows, "incorporated_county"),
        "city_town_rows": count_geographies(geography_rows, "city_town"),
        "state_total_rows": count_geographies(geography_rows, "state_total"),
        "separator_rows": parsed["separator_rows"],
    }
    checks = validation_checks(geography_rows)
    fingerprint = source_fingerprint(source, row_counts, checks, file_metadata)
    return {
        "source_id": source["id"],
        "snapshot_version": source["snapshot_version"],
        "release": source["release"],
        "latest_estimate_date": source["latest_estimate_date"],
        "source_file": file_metadata,
        "row_counts": row_counts,
        "validation_checks": checks,
        "source_fingerprint": fingerprint,
    }


def build_provenance(
    source: dict[str, Any],
    parsed: dict[str, Any],
    summary: dict[str, Any],
    file_metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "source_id": source["id"],
        "access_method": source["access_method"],
        "snapshot_version": source["snapshot_version"],
        "release": source["release"],
        "public_inspection_url": source["official_page"],
        "source_file": file_metadata,
        "workbook": {
            "sheet_names": parsed["sheet_names"],
            "population_headers": parsed["headers"],
        },
        "source_fingerprint": summary["source_fingerprint"],
    }


def source_fingerprint(
    source: dict[str, Any],
    row_counts: dict[str, int],
    checks: dict[str, Any],
    file_metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "public_inspection_urls": [
            source["official_page"],
            source["source_file_url"],
            source["official_pdf_url"],
        ],
        "machine_access": {
            "type": "official_bulk_download",
            "accepted_source_surfaces": ["april1_population_final_xlsx"],
            "file_url": source["source_file_url"],
            "content_type": file_metadata.get("content_type"),
        },
        "retrieval_context": {
            "source_surface_id": "april1_population_final_xlsx",
            "workbook_sheet": "Population",
            "notation_sheet": "Notations",
            "normalized_table": "population-estimates.jsonl",
        },
        "version_boundary": {
            "snapshot_version": source["snapshot_version"],
            "release": source["release"],
            "latest_estimate_date": source["latest_estimate_date"],
            "file_last_modified": file_metadata.get("last_modified"),
            "file_etag": file_metadata.get("etag"),
            "file_sha256": file_metadata.get("sha256"),
        },
        "row_counts": row_counts,
        "checks": checks,
    }


def validation_checks(geography_rows: list[dict[str, Any]]) -> dict[str, Any]:
    seattle = find_population_row(geography_rows, "Seattle", "city_town")
    king = find_population_row(geography_rows, "King County", "county")
    king_unincorporated = find_population_row(
        geography_rows,
        "Unincorporated King County",
        "unincorporated_county",
    )
    king_incorporated = find_population_row(
        geography_rows,
        "Incorporated King County",
        "incorporated_county",
    )
    state_total = find_population_row(geography_rows, "State Total", "state_total")
    king_city_town_total = sum(
        row["values"]["2025"]
        for row in geography_rows
        if row["county"] == "King" and row["row_type"] == "city_town"
    )
    return {
        "latest_estimate_year": 2025,
        "latest_estimate_date": "2025-04-01",
        "seattle_2025_population": seattle["values"]["2025"],
        "king_county_2025_population": king["values"]["2025"],
        "state_total_2025_population": state_total["values"]["2025"],
        "king_county_unincorporated_2025_population": king_unincorporated["values"]["2025"],
        "king_county_incorporated_2025_population": king_incorporated["values"]["2025"],
        "king_county_city_town_sum_2025": king_city_town_total,
        "king_county_incorporated_reconciles": (
            king_city_town_total == king_incorporated["values"]["2025"]
        ),
        "king_county_total_reconciles": (
            king_unincorporated["values"]["2025"] + king_incorporated["values"]["2025"]
            == king["values"]["2025"]
        ),
    }


def count_geographies(rows: list[dict[str, Any]], row_type: str) -> int:
    return sum(1 for row in rows if row["row_type"] == row_type)


def find_population_row(
    rows: list[dict[str, Any]],
    jurisdiction: str,
    row_type: str,
) -> dict[str, Any]:
    for row in rows:
        if row["jurisdiction"] == jurisdiction and row["row_type"] == row_type:
            return row
    raise PopulationExtractError(f"missing {row_type} row for {jurisdiction}")


def parse_notations(rows: list[list[str]]) -> dict[int, dict[str, str]]:
    header_index = next(
        index
        for index, row in enumerate(rows)
        if [normalize_header(cell) for cell in row[:4]] == ["Line", "Filter", "County", "Jurisdiction"]
    )
    lookup: dict[int, dict[str, str]] = {}
    for row in rows[header_index + 1 :]:
        line = cell_text(row, 0)
        if not line or not line.isdigit():
            continue
        notes = {}
        for column_index, year in enumerate(("2020", "2021", "2022", "2023", "2024", "2025"), start=4):
            note = normalize_space(cell_text(row, column_index))
            if note:
                notes[year] = note
        if notes:
            lookup[int(line)] = notes
    return lookup


def parse_workbook_sheets(xlsx_bytes: bytes) -> dict[str, list[list[str]]]:
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes)) as archive:
        shared_strings = read_shared_strings(archive)
        sheet_paths = workbook_sheet_paths(archive)
        return {
            name: parse_sheet_rows(archive, path, shared_strings)
            for name, path in sheet_paths.items()
        }


def workbook_sheet_paths(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        relationship.get("Id"): relationship.get("Target")
        for relationship in relationships.findall("r:Relationship", PKG_REL_NS)
    }
    sheet_paths = {}
    for sheet in workbook.findall("a:sheets/a:sheet", NS):
        name = sheet.get("name")
        relationship_id = sheet.get(REL_NS)
        target = targets.get(relationship_id)
        if not name or not target:
            continue
        sheet_paths[name] = normalize_workbook_target(target)
    return sheet_paths


def normalize_workbook_target(target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return f"xl/{target}"


def parse_sheet_rows(
    archive: zipfile.ZipFile,
    sheet_path: str,
    shared_strings: list[str],
) -> list[list[str]]:
    root = ET.fromstring(archive.read(sheet_path))
    parsed_rows = []
    for row in root.findall(".//a:sheetData/a:row", NS):
        cells = {}
        for cell in row.findall("a:c", NS):
            ref = cell.get("r", "A1")
            cells[column_number(ref)] = xlsx_cell_text(cell, shared_strings)
        max_column = max(cells, default=0)
        parsed_rows.append([cells.get(index, "") for index in range(1, max_column + 1)])
    return parsed_rows


def find_header_row(rows: list[list[str]]) -> int:
    for index, row in enumerate(rows):
        headers = normalize_headers(row)
        if headers[:4] == ["Line", "Filter", "County", "Jurisdiction"]:
            return index
    raise PopulationExtractError("header row not found")


def normalize_headers(row: list[str]) -> list[str]:
    return [normalize_header(cell) for cell in row[: len(EXPECTED_HEADERS)]]


def normalize_header(value: Any) -> str:
    text = normalize_space(str(value))
    text = text.replace("\u00b9", "")
    return text


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(text.text or "" for text in item.findall(".//a:t", NS)) for item in root.findall("a:si", NS)]


def xlsx_cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//a:is//a:t", NS))
    value = cell.find("a:v", NS)
    text = "" if value is None else value.text or ""
    if cell_type == "s" and text.isdigit():
        return shared_strings[int(text)]
    return text


def column_number(cell_ref: str) -> int:
    number = 0
    for character in "".join(ch for ch in cell_ref if ch.isalpha()).upper():
        number = number * 26 + ord(character) - 64
    return number


def cell_text(row: list[Any], index: int) -> str:
    if index >= len(row):
        return ""
    return normalize_space(str(row[index]))


def parse_int(value: Any) -> int:
    text = normalize_space(str(value))
    if not text:
        raise PopulationExtractError("missing integer value")
    try:
        return int(float(text))
    except ValueError as exc:
        raise PopulationExtractError(f"invalid integer value: {value!r}") from exc


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def download_source(url: str) -> tuple[bytes, dict[str, Any]]:
    request = Request(url, headers={"User-Agent": "civic-agent-source-probe/1.0"})
    with urlopen(request, timeout=60) as response:
        data = response.read()
        headers = response.headers
    return data, {
        "url": url,
        "content_type": headers.get("content-type"),
        "content_length": int(headers.get("content-length") or len(data)),
        "last_modified": headers.get("last-modified"),
        "etag": headers.get("etag"),
        "sha256": sha256_bytes(data),
        "fetched_at": utc_now(),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    try:
        main()
    except PopulationExtractError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
