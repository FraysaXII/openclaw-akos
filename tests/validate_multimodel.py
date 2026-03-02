"""Validation tests for the multi-model architecture.

Tests model-tiers.json integrity, environment profile completeness,
assembled prompt sizes, and tier/config consistency -- leveraging
Pydantic models from akos.models for schema validation.

Run:
    python -m pytest tests/validate_multimodel.py -v
"""

import subprocess
import sys

import pytest

from conftest import REPO_ROOT

from akos.models import (
    Alert,
    Baseline,
    EnvironmentOverlay,
    ModelTiersRegistry,
    load_alerts,
    load_baselines,
    load_tiers,
)
from akos.io import load_json

CONFIG_DIR = REPO_ROOT / "config"
TIERS_PATH = CONFIG_DIR / "model-tiers.json"
ENVS_DIR = CONFIG_DIR / "environments"
PROMPTS_DIR = REPO_ROOT / "prompts"
ASSEMBLED_DIR = PROMPTS_DIR / "assembled"
SCRIPTS_DIR = REPO_ROOT / "scripts"

BOOTSTRAP_MAX_CHARS = 20_000
VALID_VARIANTS = {"compact", "standard", "full"}


# ---------------------------------------------------------------------------
# model-tiers.json -- Pydantic does the heavy lifting
# ---------------------------------------------------------------------------

class TestModelTiers:
    @pytest.fixture(autouse=True)
    def _load(self):
        self.registry = load_tiers(TIERS_PATH)

    def test_loads_and_validates(self):
        assert self.registry is not None

    def test_has_all_four_tiers(self):
        assert set(self.registry.tiers.keys()) == {"small", "medium", "large", "sota"}

    def test_variant_overlays_cover_all_variants(self):
        assert set(self.registry.variantOverlays.keys()) >= VALID_VARIANTS

    def test_overlay_files_exist(self):
        overlay_dir = PROMPTS_DIR / "overlays"
        for variant, overlays in self.registry.variantOverlays.items():
            for overlay_name in overlays:
                assert (overlay_dir / overlay_name).exists(), \
                    f"Overlay file missing for variant '{variant}': {overlay_name}"

    def test_no_duplicate_models_across_tiers(self):
        all_models = []
        for tier in self.registry.tiers.values():
            all_models.extend(tier.models)
        assert len(all_models) == len(set(all_models))


# ---------------------------------------------------------------------------
# Environment Profiles -- validated via Pydantic EnvironmentOverlay
# ---------------------------------------------------------------------------

class TestEnvironmentProfiles:
    def _env_names(self) -> list[str]:
        return [p.stem for p in ENVS_DIR.glob("*.json")]

    def test_at_least_one_environment_exists(self):
        assert len(self._env_names()) > 0

    def test_each_overlay_validates_as_pydantic_model(self):
        for name in self._env_names():
            data = load_json(ENVS_DIR / f"{name}.json")
            overlay = EnvironmentOverlay.model_validate(data)
            assert overlay.agents.defaults.model.primary, \
                f"Environment '{name}' missing model.primary"

    def test_each_env_has_env_example(self):
        for name in self._env_names():
            path = ENVS_DIR / f"{name}.env.example"
            assert path.exists(), f"Missing .env.example: {path}"

    def test_env_examples_contain_no_real_secrets(self):
        secret_patterns = ["sk-", "ghp_", "Bearer ", "-----BEGIN"]
        for path in ENVS_DIR.glob("*.env.example"):
            content = path.read_text(encoding="utf-8")
            for pattern in secret_patterns:
                assert pattern not in content, \
                    f"{path.name} contains potential secret pattern: {pattern}"


# ---------------------------------------------------------------------------
# Eval configs -- validated via Pydantic Alert / Baseline
# ---------------------------------------------------------------------------

class TestEvalConfigs:
    def test_alerts_validate(self):
        alerts = load_alerts(CONFIG_DIR / "eval" / "alerts.json")
        assert len(alerts) >= 3

    def test_baselines_validate(self):
        baselines = load_baselines(CONFIG_DIR / "eval" / "baselines.json")
        assert len(baselines) == 4

    def test_has_critical_severity_alert(self):
        alerts = load_alerts(CONFIG_DIR / "eval" / "alerts.json")
        assert any(a.severity == "critical" for a in alerts)


# ---------------------------------------------------------------------------
# Assembled Prompts
# ---------------------------------------------------------------------------

class TestAssembledPrompts:
    @pytest.fixture(autouse=True)
    def _build(self):
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
