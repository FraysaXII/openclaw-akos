"""Tests for live-API dispatch in `akos.eval_harness.judge` (I52 P3 / OPS-58-1).

Covers `_call_member_via_api` and the helpers it depends on. SDK calls are
isolated via the `_anthropic_client_factory` / `_openai_client_factory` module
seams — no real network calls are made.

Scope:
- Provider dispatch (anthropic, openai, unsupported)
- JSON output parsing (strict, fence-tolerant, schema-violation rejection)
- Cost computation (known + unknown models)
- Payload shape (mandatory + optional persona context)
- Front-matter stripping in the system prompt loader
- Fallback-reason discrimination via `JudgeRoster.score` notes
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from akos.eval_harness import judge as judge_mod
from akos.eval_harness.judge import (
    JUDGE_AXES,
    JudgeRoster,
    MemberScore,
    _build_judge_payload,
    _call_member_via_api,
    _compute_cost_usd,
    _load_judge_prompt,
    _parse_judge_output,
)


# ──────────────────────────────────────────────────────────────────────────────
# SDK stubs (no real network)
# ──────────────────────────────────────────────────────────────────────────────


class _StubAnthropicMessage:
    def __init__(self, text: str, in_tok: int = 100, out_tok: int = 50) -> None:
        class _Block:
            type = "text"

            def __init__(self, t: str) -> None:
                self.text = t

        class _Usage:
            input_tokens = in_tok
            output_tokens = out_tok

        self.content = [_Block(text)]
        self.usage = _Usage()


class _StubAnthropicClient:
    def __init__(self, response_text: str) -> None:
        self._response_text = response_text
        self.calls: list[dict[str, Any]] = []

        class _Messages:
            def __init__(self, outer: "_StubAnthropicClient") -> None:
                self.outer = outer

            def create(self, **kwargs: Any) -> _StubAnthropicMessage:
                self.outer.calls.append(kwargs)
                return _StubAnthropicMessage(self.outer._response_text)

        self.messages = _Messages(self)


class _StubOpenAIClient:
    def __init__(self, response_text: str, prompt_tokens: int = 80, completion_tokens: int = 40) -> None:
        self._response_text = response_text
        self._prompt_tokens = prompt_tokens
        self._completion_tokens = completion_tokens
        self.calls: list[dict[str, Any]] = []

        class _Choice:
            def __init__(self, text: str) -> None:
                class _Msg:
                    pass

                self.message = _Msg()
                self.message.content = text

        class _Usage:
            def __init__(self, p: int, c: int) -> None:
                self.prompt_tokens = p
                self.completion_tokens = c

        outer = self

        class _Completions:
            def create(self, **kwargs: Any) -> Any:
                outer.calls.append(kwargs)

                class _Resp:
                    def __init__(self, text: str, p: int, c: int) -> None:
                        self.choices = [_Choice(text)]
                        self.usage = _Usage(p, c)

                return _Resp(outer._response_text, outer._prompt_tokens, outer._completion_tokens)

        class _Chat:
            completions = _Completions()

        self.chat = _Chat()


SCENARIO = {
    "scenario_id": "SCN-OPS-58-1-TEST-001",
    "persona_id": "OPERATOR",
    "expected_outcome_class": "GROUND",
    "prompt": "What governs the qualification gate?",
}

VALID_OUTPUT = json.dumps(
    {
        "scenario_id": "SCN-OPS-58-1-TEST-001",
        "scores": {"brand_voice": 4, "citation": 5, "persona_fit": 4},
        "notes": {
            "brand_voice": "concise + governance terms",
            "citation": "cites canonical csv path",
            "persona_fit": "matches operator register",
        },
    }
)


@pytest.fixture(autouse=True)
def _reset_factories():
    judge_mod._anthropic_client_factory = None
    judge_mod._openai_client_factory = None
    yield
    judge_mod._anthropic_client_factory = None
    judge_mod._openai_client_factory = None


# ──────────────────────────────────────────────────────────────────────────────
# _load_judge_prompt — strips YAML front-matter
# ──────────────────────────────────────────────────────────────────────────────


def test_load_judge_prompt_strips_front_matter():
    body = _load_judge_prompt()
    assert not body.lstrip().startswith("---"), "front-matter should be stripped"
    assert "JUDGE_PROMPT_V1" in body, "system prompt body should be preserved"
    assert "scores" in body, "schema description should be preserved"


# ──────────────────────────────────────────────────────────────────────────────
# _build_judge_payload — mandatory + optional shape
# ──────────────────────────────────────────────────────────────────────────────


def test_build_judge_payload_mandatory_keys():
    payload = _build_judge_payload("agent response text", SCENARIO, persona=None)
    assert payload["scenario_id"] == "SCN-OPS-58-1-TEST-001"
    assert payload["persona_id"] == "OPERATOR"
    assert payload["response"] == "agent response text"
    assert payload["expected_outcome_class"] == "GROUND"
    assert payload["persona_context"] is None


def test_build_judge_payload_with_persona_context():
    persona = {
        "typical_distance_band": "warm",
        "typical_languages": ["en"],
        "qualification_gate": "founder_qualification",
    }
    payload = _build_judge_payload("response", SCENARIO, persona=persona)
    ctx = payload["persona_context"]
    assert ctx == {
        "typical_distance_band": "warm",
        "typical_languages": ["en"],
        "qualification_gate": "founder_qualification",
    }


# ──────────────────────────────────────────────────────────────────────────────
# _parse_judge_output — strict + fence-tolerant
# ──────────────────────────────────────────────────────────────────────────────


def test_parse_judge_output_strict_valid():
    parsed = _parse_judge_output(VALID_OUTPUT, SCENARIO)
    assert parsed["scores"] == {"brand_voice": 4, "citation": 5, "persona_fit": 4}
    assert "concise" in parsed["notes"]["brand_voice"]


def test_parse_judge_output_fence_tolerant():
    fenced = "```json\n" + VALID_OUTPUT + "\n```"
    parsed = _parse_judge_output(fenced, SCENARIO)
    assert parsed["scores"]["citation"] == 5


def test_parse_judge_output_missing_axis_raises():
    bad = json.dumps({"scenario_id": "x", "scores": {"brand_voice": 4, "citation": 5}})
    with pytest.raises(ValueError, match="persona_fit"):
        _parse_judge_output(bad, SCENARIO)


def test_parse_judge_output_out_of_range_raises():
    bad = json.dumps({"scenario_id": "x", "scores": {"brand_voice": 9, "citation": 5, "persona_fit": 4}})
    with pytest.raises(ValueError, match=r"brand_voice"):
        _parse_judge_output(bad, SCENARIO)


def test_parse_judge_output_non_json_raises():
    with pytest.raises(json.JSONDecodeError):
        _parse_judge_output("not json", SCENARIO)


# ──────────────────────────────────────────────────────────────────────────────
# _compute_cost_usd
# ──────────────────────────────────────────────────────────────────────────────


def test_compute_cost_known_model():
    # claude-3-5-sonnet @ ($3 in, $15 out) per 1M, 100 in / 50 out
    cost = _compute_cost_usd("claude-3-5-sonnet-20241022", 100, 50)
    assert cost == pytest.approx((100 * 3 + 50 * 15) / 1_000_000)


def test_compute_cost_unknown_model_raises():
    with pytest.raises(ValueError, match="Unknown judge model"):
        _compute_cost_usd("openai:fictional-model-9000", 100, 50)


# ──────────────────────────────────────────────────────────────────────────────
# _call_member_via_api — provider dispatch
# ──────────────────────────────────────────────────────────────────────────────


def test_call_member_anthropic_returns_member_score():
    judge_mod._anthropic_client_factory = lambda: _StubAnthropicClient(VALID_OUTPUT)
    ms = _call_member_via_api(
        "anthropic:claude-3-5-sonnet-20241022", "response", SCENARIO, persona=None
    )
    assert isinstance(ms, MemberScore)
    assert ms.model_id == "anthropic:claude-3-5-sonnet-20241022"
    assert ms.scores == {"brand_voice": 4, "citation": 5, "persona_fit": 4}
    assert ms.fallback_offline is False
    assert ms.cost_usd > 0
    assert ms.latency_ms >= 0
    assert ms.notes["brand_voice"]


def test_call_member_openai_returns_member_score():
    judge_mod._openai_client_factory = lambda: _StubOpenAIClient(VALID_OUTPUT)
    ms = _call_member_via_api("openai:gpt-4o", "response", SCENARIO, persona=None)
    assert ms.model_id == "openai:gpt-4o"
    assert ms.scores == {"brand_voice": 4, "citation": 5, "persona_fit": 4}
    assert ms.cost_usd > 0


def test_call_member_unsupported_provider_raises():
    with pytest.raises(ValueError, match="unsupported provider"):
        _call_member_via_api("cohere:command-r", "response", SCENARIO, persona=None)


def test_call_member_missing_model_suffix_raises():
    with pytest.raises(ValueError, match="missing ':<model>' suffix"):
        _call_member_via_api("anthropic", "response", SCENARIO, persona=None)


def test_call_member_malformed_output_raises():
    judge_mod._openai_client_factory = lambda: _StubOpenAIClient("not json at all")
    with pytest.raises(json.JSONDecodeError):
        _call_member_via_api("openai:gpt-4o", "response", SCENARIO, persona=None)


# ──────────────────────────────────────────────────────────────────────────────
# JudgeRoster.score — fallback-reasons surface in notes (D-IH-58-F)
# ──────────────────────────────────────────────────────────────────────────────


def test_roster_score_surfaces_fallback_reasons_in_notes(monkeypatch):
    monkeypatch.delenv("AKOS_JUDGE_LIVE_API", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    roster = JudgeRoster(members=["anthropic:claude-3-5-sonnet-20241022"], mode="consensus")
    result = roster.score("agent response", SCENARIO, persona=None)
    assert "fallback-offline" in result.notes
    assert "fallback-reasons:" in result.notes
    # Either no-api-key or no-live-api-flag should be surfaced
    assert ("no-api-key" in result.notes) or ("no-live-api-flag" in result.notes)


def test_roster_score_no_fallback_when_member_succeeds(monkeypatch):
    judge_mod._anthropic_client_factory = lambda: _StubAnthropicClient(VALID_OUTPUT)
    monkeypatch.setenv("AKOS_JUDGE_LIVE_API", "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    roster = JudgeRoster(members=["anthropic:claude-3-5-sonnet-20241022"], mode="consensus")
    result = roster.score("agent response", SCENARIO, persona=None)
    assert "fallback-offline" not in result.notes
    assert "fallback-reasons" not in result.notes
    assert result.cost_usd > 0
