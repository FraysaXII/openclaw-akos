"""Initiative 47 P10 tests — per-persona scorecard + difficulty calibration meta-eval.

Coverage:
- ScoreRow extended fields (persona_id / difficulty_class / scenario_class / judge_scores)
- Scorecard.to_markdown emits per-persona section when ANY row has persona_id
- Scorecard.to_markdown emits LLM-judge section when ANY row has judge_scores
- akos.eval_harness.persona helpers: load, filter, aggregate, calibration
- scripts/calibrate_scenarios.py CLI surface
- scripts/eval.py --persona / --difficulty / --calibrate flags
- Supabase migration shape (column presence + indexes)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.eval_harness.persona import (
    CALIBRATION_TARGET,
    CALIBRATION_TOLERANCE_PP,
    aggregate_by_persona,
    calibration_distribution,
    filter_scenarios,
    load_persona_scenarios,
    render_calibration_markdown,
)
from akos.eval_harness.v2 import ScoreRow, Scorecard

CALIBRATE_SCRIPT = REPO_ROOT / "scripts" / "calibrate_scenarios.py"
EVAL_SCRIPT = REPO_ROOT / "scripts" / "eval.py"
MIGRATION = REPO_ROOT / "supabase" / "migrations" / "20260502033500_i47_eval_run_persona_columns.sql"


# ---------------------------------------------------------------------------
# ScoreRow extended fields (D-IH-47-F)
# ---------------------------------------------------------------------------

def test_scorerow_has_p10_fields() -> None:
    """ScoreRow must carry persona_id, difficulty_class, scenario_class, judge_scores."""
    r = ScoreRow(
        mode="canary",
        skill_id="SKILL-MADEIRA-LOOKUP-V1",
        persona_id="PERSONA-INVESTOR-COLD",
        difficulty_class="hard",
        scenario_class="multihop",
        judge_scores={"brand_voice": 4, "citation": 5, "persona_fit": 4},
    )
    assert r.persona_id == "PERSONA-INVESTOR-COLD"
    assert r.difficulty_class == "hard"
    assert r.scenario_class == "multihop"
    assert r.judge_scores == {"brand_voice": 4, "citation": 5, "persona_fit": 4}


def test_scorerow_p10_fields_default_safely() -> None:
    """Existing ScoreRow consumers must continue working (back-compat)."""
    r = ScoreRow(mode="canary", skill_id="SKILL-X")
    assert r.persona_id is None
    assert r.difficulty_class is None
    assert r.scenario_class is None
    assert r.judge_scores == {}


# ---------------------------------------------------------------------------
# Scorecard to_markdown extensions (D-IH-47-F + D-IH-47-J)
# ---------------------------------------------------------------------------

def test_to_markdown_shows_per_persona_when_persona_id_set() -> None:
    sc = Scorecard()
    sc.modes_run = ["canary"]
    sc.add(ScoreRow(mode="canary", skill_id="S1", persona_id="OPERATOR", difficulty_class="trivial", status="PASS"))
    sc.add(ScoreRow(mode="canary", skill_id="S1", persona_id="OPERATOR", difficulty_class="hard", status="FAIL"))
    sc.add(ScoreRow(mode="canary", skill_id="S2", persona_id="PERSONA-INVESTOR-COLD", difficulty_class="hard", status="PASS"))
    md = sc.to_markdown()
    assert "Per-persona breakdown" in md
    assert "OPERATOR" in md
    assert "PERSONA-INVESTOR-COLD" in md


def test_to_markdown_skips_per_persona_when_no_persona_rows() -> None:
    sc = Scorecard()
    sc.add(ScoreRow(mode="rubric", skill_id="__suite__", status="PASS"))
    md = sc.to_markdown()
    assert "Per-persona breakdown" not in md


def test_to_markdown_shows_judge_axis_when_judge_scores_present() -> None:
    sc = Scorecard()
    sc.add(ScoreRow(mode="canary", skill_id="S1", judge_scores={"brand_voice": 5, "citation": 4, "persona_fit": 4}))
    sc.add(ScoreRow(mode="canary", skill_id="S2", judge_scores={"brand_voice": 3, "citation": 5, "persona_fit": 4}))
    md = sc.to_markdown()
    assert "LLM-judge 3-axis" in md
    assert "brand_voice" in md
    assert "citation" in md
    assert "persona_fit" in md


# ---------------------------------------------------------------------------
# persona aggregator helpers
# ---------------------------------------------------------------------------

def test_load_persona_scenarios_returns_active_rows() -> None:
    rows = load_persona_scenarios()
    assert len(rows) >= 200, "P9 should have produced ≥200 scenarios"
    assert all("scenario_id" in r for r in rows)


def test_filter_scenarios_by_persona() -> None:
    rows = load_persona_scenarios()
    operator = filter_scenarios(rows, persona_id="OPERATOR")
    assert len(operator) >= 20, "operator P2 library has ≥20 scenarios"
    assert all(r["persona_id"] == "OPERATOR" for r in operator)


def test_filter_scenarios_by_multiple_dims() -> None:
    rows = load_persona_scenarios()
    hard_inv_cold = filter_scenarios(rows, persona_id="PERSONA-INVESTOR-COLD", difficulty_class="hard")
    assert len(hard_inv_cold) >= 5
    assert all(r["persona_id"] == "PERSONA-INVESTOR-COLD" for r in hard_inv_cold)
    assert all(r["difficulty_class"] == "hard" for r in hard_inv_cold)


def test_filter_scenarios_excludes_deprecated_by_default() -> None:
    rows = load_persona_scenarios()
    # Inject a deprecated-row (in-memory only)
    rows_with_deprecated = rows + [{**rows[0], "scenario_id": "SCN-TEST-DEP-V1", "lifecycle_status": "deprecated"}]
    active = filter_scenarios(rows_with_deprecated)
    assert all((r.get("lifecycle_status") or "active") == "active" for r in active)


def test_aggregate_by_persona() -> None:
    rows = [
        ScoreRow(mode="canary", skill_id="X", persona_id="OPERATOR", difficulty_class="hard", status="PASS"),
        ScoreRow(mode="canary", skill_id="X", persona_id="OPERATOR", difficulty_class="trivial", status="PASS"),
        ScoreRow(mode="canary", skill_id="X", persona_id="OPERATOR", difficulty_class="hard", status="FAIL"),
        ScoreRow(mode="canary", skill_id="X", persona_id="PERSONA-INVESTOR-COLD", difficulty_class="moderate", status="SKIP"),
    ]
    agg = aggregate_by_persona(rows)
    assert agg["OPERATOR"]["total"] == 3
    assert agg["OPERATOR"]["PASS"] == 2
    assert agg["OPERATOR"]["FAIL"] == 1
    assert agg["OPERATOR"]["hard"] == 2
    assert agg["OPERATOR"]["trivial"] == 1
    assert agg["PERSONA-INVESTOR-COLD"]["SKIP"] == 1


def test_aggregate_by_persona_handles_missing_persona() -> None:
    rows = [ScoreRow(mode="rubric", skill_id="__suite__", status="PASS")]
    agg = aggregate_by_persona(rows)
    assert "__no_persona__" in agg
    assert agg["__no_persona__"]["total"] == 1


# ---------------------------------------------------------------------------
# calibration distribution
# ---------------------------------------------------------------------------

def test_calibration_target_constants() -> None:
    """D-IH-47-C: 40/40/10/10."""
    assert CALIBRATION_TARGET["hard"] == 40.0
    assert CALIBRATION_TARGET["moderate"] == 40.0
    assert CALIBRATION_TARGET["trivial"] == 10.0
    assert CALIBRATION_TARGET["impossible"] == 10.0
    assert CALIBRATION_TOLERANCE_PP == 5.0


def test_calibration_distribution_overall_passes() -> None:
    """The cumulative library is within ±5pp of D-IH-47-C target."""
    results = calibration_distribution()
    overall = results["__overall__"]
    assert overall.overall_pass, (
        f"overall calibration FAIL: {overall.pct} (deltas: {overall.deltas_pp})"
    )


def test_calibration_distribution_per_persona_includes_all_personas() -> None:
    results = calibration_distribution()
    # Should include OPERATOR + 16 PERSONA_REGISTRY archetypes + __overall__
    persona_keys = {k for k in results if k != "__overall__"}
    assert "OPERATOR" in persona_keys
    assert "PERSONA-INVESTOR-COLD" in persona_keys
    assert len(persona_keys) >= 16  # all 16 + OPERATOR


def test_render_calibration_markdown_contains_overall_first() -> None:
    results = calibration_distribution()
    md = render_calibration_markdown(results)
    assert "Calibration distribution" in md
    assert "tolerance" in md.lower()
    overall_idx = md.find("__overall__")
    operator_idx = md.find("OPERATOR")
    assert overall_idx >= 0 and operator_idx >= 0
    assert overall_idx < operator_idx, "__overall__ row should appear first"


# ---------------------------------------------------------------------------
# CLI surfaces
# ---------------------------------------------------------------------------

def test_calibrate_script_cli_runs_and_writes_artifact() -> None:
    proc = subprocess.run(
        [sys.executable, str(CALIBRATE_SCRIPT), "--quiet"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    # Exit 0 even if some personas drift (warn-only by default)
    assert proc.returncode == 0
    assert "Calibration report written" in proc.stdout


def test_calibrate_script_filters_to_persona() -> None:
    proc = subprocess.run(
        [sys.executable, str(CALIBRATE_SCRIPT), "--persona", "OPERATOR", "--quiet"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 0


def test_calibrate_script_unknown_persona_fails() -> None:
    proc = subprocess.run(
        [sys.executable, str(CALIBRATE_SCRIPT), "--persona", "PERSONA-NONE-EXISTS", "--quiet"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 1


def test_eval_script_calibrate_flag() -> None:
    proc = subprocess.run(
        [sys.executable, str(EVAL_SCRIPT), "--calibrate"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 0
    assert "Calibration distribution" in proc.stdout
    assert "OPERATOR" in proc.stdout


def test_eval_script_persona_filter_argparse_only() -> None:
    """Verify --persona/--difficulty are accepted by argparse (smoke)."""
    proc = subprocess.run(
        [sys.executable, str(EVAL_SCRIPT), "--help"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 0
    assert "--persona" in proc.stdout
    assert "--difficulty" in proc.stdout
    assert "--calibrate" in proc.stdout
    assert "--judge-cost-cap" in proc.stdout


def test_calibrate_script_help_lists_write_priority_scores_flag() -> None:
    proc = subprocess.run(
        [sys.executable, str(CALIBRATE_SCRIPT), "--help"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 0
    assert "--write-priority-scores" in proc.stdout


# ---------------------------------------------------------------------------
# Supabase migration shape (D-IH-47-F + D-IH-47-J)
# ---------------------------------------------------------------------------

def test_migration_file_exists() -> None:
    assert MIGRATION.is_file()


def test_migration_adds_p10_columns() -> None:
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    for col in ("persona_id", "difficulty_class", "scenario_class", "judge_scores"):
        assert col in sql, f"migration missing column {col}"
    assert "jsonb" in sql, "judge_scores must be JSONB per D-IH-47-J"
    assert "add column if not exists" in sql, "must use additive ALTER for back-compat"


def test_migration_creates_indexes() -> None:
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    assert "eval_run_persona_id_idx" in sql
    assert "eval_run_difficulty_class_idx" in sql
    assert "eval_run_persona_difficulty_idx" in sql
    assert "where persona_id is not null" in sql


def test_migration_preserves_rls() -> None:
    sql = MIGRATION.read_text(encoding="utf-8").lower()
    assert "row level security" in sql
    assert "deny_authenticated" in sql
    assert "deny_anon" in sql
    assert "service_role" in sql


# ---------------------------------------------------------------------------
# Cumulative end-to-end sanity
# ---------------------------------------------------------------------------

def test_existing_validate_hlk_still_passes() -> None:
    """P10 wiring must not break existing validators."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "validate_hlk.py")],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OVERALL: PASS" in proc.stdout
