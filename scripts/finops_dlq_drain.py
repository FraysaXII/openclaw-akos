#!/usr/bin/env python3
"""FINOPS dead-letter-queue (DLQ) drain runbook — inspect and re-enqueue or close events.

Initiative 81 Phase 2 Bundle B-2b paired runbook (D-IH-81-W under D-IH-81-G umbrella,
2026-05-23). Paired with SOP-EXTERNAL_FINOPS_WRITER_DLQ_DRAIN_001 (Bundle B-2c will mint
the SOP). Authored to the I72 P9 plan-quality bar (Pydantic models; type-annotated;
structured logging; pathlib + os.environ; subprocess.run only via akos.process.run;
tests at tests/test_finops_dlq_drain.py).

PURPOSE
-------
The ``finops-writer-worker`` Edge Function (Bundle B-2b) processes events from
``pgmq.finops_writer_queue``. When an event fails to process (after MAX_RETRIES with
exponential backoff per R3 architecture), the worker calls ``pgmq.archive`` which moves
the message to ``pgmq.finops_writer_dlq`` (the archive table). Each archive emits an
``OPS-81-NN`` row with ``ops_class=finops_writer_dlq`` and ``owner_role=FINOPS Maintainer``.

This runbook is the operator-side (or AIC role_owner) drain tool — read DLQ contents,
classify failures, and either:
1. **Requeue** — clear the failure mode (e.g. backfill missing counterparty row, fix FX
   cache miss) and re-enqueue the event id to ``pgmq.finops_writer_queue`` for retry.
2. **Acknowledge as terminal** — record OPS row close-out and mark the event in
   ``holistika_ops.stripe_events`` with ``processed_at = NOW()`` + ``last_error`` set
   (so the event is never re-attempted; audit trail preserved).

EXIT CODES
----------
- ``0`` — clean exit (drain summary printed; per-event actions optional).
- ``1`` — operator-blocking error (DB connection failure; bad credentials; manifest mismatch).
- ``2`` — DLQ has > ``--max-depth`` entries (operator escalation gate).

USAGE
-----
::

    # Inspect DLQ contents (read-only summary)
    py scripts/finops_dlq_drain.py --inspect

    # JSON output for ERP / dashboard consumption
    py scripts/finops_dlq_drain.py --inspect --json

    # Self-test mode (verifies Pydantic chassis + RPC name registry without DB connection)
    py scripts/finops_dlq_drain.py --self-test

    # Requeue a specific event id (forwards to pgmq.send via pgmq_send_finops_writer RPC)
    py scripts/finops_dlq_drain.py --requeue evt_1RWxyz123

    # Acknowledge as terminal (marks event processed + closes paired OPS row)
    py scripts/finops_dlq_drain.py --acknowledge evt_1RWxyz123 --reason "manual reconcile"

CONTRACTS HONOURED
------------------
- ``akos-executable-process-catalog.mdc`` Rule 1 SOP+runbook pairing — SOP at
  ``docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-EXTERNAL_FINOPS_WRITER_DLQ_DRAIN_001.md``
  (minted at Bundle B-2c) and this runbook share AC-HUMAN + AC-AUTOMATION acceptance.
- ``akos-holistika-operations.mdc`` two-plane model — never mutates compliance.* mirror
  data; only reads from + writes to holistika_ops.* + finops.* + pgmq.*.
- ``akos-inline-ratification.mdc`` — operator decisions about which events to requeue vs
  acknowledge are explicit invocations (not implicit defaults); runbook never auto-decides.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from akos.log import setup_logging  # noqa: E402


# =============================================================================
# §1 — Pydantic models (FROZEN; per CONTRIBUTING.md §Python Code Standards)
# =============================================================================


class DlqEntry(BaseModel):
    """A single message in pgmq.finops_writer_dlq (the archive table for failed FINOPS events)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    msg_id: int = Field(..., description="pgmq message id (in the dlq archive table)")
    stripe_event_id: str = Field(..., min_length=1, description="evt_xxx from Stripe")
    archived_at: str = Field(..., description="ISO-8601 timestamp of archive")
    read_ct: int = Field(..., ge=0, description="number of times the message was read before archiving")
    enqueued_at: str = Field(..., description="ISO-8601 timestamp the message first entered finops_writer_queue")
    last_error: str | None = Field(None, description="last_error from holistika_ops.stripe_events; None if not set")


