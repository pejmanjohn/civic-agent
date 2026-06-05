#!/usr/bin/env python3
"""Managed local data helpers for Civic Agent sources."""

from __future__ import annotations

import argparse
import json
import os
import sys
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

BUILDER_REGISTRY: dict[str, Builder] = {}
QUERY_REGISTRY: dict[str, QueryRunner] = {}


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
    try:
        result = builder(context, force)
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
