#!/usr/bin/env python3
"""Build a managed local database for Washington Fiscal WA Open Checkbook."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zipfile import ZipFile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "open-checkbook.source.json"
REQUIRED_HEADERS = [
    "Bien",
    "FY",
    "FMonth",
    "Agy",
    "Agency",
    "Object",
    "Category",
    "Subobj",
    "SubCategory",
    "Vendor",
    "Amount",
]
HEADER_ALIASES = {
    "Fiscal Month": "FMonth",
}
NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


class CheckbookExtractError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Washington Open Checkbook local DB.")
    parser.add_argument(
        "--data-home",
        type=Path,
        default=Path(os.environ.get("CIVIC_AGENT_DATA_HOME", ".civic-agent-data")),
        help="Data cache root. Defaults to .civic-agent-data for direct script runs.",
    )
    parser.add_argument("--force", action="store_true", help="Rebuild even if a DB exists.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scripts_dir = ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import source_data

    source = load_json(SOURCE_CARD_PATH)
    context = source_data.SourceContext(
        source_id=source["id"],
        source_card={**source, "_path": SOURCE_CARD_PATH.relative_to(ROOT).as_posix()},
        data_home=args.data_home,
        source_dir=args.data_home / "sources" / "washington" / "open_checkbook",
        manifest_path=args.data_home / "sources" / "washington" / "open_checkbook" / "manifest.json",
    )
    result = build_local_database(context, args.force)
    source_data.write_json(context.manifest_path, result)
    print(json.dumps(result, indent=2, sort_keys=True))


def build_local_database(context: Any, force: bool) -> dict[str, Any]:
    db_path = context.source_dir / "open_checkbook.sqlite"
    if db_path.is_file() and context.manifest_path.is_file() and not force:
        manifest = load_json(context.manifest_path)
        manifest["status"] = manifest.get("status", "current")
        manifest["message"] = "Local database already exists."
        return manifest

    context.source_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = context.source_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    file_entries = []
    for surface_id, surface in accepted_surfaces(context.source_card).items():
        local_path = raw_dir / Path(surface["url"]).name
        download_file(surface["url"], local_path)
        file_entries.append(
            {
                "source_surface_id": surface_id,
                "biennium": surface["biennium"],
                "url": surface["url"],
                "path": local_path,
                "last_modified": surface.get("last_modified"),
                "expected_content_length": surface.get("content_length"),
            }
        )

    return build_database_from_files(context.source_card, file_entries, db_path)


def run_named_query(context: Any, named_query: str, params: dict[str, str]) -> dict[str, Any]:
    manifest = load_json(context.manifest_path)
    db_path = Path(manifest["database_path"])
    if not db_path.is_file():
        raise CheckbookExtractError(f"Local database is missing: {db_path}")

    biennium = params.get("biennium") or manifest.get("current_biennium")
    limit = int(params.get("limit", "10"))
    filters = ["biennium = ?"]
    values: list[Any] = [biennium]
    if params.get("agency_code"):
        filters.append("agency_code = ?")
        values.append(params["agency_code"])
    if params.get("category"):
        filters.append("category = ?")
        values.append(params["category"])
    where = " AND ".join(filters)

    query_map = {
        "category_breakdown": (
            "category",
            f"""
            SELECT category AS name, SUM(amount) AS amount, COUNT(*) AS payment_rows
            FROM payments
            WHERE {where}
            GROUP BY category
            ORDER BY amount DESC
            LIMIT ?
            """,
        ),
        "agency_totals": (
            "agency",
            f"""
            SELECT agency_code, agency_name AS name, SUM(amount) AS amount, COUNT(*) AS payment_rows
            FROM payments
            WHERE {where}
            GROUP BY agency_code, agency_name
            ORDER BY amount DESC
            LIMIT ?
            """,
        ),
        "vendor_totals": (
            "vendor",
            f"""
            SELECT vendor_name AS name, SUM(amount) AS amount, COUNT(*) AS payment_rows
            FROM payments
            WHERE {where}
            GROUP BY vendor_name
            ORDER BY amount DESC
            LIMIT ?
            """,
        ),
        "monthly_trend": (
            "calendar_month",
            f"""
            SELECT calendar_month AS name, SUM(amount) AS amount, COUNT(*) AS payment_rows
            FROM payments
            WHERE {where}
            GROUP BY calendar_month
            ORDER BY calendar_month
            LIMIT ?
            """,
        ),
    }
    if named_query not in query_map:
        raise CheckbookExtractError(f"Unknown Open Checkbook query: {named_query}")
    grain, sql = query_map[named_query]
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = [dict(row) for row in conn.execute(sql, [*values, limit])]
    return {
        "ok": True,
        "source_id": context.source_id,
        "named_query": named_query,
        "grain": grain,
        "measure": "amount",
        "params": params,
        "biennium": biennium,
        "data_through": manifest.get("data_through"),
        "database_path": str(db_path),
        "rows": rows,
    }


def accepted_surfaces(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        surface_id: surface
        for surface_id, surface in source.get("source_surfaces", {}).items()
        if surface.get("status") == "accepted"
    }


def build_database_from_files(
    source: dict[str, Any],
    file_entries: list[dict[str, Any]],
    db_path: Path,
) -> dict[str, Any]:
    temp_path = db_path.with_suffix(".tmp.sqlite")
    if temp_path.exists():
        temp_path.unlink()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    source_file_results = []
    current_biennium = source.get("current_biennium")
    current_months: list[str] = []
    started_at = utc_now()

    with sqlite3.connect(temp_path) as conn:
        create_schema(conn)
        for entry in file_entries:
            rows = parse_xlsx_rows(entry["path"])
            row_count = 0
            for row in rows:
                normalized = normalize_payment_row(row)
                insert_payment(conn, normalized)
                row_count += 1
                if normalized["biennium"] == current_biennium:
                    current_months.append(normalized["calendar_month"])
            sha256 = sha256_file(entry["path"])
            content_length = entry["path"].stat().st_size
            conn.execute(
                """
                INSERT INTO source_files (
                  source_surface_id, biennium, url, fetched_at, last_modified,
                  content_length, sha256, row_count, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["source_surface_id"],
                    entry["biennium"],
                    entry["url"],
                    utc_now(),
                    entry.get("last_modified"),
                    content_length,
                    sha256,
                    row_count,
                    "accepted",
                ),
            )
            source_file_results.append(
                {
                    "source_surface_id": entry["source_surface_id"],
                    "biennium": entry["biennium"],
                    "url": entry["url"],
                    "path": str(entry["path"]),
                    "last_modified": entry.get("last_modified"),
                    "content_length": content_length,
                    "sha256": sha256,
                    "row_count": row_count,
                }
            )
            total_rows += row_count
        create_indexes(conn)
        conn.execute(
            """
            INSERT INTO refresh_runs (run_id, started_at, finished_at, status, message)
            VALUES (?, ?, ?, ?, ?)
            """,
            (started_at, started_at, utc_now(), "current", "Built local database."),
        )
        conn.commit()

    if total_rows == 0:
        temp_path.unlink(missing_ok=True)
        raise CheckbookExtractError("No payment rows were parsed; refusing to replace database.")

    shutil.move(str(temp_path), db_path)
    data_through = max(current_months) if current_months else source.get("current_data_through")
    return {
        "ok": True,
        "status": "partial_current_period" if data_through else "current",
        "storage_tier": "managed_local_db",
        "normal_answer_source": "local_db",
        "source_id": source["id"],
        "database_path": str(db_path),
        "row_count": total_rows,
        "source_files": source_file_results,
        "current_biennium": current_biennium,
        "data_through": data_through,
        "data_through_label": (
            f"Payments through {month_label(data_through)}" if data_through else None
        ),
        "built_at": utc_now(),
        "message": "Built Washington Open Checkbook local database.",
    }


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS source_files;
        DROP TABLE IF EXISTS refresh_runs;

        CREATE TABLE source_files (
          file_id INTEGER PRIMARY KEY,
          source_surface_id TEXT NOT NULL,
          biennium TEXT NOT NULL,
          url TEXT NOT NULL,
          fetched_at TEXT NOT NULL,
          last_modified TEXT,
          content_length INTEGER NOT NULL,
          sha256 TEXT NOT NULL,
          row_count INTEGER NOT NULL,
          status TEXT NOT NULL
        );

        CREATE TABLE payments (
          payment_id INTEGER PRIMARY KEY,
          biennium TEXT NOT NULL,
          fiscal_year INTEGER NOT NULL,
          fiscal_month INTEGER NOT NULL,
          calendar_month TEXT NOT NULL,
          agency_code TEXT NOT NULL,
          agency_name TEXT NOT NULL,
          object_code TEXT NOT NULL,
          category TEXT NOT NULL,
          subobject_code TEXT NOT NULL,
          subcategory TEXT NOT NULL,
          vendor_name TEXT NOT NULL,
          amount REAL NOT NULL
        );

        CREATE TABLE refresh_runs (
          run_id TEXT PRIMARY KEY,
          started_at TEXT NOT NULL,
          finished_at TEXT NOT NULL,
          status TEXT NOT NULL,
          message TEXT NOT NULL
        );
        """
    )


def create_indexes(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE INDEX idx_payments_biennium ON payments (biennium);
        CREATE INDEX idx_payments_period ON payments (fiscal_year, fiscal_month);
        CREATE INDEX idx_payments_month ON payments (calendar_month);
        CREATE INDEX idx_payments_agency ON payments (agency_code, agency_name);
        CREATE INDEX idx_payments_category ON payments (category, subcategory);
        CREATE INDEX idx_payments_vendor ON payments (vendor_name);
        """
    )


