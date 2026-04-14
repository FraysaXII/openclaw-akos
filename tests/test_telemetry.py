"""Tests for akos/telemetry.py LangfuseReporter (SDK v4 API)."""

import os
from unittest.mock import MagicMock, patch

import pytest

from akos.models import LangfuseTraceContext
from akos.telemetry import LangfuseReporter, _coerce_metadata


class TestNormalizeEnv:
    def test_normal_env(self):
        assert LangfuseReporter._normalize_env("dev-local") == "dev-local"

    def test_uppercase_converted(self):
        assert LangfuseReporter._normalize_env("GPU-RunPod") == "gpu-runpod"

    def test_dots_replaced(self):
        assert LangfuseReporter._normalize_env("prod.cloud.v2") == "prod-cloud-v2"

    def test_spaces_replaced(self):
        assert LangfuseReporter._normalize_env("my env") == "my-env"

    def test_empty_returns_default(self):
        assert LangfuseReporter._normalize_env("") == "dev-local"

    def test_starts_with_langfuse_returns_default(self):
        assert LangfuseReporter._normalize_env("langfuse-test") == "dev-local"

    def test_truncated_at_40_chars(self):
        long_env = "a" * 50
        assert len(LangfuseReporter._normalize_env(long_env)) == 40


def _make_mock_client():
    """Build a MagicMock that behaves like a Langfuse v4 client."""
    mock_client = MagicMock()
    mock_span = MagicMock()
    mock_ctx = MagicMock()
    mock_ctx.__enter__ = MagicMock(return_value=mock_span)
    mock_ctx.__exit__ = MagicMock(return_value=False)
    mock_client.start_as_current_observation.return_value = mock_ctx
    return mock_client, mock_span


class TestReporterInit:
    def test_disabled_without_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            reporter = LangfuseReporter()
            assert not reporter.enabled

    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_enabled_with_credentials(self, mock_langfuse_cls):
        mock_langfuse_cls.return_value = MagicMock()
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter(environment="test-env")
            assert reporter.enabled
            mock_langfuse_cls.assert_called_once()

    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse", side_effect=Exception("init fail"))
    def test_graceful_on_init_failure(self, mock_langfuse_cls):
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            assert not reporter.enabled


class TestAuthCheck:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_auth_check_returns_true(self, mock_langfuse_cls):
        mock_client, _ = _make_mock_client()
        mock_client.auth_check.return_value = True
        mock_langfuse_cls.return_value = mock_client
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            assert reporter.auth_check() is True
        mock_client.auth_check.assert_called_once()

    def test_auth_check_disabled(self):
        with patch.dict(os.environ, {}, clear=True):
            reporter = LangfuseReporter()
            assert reporter.auth_check() is False


class TestTraceRequest:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_request_uses_v4_observation(self, mock_langfuse_cls, mock_propagate):
        mock_client, mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter(environment="test")
            reporter.trace_request({
                "agent_role": "executor",
                "tool_name": "write_file",
                "outcome": "success",
            })

        mock_client.start_as_current_observation.assert_called_once()
        call_kwargs = mock_client.start_as_current_observation.call_args[1]
        assert call_kwargs["name"] == "akos-executor"
        assert call_kwargs["output"] == "success"


class TestTraceStartupCompliance:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_startup_pass(self, mock_langfuse_cls, mock_propagate):
        mock_client, mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.trace_startup_compliance("orchestrator", ["f1"], [], True)

        mock_span.score.assert_called_once_with(name="startup_compliance", value=1.0)

    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_startup_fail(self, mock_langfuse_cls, mock_propagate):
        mock_client, mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.trace_startup_compliance("unknown", [], ["SOUL.md"], False)

        mock_span.score.assert_called_once_with(name="startup_compliance", value=0.0)


class TestTraceAlert:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_alert_critical(self, mock_langfuse_cls, mock_propagate):
        mock_client, mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.trace_alert("soc_chmod", "critical", "chmod detected")

        call_kwargs = mock_client.start_as_current_observation.call_args[1]
        assert call_kwargs["name"] == "akos-alert-critical"
        mock_span.score.assert_called_once_with(name="soc_alert", value=1.0)


class TestTraceMetric:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_metric_sends_observation(self, mock_langfuse_cls, mock_propagate):
        mock_client, mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter(environment="dev-local")
            reporter.trace_metric("agent_latency_avg_ms", 150.0, {"sample_count": 10})

        call_kwargs = mock_client.start_as_current_observation.call_args[1]
        assert call_kwargs["name"] == "akos-metric-agent_latency_avg_ms"


