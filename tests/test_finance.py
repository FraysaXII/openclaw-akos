"""Tests for akos/finance.py FinanceService and Pydantic response models."""

from __future__ import annotations

import time
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from akos.finance import FinanceService, _TTLCache
from akos.models import (
    FinanceResponse,
    FinanceStatus,
    QuoteData,
    SearchResult,
    SentimentItem,
)


# ── Response model validation ──────────────────────────────────────────

class TestFinanceResponseModel:
    def test_minimal_ok(self):
        resp = FinanceResponse(status="ok")
        assert resp.status == "ok"
        assert resp.warnings == []

    def test_full_quote_response(self):
        resp = FinanceResponse(
            status="ok",
            source="yfinance",
            freshness="~15 min delayed",
            quotes=[QuoteData(ticker="AAPL", last_price=195.50)],
        )
        assert resp.quotes[0].ticker == "AAPL"
        assert resp.quotes[0].last_price == 195.50

    def test_degraded_with_warnings(self):
        resp = FinanceResponse(
            status="degraded",
            warnings=["yfinance not installed"],
        )
        assert resp.status == "degraded"
        assert len(resp.warnings) == 1

    def test_search_result_model(self):
        sr = SearchResult(ticker="AAPL", name="Apple Inc.", exchange="NMS")
        assert sr.ticker == "AAPL"
        assert sr.asset_type == ""

    def test_sentiment_item_model(self):
        item = SentimentItem(headline="Apple beats earnings", sentiment="Bullish")
        assert item.sentiment == "Bullish"
        assert item.relevance is None

    def test_json_serialization_excludes_none(self):
        resp = FinanceResponse(status="ok", source="yfinance")
        data = resp.model_dump(exclude_none=True)
        assert "quotes" not in data
        assert "sentiment" not in data


# ── TTL cache ──────────────────────────────────────────────────────────

