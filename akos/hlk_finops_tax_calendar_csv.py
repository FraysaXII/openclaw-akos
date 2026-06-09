"""Field contract for FINOPS_TAX_CALENDAR.csv (FINANCE-AREA-FULL F2b).

Canonical CSV lives under
``docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/dimensions/``
per FINOPS_DISCIPLINE plane 3 (OPS-81-13).

Rows declare **filing obligations** and cadence rules — not production monetary
amounts. Entity-specific ``next_due_at`` values are counsel / gestoría confirmed
per D-IH-81-P internal-first posture.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

FINOPS_TAX_CALENDAR_FIELDNAMES: tuple[str, ...] = (
    "obligation_id",
    "modelo_code",
    "obligation_name",
    "cadence_type",
    "cadence_rule",
    "hacienda_authority",
    "applicability_gate",
    "responsible_role",
    "executor_party",
    "paired_sop_path",
    "paired_runbook_path",
    "last_filed_at",
    "next_due_at",
    "source_ref",
    "status",
    "last_review_at",
    "last_review_by",
    "last_review_decision_id",
    "methodology_version_at_review",
    "notes",
)

CSV_PATH_RELATIVE: str = (
    "docs/references/hlk/v3.0/Admin/O5-1/Finance/Governance/canonicals/"
    "dimensions/FINOPS_TAX_CALENDAR.csv"
)

_DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

VALID_TAX_CALENDAR_CADENCE_TYPES: frozenset[str] = frozenset({
    "monthly", "quarterly", "annual", "event_triggered", "on_demand",
})
VALID_HACIENDA_AUTHORITIES: frozenset[str] = frozenset({"AEAT_common", "foral_deferred"})
VALID_APPLICABILITY_GATES: frozenset[str] = frozenset({
    "always", "at_incorporation", "if_autonomo_path", "if_foreign_assets_gt_50k_eur", "post_first_fiscal_year",
})
VALID_TAX_CALENDAR_STATUSES: frozenset[str] = frozenset({"active", "draft", "not_applicable_yet"})


class FinopsTaxCalendarRow(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    obligation_id: str = Field(pattern=r"^TAX-FIN-HOL-[A-Z0-9-]+$")
    modelo_code: str = Field(min_length=1, max_length=32)
    obligation_name: str = Field(min_length=1, max_length=200)
    cadence_type: Literal[
        "monthly",
        "quarterly",
        "annual",
        "event_triggered",
        "on_demand",
    ]
    cadence_rule: str = Field(min_length=1, max_length=512)
    hacienda_authority: Literal["AEAT_common", "foral_deferred"]
    applicability_gate: Literal[
        "always",
        "at_incorporation",
        "if_autonomo_path",
        "if_foreign_assets_gt_50k_eur",
        "post_first_fiscal_year",
    ]
    responsible_role: str = Field(min_length=1, max_length=120)
    executor_party: str = Field(min_length=1, max_length=120)
    paired_sop_path: str = Field(default="", max_length=512)
    paired_runbook_path: str = Field(default="", max_length=512)
    last_filed_at: str = Field(default="", max_length=16)
    next_due_at: str = Field(default="", max_length=16)
    source_ref: str = Field(min_length=1, max_length=512)
    status: Literal["active", "draft", "not_applicable_yet"]
    last_review_at: str = Field(pattern=_DATE_PATTERN)
    last_review_by: str = Field(min_length=1, max_length=120)
    last_review_decision_id: str = Field(min_length=1, max_length=32)
    methodology_version_at_review: str = Field(min_length=1, max_length=16)
    notes: str = Field(default="", max_length=2000)

    @field_validator("last_filed_at", "next_due_at")
    @classmethod
    def _optional_date(cls, value: str) -> str:
        if not value:
            return value
        import re

        if not re.fullmatch(_DATE_PATTERN, value):
            raise ValueError("must be empty or YYYY-MM-DD")
        return value
