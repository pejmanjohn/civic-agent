#!/usr/bin/env python3
"""Extract the King County Open Budget Dashboard snapshot.

This script is intentionally source-specific. It replays reviewed Power BI
query payloads for this public report and normalizes the known response shapes.
It is not a generic Power BI adapter.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
JURISDICTION_ROOT = ROOT / "jurisdictions" / "king_county"
DATASET_ROOT = JURISDICTION_ROOT / "data" / "open-budget-dashboard"
SOURCE_CARD_PATH = JURISDICTION_ROOT / "sources" / "open-budget-dashboard.source.json"
QUERY_TEMPLATE_ROOT = DATASET_ROOT / "query_templates"
DEFAULT_FIXTURE_DIR = ROOT / "tests" / "fixtures" / "king_county"

QUERY_TEMPLATE_FILES = {
    "overview_by_year": "overview-by-year.query.json",
    "department_revenue_expenditure_by_year": "department-revenue-expenditure-by-year.query.json",
    "department_fte_by_year": "department-fte-by-year.query.json",
}

FIXTURE_RESPONSE_FILES = {
    "overview_by_year": "overview-by-year.response.json",
    "department_revenue_expenditure_by_year": "department-revenue-expenditure-by-year.response.json",
    "department_fte_by_year": "department-fte-by-year.response.json",
}


class ExtractionError(RuntimeError):
    """Raised when the Power BI response does not match this source slice."""


def main() -> None:
    args = parse_args()
    source = load_json(SOURCE_CARD_PATH)
    templates = {
        key: load_json(QUERY_TEMPLATE_ROOT / filename)
        for key, filename in QUERY_TEMPLATE_FILES.items()
    }

    if args.live:
        metadata = fetch_models_and_exploration(source)
        conceptual_schema = fetch_conceptual_schema(source)
        verify_metadata(source, metadata)
        responses = {key: post_querydata(source, template) for key, template in templates.items()}
        if args.raw_dir:
            write_raw_responses(args.raw_dir, responses)
    else:
        metadata = metadata_from_source_card(source)
        conceptual_schema = load_json(args.fixture_dir / "conceptualschema-sample.json")
        responses = {
            key: load_json(args.fixture_dir / filename)
            for key, filename in FIXTURE_RESPONSE_FILES.items()
        }

    output_dir = args.output_dir or DATASET_ROOT / str(source["snapshot_version"])
    write_snapshot(
        source=source,
        templates=templates,
        responses=responses,
        metadata=metadata,
        conceptual_schema=conceptual_schema,
        output_dir=output_dir,
        live=args.live,
    )
    print(f"Wrote King County snapshot to {output_dir.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live Power BI metadata and querydata responses.",
    )
    parser.add_argument(
        "--fixture-dir",
        type=Path,
        default=DEFAULT_FIXTURE_DIR,
        help="Fixture directory used when --live is not set.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Snapshot output directory. Defaults to the source-card snapshot version.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        help="Optional local directory for reviewed raw live responses.",
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


def sha256_json(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def fetch_models_and_exploration(source: dict[str, Any]) -> dict[str, Any]:
    return get_json(source["metadata_endpoint"], source)


def fetch_conceptual_schema(source: dict[str, Any]) -> dict[str, Any]:
    return get_json(source["conceptual_schema_endpoint"], source)


def get_json(url: str, source: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0",
            "X-PowerBI-ResourceKey": source["powerbi_resource_key"],
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            encoding = response.headers.get("Content-Encoding")
    except urllib.error.URLError as exc:
        raise ExtractionError(f"failed to fetch {url}: {exc}") from exc
    text = decode_response(raw, encoding)
    return json.loads(text)


def post_querydata(source: dict[str, Any], query_template: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps(query_template, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        source["querydata_endpoint"],
        data=payload,
        method="POST",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "ActivityId": "11111111-1111-4111-8111-111111111111",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://app.powerbigov.us",
            "Referer": "https://app.powerbigov.us/",
            "RequestId": "22222222-2222-4222-8222-222222222222",
            "User-Agent": "Mozilla/5.0",
            "X-PowerBI-ResourceKey": source["powerbi_resource_key"],
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            encoding = response.headers.get("Content-Encoding")
    except urllib.error.URLError as exc:
        raise ExtractionError(f"failed to post querydata: {exc}") from exc
    text = decode_response(raw, encoding)
    return json.loads(text)


def decode_response(raw: bytes, content_encoding: str | None) -> str:
    if content_encoding == "gzip" or raw.startswith(b"\x1f\x8b"):
        return gzip.decompress(raw).decode("utf-8")
    return raw.decode("utf-8")


def metadata_from_source_card(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "models": [
            {
                "id": source["model_id"],
                "displayName": source["dataset_display_name"],
                "dbName": source["dataset_id"],
                "LastRefreshTime": source["observed_model_refresh_time"],
                "directQueryMode": False,
                "sizeInMBs": 1,
            }
        ],
        "exploration": {
            "reportId": None,
            "id": None,
        },
    }


def verify_metadata(source: dict[str, Any], metadata: dict[str, Any]) -> None:
    try:
        model = metadata["models"][0]
    except (KeyError, IndexError) as exc:
        raise ExtractionError("metadata response does not include models[0]") from exc
    if model.get("id") != source["model_id"]:
        raise ExtractionError(
            f"model id mismatch: expected {source['model_id']}, got {model.get('id')}"
        )
    if model.get("dbName") != source["dataset_id"]:
        raise ExtractionError(
            f"dataset id mismatch: expected {source['dataset_id']}, got {model.get('dbName')}"
        )


def response_data(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return payload["results"][0]["result"]["data"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ExtractionError("querydata response is missing results[0].result.data") from exc


def primary_rows(payload: dict[str, Any], block_name: str) -> list[dict[str, Any]]:
    data = response_data(payload)
    try:
        ph = data["dsr"]["DS"][0]["PH"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ExtractionError("querydata response is missing dsr.DS[0].PH") from exc
    for block in ph:
        if block_name in block:
            rows = block[block_name]
            if isinstance(rows, list):
                return rows
    raise ExtractionError(f"querydata response does not include {block_name}")


def parse_c_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields: list[str] | None = None
    parsed: list[dict[str, Any]] = []
    for row in rows:
        if "S" in row:
            fields = [field["N"] for field in row["S"]]
        if "C" not in row:
            continue
        if fields is None:
            raise ExtractionError("compressed row encountered before schema row")
        values = row["C"]
        if (
            row.get("R") == 2
            and fields == ["G0", "M0", "M1"]
            and len(values) == 2
        ):
            # This report uses this shape for the FY2026 "Non KC" row:
            # department name, omitted zero revenue, expenditure value.
            values = [values[0], 0, values[1]]
        parsed.append(dict(zip(fields, values)))
    return parsed


def metric_row_count(payload: dict[str, Any]) -> int | None:
    events = response_data(payload).get("metrics", {}).get("Events", [])
    for event in events:
        metrics = event.get("Metrics", {})
        if "RowCount" in metrics:
            return int(metrics["RowCount"])
    return None


def template_year(query_template: dict[str, Any]) -> int | None:
    def walk(value: Any) -> int | None:
        if isinstance(value, dict):
            in_clause = value.get("In")
            if isinstance(in_clause, dict) and in_clause_targets_year(in_clause):
                for row in in_clause.get("Values", []):
                    for cell in row:
                        literal = cell.get("Literal") if isinstance(cell, dict) else None
                        if isinstance(literal, dict):
                            raw = literal.get("Value")
                            if (
                                isinstance(raw, str)
                                and raw.endswith("L")
                                and raw[:-1].isdigit()
                            ):
                                return int(raw[:-1])
            for child in value.values():
                found = walk(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = walk(child)
                if found is not None:
                    return found
        return None

    return walk(query_template)


def in_clause_targets_year(in_clause: dict[str, Any]) -> bool:
    for expression in in_clause.get("Expressions", []):
        column = expression.get("Column") if isinstance(expression, dict) else None
        if isinstance(column, dict) and column.get("Property") == "Year":
            return True
    return False


def visual_id(query_template: dict[str, Any]) -> str | None:
    try:
        sources = query_template["queries"][0]["ApplicationContext"]["Sources"]
    except (KeyError, IndexError, TypeError):
        return None
    if not sources:
        return None
    return sources[0].get("VisualId")


def normalize_overview_by_year(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = parse_c_rows(primary_rows(payload, "DM0"))
    normalized = []
    for row in rows:
        normalized.append(
            {
                "year": int(row["G0"]),
                "budgeted_revenue": int(row["M0"]),
                "budgeted_expenditure": int(row["M1"]),
                "budgeted_fte": int(row["M2"]),
            }
        )
    return normalized


def normalize_department_revenue_expenditure(
    payload: dict[str, Any], *, year: int
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    total_rows = parse_c_rows(primary_rows(payload, "DM0"))
    if len(total_rows) != 1:
        raise ExtractionError("department revenue/expenditure response should contain one total row")
    total = {
        "budgeted_revenue": int(total_rows[0]["A0"]),
        "budgeted_expenditure": int(total_rows[0]["A1"]),
    }
    rows = []
    for row in parse_c_rows(primary_rows(payload, "DM1")):
        rows.append(
            {
                "year": year,
                "department": row["G0"],
                "budgeted_revenue": int(row["M0"]),
                "budgeted_expenditure": int(row["M1"]),
            }
        )
    return rows, total


def normalize_department_fte(
    payload: dict[str, Any], *, year: int
) -> tuple[list[dict[str, Any]], int]:
    total_rows = primary_rows(payload, "DM0")
    if len(total_rows) != 1 or "A0" not in total_rows[0]:
        raise ExtractionError("FTE response should contain one A0 total row")
    total = int(total_rows[0]["A0"])
    rows = []
    for row in primary_rows(payload, "DM1"):
        department = row.get("G0")
        nested = row.get("M", [])
        fte = None
        if nested and "DM2" in nested[0] and nested[0]["DM2"]:
            fte = nested[0]["DM2"][0].get("A1")
        if department is None or fte is None:
            raise ExtractionError("FTE department row is missing G0 or nested A1")
        rows.append(
            {
                "year": year,
                "department": department,
                "budgeted_fte": int(fte),
            }
        )
    return rows, total


def conceptual_entities(conceptual_schema: dict[str, Any]) -> dict[str, list[str]]:
    schemas = conceptual_schema.get("schemas", [])
    if not schemas:
        raise ExtractionError("conceptual schema response is missing schemas")
    schema = schemas[0].get("schema", {})
    entities = schema.get("Entities", [])
    return {
        entity.get("Name"): [prop.get("Name") for prop in entity.get("Properties", [])]
        for entity in entities
        if entity.get("Name")
    }


def write_raw_responses(raw_dir: Path, responses: dict[str, dict[str, Any]]) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    for key, response in responses.items():
        write_json(raw_dir / f"{key}.response.json", response)


def write_snapshot(
    *,
    source: dict[str, Any],
    templates: dict[str, dict[str, Any]],
    responses: dict[str, dict[str, Any]],
    metadata: dict[str, Any],
    conceptual_schema: dict[str, Any],
    output_dir: Path,
    live: bool,
) -> None:
    verify_metadata(source, metadata)

    overview_rows = normalize_overview_by_year(responses["overview_by_year"])

    department_year = template_year(templates["department_revenue_expenditure_by_year"])
    if department_year is None:
        raise ExtractionError("department revenue/expenditure template is missing year filter")
    department_rows, department_total = normalize_department_revenue_expenditure(
        responses["department_revenue_expenditure_by_year"], year=department_year
    )

    fte_year = template_year(templates["department_fte_by_year"])
    fte_rows: list[dict[str, Any]] = []
    fte_total: int | None = None
    if fte_year is not None:
        fte_rows, fte_total = normalize_department_fte(
            responses["department_fte_by_year"], year=fte_year
        )

    normalized_dir = output_dir / "normalized"
    write_jsonl(normalized_dir / "overview-by-year.jsonl", overview_rows)
    write_jsonl(
        normalized_dir / "department-revenue-expenditure-by-year.jsonl", department_rows
    )
    if fte_rows:
        write_jsonl(normalized_dir / "department-fte-by-year.jsonl", fte_rows)

    years = [row["year"] for row in overview_rows]
    fy2026 = next((row for row in overview_rows if row["year"] == 2026), None)
    if fy2026 is None:
        raise ExtractionError("overview rows do not include 2026")

    summary = {
        "source_id": source["id"],
        "snapshot_version": source["snapshot_version"],
        "model_refresh_time": model_metadata(metadata).get("LastRefreshTime"),
        "known_years": years,
        "row_counts": {
            "overview_by_year": len(overview_rows),
            "department_revenue_expenditure_by_year": len(department_rows),
            "department_fte_by_year": len(fte_rows),
        },
        "validation_checks": {
            "fy2026_revenue_total": int(fy2026["budgeted_revenue"]),
            "fy2026_expenditure_total": int(fy2026["budgeted_expenditure"]),
            "fy2026_fte_total": int(fy2026["budgeted_fte"]),
            "fy2026_department_revenue_total": department_total["budgeted_revenue"],
            "fy2026_department_expenditure_total": department_total[
                "budgeted_expenditure"
            ],
            "fy2026_department_rows": len(department_rows),
            "fy2026_department_fte_total": fte_total,
            "fy2026_department_fte_rows": len(fte_rows),
        },
        "notes": [
            "Amounts are authorized or budgeted dashboard values, not actual spending or actual revenue earned.",
            "Future years in the dashboard are budget years, not completed actuals.",
        ],
    }
    write_json(output_dir / "summary.json", summary)

    provenance = {
        "source_id": source["id"],
        "generated_by": "jurisdictions/king_county/scripts/extract_open_budget.py",
        "generated_from_live_powerbi": live,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "official_dashboard_page": source["official_dashboard_page"],
        "powerbi_report_url": source["powerbi_report_url"],
        "api_host": source["powerbi_api_host"],
        "model_metadata": model_metadata(metadata),
        "source_card_expected_model": {
            "model_id": source["model_id"],
            "dataset_id": source["dataset_id"],
            "observed_model_refresh_time": source["observed_model_refresh_time"],
        },
        "conceptual_entities": conceptual_entities(conceptual_schema),
        "raw_response_policy": {
            "committed_raw_live_responses": False,
            "committed_sanitized_fixtures": True,
            "local_raw_capture_path": "jurisdictions/king_county/data/open-budget-dashboard/local_raw/",
            "reproduction": (
                "python3 jurisdictions/king_county/scripts/extract_open_budget.py "
                "--live --raw-dir jurisdictions/king_county/data/open-budget-dashboard/local_raw"
            ),
        },
        "query_templates": query_template_provenance(templates, responses),
        "response_metrics": {
            key: {"row_count": metric_row_count(response)}
            for key, response in responses.items()
        },
    }
    write_json(output_dir / "provenance.json", provenance)


def model_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    model = metadata["models"][0]
    exploration = metadata.get("exploration", {})
    return {
        "model_id": model.get("id"),
        "display_name": model.get("displayName"),
        "dataset_id": model.get("dbName"),
        "LastRefreshTime": model.get("LastRefreshTime"),
        "direct_query_mode": model.get("directQueryMode"),
        "size_in_mbs": model.get("sizeInMBs"),
        "exploration_id": exploration.get("id"),
        "report_id": exploration.get("reportId"),
    }


def query_template_provenance(
    templates: dict[str, dict[str, Any]], responses: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    details = {}
    for key, template in templates.items():
        details[key] = {
            "template_path": str(
                (
                    QUERY_TEMPLATE_ROOT / QUERY_TEMPLATE_FILES[key]
                ).relative_to(ROOT)
            ),
            "template_sha256": sha256_json(template),
            "response_sha256": sha256_json(responses[key]),
            "visual_id": visual_id(template),
            "year_filter": template_year(template),
        }
    return details


if __name__ == "__main__":
    main()
