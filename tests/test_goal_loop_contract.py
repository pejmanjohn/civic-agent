import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GOAL_README = ROOT / "docs" / "goals" / "README.md"
GOAL_BRIEF_TEMPLATE = ROOT / "docs" / "goals" / "templates" / "civic-agent-goal-brief.md"
POST_EVAL_TEMPLATE = ROOT / "docs" / "goals" / "templates" / "civic-agent-post-eval.md"
FAILURE_MODES = ROOT / "docs" / "goals" / "failure-modes.md"
SCORING_RUBRIC = ROOT / "docs" / "goals" / "eval-scoring-rubric.md"
PROCESS_DOC = ROOT / "docs" / "processes" / "civic-agent-improvement-loop.md"
GOAL_SKILL = ROOT / "skills" / "civic-agent-goal" / "SKILL.md"

REQUIRED_FILES = [
    GOAL_README,
    GOAL_BRIEF_TEMPLATE,
    POST_EVAL_TEMPLATE,
    FAILURE_MODES,
    SCORING_RUBRIC,
    PROCESS_DOC,
    GOAL_SKILL,
]

GOAL_BRIEF_HEADINGS = [
    "## Trigger",
    "## Evidence Inputs",
    "## Raw Observations",
    "## Plugin vs Baseline Gap",
    "## Failure Modes",
    "## Blind Review Summary",
    "## Extracted Principles",
    "## Ranked Goals",
    "## Contract Changes Needed",
    "## Milestone Queue",
    "## Expected Eval Movement",
    "## Handoff Prompt For /ce-plan",
]

POST_EVAL_HEADINGS = [
    "## Implementation Under Test",
    "## Eval Method",
    "## Score Delta",
    "## Average",
    "## What Improved",
    "## What Did Not Improve Much",
    "## Regressions",
    "## Scorer Gaps",
    "## Next Goal Recommendations",
]

EXPECTED_FAILURE_MODES = [
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
]

EXPECTED_SCORE_DIMENSIONS = [
    "correctness",
    "traceability",
    "coverage_awareness",
    "comparability",
    "civic_usefulness",
    "freshness",
    "improvement_path",
]


def read(path):
    return path.read_text(encoding="utf-8")


class GoalLoopContractTest(unittest.TestCase):
    def test_goal_loop_artifacts_exist(self):
        for path in REQUIRED_FILES:
            self.assertTrue(path.is_file(), path.relative_to(ROOT))

    def test_goal_brief_template_keeps_required_sections(self):
        text = read(GOAL_BRIEF_TEMPLATE)
        for heading in GOAL_BRIEF_HEADINGS:
            self.assertIn(heading, text)
        self.assertIn("| Question | Plugin behavior | Baseline behavior | Gap |", text)
        self.assertIn("| Case | Expected improvement | Why |", text)

    def test_post_eval_template_records_validity_and_score_deltas(self):
        text = read(POST_EVAL_TEMPLATE)
        for heading in POST_EVAL_HEADINGS:
            self.assertIn(heading, text)
        for phrase in (
            "Plugin package:",
            "Dev install verified:",
            "Production install status:",
            "| Case | Old | New | Delta | Improved? | Notes |",
            "Old arithmetic average:",
        ):
            self.assertIn(phrase, text)

    def test_failure_mode_vocab_includes_eval_validity_gaps(self):
        text = read(FAILURE_MODES)
        for mode in EXPECTED_FAILURE_MODES:
            self.assertIn(f"`{mode}`", text)

    def test_scoring_rubric_matches_scale_dimensions(self):
        text = read(SCORING_RUBRIC)
        for dimension in EXPECTED_SCORE_DIMENSIONS:
            self.assertIn(f"`{dimension}`", text)
        self.assertIn("0", text)
        self.assertIn("5", text)

    def test_goal_skill_is_non_mutating_and_points_to_templates(self):
        text = read(GOAL_SKILL)
        self.assertIn("name: civic-agent-goal", text)
        self.assertIn("Non-mutating", text)
        self.assertIn("docs/goals/templates/civic-agent-goal-brief.md", text)
        self.assertIn("docs/goals/templates/civic-agent-post-eval.md", text)
        self.assertIn("docs/processes/civic-agent-improvement-loop.md", text)


if __name__ == "__main__":
    unittest.main()
