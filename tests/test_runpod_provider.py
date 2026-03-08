"""Tests for akos.runpod_provider -- RunPod GPU infrastructure wrapper.

All tests mock the ``runpod`` SDK so no real API calls are made.
"""

from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from akos.runpod_provider import (
    EndpointInfo,
    GpuInfo,
    HealthStatus,
    InferenceResult,
    RunPodEndpointConfig,
    RunPodProvider,
)


@pytest.fixture()
def runpod_config() -> RunPodEndpointConfig:
    return RunPodEndpointConfig(
        gpuIds=["AMPERE_80"],
        templateName="test-template",
        vllmImage="runpod/worker-v1-vllm:stable-cuda12.8.0",
        modelName="deepseek-ai/DeepSeek-R1-Test",
        maxModelLen=32768,
        activeWorkers=0,
        maxWorkers=1,
        idleTimeoutSeconds=60,
    )


@pytest.fixture()
def mock_runpod():
    """Patch the ``runpod`` module used inside runpod_provider."""
    with patch("akos.runpod_provider.runpod") as mock_rp:
        mock_rp.api_key = None
        yield mock_rp


@pytest.fixture()
def provider_env():
    """Set required env vars for a RunPod provider."""
    original = os.environ.get("RUNPOD_API_KEY")
    os.environ["RUNPOD_API_KEY"] = "test-key-123"
    yield
    if original is None:
        os.environ.pop("RUNPOD_API_KEY", None)
    else:
        os.environ["RUNPOD_API_KEY"] = original


class TestRunPodProviderDisabled:
    def test_no_api_key_disables_provider(self, runpod_config: RunPodEndpointConfig):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        assert not provider.enabled

    def test_disabled_ensure_endpoint_returns_none(
        self, runpod_config: RunPodEndpointConfig
    ):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        assert provider.ensure_endpoint() is None

    def test_disabled_health_check_returns_unhealthy(
        self, runpod_config: RunPodEndpointConfig
    ):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        status = provider.health_check()
        assert not status.healthy

    def test_disabled_infer_returns_disabled_status(
        self, runpod_config: RunPodEndpointConfig
    ):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        result = provider.infer("test prompt")
        assert result.status == "disabled"

    def test_disabled_scale_returns_false(
        self, runpod_config: RunPodEndpointConfig
    ):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        assert not provider.scale(0, 1)

    def test_disabled_teardown_returns_false(
        self, runpod_config: RunPodEndpointConfig
    ):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        assert not provider.teardown()

    def test_disabled_gpu_availability_returns_empty(
        self, runpod_config: RunPodEndpointConfig
    ):
        os.environ.pop("RUNPOD_API_KEY", None)
        provider = RunPodProvider(runpod_config)
        assert provider.get_gpu_availability() == []


