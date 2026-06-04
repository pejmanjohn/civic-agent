#!/usr/bin/env python3
"""Extract the Washington Fiscal WA operating budget snapshot.

This script is intentionally source-specific. It replays reviewed Power BI
query payloads for accepted Fiscal WA operating budget summary reports and
normalizes the known response shapes. It is not a generic Power BI adapter.
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
JURISDICTION_ROOT = ROOT / "jurisdictions" / "washington"
DATASET_ROOT = JURISDICTION_ROOT / "data" / "operating-budget"
SOURCE_CARD_PATH = JURISDICTION_ROOT / "sources" / "operating-budget.source.json"
QUERY_TEMPLATE_ROOT = DATASET_ROOT / "query_templates"
CURRENT_SURFACE_ID = "current_biennial_summary_powerbi"
PRIOR_SURFACE_ID = "prior_summary_powerbi"

QUERY_TEMPLATE_FILES = {
    "version_summary": "version-summary.query.json",
    "agency_by_fund_view": "agency-by-fund-view.query.json",
    "functional_area_by_fund_view": "functional-area-by-fund-view.query.json",
    "historical_biennium_summary": "historical-biennium-summary.query.json",
    "historical_agency_by_biennium": "historical-agency-by-biennium.query.json",
    "historical_functional_area_by_biennium": "historical-functional-area-by-biennium.query.json",
}

QUERY_TEMPLATE_SURFACES = {
    "version_summary": CURRENT_SURFACE_ID,
    "agency_by_fund_view": CURRENT_SURFACE_ID,
    "functional_area_by_fund_view": CURRENT_SURFACE_ID,
    "historical_biennium_summary": PRIOR_SURFACE_ID,
    "historical_agency_by_biennium": PRIOR_SURFACE_ID,
    "historical_functional_area_by_biennium": PRIOR_SURFACE_ID,
}


class ExtractionError(RuntimeError):
    """Raised when the Power BI response does not match this source slice."""


def main() -> None:
    args = parse_args()
    source = load_json(SOURCE_CARD_PATH)
    templates = build_query_templates(source)

    if args.write_query_templates:
        for key, template in templates.items():
            write_json(QUERY_TEMPLATE_ROOT / QUERY_TEMPLATE_FILES[key], template)

    if args.live:
        surfaces = live_powerbi_surfaces(source)
        metadata = {
            surface_id: fetch_models_and_exploration(surface)
            for surface_id, surface in surfaces.items()
        }
        conceptual_schema = {
            surface_id: fetch_conceptual_schema(surface)
            for surface_id, surface in surfaces.items()
        }
        for surface_id, surface_metadata in metadata.items():
            verify_metadata(surfaces[surface_id], surface_metadata)
        responses = {
            key: post_querydata(surfaces[QUERY_TEMPLATE_SURFACES[key]], template)
            for key, template in templates.items()
        }
        if args.raw_dir:
            write_raw_responses(args.raw_dir, responses)
    else:
        raise ExtractionError("Washington extraction currently requires --live")

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
    print(f"Wrote Washington snapshot to {output_dir.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live Power BI metadata and querydata responses.",
    )
    parser.add_argument(
        "--write-query-templates",
        action="store_true",
        help="Write generated reviewed query templates before extraction.",
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


def column_expression(source: str, property_name: str) -> dict[str, Any]:
    return {
        "Column": {
            "Expression": {"SourceRef": {"Source": source}},
            "Property": property_name,
        }
    }


def select_column(source: str, property_name: str, name: str) -> dict[str, Any]:
    expression = column_expression(source, property_name)
    expression["Name"] = name
    return expression


def select_sum(source: str, property_name: str, name: str) -> dict[str, Any]:
    return {
        "Aggregation": sum_expression(source, property_name)["Aggregation"],
        "Name": name,
    }


def select_min(source: str, property_name: str, name: str) -> dict[str, Any]:
    return {
        "Aggregation": {
            "Expression": column_expression(source, property_name),
            "Function": 4,
        },
        "Name": name,
    }


def sum_expression(source: str, property_name: str) -> dict[str, Any]:
    return {
        "Aggregation": {
            "Expression": column_expression(source, property_name),
            "Function": 0,
        }
    }


def in_filter(source: str, property_name: str, values: list[str]) -> dict[str, Any]:
    return {
        "Condition": {
            "In": {
                "Expressions": [column_expression(source, property_name)],
                "Values": [[{"Literal": {"Value": powerbi_literal(value)}}] for value in values],
            }
        }
    }


def not_null_filter(source: str, property_name: str) -> dict[str, Any]:
    return {
        "Condition": {
            "Not": {
                "Expression": {
                    "In": {
                        "Expressions": [column_expression(source, property_name)],
                        "Values": [[{"Literal": {"Value": "null"}}]],
                    }
                }
            }
        }
    }


def powerbi_literal(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def order_by(expression: dict[str, Any], direction: int = 1) -> dict[str, Any]:
    return {"Direction": direction, "Expression": expression}


def source_surface(source: dict[str, Any], surface_id: str) -> dict[str, Any]:
    surfaces = source.get("source_surfaces", {})
    if surface_id not in surfaces:
        if surface_id == CURRENT_SURFACE_ID:
            # Backward-compatible fallback for the original single-surface card.
            return {
                "id": CURRENT_SURFACE_ID,
                "status": "accepted",
                "powerbi_resource_key": source["powerbi_resource_key"],
                "powerbi_api_host": source["powerbi_api_host"],
                "metadata_endpoint": source["metadata_endpoint"],
                "conceptual_schema_endpoint": source["conceptual_schema_endpoint"],
                "querydata_endpoint": source["querydata_endpoint"],
                "model_id": source["model_id"],
                "report_id": source["report_id"],
                "dataset_id": source["dataset_id"],
                "dataset_display_name": source["dataset_display_name"],
                "observed_model_refresh_time": source["observed_model_refresh_time"],
            }
        raise ExtractionError(f"source card does not include surface {surface_id}")
    surface = dict(surfaces[surface_id])
    surface.setdefault("id", surface_id)
    return surface


def live_powerbi_surfaces(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        surface_id: source_surface(source, surface_id)
        for surface_id in sorted(set(QUERY_TEMPLATE_SURFACES.values()))
    }


def build_query_templates(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "version_summary": build_version_summary_template(source),
        "agency_by_fund_view": build_grouped_budget_template(
            source=source,
            group_source="a",
            group_entity="Titles_Agency",
            group_property="Title35",
            group_code_property="Agency",
            group_name="agency",
            group_code_name="agency_code",
            visual_id="codex_agency_by_fund_view",
        ),
        "functional_area_by_fund_view": build_grouped_budget_template(
            source=source,
            group_source="fa",
            group_entity="Titles_FunctionalArea",
            group_property="Title35",
            group_code_property="FunctionalArea",
            group_name="functional_area",
            group_code_name="functional_area_code",
            visual_id="codex_functional_area_by_fund_view",
        ),
        "historical_biennium_summary": build_historical_biennium_summary_template(source),
        "historical_agency_by_biennium": build_historical_grouped_budget_template(
            source=source,
            group_source="a",
            group_entity="Titles_Agency",
            group_property="Title35",
            group_code_property="Agency",
            group_name="agency",
            group_code_name="agency_code",
            visual_id="codex_historical_agency_by_biennium",
        ),
        "historical_functional_area_by_biennium": build_historical_grouped_budget_template(
            source=source,
            group_source="fa",
            group_entity="Titles_FunctionalArea",
            group_property="Title35",
            group_code_property="FunctionalArea",
            group_name="functional_area",
            group_code_name="functional_area_code",
            visual_id="codex_historical_functional_area_by_biennium",
        ),
    }


def build_version_summary_template(source: dict[str, Any]) -> dict[str, Any]:
    select = [
        select_column("v", "Verttl", "version_filter"),
        select_column("v", "Title35", "budget_version"),
        select_column("c", "Fundname", "fund_view"),
        select_min("v", "PublishDate", "publish_date"),
        select_sum("f", "Amount", "amount_thousands"),
    ]
    query = {
        "Version": 2,
        "From": common_from(include_functional_area=False),
        "Select": select,
        "Where": [
            in_filter("c", "Fundname", source["fund_views"]),
            not_null_filter("v", "Verttl"),
        ],
        "OrderBy": [
            order_by(column_expression("v", "PublishDate"), 2),
            order_by(column_expression("c", "Fundname"), 1),
        ],
    }
    return querydata_payload(
        source_surface(source, CURRENT_SURFACE_ID),
        query,
        list(range(len(select))),
        "codex_version_summary",
        1000,
    )


def build_grouped_budget_template(
    *,
    source: dict[str, Any],
    group_source: str,
    group_entity: str,
    group_property: str,
    group_code_property: str,
    group_name: str,
    group_code_name: str,
    visual_id: str,
) -> dict[str, Any]:
    select = [
        select_column(group_source, group_code_property, group_code_name),
        select_column(group_source, group_property, group_name),
        select_column("c", "Fundname", "fund_view"),
        select_sum("f", "Amount", "amount_thousands"),
    ]
    from_entities = common_from(include_functional_area=group_entity == "Titles_FunctionalArea")
    if group_entity == "Titles_Agency":
        from_entities.append({"Name": group_source, "Entity": group_entity, "Type": 0})
    query = {
        "Version": 2,
        "From": from_entities,
        "Select": select,
        "Where": [
            in_filter("v", "Verttl", [source["budget_version_filter"]]),
            in_filter("c", "Fundname", source["fund_views"]),
            not_null_filter(group_source, group_property),
        ],
        "OrderBy": [order_by(sum_expression("f", "Amount"), 2)],
    }
    return querydata_payload(
        source_surface(source, CURRENT_SURFACE_ID),
        query,
        list(range(len(select))),
        visual_id,
        500,
    )


def build_historical_biennium_summary_template(source: dict[str, Any]) -> dict[str, Any]:
    select = historical_base_select(include_publish_date=True)
    select.append(select_sum("f", "Amount", "amount_thousands"))
    query = {
        "Version": 2,
        "From": historical_common_from(include_functional_area=False),
        "Select": select,
        "Where": historical_default_where(source),
        "OrderBy": historical_order_by(),
    }
    return querydata_payload(
        source_surface(source, PRIOR_SURFACE_ID),
        query,
        list(range(len(select))),
        "codex_historical_biennium_summary",
        1000,
    )


def build_historical_grouped_budget_template(
    *,
    source: dict[str, Any],
    group_source: str,
    group_entity: str,
    group_property: str,
    group_code_property: str,
    group_name: str,
    group_code_name: str,
    visual_id: str,
) -> dict[str, Any]:
    select = historical_base_select(include_publish_date=False)
    select.extend(
        [
            select_column(group_source, group_code_property, group_code_name),
            select_column(group_source, group_property, group_name),
            select_min("v", "PublishDate", "publish_date"),
            select_sum("f", "Amount", "amount_thousands"),
        ]
    )
    from_entities = historical_common_from(include_functional_area=group_entity == "Titles_FunctionalArea")
    if group_entity == "Titles_Agency":
        from_entities.append({"Name": group_source, "Entity": group_entity, "Type": 0})
    query = {
        "Version": 2,
        "From": from_entities,
        "Select": select,
        "Where": historical_default_where(source) + [not_null_filter(group_source, group_property)],
        "OrderBy": historical_order_by() + [order_by(column_expression(group_source, group_property), 1)],
    }
    return querydata_payload(
        source_surface(source, PRIOR_SURFACE_ID),
        query,
        list(range(len(select))),
        visual_id,
        3000,
    )


def historical_base_select(*, include_publish_date: bool) -> list[dict[str, Any]]:
    select = [
        select_column("f", "Biennium", "biennium"),
        select_column("v", "SessionType", "session_type"),
        select_column("v", "Verttl", "budget_version_filter"),
        select_column("v", "Title35", "budget_version"),
    ]
    if include_publish_date:
        select.append(select_min("v", "PublishDate", "publish_date"))
    return select


def historical_default_where(source: dict[str, Any]) -> list[dict[str, Any]]:
    trend = source["default_trend"]
    return [
        in_filter("v", "Title35", [trend["budget_version"]]),
        in_filter("v", "SessionType", [trend["session_type"]]),
    ]


def historical_order_by() -> list[dict[str, Any]]:
    return [
        order_by(column_expression("f", "Biennium"), 1),
        order_by(column_expression("v", "PublishDate"), 1),
    ]


def common_from(*, include_functional_area: bool) -> list[dict[str, Any]]:
    from_entities = [
        {"Name": "f", "Entity": "Operating_Funding", "Type": 0},
        {"Name": "v", "Entity": "Operating_VersionInfo", "Type": 0},
        {"Name": "c", "Entity": "ComboFundBridge", "Type": 0},
    ]
    if include_functional_area:
        from_entities.append({"Name": "fa", "Entity": "Titles_FunctionalArea", "Type": 0})
    return from_entities


def historical_common_from(*, include_functional_area: bool) -> list[dict[str, Any]]:
    from_entities = [
        {"Name": "f", "Entity": "Operating_Funding", "Type": 0},
        {"Name": "v", "Entity": "Operating_VersionInfo", "Type": 0},
    ]
    if include_functional_area:
        from_entities.append({"Name": "fa", "Entity": "Titles_FunctionalArea", "Type": 0})
    return from_entities


def querydata_payload(
    surface: dict[str, Any],
    query: dict[str, Any],
    projections: list[int],
    visual_id: str,
    count: int,
) -> dict[str, Any]:
    return {
        "version": "1.0.0",
        "queries": [
            {
                "Query": {
                    "Commands": [
                        {
                            "SemanticQueryDataShapeCommand": {
                                "Query": query,
                                "Binding": {
                                    "Primary": {"Groupings": [{"Projections": projections}]},
                                    "DataReduction": {
                                        "DataVolume": 3,
                                        "Primary": {"Window": {"Count": count}},
                                    },
                                    "Version": 1,
                                },
                                "ExecutionMetricsKind": 1,
                            }
                        }
                    ]
                },
                "QueryId": "",
                "ApplicationContext": {
                    "DatasetId": surface["dataset_id"],
                    "Sources": [
                        {
                            "ReportId": surface["report_id"],
                            "VisualId": visual_id,
                        }
                    ],
                },
            }
        ],
        "cancelQueries": [],
        "modelId": surface["model_id"],
    }


def fetch_models_and_exploration(surface: dict[str, Any]) -> dict[str, Any]:
    return get_json(surface["metadata_endpoint"], surface)


def fetch_conceptual_schema(surface: dict[str, Any]) -> dict[str, Any]:
    return get_json(surface["conceptual_schema_endpoint"], surface)


def get_json(url: str, surface: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers=powerbi_headers(surface),
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            encoding = response.headers.get("Content-Encoding")
    except urllib.error.URLError as exc:
        raise ExtractionError(f"failed to fetch {url}: {exc}") from exc
    return json.loads(decode_response(raw, encoding))


def post_querydata(surface: dict[str, Any], query_template: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps(query_template, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        surface["querydata_endpoint"],
        data=payload,
        method="POST",
        headers={
            **powerbi_headers(surface),
            "ActivityId": "11111111-1111-4111-8111-111111111111",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://app.powerbi.com",
            "Referer": "https://app.powerbi.com/",
            "RequestId": "22222222-2222-4222-8222-222222222222",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            encoding = response.headers.get("Content-Encoding")
    except urllib.error.URLError as exc:
        raise ExtractionError(f"failed to post querydata: {exc}") from exc
    return json.loads(decode_response(raw, encoding))


def powerbi_headers(surface: dict[str, Any]) -> dict[str, str]:
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0",
        "X-PowerBI-ResourceKey": surface["powerbi_resource_key"],
    }


def decode_response(raw: bytes, content_encoding: str | None) -> str:
    if content_encoding == "gzip" or raw.startswith(b"\x1f\x8b"):
        return gzip.decompress(raw).decode("utf-8")
    return raw.decode("utf-8")


def verify_metadata(surface: dict[str, Any], metadata: dict[str, Any]) -> None:
    try:
        model = metadata["models"][0]
    except (KeyError, IndexError) as exc:
        raise ExtractionError("metadata response does not include models[0]") from exc
    if model.get("id") != surface["model_id"]:
        raise ExtractionError(
            f"model id mismatch for {surface['id']}: expected {surface['model_id']}, got {model.get('id')}"
        )
    if model.get("dbName") != surface["dataset_id"]:
        raise ExtractionError(
            f"dataset id mismatch for {surface['id']}: expected {surface['dataset_id']}, got {model.get('dbName')}"
        )


def response_data(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return payload["results"][0]["result"]["data"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ExtractionError("querydata response is missing results[0].result.data") from exc


def primary_rows(payload: dict[str, Any], block_name: str = "DM0") -> list[dict[str, Any]]:
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


def value_dicts(payload: dict[str, Any]) -> dict[str, list[Any]]:
    try:
        return response_data(payload)["dsr"]["DS"][0].get("ValueDicts", {})
    except (KeyError, IndexError, TypeError) as exc:
        raise ExtractionError("querydata response is missing dsr.DS[0]") from exc


def parse_rows(payload: dict[str, Any], output_fields: list[str]) -> list[dict[str, Any]]:
    rows = primary_rows(payload)
    dictionaries = value_dicts(payload)
    schema: list[dict[str, Any]] | None = None
    previous: list[Any] = []
    parsed: list[dict[str, Any]] = []

    for row in rows:
        if "S" in row:
            schema = row["S"]
        if "C" not in row:
            continue
        if schema is None:
            raise ExtractionError("compressed row encountered before schema row")

        values = []
        compressed_values = row["C"]
        compressed_index = 0
        repeat_mask = int(row.get("R", 0))
        for index, field_schema in enumerate(schema):
            if repeat_mask & (1 << index):
                value = previous[index]
            else:
                value = compressed_values[compressed_index]
                compressed_index += 1
            dictionary_name = field_schema.get("DN")
            if dictionary_name and isinstance(value, int):
                value = dictionaries[dictionary_name][value]
            values.append(value)

        previous = values
        if len(values) != len(output_fields):
            raise ExtractionError(
                f"expected {len(output_fields)} fields, parsed {len(values)}"
            )
        parsed.append(dict(zip(output_fields, values)))
    return parsed


def metric_row_count(payload: dict[str, Any]) -> int | None:
    events = response_data(payload).get("metrics", {}).get("Events", [])
    for event in events:
        metrics = event.get("Metrics", {})
        if "RowCount" in metrics:
            return int(metrics["RowCount"])
    return None


def normalize_grouped_budget_rows(
    source: dict[str, Any],
    rows: list[dict[str, Any]],
    group_field: str,
    group_code_field: str,
) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        amount_thousands = int(row["amount_thousands"])
        normalized.append(
            {
                "source_surface_id": CURRENT_SURFACE_ID,
                "biennium": source["biennium"],
                "period_type": "biennium",
                "budget_state": source["default_trend"]["budget_state"],
                "revision_scope": source["default_trend"]["revision_scope"],
                "budget_version": source["budget_version_label"],
                "budget_version_filter": source["budget_version_filter"],
                "fund_view": row["fund_view"],
                group_code_field: str(row[group_code_field]),
                group_field: row[group_field],
                "amount_thousands": amount_thousands,
                "budgeted_amount": amount_thousands * 1000,
            }
        )
    return normalized


def normalize_version_summary(
    source: dict[str, Any], rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        amount_thousands = int(row["amount_thousands"])
        publish_date = powerbi_date_to_iso(row.get("publish_date"))
        normalized.append(
            {
                "source_surface_id": CURRENT_SURFACE_ID,
                "biennium": source["biennium"],
                "period_type": "biennium",
                "budget_state": source["default_trend"]["budget_state"],
                "revision_scope": source["default_trend"]["revision_scope"],
                "version_filter": row["version_filter"],
                "budget_version": row["budget_version"],
                "fund_view": row["fund_view"],
                "publish_date": publish_date,
                "amount_thousands": amount_thousands,
                "budgeted_amount": amount_thousands * 1000,
            }
        )
    return normalized


def normalize_historical_summary_rows(
    source: dict[str, Any], rows: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    trend = source["default_trend"]
    normalized = []
    for row in rows:
        amount_thousands = int(row["amount_thousands"])
        normalized.append(
            {
                "source_surface_id": PRIOR_SURFACE_ID,
                "biennium": row["biennium"],
                "period_type": trend["period_type"],
                "session_type": row["session_type"],
                "budget_state": trend["budget_state"],
                "revision_scope": trend["revision_scope"],
                "budget_version_filter": row["budget_version_filter"],
                "budget_version": row["budget_version"],
                "fund_view": trend["fund_view"],
                "publish_date": powerbi_date_to_iso(row.get("publish_date")),
                "amount_thousands": amount_thousands,
                "budgeted_amount": amount_thousands * 1000,
            }
        )
    return normalized


def normalize_historical_grouped_budget_rows(
    source: dict[str, Any],
    rows: list[dict[str, Any]],
    group_field: str,
    group_code_field: str,
) -> list[dict[str, Any]]:
    trend = source["default_trend"]
    normalized = []
    for row in rows:
        amount_thousands = int(row["amount_thousands"])
        normalized.append(
            {
                "source_surface_id": PRIOR_SURFACE_ID,
                "biennium": row["biennium"],
                "period_type": trend["period_type"],
                "session_type": row["session_type"],
                "budget_state": trend["budget_state"],
                "revision_scope": trend["revision_scope"],
                "budget_version_filter": row["budget_version_filter"],
                "budget_version": row["budget_version"],
                "fund_view": trend["fund_view"],
                "publish_date": powerbi_date_to_iso(row.get("publish_date")),
                group_code_field: str(row[group_code_field]),
                group_field: row[group_field],
                "amount_thousands": amount_thousands,
                "budgeted_amount": amount_thousands * 1000,
            }
        )
    return normalized


def current_rows_as_historical(
    source: dict[str, Any],
    rows: list[dict[str, Any]],
    group_field: str,
    group_code_field: str,
) -> list[dict[str, Any]]:
    trend = source["default_trend"]
    historical = []
    for row in rows:
        if row["fund_view"] != trend["fund_view"]:
            continue
        historical.append(
            {
                "source_surface_id": CURRENT_SURFACE_ID,
                "biennium": row["biennium"],
                "period_type": trend["period_type"],
                "session_type": trend["session_type"],
                "budget_state": trend["budget_state"],
                "revision_scope": trend["revision_scope"],
                "budget_version_filter": row["budget_version_filter"],
                "budget_version": row["budget_version"],
                "fund_view": row["fund_view"],
                "publish_date": source["budget_version_date"],
                group_code_field: str(row[group_code_field]),
                group_field: row[group_field],
                "amount_thousands": row["amount_thousands"],
                "budgeted_amount": row["budgeted_amount"],
            }
        )
    return historical


def powerbi_date_to_iso(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).date().isoformat()
    return str(value)


def conceptual_entities(conceptual_schema: dict[str, Any]) -> dict[str, list[str]]:
    schemas = conceptual_schema.get("schemas", [])
    if not schemas:
        raise ExtractionError("conceptual schema response is missing schemas")
    schema = schemas[0].get("schema", {})
    entities = schema.get("Entities", [])
    keep = {
        "Operating_Funding",
        "Operating_VersionInfo",
        "ComboFundBridge",
        "Titles_Agency",
        "Titles_FunctionalArea",
    }
    return {
        entity.get("Name"): [prop.get("Name") for prop in entity.get("Properties", [])]
        for entity in entities
        if entity.get("Name") in keep
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
    version_rows = normalize_version_summary(
        source,
        parse_rows(
            responses["version_summary"],
            ["version_filter", "budget_version", "fund_view", "publish_date", "amount_thousands"],
        ),
    )
    agency_rows = normalize_grouped_budget_rows(
        source,
        parse_rows(
            responses["agency_by_fund_view"],
            ["agency_code", "agency", "fund_view", "amount_thousands"],
        ),
        "agency",
        "agency_code",
    )
    functional_area_rows = normalize_grouped_budget_rows(
        source,
        parse_rows(
            responses["functional_area_by_fund_view"],
            ["functional_area_code", "functional_area", "fund_view", "amount_thousands"],
        ),
        "functional_area",
        "functional_area_code",
    )
    historical_summary_rows = normalize_historical_summary_rows(
        source,
        parse_rows(
            responses["historical_biennium_summary"],
            [
                "biennium",
                "session_type",
                "budget_version_filter",
                "budget_version",
                "publish_date",
                "amount_thousands",
            ],
        ),
    )
    historical_agency_rows = normalize_historical_grouped_budget_rows(
        source,
        parse_rows(
            responses["historical_agency_by_biennium"],
            [
                "biennium",
                "session_type",
                "budget_version_filter",
                "budget_version",
                "agency_code",
                "agency",
                "publish_date",
                "amount_thousands",
            ],
        ),
        "agency",
        "agency_code",
    ) + current_rows_as_historical(source, agency_rows, "agency", "agency_code")
    historical_functional_area_rows = normalize_historical_grouped_budget_rows(
        source,
        parse_rows(
            responses["historical_functional_area_by_biennium"],
            [
                "biennium",
                "session_type",
                "budget_version_filter",
                "budget_version",
                "functional_area_code",
                "functional_area",
                "publish_date",
                "amount_thousands",
            ],
        ),
        "functional_area",
        "functional_area_code",
    ) + current_rows_as_historical(
        source,
        functional_area_rows,
        "functional_area",
        "functional_area_code",
    )

    normalized_dir = output_dir / "normalized"
    write_jsonl(normalized_dir / "version-summary.jsonl", version_rows)
    write_jsonl(normalized_dir / "agency-by-fund-view.jsonl", agency_rows)
    write_jsonl(normalized_dir / "functional-area-by-fund-view.jsonl", functional_area_rows)
    write_jsonl(normalized_dir / "historical-biennium-summary.jsonl", historical_summary_rows)
    write_jsonl(normalized_dir / "historical-agency-by-biennium.jsonl", historical_agency_rows)
    write_jsonl(
        normalized_dir / "historical-functional-area-by-biennium.jsonl",
        historical_functional_area_rows,
    )

    totals_by_fund = totals_by(agency_rows, "fund_view")
    functional_totals_by_fund = totals_by(functional_area_rows, "fund_view")
    for fund_view, agency_total in totals_by_fund.items():
        function_total = functional_totals_by_fund.get(fund_view)
        if function_total != agency_total:
            raise ExtractionError(
                f"agency/function total mismatch for {fund_view}: "
                f"{agency_total} vs {function_total}"
            )

    historical_summary_totals = totals_by(historical_summary_rows, "biennium")
    historical_agency_totals = totals_by(historical_agency_rows, "biennium")
    historical_functional_area_totals = totals_by(historical_functional_area_rows, "biennium")
    if historical_summary_totals != historical_agency_totals:
        raise ExtractionError(
            "historical statewide/agency totals mismatch: "
            f"{historical_summary_totals} vs {historical_agency_totals}"
        )
    if historical_summary_totals != historical_functional_area_totals:
        raise ExtractionError(
            "historical statewide/functional-area totals mismatch: "
            f"{historical_summary_totals} vs {historical_functional_area_totals}"
        )
    current_default_total = totals_by_fund[source["default_trend"]["fund_view"]]
    historical_current_total = historical_summary_totals.get(source["biennium"])
    if historical_current_total != current_default_total:
        raise ExtractionError(
            f"historical/current overlap mismatch for {source['biennium']}: "
            f"{historical_current_total} vs {current_default_total}"
        )
    verify_unique_keys(historical_summary_rows, ["biennium"], "historical biennium")
    verify_unique_keys(
        historical_agency_rows,
        ["biennium", "agency_code"],
        "historical agency",
    )
    verify_unique_keys(
        historical_functional_area_rows,
        ["biennium", "functional_area_code"],
        "historical functional area",
    )

    default_fund_view = source["default_fund_view"]
    default_agency_rows = [row for row in agency_rows if row["fund_view"] == default_fund_view]
    default_function_rows = [
        row for row in functional_area_rows if row["fund_view"] == default_fund_view
    ]
    biennia = sorted(historical_summary_totals)

    summary = {
        "source_id": source["id"],
        "snapshot_version": source["snapshot_version"],
        "model_refresh_time": model_metadata(metadata[CURRENT_SURFACE_ID]).get("LastRefreshTime"),
        "surface_refresh_times": {
            surface_id: model_metadata(surface_metadata).get("LastRefreshTime")
            for surface_id, surface_metadata in metadata.items()
        },
        "biennium": source["biennium"],
        "budget_version_filter": source["budget_version_filter"],
        "budget_version": source["budget_version_label"],
        "fund_views": source["fund_views"],
        "default_fund_view": default_fund_view,
        "default_trend": source["default_trend"],
        "historical_coverage": {
            "biennia": biennia,
            "start_biennium": biennia[0],
            "end_biennium": biennia[-1],
            "statewide_grain": True,
            "agency_grain": True,
            "functional_area_grain": True,
        },
        "amount_units": "dollars",
        "row_counts": {
            "version_summary": len(version_rows),
            "agency_by_fund_view": len(agency_rows),
            "functional_area_by_fund_view": len(functional_area_rows),
            "historical_biennium_summary": len(historical_summary_rows),
            "historical_agency_by_biennium": len(historical_agency_rows),
            "historical_functional_area_by_biennium": len(historical_functional_area_rows),
        },
        "validation_checks": {
            "default_fund_view_total": totals_by_fund[default_fund_view],
            "default_fund_view_agency_rows": len(default_agency_rows),
            "default_fund_view_functional_area_rows": len(default_function_rows),
            "totals_by_fund_view": totals_by_fund,
            "agency_function_totals_match": True,
            "historical_totals_by_biennium": historical_summary_totals,
            "historical_agency_totals_match": True,
            "historical_functional_area_totals_match": True,
            "historical_current_overlap_matches": True,
            "historical_current_overlap_total": historical_current_total,
        },
        "top_agencies_default_fund_view": top_rows(
            default_agency_rows, "agency", "budgeted_amount", 8
        ),
        "top_functional_areas_default_fund_view": top_rows(
            default_function_rows, "functional_area", "budgeted_amount", 8
        ),
        "notes": [
            "Amounts are budgeted/authorized report values, not actual spending.",
            "Fiscal WA report values are returned in thousands; normalized rows store dollars.",
            "Outlook Funds (NGF-O) and Total Budgeted are separate fund views.",
            (
                "Historical trend rows default to enacted base biennial operating "
                "budgets, using Fiscal WA SessionType R1 and budget version Enacted."
            ),
        ],
    }
    write_json(output_dir / "summary.json", summary)

    provenance = {
        "source_id": source["id"],
        "generated_by": "jurisdictions/washington/scripts/extract_operating_budget.py",
        "generated_from_live_powerbi": live,
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "official_dashboard_page": source["official_dashboard_page"],
        "official_context_page": source["official_context_page"],
        "powerbi_report_url": source["powerbi_report_url"],
        "api_host": source["powerbi_api_host"],
        "source_surfaces": source_surfaces_provenance(source),
        "model_metadata": model_metadata(metadata[CURRENT_SURFACE_ID]),
        "model_metadata_by_surface": {
            surface_id: model_metadata(surface_metadata)
            for surface_id, surface_metadata in metadata.items()
        },
        "source_card_expected_models": {
            surface_id: {
                "model_id": source_surface(source, surface_id)["model_id"],
                "dataset_id": source_surface(source, surface_id)["dataset_id"],
                "observed_model_refresh_time": source_surface(
                    source, surface_id
                )["observed_model_refresh_time"],
            }
            for surface_id in metadata
        },
        "filters": {
            "budget_version_filter": source["budget_version_filter"],
            "budget_version": source["budget_version_label"],
            "fund_views": source["fund_views"],
            "default_trend": source["default_trend"],
        },
        "conceptual_entities": conceptual_entities(conceptual_schema[CURRENT_SURFACE_ID]),
        "conceptual_entities_by_surface": {
            surface_id: conceptual_entities(surface_schema)
            for surface_id, surface_schema in conceptual_schema.items()
        },
        "raw_response_policy": {
            "committed_raw_live_responses": False,
            "local_raw_capture_path": "jurisdictions/washington/data/operating-budget/local_raw/",
            "reproduction": (
                "python3 jurisdictions/washington/scripts/extract_operating_budget.py "
                "--live --write-query-templates "
                "--raw-dir jurisdictions/washington/data/operating-budget/local_raw"
            ),
        },
        "query_templates": query_template_provenance(templates, responses),
        "response_metrics": {
            key: {"row_count": metric_row_count(response)}
            for key, response in responses.items()
        },
    }
    write_json(output_dir / "provenance.json", provenance)


def verify_unique_keys(
    rows: list[dict[str, Any]], key_fields: list[str], label: str
) -> None:
    seen: set[tuple[Any, ...]] = set()
    for row in rows:
        key = tuple(row[field] for field in key_fields)
        if key in seen:
            raise ExtractionError(f"duplicate {label} row key: {key}")
        seen.add(key)


def totals_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    totals: dict[str, int] = {}
    for row in rows:
        totals[row[key]] = totals.get(row[key], 0) + int(row["budgeted_amount"])
    return dict(sorted(totals.items()))


def top_rows(
    rows: list[dict[str, Any]], label_field: str, amount_field: str, count: int
) -> list[dict[str, Any]]:
    return [
        {label_field: row[label_field], amount_field: row[amount_field]}
        for row in sorted(rows, key=lambda item: item[amount_field], reverse=True)[:count]
    ]


def model_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    model = metadata["models"][0]
    exploration = metadata.get("exploration", {})
    report = exploration.get("report", {})
    return {
        "model_id": model.get("id"),
        "display_name": model.get("displayName"),
        "dataset_id": model.get("dbName"),
        "LastRefreshTime": model.get("LastRefreshTime"),
        "direct_query_mode": model.get("directQueryMode"),
        "size_in_mbs": model.get("sizeInMBs"),
        "exploration_id": exploration.get("id"),
        "report_id": exploration.get("reportId"),
        "report_object_id": report.get("objectId"),
    }


def query_template_provenance(
    templates: dict[str, dict[str, Any]], responses: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    details = {}
    for key, template in templates.items():
        details[key] = {
            "template_path": str((QUERY_TEMPLATE_ROOT / QUERY_TEMPLATE_FILES[key]).relative_to(ROOT)),
            "template_sha256": sha256_json(template),
            "response_sha256": sha256_json(responses[key]),
            "source_surface_id": QUERY_TEMPLATE_SURFACES[key],
            "visual_id": visual_id(template),
        }
    return details


def source_surfaces_provenance(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    surfaces = source.get("source_surfaces", {})
    if not surfaces:
        return {
            CURRENT_SURFACE_ID: {
                "status": "accepted",
                "official_dashboard_page": source["official_dashboard_page"],
                "powerbi_report_url": source["powerbi_report_url"],
                "dataset_display_name": source["dataset_display_name"],
                "dataset_id": source["dataset_id"],
                "model_id": source["model_id"],
                "report_id": source["report_id"],
            }
        }
    keep = [
        "status",
        "official_dashboard_page",
        "powerbi_report_url",
        "dataset_display_name",
        "dataset_id",
        "model_id",
        "report_id",
        "coverage",
        "notes",
    ]
    return {
        surface_id: {
            key: surface[key]
            for key in keep
            if key in surface
        }
        for surface_id, surface in surfaces.items()
    }


def visual_id(query_template: dict[str, Any]) -> str | None:
    try:
        sources = query_template["queries"][0]["ApplicationContext"]["Sources"]
    except (KeyError, IndexError, TypeError):
        return None
    if not sources:
        return None
    return sources[0].get("VisualId")


if __name__ == "__main__":
    main()
