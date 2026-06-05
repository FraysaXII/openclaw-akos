"""Pydantic SSOT models for area-completeness sweeps.

v1 (I93 P0, ``D-IH-93-B``): flat 14-component checklist.
v2 (I94 P1, ``D-IH-94-A``): 2-D capability-maturity model — 16 components scored on a
maturity level (L0..L5) with criticality, area ``kind`` + ``entity`` axes, per-tier
thresholds, and **action-emitting** findings (current/target level + next action + owner
role) so the discipline is activatable by humans AND AICs.

Canonical doctrine:
``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md`` (v2)
Paired runbook: ``scripts/validate_area_completeness.py``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md``
Companion cursor rule: ``.cursor/rules/akos-area-governance.mdc``
Research grounding: ``docs/wip/intelligence/area-completeness-doctrine-2026-06-05/`` (131 sources).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AREA_COMPLETENESS_FINDING_FIELDNAMES: tuple[str, ...] = (
    "component_code",
    "area",
    "verdict",
    "maturity_level",
    "target_level",
    "criticality",
    "evidence_summary",
    "proposed_action",
    "next_action",
    "owner_role",
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

# --- v2 component set (16) ---------------------------------------------------
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
    "AREA-14-KIND-ENTITY",          # v2: was AREA-14-INHERITED-PATTERN; now kind+entity+APQC+inherited-pattern
    "AREA-15-PLACEMENT-INTEGRITY",  # v2 NEW
    "AREA-16-FILE-PLAN",            # v2 NEW
})

# Critical components must reach L3 (Defined) for an area to be "complete for its tier".
# AREA-09 (paired SOP+runbook) is deliberately ENHANCING, not critical: it was `partial`
# for every area in v1 (the pairing cliff = real forward debt, retrofitted per-wave), so
# gating closure on it would wrongly break the Data/Finance closures. It carries weight +
# a maturity badge and is tracked, but does not block "complete for tier" (I94 P1 calibration
# finding from proving v2 on Finance/Data; D-IH-94-A learning loop).
CRITICAL_COMPONENT_CODES: frozenset[str] = frozenset({
    "AREA-01-PARENT-REDESIGN",
    "AREA-02-AREA-CHARTER",
    "AREA-03-DISCIPLINE-CHARTERS",
    "AREA-04-PROCESS-LIST",
    "AREA-05-BASELINE-ROLES",
    "AREA-06-CAPABILITY-CONFIDENCE",
    "AREA-07-CANONICAL-PRECEDENCE",
    "AREA-08-DIMENSION-REGISTRIES",
    "AREA-14-KIND-ENTITY",
    "AREA-15-PLACEMENT-INTEGRITY",
})
# Enhancing components contribute a weighted badge but never gate closure.
ENHANCING_COMPONENT_CODES: frozenset[str] = VALID_AREA_COMPONENT_CODES - CRITICAL_COMPONENT_CODES

VALID_AREA_VERDICTS: frozenset[str] = frozenset({
    "pass",
    "partial",
    "gap",
    "blocked",
    "skip",
})

VALID_MATURITY_LEVELS: frozenset[str] = frozenset({"L0", "L1", "L2", "L3", "L4", "L5"})

VALID_AREA_CRITICALITY: frozenset[str] = frozenset({"critical", "enhancing"})

VALID_AREA_SEVERITIES: frozenset[str] = frozenset({"low", "medium", "high"})

VALID_AREA_SWEEP_TRIGGERS: frozenset[str] = frozenset({
    "on_demand",
    "area_buildout",
    "wave_close",
    "pre_commit_self_test",
})

# --- v2 area set (8; Legal added — BUG-1 fix) --------------------------------
VALID_SCORED_AREAS: frozenset[str] = frozenset({
    "Data",
    "Tech",
    "Finance",
    "Marketing",
    "Operations",
    "People",
    "Research",
    "Legal",
})

VALID_AREA_KINDS: frozenset[str] = frozenset({
    "stream_aligned",
    "platform",
    "capability_meta",
    "delivery_capacity",
})

VALID_AREA_ENTITIES: frozenset[str] = frozenset({
    "Holistika",
    "Think Big",
    "HLK Tech Lab",
})

# Per-area kind + entity + owning C-level role (per baseline_organisation.csv).
AREA_KIND_ENTITY: dict[str, dict[str, str]] = {
    "Data": {"kind": "platform", "entity": "HLK Tech Lab", "owner_role": "CDO"},
    "Tech": {"kind": "platform", "entity": "HLK Tech Lab", "owner_role": "CTO"},
    "Finance": {"kind": "stream_aligned", "entity": "Think Big", "owner_role": "CFO"},
    "Marketing": {"kind": "stream_aligned", "entity": "Think Big", "owner_role": "CMO"},
    "Operations": {"kind": "delivery_capacity", "entity": "Think Big", "owner_role": "COO"},
    "People": {"kind": "capability_meta", "entity": "Holistika", "owner_role": "CPO"},
    "Research": {"kind": "stream_aligned", "entity": "Holistika", "owner_role": "Holistik Researcher"},
    "Legal": {"kind": "stream_aligned", "entity": "Think Big", "owner_role": "Legal Counsel"},
}

# verdict -> default maturity level (probes may override upward for L4/L5 evidence).
VERDICT_TO_LEVEL: dict[str, str] = {
    "gap": "L0",
    "blocked": "L0",
    "skip": "L0",
    "partial": "L2",
    "pass": "L3",
}

_LEVEL_ORDER: dict[str, int] = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}


def level_ge(level: str, target: str) -> bool:
    """Return True when ``level`` is at or above ``target`` on the L0..L5 ladder."""
    return _LEVEL_ORDER.get(level, 0) >= _LEVEL_ORDER.get(target, 0)


class AreaCompletenessFindingRow(BaseModel):
    """One component probe result for one O5-1 area (v2 — maturity + action-emitting)."""

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
        "AREA-14-KIND-ENTITY",
        "AREA-15-PLACEMENT-INTEGRITY",
        "AREA-16-FILE-PLAN",
    ]
    area: Literal[
        "Data",
        "Tech",
        "Finance",
        "Marketing",
        "Operations",
        "People",
        "Research",
        "Legal",
    ]
    verdict: Literal["pass", "partial", "gap", "blocked", "skip"]
    maturity_level: Literal["L0", "L1", "L2", "L3", "L4", "L5"] = "L0"
    target_level: Literal["L0", "L1", "L2", "L3", "L4", "L5"] = "L3"
    criticality: Literal["critical", "enhancing"] = "enhancing"
    evidence_summary: str = Field(default="", max_length=1024)
    proposed_action: str = Field(default="", max_length=1024)
    next_action: str = Field(default="", max_length=1024)
    owner_role: str = Field(default="", max_length=128)
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
        "wave_close",
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
