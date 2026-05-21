"""Field contract for AIC_REGISTRY.csv (Initiative 82 P4 / I86 Wave Q CSV 4 parent).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per HOLISTIKA_AGENTIC_DOCTRINE.md (the AIC = AI Collaborator role-class) +
SUBSTRATE_LANDSCAPE_DOCTRINE.md (the substrates AICs run on; FK substrate_id).

Each row registers one AI Collaborator (AIC) instance — the concrete pairing
of an agent-class role with a runtime substrate. Madeira (current AI O5-1)
appears as multiple rows when the same role-class runs on multiple substrates
(e.g., Madeira-on-Cursor vs Madeira-on-OpenClaw vs Madeira-on-Cursor-SDK).

Per akos-people-discipline-of-disciplines.mdc RULE 5: "Madeira named-explicit,
role-class anchored." AIC_REGISTRY makes the role-class vs embodiment
distinction mechanical: aic_id names the embodiment; role_owner_class names
the role-class.

Pulled into Wave Q from Wave R per D-IH-82-S coordination resolution
(MADEIRA_AIC_PER_TASK_REGISTRY needs AIC_REGISTRY as parent FK; pull-forward
avoids minting child before parent).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AIC_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "aic_id",
    "aic_name",
    "substrate_id",
    "runtime_instance",
    "role_owner_class",
    "parent_doctrine_canonical",
    "status",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)


VALID_STATUSES: frozenset[str] = frozenset(
    {
        "active",
        "pilot",
        "forecasted",
        "retired",
    }
)


CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/AIC_REGISTRY.csv"
)


VALID_ROLE_OWNER_CLASSES: frozenset[str] = frozenset(
    {
        "ai-o5-1",
        "ai-collaborator",
        "ai-product-agent",
        "ai-supervisor",
        "ai-peer",
        "ai-dispatcher",
    }
)


class AICRegistryRow(BaseModel):
    """One AIC = (role-class x substrate x runtime instance) instance."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    aic_id: str = Field(pattern=r"^AIC-[A-Z0-9-]+$", min_length=5, max_length=80)
    aic_name: str = Field(min_length=1, max_length=160)
    substrate_id: str = Field(pattern=r"^SUBS-[A-Z0-9-]+$", min_length=6, max_length=80)
    runtime_instance: str = Field(min_length=1, max_length=160)
    role_owner_class: Literal[
        "ai-o5-1",
        "ai-collaborator",
        "ai-product-agent",
        "ai-supervisor",
        "ai-peer",
        "ai-dispatcher",
    ]
    parent_doctrine_canonical: str = Field(min_length=1, max_length=240)
    status: Literal["active", "pilot", "forecasted", "retired"]
    notes: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
