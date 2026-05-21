"""Pydantic SSOT models for inter-wave regression sweeps (Wave M P2 mint).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md``
Paired runbook: ``scripts/inter_wave_regression_sweep.py``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md``
Companion cursor rule: ``.cursor/rules/akos-inter-wave-regression.mdc``
Wave M decision lineage: D-IH-86-BK (canonical mint), D-IH-86-BL (5-option enum),
D-IH-86-BO (initial Pydantic + runbook + tests + release-gate wiring),
D-IH-86-BW (Wave M.5 hotfix; doctrine-wins reconciliation: the 12 dimension
codes here now mirror the canonical INTER_WAVE_REGRESSION_DISCIPLINE.md
section 2 table exactly, and the ``BASELINE_DIMENSION_CODES`` /
``CONDITIONAL_DIMENSION_CODES`` frozensets reflect the canonical section 3
``compose_REGRESSION`` baseline / conditional split).

Two frozen models:

- ``RegressionFindingRow`` — one row per probe finding (1 wave-close sweep emits
  typically 10-30 such rows across the 12 dimensions).
- ``RegressionSweepReport`` — wrapper aggregating findings + counts + metadata
  for one wave-close gate.

Both models follow ``akos-holistika-operations.mdc`` §"New git-canonical compliance
registers" + ``CONTRIBUTING.md`` §"Python Code Standards": frozen BaseModel,
Literal enums for governed columns, regex patterns on slug-shaped fields,
length bounds on free-text fields.

The runbook ``scripts/inter_wave_regression_sweep.py`` constructs these models
from the 12 probe functions and emits both a markdown report (operator-facing)
and a JSON artifact (machine-readable for future agents). The release-gate's
``run_inter_wave_regression_self_test()`` validates fixture rows against these
schemas (not the full 12-dimension sweep — that's on_demand cadence per the
canonical §4).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

REGRESSION_FINDING_FIELDNAMES: tuple[str, ...] = (
    "dimension_code",
    "surface_path",
    "verdict",
    "proposed_rework_action",
    "candidate_decision_id",
    "severity",
    "notes",
)


REGRESSION_SWEEP_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "wave_closing",
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


VALID_DIMENSION_CODES: frozenset[str] = frozenset({
    "DIM-01-DECISION-LINEAGE",
    "DIM-02-FORWARD-CHARTER-CARRYOVER",
    "DIM-03-VALIDATOR-RAMP-CONSISTENCY",
    "DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
    "DIM-05-SOP-RUNBOOK-PAIRING",
    "DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
    "DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
    "DIM-08-BRAND-BASELINE-REGISTER-MATCH",
    "DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
    "DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
    "DIM-11-CURSOR-RULE-SKILL-PAIRING",
    "DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
})


BASELINE_DIMENSION_CODES: frozenset[str] = frozenset({
    "DIM-01-DECISION-LINEAGE",
    "DIM-02-FORWARD-CHARTER-CARRYOVER",
    "DIM-03-VALIDATOR-RAMP-CONSISTENCY",
    "DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
    "DIM-05-SOP-RUNBOOK-PAIRING",
    "DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
    "DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
})


CONDITIONAL_DIMENSION_CODES: frozenset[str] = frozenset({
    "DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
    "DIM-08-BRAND-BASELINE-REGISTER-MATCH",
    "DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
    "DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
    "DIM-11-CURSOR-RULE-SKILL-PAIRING",
})


VALID_VERDICTS: frozenset[str] = frozenset({
    "clean",
    "drift",
    "gap",
    "blocked",
    "skip",
})


VALID_SEVERITIES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})


class RegressionFindingRow(BaseModel):
    """One probe finding from a single dimension of one wave-close sweep.

    A clean sweep emits one row per dimension with ``verdict='clean'`` and
    empty ``proposed_rework_action``. A non-clean sweep emits one row per
    surfaced gap; each non-clean row becomes one AskQuestion option set at P4
    per ``akos-inter-wave-regression.mdc`` RULE 3 (inline-ratify every gap).

    The ``candidate_decision_id`` field is optional — populated only when the
    finding has already been pre-allocated a decision slot in
    ``DECISION_REGISTER.csv`` (e.g., D-IH-86-BS umbrella + D-IH-86-BT..BCC
    per-dimension sub-decisions in Wave M P4).

    Per ``CONTRIBUTING.md`` Python Code Standards: frozen BaseModel +
    ``str_strip_whitespace=True`` + Literal enums for governed columns.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    dimension_code: Literal[
        "DIM-01-DECISION-LINEAGE",
        "DIM-02-FORWARD-CHARTER-CARRYOVER",
        "DIM-03-VALIDATOR-RAMP-CONSISTENCY",
        "DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
        "DIM-05-SOP-RUNBOOK-PAIRING",
        "DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
        "DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
        "DIM-08-BRAND-BASELINE-REGISTER-MATCH",
        "DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
        "DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
        "DIM-11-CURSOR-RULE-SKILL-PAIRING",
        "DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
    ]
    surface_path: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Repo-root-relative POSIX path of the artifact this finding "
            "concerns (e.g., 'docs/references/hlk/v3.0/Admin/...'), OR a "
            "synthetic identifier for cross-cutting findings (e.g., "
            "'SUPABASE-MIRROR-PARITY:people_design_pattern_registry_mirror')."
        ),
    )
    verdict: Literal[
        "clean",
        "drift",
        "gap",
        "blocked",
        "skip",
    ] = Field(
        ...,
        description=(
            "5-option enum per D-IH-86-BL: clean (no action), drift (stale "
            "vs canonical), gap (missing artifact), blocked (MCP/external "
            "unavailable), skip (out-of-scope this wave with one-clause "
            "reason in notes)."
        ),
    )
    proposed_rework_action: str = Field(
        default="",
        max_length=1024,
        description=(
            "One-line proposed action for the AskQuestion option set at P4. "
            "Empty for clean/skip verdicts; mandatory for drift/gap/blocked."
        ),
    )
    candidate_decision_id: str | None = Field(
        default=None,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
        description=(
            "Pre-allocated DECISION_REGISTER.csv slot for this finding's "
            "ratification at P4. Optional; populated only when slot has "
            "already been reserved (e.g., D-IH-86-BT..BCC for Wave M; or "
            "D-IH-86-BW for the Wave M.5 doctrine-reconciliation hotfix)."
        ),
    )
    severity: Literal["low", "medium", "high"] = Field(
        ...,
        description=(
            "Severity heuristic feeding the recommended-default per "
            "akos-inter-wave-regression.mdc RULE 3 (high-severity "
            "reversible → rework-now; low-severity → rework-next-wave; "
            "novel-architectural → forward-charter)."
        ),
    )
    notes: str = Field(
        default="",
        max_length=2048,
        description=(
            "Free-text context for the finding. For skip verdict, MUST "
            "carry a one-clause reason per akos-inter-wave-regression.mdc "
            "RULE 2."
        ),
    )


