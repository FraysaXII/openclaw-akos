"""Tests for akos.hlk_graph_model CSV projection."""

from __future__ import annotations

import pytest
from akos.hlk import get_hlk_registry
from akos.hlk_graph_model import (
    assert_graph_registry_parity,
    build_hlk_csv_graph,
    graph_parity_counts,
)

pytestmark = pytest.mark.graph


def test_build_hlk_csv_graph_parity():
    reg = get_hlk_registry()
    nodes, edges = build_hlk_csv_graph(reg)
    assert_graph_registry_parity(reg, nodes, edges)
    counts = graph_parity_counts(reg, nodes, edges)
    assert counts["registry_roles"] == counts["graph_role_nodes"]
    assert counts["registry_processes"] == counts["graph_process_nodes"]
    assert counts["edge_parent_of"] >= 0
    assert counts["edge_owned_by"] >= 0


def test_edges_reference_existing_ids():
    reg = get_hlk_registry()
    nodes, edges = build_hlk_csv_graph(reg)
    proc_ids = {n.id for n in nodes if n.label == "Process"}
    role_ids = {n.id for n in nodes if n.label == "Role"}
    for e in edges:
        if e.from_label == "Process":
            assert e.from_id in proc_ids, e
        if e.to_label == "Process":
            assert e.to_id in proc_ids, e
        if e.from_label == "Role":
            assert e.from_id in role_ids, e
        if e.to_label == "Role":
            assert e.to_id in role_ids, e
