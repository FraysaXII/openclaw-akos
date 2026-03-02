"""Alert evaluation engine for AKOS SOC monitoring.

Activates the dormant config/eval/alerts.json and config/eval/baselines.json
as live enforcement, evaluating log entries in real-time and metrics
against baseline thresholds periodically.
"""

from __future__ import annotations

import logging
from pathlib import Path

from akos.models import Alert, Baseline, load_alerts, load_baselines

logger = logging.getLogger("akos.alerts")


class AlertEvaluator:
    """Evaluates log entries and metrics against configured alerts and baselines.

    Usage:
        evaluator = AlertEvaluator(alerts_path, baselines_path)
        fired = evaluator.check_realtime(log_entry)
        violations = evaluator.check_periodic(metrics)
    """

    def __init__(self, alerts_path: Path, baselines_path: Path) -> None:
        self.alerts: list[Alert] = load_alerts(alerts_path)
        self.baselines: list[Baseline] = load_baselines(baselines_path)
        self._realtime_alerts = [a for a in self.alerts if a.evaluation_window == "real-time"]
        logger.info(
            "AlertEvaluator loaded: %d alerts (%d real-time), %d baselines",
            len(self.alerts), len(self._realtime_alerts), len(self.baselines),
        )

    def check_realtime(self, log_entry: dict) -> list[Alert]:
        """Evaluate a single log entry against real-time alerts.

        Returns a list of alerts that were triggered.
        """
        fired: list[Alert] = []
        for alert in self._realtime_alerts:
            if alert.matches_realtime(log_entry):
                fired.append(alert)
                logger.critical(
                    "ALERT FIRED: %s [%s] -- %s",
                    alert.alert_id, alert.severity, alert.description,
                )
        return fired

    def check_periodic(self, metrics: dict[str, float]) -> list[Baseline]:
        """Evaluate aggregated metrics against baseline thresholds.

        Args:
            metrics: dict mapping metric_id -> current value.

        Returns:
            List of baselines that are NOT met (violations).
        """
        violations: list[Baseline] = []
        for baseline in self.baselines:
            value = metrics.get(baseline.metric_id)
            if value is None:
                continue
            if not baseline.passes(value):
                violations.append(baseline)
                logger.warning(
                    "BASELINE VIOLATION: %s = %.3f (target: %s %s)",
                    baseline.metric_id, value, baseline.comparator, baseline.target_value,
                )
        return violations
