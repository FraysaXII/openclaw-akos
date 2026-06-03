"""Fleet hygiene Pydantic models — multi-repo worktree + standing-obligation rechecks.

Pairs with ``scripts/workspace_fleet_hygiene_sweep.py`` and the CICD baseline
discipline (``SOP-CICD_BASELINE_001`` + ``akos/cicd_baseline.py``). Complements
drift-only gates (``check-drift.py``, bless sha256) with **content** signals:
what is uncommitted, unpushed, stale in OPS_REGISTER, or missing from CI workflows.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

FleetDimensionCode = Literal[
    "FLEET-01-WORKTREE",
    "FLEET-02-PUBLISH-DRIFT",
    "FLEET-03-CI-CONTENT",
    "FLEET-04-STANDING-OPS",
]

FleetVerdict = Literal["clean", "drift", "gap", "blocked", "skip"]
FleetSeverity = Literal["low", "medium", "high"]

VALID_FLEET_DIMENSION_CODES: frozenset[str] = frozenset(
    {
        "FLEET-01-WORKTREE",
        "FLEET-02-PUBLISH-DRIFT",
        "FLEET-03-CI-CONTENT",
        "FLEET-04-STANDING-OPS",
    }
)

FLEET_FINDING_FIELDNAMES: tuple[str, ...] = (
    "dimension_code",
    "surface_path",
    "verdict",
    "severity",
    "notes",
    "proposed_rework_action",
)

FLEET_SWEEP_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "swept_at",
    "swept_by",
    "clean_count",
    "drift_count",
    "gap_count",
    "blocked_count",
    "skip_count",
    "total_findings",
    "findings",
)

# Governed repos the sweep always probes when ``local_path`` resolves.
DEFAULT_GOVERNED_REPO_SLUGS: frozenset[str] = frozenset(
    {"openclaw-akos", "hlk-erp", "kirbe-platform", "boilerplate"}
)

# Open OPS rows with explicit standing / continuous recheck obligation (agent watch list).
STANDING_OPS_WATCH_IDS: frozenset[str] = frozenset(
    {
        "OPS-81-1",  # I81 vault integrity observation cadence
        "OPS-86-1",  # I86 cluster coordination
        "OPS-86-9",  # TechOps / DataOps / MKTOPS / UX runbook threads
        "OPS-90-6",  # KiRBe GDrive pairing forward (I81 P6)
    }
)

STANDING_OPS_STALE_DAYS: int = 30


class FleetFindingRow(BaseModel):
    dimension_code: FleetDimensionCode
    surface_path: str
    verdict: FleetVerdict
    severity: FleetSeverity = "medium"
    notes: str = ""
    proposed_rework_action: str = ""


class FleetSweepReport(BaseModel):
    report_id: str
    swept_at: str
    swept_by: str = "workspace_fleet_hygiene_sweep.py"
    findings: tuple[FleetFindingRow, ...]
    clean_count: int = 0
    drift_count: int = 0
    gap_count: int = 0
    blocked_count: int = 0
    skip_count: int = 0
    total_findings: int = 0


def fixture_fleet_finding_row() -> FleetFindingRow:
    return FleetFindingRow(
        dimension_code="FLEET-01-WORKTREE",
        surface_path="openclaw-akos",
        verdict="clean",
        severity="low",
        notes="fixture",
        proposed_rework_action="",
    )


def fixture_fleet_sweep_report() -> FleetSweepReport:
    row = fixture_fleet_finding_row()
    return FleetSweepReport(
        report_id="fleet-hygiene-fixture",
        swept_at="2026-06-01",
        findings=(row,),
        clean_count=1,
        total_findings=1,
    )
