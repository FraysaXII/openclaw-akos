#!/usr/bin/env python3
"""HLK Neo4j graph MCP server (optional mirrored projection).

Read-only tools with allowlisted queries. Loads ``~/.openclaw/.env`` via
``bootstrap_openclaw_process_env`` before connecting (same contract as
``scripts/serve-api.py``).

Requires: pip install mcp neo4j
Env: NEO4J_URI, NEO4J_USERNAME (optional), NEO4J_PASSWORD

Usage:
    python scripts/hlk_graph_mcp_server.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Install mcp: pip install mcp", file=sys.stderr)
    sys.exit(1)

from akos.io import bootstrap_openclaw_process_env

bootstrap_openclaw_process_env()

from akos.hlk_neo4j import (  # noqa: E402
    get_neo4j_driver,
    graph_summary,
    neo4j_configured,
    process_neighbourhood,
    role_neighbourhood,
)

mcp = FastMCP("AKOS HLK Graph", host="127.0.0.1", port=8424)


def _neo4j_tool_precheck() -> str | None:
    """Return JSON error payload string, or ``None`` if Neo4j may be usable."""
    if not neo4j_configured():
        return json.dumps({"status": "error", "detail": "Neo4j not configured (NEO4J_URI, NEO4J_PASSWORD)"})
    return None


@mcp.tool()
def hlk_graph_summary() -> str:
    """Return CSV registry counts (always) plus Neo4j label/relationship counts when connected."""
    from akos.hlk import get_hlk_registry

    reg = get_hlk_registry()
    out: dict = {
        "status": "ok",
        "csv": {"roles": len(reg._roles), "processes": len(reg._processes)},  # noqa: SLF001
        "neo4j": "unconfigured",
    }
    if not neo4j_configured():
        return json.dumps(out, indent=2)
    drv = get_neo4j_driver()
    if drv is None:
        out["neo4j"] = "driver_unavailable"
        return json.dumps(out, indent=2)
    try:
        with drv.session() as session:
            out["neo4j"] = "connected"
            out["graph"] = graph_summary(session)
    finally:
        drv.close()
    return json.dumps(out, indent=2)


@mcp.tool()
def hlk_graph_process_neighbourhood(item_id: str, depth: int = 2, limit: int = 80) -> str:
    """Neighbourhood subgraph for one process item_id (bounded depth and node limit)."""
    err = _neo4j_tool_precheck()
    if err:
        return err
    drv = get_neo4j_driver()
    if drv is None:
        return json.dumps({"status": "error", "detail": "Neo4j driver unavailable (install neo4j package)"})
    try:
        with drv.session() as session:
            data = process_neighbourhood(session, item_id, depth=int(depth), limit=int(limit))
    finally:
        drv.close()
    return json.dumps(data, indent=2)


@mcp.tool()
def hlk_graph_role_neighbourhood(role_name: str, depth: int = 2, limit: int = 80) -> str:
    """Processes and reporting roles linked to role_name (bounded)."""
    err = _neo4j_tool_precheck()
    if err:
        return err
    drv = get_neo4j_driver()
    if drv is None:
        return json.dumps({"status": "error", "detail": "Neo4j driver unavailable (install neo4j package)"})
    try:
        with drv.session() as session:
            data = role_neighbourhood(session, role_name, depth=int(depth), limit=int(limit))
    finally:
        drv.close()
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
