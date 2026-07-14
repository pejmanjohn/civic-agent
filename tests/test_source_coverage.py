import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "docs" / "coverage-taxonomy.md"
MATRIX_PATH = ROOT / "docs" / "coverage-matrix.md"
SCRIPT_PATH = ROOT / "scripts" / "coverage.py"
SOURCE_ROOT = ROOT / "jurisdictions"

EXPECTED_ACTIVE_CATEGORIES = {
    "budget_finance.operating_budget",
    "budget_finance.revenue_budget",
    "workforce.budgeted_fte",
    "budget_finance.actual_spending_checkbook",
    "budget_finance.filed_annual_actuals",
    "budget_finance.property_tax_levies",
    "population_demographics.population_denominator",
}
EXPECTED_BUDGET_CATEGORIES = EXPECTED_ACTIVE_CATEGORIES - {
    "population_demographics.population_denominator",
    "budget_finance.filed_annual_actuals",
    "budget_finance.property_tax_levies",
}
EXPECTED_CURRENT_CLAIMS = {
    "seattle.operating_budget": EXPECTED_BUDGET_CATEGORIES,
    "king_county.open_budget_dashboard": EXPECTED_BUDGET_CATEGORIES,
    "washington.operating_budget": EXPECTED_BUDGET_CATEGORIES,
    "washington.revenue_by_biennium": EXPECTED_BUDGET_CATEGORIES,
    "washington.open_checkbook": EXPECTED_BUDGET_CATEGORIES,
    "washington.ofm_population": {"population_demographics.population_denominator"},
    "washington.fit_filed_actuals": EXPECTED_BUDGET_CATEGORIES
    | {"budget_finance.filed_annual_actuals"},
    "washington.dor_property_tax_levies": EXPECTED_BUDGET_CATEGORIES
    | {"budget_finance.property_tax_levies"},
    "pierce_county.open_budget": EXPECTED_BUDGET_CATEGORIES,
    "pierce_county.open_checkbook": EXPECTED_BUDGET_CATEGORIES,
}
ALLOWED_STATUSES = {"supported", "partial", "unsupported"}
REQUIRED_SEMANTIC_FIELDS = {
    "amount_basis",
    "budget_frame",
    "period_type",
    "period_status",
    "unit",
    "government_scope",
    "geography_basis",
    "comparability_notes",
}
REQUIRED_DENOMINATOR_SEMANTIC_FIELDS = {
    "denominator_basis",
    "period_type",
    "period_status",
    "unit",
    "government_scope",
    "geography_basis",
    "comparability_notes",
}
ALLOWED_SEMANTICS = {
    "amount_basis": {
        "actual",
        "adopted",
        "approved",
        "budgeted",
        "estimated",
        "projected",
        "proposed",
        "appropriated",
    },
    "budget_frame": {
        "actual_spending_checkbook",
        "filed_annual_actuals",
        "property_tax_levies",
        "general_fund_revenue",
        "operating",
        "operating_dashboard",
        "revenue_dashboard",
        "workforce",
    },
    "period_type": {
        "biennium",
        "calendar_year",
        "fiscal_year",
        "quarter",
        "month",
        "current_period_to_date",
        "point_in_time",
    },
    "period_status": {
        "actualized",
        "adopted",
        "amended",
        "approved",
        "budgeted",
        "enacted",
        "partial_current_period",
        "proposed",
        "official_estimate",
    },
    "unit": {
        "dollars",
        "fte",
        "residents",
    },
    "government_scope": {
        "city",
        "county",
        "state",
        "federal",
        "multi_jurisdiction",
        "regional_authority",
        "school_district",
        "special_district",
    },
    "geography_basis": {
        "resident_jurisdiction",
        "service_area",
        "statewide",
        "taxing_district",
        "regional_service_area",
    },
    "denominator_basis": {
        "resident_population",
    },
}
FORBIDDEN_UNSUPPORTED_PATTERNS = [
    re.compile(r"\bseattle\s+(does not|doesn't|lacks|has no)\b", re.I),
    re.compile(r"\bking county\s+(does not|doesn't|lacks|has no)\b", re.I),
    re.compile(r"\bwashington(?: state)?\s+(does not|doesn't|lacks|has no)\b", re.I),
]


