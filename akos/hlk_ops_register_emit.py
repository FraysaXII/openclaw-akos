"""OPS_REGISTER emit helper — programmatic Python contract for writers that need to surface operator actions.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).

Per R4 (HLK-ERP observability convergence) in the Bundle B-2 architecture report: instead of minting new
dashboards / surfaces / alert channels for FINOPS-writer events (DLQ alerts, FX divergence, counterparty
resolution failures), the writer emits rows to OPS_REGISTER.csv which auto-render into OPERATOR_INBOX.md
via the existing scripts/render_operator_inbox.py pipeline.

This module is the **Python-side** contract; the **TypeScript-side** mirror lives in the Edge Function
finops-writer-worker (Bundle B-2b) and writes directly to compliance.ops_register_mirror via service_role.

Two emission paths:

1. **In-Python / agent emit** (this module's primary use): tools/scripts/agents call
   ``emit_ops_register_row()`` to build a well-formed row dict, then append to OPS_REGISTER.csv via
   the canonical-CSV-write discipline (operator gate per akos-governance-remediation.mdc when manual;
   automatic for system writes per R4 + the OPS_REGISTER.csv `operator_runbook_path` column).

2. **Worker emit** (Bundle B-2b): TypeScript worker uses the equivalent shape directly against
   compliance.ops_register_mirror. Drift between Python and TypeScript schemas surfaces as test failure
   in B-2b worker tests.

See:
- ``docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/p2-bundle-b2-architecture-2026-05-23.md`` §3.4 for R4 architecture.
- ``scripts/render_operator_inbox.py`` for the auto-render pipeline.
- ``docs/wip/planning/OPERATOR_INBOX.md`` for the rendered operator surface.
- ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv`` for the SSOT.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Keep in sync with OPS_REGISTER.csv header row (24 columns as of I71 P4 review-stamp extension).
OPS_REGISTER_FIELDNAMES: tuple[str, ...] = (
    "ops_action_id",
    "title",
    "originating_initiative_id",
    "forwarded_to_initiative_id",
    "owner_class",
    "owner_role",
    "status",
    "rice_reach",
    "rice_impact",
    "rice_confidence_pct",
    "rice_effort_person_weeks",
    "rice_score",
    "gate_id",
    "linked_decision_ids",
    "summary",
    "operator_runbook_path",
    "evidence_path",
    "opened_at",
    "closed_at",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)


VALID_OWNER_CLASSES: frozenset[str] = frozenset({
    "operator",      # human operator action required (highest visibility)
    "system",        # system action queued; informational
    "agent",         # AIC/agent action queued; informational
    "shared",        # operator + system collaboration
})


VALID_STATUSES: frozenset[str] = frozenset({
    "open",          # row is actionable; appears in OPERATOR_INBOX
    "in_progress",   # being worked on
    "blocked",       # blocked on external dependency
    "closed",        # resolved; archived from OPERATOR_INBOX active view
    "cancelled",     # never triggered or no longer applicable
})


VALID_FINOPS_WRITER_OPS_CLASSES: frozenset[str] = frozenset({
    # FINOPS writer-specific ops_class values (subset; full catalog at OPS_REGISTER.csv per-row notes).
    "counterparty_resolution_failed",          # R1 strategy 4 — manual_review fallback fired
    "stripe_customer_link_lookup_pending",     # R1 strategy 3 — SQL lookup needed before fact write
    "fx_divergence_threshold_exceeded",        # R2 — ECB vs Stripe FX rate divergence > 0.5%
    "fx_cache_stale",                          # R2 — ECB cache > 2 days behind; used fallback
    "dlq_threshold_exceeded",                  # R3 — finops_writer_dlq depth > N
    "dlq_event_max_retries",                   # R3 — single event exhausted retry budget
    "stripe_webhook_signature_mismatch",       # security: invalid webhook signature received
    "stripe_metadata_missing",                 # event missing hlk_billing_plane / hlk_engagement_id metadata
})


class OpsRegisterRow(BaseModel):
    """Pydantic frozen BaseModel for one OPS_REGISTER.csv row (24-column SSOT).

    Per CONTRIBUTING.md Python Code Standards + akos-holistika-operations.mdc.
    Used by FINOPS writer (B-2a Python emit) + Edge Function worker (B-2b TypeScript emit, schema mirror).
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    ops_action_id: str = Field(
        ...,
        pattern=r"^OPS-\d{1,3}-\d{1,4}$",
        description="Format: OPS-<initiative-num>-<seq>. Initiative-num matches originating_initiative_id INIT-OPENCLAW_AKOS-XX suffix.",
    )
    title: str = Field("", max_length=240)
    originating_initiative_id: str = Field(
        ...,
        pattern=r"^INIT-[A-Z_]+-\d{1,3}$",
        description="FK-by-convention to INITIATIVE_REGISTRY.csv initiative_id (e.g. INIT-OPENCLAW_AKOS-81).",
    )
    forwarded_to_initiative_id: str = Field("", description="Optional FK if this OPS row is forwarded to a successor initiative.")
    owner_class: Literal["operator", "system", "agent", "shared"]
    owner_role: str = Field(..., min_length=1, max_length=120, description="FK-by-convention to baseline_organisation.csv role_name.")
    status: Literal["open", "in_progress", "blocked", "closed", "cancelled"]
    rice_reach: str = Field("", description="RICE reach component (free text per OPS_REGISTER convention).")
    rice_impact: str = Field("", description="RICE impact component.")
    rice_confidence_pct: str = Field("", description="RICE confidence percentage (e.g. '80').")
    rice_effort_person_weeks: str = Field("", description="RICE effort in person-weeks (e.g. '2').")
    rice_score: str = Field("", description="Computed RICE score (caller's responsibility).")
    gate_id: str = Field("", max_length=120, description="Optional gate identifier this OPS row is tied to.")
    linked_decision_ids: str = Field("", description="Semicolon-separated list of D-IH-XX-Y decision ids.")
    summary: str = Field(..., min_length=1, max_length=2048, description="Human-readable summary; renders to OPERATOR_INBOX.md.")
    operator_runbook_path: str = Field("", description="Optional path to runbook the operator should consult.")
    evidence_path: str = Field("", description="Optional path to evidence file (e.g. reports/uat-*.md).")
    opened_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    closed_at: str = Field("", description="ISO date when status flipped to closed; empty otherwise.")
    notes: str = Field("", max_length=2048)
    last_review_at: str = Field("", description="I71 P4 review-stamp (ISO YYYY-MM-DD).")
    last_review_by: str = Field("", description="I71 P4 review-stamp (FK-by-convention to baseline_organisation.csv role_name).")
    last_review_decision_id: str = Field("", description="I71 P4 review-stamp (FK-by-convention to DECISION_REGISTER.csv decision_id).")
    methodology_version_at_review: str = Field("", description="I71 P4 review-stamp (e.g. 'v3.1').")


