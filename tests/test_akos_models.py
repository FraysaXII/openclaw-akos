"""Unit tests for akos.models Pydantic schemas.

Tests loading known-good JSON configs through Pydantic models,
and verifies that known-bad data raises validation errors.

Run:
    python -m pytest tests/test_akos_models.py -v
"""

import pytest
from pydantic import ValidationError

from akos.models import (
    AgentBlock,
    AgentEntry,
    AgentIdentity,
    AgentsDefaults,
    Alert,
    Baseline,
    ControlUiConfig,
    EnvironmentOverlay,
    GatewayConfig,
    ModelRef,
    ModelTiersRegistry,
    OpenClawConfig,
    OpenStackInstanceConfig,
    PodConfig,
    RunPodEndpointConfig,
    TierConfig,
)


# ---------------------------------------------------------------------------
# TierConfig
# ---------------------------------------------------------------------------

class TestTierConfig:
    def test_valid(self):
        t = TierConfig(
            contextBudget=16384,
            thinkingDefault="off",
            promptVariant="compact",
            description="Small models",
            models=["ollama/qwen3:8b"],
        )
        assert t.contextBudget == 16384

    def test_rejects_zero_context(self):
        with pytest.raises(ValidationError):
            TierConfig(
                contextBudget=0,
                thinkingDefault="off",
                promptVariant="compact",
                description="bad",
                models=["x"],
            )

    def test_rejects_empty_models(self):
        with pytest.raises(ValidationError):
            TierConfig(
                contextBudget=1000,
                thinkingDefault="off",
                promptVariant="compact",
                description="bad",
                models=[],
            )

    def test_rejects_invalid_thinking(self):
        with pytest.raises(ValidationError):
            TierConfig(
                contextBudget=1000,
                thinkingDefault="ultra",
                promptVariant="compact",
                description="bad",
                models=["x"],
            )


# ---------------------------------------------------------------------------
# ModelTiersRegistry
# ---------------------------------------------------------------------------

class TestModelTiersRegistry:
    @pytest.fixture
    def registry(self):
        return ModelTiersRegistry(
            tiers={
                "small": TierConfig(contextBudget=16384, thinkingDefault="off", promptVariant="compact", description="s", models=["m1"]),
                "medium": TierConfig(contextBudget=32768, thinkingDefault="low", promptVariant="standard", description="m", models=["m2"]),
                "large": TierConfig(contextBudget=131072, thinkingDefault="medium", promptVariant="full", description="l", models=["m3"]),
                "sota": TierConfig(contextBudget=200000, thinkingDefault="high", promptVariant="full", description="st", models=["m4"]),
            },
            variantOverlays={"compact": [], "standard": ["a.md"], "full": ["a.md", "b.md"]},
        )

    def test_lookup_known_model(self, registry):
        result = registry.lookup_tier("m1")
        assert result is not None
        assert result[0] == "small"

    def test_lookup_unknown_model(self, registry):
        assert registry.lookup_tier("unknown") is None

    def test_rejects_duplicate_models(self):
        with pytest.raises(ValidationError, match="Duplicate"):
            ModelTiersRegistry(
                tiers={
                    "small": TierConfig(contextBudget=1000, thinkingDefault="off", promptVariant="compact", description="s", models=["dup"]),
                    "medium": TierConfig(contextBudget=2000, thinkingDefault="low", promptVariant="standard", description="m", models=["dup"]),
                    "large": TierConfig(contextBudget=3000, thinkingDefault="medium", promptVariant="full", description="l", models=["x"]),
                    "sota": TierConfig(contextBudget=4000, thinkingDefault="high", promptVariant="full", description="st", models=["y"]),
                },
                variantOverlays={"compact": [], "standard": [], "full": []},
            )


# ---------------------------------------------------------------------------
# AgentBlock + OpenClawConfig
# ---------------------------------------------------------------------------

class TestAgentBlock:
    def test_valid_with_alias(self):
        data = {
            "defaults": {"model": {"primary": "ollama/qwen3:8b"}, "thinkingDefault": "off", "verboseDefault": "on"},
            "list": [
                {"id": "architect", "name": "Architect", "workspace": "/ws-a", "identity": {"name": "Architect"}},
            ],
        }
        block = AgentBlock.model_validate(data)
        assert len(block.agents) == 1

    def test_rejects_missing_defaults(self):
        with pytest.raises(ValidationError):
            AgentBlock.model_validate({"list": []})


