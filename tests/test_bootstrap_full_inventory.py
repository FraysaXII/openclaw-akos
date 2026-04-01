from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

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
    example = Path("config/environments/dev-local.env.example")
    if not example.exists():
        return
    _seed_env_file_if_missing(tmp_path)
    env_file = tmp_path / ".env"
    assert env_file.exists()
    content = env_file.read_text()
    assert "OLLAMA_GPU_URL" in content


def test_seed_env_file_skips_when_env_exists(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("EXISTING=true\n")
    _seed_env_file_if_missing(tmp_path)
    assert env_file.read_text() == "EXISTING=true\n"


def test_backfill_env_placeholders_adds_missing_values(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("EXISTING=true\nOLLAMA_API_KEY=ollama-local\n", encoding="utf-8")
    cfg_dir = tmp_path / "config" / "environments"
    cfg_dir.mkdir(parents=True)
    example = cfg_dir / "dev-local.env.example"
    example.write_text(
        "OLLAMA_API_KEY=ollama-local\nRUNPOD_API_KEY=not-configured\nVLLM_RUNPOD_URL=http://localhost:8000/v1\n",
        encoding="utf-8",
    )
    with patch("scripts.bootstrap.REPO_ROOT", tmp_path):
        _backfill_env_placeholders(tmp_path)
    text = env_file.read_text(encoding="utf-8")
    assert "RUNPOD_API_KEY=not-configured" in text
    assert "VLLM_RUNPOD_URL=http://localhost:8000/v1" in text


def test_bootstrap_preserves_template_allowlists_for_minimal_roles() -> None:
    merged = {
        "agents": {
            "list": [
                {
                    "id": "orchestrator",
                    "tools": {
                        "profile": "minimal",
                        "allow": ["web_search", "memory_store", "finance_quote"],
                    },
                },
                {
                    "id": "architect",
                    "tools": {
                        "profile": "minimal",
                        "allow": ["web_search", "browser_snapshot", "finance_search"],
                    },
                },
            ]
        }
    }

    _sync_tool_profiles_from_capability_matrix(merged)

    orch_tools = merged["agents"]["list"][0]["tools"]
    arch_tools = merged["agents"]["list"][1]["tools"]

    assert orch_tools["allow"] == ["web_search", "memory_store", "finance_quote"]
    assert arch_tools["allow"] == ["web_search", "browser_snapshot", "finance_search"]
    assert "read_file" not in orch_tools["allow"]
    assert "filesystem_read" not in arch_tools["allow"]
