"""Tests for scripts/render_topic_graph.py (Initiative 25 P3).

Locks in the deterministic topic-graph rendering contract:
- `_safe_id` produces Mermaid-safe identifiers (no spaces, no punctuation).
- `_split` parses semicolon-separated lists (empty string -> empty list).
- `build_mermaid` renders a stable `flowchart LR` with subgraph clusters
  by `program_id` and the four edge types (parent_topic / depends_on /
  related_topics / subsumes).
- The shipped `_assets/_meta/topic_graph.mmd` parses minimally and contains
  the expected node IDs.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "render_topic_graph.py"
SHIPPED_MMD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "_assets"
    / "_meta"
    / "topic_graph.mmd"
)


@pytest.fixture(scope="module")
def render_topic_graph_module():
    spec = importlib.util.spec_from_file_location(
        "render_topic_graph_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["render_topic_graph_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_safe_id_strips_punctuation_and_spaces(render_topic_graph_module):
    assert render_topic_graph_module._safe_id("PRJ-HOL-FOUNDING-2026") == "PRJ_HOL_FOUNDING_2026"
    assert render_topic_graph_module._safe_id("a b c") == "a_b_c"
    assert render_topic_graph_module._safe_id("topic.dotted") == "topic_dotted"
    assert render_topic_graph_module._safe_id("") == ""


def test_safe_id_preserves_alnum_and_underscore(render_topic_graph_module):
    assert render_topic_graph_module._safe_id("topic_km_governance") == "topic_km_governance"
    assert render_topic_graph_module._safe_id("topic_external_adviser_handoff") == "topic_external_adviser_handoff"


def test_split_handles_empty_and_semicolon_list(render_topic_graph_module):
    assert render_topic_graph_module._split("") == []
    assert render_topic_graph_module._split("a") == ["a"]
    assert render_topic_graph_module._split("a;b;c") == ["a", "b", "c"]
    # Strips whitespace + drops empties:
    assert render_topic_graph_module._split(" a ; ; b ;") == ["a", "b"]


def test_build_mermaid_emits_flowchart_lr_header(render_topic_graph_module):
    rows = [
        {
            "topic_id": "topic_a",
            "title": "A",
            "topic_class": "process_map",
            "program_id": "PRJ-HOL-FOUNDING-2026",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        }
    ]
    out = render_topic_graph_module.build_mermaid(rows)
    assert "flowchart LR" in out
    assert "subgraph PRJ_HOL_FOUNDING_2026" in out
    assert 'topic_a["A"]' in out


def test_build_mermaid_clusters_by_program(render_topic_graph_module):
    rows = [
        {
            "topic_id": "t1",
            "title": "T1",
            "topic_class": "",
            "program_id": "PRJ-HOL-A-2026",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        },
        {
            "topic_id": "t2",
            "title": "T2",
            "topic_class": "",
            "program_id": "PRJ-HOL-B-2026",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        },
        {
            "topic_id": "t3",
            "title": "T3",
            "topic_class": "",
            "program_id": "",  # -> shared
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        },
    ]
    out = render_topic_graph_module.build_mermaid(rows)
    assert "subgraph PRJ_HOL_A_2026" in out
    assert "subgraph PRJ_HOL_B_2026" in out
    assert "subgraph shared" in out


def test_build_mermaid_emits_four_edge_kinds(render_topic_graph_module):
    rows = [
        {
            "topic_id": "src",
            "title": "Src",
            "topic_class": "",
            "program_id": "shared",
            "parent_topic": "parent_x",
            "depends_on": "dep_y",
            "related_topics": "rel_z",
            "subsumes": "sub_w",
        }
    ]
    out = render_topic_graph_module.build_mermaid(rows)
    assert "parent_x --> src" in out
    assert "src -.-> dep_y" in out
    assert "src --- rel_z" in out
    assert "src ==> sub_w" in out


def test_build_mermaid_evidence_pack_uses_round_brackets(render_topic_graph_module):
    rows = [
        {
            "topic_id": "topic_e",
            "title": "Evidence",
            "topic_class": "evidence_pack",
            "program_id": "shared",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        }
    ]
    out = render_topic_graph_module.build_mermaid(rows)
    # evidence_pack -> `(["..."])` shape; default -> `["..."]`.
    assert 'topic_e(["Evidence"])' in out


def test_build_mermaid_skips_rows_without_topic_id(render_topic_graph_module):
    rows = [
        {
            "topic_id": "",
            "title": "Empty",
            "topic_class": "",
            "program_id": "shared",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        }
    ]
    out = render_topic_graph_module.build_mermaid(rows)
    # Should still produce a valid header + subgraph but no nodes.
    assert "flowchart LR" in out
    assert "Empty" not in out


def test_build_mermaid_is_deterministic(render_topic_graph_module):
    """Same input -> byte-identical output (idempotency contract)."""
    rows = [
        {
            "topic_id": "topic_a",
            "title": "A",
            "topic_class": "",
            "program_id": "PRJ-HOL-FOUNDING-2026",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "",
            "subsumes": "",
        },
        {
            "topic_id": "topic_b",
            "title": "B",
            "topic_class": "",
            "program_id": "PRJ-HOL-FOUNDING-2026",
            "parent_topic": "",
            "depends_on": "",
            "related_topics": "topic_a",
            "subsumes": "",
        },
    ]
    out1 = render_topic_graph_module.build_mermaid(rows)
    out2 = render_topic_graph_module.build_mermaid(rows)
    assert out1 == out2


def test_shipped_topic_graph_mmd_has_expected_topics():
    """The committed `_assets/_meta/topic_graph.mmd` contains all 3 known topics."""
    if not SHIPPED_MMD.is_file():
        pytest.skip("topic_graph.mmd not yet rendered")
    text = SHIPPED_MMD.read_text(encoding="utf-8")
    assert "flowchart LR" in text
    assert "topic_external_adviser_handoff" in text
    assert "topic_kirbe_billing_plane_routing" in text
    assert "topic_km_governance" in text


def test_shipped_topic_graph_mmd_clusters_by_program():
    """Subgraphs reflect the 3 program identifiers (FOUNDING / KIR / shared)."""
    if not SHIPPED_MMD.is_file():
        pytest.skip("topic_graph.mmd not yet rendered")
    text = SHIPPED_MMD.read_text(encoding="utf-8")
    assert "subgraph PRJ_HOL_FOUNDING_2026" in text
    assert "subgraph PRJ_HOL_KIR_2026" in text
    assert "subgraph shared" in text
