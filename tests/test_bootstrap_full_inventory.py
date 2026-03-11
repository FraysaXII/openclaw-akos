from __future__ import annotations

from pathlib import Path

from scripts.bootstrap import _collect_unresolved_provider_inputs, _seed_env_file_if_missing


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
