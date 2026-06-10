"""Field contract for INTELLIGENCEOPS_REGISTER.csv (I72 P1 + I75 R+5 extension).

Canonical CSV:
``docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv``

Mirrored to ``compliance.intelligenceops_register_mirror`` per
``supabase/migrations/20260514240000_i72_intelligenceops_register_mirror.sql``
+ ``20260529120000_i75_intelligenceops_radar_freshness_columns.sql``.

Radar freshness columns per D-IH-86-FH (Wave R+5 C1).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from akos.hlk_research_radar import (  # noqa: F401
    INTELLIGENCEOPS_REGISTER_FIELDNAMES,
    VALID_STALENESS_POSTURES,
    VALID_VOLATILITY_CLASSES,
)

__all__ = [
    "INTELLIGENCEOPS_REGISTER_FIELDNAMES",
    "VALID_TARGET_CLASSES",
    "VALID_CADENCE",
    "VALID_SOURCE_TYPES",
    "VALID_RELIABILITY",
    "VALID_LIFECYCLE_STATUS",
    "VALID_VOLATILITY_CLASSES",
    "VALID_STALENESS_POSTURES",
    "IntelligenceOpsRegisterRow",
]

VALID_TARGET_CLASSES: frozenset[str] = frozenset({
    "regulator",
    "competitor_intelligence_target",
    "media",
    "recommendation",
})

VALID_CADENCE: frozenset[str] = frozenset({
    "on_demand",
    "scheduled",
    "event_triggered",
    "gated_operator",
})

VALID_SOURCE_TYPES: frozenset[str] = frozenset({
    "OSINT",
    "HUMINT",
    "SIGINT",
    "CORPINT",
    "MOTINT",
    "TBD",
})

VALID_RELIABILITY: frozenset[str] = frozenset({
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
})

VALID_LIFECYCLE_STATUS: frozenset[str] = frozenset({
    "active",
    "scaffold",
    "deprecated",
})

# Back-compat aliases for ``scripts/validate_intelligenceops_register.py``.
VALID_CADENCES = VALID_CADENCE
VALID_LIFECYCLE_STATUSES = VALID_LIFECYCLE_STATUS
VALID_RELIABILITY_GRADES = VALID_RELIABILITY


class IntelligenceOpsRegisterRow(BaseModel):
    """One INTELLIGENCEOPS_REGISTER row including radar freshness columns."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    register_id: str = Field(min_length=1, max_length=80)
    target_id: str = Field(min_length=1, max_length=120)
    target_class: str
    cadence: str
    source_type: str
    reliability: str
    output_artifact: str = ""
    responsible_role: str
    lifecycle_status: Literal["active", "scaffold", "deprecated"]
    intro_decision_id: str = ""
    linked_sop_path: str = ""
    linked_runbook_path: str = ""
    notes: str = ""
    last_review_at: str = ""
    last_review_by: str = ""
    last_review_decision_id: str = ""
    methodology_version_at_review: str = ""
    volatility_class: str = ""
    staleness_days: str = ""
    staleness_posture: str = ""
    next_verify_by: str = ""

    @model_validator(mode="after")
    def _validate_enums(self) -> IntelligenceOpsRegisterRow:
        if self.target_class not in VALID_TARGET_CLASSES:
            raise ValueError(f"invalid target_class: {self.target_class}")
        if self.cadence not in VALID_CADENCE:
            raise ValueError(f"invalid cadence: {self.cadence}")
        if self.source_type not in VALID_SOURCE_TYPES:
            raise ValueError(f"invalid source_type: {self.source_type}")
        if self.reliability not in VALID_RELIABILITY:
            raise ValueError(f"invalid reliability: {self.reliability}")
        if self.volatility_class and self.volatility_class not in VALID_VOLATILITY_CLASSES:
            raise ValueError(f"invalid volatility_class: {self.volatility_class}")
        if self.staleness_posture and self.staleness_posture not in VALID_STALENESS_POSTURES:
            raise ValueError(f"invalid staleness_posture: {self.staleness_posture}")
        return self