class TestOpenClawConfig:
    def test_minimal_valid(self):
        config = OpenClawConfig(
            agents=AgentBlock(
                defaults=AgentsDefaults(model=ModelRef(primary="ollama/qwen3:8b")),
                agents=[],
            ),
        )
        assert config.gateway.port == 18789


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------

class TestAlert:
    def test_realtime_contains_match(self):
        a = Alert(
            alert_id="test", description="test", condition="command CONTAINS 'chmod'",
            evaluation_window="real-time", severity="critical",
        )
        assert a.matches_realtime({"command": "chmod 777 /etc/passwd"})
        assert not a.matches_realtime({"command": "ls -la"})

    def test_realtime_equals_match(self):
        a = Alert(
            alert_id="test", description="test", condition="tool_name == 'canvas.eval'",
            evaluation_window="real-time", severity="high",
        )
        assert a.matches_realtime({"tool_name": "canvas.eval"})
        assert not a.matches_realtime({"tool_name": "web_search"})

    def test_realtime_starts_with_match(self):
        a = Alert(
            alert_id="test", description="test", condition="target_path STARTS_WITH '/etc/'",
            evaluation_window="real-time", severity="critical",
        )
        assert a.matches_realtime({"target_path": "/etc/shadow"})
        assert not a.matches_realtime({"target_path": "/home/user"})

    def test_non_realtime_never_matches(self):
        a = Alert(
            alert_id="test", description="test", condition="command CONTAINS 'rm'",
            evaluation_window="7d", severity="low",
        )
        assert not a.matches_realtime({"command": "rm -rf /"})

    def test_and_condition(self):
        a = Alert(
            alert_id="test", description="test",
            condition="tool_name == 'shell' AND command CONTAINS 'rm'",
            evaluation_window="real-time", severity="critical",
        )
        assert a.matches_realtime({"tool_name": "shell", "command": "rm file"})
        assert not a.matches_realtime({"tool_name": "shell", "command": "ls"})
        assert not a.matches_realtime({"tool_name": "read", "command": "rm file"})


# ---------------------------------------------------------------------------
# Baseline
# ---------------------------------------------------------------------------

class TestBaseline:
    def test_passes_gte(self):
        b = Baseline(metric_id="m", target_value=0.85, comparator=">=")
        assert b.passes(0.9)
        assert b.passes(0.85)
        assert not b.passes(0.5)

    def test_passes_lte(self):
        b = Baseline(metric_id="m", target_value=100, comparator="<=")
        assert b.passes(50)
        assert not b.passes(200)

    def test_maximize_always_passes(self):
        b = Baseline(metric_id="m", target_value=0.5, comparator="maximize")
        assert b.passes(0.0)

    def test_none_target_always_passes(self):
        b = Baseline(metric_id="m", target_value=None)
        assert b.passes(999)


# ---------------------------------------------------------------------------
# EnvironmentOverlay
# ---------------------------------------------------------------------------

class TestEnvironmentOverlay:
    def test_valid(self):
        data = {
            "agents": {
                "defaults": {
                    "model": {"primary": "ollama/qwen3:8b"},
                    "thinkingDefault": "off",
                    "verboseDefault": "on",
                },
            },
        }
        overlay = EnvironmentOverlay.model_validate(data)
        assert overlay.agents.defaults.model.primary == "ollama/qwen3:8b"

    def test_with_openstack_block(self):
        data = {
            "agents": {
                "defaults": {
                    "model": {"primary": "vllm-shadow/deepseek-r1-70b"},
                    "thinkingDefault": "medium",
                },
            },
            "openstack": {
                "region": "FRDUN02",
                "flavor": "boost-c8m12-gpu-a4500-4",
                "gpuType": "RTX A4500",
                "gpuCount": 4,
                "gpuVramGb": 20,
            },
        }
        overlay = EnvironmentOverlay.model_validate(data)
        assert overlay.openstack is not None
        assert overlay.openstack.region == "FRDUN02"
        assert overlay.openstack.gpuCount == 4

    def test_openstack_optional(self):
        data = {
            "agents": {
                "defaults": {
                    "model": {"primary": "ollama/qwen3:8b"},
                    "thinkingDefault": "off",
                },
            },
        }
        overlay = EnvironmentOverlay.model_validate(data)
        assert overlay.openstack is None