spec = importlib.util.spec_from_file_location("coverage_renderer", SCRIPT_PATH)
coverage_renderer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(coverage_renderer)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def source_card_paths():
    return sorted(SOURCE_ROOT.glob("*/sources/*.source.json"))


def source_cards():
    return [load_json(path) for path in source_card_paths()]


def markdown_table_rows(path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [
            cell.strip().strip("`")
            for cell in stripped.strip("|").split("|")
        ]
        rows.append(cells)
    return rows


def active_categories_from_taxonomy():
    categories = set()
    for cells in markdown_table_rows(TAXONOMY_PATH):
        if len(cells) >= 2 and cells[1] == "active":
            categories.add(cells[0])
    return categories


def backlog_families_from_taxonomy():
    families = set()
    for cells in markdown_table_rows(TAXONOMY_PATH):
        if len(cells) >= 2 and cells[1] == "backlog":
            families.add(cells[0])
    return families


def source_measure_names(source):
    names = {field["name"] for field in source.get("fields", [])}
    primary_measure = source.get("primary_measure")
    if primary_measure:
        names.add(primary_measure)
    names.update(source.get("primary_measures", []))
    return names


def source_has_evidence_ref(source, ref):
    if ref.startswith("validation_checks."):
        key = ref.split(".", 1)[1]
        return key in source.get("validation_checks", {})
    return ref in source


def validate_claim_semantics(source_id, claim):
    semantics = claim.get("semantics")
    if claim["status"] in {"supported", "partial"}:
        if not isinstance(semantics, dict):
            raise AssertionError(f"{source_id} {claim['category']} missing semantics")
        if claim["category"] == "population_demographics.population_denominator":
            required_fields = REQUIRED_DENOMINATOR_SEMANTIC_FIELDS
        else:
            required_fields = REQUIRED_SEMANTIC_FIELDS
        missing = required_fields.difference(semantics)
        if missing:
            raise AssertionError(f"{source_id} {claim['category']} missing {sorted(missing)}")
        for field in required_fields - {"comparability_notes"}:
            allowed_values = ALLOWED_SEMANTICS[field]
            if semantics[field] not in allowed_values:
                raise AssertionError(
                    f"{source_id} {claim['category']} has unknown {field}: "
                    f"{semantics[field]!r}"
                )
        notes = semantics["comparability_notes"]
        if not isinstance(notes, list):
            raise AssertionError(f"{source_id} {claim['category']} notes must be a list")
        if not notes:
            raise AssertionError(f"{source_id} {claim['category']} notes must not be empty")
    elif "semantics" in claim:
        raise AssertionError(f"{source_id} unsupported claim should not have semantics")


class SourceCoverageTest(unittest.TestCase):
    def test_taxonomy_declares_expected_active_categories(self):
        self.assertEqual(active_categories_from_taxonomy(), EXPECTED_ACTIVE_CATEGORIES)

    def test_taxonomy_keeps_backlog_out_of_active_categories(self):
        backlog = backlog_families_from_taxonomy()
        self.assertIn("population_demographics", backlog)
        self.assertIn("public_safety_crime", backlog)
        self.assertTrue(backlog.isdisjoint(active_categories_from_taxonomy()))

    def test_current_source_cards_have_reviewed_active_category_claims(self):
        for source in source_cards():
            if source["id"] not in EXPECTED_CURRENT_CLAIMS:
                continue
            categories = {
                claim["category"]
                for claim in source.get("coverage_claims", [])
            }
            self.assertEqual(categories, EXPECTED_CURRENT_CLAIMS[source["id"]])

    def test_claims_use_active_categories_statuses_and_no_duplicates(self):
        active_categories = active_categories_from_taxonomy()
        for source in source_cards():
            seen = set()
            for claim in source.get("coverage_claims", []):
                claim_key = (source["id"], claim["category"])
                self.assertNotIn(claim_key, seen)
                seen.add(claim_key)
                self.assertIn(claim["category"], active_categories)
                self.assertIn(claim["status"], ALLOWED_STATUSES)

    def test_supported_and_partial_claims_have_existing_measures_and_evidence(self):
        for source in source_cards():
            source_measures = source_measure_names(source)
            for claim in source.get("coverage_claims", []):
                if claim["status"] not in {"supported", "partial"}:
                    continue
                self.assertTrue(claim.get("measures"), claim)
                self.assertTrue(claim.get("grains"), claim)
                self.assertTrue(claim.get("time_coverage"), claim)
                self.assertTrue(claim.get("evidence"), claim)
                for measure in claim["measures"]:
                    self.assertIn(measure, source_measures)
                for evidence_ref in claim["evidence"]:
                    self.assertTrue(
                        source_has_evidence_ref(source, evidence_ref),
                        f"{source['id']} claim {claim['category']} missing {evidence_ref}",
                    )

    def test_supported_and_partial_claims_have_composition_semantics(self):
        for source in source_cards():
            for claim in source.get("coverage_claims", []):
                validate_claim_semantics(source["id"], claim)

    def test_semantic_validation_rejects_unknown_vocabulary(self):
        source, supported_claim = next(
            (source, claim)
            for source in source_cards()
            for claim in source.get("coverage_claims", [])
            if claim["status"] in {"supported", "partial"}
        )
        claim = json.loads(json.dumps(supported_claim))
        claim["semantics"]["amount_basis"] = "made_up_basis"
        with self.assertRaisesRegex(AssertionError, "unknown amount_basis"):
            validate_claim_semantics(source["id"], claim)

    def test_unsupported_claims_use_source_level_wording(self):
        for source in source_cards():
            for claim in source.get("coverage_claims", []):
                if claim["status"] != "unsupported":
                    continue
                reason = claim.get("unsupported_reason", "")
                self.assertIn("unsupported by this source", reason.lower())
                for pattern in FORBIDDEN_UNSUPPORTED_PATTERNS:
                    self.assertIsNone(pattern.search(reason), reason)


class CoverageRendererTest(unittest.TestCase):
    def test_rollup_status_distinguishes_not_yet_probed_from_unsupported(self):
        self.assertEqual(
            coverage_renderer.rollup_status([]),
            ("not-yet-probed", [], "No reviewed source card claim."),
        )
        source = {"id": "example.source"}
        unsupported = {"status": "unsupported"}
        status, sources, notes = coverage_renderer.rollup_status([(source, unsupported)])
        self.assertEqual(status, "unsupported-by-reviewed-source")
        self.assertEqual(sources, ["example.source"])
        self.assertIn("source-scoped", notes)

    def test_rollup_status_prefers_supported_claims_without_dropping_trace(self):
        supported_source = {"id": "example.supported"}
        unsupported_source = {"id": "example.unsupported"}
        status, sources, _ = coverage_renderer.rollup_status(
            [
                (unsupported_source, {"status": "unsupported"}),
                (supported_source, {"status": "supported"}),
            ]
        )
        self.assertEqual(status, "supported")
        self.assertEqual(sources, ["example.unsupported", "example.supported"])

    def test_checked_in_matrix_matches_renderer_output(self):
        rendered = coverage_renderer.render_markdown(
            coverage_renderer.parse_taxonomy(TAXONOMY_PATH),
            coverage_renderer.load_source_cards(),
        )
        self.assertEqual(MATRIX_PATH.read_text(encoding="utf-8"), rendered)

    def test_statewide_population_source_rolls_up_to_covered_local_jurisdictions(self):
        rendered = coverage_renderer.render_markdown(
            coverage_renderer.parse_taxonomy(TAXONOMY_PATH),
            coverage_renderer.load_source_cards(),
        )
        self.assertIn(
            "| City of Seattle | `population_demographics.population_denominator` | "
            "`supported` | washington.ofm_population |",
            rendered,
        )
        self.assertIn(
            "| King County, Washington | `population_demographics.population_denominator` | "
            "`supported` | washington.ofm_population |",
            rendered,
        )

    def test_renderer_has_no_network_fetch_dependencies(self):
        script = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("requests", script)
        self.assertNotIn("urllib", script)
        self.assertNotIn("http.client", script)
        self.assertNotIn("socket", script)


if __name__ == "__main__":
    unittest.main()