class TestTraceAnswerQuality:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_answer_quality_sends_scores(self, mock_langfuse_cls, mock_propagate):
        mock_client, mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter(environment="dev-local")
            reporter.trace_answer_quality({
                "agent_role": "madeira",
                "session_id": "session-1",
                "route_kind": "hlk_direct_lookup",
                "user_text": "Who is the CTO?",
                "assistant_text": "The CTO role exists.",
                "tool_calls": ["hlk_role"],
                "tool_backed": True,
                "citation_asset": "baseline_organisation.csv",
                "best_match_present": True,
                "escalation_present": False,
                "compaction_interference": False,
                "residual_flags": [],
                "quality_score": 1.0,
                "provider": "ollama",
                "model": "qwen3:8b",
            })

        call_kwargs = mock_client.start_as_current_observation.call_args[1]
        assert call_kwargs["name"] == "akos-answer-quality-madeira"
        mock_span.score.assert_any_call(name="answer_quality", value=1.0)
        mock_span.score.assert_any_call(name="citation_present", value=1.0)
        meta = mock_client.start_as_current_observation.call_args[1].get("metadata") or {}
        assert meta.get("hlk_surface") == "log_watcher"
        assert meta.get("eu_aia_req") == "EU-AIA-1"
        assert meta.get("compliance_family") == "hlk_csv"


class TestCoerceMetadata:
    def test_normalizes_keys_and_truncates_values(self):
        out = _coerce_metadata({"EU AIA Req": "EU-AIA-1", "long": "x" * 300})
        assert "eu_aia_req" in out
        assert out["eu_aia_req"] == "EU-AIA-1"
        assert len(out["long"]) == 200


class TestTraceContextMerge:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.propagate_attributes")
    @patch("akos.telemetry.Langfuse")
    def test_trace_request_merges_trace_context(self, mock_langfuse_cls, mock_propagate):
        mock_client, _mock_span = _make_mock_client()
        mock_langfuse_cls.return_value = mock_client
        mock_propagate.return_value.__enter__ = MagicMock()
        mock_propagate.return_value.__exit__ = MagicMock(return_value=False)

        ctx = LangfuseTraceContext(
            eu_aia_req="EU-AIA-1",
            hlk_surface="rest_api",
            hlk_tool="hlk_search",
            compliance_family="hlk_csv",
        )
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter(environment="test")
            reporter.trace_request(
                {"agent_role": "madeira", "tool_name": "hlk_role", "outcome": "ok"},
                trace_context=ctx,
            )

        kw = mock_propagate.call_args[1]
        assert kw["metadata"]["hlk_surface"] == "rest_api"
        assert kw["metadata"]["eu_aia_req"] == "EU-AIA-1"


class TestSampling:
    def test_sample_rate_zero_skips_client(self):
        with patch("akos.telemetry.Langfuse") as mock_langfuse_cls:
            mock_langfuse_cls.return_value = MagicMock()
            with patch("akos.telemetry._langfuse_available", True):
                with patch("akos.telemetry.random.random", return_value=1.0):
                    with patch.dict(os.environ, {
                        "LANGFUSE_PUBLIC_KEY": "pk-test",
                        "LANGFUSE_SECRET_KEY": "sk-test",
                        "LANGFUSE_TRACE_SAMPLE_RATE": "0",
                    }):
                        reporter = LangfuseReporter()
                        reporter.trace_request({"agent_role": "x", "tool_name": "y", "outcome": "z"})
        mock_langfuse_cls.return_value.start_as_current_observation.assert_not_called()


class TestFlush:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_flush_calls_client(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_langfuse_cls.return_value = mock_client

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.flush()

        mock_client.flush.assert_called_once()

    def test_flush_noop_when_disabled(self):
        with patch.dict(os.environ, {}, clear=True):
            reporter = LangfuseReporter()
            reporter.flush()


class TestShutdown:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_shutdown_calls_client(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_langfuse_cls.return_value = mock_client

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.shutdown()

        mock_client.shutdown.assert_called_once()
        assert not reporter.enabled

    def test_shutdown_noop_when_disabled(self):
        with patch.dict(os.environ, {}, clear=True):
            reporter = LangfuseReporter()
            reporter.shutdown()
