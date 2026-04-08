"""Tests for the GPU CLI (scripts/gpu.py) and model catalog.

Covers catalog validation, VRAM-driven GPU auto-selection, vLLM command
generation per model family, deploy/teardown/status flows (mocked),
env key propagation, and OpenClaw overlay config assertions.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.model_catalog import CatalogEntry, GpuDefault, load_catalog
from akos.models import PodConfig
from akos.state import ActiveInfra

REPO_ROOT = Path(__file__).resolve().parent.parent


# ── Fixtures ─────────────────────────────────────────────────────────


@pytest.fixture
def catalog():
    return load_catalog()


@pytest.fixture
def deepseek_entry(catalog):
    return next(e for e in catalog if "DeepSeek R1 70B" in e.displayName)


@pytest.fixture
def llama8b_entry(catalog):
    return next(e for e in catalog if "8B" in e.displayName)


@pytest.fixture
def qwq_entry(catalog):
    return next(e for e in catalog if "QwQ" in e.displayName)


@pytest.fixture
def mistral_entry(catalog):
    return next(e for e in catalog if "Mistral" in e.displayName)


@pytest.fixture
def tmp_oc_home(tmp_path):
    oc = tmp_path / ".openclaw"
    oc.mkdir()
    (oc / ".env").write_text("VLLM_RUNPOD_URL=http://localhost:8000/v1\n", encoding="utf-8")
    return oc


@pytest.fixture
def tmp_pod_env(tmp_path):
    env_file = tmp_path / "gpu-runpod-pod.env"
    env_file.write_text("RUNPOD_API_KEY=test\nVLLM_RUNPOD_URL=\n", encoding="utf-8")
    return env_file


# ── Catalog loading ──────────────────────────────────────────────────


class TestCatalogLoading:
    def test_all_entries_parse(self, catalog):
        assert len(catalog) >= 9

    def test_no_duplicate_served_names_within_same_quant(self, catalog):
        seen: dict[tuple[str, str | None], str] = {}
        for e in catalog:
            key = (e.servedModelName, e.quantization)
            assert key not in seen, f"Duplicate: {e.hfId} vs {seen[key]} (same served name + quantization)"
            seen[key] = e.hfId

    def test_no_duplicate_hf_ids(self, catalog):
        ids = [e.hfId for e in catalog]
        assert len(ids) == len(set(ids))

    def test_every_entry_has_tool_parser(self, catalog):
        for e in catalog:
            assert e.toolCallParser, f"{e.displayName} missing toolCallParser"

    def test_every_entry_has_default_gpu(self, catalog):
        for e in catalog:
            assert e.defaultGpu.type
            assert e.defaultGpu.count >= 1

    def test_reasoning_models_flagged(self, catalog):
        reasoning_names = {e.displayName for e in catalog if e.reasoning}
        assert "DeepSeek R1 70B" in reasoning_names
        assert "QwQ 32B (reasoning)" in reasoning_names

    def test_awq_entry_exists(self, catalog):
        awq_entries = [e for e in catalog if e.quantization == "awq"]
        assert len(awq_entries) >= 1
        awq = awq_entries[0]
        assert awq.vramGb < 140, "AWQ model should need less VRAM than bf16"
        assert awq.reasoning is True

    def test_quantization_field_present(self, catalog):
        for e in catalog:
            assert hasattr(e, "quantization"), f"{e.displayName} missing quantization field"

    def test_non_reasoning_models_unflagged(self, catalog):
        for e in catalog:
            if "Llama 3.1 70B" in e.displayName:
                assert not e.reasoning


# ── VRAM auto-GPU selection ──────────────────────────────────────────


class TestVramAutoGpu:
    def test_70b_on_a100_needs_2(self, deepseek_entry):
        assert deepseek_entry.min_gpus_for(80) == 2

    def test_70b_on_h200_needs_1(self, deepseek_entry):
        assert deepseek_entry.min_gpus_for(141) == 1

    def test_8b_on_rtx4090_needs_1(self, llama8b_entry):
        assert llama8b_entry.min_gpus_for(24) == 1

    def test_32b_on_a100_needs_1(self, qwq_entry):
        assert qwq_entry.min_gpus_for(80) == 1

    def test_32b_on_rtx4090_needs_3(self, qwq_entry):
        assert qwq_entry.min_gpus_for(24) == 3

    def test_123b_on_h100_needs_4(self, mistral_entry):
        assert mistral_entry.min_gpus_for(80) >= 4

    def test_formula_matches_ceil(self, catalog):
        for entry in catalog:
            for vram in [24, 48, 80, 141]:
                expected = max(1, math.ceil(entry.vramGb / vram))
                assert entry.min_gpus_for(vram) == expected


# ── vLLM command generation per model family ─────────────────────────


class TestVllmCommandPerFamily:
    def _build_cmd(self, entry: CatalogEntry) -> list[str]:
        from scripts.gpu import _apply_catalog_to_pod_config
        pc = PodConfig(gpuCount=entry.defaultGpu.count)
        _apply_catalog_to_pod_config(pc, entry)
        return pc.build_vllm_command()

    def test_deepseek_has_deepseek_v3_parser(self, deepseek_entry):
        cmd = self._build_cmd(deepseek_entry)
        assert "--tool-call-parser" in cmd
        idx = cmd.index("--tool-call-parser")
        assert cmd[idx + 1] == "deepseek_v3"

    def test_deepseek_has_reasoning_parser(self, deepseek_entry):
        cmd = self._build_cmd(deepseek_entry)
        assert "--reasoning-parser" in cmd
        idx = cmd.index("--reasoning-parser")
        assert cmd[idx + 1] == "deepseek_r1"

    def test_llama_has_llama3_json_parser(self, llama8b_entry):
        cmd = self._build_cmd(llama8b_entry)
        idx = cmd.index("--tool-call-parser")
        assert cmd[idx + 1] == "llama3_json"

    def test_llama_no_reasoning_parser(self, llama8b_entry):
        cmd = self._build_cmd(llama8b_entry)
        assert "--reasoning-parser" not in cmd

    def test_qwen_has_hermes_parser(self, qwq_entry):
        cmd = self._build_cmd(qwq_entry)
        idx = cmd.index("--tool-call-parser")
        assert cmd[idx + 1] == "hermes"

    def test_mistral_has_mistral_parser(self, mistral_entry):
        cmd = self._build_cmd(mistral_entry)
        idx = cmd.index("--tool-call-parser")
        assert cmd[idx + 1] == "mistral"

    def test_served_model_name_matches(self, catalog):
        for entry in catalog:
            cmd = self._build_cmd(entry)
            idx = cmd.index("--served-model-name")
            assert cmd[idx + 1] == entry.servedModelName

    def test_model_name_matches(self, catalog):
        for entry in catalog:
            cmd = self._build_cmd(entry)
            idx = cmd.index("--model")
            assert cmd[idx + 1] == entry.hfId
            assert "python" not in cmd[0], "CMD must not start with python"

    def test_awq_model_has_quantization_flag(self, catalog):
        awq_entries = [e for e in catalog if e.quantization == "awq"]
        assert len(awq_entries) >= 1
        for entry in awq_entries:
            cmd = self._build_cmd(entry)
            assert "--quantization" in cmd
            idx = cmd.index("--quantization")
            assert cmd[idx + 1] == "awq"


# ── Overlay JSON wiring ─────────────────────────────────────────────


class TestOverlayWiring:
    def test_reasoning_model_sets_thinking_medium(self, tmp_path, deepseek_entry):
        overlay = tmp_path / "gpu-runpod-pod.json"
        overlay.write_text(json.dumps({"agents": {"defaults": {}}, "pod": {}}), encoding="utf-8")
        from scripts.gpu import _update_overlay_json
        with patch("scripts.gpu.REPO_ROOT", tmp_path):
            (tmp_path / "config" / "environments").mkdir(parents=True)
            target = tmp_path / "config" / "environments" / "gpu-runpod-pod.json"
            target.write_text(json.dumps({"agents": {"defaults": {}}}), encoding="utf-8")
            _update_overlay_json(deepseek_entry)
            data = json.loads(target.read_text(encoding="utf-8"))
        assert data["agents"]["defaults"]["thinkingDefault"] == "medium"
        assert "deepseek-r1-70b" in data["agents"]["defaults"]["model"]["primary"]

    def test_non_reasoning_model_sets_thinking_off(self, tmp_path, llama8b_entry):
        from scripts.gpu import _update_overlay_json
        with patch("scripts.gpu.REPO_ROOT", tmp_path):
            (tmp_path / "config" / "environments").mkdir(parents=True)
            target = tmp_path / "config" / "environments" / "gpu-runpod-pod.json"
            target.write_text(json.dumps({"agents": {"defaults": {}}}), encoding="utf-8")
            _update_overlay_json(llama8b_entry)
            data = json.loads(target.read_text(encoding="utf-8"))
        assert data["agents"]["defaults"]["thinkingDefault"] == "off"
        assert "llama-3.1-8b" in data["agents"]["defaults"]["model"]["primary"]

    def test_serverless_overlay_wiring(self, tmp_path, deepseek_entry):
        from scripts.gpu import _update_serverless_overlay_json
        with patch("scripts.gpu.REPO_ROOT", tmp_path):
            (tmp_path / "config" / "environments").mkdir(parents=True)
            target = tmp_path / "config" / "environments" / "gpu-runpod.json"
            target.write_text(json.dumps({"agents": {"defaults": {}}, "runpod": {"envVars": {}}}), encoding="utf-8")
            _update_serverless_overlay_json(deepseek_entry)
            data = json.loads(target.read_text(encoding="utf-8"))
        assert data["agents"]["defaults"]["thinkingDefault"] == "medium"
        assert data["runpod"]["modelName"] == deepseek_entry.hfId
        assert data["runpod"]["envVars"]["TOOL_CALL_PARSER"] == "deepseek_v3"
        assert data["runpod"]["envVars"]["KV_CACHE_DTYPE"] == "auto"
        assert data["runpod"]["envVars"]["VLLM_ATTENTION_BACKEND"] == "TRITON_ATTN"


# ── _apply_catalog_to_pod_config ─────────────────────────────────────


class TestApplyCatalog:
    def test_sets_model_name(self, deepseek_entry):
        from scripts.gpu import _apply_catalog_to_pod_config
        pc = PodConfig(gpuCount=2)
        _apply_catalog_to_pod_config(pc, deepseek_entry)
        assert pc.modelName == deepseek_entry.hfId

    def test_sets_tool_parser(self, llama8b_entry):
        from scripts.gpu import _apply_catalog_to_pod_config
        pc = PodConfig(gpuCount=1)
        _apply_catalog_to_pod_config(pc, llama8b_entry)
        assert pc.envVars["TOOL_CALL_PARSER"] == "llama3_json"

    def test_removes_reasoning_parser_when_none(self, llama8b_entry):
        from scripts.gpu import _apply_catalog_to_pod_config
        pc = PodConfig(gpuCount=1, envVars={"REASONING_PARSER": "deepseek_r1"})
        _apply_catalog_to_pod_config(pc, llama8b_entry)
        assert "REASONING_PARSER" not in pc.envVars

    def test_sets_reasoning_parser_when_present(self, deepseek_entry):
        from scripts.gpu import _apply_catalog_to_pod_config
        pc = PodConfig(gpuCount=2)
        _apply_catalog_to_pod_config(pc, deepseek_entry)
        assert pc.envVars["REASONING_PARSER"] == "deepseek_r1"

    def test_applies_env_overrides(self, deepseek_entry):
        from scripts.gpu import _apply_catalog_to_pod_config
        pc = PodConfig(gpuCount=2)
        _apply_catalog_to_pod_config(pc, deepseek_entry)
        assert pc.envVars.get("KV_CACHE_DTYPE") == "fp8"


# ── Env key propagation ─────────────────────────────────────────────


class TestEnvKeyPropagation:
    def test_upsert_creates_key(self, tmp_path):
        from scripts.gpu import _upsert_env_line
        f = tmp_path / "test.env"
        f.write_text("A=1\n", encoding="utf-8")
        _upsert_env_line(f, "B", "2")
        text = f.read_text(encoding="utf-8")
        assert "B=2" in text
        assert "A=1" in text

    def test_upsert_updates_existing(self, tmp_path):
        from scripts.gpu import _upsert_env_line
        f = tmp_path / "test.env"
        f.write_text("A=old\n", encoding="utf-8")
        _upsert_env_line(f, "A", "new")
        text = f.read_text(encoding="utf-8")
        assert "A=new" in text
        assert "old" not in text

    def test_save_key_writes_to_both(self, tmp_path):
        from scripts.gpu import _save_key_to_env, _upsert_env_line
        pod_env = tmp_path / "config" / "environments" / "gpu-runpod-pod.env"
        pod_env.parent.mkdir(parents=True)
        pod_env.write_text("", encoding="utf-8")
        oc_env = tmp_path / ".openclaw" / ".env"
        oc_env.parent.mkdir(parents=True)
        oc_env.write_text("", encoding="utf-8")

        with patch("scripts.gpu.REPO_ROOT", tmp_path), \
             patch("scripts.gpu.resolve_openclaw_home", return_value=tmp_path / ".openclaw"):
            _save_key_to_env("TEST_KEY", "test_value")

        assert "TEST_KEY=test_value" in pod_env.read_text(encoding="utf-8")
        assert "TEST_KEY=test_value" in oc_env.read_text(encoding="utf-8")


# ── Deploy pod (mocked) ─────────────────────────────────────────────


class TestDeployPodMocked:
    @patch("scripts.gpu.time.sleep")
    @patch("scripts.gpu.RunPodProvider.probe_vllm_health")
    @patch("scripts.gpu.PodManager")
    @patch("scripts.gpu.save_state")
    @patch("scripts.gpu.load_state")
    @patch("scripts.gpu._update_overlay_json")
    @patch("scripts.gpu._save_key_to_env")
    @patch("scripts.gpu._pick_gpu", return_value=("NVIDIA A100-SXM4-80GB", 2))
    @patch("scripts.gpu._pick_model")
    @patch("scripts.gpu._ensure_hf_token", return_value="hf_test")
    @patch("scripts.gpu._ensure_api_key", return_value="rp_test_key")
    @patch("scripts.gpu.load_catalog")
    def test_deploy_creates_pod_and_saves_state(
        self, mock_catalog, mock_api, mock_hf, mock_pick_model,
        mock_pick_gpu, mock_save_env, mock_overlay, mock_load_state,
        mock_save_state, mock_pm_cls, mock_health, mock_sleep,
    ):
        from akos.runpod_provider import PodInfo

        entry = CatalogEntry(
            hfId="test/Model-70B", displayName="Test 70B", family="test",
            paramsBillions=70, vramGb=140, toolCallParser="hermes",
            servedModelName="test-70b", defaultGpu=GpuDefault(type="A100", count=2),
        )
        mock_catalog.return_value = [entry]
        mock_pick_model.return_value = entry

        mock_load_state.return_value = MagicMock(activeInfra=ActiveInfra())

        mock_pm = MagicMock()
        mock_pm.create_pod.return_value = PodInfo(
            pod_id="pod-abc", status="RUNNING", gpu_type="A100", gpu_count=2,
        )
        mock_pm_cls.return_value = mock_pm

        mock_health.return_value = MagicMock(healthy=True)

        with patch("scripts.gpu.load_json", return_value={"pod": {}}), \
             patch("akos.process.run", return_value=MagicMock(success=True)):
            from scripts.gpu import deploy_pod
            result = deploy_pod(dry_run=False)

        assert result == 0
        mock_pm.create_pod.assert_called_once()
        mock_save_state.assert_called_once()
        saved_infra = mock_save_state.call_args[0][1].activeInfra
        assert saved_infra.podId == "pod-abc"
        assert saved_infra.modelName == "test/Model-70B"

    @patch("scripts.gpu._pick_gpu", return_value=("NVIDIA A100-SXM4-80GB", 2))
    @patch("scripts.gpu._pick_model")
    @patch("scripts.gpu._ensure_hf_token", return_value="")
    @patch("scripts.gpu._ensure_api_key", return_value="rp_key")
    @patch("scripts.gpu.load_catalog")
    def test_dry_run_returns_zero(
        self, mock_catalog, mock_api, mock_hf, mock_pick_model, mock_pick_gpu,
    ):
        entry = CatalogEntry(
            hfId="test/Small-8B", displayName="Test 8B", family="test",
            paramsBillions=8, vramGb=18, toolCallParser="llama3_json",
            servedModelName="test-8b", defaultGpu=GpuDefault(type="RTX4090", count=1),
        )
        mock_catalog.return_value = [entry]
        mock_pick_model.return_value = entry

        with patch("scripts.gpu.load_json", return_value={"pod": {}}):
            from scripts.gpu import deploy_pod
            result = deploy_pod(dry_run=True)

        assert result == 0


class TestDeployServerlessMocked:
    @patch("scripts.gpu.save_state")
    @patch("scripts.gpu.load_state")
    @patch("scripts.gpu._update_serverless_overlay_json")
    @patch("scripts.gpu._pick_model")
    @patch("scripts.gpu.load_catalog")
    @patch("scripts.gpu._ensure_api_key", return_value="rp_test_key")
    def test_serverless_dry_run(
        self, mock_api, mock_catalog, mock_pick_model, mock_update, mock_load_state, mock_save_state
    ):
        entry = CatalogEntry(
            hfId="test/Model-70B", displayName="Test 70B", family="test",
            paramsBillions=70, vramGb=140, toolCallParser="hermes",
            servedModelName="test-70b", defaultGpu=GpuDefault(type="A100", count=2),
        )
        mock_catalog.return_value = [entry]
        mock_pick_model.return_value = entry
        from scripts.gpu import deploy_serverless
        result = deploy_serverless(dry_run=True)
        assert result == 0
        mock_update.assert_called_once()

    @patch("scripts.gpu.save_state")
    @patch("scripts.gpu.load_state")
    @patch("scripts.gpu._ensure_env_placeholders")
    @patch("scripts.gpu._update_serverless_overlay_json")
    @patch("scripts.gpu._pick_model")
    @patch("scripts.gpu.load_catalog")
    @patch("scripts.gpu._ensure_api_key", return_value="rp_test_key")
    def test_serverless_sets_active_infra(
        self, mock_api, mock_catalog, mock_pick_model, mock_update, mock_placeholders, mock_load_state, mock_save_state, tmp_path
    ):
        entry = CatalogEntry(
            hfId="test/Model-70B", displayName="Test 70B", family="test",
            paramsBillions=70, vramGb=140, toolCallParser="hermes",
            servedModelName="test-70b", defaultGpu=GpuDefault(type="A100", count=2),
        )
        mock_catalog.return_value = [entry]
        mock_pick_model.return_value = entry
        mock_load_state.return_value = MagicMock(activeInfra=ActiveInfra())
        tmp_oc = tmp_path / ".openclaw"
        env_file = tmp_oc / ".env"
        env_file.parent.mkdir(parents=True, exist_ok=True)
        env_file.write_text("RUNPOD_ENDPOINT_ID=ep-123\nVLLM_RUNPOD_URL=https://api.runpod.ai/v2/ep-123/openai/v1\n", encoding="utf-8")
        with patch("scripts.gpu.resolve_openclaw_home", return_value=tmp_oc), \
             patch("scripts.gpu.load_env_file", return_value={"RUNPOD_ENDPOINT_ID": "ep-123", "VLLM_RUNPOD_URL": "https://api.runpod.ai/v2/ep-123/openai/v1"}), \
             patch("akos.process.run", return_value=MagicMock(success=True)):
            from scripts.gpu import deploy_serverless
            result = deploy_serverless(dry_run=False)
        assert result == 0
        saved = mock_save_state.call_args[0][1]
        assert saved.activeInfra.type == "serverless"
        assert saved.activeInfra.endpointId == "ep-123"


# ── Teardown (mocked) ───────────────────────────────────────────────


class TestTeardownMocked:
    @patch("scripts.gpu.save_state")
    @patch("scripts.gpu.load_state")
    @patch("scripts.gpu.PodManager")
    def test_teardown_terminates_pod(self, mock_pm_cls, mock_load_state, mock_save_state):
        state = MagicMock()
        state.activeInfra = ActiveInfra(type="pod", podId="pod-xyz")
        mock_load_state.return_value = state

        mock_pm = MagicMock()
        mock_pm.terminate_pod.return_value = True
        mock_pm_cls.return_value = mock_pm

        import os
        with patch.dict(os.environ, {"RUNPOD_API_KEY": "key123", "RUNPOD_POD_ID": "pod-xyz"}), \
             patch("scripts.gpu.resolve_openclaw_home", return_value=Path("/tmp/oc")), \
             patch("akos.process.run", return_value=MagicMock(success=True)):
            from scripts.gpu import teardown_infra
            result = teardown_infra(dry_run=False)

        assert result == 0
        mock_pm.terminate_pod.assert_called_once_with("pod-xyz")
        saved = mock_save_state.call_args[0][1]
        assert saved.activeInfra.type == "local"
