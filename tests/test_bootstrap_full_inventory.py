from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from akos.io import RUNTIME_ENV_PLACEHOLDERS, deploy_openclaw_plugins, ensure_memory_journal_files
from scripts.bootstrap import (
    _backfill_env_placeholders,
    _collect_unresolved_provider_inputs,
    _seed_env_file_if_missing,
    _sync_tool_profiles_from_capability_matrix,
)


def test_unresolved_provider_inputs_do_not_remove_provider_blocks(monkeypatch) -> None:
    monkeypatch.delenv("OLLAMA_GPU_URL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    config = {
        "models": {
            "providers": {
                "ollama-gpu": {"baseUrl": "${OLLAMA_GPU_URL}", "models": [{"id": "qwen3:32b"}]},
                "openai": {"apiKey": {"source": "env", "id": "OPENAI_API_KEY"}, "models": []},
            }
        }
    }

    issues = _collect_unresolved_provider_inputs(config)
    assert "ollama-gpu" in config["models"]["providers"]
    assert "openai" in config["models"]["providers"]
    assert any("OLLAMA_GPU_URL" in issue for issue in issues)
    assert any("OPENAI_API_KEY" in issue for issue in issues)


def test_seed_env_file_creates_env_when_missing(tmp_path: Path) -> None:
    _seed_env_file_if_missing(tmp_path)
    env_file = tmp_path / ".env"
    assert env_file.exists()
    content = env_file.read_text()
    assert f"OLLAMA_GPU_URL={RUNTIME_ENV_PLACEHOLDERS['OLLAMA_GPU_URL']}" in content
    assert f"VLLM_SHADOW_URL={RUNTIME_ENV_PLACEHOLDERS['VLLM_SHADOW_URL']}" in content


def test_seed_env_file_skips_when_env_exists(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("EXISTING=true\n")
    _seed_env_file_if_missing(tmp_path)
    assert env_file.read_text() == "EXISTING=true\n"


def test_backfill_env_placeholders_adds_missing_values(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("EXISTING=true\nOLLAMA_API_KEY=ollama-local\n", encoding="utf-8")
    _backfill_env_placeholders(tmp_path)
    text = env_file.read_text(encoding="utf-8")
    assert f"RUNPOD_API_KEY={RUNTIME_ENV_PLACEHOLDERS['RUNPOD_API_KEY']}" in text
    assert f"VLLM_RUNPOD_URL={RUNTIME_ENV_PLACEHOLDERS['VLLM_RUNPOD_URL']}" in text
    assert f"VLLM_SHADOW_URL={RUNTIME_ENV_PLACEHOLDERS['VLLM_SHADOW_URL']}" in text


def test_bootstrap_preserves_template_gateway_tool_blocks() -> None:
    merged = {
        "agents": {
            "list": [
                {
                    "id": "orchestrator",
                    "tools": {
                        "profile": "minimal",
                        "alsoAllow": ["read", "web_search", "memory_search", "finance_quote"],
                        "deny": ["write", "exec"],
                    },
                },
                {
                    "id": "madeira",
                    "tools": {
                        "profile": "minimal",
                        "alsoAllow": ["hlk_role", "finance_search"],
                        "deny": ["write", "edit", "apply_patch", "exec", "browser"],
                    },
                },
            ]
        }
    }

    _sync_tool_profiles_from_capability_matrix(merged)

    orch_tools = merged["agents"]["list"][0]["tools"]
    madeira_tools = merged["agents"]["list"][1]["tools"]

    assert orch_tools["profile"] == "minimal"
    assert orch_tools["alsoAllow"] == ["read", "web_search", "memory_search", "finance_quote"]
    assert orch_tools["deny"] == ["write", "exec"]

    assert madeira_tools["profile"] == "minimal"
    assert madeira_tools["alsoAllow"] == ["hlk_role", "finance_search"]
    assert madeira_tools["deny"] == ["write", "edit", "apply_patch", "exec", "browser"]
    assert "allow" not in madeira_tools


def test_bootstrap_migrates_legacy_allow_to_also_allow() -> None:
    merged = {
        "agents": {
            "list": [
                {
                    "id": "architect",
                    "tools": {
                        "profile": "minimal",
                        "allow": ["read", "web_search", "hlk_search"],
                    },
                },
            ]
        }
    }

    _sync_tool_profiles_from_capability_matrix(merged)

    architect_tools = merged["agents"]["list"][0]["tools"]
    assert architect_tools["profile"] == "minimal"
    assert architect_tools["alsoAllow"] == ["read", "web_search", "hlk_search"]
    assert "allow" not in architect_tools


def test_bootstrap_uses_runtime_profile_override() -> None:
    merged = {
        "agents": {
            "list": [
                {
                    "id": "madeira",
                    "tools": {
                        "profile": "minimal",
                        "alsoAllow": ["hlk_role"],
                    },
                },
            ]
        }
    }

    _sync_tool_profiles_from_capability_matrix(merged)

    madeira_tools = merged["agents"]["list"][0]["tools"]
    assert madeira_tools["profile"] == "minimal"


def test_deploy_openclaw_plugins_syncs_repo_state(tmp_path: Path) -> None:
    source_root = tmp_path / "openclaw-plugins"
    plugin_dir = source_root / "akos-runtime-tools"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "openclaw.plugin.json").write_text('{"id":"akos-runtime-tools"}\n', encoding="utf-8")
    (plugin_dir / "index.ts").write_text("export default {};\n", encoding="utf-8")

    oc_home = tmp_path / ".openclaw"
    stale_target = oc_home / "extensions" / "akos-runtime-tools"
    stale_target.mkdir(parents=True)
    (stale_target / "index.ts").write_text("stale\n", encoding="utf-8")

    deployed = deploy_openclaw_plugins(oc_home, plugin_source_root=source_root)

    assert stale_target.joinpath("openclaw.plugin.json").read_text(encoding="utf-8") == '{"id":"akos-runtime-tools"}\n'
    assert stale_target.joinpath("index.ts").read_text(encoding="utf-8") == "export default {};\n"
    assert {path.name for path in deployed} == {"openclaw.plugin.json", "index.ts"}


def test_ensure_memory_journal_files_creates_continuity_notes(tmp_path: Path) -> None:
    oc_home = tmp_path / ".openclaw"
    ws_dir = oc_home / "workspace-madeira"
    ws_dir.mkdir(parents=True)
    (ws_dir / "MEMORY.md").write_text("# MEMORY\n\nState\n", encoding="utf-8")

    deployed = ensure_memory_journal_files(oc_home, days=2)

    memory_dir = ws_dir / "memory"
    assert memory_dir.is_dir()
    created_names = sorted(path.name for path in deployed)
    assert len(created_names) == 2
    assert all(name.endswith(".md") for name in created_names)
    first_note = memory_dir / created_names[0]
    assert "Bootstrap-generated continuity mirror" in first_note.read_text(encoding="utf-8")


def test_load_env_file_rejects_malformed_lines(tmp_path: Path) -> None:
    from akos.io import load_env_file

    env_path = tmp_path / "bad.env"
    env_path.write_text('GOOD=value\nBROKEN"oops"\n', encoding="utf-8")

    with pytest.raises(ValueError):
        load_env_file(env_path)