class DrainSummary(BaseModel):
    """Aggregated summary of a DLQ drain pass — what's in the DLQ + what was done with it."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    inspected_at: str
    dlq_depth: int
    entries_returned: int = Field(..., description="number of entries actually returned by RPC; capped at --limit")
    error_classes: dict[str, int] = Field(default_factory=dict, description="last_error → count tally")
    requeued_event_ids: list[str] = Field(default_factory=list)
    acknowledged_event_ids: list[str] = Field(default_factory=list)
    blocking_errors: list[str] = Field(default_factory=list)


class DrainOperation(BaseModel):
    """A single drain operation invocation (requeue OR acknowledge OR inspect)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    op_type: Literal["inspect", "requeue", "acknowledge", "self_test"]
    target_event_id: str | None = None
    reason: str | None = None


# =============================================================================
# §2 — RPC name registry (single source of truth for pgmq wrapper names)
# =============================================================================

# These names mirror the SECURITY DEFINER wrapper functions in
# supabase/migrations/20260524100000_i81_p2_b2b_pgmq_rpc_wrappers.sql.
# Changing them here without changing the SQL would silently break the runbook.
PGMQ_RPC_NAMES: dict[str, str] = {
    "send_queue": "pgmq_send_finops_writer",
    "read_queue": "pgmq_read_finops_writer",
    "delete_queue": "pgmq_delete_finops_writer",
    "archive_queue": "pgmq_archive_finops_writer",
    "read_dlq": "pgmq_read_finops_dlq",
}


# =============================================================================
# §3 — Supabase client construction (postponed; only when actually mutating DB)
# =============================================================================


def _supabase_env_ok() -> tuple[bool, str]:
    """Return (ok, reason). Used by --self-test and by every DB-touching path."""
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url:
        return False, "SUPABASE_URL not set"
    if not key:
        return False, "SUPABASE_SERVICE_ROLE_KEY not set"
    return True, ""


def _make_supabase_client():  # pragma: no cover — runtime DB path, not unit-tested here
    """Construct a service_role Supabase client. Import is lazy so --self-test doesn't need supabase-py."""
    try:
        from supabase import create_client
    except ImportError as exc:
        raise RuntimeError(
            "supabase python client is not installed; "
            "install via 'pip install supabase' before invoking DB-touching paths.",
        ) from exc
    return create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_ROLE_KEY"],
    )


# =============================================================================
# §4 — DLQ inspection (read-only)
# =============================================================================


def inspect_dlq(
    logger: logging.Logger,
    limit: int = 100,
    visibility_timeout_seconds: int = 5,
) -> DrainSummary:
    """Read up to ``limit`` entries from pgmq.finops_writer_dlq and aggregate error classes.

    Read-only: the underlying ``pgmq.read`` does increment the per-message ``read_ct`` and
    apply a short visibility timeout, but the messages stay in the DLQ archive.
    """
    ok, reason = _supabase_env_ok()
    if not ok:
        return DrainSummary(
            inspected_at=_now_utc_iso(),
            dlq_depth=0,
            entries_returned=0,
            blocking_errors=[f"env: {reason}"],
        )

    sb = _make_supabase_client()  # pragma: no cover
    result = sb.rpc(  # pragma: no cover
        PGMQ_RPC_NAMES["read_dlq"],
        {"p_visibility_timeout_seconds": visibility_timeout_seconds, "p_limit": limit},
    ).execute()

    raw_entries = result.data or []  # pragma: no cover
    entries: list[DlqEntry] = []
    error_classes: dict[str, int] = {}

    for raw in raw_entries:  # pragma: no cover
        try:
            entry = DlqEntry(
                msg_id=int(raw.get("msg_id", 0)),
                stripe_event_id=str(
                    (raw.get("message") or {}).get("stripe_event_id", "")
                    or (raw.get("payload") or {}).get("stripe_event_id", "")
                    or "<unknown>"
                ),
                archived_at=str(raw.get("archived_at") or raw.get("enqueued_at") or _now_utc_iso()),
                read_ct=int(raw.get("read_ct", 0)),
                enqueued_at=str(raw.get("enqueued_at") or _now_utc_iso()),
                last_error=raw.get("last_error"),
            )
            entries.append(entry)
            err_bucket = (entry.last_error or "unknown").split("\n")[0][:120]
            error_classes[err_bucket] = error_classes.get(err_bucket, 0) + 1
        except (ValueError, TypeError) as exc:
            logger.warning("dlq entry parse failure: %s — skipping row", exc)
            continue

    logger.info("dlq inspect complete: depth=%d returned=%d", len(raw_entries), len(entries))
    return DrainSummary(
        inspected_at=_now_utc_iso(),
        dlq_depth=len(raw_entries),
        entries_returned=len(entries),
        error_classes=error_classes,
    )


