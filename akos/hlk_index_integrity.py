"""Pydantic SSOT models for baseline-index integrity sweeps (Wave N P3 mint).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md``
Paired runbook: ``scripts/baseline_index_sweep.py``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INDEX_INTEGRITY_001.md``
Companion cursor rule: ``.cursor/rules/akos-index-integrity.mdc``
Wave N decision lineage: D-IH-86-CD (canonical mint + INFO ramp),
D-IH-86-CE (8-dimension probe set), D-IH-86-CF (paired SOP+runbook gate).

Two frozen models:

- ``IndexFreshnessRow`` — one row per probe finding (1 sweep typically emits
  8-30 such rows across the 8 dimensions when baseline docs are out of sync).
- ``IndexFreshnessReport`` — wrapper aggregating findings + counts + metadata
  for one sweep run.

The INDEX_INTEGRITY discipline is the **11th** Quality Fabric specialty
(per HOLISTIKA_QUALITY_FABRIC.md §6 row added at this mint). It is the
mechanical-enforcement sister to the doctrine-of-clarity principle named in
``akos-people-discipline-of-disciplines.mdc`` RULE 4 (anti-jargon drift gate)
and the inter-wave regression discipline (10th specialty, Wave M mint).
Whereas INTER_WAVE_REGRESSION sweeps at wave-close to catch drift in
governance artifacts produced by the wave, INDEX_INTEGRITY sweeps at every
wave-close AND at every canonical-CSV mint to catch drift in the **baseline
index documents** that downstream agents read first (planning README,
PRECEDENCE.md, CHANGELOG.md, INITIATIVE_DEPENDENCIES.md, USER_GUIDE.md HLK
Operator Model section, ARCHITECTURE.md HLK Registry, dashboards, vault
index.md).

Per ``akos-holistika-operations.mdc`` §"New git-canonical compliance
registers" + ``CONTRIBUTING.md`` §"Python Code Standards": frozen BaseModel,
Literal enums for governed columns, regex patterns on slug-shaped fields,
length bounds on free-text fields.

The runbook ``scripts/baseline_index_sweep.py`` constructs these models from
the 8 probe functions and emits both a markdown report (operator-facing) and
a JSON artifact (machine-readable for future agents). The release-gate's
``run_index_freshness_self_test()`` validates fixture rows against these
schemas (not the full 8-dimension sweep — that runs at wave-close + on every
canonical-CSV mint).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

INDEX_FRESHNESS_FIELDNAMES: tuple[str, ...] = (
    "dimension_code",
    "index_path",
    "verdict",
    "drift_summary",
    "proposed_fix_action",
    "candidate_decision_id",
    "severity",
    "notes",
)


INDEX_FRESHNESS_REPORT_FIELDNAMES: tuple[str, ...] = (
    "report_id",
    "sweep_trigger",
    "swept_at",
    "swept_by",
    "findings",
    "fresh_count",
    "drift_count",
    "gap_count",
    "blocked_count",
    "skip_count",
    "total_findings",
)


VALID_INDEX_DIMENSION_CODES: frozenset[str] = frozenset({
    "IDX-01-PLANNING-README-INITIATIVE-COUNT",
    "IDX-02-PRECEDENCE-CSV-COVERAGE",
    "IDX-03-CHANGELOG-WAVE-COVERAGE",
    "IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
    "IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
    "IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
    "IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
    "IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
})


BASELINE_INDEX_DIMENSION_CODES: frozenset[str] = frozenset({
    "IDX-01-PLANNING-README-INITIATIVE-COUNT",
    "IDX-02-PRECEDENCE-CSV-COVERAGE",
    "IDX-03-CHANGELOG-WAVE-COVERAGE",
    "IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
    "IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
    "IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
})


CONDITIONAL_INDEX_DIMENSION_CODES: frozenset[str] = frozenset({
    "IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
    "IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
})


VALID_INDEX_VERDICTS: frozenset[str] = frozenset({
    "fresh",
    "drift",
    "gap",
    "blocked",
    "skip",
})


VALID_INDEX_SEVERITIES: frozenset[str] = frozenset({
    "low",
    "medium",
    "high",
})


VALID_SWEEP_TRIGGERS: frozenset[str] = frozenset({
    "wave_close",
    "canonical_csv_mint",
    "on_demand",
    "pre_commit_self_test",
})


class IndexFreshnessRow(BaseModel):
    """One probe finding from a single dimension of one index-freshness sweep.

    A fresh sweep emits one row per dimension with ``verdict='fresh'`` and
    empty ``proposed_fix_action``. A non-fresh sweep emits one row per
    surfaced drift; each non-fresh row becomes one ratify option at the
    triage gate per ``akos-index-integrity.mdc`` RULE 3 (deterministic-fix
    via the paired runbook OR inline-ratify when the fix needs judgement).

    The ``candidate_decision_id`` field is optional — populated only when
    the finding has already been pre-allocated a decision slot in
    ``DECISION_REGISTER.csv``.

    Per ``CONTRIBUTING.md`` Python Code Standards: frozen BaseModel +
    ``str_strip_whitespace=True`` + Literal enums for governed columns.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    dimension_code: Literal[
        "IDX-01-PLANNING-README-INITIATIVE-COUNT",
        "IDX-02-PRECEDENCE-CSV-COVERAGE",
        "IDX-03-CHANGELOG-WAVE-COVERAGE",
        "IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
        "IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
        "IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
        "IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
        "IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
    ]
    index_path: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description=(
            "Repo-root-relative POSIX path of the index document this "
            "finding concerns (e.g., 'docs/wip/planning/README.md'), OR a "
            "synthetic identifier for cross-cutting findings (e.g., "
            "'FILESYSTEM-PARITY:planning-folders-vs-readme')."
        ),
    )
    verdict: Literal[
        "fresh",
        "drift",
        "gap",
        "blocked",
        "skip",
    ] = Field(
        ...,
        description=(
            "5-option enum per D-IH-86-CD: fresh (no action), drift "
            "(stale vs source-of-truth), gap (missing index entry), "
            "blocked (sweep cannot complete — MCP/external unavailable), "
            "skip (out-of-scope for this trigger with one-clause reason)."
        ),
    )
    drift_summary: str = Field(
        default="",
        max_length=1024,
        description=(
            "One-line summary of the drift detected: what the index says, "
            "what the source-of-truth says, and the delta. Empty for "
            "fresh/skip; mandatory for drift/gap/blocked."
        ),
    )
    proposed_fix_action: str = Field(
        default="",
        max_length=1024,
        description=(
            "One-line proposed action: either a runbook invocation "
            "(deterministic fix) or a description of the judgement-call "
            "fix (inline-ratify gate). Empty for fresh/skip; mandatory "
            "for drift/gap/blocked."
        ),
    )
    candidate_decision_id: str | None = Field(
        default=None,
        pattern=r"^D-IH-\d+-[A-Z0-9_]+$",
        min_length=8,
        max_length=64,
        description=(
            "Pre-allocated DECISION_REGISTER.csv slot for this finding's "
            "ratification (when judgement-call). Optional; populated only "
            "when the slot has already been reserved."
        ),
    )
    severity: Literal["low", "medium", "high"] = Field(
        ...,
        description=(
            "Severity heuristic feeding the recommended-default per "
            "akos-index-integrity.mdc RULE 3 (high-severity reversible → "
            "deterministic-fix-now; medium → next-wave; low → defer-OPS)."
        ),
    )
    notes: str = Field(
        default="",
        max_length=2048,
        description=(
            "Free-text context for the finding. For skip verdict, MUST "
            "carry a one-clause reason per akos-index-integrity.mdc "
            "RULE 2."
        ),
    )