def insert_payment(conn: sqlite3.Connection, row: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO payments (
          biennium, fiscal_year, fiscal_month, calendar_month, agency_code, agency_name,
          object_code, category, subobject_code, subcategory, vendor_name, amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["biennium"],
            row["fiscal_year"],
            row["fiscal_month"],
            row["calendar_month"],
            row["agency_code"],
            row["agency_name"],
            row["object_code"],
            row["category"],
            row["subobject_code"],
            row["subcategory"],
            row["vendor_name"],
            row["amount"],
        ),
    )


def parse_xlsx_rows(path: Path):
    with ZipFile(path) as zf:
        shared_strings = load_shared_strings(zf)
        sheet_path = first_sheet_path(zf)
        headers: list[str] | None = None
        with zf.open(sheet_path) as handle:
            for event, elem in ET.iterparse(handle, events=("end",)):
                if not elem.tag.endswith("}row"):
                    continue
                values = row_values(elem, shared_strings)
                elem.clear()
                if not values:
                    continue
                if headers is None:
                    headers = normalize_headers(values)
                    validate_headers(headers)
                    continue
                row = {
                    header: values[index] if index < len(values) else ""
                    for index, header in enumerate(headers)
                }
                if any(value != "" for value in row.values()):
                    yield row


def load_shared_strings(zf: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    shared = []
    for item in root.findall("a:si", NS):
        shared.append("".join((node.text or "") for node in item.iterfind(".//a:t", NS)))
    return shared


def first_sheet_path(zf: ZipFile) -> str:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    relmap = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    first_sheet = workbook.find("a:sheets/a:sheet", NS)
    if first_sheet is None:
        raise CheckbookExtractError("XLSX workbook has no sheets.")
    rel_id = first_sheet.attrib[REL_NS]
    target = relmap[rel_id]
    if target.startswith("/xl/"):
        return target.lstrip("/")
    if target.startswith("xl/"):
        return target
    return "xl/" + target.lstrip("/")


def row_values(elem: ET.Element, shared_strings: list[str]) -> list[str]:
    by_column: dict[int, str] = {}
    max_column = 0
    for cell in elem:
        if not cell.tag.endswith("}c"):
            continue
        ref = cell.attrib.get("r", "")
        column = column_index("".join(ch for ch in ref if ch.isalpha()))
        max_column = max(max_column, column)
        by_column[column] = cell_value(cell, shared_strings)
    return [by_column.get(index, "") for index in range(1, max_column + 1)]


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join((node.text or "") for node in cell.iterfind(".//a:t", NS))
    value_node = None
    for child in cell:
        if child.tag.endswith("}v"):
            value_node = child
            break
    if value_node is None or value_node.text is None:
        return ""
    if cell_type == "s":
        return shared_strings[int(value_node.text)]
    return value_node.text


def column_index(letters: str) -> int:
    index = 0
    for char in letters:
        index = index * 26 + ord(char.upper()) - ord("A") + 1
    return index


def normalize_headers(headers: list[str]) -> list[str]:
    return [HEADER_ALIASES.get(header.strip(), header.strip()) for header in headers]


def validate_headers(headers: list[str]) -> None:
    if headers[: len(REQUIRED_HEADERS)] != REQUIRED_HEADERS:
        raise CheckbookExtractError(
            f"Unexpected Open Checkbook headers: {headers}; expected {REQUIRED_HEADERS}"
        )


def normalize_payment_row(row: dict[str, str]) -> dict[str, Any]:
    fiscal_year = int(number_text(row["FY"]))
    fiscal_month = int(number_text(row["FMonth"]))
    return {
        "biennium": clean(row["Bien"]),
        "fiscal_year": fiscal_year,
        "fiscal_month": fiscal_month,
        "calendar_month": calendar_month_from_fiscal(fiscal_year, fiscal_month),
        "agency_code": clean(row["Agy"]),
        "agency_name": clean(row["Agency"]),
        "object_code": clean(row["Object"]),
        "category": clean(row["Category"]),
        "subobject_code": clean(row["Subobj"]),
        "subcategory": clean(row["SubCategory"]),
        "vendor_name": clean(row["Vendor"]),
        "amount": float(number_text(row["Amount"])),
    }


def clean(value: str) -> str:
    return " ".join(str(value).strip().split())


def number_text(value: str) -> str:
    text = str(value).strip().replace(",", "").replace("$", "")
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    return text


def calendar_month_from_fiscal(fiscal_year: int, fiscal_month: int) -> str:
    if fiscal_month < 1 or fiscal_month > 12:
        raise CheckbookExtractError(f"Invalid fiscal month: {fiscal_month}")
    calendar_month = ((fiscal_month + 6 - 1) % 12) + 1
    calendar_year = fiscal_year - 1 if fiscal_month <= 6 else fiscal_year
    return f"{calendar_year:04d}-{calendar_month:02d}"


def month_label(year_month: str) -> str:
    if not year_month:
        return ""
    year, month = year_month.split("-", 1)
    names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    return f"{names[int(month) - 1]} {year}"


def download_file(url: str, path: Path) -> None:
    request = Request(url)
    try:
        with urlopen(request, timeout=120) as response:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as handle:
                shutil.copyfileobj(response, handle, length=1024 * 1024)
    except (HTTPError, URLError) as exc:
        raise CheckbookExtractError(f"Failed to download {url}: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


if __name__ == "__main__":
    main()
