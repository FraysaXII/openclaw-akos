"""Field contracts for the SYNTHESIS_BEFORE_TRANCHE discipline (D-IH-86-EA..ED).

The 14th Quality Fabric specialty per `D-IH-86-EA` ratification (2026-05-25).
Canonical doctrine lives at::

    docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/
        SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md

Unlike COLLABORATOR_SHARE (the 13th specialty) — which authors persistent CSV
rows tracking engagement economics — SYNTHESIS_BEFORE_TRANCHE authors
**per-tranche synthesis reports** at::

    reports/synthesis-<tranche-id>-<YYYY-MM-DD>.md

The reports are markdown deliverables; this module defines the Pydantic
finding-row model the runbook (`scripts/synthesis_before_tranche_check.py`)
uses to emit findings + the validator (`scripts/validate_synthesis_before_tranche.py`)
uses to enforce the 10-dimension contract.

The 10 dimensions are codified in :data:`VALID_DIMENSION_CODES` and per-class
firing rules in :data:`DIMENSION_FIRE_RULES`. Per-tranche-class composition
mirrors INDEX_INTEGRITY (governance-only) and INTER_WAVE_REGRESSION (governance-
only) BUT spans all 5 fabric axes when the tranche-class warrants.

Mint references:
- D-IH-86-EA — canonical doctrine mint + INFO ramp (charter status)
- D-IH-86-EB — 10-dimension probe set ratification (SYN-01..SYN-10)
- D-IH-86-EC — 5-option disposition enum + per-tranche-class firing
- D-IH-86-ED — broad-fire posture with INFO ramp
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# =============================================================================
# 1. The 10 dimensions (SYN-01..SYN-10)
# =============================================================================

VALID_DIMENSION_CODES: frozenset[str] = frozenset({
    "SYN-01-AUDIENCE-COMPLETENESS",
    "SYN-02-CHANNEL-COVERAGE",
    "SYN-03-SCENARIO-INVENTORY",
    "SYN-04-BRAND-REGISTER-CITATION",
    "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
    "SYN-06-ERP-SURFACE-CITATION",
    "SYN-07-TRANCHE-ATOMICITY",
    "SYN-08-REVERSIBILITY-DECLARATION",
    "SYN-09-CLOSING-LOOP-TEST",
    "SYN-10-RECIPIENT-FALLBACK-CHANNEL",
})

# Human-readable dimension descriptions for the report.
DIMENSION_DESCRIPTIONS: dict[str, str] = {
    "SYN-01-AUDIENCE-COMPLETENESS": (
        "Has the tranche named every audience class touched by the tranche's "
        "output? FK-resolves against AUDIENCE_REGISTRY.csv."
    ),
    "SYN-02-CHANNEL-COVERAGE": (
        "Has the tranche named every channel through which the tranche's "
        "output reaches each audience? FK-resolves against "
        "CHANNEL_TOUCHPOINT_REGISTRY.csv."
    ),
    "SYN-03-SCENARIO-INVENTORY": (
        "Has the tranche named all scenarios (first-look / re-visit / "
        "empty-state / error-state / mobile-vs-desktop / etc.) the "
        "audience-channel pairs will be in when consuming the output?"
    ),
    "SYN-04-BRAND-REGISTER-CITATION": (
        "Has the tranche cited which brand register applies per audience "
        "(internal CORPINT vs external translated) + which voice traits "
        "+ which visual identity surface?"
    ),
    "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE": (
        "Has the tranche cited which D-IH-NN-X decisions ratify the "
        "design intent? FK-resolves against DECISION_REGISTER.csv."
    ),
    "SYN-06-ERP-SURFACE-CITATION": (
        "For engagement-class tranches: has the tranche named which of "
        "the 3 ERP-engagement-governance surfaces (operator dashboard / "
        "customer dashboard / ERP workflow join) it lives in?"
    ),
    "SYN-07-TRANCHE-ATOMICITY": (
        "Is the tranche scoped as ONE atomic commit or one operator-"
        "readable artifact? Does it land as one decision-point?"
    ),
    "SYN-08-REVERSIBILITY-DECLARATION": (
        "Has the tranche declared its reversibility class (low / medium "
        "/ high) with rationale? Has irreversibility been flagged before "
        "commit?"
    ),
    "SYN-09-CLOSING-LOOP-TEST": (
        "Has the tranche named the self-test / field-test / observability "
        "signal that confirms the tranche works as designed post-ship?"
    ),
    "SYN-10-RECIPIENT-FALLBACK-CHANNEL": (
        "Has the tranche named the traditional-means fallback (PDF / "
        "drive / mail / Loom / phone) for recipients who don't access "
        "the primary surface?"
    ),
}

# =============================================================================
# 2. Tranche classes (per-class dimension firing rules)
# =============================================================================

VALID_TRANCHE_CLASSES: frozenset[str] = frozenset({
    "engagement",
    "specialty_mint",
    "internal_governance",
    "canonical_csv_mint",
    "brand_surface",
    "external_deliverable",
})

# Per-class fire-set per SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md §2 table +
# D-IH-86-EC ratification. Keys: tranche class. Values: tuple of
# (always_fire, conditional_fire) frozensets.
DIMENSION_FIRE_RULES: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "engagement": (
        # all 10 fire
        frozenset(VALID_DIMENSION_CODES),
        frozenset(),
    ),
    "specialty_mint": (
        # 7 baseline fire
        frozenset({
            "SYN-01-AUDIENCE-COMPLETENESS",
            "SYN-02-CHANNEL-COVERAGE",
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-07-TRANCHE-ATOMICITY",
            "SYN-08-REVERSIBILITY-DECLARATION",
            "SYN-09-CLOSING-LOOP-TEST",
        }),
        # SYN-03 conditional (fires only when specialty has end-user scenarios)
        frozenset({"SYN-03-SCENARIO-INVENTORY"}),
    ),
    "internal_governance": (
        # 3 baseline fire
        frozenset({
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-07-TRANCHE-ATOMICITY",
            "SYN-08-REVERSIBILITY-DECLARATION",
        }),
        # 4 conditional (fire only when non-J-OP audience)
        frozenset({
            "SYN-01-AUDIENCE-COMPLETENESS",
            "SYN-02-CHANNEL-COVERAGE",
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-09-CLOSING-LOOP-TEST",
        }),
    ),
    "canonical_csv_mint": (
        # 6 baseline fire
        frozenset({
            "SYN-01-AUDIENCE-COMPLETENESS",
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-07-TRANCHE-ATOMICITY",
            "SYN-08-REVERSIBILITY-DECLARATION",
            "SYN-09-CLOSING-LOOP-TEST",
        }),
        # 3 conditional (fire when CSV rows surface in operator/customer dashboards)
        frozenset({
            "SYN-02-CHANNEL-COVERAGE",
            "SYN-03-SCENARIO-INVENTORY",
            "SYN-10-RECIPIENT-FALLBACK-CHANNEL",
        }),
    ),
    "brand_surface": (
        # 9 baseline fire (all except SYN-06)
        frozenset({
            "SYN-01-AUDIENCE-COMPLETENESS",
            "SYN-02-CHANNEL-COVERAGE",
            "SYN-03-SCENARIO-INVENTORY",
            "SYN-04-BRAND-REGISTER-CITATION",
            "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
            "SYN-07-TRANCHE-ATOMICITY",
            "SYN-08-REVERSIBILITY-DECLARATION",
            "SYN-09-CLOSING-LOOP-TEST",
            "SYN-10-RECIPIENT-FALLBACK-CHANNEL",
        }),
        # SYN-06 conditional (fires only when brand surface is engagement-scoped)
        frozenset({"SYN-06-ERP-SURFACE-CITATION"}),
    ),
    "external_deliverable": (
        # all 10 fire
        frozenset(VALID_DIMENSION_CODES),
        frozenset(),
    ),
}


def resolve_fire_set(tranche_class: str, conditional_triggers: bool = False) -> frozenset[str]:
    """Return the dimensions that fire for the given tranche class.

    Parameters
    ----------
    tranche_class
        One of :data:`VALID_TRANCHE_CLASSES`.
    conditional_triggers
        When True, include the conditional dimensions too. When False
        (default), return only the always-fire dimensions.
    """
    if tranche_class not in VALID_TRANCHE_CLASSES:
        raise ValueError(
            f"unknown tranche_class {tranche_class!r}; "
            f"must be one of {sorted(VALID_TRANCHE_CLASSES)}"
        )
    always, conditional = DIMENSION_FIRE_RULES[tranche_class]
    if conditional_triggers:
        return always | conditional
    return always


# =============================================================================
# 3. Finding statuses + dispositions
# =============================================================================

VALID_FINDING_STATUSES: frozenset[str] = frozenset({
    "PASS",
    "WARN",
    "FAIL",
    "INFO",
    "N/A",
})

# 5-option disposition enum per D-IH-86-EC.
VALID_DISPOSITIONS: frozenset[str] = frozenset({
    "scope-complete",
    "scope-extend",
    "scope-narrow",
    "defer-OPS",
    "escalate-to-blocker-tracker",
})

VALID_REVERSIBILITY_CLASSES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})

# Per-dimension severity bound per SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md §5.
# The validator enforces: a dimension classified `mandatory-citation` (FAIL ramp)
# must emit FAIL on missing; a dimension classified `judgement` (WARN ramp)
# emits WARN on missing; SYN-07 is binary atomicity (FAIL ramp permanently).
DIMENSION_SEVERITY_CLASS: dict[str, str] = {
    "SYN-01-AUDIENCE-COMPLETENESS": "judgement",
    "SYN-02-CHANNEL-COVERAGE": "judgement",
    "SYN-03-SCENARIO-INVENTORY": "judgement",
    "SYN-04-BRAND-REGISTER-CITATION": "mandatory-citation",
    "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE": "mandatory-citation",
    "SYN-06-ERP-SURFACE-CITATION": "judgement",
    "SYN-07-TRANCHE-ATOMICITY": "atomicity",
    "SYN-08-REVERSIBILITY-DECLARATION": "mandatory-citation",
    "SYN-09-CLOSING-LOOP-TEST": "judgement",
    "SYN-10-RECIPIENT-FALLBACK-CHANNEL": "judgement",
}

# =============================================================================
# 4. Sweep triggers (cadence enum)
# =============================================================================

VALID_SWEEP_TRIGGERS: frozenset[str] = frozenset({
    "pre_commit_self_test",
    "tranche_charter",
    "tranche_pre_commit",
    "on_demand",
})

# =============================================================================
# 5. Pydantic models
# =============================================================================


class SynthesisFindingRow(BaseModel):
    """One finding row emitted by the synthesis sweep for one tranche.

    Each row represents the outcome of one probe (one dimension) for one
    tranche. The runbook emits one row per (tranche, dimension) pair where
    the dimension fires per :data:`DIMENSION_FIRE_RULES`. Skipped (N/A)
    dimensions are recorded explicitly so the audit trail never has gaps.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    tranche_id: str = Field(min_length=1, max_length=120)
    tranche_class: Literal[
        "engagement",
        "specialty_mint",
        "internal_governance",
        "canonical_csv_mint",
        "brand_surface",
        "external_deliverable",
    ]
    dimension_code: Literal[
        "SYN-01-AUDIENCE-COMPLETENESS",
        "SYN-02-CHANNEL-COVERAGE",
        "SYN-03-SCENARIO-INVENTORY",
        "SYN-04-BRAND-REGISTER-CITATION",
        "SYN-05-GOVERNANCE-RATIFICATION-LINEAGE",
        "SYN-06-ERP-SURFACE-CITATION",
        "SYN-07-TRANCHE-ATOMICITY",
        "SYN-08-REVERSIBILITY-DECLARATION",
        "SYN-09-CLOSING-LOOP-TEST",
        "SYN-10-RECIPIENT-FALLBACK-CHANNEL",
    ]
    status: Literal["PASS", "WARN", "FAIL", "INFO", "N/A"]
    finding_text: str = Field(min_length=1, max_length=2000)
    recommendation_text: str = Field(default="", max_length=2000)
    evidence_path: str = Field(
        default="",
        max_length=400,
        description=(
            "Repo-root-relative path to the artifact that proves the finding "
            "OR cites the design decision. May be a master-roadmap.md, a "
            "decision-register row anchor, a canonical CSV row, or a brand "
            "surface path."
        ),
    )
    recommended_disposition: Literal[
        "scope-complete",
        "scope-extend",
        "scope-narrow",
        "defer-OPS",
        "escalate-to-blocker-tracker",
        "n/a",
    ] = "n/a"
    notes: str = Field(default="", max_length=2000)