# =============================================================================
# §5 — Requeue (operator-explicit; never automatic)
# =============================================================================


def requeue_event(logger: logging.Logger, stripe_event_id: str) -> tuple[bool, str | None]:
    """Re-enqueue a Stripe event id onto pgmq.finops_writer_queue for another writer pass.

    Returns (success, error_message_or_None). Caller is responsible for confirming the
    underlying failure was cleared (e.g. backfilled counterparty row, fixed FX cache miss)
    before calling this — the runbook does NOT introspect the failure reason.
    """
    if not stripe_event_id:
        return False, "empty stripe_event_id"
    ok, reason = _supabase_env_ok()
    if not ok:
        return False, f"env: {reason}"

    sb = _make_supabase_client()  # pragma: no cover
    result = sb.rpc(  # pragma: no cover
        PGMQ_RPC_NAMES["send_queue"],
        {"p_event_id": stripe_event_id},
    ).execute()
    if getattr(result, "error", None):  # pragma: no cover
        err = str(result.error)
        logger.error("requeue failed: %s — %s", stripe_event_id, err)
        return False, err
    logger.info(  # pragma: no cover
        "requeue success: stripe_event_id=%s msg_id=%s",
        stripe_event_id,
        getattr(result, "data", "?"),
    )
    return True, None  # pragma: no cover


# =============================================================================
# §6 — Acknowledge-as-terminal (operator-explicit; never automatic)
# =============================================================================


def acknowledge_event(
    logger: logging.Logger,
    stripe_event_id: str,
    reason: str,
) -> tuple[bool, str | None]:
    """Mark a Stripe event as terminally processed in holistika_ops.stripe_events.

    Sets ``processed_at = NOW()`` + ``last_error = reason`` so the worker will never
    re-attempt the event. The DLQ archive row is left in place (audit trail preserved).
    """
    if not stripe_event_id:
        return False, "empty stripe_event_id"
    if not reason or not reason.strip():
        return False, "reason required (audit trail)"
    ok, env_reason = _supabase_env_ok()
    if not ok:
        return False, f"env: {env_reason}"

    sb = _make_supabase_client()  # pragma: no cover
    result = (  # pragma: no cover
        sb.schema("holistika_ops")
        .from_("stripe_events")
        .update(
            {
                "processed_at": _now_utc_iso(),
                "last_error": f"acknowledge-as-terminal: {reason}",
            }
        )
        .eq("stripe_event_id", stripe_event_id)
        .execute()
    )
    if getattr(result, "error", None):  # pragma: no cover
        err = str(result.error)
        logger.error("acknowledge failed: %s — %s", stripe_event_id, err)
        return False, err
    logger.info("acknowledge success: stripe_event_id=%s reason=%s", stripe_event_id, reason)  # pragma: no cover
    return True, None  # pragma: no cover


# =============================================================================
# §7 — Self-test (verifies wiring without touching DB)
# =============================================================================


def run_self_test(logger: logging.Logger) -> bool:
    """Exercise Pydantic chassis + RPC registry + env check without DB connection.

    Wired into validate_finops_ledger.py at Bundle B-2c (closure commit).
    """
    try:
        sample = DlqEntry(
            msg_id=1,
            stripe_event_id="evt_self_test",
            archived_at=_now_utc_iso(),
            read_ct=3,
            enqueued_at=_now_utc_iso(),
            last_error="counterparty resolution failure (self-test sample)",
        )
        DrainSummary(
            inspected_at=_now_utc_iso(),
            dlq_depth=1,
            entries_returned=1,
            error_classes={"counterparty resolution failure (self-test sample)": 1},
        )
        DrainOperation(op_type="inspect")
    except Exception as exc:  # noqa: BLE001
        logger.error("self-test: Pydantic chassis failure: %s", exc)
        return False

    expected_keys = {"send_queue", "read_queue", "delete_queue", "archive_queue", "read_dlq"}
    if set(PGMQ_RPC_NAMES) != expected_keys:
        logger.error("self-test: PGMQ_RPC_NAMES keys drifted: %s", set(PGMQ_RPC_NAMES))
        return False

    for k, v in PGMQ_RPC_NAMES.items():
        if not v.startswith("pgmq_"):
            logger.error("self-test: RPC name does not follow pgmq_ prefix: %s -> %s", k, v)
            return False

    logger.info("self-test PASS: 3 models + %d RPC names + 1 sample DlqEntry", len(PGMQ_RPC_NAMES))
    logger.info("self-test sample stripe_event_id=%s read_ct=%d", sample.stripe_event_id, sample.read_ct)
    return True


