"""Tests for akos/router.py FailoverRouter."""

from akos.router import FailoverRouter


class TestFailoverRouter:
    def test_no_failover_under_threshold(self):
        router = FailoverRouter(threshold=3)
        for _ in range(2):
            alerts = router.record_failure("primary")
            assert not alerts
        assert not router.failover_active

    def test_failover_at_threshold(self):
        router = FailoverRouter(threshold=3)
        for _ in range(2):
            router.record_failure("primary")
        alerts = router.record_failure("primary")
        assert len(alerts) == 1
        assert alerts[0]["alert_id"] == "infra_failover_triggered"
        assert alerts[0]["severity"] == "critical"
        assert router.failover_active

    def test_no_duplicate_alert_after_threshold(self):
        router = FailoverRouter(threshold=3)
        for _ in range(3):
            router.record_failure("primary")
        alerts = router.record_failure("primary")
        assert not alerts

    def test_recovery_resets_failover(self):
        router = FailoverRouter(threshold=3)
        for _ in range(3):
            router.record_failure("primary")
        assert router.failover_active
        router.record_success("primary")
        assert not router.failover_active
        state = router.get_state("primary")
        assert state.consecutive_failures == 0
        assert state.active

    def test_success_resets_counter(self):
        router = FailoverRouter(threshold=3)
        router.record_failure("primary")
        router.record_failure("primary")
        router.record_success("primary")
        state = router.get_state("primary")
        assert state.consecutive_failures == 0

    def test_multiple_providers_independent(self):
        router = FailoverRouter(threshold=2)
        router.record_failure("primary")
        router.record_failure("secondary")
        assert not router.failover_active
        router.record_failure("primary")
        assert router.failover_active

    def test_should_probe_recovery_false_when_active(self):
        router = FailoverRouter(threshold=3, recovery_probe_interval=0.0)
        router.record_failure("primary")
        assert not router.should_probe_recovery("primary")

    def test_should_probe_recovery_after_interval(self):
        router = FailoverRouter(threshold=1, recovery_probe_interval=0.0)
        router.record_failure("primary")
        assert router.should_probe_recovery("primary")

    def test_unknown_provider_returns_default_state(self):
        router = FailoverRouter()
        state = router.get_state("nonexistent")
        assert state.consecutive_failures == 0
        assert state.active
