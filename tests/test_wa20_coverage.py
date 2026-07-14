import datetime as dt
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "wa20.py"
SCOREBOARD_PATH = ROOT / "benchmarks" / "wa-citizen" / "scoreboard.md"

spec = importlib.util.spec_from_file_location("wa20", SCRIPT_PATH)
wa20 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wa20)

AS_OF = dt.date(2026, 7, 13)


def make_card(
    card_id="test.source",
    jurisdiction_name="Testville",
    claims=None,
    coverage_jurisdictions=None,
    data_through=None,
):
    card = {
        "id": card_id,
        "jurisdiction_name": jurisdiction_name,
        "coverage_claims": claims or [],
    }
    if coverage_jurisdictions:
        card["coverage_jurisdictions"] = [
            {"jurisdiction_id": name.lower(), "jurisdiction_name": name}
            for name in coverage_jurisdictions
        ]
    if data_through:
        card["source_fingerprint"] = {
            "version_boundary": {"current_data_through": data_through}
        }
    return card


def make_case(
    case_id="test-case",
    claims=None,
    expected_mode="exact",
    ceiling="exact",
    max_data_age_days=None,
):
    case = {
        "id": case_id,
        "question": "How big is the Testville budget?",
        "difficulty": "T1_lookup",
        "altitude": "city",
        "anchor": False,
        "required_claims": claims
        or [
            {
                "jurisdiction": "Testville",
                "category": "budget_finance.operating_budget",
                "role": "core",
            }
        ],
        "mode_ceiling": ceiling,
        "expected_answer_mode": expected_mode,
    }
    if max_data_age_days:
        case["max_data_age_days"] = max_data_age_days
    return case


SUPPORTED_CARD = make_card(
    claims=[{"category": "budget_finance.operating_budget", "status": "supported"}]
)


class ParseDateishTest(unittest.TestCase):
    def test_parses_year_month(self):
        self.assertEqual(wa20.parse_dateish("2026-04"), dt.date(2026, 4, 1))

    def test_parses_full_date(self):
        self.assertEqual(wa20.parse_dateish("2026-04-01"), dt.date(2026, 4, 1))

    def test_skips_biennium_tokens_and_finds_embedded_date(self):
        self.assertEqual(
            wa20.parse_dateish("2025-27-enacted-2025-05-20"), dt.date(2025, 5, 20)
        )

    def test_returns_none_without_date(self):
        self.assertIsNone(wa20.parse_dateish("no dates here"))


class CardFreshnessTest(unittest.TestCase):
    def test_prefers_data_through_over_snapshot_version(self):
        card = make_card()
        card["source_fingerprint"] = {
            "version_boundary": {
                "snapshot_version": "2026-06-01",
                "actual_data_through": "2026-04",
                "actual_data_through_label": "Through April 2026 (ignored)",
            }
        }
        self.assertEqual(wa20.card_freshness_date(card), dt.date(2026, 4, 1))

    def test_falls_back_to_snapshot_version(self):
        card = make_card()
        card["source_fingerprint"] = {
            "version_boundary": {"snapshot_version": "2026-04-01"}
        }
        self.assertEqual(wa20.card_freshness_date(card), dt.date(2026, 4, 1))

    def test_returns_none_without_fingerprint(self):
        self.assertIsNone(wa20.card_freshness_date(make_card()))


