import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    ROOT / "jurisdictions" / "king_county" / "scripts" / "extract_open_budget.py"
)
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "king_county"
SOURCE_CARD_PATH = (
    ROOT
    / "jurisdictions"
    / "king_county"
    / "sources"
    / "open-budget-dashboard.source.json"
)
TEMPLATE_ROOT = (
    ROOT
    / "jurisdictions"
    / "king_county"
    / "data"
    / "open-budget-dashboard"
    / "query_templates"
)


spec = importlib.util.spec_from_file_location("king_county_extract", SCRIPT_PATH)
extract = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(extract)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class KingCountyPowerBiExtractTest(unittest.TestCase):
    def test_source_card_is_parseable_and_scoped(self):
        source = load_json(SOURCE_CARD_PATH)
        self.assertEqual(source["id"], "king_county.open_budget_dashboard")
        self.assertIn("safe_answer_patterns", source)
        self.assertIn("not_supported_by_this_source", source)
        unsupported = " ".join(source["not_supported_by_this_source"])
        self.assertIn("Actual spending", unsupported)
        self.assertIn("Cross-jurisdiction", unsupported)

    def test_overview_fixture_normalizes_year_totals(self):
        payload = load_json(FIXTURE_DIR / "overview-by-year.response.json")
        rows = extract.normalize_overview_by_year(payload)
        self.assertEqual(len(rows), 11)
        fy2026 = next(row for row in rows if row["year"] == 2026)
        self.assertEqual(fy2026["budgeted_revenue"], 8865634686)
        self.assertEqual(fy2026["budgeted_expenditure"], 8598795612)
        self.assertEqual(fy2026["budgeted_fte"], 18333)

    def test_department_fixture_normalizes_revenue_and_expenditure(self):
        payload = load_json(
            FIXTURE_DIR / "department-revenue-expenditure-by-year.response.json"
        )
        rows, total = extract.normalize_department_revenue_expenditure(payload, year=2026)
        self.assertEqual(total["budgeted_revenue"], 8865634686)
        self.assertEqual(total["budgeted_expenditure"], 8598795612)
        self.assertEqual(len(rows), 22)

        dchs = next(
            row
            for row in rows
            if row["department"] == "DCHS - Community and Human Services"
        )
        self.assertEqual(dchs["budgeted_revenue"], 1496409023)
        self.assertEqual(dchs["budgeted_expenditure"], 1623966003)

        metro = next(row for row in rows if row["department"] == "MTD - Metro Transit")
        self.assertEqual(metro["budgeted_revenue"], 1539766467)
        self.assertEqual(metro["budgeted_expenditure"], 1498241453)

        non_kc = next(row for row in rows if row["department"] == "Non KC")
        self.assertEqual(non_kc["budgeted_revenue"], 0)
        self.assertEqual(non_kc["budgeted_expenditure"], 501929)

    def test_fte_fixture_normalizes_department_totals(self):
        payload = load_json(FIXTURE_DIR / "department-fte-by-year.response.json")
        rows, total = extract.normalize_department_fte(payload, year=2026)
        self.assertEqual(total, 18333)
        self.assertEqual(len(rows), 21)

        metro = next(row for row in rows if row["department"] == "MTD - Metro Transit")
        self.assertEqual(metro["budgeted_fte"], 6373)

    def test_conceptual_schema_fixture_extracts_entities(self):
        payload = load_json(FIXTURE_DIR / "conceptualschema-sample.json")
        entities = extract.conceptual_entities(payload)
        self.assertIn("Revenues", entities)
        self.assertIn("Expenditures", entities)
        self.assertIn("FTEData", entities)
        self.assertIn("Year", entities)

    def test_template_year_and_visual_id_are_discoverable(self):
        template = load_json(
            TEMPLATE_ROOT / "department-revenue-expenditure-by-year.query.json"
        )
        self.assertEqual(extract.template_year(template), 2026)
        self.assertEqual(extract.visual_id(template), "2ad918b7b77cb4d00a40")

    def test_snapshot_writer_outputs_summary_and_provenance(self):
        source = load_json(SOURCE_CARD_PATH)
        templates = {
            key: load_json(TEMPLATE_ROOT / filename)
            for key, filename in extract.QUERY_TEMPLATE_FILES.items()
        }
        responses = {
            key: load_json(FIXTURE_DIR / filename)
            for key, filename in extract.FIXTURE_RESPONSE_FILES.items()
        }
        metadata = extract.metadata_from_source_card(source)
        conceptual_schema = load_json(FIXTURE_DIR / "conceptualschema-sample.json")

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "snapshot"
            extract.write_snapshot(
                source=source,
                templates=templates,
                responses=responses,
                metadata=metadata,
                conceptual_schema=conceptual_schema,
                output_dir=output_dir,
                live=False,
            )
            summary = load_json(output_dir / "summary.json")
            self.assertEqual(
                summary["validation_checks"]["fy2026_revenue_total"], 8865634686
            )
            self.assertEqual(
                summary["validation_checks"]["fy2026_expenditure_total"], 8598795612
            )
            provenance = load_json(output_dir / "provenance.json")
            self.assertFalse(provenance["generated_from_live_powerbi"])
            self.assertEqual(
                summary["source_fingerprint"]["row_counts"],
                summary["row_counts"],
            )
            self.assertEqual(
                provenance["source_fingerprint"]["integrity"]["response_metrics"],
                provenance["response_metrics"],
            )
            self.assertIn(
                "template_sha256",
                provenance["query_templates"]["overview_by_year"],
            )
            normalized = output_dir / "normalized"
            self.assertTrue((normalized / "overview-by-year.jsonl").is_file())
            self.assertTrue(
                (normalized / "department-revenue-expenditure-by-year.jsonl").is_file()
            )
            self.assertTrue((normalized / "department-fte-by-year.jsonl").is_file())


if __name__ == "__main__":
    unittest.main()
