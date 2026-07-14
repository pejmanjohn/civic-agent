#!/usr/bin/env python3
"""Extract the Washington Fiscal WA revenue by biennium snapshot.

This script is intentionally source-specific. It drives the official Fiscal WA
ReportViewer page for the accepted revenue report, exports XML/XLSX for each
reviewed biennium, and normalizes the known response shape. It is not a generic
SSRS adapter.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import http.cookiejar
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
JURISDICTION_ROOT = ROOT / "jurisdictions" / "washington"
DATASET_ROOT = JURISDICTION_ROOT / "data" / "revenue-by-biennium"
SOURCE_CARD_PATH = JURISDICTION_ROOT / "sources" / "revenue-by-biennium.source.json"
SURFACE_ID = "statewide_revenue_reportviewer"
REPORT_PAGE = "https://fiscal.wa.gov/Revenue/RevenueGeneral.aspx"
BIENNIUM_FIELD = "ReportViewer1$ctl08$ctl03$ddValue"
FUND_FIELD = "ReportViewer1$ctl08$ctl05$ddValue"
# Last-observed dropdown value for General Fund (001). The ReportViewer fund
# list grows over time and values SHIFT (2026-07-14: 192 -> 194 when the list
# reached 539 options; 192 became Gambling Revolving Account). The value is
# resolved by LABEL at run time; this constant is only the recorded default.
GENERAL_FUND_VALUE = "194"
GENERAL_FUND_LABEL = "General Fund (001)"
GENERAL_FUND_CODE = "001"


class ExtractionError(RuntimeError):
    """Raised when the ReportViewer response does not match this source slice."""


@dataclass(frozen=True)
class SelectOption:
    value: str
    text: str
    selected: bool


@dataclass(frozen=True)
class SelectField:
    name: str
    options: list[SelectOption]


@dataclass(frozen=True)
class ReportSession:
    final_url: str
    html_text: str
    form_fields: dict[str, str]
    select_fields: list[SelectField]


@dataclass(frozen=True)
class BienniumExport:
    biennium: str
    biennium_value: str
    html_text: str
    xml_bytes: bytes
    xlsx_bytes: bytes
    csv_bytes: bytes
    export_urls: dict[str, str]


class FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.inputs: list[dict[str, str]] = []
        self.select_fields: list[SelectField] = []
        self._current_select_name: str | None = None
        self._current_options: list[SelectOption] = []
        self._current_option_value: str | None = None
        self._current_option_selected = False
        self._current_option_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        if tag == "input":
            self.inputs.append(attrs_dict)
        elif tag == "select":
            self._current_select_name = attrs_dict.get("name")
            self._current_options = []
        elif tag == "option" and self._current_select_name is not None:
            self._current_option_value = attrs_dict.get("value", "")
            self._current_option_selected = "selected" in attrs_dict
            self._current_option_text = []

    def handle_data(self, data: str) -> None:
        if self._current_option_value is not None:
            self._current_option_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "option" and self._current_option_value is not None:
            self._current_options.append(
                SelectOption(
                    value=self._current_option_value,
                    text=normalize_space(html.unescape("".join(self._current_option_text))),
                    selected=self._current_option_selected,
                )
            )
            self._current_option_value = None
            self._current_option_selected = False
            self._current_option_text = []
        elif tag == "select" and self._current_select_name is not None:
            self.select_fields.append(
                SelectField(name=self._current_select_name, options=self._current_options)
            )
            self._current_select_name = None
            self._current_options = []


def main() -> None:
    args = parse_args()
    source = load_json(SOURCE_CARD_PATH)
    if not args.live:
        raise ExtractionError("Washington revenue extraction currently requires --live")

    fetched_at = datetime.now(timezone.utc).isoformat()
    exports = fetch_biennium_exports(source)
    if args.raw_dir:
        write_raw_exports(args.raw_dir, exports)

    output_dir = args.output_dir or DATASET_ROOT / str(source["snapshot_version"])
    write_snapshot(source=source, exports=exports, output_dir=output_dir, fetched_at=fetched_at)
    try:
        location = output_dir.relative_to(ROOT)
    except ValueError:
        location = output_dir
    print(f"Wrote Washington revenue snapshot to {location}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live Fiscal WA ReportViewer exports.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Snapshot output directory. Defaults to the source-card snapshot version.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        help="Optional local directory for raw XML/XLSX/CSV exports.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def resolve_general_fund_value(select_fields: list[SelectField]) -> str:
    """Resolve the General Fund (001) dropdown value by LABEL. The fund list
    grows and positional values shift between site updates; hardcoding the
    value selects the wrong fund silently."""
    import html as html_module

    for field in select_fields:
        if field.name != FUND_FIELD:
            continue
        matches = [
            option.value
            for option in field.options
            if html_module.unescape(option.text).strip() == GENERAL_FUND_LABEL
        ]
        if len(matches) == 1:
            RESOLVED_FUND.update(value=matches[0])
            return matches[0]
        raise ExtractionError(
            f"could not resolve {GENERAL_FUND_LABEL!r} uniquely in fund dropdown "
            f"({len(field.options)} options, {len(matches)} label matches)"
        )
    raise ExtractionError(f"fund dropdown {FUND_FIELD!r} not found on report page")


RESOLVED_FUND: dict[str, str] = {"value": GENERAL_FUND_VALUE}


def fetch_biennium_exports(source: dict[str, Any]) -> list[BienniumExport]:
    first_session = open_report_session()
    fund_value = resolve_general_fund_value(first_session.select_fields)
    biennium_options = biennium_select_options(first_session.select_fields)
    expected = source["source_surfaces"][SURFACE_ID]["coverage"]["biennia"]
    observed = sorted((option.text.split()[0] for option in biennium_options), key=biennium_sort_key)
    if observed != expected:
        raise ExtractionError(f"unexpected biennium options: {observed}")

    exports = []
    for option in sorted(biennium_options, key=lambda opt: biennium_sort_key(opt.text.split()[0])):
        biennium = option.text.split()[0]
        exports.append(fetch_biennium_export(biennium, option.value, fund_value))
    return exports


def open_report_session() -> ReportSession:
    opener = make_opener()
    final_url, _, _, body = open_with(opener, urllib.request.Request(REPORT_PAGE, headers=request_headers()))
    html_text = body.decode("utf-8", errors="replace")
    form_fields, select_fields = parse_report_form(html_text)
    return ReportSession(
        final_url=final_url,
        html_text=html_text,
        form_fields=form_fields,
        select_fields=select_fields,
    )


def fetch_biennium_export(biennium: str, biennium_value: str, fund_value: str = GENERAL_FUND_VALUE) -> BienniumExport:
    opener = make_opener()
    final_url, _, _, body = open_with(opener, urllib.request.Request(REPORT_PAGE, headers=request_headers()))
    html_text = body.decode("utf-8", errors="replace")
    form_fields, _ = parse_report_form(html_text)
    form_fields[BIENNIUM_FIELD] = biennium_value
    form_fields[FUND_FIELD] = fund_value
    form_fields["__EVENTTARGET"] = BIENNIUM_FIELD
    form_fields["__EVENTARGUMENT"] = ""
    post_body = urllib.parse.urlencode(form_fields).encode("utf-8")
    post_request = urllib.request.Request(
        final_url,
        data=post_body,
        headers={
            **request_headers(),
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    posted_url, _, _, posted_body = open_with(opener, post_request)
    posted_html = posted_body.decode("utf-8", errors="replace")
    export_base = report_export_base(posted_html)
    xml_url = urllib.parse.urljoin(posted_url, export_base + "XML")
    xlsx_url = urllib.parse.urljoin(posted_url, export_base + "EXCELOPENXML")
    csv_url = urllib.parse.urljoin(posted_url, export_base + "CSV")
    _, _, _, xml_bytes = open_with(opener, urllib.request.Request(xml_url, headers=request_headers()))
    _, _, _, xlsx_bytes = open_with(opener, urllib.request.Request(xlsx_url, headers=request_headers()))
    _, _, _, csv_bytes = open_with(opener, urllib.request.Request(csv_url, headers=request_headers()))
    return BienniumExport(
        biennium=biennium,
        biennium_value=biennium_value,
        html_text=posted_html,
        xml_bytes=xml_bytes,
        xlsx_bytes=xlsx_bytes,
        csv_bytes=csv_bytes,
        export_urls={"XML": xml_url, "EXCELOPENXML": xlsx_url, "CSV": csv_url},
    )


def make_opener() -> urllib.request.OpenerDirector:
    cookie_jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def request_headers() -> dict[str, str]:
    return {"User-Agent": "Mozilla/5.0"}


def open_with(
    opener: urllib.request.OpenerDirector,
    request: urllib.request.Request,
) -> tuple[str, int, Any, bytes]:
    try:
        with opener.open(request, timeout=90) as response:
            return response.geturl(), response.status, response.headers, response.read()
    except urllib.error.URLError as exc:
        raise ExtractionError(f"failed to fetch {request.full_url}: {exc}") from exc


def parse_report_form(html_text: str) -> tuple[dict[str, str], list[SelectField]]:
    parser = FormParser()
    parser.feed(html_text)
    fields: dict[str, str] = {}
    for input_attrs in parser.inputs:
        name = input_attrs.get("name")
        if name:
            fields[name] = input_attrs.get("value", "")
    for select in parser.select_fields:
        selected = next((option for option in select.options if option.selected), None)
        if selected is None and select.options:
            selected = select.options[0]
        if selected is not None:
            fields[select.name] = selected.value
    return fields, parser.select_fields


def biennium_select_options(select_fields: list[SelectField]) -> list[SelectOption]:
    for select in select_fields:
        if select.name == BIENNIUM_FIELD:
            return [option for option in select.options if "Biennium" in option.text]
    raise ExtractionError("could not find biennium parameter select")


def report_export_base(html_text: str) -> str:
    match = re.search(r'"ExportUrlBase":"([^"]+)"', html_text)
    if match is None:
        raise ExtractionError("could not find ReportViewer ExportUrlBase")
    return html.unescape(match.group(1)).replace("\\u0026", "&")


def write_snapshot(
    *,
    source: dict[str, Any],
    exports: list[BienniumExport],
    output_dir: Path,
    fetched_at: str,
) -> None:
    statewide_rows: list[dict[str, Any]] = []
    detail_rows: list[dict[str, Any]] = []
    export_metadata: dict[str, Any] = {}

    for export in exports:
        workbook_metadata = parse_workbook_metadata(export.xlsx_bytes)
        report = parse_revenue_xml(export.xml_bytes)
        actual_data = actual_data_metadata(workbook_metadata, source)
        actual_status = actual_data_status(export.biennium, actual_data["actual_data_through"])
        statewide_row = statewide_revenue_row(export, report, workbook_metadata, actual_data, actual_status)
        statewide_rows.append(statewide_row)
        detail_rows.extend(
            detail_revenue_rows(export, report, workbook_metadata, actual_data, actual_status)
        )
        export_metadata[export.biennium] = {
            "biennium_value": export.biennium_value,
            "report_period_label": workbook_metadata["report_period_label"],
            "fund": workbook_metadata["fund"],
            "actual_data_through": actual_data["actual_data_through"],
            "actual_data_through_label": actual_data["actual_data_through_label"],
            "actual_data_status": actual_status,
            "xml_sha256": sha256_bytes(export.xml_bytes),
            "xlsx_sha256": sha256_bytes(export.xlsx_bytes),
            "csv_sha256": sha256_bytes(export.csv_bytes),
            "csv_row_count": csv_row_count(export.csv_bytes),
        }

    statewide_rows = sorted(statewide_rows, key=lambda row: biennium_sort_key(row["biennium"]))
    detail_rows = sorted(
        detail_rows,
        key=lambda row: (
            biennium_sort_key(row["biennium"]),
            row["revenue_area"],
            row["account_or_agency"],
        ),
    )
    summary = build_summary(source, statewide_rows, detail_rows, export_metadata, fetched_at)
    provenance = build_provenance(
        source,
        export_metadata,
        fetched_at,
        row_counts=summary["row_counts"],
    )

    normalized_dir = output_dir / "normalized"
    write_jsonl(normalized_dir / "general-fund-revenue-by-biennium.jsonl", statewide_rows)
    write_jsonl(normalized_dir / "general-fund-revenue-by-area-account.jsonl", detail_rows)
    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "provenance.json", provenance)


def parse_workbook_metadata(xlsx_bytes: bytes) -> dict[str, str]:
    rows = parse_xlsx_rows(xlsx_bytes, max_rows=12)
    non_empty = [first_non_empty_cell(row) for row in rows]
    labels = [label for label in non_empty if label]
    period = next((label for label in labels if "Biennium" in label), None)
    actual_label = next((label for label in labels if label.startswith("Actual Data Through")), None)
    fund = next((label for label in labels if label.endswith("(001)")), None)
    if period is None or fund is None:
        raise ExtractionError(f"could not parse workbook metadata: {labels}")
    return {
        "report_period_label": period,
        "actual_data_through_label": actual_label or "",
        "fund": fund,
    }


def parse_xlsx_rows(xlsx_bytes: bytes, max_rows: int) -> list[list[str]]:
    namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes)) as archive:
        shared_strings = read_shared_strings(archive, namespace)
        sheet_name = next(
            name
            for name in archive.namelist()
            if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")
        )
        root = ET.fromstring(archive.read(sheet_name))
    rows: list[list[str]] = []
    for row in root.findall(".//a:sheetData/a:row", namespace)[:max_rows]:
        cells: dict[int, str] = {}
        for cell in row.findall("a:c", namespace):
            ref = cell.get("r", "A1")
            cells[column_number(ref)] = xlsx_cell_text(cell, shared_strings, namespace)
        max_column = max(cells, default=0)
        rows.append([cells.get(index, "") for index in range(1, max_column + 1)])
    return rows


def read_shared_strings(
    archive: zipfile.ZipFile,
    namespace: dict[str, str],
) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    strings = []
    for item in root.findall("a:si", namespace):
        strings.append("".join(text.text or "" for text in item.findall(".//a:t", namespace)))
    return strings


def xlsx_cell_text(
    cell: ET.Element,
    shared_strings: list[str],
    namespace: dict[str, str],
) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//a:is//a:t", namespace))
    value = cell.find("a:v", namespace)
    text = "" if value is None else value.text or ""
    if cell_type == "s" and text.isdigit():
        return shared_strings[int(text)]
    return text


def column_number(cell_ref: str) -> int:
    number = 0
    for character in "".join(ch for ch in cell_ref if ch.isalpha()).upper():
        number = number * 26 + ord(character) - 64
    return number


def first_non_empty_cell(row: list[str]) -> str:
    for cell in row:
        normalized = normalize_space(cell)
        if normalized:
            return normalized
    return ""


def actual_data_metadata(workbook_metadata: dict[str, str], source: dict[str, Any]) -> dict[str, str]:
    label = workbook_metadata["actual_data_through_label"] or source["actual_data_through_label"]
    match = re.search(r"Actual Data Through ([A-Za-z]+) (\d{4})", label)
    if match is None:
        raise ExtractionError(f"could not parse actual data through label: {label}")
    month_name, year = match.groups()
    month_number = datetime.strptime(month_name, "%B").month
    return {
        "actual_data_through": f"{year}-{month_number:02d}",
        "actual_data_through_label": label,
        "actual_data_through_precision": "month",
    }


def actual_data_status(biennium: str, actual_data_through: str) -> str:
    _, end_year_suffix = biennium.split("-")
    end_year = 2000 + int(end_year_suffix)
    end_period = f"{end_year}-06"
    return "complete" if actual_data_through >= end_period else "partial"


def parse_revenue_xml(xml_bytes: bytes) -> dict[str, Any]:
    root = ET.fromstring(xml_bytes.decode("utf-8-sig", errors="replace"))
    table = first_element(root, "table1")
    totals = {
        "estimated_revenue_thousands": decimal_attr(table, "textbox32"),
        "actual_revenue_thousands": decimal_attr(table, "textbox33"),
        "actual_minus_estimate_thousands": decimal_attr(table, "textbox34"),
    }
    groups = []
    for group_element in elements_by_local_name(root, "table1_Group1"):
        group = {
            "revenue_area": normalize_space(group_element.attrib.get("textbox13", "")),
            "estimated_revenue_thousands": decimal_attr(group_element, "textbox26"),
            "actual_revenue_thousands": decimal_attr(group_element, "textbox27"),
            "actual_minus_estimate_thousands": decimal_attr(group_element, "textbox28"),
            "details": [],
        }
        for detail_element in elements_by_local_name(group_element, "Detail"):
            account = normalize_space(detail_element.attrib.get("AgencyTitle", ""))
            if not account:
                continue
            group["details"].append(
                {
                    "account_or_agency": account,
                    "estimated_revenue_thousands": decimal_attr(detail_element, "Amount1"),
                    "actual_revenue_thousands": decimal_attr(detail_element, "Amount2"),
                    "actual_minus_estimate_thousands": decimal_attr(detail_element, "Amount3"),
                }
            )
        if group["details"]:
            groups.append(group)
    if not groups:
        raise ExtractionError("RevenueSW XML did not contain detail rows")
    return {"totals": totals, "groups": groups}


def first_element(root: ET.Element, local_name: str) -> ET.Element:
    for element in root.iter():
        if strip_namespace(element.tag) == local_name:
            return element
    raise ExtractionError(f"could not find XML element {local_name}")


def elements_by_local_name(root: ET.Element, local_name: str) -> list[ET.Element]:
    return [element for element in root.iter() if strip_namespace(element.tag) == local_name]


def strip_namespace(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def decimal_attr(element: ET.Element, attr: str) -> Decimal:
    return Decimal(element.attrib[attr])


def statewide_revenue_row(
    export: BienniumExport,
    report: dict[str, Any],
    workbook_metadata: dict[str, str],
    actual_data: dict[str, str],
    actual_status: str,
) -> dict[str, Any]:
    return base_row(export, workbook_metadata, actual_data, actual_status) | amount_fields(
        report["totals"]
    )


def detail_revenue_rows(
    export: BienniumExport,
    report: dict[str, Any],
    workbook_metadata: dict[str, str],
    actual_data: dict[str, str],
    actual_status: str,
) -> list[dict[str, Any]]:
    rows = []
    for group in report["groups"]:
        for detail in group["details"]:
            rows.append(
                base_row(export, workbook_metadata, actual_data, actual_status)
                | {
                    "revenue_area": group["revenue_area"],
                    "account_or_agency": detail["account_or_agency"],
                }
                | amount_fields(detail)
                | {
                    "revenue_area_estimated_revenue": dollars_from_thousands(
                        group["estimated_revenue_thousands"]
                    ),
                    "revenue_area_actual_revenue": dollars_from_thousands(
                        group["actual_revenue_thousands"]
                    ),
                    "revenue_area_actual_minus_estimate": dollars_from_thousands(
                        group["actual_minus_estimate_thousands"]
                    ),
                }
            )
    return rows


def base_row(
    export: BienniumExport,
    workbook_metadata: dict[str, str],
    actual_data: dict[str, str],
    actual_status: str,
) -> dict[str, Any]:
    return {
        "source_surface_id": SURFACE_ID,
        "biennium": export.biennium,
        "period_type": "biennium",
        "fund": workbook_metadata["fund"],
        "fund_code": GENERAL_FUND_CODE,
        "actual_data_through": actual_data["actual_data_through"],
        "actual_data_through_label": actual_data["actual_data_through_label"],
        "actual_data_through_precision": actual_data["actual_data_through_precision"],
        "actual_data_status": actual_status,
    }


def amount_fields(values: dict[str, Decimal]) -> dict[str, Any]:
    estimated = values["estimated_revenue_thousands"]
    actual = values["actual_revenue_thousands"]
    difference = values["actual_minus_estimate_thousands"]
    return {
        "estimated_revenue_thousands": json_number(estimated),
        "actual_revenue_thousands": json_number(actual),
        "actual_minus_estimate_thousands": json_number(difference),
        "estimated_revenue": dollars_from_thousands(estimated),
        "actual_revenue": dollars_from_thousands(actual),
        "actual_minus_estimate": dollars_from_thousands(difference),
    }


def dollars_from_thousands(value: Decimal) -> int | float:
    dollars = (value * Decimal("1000")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return json_number(dollars)


def json_number(value: Decimal) -> int | float:
    if value == value.to_integral_value():
        return int(value)
    return float(value)


def current_actual_boundary(source: dict[str, Any], export_metadata: dict[str, Any]) -> dict[str, str]:
    """The authoritative data boundary is the CURRENT biennium's export label.
    Closed biennia keep stale banners (observed 2026-07: closed exports still
    said April while the in-progress 2025-27 export said May); taking the
    card's asserted value or the first export's label masks new months."""
    current = export_metadata.get(source["current_biennium"])
    if current is None:
        raise ExtractionError(
            f"current biennium {source['current_biennium']!r} missing from exports"
        )
    return current


def build_summary(
    source: dict[str, Any],
    statewide_rows: list[dict[str, Any]],
    detail_rows: list[dict[str, Any]],
    export_metadata: dict[str, Any],
    fetched_at: str,
) -> dict[str, Any]:
    totals = {row["biennium"]: amount_summary(row) for row in statewide_rows}
    detail_totals = detail_totals_by_biennium(detail_rows)
    detail_totals_match = detail_totals_match_statewide(totals, detail_totals)
    current = next(row for row in statewide_rows if row["biennium"] == source["current_biennium"])
    row_counts = {
        "general_fund_revenue_by_biennium": len(statewide_rows),
        "general_fund_revenue_by_area_account": len(detail_rows),
    }
    validation_checks = {
        "historical_biennia": [row["biennium"] for row in statewide_rows],
        "totals_by_biennium": totals,
        "detail_totals_by_biennium": detail_totals,
        "detail_totals_match_statewide_totals": detail_totals_match,
        "current_biennium": source["current_biennium"],
        "current_biennium_estimated_revenue": current["estimated_revenue"],
        "current_biennium_actual_revenue": current["actual_revenue"],
        "current_biennium_actual_minus_estimate": current["actual_minus_estimate"],
        "current_biennium_actual_data_status": current["actual_data_status"],
    }
    return {
        "source_id": source["id"],
        "snapshot_version": source["snapshot_version"],
        "snapshot_fetched_at": fetched_at,
        "official_report_page": source["official_report_page"],
        "fund": GENERAL_FUND_LABEL,
        "fund_code": GENERAL_FUND_CODE,
        "actual_data_through": current_actual_boundary(source, export_metadata)["actual_data_through"],
        "actual_data_through_label": current_actual_boundary(source, export_metadata)["actual_data_through_label"],
        "actual_data_through_precision": source["actual_data_through_precision"],
        "row_counts": row_counts,
        "historical_coverage": {
            "start_biennium": statewide_rows[0]["biennium"],
            "end_biennium": statewide_rows[-1]["biennium"],
            "biennia": [row["biennium"] for row in statewide_rows],
        },
        "actual_data_status_by_biennium": {
            row["biennium"]: row["actual_data_status"] for row in statewide_rows
        },
        "validation_checks": validation_checks,
        "source_fingerprint": source_fingerprint(
            source,
            row_counts=row_counts,
            checks=validation_checks,
            integrity=export_integrity(export_metadata),
        ),
        "exports": export_metadata,
        "caveats": source["caveats"],
    }


def amount_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "estimated_revenue": row["estimated_revenue"],
        "actual_revenue": row["actual_revenue"],
        "actual_minus_estimate": row["actual_minus_estimate"],
    }


def detail_totals_by_biennium(detail_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    totals: dict[str, dict[str, Decimal]] = {}
    for row in detail_rows:
        bucket = totals.setdefault(
            row["biennium"],
            {
                "estimated_revenue": Decimal("0"),
                "actual_revenue": Decimal("0"),
                "actual_minus_estimate": Decimal("0"),
            },
        )
        for key in bucket:
            bucket[key] += Decimal(str(row[key]))
    return {
        biennium: {key: json_number(value) for key, value in values.items()}
        for biennium, values in sorted(totals.items(), key=lambda item: biennium_sort_key(item[0]))
    }


def detail_totals_match_statewide(
    statewide_totals: dict[str, dict[str, Any]],
    detail_totals: dict[str, dict[str, Any]],
) -> bool:
    for biennium, statewide in statewide_totals.items():
        detail = detail_totals.get(biennium)
        if detail is None:
            return False
        for key, statewide_value in statewide.items():
            if abs(Decimal(str(statewide_value)) - Decimal(str(detail[key]))) > Decimal("1"):
                return False
    return True


def build_provenance(
    source: dict[str, Any],
    export_metadata: dict[str, Any],
    fetched_at: str,
    *,
    row_counts: dict[str, Any],
) -> dict[str, Any]:
    return {
        "source_id": source["id"],
        "dataset_name": source["dataset_name"],
        "provider": source["provider"],
        "access_method": source["access_method"],
        "snapshot_version": source["snapshot_version"],
        "snapshot_fetched_at": fetched_at,
        "actual_data_through": current_actual_boundary(source, export_metadata)["actual_data_through"],
        "actual_data_through_label": current_actual_boundary(source, export_metadata)["actual_data_through_label"],
        "actual_data_through_precision": source["actual_data_through_precision"],
        "source_surfaces": source["source_surfaces"],
        "report_parameters": {
            "biennium_field": BIENNIUM_FIELD,
            "fund_field": FUND_FIELD,
            "fund_value": RESOLVED_FUND["value"],
            "fund": GENERAL_FUND_LABEL,
        },
        "exports": export_metadata,
        "source_fingerprint": source_fingerprint(
            source,
            row_counts=row_counts,
            checks={
                "actual_data_through": source["actual_data_through"],
                "actual_data_through_label": source["actual_data_through_label"],
                "exports": list(export_metadata),
            },
            integrity=export_integrity(export_metadata),
        ),
        "normalization": {
            "source_units": source["amount_units_from_report"],
            "normalized_units": "dollars",
            "difference_semantics": "actual_minus_estimate",
            "actual_data_status": "complete when actual_data_through is on or after the biennium end month; otherwise partial",
        },
        "caveats": source["caveats"],
    }


def source_fingerprint(
    source: dict[str, Any],
    *,
    row_counts: dict[str, Any],
    checks: dict[str, Any],
    integrity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    fingerprint = dict(source.get("source_fingerprint", {}))
    fingerprint["row_counts"] = row_counts
    fingerprint["checks"] = checks
    if integrity:
        fingerprint["integrity"] = integrity
    return fingerprint


def export_integrity(export_metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "exports": {
            biennium: {
                "csv_row_count": metadata["csv_row_count"],
                "csv_sha256": metadata["csv_sha256"],
                "xlsx_sha256": metadata["xlsx_sha256"],
                "xml_sha256": metadata["xml_sha256"],
            }
            for biennium, metadata in export_metadata.items()
        }
    }


def write_raw_exports(raw_dir: Path, exports: list[BienniumExport]) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    for export in exports:
        stem = export.biennium
        (raw_dir / f"{stem}.xml").write_bytes(export.xml_bytes)
        (raw_dir / f"{stem}.xlsx").write_bytes(export.xlsx_bytes)
        (raw_dir / f"{stem}.csv").write_bytes(export.csv_bytes)


def csv_row_count(csv_bytes: bytes) -> int:
    text = csv_bytes.decode("utf-8-sig", errors="replace")
    return max(0, sum(1 for _ in csv.reader(io.StringIO(text))) - 1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_space(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def biennium_sort_key(biennium: str) -> int:
    return int(biennium.split("-", 1)[0])


if __name__ == "__main__":
    try:
        main()
    except ExtractionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
