"""Unit tests for akos.alerts.AlertEvaluator.

Feeds synthetic log entries and metrics, asserting correct alerts fire.

Run:
    python -m pytest tests/test_akos_alerts.py -v
"""

import pytest

from conftest import REPO_ROOT

from akos.alerts import AlertEvaluator


ALERTS_PATH = REPO_ROOT / "config" / "eval" / "alerts.json"
BASELINES_PATH = REPO_ROOT / "config" / "eval" / "baselines.json"


class TestAlertEvaluatorInit:
    def test_loads_successfully(self):
        evaluator = AlertEvaluator(ALERTS_PATH, BASELINES_PATH)
        assert len(evaluator.alerts) >= 3
        assert len(evaluator.baselines) == 4
        assert len(evaluator._realtime_alerts) >= 1


class TestRealtimeAlerts:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.evaluator = AlertEvaluator(ALERTS_PATH, BASELINES_PATH)

    def test_chmod_triggers_alert(self):
        entry = {"command": "chmod 777 /var/www", "tool_name": "shell_exec"}
        fired = self.evaluator.check_realtime(entry)
        assert len(fired) >= 1
        assert any(a.severity in ("critical", "high") for a in fired)

    def test_etc_path_triggers_alert(self):
        entry = {"target_path": "/etc/shadow", "tool_name": "read_file"}
        fired = self.evaluator.check_realtime(entry)
        assert len(fired) >= 1

    def test_benign_entry_does_not_trigger(self):
        entry = {"tool_name": "web_search", "command": "search for pandas docs"}
        fired = self.evaluator.check_realtime(entry)
        assert len(fired) == 0

    def test_canvas_eval_triggers_alert(self):
        entry = {"tool_name": "canvas_eval", "command": "eval('malicious')"}
        fired = self.evaluator.check_realtime(entry)
        assert len(fired) >= 1


class TestPeriodicBaselines:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.evaluator = AlertEvaluator(ALERTS_PATH, BASELINES_PATH)

    def test_good_metrics_pass(self):
        metrics = {
            "completion_rate": 0.80,
            "containment_rate": 0.90,
            "pr_throughput_increase": 0.50,
            "prompt_injection_vuln_rate": 0.0,
        }
        violations = self.evaluator.check_periodic(metrics)
        assert len(violations) == 0

    def test_low_completion_rate_violates(self):
        metrics = {"completion_rate": 0.1}
        violations = self.evaluator.check_periodic(metrics)
        ids = {v.metric_id for v in violations}
        assert "completion_rate" in ids

    def test_missing_metrics_do_not_violate(self):
        violations = self.evaluator.check_periodic({})
        assert len(violations) == 0