class IndexFreshnessReport(BaseModel):
    """Aggregate report for one 8-dimension baseline-index sweep.

    Constructed by ``scripts/baseline_index_sweep.py`` after all 8
    ``_probe_dimension_N`` functions return their finding lists.
    Emitted as both ``reports/index-sweep-<YYYY-MM-DD>.md`` (operator-
    facing markdown table) AND ``artifacts/index-sweep-<YYYY-MM-DD>.json``
    (machine-readable for future agents).

    Per ``akos-index-integrity.mdc`` RULE 1: at every wave-close OR every
    canonical-CSV mint, the runbook runs the sweep before the wave's UAT
    verdict line is filled in / before the CSV-mint commit lands. The
    ``sweep_trigger`` field carries the trigger code.

    Counts are eagerly computed at construction time (not lazy properties)
    because the JSON artifact is consumed by downstream agents that don't
    re-instantiate the model — keeping counts as plain fields ensures the
    JSON serialisation carries them directly.
    """

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    report_id: str = Field(
        ...,
        pattern=r"^index-sweep-\d{4}-\d{2}-\d{2}(-[a-z0-9]+)?$",
        min_length=17,
        max_length=64,
        description=(
            "Stable slug matching ``^index-sweep-YYYY-MM-DD(-<slug>)?$``. "
            "Aligns with the report file basename. Optional ``-<slug>`` "
            "suffix disambiguates multiple sweeps on the same day (e.g., "
            "'index-sweep-2026-05-21-wave-n-close')."
        ),
    )
    sweep_trigger: Literal[
        "wave_close",
        "canonical_csv_mint",
        "on_demand",
        "pre_commit_self_test",
    ] = Field(
        ...,
        description=(
            "What triggered this sweep. Per the canonical §4 cadence: "
            "wave_close (every wave-close gate), canonical_csv_mint "
            "(every new CSV row in compliance/dimensions/), on_demand "
            "(operator-triggered), pre_commit_self_test (zero-cost "
            "fixture validation; not a real sweep)."
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
    findings: list[IndexFreshnessRow] = Field(
        ...,
        description=(
            "All findings emitted by the 8 probe functions. Empty list is "
            "valid (every dimension skipped), but RULE 2 requires every "
            "skip to carry a one-clause reason in notes — the model does "
            "not enforce that recursively; the runbook does at finding-"
            "construction time."
        ),
    )
    fresh_count: int = Field(..., ge=0, description="Count of fresh verdicts")
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
