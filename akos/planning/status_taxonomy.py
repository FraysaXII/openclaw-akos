"""Initiative status taxonomy SSOT (Initiative 59 P2; **D-IH-59-D**).

Single source of truth for the seven-value initiative-status enum, shared by:

- ``master-roadmap.md`` frontmatter ``status:`` field validator.
- ``INITIATIVE_REGISTRY.csv`` ``status`` column schema.
- ``scripts/render_wip_dashboard.py`` section-split renderer.
- ``scripts/render_operator_inbox.py`` (filters by ``gated_operator``).
- ``scripts/check_active_initiative_freshness.py`` (filters by ``active``).

The seven values are deliberately distinct: each maps to a different operator
expectation and dashboard section. Adding a new status requires extending this
module, then updating ``render_wip_dashboard.py`` to add a section for it.

Companion fields (per **D-IH-59-D**):

- ``closed`` — requires ``closed_at`` (YYYY-MM-DD) and typically ``closure_decision_id``.
- ``archived`` — requires ``archived_at`` (YYYY-MM-DD) and ``superseded_by``.
- ``active`` — no required companion fields; ``last_review`` informs freshness canary.
- ``continuous`` — requires ``continuous_rationale`` (free-form prose).
- ``program_line`` — requires ``cadence`` (weekly | monthly | quarterly | event_driven).
- ``gated_external`` — requires ``gated_on`` (free-form prose, e.g. "advisor reply").
- ``gated_operator`` — requires ``gated_on`` AND ``operator_action`` (linked OPS action).
"""

from __future__ import annotations

from enum import StrEnum


class InitiativeStatus(StrEnum):
    """Seven-value initiative status enum.

    See module docstring for companion-field rules.
    """

    CLOSED = "closed"
    ARCHIVED = "archived"
    ACTIVE = "active"
    CONTINUOUS = "continuous"
    PROGRAM_LINE = "program_line"
    GATED_EXTERNAL = "gated_external"
    GATED_OPERATOR = "gated_operator"


VALID_INITIATIVE_STATUSES: frozenset[str] = frozenset(s.value for s in InitiativeStatus)
"""Frozenset of valid status string values (validator-friendly form)."""


REQUIRED_COMPANION_FIELDS: dict[str, tuple[str, ...]] = {
    InitiativeStatus.CLOSED.value: ("closed_at",),
    InitiativeStatus.ARCHIVED.value: ("archived_at", "superseded_by"),
    InitiativeStatus.ACTIVE.value: (),
    InitiativeStatus.CONTINUOUS.value: ("continuous_rationale",),
    InitiativeStatus.PROGRAM_LINE.value: ("cadence",),
    InitiativeStatus.GATED_EXTERNAL.value: ("gated_on",),
    InitiativeStatus.GATED_OPERATOR.value: ("gated_on", "operator_action"),
}
"""Map of status value → required companion field names.

Validators consume this to enforce companion-field presence per the
D-IH-59-D contract. An empty tuple means no companion fields are required.
"""


DASHBOARD_SECTION_ORDER: tuple[str, ...] = (
    InitiativeStatus.ACTIVE.value,
    InitiativeStatus.GATED_EXTERNAL.value,
    InitiativeStatus.GATED_OPERATOR.value,
    InitiativeStatus.CONTINUOUS.value,
    InitiativeStatus.PROGRAM_LINE.value,
    InitiativeStatus.CLOSED.value,
    InitiativeStatus.ARCHIVED.value,
)
"""Canonical section order for the WIP dashboard (P2 split)."""


DASHBOARD_SECTION_TITLES: dict[str, str] = {
    InitiativeStatus.ACTIVE.value: "Active (in execution)",
    InitiativeStatus.GATED_EXTERNAL.value: "Gated on external event",
    InitiativeStatus.GATED_OPERATOR.value: "Gated on operator action",
    InitiativeStatus.CONTINUOUS.value: "Continuous loops (active by design)",
    InitiativeStatus.PROGRAM_LINE.value: "Program lines (cadence-driven)",
    InitiativeStatus.CLOSED.value: "Closed",
    InitiativeStatus.ARCHIVED.value: "Archived (superseded)",
}
"""Operator-friendly section headings keyed by status value."""


def required_companion_fields(status: str) -> tuple[str, ...]:
    """Return the tuple of required companion field names for ``status``.

    Returns an empty tuple if ``status`` is unknown (lenient lookup so callers
    can decide error handling separately from companion-field discovery).
    """
    return REQUIRED_COMPANION_FIELDS.get(status, ())


def is_valid_status(status: str) -> bool:
    """Return True if ``status`` is one of the seven enum values."""
    return status in VALID_INITIATIVE_STATUSES
