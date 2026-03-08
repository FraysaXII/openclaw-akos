#!/usr/bin/env python3
"""Custom AKOS MCP server.

Exposes tools for agents to self-check the control plane:
- akos_health: GET /health
- akos_agents: GET /agents
- akos_status: GET /status

Requires: pip install mcp httpx
Usage: python scripts/mcp_akos_server.py
       or: uv run --with mcp scripts/mcp_akos_server.py (stdio)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Install mcp: pip install mcp httpx", file=sys.stderr)
    sys.exit(1)

import httpx

AKOS_API_URL = os.environ.get("AKOS_API_URL", "http://127.0.0.1:8420")
AKOS_API_KEY = os.environ.get("AKOS_API_KEY", "")

mcp = FastMCP("AKOS Control Plane", host="127.0.0.1", port=8421)


def _get_headers() -> dict[str, str]:
    headers: dict[str, str] = {}
    if AKOS_API_KEY:
        headers["Authorization"] = f"Bearer {AKOS_API_KEY}"
    return headers


@mcp.tool()
def akos_health() -> str:
    """Check AKOS control plane health. Returns gateway, RunPod, and Langfuse status."""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{AKOS_API_URL}/health", headers=_get_headers())
            resp.raise_for_status()
            data = resp.json()
            return f"status={data.get('status', 'unknown')} gateway={data.get('gateway', '?')} runpod={data.get('runpod', '?')} langfuse={data.get('langfuse', '?')}"
    except httpx.RequestError as e:
        return f"error: {e}"
    except Exception as e:
        return f"error: {e}"


@mcp.tool()
def akos_agents() -> str:
    """List registered AKOS agents (orchestrator, architect, executor, verifier)."""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{AKOS_API_URL}/agents", headers=_get_headers())
            resp.raise_for_status()
            data = resp.json()
            agents = data if isinstance(data, list) else data.get("agents", [])
            names = [a.get("name", a.get("id", "?")) for a in agents] if isinstance(agents, list) else []
            return f"agents: {', '.join(names) or 'none'}"
    except httpx.RequestError as e:
        return f"error: {e}"
    except Exception as e:
        return f"error: {e}"


@mcp.tool()
def akos_status() -> str:
    """Get current AKOS runtime status (environment, model, tier)."""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{AKOS_API_URL}/status", headers=_get_headers())
            resp.raise_for_status()
            data = resp.json()
            return f"env={data.get('environment', '?')} model={data.get('model', '?')} tier={data.get('tier', '?')}"
    except httpx.RequestError as e:
        return f"error: {e}"
    except Exception as e:
        return f"error: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
