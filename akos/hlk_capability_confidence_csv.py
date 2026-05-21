"""Field contract for CAPABILITY_CONFIDENCE_REGISTRY.csv (Initiative 82 P3 / I86 Wave Q CSV 2).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per HOLISTIKA_CAPABILITY_DOCTRINE.md §6 (5-dimension confidence taxonomy:
Substrate / Repeatability / Quality / Translatability / Auditability, each 1-5)
+ D-IH-82-Q (Wave Q CSV 2 seed-posture: all 1092 capabilities seeded at
``rating_method=seed_v1_unrated`` with all scores = 1 + aggregate = 1.0
pending P3 quarterly review by Capability Curator).

Conundrum C-82-2 (confidence naming: SCP-cameo vs numbers vs plain) auto-defaults
to numeric-v1 at v1 (doctrine-anchored); SCP-cameo + plain-register addendum
stubs forward-chartered to I82 P3 Marketing/Brand co-sign.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CAPABILITY_CONFIDENCE_FIELDNAMES: tuple[str, ...] = (
    "confidence_id",
    "capability_id",
    "substrate_score",
    "repeatability_score",
    "quality_score",
    "translatability_score",
    "auditability_score",
    "aggregate_confidence",
    "rating_method",
    "rated_at",
    "rated_by",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)

VALID_SCORES: frozenset[int] = frozenset({1, 2, 3, 4, 5})

VALID_RATING_METHODS: frozenset[str] = frozenset({
    "seed_v1_unrated",
    "numeric_v1",
    "scp_cameo_pending",
    "plain_register_pending",
    "operator_ratified_v1",
})

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/CAPABILITY_CONFIDENCE_REGISTRY.csv"
)


class CapabilityConfidenceRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    confidence_id: str = Field(pattern=r"^CONF-CAP-[A-Z0-9-]+-\d{8}$")
    capability_id: str = Field(pattern=r"^CAP-[A-Z0-9-]+$")
    substrate_score: int = Field(ge=1, le=5)
    repeatability_score: int = Field(ge=1, le=5)
    quality_score: int = Field(ge=1, le=5)
    translatability_score: int = Field(ge=1, le=5)
    auditability_score: int = Field(ge=1, le=5)
    aggregate_confidence: float = Field(ge=1.0, le=5.0)
    rating_method: Literal[
        "seed_v1_unrated",
        "numeric_v1",
        "scp_cameo_pending",
        "plain_register_pending",
        "operator_ratified_v1",
    ]
    rated_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    rated_by: str = Field(min_length=1, max_length=120)
    notes: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)

    @model_validator(mode="after")
    def _aggregate_matches_mean(self) -> "CapabilityConfidenceRow":
        mean = (
            self.substrate_score
            + self.repeatability_score
            + self.quality_score
            + self.translatability_score
            + self.auditability_score
        ) / 5.0
        expected = round(mean, 1)
        if abs(self.aggregate_confidence - expected) > 0.05:
            raise ValueError(
                f"aggregate_confidence={self.aggregate_confidence} does not match "
                f"computed mean={expected} (per HOLISTIKA_CAPABILITY_DOCTRINE.md §6)"
            )
        return self
