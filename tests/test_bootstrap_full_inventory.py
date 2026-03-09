from __future__ import annotations

from scripts.bootstrap import _collect_unresolved_provider_inputs


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
