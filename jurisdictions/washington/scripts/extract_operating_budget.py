#!/usr/bin/env python3
"""Extract the Washington Fiscal WA operating budget snapshot.

This script is intentionally source-specific. It replays reviewed Power BI
query payloads for the Fiscal WA 2025-27 biennial operating summary comparison
report and normalizes the known response shapes. It is not a generic Power BI
adapter.
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

QUERY_TEMPLATE_FILES = {
    "version_summary": "version-summary.query.json",
    "agency_by_fund_view": "agency-by-fund-view.query.json",
    "functional_area_by_fund_view": "functional-area-by-fund-view.query.json",
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
        metadata = fetch_models_and_exploration(source)
        conceptual_schema = fetch_conceptual_schema(source)
        verify_metadata(source, metadata)
        responses = {key: post_querydata(source, template) for key, template in templates.items()}
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


def build_query_templates(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "version_summary": build_version_summary_template(source),
        "agency_by_fund_view": build_grouped_budget_template(
            source=source,
            group_source="a",
            group_entity="Titles_Agency",
            group_property="Title35",
            group_name="agency",
            visual_id="codex_agency_by_fund_view",
        ),
        "functional_area_by_fund_view": build_grouped_budget_template(
            source=source,
            group_source="fa",
            group_entity="Titles_FunctionalArea",
            group_property="Title35",
            group_name="functional_area",
            visual_id="codex_functional_area_by_fund_view",
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
    return querydata_payload(source, query, list(range(len(select))), "codex_version_summary", 1000)


def build_grouped_budget_template(
    *,
    source: dict[str, Any],
    group_source: str,
    group_entity: str,
    group_property: str,
    group_name: str,
    visual_id: str,
) -> dict[str, Any]:
    select = [
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
    return querydata_payload(source, query, list(range(len(select))), visual_id, 500)


def common_from(*, include_functional_area: bool) -> list[dict[str, Any]]:
    from_entities = [
        {"Name": "f", "Entity": "Operating_Funding", "Type": 0},
        {"Name": "v", "Entity": "Operating_VersionInfo", "Type": 0},
        {"Name": "c", "Entity": "ComboFundBridge", "Type": 0},
    ]
    if include_functional_area:
        from_entities.append({"Name": "fa", "Entity": "Titles_FunctionalArea", "Type": 0})
    return from_entities


def querydata_payload(
    source: dict[str, Any],
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
                    "DatasetId": source["dataset_id"],
                    "Sources": [
                        {
                            "ReportId": source["report_id"],
                            "VisualId": visual_id,
                        }
                    ],
                },
            }
        ],
        "cancelQueries": [],
        "modelId": source["model_id"],
    }


def fetch_models_and_exploration(source: dict[str, Any]) -> dict[str, Any]:
    return get_json(source["metadata_endpoint"], source)


def fetch_conceptual_schema(source: dict[str, Any]) -> dict[str, Any]:
    return get_json(source["conceptual_schema_endpoint"], source)


def get_json(url: str, source: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers=powerbi_headers(source),
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            encoding = response.headers.get("Content-Encoding")
    except urllib.error.URLError as exc:
        raise ExtractionError(f"failed to fetch {url}: {exc}") from exc
    return json.loads(decode_response(raw, encoding))


def post_querydata(source: dict[str, Any], query_template: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps(query_template, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        source["querydata_endpoint"],
        data=payload,
        method="POST",
        headers={
            **powerbi_headers(source),
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


def powerbi_headers(source: dict[str, Any]) -> dict[str, str]:
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0",
        "X-PowerBI-ResourceKey": source["powerbi_resource_key"],
    }


def decode_response(raw: bytes, content_encoding: str | None) -> str:
    if content_encoding == "gzip" or raw.startswith(b"\x1f\x8b"):
        return gzip.decompress(raw).decode("utf-8")
    return raw.decode("utf-8")


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
) -> list[dict[str, Any]]:
    normalized = []
    for row in rows:
        amount_thousands = int(row["amount_thousands"])
        normalized.append(
            {
                "biennium": source["biennium"],
                "budget_version": source["budget_version_label"],
                "budget_version_filter": source["budget_version_filter"],
                "fund_view": row["fund_view"],
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
                "biennium": source["biennium"],
                "version_filter": row["version_filter"],
                "budget_version": row["budget_version"],
                "fund_view": row["fund_view"],
                "publish_date": publish_date,
                "amount_thousands": amount_thousands,
                "budgeted_amount": amount_thousands * 1000,
            }
        )
    return normalized


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
    verify_metadata(source, metadata)

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
            ["agency", "fund_view", "amount_thousands"],
        ),
        "agency",
    )
    functional_area_rows = normalize_grouped_budget_rows(
        source,
        parse_rows(
            responses["functional_area_by_fund_view"],
            ["functional_area", "fund_view", "amount_thousands"],
        ),
        "functional_area",
    )

    normalized_dir = output_dir / "normalized"
    write_jsonl(normalized_dir / "version-summary.jsonl", version_rows)
    write_jsonl(normalized_dir / "agency-by-fund-view.jsonl", agency_rows)
    write_jsonl(normalized_dir / "functional-area-by-fund-view.jsonl", functional_area_rows)

    totals_by_fund = totals_by(agency_rows, "fund_view")
    functional_totals_by_fund = totals_by(functional_area_rows, "fund_view")
    for fund_view, agency_total in totals_by_fund.items():
        function_total = functional_totals_by_fund.get(fund_view)
        if function_total != agency_total:
            raise ExtractionError(
                f"agency/function total mismatch for {fund_view}: "
                f"{agency_total} vs {function_total}"
            )

    default_fund_view = source["default_fund_view"]
    default_agency_rows = [row for row in agency_rows if row["fund_view"] == default_fund_view]
    default_function_rows = [
        row for row in functional_area_rows if row["fund_view"] == default_fund_view
    ]

    summary = {
        "source_id": source["id"],
        "snapshot_version": source["snapshot_version"],
        "model_refresh_time": model_metadata(metadata).get("LastRefreshTime"),
        "biennium": source["biennium"],
        "budget_version_filter": source["budget_version_filter"],
        "budget_version": source["budget_version_label"],
        "fund_views": source["fund_views"],
        "default_fund_view": default_fund_view,
        "amount_units": "dollars",
        "row_counts": {
            "version_summary": len(version_rows),
            "agency_by_fund_view": len(agency_rows),
            "functional_area_by_fund_view": len(functional_area_rows),
        },
        "validation_checks": {
            "default_fund_view_total": totals_by_fund[default_fund_view],
            "default_fund_view_agency_rows": len(default_agency_rows),
            "default_fund_view_functional_area_rows": len(default_function_rows),
            "totals_by_fund_view": totals_by_fund,
            "agency_function_totals_match": True,
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
        "model_metadata": model_metadata(metadata),
        "source_card_expected_model": {
            "model_id": source["model_id"],
            "dataset_id": source["dataset_id"],
            "observed_model_refresh_time": source["observed_model_refresh_time"],
        },
        "filters": {
            "budget_version_filter": source["budget_version_filter"],
            "budget_version": source["budget_version_label"],
            "fund_views": source["fund_views"],
        },
        "conceptual_entities": conceptual_entities(conceptual_schema),
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
            "visual_id": visual_id(template),
        }
    return details


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
