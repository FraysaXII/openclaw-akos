"""Field contract for AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv (I86 Wave R / OPS-86-11).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/``
per akos-holistika-operations.mdc §"New git-canonical compliance registers".

Each row is one (capability_id × aic_id) cell — declares whether a given AIC
can implement a given capability, via which approach, at which maturity. The
matrix is the operational join surface between:

- CAPABILITY_REGISTRY.csv (1092 rows; the capability domain per I82 P4)
- AIC_REGISTRY.csv (5 rows; the AIC instance domain per Wave Q D-IH-82-S)
- USE_CASE_ARCHIVE.csv (realisation evidence per Wave Q D-IH-82-R)
- MADEIRA_AIC_PER_TASK_REGISTRY.csv (per-task dispatcher bindings; optional FK
  for MADEIRA-class AICs)

Per D-IH-86-CH operator ratification (scratchpad 2026-05-21 21:23): the matrix
is the SSOT for "which AIC can do what" — agentic capability planning,
operator dispatcher choice, and capability-gap surfacing all read from here.

Mint decision: D-IH-86-CQ (Wave R Lane A; agent-authorable per operator
inline-ratify gate 2026-05-22 selecting Lane A from 4-option Wave R lane
batch).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv"
)


AIC_CAPABILITY_IMPLEMENTATION_MATRIX_FIELDNAMES: tuple[str, ...] = (
    "matrix_id",
    "capability_id",
    "aic_id",
    "implementation_status",
    "approach_summary",
    "tool_catalog_ref",
    "realisation_refs",
    "paired_madeira_task_id",
    "confidence_class",
    "notes",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
)


VALID_IMPLEMENTATION_STATUSES: frozenset[str] = frozenset(
    {
        "implemented",
        "pilot",
        "forecasted",
        "not-applicable",
        "blocked",
    }
)


VALID_CONFIDENCE_CLASSES: frozenset[str] = frozenset(
    {
        "confirmed",
        "inferred",
        "pre-ratified",
        "experimental",
    }
)


class AICCapabilityImplementationMatrixRow(BaseModel):
    """One (capability_id × aic_id) cell of the implementation matrix."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    matrix_id: str = Field(
        pattern=r"^ACIM-\d{4,6}$", min_length=9, max_length=11
    )
    capability_id: str = Field(
        pattern=r"^CAP-[A-Z0-9-]+$", min_length=5, max_length=120
    )
    aic_id: str = Field(
        pattern=r"^AIC-[A-Z0-9-]+$", min_length=5, max_length=80
    )
    implementation_status: Literal[
        "implemented",
        "pilot",
        "forecasted",
        "not-applicable",
        "blocked",
    ]
    approach_summary: str = Field(min_length=1, max_length=400)
    tool_catalog_ref: str = ""
    realisation_refs: str = ""
    paired_madeira_task_id: str = ""
    confidence_class: Literal[
        "confirmed",
        "inferred",
        "pre-ratified",
        "experimental",
    ]
    notes: str = ""
    last_review_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
