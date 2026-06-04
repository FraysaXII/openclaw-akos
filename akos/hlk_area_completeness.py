"""Pydantic SSOT models for area-completeness sweeps (I93 P0 mint).

Canonical doctrine:
``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md``
Paired runbook: ``scripts/validate_area_completeness.py``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md``
Companion cursor rule: ``.cursor/rules/akos-area-governance.mdc``
Decision lineage: D-IH-93-B (People area-governance meta-process).

The 14-component bar (AREA-01..AREA-14) is the harmonization SSOT for
``compose_AREA(governance)`` — the 17th Quality Fabric specialty.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AREA_COMPLETENESS_FINDING_FIELDNAMES: tuple[str, ...] = (
    "component_code",
    "area",
    "verdict",
    "evidence_summary",
    "proposed_action",
    "severity",
    "notes",
)

AREA_COMPLETENESS_REPORT_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "sweep_trigger",
    "swept_at",
    "swept_by",
    "findings",
    "pass_count",
    "partial_count",
    "gap_count",
    "blocked_count",
    "skip_count",
    "total_findings",
)

VALID_AREA_COMPONENT_CODES: frozenset[str] = frozenset({
    "AREA-01-PARENT-REDESIGN",
    "AREA-02-AREA-CHARTER",
    "AREA-03-DISCIPLINE-CHARTERS",
    "AREA-04-PROCESS-LIST",
    "AREA-05-BASELINE-ROLES",
    "AREA-06-CAPABILITY-CONFIDENCE",
    "AREA-07-CANONICAL-PRECEDENCE",
    "AREA-08-DIMENSION-REGISTRIES",
    "AREA-09-PAIRED-SOP-RUNBOOK",
    "AREA-10-SUPABASE-MIRRORS",
    "AREA-11-CURSOR-RULE-SKILL",
    "AREA-12-QUALITY-FABRIC",
    "AREA-13-AREA-README",
    "AREA-14-INHERITED-PATTERN",
})

VALID_AREA_VERDICTS: frozenset[str] = frozenset({
    "pass",
    "partial",
    "gap",
    "blocked",
    "skip",
})

VALID_AREA_SEVERITIES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})

VALID_AREA_SWEEP_TRIGGERS: frozenset[str] = frozenset({
    "on_demand",
    "area_buildout",
    "pre_commit_self_test",
})

VALID_SCORED_AREAS: frozenset[str] = frozenset({
    "Data",
    "Tech",
    "Finance",
    "Marketing",
    "Operations",
    "People",
    "Research",
})


class AreaCompletenessFindingRow(BaseModel):
    """One component probe result for one O5-1 area."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    component_code: Literal[
        "AREA-01-PARENT-REDESIGN",
        "AREA-02-AREA-CHARTER",
        "AREA-03-DISCIPLINE-CHARTERS",
        "AREA-04-PROCESS-LIST",
        "AREA-05-BASELINE-ROLES",
        "AREA-06-CAPABILITY-CONFIDENCE",
        "AREA-07-CANONICAL-PRECEDENCE",
        "AREA-08-DIMENSION-REGISTRIES",
        "AREA-09-PAIRED-SOP-RUNBOOK",
        "AREA-10-SUPABASE-MIRRORS",
        "AREA-11-CURSOR-RULE-SKILL",
        "AREA-12-QUALITY-FABRIC",
        "AREA-13-AREA-README",
        "AREA-14-INHERITED-PATTERN",
    ]
    area: Literal[
        "Data",
        "Tech",
        "Finance",
        "Marketing",
        "Operations",
        "People",
        "Research",
    ]
    verdict: Literal["pass", "partial", "gap", "blocked", "skip"]
    evidence_summary: str = Field(default="", max_length=1024)
    proposed_action: str = Field(default="", max_length=1024)
    severity: Literal["low", "medium", "high"]
    notes: str = Field(default="", max_length=2048)


class AreaCompletenessReport(BaseModel):
    """Aggregate report for one area-completeness sweep."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(
        ...,
        pattern=r"^area-completeness-\d{4}-\d{2}-\d{2}(-[a-z0-9]+)?$",
        min_length=22,
        max_length=64,
    )
    sweep_trigger: Literal[
        "on_demand",
        "area_buildout",
        "pre_commit_self_test",
    ]
    swept_at: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    swept_by: str = Field(..., min_length=1, max_length=128)
    findings: list[AreaCompletenessFindingRow]
    pass_count: int = Field(..., ge=0)
    partial_count: int = Field(..., ge=0)
    gap_count: int = Field(..., ge=0)
    blocked_count: int = Field(..., ge=0)
    skip_count: int = Field(..., ge=0)
    total_findings: int = Field(..., ge=0)
