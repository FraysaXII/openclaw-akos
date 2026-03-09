from __future__ import annotations

import json
from pathlib import Path

from scripts.doctor import _is_env_backed, _iter_sensitive_paths, check_sensitive_key_signals


def test_iter_sensitive_paths_returns_key_paths_only() -> None:
    data = {
        "models": {"providers": {"openai": {"apiKey": {"source": "env", "id": "OPENAI_API_KEY"}}}},
        "authToken": "${AUTH_TOKEN}",
    }
    paths = [path for path, _ in _iter_sensitive_paths(data)]
    assert "models.providers.openai.apiKey" in paths
    assert "authToken" in paths


def test_is_env_backed_detects_safe_patterns() -> None:
    assert _is_env_backed("${OPENAI_API_KEY}")
    assert _is_env_backed({"source": "env", "id": "OPENAI_API_KEY"})
    assert not _is_env_backed("hardcoded-secret")


def test_sensitive_key_signals_classify_actionable_vs_informational(tmp_path: Path) -> None:
    oc_home = tmp_path
    cfg = {
        "models": {
            "providers": {
                "openai": {"apiKey": {"source": "env", "id": "OPENAI_API_KEY"}},
                "custom": {"apiKey": "hardcoded"},
            }
        }
    }
    (oc_home / "openclaw.json").write_text(json.dumps(cfg), encoding="utf-8")
    checks = check_sensitive_key_signals(oc_home)
    levels = [level for level, _ in checks]
    assert "PASS" in levels
    assert "WARN" in levels
