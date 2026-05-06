"""Initiative 59 P6 — tests for OPS-58-3 persona_fit rubric fix.

Validates that ``_heuristic_persona_fit`` and ``score_response_offline``
correctly resolve persona context from ``PERSONA_REGISTRY.csv`` via
``resolve_persona`` when the caller passes ``persona=None`` but the
scenario carries a ``persona_id``.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from akos.eval_harness.judge import (
    _heuristic_persona_fit,
    resolve_persona,
    score_response_offline,
    _PERSONA_CACHE,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _clear_persona_cache() -> None:
    _PERSONA_CACHE.clear()
    yield
    _PERSONA_CACHE.clear()


def _seed_persona_csv(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    csv_path = tmp_path / "PERSONA_REGISTRY.csv"
    fields = [
        "persona_id", "name", "direction", "intent_summary", "value_band",
        "typical_languages", "typical_channels", "typical_distance_band",
        "qualification_gate", "intro_artifact_path", "handoff_role",
        "linked_topic_ids", "notes",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({f: r.get(f, "") for f in fields})
    return csv_path


class TestHeuristicPersonaFit:
    def test_none_persona_returns_3(self) -> None:
        assert _heuristic_persona_fit("hello there", None) == 3

    def test_empty_response_returns_1(self) -> None:
        assert _heuristic_persona_fit("", {"persona_id": "p1"}) == 1

    def test_qualification_gate_match_returns_5(self) -> None:
        persona = {"qualification_gate": "Please confirm your background", "typical_distance_band": "N1"}
        assert _heuristic_persona_fit("We need to confirm your qualification first.", persona) == 5

    def test_qualification_gate_no_match_returns_3(self) -> None:
        persona = {"qualification_gate": "Please confirm your background", "typical_distance_band": "N1"}
        assert _heuristic_persona_fit("Hello, welcome!", persona) == 3

    def test_cold_persona_escalate_returns_5(self) -> None:
        persona = {"typical_distance_band": "N4-cold", "qualification_gate": ""}
        assert _heuristic_persona_fit("I would escalate this to a senior partner.", persona) == 5

    def test_cold_persona_no_escalate_returns_3(self) -> None:
        persona = {"typical_distance_band": "N3-neutral", "qualification_gate": ""}
        assert _heuristic_persona_fit("Hello, welcome!", persona) == 3

    def test_warm_persona_returns_4(self) -> None:
        persona = {"typical_distance_band": "N1-warm", "qualification_gate": ""}
        assert _heuristic_persona_fit("Great to hear from you!", persona) == 4


class TestResolvePersona:
    def test_returns_passed_persona_when_not_none(self) -> None:
        persona = {"persona_id": "direct"}
        result = resolve_persona({"persona_id": "from_scenario"}, persona)
        assert result is persona

    def test_returns_none_when_no_persona_id(self) -> None:
        result = resolve_persona({}, None)
        assert result is None

    def test_resolves_from_registry(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        csv_path = _seed_persona_csv(tmp_path, [
            {"persona_id": "PE-INV-01", "name": "Investor", "typical_distance_band": "N3"},
        ])
        import akos.eval_harness.judge as judge_mod
        monkeypatch.setattr(judge_mod, "PERSONA_CSV", csv_path)

        result = resolve_persona({"persona_id": "PE-INV-01"}, None)
        assert result is not None
        assert result["persona_id"] == "PE-INV-01"
        assert result["typical_distance_band"] == "N3"

    def test_returns_none_for_unknown_id(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        csv_path = _seed_persona_csv(tmp_path, [
            {"persona_id": "PE-INV-01", "name": "Investor"},
        ])
        import akos.eval_harness.judge as judge_mod
        monkeypatch.setattr(judge_mod, "PERSONA_CSV", csv_path)

        result = resolve_persona({"persona_id": "UNKNOWN"}, None)
        assert result is None


class TestScoreResponseOfflineWithResolve:
    def test_persona_resolved_from_scenario(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        csv_path = _seed_persona_csv(tmp_path, [
            {"persona_id": "PE-INV-01", "name": "Investor", "typical_distance_band": "N4-cold", "qualification_gate": ""},
        ])
        import akos.eval_harness.judge as judge_mod
        monkeypatch.setattr(judge_mod, "PERSONA_CSV", csv_path)

        scenario = {"scenario_id": "S1", "persona_id": "PE-INV-01"}
        result = score_response_offline("I would escalate this matter.", scenario, persona=None)
        assert result.scores["persona_fit"] == 5
        assert result.persona_id == "PE-INV-01"

    def test_no_persona_id_falls_back_to_neutral(self) -> None:
        scenario = {"scenario_id": "S2"}
        result = score_response_offline("Hello there.", scenario, persona=None)
        assert result.scores["persona_fit"] == 3

    def test_explicit_persona_overrides_registry(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        csv_path = _seed_persona_csv(tmp_path, [
            {"persona_id": "PE-INV-01", "name": "Investor", "typical_distance_band": "N4-cold"},
        ])
        import akos.eval_harness.judge as judge_mod
        monkeypatch.setattr(judge_mod, "PERSONA_CSV", csv_path)

        explicit_persona = {"persona_id": "PE-INV-01", "typical_distance_band": "N1-warm", "qualification_gate": ""}
        scenario = {"scenario_id": "S3", "persona_id": "PE-INV-01"}
        result = score_response_offline("Great to hear!", scenario, persona=explicit_persona)
        assert result.scores["persona_fit"] == 4
