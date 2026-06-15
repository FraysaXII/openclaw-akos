"""Tests for LangGraph OSS evaluation spike."""

from __future__ import annotations

from pathlib import Path

import pytest

from akos.langgraph_spike.graph import (
    CAPABILITY_TARGETS,
    SUBSTRATE_ADAPTER_ID,
    run_mock_graph,
    run_spike_graph,
)
from akos.langgraph_spike.runner import run_research_action_spike

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv"
)


def test_mock_graph_ingests_fixture_rows():
    state = run_mock_graph(FIXTURE)
    assert state["sources_ingested"] > 0
    assert state["sources_rated"] == state["sources_ingested"]
    assert state["substrate_adapter_id"] == SUBSTRATE_ADAPTER_ID
    assert state["mcp_read_posture"] == "read"
    assert set(CAPABILITY_TARGETS).issubset(set(state.get("capability_ids") or []))


def test_spike_runner_passes_on_default_fixture():
    result = run_research_action_spike(FIXTURE, emit_langfuse=False)
    assert result.status == "PASS"
    assert result.research_action_validation == "PASS"
    assert result.substrate_adapter_id == SUBSTRATE_ADAPTER_ID
    assert result.engine in ("mock", "langgraph")


def test_spike_graph_engine_label():
    _, engine = run_spike_graph(FIXTURE)
    pytest.importorskip("langgraph")
    assert engine in ("mock", "langgraph")


def test_require_langgraph_fails_when_mock_only():
    result = run_research_action_spike(FIXTURE, emit_langfuse=False, require_langgraph=True)
    if result.engine == "langgraph":
        assert result.status == "PASS"
    else:
        assert result.status == "FAIL"
        assert any("require_langgraph" in n for n in result.notes)
