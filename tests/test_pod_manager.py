"""Tests for PodManager REST API in akos/runpod_provider.py."""

import json
from unittest.mock import MagicMock, patch

import pytest

from akos.runpod_provider import PodInfo, PodManager


class TestPodManagerDisabled:
    def test_no_api_key_disables(self):
        pm = PodManager("")
        assert not pm.enabled

    def test_create_pod_returns_none(self):
        pm = PodManager("")
        assert pm.create_pod(name="test", gpu_type_id="A100") is None

    def test_get_pod_returns_none(self):
        pm = PodManager("")
        assert pm.get_pod("abc") is None

    def test_list_pods_returns_empty(self):
        pm = PodManager("")
        assert pm.list_pods() == []

    def test_terminate_returns_false(self):
        pm = PodManager("")
        assert pm.terminate_pod("abc") is False


class TestPodManagerEnabled:
    @patch("akos.runpod_provider.urllib.request.urlopen")
    def test_create_pod_success(self, mock_urlopen):
        resp = MagicMock()
        resp.read.return_value = json.dumps({
            "id": "pod-123",
            "desiredStatus": "CREATED",
            "gpuCount": 2,
        }).encode()
        resp.status = 201
        resp.__enter__ = MagicMock(return_value=resp)
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp

        pm = PodManager("test-key")
        pod = pm.create_pod(name="test-pod", gpu_type_id="NVIDIA A100-SXM4-80GB", gpu_count=2)
        assert pod is not None
        assert pod.pod_id == "pod-123"
        assert "pod-123" in pod.url

    @patch("akos.runpod_provider.urllib.request.urlopen")
    def test_get_pod_success(self, mock_urlopen):
        resp = MagicMock()
        resp.read.return_value = json.dumps({
            "id": "pod-456",
            "desiredStatus": "RUNNING",
            "gpuCount": 1,
        }).encode()
        resp.__enter__ = MagicMock(return_value=resp)
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp

        pm = PodManager("test-key")
        pod = pm.get_pod("pod-456")
        assert pod is not None
        assert pod.pod_id == "pod-456"
        assert pod.status == "RUNNING"

    @patch("akos.runpod_provider.urllib.request.urlopen")
    def test_list_pods_success(self, mock_urlopen):
        resp = MagicMock()
        resp.read.return_value = json.dumps([
            {"id": "p1", "desiredStatus": "RUNNING", "gpuCount": 1},
            {"id": "p2", "desiredStatus": "EXITED", "gpuCount": 2},
        ]).encode()
        resp.__enter__ = MagicMock(return_value=resp)
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp

        pm = PodManager("test-key")
        pods = pm.list_pods()
        assert len(pods) == 2
        assert pods[0].pod_id == "p1"

    @patch("akos.runpod_provider.urllib.request.urlopen")
    def test_terminate_pod_success(self, mock_urlopen):
        resp = MagicMock()
        resp.read.return_value = b"{}"
        resp.__enter__ = MagicMock(return_value=resp)
        resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = resp

        pm = PodManager("test-key")
        assert pm.terminate_pod("pod-789") is True

    @patch("akos.runpod_provider.urllib.request.urlopen", side_effect=Exception("network error"))
    def test_create_pod_failure(self, mock_urlopen):
        pm = PodManager("test-key")
        assert pm.create_pod(name="test", gpu_type_id="A100") is None


class TestPodConfig:
    def test_tensor_parallel_auto_derived(self):
        from akos.models import PodConfig
        config = PodConfig(gpuCount=4)
        assert config.envVars["TENSOR_PARALLEL_SIZE"] == "4"

    def test_tensor_parallel_overridden_by_gpu_count(self):
        from akos.models import PodConfig
        config = PodConfig(gpuCount=2, envVars={"TENSOR_PARALLEL_SIZE": "1"})
        assert config.envVars["TENSOR_PARALLEL_SIZE"] == "2"

    def test_build_vllm_command_includes_model(self):
        from akos.models import PodConfig
        config = PodConfig(modelName="deepseek-ai/DeepSeek-R1-Distill-Llama-70B", gpuCount=2)
        cmd = config.build_vllm_command()
        assert "--model" in cmd
        assert "deepseek-ai/DeepSeek-R1-Distill-Llama-70B" in cmd
        assert "--tensor-parallel-size" in cmd
        idx = cmd.index("--tensor-parallel-size")
        assert cmd[idx + 1] == "2"

    def test_build_vllm_command_port(self):
        from akos.models import PodConfig
        config = PodConfig(vllmPort=8080)
        cmd = config.build_vllm_command()
        assert "--port" in cmd
        idx = cmd.index("--port")
        assert cmd[idx + 1] == "8080"


class TestActiveInfra:
    def test_default_state_is_local(self):
        from akos.state import ActiveInfra
        infra = ActiveInfra()
        assert infra.type == "local"
        assert infra.podId == ""

    def test_pod_state(self):
        from akos.state import ActiveInfra
        infra = ActiveInfra(type="pod", podId="p123", url="https://p123-8080.proxy.runpod.net/v1")
        assert infra.type == "pod"
        assert infra.podId == "p123"
