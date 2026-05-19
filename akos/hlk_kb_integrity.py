"""Pydantic chassis for the KB integrity baseline matrix per I81 P1.

The vault has substrate (SOPs + addenda + canonicals + pairing registry + validators)
but lacks an **evidence baseline** that proves end-to-end integrity. I81 P1 produces
that baseline: a per-executable-process row carrying 5 coverage signals + a gap
summary, plus a narrative audit that quantifies the current state and routes
downstream retrofits.

**Scope of "executable" rows** (per D-IH-81-F integrity-matrix methodology
ratified inline at this commit): rows in [`process_list.csv`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv)
with ``item_granularity`` in ``{"task", "process"}``. The other granularities
(``project``, ``workstream``) are scope/structure aggregates that do not name
discrete executable units. As of the P1 baseline commit there are 1085 such
executable rows across 9 areas.

**5 coverage signals** per row:

1. ``knowledge_pairing_status`` — does the item appear in
   [`KNOWLEDGE_PAIRING_REGISTRY.csv`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv)?
2. ``paired_sop_status`` — does a v3.0 SOP markdown file exist that references
   the item_id (best-effort path scan)?
3. ``mirror_coverage_status`` — does the row land in the Supabase
   ``compliance.process_list_mirror`` table via ``compliance_mirror_emit``?
   At P1 baseline this is ``covered_by_emit`` for every row by construction of
   the sync flow; the column exists so a future commit can flip individual
   rows to ``mirror-skip`` when the row is intentionally not mirrored
   (e.g. duplicate or test-only rows).
4. ``audience_tags_status`` — is the owning role's audience tag coverage
   resolvable via I85 P1 ``AUDIENCE_REGISTRY``? At P1 baseline this is
   ``deferred`` for every row; the live wire is forward-chartered to the I81
   P1 follow-up that joins the audience-tag axis after I85 stabilizes.
5. ``cadence_status`` — does the row carry a non-empty ``cadence_type`` per
   I72 P4 (``on_demand`` / ``scheduled`` / ``event_triggered`` / ``gated_operator``)?
   Cadence-untyped rows are flagged so the [`akos-executable-process-catalog.mdc`](.cursor/rules/akos-executable-process-catalog.mdc)
   RULE 3 cadence taxonomy gets quantified coverage.

**Gap classification** at row level (``KbIntegrityRowVerdict``):

- ``pass`` — ALL 5 coverage signals in good state (knowledge_pairing matched
  + paired_sop present + mirror covered + audience tags resolved + cadence
  declared). At P1 baseline this is necessarily a small minority of rows
  because audience_tags_status is ``deferred`` for all.
- ``partial`` — at least the mirror coverage signal is good, but ≥ 1 other
  signal is missing. The most common P1 baseline state.
- ``fail`` — mirror coverage is missing (the row never landed in the mirror).
  At P1 baseline this is ``fail`` only for rows whose ``item_id`` violates
  the mirror sync contract (rare; flags a sync-flow bug).

**PASS threshold** per D-IH-81-F: ≥ 95% of rows reach ``pass`` verdict.
P1 baseline records the gap; P4-P8 retrofit waves move the needle.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# -----------------------------------------------------------------------------
# Type aliases (Literal-based enums per akos.hlk_madeira_mode chassis pattern)
# -----------------------------------------------------------------------------

KbCoverageStatus = Literal["matched", "unmatched", "deferred", "covered_by_emit", "mirror_skip", "declared", "undeclared"]
"""Union over per-signal coverage status values. Each signal column uses a
subset of this union (typed via the model field's `Literal[...]`)."""


KbIntegrityVerdict = Literal["pass", "partial", "fail"]
"""Row-level verdict aggregated from the 5 coverage signals per the
``KbIntegrityMatrixRow.compute_verdict()`` deterministic function."""


KbExecutableGranularity = Literal["task", "process"]
"""The 2 granularities deemed executable per I81 P1 scope (D-IH-81-F)."""


# Item-id regex per process_list.csv convention.
#
# Two patterns are both legitimate in the real corpus:
#   1. Standard lowercase-underscore: `hol_resea_prj_1`, `env_tech_dtp_307`,
#      `tbi_mkt_prc_brand_canon_mtnce_001` — the dominant pattern (~1080+ rows).
#   2. SOP-prefixed legacy: `SOP-META_PROCESS_MGMT_001`, `SOP-EXTERNAL_REPO_BLESSING_001`
#      — older rows whose item_id is the SOP file basename.
#
# Both patterns are accepted by this regex; rows that fail (e.g. empty,
# whitespace, leading digit) are skipped by the audit tool with a warning.
ITEM_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]+$")


# -----------------------------------------------------------------------------
# Per-row matrix model
# -----------------------------------------------------------------------------


