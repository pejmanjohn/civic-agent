import html
import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "jurisdictions" / "washington" / "scripts" / "extract_open_checkbook.py"
SOURCE_CARD_PATH = ROOT / "jurisdictions" / "washington" / "sources" / "open-checkbook.source.json"


spec = importlib.util.spec_from_file_location("washington_extract_open_checkbook", SCRIPT_PATH)
extract = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = extract
spec.loader.exec_module(extract)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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


def write_minimal_xlsx(path, rows, *, absolute_sheet_target=False):
    row_xml = []
    for row_index, row in enumerate(rows, start=1):
        cells = [
            cell_xml(f"{column_name(column_index)}{row_index}", value)
            for column_index, value in enumerate(row, start=1)
        ]
        row_xml.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    target = "/xl/worksheets/sheet1.xml" if absolute_sheet_target else "worksheets/sheet1.xml"
    with ZipFile(path, "w") as zf:
        zf.writestr(
            "xl/workbook.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>
</workbook>
""",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            f"""<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="{target}"/>
</Relationships>
""",
        )
        zf.writestr(
            "xl/worksheets/sheet1.xml",
            f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>{"".join(row_xml)}</sheetData>
</worksheet>
""",
        )


CURRENT_HEADERS = [
    "Bien",
    "FY",
    "FMonth",
    "Agy",
    "Agency",
    "Object",
    "Category",
    "Subobj",
    "SubCategory",
    "Vendor",
    "Amount",
]


class WashingtonCheckbookExtractTest(unittest.TestCase):
    def test_calendar_month_from_fiscal_month_uses_washington_fiscal_year(self):
        self.assertEqual(extract.calendar_month_from_fiscal(2026, 1), "2025-07")
        self.assertEqual(extract.calendar_month_from_fiscal(2026, 6), "2025-12")
        self.assertEqual(extract.calendar_month_from_fiscal(2026, 7), "2026-01")
        self.assertEqual(extract.calendar_month_from_fiscal(2026, 10), "2026-04")
        with self.assertRaises(extract.CheckbookExtractError):
            extract.calendar_month_from_fiscal(2026, 13)

    def test_parse_xlsx_rows_handles_current_header_variant(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "VendorPayments2527.xlsx"
            write_minimal_xlsx(
                path,
                [
                    CURRENT_HEADERS,
                    [
                        "2025-27",
                        2026,
                        10,
                        " 100 ",
                        "Agency A",
                        "C",
                        "Goods and Services",
                        "01",
                        "Office Supplies",
                        "Vendor A",
                        1234.56,
                    ],
                ],
            )

            rows = list(extract.parse_xlsx_rows(path))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["FMonth"], "10")
            normalized = extract.normalize_payment_row(rows[0])
            self.assertEqual(normalized["agency_code"], "100")
            self.assertEqual(normalized["calendar_month"], "2026-04")
            self.assertEqual(normalized["amount"], 1234.56)

    def test_parse_xlsx_rows_handles_older_fiscal_month_header_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "VendorPayments1315.xlsx"
            write_minimal_xlsx(
                path,
                [
                    [
                        "Bien",
                        "FY",
                        "Fiscal Month",
                        "Agy",
                        "Agency",
                        "Object",
                        "Category",
                        "Subobj",
                        "SubCategory",
                        "Vendor",
                        "Amount",
                    ],
                    [
                        "2013-15",
                        2014,
                        1,
                        "200",
                        "Agency B",
                        "D",
                        "Travel",
                        "02",
                        "Airfare",
                        "Vendor B",
                        "(1,000.25)",
                    ],
                ],
                absolute_sheet_target=True,
            )

            rows = list(extract.parse_xlsx_rows(path))
            self.assertEqual(rows[0]["FMonth"], "1")
            normalized = extract.normalize_payment_row(rows[0])
            self.assertEqual(normalized["calendar_month"], "2013-07")
            self.assertEqual(normalized["amount"], -1000.25)

    def test_parse_xlsx_rows_rejects_unexpected_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.xlsx"
            write_minimal_xlsx(path, [["Bien", "FY", "Month"], ["2025-27", 2026, 10]])
            with self.assertRaises(extract.CheckbookExtractError):
                list(extract.parse_xlsx_rows(path))

    def test_build_database_from_files_writes_manifest_and_queryable_rows(self):
        source = load_json(SOURCE_CARD_PATH)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            xlsx_path = tmp_path / "VendorPayments2527.xlsx"
            db_path = tmp_path / "open_checkbook.sqlite"
            manifest_path = tmp_path / "manifest.json"
            write_minimal_xlsx(
                xlsx_path,
                [
                    CURRENT_HEADERS,
                    [
                        "2025-27",
                        2026,
                        10,
                        "100",
                        "Agency A",
                        "C",
                        "Goods and Services",
                        "01",
                        "Office Supplies",
                        "Vendor A",
                        100,
                    ],
                    [
                        "2025-27",
                        2026,
                        9,
                        "200",
                        "Agency B",
                        "D",
                        "Travel",
                        "02",
                        "Airfare",
                        "Vendor B",
                        50,
                    ],
                ],
            )

            manifest = extract.build_database_from_files(
                source,
                [
                    {
                        "source_surface_id": "vendor_payments_2025_27_xlsx",
                        "biennium": "2025-27",
                        "url": "https://example.test/VendorPayments2527.xlsx",
                        "path": xlsx_path,
                        "last_modified": "Tue, 26 May 2026 23:51:24 GMT",
                    }
                ],
                db_path,
            )

            self.assertEqual(manifest["status"], "partial_current_period")
            self.assertEqual(manifest["row_count"], 2)
            self.assertEqual(manifest["data_through"], "2026-04")
            self.assertEqual(manifest["data_through_label"], "Payments through April 2026")
            self.assertEqual(manifest["source_files"][0]["row_count"], 2)
            self.assertTrue(db_path.is_file())

            with sqlite3.connect(db_path) as conn:
                amount = conn.execute("SELECT SUM(amount) FROM payments").fetchone()[0]
                self.assertEqual(amount, 150)
                source_file_count = conn.execute("SELECT COUNT(*) FROM source_files").fetchone()[0]
                self.assertEqual(source_file_count, 1)

            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            context = SimpleNamespace(
                source_id=source["id"],
                manifest_path=manifest_path,
            )
            result = extract.run_named_query(
                context,
                "category_breakdown",
                {"biennium": "2025-27", "limit": "5"},
            )
            self.assertEqual(result["grain"], "category")
            self.assertEqual(result["data_through"], "2026-04")
            self.assertEqual(
                [(row["name"], row["amount"], row["payment_rows"]) for row in result["rows"]],
                [("Goods and Services", 100.0, 1), ("Travel", 50.0, 1)],
            )


if __name__ == "__main__":
    unittest.main()