class SynthesisTrancheCharter(BaseModel):
    """The frontmatter contract that a tranche's master-roadmap or candidate
    file MUST satisfy for the synthesis runbook to read it via
    ``--check-from-frontmatter``.

    A tranche-charter frontmatter is the operator's declaration of intent for
    the tranche BEFORE the synthesis sweep runs. The sweep then verifies that
    the tranche's actual scope matches the charter's 5-axis declaration.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    tranche_id: str = Field(min_length=1, max_length=120)
    tranche_class: Literal[
        "engagement",
        "specialty_mint",
        "internal_governance",
        "canonical_csv_mint",
        "brand_surface",
        "external_deliverable",
    ]
    tranche_title: str = Field(min_length=1, max_length=240)
    audiences_named: list[str] = Field(
        default_factory=list,
        description="FK list against AUDIENCE_REGISTRY.csv (e.g., J-OP, J-CU).",
    )
    channels_named: list[str] = Field(
        default_factory=list,
        description=(
            "FK list against CHANNEL_TOUCHPOINT_REGISTRY.csv "
            "(e.g., CHAN-EMAIL-OUTBOUND, CHAN-WEB-DASHBOARD)."
        ),
    )
    scenarios_named: list[str] = Field(default_factory=list)
    brand_register: Literal["internal-corpint", "external-translated", "mixed"] = (
        "internal-corpint"
    )
    ratifying_decisions: list[str] = Field(
        default_factory=list,
        description="FK list against DECISION_REGISTER.csv (e.g., D-IH-86-EA).",
    )
    erp_surface_citations: list[str] = Field(
        default_factory=list,
        description=(
            "For engagement-class only: list naming which of the 3 ERP-"
            "engagement-governance surfaces (operator-dashboard / "
            "customer-dashboard / erp-workflow-join) the tranche's "
            "deliverables surface in."
        ),
    )
    is_atomic_commit: bool = True
    reversibility_class: Literal["low", "medium", "high"] = "medium"
    reversibility_rationale: str = Field(default="", max_length=2000)
    closing_loop_test: str = Field(default="", max_length=2000)
    recipient_fallback_channel: str = Field(default="", max_length=400)
    operator_framing_quote: str = Field(default="", max_length=2000)


class SynthesisReportSummary(BaseModel):
    """Per-tranche rollup emitted as the synthesis report's frontmatter."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    tranche_id: str = Field(min_length=1, max_length=120)
    tranche_class: Literal[
        "engagement",
        "specialty_mint",
        "internal_governance",
        "canonical_csv_mint",
        "brand_surface",
        "external_deliverable",
    ]
    swept_at: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    sweep_trigger: Literal[
        "pre_commit_self_test",
        "tranche_charter",
        "tranche_pre_commit",
        "on_demand",
    ]
    dimensions_fired: int = Field(ge=0, le=10)
    pass_count: int = Field(ge=0, le=10)
    warn_count: int = Field(ge=0, le=10)
    fail_count: int = Field(ge=0, le=10)
    info_count: int = Field(ge=0, le=10)
    na_count: int = Field(ge=0, le=10)
    synthesis_complete: bool = Field(
        description=(
            "True when zero FAIL findings + all mandatory-citation "
            "dimensions PASS or N/A; False otherwise. Drift gate consumes "
            "this field for FAIL-ramp decisions per D-IH-86-ED."
        )
    )
    inline_ratify_gates_open: int = Field(ge=0)
    operator_disposition_recorded: bool = False
