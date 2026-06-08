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
    # bearer_class REMOVED at D-IH-95-I: de-densified capabilities are bearer-agnostic — the
    # bearer (Talent-H human role vs Talent-A AIC) is derived from the realizing process's owner.
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
    "capability_tier",  # D-IH-95-H — differentiating | utility (empty until the area-by-area collapse curates it); drives rating cadence + the gold-layer heat map
    "l1_domain",        # D-IH-95-I — the ~9-domain grouping (capability area stays the HLK area; l1_domain is the cross-area capability-map grouping)
    "definition",       # D-IH-95-I — 1-sentence stable-capability definition (the sellable "what")
)

VALID_BEARER_CLASSES: frozenset[str] = frozenset({"Talent-H", "Talent-A"})

# D-IH-95-H: value-tier overlay (differentiating vs utility) for the de-densified map.
# Empty allowed pre-collapse; the area-by-area collapse + Capability Curator set it.
VALID_CAPABILITY_TIERS: frozenset[str] = frozenset({"", "differentiating", "utility"})

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
    area: str = Field(min_length=1, max_length=32)
    role_owner: str = Field(min_length=1, max_length=120)
    # N:N at D-IH-95-I — a de-densified capability is realized by many processes (semicolon list).
    originating_process_ids: str = Field(min_length=1, max_length=800)
    substrate_id: str = ""
    skill_ids: str = ""
    lifecycle_status: Literal["active", "planned", "deprecated", "scaffold"]
    # "" allowed at D-IH-95-I — i81 seed-audit verdict is legacy seed metadata; de-densified
    # capabilities are not I81-seed-derived, so they carry an empty verdict.
    i81_verdict: Literal["", "pass", "partial", "fail"] = ""
    i81_gap_summary: str = ""
    external_register_summary: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = ""
    capability_tier: Literal["", "differentiating", "utility"] = ""
    l1_domain: str = Field(default="", max_length=80)
    definition: str = Field(default="", max_length=400)
