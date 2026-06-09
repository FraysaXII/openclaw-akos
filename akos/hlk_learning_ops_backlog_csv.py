"""Field contract for LEARNING_OPS_BACKLOG.csv (People/Learning; I73 P2 / P95-GOV-4).

Canonical CSV at
``docs/references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/dimensions/LEARNING_OPS_BACKLOG.csv``.
Git-only SSOT; cohort rows FK to ``ENGAGEMENT_MODEL_REGISTRY.csv`` per D-IH-73-K.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

LEARNING_OPS_BACKLOG_FIELDNAMES: tuple[str, ...] = (
    "cohort_id",
    "engagement_model_id",
    "methodology_version_at_onboarding",
    "start_date",
    "status",
    "notes",
)

CANONICAL_PATH = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Learning/canonicals/dimensions/"
    "LEARNING_OPS_BACKLOG.csv"
)

COHORT_ID_RE = re.compile(r"^cohort_[a-z0-9_]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

VALID_BACKLOG_STATUSES: frozenset[str] = frozenset({
    "planned",
    "active",
    "completed",
    "cancelled",
})


class LearningOpsBacklogRow(BaseModel):
    """Pydantic model for one row of LEARNING_OPS_BACKLOG.csv."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    cohort_id: str
    engagement_model_id: str
    methodology_version_at_onboarding: str = Field(min_length=1, max_length=80)
    start_date: str
    status: Literal["planned", "active", "completed", "cancelled"]
    notes: str = Field(default="", max_length=400)

    @field_validator("cohort_id")
    @classmethod
    def cohort_id_shape(cls, value: str) -> str:
        if not COHORT_ID_RE.match(value):
            raise ValueError("cohort_id must match cohort_<slug>")
        return value

    @field_validator("engagement_model_id")
    @classmethod
    def engagement_model_slug(cls, value: str) -> str:
        if not value.startswith("eng_model_"):
            raise ValueError("engagement_model_id must start with eng_model_")
        return value

    @field_validator("start_date")
    @classmethod
    def start_date_shape(cls, value: str) -> str:
        if not DATE_RE.match(value):
            raise ValueError("start_date must be YYYY-MM-DD")
        return value
