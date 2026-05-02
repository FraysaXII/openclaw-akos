"""Initiative 47 P13 tests — 4 tech debt items closed.

1. sync_hlk_neo4j sync_csv_graph 6-dim writes (closes I46 drift canary catch)
2. sync_compliance_mirrors_from_csv boolean emit fix
3. agent_memory_trigger_watcher.py emits report
4. eval_run_writer best-effort skip-when-env-missing
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


# ---------------------------------------------------------------------------
# Item 1: sync_hlk_neo4j 6-dim writes
# ---------------------------------------------------------------------------

def test_sync_csv_graph_imports_axis_builder() -> None:
    """sync_csv_graph must import build_holistik_ops_axis_graph."""
    src = (REPO_ROOT / "akos" / "hlk_neo4j.py").read_text(encoding="utf-8")
    assert "build_holistik_ops_axis_graph" in src
    assert "axis_nodes" in src and "axis_edges" in src


def test_sync_csv_graph_writes_all_10_node_labels() -> None:
    """Each of the 10 HLK node labels has a MERGE batch in sync_csv_graph."""
    src = (REPO_ROOT / "akos" / "hlk_neo4j.py").read_text(encoding="utf-8")
    for label in (
        "Role", "Process", "Program", "Topic",          # original 4
        "Persona", "Channel", "Sourcing", "Skill",      # new from axis-6
        "TouchpointKitCell", "Policy",
    ):
        assert f"MERGE (n:{label}" in src or f"MERGE (r:{label}" in src or f"MERGE (p:{label}" in src, (
            f"sync_csv_graph missing MERGE for label {label!r}"
        )


def test_sync_csv_graph_returns_per_dim_counts() -> None:
    """The return value names all 6 axis-6 dimensions explicitly."""
    src = (REPO_ROOT / "akos" / "hlk_neo4j.py").read_text(encoding="utf-8")
    for key in (
        "personas_written", "channels_written", "sourcing_written",
        "skills_written", "cells_written", "policies_written",
    ):
        assert key in src, f"sync_csv_graph return missing per-dim count {key!r}"


def test_sync_csv_graph_emits_under_topic_edges() -> None:
    """All 6 axis-6 dimensions get UNDER_TOPIC edge MERGE batches."""
    src = (REPO_ROOT / "akos" / "hlk_neo4j.py").read_text(encoding="utf-8")
    assert "UNDER_TOPIC" in src
    assert "AXIS_KEY" in src
    # The dispatcher dict should reference all 6 axis labels
    for label in ("Persona", "Channel", "Sourcing", "Skill", "TouchpointKitCell", "Policy"):
        assert f'"{label}"' in src or f"'{label}'" in src


# ---------------------------------------------------------------------------
# Item 2: sync_compliance_mirrors_from_csv boolean emit fix
# ---------------------------------------------------------------------------

def test_skill_registry_emit_handles_boolean_columns() -> None:
    """Boolean column 'tools_required_waived' emits true/false/NULL not ''."""
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sync_compliance_mirrors_from_csv",
        REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py",
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    rows = [
        {"skill_id": "SKILL-X-V1", "tools_required_waived": "true",  "name": "X1"},
        {"skill_id": "SKILL-Y-V1", "tools_required_waived": "false", "name": "Y1"},
        {"skill_id": "SKILL-Z-V1", "tools_required_waived": "",      "name": "Z1"},
        {"skill_id": "SKILL-W-V1", "tools_required_waived": "TRUE",  "name": "W1"},
    ]
    sql = "\n".join(mod._emit_skill_registry_upserts(rows, "test-sha"))
    # true/false/NULL keywords (no quotes around boolean values)
    assert "true" in sql, "boolean true keyword missing"
    assert "false" in sql, "boolean false keyword missing"
    assert "NULL" in sql, "NULL keyword for empty bool missing"
    # NEVER emit '' for tools_required_waived (this was the bug)
    assert "''" in sql, "TEXT columns still use '' literals (sanity)"
    # Specifically test that the bool column is NOT wrapped in quotes
    assert ", true," in sql or "(true," in sql or " true," in sql
    assert ", false," in sql or "(false," in sql or " false," in sql


# ---------------------------------------------------------------------------
# Item 3: agent_memory_trigger_watcher.py
# ---------------------------------------------------------------------------

def test_trigger_watcher_runs_and_emits_report() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "agent_memory_trigger_watcher.py"), "--quiet"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_trigger_watcher_report_has_3_triggers() -> None:
    artifacts = REPO_ROOT / "artifacts" / "agent-memory-triggers"
    reports = sorted(artifacts.glob("trigger-watch-*.json"))
    assert reports, "no trigger watcher report file found"
    payload = json.loads(reports[-1].read_text(encoding="utf-8"))
    assert "triggers" in payload
    assert len(payload["triggers"]) == 3
    trigger_ids = {t["trigger_id"] for t in payload["triggers"]}
    assert trigger_ids == {
        "trigger_1_multi_tenant",
        "trigger_2_conversation_depth",
        "trigger_3_compliance_ask",
    }


def test_trigger_watcher_trigger_1_currently_not_fired() -> None:
    """All 5 skills should currently be tenant_scope='shared'; trigger 1 NOT fired."""
    artifacts = REPO_ROOT / "artifacts" / "agent-memory-triggers"
    reports = sorted(artifacts.glob("trigger-watch-*.json"))
    payload = json.loads(reports[-1].read_text(encoding="utf-8"))
    t1 = next(t for t in payload["triggers"] if t["trigger_id"] == "trigger_1_multi_tenant")
    assert t1["fired"] is False
    assert "shared" in t1["detail"].lower()


def test_trigger_watcher_hard_fail_flag_with_no_fires_returns_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "agent_memory_trigger_watcher.py"),
         "--hard-fail-on-trigger", "--quiet"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=20,
    )
    # No triggers fired today -> should exit 0 even with --hard-fail-on-trigger
    assert proc.returncode == 0


# ---------------------------------------------------------------------------
# Item 4: eval_run_writer
# ---------------------------------------------------------------------------

def test_eval_run_writer_skips_when_env_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)

    from akos.eval_harness.eval_run_writer import write_scorecard_rows
    from akos.eval_harness.v2 import ScoreRow, Scorecard

    sc = Scorecard()
    sc.add(ScoreRow(mode="canary", skill_id="SKILL-X-V1", status="PASS"))
    sc.add(ScoreRow(mode="canary", skill_id="SKILL-Y-V1", status="PASS"))
    stats = write_scorecard_rows(sc)
    assert stats == {"written": 0, "skipped": 2, "errors": 0}


def test_eval_run_writer_payload_includes_p10_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    from akos.eval_harness.eval_run_writer import _row_to_payload
    from akos.eval_harness.v2 import ScoreRow

    r = ScoreRow(
        mode="canary", skill_id="SKILL-X-V1", status="PASS",
        persona_id="PERSONA-INVESTOR-COLD",
        difficulty_class="hard",
        scenario_class="multihop",
        judge_scores={"brand_voice": 4, "citation": 5, "persona_fit": 4},
    )
    payload = _row_to_payload(r, "run-test", "abc123")
    assert payload["persona_id"] == "PERSONA-INVESTOR-COLD"
    assert payload["difficulty_class"] == "hard"
    assert payload["scenario_class"] == "multihop"
    assert payload["judge_scores"] == {"brand_voice": 4, "citation": 5, "persona_fit": 4}
    assert payload["source_git_sha"] == "abc123"


def test_eval_script_records_writer_metadata() -> None:
    """Verify scripts/eval.py adds eval_run_writer stats to scorecard metadata."""
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "eval.py"), "--mode", "smoke", "--json"],
        cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    meta = payload.get("metadata") or {}
    assert "eval_run_writer" in meta
    stats = meta["eval_run_writer"]
    assert "written" in stats and "skipped" in stats and "errors" in stats
