import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "eval.py"

spec = importlib.util.spec_from_file_location("wa20_eval", SCRIPT_PATH)
wa20_eval = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wa20_eval)


CASE = {
    "id": "test-case",
    "anchor": True,
    "expected_answer_mode": "exact",
    "expected_source_ids": ["seattle.operating_budget"],
    "required_caveats": [
        {
            "id": "approved-not-actual",
            "pattern": "approved[^.]{0,60}not[^.]{0,40}actual",
            "description": "approved is not actual",
        }
    ],
    "expected_facts": [
        {
            "id": "total",
            "value": 272607622.34,
            "tolerance": 3000000,
            "unit": "dollars",
            "description": "parks total",
            "reproduction_ref": "test",
        }
    ],
}

GOOD_ANSWER = """---
case: test-case
surface: plugin
answer_mode: exact
---

Conclusion: Seattle budgets about $272.6 million for parks in FY2026.

Numbers: FY2026 approved total $272,607,622 across 707 rows.

How to read this: approved budget amounts are not actual spending.

Trace: source seattle.operating_budget (data.seattle.gov 8u2j-imqx).
"""


class ExtractNumbersTest(unittest.TestCase):
    def test_extracts_plain_numbers_with_commas(self):
        self.assertIn(272607622.0, wa20_eval.extract_numbers("total $272,607,622 across"))

    def test_extracts_magnitude_suffixes(self):
        numbers = wa20_eval.extract_numbers("about $272.6 million, or $0.27B, of $150.411 billion")
        self.assertIn(272600000.0, numbers)
        self.assertIn(270000000.0, numbers)
        self.assertIn(150411000000.0, numbers)

    def test_fte_style_integers(self):
        self.assertIn(1246.0, wa20_eval.extract_numbers("1,246 budgeted FTE"))


class FactMatchingTest(unittest.TestCase):
    def test_exact_value_matches(self):
        fact = {"value": 1246, "tolerance": 0}
        self.assertTrue(wa20_eval.fact_matches(fact, [1246.0]))
        self.assertFalse(wa20_eval.fact_matches(fact, [1245.0]))

    def test_relative_floor_accepts_honest_rounding(self):
        # "$150.411 billion" vs exact 150,411,096,000: within the 0.05% floor
        fact = {"value": 150411096000, "tolerance": 0}
        self.assertTrue(wa20_eval.fact_matches(fact, [150411000000.0]))
        # "$150 billion" is 0.27% off: fails
        self.assertFalse(wa20_eval.fact_matches(fact, [150000000000.0]))

    def test_explicit_tolerance_still_applies(self):
        fact = {"value": 272607622.34, "tolerance": 3000000}
        self.assertTrue(wa20_eval.fact_matches(fact, [272600000.0]))
        self.assertFalse(wa20_eval.fact_matches(fact, [265000000.0]))


class AnswerParsingTest(unittest.TestCase):
    def test_parses_front_matter_and_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.md"
            path.write_text(GOOD_ANSWER, encoding="utf-8")
            parsed = wa20_eval.parse_answer_file(path)
        self.assertEqual(parsed["meta"]["answer_mode"], "exact")
        self.assertIn("Conclusion", parsed["body"])

    def test_template_counts_as_not_captured(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.md"
            path.write_text(
                "---\ncase: x\nanswer_mode: <exact>\n---\n\nPASTE THE FULL ANSWER HERE.\n",
                encoding="utf-8",
            )
            parsed = wa20_eval.parse_answer_file(path)
        self.assertFalse(wa20_eval.answer_is_captured(parsed))


class ScoreCaseTest(unittest.TestCase):
    def parsed(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "a.md"
            path.write_text(text, encoding="utf-8")
            return wa20_eval.parse_answer_file(path)

    def test_good_answer_passes_all_checks(self):
        result = wa20_eval.score_case(CASE, self.parsed(GOOD_ANSWER))
        failing = [c for c in result["checks"] if not c["passed"]]
        self.assertEqual(failing, [], failing)
        self.assertEqual(result["passed"], result["total"])

    def test_wrong_mode_fails_mode_check(self):
        answer = GOOD_ANSWER.replace("answer_mode: exact", "answer_mode: partial")
        result = wa20_eval.score_case(CASE, self.parsed(answer))
        mode = [c for c in result["checks"] if c["check"] == "answer_mode"][0]
        self.assertFalse(mode["passed"])

    def test_missing_source_and_caveat_fail(self):
        answer = """---
case: test-case
answer_mode: exact
---

Seattle budgets $272,607,622 for parks. Everything is great.
"""
        result = wa20_eval.score_case(CASE, self.parsed(answer))
        by_check = {c["check"]: c["passed"] for c in result["checks"]}
        self.assertFalse(by_check["source:seattle.operating_budget"])
        self.assertFalse(by_check["caveat:approved-not-actual"])
        self.assertTrue(by_check["fact:total"])

    def test_wrong_number_fails_fact_check(self):
        answer = GOOD_ANSWER.replace("$272,607,622", "$372,607,622").replace(
            "$272.6 million", "$372.6 million"
        )
        result = wa20_eval.score_case(CASE, self.parsed(answer))
        fact = [c for c in result["checks"] if c["check"] == "fact:total"][0]
        self.assertFalse(fact["passed"])


class WorksheetTest(unittest.TestCase):
    def test_worksheet_lists_anchor_cases_and_failures(self):
        payload = {
            "run": "2026-07-13",
            "results": [
                {
                    "case": "test-case",
                    "anchor": True,
                    "captured": True,
                    "passed": 1,
                    "total": 2,
                    "checks": [
                        {"check": "answer_mode", "passed": True, "expected": "exact", "actual": "exact"},
                        {"check": "fact:total", "passed": False, "expected": 1, "actual": "not found"},
                    ],
                },
                {
                    "case": "non-anchor",
                    "anchor": False,
                    "captured": False,
                    "passed": 0,
                    "total": 0,
                    "checks": [],
                },
            ],
        }
        worksheet = wa20_eval.render_worksheet(payload)
        self.assertIn("`test-case` | 1/2", worksheet)
        self.assertNotIn("| `non-anchor` |", worksheet)
        self.assertIn("fact:total", worksheet)


class InitRunTest(unittest.TestCase):
    def test_init_creates_prompts_templates_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = wa20_eval.RUNS_ROOT
            wa20_eval.RUNS_ROOT = Path(tmp)
            try:
                wa20_eval.init_run(label="test", date="2026-07-13")
            finally:
                wa20_eval.RUNS_ROOT = original
            run_dir = Path(tmp) / "2026-07-13-test"
            cases = wa20_eval.load_cases()
            self.assertEqual(
                len(list(run_dir.glob("*.prompt.txt"))), len(cases)
            )
            self.assertEqual(len(list(run_dir.glob("*.md"))), len(cases))
            metadata = json.loads((run_dir / "run-metadata.json").read_text())
            self.assertEqual(metadata["cases"], len(cases))
            self.assertIn("capture_protocol", metadata)


if __name__ == "__main__":
    unittest.main()
