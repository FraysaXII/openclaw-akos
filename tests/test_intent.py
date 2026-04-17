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

    def test_classify_draft_standup_not_admin(self):
        """Day-to-day drafts must not hit admin_escalate without mutation verbs/objects."""
        # Avoid bare word "org" — regex HLK token list includes \\borg\\b.
        result = _classify_regex(
            "Help me draft a short standup update for today."
        )
        assert result == "other"

    def test_classify_draft_email_not_admin(self):
        result = _classify_regex(
            "Draft a neutral email to stakeholders about the upcoming milestone."
        )
        assert result == "other"

    def test_classify_execution_escalate_playwright(self):
        result = _classify_regex("Use Playwright to click through the checkout flow.")
        assert result == "execution_escalate"

    def test_classify_execution_escalate_mcp(self):
        result = _classify_regex("Connect to the MCP server and update the schema.")
        assert result == "execution_escalate"


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

    @patch("akos.intent._get_classifier", return_value=None)
    def test_execution_escalate_regex(self, _mock):
        result = classify_request("Run pytest and open a pull request.")
        assert result["route"] == "execution_escalate"
        assert result["must_escalate"] is True
