#!/usr/bin/env python3
"""Operator-invoked health-monitor escalation helper (I87 P1 / D-IH-87-A).

Per **D-IH-87-A** (I87 P0 charter): the OpenClaw runtime health-monitor must
emit an operator-visible escalation row to ``OPS_REGISTER.csv`` (low-coupling
sink already rendered by ``scripts/render_operator_inbox.py``) when N=3
consecutive health-probe failures of the same class are observed. The full
auto-emit integration into the OpenClaw control-plane health monitor is
deferred to a follow-up; this MVP exposes the **same emission path** as a
deterministic operator-invoked CLI so:

1. The escalation contract is testable + governed before the runtime hooks land.
2. Operators can manually escalate observed multi-failure scenarios today.
3. The next iteration (auto-emit) reuses ``emit_escalation_row()`` verbatim,
   importable as a library function from the runtime monitor.

Usage
=====

::

    py scripts/openclaw_health_escalate.py \\
        --symptom-class ws-token-expiration \\
        --consecutive-failures 3 \\
        --evidence-path docs/wip/intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md \\
        --rice-impact 2

The script appends one ``OPS-87-<seq>`` row to ``OPS_REGISTER.csv`` with
``status=open``, ``owner_class=operator``, ``originating_initiative_id=INIT-OPENCLAW_AKOS-87``,
and the supplied symptom-class + evidence path. The next ``render_operator_inbox.py``
run will surface the row in ``OPERATOR_INBOX.md`` at the position determined by
the RICE score.

Governance contract
===================

Per [`akos-governance-remediation.mdc`](../.cursor/rules/akos-governance-remediation.mdc)
§"Runtime contract": treating ``Runtime: unknown`` as a healthy state is an
observability contract bug. This script makes the failure-loop observable by
turning it into a row the operator surface already renders. Per
[`akos-holistika-operations.mdc`](../.cursor/rules/akos-holistika-operations.mdc)
§"New git-canonical compliance registers": OPS_REGISTER.csv is the canonical
sink for operator-visible actions; no separate sidecar register is minted.

The script is **idempotent within a calendar day**: if an OPS row already exists
for the same ``symptom_class`` with ``opened_at`` equal to today and
``status=open``, the script logs the duplicate and exits 0 without appending,
so a noisy health-monitor cannot flood the inbox.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.log import setup_logging

setup_logging()
log = logging.getLogger(__name__)

OPS_REGISTER_CSV = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "People"
    / "Compliance"
    / "canonicals"
    / "OPS_REGISTER.csv"
)

I87_INITIATIVE_ID = "INIT-OPENCLAW_AKOS-87"
I87_OWNER_ROLE = "System Owner"
I87_DECISION_ID = "D-IH-87-A"

# Allowed symptom-class slugs (free-form ``[a-z0-9-]+`` but constrained at CLI
# parse-time so the inbox stays scannable).
SYMPTOM_CLASS_RE = re.compile(r"^[a-z][a-z0-9-]{2,40}$")

# Allowed RICE impact tiers (must match ``akos/hlk_ops_register_csv.py`` enum).
ALLOWED_RICE_IMPACT = ("0.25", "0.5", "1", "2", "3")


def _next_ops_sequence(rows: list[dict[str, str]]) -> int:
    """Return the next integer sequence within ``OPS-87-<seq>``.

    Counts existing rows with ``originating_initiative_id == INIT-OPENCLAW_AKOS-87``
    and returns one greater than the maximum trailing integer parsed from
    ``ops_action_id``. New initiatives start at 1.
    """
    max_seq = 0
    for row in rows:
        if row.get("originating_initiative_id") != I87_INITIATIVE_ID:
            continue
        action_id = row.get("ops_action_id", "")
        m = re.match(r"^OPS-87-(\d+)(?:\.[a-z0-9]+)?$", action_id)
        if m:
            max_seq = max(max_seq, int(m.group(1)))
    return max_seq + 1


def _has_open_row_for_today(
    rows: list[dict[str, str]], symptom_class: str, today: str
) -> bool:
    """Check the idempotency-within-a-day contract.

    Returns True when an open OPS-87 row already references this ``symptom_class``
    via its ``title`` field and was opened today.
    """
    for row in rows:
        if row.get("originating_initiative_id") != I87_INITIATIVE_ID:
            continue
        if row.get("status") != "open":
            continue
        if row.get("opened_at") != today:
            continue
        title = row.get("title", "")
        if symptom_class in title:
            return True
    return False


def emit_escalation_row(
    *,
    symptom_class: str,
    consecutive_failures: int,
    evidence_path: str,
    rice_impact: str = "2",
    dry_run: bool = False,
    today: str | None = None,
) -> dict[str, str] | None:
    """Append one OPS-87-<seq> row to OPS_REGISTER.csv. Library entrypoint.

    Returns the appended row dict, or ``None`` when the idempotency guard fires
    (duplicate open row for the same symptom_class on the same day). Returns
    the would-be row without writing when ``dry_run=True``.
    """
    if not SYMPTOM_CLASS_RE.match(symptom_class):
        raise ValueError(
            f"symptom_class must match {SYMPTOM_CLASS_RE.pattern!r}; got "
            f"{symptom_class!r}"
        )
    if consecutive_failures < 1:
        raise ValueError(
            f"consecutive_failures must be >= 1; got {consecutive_failures}"
        )
    if rice_impact not in ALLOWED_RICE_IMPACT:
        raise ValueError(
            f"rice_impact must be one of {ALLOWED_RICE_IMPACT}; got {rice_impact!r}"
        )

    today = today or dt.date.today().isoformat()

    if not OPS_REGISTER_CSV.exists():
        raise FileNotFoundError(f"OPS_REGISTER.csv not found at {OPS_REGISTER_CSV}")

    with OPS_REGISTER_CSV.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    if _has_open_row_for_today(rows, symptom_class, today):
        log.info(
            "Idempotency guard: open OPS-87 row already exists for "
            "symptom_class=%s opened_at=%s; skipping append",
            symptom_class,
            today,
        )
        return None

    seq = _next_ops_sequence(rows)
    new_row: dict[str, str] = {
        "ops_action_id": f"OPS-87-{seq}",
        "title": f"OpenClaw health-monitor escalation: {symptom_class}",
        "originating_initiative_id": I87_INITIATIVE_ID,
        "forwarded_to_initiative_id": "",
        "owner_class": "operator",
        "owner_role": I87_OWNER_ROLE,
        "status": "open",
        "rice_reach": "10",
        "rice_impact": rice_impact,
        "rice_confidence_pct": "80",
        "rice_effort_person_weeks": "0.5",
        "rice_score": "",
        "gate_id": "",
        "linked_decision_ids": I87_DECISION_ID,
        "summary": (
            f"Health-monitor observed {consecutive_failures} consecutive "
            f"failures of class {symptom_class}; escalated to operator inbox "
            f"per D-IH-87-A."
        ),
        "operator_runbook_path": "scripts/openclaw_health_escalate.py",
        "evidence_path": evidence_path,
        "opened_at": today,
        "closed_at": "",
        "notes": (
            f"Auto-emitted by scripts/openclaw_health_escalate.py "
            f"(consecutive_failures={consecutive_failures})"
        ),
        "last_review_at": today,
        "last_review_by": I87_OWNER_ROLE,
        "last_review_decision_id": I87_DECISION_ID,
        "methodology_version_at_review": "v3.0",
    }

    # Compute RICE score: reach * impact * (confidence/100) / effort
    reach = float(new_row["rice_reach"])
    impact = float(new_row["rice_impact"])
    confidence = float(new_row["rice_confidence_pct"]) / 100.0
    effort = float(new_row["rice_effort_person_weeks"])
    new_row["rice_score"] = f"{reach * impact * confidence / effort:.2f}"

    if dry_run:
        log.info("DRY-RUN: would append row %s", new_row["ops_action_id"])
        return new_row

    with OPS_REGISTER_CSV.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writerow(new_row)

    log.info(
        "Appended %s to OPS_REGISTER.csv (symptom_class=%s, consecutive_failures=%s)",
        new_row["ops_action_id"],
        symptom_class,
        consecutive_failures,
    )
    return new_row


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Emit an OPS-87-<seq> escalation row to OPS_REGISTER.csv when the "
            "OpenClaw health-monitor observes N consecutive failures of the "
            "same class. Per D-IH-87-A (I87 P1)."
        )
    )
    parser.add_argument(
        "--symptom-class",
        required=True,
        help=(
            "Slug for the failure class (e.g. ws-token-expiration, "
            "docker-sandbox-churn). Must match [a-z][a-z0-9-]{2,40}."
        ),
    )
    parser.add_argument(
        "--consecutive-failures",
        required=True,
        type=int,
        help="Number of consecutive failures observed (must be >= 1; N=3 is the canonical threshold).",
    )
    parser.add_argument(
        "--evidence-path",
        required=True,
        help=(
            "Path (repo-relative) to the evidence file/log capturing the "
            "failure pattern. Stored on the OPS row for operator review."
        ),
    )
    parser.add_argument(
        "--rice-impact",
        default="2",
        choices=ALLOWED_RICE_IMPACT,
        help="RICE impact tier (default: 2).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the would-be row to stderr but do not write the CSV.",
    )
    args = parser.parse_args(argv)

    try:
        row = emit_escalation_row(
            symptom_class=args.symptom_class,
            consecutive_failures=args.consecutive_failures,
            evidence_path=args.evidence_path,
            rice_impact=args.rice_impact,
            dry_run=args.dry_run,
        )
    except (ValueError, FileNotFoundError) as exc:
        log.error("Escalation aborted: %s", exc)
        return 2

    if row is None:
        log.info("No row appended (idempotency guard)")
        return 0

    if args.dry_run:
        log.info("DRY-RUN row: %s", row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
