import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "scale" / "cases.json"
SOURCE_ROOT = ROOT / "jurisdictions"

REQUIRED_FIELDS = {
    "id",
    "bucket",
    "question",
    "recipe",
    "jurisdictions",
    "plugin_prompt",
    "web_prompt",
    "expected_source_ids",
    "expected_missing_sources",
    "expected_answer_mode",
    "expected_failure_mode",
    "required_caveats",
    "score_dimensions",
    "improvement_path",
}
EXPECTED_CASE_IDS = {
    "scale.seattle.current_operating_total",
    "scale.king_county.current_budget_size",
    "scale.seattle_king_county.trend",
    "scale.seattle_king_county.per_resident",
}
EXPECTED_SCORE_DIMENSIONS = [
    "correctness",
    "traceability",
    "coverage_awareness",
    "comparability",
    "civic_usefulness",
    "freshness",
    "improvement_path",
]
ALLOWED_ANSWER_MODES = {
    "exact",
    "partial",
    "side_by_side_only",
    "unsupported_with_path",
    "needs_refresh",
}
ALLOWED_FAILURE_MODES = {
    "none",
    "missing_source",
    "missing_denominator",
    "semantic_mismatch",
    "missing_recipe",
    "weak_trace",
    "freshness_unclear",
    "unsupported_question",
    "packaging_or_install_drift",
    "validation_gap",
    "scorer_gap",
}


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_source_ids():
    source_ids = set()
    for path in SOURCE_ROOT.glob("*/sources/*.source.json"):
        source_ids.add(load_json(path)["id"])
    return source_ids


def load_cases():
    return load_json(CASES_PATH)


def validate_case(case, source_ids):
    missing = REQUIRED_FIELDS.difference(case)
    if missing:
        raise AssertionError(f"{case.get('id', '<missing id>')} missing fields: {sorted(missing)}")

    for field in (
        "id",
        "bucket",
        "question",
        "recipe",
        "plugin_prompt",
        "web_prompt",
        "expected_answer_mode",
        "expected_failure_mode",
        "improvement_path",
    ):
        value = case[field]
        if not isinstance(value, str) or not value.strip():
            raise AssertionError(f"{case['id']} has invalid {field}: {value!r}")

    for field in (
        "jurisdictions",
        "expected_source_ids",
        "expected_missing_sources",
        "required_caveats",
        "score_dimensions",
    ):
        if not isinstance(case[field], list):
            raise AssertionError(f"{case['id']} {field} must be a list")

    if case["score_dimensions"] != EXPECTED_SCORE_DIMENSIONS:
        raise AssertionError(f"{case['id']} has unexpected score dimensions")
    if case["expected_answer_mode"] not in ALLOWED_ANSWER_MODES:
        raise AssertionError(f"{case['id']} has unknown answer mode")
    if case["expected_failure_mode"] not in ALLOWED_FAILURE_MODES:
        raise AssertionError(f"{case['id']} has unknown failure mode")
    if not case["required_caveats"]:
        raise AssertionError(f"{case['id']} must declare required caveats")
    for source_id in case["expected_source_ids"]:
        if source_id not in source_ids:
            raise AssertionError(f"{case['id']} references unknown source id: {source_id}")


def validate_cases(cases, source_ids):
    ids = [case.get("id") for case in cases]
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicates:
        raise AssertionError(f"duplicate benchmark case ids: {duplicates}")
    for case in cases:
        validate_case(case, source_ids)


class BenchmarkContractTest(unittest.TestCase):
    def test_scale_benchmark_declares_expected_seed_cases(self):
        cases = load_cases()
        self.assertEqual({case["id"] for case in cases}, EXPECTED_CASE_IDS)

    def test_scale_benchmark_cases_follow_contract(self):
        validate_cases(load_cases(), load_source_ids())

    def test_each_case_uses_standard_score_dimensions(self):
        for case in load_cases():
            self.assertEqual(case["score_dimensions"], EXPECTED_SCORE_DIMENSIONS)

    def test_expected_source_ids_resolve_to_checked_in_source_cards(self):
        source_ids = load_source_ids()
        for case in load_cases():
            for source_id in case["expected_source_ids"]:
                self.assertIn(source_id, source_ids, case["id"])

    def test_contract_validation_rejects_missing_required_caveats(self):
        case = dict(load_cases()[0])
        case["required_caveats"] = []
        with self.assertRaisesRegex(AssertionError, "required caveats"):
            validate_case(case, load_source_ids())

    def test_contract_validation_rejects_missing_failure_mode(self):
        case = dict(load_cases()[0])
        del case["expected_failure_mode"]
        with self.assertRaisesRegex(AssertionError, "missing fields"):
            validate_case(case, load_source_ids())

    def test_contract_validation_rejects_duplicate_case_ids(self):
        cases = load_cases()
        duplicate = dict(cases[0])
        cases.append(duplicate)
        with self.assertRaisesRegex(AssertionError, "duplicate benchmark case ids"):
            validate_cases(cases, load_source_ids())


if __name__ == "__main__":
    unittest.main()
