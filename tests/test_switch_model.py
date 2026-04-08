import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_switch_model_module():
    path = REPO_ROOT / "scripts" / "switch-model.py"
    spec = importlib.util.spec_from_file_location("switch_model_module", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_seed_full_provider_inventory_adds_missing_provider(monkeypatch):
    module = _load_switch_model_module()
    template = {
        "models": {
            "providers": {
                "ollama": {"models": [{"id": "qwen3:8b"}]},
                "vllm-shadow": {"models": [{"id": "deepseek-r1-70b"}]},
            }
        }
    }
    monkeypatch.setattr(module, "load_json", lambda _: template)

    existing = {"models": {"providers": {"ollama": {"models": [{"id": "custom"}]}}}}
    seeded = module._seed_full_provider_inventory(existing)

    assert "vllm-shadow" in seeded["models"]["providers"]
    assert seeded["models"]["providers"]["ollama"] == {"models": [{"id": "custom"}]}


def test_seed_full_provider_inventory_creates_models_block(monkeypatch):
    module = _load_switch_model_module()
    template = {
        "models": {
            "providers": {
                "ollama": {"models": [{"id": "qwen3:8b"}]},
            }
        }
    }
    monkeypatch.setattr(module, "load_json", lambda _: template)

    seeded = module._seed_full_provider_inventory({})

    assert seeded["models"]["providers"]["ollama"]["models"][0]["id"] == "qwen3:8b"


def test_find_env_file_prefers_real_env(monkeypatch, tmp_path):
    module = _load_switch_model_module()
    env_dir = tmp_path / "config" / "environments"
    env_dir.mkdir(parents=True)
    env_file = env_dir / "dev-local.env"
    env_file.write_text("A=1\n", encoding="utf-8")
    (env_dir / "dev-local.env.example").write_text("A=2\n", encoding="utf-8")
    monkeypatch.setattr(module, "ENVS_DIR", env_dir)

    assert module.find_env_file("dev-local") == env_file


def test_find_env_file_does_not_use_example(monkeypatch, tmp_path):
    module = _load_switch_model_module()
    env_dir = tmp_path / "config" / "environments"
    env_dir.mkdir(parents=True)
    (env_dir / "dev-local.env.example").write_text("A=2\n", encoding="utf-8")
    monkeypatch.setattr(module, "ENVS_DIR", env_dir)

    assert module.find_env_file("dev-local") is None