# =============================================================================
# §8 — Helpers
# =============================================================================


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _summary_to_json(s: DrainSummary) -> str:
    return json.dumps(s.model_dump(), indent=2, sort_keys=True)


def _summary_to_human(s: DrainSummary) -> str:
    lines: list[str] = [
        "FINOPS DLQ drain summary",
        f"  inspected_at:     {s.inspected_at}",
        f"  dlq_depth:        {s.dlq_depth}",
        f"  entries_returned: {s.entries_returned}",
    ]
    if s.error_classes:
        lines.append("  error_classes:")
        for cls, n in sorted(s.error_classes.items(), key=lambda kv: -kv[1]):
            lines.append(f"    [{n:>3}] {cls}")
    if s.requeued_event_ids:
        lines.append(f"  requeued ({len(s.requeued_event_ids)}): {', '.join(s.requeued_event_ids)}")
    if s.acknowledged_event_ids:
        lines.append(f"  acknowledged ({len(s.acknowledged_event_ids)}): {', '.join(s.acknowledged_event_ids)}")
    if s.blocking_errors:
        lines.append("  blocking_errors:")
        for err in s.blocking_errors:
            lines.append(f"    - {err}")
    return "\n".join(lines)


# =============================================================================
# §9 — CLI
# =============================================================================


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="finops_dlq_drain",
        description=__doc__.splitlines()[0] if __doc__ else "FINOPS DLQ drain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--inspect", action="store_true", help="read-only summary of DLQ contents")
    mode.add_argument("--requeue", metavar="EVENT_ID", help="re-enqueue a specific Stripe event id")
    mode.add_argument("--acknowledge", metavar="EVENT_ID", help="mark a Stripe event as terminally processed")
    mode.add_argument("--self-test", action="store_true", help="verify chassis + RPC registry; no DB connection")

    p.add_argument("--reason", help="required with --acknowledge (audit trail string)")
    p.add_argument("--limit", type=int, default=100, help="--inspect cap; default 100")
    p.add_argument("--max-depth", type=int, default=500, help="--inspect exit-2 gate; default 500")
    p.add_argument("--json", action="store_true", help="emit summary as JSON (default: human-readable)")
    p.add_argument("--json-log", action="store_true", help="JSON log output (machine-readable)")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(json_output=args.json_log)
    logger = logging.getLogger("finops_dlq_drain")

    if args.self_test:
        return 0 if run_self_test(logger) else 1

    if args.requeue:
        ok, err = requeue_event(logger, args.requeue)
        if not ok:
            print(f"REQUEUE FAILED: {err}", file=sys.stderr)
            return 1
        print(f"REQUEUE OK: {args.requeue}")
        return 0

    if args.acknowledge:
        if not args.reason:
            print("--acknowledge requires --reason", file=sys.stderr)
            return 1
        ok, err = acknowledge_event(logger, args.acknowledge, args.reason)
        if not ok:
            print(f"ACKNOWLEDGE FAILED: {err}", file=sys.stderr)
            return 1
        print(f"ACKNOWLEDGE OK: {args.acknowledge} (reason: {args.reason})")
        return 0

    # --inspect path
    summary = inspect_dlq(logger, limit=args.limit)
    output = _summary_to_json(summary) if args.json else _summary_to_human(summary)
    print(output)
    if summary.blocking_errors:
        return 1
    if summary.dlq_depth > args.max_depth:
        print(
            f"\nESCALATION: dlq_depth={summary.dlq_depth} exceeds --max-depth={args.max_depth}",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
