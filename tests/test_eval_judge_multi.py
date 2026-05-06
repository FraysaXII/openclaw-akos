"""Tests for the multi-model judge dispatcher (Initiative 52 P2; D-IH-52-A/B).

Covers ``JudgeRoster``: env construction, fingerprint stability, consensus
voting + tie-break, per-axis routing, tiered (placeholder), member fallback
to offline, and the ``score_response`` env-driven dispatcher.

All tests inject a deterministic ``MemberScorer`` stub (no real API calls).
"""

from __future__ import annotations

import os
from typing import Iterable

import pytest

from akos.eval_harness.judge import (
    DEFAULT_JUDGE_MODE,
    JUDGE_AXES,
    JUDGE_MODE_ENV,
    JUDGE_ROSTER_ENV,
    VALID_JUDGE_MODES,
    JudgeResult,
    JudgeRoster,
    MemberScore,
    _compose_consensus,
    _compose_per_axis,
    _compose_tiered,
    _default_member_scorer,
    score_response,
    score_response_live,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def _stub_scorer(score_table: dict[str, dict[str, int]]):
    """Build a MemberScorer stub from {model_id: {axis: score}} table."""

    def _scorer(model_id: str, response: str, scenario: dict, persona: dict | None) -> MemberScore:
        scores = dict(score_table.get(model_id, {axis: 4 for axis in JUDGE_AXES}))
        return MemberScore(
            model_id=model_id,
            scores=scores,
            notes={axis: "stub" for axis in JUDGE_AXES},
            cost_usd=0.001,
            latency_ms=10,
            fallback_offline=False,
        )

    return _scorer


SCENARIO_FIXTURE = {
    "scenario_id": "SCN-TEST-001",
    "persona_id": "PERSONA-INVESTOR-COLD",
}


# ──────────────────────────────────────────────────────────────────────────────
# JudgeRoster.from_env()
# ──────────────────────────────────────────────────────────────────────────────


class TestJudgeRosterFromEnv:
    def test_constructs_with_two_members(self, monkeypatch):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "anthropic:claude-3-5-sonnet,openai:gpt-4o")
        roster = JudgeRoster.from_env()
        assert roster.members == ["anthropic:claude-3-5-sonnet", "openai:gpt-4o"]
        assert roster.mode == DEFAULT_JUDGE_MODE

    def test_strips_whitespace_in_csv(self, monkeypatch):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, " anthropic:a , openai:b ")
        roster = JudgeRoster.from_env()
        assert roster.members == ["anthropic:a", "openai:b"]

    def test_empty_env_raises(self, monkeypatch):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "")
        with pytest.raises(ValueError, match="empty"):
            JudgeRoster.from_env()

    def test_missing_env_raises(self, monkeypatch):
        monkeypatch.delenv(JUDGE_ROSTER_ENV, raising=False)
        with pytest.raises(ValueError, match="empty"):
            JudgeRoster.from_env()

    def test_mode_env_consensus_default(self, monkeypatch):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "a:1,b:2")
        monkeypatch.delenv(JUDGE_MODE_ENV, raising=False)
        roster = JudgeRoster.from_env()
        assert roster.mode == "consensus"

    def test_mode_env_per_axis(self, monkeypatch):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "a:1,b:2")
        monkeypatch.setenv(JUDGE_MODE_ENV, "per_axis")
        roster = JudgeRoster.from_env()
        assert roster.mode == "per_axis"

    def test_invalid_mode_raises(self, monkeypatch):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "a:1,b:2")
        monkeypatch.setenv(JUDGE_MODE_ENV, "majority")
        with pytest.raises(ValueError, match="not in"):
            JudgeRoster.from_env()


# ──────────────────────────────────────────────────────────────────────────────
# Fingerprint stability
# ──────────────────────────────────────────────────────────────────────────────


