"""Validation tests for the multi-model architecture.

Tests model-tiers.json integrity, environment profile completeness,
assembled prompt sizes, and tier/config consistency.

Run:
    python -m pytest tests/validate_multimodel.py -v
"""

import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
TIERS_PATH = CONFIG_DIR / "model-tiers.json"
ENVS_DIR = CONFIG_DIR / "environments"
PROMPTS_DIR = REPO_ROOT / "prompts"
ASSEMBLED_DIR = PROMPTS_DIR / "assembled"
SCRIPTS_DIR = REPO_ROOT / "scripts"

BOOTSTRAP_MAX_CHARS = 20_000
VALID_TIERS = {"small", "medium", "large", "sota"}
VALID_VARIANTS = {"compact", "standard", "full"}
VALID_THINKING = {"off", "low", "medium", "high"}


def _load_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# model-tiers.json
# ---------------------------------------------------------------------------

class TestModelTiers:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.data = _load_json(TIERS_PATH)

    def test_has_tiers_key(self):
        assert "tiers" in self.data

    def test_has_variant_overlays_key(self):
        assert "variantOverlays" in self.data

    def test_all_tier_names_are_valid(self):
        for tier_name in self.data["tiers"]:
            assert tier_name in VALID_TIERS, f"Unknown tier: {tier_name}"

    def test_each_tier_has_required_fields(self):
        required = {"contextBudget", "thinkingDefault", "promptVariant", "description", "models"}
        for tier_name, tier_data in self.data["tiers"].items():
            missing = required - set(tier_data.keys())
            assert not missing, f"Tier '{tier_name}' missing: {missing}"

    def test_thinking_defaults_are_valid(self):
        for tier_name, tier_data in self.data["tiers"].items():
            assert tier_data["thinkingDefault"] in VALID_THINKING, \
                f"Tier '{tier_name}' has invalid thinkingDefault: {tier_data['thinkingDefault']}"

    def test_prompt_variants_are_valid(self):
        for tier_name, tier_data in self.data["tiers"].items():
            assert tier_data["promptVariant"] in VALID_VARIANTS, \
                f"Tier '{tier_name}' has invalid promptVariant: {tier_data['promptVariant']}"

    def test_each_tier_has_at_least_one_model(self):
        for tier_name, tier_data in self.data["tiers"].items():
            assert len(tier_data["models"]) > 0, f"Tier '{tier_name}' has no models"

    def test_no_duplicate_models_across_tiers(self):
        all_models = []
        for tier_data in self.data["tiers"].values():
            all_models.extend(tier_data["models"])
        assert len(all_models) == len(set(all_models)), \
            f"Duplicate models found across tiers"

    def test_variant_overlays_cover_all_variants(self):
        for variant in VALID_VARIANTS:
            assert variant in self.data["variantOverlays"], \
                f"variantOverlays missing variant: {variant}"

    def test_overlay_files_exist(self):
        overlay_dir = PROMPTS_DIR / "overlays"
        for variant, overlays in self.data["variantOverlays"].items():
            for overlay_name in overlays:
                assert (overlay_dir / overlay_name).exists(), \
                    f"Overlay file missing for variant '{variant}': {overlay_name}"


# ---------------------------------------------------------------------------
# Environment Profiles
# ---------------------------------------------------------------------------

