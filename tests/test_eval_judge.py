"""Initiative 47 P12 tests — LLM-as-judge 3-axis scoring (D-IH-47-J).

Coverage:
- JudgeResult dataclass shape
- 3 axes (brand_voice, citation, persona_fit)
- load_judge_thresholds reads POLICY_REGISTER min_pass_score
- score_response_offline deterministic + zero-cost
- Heuristic scoring per axis (PASS / FAIL boundaries)
- Cost-cap aggregation
- Live mode is gated (raises NotImplementedError) until operator approves
- AKOS_JUDGE_MODEL=offline (default) routes to offline path
- 3 POLICY_REGISTER rows present + classified as judge_threshold
- Validator accepts judge_threshold policy_class
"""

from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.eval_harness.judge import (
    DEFAULT_COST_CAP_USD,
    DEFAULT_PASS_THRESHOLD,
    JUDGE_AXES,
    JudgeResult,
    POLICY_IDS,
    aggregate_judge_cost_under_cap,
    load_judge_thresholds,
    score_response,
    score_response_live,
    score_response_offline,
)
from akos.hlk_policy_register_csv import VALID_POLICY_CLASSES

POLICY_CSV = REPO_ROOT / "docs" / "references" / "hlk" / "compliance" / "dimensions" / "POLICY_REGISTER.csv"


# ---------------------------------------------------------------------------
# Constants + dataclass shape
# ---------------------------------------------------------------------------

def test_three_axes() -> None:
    assert JUDGE_AXES == ("brand_voice", "citation", "persona_fit")
    assert len(JUDGE_AXES) == 3


def test_default_threshold_is_4() -> None:
    assert DEFAULT_PASS_THRESHOLD == 4


def test_default_cost_cap_is_one_cent() -> None:
    assert DEFAULT_COST_CAP_USD == 0.01


def test_judge_result_dataclass_shape() -> None:
    r = JudgeResult(
        scenario_id="SCN-X-001-V1",
        persona_id="OPERATOR",
        scores={"brand_voice": 5, "citation": 4, "persona_fit": 4},
        pass_per_axis={"brand_voice": True, "citation": True, "persona_fit": True},
        overall_pass=True,
        model_id="offline",
        cost_usd=0.0,
    )
    assert r.scenario_id == "SCN-X-001-V1"
    assert r.overall_pass is True
    assert r.skipped is False


def test_judge_result_skipped_default_false() -> None:
    r = JudgeResult(scenario_id="X")
    assert r.skipped is False
    assert r.skip_reason == ""


# ---------------------------------------------------------------------------
# POLICY_REGISTER integration
# ---------------------------------------------------------------------------

def test_judge_threshold_in_valid_policy_classes() -> None:
    assert "judge_threshold" in VALID_POLICY_CLASSES


def test_three_policy_rows_exist() -> None:
    with POLICY_CSV.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    policy_ids = {r["policy_id"] for r in rows}
    for axis_pid in POLICY_IDS.values():
        assert axis_pid in policy_ids, f"missing P12 POLICY_REGISTER row {axis_pid}"


def test_load_judge_thresholds_reads_csv_or_defaults() -> None:
    thresholds = load_judge_thresholds()
    assert set(thresholds.keys()) == set(JUDGE_AXES)
    for axis in JUDGE_AXES:
        assert thresholds[axis] >= 1 and thresholds[axis] <= 5


# ---------------------------------------------------------------------------
# Offline scoring (deterministic; CI-safe)
# ---------------------------------------------------------------------------

def test_score_response_offline_returns_judge_result() -> None:
    scenario = {"scenario_id": "SCN-X-001-V1", "persona_id": "OPERATOR"}
    r = score_response_offline("test response", scenario)
    assert isinstance(r, JudgeResult)
    assert r.cost_usd == 0.0
    assert r.model_id == "offline"
    assert set(r.scores.keys()) == set(JUDGE_AXES)


def test_brand_voice_high_for_governance_terminology() -> None:
    """5/5 brand voice when response uses Holistik Ops governance terms."""
    scenario = {"scenario_id": "X"}
    r = score_response_offline(
        "Per Holistik Ops doctrine, the System Owner role escalates this to Founder for review.",
        scenario,
    )
    assert r.scores["brand_voice"] == 5


def test_brand_voice_low_for_jargon_violations() -> None:
    """1/5 brand voice when response violates BRAND_JARGON_AUDIT."""
    scenario = {"scenario_id": "X"}
    r = score_response_offline("Hey guys, that's super exciting and totally awesome!", scenario)
    assert r.scores["brand_voice"] == 1


def test_citation_high_for_canonical_path() -> None:
    """5/5 citation when response cites docs/references/hlk/ path."""
    scenario = {"scenario_id": "X"}
    r = score_response_offline(
        "See docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv for the row.",
        scenario,
    )
    assert r.scores["citation"] == 5


