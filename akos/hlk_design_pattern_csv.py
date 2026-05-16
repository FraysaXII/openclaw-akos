"""Field contract for PEOPLE_DESIGN_PATTERN_REGISTRY.csv (Initiative 79 P2).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per `D-IH-79-D` (CSV registry home; sibling of TOPIC_REGISTRY + PROGRAM_REGISTRY +
GOI_POI_REGISTER + ENGAGEMENT_TEMPLATE_REGISTRY etc.).

Mirrored to ``compliance.people_design_pattern_registry_mirror`` on Supabase per
the pattern established by Initiative 32 P2 (skill_registry_mirror) and
Initiative 73 P1 (engagement_model_registry_mirror) — itself an instance of
``pattern_register_csv_pydantic_validator_mirror`` listed in this very registry.

PEOPLE_DESIGN_PATTERN_REGISTRY = the canonical taxonomy of consulting design
patterns People mints for other areas to inherit. Other areas author their own
processes under their own ``canonicals/`` folder and declare which People
pattern parents the row via the ``inherited_pattern_id`` FK column on
``process_list.csv`` (Initiative 79 P6 schema extension; D-IH-79-E).

Decision lineage:
- D-IH-79-A (mega scope; charter)
- D-IH-79-C (pattern library shape — both CSV registry + MD narrative paired by pattern_id)
- D-IH-79-D (CSV registry home)
- D-IH-79-E (process_list 8th col inherited_pattern_id FK)
- D-IH-79-N (anti-jargon drift gate via validate_design_pattern_registry.py --jargon-scan)

See ``PEOPLE_DESIGN_PATTERN_LIBRARY.md`` (sibling Markdown narrative) for the
human-readable companion; CSV anchor is the join key.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DESIGN_PATTERN_FIELDNAMES: tuple[str, ...] = (
    "pattern_id",
    "pattern_name",
    "pattern_class",
    "discipline_origin",
    "consumer_areas",
    "ratifying_decision_id",
    "originating_initiative_id",
    "pattern_md_anchor",
    "canonical_artifact_path",
    "acceptance_criteria_human",
    "acceptance_criteria_automation",
    "status",
    "last_review",
    "last_review_by",
    "notes",
)


VALID_PATTERN_CLASSES: frozenset[str] = frozenset({
    "register_dimension",
    "paired_sop_runbook",
    "lifecycle_taxonomy",
    "cross_area_propagation",
    "classification_lattice",
    "dual_register",
    "drift_gate",
    "inline_ratify",
    "forward_layout",
    "adapter",
    "documentation_layering",
})


VALID_DISCIPLINE_ORIGINS: frozenset[str] = frozenset({
    "compliance",
    "ethics",
    "learning",
    "people_operations",
    "cross_people",
})


VALID_CONSUMER_AREAS: frozenset[str] = frozenset({
    "marketing",
    "research",
    "techlab",
    "operations",
    "legal",
    "compliance",
    "ethics",
    "finance",
    "people",
})


VALID_STATUSES: frozenset[str] = frozenset({
    "active",
    "inactive",
    "planned",
    "deprecated",
    "experimental",
})


class DesignPatternRow(BaseModel):
    """Pydantic frozen BaseModel for one row of PEOPLE_DESIGN_PATTERN_REGISTRY.csv.

    Per CONTRIBUTING.md "Python Code Standards" and akos-holistika-operations.mdc
    "New git-canonical compliance registers": frozen BaseModel + Literal enums for
    governed columns + length bounds + slug regex on pattern_id.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    pattern_id: str = Field(
        ...,
        pattern=r"^pattern_[a-z0-9_]+$",
        min_length=10,
        max_length=96,
        description="Stable slug; matches ^pattern_[a-z0-9_]+$",
    )
    pattern_name: str = Field(..., min_length=1, max_length=160)
    pattern_class: Literal[
        "register_dimension",
        "paired_sop_runbook",
        "lifecycle_taxonomy",
        "cross_area_propagation",
        "classification_lattice",
        "dual_register",
        "drift_gate",
        "inline_ratify",
        "forward_layout",
        "adapter",
        "documentation_layering",
    ]
    discipline_origin: Literal[
        "compliance",
        "ethics",
        "learning",
        "people_operations",
        "cross_people",
    ]
    consumer_areas: str = Field(
        ...,
        min_length=1,
        max_length=256,
        description="Semicolon-separated list of consumer area tokens; values validated against VALID_CONSUMER_AREAS",
    )
    ratifying_decision_id: str = Field(
        ...,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
        description="Foreign key into DECISION_REGISTER.csv decision_id",
    )
    originating_initiative_id: str = Field(
        ...,
        pattern=r"^INIT-OPENCLAW_AKOS-\d+$",
        min_length=20,
        max_length=64,
        description="Foreign key into INITIATIVE_REGISTRY.csv initiative_id",
    )
    pattern_md_anchor: str = Field(
        ...,
        pattern=r"^#pattern-[a-z0-9-]+$",
        min_length=10,
        max_length=128,
        description="Markdown anchor in PEOPLE_DESIGN_PATTERN_LIBRARY.md; matches ^#pattern-[a-z0-9-]+$",
    )
    canonical_artifact_path: str = Field(..., min_length=1, max_length=512)
    acceptance_criteria_human: str = Field(..., min_length=1, max_length=1024)
    acceptance_criteria_automation: str = Field(..., min_length=1, max_length=1024)
    status: Literal[
        "active",
        "inactive",
        "planned",
        "deprecated",
        "experimental",
    ]
    last_review: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO date YYYY-MM-DD",
    )
    last_review_by: str = Field(..., min_length=1, max_length=128)
    notes: str = Field(default="", max_length=2048)