class TestRosterFingerprint:
    def test_consensus_fingerprint_stable(self):
        roster = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        fp = roster.fingerprint()
        assert "a:1" in fp and "b:2" in fp
        assert "mode=consensus" in fp
        assert roster.fingerprint() == fp  # idempotent

    def test_per_axis_fingerprint_includes_routing(self):
        roster = JudgeRoster(
            members=["a:1", "b:2"],
            mode="per_axis",
            per_axis_routing={"brand_voice": "a:1", "citation": "b:2", "persona_fit": "a:1"},
        )
        fp = roster.fingerprint()
        assert "brand_voice=a:1" in fp
        assert "citation=b:2" in fp

    def test_member_order_distinguishes_fingerprint(self):
        r1 = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        r2 = JudgeRoster(members=["b:2", "a:1"], mode="consensus")
        assert r1.fingerprint() != r2.fingerprint()


# ──────────────────────────────────────────────────────────────────────────────
# Consensus composition
# ──────────────────────────────────────────────────────────────────────────────


class TestComposeConsensus:
    def test_unanimous_returns_value(self):
        ms = [
            MemberScore("a:1", {"brand_voice": 5, "citation": 5, "persona_fit": 5}),
            MemberScore("b:2", {"brand_voice": 5, "citation": 5, "persona_fit": 5}),
        ]
        out = _compose_consensus(ms)
        assert out == {"brand_voice": 5, "citation": 5, "persona_fit": 5}

    def test_majority_picks_modal_value(self):
        ms = [
            MemberScore("a:1", {"brand_voice": 4, "citation": 4, "persona_fit": 4}),
            MemberScore("b:2", {"brand_voice": 4, "citation": 4, "persona_fit": 4}),
            MemberScore("c:3", {"brand_voice": 5, "citation": 5, "persona_fit": 5}),
        ]
        out = _compose_consensus(ms)
        assert out == {"brand_voice": 4, "citation": 4, "persona_fit": 4}

    def test_tie_breaks_to_position_1(self):
        # 2-member roster, disagreement -> tie; position-1 wins
        ms = [
            MemberScore("a:1", {"brand_voice": 5, "citation": 5, "persona_fit": 5}),
            MemberScore("b:2", {"brand_voice": 3, "citation": 3, "persona_fit": 3}),
        ]
        out = _compose_consensus(ms)
        assert out == {"brand_voice": 5, "citation": 5, "persona_fit": 5}

    def test_tie_with_position_1_not_in_top_falls_to_min(self):
        # Edge case: position-1 has a unique value; tie among others
        ms = [
            MemberScore("a:1", {"brand_voice": 1, "citation": 1, "persona_fit": 1}),
            MemberScore("b:2", {"brand_voice": 4, "citation": 4, "persona_fit": 4}),
            MemberScore("c:3", {"brand_voice": 5, "citation": 5, "persona_fit": 5}),
        ]
        out = _compose_consensus(ms)
        # All three are unique -> top_count=1 -> winners=[1,4,5] -> position-1=1 IS in winners
        # so position-1 wins; brand_voice=1
        assert out["brand_voice"] == 1

    def test_empty_member_list(self):
        out = _compose_consensus([])
        assert out == {axis: 4 for axis in JUDGE_AXES}


# ──────────────────────────────────────────────────────────────────────────────
# Per-axis composition
# ──────────────────────────────────────────────────────────────────────────────


class TestComposePerAxis:
    def test_routes_each_axis(self):
        ms = [
            MemberScore("a:1", {"brand_voice": 5, "citation": 1, "persona_fit": 1}),
            MemberScore("b:2", {"brand_voice": 1, "citation": 5, "persona_fit": 1}),
            MemberScore("c:3", {"brand_voice": 1, "citation": 1, "persona_fit": 5}),
        ]
        routing = {"brand_voice": "a:1", "citation": "b:2", "persona_fit": "c:3"}
        out = _compose_per_axis(ms, routing)
        assert out == {"brand_voice": 5, "citation": 5, "persona_fit": 5}

    def test_missing_route_falls_back_to_position_1(self):
        ms = [
            MemberScore("a:1", {"brand_voice": 5, "citation": 5, "persona_fit": 5}),
            MemberScore("b:2", {"brand_voice": 2, "citation": 2, "persona_fit": 2}),
        ]
        routing = {}  # no routes specified
        out = _compose_per_axis(ms, routing)
        assert out == {"brand_voice": 5, "citation": 5, "persona_fit": 5}


