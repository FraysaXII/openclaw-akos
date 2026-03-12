"""Infrastructure failover router for AKOS.

Tracks consecutive health failures per provider and auto-switches to
fallback models when a provider becomes unhealthy.  Emits SOC alerts
on failover and auto-recovery events.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

logger = logging.getLogger("akos.router")


@dataclass
class ProviderState:
    consecutive_failures: int = 0
    failed_at: float = 0.0
    active: bool = True


class FailoverRouter:
    """Tracks provider health and triggers failover after consecutive failures.

    Args:
        threshold: number of consecutive failures before failover.
        recovery_probe_interval: seconds between re-checks of a failed provider.
    """

    def __init__(
        self,
        *,
        threshold: int = 3,
        recovery_probe_interval: float = 120.0,
    ) -> None:
        self._threshold = threshold
        self._recovery_interval = recovery_probe_interval
        self._providers: dict[str, ProviderState] = {}
        self._failover_active = False
        self._active_provider: str | None = None

    @property
    def failover_active(self) -> bool:
        return self._failover_active

    @property
    def active_provider(self) -> str | None:
        return self._active_provider

    def record_success(self, provider: str) -> None:
        """Record a successful health check for a provider."""
        state = self._providers.setdefault(provider, ProviderState())
        was_failed = state.consecutive_failures >= self._threshold
        state.consecutive_failures = 0
        state.active = True

        if was_failed:
            logger.info("Provider %s recovered; resetting failover", provider)
            self._failover_active = False
            self._active_provider = provider

    def record_failure(self, provider: str) -> list[dict]:
        """Record a failed health check. Returns list of fired alert dicts (may be empty)."""
        state = self._providers.setdefault(provider, ProviderState())
        state.consecutive_failures += 1
        alerts: list[dict] = []

        if state.consecutive_failures >= self._threshold and state.active:
            state.active = False
            state.failed_at = time.monotonic()
            self._failover_active = True
            logger.critical(
                "FAILOVER: provider %s failed %d consecutive health checks; switching to fallback",
                provider, state.consecutive_failures,
            )
            alerts.append({
                "alert_id": "infra_failover_triggered",
                "severity": "critical",
                "provider": provider,
                "consecutive_failures": state.consecutive_failures,
                "description": f"Provider {provider} failed {state.consecutive_failures} consecutive checks",
            })
        return alerts

    def should_probe_recovery(self, provider: str) -> bool:
        """Return True if enough time has passed to re-check a failed provider."""
        state = self._providers.get(provider)
        if state is None or state.active:
            return False
        return (time.monotonic() - state.failed_at) >= self._recovery_interval

    def get_state(self, provider: str) -> ProviderState:
        return self._providers.get(provider, ProviderState())
