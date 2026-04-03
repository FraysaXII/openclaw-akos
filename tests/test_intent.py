"""Tests for AKOS request intent classification."""

from akos.intent import classify_request


def test_classify_admin_request():
    result = classify_request("I need to restructure the Finance area.")
    assert result["route"] == "admin_escalate"
    assert result["must_escalate"] is True


def test_classify_finance_request():
    result = classify_request("What is the current AAPL stock price?")
    assert result["route"] == "finance_research"
    assert result["must_escalate"] is False


def test_classify_explicit_hlk_search():
    result = classify_request("Search HLK for CTO and return the closest canonical role.")
    assert result["route"] == "hlk_search"


def test_classify_hlk_lookup():
    result = classify_request("Who is the CTO?")
    assert result["route"] == "hlk_lookup"