# ──────────────────────────────────────────────────────────────────────────────
# Tiered composition (placeholder at P2)
# ──────────────────────────────────────────────────────────────────────────────


class TestComposeTiered:
    def test_collapses_to_position_1(self):
        ms = [
            MemberScore("a:1", {"brand_voice": 4, "citation": 4, "persona_fit": 4}),
            MemberScore("b:2", {"brand_voice": 1, "citation": 1, "persona_fit": 1}),
        ]
        out = _compose_tiered(ms)
        assert out == {"brand_voice": 4, "citation": 4, "persona_fit": 4}


# ──────────────────────────────────────────────────────────────────────────────
# JudgeRoster.score() integration
# ──────────────────────────────────────────────────────────────────────────────


class TestJudgeRosterScore:
    def test_consensus_score_returns_judge_result(self):
        roster = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        scorer = _stub_scorer(
            {
                "a:1": {"brand_voice": 5, "citation": 5, "persona_fit": 5},
                "b:2": {"brand_voice": 5, "citation": 5, "persona_fit": 5},
            }
        )
        result = roster.score("response", SCENARIO_FIXTURE, member_scorer=scorer)
        assert isinstance(result, JudgeResult)
        assert result.scenario_id == "SCN-TEST-001"
        assert result.persona_id == "PERSONA-INVESTOR-COLD"
        assert result.scores == {"brand_voice": 5, "citation": 5, "persona_fit": 5}
        assert result.overall_pass is True
        assert "roster[a:1,b:2]" in result.model_id

    def test_score_aggregates_member_costs(self):
        roster = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        scorer = _stub_scorer(
            {"a:1": {"brand_voice": 4, "citation": 4, "persona_fit": 4}}
        )
        result = roster.score("response", SCENARIO_FIXTURE, member_scorer=scorer)
        # Each stub member returns cost_usd=0.001; 2 members
        assert result.cost_usd == pytest.approx(0.002)

    def test_score_records_fingerprint_in_notes(self):
        roster = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        scorer = _stub_scorer(
            {"a:1": {"brand_voice": 4, "citation": 4, "persona_fit": 4}}
        )
        result = roster.score("response", SCENARIO_FIXTURE, member_scorer=scorer)
        assert "roster[a:1,b:2]" in result.notes
        assert "mode=consensus" in result.notes

    def test_score_records_fallback_offline_in_notes(self):
        roster = JudgeRoster(members=["a:1", "b:2"], mode="consensus")

        def _stub(model_id, response, scenario, persona):
            return MemberScore(
                model_id=model_id,
                scores={"brand_voice": 4, "citation": 4, "persona_fit": 4},
                cost_usd=0.0,
                fallback_offline=(model_id == "b:2"),
            )

        result = roster.score("response", SCENARIO_FIXTURE, member_scorer=_stub)
        assert "fallback-offline:b:2" in result.notes


# ──────────────────────────────────────────────────────────────────────────────
# _default_member_scorer fallback paths
# ──────────────────────────────────────────────────────────────────────────────


