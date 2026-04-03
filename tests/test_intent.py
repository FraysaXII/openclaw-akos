"""Tests for AKOS request intent classification."""

from unittest.mock import patch

from akos.intent import classify_request, _classify_regex


class TestRegexFallback:
    """Regex fallback always works without Ollama."""

    def test_classify_admin_request(self):
        result = _classify_regex("I need to restructure the Finance area.")
        assert result == "admin_escalate"

    def test_classify_finance_request(self):
        result = _classify_regex("What is the current AAPL stock price?")
        assert result == "finance_research"

    def test_classify_explicit_hlk_search(self):
        result = _classify_regex("Search HLK for CTO and return the closest canonical role.")
        assert result == "hlk_search"

    def test_classify_hlk_lookup(self):
        result = _classify_regex("Who is the CTO?")
        assert result == "hlk_lookup"

    def test_classify_gtm_project(self):
        result = _classify_regex("What's the status of the GTM launch plan?")
        assert result == "gtm_project"

    def test_classify_general(self):
        result = _classify_regex("Hello, how are you?")
        assert result == "other"


class TestClassifyRequestIntegration:
    """Test the full classify_request path with regex fallback."""

    @patch("akos.intent._get_classifier", return_value=None)
    def test_admin_with_regex_fallback(self, _mock):
        result = classify_request("I need to restructure the Finance area.")
        assert result["route"] == "admin_escalate"
        assert result["must_escalate"] is True
        assert result["method"] == "regex"

    @patch("akos.intent._get_classifier", return_value=None)
    def test_finance_with_regex_fallback(self, _mock):
        result = classify_request("What is the current AAPL stock price?")
        assert result["route"] == "finance_research"
        assert result["must_escalate"] is False

    @patch("akos.intent._get_classifier", return_value=None)
    def test_gtm_with_regex_fallback(self, _mock):
        result = classify_request("Show me the GTM launch plan status.")
        assert result["route"] == "gtm_project"
        assert "confidence" in result

    @patch("akos.intent._get_classifier", return_value=None)
    def test_result_contains_all_keys(self, _mock):
        result = classify_request("Who is the CTO?")
        for key in ["route", "confidence", "method", "must_escalate", "reason", "operator_message"]:
            assert key in result, f"Missing key: {key}"