class AchievableModeTest(unittest.TestCase):
    def test_all_claims_supported_reaches_ceiling(self):
        result = wa20.evaluate_case(make_case(), [SUPPORTED_CARD], AS_OF)
        self.assertEqual(result["achievable_mode"], "exact")
        self.assertIsNone(result["error"])

    def test_no_core_support_is_unsupported_even_with_adjunct(self):
        case = make_case(
            expected_mode="unsupported_with_path",
            claims=[
                {
                    "jurisdiction": "Testville",
                    "category": "proposed:budget_finance.filed_annual_actuals",
                    "role": "core",
                },
                {
                    "jurisdiction": "Testville",
                    "category": "budget_finance.operating_budget",
                    "role": "adjunct",
                },
            ],
        )
        result = wa20.evaluate_case(case, [SUPPORTED_CARD], AS_OF)
        self.assertEqual(result["achievable_mode"], "unsupported_with_path")

    def test_some_core_supported_is_partial(self):
        case = make_case(
            expected_mode="partial",
            claims=[
                {
                    "jurisdiction": "Testville",
                    "category": "budget_finance.operating_budget",
                    "role": "core",
                },
                {
                    "jurisdiction": "Elsewhere",
                    "category": "budget_finance.operating_budget",
                    "role": "core",
                },
            ],
        )
        result = wa20.evaluate_case(case, [SUPPORTED_CARD], AS_OF)
        self.assertEqual(result["achievable_mode"], "partial")

    def test_missing_adjunct_caps_at_partial(self):
        case = make_case(
            expected_mode="partial",
            claims=[
                {
                    "jurisdiction": "Testville",
                    "category": "budget_finance.operating_budget",
                    "role": "core",
                },
                {
                    "jurisdiction": "Testville",
                    "category": "proposed:budget_finance.property_tax_levies",
                    "role": "adjunct",
                },
            ],
        )
        result = wa20.evaluate_case(case, [SUPPORTED_CARD], AS_OF)
        self.assertEqual(result["achievable_mode"], "partial")

    def test_ceiling_caps_fully_supported_case(self):
        case = make_case(expected_mode="partial", ceiling="partial")
        result = wa20.evaluate_case(case, [SUPPORTED_CARD], AS_OF)
        self.assertEqual(result["achievable_mode"], "partial")

    def test_partial_status_claim_counts_as_supporting(self):
        card = make_card(
            claims=[{"category": "budget_finance.operating_budget", "status": "partial"}]
        )
        result = wa20.evaluate_case(make_case(), [card], AS_OF)
        self.assertEqual(result["achievable_mode"], "exact")

    def test_unsupported_status_claim_does_not_support(self):
        card = make_card(
            claims=[
                {"category": "budget_finance.operating_budget", "status": "unsupported"}
            ]
        )
        case = make_case(expected_mode="unsupported_with_path")
        result = wa20.evaluate_case(case, [card], AS_OF)
        self.assertEqual(result["achievable_mode"], "unsupported_with_path")

    def test_coverage_jurisdictions_extend_card_reach(self):
        card = make_card(
            jurisdiction_name="State",
            coverage_jurisdictions=["State", "Testville"],
            claims=[
                {
                    "category": "population_demographics.population_denominator",
                    "status": "supported",
                }
            ],
        )
        case = make_case(
            claims=[
                {
                    "jurisdiction": "Testville",
                    "category": "population_demographics.population_denominator",
                    "role": "core",
                }
            ]
        )
        result = wa20.evaluate_case(case, [card], AS_OF)
        self.assertEqual(result["achievable_mode"], "exact")


class StalenessTest(unittest.TestCase):
    def test_stale_source_degrades_to_needs_refresh(self):
        card = make_card(
            claims=[{"category": "budget_finance.operating_budget", "status": "supported"}],
            data_through="2026-04",
        )
        case = make_case(expected_mode="needs_refresh", max_data_age_days=60)
        result = wa20.evaluate_case(case, [card], AS_OF)
        self.assertEqual(result["achievable_mode"], "needs_refresh")
        self.assertTrue(result["stale_sources"])

    def test_fresh_source_keeps_ceiling(self):
        card = make_card(
            claims=[{"category": "budget_finance.operating_budget", "status": "supported"}],
            data_through="2026-06",
        )
        case = make_case(max_data_age_days=60)
        result = wa20.evaluate_case(case, [card], AS_OF)
        self.assertEqual(result["achievable_mode"], "exact")

    def test_unknown_freshness_is_noted_not_stale(self):
        case = make_case(max_data_age_days=60)
        result = wa20.evaluate_case(case, [SUPPORTED_CARD], AS_OF)
        self.assertEqual(result["achievable_mode"], "exact")
        self.assertTrue(result["unknown_freshness"])

    def test_stale_note_is_day_stable(self):
        card = make_card(
            claims=[{"category": "budget_finance.operating_budget", "status": "supported"}],
            data_through="2026-04",
        )
        case = make_case(expected_mode="needs_refresh", max_data_age_days=60)
        note_a = wa20.evaluate_case(case, [card], AS_OF)["stale_sources"][0]
        note_b = wa20.evaluate_case(case, [card], AS_OF + dt.timedelta(days=30))[
            "stale_sources"
        ][0]
        self.assertEqual(note_a, note_b)