class TestRunPodProviderEnabled:
    @patch("akos.runpod_provider._runpod_available", True)
    def test_enabled_with_api_key(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        provider = RunPodProvider(runpod_config)
        assert provider.enabled

    @patch("akos.runpod_provider._runpod_available", True)
    def test_ensure_endpoint_creates_new(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        mock_runpod.create_template.return_value = {"id": "tmpl-abc"}
        mock_runpod.create_endpoint.return_value = {"id": "ep-xyz"}

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)
        provider = RunPodProvider(runpod_config)
        info = provider.ensure_endpoint()

        assert info is not None
        assert info.endpoint_id == "ep-xyz"
        assert "ep-xyz" in info.url
        assert info.template_id == "tmpl-abc"
        mock_runpod.create_template.assert_called_once()
        mock_runpod.create_endpoint.assert_called_once()

    @patch("akos.runpod_provider._runpod_available", True)
    def test_ensure_endpoint_reuses_existing(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-existing"
        mock_runpod.get_endpoints.return_value = [
            {"id": "ep-existing", "templateId": "tmpl-old"}
        ]

        provider = RunPodProvider(runpod_config)
        info = provider.ensure_endpoint()

        assert info is not None
        assert info.endpoint_id == "ep-existing"
        mock_runpod.create_template.assert_not_called()

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_health_check_healthy(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"
        mock_ep = MagicMock()
        mock_ep.health.return_value = {
            "status": "READY",
            "workers": {"ready": 1, "running": 0},
            "jobsInQueue": 0,
        }
        mock_runpod.Endpoint.return_value = mock_ep

        provider = RunPodProvider(runpod_config)
        status = provider.health_check()

        assert status.healthy
        assert status.workers_ready == 1
        assert status.queue_depth == 0

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_health_check_unhealthy(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"
        mock_ep = MagicMock()
        mock_ep.health.return_value = {
            "status": "SCALING",
            "workers": {"ready": 0, "running": 0},
            "jobsInQueue": 5,
        }
        mock_runpod.Endpoint.return_value = mock_ep

        provider = RunPodProvider(runpod_config)
        status = provider.health_check()

        assert not status.healthy
        assert status.queue_depth == 5

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_infer_success(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"
        mock_ep = MagicMock()
        mock_ep.run_sync.return_value = {
            "output": "Hello world",
            "usage": {"total_tokens": 42},
        }
        mock_runpod.Endpoint.return_value = mock_ep

        provider = RunPodProvider(runpod_config)
        result = provider.infer("Say hello")

        assert result.status == "completed"
        assert result.output == "Hello world"
        assert result.tokens_used == 42
        assert result.latency_ms > 0

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_infer_error(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"
        mock_ep = MagicMock()
        mock_ep.run_sync.side_effect = RuntimeError("timeout")
        mock_runpod.Endpoint.return_value = mock_ep

        provider = RunPodProvider(runpod_config)
        result = provider.infer("test")

        assert result.status == "error"
        assert result.output == ""

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_scale(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"

        provider = RunPodProvider(runpod_config)
        assert provider.scale(1, 3)

        mock_runpod.update_endpoint_template.assert_called_once_with(
            endpoint_id="ep-test", workers_min=1, workers_max=3
        )
        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_teardown_scale_to_zero(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"

        provider = RunPodProvider(runpod_config)
        assert provider.teardown()
        assert provider.endpoint_id == "ep-test"

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_teardown_delete(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        os.environ["RUNPOD_ENDPOINT_ID"] = "ep-test"

        provider = RunPodProvider(runpod_config)
        assert provider.teardown(delete=True)
        assert provider.endpoint_id is None
        mock_runpod.delete_endpoint.assert_called_once_with("ep-test")

        os.environ.pop("RUNPOD_ENDPOINT_ID", None)

    @patch("akos.runpod_provider._runpod_available", True)
    def test_get_gpu_availability(
        self, mock_runpod, provider_env, runpod_config: RunPodEndpointConfig
    ):
        mock_runpod.get_gpus.return_value = [
            {
                "id": "AMPERE_80",
                "displayName": "A100 80GB",
                "memoryInGb": 80,
                "communityCloud": True,
                "secureCloud": True,
                "communityPrice": 0.00116,
            },
        ]

        provider = RunPodProvider(runpod_config)
        gpus = provider.get_gpu_availability()

        assert len(gpus) == 1
        assert gpus[0].gpu_id == "AMPERE_80"
        assert gpus[0].memory_gb == 80
        assert gpus[0].available


class TestRunPodEndpointConfig:
    def test_default_config_valid(self):
        config = RunPodEndpointConfig()
        assert config.maxWorkers >= 1
        assert config.maxModelLen > 0

    def test_custom_config(self):
        config = RunPodEndpointConfig(
            gpuIds=["ADA_80"],
            templateName="custom",
            maxWorkers=5,
            envVars={"CUSTOM_KEY": "value"},
        )
        assert config.gpuIds == ["ADA_80"]
        assert config.maxWorkers == 5
        assert config.envVars["CUSTOM_KEY"] == "value"

    def test_health_check_defaults(self):
        config = RunPodEndpointConfig()
        assert config.healthCheck.intervalSeconds == 60
        assert config.healthCheck.unhealthyThreshold == 3
