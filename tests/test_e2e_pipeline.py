"""E2E tests for the multi-agent pipeline via the FastAPI control plane.

Tests the Orchestrator -> Architect -> Executor -> Verifier pipeline
using the FastAPI TestClient.  RunPod tests use mocked SDK.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from akos.api import app
from akos.checkpoints import create_checkpoint, list_checkpoints, restore_checkpoint
from akos.io import AGENT_WORKSPACES, REPO_ROOT
from akos.tools import ToolRegistry

client = TestClient(app)


class TestE2EAgentPipeline:
    """Verify the 5-agent system is correctly wired end-to-end."""

    def test_all_five_agents_registered(self):
        resp = client.get("/agents")
        assert resp.status_code == 200
        data = resp.json()
        ids = {a["id"] for a in data}
        assert ids == {"madeira", "orchestrator", "architect", "executor", "verifier"}

    def test_agent_workspaces_match_config(self):
        assert "MADEIRA" in AGENT_WORKSPACES
        assert "ORCHESTRATOR" in AGENT_WORKSPACES
        assert "ARCHITECT" in AGENT_WORKSPACES
        assert "EXECUTOR" in AGENT_WORKSPACES
        assert "VERIFIER" in AGENT_WORKSPACES

    def test_prompt_bases_exist(self):
        base_dir = REPO_ROOT / "prompts" / "base"
        assert (base_dir / "MADEIRA_BASE.md").exists()
        assert (base_dir / "ORCHESTRATOR_BASE.md").exists()
        assert (base_dir / "ARCHITECT_BASE.md").exists()
        assert (base_dir / "EXECUTOR_BASE.md").exists()
        assert (base_dir / "VERIFIER_BASE.md").exists()

    def test_compact_prompts_exist(self):
        prompts_dir = REPO_ROOT / "prompts"
        assert (prompts_dir / "MADEIRA_PROMPT.md").exists()
        assert (prompts_dir / "ORCHESTRATOR_PROMPT.md").exists()
        assert (prompts_dir / "ARCHITECT_PROMPT.md").exists()
        assert (prompts_dir / "EXECUTOR_PROMPT.md").exists()
        assert (prompts_dir / "VERIFIER_PROMPT.md").exists()

    def test_workspace_scaffolds_exist(self):
        scaffold = REPO_ROOT / "config" / "workspace-scaffold"
        for agent in ["madeira", "orchestrator", "architect", "executor", "verifier"]:
            assert (scaffold / agent / "IDENTITY.md").exists()
        for name in ["MEMORY.md", "USER.md", "WORKFLOW_AUTO.md"]:
            assert (scaffold / "madeira" / name).exists()
        assert (scaffold / "madeira" / "memory" / "README.md").exists()
        assert (scaffold / "orchestrator" / "WORKFLOW_AUTO.md").exists()

    def test_health_endpoint_healthy(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_switch_dry_run_returns_model_info(self):
        resp = client.post("/switch", json={
            "environment": "dev-local",
            "dry_run": True,
        })
        data = resp.json()
        assert data["dry_run"] is True
        assert "model" in data
        assert "tier" in data
        assert "variant" in data


class TestE2ERunPodIntegration:
    """Verify RunPod integration wiring via the control plane."""

    def test_runpod_health_when_disabled(self):
        resp = client.get("/runpod/health")
        data = resp.json()
        assert data["enabled"] is False

    def test_runpod_config_in_gpu_env(self):
        config_path = REPO_ROOT / "config" / "environments" / "gpu-runpod.json"
        assert config_path.exists()
        import json
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        assert "runpod" in raw
        assert "gpuIds" in raw["runpod"]
        assert "healthCheck" in raw["runpod"]


class TestE2EToolsRegistry:
    """Verify the tool registry correctly reads config."""

    def test_registry_loads_servers(self):
        registry = ToolRegistry()
        assert "sequential-thinking" in registry.server_names
        assert "playwright" in registry.server_names
        assert "memory" in registry.server_names
        assert "filesystem" in registry.server_names
        assert "fetch" in registry.server_names
        assert "hlk" in registry.server_names

    def test_autonomous_tools_classified(self):
        registry = ToolRegistry()
        assert registry.classify("read_file") == "autonomous"
        assert registry.classify("memory_retrieve") == "autonomous"

    def test_approval_tools_classified(self):
        registry = ToolRegistry()
        assert registry.classify("write_file") == "requires_approval"
        assert registry.classify("memory_store") == "requires_approval"
        assert registry.classify("browser_console_exec") == "requires_approval"

    def test_unknown_tool_classified(self):
        registry = ToolRegistry()
        assert registry.classify("totally_fake_tool") == "unknown"


class TestE2ECheckpoints:
    """Verify checkpoints work with the API."""

    def test_checkpoint_api_create_and_list(self, tmp_path: Path):
        ws = tmp_path / "ws"
        ws.mkdir()
        (ws / "test.txt").write_text("data", encoding="utf-8")

        resp = client.post("/checkpoints", json={
            "name": "e2e-test",
            "workspace": str(ws),
        })
        assert resp.json()["created"] is True

        resp = client.get("/checkpoints", params={"workspace": str(ws)})
        data = resp.json()
        assert len(data["checkpoints"]) == 1
        assert data["checkpoints"][0]["name"] == "e2e-test"


class TestE2EOverlayConsistency:
    """Verify overlays referenced in model-tiers.json actually exist."""

    def test_all_referenced_overlays_exist(self):
        import json
        tiers_path = REPO_ROOT / "config" / "model-tiers.json"
        raw = json.loads(tiers_path.read_text(encoding="utf-8"))
        overlays_dir = REPO_ROOT / "prompts" / "overlays"

        for variant, entries in raw.get("variantOverlays", {}).items():
            for entry in entries:
                overlay_file = overlays_dir / entry["file"]
                assert overlay_file.exists(), f"Missing overlay: {overlay_file} (variant={variant})"

    def test_new_agents_in_openclaw_config(self):
        import json
        config_path = REPO_ROOT / "config" / "openclaw.json.example"
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        agent_ids = {a["id"] for a in raw["agents"]["list"]}
        assert agent_ids == {"madeira", "orchestrator", "architect", "executor", "verifier"}