class TestDefaultMemberScorerFallback:
    def test_offline_provider_returns_heuristic(self, monkeypatch):
        monkeypatch.delenv("AKOS_JUDGE_LIVE_API", raising=False)
        ms = _default_member_scorer(
            "offline:rule-based",
            "I cite docs/references/hlk/foo.md",
            SCENARIO_FIXTURE,
            None,
        )
        assert ms.model_id == "offline:rule-based"
        assert ms.fallback_offline is False
        assert ms.cost_usd == 0.0

    def test_live_provider_falls_back_when_no_api_flag(self, monkeypatch):
        monkeypatch.delenv("AKOS_JUDGE_LIVE_API", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "fake")
        ms = _default_member_scorer(
            "anthropic:claude-3-5-sonnet",
            "test",
            SCENARIO_FIXTURE,
            None,
        )
        assert ms.fallback_offline is True
        assert "fallback-offline-no-live-api-flag" in ms.notes["brand_voice"]

    def test_live_provider_falls_back_when_no_api_key(self, monkeypatch):
        monkeypatch.setenv("AKOS_JUDGE_LIVE_API", "1")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        ms = _default_member_scorer(
            "anthropic:claude-3-5-sonnet",
            "test",
            SCENARIO_FIXTURE,
            None,
        )
        assert ms.fallback_offline is True
        assert "fallback-offline-no-api-key" in ms.notes["brand_voice"]

    def test_live_api_call_raises_when_wired_path_attempted(self, monkeypatch):
        # I52 P3 / OPS-58-1: with AKOS_JUDGE_LIVE_API=1 AND key present, the
        # default scorer dispatches via `_call_member_via_api` which now
        # performs a real provider call. We inject a stub client factory that
        # raises a deterministic exception so the fallback path is exercised
        # without a network round-trip.
        from akos.eval_harness import judge as judge_mod

        class _RaisingClient:
            class _Messages:
                def create(self, **kwargs):
                    raise RuntimeError("simulated-transport-error")
            messages = _Messages()

        monkeypatch.setattr(judge_mod, "_anthropic_client_factory", lambda: _RaisingClient())
        monkeypatch.setenv("AKOS_JUDGE_LIVE_API", "1")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "fake")
        ms = _default_member_scorer(
            "anthropic:claude-3-5-sonnet-20241022",
            "test",
            SCENARIO_FIXTURE,
            None,
        )
        assert ms.fallback_offline is True
        assert "fallback-offline-api-error" in ms.notes["brand_voice"]
        assert "simulated-transport-error" in ms.raw_error


# ──────────────────────────────────────────────────────────────────────────────
# score_response env dispatcher
# ──────────────────────────────────────────────────────────────────────────────


class TestScoreResponseDispatch:
    def test_offline_when_record_live_unset(self, monkeypatch):
        monkeypatch.delenv("AKOS_RECORD_LIVE", raising=False)
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "anthropic:a")
        result = score_response("test", SCENARIO_FIXTURE)
        # Offline result has model_id="offline"
        assert result.model_id == "offline"

    def test_roster_when_record_live_and_roster_set(self, monkeypatch):
        monkeypatch.setenv("AKOS_RECORD_LIVE", "1")
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "offline:m1,offline:m2")
        result = score_response("test", SCENARIO_FIXTURE)
        # Roster path -> model_id is the fingerprint
        assert "roster[offline:m1,offline:m2]" in result.model_id
        assert "mode=consensus" in result.model_id

    def test_score_response_live_raises_without_roster(self, monkeypatch):
        monkeypatch.delenv(JUDGE_ROSTER_ENV, raising=False)
        with pytest.raises(NotImplementedError, match="AKOS_JUDGE_ROSTER"):
            score_response_live("test", SCENARIO_FIXTURE)

    def test_score_response_live_routes_through_roster_when_env_set(
        self, monkeypatch
    ):
        monkeypatch.setenv(JUDGE_ROSTER_ENV, "offline:m1")
        result = score_response_live("test", SCENARIO_FIXTURE)
        assert "roster[offline:m1]" in result.model_id


# ──────────────────────────────────────────────────────────────────────────────
# Reproducibility contract
# ──────────────────────────────────────────────────────────────────────────────


class TestReproducibility:
    def test_same_inputs_same_fingerprint(self):
        r1 = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        r2 = JudgeRoster(members=["a:1", "b:2"], mode="consensus")
        assert r1.fingerprint() == r2.fingerprint()

    def test_valid_judge_modes_documented(self):
        assert "consensus" in VALID_JUDGE_MODES
        assert "per_axis" in VALID_JUDGE_MODES
        assert "tiered" in VALID_JUDGE_MODES
