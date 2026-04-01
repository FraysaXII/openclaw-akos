#!/usr/bin/env python3
"""Finance research MCP server for AKOS agents.

Exposes read-only financial data tools:
- finance_quote: get a quote bundle for a ticker symbol
- finance_search: resolve a company name to ticker symbols
- finance_sentiment: fetch news sentiment for tickers (requires ALPHA_VANTAGE_KEY)

All responses use the FinanceResponse envelope from akos.models.

Requires: pip install mcp yfinance httpx
Usage: python scripts/finance_mcp_server.py
       or: uv run --with mcp scripts/finance_mcp_server.py (stdio)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Install mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

from akos.finance import FinanceService

mcp = FastMCP("AKOS Finance Research", host="127.0.0.1", port=8422)
_service = FinanceService()


@mcp.tool()
def finance_quote(ticker: str) -> str:
    """Get a quote bundle for a stock ticker symbol.

    Returns price, day range, volume, market cap, exchange, currency,
    data source, freshness estimate, and any warnings.  Quotes from
    Yahoo Finance free tier are typically delayed ~15 minutes.

    This tool is for research only -- not for trading decisions.
    """
    resp = _service.get_quote(ticker)
    return resp.model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def finance_search(query: str) -> str:
    """Resolve a company name or partial ticker to matching symbols.

    Use this before finance_quote when the user provides a company
    name (e.g. "Apple") instead of a ticker symbol (e.g. "AAPL").
    Returns ticker, full name, exchange, and asset type for each match.

    When FINNHUB_API_KEY is configured, this uses Finnhub's fuzzy symbol
    search for better natural company-name resolution. Otherwise it falls
    back to yfinance ticker metadata lookup.
    """
    resp = _service.search_ticker(query)
    return resp.model_dump_json(indent=2, exclude_none=True)


@mcp.tool()
def finance_sentiment(tickers: str) -> str:
    """Fetch recent news sentiment for one or more tickers.

    Returns headlines, sentiment labels, and relevance scores from
    Alpha Vantage.  Requires ALPHA_VANTAGE_KEY environment variable.
    If the key is not set, returns a degraded response with a warning.

    Pass a comma-separated list for multiple tickers (e.g. "AAPL,MSFT").
    """
    resp = _service.get_sentiment(tickers)
    return resp.model_dump_json(indent=2, exclude_none=True)


if __name__ == "__main__":
    mcp.run(transport="stdio")
