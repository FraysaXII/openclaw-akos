"""Langfuse telemetry integration for AKOS (SDK v4).

Wraps the Langfuse v4 client to push agent request/response traces using the
observation-centric API.  Graceful no-op when credentials are absent.

SDK v4 breaking changes addressed here:
  - ``Langfuse.trace()`` removed -> use ``start_as_current_observation()``
  - ``trace.generation()`` removed -> use nested ``start_observation(as_type="generation")``
  - ``trace.score()`` removed -> use ``span.score()``
  - ``environment=`` constructor arg removed -> use ``LANGFUSE_TRACING_ENVIRONMENT`` env var
  - ``shutdown()`` replaces ``flush()`` as the recommended cleanup path
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger("akos.telemetry")

_langfuse_available = False
try:
    from langfuse import Langfuse, propagate_attributes
    _langfuse_available = True
except Exception:
    pass


def _coerce_metadata(raw: dict) -> dict[str, str]:
    """Langfuse v4 metadata values must be str, max 200 chars."""
    result: dict[str, str] = {}
    for key, value in raw.items():
        s = str(value) if not isinstance(value, str) else value
        result[str(key)] = s[:200]
    return result


class LangfuseReporter:
    """Lightweight wrapper around Langfuse v4 for AKOS observability."""

    def __init__(self, *, environment: str = "dev-local") -> None:
        self._client: Langfuse | None = None
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

        os.environ.setdefault("LANGFUSE_TRACING_ENVIRONMENT", self._environment)

        debug = os.environ.get("LANGFUSE_DEBUG", "").lower() in ("1", "true", "yes")

        try:
            self._client = Langfuse(
                public_key=public_key,
                secret_key=secret_key,
                host=host,
                debug=debug,
            )
            logger.info("Langfuse reporter initialized (host=%s, environment=%s)", host, self._environment)
        except Exception as exc:
            logger.warning("Failed to initialize Langfuse client: %s", exc)
            self._client = None

    @staticmethod
    def _normalize_env(env: str) -> str:
        sanitized = str(env).lower().replace(" ", "-").replace(".", "-")[:40]
        return sanitized if sanitized and not sanitized.startswith("langfuse") else "dev-local"

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def auth_check(self) -> bool:
        """Verify credentials reach the correct Langfuse project. Blocking."""
        if not self._client:
            return False
        try:
            return self._client.auth_check()
        except Exception as exc:
            logger.warning("Langfuse auth_check failed: %s", exc)
            return False

    def trace_request(self, entry: dict) -> None:
        """Push a single agent log entry as a Langfuse observation."""
        if not self._client:
            return
        try:
            agent_role = entry.get("agent_role", "unknown")
            meta = _coerce_metadata({
                "environment": self._environment,
                "tool_name": entry.get("tool_name", ""),
                "agent_role": agent_role,
            })
            with propagate_attributes(
                metadata=meta,
                tags=[str(agent_role)],
                trace_name=f"akos-{agent_role}",
            ):
                with self._client.start_as_current_observation(
                    name=f"akos-{agent_role}",
                    as_type="span",
                    input=entry.get("input", ""),
                    output=entry.get("outcome", ""),
                    metadata=meta,
                ) as span:
                    span.update(
                        name=entry.get("tool_name", "agent-response"),
                    )
        except Exception as exc:
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
            meta = _coerce_metadata({
                "environment": self._environment,
                "agent_role": agent_role,
                "files_read": ",".join(files_read),
                "files_missing": ",".join(files_missing),
                "audit_passed": str(audit_passed),
            })
            with propagate_attributes(
                metadata=meta,
                tags=[agent_role, "startup-compliance"],
                trace_name=f"akos-startup-{agent_role}",
            ):
                with self._client.start_as_current_observation(
                    name=f"akos-startup-{agent_role}",
                    as_type="span",
                    metadata=meta,
                ) as span:
                    span.score(name="startup_compliance", value=1.0 if audit_passed else 0.0)
        except Exception as exc:
            logger.debug("Failed to push startup trace: %s", exc)

    def trace_alert(self, alert_id: str, severity: str, description: str) -> None:
        """Trace a SOC alert event with a severity score."""
        if not self._client:
            return
        try:
            meta = _coerce_metadata({
                "environment": self._environment,
                "alert_id": alert_id,
                "severity": severity,
                "description": description,
            })
            severity_scores = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
            with propagate_attributes(
                metadata=meta,
                tags=[severity, "soc-alert"],
                trace_name=f"akos-alert-{severity}",
            ):
                with self._client.start_as_current_observation(
                    name=f"akos-alert-{severity}",
                    as_type="span",
                    metadata=meta,
                ) as span:
                    span.score(name="soc_alert", value=severity_scores.get(severity, 0.5))
        except Exception as exc:
            logger.debug("Failed to push alert trace: %s", exc)

    def trace_metric(self, metric_name: str, value: float, metadata: dict | None = None) -> None:
        """Push a DX metric as a Langfuse observation for dashboard consumption."""
        if not self._client:
            return
        try:
            meta = _coerce_metadata({
                "environment": self._environment,
                "metric_name": metric_name,
                "metric_value": str(value),
                **(metadata or {}),
            })
            with propagate_attributes(
                metadata=meta,
                tags=["dx-metric"],
                trace_name=f"akos-metric-{metric_name}",
            ):
                with self._client.start_as_current_observation(
                    name=f"akos-metric-{metric_name}",
                    as_type="span",
                    metadata=meta,
                ):
                    pass
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
            meta = _coerce_metadata({
                "environment": self._environment,
                "agent_role": agent_role,
                "route_kind": route_kind,
                "tool_calls": str(record.get("tool_calls", [])),
                "tool_backed": str(record.get("tool_backed", False)),
                "citation_asset": record.get("citation_asset", ""),
                "best_match_present": str(record.get("best_match_present", False)),
                "escalation_present": str(record.get("escalation_present", False)),
                "compaction_interference": str(record.get("compaction_interference", False)),
                "residual_flags": str(record.get("residual_flags", [])),
                "provider": record.get("provider", ""),
                "model": record.get("model", ""),
            })
            with propagate_attributes(
                session_id=session_id,
                metadata=meta,
                tags=[agent_role, route_kind, "answer-quality"],
                trace_name=f"akos-answer-quality-{agent_role}",
            ):
                with self._client.start_as_current_observation(
                    name=f"akos-answer-quality-{agent_role}",
                    as_type="span",
                    input=record.get("user_text", ""),
                    output=record.get("assistant_text", ""),
                    metadata=meta,
                ) as span:
                    span.score(name="answer_quality", value=quality_score)
                    span.score(name="citation_present", value=1.0 if record.get("citation_asset") else 0.0)
                    span.score(name="escalation_correct", value=1.0 if record.get("escalation_present") else 0.0)
                    span.score(
                        name="compaction_clean",
                        value=0.0 if record.get("compaction_interference") else 1.0,
                    )
        except Exception as exc:
            logger.debug("Failed to push answer-quality trace: %s", exc)

    def flush(self) -> None:
        """Flush pending traces to Langfuse (use shutdown() for final cleanup)."""
        if self._client:
            try:
                self._client.flush()
            except Exception as exc:
                logger.debug("Flush failed: %s", exc)

    def shutdown(self) -> None:
        """Shut down the Langfuse client, ensuring all buffered data is exported."""
        if self._client:
            try:
                self._client.shutdown()
            except Exception as exc:
                logger.debug("Shutdown failed: %s", exc)
            finally:
                self._client = None
