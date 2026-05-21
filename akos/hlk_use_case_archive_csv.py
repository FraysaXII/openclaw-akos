"""Field contract for USE_CASE_ARCHIVE.csv (Initiative 82 P4 / I86 Wave Q CSV 3).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per HOLISTIKA_CAPABILITY_DOCTRINE.md §8 "Capability lifecycle"
(Registered → Active state transition: automatic upon first USE_CASE_ARCHIVE.csv
realisation row append).

Each row records one realisation of one capability in real Holistika work —
either an external engagement (FK to ENGAGEMENT_REGISTRY) or an internal
initiative use (engagement_id empty). The archive feeds the Active → Promoted
transition (3+ realisations + Quality ≥ 4) and the audience-translation cadence
(per §7 Translatability ≥ 3 should have ≥ 1 external translation).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

USE_CASE_ARCHIVE_FIELDNAMES: tuple[str, ...] = (
    "use_case_id",
    "capability_id",
    "engagement_id",
    "realised_at",
    "realised_by",
    "outcome_summary",
    "evidence_paths",
    "audience_tags",
    "channel_tag",
    "artifact_class_id",
    "quality_self_rating",
    "lifecycle_event",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)

VALID_LIFECYCLE_EVENTS: frozenset[str] = frozenset({
    "first_realisation",
    "repeat_realisation",
    "promotion_evidence",
    "deprecation_evidence",
    "rebirth_evidence",
})

VALID_QUALITY_RATINGS: frozenset[int] = frozenset({1, 2, 3, 4, 5})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/USE_CASE_ARCHIVE.csv"
)


class UseCaseArchiveRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    use_case_id: str = Field(pattern=r"^USE-\d{4,6}$")
    capability_id: str = Field(pattern=r"^CAP-[A-Z0-9-]+$")
    engagement_id: str = ""
    realised_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    realised_by: str = Field(min_length=1, max_length=120)
    outcome_summary: str = Field(min_length=1, max_length=400)
    evidence_paths: str = ""
    audience_tags: str = ""
    channel_tag: str = ""
    artifact_class_id: str = ""
    quality_self_rating: int = Field(ge=1, le=5)
    lifecycle_event: Literal[
        "first_realisation",
        "repeat_realisation",
        "promotion_evidence",
        "deprecation_evidence",
        "rebirth_evidence",
    ]
    notes: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
