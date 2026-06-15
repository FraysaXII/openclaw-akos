"""LangGraph spike graph — ingest → rate → synthesize (+ mock MCP read node)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, TypedDict


SUBSTRATE_ADAPTER_ID = "SUBS-LANGGRAPH-OSS-SELFHOST"
CAPABILITY_TARGETS = ("CAP-M05", "CAP-M10", "CAP-M21")


class SpikeState(TypedDict, total=False):
    fixture_path: str
    sources_ingested: int
    sources_rated: int
    synthesis_summary: str
    mcp_read_posture: str
    mcp_tool: str
    substrate_adapter_id: str
    capability_ids: list[str]


def _ingest_node(state: SpikeState) -> dict[str, Any]:
    path = Path(state["fixture_path"])
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    return {"sources_ingested": len(rows), "sources_rated": 0}


def _rate_node(state: SpikeState) -> dict[str, Any]:
    return {"sources_rated": state.get("sources_ingested", 0)}


def _synthesize_node(state: SpikeState) -> dict[str, Any]:
    n = state.get("sources_rated", 0)
    return {
        "synthesis_summary": f"Spike synthesis over {n} fixture sources (mock LLM).",
        "substrate_adapter_id": SUBSTRATE_ADAPTER_ID,
        "capability_ids": list(CAPABILITY_TARGETS),
    }


def _mcp_read_node(state: SpikeState) -> dict[str, Any]:
    """CAP-M21 — read-only MCP posture mock (no live MCP server in spike)."""
    return {
        "mcp_tool": "hlk_lookup_read",
        "mcp_read_posture": "read",
    }


def run_mock_graph(fixture_path: Path) -> SpikeState:
    """Deterministic three-node loop without LangGraph installed."""
    state: SpikeState = {"fixture_path": str(fixture_path)}
    for step in (_ingest_node, _rate_node, _synthesize_node, _mcp_read_node):
        state.update(step(state))  # type: ignore[arg-type]
    return state


def run_langgraph_graph(fixture_path: Path) -> SpikeState:
    """Run via LangGraph StateGraph when the package is importable."""
    from langgraph.graph import END, START, StateGraph

    builder = StateGraph(SpikeState)
    builder.add_node("ingest", _ingest_node)
    builder.add_node("rate", _rate_node)
    builder.add_node("synthesize", _synthesize_node)
    builder.add_node("mcp_read", _mcp_read_node)
    builder.add_edge(START, "ingest")
    builder.add_edge("ingest", "rate")
    builder.add_edge("rate", "synthesize")
    builder.add_edge("synthesize", "mcp_read")
    builder.add_edge("mcp_read", END)

    try:
        from langgraph.checkpoint.memory import MemorySaver

        checkpointer = MemorySaver()
        graph = builder.compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": "langgraph-spike-1"}}
        out = graph.invoke({"fixture_path": str(fixture_path)}, config=config)
        return out  # type: ignore[return-value]
    except ImportError:
        from langgraph.checkpoint.sqlite import SqliteSaver

        import sqlite3

        conn = sqlite3.connect(":memory:", check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        graph = builder.compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": "langgraph-spike-1"}}
        out = graph.invoke({"fixture_path": str(fixture_path)}, config=config)
        return out  # type: ignore[return-value]


def run_spike_graph(fixture_path: Path) -> tuple[SpikeState, str]:
    """Return (final state, engine label)."""
    try:
        import langgraph  # noqa: F401

        return run_langgraph_graph(fixture_path), "langgraph"
    except ImportError:
        return run_mock_graph(fixture_path), "mock"
