#!/usr/bin/env python3
"""Deterministic OpenClaw gateway repair runbook (I90 gateway tranche / CO-90-004).

Pairs with **SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001** §4.6 (schema drift + cold-start).
This is the **repair** path; escalation to OPS_REGISTER remains
``scripts/openclaw_health_escalate.py``.

AKOS adapts upstream OpenClaw semantics via config normalization and Windows
listener hygiene — it does not fork the gateway runtime.

Usage::

    py scripts/openclaw_gateway_repair.py
    py scripts/openclaw_gateway_repair.py --normalize-only
    py scripts/openclaw_gateway_repair.py --json
    py scripts/openclaw_gateway_repair.py --check-only --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from akos.log import setup_logging
from akos.openclaw_config import apply_normalize_to_user_config
from akos.runtime import (
    GATEWAY_HTTP_RECOVERY_TIMEOUT_SEC,
    GATEWAY_RECOVERY_DEFAULT_TIMEOUT_SEC,
    GATEWAY_RECOVERY_POLL_SEC,
    GATEWAY_RPC_RECOVERY_TIMEOUT_SEC,
    GATEWAY_WARM_PROBE_RPC_PAUSE_SEC,
    GatewayRecoveryResult,
    check_openclaw_cli_version,
    gateway_probe_success,
    probe_gateway_http,
    probe_gateway_rpc_with_retries,
    recover_gateway_service,
    resolve_openclaw_cli,
)


def _emit_langfuse_repair_summary(summary: dict) -> bool:
    """Log repair outcome to Langfuse when credentials are present (H3)."""
    recovery = summary.get("recovery") or {}
    try:
        from akos.models import LangfuseTraceContext
        from akos.telemetry import LangfuseReporter

        reporter = LangfuseReporter(environment="gateway-repair")
        if not reporter.enabled:
            return False
        outcome = "ok" if recovery.get("success") else "fail"
        reporter.trace_request(
            {
                "agent_role": "gateway-repair",
                "tool_name": "openclaw_gateway_repair",
                "outcome": outcome,
                "input": str(summary.get("check_only", False)),
            },
            trace_context=LangfuseTraceContext(
                hlk_surface="rest_api",
                hlk_tool="openclaw_gateway_repair",
                substrate_adapter_id="SUB-OPENCLAW-GW-001",
            ),
        )
        reporter.flush()
        return True
    except Exception:
        return False


def run_check_only(*, wait_sec: float = 0.0) -> dict:
    cli = resolve_openclaw_cli()
    if not cli:
        return {
            "check_only": True,
            "recovery": {
                "success": False,
                "detail": "openclaw CLI not found",
                "http_ready": False,
                "rpc_ready": False,
                "recovery_hints": "",
            },
        }
    if wait_sec <= 0 and os.name == "nt":
        wait_sec = 180.0
    deadline = time.monotonic() + wait_sec
    http_ready = False
    rpc_ready = False
    rpc_detail = ""
    http_ready_since: float | None = None
    rpc_timeout = GATEWAY_RPC_RECOVERY_TIMEOUT_SEC if os.name == "nt" else 20
    while time.monotonic() <= deadline or (http_ready and not rpc_ready):
        http_ready = probe_gateway_http(timeout=GATEWAY_HTTP_RECOVERY_TIMEOUT_SEC)
        if http_ready and http_ready_since is None:
            http_ready_since = time.monotonic()
        if http_ready:
            rpc_ready, rpc_detail = probe_gateway_rpc_with_retries(
                cli,
                attempts=2,
                pause_sec=GATEWAY_WARM_PROBE_RPC_PAUSE_SEC,
                timeout=rpc_timeout,
            )
            warm_ok, warm_detail = gateway_probe_success(
                http_ready,
                rpc_ready,
                http_ready_since=http_ready_since,
            )
            if warm_ok:
                detail = (
                    "gateway healthy (check-only; no restart)"
                    if rpc_ready
                    else f"gateway healthy (check-only; {warm_detail})"
                )
                return {
                    "check_only": True,
                    "openclaw_version_ok": _version_preflight(cli),
                    "recovery": {
                        "success": True,
                        "detail": detail,
                        "http_ready": http_ready,
                        "rpc_ready": rpc_ready,
                        "recovery_hints": "",
                    },
                }
        if time.monotonic() >= deadline:
            break
        time.sleep(GATEWAY_RECOVERY_POLL_SEC)
    success = http_ready and rpc_ready
    detail = (
        "gateway healthy (check-only; no restart)"
        if success
        else f"gateway not ready (check-only; http={http_ready}, rpc={rpc_ready})"
    )
    hints = rpc_detail if not success and rpc_detail else ""
    return {
        "check_only": True,
        "openclaw_version_ok": _version_preflight(cli),
        "recovery": {
            "success": success,
            "detail": detail,
            "http_ready": http_ready,
            "rpc_ready": rpc_ready,
            "recovery_hints": hints,
        },
    }


def _version_preflight(cli: str | None) -> dict:
    if not cli:
        return {
            "meets_known_fix_floor": False,
            "parsed_version": "",
            "min_known_fix_version": "2026.4",
            "raw": "",
        }
    meets, parsed, raw = check_openclaw_cli_version(cli)
    return {
        "meets_known_fix_floor": meets,
        "parsed_version": parsed,
        "min_known_fix_version": "2026.4",
        "raw": raw[:120],
    }


def run_repair(
    *,
    normalize_only: bool = False,
    repair: bool = False,
    force: bool = False,
    timeout_seconds: int = GATEWAY_RECOVERY_DEFAULT_TIMEOUT_SEC,
    attempts: int = 2,
) -> dict:
    normalize_changed, normalize_notes = apply_normalize_to_user_config()
    if normalize_only:
        return {
            "normalize_changed": normalize_changed,
            "normalize_notes": normalize_notes,
            "recovery": None,
        }

    recovery: GatewayRecoveryResult | None = None
    for attempt in range(max(1, attempts)):
        recovery = recover_gateway_service(
            repair=repair,
            force=force,
            timeout_seconds=timeout_seconds,
            normalize_config=False,
        )
        if recovery.success:
            break

    assert recovery is not None
    payload = {
        "normalize_changed": normalize_changed,
        "normalize_notes": normalize_notes,
        "openclaw_version_ok": _version_preflight(resolve_openclaw_cli()),
        "recovery": {
            "success": recovery.success,
            "detail": recovery.detail,
            "http_ready": recovery.http_ready,
            "rpc_ready": recovery.rpc_ready,
            "recovery_hints": recovery.recovery_hints,
        },
    }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw gateway repair (AKOS adapter runbook)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable summary")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Probe HTTP+RPC only — no stop/start (use after reboot when scheduled task auto-starts gateway)",
    )
    parser.add_argument(
        "--normalize-only",
        action="store_true",
        help="Only align ~/.openclaw/openclaw.json with OpenClaw schema (no gateway restart)",
    )
    parser.add_argument(
        "--upstream-doctor",
        action="store_true",
        help="Run upstream openclaw doctor --repair after port reset (slower)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Pass --force to upstream openclaw doctor when --upstream-doctor is set",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=GATEWAY_RECOVERY_DEFAULT_TIMEOUT_SEC,
        help=f"Recovery poll budget in seconds (default {GATEWAY_RECOVERY_DEFAULT_TIMEOUT_SEC})",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=2,
        help="Automated recovery attempts before FAIL (default 2; operator does not retry manually)",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=None,
        help="Seconds to poll before giving up (check-only; default 180 on Windows, 0 elsewhere)",
    )
    parser.add_argument("--json-log", action="store_true", help="JSON logging for AKOS scripts")
    args = parser.parse_args()

    setup_logging(json_output=args.json_log)
    if args.check_only:
        wait = 180.0 if args.wait is None and os.name == "nt" else (args.wait or 0.0)
        summary = run_check_only(wait_sec=wait)
    else:
        summary = run_repair(
            normalize_only=args.normalize_only,
            repair=args.upstream_doctor,
            force=args.force,
            timeout_seconds=args.timeout,
            attempts=args.attempts,
        )

    if args.json:
        summary["langfuse_trace_logged"] = _emit_langfuse_repair_summary(summary)
        print(json.dumps(summary, indent=2))
    else:
        print()
        print("  OpenClaw gateway repair")
        if summary.get("normalize_changed"):
            print("    Config normalization applied:")
            for note in summary.get("normalize_notes") or []:
                print(f"      - {note}")
        elif summary.get("normalize_notes"):
            print(f"    Config: {summary['normalize_notes'][0]}")
        if summary["recovery"] is not None:
            rec = summary["recovery"]
            status = "PASS" if rec["success"] else "FAIL"
            print(f"    Recovery: {status}  {rec['detail']}")
            print(f"    HTTP ready: {rec['http_ready']}  RPC ready: {rec['rpc_ready']}")
            if rec.get("recovery_hints"):
                print("    Hints:")
                for line in str(rec["recovery_hints"]).splitlines():
                    print(f"      {line}")
        print()

    ok = args.normalize_only or bool(summary.get("recovery") and summary["recovery"]["success"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
