import html
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "jurisdictions" / "washington" / "scripts" / "extract_ofm_population.py"
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "ofm-population.source.json"
SNAPSHOT_DIR = (
    ROOT
    / "jurisdictions"
    / "washington"
    / "data"
    / "ofm-population"
    / "2025-04-01"
)


spec = importlib.util.spec_from_file_location("washington_ofm_population_extract", SCRIPT_PATH)
extract = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = extract
spec.loader.exec_module(extract)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def column_name(index):
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(ord("A") + remainder) + name
    return name


def cell_xml(ref, value):
    if isinstance(value, (int, float)):
        return f'<c r="{ref}"><v>{value}</v></c>'
    escaped = html.escape(str(value), quote=False)
    return f'<c r="{ref}" t="inlineStr"><is><t>{escaped}</t></is></c>'


def sheet_xml(rows):
    row_xml = []
    for row_index, row in enumerate(rows, start=1):
        cells = [
            cell_xml(f"{column_name(column_index)}{row_index}", value)
            for column_index, value in enumerate(row, start=1)
        ]
        row_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>{"".join(row_xml)}</sheetData>
</worksheet>
"""


def minimal_population_workbook(rows, notation_rows):
    import io

    output = io.BytesIO()
    with ZipFile(output, "w") as zf:
        zf.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Population" sheetId="1" r:id="rId1"/>
    <sheet name="Notations" sheetId="2" r:id="rId2"/>
  </sheets>
</workbook>
""",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
</Relationships>
""",
        )
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml(rows))
        zf.writestr("xl/worksheets/sheet2.xml", sheet_xml(notation_rows))
    return output.getvalue()


class WashingtonOfmPopulationExtractTest(unittest.TestCase):
    def test_source_card_is_parseable_and_scoped_to_denominators(self):
        source = load_json(SOURCE_CARD_PATH)
        self.assertEqual(source["id"], "washington.ofm_population")
        self.assertEqual(source["access_method"], "official_bulk_download")
        self.assertEqual(source["storage_policy"]["tier"], "checked_in_snapshot")
        self.assertEqual(source["snapshot_version"], "2025-04-01")
        self.assertEqual(source["latest_estimate_date"], "2025-04-01")
        claim = source["coverage_claims"][0]
        self.assertEqual(claim["category"], "population_demographics.population_denominator")
        self.assertEqual(claim["status"], "supported")
        self.assertEqual(claim["semantics"]["denominator_basis"], "resident_population")
        unsupported = " ".join(source["not_supported_by_this_source"])
        self.assertIn("Service population", unsupported)
        self.assertIn("demographic composition", unsupported)

    def test_snapshot_summary_has_known_validation_checks(self):
        summary = load_json(SNAPSHOT_DIR / "summary.json")
        checks = summary["validation_checks"]
        self.assertEqual(summary["source_fingerprint"]["row_counts"], summary["row_counts"])
        self.assertEqual(summary["source_fingerprint"]["checks"], checks)
        self.assertEqual(summary["row_counts"]["geography_rows"], 409)
        self.assertEqual(summary["row_counts"]["population_estimates"], 2454)
        self.assertEqual(summary["row_counts"]["county_rows"], 39)
        self.assertEqual(summary["row_counts"]["city_town_rows"], 289)
        self.assertEqual(checks["seattle_2025_population"], 816600)
        self.assertEqual(checks["king_county_2025_population"], 2411700)
        self.assertEqual(checks["state_total_2025_population"], 8115100)
        self.assertTrue(checks["king_county_incorporated_reconciles"])
        self.assertTrue(checks["king_county_total_reconciles"])

    def test_normalized_rows_include_seattle_and_king_county_denominators(self):
        rows = load_jsonl(SNAPSHOT_DIR / "normalized" / "population-estimates.jsonl")
        seattle = population_row(rows, "Seattle", "city_town", 2025)
        king = population_row(rows, "King County", "county", 2025)

        self.assertEqual(seattle["population"], 816600)
        self.assertEqual(seattle["estimate_date"], "2025-04-01")
        self.assertEqual(seattle["geography_basis"], "resident_jurisdiction")
        self.assertEqual(king["population"], 2411700)
        self.assertEqual(king["estimate_date"], "2025-04-01")

    def test_provenance_records_source_file_identity(self):
        summary = load_json(SNAPSHOT_DIR / "summary.json")
        provenance = load_json(SNAPSHOT_DIR / "provenance.json")
        self.assertEqual(provenance["source_id"], "washington.ofm_population")
        self.assertEqual(provenance["source_fingerprint"], summary["source_fingerprint"])
        self.assertEqual(provenance["workbook"]["sheet_names"], ["Population", "Notations"])
        self.assertEqual(
            provenance["source_file"]["sha256"],
            "1a5bc5ea6927b6037741344df67e2161f3507fed25ac6ad0e9008f3941df5598",
        )

    def test_parse_population_workbook_handles_minimal_xlsx_shape(self):
        rows = [
            ["April 1, 2025 Population of Cities, Towns and Counties"],
            [],
            [],
            [],
            extract.EXPECTED_HEADERS,
            [1, 1, "King", "King County", 10, 11, 12, 13, 14, 15],
            [2, 4, "King", "Seattle", 5, 6, 7, 8, 9, 10],
            [3, ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ]
        notation_rows = [
            ["April 1, 2025 Population of Cities, Towns and Counties"],
            [],
            [],
            [],
            ["Line", "Filter", "County", "Jurisdiction", "2020 Notation", "2021 Notation", "2022 Notation", "2023 Notation", "2024 Notation", "2025 Notation"],
            [1, 1, "King", "King County", "", "", "", "", "", ""],
            [2, 4, "King", "Seattle", "", "", "", "", "", "*"],
        ]

        parsed = extract.parse_population_workbook(minimal_population_workbook(rows, notation_rows))
        normalized = extract.build_normalized_rows(parsed)

        self.assertEqual(parsed["separator_rows"], 1)
        self.assertEqual(len(parsed["geography_rows"]), 2)
        self.assertEqual(len(normalized), 12)
        seattle_2025 = population_row(normalized, "Seattle", "city_town", 2025)
        self.assertEqual(seattle_2025["population"], 10)
        self.assertEqual(seattle_2025["notation"], "*")


def population_row(rows, jurisdiction, row_type, year):
    return next(
        row
        for row in rows
        if row["jurisdiction"] == jurisdiction
        and row["row_type"] == row_type
        and row["year"] == year
    )


if __name__ == "__main__":
    unittest.main()
