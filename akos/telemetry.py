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
import random
import re
from typing import TYPE_CHECKING, get_args

logger = logging.getLogger("akos.telemetry")

if TYPE_CHECKING:
    from akos.models import LangfuseTraceContext

_langfuse_available = False
try:
    from langfuse import Langfuse, propagate_attributes
    _langfuse_available = True
except Exception:
    pass


def _normalize_langfuse_metadata_key(key: str) -> str:
    """Langfuse metrics-friendly keys: alphanumeric + underscore, lowercase, bounded."""
    raw = "".join((c if c.isalnum() else "_") for c in str(key))
    raw = re.sub(r"_+", "_", raw).strip("_").lower()
    return (raw or "key")[:64]


def _coerce_metadata(raw: dict) -> dict[str, str]:
    """Langfuse v4 metadata values must be str, max 200 chars; keys normalized."""
    result: dict[str, str] = {}
    for key, value in raw.items():
        nk = _normalize_langfuse_metadata_key(key)
        s = str(value) if not isinstance(value, str) else value
        result[nk] = s[:200]
    return result


def _parse_trace_context(
    trace_context: LangfuseTraceContext | dict | None,
) -> dict[str, str]:
    if trace_context is None:
        return {}
    from akos.models import LangfuseTraceContext as _LTC

    if isinstance(trace_context, _LTC):
        return trace_context.to_metadata()
    return _LTC.model_validate(trace_context).to_metadata()


