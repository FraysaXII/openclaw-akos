import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_inventory_module():
    path = REPO_ROOT / "scripts" / "legacy" / "verify_openclaw_inventory.py"
    spec = importlib.util.spec_from_file_location("verify_inventory_module", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_expected_default_primary_model_uses_active_env_overlay(monkeypatch, tmp_path):
    module = _load_inventory_module()
    home = tmp_path / "home"
    oc_home = home / ".openclaw"
    oc_home.mkdir(parents=True)
    (oc_home / ".akos-state.json").write_text(
        json.dumps({"activeEnvironment": "dev-local"}),
        encoding="utf-8",
    )

    env_dir = tmp_path / "repo" / "config" / "environments"
    env_dir.mkdir(parents=True)
    (env_dir / "dev-local.json").write_text(
        json.dumps(
            {
                "agents": {
                    "defaults": {
                        "model": {"primary": "ollama/deepseek-r1:14b"}
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(module, "REPO_ROOT", tmp_path / "repo")
    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))

    assert module.expected_default_primary_model() == "ollama/deepseek-r1:14b"


def test_expected_default_primary_model_falls_back_without_state(monkeypatch, tmp_path):
    module = _load_inventory_module()
    home = tmp_path / "home"
    home.mkdir(parents=True)

    monkeypatch.setattr(module.Path, "home", staticmethod(lambda: home))

    assert module.expected_default_primary_model() == module.EXPECTED["default_primary_model"]
