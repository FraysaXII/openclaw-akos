"""Finance data service for AKOS.

Provides quote, search, and sentiment capabilities backed by yfinance
and Alpha Vantage.  All provider-specific details are hidden behind
normalised Pydantic models so the MCP wrapper and tests stay clean.

Backend swap (e.g. Finnhub, Twelve Data) requires changes only here;
tool signatures and response envelopes remain stable.

Requires: pip install yfinance (optional -- degrades gracefully).
Alpha Vantage sentiment requires ALPHA_VANTAGE_KEY env var (optional).
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from typing import Any

from akos.models import (
    FinanceResponse,
    QuoteData,
    SearchResult,
    SentimentItem,
)

logger = logging.getLogger("akos.finance")

_yfinance_available = False
try:
    import yfinance as yf

    _yfinance_available = True
except ImportError:
    pass

_httpx_available = False
try:
    import httpx

    _httpx_available = True
except ImportError:
    pass


class _TTLCache:
    """Minimal TTL cache keyed by arbitrary strings."""

    def __init__(self, ttl_seconds: float) -> None:
        self._ttl = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        ts, value = entry
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (time.monotonic(), value)

    def clear(self) -> None:
        self._store.clear()


class FinanceService:
    """Thin abstraction over financial data providers.

    Instantiate once per MCP server lifetime.  Thread-safe enough for
    the single-threaded FastMCP stdio loop.
    """

    QUOTE_TTL = 60.0
    SEARCH_TTL = 300.0
    SENTIMENT_TTL = 300.0

    def __init__(self) -> None:
        self._quote_cache = _TTLCache(self.QUOTE_TTL)
        self._search_cache = _TTLCache(self.SEARCH_TTL)
        self._sentiment_cache = _TTLCache(self.SENTIMENT_TTL)
        self._av_key = os.environ.get("ALPHA_VANTAGE_KEY", "")

    @property
    def yfinance_available(self) -> bool:
        return _yfinance_available

    @property
    def sentiment_available(self) -> bool:
        return bool(self._av_key) and _httpx_available

    def get_quote(self, ticker: str) -> FinanceResponse:
        """Fetch a quote bundle for *ticker*."""
        ticker = ticker.upper().strip()
        if not ticker:
            return FinanceResponse(status="error", error_detail="Empty ticker")

        if not _yfinance_available:
            return FinanceResponse(
                status="degraded",
                warnings=["yfinance not installed; pip install yfinance"],
                error_detail="yfinance not available",
            )

        cached = self._quote_cache.get(ticker)
        if cached is not None:
            return cached

        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            quote = QuoteData(
                ticker=ticker,
                last_price=_safe_float(info, "last_price"),
                day_high=_safe_float(info, "day_high"),
                day_low=_safe_float(info, "day_low"),
                open_price=_safe_float(info, "open"),
                previous_close=_safe_float(info, "previous_close"),
                volume=_safe_int(info, "last_volume"),
                market_cap=_safe_float(info, "market_cap"),
                currency=getattr(info, "currency", "USD") or "USD",
                exchange=getattr(info, "exchange", "") or "",
            )
            resp = FinanceResponse(
                status="ok",
                source="yfinance",
                as_of=datetime.now(timezone.utc),
                freshness="~15 min delayed (Yahoo Finance free tier)",
                quotes=[quote],
            )
            self._quote_cache.set(ticker, resp)
            return resp
        except Exception as exc:
            logger.debug("Quote fetch failed for %s: %s", ticker, exc)
            return FinanceResponse(
                status="not_found",
                source="yfinance",
                as_of=datetime.now(timezone.utc),
                error_detail=f"Could not fetch quote for '{ticker}': {exc}",
            )

    def search_ticker(self, query: str) -> FinanceResponse:
        """Resolve a company name or partial ticker to matching symbols."""
        query = query.strip()
        if not query:
            return FinanceResponse(status="error", error_detail="Empty search query")

        if not _yfinance_available:
            return FinanceResponse(
                status="degraded",
                warnings=["yfinance not installed; pip install yfinance"],
                error_detail="yfinance not available",
            )

        cached = self._search_cache.get(query.lower())
        if cached is not None:
            return cached

        try:
            results: list[SearchResult] = []
            screener = yf.Ticker(query)
            info_dict = screener.info or {}
            if info_dict.get("symbol"):
                results.append(SearchResult(
                    ticker=info_dict["symbol"],
                    name=info_dict.get("shortName", info_dict.get("longName", query)),
                    exchange=info_dict.get("exchange", ""),
                    asset_type=info_dict.get("quoteType", ""),
                ))

            status = "ok" if results else "not_found"
            resp = FinanceResponse(
                status=status,
                source="yfinance",
                as_of=datetime.now(timezone.utc),
                freshness="ticker metadata (static)",
                search_results=results if results else None,
                error_detail="" if results else f"No results for '{query}'",
            )
            self._search_cache.set(query.lower(), resp)
            return resp
        except Exception as exc:
            logger.debug("Search failed for %s: %s", query, exc)
            return FinanceResponse(
                status="error",
                source="yfinance",
                error_detail=f"Search failed: {exc}",
            )

    def get_sentiment(self, tickers: str) -> FinanceResponse:
        """Fetch news sentiment for *tickers* via Alpha Vantage."""
        tickers = tickers.upper().strip()
        if not tickers:
            return FinanceResponse(status="error", error_detail="Empty tickers")

        warns: list[str] = []

        if not self._av_key:
            return FinanceResponse(
                status="degraded",
                source="alpha_vantage",
                warnings=["ALPHA_VANTAGE_KEY not set; sentiment unavailable"],
                error_detail="Missing API key",
            )

        if not _httpx_available:
            return FinanceResponse(
                status="degraded",
                warnings=["httpx not installed; pip install httpx"],
                error_detail="httpx not available",
            )

        cached = self._sentiment_cache.get(tickers)
        if cached is not None:
            return cached

        url = (
            "https://www.alphavantage.co/query"
            f"?function=NEWS_SENTIMENT&tickers={tickers}"
            f"&apikey={self._av_key}"
        )
        try:
            with httpx.Client(timeout=15.0) as client:
                resp = client.get(url)
                resp.raise_for_status()
                data = resp.json()

            if "Information" in data:
                return FinanceResponse(
                    status="rate_limited",
                    source="alpha_vantage",
                    as_of=datetime.now(timezone.utc),
                    warnings=["Alpha Vantage rate limit reached (5 calls/min free tier)"],
                    error_detail=data["Information"],
                )

            feed = data.get("feed", [])[:5]
            items = [
                SentimentItem(
                    headline=article.get("title", ""),
                    sentiment=article.get("overall_sentiment_label", ""),
                    relevance=_parse_float(article.get("relevance_score")),
                    source=article.get("source", ""),
                )
                for article in feed
            ]

            if not items:
                warns.append(f"No recent sentiment data for {tickers}")

            result = FinanceResponse(
                status="ok" if items else "not_found",
                source="alpha_vantage",
                as_of=datetime.now(timezone.utc),
                freshness="near-real-time (Alpha Vantage news feed)",
                warnings=warns,
                sentiment=items if items else None,
                error_detail="" if items else f"No sentiment for '{tickers}'",
            )
            self._sentiment_cache.set(tickers, result)
            return result
        except Exception as exc:
            logger.debug("Sentiment fetch failed for %s: %s", tickers, exc)
            return FinanceResponse(
                status="error",
                source="alpha_vantage",
                error_detail=f"Sentiment fetch failed: {exc}",
            )


def _safe_float(obj: object, attr: str) -> float | None:
    try:
        val = getattr(obj, attr, None)
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def _safe_int(obj: object, attr: str) -> int | None:
    try:
        val = getattr(obj, attr, None)
        return int(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def _parse_float(val: Any) -> float | None:
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None