class TestEnvironmentProfiles:
    def _env_names(self) -> list[str]:
        return [p.stem for p in ENVS_DIR.glob("*.json")]

    def test_at_least_one_environment_exists(self):
        assert len(self._env_names()) > 0

    def test_each_env_has_json_overlay(self):
        for name in self._env_names():
            path = ENVS_DIR / f"{name}.json"
            assert path.exists(), f"Missing JSON overlay: {path}"

    def test_each_env_has_env_example(self):
        for name in self._env_names():
            path = ENVS_DIR / f"{name}.env.example"
            assert path.exists(), f"Missing .env.example: {path}"

    def test_each_overlay_specifies_model_primary(self):
        for name in self._env_names():
            data = _load_json(ENVS_DIR / f"{name}.json")
            model = data.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
            assert model, f"Environment '{name}' missing agents.defaults.model.primary"

    def test_each_overlay_specifies_thinking_default(self):
        for name in self._env_names():
            data = _load_json(ENVS_DIR / f"{name}.json")
            td = data.get("agents", {}).get("defaults", {}).get("thinkingDefault")
            assert td is not None, f"Environment '{name}' missing thinkingDefault"
            assert td in VALID_THINKING, f"Environment '{name}' invalid thinkingDefault: {td}"

    def test_env_examples_contain_no_real_secrets(self):
        secret_patterns = ["sk-", "ghp_", "Bearer ", "-----BEGIN"]
        for path in ENVS_DIR.glob("*.env.example"):
            content = path.read_text(encoding="utf-8")
            for pattern in secret_patterns:
                assert pattern not in content, \
                    f"{path.name} contains potential secret pattern: {pattern}"


# ---------------------------------------------------------------------------
# Assembled Prompts
# ---------------------------------------------------------------------------

class TestAssembledPrompts:
    @pytest.fixture(autouse=True)
    def _build(self):
        """Run the assemble script before testing."""
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "assemble-prompts.py")],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"assemble-prompts.py failed: {result.stderr}"

    def test_all_variants_exist(self):
        for variant in VALID_VARIANTS:
            for agent in ["ARCHITECT", "EXECUTOR"]:
                path = ASSEMBLED_DIR / f"{agent}_PROMPT.{variant}.md"
                assert path.exists(), f"Missing assembled prompt: {path}"

    def test_assembled_prompts_under_bootstrap_max_chars(self):
        for path in ASSEMBLED_DIR.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            assert len(content) <= BOOTSTRAP_MAX_CHARS, \
                f"{path.name} is {len(content)} chars, exceeds {BOOTSTRAP_MAX_CHARS}"

    def test_compact_is_smallest_variant(self):
        for agent in ["ARCHITECT", "EXECUTOR"]:
            compact = (ASSEMBLED_DIR / f"{agent}_PROMPT.compact.md").stat().st_size
            full = (ASSEMBLED_DIR / f"{agent}_PROMPT.full.md").stat().st_size
            assert compact <= full, \
                f"{agent} compact ({compact}B) should be <= full ({full}B)"

    def test_assembled_prompts_are_nonempty(self):
        for path in ASSEMBLED_DIR.glob("*.md"):
            assert path.stat().st_size > 0, f"{path.name} is empty"


# ---------------------------------------------------------------------------
# Script Existence
# ---------------------------------------------------------------------------

class TestScriptsExist:
    def test_assemble_prompts_exists(self):
        assert (SCRIPTS_DIR / "assemble-prompts.py").exists()

    def test_switch_model_exists(self):
        assert (SCRIPTS_DIR / "switch-model.py").exists()

    def test_bootstrap_py_exists(self):
        assert (SCRIPTS_DIR / "bootstrap.py").exists()

    def test_bootstrap_ps1_exists(self):
        assert (SCRIPTS_DIR / "bootstrap.ps1").exists()


# ---------------------------------------------------------------------------
# Base + Overlay Structure
# ---------------------------------------------------------------------------

class TestPromptStructure:
    def test_base_dir_exists(self):
        assert (PROMPTS_DIR / "base").is_dir()

    def test_overlays_dir_exists(self):
        assert (PROMPTS_DIR / "overlays").is_dir()

    def test_architect_base_exists(self):
        assert (PROMPTS_DIR / "base" / "ARCHITECT_BASE.md").exists()

    def test_executor_base_exists(self):
        assert (PROMPTS_DIR / "base" / "EXECUTOR_BASE.md").exists()

    def test_base_prompts_contain_must_directives(self):
        for base_file in (PROMPTS_DIR / "base").glob("*.md"):
            content = base_file.read_text(encoding="utf-8")
            assert "MUST" in content, \
                f"{base_file.name} should contain MUST directives"
