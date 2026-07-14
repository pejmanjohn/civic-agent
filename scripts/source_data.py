#!/usr/bin/env python3
"""Managed local data helpers for Civic Agent sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "jurisdictions"
DEFAULT_DATA_HOME = Path.home() / ".civic-agent" / "data"


class SourceDataError(RuntimeError):
    pass


@dataclass
class SourceContext:
    source_id: str
    source_card: dict[str, Any]
    data_home: Path
    source_dir: Path
    manifest_path: Path


Builder = Callable[[SourceContext, bool], dict[str, Any]]
QueryRunner = Callable[[SourceContext, str, dict[str, str]], dict[str, Any]]
Validator = Callable[[SourceContext, bool], dict[str, Any]]

BUILDER_REGISTRY: dict[str, Builder] = {}
QUERY_REGISTRY: dict[str, QueryRunner] = {}
VALIDATOR_REGISTRY: dict[str, Validator] = {}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect and manage Civic Agent source data.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON.",
    )
    parser.add_argument(
        "--data-home",
        type=Path,
        default=None,
        help="Override the Civic Agent data cache directory.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    for name in ("inspect", "status", "ensure", "refresh"):
        command = subcommands.add_parser(name)
        command.add_argument("source_id")

    query = subcommands.add_parser("query")
    query.add_argument("source_id")
    query.add_argument("named_query")
    query.add_argument(
        "--param",
        action="append",
        default=[],
        help="Named query parameter as key=value. May be passed multiple times.",
    )

    validate = subcommands.add_parser("validate")
    validate.add_argument("source_id", nargs="?")
    validate.add_argument(
        "--all",
        action="store_true",
        dest="all_sources",
        help="Validate every reviewed source card.",
    )
    validate.add_argument(
        "--refresh-check",
        action="store_true",
        help="Run optional source-specific drift checks when available.",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        result = run_command(args)
    except SourceDataError as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result)


def run_command(args: argparse.Namespace) -> dict[str, Any]:
    if args.command == "validate":
        if args.all_sources:
            return validate_all(data_home=args.data_home, refresh_check=args.refresh_check)
        if not args.source_id:
            raise SourceDataError("validate requires a source_id or --all")
        return validate_source(
            source_context(args.source_id, data_home=args.data_home),
            refresh_check=args.refresh_check,
        )

    context = source_context(args.source_id, data_home=args.data_home)
    if args.command == "inspect":
        return inspect_source(context)
    if args.command == "status":
        return status_source(context)
    if args.command == "ensure":
        return ensure_source(context, force=False)
    if args.command == "refresh":
        return ensure_source(context, force=True)
    if args.command == "query":
        return query_source(context, args.named_query, parse_params(args.param))
    raise SourceDataError(f"Unknown command: {args.command}")


def source_context(source_id: str, *, data_home: Path | None = None) -> SourceContext:
    source_card = load_source_card(source_id)
    home = data_home or data_home_from_env()
    source_dir = home / "sources" / safe_source_path(source_id)
    return SourceContext(
        source_id=source_id,
        source_card=source_card,
        data_home=home,
        source_dir=source_dir,
        manifest_path=source_dir / "manifest.json",
    )


def data_home_from_env() -> Path:
    configured = os.environ.get("CIVIC_AGENT_DATA_HOME")
    if configured:
        return Path(configured).expanduser()
    return DEFAULT_DATA_HOME


def safe_source_path(source_id: str) -> Path:
    return Path(*source_id.split("."))


def load_source_card(source_id: str) -> dict[str, Any]:
    matches = []
    for path in sorted(SOURCE_ROOT.glob("*/sources/*.source.json")):
        with path.open(encoding="utf-8") as handle:
            source = json.load(handle)
        if source.get("id") == source_id:
            source["_path"] = path.relative_to(ROOT).as_posix()
            matches.append(source)
    if not matches:
        raise SourceDataError(f"Unknown source id: {source_id}")
    if len(matches) > 1:
        raise SourceDataError(f"Source id is not unique: {source_id}")
    return matches[0]


def load_source_cards() -> list[dict[str, Any]]:
    sources = []
    for path in sorted(SOURCE_ROOT.glob("*/sources/*.source.json")):
        with path.open(encoding="utf-8") as handle:
            source = json.load(handle)
        source["_path"] = path.relative_to(ROOT).as_posix()
        sources.append(source)
    return sources


def inspect_source(context: SourceContext) -> dict[str, Any]:
    return {
        "ok": True,
        "command": "inspect",
        "source_id": context.source_id,
        "source_card_path": context.source_card["_path"],
        "data_home": str(context.data_home),
        "source_dir": str(context.source_dir),
        "storage_policy": context.source_card.get("storage_policy", {}),
        "access_method": context.source_card.get("access_method"),
    }


def status_source(context: SourceContext) -> dict[str, Any]:
    policy = context.source_card.get("storage_policy", {})
    if not context.manifest_path.is_file():
        return {
            "ok": True,
            "command": "status",
            "source_id": context.source_id,
            "status": "missing",
            "storage_tier": policy.get("tier"),
            "normal_answer_source": policy.get("normal_answer_source"),
            "data_home": str(context.data_home),
            "manifest_path": str(context.manifest_path),
            "message": "No local manifest exists for this source.",
        }
    manifest = read_json(context.manifest_path)
    database_path = manifest.get("database_path")
    if (
        context.source_card.get("storage_policy", {}).get("tier") == "managed_local_db"
        and database_path
        and not Path(database_path).is_file()
    ):
        manifest["status"] = "missing"
        manifest["message"] = f"Manifest exists but local database is missing: {database_path}"
    elif context.source_card.get("storage_policy", {}).get("tier") == "managed_local_db":
        stale_reason = managed_source_stale_reason(context.source_card, manifest)
        if stale_reason:
            manifest["status"] = "stale"
            manifest["message"] = stale_reason
    manifest.setdefault("ok", True)
    manifest.setdefault("command", "status")
    manifest.setdefault("source_id", context.source_id)
    manifest.setdefault("manifest_path", str(context.manifest_path))
    return manifest


def managed_source_stale_reason(
    source_card: dict[str, Any],
    manifest: dict[str, Any],
) -> str | None:
    accepted_surfaces = {
        surface_id: surface
        for surface_id, surface in source_card.get("source_surfaces", {}).items()
        if surface.get("status") == "accepted"
    }
    if not accepted_surfaces:
        return None
    manifest_files = {
        file_info.get("source_surface_id"): file_info
        for file_info in manifest.get("source_files", [])
        if file_info.get("source_surface_id")
    }
    for surface_id, surface in accepted_surfaces.items():
        file_info = manifest_files.get(surface_id)
        if file_info is None:
            return f"Local manifest is missing accepted source surface: {surface_id}"
        for field in ("url", "last_modified", "content_length"):
            expected = surface.get(field)
            if expected is None:
                continue
            observed = file_info.get(field)
            if observed != expected:
                return (
                    f"Local manifest metadata for {surface_id} is stale: "
                    f"{field} is {observed!r}, expected {expected!r}"
                )
    return None


def validate_all(*, data_home: Path | None, refresh_check: bool) -> dict[str, Any]:
    home = data_home or data_home_from_env()
    results = []
    for source_card in load_source_cards():
        if "storage_policy" not in source_card:
            continue
        context = SourceContext(
            source_id=source_card["id"],
            source_card=source_card,
            data_home=home,
            source_dir=home / "sources" / safe_source_path(source_card["id"]),
            manifest_path=home
            / "sources"
            / safe_source_path(source_card["id"])
            / "manifest.json",
        )
        results.append(validate_source(context, refresh_check=refresh_check))
    ok = all(result.get("ok") for result in results)
    return {
        "ok": ok,
        "command": "validate",
        "status": "valid" if ok else "validation_failed",
        "source_count": len(results),
        "results": results,
    }


def validate_source(context: SourceContext, *, refresh_check: bool = False) -> dict[str, Any]:
    validator = VALIDATOR_REGISTRY.get(context.source_id) or load_validator(context.source_id)
    if validator is None:
        validator = validate_by_storage_tier
    try:
        result = validator(context, refresh_check)
    except SourceDataError:
        raise
    except Exception as exc:
        result = {
            "ok": False,
            "command": "validate",
            "source_id": context.source_id,
            "status": "validation_failed",
            "storage_tier": context.source_card.get("storage_policy", {}).get("tier"),
            "normal_answer_source": context.source_card.get("storage_policy", {}).get(
                "normal_answer_source"
            ),
            "checks": [failed_check("validator_error", message=str(exc))],
            "warnings": [],
            "message": str(exc),
        }
    if not isinstance(result, dict):
        raise SourceDataError(f"Validator returned non-object result for {context.source_id}")
    return normalize_validation_result(context, result)


def load_validator(source_id: str) -> Validator | None:
    validators: dict[str, Validator] = {
        "seattle.operating_budget": validate_live_source,
        "king_county.open_budget_dashboard": validate_king_county_open_budget_snapshot,
        "washington.operating_budget": validate_washington_operating_budget_snapshot,
        "washington.revenue_by_biennium": validate_washington_revenue_snapshot,
        "washington.open_checkbook": validate_washington_open_checkbook,
        "washington.ofm_population": validate_washington_ofm_population_snapshot,
        "washington.fit_filed_actuals": validate_washington_fit_snapshot,
    }
    return validators.get(source_id)


def validate_by_storage_tier(context: SourceContext, refresh_check: bool) -> dict[str, Any]:
    tier = context.source_card.get("storage_policy", {}).get("tier")
    if tier == "live":
        return validate_live_source(context, refresh_check)
    return validation_result(
        context,
        status="validation_failed",
        checks=source_fingerprint_contract_checks(context.source_card)
        + [
            failed_check(
                "validator_registered",
                message=f"No validator is registered for storage tier {tier!r}.",
            )
        ],
    )


def normalize_validation_result(context: SourceContext, result: dict[str, Any]) -> dict[str, Any]:
    policy = context.source_card.get("storage_policy", {})
    result.setdefault("command", "validate")
    result.setdefault("source_id", context.source_id)
    result.setdefault("storage_tier", policy.get("tier"))
    result.setdefault("normal_answer_source", policy.get("normal_answer_source"))
    result.setdefault("source_card_path", context.source_card.get("_path"))
    result.setdefault("source_fingerprint", context.source_card.get("source_fingerprint", {}))
    result.setdefault("checks", [])
    result.setdefault("warnings", [])
    result.setdefault("status", status_from_checks(result["checks"]))
    result.setdefault("ok", result["status"] in {"valid", "partial_current_period"})
    return result


def validation_result(
    context: SourceContext,
    *,
    status: str | None = None,
    checks: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    source_fingerprint: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    checks = checks or []
    status = status or status_from_checks(checks)
    return {
        "ok": status in {"valid", "partial_current_period"},
        "command": "validate",
        "source_id": context.source_id,
        "storage_tier": context.source_card.get("storage_policy", {}).get("tier"),
        "normal_answer_source": context.source_card.get("storage_policy", {}).get(
            "normal_answer_source"
        ),
        "status": status,
        "source_card_path": context.source_card.get("_path"),
        "source_fingerprint": source_fingerprint
        if source_fingerprint is not None
        else context.source_card.get("source_fingerprint", {}),
        "checks": checks,
        "warnings": warnings or [],
        **extra,
    }


def status_from_checks(checks: list[dict[str, Any]]) -> str:
    if any(check.get("status") == "failed" for check in checks):
        return "validation_failed"
    return "valid"


def passed_check(
    name: str,
    *,
    evidence: dict[str, Any] | None = None,
    message: str = "",
) -> dict[str, Any]:
    return validation_check(name, "passed", evidence=evidence, message=message)


def failed_check(
    name: str,
    *,
    evidence: dict[str, Any] | None = None,
    message: str = "",
) -> dict[str, Any]:
    return validation_check(name, "failed", evidence=evidence, message=message)


def skipped_check(
    name: str,
    *,
    evidence: dict[str, Any] | None = None,
    message: str = "",
) -> dict[str, Any]:
    return validation_check(name, "skipped", evidence=evidence, message=message)


def validation_check(
    name: str,
    status: str,
    *,
    evidence: dict[str, Any] | None = None,
    message: str = "",
) -> dict[str, Any]:
    check = {"name": name, "status": status}
    if evidence is not None:
        check["evidence"] = evidence
    if message:
        check["message"] = message
    return check


def source_fingerprint_contract_checks(source_card: dict[str, Any]) -> list[dict[str, Any]]:
    required = {
        "public_inspection_urls",
        "machine_access",
        "retrieval_context",
        "version_boundary",
        "row_counts",
        "checks",
    }
    fingerprint = source_card.get("source_fingerprint")
    if not isinstance(fingerprint, dict):
        return [
            failed_check(
                "source_fingerprint_present",
                message="Source card is missing source_fingerprint.",
            )
        ]
    checks = [
        passed_check(
            "source_fingerprint_present",
            evidence={"fields": sorted(fingerprint)},
        )
    ]
    missing = sorted(required - set(fingerprint))
    if missing:
        checks.append(
            failed_check(
                "source_fingerprint_required_fields",
                evidence={"missing": missing},
                message="Source fingerprint is missing required fields.",
            )
        )
    else:
        checks.append(
            passed_check(
                "source_fingerprint_required_fields",
                evidence={"required": sorted(required)},
            )
        )
    public_urls = fingerprint.get("public_inspection_urls")
    if isinstance(public_urls, list) and public_urls:
        checks.append(
            passed_check(
                "source_fingerprint_public_urls",
                evidence={"count": len(public_urls)},
            )
        )
    else:
        checks.append(
            failed_check(
                "source_fingerprint_public_urls",
                message="Source fingerprint must include at least one public inspection URL.",
            )
        )
    return checks


def refresh_check_placeholder(refresh_check: bool) -> tuple[list[dict[str, Any]], list[str]]:
    if not refresh_check:
        return [], []
    message = (
        "Refresh-check requested, but this source currently supports offline "
        "validation only; normal answer routing is unchanged."
    )
    return [
        skipped_check(
            "refresh_check",
            evidence={"mode": "offline_only"},
            message=message,
        )
    ], [message]


def ensure_source(context: SourceContext, *, force: bool) -> dict[str, Any]:
    policy = context.source_card.get("storage_policy", {})
    tier = policy.get("tier")
    if tier != "managed_local_db":
        return {
            "ok": True,
            "command": "refresh" if force else "ensure",
            "source_id": context.source_id,
            "status": "not_managed",
            "storage_tier": tier,
            "normal_answer_source": policy.get("normal_answer_source"),
            "message": "This source does not require managed local data.",
        }

    builder = BUILDER_REGISTRY.get(context.source_id) or load_builder(context.source_id)
    if builder is None:
        raise SourceDataError(f"No local data builder is registered for {context.source_id}")
    context.source_dir.mkdir(parents=True, exist_ok=True)
    current_status = status_source(context)
    current_status_value = current_status.get("status")
    builder_force = (
        force
        or current_status_value in {"stale", "refresh_failed"}
        or (current_status_value == "missing" and context.manifest_path.is_file())
    )
    try:
        result = builder(context, builder_force)
    except SourceDataError:
        raise
    except Exception as exc:
        raise SourceDataError(str(exc)) from exc
    result.setdefault("ok", True)
    result.setdefault("command", "refresh" if force else "ensure")
    result.setdefault("source_id", context.source_id)
    result.setdefault("refreshed_at", utc_now())
    write_json(context.manifest_path, result)
    return result


def load_builder(source_id: str) -> Builder | None:
    if source_id == "washington.open_checkbook":
        scripts_dir = ROOT / "jurisdictions" / "washington" / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        try:
            import extract_open_checkbook
        except ModuleNotFoundError:
            return None
        return extract_open_checkbook.build_local_database
    return None


def query_source(
    context: SourceContext,
    named_query: str,
    params: dict[str, str],
) -> dict[str, Any]:
    runner = QUERY_REGISTRY.get(context.source_id) or load_query_runner(context.source_id)
    if runner is None:
        raise SourceDataError(f"No local query runner is registered for {context.source_id}")
    try:
        return runner(context, named_query, params)
    except SourceDataError:
        raise
    except Exception as exc:
        raise SourceDataError(str(exc)) from exc


def load_query_runner(source_id: str) -> QueryRunner | None:
    if source_id == "washington.open_checkbook":
        scripts_dir = ROOT / "jurisdictions" / "washington" / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        try:
            import extract_open_checkbook
        except ModuleNotFoundError:
            return None
        return extract_open_checkbook.run_named_query
    return None


def validate_live_source(context: SourceContext, refresh_check: bool) -> dict[str, Any]:
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    checks.append(
        passed_check(
            "live_artifact_not_required",
            evidence={"storage_tier": "live"},
            message="Live source validation checks the source-card contract only.",
        )
    )
    return validation_result(context, checks=checks, warnings=warnings)


def validate_king_county_open_budget_snapshot(
    context: SourceContext,
    refresh_check: bool,
) -> dict[str, Any]:
    snapshot_dir = (
        ROOT
        / "jurisdictions"
        / "king_county"
        / "data"
        / "open-budget-dashboard"
        / context.source_card["snapshot_version"]
    )
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    summary, provenance = load_snapshot_artifacts(snapshot_dir, checks)
    if summary is None or provenance is None:
        return validation_result(
            context,
            status="validation_failed",
            checks=checks,
            warnings=warnings,
            snapshot_path=str(snapshot_dir),
        )
    checks.extend(artifact_fingerprint_checks(summary, provenance))

    overview_rows = load_jsonl_artifact(
        snapshot_dir / "normalized" / "overview-by-year.jsonl",
        checks,
        "overview_by_year_jsonl",
    )
    department_rows = load_jsonl_artifact(
        snapshot_dir / "normalized" / "department-revenue-expenditure-by-year.jsonl",
        checks,
        "department_revenue_expenditure_by_year_jsonl",
    )
    fte_rows = load_jsonl_artifact(
        snapshot_dir / "normalized" / "department-fte-by-year.jsonl",
        checks,
        "department_fte_by_year_jsonl",
    )

    if overview_rows is not None and department_rows is not None and fte_rows is not None:
        row_counts = {
            "overview_by_year": len(overview_rows),
            "department_revenue_expenditure_by_year": len(department_rows),
            "department_fte_by_year": len(fte_rows),
        }
        compare_value(checks, "row_counts", row_counts, summary.get("row_counts"))
        fy2026 = next((row for row in overview_rows if row.get("year") == 2026), None)
        if fy2026:
            compare_value(
                checks,
                "fy2026_revenue_total",
                int(fy2026["budgeted_revenue"]),
                summary["validation_checks"]["fy2026_revenue_total"],
            )
            compare_value(
                checks,
                "fy2026_expenditure_total",
                int(fy2026["budgeted_expenditure"]),
                summary["validation_checks"]["fy2026_expenditure_total"],
            )
            compare_value(
                checks,
                "fy2026_fte_total",
                int(fy2026["budgeted_fte"]),
                summary["validation_checks"]["fy2026_fte_total"],
            )
        else:
            checks.append(failed_check("fy2026_overview_row", message="Missing FY2026 row."))
        compare_value(
            checks,
            "fy2026_department_revenue_total",
            sum(int(row["budgeted_revenue"]) for row in department_rows),
            summary["validation_checks"]["fy2026_department_revenue_total"],
        )
        compare_value(
            checks,
            "fy2026_department_expenditure_total",
            sum(int(row["budgeted_expenditure"]) for row in department_rows),
            summary["validation_checks"]["fy2026_department_expenditure_total"],
        )
        compare_value(
            checks,
            "fy2026_department_fte_total",
            sum(int(row["budgeted_fte"]) for row in fte_rows),
            summary["validation_checks"]["fy2026_department_fte_total"],
        )
    checks.extend(query_template_hash_checks(provenance))
    return validation_result(
        context,
        checks=checks,
        warnings=warnings,
        source_fingerprint=summary.get("source_fingerprint"),
        snapshot_path=str(snapshot_dir),
    )


def validate_washington_operating_budget_snapshot(
    context: SourceContext,
    refresh_check: bool,
) -> dict[str, Any]:
    snapshot_dir = (
        ROOT
        / "jurisdictions"
        / "washington"
        / "data"
        / "operating-budget"
        / context.source_card["snapshot_version"]
    )
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    summary, provenance = load_snapshot_artifacts(snapshot_dir, checks)
    if summary is None or provenance is None:
        return validation_result(
            context,
            status="validation_failed",
            checks=checks,
            warnings=warnings,
            snapshot_path=str(snapshot_dir),
        )
    checks.extend(artifact_fingerprint_checks(summary, provenance))

    normalized_dir = snapshot_dir / "normalized"
    agency_rows = load_jsonl_artifact(normalized_dir / "agency-by-fund-view.jsonl", checks, "agency_jsonl")
    function_rows = load_jsonl_artifact(
        normalized_dir / "functional-area-by-fund-view.jsonl",
        checks,
        "functional_area_jsonl",
    )
    historical_summary_rows = load_jsonl_artifact(
        normalized_dir / "historical-biennium-summary.jsonl",
        checks,
        "historical_summary_jsonl",
    )
    historical_agency_rows = load_jsonl_artifact(
        normalized_dir / "historical-agency-by-biennium.jsonl",
        checks,
        "historical_agency_jsonl",
    )
    historical_function_rows = load_jsonl_artifact(
        normalized_dir / "historical-functional-area-by-biennium.jsonl",
        checks,
        "historical_functional_area_jsonl",
    )
    version_rows = load_jsonl_artifact(
        normalized_dir / "version-summary.jsonl",
        checks,
        "version_summary_jsonl",
    )
    if all(
        rows is not None
        for rows in (
            agency_rows,
            function_rows,
            historical_summary_rows,
            historical_agency_rows,
            historical_function_rows,
            version_rows,
        )
    ):
        row_counts = {
            "agency_by_fund_view": len(agency_rows),
            "functional_area_by_fund_view": len(function_rows),
            "historical_agency_by_biennium": len(historical_agency_rows),
            "historical_biennium_summary": len(historical_summary_rows),
            "historical_functional_area_by_biennium": len(historical_function_rows),
            "version_summary": len(version_rows),
        }
        compare_value(checks, "row_counts", row_counts, summary.get("row_counts"))
        agency_totals = amount_totals_by(agency_rows, "fund_view")
        function_totals = amount_totals_by(function_rows, "fund_view")
        compare_value(
            checks,
            "totals_by_fund_view",
            agency_totals,
            summary["validation_checks"]["totals_by_fund_view"],
        )
        compare_value(
            checks,
            "agency_function_totals_match",
            agency_totals,
            function_totals,
        )
        historical_totals = amount_totals_by(historical_summary_rows, "biennium")
        compare_value(
            checks,
            "historical_totals_by_biennium",
            historical_totals,
            summary["validation_checks"]["historical_totals_by_biennium"],
        )
        compare_value(
            checks,
            "historical_agency_totals_match",
            amount_totals_by(historical_agency_rows, "biennium"),
            historical_totals,
        )
        compare_value(
            checks,
            "historical_functional_area_totals_match",
            amount_totals_by(historical_function_rows, "biennium"),
            historical_totals,
        )
        compare_value(
            checks,
            "historical_current_overlap_total",
            historical_totals.get(context.source_card["biennium"]),
            summary["validation_checks"]["historical_current_overlap_total"],
        )
    checks.extend(query_template_hash_checks(provenance))
    return validation_result(
        context,
        checks=checks,
        warnings=warnings,
        source_fingerprint=summary.get("source_fingerprint"),
        snapshot_path=str(snapshot_dir),
    )


def validate_washington_revenue_snapshot(
    context: SourceContext,
    refresh_check: bool,
) -> dict[str, Any]:
    snapshot_dir = (
        ROOT
        / "jurisdictions"
        / "washington"
        / "data"
        / "revenue-by-biennium"
        / context.source_card["snapshot_version"]
    )
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    summary, provenance = load_snapshot_artifacts(snapshot_dir, checks)
    if summary is None or provenance is None:
        return validation_result(
            context,
            status="validation_failed",
            checks=checks,
            warnings=warnings,
            snapshot_path=str(snapshot_dir),
        )
    checks.extend(artifact_fingerprint_checks(summary, provenance))
    statewide_rows = load_jsonl_artifact(
        snapshot_dir / "normalized" / "general-fund-revenue-by-biennium.jsonl",
        checks,
        "statewide_revenue_jsonl",
    )
    detail_rows = load_jsonl_artifact(
        snapshot_dir / "normalized" / "general-fund-revenue-by-area-account.jsonl",
        checks,
        "detail_revenue_jsonl",
    )
    status = "valid"
    if statewide_rows is not None and detail_rows is not None:
        row_counts = {
            "general_fund_revenue_by_area_account": len(detail_rows),
            "general_fund_revenue_by_biennium": len(statewide_rows),
        }
        compare_value(checks, "row_counts", row_counts, summary.get("row_counts"))
        statewide_totals = {
            row["biennium"]: {
                "actual_minus_estimate": row["actual_minus_estimate"],
                "actual_revenue": row["actual_revenue"],
                "estimated_revenue": row["estimated_revenue"],
            }
            for row in statewide_rows
        }
        compare_value(
            checks,
            "totals_by_biennium",
            statewide_totals,
            summary["validation_checks"]["totals_by_biennium"],
        )
        detail_totals = revenue_detail_totals(detail_rows)
        compare_value(
            checks,
            "detail_totals_by_biennium",
            detail_totals,
            summary["validation_checks"]["detail_totals_by_biennium"],
        )
        current = next(
            row for row in statewide_rows if row["biennium"] == context.source_card["current_biennium"]
        )
        compare_value(
            checks,
            "current_biennium_actual_data_status",
            current["actual_data_status"],
            summary["validation_checks"]["current_biennium_actual_data_status"],
        )
        if current["actual_data_status"] == "partial":
            status = "partial_current_period"
    checks.extend(export_metadata_checks(provenance))
    return validation_result(
        context,
        status=status if not any(check.get("status") == "failed" for check in checks) else None,
        checks=checks,
        warnings=warnings,
        source_fingerprint=summary.get("source_fingerprint"),
        snapshot_path=str(snapshot_dir),
        data_through=summary.get("actual_data_through"),
    )


def validate_washington_fit_snapshot(
    context: SourceContext,
    refresh_check: bool,
) -> dict[str, Any]:
    snapshot_dir = (
        ROOT
        / "jurisdictions"
        / "washington"
        / "data"
        / "fit-filed-actuals"
        / context.source_card["snapshot_version"]
    )
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    summary, provenance = load_snapshot_artifacts(snapshot_dir, checks)
    if summary is None or provenance is None:
        return validation_result(
            context,
            status="validation_failed",
            checks=checks,
            warnings=warnings,
            snapshot_path=str(snapshot_dir),
        )
    checks.extend(artifact_fingerprint_checks(summary, provenance))

    expected = context.source_card["validation_checks"]
    governments = load_jsonl_artifact(
        snapshot_dir / "normalized" / "government-annual-totals.jsonl",
        checks,
        "government_annual_totals_jsonl",
    )
    schools = load_jsonl_artifact(
        snapshot_dir / "normalized" / "school-district-annual-totals.jsonl",
        checks,
        "school_district_annual_totals_jsonl",
    )
    if governments is not None and schools is not None:
        compare_value(
            checks,
            "government_annual_totals_rows",
            len(governments),
            expected["government_annual_totals_rows"],
        )
        compare_value(
            checks,
            "school_district_annual_totals_rows",
            len(schools),
            expected["school_district_annual_totals_rows"],
        )

        def total(rows: list[dict[str, Any]], government: str, year: int, measure: str):
            year_field = (
                "school_fiscal_year_ending_aug31"
                if rows is schools
                else "year"
            )
            for row in rows:
                if row["government"] == government and row[year_field] == year:
                    return row[measure]
            return None

        compare_value(
            checks,
            "spokane_2024_revenues",
            total(governments, "City of Spokane", 2024, "total_revenues"),
            expected["spokane_2024_revenues"],
        )
        compare_value(
            checks,
            "spokane_2024_expenditures",
            total(governments, "City of Spokane", 2024, "total_expenditures"),
            expected["spokane_2024_expenditures"],
        )
        compare_value(
            checks,
            "sound_transit_2024_revenues",
            total(governments, "Sound Transit", 2024, "total_revenues"),
            expected["sound_transit_2024_revenues"],
        )
        compare_value(
            checks,
            "kcrha_2024_expenditures",
            total(
                governments,
                "King County Regional Homelessness Authority",
                2024,
                "total_expenditures",
            ),
            expected["kcrha_2024_expenditures"],
        )
        compare_value(
            checks,
            "seattle_sd_2025_revenues",
            total(schools, "Seattle School District No. 1", 2025, "total_revenues"),
            expected["seattle_sd_2025_revenues"],
        )

        claimed = {
            entry["jurisdiction_name"]
            for entry in context.source_card.get("coverage_jurisdictions", [])
        }
        snapshot_governments = {row["government"] for row in governments} | {
            row["government"] for row in schools
        }
        compare_value(
            checks,
            "claimed_jurisdictions_present_in_snapshot",
            sorted(claimed - snapshot_governments),
            [],
        )

    return validation_result(
        context,
        status=status_from_checks(checks),
        checks=checks,
        warnings=warnings,
        snapshot_path=str(snapshot_dir),
    )


def validate_washington_ofm_population_snapshot(
    context: SourceContext,
    refresh_check: bool,
) -> dict[str, Any]:
    snapshot_dir = (
        ROOT
        / "jurisdictions"
        / "washington"
        / "data"
        / "ofm-population"
        / context.source_card["snapshot_version"]
    )
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    summary, provenance = load_snapshot_artifacts(snapshot_dir, checks)
    if summary is None or provenance is None:
        return validation_result(
            context,
            status="validation_failed",
            checks=checks,
            warnings=warnings,
            snapshot_path=str(snapshot_dir),
        )
    checks.extend(artifact_fingerprint_checks(summary, provenance))
    rows = load_jsonl_artifact(
        snapshot_dir / "normalized" / "population-estimates.jsonl",
        checks,
        "population_estimates_jsonl",
    )
    if rows is not None:
        row_counts = {
            "population_estimates": len(rows),
            "geography_rows": len(
                {
                    (
                        row["source_line"],
                        row["row_type"],
                        row["county"],
                        row["jurisdiction"],
                    )
                    for row in rows
                }
            ),
            "county_rows": count_population_rows(rows, "county"),
            "unincorporated_county_rows": count_population_rows(
                rows,
                "unincorporated_county",
            ),
            "incorporated_county_rows": count_population_rows(
                rows,
                "incorporated_county",
            ),
            "city_town_rows": count_population_rows(rows, "city_town"),
            "state_total_rows": count_population_rows(rows, "state_total"),
            "separator_rows": summary["row_counts"].get("separator_rows"),
        }
        compare_value(checks, "row_counts", row_counts, summary.get("row_counts"))
        latest_rows = [
            row
            for row in rows
            if row.get("value_kind") == "estimate"
            and row.get("estimate_date") == context.source_card["latest_estimate_date"]
        ]
        compare_value(
            checks,
            "latest_estimate_row_count",
            len(latest_rows),
            summary["row_counts"]["geography_rows"],
        )
        compare_value(
            checks,
            "seattle_2025_population",
            population_for(rows, "Seattle", "city_town", 2025),
            summary["validation_checks"]["seattle_2025_population"],
        )
        compare_value(
            checks,
            "king_county_2025_population",
            population_for(rows, "King County", "county", 2025),
            summary["validation_checks"]["king_county_2025_population"],
        )
        compare_value(
            checks,
            "state_total_2025_population",
            population_for(rows, "State Total", "state_total", 2025),
            summary["validation_checks"]["state_total_2025_population"],
        )
        king_city_town_sum = sum(
            int(row["population"])
            for row in rows
            if row.get("county") == "King"
            and row.get("row_type") == "city_town"
            and row.get("year") == 2025
        )
        compare_value(
            checks,
            "king_county_city_town_sum_2025",
            king_city_town_sum,
            summary["validation_checks"]["king_county_city_town_sum_2025"],
        )
        king_unincorporated = population_for(
            rows,
            "Unincorporated King County",
            "unincorporated_county",
            2025,
        )
        king_incorporated = population_for(
            rows,
            "Incorporated King County",
            "incorporated_county",
            2025,
        )
        king_county = population_for(rows, "King County", "county", 2025)
        compare_value(
            checks,
            "king_county_total_reconciles",
            king_unincorporated + king_incorporated,
            king_county,
        )
    return validation_result(
        context,
        checks=checks,
        warnings=warnings,
        source_fingerprint=summary.get("source_fingerprint"),
        snapshot_path=str(snapshot_dir),
    )


def validate_washington_open_checkbook(
    context: SourceContext,
    refresh_check: bool,
) -> dict[str, Any]:
    checks = source_fingerprint_contract_checks(context.source_card)
    refresh_checks, warnings = refresh_check_placeholder(refresh_check)
    checks.extend(refresh_checks)
    status = status_source(context)
    if status.get("status") == "missing":
        checks.append(
            failed_check(
                "local_manifest_and_database_present",
                evidence={"manifest_path": str(context.manifest_path)},
                message=status.get("message", "Local Open Checkbook cache is missing."),
            )
        )
        return validation_result(
            context,
            status="missing",
            checks=checks,
            warnings=warnings,
            manifest_path=str(context.manifest_path),
            message=status.get("message"),
        )
    manifest = status
    if manifest.get("status") == "stale":
        checks.append(
            failed_check(
                "source_file_metadata_current",
                message=manifest.get("message", "Local manifest is stale."),
            )
        )
    else:
        checks.append(passed_check("source_file_metadata_current"))
    checks.extend(manifest_fingerprint_checks(manifest))
    db_path = Path(manifest.get("database_path", ""))
    if not db_path.is_file():
        checks.append(
            failed_check(
                "local_database_present",
                evidence={"database_path": str(db_path)},
                message="Manifest exists but local database is missing.",
            )
        )
        return validation_result(
            context,
            status="missing",
            checks=checks,
            warnings=warnings,
            manifest_path=str(context.manifest_path),
            database_path=str(db_path),
        )
    checks.extend(sqlite_checkbook_checks(context.source_card, manifest, db_path))
    result_status = "stale" if manifest.get("status") == "stale" else manifest.get("status", "valid")
    if result_status == "current":
        result_status = "valid"
    if any(check.get("status") == "failed" for check in checks) and result_status not in {
        "stale",
    }:
        result_status = "validation_failed"
    return validation_result(
        context,
        status=result_status,
        checks=checks,
        warnings=warnings,
        source_fingerprint=manifest.get("source_fingerprint", context.source_card.get("source_fingerprint")),
        manifest_path=str(context.manifest_path),
        database_path=str(db_path),
        data_through=manifest.get("data_through"),
        row_count=manifest.get("row_count"),
    )


def load_snapshot_artifacts(
    snapshot_dir: Path,
    checks: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    summary = load_json_artifact(snapshot_dir / "summary.json", checks, "summary_json")
    provenance = load_json_artifact(
        snapshot_dir / "provenance.json",
        checks,
        "provenance_json",
    )
    return summary, provenance


def load_json_artifact(
    path: Path,
    checks: list[dict[str, Any]],
    check_name: str,
) -> dict[str, Any] | None:
    if not path.is_file():
        checks.append(
            failed_check(
                check_name,
                evidence={"path": path.relative_to(ROOT).as_posix()},
                message="Required JSON artifact is missing.",
            )
        )
        return None
    try:
        data = read_json(path)
    except json.JSONDecodeError as exc:
        checks.append(
            failed_check(
                check_name,
                evidence={"path": path.relative_to(ROOT).as_posix()},
                message=f"JSON artifact is malformed: {exc}",
            )
        )
        return None
    checks.append(
        passed_check(
            check_name,
            evidence={"path": path.relative_to(ROOT).as_posix()},
        )
    )
    return data


def load_jsonl_artifact(
    path: Path,
    checks: list[dict[str, Any]],
    check_name: str,
) -> list[dict[str, Any]] | None:
    if not path.is_file():
        checks.append(
            failed_check(
                check_name,
                evidence={"path": path.relative_to(ROOT).as_posix()},
                message="Required JSONL artifact is missing.",
            )
        )
        return None
    rows = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                rows.append(json.loads(line))
    except json.JSONDecodeError as exc:
        checks.append(
            failed_check(
                check_name,
                evidence={
                    "path": path.relative_to(ROOT).as_posix(),
                    "line": line_number,
                },
                message=f"JSONL artifact is malformed: {exc}",
            )
        )
        return None
    checks.append(
        passed_check(
            check_name,
            evidence={"path": path.relative_to(ROOT).as_posix(), "rows": len(rows)},
        )
    )
    return rows


def artifact_fingerprint_checks(
    summary: dict[str, Any],
    provenance: dict[str, Any],
) -> list[dict[str, Any]]:
    checks = []
    for label, artifact in (("summary", summary), ("provenance", provenance)):
        fingerprint = artifact.get("source_fingerprint")
        if not isinstance(fingerprint, dict):
            checks.append(
                failed_check(
                    f"{label}_source_fingerprint",
                    message=f"{label}.json is missing source_fingerprint.",
                )
            )
            continue
        checks.append(passed_check(f"{label}_source_fingerprint"))
        compare_value(
            checks,
            f"{label}_fingerprint_row_counts",
            fingerprint.get("row_counts"),
            summary.get("row_counts"),
        )
    return checks


def manifest_fingerprint_checks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    fingerprint = manifest.get("source_fingerprint")
    if not isinstance(fingerprint, dict):
        return [
            failed_check(
                "manifest_source_fingerprint",
                message="Managed local manifest is missing source_fingerprint.",
            )
        ]
    checks = [passed_check("manifest_source_fingerprint")]
    compare_value(
        checks,
        "manifest_fingerprint_payment_rows",
        fingerprint.get("row_counts", {}).get("payments"),
        manifest.get("row_count"),
    )
    return checks


def compare_value(
    checks: list[dict[str, Any]],
    name: str,
    observed: Any,
    expected: Any,
) -> None:
    evidence = {"observed": json_safe(observed), "expected": json_safe(expected)}
    if observed == expected:
        checks.append(passed_check(name, evidence=evidence))
    else:
        checks.append(
            failed_check(
                name,
                evidence=evidence,
                message="Observed value does not match expected value.",
            )
        )


def json_safe(value: Any) -> Any:
    if isinstance(value, set):
        return sorted(value)
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def query_template_hash_checks(provenance: dict[str, Any]) -> list[dict[str, Any]]:
    checks = []
    for name, info in provenance.get("query_templates", {}).items():
        template_path = ROOT / info["template_path"]
        if not template_path.is_file():
            checks.append(
                failed_check(
                    f"query_template_{name}",
                    evidence={"template_path": info["template_path"]},
                    message="Query template is missing.",
                )
            )
            continue
        observed = sha256_json(read_json(template_path))
        expected = info.get("template_sha256")
        compare_value(checks, f"query_template_hash_{name}", observed, expected)
    return checks


def export_metadata_checks(provenance: dict[str, Any]) -> list[dict[str, Any]]:
    checks = []
    exports = provenance.get("exports", {})
    if not exports:
        return [failed_check("reportviewer_exports", message="No export metadata found.")]
    for biennium, metadata in exports.items():
        missing = [
            field
            for field in ("csv_row_count", "csv_sha256", "xlsx_sha256", "xml_sha256")
            if field not in metadata
        ]
        if missing:
            checks.append(
                failed_check(
                    f"reportviewer_export_{biennium}",
                    evidence={"missing": missing},
                    message="Export metadata is incomplete.",
                )
            )
        else:
            checks.append(
                passed_check(
                    f"reportviewer_export_{biennium}",
                    evidence={
                        "csv_row_count": metadata["csv_row_count"],
                        "hashes": ["csv_sha256", "xlsx_sha256", "xml_sha256"],
                    },
                )
            )
    return checks


def sqlite_checkbook_checks(
    source_card: dict[str, Any],
    manifest: dict[str, Any],
    db_path: Path,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    required_tables = {"payments", "source_files", "refresh_runs"}
    required_indexes = {
        "idx_payments_biennium",
        "idx_payments_period",
        "idx_payments_month",
        "idx_payments_agency",
        "idx_payments_category",
        "idx_payments_vendor",
    }
    with closing(sqlite3.connect(db_path)) as conn:
        table_rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
        tables = {row[0] for row in table_rows}
        compare_value(checks, "local_database_required_tables", tables & required_tables, required_tables)
        if not required_tables.issubset(tables):
            return checks
        index_rows = conn.execute("PRAGMA index_list(payments)").fetchall()
        indexes = {row[1] for row in index_rows}
        compare_value(
            checks,
            "local_database_required_indexes",
            indexes & required_indexes,
            required_indexes,
        )
        payment_count = int(conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0])
        source_file_count = int(conn.execute("SELECT COUNT(*) FROM source_files").fetchone()[0])
        compare_value(checks, "local_database_payment_rows", payment_count, manifest.get("row_count"))
        compare_value(
            checks,
            "local_database_source_file_rows",
            source_file_count,
            len(manifest.get("source_files", [])),
        )
        current_biennium = manifest.get("current_biennium") or source_card.get("current_biennium")
        current_data_through = conn.execute(
            "SELECT MAX(calendar_month) FROM payments WHERE biennium = ?",
            (current_biennium,),
        ).fetchone()[0]
        compare_value(
            checks,
            "local_database_data_through",
            current_data_through,
            manifest.get("data_through"),
        )
        category_count = int(
            conn.execute(
                "SELECT COUNT(DISTINCT category) FROM payments WHERE biennium = ?",
                (current_biennium,),
            ).fetchone()[0]
        )
        checks.append(
            passed_check(
                "local_database_category_aggregate",
                evidence={"current_biennium": current_biennium, "category_count": category_count},
            )
        )
    return checks


def amount_totals_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    totals: dict[str, int] = {}
    for row in rows:
        totals[row[key]] = totals.get(row[key], 0) + int(row["budgeted_amount"])
    return dict(sorted(totals.items()))


def revenue_detail_totals(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    totals: dict[str, dict[str, float]] = {}
    for row in rows:
        bucket = totals.setdefault(
            row["biennium"],
            {
                "actual_minus_estimate": 0,
                "actual_revenue": 0,
                "estimated_revenue": 0,
            },
        )
        for key in bucket:
            bucket[key] += row[key]
    return {
        biennium: {
            key: int(value) if float(value).is_integer() else round(value, 2)
            for key, value in values.items()
        }
        for biennium, values in sorted(totals.items())
    }


def count_population_rows(rows: list[dict[str, Any]], row_type: str) -> int:
    return len(
        {
            row["source_line"]
            for row in rows
            if row.get("row_type") == row_type and row.get("year") == 2025
        }
    )


def population_for(
    rows: list[dict[str, Any]],
    jurisdiction: str,
    row_type: str,
    year: int,
) -> int:
    for row in rows:
        if (
            row.get("jurisdiction") == jurisdiction
            and row.get("row_type") == row_type
            and row.get("year") == year
        ):
            return int(row["population"])
    raise SourceDataError(f"Missing population row: {jurisdiction} {row_type} {year}")


def sha256_json(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def parse_params(raw_params: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for raw_param in raw_params:
        if "=" not in raw_param:
            raise SourceDataError(f"Invalid --param value, expected key=value: {raw_param}")
        key, value = raw_param.split("=", 1)
        if not key:
            raise SourceDataError(f"Invalid --param value, empty key: {raw_param}")
        params[key] = value
    return params


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def print_human(result: dict[str, Any]) -> None:
    source_id = result.get("source_id", "-")
    status = result.get("status") or ("ok" if result.get("ok") else "error")
    print(f"{source_id}: {status}")
    for key in (
        "message",
        "storage_tier",
        "normal_answer_source",
        "data_through",
        "row_count",
        "manifest_path",
    ):
        if key in result and result[key] is not None:
            print(f"{key}: {result[key]}")


if __name__ == "__main__":
    main()
