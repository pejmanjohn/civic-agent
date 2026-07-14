#!/usr/bin/env python3
"""WA-20 Tier 1 answer scorer (mechanical checks + human worksheet).

Implements the semi-automated scorer specced in
docs/processes/civic-agent-improvement-loop.md: it never scores civic
usefulness itself - it mechanically checks saved answers and produces a
worksheet so the only human judgment left is `civic_usefulness` on the five
anchor cases.

Workflow:

1. `python3 scripts/eval.py --init [--label pre-fit]`
     Creates benchmarks/wa-citizen/runs/YYYY-MM-DD[-label]/ with one prompt
     file per case, one answer template per case, and run-metadata.json
     recording commit and package state (eval-validity requirements).
     Capture answers by running each case's plugin_prompt in a FRESH agent
     session and pasting the full answer below the template's front matter.

2. `python3 scripts/eval.py --score RUN_DIR`
     Mechanically checks every captured answer: declared answer mode vs
     expected, expected source ids present, required caveat patterns match,
     expected numeric facts found within tolerance. Writes results.json and
     worksheet.md into the run dir. Never prints a composite mean.

3. `python3 scripts/eval.py --compare RUN_A RUN_B`
     Per-case, per-check agreement between two runs. Two same-config runs
     establish the noise floor; the observed flip count is the significance
     threshold for any later improvement claim.

Numeric fact matching: all dollar/number tokens in the answer (including
"$150.4 billion" style) are parsed to absolute values; a fact passes when any
parsed value falls within max(tolerance, 0.05% of expected) - the relative
floor accepts honest rounding in prose while still failing wrong numbers.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "wa-citizen" / "cases.json"
RUNS_ROOT = ROOT / "benchmarks" / "wa-citizen" / "runs"

RELATIVE_TOLERANCE_FLOOR = 0.0005  # 0.05% of expected value

MAGNITUDES = {
    "k": 1e3,
    "thousand": 1e3,
    "m": 1e6,
    "million": 1e6,
    "b": 1e9,
    "billion": 1e9,
    "t": 1e12,
    "trillion": 1e12,
}
NUMBER_PATTERN = re.compile(
    r"\$?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(k|m|b|t|thousand|million|billion|trillion)?\b",
    re.IGNORECASE,
)
FRONT_MATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WA-20 Tier 1 answer scorer.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", action="store_true", help="Create a new run directory.")
    group.add_argument("--score", metavar="RUN_DIR", help="Score a captured run directory.")
    group.add_argument(
        "--compare",
        nargs=2,
        metavar=("RUN_A", "RUN_B"),
        help="Compare two scored runs (noise floor / before-after).",
    )
    parser.add_argument("--label", help="Optional suffix for --init run directory name.")
    parser.add_argument(
        "--date",
        help="Override run date for --init (YYYY-MM-DD; defaults to today).",
    )
    return parser.parse_args()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_cases() -> list[dict]:
    with CASES_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def git_value(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


# --- number extraction -------------------------------------------------------

def extract_numbers(text: str) -> list[float]:
    values = []
    for match in NUMBER_PATTERN.finditer(text):
        raw, magnitude = match.groups()
        try:
            value = float(raw.replace(",", ""))
        except ValueError:
            continue
        if magnitude:
            value *= MAGNITUDES[magnitude.lower()]
        values.append(value)
    return values


def fact_matches(fact: dict, numbers: list[float]) -> bool:
    expected = float(fact["value"])
    tolerance = max(float(fact["tolerance"]), abs(expected) * RELATIVE_TOLERANCE_FLOOR)
    return any(abs(value - expected) <= tolerance for value in numbers)


# --- answer files ------------------------------------------------------------

def parse_answer_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_PATTERN.match(text)
    meta = {}
    body = text
    if match:
        body = text[match.end():]
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip()
    return {"meta": meta, "body": body.strip()}


def answer_is_captured(parsed: dict) -> bool:
    body = parsed["body"]
    return bool(body) and "PASTE THE FULL ANSWER" not in body


# --- init --------------------------------------------------------------------

def init_run(label: str | None, date: str | None) -> None:
    run_date = date or dt.date.today().isoformat()
    run_name = f"{run_date}-{label}" if label else run_date
    run_dir = RUNS_ROOT / run_name
    if run_dir.exists():
        raise SystemExit(f"Run directory already exists: {run_dir}")
    run_dir.mkdir(parents=True)

    cases = load_cases()
    for case in cases:
        (run_dir / f"{case['id']}.prompt.txt").write_text(
            case["plugin_prompt"] + "\n", encoding="utf-8"
        )
        (run_dir / f"{case['id']}.md").write_text(
            "---\n"
            f"case: {case['id']}\n"
            "surface: plugin\n"
            "answer_mode: <exact|partial|side_by_side_only|unsupported_with_path|needs_refresh>\n"
            "session: fresh\n"
            "---\n\n"
            "PASTE THE FULL ANSWER (Conclusion / Numbers / How to read this / Trace) HERE.\n",
            encoding="utf-8",
        )

    metadata = {
        "run": run_name,
        "created": run_date,
        "commit": git_value(["rev-parse", "HEAD"]),
        "branch": git_value(["rev-parse", "--abbrev-ref", "HEAD"]),
        "dirty": bool(git_value(["status", "--porcelain"])),
        "cases": len(cases),
        "capture_protocol": (
            "Run each .prompt.txt in a FRESH agent session with the dev plugin "
            "installed (python3 scripts/dev.py status first); paste the full "
            "answer into the matching .md below its front matter and set "
            "answer_mode to the mode the answer actually claims. Do not edit "
            "answers. Score with: python3 scripts/eval.py --score <run_dir>"
        ),
    }
    (run_dir / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Initialized {display_path(run_dir)} with {len(cases)} cases.")


# --- score -------------------------------------------------------------------

def score_case(case: dict, parsed: dict) -> dict:
    body = parsed["body"]
    lowered = body.lower()
    checks = []

    declared_mode = parsed["meta"].get("answer_mode", "").strip()
    checks.append(
        {
            "check": "answer_mode",
            "passed": declared_mode == case["expected_answer_mode"],
            "expected": case["expected_answer_mode"],
            "actual": declared_mode or "<undeclared>",
        }
    )

    for source_id in case["expected_source_ids"]:
        checks.append(
            {
                "check": f"source:{source_id}",
                "passed": source_id.lower() in lowered,
                "expected": "cited",
                "actual": "present" if source_id.lower() in lowered else "absent",
            }
        )

    for caveat in case["required_caveats"]:
        matched = re.search(caveat["pattern"], body, re.IGNORECASE) is not None
        checks.append(
            {
                "check": f"caveat:{caveat['id']}",
                "passed": matched,
                "expected": caveat["description"],
                "actual": "matched" if matched else "not found",
            }
        )

    numbers = extract_numbers(body)
    for fact in case["expected_facts"]:
        matched = fact_matches(fact, numbers)
        checks.append(
            {
                "check": f"fact:{fact['id']}",
                "passed": matched,
                "expected": fact["value"],
                "actual": "found within tolerance" if matched else "not found",
            }
        )

    return {
        "case": case["id"],
        "anchor": case.get("anchor", False),
        "captured": True,
        "checks": checks,
        "passed": sum(1 for check in checks if check["passed"]),
        "total": len(checks),
    }


def score_run(run_dir_arg: str) -> None:
    run_dir = Path(run_dir_arg)
    if not run_dir.is_absolute():
        run_dir = ROOT / run_dir
    if not run_dir.is_dir():
        raise SystemExit(f"Run directory not found: {run_dir}")

    cases = load_cases()
    results = []
    for case in cases:
        answer_path = run_dir / f"{case['id']}.md"
        if not answer_path.is_file():
            results.append(
                {"case": case["id"], "anchor": case.get("anchor", False),
                 "captured": False, "checks": [], "passed": 0, "total": 0}
            )
            continue
        parsed = parse_answer_file(answer_path)
        if not answer_is_captured(parsed):
            results.append(
                {"case": case["id"], "anchor": case.get("anchor", False),
                 "captured": False, "checks": [], "passed": 0, "total": 0}
            )
            continue
        results.append(score_case(case, parsed))

    captured = [r for r in results if r["captured"]]
    fully_passing = [r for r in captured if r["passed"] == r["total"]]
    payload = {
        "run": run_dir.name,
        "scorer": "mechanical",
        "captured_cases": len(captured),
        "total_cases": len(results),
        "fully_passing_cases": len(fully_passing),
        "results": results,
    }
    (run_dir / "results.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (run_dir / "worksheet.md").write_text(render_worksheet(payload), encoding="utf-8")

    print(
        f"Scored {len(captured)}/{len(results)} captured cases; "
        f"{len(fully_passing)} pass all mechanical checks. "
        f"Wrote results.json and worksheet.md to {display_path(run_dir)}."
    )
    for result in captured:
        failures = [c for c in result["checks"] if not c["passed"]]
        if failures:
            print(f"- {result['case']}: {len(failures)} failing "
                  f"({', '.join(c['check'] for c in failures)})")


def render_worksheet(payload: dict) -> str:
    lines = [
        f"# Tier 1 Worksheet - {payload['run']}",
        "",
        "Mechanical results are in results.json. Human judgment is ONLY "
        "`civic_usefulness` (0-5 per docs/goals/eval-scoring-rubric.md) on the "
        "anchor cases below - author-scored, unblinded, and labeled as such. "
        "Do not re-score mechanical dimensions by hand.",
        "",
        "| Anchor case | Mechanical | civic_usefulness (0-5) | Notes |",
        "|---|---|---|---|",
    ]
    for result in payload["results"]:
        if not result["anchor"]:
            continue
        mechanical = (
            f"{result['passed']}/{result['total']}" if result["captured"] else "NOT CAPTURED"
        )
        lines.append(f"| `{result['case']}` | {mechanical} |  |  |")
    lines.extend(
        [
            "",
            "Per-case mechanical failures (fix the capture or record as findings):",
            "",
        ]
    )
    any_failures = False
    for result in payload["results"]:
        failures = [c for c in result["checks"] if not c["passed"]]
        if result["captured"] and failures:
            any_failures = True
            for check in failures:
                lines.append(
                    f"- `{result['case']}` / {check['check']}: expected "
                    f"{check['expected']!r}, got {check['actual']!r}"
                )
    if not any_failures:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


# --- compare -----------------------------------------------------------------

def compare_runs(run_a: str, run_b: str) -> None:
    payloads = []
    for arg in (run_a, run_b):
        path = Path(arg)
        if not path.is_absolute():
            path = ROOT / arg
        results_path = path / "results.json"
        if not results_path.is_file():
            raise SystemExit(f"Missing results.json in {path}; run --score first.")
        payloads.append(json.loads(results_path.read_text(encoding="utf-8")))

    by_case_a = {r["case"]: r for r in payloads[0]["results"]}
    by_case_b = {r["case"]: r for r in payloads[1]["results"]}
    flips = []
    for case_id in sorted(set(by_case_a) & set(by_case_b)):
        a, b = by_case_a[case_id], by_case_b[case_id]
        if not (a["captured"] and b["captured"]):
            continue
        a_pass = a["passed"] == a["total"]
        b_pass = b["passed"] == b["total"]
        if a_pass != b_pass:
            flips.append(
                f"{case_id}: {'pass' if a_pass else 'fail'} -> {'pass' if b_pass else 'fail'}"
            )
        else:
            checks_a = {c["check"]: c["passed"] for c in a["checks"]}
            checks_b = {c["check"]: c["passed"] for c in b["checks"]}
            for check in sorted(set(checks_a) & set(checks_b)):
                if checks_a[check] != checks_b[check]:
                    flips.append(f"{case_id} / {check}: {checks_a[check]} -> {checks_b[check]}")

    print(f"Comparing {payloads[0]['run']} -> {payloads[1]['run']}")
    print(f"Case/check flips: {len(flips)}")
    for flip in flips:
        print(f"- {flip}")
    print(
        "\nIf these runs used the same config, this flip count IS the noise "
        "floor: later improvement claims must exceed it."
    )


def main() -> None:
    args = parse_args()
    if args.init:
        init_run(args.label, args.date)
    elif args.score:
        score_run(args.score)
    else:
        compare_runs(*args.compare)


if __name__ == "__main__":
    main()
