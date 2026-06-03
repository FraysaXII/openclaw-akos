"""Pydantic SSOT models for TechOps reliability sweeps (I90 P3b / OPS-86-9).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md``
Paired runbook: ``scripts/techops_reliability_check.py``
Companion cursor rule: ``.cursor/rules/akos-techops-discipline.mdc``
Decision lineage: D-IH-86-BX (canonical mint), D-IH-90-Z (P3b TechOps runbook chassis).

Seven frozen dimension codes TECH-01..TECH-07 mirror TECHOPS_DISCIPLINE.md section 2.
Full MCP-backed probes are deferred to deploy/event cadence; ``--self-test`` validates
chassis only (INFO ramp at pre_commit per I90 P3b packet).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TECHOPS_FINDING_FIELDNAMES: tuple[str, ...] = (
    "dimension_code",
    "surface_path",
    "verdict",
    "proposed_rework_action",
    "severity",
    "notes",
)

TECHOPS_SWEEP_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "service_tier",
    "swept_at",
    "swept_by",
    "findings",
    "clean_count",
    "drift_count",
    "gap_count",
    "blocked_count",
    "skip_count",
    "total_findings",
)

VALID_TECHOPS_DIMENSION_CODES: frozenset[str] = frozenset({
    "TECH-01-UPTIME-SLO",
    "TECH-02-CORE-WEB-VITALS",
    "TECH-03-ERROR-BUDGET",
    "TECH-04-DEPLOY-POSTURE",
    "TECH-05-SECURITY-POSTURE",
    "TECH-06-OBSERVABILITY-EVIDENCE",
    "TECH-07-INCIDENT-MANAGEMENT",
})

VALID_TECHOPS_VERDICTS: frozenset[str] = frozenset({
    "clean",
    "drift",
    "gap",
    "blocked",
    "skip",
})

VALID_TECHOPS_SEVERITIES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})

VALID_SERVICE_TIERS: frozenset[str] = frozenset({
    "production",
    "staging",
    "preview",
    "internal_dev",
})


class TechOpsFindingRow(BaseModel):
    """One probe finding from a single TechOps dimension sweep."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    dimension_code: Literal[
        "TECH-01-UPTIME-SLO",
        "TECH-02-CORE-WEB-VITALS",
        "TECH-03-ERROR-BUDGET",
        "TECH-04-DEPLOY-POSTURE",
        "TECH-05-SECURITY-POSTURE",
        "TECH-06-OBSERVABILITY-EVIDENCE",
        "TECH-07-INCIDENT-MANAGEMENT",
    ]
    surface_path: str = Field(default="", max_length=512)
    verdict: Literal["clean", "drift", "gap", "blocked", "skip"]
    proposed_rework_action: str = Field(default="", max_length=512)
    severity: Literal["low", "medium", "high"] = "low"
    notes: str = Field(default="", max_length=1024)


class TechOpsSweepReport(BaseModel):
    """Wrapper aggregating findings + counts for one TechOps reliability gate."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(..., min_length=1, max_length=128)
    service_tier: Literal["production", "staging", "preview", "internal_dev"] = "production"
    swept_at: str = Field(..., min_length=10, max_length=10)
    swept_by: str = Field(default="agent", max_length=64)
    findings: tuple[TechOpsFindingRow, ...] = ()
    clean_count: int = Field(default=0, ge=0)
    drift_count: int = Field(default=0, ge=0)
    gap_count: int = Field(default=0, ge=0)
    blocked_count: int = Field(default=0, ge=0)
    skip_count: int = Field(default=0, ge=0)
    total_findings: int = Field(default=0, ge=0)


def fixture_techops_finding_row() -> TechOpsFindingRow:
    """Well-formed finding for self-test / pytest."""
    return TechOpsFindingRow(
        dimension_code="TECH-04-DEPLOY-POSTURE",
        surface_path="REPOSITORY_REGISTRY.csv",
        verdict="skip",
        proposed_rework_action="",
        severity="low",
        notes="self-test fixture; MCP deploy probe deferred",
    )


def fixture_techops_sweep_report() -> TechOpsSweepReport:
    """Well-formed sweep report for self-test / pytest."""
    finding = fixture_techops_finding_row()
    return TechOpsSweepReport(
        report_id="techops-reliability-self-test",
        service_tier="production",
        swept_at="2026-06-01",
        swept_by="self-test",
        findings=(finding,),
        clean_count=0,
        drift_count=0,
        gap_count=0,
        blocked_count=0,
        skip_count=1,
        total_findings=1,
    )
