"""Tests for scripts/finops_dlq_drain.py operator runbook.

Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).

Covers:
- Pydantic chassis: DlqEntry + DrainSummary + DrainOperation construction + frozen-ness.
- PGMQ_RPC_NAMES single-source-of-truth registry matches the SQL migration wrappers.
- Self-test path runs cleanly without DB / Supabase connection.
- inspect_dlq + requeue_event + acknowledge_event short-circuit cleanly when
  SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY env vars are not set (no DB attempt).
- CLI smoke: --self-test exits 0; --acknowledge without --reason exits 1.

These tests run under the default `py scripts/test.py all` collection via the implicit
`tests/test_*.py` glob.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import finops_dlq_drain  # noqa: E402
from finops_dlq_drain import (  # noqa: E402
    PGMQ_RPC_NAMES,
    DlqEntry,
    DrainOperation,
    DrainSummary,
    acknowledge_event,
    inspect_dlq,
    requeue_event,
    run_self_test,
)


# -----------------------------------------------------------------------------
# Pydantic chassis
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestPydanticChassis:
    def test_dlq_entry_valid(self) -> None:
        entry = DlqEntry(
            msg_id=42,
            stripe_event_id="evt_test_123",
            archived_at="2026-05-23T15:30:00+00:00",
            read_ct=3,
            enqueued_at="2026-05-23T15:00:00+00:00",
            last_error="counterparty resolution failure",
        )
        assert entry.msg_id == 42
        assert entry.stripe_event_id == "evt_test_123"
        assert entry.read_ct == 3

    def test_dlq_entry_frozen(self) -> None:
        entry = DlqEntry(
            msg_id=1,
            stripe_event_id="evt_x",
            archived_at="2026-05-23T00:00:00+00:00",
            read_ct=0,
            enqueued_at="2026-05-23T00:00:00+00:00",
        )
        with pytest.raises((TypeError, ValueError, ValidationError)):
            entry.msg_id = 99  # type: ignore[misc]

    def test_dlq_entry_rejects_empty_stripe_event_id(self) -> None:
        with pytest.raises(ValidationError):
            DlqEntry(
                msg_id=1,
                stripe_event_id="",
                archived_at="2026-05-23T00:00:00+00:00",
                read_ct=0,
                enqueued_at="2026-05-23T00:00:00+00:00",
            )

    def test_dlq_entry_rejects_negative_read_ct(self) -> None:
        with pytest.raises(ValidationError):
            DlqEntry(
                msg_id=1,
                stripe_event_id="evt_x",
                archived_at="2026-05-23T00:00:00+00:00",
                read_ct=-1,
                enqueued_at="2026-05-23T00:00:00+00:00",
            )

    def test_drain_summary_default_factories(self) -> None:
        s = DrainSummary(
            inspected_at="2026-05-23T00:00:00+00:00",
            dlq_depth=5,
            entries_returned=5,
        )
        assert s.error_classes == {}
        assert s.requeued_event_ids == []
        assert s.blocking_errors == []

    def test_drain_operation_literal_enum(self) -> None:
        DrainOperation(op_type="inspect")
        DrainOperation(op_type="requeue", target_event_id="evt_x")
        DrainOperation(op_type="acknowledge", target_event_id="evt_x", reason="manual")
        DrainOperation(op_type="self_test")
        with pytest.raises(ValidationError):
            DrainOperation(op_type="bogus")  # type: ignore[arg-type]


# -----------------------------------------------------------------------------
# RPC name registry
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestRpcNameRegistry:
    def test_expected_keys_present(self) -> None:
        expected = {"send_queue", "read_queue", "delete_queue", "archive_queue", "read_dlq"}
        assert set(PGMQ_RPC_NAMES) == expected

    def test_all_names_have_pgmq_prefix(self) -> None:
        for key, name in PGMQ_RPC_NAMES.items():
            assert name.startswith("pgmq_"), f"{key} -> {name} missing pgmq_ prefix"

    def test_all_names_reference_finops_writer_or_dlq(self) -> None:
        for key, name in PGMQ_RPC_NAMES.items():
            assert (
                "finops_writer" in name or "finops_dlq" in name
            ), f"{key} -> {name} not in finops_writer / finops_dlq scope"


# -----------------------------------------------------------------------------
# Self-test path (no DB connection)
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestSelfTest:
    def test_self_test_passes(self, caplog: pytest.LogCaptureFixture) -> None:
        import logging

        logger = logging.getLogger("test_finops_dlq_drain.self_test")
        caplog.set_level("INFO")
        assert run_self_test(logger) is True


# -----------------------------------------------------------------------------
# Env-guard short-circuits (no DB connection attempts)
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestEnvShortCircuit:
    def _scrub_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        for var in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
            monkeypatch.delenv(var, raising=False)

    def test_inspect_dlq_returns_blocking_error_without_env(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import logging

        self._scrub_env(monkeypatch)
        logger = logging.getLogger("test_finops_dlq_drain.env_short_circuit")
        summary = inspect_dlq(logger)
        assert summary.dlq_depth == 0
        assert summary.entries_returned == 0
        assert any("env" in e for e in summary.blocking_errors)

    def test_requeue_returns_false_without_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import logging

        self._scrub_env(monkeypatch)
        logger = logging.getLogger("test_finops_dlq_drain.env_short_circuit")
        ok, err = requeue_event(logger, "evt_test_x")
        assert ok is False
        assert err is not None and "env" in err

    def test_acknowledge_returns_false_without_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import logging

        self._scrub_env(monkeypatch)
        logger = logging.getLogger("test_finops_dlq_drain.env_short_circuit")
        ok, err = acknowledge_event(logger, "evt_test_x", "manual")
        assert ok is False
        assert err is not None and "env" in err

    def test_requeue_rejects_empty_event_id(self) -> None:
        import logging

        logger = logging.getLogger("test_finops_dlq_drain.empty_id")
        ok, err = requeue_event(logger, "")
        assert ok is False
        assert err == "empty stripe_event_id"

    def test_acknowledge_rejects_empty_event_id(self) -> None:
        import logging

        logger = logging.getLogger("test_finops_dlq_drain.empty_id")
        ok, err = acknowledge_event(logger, "", "reason")
        assert ok is False
        assert err == "empty stripe_event_id"

    def test_acknowledge_rejects_empty_reason(self) -> None:
        import logging

        logger = logging.getLogger("test_finops_dlq_drain.empty_reason")
        ok, err = acknowledge_event(logger, "evt_x", "  ")
        assert ok is False
        assert err == "reason required (audit trail)"


# -----------------------------------------------------------------------------
# CLI smoke (subprocess)
# -----------------------------------------------------------------------------


class TestCliSmoke:
    def test_self_test_cli_exits_zero(self) -> None:
        env = {**os.environ}
        env.pop("SUPABASE_URL", None)
        env.pop("SUPABASE_SERVICE_ROLE_KEY", None)
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "finops_dlq_drain.py"), "--self-test"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            env=env,
        )
        assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    def test_acknowledge_without_reason_exits_nonzero(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts" / "finops_dlq_drain.py"),
                "--acknowledge",
                "evt_test",
            ],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode != 0
        assert "reason" in (result.stdout + result.stderr).lower()

    def test_no_mode_flag_exits_nonzero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "finops_dlq_drain.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        # argparse exits with code 2 when required mutually-exclusive group missing
        assert result.returncode != 0


# -----------------------------------------------------------------------------
# Helper coverage
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestHelpers:
    def test_now_utc_iso_returns_iso_string(self) -> None:
        s = finops_dlq_drain._now_utc_iso()
        assert "T" in s
        assert s.endswith("+00:00") or s.endswith("Z")

    def test_summary_to_json_roundtrip(self) -> None:
        import json

        s = DrainSummary(
            inspected_at="2026-05-23T00:00:00+00:00",
            dlq_depth=2,
            entries_returned=2,
            error_classes={"fx cache miss": 2},
        )
        text = finops_dlq_drain._summary_to_json(s)
        parsed = json.loads(text)
        assert parsed["dlq_depth"] == 2
        assert parsed["error_classes"]["fx cache miss"] == 2

    def test_summary_to_human_contains_header(self) -> None:
        s = DrainSummary(
            inspected_at="2026-05-23T00:00:00+00:00",
            dlq_depth=0,
            entries_returned=0,
        )
        text = finops_dlq_drain._summary_to_human(s)
        assert "FINOPS DLQ drain summary" in text
        assert "dlq_depth:        0" in text
