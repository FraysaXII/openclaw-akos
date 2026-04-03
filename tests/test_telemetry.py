"""Tests for akos/telemetry.py LangfuseReporter."""

import os
from unittest.mock import MagicMock, patch

import pytest

from akos.telemetry import LangfuseReporter


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
            call_kwargs = mock_langfuse_cls.call_args[1]
            assert call_kwargs["environment"] == "test-env"

    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse", side_effect=Exception("init fail"))
    def test_graceful_on_init_failure(self, mock_langfuse_cls):
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            assert not reporter.enabled


class TestTraceRequest:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_trace_request_sends_trace(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_trace = MagicMock()
        mock_client.trace.return_value = mock_trace
        mock_langfuse_cls.return_value = mock_client

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

        mock_client.trace.assert_called_once()
        call_kwargs = mock_client.trace.call_args[1]
        assert call_kwargs["name"] == "akos-executor"
        assert call_kwargs["metadata"]["environment"] == "test"
        mock_trace.generation.assert_called_once()


class TestTraceStartupCompliance:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_trace_startup_pass(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_trace = MagicMock()
        mock_client.trace.return_value = mock_trace
        mock_langfuse_cls.return_value = mock_client

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.trace_startup_compliance("orchestrator", ["f1"], [], True)

        mock_trace.score.assert_called_once_with(name="startup_compliance", value=1.0)

    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_trace_startup_fail(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_trace = MagicMock()
        mock_client.trace.return_value = mock_trace
        mock_langfuse_cls.return_value = mock_client

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.trace_startup_compliance("unknown", [], ["SOUL.md"], False)

        mock_trace.score.assert_called_once_with(name="startup_compliance", value=0.0)


class TestTraceAlert:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_trace_alert_critical(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_trace = MagicMock()
        mock_client.trace.return_value = mock_trace
        mock_langfuse_cls.return_value = mock_client

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter()
            reporter.trace_alert("soc_chmod", "critical", "chmod detected")

        call_kwargs = mock_client.trace.call_args[1]
        assert call_kwargs["name"] == "akos-alert-critical"
        mock_trace.score.assert_called_once_with(name="soc_alert", value=1.0)


class TestTraceMetric:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_trace_metric_sends_trace(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_langfuse_cls.return_value = mock_client

        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-test",
            "LANGFUSE_SECRET_KEY": "sk-test",
        }):
            reporter = LangfuseReporter(environment="dev-local")
            reporter.trace_metric("agent_latency_avg_ms", 150.0, {"sample_count": 10})

        call_kwargs = mock_client.trace.call_args[1]
        assert call_kwargs["name"] == "akos-metric-agent_latency_avg_ms"
        assert call_kwargs["metadata"]["metric_value"] == 150.0


class TestTraceAnswerQuality:
    @patch("akos.telemetry._langfuse_available", True)
    @patch("akos.telemetry.Langfuse")
    def test_trace_answer_quality_sends_scores(self, mock_langfuse_cls):
        mock_client = MagicMock()
        mock_trace = MagicMock()
        mock_client.trace.return_value = mock_trace
        mock_langfuse_cls.return_value = mock_client

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
                "local_mirror_path": "C:/tmp/mirror.jsonl",
            })

        call_kwargs = mock_client.trace.call_args[1]
        assert call_kwargs["name"] == "akos-answer-quality-madeira"
        assert call_kwargs["session_id"] == "session-1"
        mock_trace.score.assert_any_call(name="answer_quality", value=1.0)
        mock_trace.score.assert_any_call(name="citation_present", value=1.0)


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
