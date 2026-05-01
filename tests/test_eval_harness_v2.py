"""Initiative 45 P1 — Tests for the unified eval harness v2.

Asserts:
- Backward compat: ``akos.eval_harness`` re-exports the I10 API unchanged
- v2 module: Scorecard schema + 4 mode runners
- CLI surface: ``scripts/eval.py`` list / --mode all / --json all PASS green-state
- Shims still work: ``scripts/eval_per_skill.py`` and ``scripts/run-evals.py``
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


# ── Backward compat ───────────────────────────────────────────────────────────


def test_back_compat_load_suite_importable() -> None:
    from akos.eval_harness import load_suite

    assert callable(load_suite)


def test_back_compat_score_rubric_task_importable() -> None:
    from akos.eval_harness import score_rubric_task

    assert callable(score_rubric_task)


def test_back_compat_list_suite_ids_returns_known_suites() -> None:
    from akos.eval_harness import list_suite_ids

    suites = list_suite_ids()
    assert "pathc-research-spine" in suites
    assert "madeira-operator-coverage" in suites


def test_back_compat_score_rubric_task_substring_match() -> None:
    from akos.eval_harness import score_rubric_task

    task = {"rubric": {"contains": ["foo"], "forbidden": ["bar"]}}
    status, fails = score_rubric_task(task, "the foo is here")
    assert status == "PASS"
    assert fails == []

    status, fails = score_rubric_task(task, "the bar is here")
    assert status == "FAIL"
    assert any("missing_contains:foo" in f for f in fails)
    assert any("forbidden_present:bar" in f for f in fails)


# ── v2 module ─────────────────────────────────────────────────────────────────


def test_v2_scorecard_dataclass_serializes_to_json() -> None:
    from akos.eval_harness.v2 import ScoreRow, Scorecard

    sc = Scorecard()
    sc.modes_run = ["smoke"]
    sc.add(ScoreRow(mode="smoke", skill_id="x", status="PASS"))
    s = sc.to_json()
    parsed = json.loads(s)
    assert parsed["schema_version"] == "1.0"
    assert parsed["overall_status"] == "pass"
    assert len(parsed["rows"]) == 1


def test_v2_scorecard_fail_propagates_to_overall() -> None:
    from akos.eval_harness.v2 import ScoreRow, Scorecard

    sc = Scorecard()
    sc.add(ScoreRow(mode="smoke", skill_id="x", status="PASS"))
    sc.add(ScoreRow(mode="canary", skill_id="y", status="FAIL", failures=["bad"]))
    parsed = json.loads(sc.to_json())
    assert parsed["overall_status"] == "fail"


def test_v2_scorecard_markdown_has_table_header() -> None:
    from akos.eval_harness.v2 import Scorecard

    sc = Scorecard()
    md = sc.to_markdown()
    assert "| mode | skill_id" in md
    assert "overall_status" in md


def test_v2_run_canary_returns_5_skill_rows() -> None:
    from akos.eval_harness.v2 import Scorecard, run_canary

    sc = Scorecard()
    run_canary(sc)
    skill_rows = [r for r in sc.rows if r.mode == "canary"]
    assert len(skill_rows) == 5
    assert all(r.status == "PASS" for r in skill_rows)


def test_v2_run_canary_trips_on_synthetic_regression() -> None:
    from akos.eval_harness.v2 import Scorecard, run_canary

    sc = Scorecard()
    run_canary(sc, threshold_pp=2.0, overrides={"SKILL-MADEIRA-LOOKUP-V1": 80.0})
    madeira = next(r for r in sc.rows if r.skill_id == "SKILL-MADEIRA-LOOKUP-V1")
    assert madeira.canary_2_tripped is True
    assert madeira.status == "FAIL"
    assert any("canary_2_regression" in f for f in madeira.failures)


def test_v2_run_smoke_passes_in_clean_state() -> None:
    from akos.eval_harness.v2 import Scorecard, run_smoke

    sc = Scorecard()
    run_smoke(sc)
    smoke_rows = [r for r in sc.rows if r.mode == "smoke"]
    fails = [r for r in smoke_rows if r.status == "FAIL"]
    assert len(smoke_rows) >= 7, f"expected >=7 smoke probes, got {len(smoke_rows)}"
    assert not fails, f"smoke regressions: {[(r.skill_id, r.failures) for r in fails]}"


def test_v2_run_rubric_returns_known_suites() -> None:
    from akos.eval_harness.v2 import Scorecard, run_rubric

    sc = Scorecard()
    run_rubric(sc)
    rubric_rows = [r for r in sc.rows if r.mode == "rubric"]
    assert any(r.skill_id == "suite:pathc-research-spine" for r in rubric_rows)
    assert any(r.skill_id == "suite:madeira-operator-coverage" for r in rubric_rows)


def test_v2_run_replay_skips_when_cassette_root_empty_or_missing() -> None:
    from akos.eval_harness.v2 import Scorecard, run_replay

    sc = Scorecard()
    run_replay(sc)
    rep = [r for r in sc.rows if r.mode == "replay"]
    assert len(rep) >= 1
    assert all(r.status == "SKIP" for r in rep)


def test_v2_run_modes_all_combines_smoke_canary_rubric() -> None:
    from akos.eval_harness.v2 import run_modes

    sc = run_modes(["all"])
    modes = {r.mode for r in sc.rows}
    assert modes == {"smoke", "canary", "rubric"}, f"unexpected modes: {modes}"
    assert sc.overall_status == "pass"


# ── CLI surface ───────────────────────────────────────────────────────────────


def _run_cli(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    import os

    cli_env = os.environ.copy()
    cli_env["AKOS_EVAL_NO_DEPRECATION_WARN"] = "1"
    if env:
        cli_env.update(env)
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "eval.py"), *args],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
        env=cli_env,
    )


def test_cli_list_returns_zero_and_lists_5_skills() -> None:
    p = _run_cli("list")
    assert p.returncode == 0
    assert "Skills in SKILL_REGISTRY.csv (5)" in p.stdout
    assert "SKILL-MADEIRA-LOOKUP-V1" in p.stdout


def test_cli_mode_all_json_emits_valid_scorecard_with_overall_pass() -> None:
    p = _run_cli("--mode", "all", "--json")
    assert p.returncode == 0
    parsed = json.loads(p.stdout)
    assert parsed["overall_status"] == "pass"
    assert set(parsed["modes_run"]) == {"smoke", "canary", "rubric"}
    assert len(parsed["rows"]) >= 12  # >=7 smoke + 5 canary + 2 rubric


def test_cli_mode_canary_with_synthetic_regression_exits_1() -> None:
    p = _run_cli(
        "--mode", "canary", "--current", "SKILL-MADEIRA-LOOKUP-V1=80.0", "--json"
    )
    assert p.returncode == 1, f"expected 1, got {p.returncode} stdout={p.stdout[:200]}"
    parsed = json.loads(p.stdout)
    assert parsed["overall_status"] == "fail"
    madeira = next(r for r in parsed["rows"] if r["skill_id"] == "SKILL-MADEIRA-LOOKUP-V1")
    assert madeira["canary_2_tripped"] is True


def test_cli_mode_replay_alone_skips_and_exits_zero() -> None:
    p = _run_cli("--mode", "replay", "--json")
    assert p.returncode == 0
    parsed = json.loads(p.stdout)
    rep = [r for r in parsed["rows"] if r["mode"] == "replay"]
    assert all(r["status"] == "SKIP" for r in rep)


def test_cli_record_without_live_env_exits_2() -> None:
    p = _run_cli("record", "--skill", "SKILL-MADEIRA-LOOKUP-V1")
    assert p.returncode == 2
    assert "AKOS_RECORD_LIVE=1" in p.stderr


# ── Shim back-compat (CLI level) ──────────────────────────────────────────────


def test_shim_eval_per_skill_still_runs() -> None:
    import os

    cli_env = os.environ.copy()
    cli_env["AKOS_EVAL_NO_DEPRECATION_WARN"] = "1"
    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "eval_per_skill.py"), "--json"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=REPO_ROOT,
        env=cli_env,
    )
    assert p.returncode == 0
    parsed = json.loads(p.stdout)
    assert parsed["overall_status"] == "pass"
    assert parsed["skills_total"] == 5


def test_shim_run_evals_list_still_runs() -> None:
    import os

    cli_env = os.environ.copy()
    cli_env["AKOS_EVAL_NO_DEPRECATION_WARN"] = "1"
    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "run-evals.py"), "list"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=REPO_ROOT,
        env=cli_env,
    )
    assert p.returncode == 0
    assert "pathc-research-spine" in p.stdout


# ── Drift checks (catch regressions in the unification contract) ──────────────


def test_eval_harness_module_is_a_package_not_file() -> None:
    """If someone reverts P1, this fails fast."""
    import akos.eval_harness as eh

    assert hasattr(eh, "__path__"), "akos.eval_harness must be a package, not a single file"


def test_v2_module_exists_under_eval_harness_package() -> None:
    from akos.eval_harness import v2

    assert hasattr(v2, "Scorecard")
    assert hasattr(v2, "run_modes")
    assert hasattr(v2, "VALID_MODES")
    assert "smoke" in v2.VALID_MODES
    assert "rubric" in v2.VALID_MODES
    assert "canary" in v2.VALID_MODES
    assert "replay" in v2.VALID_MODES
    assert "all" in v2.VALID_MODES