class ConsistencyTest(unittest.TestCase):
    def test_expectation_above_achievable_is_error(self):
        case = make_case(expected_mode="exact")
        result = wa20.evaluate_case(case, [], AS_OF)
        self.assertEqual(result["achievable_mode"], "unsupported_with_path")
        self.assertIsNotNone(result["error"])

    def test_coverage_exceeding_expectation_is_ratchet_candidate(self):
        case = make_case(expected_mode="unsupported_with_path")
        result = wa20.evaluate_case(case, [SUPPORTED_CARD], AS_OF)
        self.assertTrue(result["ratchet_candidate"])
        self.assertIsNone(result["error"])


class RatchetTest(unittest.TestCase):
    def base_case(self, mode="partial"):
        return {
            "id": "case-a",
            "question": "Original question?",
            "expected_answer_mode": mode,
        }

    def test_upgrade_passes_without_log(self):
        violations = wa20.ratchet_violations(
            [self.base_case("partial")],
            [{**self.base_case("exact")}],
            expectation_log="",
        )
        self.assertEqual(violations, [])

    def test_downgrade_without_log_entry_fails(self):
        violations = wa20.ratchet_violations(
            [self.base_case("exact")],
            [{**self.base_case("partial")}],
            expectation_log="",
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("downgraded", violations[0])

    def test_downgrade_with_log_entry_passes(self):
        violations = wa20.ratchet_violations(
            [self.base_case("exact")],
            [{**self.base_case("partial")}],
            expectation_log="## 2026-08-01\n- case-a: source retired upstream",
        )
        self.assertEqual(violations, [])

    def test_question_change_fails(self):
        changed = {**self.base_case("partial"), "question": "Different question?"}
        violations = wa20.ratchet_violations(
            [self.base_case("partial")], [changed], expectation_log=""
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("immutable", violations[0])

    def test_removal_without_log_entry_fails(self):
        violations = wa20.ratchet_violations(
            [self.base_case("partial")], [], expectation_log=""
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("removed", violations[0])


class SuiteIntegrationTest(unittest.TestCase):
    """Pinned-date evaluation of the real cases against real source cards."""

    @classmethod
    def setUpClass(cls):
        cls.evaluation = wa20.evaluate_suite(
            wa20.load_cases(), wa20.load_source_cards(), AS_OF
        )

    def test_no_consistency_errors_at_pinned_date(self):
        errors = [
            f"{result['id']}: {result['error']}" for result in self.evaluation["errors"]
        ]
        self.assertEqual(errors, [])

    def test_known_stable_cases(self):
        by_id = {result["id"]: result for result in self.evaluation["results"]}
        self.assertEqual(
            by_id["seattle-parks-2026-lookup"]["achievable_mode"], "exact"
        )
        # kc-property-tax-why-up's mode_ceiling is partial (parcel-level
        # answers are permanently out of scope), so this pin is stable.
        self.assertEqual(
            by_id["kc-property-tax-why-up"]["achievable_mode"], "partial"
        )

    def test_weighted_score_formula(self):
        weights = {
            "exact": 1.0,
            "partial": 0.5,
            "side_by_side_only": 0.5,
            "needs_refresh": 0.25,
            "unsupported_with_path": 0.0,
        }
        expected = sum(
            weights[result["achievable_mode"]] for result in self.evaluation["results"]
        )
        self.assertAlmostEqual(self.evaluation["weighted_score"], expected)

    def test_scoreboard_renders_and_is_checked_in(self):
        content = wa20.render_scoreboard(self.evaluation)
        self.assertIn("# WA-20 Tier 0 Coverage Scoreboard", content)
        self.assertTrue(SCOREBOARD_PATH.is_file(), "scoreboard.md must be checked in")


if __name__ == "__main__":
    unittest.main()
