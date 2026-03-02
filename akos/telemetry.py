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
except ImportError:
    pass


class LangfuseReporter:
    """Lightweight wrapper around Langfuse for AKOS observability.

    Creates traces for each agent request/response pair parsed from
    OpenCLAW gateway logs.
    """

    def __init__(self) -> None:
        self._client = None
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
            )
            logger.info("Langfuse reporter initialized (host=%s)", host)
        except Exception as exc:
            logger.warning("Failed to initialize Langfuse client: %s", exc)
            self._client = None

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
                    "tool_name": entry.get("tool_name"),
                    "agent_role": entry.get("agent_role"),
                },
            )
            trace.generation(
                name=entry.get("tool_name", "agent-response"),
                input=entry.get("input", ""),
                output=entry.get("outcome", ""),
            )
        except Exception as exc:
            logger.debug("Failed to push trace: %s", exc)

    def flush(self) -> None:
        """Flush pending traces to Langfuse."""
        if self._client:
            try:
                self._client.flush()
            except Exception as exc:
                logger.debug("Flush failed: %s", exc)
