"""Initiative 46 P6 — Tests for graph-escape adversarial cassettes + GraphRAG dir scaffold."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
ADVERSARIAL_ROOT = REPO_ROOT / "tests" / "evals" / "cassettes" / "adversarial"
GRAPH_RAG_ROOT = REPO_ROOT / "tests" / "evals" / "cassettes" / "graph_rag"


# ── Graph-escape cassettes ───────────────────────────────────────────────────


def test_3_graph_escape_cassettes_shipped() -> None:
    probes = sorted(ADVERSARIAL_ROOT.glob("**/ge_*.jsonl"))
    assert len(probes) >= 3, f"expected >=3 graph-escape probes, got {len(probes)}"


def test_graph_escape_cassettes_target_madeira_lookup() -> None:
    """The 3 ge_* probes target the highest-traffic skill (most likely to be
    over-eagerly routed to GraphRAG)."""
    probes = sorted(ADVERSARIAL_ROOT.glob("**/ge_*.jsonl"))
    for p in probes:
        # parent is the skill_id directory
        assert p.parent.name == "SKILL-MADEIRA-LOOKUP-V1", (
            f"graph-escape probe should target MADEIRA-LOOKUP, got {p.parent.name}"
        )


def test_graph_escape_cassettes_forbid_neo4j_in_response() -> None:
    """Per the R-46-2 guard: graph-escape probes ensure 'graph_rag' / 'neo4j' tokens
    don't leak into classify_request responses for simple direct lookups."""
    probes = sorted(ADVERSARIAL_ROOT.glob("**/ge_*.jsonl"))
    for p in probes:
        text = p.read_text(encoding="utf-8")
        assert "graph_rag" in text, f"{p.name}: missing graph_rag in forbidden_in_response"
        assert "neo4j" in text, f"{p.name}: missing neo4j in forbidden_in_response"


def test_all_graph_escape_cassettes_replay_pass() -> None:
    """If any ge_* cassette regresses, MADEIRA's classify_request started leaking
    graph/neo4j tokens for simple lookups (or routing changed unexpectedly)."""
    from akos.eval_harness.adversarial import replay_adversarial_classify_request_cassette

    probes = sorted(ADVERSARIAL_ROOT.glob("**/ge_*.jsonl"))
    fails: list[tuple[str, list[str]]] = []
    for p in probes:
        out = replay_adversarial_classify_request_cassette(p)
        if out["status"] != "PASS":
            fails.append((p.name, out["failures"]))
    assert not fails, f"graph-escape regressions: {fails}"


# ── GraphRAG cassette directory scaffold ─────────────────────────────────────


def test_graph_rag_cassette_dir_exists_with_readme() -> None:
    """The directory is scaffold-only today (no live cassettes yet) but
    the README.md must exist so the cassette pattern is documented."""
    assert GRAPH_RAG_ROOT.is_dir(), "tests/evals/cassettes/graph_rag/ must exist"
    readme = GRAPH_RAG_ROOT / "README.md"
    assert readme.is_file(), "graph_rag/README.md must exist (P6 scaffold marker)"


def test_graph_rag_readme_documents_activation_flow() -> None:
    text = (GRAPH_RAG_ROOT / "README.md").read_text(encoding="utf-8")
    # Must explain when this directory populates
    assert "AKOS_RECORD_LIVE=1" in text
    assert "graphrag_poc.py" in text
    assert "D-IH-46-Decision-P3" in text


def test_graph_rag_readme_has_language_frontmatter() -> None:
    """Every canonical doc in the vault declares language: en|es|fr per
    SOP-HLK_LOCALISATION_001.md."""
    text = (GRAPH_RAG_ROOT / "README.md").read_text(encoding="utf-8")
    assert "language: en" in text


# ── WIP_DASHBOARD operational health surface ─────────────────────────────────


def test_wip_dashboard_carries_neo4j_drift_canary_pointer() -> None:
    """P6 added a hand-written 'Operational health' section pointing at
    scripts/graphrag_drift_canary.py."""
    dashboard = REPO_ROOT / "docs" / "wip" / "planning" / "WIP_DASHBOARD.md"
    text = dashboard.read_text(encoding="utf-8")
    assert "Operational health" in text
    assert "graphrag_drift_canary" in text


def test_wip_dashboard_carries_eval_harness_smoke_pointer() -> None:
    """The same operational health section also points at the eval harness CLI
    + cassette PII linter + adversarial floor (cross-coupling I45 + I46 signals)."""
    dashboard = REPO_ROOT / "docs" / "wip" / "planning" / "WIP_DASHBOARD.md"
    text = dashboard.read_text(encoding="utf-8")
    assert "eval.py --mode all" in text
    assert "lint_cassette_pii" in text
    assert "eval.py --mode adversarial" in text


def test_wip_dashboard_auto_section_unchanged_after_p6() -> None:
    """The hand-written section must NOT live inside the BEGIN AUTO/END AUTO
    markers (otherwise the next render would clobber it)."""
    dashboard = REPO_ROOT / "docs" / "wip" / "planning" / "WIP_DASHBOARD.md"
    text = dashboard.read_text(encoding="utf-8")
    auto_block = text.split("<!-- BEGIN AUTO -->")[1].split("<!-- END AUTO -->")[0]
    assert "Operational health" not in auto_block
    assert "graphrag_drift_canary" not in auto_block
