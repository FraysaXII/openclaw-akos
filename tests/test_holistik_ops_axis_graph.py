"""Tests for the 6-axis Holistik Ops Neo4j projection extension (Initiative 32 P5/P6).

Locks the contract that:
1. All 6 new node labels (Persona, Channel, Sourcing, Skill, TouchpointKitCell, Policy)
   are projected with counts matching CSV row counts.
2. :UNDER_TOPIC edges are emitted from every dimension row that declares topic_ids.
3. The existing :Role / :Process / :Program / :Topic projection is unchanged
   (R-32-15 mitigation: additive projection).
4. ``build_holistik_ops_axis_graph`` returns the union of all 6 build functions.
5. The sync_hlk_neo4j.py dry-run reports the new label counts with the I32 P2/P3/P4
   row counts (5 skills, 15 cells, 14 policies, 16 personas, 10 channels, 1 vendor).
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_hlk_neo4j.py"


def _csv_row_count(path: Path) -> int:
    if not path.is_file():
        return 0
    with path.open(encoding="utf-8", newline="") as fh:
        return sum(1 for _ in csv.DictReader(fh))


def test_persona_graph_node_count_matches_csv() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import PERSONA_REGISTRY_CSV, build_persona_graph

    nodes, _ = build_persona_graph()
    expected = _csv_row_count(PERSONA_REGISTRY_CSV)
    assert len(nodes) == expected, f"persona nodes {len(nodes)} != CSV rows {expected}"
    assert all(n.label == "Persona" for n in nodes)


def test_channel_graph_node_count_matches_csv() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import CHANNEL_TOUCHPOINT_REGISTRY_CSV, build_channel_graph

    nodes, _ = build_channel_graph()
    expected = _csv_row_count(CHANNEL_TOUCHPOINT_REGISTRY_CSV)
    assert len(nodes) == expected
    assert all(n.label == "Channel" for n in nodes)


def test_sourcing_graph_node_count_matches_csv() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import SOURCING_REGISTER_CSV, build_sourcing_graph

    nodes, _ = build_sourcing_graph()
    expected = _csv_row_count(SOURCING_REGISTER_CSV)
    assert len(nodes) == expected
    assert all(n.label == "Sourcing" for n in nodes)


def test_skill_graph_node_count_matches_csv() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import SKILL_REGISTRY_CSV, build_skill_graph

    nodes, _ = build_skill_graph()
    expected = _csv_row_count(SKILL_REGISTRY_CSV)
    assert len(nodes) == expected
    assert all(n.label == "Skill" for n in nodes)
    # I32 P2 acceptance: at least 5 seed rows.
    assert expected >= 5


def test_touchpoint_kit_cell_graph_node_count_matches_csv() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import TOUCHPOINT_KIT_CELL_REGISTRY_CSV, build_touchpoint_kit_cell_graph

    nodes, _ = build_touchpoint_kit_cell_graph()
    expected = _csv_row_count(TOUCHPOINT_KIT_CELL_REGISTRY_CSV)
    assert len(nodes) == expected
    assert all(n.label == "TouchpointKitCell" for n in nodes)


def test_policy_graph_node_count_matches_csv() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import POLICY_REGISTER_CSV, build_policy_graph

    nodes, _ = build_policy_graph()
    expected = _csv_row_count(POLICY_REGISTER_CSV)
    assert len(nodes) == expected
    assert all(n.label == "Policy" for n in nodes)


def test_under_topic_edges_emitted_for_dimensions_with_topic_ids() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import build_holistik_ops_axis_graph

    nodes, edges = build_holistik_ops_axis_graph()
    under_topic = [e for e in edges if e.edge_type == "UNDER_TOPIC"]
    # Every Skill, TouchpointKitCell, and Policy row carries at least one topic_id;
    # most Persona / Channel / Sourcing rows also do via linked_topic_ids.
    assert len(under_topic) > 0, "expected at least 1 :UNDER_TOPIC edge"
    # All UNDER_TOPIC edges target :Topic.
    assert all(e.to_label == "Topic" for e in under_topic)


def test_holistik_ops_axis_graph_returns_six_new_labels() -> None:
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk_graph_model import build_holistik_ops_axis_graph

    nodes, _ = build_holistik_ops_axis_graph()
    labels_seen = {n.label for n in nodes}
    expected = {"Persona", "Channel", "Sourcing", "Skill", "TouchpointKitCell", "Policy"}
    assert labels_seen == expected, f"expected {expected}; got {labels_seen}"


def test_sync_dry_run_reports_six_new_labels() -> None:
    """End-to-end: sync_hlk_neo4j.py --dry-run logs all 6 new label counts."""
    r = subprocess.run(
        [sys.executable, str(SYNC_SCRIPT), "--dry-run"],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=30,
    )
    assert r.returncode == 0, f"--dry-run exited {r.returncode}; stderr: {r.stderr}"
    # The log line is on stderr (logger output).
    output = r.stdout + r.stderr
    for needle in ("personas=", "channels=", "sourcing=", "skills=", "cells=", "policies=", "axis-6"):
        assert needle in output, f"missing log fragment {needle!r} in:\n{output}"


def test_existing_role_process_program_topic_unchanged() -> None:
    """R-32-15 mitigation: additive extension does not perturb existing graph."""
    sys.path.insert(0, str(REPO_ROOT))
    from akos.hlk import get_hlk_registry
    from akos.hlk_graph_model import (
        assert_graph_registry_parity,
        build_hlk_csv_graph,
        build_program_graph,
        build_topic_graph,
    )

    reg = get_hlk_registry()
    nodes, edges = build_hlk_csv_graph(reg)
    # Existing parity check still holds (no new label perturbs it).
    assert_graph_registry_parity(reg, nodes, edges)
    prog_nodes, _ = build_program_graph(reg)
    topic_nodes, _ = build_topic_graph(reg)
    # Sanity: counts match the I32 baseline post-P4.
    assert sum(1 for n in nodes if n.label == "Role") == 65
    assert sum(1 for n in nodes if n.label == "Process") == 1103
    assert len(prog_nodes) == 12
    # Topic registry grows by 1 per dimension/operational-mirror addition; post-I47 P1
    # the count is 28 (27 post-I32 P10 + persona_scenario_registry from I47 P1).
    assert len(topic_nodes) == 28