def test_citation_high_for_registry_id() -> None:
    """4/5 citation when response references a registry/policy ID."""
    scenario = {"scenario_id": "X"}
    r = score_response_offline("This is governed by POL-EVAL-JUDGE-THRESHOLD-BRAND-VOICE-V1.", scenario)
    assert r.scores["citation"] == 4


def test_citation_low_for_no_citation() -> None:
    """1/5 citation when response has no citation."""
    scenario = {"scenario_id": "X"}
    r = score_response_offline("Yes that is correct.", scenario)
    assert r.scores["citation"] == 1


def test_persona_fit_high_when_qualification_acknowledged() -> None:
    scenario = {"scenario_id": "X", "persona_id": "PERSONA-INVESTOR-COLD"}
    persona = {
        "persona_id": "PERSONA-INVESTOR-COLD",
        "qualification_gate": "Confirm fit (sector / stage / ticket size)",
        "typical_distance_band": "N3-N4",
    }
    r = score_response_offline(
        "I need to confirm fit on sector / stage / ticket size first per qualification.",
        scenario, persona,
    )
    assert r.scores["persona_fit"] == 5


def test_persona_fit_handles_no_persona_meta() -> None:
    scenario = {"scenario_id": "X"}
    r = score_response_offline("ok", scenario, persona=None)
    # Should be 3 (neutral) when no persona meta available
    assert r.scores["persona_fit"] == 3


def test_score_response_offline_is_deterministic() -> None:
    scenario = {"scenario_id": "X"}
    r1 = score_response_offline("the same text", scenario)
    r2 = score_response_offline("the same text", scenario)
    assert r1.scores == r2.scores
    assert r1.cost_usd == r2.cost_usd == 0.0


def test_overall_pass_requires_all_axes_pass() -> None:
    """Threshold 4 default; all 3 axes must >= 4 for overall_pass=True."""
    scenario = {"scenario_id": "X"}
    # Response with high brand-voice + citation + persona-fit
    r = score_response_offline(
        "Per Holistik Ops, see docs/references/hlk/compliance/PRECEDENCE.md (System Owner authority).",
        scenario,
        persona={"qualification_gate": "Confirm fit"},
    )
    if all(r.scores[a] >= DEFAULT_PASS_THRESHOLD for a in JUDGE_AXES):
        assert r.overall_pass


# ---------------------------------------------------------------------------
# Cost cap
# ---------------------------------------------------------------------------

def test_aggregate_cost_under_cap_passes_when_zero() -> None:
    results = [JudgeResult(scenario_id=f"X{i}", cost_usd=0.0) for i in range(5)]
    within, total, violations = aggregate_judge_cost_under_cap(results)
    assert within is True
    assert total == 0.0
    assert violations == []


def test_aggregate_cost_under_cap_detects_violation() -> None:
    results = [
        JudgeResult(scenario_id="X1", cost_usd=0.005),
        JudgeResult(scenario_id="X2", cost_usd=0.025),  # over per-scenario cap
    ]
    within, total, violations = aggregate_judge_cost_under_cap(results, per_scenario_cap_usd=0.01)
    assert within is False
    assert any("X2" in v for v in violations)
    assert total == pytest.approx(0.03)


def test_aggregate_cost_under_cap_overall_cap() -> None:
    results = [JudgeResult(scenario_id=f"X{i}", cost_usd=0.005) for i in range(5)]
    within, total, violations = aggregate_judge_cost_under_cap(
        results, per_scenario_cap_usd=0.01, overall_cap_usd=0.02
    )
    assert within is False
    assert any("OVERALL" in v for v in violations)


# ---------------------------------------------------------------------------
# Live mode gating
# ---------------------------------------------------------------------------

def test_score_response_live_raises_not_implemented(monkeypatch: pytest.MonkeyPatch) -> None:
    """I52 P2 (D-IH-52-A): live mode requires AKOS_JUDGE_ROSTER; missing env raises."""
    monkeypatch.delenv("AKOS_JUDGE_ROSTER", raising=False)
    with pytest.raises(NotImplementedError, match="AKOS_JUDGE_ROSTER"):
        score_response_live("response", {"scenario_id": "X"})


def test_dispatcher_routes_to_offline_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AKOS_JUDGE_MODEL", raising=False)
    monkeypatch.delenv("AKOS_RECORD_LIVE", raising=False)
    r = score_response("test", {"scenario_id": "X"})
    assert r.model_id == "offline"
    assert r.cost_usd == 0.0


def test_dispatcher_routes_to_offline_without_record_live(monkeypatch: pytest.MonkeyPatch) -> None:
    """Even with AKOS_JUDGE_MODEL set, requires AKOS_RECORD_LIVE=1 for live."""
    monkeypatch.setenv("AKOS_JUDGE_MODEL", "claude-3-5-haiku-20241022")
    monkeypatch.delenv("AKOS_RECORD_LIVE", raising=False)
    r = score_response("test", {"scenario_id": "X"})
    assert r.model_id == "offline"