class KbIntegrityMatrixRow(BaseModel):
    """One row of the KB integrity baseline matrix per I81 P1.

    Mirrors [`process_list.csv`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv)
    `item_id` 1:1 (composite PK = item_id alone, given executable-granularity
    scope). Each row carries the 5 coverage signals + a row-level verdict
    derived from them deterministically via ``compute_verdict()``.

    The matrix is **report-class** (not canonical SSOT) per the master-roadmap
    §6 asset classification. The audit script emits this row shape into
    ``reports/i81/kb-integrity-matrix-<date>.csv``; the Pydantic model exists
    to lock the schema so downstream consumers + future commits can rely on
    the column set staying stable.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    item_id: str = Field(..., description="FK to process_list.csv item_id.")
    area: str = Field(..., min_length=1, description="process_list.csv area cell.")
    role_owner: str = Field(..., min_length=1, description="process_list.csv role_owner cell.")
    item_granularity: KbExecutableGranularity
    item_name: str = Field(..., min_length=1)

    # --- 5 coverage signals (typed Literal subsets of KbCoverageStatus) -------
    knowledge_pairing_status: Literal["matched", "unmatched"] = Field(
        ...,
        description="Is the item_id resolvable into KNOWLEDGE_PAIRING_REGISTRY.csv pairing_id "
        "or parent_doc_path heuristic? matched | unmatched.",
    )
    paired_sop_status: Literal["matched", "unmatched"] = Field(
        ...,
        description="Does a v3.0 SOP markdown file reference the item_id (best-effort path scan)? "
        "matched | unmatched.",
    )
    mirror_coverage_status: Literal["covered_by_emit", "mirror_skip"] = Field(
        default="covered_by_emit",
        description="Mirror coverage status. By construction of compliance_mirror_emit, every "
        "process_list row lands in compliance.process_list_mirror unless explicitly "
        "marked mirror_skip (forward-charter to a future commit when relevant).",
    )
    audience_tags_status: Literal["matched", "deferred"] = Field(
        default="deferred",
        description="Audience-tag coverage via I85 AUDIENCE_REGISTRY join. P1 baseline defers "
        "this for every row pending I85 P1 stabilization + an explicit wire commit.",
    )
    cadence_status: Literal["declared", "undeclared"] = Field(
        ...,
        description="Does process_list.csv cadence_type cell carry one of the 4 canonical "
        "values (on_demand / scheduled / event_triggered / gated_operator)? declared | undeclared.",
    )

    # --- aggregated row-level verdict + gap summary --------------------------
    verdict: KbIntegrityVerdict = Field(
        ...,
        description="Deterministic aggregation per compute_verdict() — pass when all 5 signals "
        "are good; fail when mirror_coverage_status is mirror_skip; partial otherwise.",
    )
    gap_summary: str = Field(
        default="",
        description="One-line summary of which coverage signals are missing (semicolon-separated). "
        "Empty when verdict=pass.",
    )

    @staticmethod
    def compute_verdict(
        knowledge_pairing_status: str,
        paired_sop_status: str,
        mirror_coverage_status: str,
        audience_tags_status: str,
        cadence_status: str,
    ) -> tuple[KbIntegrityVerdict, str]:
        """Deterministic verdict + gap-summary aggregator.

        Returns the verdict + a one-line semicolon-separated gap summary.
        Used by the audit script + tests; pure function over the 5 signal values.
        """
        if mirror_coverage_status == "mirror_skip":
            return ("fail", "mirror_skip (intentional or sync-flow gap)")
        gaps: list[str] = []
        if knowledge_pairing_status != "matched":
            gaps.append("knowledge_pairing")
        if paired_sop_status != "matched":
            gaps.append("paired_sop")
        if audience_tags_status != "matched":
            gaps.append("audience_tags_deferred")
        if cadence_status != "declared":
            gaps.append("cadence_undeclared")
        if not gaps:
            return ("pass", "")
        return ("partial", ";".join(gaps))


# -----------------------------------------------------------------------------
# Audit summary model
# -----------------------------------------------------------------------------


class KbIntegrityAuditSummary(BaseModel):
    """Audit-level summary across all KbIntegrityMatrixRow rows per I81 P1.

    Mirrors the canonical PASS-threshold contract per D-IH-81-F: ≥ 95% pass
    rate gates I81 closure at P9. P1 baseline emits the snapshot; P4-P8
    retrofit waves move the needle.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    matrix_csv_path: str = Field(..., min_length=1)
    audit_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    executable_row_count: int = Field(..., ge=0)
    pass_count: int = Field(..., ge=0)
    partial_count: int = Field(..., ge=0)
    fail_count: int = Field(..., ge=0)
    pass_rate: float = Field(..., ge=0.0, le=1.0)
    pass_threshold: float = Field(default=0.95, ge=0.0, le=1.0)
    meets_threshold: bool
    knowledge_pairing_matched_count: int = Field(..., ge=0)
    paired_sop_matched_count: int = Field(..., ge=0)
    audience_tags_deferred_count: int = Field(..., ge=0)
    cadence_undeclared_count: int = Field(..., ge=0)
    top_gap_signals: tuple[str, ...] = Field(
        default=(),
        description="Top gap signals in descending count order; surface for the audit narrative.",
    )
    notes: str | None = None


__all__ = [
    "ITEM_ID_RE",
    "KbCoverageStatus",
    "KbExecutableGranularity",
    "KbIntegrityAuditSummary",
    "KbIntegrityMatrixRow",
    "KbIntegrityVerdict",
]


# -----------------------------------------------------------------------------
# Repo-root path helpers (re-exported for the audit script + tests)
# -----------------------------------------------------------------------------


def repo_root() -> Path:
    """Repo root resolved relative to this module's location."""
    return Path(__file__).resolve().parent.parent


PROCESS_LIST_REL = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
)
KNOWLEDGE_PAIRING_REL = (
    "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/"
    "dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv"
)
SOP_SCAN_ROOT_REL = "docs/references/hlk/v3.0"
