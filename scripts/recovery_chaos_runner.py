#!/usr/bin/env python3
"""Initiative 47 P9 — Real-chaos opt-in runner (D-IH-47-L).

Hybrid chaos posture per D-IH-47-L: synthetic mocks are the default; this
script is the single OPT-IN real-chaos surface.

## Safety contract (verified BEFORE any destructive op)

1. ``AKOS_REAL_CHAOS_OK=1`` env var must be set (default: refuse to run).
2. ``NEO4J_URI`` host MUST NOT match the MasterData host (default-refuse list:
   ``cpibdpgaarsbfnamudya.databases.neo4j.io`` and any host listed in
   ``AKOS_REAL_CHAOS_FORBIDDEN_HOSTS`` env var, semicolon-separated).
3. Operator must confirm the test instance ID via interactive prompt
   (pass ``--non-interactive`` ONLY in test fixtures with explicit
   ``--confirm-test-host=<host>`` matching the URI host).
4. The chaos op (NEO4J_PASSWORD rotation) MUST be paired with a restore step;
   the script exits non-zero if restore fails (operator must intervene
   manually via Aura console).

## Use cases

- Validate that ``scripts/graphrag_drift_canary.py`` correctly detects an
  Aura authentication failure (catches the I46 D-IH-32-Q password-truncation
  class of bug that mocks miss).
- Validate that the eval-tier-b matrix correctly reports the failure mode.

## Output

Writes a chaos report to:
``artifacts/chaos/real-chaos-neo4j-rotation-<UTC-timestamp>.json``

Run::

    AKOS_REAL_CHAOS_OK=1 py scripts/recovery_chaos_runner.py --scenario neo4j-password-rotation
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent
ARTIFACTS = REPO / "artifacts" / "chaos"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

# Default forbidden hosts (operator can extend via env).
DEFAULT_FORBIDDEN_HOSTS = {
    "cpibdpgaarsbfnamudya.databases.neo4j.io",  # MasterData
}

EXIT_NOT_OPTED_IN = 10
EXIT_FORBIDDEN_HOST = 11
EXIT_OPERATOR_DECLINED = 12
EXIT_RESTORE_FAILED = 13
EXIT_DEPENDENCY_MISSING = 14


def _emit_report(payload: dict) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ARTIFACTS / f"real-chaos-neo4j-rotation-{ts}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out


def _resolve_forbidden_hosts() -> set[str]:
    extra = (os.environ.get("AKOS_REAL_CHAOS_FORBIDDEN_HOSTS") or "").strip()
    extras = {h.strip().lower() for h in extra.split(";") if h.strip()} if extra else set()
    return {h.lower() for h in DEFAULT_FORBIDDEN_HOSTS} | extras


def _extract_uri_host(uri: str) -> str:
    """Extract host portion from a Neo4j URI (neo4j+s://host:port)."""
    if not uri:
        return ""
    parsed = urlparse(uri)
    return (parsed.hostname or "").lower()


def main() -> int:
    parser = argparse.ArgumentParser(description="I47 P9 real-chaos opt-in runner")
    parser.add_argument(
        "--scenario",
        choices=["neo4j-password-rotation"],
        required=True,
        help="Which chaos scenario to run.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip the interactive operator confirmation. ONLY for test fixtures; must be paired with --confirm-test-host.",
    )
    parser.add_argument(
        "--confirm-test-host",
        default="",
        help="Required with --non-interactive; must match the NEO4J_URI host exactly.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify all gates and emit a planned-only report; do not actually rotate.",
    )
    args = parser.parse_args()

    payload: dict = {
        "scenario": args.scenario,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "gate_checks": {},
    }

    # Gate 1: AKOS_REAL_CHAOS_OK=1
    opt_in = (os.environ.get("AKOS_REAL_CHAOS_OK") or "").strip()
    payload["gate_checks"]["akos_real_chaos_ok"] = opt_in
    if opt_in != "1":
        payload["status"] = "REFUSED"
        payload["reason"] = (
            "AKOS_REAL_CHAOS_OK env var not set to '1'. Real-chaos refuses to "
            "run by default per D-IH-47-L. Set AKOS_REAL_CHAOS_OK=1 to proceed."
        )
        out = _emit_report(payload)
        print(f"REFUSED: AKOS_REAL_CHAOS_OK != 1. Report: {out}")
        return EXIT_NOT_OPTED_IN

    # Gate 2: NEO4J_URI host check
    uri = os.environ.get("NEO4J_URI", "")
    host = _extract_uri_host(uri)
    forbidden = _resolve_forbidden_hosts()
    payload["gate_checks"]["neo4j_uri_host"] = host
    payload["gate_checks"]["forbidden_hosts"] = sorted(forbidden)
    if not host:
        payload["status"] = "REFUSED"
        payload["reason"] = "NEO4J_URI not set or unparseable; refuse to operate without explicit host."
        out = _emit_report(payload)
        print(f"REFUSED: NEO4J_URI missing/unparseable. Report: {out}")
        return EXIT_FORBIDDEN_HOST
    if host in forbidden:
        payload["status"] = "REFUSED"
        payload["reason"] = (
            f"NEO4J_URI host {host!r} is in the forbidden-hosts list. "
            f"Real-chaos REFUSES to run against MasterData or any operator-protected host. "
            f"Use a throwaway test instance only."
        )
        out = _emit_report(payload)
        print(f"REFUSED: host {host} is forbidden. Report: {out}")
        return EXIT_FORBIDDEN_HOST

    # Gate 3: operator confirmation
    if args.non_interactive:
        if args.confirm_test_host.strip().lower() != host:
            payload["status"] = "REFUSED"
            payload["reason"] = (
                f"--non-interactive requires --confirm-test-host to match the URI host exactly. "
                f"Got {args.confirm_test_host!r}; expected {host!r}."
            )
            out = _emit_report(payload)
            print(f"REFUSED: --confirm-test-host mismatch. Report: {out}")
            return EXIT_OPERATOR_DECLINED
        payload["gate_checks"]["operator_confirmation"] = "non_interactive_match"
    else:
        print(f"Real-chaos scenario: {args.scenario}")
        print(f"NEO4J_URI host: {host}")
        print(f"This will ROTATE the NEO4J_PASSWORD on this instance, run the drift canary, then RESTORE.")
        try:
            answer = input(f"Type the host {host!r} to confirm: ").strip().lower()
        except EOFError:
            answer = ""
        if answer != host:
            payload["status"] = "REFUSED"
            payload["reason"] = "Operator declined or did not type the host correctly."
            out = _emit_report(payload)
            print(f"REFUSED: operator declined. Report: {out}")
            return EXIT_OPERATOR_DECLINED
        payload["gate_checks"]["operator_confirmation"] = "interactive_confirmed"

    payload["gate_checks"]["all_gates_passed"] = True

    if args.dry_run:
        payload["status"] = "PLANNED"
        payload["plan"] = [
            "Read current NEO4J_PASSWORD from env (~/.openclaw/.env)",
            "Rotate Aura password via Aura HTTP API (operator must have NEO4J_AURA_API_KEY set)",
            "Wait 5s for propagation",
            "Run scripts/graphrag_drift_canary.py with the OLD password (expect AuthError)",
            "Restore the original password via Aura HTTP API",
            "Run drift canary again with restored password (expect 0 drift)",
            "Emit chaos report with timeline + drift-canary outputs",
        ]
        out = _emit_report(payload)
        print(f"DRY-RUN: gates verified; plan emitted. Report: {out}")
        return 0

    # Live mode requires the Aura HTTP API surface; if neither key is present
    # we exit-with-actionable rather than half-rotating.
    aura_key = os.environ.get("NEO4J_AURA_API_KEY", "")
    if not aura_key:
        payload["status"] = "REFUSED"
        payload["reason"] = (
            "NEO4J_AURA_API_KEY env var missing. Real-chaos runner requires the "
            "Aura HTTP API to perform credential rotation safely. See: "
            "https://neo4j.com/docs/aura/api/authentication/"
        )
        out = _emit_report(payload)
        print(f"REFUSED: NEO4J_AURA_API_KEY missing. Report: {out}")
        return EXIT_DEPENDENCY_MISSING

    # Live mode (placeholder; full implementation lands when operator approves
    # first chaos run and pins the Aura API contract).
    payload["status"] = "PLANNED"
    payload["reason"] = (
        "Live rotation path is gated until operator approves first chaos run "
        "and the Aura API contract is pinned in the chaos runner. Use --dry-run "
        "until then. Tracked as D-IH-47-L follow-up."
    )
    out = _emit_report(payload)
    print(f"PLANNED-ONLY: gates verified; live rotation deferred to operator approval. Report: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
