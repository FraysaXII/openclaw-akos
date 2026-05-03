"""Initiative 52 P6 — Tests for judge-axes + endpoint cost dossier surfaces.

Covers:
- gather_madeira_judge_axis_fail_summary: empty-artifact fallback, status-key
  shapes, score-threshold path, worst-axis selection
- gather_madeira_endpoint_cost_summary: missing-probe, present-probe,
  worst-status ranking, operator-action one-liners
- Section03EvalHealth render adds judge-axis subsection on madeira flavor
- Section04PersonaCalibration render adds worst-axis cross-reference
- Section08OperationalHealth render adds endpoint cost subsection
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.dossier import (
    DossierFilter,
    Section03EvalHealth,
    Section04PersonaCalibration,
    Section08OperationalHealth,
    SectionData,
    dossier_filter_madeira_preset,
)
from akos.dossier import sources as dossier_sources


# ── gather_madeira_judge_axis_fail_summary ─────────────────────────────────────


def test_judge_axis_summary_empty_when_no_artifact(tmp_path: Path) -> None:
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_judge_axis_fail_summary()
    assert out["per_axis_fail_count"] == {
        "brand_voice": 0,
        "citation": 0,
        "persona_fit": 0,
    }
    assert out["worst_axis"] is None
    assert out["judge_member_ids"] == []


def test_judge_axis_summary_status_keys(tmp_path: Path) -> None:
    history = tmp_path / "eval-history"
    history.mkdir()
    (history / "eval-scorecard-2026-05-03T00-00-00Z.json").write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "judge_brand_voice_status": "FAIL",
                        "judge_citation_status": "PASS",
                        "judge_persona_fit_status": "FAIL",
                        "judge_member_ids": [
                            "anthropic:claude-3-5-sonnet-20241022",
                            "openai:gpt-4o",
                        ],
                    },
                    {
                        "judge_brand_voice_status": "FAIL",
                        "judge_citation_status": "PASS",
                        "judge_persona_fit_status": "PASS",
                        "judge_member_ids": "anthropic:claude-3-5-sonnet-20241022,openai:gpt-4o",
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_judge_axis_fail_summary()
    assert out["per_axis_fail_count"] == {
        "brand_voice": 2,
        "citation": 0,
        "persona_fit": 1,
    }
    assert out["per_axis_total"] == {
        "brand_voice": 2,
        "citation": 2,
        "persona_fit": 2,
    }
    assert out["worst_axis"] == "brand_voice"
    assert out["worst_axis_fail_count"] == 2
    assert "anthropic:claude-3-5-sonnet-20241022" in out["judge_member_ids"]
    assert "openai:gpt-4o" in out["judge_member_ids"]


def test_judge_axis_summary_score_threshold_path(tmp_path: Path) -> None:
    history = tmp_path / "eval-history"
    history.mkdir()
    (history / "eval-scorecard-x.json").write_text(
        json.dumps(
            {
                "rows": [
                    {
                        "judge_brand_voice_score": 5,
                        "judge_citation_score": 3,
                        "judge_persona_fit_score": 2,
                    },
                    {
                        "judge_brand_voice_score": 4,
                        "judge_citation_score": 4,
                        "judge_persona_fit_score": 3,
                    },
                ]
            }
        ),
        encoding="utf-8",
    )
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_judge_axis_fail_summary()
    # min_pass_score = 4 (POL-EVAL-JUDGE-THRESHOLD-*-V1).
    # row 1: brand_voice=5 PASS, citation=3 FAIL, persona_fit=2 FAIL
    # row 2: brand_voice=4 PASS, citation=4 PASS, persona_fit=3 FAIL
    assert out["per_axis_fail_count"] == {
        "brand_voice": 0,
        "citation": 1,
        "persona_fit": 2,
    }
    assert out["worst_axis"] == "persona_fit"


def test_judge_axis_summary_no_judge_rows_returns_clean_zeros(
    tmp_path: Path,
) -> None:
    history = tmp_path / "eval-history"
    history.mkdir()
    (history / "eval-scorecard-x.json").write_text(
        json.dumps({"rows": [{"persona_id": "OPERATOR", "cost_usd": 0.001}]}),
        encoding="utf-8",
    )
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_judge_axis_fail_summary()
    assert out["per_axis_fail_count"] == {
        "brand_voice": 0,
        "citation": 0,
        "persona_fit": 0,
    }
    assert out["worst_axis"] is None


# ── gather_madeira_endpoint_cost_summary ───────────────────────────────────────


def test_endpoint_cost_summary_absent_probe(tmp_path: Path) -> None:
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_endpoint_cost_summary()
    assert out["probe_present"] is False
    assert out["endpoints"] == {}
    assert out["worst_envelope_status"] == "SKIP"


def _write_endpoint_probe(tmp_path: Path, *, statuses: dict[str, str], is_stub: bool = False) -> None:
    ec = tmp_path / "endpoint-cost"
    ec.mkdir()
    payload = {
        "ts_utc": "2026-05-03T18-49-19Z",
        "is_stub": is_stub,
        "endpoints": {},
    }
    for eid, status in statuses.items():
        payload["endpoints"][eid] = {
            "runs": 1,
            "duration_hours_total": 1.0,
            "cost_usd_total": 1.0,
            "cost_usd_per_hour_avg": 1.0,
            "projected_daily_usd": 24.0,
            "envelope": {"status": status, "reason": f"reason-{status}"},
        }
    (ec / "endpoint-cost-probe-2026-05-03T18-49-19Z.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_endpoint_cost_summary_pass_only(tmp_path: Path) -> None:
    _write_endpoint_probe(tmp_path, statuses={"runpod:a": "PASS", "kalavai:x": "PASS"})
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_endpoint_cost_summary()
    assert out["probe_present"] is True
    assert out["worst_envelope_status"] == "PASS"
    assert "runpod:a" in out["endpoints"]
    assert out["endpoints"]["runpod:a"]["envelope_status"] == "PASS"
    assert "OK" in out["endpoints"]["runpod:a"]["operator_action"]


def test_endpoint_cost_summary_worst_status_ranks_fail_above_warn(
    tmp_path: Path,
) -> None:
    _write_endpoint_probe(
        tmp_path, statuses={"runpod:a": "WARN", "kalavai:x": "FAIL", "kalavai:y": "PASS"}
    )
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_endpoint_cost_summary()
    assert out["worst_envelope_status"] == "FAIL"


def test_endpoint_cost_summary_marks_stub_runs(tmp_path: Path) -> None:
    _write_endpoint_probe(tmp_path, statuses={"runpod:a": "PASS"}, is_stub=True)
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_endpoint_cost_summary()
    assert out["is_stub"] is True


def test_endpoint_cost_summary_operator_action_for_fail(tmp_path: Path) -> None:
    _write_endpoint_probe(tmp_path, statuses={"runpod:bad": "FAIL"})
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_endpoint_cost_summary()
    action = out["endpoints"]["runpod:bad"]["operator_action"]
    assert "Scale endpoint runpod:bad down NOW" in action
    assert "hard-fail band" in action


def test_endpoint_cost_summary_operator_action_for_warn(tmp_path: Path) -> None:
    _write_endpoint_probe(tmp_path, statuses={"runpod:hot": "WARN"})
    with patch.object(dossier_sources, "ARTIFACTS_DIR", tmp_path):
        out = dossier_sources.gather_madeira_endpoint_cost_summary()
    action = out["endpoints"]["runpod:hot"]["operator_action"]
    assert "Investigate" in action
    assert "10-20%" in action


# ── Section03EvalHealth madeira render ─────────────────────────────────────────


def test_section03_madeira_render_includes_axis_block() -> None:
    s = Section03EvalHealth()
    data = SectionData(
        payload={
            "overall_status": "pass",
            "rows_total": 10,
            "rows_passed": 7,
            "rows_failed": 3,
            "modes_run": ["all"],
            "elapsed_ms": 12345,
            "cost_total_usd": 0.05,
            "madeira_judge_axis_summary": {
                "per_axis_fail_count": {
                    "brand_voice": 2,
                    "citation": 1,
                    "persona_fit": 0,
                },
                "per_axis_total": {
                    "brand_voice": 5,
                    "citation": 5,
                    "persona_fit": 5,
                },
                "worst_axis": "brand_voice",
                "worst_axis_fail_count": 2,
                "judge_member_ids": ["openai:gpt-4o"],
            },
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "MADEIRA judge-axis fail summary" in md
    assert "`brand_voice`: 2 FAIL / 5 judged" in md
    assert "worst axis: **`brand_voice`** (2 FAILs)" in md
    assert "openai:gpt-4o" in md


def test_section03_madeira_render_no_judge_rows_friendly_message() -> None:
    s = Section03EvalHealth()
    data = SectionData(
        payload={
            "overall_status": "pass",
            "rows_total": 1,
            "rows_passed": 1,
            "rows_failed": 0,
            "modes_run": ["all"],
            "elapsed_ms": 100,
            "cost_total_usd": 0.0,
            "madeira_judge_axis_summary": {
                "per_axis_fail_count": {"brand_voice": 0, "citation": 0, "persona_fit": 0},
                "per_axis_total": {"brand_voice": 0, "citation": 0, "persona_fit": 0},
                "worst_axis": None,
                "worst_axis_fail_count": 0,
                "judge_member_ids": [],
            },
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "no judge rows yet" in md


def test_section03_metrics_for_trend_includes_axis_keys() -> None:
    s = Section03EvalHealth()
    data = SectionData(
        payload={
            "overall_status": "pass",
            "rows_total": 1,
            "rows_passed": 1,
            "rows_failed": 0,
            "cost_total_usd": 0.0,
            "madeira_judge_axis_summary": {
                "per_axis_fail_count": {
                    "brand_voice": 1,
                    "citation": 0,
                    "persona_fit": 2,
                },
                "worst_axis": "persona_fit",
                "worst_axis_fail_count": 2,
            },
        },
        data_age_seconds=0.0,
    )
    out = s.metrics_for_trend(data)
    assert out["judge_axis_fail_brand_voice"] == 1
    assert out["judge_axis_fail_citation"] == 0
    assert out["judge_axis_fail_persona_fit"] == 2
    assert out["judge_worst_axis"] == "persona_fit"
    assert out["judge_worst_axis_fail_count"] == 2


# ── Section04PersonaCalibration madeira render ────────────────────────────────


def test_section04_madeira_render_includes_worst_axis_cross_ref() -> None:
    s = Section04PersonaCalibration()
    data = SectionData(
        payload={
            "total_scenarios": 329,
            "total_personas": 13,
            "overall_within_tolerance": True,
            "personas_outside_tolerance_count": 0,
            "quarantined_scenarios_count": 0,
            "madeira_judge_axis_summary": {
                "per_axis_fail_count": {"brand_voice": 0, "citation": 3, "persona_fit": 0},
                "worst_axis": "citation",
                "worst_axis_fail_count": 3,
            },
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "Worst-axis trend (cross-reference, I52 P6)" in md
    assert "**`citation`**" in md
    assert "3 FAILs" in md


def test_section04_metrics_for_trend_includes_worst_axis() -> None:
    s = Section04PersonaCalibration()
    data = SectionData(
        payload={
            "total_scenarios": 100,
            "total_personas": 5,
            "overall_within_tolerance": True,
            "personas_outside_tolerance_count": 0,
            "quarantined_scenarios_count": 0,
            "madeira_judge_axis_summary": {
                "worst_axis": "brand_voice",
                "worst_axis_fail_count": 7,
            },
        },
        data_age_seconds=0.0,
    )
    out = s.metrics_for_trend(data)
    assert out["judge_worst_axis"] == "brand_voice"
    assert out["judge_worst_axis_fail_count"] == 7


# ── Section08OperationalHealth endpoint cost subsection ────────────────────────


def test_section08_render_includes_endpoint_subsection_when_probe_present() -> None:
    s = Section08OperationalHealth()
    data = SectionData(
        payload={
            "agent_memory_triggers_fired": 0,
            "cost_ceiling_breaches_count": 0,
            "promotion_gate_pass_count": 0,
            "madeira_endpoint_cost": {
                "probe_present": True,
                "probe_artifact": "artifacts/endpoint-cost/endpoint-cost-probe-x.json",
                "is_stub": True,
                "endpoints": {
                    "runpod:a100-80gb": {
                        "runs": 3,
                        "duration_hours_total": 2.5,
                        "cost_usd_per_hour_avg": 1.89,
                        "projected_daily_usd": 45.36,
                        "envelope_status": "PASS",
                        "envelope_reason": "within endpoint ceiling",
                        "operator_action": "OK; per-hour $1.8900, projected_24h=$45.36.",
                    }
                },
                "worst_envelope_status": "PASS",
            },
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "Endpoint cost surface (I52 P6: RunPod / Kalavai)" in md
    assert "STUB FIXTURE" in md
    assert "`runpod:a100-80gb`" in md
    assert "PASS" in md
    assert "POL-EVAL-COST-CEILING-ENDPOINT-{RUNPOD,KALAVAI}-V1" in md


def test_section08_render_missing_probe_friendly_message() -> None:
    s = Section08OperationalHealth()
    data = SectionData(
        payload={
            "agent_memory_triggers_fired": 0,
            "cost_ceiling_breaches_count": 0,
            "promotion_gate_pass_count": 0,
            "madeira_endpoint_cost": {
                "probe_present": False,
                "probe_artifact": None,
                "is_stub": False,
                "endpoints": {},
                "worst_envelope_status": "SKIP",
            },
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "no endpoint cost probe yet" in md
    assert "scripts/endpoint_cost_probe.py" in md


def test_section08_metrics_for_trend_includes_endpoint_keys() -> None:
    s = Section08OperationalHealth()
    data = SectionData(
        payload={
            "madeira_endpoint_cost": {
                "probe_present": True,
                "worst_envelope_status": "WARN",
                "endpoints": {"runpod:a": {}, "kalavai:x": {}},
            }
        },
        data_age_seconds=0.0,
    )
    out = s.metrics_for_trend(data)
    assert out["madeira_endpoint_probe_present"] is True
    assert out["madeira_endpoint_worst_status"] == "WARN"
    assert out["madeira_endpoint_count"] == 2


# ── Section04 + Section03 with non-madeira filter (no axis block) ──────────────


def test_section03_default_filter_no_axis_block_in_render() -> None:
    s = Section03EvalHealth()
    data = SectionData(
        payload={
            "overall_status": "pass",
            "rows_total": 0,
            "rows_passed": 0,
            "rows_failed": 0,
            "modes_run": [],
            "elapsed_ms": 0,
            "cost_total_usd": 0.0,
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "MADEIRA judge-axis fail summary" not in md


def test_section08_default_filter_no_endpoint_subsection_in_render() -> None:
    s = Section08OperationalHealth()
    data = SectionData(
        payload={
            "agent_memory_triggers_fired": 0,
            "cost_ceiling_breaches_count": 0,
            "promotion_gate_pass_count": 0,
        },
        data_age_seconds=0.0,
    )
    md = s.render_markdown(data)
    assert "Endpoint cost surface" not in md


def test_madeira_preset_filter_has_madeira_flavor() -> None:
    f = dossier_filter_madeira_preset()
    assert f.flavor == "madeira"


def test_default_filter_does_not_have_madeira_flavor() -> None:
    f = DossierFilter()
    assert f.flavor != "madeira"
