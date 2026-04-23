"""Golden JSONL trajectory contracts for Madeira (no live LLM)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = pytest.mark.madeira

from akos.intent import classify_request
from akos.madeira_trajectory import (
    assert_tools_before_first_text,
    parse_session_jsonl,
    tool_names_from_session,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "madeira_trajectory"


def test_golden_hlk_tool_first_fixture() -> None:
    events = parse_session_jsonl(FIXTURES / "golden_hlk_tool_first.jsonl")
    assert tool_names_from_session(events) == ["hlk_role"]
    assert_tools_before_first_text(events, required=["hlk_role"])


def test_text_before_tool_fixture_fails() -> None:
    events = parse_session_jsonl(FIXTURES / "bad_text_before_tool.jsonl")
    with pytest.raises(AssertionError, match="text appeared before"):
        assert_tools_before_first_text(events, required=["hlk_role"])


def test_mixed_utterance_admin_regex_wins() -> None:
    with patch("akos.intent._get_classifier", return_value=None):
        r = classify_request("Restructure the Finance area. Who is the CTO?")
    assert r["route"] == "admin_escalate"
    assert r["must_escalate"] is True
