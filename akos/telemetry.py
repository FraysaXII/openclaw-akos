"""Langfuse telemetry integration for AKOS.

Wraps the Langfuse client to push agent request/response traces.
Graceful no-op when LANGFUSE_PUBLIC_KEY is not set (dev-local without Langfuse).
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger("akos.telemetry")

_langfuse_available = False
try:
    from langfuse import Langfuse
    _langfuse_available = True
except Exception:  # ImportError, pydantic.v1 ConfigError on Python 3.14+, etc.
    pass


class LangfuseReporter:
    """Lightweight wrapper around Langfuse for AKOS observability.

    Creates traces for each agent request/response pair parsed from
    OpenCLAW gateway logs. Environment tagging separates dev-local,
    gpu-runpod, and prod-cloud traces in Langfuse dashboards.
    """

    def __init__(self, *, environment: str = "dev-local") -> None:
        self._client = None
        self._environment = self._normalize_env(environment)
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
        host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

        if not public_key or not secret_key:
            logger.info("Langfuse credentials not set; telemetry disabled (no-op mode)")
            return

        if not _langfuse_available:
            logger.warning("langfuse package not installed; telemetry disabled")
            return

        try:
            self._client = Langfuse(
                public_key=public_key,
                secret_key=secret_key,
                host=host,
                environment=self._environment,
            )
            logger.info("Langfuse reporter initialized (host=%s, environment=%s)", host, self._environment)
        except Exception as exc:  # broad: Langfuse is optional; graceful no-op on init failure
            logger.warning("Failed to initialize Langfuse client: %s", exc)
            self._client = None

    @staticmethod
    def _normalize_env(env: str) -> str:
        """Langfuse env must match ^(?!langfuse)[a-z0-9-_]+$, max 40 chars."""
        sanitized = str(env).lower().replace(" ", "-").replace(".", "-")[:40]
        return sanitized if sanitized and not sanitized.startswith("langfuse") else "dev-local"

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def trace_request(self, entry: dict) -> None:
        """Push a single agent log entry as a Langfuse trace.

        Expected entry keys (from OpenCLAW gateway log):
          - agent_role: str (e.g. "architect", "executor")
          - tool_name: str | None
          - outcome: str
          - timestamp: str (ISO 8601)
        """
        if not self._client:
            return

        try:
            trace = self._client.trace(
                name=f"akos-{entry.get('agent_role', 'unknown')}",
                metadata={
                    "environment": self._environment,
                    "tool_name": entry.get("tool_name"),
                    "agent_role": entry.get("agent_role"),
                },
            )
            trace.generation(
                name=entry.get("tool_name", "agent-response"),
                input=entry.get("input", ""),
                output=entry.get("outcome", ""),
            )
        except Exception as exc:  # broad: Langfuse is optional; never crash the watcher
            logger.debug("Failed to push trace: %s", exc)

    def trace_startup_compliance(
        self,
        agent_role: str,
        files_read: list[str],
        files_missing: list[str],
        audit_passed: bool,
    ) -> None:
        """Trace a startup compliance event for eval dashboards."""
        if not self._client:
            return
        try:
            trace = self._client.trace(
                name=f"akos-startup-{agent_role}",
                metadata={
                    "environment": self._environment,
                    "agent_role": agent_role,
                    "files_read": files_read,
                    "files_missing": files_missing,
                    "audit_passed": audit_passed,
                },
            )
            trace.score(name="startup_compliance", value=1.0 if audit_passed else 0.0)
        except Exception as exc:
            logger.debug("Failed to push startup trace: %s", exc)

    def trace_alert(self, alert_id: str, severity: str, description: str) -> None:
        """Trace a SOC alert event with a severity score."""
        if not self._client:
            return
        try:
            trace = self._client.trace(
                name=f"akos-alert-{severity}",
                metadata={
                    "environment": self._environment,
                    "alert_id": alert_id,
                    "severity": severity,
                    "description": description,
                },
            )
            severity_scores = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
            trace.score(name="soc_alert", value=severity_scores.get(severity, 0.5))
        except Exception as exc:
            logger.debug("Failed to push alert trace: %s", exc)

    def trace_metric(self, metric_name: str, value: float, metadata: dict | None = None) -> None:
        """Push a DX metric as a Langfuse trace for dashboard consumption."""
        if not self._client:
            return
        try:
            self._client.trace(
                name=f"akos-metric-{metric_name}",
                metadata={
                    "environment": self._environment,
                    "metric_name": metric_name,
                    "metric_value": value,
                    **(metadata or {}),
                },
            )
        except Exception as exc:
            logger.debug("Failed to push metric: %s", exc)

    def trace_answer_quality(self, record: dict) -> None:
        """Trace a user-visible answer-quality event for flagship agent review."""
        if not self._client:
            return
        try:
            agent_role = str(record.get("agent_role", "unknown"))
            session_id = str(record.get("session_id", "")) or None
            route_kind = str(record.get("route_kind", "unknown"))
            quality_score = float(record.get("quality_score", 0.0))
            metadata = {
                "environment": self._environment,
                "agent_role": agent_role,
                "route_kind": route_kind,
                "tool_calls": record.get("tool_calls", []),
                "tool_backed": record.get("tool_backed", False),
                "citation_asset": record.get("citation_asset", ""),
                "best_match_present": record.get("best_match_present", False),
                "escalation_present": record.get("escalation_present", False),
                "compaction_interference": record.get("compaction_interference", False),
                "residual_flags": record.get("residual_flags", []),
                "provider": record.get("provider", ""),
                "model": record.get("model", ""),
                "local_mirror_path": record.get("local_mirror_path", ""),
            }
            trace = self._client.trace(
                name=f"akos-answer-quality-{agent_role}",
                session_id=session_id,
                metadata=metadata,
                tags=[agent_role, route_kind, "answer-quality"],
                input=record.get("user_text", ""),
                output=record.get("assistant_text", ""),
            )
            trace.score(name="answer_quality", value=quality_score)
            trace.score(name="citation_present", value=1.0 if record.get("citation_asset") else 0.0)
            trace.score(name="escalation_correct", value=1.0 if record.get("escalation_present") else 0.0)
            trace.score(
                name="compaction_clean",
                value=0.0 if record.get("compaction_interference") else 1.0,
            )
        except Exception as exc:
            logger.debug("Failed to push answer-quality trace: %s", exc)

    def flush(self) -> None:
        """Flush pending traces to Langfuse."""
        if self._client:
            try:
                self._client.flush()
            except Exception as exc:  # broad: graceful degradation for optional dependency
                logger.debug("Flush failed: %s", exc)
