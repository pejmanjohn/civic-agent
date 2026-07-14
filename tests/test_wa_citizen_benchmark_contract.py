import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "wa-citizen" / "cases.json"
EXPECTATION_LOG_PATH = ROOT / "benchmarks" / "wa-citizen" / "expectation-log.md"
TAXONOMY_PATH = ROOT / "docs" / "coverage-taxonomy.md"
SOURCE_ROOT = ROOT / "jurisdictions"

EXPECTED_CASE_COUNT = 20
EXPECTED_ANCHOR_COUNT = 5

REQUIRED_FIELDS = {
    "id",
    "bucket",
    "question",
    "paraphrases",
    "persona",
    "altitude",
    "jurisdiction",
    "archetype",
    "difficulty",
    "anchor",
    "plugin_prompt",
    "web_prompt",
    "required_claims",
    "mode_ceiling",
    "expected_answer_mode",
    "expected_failure_mode",
    "expected_source_ids",
    "expected_missing_sources",
    "expected_facts",
    "required_caveats",
    "unlocked_by",
    "improvement_path",
    "score_dimensions",
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
ALLOWED_ALTITUDES = {
    "state",
    "county",
    "city",
    "school_district",
    "special_district",
    "multi",
}
ALLOWED_DIFFICULTIES = {"T1_lookup", "T2_composition", "T3_interpretation"}
ALLOWED_CLAIM_ROLES = {"core", "adjunct"}
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

# One-way ratchet order. side_by_side_only and needs_refresh share a rank:
# both are honest intermediate states between refusal and partial.
ANSWER_MODE_RANK = {
    "unsupported_with_path": 0,
    "needs_refresh": 1,
    "side_by_side_only": 1,
    "partial": 2,
    "exact": 3,
}


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_cases():
    return load_json(CASES_PATH)


def load_source_ids():
    source_ids = set()
    for path in SOURCE_ROOT.glob("*/sources/*.source.json"):
        source_ids.add(load_json(path)["id"])
    return source_ids


def load_active_taxonomy_categories():
    categories = set()
    for line in TAXONOMY_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
        if len(cells) >= 2 and cells[1] == "active":
            categories.add(cells[0])
    return categories


def validate_case(case, source_ids, active_categories):
    missing = REQUIRED_FIELDS.difference(case)
    if missing:
        raise AssertionError(
            f"{case.get('id', '<missing id>')} missing fields: {sorted(missing)}"
        )

    case_id = case["id"]
    if case["bucket"] != "wa-citizen":
        raise AssertionError(f"{case_id} has wrong bucket: {case['bucket']!r}")

    for field in (
        "id",
        "question",
        "persona",
        "jurisdiction",
        "archetype",
        "plugin_prompt",
        "web_prompt",
        "unlocked_by",
        "improvement_path",
    ):
        value = case[field]
        if not isinstance(value, str) or not value.strip():
            raise AssertionError(f"{case_id} has invalid {field}: {value!r}")

    if case["altitude"] not in ALLOWED_ALTITUDES:
        raise AssertionError(f"{case_id} has unknown altitude: {case['altitude']!r}")
    if case["difficulty"] not in ALLOWED_DIFFICULTIES:
        raise AssertionError(f"{case_id} has unknown difficulty: {case['difficulty']!r}")
    if not isinstance(case["anchor"], bool):
        raise AssertionError(f"{case_id} anchor must be a boolean")
    if case["question"] not in case["plugin_prompt"] or case["question"] not in case["web_prompt"]:
        raise AssertionError(f"{case_id} prompts must embed the immutable question text")

    if case["expected_answer_mode"] not in ANSWER_MODE_RANK:
        raise AssertionError(f"{case_id} has unknown answer mode")
    if case["mode_ceiling"] not in ANSWER_MODE_RANK:
        raise AssertionError(f"{case_id} has unknown mode ceiling")
    if ANSWER_MODE_RANK[case["expected_answer_mode"]] > ANSWER_MODE_RANK[case["mode_ceiling"]]:
        raise AssertionError(
            f"{case_id} expects {case['expected_answer_mode']} above its ceiling {case['mode_ceiling']}"
        )
    if case["expected_failure_mode"] not in ALLOWED_FAILURE_MODES:
        raise AssertionError(f"{case_id} has unknown failure mode")

    if case["score_dimensions"] != EXPECTED_SCORE_DIMENSIONS:
        raise AssertionError(f"{case_id} has unexpected score dimensions")

    if not isinstance(case["paraphrases"], list) or not case["paraphrases"]:
        raise AssertionError(f"{case_id} must include at least one paraphrase")

    claims = case["required_claims"]
    if not isinstance(claims, list) or not claims:
        raise AssertionError(f"{case_id} must declare required claims")
    core_claims = [claim for claim in claims if claim.get("role") == "core"]
    if not core_claims:
        raise AssertionError(f"{case_id} must declare at least one core claim")
    for claim in claims:
        if claim.get("role") not in ALLOWED_CLAIM_ROLES:
            raise AssertionError(f"{case_id} claim has unknown role: {claim.get('role')!r}")
        jurisdiction = claim.get("jurisdiction")
        if not isinstance(jurisdiction, str) or not jurisdiction.strip():
            raise AssertionError(f"{case_id} claim missing jurisdiction")
        category = claim.get("category")
        if not isinstance(category, str) or not category.strip():
            raise AssertionError(f"{case_id} claim missing category")
        if category.startswith("proposed:"):
            proposed = category[len("proposed:"):]
            if not re.fullmatch(r"[a-z0-9_]+\.[a-z0-9_]+", proposed):
                raise AssertionError(
                    f"{case_id} proposed category must look like family.category: {category!r}"
                )
            if proposed in active_categories:
                raise AssertionError(
                    f"{case_id} claims proposed:{proposed} but the taxonomy already "
                    f"promoted it; drop the proposed: prefix"
                )
        elif category not in active_categories:
            raise AssertionError(
                f"{case_id} claim category is neither active in the taxonomy nor "
                f"proposed: {category!r}"
            )

    if case["expected_answer_mode"] == "unsupported_with_path" and not case["expected_missing_sources"]:
        raise AssertionError(
            f"{case_id} expects unsupported_with_path but names no missing sources - "
            f"the path is the contract"
        )

    for source_id in case["expected_source_ids"]:
        if source_id not in source_ids:
            raise AssertionError(f"{case_id} references unknown source id: {source_id}")

    for fact in case["expected_facts"]:
        for field in ("id", "value", "tolerance", "unit", "description", "reproduction_ref"):
            if field not in fact:
                raise AssertionError(f"{case_id} fact missing field: {field}")
        if not isinstance(fact["value"], (int, float)):
            raise AssertionError(f"{case_id} fact {fact['id']} value must be numeric")
        if not isinstance(fact["tolerance"], (int, float)) or fact["tolerance"] < 0:
            raise AssertionError(f"{case_id} fact {fact['id']} tolerance must be >= 0")

    if not case["required_caveats"]:
        raise AssertionError(f"{case_id} must declare required caveats")
    for caveat in case["required_caveats"]:
        for field in ("id", "pattern", "description"):
            if field not in caveat or not str(caveat[field]).strip():
                raise AssertionError(f"{case_id} caveat missing field: {field}")
        try:
            re.compile(caveat["pattern"], re.IGNORECASE)
        except re.error as exc:
            raise AssertionError(
                f"{case_id} caveat {caveat['id']} pattern does not compile: {exc}"
            )

    if "max_data_age_days" in case:
        value = case["max_data_age_days"]
        if not isinstance(value, int) or value <= 0:
            raise AssertionError(f"{case_id} max_data_age_days must be a positive integer")


class WaCitizenBenchmarkContractTest(unittest.TestCase):
    def setUp(self):
        self.cases = load_cases()
        self.source_ids = load_source_ids()
        self.active_categories = load_active_taxonomy_categories()

    def test_suite_has_exactly_twenty_cases(self):
        self.assertEqual(len(self.cases), EXPECTED_CASE_COUNT)

    def test_case_ids_are_unique(self):
        ids = [case["id"] for case in self.cases]
        self.assertEqual(len(ids), len(set(ids)), "duplicate case ids")

    def test_cases_follow_contract(self):
        for case in self.cases:
            validate_case(case, self.source_ids, self.active_categories)

    def test_exactly_five_anchor_cases(self):
        anchors = [case["id"] for case in self.cases if case["anchor"]]
        self.assertEqual(len(anchors), EXPECTED_ANCHOR_COUNT, anchors)

    def test_suite_spans_all_altitudes(self):
        altitudes = {case["altitude"] for case in self.cases}
        self.assertEqual(altitudes, ALLOWED_ALTITUDES)

    def test_suite_spans_all_difficulties(self):
        difficulties = {case["difficulty"] for case in self.cases}
        self.assertEqual(difficulties, ALLOWED_DIFFICULTIES)

    def test_taxonomy_parse_finds_active_categories(self):
        self.assertIn("budget_finance.operating_budget", self.active_categories)
        self.assertIn(
            "population_demographics.population_denominator", self.active_categories
        )

    def test_expectation_log_exists_with_baseline_entry(self):
        text = EXPECTATION_LOG_PATH.read_text(encoding="utf-8")
        self.assertIn("2026-07-13 - baseline", text)

    def test_contract_rejects_expectation_above_ceiling(self):
        case = json.loads(json.dumps(self.cases[0]))
        case["mode_ceiling"] = "partial"
        case["expected_answer_mode"] = "exact"
        with self.assertRaisesRegex(AssertionError, "above its ceiling"):
            validate_case(case, self.source_ids, self.active_categories)

    def test_contract_rejects_promoted_category_still_marked_proposed(self):
        case = json.loads(json.dumps(self.cases[0]))
        case["required_claims"] = [
            {
                "jurisdiction": "City of Seattle",
                "category": "proposed:budget_finance.operating_budget",
                "role": "core",
            }
        ]
        with self.assertRaisesRegex(AssertionError, "already promoted"):
            validate_case(case, self.source_ids, self.active_categories)

    def test_contract_rejects_unsupported_case_without_named_path(self):
        case = json.loads(json.dumps(self.cases[0]))
        case["expected_answer_mode"] = "unsupported_with_path"
        case["mode_ceiling"] = "exact"
        case["expected_missing_sources"] = []
        with self.assertRaisesRegex(AssertionError, "names no missing sources"):
            validate_case(case, self.source_ids, self.active_categories)

    def test_contract_rejects_caveat_with_bad_regex(self):
        case = json.loads(json.dumps(self.cases[0]))
        case["required_caveats"] = [
            {"id": "broken", "pattern": "(unclosed", "description": "bad"}
        ]
        with self.assertRaisesRegex(AssertionError, "does not compile"):
            validate_case(case, self.source_ids, self.active_categories)


if __name__ == "__main__":
    unittest.main()
