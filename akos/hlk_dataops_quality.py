"""Pydantic SSOT models for DataOps quality sweeps (I90 P3c / OPS-86-19).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/DATAOPS_DISCIPLINE.md``
Paired runbook: ``scripts/dataops_quality_check.py``
Companion cursor rule: ``.cursor/rules/akos-dataops-discipline.mdc``
Decision lineage: D-IH-86-BV (canonical mint), D-IH-90-AA (charter -> active promotion).

Seven frozen dimension codes DATA-01..DATA-07 mirror DATAOPS_DISCIPLINE.md section 2.
Full live probes (mirror parity, FDW health, Supabase advisors) defer to event cadence;
``--self-test`` validates chassis only (INFO ramp at pre_commit per I90 P3c).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DATAOPS_FINDING_FIELDNAMES: tuple[str, ...] = (
    "dimension_code",
    "surface_path",
    "verdict",
    "proposed_rework_action",
    "severity",
    "notes",
)

DATAOPS_SWEEP_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "data_surface",
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

VALID_DATAOPS_DIMENSION_CODES: frozenset[str] = frozenset({
    "DATA-01-FK-INTEGRITY",
    "DATA-02-MIRROR-PARITY",
    "DATA-03-FDW-HEALTH",
    "DATA-04-PIPELINE-FRESHNESS",
    "DATA-05-SCHEMA-DRIFT",
    "DATA-06-LINEAGE",
    "DATA-07-QUALITY-METRICS",
})

VALID_DATAOPS_VERDICTS: frozenset[str] = frozenset({
    "clean",
    "drift",
    "gap",
    "blocked",
    "skip",
})

VALID_DATAOPS_SEVERITIES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})

VALID_DATA_SURFACES: frozenset[str] = frozenset({
    "canonical_csv",
    "mirror_table",
    "fdw_projection",
    "manifest_md",
    "pydantic_ssot",
    "observability_evidence",
})


class DataOpsFindingRow(BaseModel):
    """One probe finding from a single DataOps dimension sweep."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    dimension_code: Literal[
        "DATA-01-FK-INTEGRITY",
        "DATA-02-MIRROR-PARITY",
        "DATA-03-FDW-HEALTH",
        "DATA-04-PIPELINE-FRESHNESS",
        "DATA-05-SCHEMA-DRIFT",
        "DATA-06-LINEAGE",
        "DATA-07-QUALITY-METRICS",
    ]
    surface_path: str = Field(default="", max_length=512)
    verdict: Literal["clean", "drift", "gap", "blocked", "skip"]
    proposed_rework_action: str = Field(default="", max_length=512)
    severity: Literal["low", "medium", "high"] = "low"
    notes: str = Field(default="", max_length=1024)


class DataOpsSweepReport(BaseModel):
    """Wrapper aggregating findings + counts for one DataOps quality gate."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(..., min_length=1, max_length=128)
    data_surface: Literal[
        "canonical_csv",
        "mirror_table",
        "fdw_projection",
        "manifest_md",
        "pydantic_ssot",
        "observability_evidence",
    ] = "canonical_csv"
    swept_at: str = Field(..., min_length=10, max_length=10)
    swept_by: str = Field(default="agent", max_length=64)
    findings: tuple[DataOpsFindingRow, ...] = ()
    clean_count: int = Field(default=0, ge=0)
    drift_count: int = Field(default=0, ge=0)
    gap_count: int = Field(default=0, ge=0)
    blocked_count: int = Field(default=0, ge=0)
    skip_count: int = Field(default=0, ge=0)
    total_findings: int = Field(default=0, ge=0)


def fixture_dataops_finding_row() -> DataOpsFindingRow:
    """Well-formed finding for self-test / pytest."""
    return DataOpsFindingRow(
        dimension_code="DATA-05-SCHEMA-DRIFT",
        surface_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv",
        verdict="skip",
        proposed_rework_action="",
        severity="low",
        notes="self-test fixture; full schema-drift probe deferred to canonical-CSV mint cadence",
    )


def fixture_dataops_sweep_report() -> DataOpsSweepReport:
    """Well-formed sweep report for self-test / pytest."""
    finding = fixture_dataops_finding_row()
    return DataOpsSweepReport(
        report_id="dataops-quality-self-test",
        data_surface="canonical_csv",
        swept_at="2026-06-04",
        swept_by="self-test",
        findings=(finding,),
        clean_count=0,
        drift_count=0,
        gap_count=0,
        blocked_count=0,
        skip_count=1,
        total_findings=1,
    )