class RegressionSweepReport(BaseModel):
    """Aggregate report for one wave-close 12-dimension regression sweep.

    Constructed by the runbook ``scripts/inter_wave_regression_sweep.py``
    after all 12 ``_probe_dimension_N`` functions return their finding lists.
    Emitted as both ``reports/regression-sweep-<YYYY-MM-DD>.md`` (operator-
    facing markdown table) AND ``artifacts/regression-sweep-<YYYY-MM-DD>.json``
    (machine-readable for future agents per the canonical §7 drift gate).

    Per ``akos-inter-wave-regression.mdc`` RULE 1: one sweep per wave-close
    gate. The ``wave_closing`` field carries the wave code (e.g., 'Wave-L'
    when sweeping at Wave M close) per the regex ``^Wave-[A-Z]+(\\.\\d+)?$``
    (the optional dot-decimal accommodates split waves like 'Wave-M.5' per
    R-86-WaveM-1 mitigation).

    Counts are eagerly computed at construction time (not lazy properties)
    because the JSON artifact is consumed by downstream agents that don't
    re-instantiate the model — keeping counts as plain fields ensures the
    JSON serialisation carries them directly.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(
        ...,
        pattern=r"^regression-sweep-\d{4}-\d{2}-\d{2}$",
        min_length=24,
        max_length=64,
        description=(
            "Stable slug matching ``^regression-sweep-YYYY-MM-DD$``. "
            "Aligns with the report file basename under reports/."
        ),
    )
    wave_closing: str = Field(
        ...,
        pattern=r"^Wave-[A-Z]+(\.\d+)?$",
        min_length=6,
        max_length=16,
        description=(
            "Wave code being closed (e.g., 'Wave-L' when this sweep fires "
            "at Wave M close). Regex permits dot-decimal split-wave codes "
            "like 'Wave-M.5' per R-86-WaveM-1 mitigation."
        ),
    )
    swept_at: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="ISO date YYYY-MM-DD when the sweep ran.",
    )
    swept_by: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description=(
            "Agent or operator identifier that ran the sweep. AC-AUTOMATION "
            "path: 'agent:<chat-uuid>'; AC-HUMAN path: 'operator' or "
            "'AIC:<role>'."
        ),
    )
    findings: list[RegressionFindingRow] = Field(
        ...,
        description=(
            "All findings emitted by the 12 probe functions. Empty list is "
            "valid (every dimension SKIP-d), but RULE 2 requires every "
            "SKIP to carry a one-clause reason in notes — the model does "
            "not enforce that recursively; the runbook does at finding-"
            "construction time."
        ),
    )
    clean_count: int = Field(..., ge=0, description="Count of clean verdicts")
    drift_count: int = Field(..., ge=0, description="Count of drift verdicts")
    gap_count: int = Field(..., ge=0, description="Count of gap verdicts")
    blocked_count: int = Field(
        ..., ge=0, description="Count of blocked verdicts"
    )
    skip_count: int = Field(..., ge=0, description="Count of skip verdicts")
    total_findings: int = Field(
        ...,
        ge=0,
        description=(
            "Total findings across all verdicts (sum of the 5 _count "
            "fields above). The model does not enforce sum-equality "
            "internally; the runbook asserts it at construction."
        ),
    )
