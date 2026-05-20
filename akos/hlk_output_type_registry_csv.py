"""SSOT field contract for OUTPUT_TYPE_REGISTRY.csv (Initiative 86 Wave K + L).

Layer 1 of the 4-layer output architecture sitting beneath the 5-axis Holistika
Quality Fabric (per D-IH-86-BB). Names the **medium / shape** of every output
Holistika emits (prose / slide / image / voice / mermaid / gantt / excalidraw /
web / pdf / video / audio).

Canonical CSV at:
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/
    OUTPUT_TYPE_REGISTRY.csv

Mirrored to ``compliance.output_type_registry_mirror`` on Supabase via
``sync_compliance_mirrors_from_csv.py`` (Wave L mint).

Owning role: Brand & Narrative Manager (output-type doctrine governance).
Co-owning role: System Owner (validator + drift gate infrastructure).

Decision lineage:
- D-IH-86-BB (4-layer architecture mint at Wave K).
- D-IH-86-BG (Pydantic model + Supabase mirror at Wave L; this module).

Per ``CONTRIBUTING.md`` "Python Code Standards" + ``akos-holistika-operations.mdc``
"New git-canonical compliance registers": frozen BaseModel + Literal enums for
governed columns + slug regex on output_type_code.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

OUTPUT_TYPE_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "output_type_code",
    "name",
    "medium_class",
    "render_targets",
    "authoring_tool",
    "accessibility_concerns",
    "brand_visual_anchor",
    "status",
    "added_at",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)


VALID_MEDIUM_CLASSES: frozenset[str] = frozenset({
    "text",
    "visual",
    "multimedia",
    "interactive",
    "document",
})


VALID_RENDER_TARGETS: frozenset[str] = frozenset({
    "pdf",
    "web",
    "erp",
    "mail",
    "slide",
    "broadcast",
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
    "dimensions/OUTPUT_TYPE_REGISTRY.csv"
)


class OutputTypeRegistryRow(BaseModel):
    """Frozen Pydantic model for one row of OUTPUT_TYPE_REGISTRY.csv."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    output_type_code: str = Field(
        ...,
        pattern=r"^OT-[A-Z0-9][A-Z0-9-]+$",
        min_length=4,
        max_length=64,
        description="Stable slug; matches ^OT-[A-Z0-9][A-Z0-9-]+$",
    )
    name: str = Field(..., min_length=1, max_length=160)
    medium_class: Literal[
        "text",
        "visual",
        "multimedia",
        "interactive",
        "document",
    ]
    render_targets: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description=(
            "Semicolon-separated list of render-target tokens; values "
            "validated against VALID_RENDER_TARGETS at validator layer."
        ),
    )
    authoring_tool: str = Field(..., min_length=1, max_length=256)
    accessibility_concerns: str = Field(..., min_length=1, max_length=512)
    brand_visual_anchor: str = Field(..., min_length=1, max_length=512)
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
        description="ISO date YYYY-MM-DD",
    )
    last_review_by: str = Field(..., min_length=1, max_length=128)
    last_review_decision_id: str = Field(
        ...,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
        description="Foreign key into DECISION_REGISTER.csv decision_id",
    )
    methodology_version_at_review: str = Field(
        ...,
        pattern=r"^v\d+\.\d+$",
        description="Methodology version vMAJOR.MINOR per D-IH-71-D",
    )
    notes: str = Field(default="", max_length=2048)
