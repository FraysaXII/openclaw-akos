"""SSOT field contract for ARTIFACT_CLASS_REGISTRY.csv (Initiative 86 Wave K + L).

Layer 2 of the 4-layer output architecture beneath the 5-axis Holistika Quality
Fabric (per D-IH-86-BB). Names the **named purpose** of every output Holistika
emits (dossier / cover-email / intro-message / decks / UAT-report / SOP / etc).

Canonical CSV at:
    docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/
    ARTIFACT_CLASS_REGISTRY.csv

Mirrored to ``compliance.artifact_class_registry_mirror`` on Supabase via
``sync_compliance_mirrors_from_csv.py`` (Wave L mint).

Owning role: Brand & Narrative Manager.
Co-owning role: System Owner.

Decision lineage:
- D-IH-86-BB (4-layer architecture mint at Wave K).
- D-IH-86-BG (Pydantic model + Supabase mirror at Wave L; this module).

Cross-FK references:
- ``output_type_codes`` semicolon-list FK-resolves into OUTPUT_TYPE_REGISTRY.csv
  (one artifact class can be rendered as multiple output types).
- ``typical_audience_codes`` semicolon-list FK-resolves into AUDIENCE_REGISTRY.csv.
- ``typical_channel_codes`` semicolon-list FK-resolves into
  CHANNEL_TOUCHPOINT_REGISTRY.csv (or ``broadcast`` shorthand for non-tagged).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ARTIFACT_CLASS_REGISTRY_FIELDNAMES: tuple[str, ...] = (
    "artifact_class_code",
    "name",
    "output_type_codes",
    "typical_audience_codes",
    "typical_channel_codes",
    "render_script_path",
    "exemplar_path",
    "doctrine_owner_role",
    "quality_fabric_invocation",
    "status",
    "added_at",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)


VALID_STATUSES: frozenset[str] = frozenset({
    "active",
    "inactive",
    "planned",
    "deprecated",
    "experimental",
})


CANONICAL_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/ARTIFACT_CLASS_REGISTRY.csv"
)


class ArtifactClassRegistryRow(BaseModel):
    """Frozen Pydantic model for one row of ARTIFACT_CLASS_REGISTRY.csv."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    artifact_class_code: str = Field(
        ...,
        pattern=r"^AC-[A-Z0-9][A-Z0-9-]+$",
        min_length=4,
        max_length=64,
        description="Stable slug; matches ^AC-[A-Z0-9][A-Z0-9-]+$",
    )
    name: str = Field(..., min_length=1, max_length=200)
    output_type_codes: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Semicolon-list of OUTPUT_TYPE_REGISTRY.output_type_code values; "
            "FK-resolved at validator layer."
        ),
    )
    typical_audience_codes: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description=(
            "Semicolon-list of AUDIENCE_REGISTRY.audience_code values; "
            "FK-resolved at validator layer."
        ),
    )
    typical_channel_codes: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description=(
            "Semicolon-list of CHANNEL_TOUCHPOINT_REGISTRY.channel_code values "
            "(or short-form tokens for non-canonical channels)."
        ),
    )
    render_script_path: str = Field(
        default="",
        max_length=1024,
        description=(
            "Semicolon-list of relative paths to render scripts (scripts/render_*.py "
            "or scripts/export_*.py). Empty for purely-authored artifacts (markdown SSOT)."
        ),
    )
    exemplar_path: str = Field(
        default="",
        max_length=1024,
        description=(
            "Semicolon-list of relative paths to one or more exemplar artifacts "
            "(rendered or authored). Operator can open these to see the artifact class shape."
        ),
    )
    doctrine_owner_role: str = Field(..., min_length=1, max_length=128)
    quality_fabric_invocation: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Quality fabric compose() invocation pattern per "
            "HOLISTIKA_QUALITY_FABRIC.md. Names the audience x channel x scenario "
            "x brand x governance composition the artifact class invokes."
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
        description="ISO date YYYY-MM-DD",
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