def emit_ops_register_row(
    *,
    ops_action_id: str,
    originating_initiative_id: str,
    owner_class: str,
    owner_role: str,
    summary: str,
    title: str = "",
    linked_decision_ids: str = "",
    notes: str = "",
    rice_reach: str = "",
    rice_impact: str = "",
    rice_confidence_pct: str = "",
    rice_effort_person_weeks: str = "",
    operator_runbook_path: str = "",
    evidence_path: str = "",
    opened_at: str | None = None,
) -> dict[str, str]:
    """Build a well-formed OPS_REGISTER row dict ready to append to OPS_REGISTER.csv.

    All defaults are conservative: status='open' (highest visibility), rice_score computed if all
    RICE components present (else empty), opened_at defaults to today (UTC), review-stamp columns
    left empty (callers responsibility on next quarterly review per I71 P4 cadence).

    Args:
        ops_action_id: Format OPS-<init-num>-<seq>; caller is responsible for sequence uniqueness.
        originating_initiative_id: FK to INITIATIVE_REGISTRY.csv (e.g. 'INIT-OPENCLAW_AKOS-81').
        owner_class: one of VALID_OWNER_CLASSES.
        owner_role: FK-by-convention to baseline_organisation.csv role_name.
        summary: human-readable summary for OPERATOR_INBOX render.
        title: optional short title (defaults to first 80 chars of summary).
        linked_decision_ids: semicolon-list of D-IH-XX-Y decision ids.
        notes: free-text notes.
        rice_*: optional RICE components (free text per OPS_REGISTER convention).
        operator_runbook_path: optional path to runbook.
        evidence_path: optional path to evidence file.
        opened_at: ISO date YYYY-MM-DD (defaults to today UTC).

    Returns:
        Dict ready for csv.DictWriter.writerow against OPS_REGISTER_FIELDNAMES.

    Raises:
        ValueError: if ops_action_id / originating_initiative_id / owner_class fail format checks.
    """

    if not re.match(r"^OPS-\d{1,3}-\d{1,4}$", ops_action_id):
        raise ValueError(f"ops_action_id must match OPS-<num>-<seq>; got {ops_action_id!r}")
    if not re.match(r"^INIT-[A-Z_]+-\d{1,3}$", originating_initiative_id):
        raise ValueError(f"originating_initiative_id must match INIT-<NAME>-<num>; got {originating_initiative_id!r}")
    if owner_class not in VALID_OWNER_CLASSES:
        raise ValueError(f"owner_class {owner_class!r} not in {VALID_OWNER_CLASSES}")

    if opened_at is None:
        opened_at = date.today().isoformat()

    if not title:
        title = summary[:80]

    # Compute rice_score if all components present + numeric
    rice_score = ""
    try:
        if all([rice_reach, rice_impact, rice_confidence_pct, rice_effort_person_weeks]):
            score = (
                float(rice_reach) * float(rice_impact) * (float(rice_confidence_pct) / 100.0)
            ) / float(rice_effort_person_weeks)
            rice_score = f"{score:.2f}"
    except (ValueError, ZeroDivisionError):
        rice_score = ""

    row = {
        "ops_action_id": ops_action_id,
        "title": title,
        "originating_initiative_id": originating_initiative_id,
        "forwarded_to_initiative_id": "",
        "owner_class": owner_class,
        "owner_role": owner_role,
        "status": "open",
        "rice_reach": rice_reach,
        "rice_impact": rice_impact,
        "rice_confidence_pct": rice_confidence_pct,
        "rice_effort_person_weeks": rice_effort_person_weeks,
        "rice_score": rice_score,
        "gate_id": "",
        "linked_decision_ids": linked_decision_ids,
        "summary": summary,
        "operator_runbook_path": operator_runbook_path,
        "evidence_path": evidence_path,
        "opened_at": opened_at,
        "closed_at": "",
        "notes": notes,
        "last_review_at": "",
        "last_review_by": "",
        "last_review_decision_id": "",
        "methodology_version_at_review": "",
    }

    # Pydantic validation (fail fast on schema drift)
    OpsRegisterRow.model_validate(row)
    return row
