"""Tests for scripts/log-watcher.py answer-quality review helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import MagicMock

from conftest import REPO_ROOT


def _load_log_watcher_module():
    spec = importlib.util.spec_from_file_location(
        "akos_log_watcher_test",
        REPO_ROOT / "scripts" / "log-watcher.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_answer_quality_record_for_direct_lookup():
    mod = _load_log_watcher_module()
    interaction = {
        "session_id": "session-1",
        "agent_role": "madeira",
        "user_text": "Who is the CTO?",
        "tool_calls": ["hlk_role"],
        "tool_results": [{"best_role": {"role_name": "CTO"}}],
        "post_compaction": False,
    }
    message = {
        "provider": "ollama",
        "model": "qwen3:8b",
        "content": [{
            "type": "text",
            "text": "The CTO role exists.\nSource: baseline_organisation.csv",
        }],
    }

    record = mod._build_answer_quality_record(interaction, message)

    assert record["route_kind"] == "hlk_direct_lookup"
    assert record["citation_asset"] == "baseline_organisation.csv"
    assert record["best_match_present"] is True
    assert record["residual_flags"] == []
    assert record["quality_score"] == 1.0


def test_build_answer_quality_record_flags_admin_drift():
    mod = _load_log_watcher_module()
    interaction = {
        "session_id": "session-2",
        "agent_role": "madeira",
        "user_text": "I need to restructure the Finance area.",
        "tool_calls": ["hlk_area"],
        "tool_results": [],
        "post_compaction": False,
    }
    message = {
        "provider": "ollama",
        "model": "qwen3:8b",
        "content": [{
            "type": "text",
            "text": "Would you like to merge roles or adjust reporting lines? Please specify your objectives.",
        }],
    }

    record = mod._build_answer_quality_record(interaction, message)

    assert record["route_kind"] == "admin"
    assert "missing_explicit_escalation" in record["residual_flags"]
    assert "admin_brainstorm_drift" in record["residual_flags"]
    assert record["quality_score"] < 1.0


def test_scan_madeira_sessions_writes_local_mirror(tmp_path: Path):
    mod = _load_log_watcher_module()
    sessions_dir = tmp_path / ".openclaw" / "agents" / "madeira" / "sessions"
    sessions_dir.mkdir(parents=True)
    session_file = sessions_dir / "session-a.jsonl"
    session_file.write_text(
        '\n'.join([
            '{"type":"message","id":"user-1","parentId":"root","message":{"role":"user","content":[{"type":"text","text":"Who is the CTO?"}]}}',
            '{"type":"message","id":"assistant-tool","parentId":"user-1","message":{"role":"assistant","content":[{"type":"toolCall","name":"hlk_role","arguments":{"role_name":"CTO"}}]}}',
            '{"type":"message","id":"tool-result","parentId":"assistant-tool","message":{"role":"toolResult","content":[{"type":"text","text":"{\\"status\\": \\"ok\\", \\"best_role\\": {\\"role_name\\": \\"CTO\\"}}"}]}}',
            '{"type":"message","id":"assistant-final","parentId":"tool-result","message":{"role":"assistant","provider":"ollama","model":"qwen3:8b","content":[{"type":"text","text":"The CTO role exists. Source: baseline_organisation.csv"}]}}',
        ]) + '\n',
        encoding="utf-8",
    )

    reporter = MagicMock()
    offsets: dict[Path, int] = {}
    session_key_maps: dict[Path, dict[str, str]] = {}
    interaction_state: dict[str, dict] = {}
    mirror_dir = tmp_path / "telemetry"

    mod._scan_madeira_sessions(
        tmp_path / ".openclaw",
        offsets,
        session_key_maps,
        interaction_state,
        mirror_dir,
        reporter,
        dry_run=False,
    )

    mirror_files = list(mirror_dir.glob("madeira-answer-quality-*.jsonl"))
    assert len(mirror_files) == 1
    assert "baseline_organisation.csv" in mirror_files[0].read_text(encoding="utf-8")
    reporter.trace_answer_quality.assert_called_once()
