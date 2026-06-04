import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "docs" / "coverage-taxonomy.md"
SOURCE_ROOT = ROOT / "jurisdictions"

EXPECTED_ACTIVE_CATEGORIES = {
    "budget_finance.operating_budget",
    "budget_finance.revenue_budget",
    "workforce.budgeted_fte",
    "budget_finance.actual_spending_checkbook",
}
EXPECTED_CURRENT_CLAIMS = {
    "seattle.operating_budget": EXPECTED_ACTIVE_CATEGORIES,
    "king_county.open_budget_dashboard": EXPECTED_ACTIVE_CATEGORIES,
    "washington.operating_budget": EXPECTED_ACTIVE_CATEGORIES,
}
ALLOWED_STATUSES = {"supported", "partial", "unsupported"}
FORBIDDEN_UNSUPPORTED_PATTERNS = [
    re.compile(r"\bseattle\s+(does not|doesn't|lacks|has no)\b", re.I),
    re.compile(r"\bking county\s+(does not|doesn't|lacks|has no)\b", re.I),
    re.compile(r"\bwashington(?: state)?\s+(does not|doesn't|lacks|has no)\b", re.I),
]


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

    def test_unsupported_claims_use_source_level_wording(self):
        for source in source_cards():
            for claim in source.get("coverage_claims", []):
                if claim["status"] != "unsupported":
                    continue
                reason = claim.get("unsupported_reason", "")
                self.assertIn("unsupported by this source", reason.lower())
                for pattern in FORBIDDEN_UNSUPPORTED_PATTERNS:
                    self.assertIsNone(pattern.search(reason), reason)


if __name__ == "__main__":
    unittest.main()