class TestTTLCache:
    def test_set_and_get(self):
        cache = _TTLCache(ttl_seconds=60)
        cache.set("key", "value")
        assert cache.get("key") == "value"

    def test_miss_returns_none(self):
        cache = _TTLCache(ttl_seconds=60)
        assert cache.get("missing") is None

    def test_expired_entry_returns_none(self):
        cache = _TTLCache(ttl_seconds=0.01)
        cache.set("key", "value")
        time.sleep(0.02)
        assert cache.get("key") is None

    def test_clear(self):
        cache = _TTLCache(ttl_seconds=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.clear()
        assert cache.get("a") is None
        assert cache.get("b") is None


# ── FinanceService: get_quote ──────────────────────────────────────────

class TestGetQuote:
    def test_empty_ticker_returns_error(self):
        svc = FinanceService()
        resp = svc.get_quote("")
        assert resp.status == "error"

    @patch("akos.finance._yfinance_available", False)
    def test_missing_yfinance_returns_degraded(self):
        svc = FinanceService()
        resp = svc.get_quote("AAPL")
        assert resp.status == "degraded"
        assert any("yfinance" in w for w in resp.warnings)

    @patch("akos.finance._yfinance_available", True)
    @patch("akos.finance.yf", create=True)
    def test_successful_quote(self, mock_yf):
        mock_info = SimpleNamespace(
            last_price=195.50,
            day_high=197.00,
            day_low=194.00,
            open=195.00,
            previous_close=194.50,
            last_volume=50000000,
            market_cap=3000000000000.0,
            currency="USD",
            exchange="NMS",
        )
        mock_ticker = MagicMock()
        mock_ticker.fast_info = mock_info
        mock_yf.Ticker.return_value = mock_ticker

        svc = FinanceService()
        resp = svc.get_quote("AAPL")
        assert resp.status == "ok"
        assert resp.source == "yfinance"
        assert resp.quotes is not None
        assert resp.quotes[0].ticker == "AAPL"
        assert resp.quotes[0].last_price == 195.50

    @patch("akos.finance._yfinance_available", True)
    @patch("akos.finance.yf", create=True)
    def test_quote_caching(self, mock_yf):
        mock_info = SimpleNamespace(
            last_price=100.0, day_high=101.0, day_low=99.0,
            open=100.0, previous_close=99.5, last_volume=1000,
            market_cap=1e9, currency="USD", exchange="NMS",
        )
        mock_ticker = MagicMock()
        mock_ticker.fast_info = mock_info
        mock_yf.Ticker.return_value = mock_ticker

        svc = FinanceService()
        svc.get_quote("TST")
        svc.get_quote("TST")
        mock_yf.Ticker.assert_called_once_with("TST")

    @patch("akos.finance._yfinance_available", True)
    @patch("akos.finance.yf", create=True)
    def test_ticker_not_found(self, mock_yf):
        mock_yf.Ticker.side_effect = Exception("No data found")
        svc = FinanceService()
        resp = svc.get_quote("ZZZZZ")
        assert resp.status == "not_found"


# ── FinanceService: search_ticker ──────────────────────────────────────

class TestSearchTicker:
    def test_empty_query_returns_error(self):
        svc = FinanceService()
        resp = svc.search_ticker("")
        assert resp.status == "error"

    @patch("akos.finance._yfinance_available", False)
    def test_missing_yfinance_returns_degraded(self):
        svc = FinanceService()
        resp = svc.search_ticker("Apple")
        assert resp.status == "degraded"

    @patch("akos.finance._yfinance_available", True)
    @patch("akos.finance.yf", create=True)
    def test_successful_search(self, mock_yf):
        mock_ticker = MagicMock()
        mock_ticker.info = {
            "symbol": "AAPL",
            "shortName": "Apple Inc.",
            "exchange": "NMS",
            "quoteType": "EQUITY",
        }
        mock_yf.Ticker.return_value = mock_ticker

        svc = FinanceService()
        resp = svc.search_ticker("AAPL")
        assert resp.status == "ok"
        assert resp.search_results is not None
        assert resp.search_results[0].ticker == "AAPL"
        assert resp.search_results[0].name == "Apple Inc."


# ── FinanceService: get_sentiment ──────────────────────────────────────

class TestGetSentiment:
    def test_empty_tickers_returns_error(self):
        svc = FinanceService()
        resp = svc.get_sentiment("")
        assert resp.status == "error"

    def test_missing_api_key_returns_degraded(self):
        with patch.dict("os.environ", {}, clear=True):
            svc = FinanceService()
            svc._av_key = ""
            resp = svc.get_sentiment("AAPL")
            assert resp.status == "degraded"
            assert any("ALPHA_VANTAGE_KEY" in w for w in resp.warnings)

    @patch("akos.finance._httpx_available", True)
    @patch("akos.finance.httpx")
    def test_successful_sentiment(self, mock_httpx):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "feed": [
                {
                    "title": "Apple beats earnings",
                    "overall_sentiment_label": "Bullish",
                    "relevance_score": "0.95",
                    "source": "Reuters",
                },
            ]
        }
        mock_resp.raise_for_status = MagicMock()
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.return_value = mock_resp
        mock_httpx.Client.return_value = mock_client

        svc = FinanceService()
        svc._av_key = "test-key"
        resp = svc.get_sentiment("AAPL")
        assert resp.status == "ok"
        assert resp.sentiment is not None
        assert resp.sentiment[0].headline == "Apple beats earnings"
        assert resp.sentiment[0].relevance == 0.95

    @patch("akos.finance._httpx_available", True)
    @patch("akos.finance.httpx")
    def test_rate_limited_sentiment(self, mock_httpx):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "Information": "API rate limit reached"
        }
        mock_resp.raise_for_status = MagicMock()
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.get.return_value = mock_resp
        mock_httpx.Client.return_value = mock_client

        svc = FinanceService()
        svc._av_key = "test-key"
        resp = svc.get_sentiment("AAPL")
        assert resp.status == "rate_limited"


# ── Service properties ─────────────────────────────────────────────────

class TestServiceProperties:
    @patch("akos.finance._yfinance_available", True)
    def test_yfinance_available_true(self):
        svc = FinanceService()
        assert svc.yfinance_available is True

    @patch("akos.finance._yfinance_available", False)
    def test_yfinance_available_false(self):
        svc = FinanceService()
        assert svc.yfinance_available is False

    def test_sentiment_available_without_key(self):
        svc = FinanceService()
        svc._av_key = ""
        assert svc.sentiment_available is False