class LangfuseReporter:
    """Lightweight wrapper around the Langfuse v4 SDK for AKOS observability."""

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

    @staticmethod
    def _sampled_out() -> bool:
        """Probabilistic drop when LANGFUSE_TRACE_SAMPLE_RATE is < 1 (OPS volume control)."""
        raw = os.environ.get("LANGFUSE_TRACE_SAMPLE_RATE", "1").strip()
        try:
            rate = float(raw)
        except ValueError:
            return False
        rate = max(0.0, min(1.0, rate))
        if rate >= 1.0:
            return False
        return random.random() > rate

    def _merged_metadata(
        self,
        base: dict,
        trace_context: LangfuseTraceContext | dict | None,
    ) -> dict[str, str]:
        merged = {**base, **_parse_trace_context(trace_context)}
        return _coerce_metadata(merged)

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

    def trace_request(
        self,
        entry: dict,
        trace_context: LangfuseTraceContext | dict | None = None,
    ) -> None:
        """Push a single agent log entry as a Langfuse observation."""
        if not self._client or self._sampled_out():
            return
        try:
            agent_role = entry.get("agent_role", "unknown")
            base = {
                "environment": self._environment,
                "tool_name": entry.get("tool_name", ""),
                "agent_role": agent_role,
            }
            meta = self._merged_metadata(base, trace_context)
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
        trace_context: LangfuseTraceContext | dict | None = None,
    ) -> None:
        """Trace a startup compliance event for eval dashboards."""
        if not self._client or self._sampled_out():
            return
        try:
            base = {
                "environment": self._environment,
                "agent_role": agent_role,
                "files_read": ",".join(files_read),
                "files_missing": ",".join(files_missing),
                "audit_passed": str(audit_passed),
            }
            meta = self._merged_metadata(base, trace_context)
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

    def trace_alert(
        self,
        alert_id: str,
        severity: str,
        description: str,
        trace_context: LangfuseTraceContext | dict | None = None,
    ) -> None:
        """Trace a SOC alert event with a severity score."""
        if not self._client or self._sampled_out():
            return
        try:
            base = {
                "environment": self._environment,
                "alert_id": alert_id,
                "severity": severity,
                "description": description,
            }
            meta = self._merged_metadata(base, trace_context)
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

    def trace_metric(
        self,
        metric_name: str,
        value: float,
        metadata: dict | None = None,
        trace_context: LangfuseTraceContext | dict | None = None,
    ) -> None:
        """Push a DX metric as a Langfuse observation for dashboard consumption."""
        if not self._client or self._sampled_out():
            return
        try:
            base = {
                "environment": self._environment,
                "metric_name": metric_name,
                "metric_value": str(value),
                **(metadata or {}),
            }
            meta = self._merged_metadata(base, trace_context)
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

    def trace_answer_quality(
        self,
        record: dict,
        trace_context: LangfuseTraceContext | dict | None = None,
    ) -> None:
        """Trace a user-visible answer-quality event for flagship agent review."""
        if not self._client or self._sampled_out():
            return
        try:
            from akos.models import LangfuseTraceContext as _LTC

            if trace_context is None:
                tools = record.get("tool_calls") or []
                hlk_tool: str | None = None
                for t in tools:
                    ts = str(t)
                    if ts.startswith("hlk_"):
                        hlk_tool = ts[:64]
                        break
                trace_context = _LTC(
                    eu_aia_req="EU-AIA-1",
                    hlk_surface="log_watcher",
                    hlk_tool=hlk_tool,
                    compliance_family="hlk_csv" if hlk_tool else "none",
                )

            agent_role = str(record.get("agent_role", "unknown"))
            session_id = str(record.get("session_id", "")) or None
            route_kind = str(record.get("route_kind", "unknown"))
            quality_score = float(record.get("quality_score", 0.0))
            base = {
                "environment": self._environment,
                "agent_role": agent_role,
                "route_kind": route_kind,
                "madeira_interaction_mode": str(record.get("madeira_interaction_mode", "")),
                "tool_calls": str(record.get("tool_calls", [])),
                "tool_backed": str(record.get("tool_backed", False)),
                "citation_asset": record.get("citation_asset", ""),
                "best_match_present": str(record.get("best_match_present", False)),
                "escalation_present": str(record.get("escalation_present", False)),
                "compaction_interference": str(record.get("compaction_interference", False)),
                "residual_flags": str(record.get("residual_flags", [])),
                "provider": record.get("provider", ""),
                "model": record.get("model", ""),
            }
            meta = self._merged_metadata(base, trace_context)
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

    def trace_eval_outcome(
        self,
        *,
        suite_id: str,
        task_id: str,
        mode: str,
        pass_fail: str,
        trials: int = 1,
        dimension_id: str | None = None,
        research_surface: str | None = None,
        madeira_interaction_mode: str | None = None,
    ) -> None:
        """Record a scored eval task run (Langfuse v4 observation-centric API)."""
        if not self._client or self._sampled_out():
            return
        try:
            from akos.models import LangfuseResearchSurface, LangfuseTraceContext as _LTC

            rs_raw = (research_surface or "none").strip().lower()
            allowed_rs = set(get_args(LangfuseResearchSurface))
            rs_lit: str = rs_raw if rs_raw in allowed_rs else "none"

            ctx = _LTC(
                hlk_surface="none",
                research_surface=rs_lit,  # type: ignore[arg-type]
                eval_suite=suite_id[:64],
                eval_task_id=task_id[:64],
                eval_mode=mode[:32],
                eval_pass_fail=pass_fail[:16],
                eval_trials=str(trials)[:8],
            )
            base_meta = {
                "environment": self._environment,
                "dimension_id": (dimension_id or "")[:64],
            }
            mim = (madeira_interaction_mode or "").strip()
            if mim:
                base_meta["madeira_interaction_mode"] = mim[:32]
            meta = self._merged_metadata(base_meta, ctx)
            with propagate_attributes(
                metadata=meta,
                tags=["akos-eval", suite_id],
                trace_name=f"akos-eval-{suite_id}",
            ):
                with self._client.start_as_current_observation(
                    name=f"eval-{task_id}",
                    as_type="span",
                    metadata=meta,
                ) as span:
                    span.score(name="eval_pass", value=1.0 if pass_fail.upper() == "PASS" else 0.0)
        except Exception as exc:
            logger.debug("Failed to push eval trace: %s", exc)

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
