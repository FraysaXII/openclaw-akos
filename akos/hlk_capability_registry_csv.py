"""Field contract for CAPABILITY_REGISTRY.csv (Initiative 82 P2 / I86 Wave Q).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per HOLISTIKA_CAPABILITY_DOCTRINE.md + D-IH-82-P (Wave Q seed from I81 matrix).

Each row maps one executable ``process_list.csv`` item to an audience-surfaceable
capability with bearer-class grounding (Talent-H / Talent-A per doctrine §4).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CAPABILITY_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "capability_id",
    "capability_name",
    "bearer_class",
    "area",
    "role_owner",
    "originating_process_ids",
    "substrate_id",
    "skill_ids",
    "lifecycle_status",
    "i81_verdict",
    "i81_gap_summary",
    "external_register_summary",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)

VALID_BEARER_CLASSES: frozenset[str] = frozenset({"Talent-H", "Talent-A"})

VALID_LIFECYCLE_STATUSES: frozenset[str] = frozenset({
    "active",
    "planned",
    "deprecated",
    "scaffold",
})

VALID_I81_VERDICTS: frozenset[str] = frozenset({"pass", "partial", "fail"})

TALENT_A_ROLE_HINTS: frozenset[str] = frozenset({
    "Talent Slot — MADEIRA",
    "Talent Slot - MADEIRA",
    "AIC",
    "AI Engineer",
    "System Owner",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/CAPABILITY_REGISTRY.csv"
)


class CapabilityRegistryRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    capability_id: str = Field(pattern=r"^CAP-[A-Z0-9-]+$")
    capability_name: str = Field(min_length=1, max_length=200)
    bearer_class: Literal["Talent-H", "Talent-A"]
    area: str = Field(min_length=1, max_length=32)
    role_owner: str = Field(min_length=1, max_length=120)
    originating_process_ids: str = Field(min_length=1, max_length=120)
    substrate_id: str = ""
    skill_ids: str = ""
    lifecycle_status: Literal["active", "planned", "deprecated", "scaffold"]
    i81_verdict: Literal["pass", "partial", "fail"]
    i81_gap_summary: str = ""
    external_register_summary: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = ""
