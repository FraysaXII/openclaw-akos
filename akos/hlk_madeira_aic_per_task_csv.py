"""Field contract for MADEIRA_AIC_PER_TASK_REGISTRY.csv (Initiative 82 P4 / I86 Wave Q CSV 4 child).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per I76 master-roadmap §P4 (MADEIRA per-task dispatcher gate) +
HOLISTIKA_AGENTIC_DOCTRINE.md (AIC consent-to-consume + KB-access posture).

Child of AIC_REGISTRY.csv via FK aic_id (filter aic_id LIKE 'AIC-MADEIRA-%';
non-MADEIRA AICs do not appear here — they get their own per-task registry
when forecasted to active status).

Each row binds one MADEIRA-class AIC to one task-class with a dispatcher
pattern, tool-catalog reference, and RBAC class. The dispatcher pattern is
the operational gate per I76 P4 doctrine.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

MADEIRA_AIC_PER_TASK_FIELDNAMES: tuple[str, ...] = (
    "task_id",
    "aic_id",
    "task_class",
    "dispatcher_pattern",
    "tool_catalog_ref",
    "rbac_class",
    "status",
    "notes",
    "last_audit_at",
    "last_audit_by",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)


CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/MADEIRA_AIC_PER_TASK_REGISTRY.csv"
)


VALID_TASK_CLASSES: frozenset[str] = frozenset(
    {
        "code-authoring",
        "doctrine-curation",
        "uat-verification",
        "research-synthesis",
        "regression-sweep",
        "render-rebuild",
        "engagement-coordination",
        "ratification-gate-authoring",
    }
)


VALID_DISPATCHER_PATTERNS: frozenset[str] = frozenset(
    {
        "operator-inline",
        "operator-async",
        "agent-spawn-subagent",
        "scheduled-cron",
        "event-triggered",
        "gated-operator",
    }
)


VALID_RBAC_CLASSES: frozenset[str] = frozenset(
    {
        "read-only",
        "read-and-write",
        "read-write-sensitive",
        "render-only",
    }
)


VALID_STATUSES: frozenset[str] = frozenset(
    {
        "active",
        "pilot",
        "forecasted",
        "retired",
    }
)


class MadeiraAICPerTaskRow(BaseModel):
    """One MADEIRA-class AIC bound to one task-class via a dispatcher pattern."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    task_id: str = Field(pattern=r"^MTASK-[A-Z0-9-]+$", min_length=7, max_length=80)
    aic_id: str = Field(pattern=r"^AIC-MADEIRA-[A-Z0-9-]+$", min_length=12, max_length=80)
    task_class: Literal[
        "code-authoring",
        "doctrine-curation",
        "uat-verification",
        "research-synthesis",
        "regression-sweep",
        "render-rebuild",
        "engagement-coordination",
        "ratification-gate-authoring",
    ]
    dispatcher_pattern: Literal[
        "operator-inline",
        "operator-async",
        "agent-spawn-subagent",
        "scheduled-cron",
        "event-triggered",
        "gated-operator",
    ]
    tool_catalog_ref: str = Field(min_length=1, max_length=240)
    rbac_class: Literal[
        "read-only",
        "read-and-write",
        "read-write-sensitive",
        "render-only",
    ]
    status: Literal["active", "pilot", "forecasted", "retired"]
    notes: str = ""
    last_audit_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_audit_by: str = Field(min_length=1, max_length=120)
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
