"""Tests for akos.api -- FastAPI control plane endpoints."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from akos.api import app

client = TestClient(app)


class TestHealth:
    def test_health_returns_ok(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "uptime_seconds" in data
        assert data["uptime_seconds"] >= 0

    def test_health_includes_runpod_status(self):
        resp = client.get("/health")
        data = resp.json()
        assert data["runpod"] in ("disabled", "healthy", "unhealthy")

    def test_health_includes_langfuse_status(self):
        resp = client.get("/health")
        data = resp.json()
        assert data["langfuse"] in ("enabled", "disabled")


class TestStatus:
    def test_status_returns_fields(self):
        resp = client.get("/status")
        assert resp.status_code == 200
        data = resp.json()
        for key in ("environment", "model", "tier", "variant"):
            assert key in data


class TestAgents:
    def test_agents_returns_list(self):
        resp = client.get("/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 5
        agent_ids = {a["id"] for a in data}
        assert agent_ids == {"madeira", "orchestrator", "architect", "executor", "verifier"}

    def test_agent_has_required_fields(self):
        resp = client.get("/agents")
        data = resp.json()
        for agent in data:
            assert "id" in agent
            assert "name" in agent
            assert "workspace" in agent
            assert "soul_md_exists" in agent
            assert "soul_md_chars" in agent


class TestAgentCapabilityDrift:
    def test_capability_drift_returns_real_issues(self):
        issues = [{"type": "tool_profile_mismatch", "agent": "madeira"}]
        with patch("akos.api._get_agent_capability_drift_issues", return_value=issues):
            resp = client.get("/agents/madeira/capability-drift")
        assert resp.status_code == 200
        data = resp.json()
        assert data["role"] == "madeira"
        assert data["runtime_profile"] == "minimal"
        assert data["drift_issues"] == issues
        assert data["policy_enforced"] is False

    def test_capability_drift_unknown_role(self):
        resp = client.get("/agents/ghost/capability-drift")
        assert resp.status_code == 200
        assert "error" in resp.json()


class TestFinance:
    def test_finance_quote_returns_payload(self):
        payload = {"status": "ok", "quotes": [{"ticker": "AAPL"}]}
        finance = SimpleNamespace(
            get_quote=lambda ticker: SimpleNamespace(model_dump=lambda exclude_none=True: payload)
        )
        with patch("akos.api._get_finance", return_value=finance):
            resp = client.get("/finance/quote/AAPL")
        assert resp.status_code == 200
        assert resp.json() == payload

    def test_finance_search_requires_query(self):
        resp = client.get("/finance/search")
        assert resp.status_code == 400

    def test_finance_sentiment_requires_tickers(self):
        resp = client.get("/finance/sentiment")
        assert resp.status_code == 400


class TestRouting:
    def test_classify_admin_route(self):
        resp = client.get("/routing/classify?q=I%20need%20to%20restructure%20the%20Finance%20area.")
        assert resp.status_code == 200
        data = resp.json()
        assert data["route"] == "admin_escalate"
        assert data["must_escalate"] is True

    def test_classify_requires_query(self):
        resp = client.get("/routing/classify")
        assert resp.status_code == 400


class TestSwitch:
    def test_switch_dry_run(self):
        resp = client.post("/switch", json={
            "environment": "dev-local",
            "dry_run": True,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["dry_run"] is True
        assert data["environment"] == "dev-local"

    def test_switch_invalid_environment(self):
        resp = client.post("/switch", json={
            "environment": "nonexistent-env",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data


class TestRunPod:
    def test_runpod_health_disabled(self):
        resp = client.get("/runpod/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["enabled"] is False

    def test_runpod_scale_disabled(self):
        resp = client.post("/runpod/scale", json={
            "min_workers": 1,
            "max_workers": 2,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data


class TestMetricsAndAlerts:
    def test_metrics_returns_baselines(self):
        resp = client.get("/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "baselines" in data

    def test_alerts_returns_alerts(self):
        resp = client.get("/alerts")
        assert resp.status_code == 200
        data = resp.json()
        assert "alerts" in data


class TestPromptAssembly:
    def test_assemble_prompts_default(self):
        resp = client.post("/prompts/assemble", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert "success" in data
        assert "stdout" in data
