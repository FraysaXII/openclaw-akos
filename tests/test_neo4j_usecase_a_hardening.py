"""Initiative 46 P2 — tests for Use-case A hardening (drift canary + skill_neighbourhood)."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


# ── Drift canary ──────────────────────────────────────────────────────────────


def test_drift_canary_csv_only_mode_lists_all_10_dimensions() -> None:
    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "graphrag_drift_canary.py"), "--csv-only", "--json"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
    )
    assert p.returncode == 0
    parsed = json.loads(p.stdout)
    csv_counts = parsed["csv_counts"]
    expected_labels = {
        "Role", "Process", "Program", "Topic",
        "Persona", "Channel", "Sourcing",
        "Skill", "TouchpointKitCell", "Policy",
    }
    assert set(csv_counts.keys()) == expected_labels


def test_drift_canary_csv_only_mode_returns_known_count_for_skill() -> None:
    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "graphrag_drift_canary.py"), "--csv-only", "--json"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
    )
    parsed = json.loads(p.stdout)
    assert parsed["csv_counts"]["Skill"] == 5


def test_drift_canary_skips_when_neo4j_not_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NEO4J_URI", raising=False)
    monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
    p = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "graphrag_drift_canary.py"), "--json"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=REPO_ROOT,
        env={**__import__("os").environ, "NEO4J_URI": "", "NEO4J_PASSWORD": ""},
    )
    assert p.returncode == 0
    parsed = json.loads(p.stdout)
    assert parsed["status"] == "skip"


def test_drift_canary_csv_count_logic() -> None:
    """Direct unit test of csv_row_count helper."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "graphrag_drift_canary", str(REPO_ROOT / "scripts" / "graphrag_drift_canary.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    n = mod.csv_row_count(REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "dimensions" / "SKILL_REGISTRY.csv")
    assert n == 5


# ── skill_neighbourhood helper ────────────────────────────────────────────────


def test_skill_neighbourhood_helper_handles_not_found() -> None:
    """When the skill_id is unknown, helper returns status=not_found, empty nodes/edges."""
    from akos.hlk_neo4j import skill_neighbourhood

    fake_session = MagicMock()
    fake_run = MagicMock()
    fake_run.single.return_value = None
    fake_session.run.return_value = fake_run

    out = skill_neighbourhood(fake_session, "SKILL-DOES-NOT-EXIST-V99")
    assert out["status"] == "not_found"
    assert out["skill_id"] == "SKILL-DOES-NOT-EXIST-V99"
    assert out["nodes"] == []
    assert out["edges"] == []


def test_skill_neighbourhood_helper_bounded_depth_and_limit() -> None:
    """Helper clamps depth to [1,3] and limit to [1,200]. When the skill is
    found, the response carries the clamped depth value."""
    from akos.hlk_neo4j import skill_neighbourhood

    # Fake session: first .run() returns root match (skill found); second .run() returns
    # the topics+owners aggregation.
    fake_session = MagicMock()
    root_call = MagicMock()
    root_call.single.return_value = {"s": MagicMock(element_id="123", labels=["Skill"])}
    agg_call = MagicMock()
    agg_call.single.return_value = {"topics": [], "owners": []}
    sib_call = MagicMock()
    sib_call.__iter__ = lambda self: iter([])
    fake_session.run.side_effect = [root_call, agg_call, sib_call]

    out = skill_neighbourhood(fake_session, "SKILL-X", depth=99, limit=999)
    assert out["status"] == "ok"
    assert out["depth"] == 3  # clamped from 99


def test_skill_neighbourhood_not_found_minimal_response() -> None:
    """The not_found shape returns status + skill_id + empty nodes/edges (no depth field)."""
    from akos.hlk_neo4j import skill_neighbourhood

    fake_session = MagicMock()
    fake_session.run.return_value.single.return_value = None
    out = skill_neighbourhood(fake_session, "SKILL-MISSING-V99")
    assert out["status"] == "not_found"
    assert out["skill_id"] == "SKILL-MISSING-V99"
    assert out["nodes"] == []
    assert out["edges"] == []


# ── MCP tool registration ────────────────────────────────────────────────────


def test_mcp_server_imports_skill_neighbourhood() -> None:
    """The MCP server file must import skill_neighbourhood at module load."""
    text = (REPO_ROOT / "scripts" / "hlk_graph_mcp_server.py").read_text(encoding="utf-8")
    assert "skill_neighbourhood" in text
    assert "@mcp.tool()" in text  # confirm tool decorator is present
    # Confirm the new tool function is defined
    assert "def hlk_graph_skill_neighbourhood(" in text


def test_agent_capabilities_madeira_has_skill_neighbourhood_tool() -> None:
    caps = json.loads(
        (REPO_ROOT / "config" / "agent-capabilities.json").read_text(encoding="utf-8")
    )
    madeira_tools = caps["roles"]["madeira"]["allowed_tools"]
    assert "hlk_graph_skill_neighbourhood" in madeira_tools


# ── Verification profile ─────────────────────────────────────────────────────


def test_verification_profile_neo4j_drift_smoke_registered() -> None:
    profiles_path = REPO_ROOT / "config" / "verification-profiles.json"
    data = json.loads(profiles_path.read_text(encoding="utf-8"))
    profiles = data.get("profiles", {})
    assert "neo4j_governance_kg_drift_smoke" in profiles
    profile = profiles["neo4j_governance_kg_drift_smoke"]
    step_ids = [s["id"] for s in profile.get("steps", [])]
    assert "neo4j_drift_canary" in step_ids
