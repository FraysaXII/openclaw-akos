"""SSOT field contract for COMPONENT_PRIMITIVE_REGISTRY.csv (Initiative 86 Wave K + L).

Layer 3 of the 4-layer output architecture beneath the 5-axis Holistika Quality
Fabric (per D-IH-86-BB). Names the **Shadcn-shape granular primitives** that
compose every Holistika output (greeting / hook / body / CTA / signature /
slide-hero / slide-compare / mermaid-flowchart / mermaid-gantt / data-table /
form-field / dashboard-card / navbar / sidebar / empty-state / loading-state /
error-state / evidence-block / methodology-note / confidentiality-block /
cover-page / executive-summary / context-anchor / slide-progress / slide-appendix).

Canonical CSV at:
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/
    COMPONENT_PRIMITIVE_REGISTRY.csv

Mirrored to ``compliance.component_primitive_registry_mirror`` on Supabase via
``sync_compliance_mirrors_from_csv.py`` (Wave L mint).

Owning role: Brand & Narrative Manager.
Co-owning role: System Owner.

Decision lineage:
- D-IH-86-BB (4-layer architecture mint at Wave K).
- D-IH-86-BG (Pydantic model + Supabase mirror at Wave L; this module).

Cross-FK references:
- ``parent_artifact_class_codes`` semicolon-list FK-resolves into
  ARTIFACT_CLASS_REGISTRY.csv (each primitive declares which artifact classes
  consume it; many-to-many).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

COMPONENT_PRIMITIVE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "component_primitive_code",
    "name",
    "kind",
    "parent_artifact_class_codes",
    "research_dimensions",
    "a11y_dimensions",
    "brand_dimensions",
    "doctrine_path",
    "status",
    "added_at",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)


VALID_KINDS: frozenset[str] = frozenset({
    "prose",
    "visual",
    "interactive",
    "mixed",
})


VALID_STATUSES: frozenset[str] = frozenset({
    "active",
    "inactive",
    "planned",
    "deprecated",
    "experimental",
})


CANONICAL_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/COMPONENT_PRIMITIVE_REGISTRY.csv"
)


class ComponentPrimitiveRegistryRow(BaseModel):
    """Frozen Pydantic model for one row of COMPONENT_PRIMITIVE_REGISTRY.csv."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    component_primitive_code: str = Field(
        ...,
        pattern=r"^CP-[A-Z0-9][A-Z0-9-]+$",
        min_length=4,
        max_length=80,
        description="Stable slug; matches ^CP-[A-Z0-9][A-Z0-9-]+$",
    )
    name: str = Field(..., min_length=1, max_length=200)
    kind: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description=(
            "Semicolon-separated list of kind tokens; values validated against "
            "VALID_KINDS at validator layer. Multi-kind primitives are common "
            "(e.g., evidence-block = prose;visual; data-table = visual;interactive)."
        ),
    )
    parent_artifact_class_codes: str = Field(
        ...,
        min_length=1,
        max_length=1024,
        description=(
            "Semicolon-list of ARTIFACT_CLASS_REGISTRY.artifact_class_code values; "
            "FK-resolved at validator layer."
        ),
    )
    research_dimensions: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Semicolon-list of research dimensions the primitive bears on "
            "(e.g., reading-level / length-budget / pattern-match-vs-novel)."
        ),
    )
    a11y_dimensions: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Semicolon-list of accessibility dimensions (e.g., reading-order / "
            "contrast / screen-reader-semantics)."
        ),
    )
    brand_dimensions: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Semicolon-list of brand dimensions (e.g., voice-register / "
            "type-scale / color-palette)."
        ),
    )
    doctrine_path: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Path + anchor to the primitive's doctrine page in "
            "COMPONENT_PRIMITIVE_LIBRARY.md (or '(forward)' if the page is "
            "not yet authored to worked-exemplar parity)."
        ),
    )
    status: Literal[
        "active",
        "inactive",
        "planned",
        "deprecated",
        "experimental",
    ]
    added_at: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO date YYYY-MM-DD",
    )
    last_review_at: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )
    last_review_by: str = Field(..., min_length=1, max_length=128)
    last_review_decision_id: str = Field(
        ...,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
    )
    methodology_version_at_review: str = Field(
        ...,
        pattern=r"^v\d+\.\d+$",
    )
    notes: str = Field(default="", max_length=2048)
