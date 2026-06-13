"""Work-item carryover posture taxonomy SSOT (Initiative 98 P0; **D-IH-98-A** pending).

Layer 2 companion to ``akos.planning.status_taxonomy`` (initiative-level **D-IH-59-D**).
Governs decisions, deliverables, OPS rows, and tracker artifacts **inside or across**
initiatives — not initiative ``status:`` itself.

Plain-language contract (operator intent 2026-06-12):

- **scheduled** ≠ **dropped**
- Bare "deferred" without a posture tag is deprecated in new artifacts
- Every scheduled/forward/blocked/overlap item carries a ``discoverability_path``

Shared by:

- ``docs/wip/planning/_trackers/carryover-posture-index.md`` row validator
- ``scripts/validate_carryover_posture.py``
- ``scripts/render_wip_dashboard.py`` scheduled-carryover section
- Initiative ``decision-log.md`` posture companion blocks
"""

from __future__ import annotations

from enum import StrEnum


class CarryoverPosture(StrEnum):
    """Seven-value work-item carryover posture enum."""

    SCHEDULED = "scheduled"
    FORWARD_CHARTER = "forward_charter"
    OVERLAP_PENDING = "overlap_pending"
    BLOCKED = "blocked"
    DROPPED = "dropped"
    SUPERSEDED = "superseded"
    MONITORING = "monitoring"


VALID_CARRYOVER_POSTURES: frozenset[str] = frozenset(p.value for p in CarryoverPosture)
"""Frozenset of valid posture string values (validator-friendly form)."""


POSTURE_PLAIN_LABELS: dict[str, str] = {
    CarryoverPosture.SCHEDULED.value: "Scheduled after evidence (not dropped)",
    CarryoverPosture.FORWARD_CHARTER.value: "Forward-chartered to successor",
    CarryoverPosture.OVERLAP_PENDING.value: "Overlap pending phase ratify",
    CarryoverPosture.BLOCKED.value: "Blocked on activation gates",
    CarryoverPosture.DROPPED.value: "Explicitly out of scope",
    CarryoverPosture.SUPERSEDED.value: "Superseded by ratified decision",
    CarryoverPosture.MONITORING.value: "Shipped with closure obligation (PWF)",
}
"""Operator-facing one-liners keyed by posture value."""


REQUIRED_COMPANION_FIELDS: dict[str, tuple[str, ...]] = {
    CarryoverPosture.SCHEDULED.value: (
        "target_initiative",
        "target_phase",
        "activation_trigger",
        "owner_role",
        "next_review_trigger",
        "discoverability_path",
    ),
    CarryoverPosture.FORWARD_CHARTER.value: (
        "successor_ref",
        "activation_trigger",
        "owner_role",
        "next_review_trigger",
        "discoverability_path",
    ),
    CarryoverPosture.OVERLAP_PENDING.value: (
        "scope_overlap_tracker",
        "ratify_phase",
        "tracked_siblings",
        "owner_role",
        "next_review_trigger",
        "discoverability_path",
    ),
    CarryoverPosture.BLOCKED.value: (
        "blocker_tracker",
        "resolution_conditions",
        "owner_role",
        "next_review_trigger",
        "discoverability_path",
    ),
    CarryoverPosture.DROPPED.value: (
        "drop_rationale",
        "reversibility",
    ),
    CarryoverPosture.SUPERSEDED.value: (
        "supersedes_decision_id",
        "successor_decision_id",
    ),
    CarryoverPosture.MONITORING.value: (
        "followup_class",
        "closure_target",
        "owner_role",
        "next_review_trigger",
        "linked_uat_path",
    ),
}
"""Map of posture value → required companion field names."""


INDEX_DASHBOARD_POSTURES: tuple[str, ...] = (
    CarryoverPosture.SCHEDULED.value,
    CarryoverPosture.FORWARD_CHARTER.value,
    CarryoverPosture.OVERLAP_PENDING.value,
    CarryoverPosture.BLOCKED.value,
    CarryoverPosture.MONITORING.value,
)
"""Postures surfaced in the WIP dashboard carryover section (active obligations)."""


def required_companion_fields(posture: str) -> tuple[str, ...]:
    """Return required companion field names for ``posture`` (empty if unknown)."""
    return REQUIRED_COMPANION_FIELDS.get(posture, ())


def is_valid_posture(posture: str) -> bool:
    """Return True if ``posture`` is one of the seven enum values."""
    return posture in VALID_CARRYOVER_POSTURES