# ---------------------------------------------------------------------------
# PodConfig -- quantization and vLLM command generation
# ---------------------------------------------------------------------------

class TestPodConfigQuantization:
    def test_quantization_flag_emitted(self):
        pc = PodConfig(envVars={"QUANTIZATION": "awq"})
        cmd = pc.build_vllm_command()
        assert "--quantization" in cmd
        idx = cmd.index("--quantization")
        assert cmd[idx + 1] == "awq"

    def test_no_quantization_when_unset(self):
        pc = PodConfig(envVars={})
        cmd = pc.build_vllm_command()
        assert "--quantization" not in cmd

    def test_enforce_eager_flag(self):
        pc = PodConfig(envVars={"ENFORCE_EAGER": "true"})
        cmd = pc.build_vllm_command()
        assert "--enforce-eager" in cmd

    def test_no_enforce_eager_when_false(self):
        pc = PodConfig(envVars={"ENFORCE_EAGER": "false"})
        cmd = pc.build_vllm_command()
        assert "--enforce-eager" not in cmd

    def test_max_num_batched_tokens_flag(self):
        pc = PodConfig(envVars={"MAX_NUM_BATCHED_TOKENS": "16384"})
        cmd = pc.build_vllm_command()
        assert "--max-num-batched-tokens" in cmd
        idx = cmd.index("--max-num-batched-tokens")
        assert cmd[idx + 1] == "16384"

    def test_awq_forces_float16_dtype(self):
        pc = PodConfig(envVars={"QUANTIZATION": "awq", "DTYPE": "bfloat16"})
        cmd = pc.build_vllm_command()
        idx = cmd.index("--dtype")
        assert cmd[idx + 1] == "float16"


class TestRunPodEndpointConfigCompat:
    def test_awq_forces_float16_dtype(self):
        cfg = RunPodEndpointConfig(
            vllmImage="runpod/worker-v1-vllm:v2.14.0",
            envVars={"QUANTIZATION": "awq", "DTYPE": "bfloat16"},
        )
        assert cfg.envVars["DTYPE"] == "float16"

    def test_runpod_worker_fp8_is_downgraded_for_stability(self):
        cfg = RunPodEndpointConfig(
            vllmImage="runpod/worker-v1-vllm:v2.14.0",
            envVars={"KV_CACHE_DTYPE": "fp8"},
        )
        assert cfg.envVars["KV_CACHE_DTYPE"] == "auto"
        assert cfg.envVars["VLLM_ATTENTION_BACKEND"] == "TRITON_ATTN"


# ---------------------------------------------------------------------------
# OpenStackInstanceConfig
# ---------------------------------------------------------------------------

class TestOpenStackInstanceConfig:
    def test_defaults(self):
        cfg = OpenStackInstanceConfig()
        assert cfg.region == "FRDUN02"
        assert cfg.gpuType == "RTX A4500"
        assert cfg.gpuCount == 4
        assert cfg.gpuVramGb == 20
        assert cfg.vllmPort == 8080

    def test_custom_values(self):
        cfg = OpenStackInstanceConfig(
            region="DEFRA01",
            flavor="boost-c8m12-gpu-a4500-8",
            gpuCount=8,
            gpuVramGb=20,
        )
        assert cfg.region == "DEFRA01"
        assert cfg.gpuCount == 8


# ---------------------------------------------------------------------------
# GatewayConfig with controlUi
# ---------------------------------------------------------------------------

class TestGatewayConfig:
    def test_control_ui_title_default(self):
        gw = GatewayConfig()
        assert gw.controlUi.title == "HLK Intelligence Platform"

    def test_control_ui_title_custom(self):
        gw = GatewayConfig(controlUi=ControlUiConfig(title="Custom Title"))
        assert gw.controlUi.title == "Custom Title"
