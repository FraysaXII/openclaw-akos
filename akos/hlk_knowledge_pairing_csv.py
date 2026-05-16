"""Field contract for KNOWLEDGE_PAIRING_REGISTRY.csv (Initiative 80 P6.5).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per `D-IH-80-H` (CSV registry home; sibling of PEOPLE_DESIGN_PATTERN_REGISTRY +
TOPIC_REGISTRY + ENGAGEMENT_REGISTRY etc.).

Purpose: register every paired-file / index-entry / doctrine-companion
relationship in the AKOS canonical vault. Operationalises the operator's
2026-05-16 framing that the SOP body/addendum doctrine (minted at I80 P1) +
indices + supporting documentation form a *graph of relationships* that DAMA,
SSOT, mirroring, hlk-erp panels, and the future AI Archivist / KiRBe ingestor
all depend on.

Mirrored to ``compliance.knowledge_pairing_registry_mirror`` on Supabase per
the pattern_register_csv_pydantic_validator_mirror established by Initiative
32 P2 (skill_registry_mirror). The mirror is consumed by hlk-erp Knowledge
panels and (forward) by the AI Archivist / KiRBe ingestor (I83 candidate).

Decision lineage:
- D-IH-80-A (mega-charter scope; charter)
- D-IH-80-B (SOP body/addendum paired-file default for DAMA-readiness)
- D-IH-80-F (anti-jargon drift gate *.addendum.md glob exclusion)
- D-IH-80-H (KNOWLEDGE_PAIRING_REGISTRY.csv mint at I80 P6.5; first instance
  of the documentation-relationship registry pattern; forward-charters to
  per-area registries when other areas mint paired patterns of their own)

This is the People-area instantiation; other areas may mint sibling registries
(e.g., Tech ``CODE_DOC_PAIRING_REGISTRY.csv``) following the same shape if
they need their own per-area governance. The People canonical is the SSOT for
the *pattern* — sibling registries inherit the contract.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

KNOWLEDGE_PAIRING_FIELDNAMES: tuple[str, ...] = (
    "pairing_id",
    "pairing_class",
    "parent_doc_path",
    "companion_doc_paths",
    "area",
    "pattern_id",
    "authority",
    "mirror_ready",
    "hlk_erp_panel_ready",
    "ai_archivist_ready",
    "status",
    "last_review",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)


VALID_PAIRING_CLASSES: frozenset[str] = frozenset({
    "sop_addendum_split",
    "sop_runbook",
    "index_entries",
    "doctrine_companion",
    "charter_phases",
    "addendum_chain",
    "registry_narrative",
})

VALID_AREAS: frozenset[str] = frozenset({
    "Admin",
    "Tech",
    "People",
    "Marketing",
    "Operations",
    "Research",
    "Finance",
    "Legal",
})

VALID_AUTHORITIES: frozenset[str] = frozenset({
    "parent",
    "companion",
    "co_authoritative",
})

VALID_READINESS_STATES: frozenset[str] = frozenset({
    "yes",
    "no",
    "partial",
    "planned",
    "n_a",
})


class KnowledgePairingRow(BaseModel):
    """Pydantic schema for a single KNOWLEDGE_PAIRING_REGISTRY.csv row.

    Validation rules (per `D-IH-80-H`):
    - ``pairing_id`` follows ``pair_<purpose>_<NNN>`` slug shape; lowercase + underscores; length <= 80.
    - ``pairing_class`` is in ``VALID_PAIRING_CLASSES`` (extensible enum; new classes need a D-IH-NN-* decision).
    - ``parent_doc_path`` is a workspace-relative path with forward slashes; ends with ``.md`` or ``.csv``.
    - ``companion_doc_paths`` is a semicolon-separated list of workspace-relative paths; each non-empty.
    - ``area`` is in ``VALID_AREAS`` (matches ``baseline_organisation.csv`` area enum).
    - ``pattern_id`` is FK to ``PEOPLE_DESIGN_PATTERN_REGISTRY.csv`` (resolved at validator runtime; not enforced here).
    - ``authority`` is in ``VALID_AUTHORITIES``.
    - ``mirror_ready`` / ``hlk_erp_panel_ready`` / ``ai_archivist_ready`` are in ``VALID_READINESS_STATES``.
    - ``status`` is in {active, deprecated, draft}.
    - ``last_review`` ISO-8601 date; ``last_review_by`` non-empty role name.
    - ``methodology_version_at_review`` matches ``vN.N`` shape.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pairing_id: str = Field(..., min_length=1, max_length=80)
    pairing_class: Literal[
        "sop_addendum_split",
        "sop_runbook",
        "index_entries",
        "doctrine_companion",
        "charter_phases",
        "addendum_chain",
        "registry_narrative",
    ]
    parent_doc_path: str = Field(..., min_length=1)
    companion_doc_paths: str = Field(..., min_length=1)
    area: Literal[
        "Admin",
        "Tech",
        "People",
        "Marketing",
        "Operations",
        "Research",
        "Finance",
        "Legal",
    ]
    pattern_id: str = Field(..., min_length=1)
    authority: Literal["parent", "companion", "co_authoritative"]
    mirror_ready: Literal["yes", "no", "partial", "planned", "n_a"]
    hlk_erp_panel_ready: Literal["yes", "no", "partial", "planned", "n_a"]
    ai_archivist_ready: Literal["yes", "no", "partial", "planned", "n_a"]
    status: Literal["active", "deprecated", "draft"]
    last_review: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(..., min_length=1)
    last_review_decision_id: str = Field(..., min_length=1)
    methodology_version_at_review: str = Field(..., pattern=r"^v\d+\.\d+$")
    notes: str = Field(default="")
