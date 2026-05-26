#!/usr/bin/env python3
"""Umbrella validator for the 5 Collaborator-Share canonical CSVs (Wave R+1 Commit 2b).

Canonical doctrine:
  ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md``
Pydantic SSOT:
  ``akos/hlk_collaborator_share.py``
Paired runbook:
  ``scripts/collaborator_share_calculate.py``
Companion cursor rule (Commit 2c):
  ``.cursor/rules/akos-collaborator-share.mdc``
Companion skill (Commit 2c):
  ``.cursor/skills/collaborator-share-craft/SKILL.md``
Decision lineage:
  D-IH-86-DA (formula-c-hybrid TRUE-MARGIN), D-IH-86-DB
  (clause-c-recommended-table partner-overlap clause register),
  D-IH-86-DC (rate-b-governed-override market-rate + override registers),
  D-IH-86-DE (Wave R+1 Commit 2b-ext: share_pattern enum extension to
  cover deep_partner_65_35 + orchestration_broker_thin_margin + custom).

Checks (8 CS-* probes; mirrors doctrine §5):

  CS-01 STRUCTURAL VALIDATION
    Header drift + per-row Pydantic instantiation across all 5 CSVs.
    FAIL on any structural error (header mismatch / Pydantic ValidationError /
    duplicate primary key).

  CS-02 CROSS-CSV FK RESOLUTION
    HOLISTIKA_VENDOR_SERVICES_BILLED.engagement_id      -> SHARE_REGISTRY.engagement_id
    HOLISTIKA_VENDOR_SERVICES_BILLED.justification_clause_id (non-empty)
                                                        -> PARTNER_OVERLAP_EXCLUSION_CLAUSES.clause_id
    COLLABORATOR_RATE_OVERRIDES.engagement_id           -> SHARE_REGISTRY.engagement_id
    COLLABORATOR_RATE_OVERRIDES.reference_rate_id (non-empty)
                                                        -> COLLABORATOR_MARKET_RATE_REFERENCE.rate_id
    Empty CSVs (header-only) trivially pass.

  CS-03 SPLIT SUMS TO 100
    Unified across-rows sum-to-100 invariant per engagement_id (covers
    all 4 base patterns + 1 overlay per the rewritten doctrine §6).
    For every engagement_id, the sum of (holistika_share_pct +
    collaborator_share_pct) across all SHARE_REGISTRY rows (base + any
    overlay sibling) must equal exactly 100. FAIL on deviation.

    Pattern composition examples:
      - deep_partner_65_35 (solo): 1 row, 65/35 -> sum 100.
      - bd_intro_only: 2 rows, (85/0) holistika-corp + (0/15) BD partner
        -> across-rows sum 100.
      - joint_venture_aventure: 2 rows, (50/0) + (0/50) -> sum 100.
      - consulting_direct (solo): 1 row, 100/0 -> sum 100.
      - consulting_direct + bd_commission_overlay: 2 rows, (85/0) base
        + (0/15) overlay -> sum 100.
      - deep_partner_65_35 + bd_commission_overlay: NOT a clean default
        (base 65/35 + overlay 0/15 = 115); requires an OVERRIDE row
        adjusting one of the slices to land on 100.

  CS-04 DEFAULT-SPLIT AUDIT
    Per-engagement composition-based audit. Each engagement is
    classified by (a) number of rows + (b) presence of overlay; the
    appropriate per-pattern default-anchor helper(s) are applied to
    each row. Any deviation requires a non-empty
    ``share_override_decision_id`` on the deviating row.

    Solo engagement (1 row, no overlay):
      - deep_partner_65_35: anchor (65/35) per ``default_split_holds``.
      - bd_intro_only: anchor (85/15) per ``bd_intro_default_split_holds``.
      - joint_venture_aventure: anchor (50/50) per
        ``joint_venture_default_split_holds``.
      - consulting_direct: anchor (100/0) per
        ``consulting_direct_solo_default_holds``.

    Multi-row engagement, no overlay (bd_intro_only OR
    joint_venture_aventure shape): each row must match ONE of the
    two distributed-default anchors for the pattern, e.g. (85/0) OR
    (0/15) for bd_intro_only; (50/0) OR (0/50) for joint_venture.

    Multi-row engagement with overlay (overlay row carries
    ``share_overlay`` non-empty):
      - base row anchor depends on base pattern:
        * consulting_direct base: (85/0) per
          ``consulting_direct_with_overlay_default_holds``.
        * deep_partner_65_35 base: NO default anchor (combining 65/35
          base with 0/15 overlay = 115; the base row MUST carry an
          override).
      - overlay row anchor: (0/15) per
        ``bd_commission_overlay_default_holds``.

    WARN at INFO ramp; FAIL on --strict.

  CS-05 BILL_MODE DEFAULT CONSISTENCY
    Every HOLISTIKA_VENDOR_SERVICES_BILLED row whose ``bill_mode`` deviates
    from ``DEFAULT_BILL_MODE_PER_SERVICE_CLASS[service_class]`` must carry a
    non-empty ``bill_mode_decision_id`` FK. WARN at INFO ramp;
    FAIL on --strict.

  CS-06 RATE WITHIN MARKET BAND
    Every SHARE_REGISTRY row's ``collaborator_billed_rate`` should sit within
    +/- MARKET_RATE_VARIANCE_TOLERANCE_PCT of the typical rate in
    COLLABORATOR_MARKET_RATE_REFERENCE for the matching role_class. Rates
    outside the band must be backed by a matching
    COLLABORATOR_RATE_OVERRIDES row with override_kind=market_rate_excursion.
    WARN at INFO ramp; FAIL on --strict.

  CS-07 OVERRIDE EXPIRY AUDIT
    Every COLLABORATOR_RATE_OVERRIDES row with ``expires_at`` in the past
    must carry status=expired (not status=active). WARN advisory only;
    auto-remediation candidate.

  CS-08 SHARE PATTERN + OVERLAY + METHODOLOGY ENUM VALIDITY
    Every SHARE_REGISTRY row's ``share_pattern`` value must be a member
    of VALID_SHARE_PATTERNS ({deep_partner_65_35, bd_intro_only,
    joint_venture_aventure, consulting_direct}). When non-empty, the
    ``share_overlay`` value must be a member of VALID_SHARE_OVERLAYS
    ({bd_commission_overlay}). The ``methodology_readiness`` value
    must be a member of VALID_METHODOLOGY_READINESS
    ({methodology_trained, methodology_in_progress, methodology_naive,
    methodology_not_applicable}). FAIL on any unknown value.

    Extended at Wave R+2 Commit 3 per D-IH-86-EJ/EM/EN (operator
    ratification 2026-05-25/26) to cover the 3 enum surfaces
    introduced by the 4-base + 1-overlay rewrite.

  CS-09 OVERLAY-BASE PAIRING + METHODOLOGY-PATTERN COHERENCE
    Two layered checks introduced at Wave R+2 Commit 3 per
    D-IH-86-EJ + D-IH-86-EN:
      (a) overlay-base pairing: any row with non-empty
          ``share_overlay`` must have at least one sibling base row
          at the same engagement_id whose ``share_pattern`` is in
          VALID_OVERLAY_BASE_PAIRINGS[share_overlay]. Forbidden
          pairings (e.g., bd_commission_overlay paired with
          bd_intro_only OR joint_venture_aventure) FAIL.
      (b) methodology-pattern coherence: any row whose
          ``share_pattern`` is NOT in
          METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS[methodology_readiness]
          FAILs. Catches the "35% compromise to bridge a methodology
          gap" failure mode operator named verbatim 2026-05-26.

Posture per D-IH-86-DA quintet (Wave R+1 P3 mint INFO ramp):

  --self-test  : Pydantic-fixture validation; zero CI cost; always exits 0
                 on PASS. Wired into release-gate.py + pre_commit profile.
  (no args)    : run full 7-check audit; emit per-check summary to stdout;
                 exit 0 (INFO posture during Wave R+1 backfill window).
  --strict     : run full audit; exit non-zero if any FAIL (CS-01..03) OR
                 WARN that the doctrine has promoted to FAIL ramp.
  --report PATH : also write a markdown audit report at PATH (analogous to
                  baseline_index_sweep.py --output).

When invoked without --json, output is a human-readable summary matching the
validate_*.py convention used by validate_hlk.py dispatcher.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import logging
import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_collaborator_share import (  # noqa: E402
    COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES,
    COLLABORATOR_RATE_OVERRIDES_FIELDNAMES,
    COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
    CSV_PATH_RELATIVE_MARKET_RATE,
    CSV_PATH_RELATIVE_OVERLAP_CLAUSES,
    CSV_PATH_RELATIVE_RATE_OVERRIDES,
    CSV_PATH_RELATIVE_SHARE_REGISTRY,
    CSV_PATH_RELATIVE_VENDOR_BILLED,
    DEFAULT_BD_COMMISSION_OVERLAY_PCT,
    DEFAULT_BD_INTRO_COLLABORATOR_PCT,
    DEFAULT_BD_INTRO_HOLISTIKA_PCT,
    DEFAULT_BILL_MODE_PER_SERVICE_CLASS,
    DEFAULT_COLLABORATOR_SHARE_PCT,
    DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO,
    DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO,
    DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY,
    DEFAULT_HOLISTIKA_SHARE_PCT,
    DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT,
    DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT,
    DEFAULT_SHARE_PATTERN,
    HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
    MARKET_RATE_VARIANCE_TOLERANCE_PCT,
    PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
    VALID_COLLABORATOR_SHARE_CHECK_CODES,
    VALID_METHODOLOGY_READINESS,
    VALID_OVERLAY_BASE_PAIRINGS,
    VALID_SHARE_OVERLAYS,
    VALID_SHARE_PATTERNS,
    CollaboratorMarketRateReferenceRow,
    CollaboratorRateOverrideRow,
    CollaboratorShareAuditReport,
    CollaboratorShareAuditRow,
    CollaboratorShareRegistryRow,
    HolistikaVendorServicesBilledRow,
    PartnerOverlapExclusionClauseRow,
    across_rows_sum_to_100,
    bd_commission_overlay_default_holds,
    bd_intro_default_split_holds,
    bill_mode_matches_default,
    consulting_direct_solo_default_holds,
    consulting_direct_with_overlay_default_holds,
    default_split_holds,
    joint_venture_default_split_holds,
    methodology_permits_share_pattern,
    methodology_readiness_is_valid,
    overlay_base_pairing_is_valid,
    rate_within_market_band,
    share_overlay_is_valid,
    share_pattern_is_valid,
)

logger = logging.getLogger(__name__)


# Path constants ---------------------------------------------------------

SHARE_REGISTRY_CSV = REPO_ROOT / CSV_PATH_RELATIVE_SHARE_REGISTRY
VENDOR_BILLED_CSV = REPO_ROOT / CSV_PATH_RELATIVE_VENDOR_BILLED
OVERLAP_CLAUSES_CSV = REPO_ROOT / CSV_PATH_RELATIVE_OVERLAP_CLAUSES
MARKET_RATE_CSV = REPO_ROOT / CSV_PATH_RELATIVE_MARKET_RATE
RATE_OVERRIDES_CSV = REPO_ROOT / CSV_PATH_RELATIVE_RATE_OVERRIDES


# Helpers ----------------------------------------------------------------


def _today() -> str:
    return _dt.date.today().isoformat()


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read rows from a CSV; empty list if missing or header-only."""
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _read_csv_header(path: Path) -> list[str]:
    """Return the header tuple of a CSV; empty list if missing."""
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        try:
            return next(reader)
        except StopIteration:
            return []


def _normalise_row(row: dict[str, str]) -> dict[str, str]:
    """Drop None keys (csv.DictReader artefact) + coerce None values to ''."""
    return {k: (v or "") for k, v in row.items() if k}


# Per-check probes -------------------------------------------------------


def _check_cs01_structural() -> list[CollaboratorShareAuditRow]:
    """CS-01: header drift + Pydantic row validation across all 5 CSVs.

    Empty CSVs (header-only) trivially pass; the check is for the header
    contract + per-row Pydantic instantiation.
    """
    findings: list[CollaboratorShareAuditRow] = []
    csv_specs: list[tuple[str, Path, tuple[str, ...], type]] = [
        (
            "COLLABORATOR_SHARE_REGISTRY",
            SHARE_REGISTRY_CSV,
            COLLABORATOR_SHARE_REGISTRY_FIELDNAMES,
            CollaboratorShareRegistryRow,
        ),
        (
            "HOLISTIKA_VENDOR_SERVICES_BILLED",
            VENDOR_BILLED_CSV,
            HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
            HolistikaVendorServicesBilledRow,
        ),
        (
            "PARTNER_OVERLAP_EXCLUSION_CLAUSES",
            OVERLAP_CLAUSES_CSV,
            PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
            PartnerOverlapExclusionClauseRow,
        ),
        (
            "COLLABORATOR_MARKET_RATE_REFERENCE",
            MARKET_RATE_CSV,
            COLLABORATOR_MARKET_RATE_REFERENCE_FIELDNAMES,
            CollaboratorMarketRateReferenceRow,
        ),
        (
            "COLLABORATOR_RATE_OVERRIDES",
            RATE_OVERRIDES_CSV,
            COLLABORATOR_RATE_OVERRIDES_FIELDNAMES,
            CollaboratorRateOverrideRow,
        ),
    ]

    issues = 0
    for label, path, expected_header, row_model in csv_specs:
        rel_path = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        if not path.is_file():
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-01-STRUCTURAL-VALIDATION",
                subject_path=rel_path,
                verdict="fail",
                drift_summary=f"{label}.csv not found at {rel_path}",
                proposed_fix_action="restore CSV from git OR re-seed header per Pydantic chassis",
                severity="high",
                notes="probe cannot complete without the file present",
            ))
            issues += 1
            continue

        header = _read_csv_header(path)
        if list(header) != list(expected_header):
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-01-STRUCTURAL-VALIDATION",
                subject_path=rel_path,
                verdict="fail",
                drift_summary=(
                    f"{label} header mismatch: expected "
                    f"{list(expected_header)} got {list(header)}"
                ),
                proposed_fix_action=(
                    f"align CSV header with akos/hlk_collaborator_share.py "
                    f"{label}_FIELDNAMES tuple (SSOT)"
                ),
                severity="high",
                notes="header drift breaks all downstream FK + Pydantic checks",
            ))
            issues += 1
            continue

        rows = _read_csv_rows(path)
        seen_ids: set[str] = set()
        id_field = expected_header[0]
        for i, raw in enumerate(rows, start=2):
            row = _normalise_row(raw)
            try:
                row_model.model_validate(row)
            except Exception as exc:  # pragma: no cover (Pydantic ValidationError catch-all)
                row_id = row.get(id_field, f"row_{i}")
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-01-STRUCTURAL-VALIDATION",
                    subject_path=rel_path,
                    subject_row_id=row_id,
                    verdict="fail",
                    drift_summary=f"{label} row {i} ({row_id}): {exc!s}"[:1000],
                    proposed_fix_action=(
                        "fix row to match Pydantic chassis: enum membership / "
                        "regex pattern / length bounds / numeric range"
                    ),
                    severity="high",
                    notes=f"Pydantic ValidationError from {row_model.__name__}",
                ))
                issues += 1
                continue
            rid = row.get(id_field, "").strip()
            if rid and rid in seen_ids:
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-01-STRUCTURAL-VALIDATION",
                    subject_path=rel_path,
                    subject_row_id=rid,
                    verdict="fail",
                    drift_summary=f"{label} duplicate primary key {rid!r} (row {i})",
                    proposed_fix_action="remove or rename duplicate row",
                    severity="medium",
                    notes=f"{id_field} must be unique within the CSV",
                ))
                issues += 1
            seen_ids.add(rid)

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-01-STRUCTURAL-VALIDATION",
            subject_path="docs/references/hlk/v3.0/.../People Operations/canonicals/dimensions/",
            verdict="pass",
            severity="low",
            notes=(
                "all 5 CSVs: header match + per-row Pydantic + no duplicate "
                "primary keys (header-only CSVs trivially pass)"
            ),
        ))
    return findings


def _check_cs02_cross_csv_fk() -> list[CollaboratorShareAuditRow]:
    """CS-02: cross-CSV FK resolution across the 5 registers."""
    findings: list[CollaboratorShareAuditRow] = []
    share_rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    vendor_rows = _read_csv_rows(VENDOR_BILLED_CSV)
    clause_rows = _read_csv_rows(OVERLAP_CLAUSES_CSV)
    rate_rows = _read_csv_rows(MARKET_RATE_CSV)
    override_rows = _read_csv_rows(RATE_OVERRIDES_CSV)

    share_engagement_ids = {(r.get("engagement_id") or "").strip() for r in share_rows}
    clause_ids = {(r.get("clause_id") or "").strip() for r in clause_rows}
    rate_ids = {(r.get("rate_id") or "").strip() for r in rate_rows}

    issues = 0

    for i, raw in enumerate(vendor_rows, start=2):
        row = _normalise_row(raw)
        eid = (row.get("engagement_id") or "").strip()
        rid = (row.get("vendor_billing_id") or f"row_{i}").strip()
        if eid and share_engagement_ids and eid not in share_engagement_ids:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-02-CROSS-CSV-FK-RESOLUTION",
                subject_path=str(VENDOR_BILLED_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"vendor row {i} engagement_id={eid!r} not found in "
                    "COLLABORATOR_SHARE_REGISTRY"
                ),
                proposed_fix_action=(
                    "add the missing SHARE_REGISTRY row first OR correct the "
                    "vendor row's engagement_id"
                ),
                severity="medium",
                notes="orphan vendor billing row",
            ))
            issues += 1
        clid = (row.get("justification_clause_id") or "").strip()
        if clid and clause_ids and clid not in clause_ids:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-02-CROSS-CSV-FK-RESOLUTION",
                subject_path=str(VENDOR_BILLED_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"vendor row {i} justification_clause_id={clid!r} not in "
                    "PARTNER_OVERLAP_EXCLUSION_CLAUSES"
                ),
                proposed_fix_action="mint the clause row OR remove the FK reference",
                severity="medium",
                notes="unknown overlap-exclusion clause",
            ))
            issues += 1

    for i, raw in enumerate(override_rows, start=2):
        row = _normalise_row(raw)
        eid = (row.get("engagement_id") or "").strip()
        rid = (row.get("override_id") or f"row_{i}").strip()
        if eid and share_engagement_ids and eid not in share_engagement_ids:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-02-CROSS-CSV-FK-RESOLUTION",
                subject_path=str(RATE_OVERRIDES_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"override row {i} engagement_id={eid!r} not found in "
                    "COLLABORATOR_SHARE_REGISTRY"
                ),
                proposed_fix_action=(
                    "add the missing SHARE_REGISTRY row first OR correct the "
                    "override row's engagement_id"
                ),
                severity="medium",
                notes="orphan override row",
            ))
            issues += 1
        ref_rid = (row.get("reference_rate_id") or "").strip()
        if ref_rid and rate_ids and ref_rid not in rate_ids:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-02-CROSS-CSV-FK-RESOLUTION",
                subject_path=str(RATE_OVERRIDES_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"override row {i} reference_rate_id={ref_rid!r} not in "
                    "COLLABORATOR_MARKET_RATE_REFERENCE"
                ),
                proposed_fix_action="add the market-rate row OR remove the FK reference",
                severity="medium",
                notes="unknown market-rate reference",
            ))
            issues += 1

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-02-CROSS-CSV-FK-RESOLUTION",
            subject_path="cross-csv",
            verdict="pass",
            severity="low",
            notes=(
                f"all FKs resolve: vendor->share ({len(vendor_rows)}) + "
                f"vendor->clause + override->share ({len(override_rows)}) + "
                "override->rate"
            ),
        ))
    return findings


def _group_share_rows_by_engagement(
    rows: list[dict[str, str]],
) -> dict[str, list[tuple[int, dict[str, str]]]]:
    """Group SHARE_REGISTRY rows by engagement_id, preserving (row_no, row)
    pairs for downstream error reporting.

    Row numbering starts at 2 (header on line 1).
    """
    grouped: dict[str, list[tuple[int, dict[str, str]]]] = {}
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        eid = (row.get("engagement_id") or "").strip()
        if not eid:
            continue
        grouped.setdefault(eid, []).append((i, row))
    return grouped


def _safe_share_pcts(row: dict[str, str]) -> tuple[int, int] | None:
    """Parse (holistika_share_pct, collaborator_share_pct) from a row; return
    None if either field is missing / non-integer (CS-01 captures the type
    error)."""
    try:
        h = int(row.get("holistika_share_pct") or "0")
        c = int(row.get("collaborator_share_pct") or "0")
    except ValueError:
        return None
    return (h, c)


def _split_eng_rows_by_overlay(
    eng_rows: list[tuple[int, dict[str, str]]],
) -> tuple[list[tuple[int, dict[str, str]]], list[tuple[int, dict[str, str], str]]]:
    """Partition engagement rows into (base_rows, overlay_rows).

    Base rows have empty ``share_overlay``; overlay rows have non-empty
    ``share_overlay`` and carry the overlay code as the 3rd tuple element
    for downstream pairing checks.
    """
    base_rows: list[tuple[int, dict[str, str]]] = []
    overlay_rows: list[tuple[int, dict[str, str], str]] = []
    for i, r in eng_rows:
        overlay = (r.get("share_overlay") or "").strip()
        if overlay:
            overlay_rows.append((i, r, overlay))
        else:
            base_rows.append((i, r))
    return base_rows, overlay_rows


def _check_cs03_split_sums_to_100() -> list[CollaboratorShareAuditRow]:
    """CS-03: unified across-rows sum-to-100 invariant per engagement_id.

    Per Wave R+2 rewrite (D-IH-86-EJ/EK), CS-03 collapses the prior
    per-pattern split (deep_partner per-row vs orchestration_broker
    across-rows vs custom skip) into a single invariant: for every
    engagement_id, the sum of (holistika_share_pct +
    collaborator_share_pct) across ALL SHARE_REGISTRY rows (base + any
    overlay sibling) must equal exactly 100.

    The unified invariant covers all 4 base patterns + 1 overlay:

      - deep_partner_65_35 (solo)        : 1 row  -> 65 + 35 = 100
      - bd_intro_only (2-row split)      : (85/0) + (0/15) = 100
      - joint_venture_aventure (2-row)   : (50/0) + (0/50) = 100
      - consulting_direct (solo)         : 1 row  -> 100 + 0 = 100
      - consulting_direct + overlay      : (85/0) + (0/15) = 100
      - deep_partner_65_35 + overlay     : (65/35) + (0/15) = 115 FAIL
        (no clean composition; requires override row reshaping to 100)
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    grouped = _group_share_rows_by_engagement(rows)
    issues = 0

    for eid, eng_rows in grouped.items():
        pct_pairs: list[tuple[int, int]] = []
        any_invalid = False
        for _i, r in eng_rows:
            pcts = _safe_share_pcts(r)
            if pcts is None:
                any_invalid = True
                break
            pct_pairs.append(pcts)
        if any_invalid or not pct_pairs:
            # CS-01 surfaces the structural defect; CS-03 skips silently.
            continue
        if across_rows_sum_to_100(pct_pairs):
            continue
        total_h = sum(p[0] for p in pct_pairs)
        total_c = sum(p[1] for p in pct_pairs)
        row_ids = ", ".join(
            (r.get("share_id") or f"row_{i}").strip()
            for i, r in eng_rows
        )
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-03-SPLIT-SUMS-TO-100",
            subject_path=rel_path,
            subject_row_id=eid,
            verdict="fail",
            drift_summary=(
                f"engagement {eid!r}: across-rows total {total_h}% "
                f"Holistika + {total_c}% collaborator = {total_h + total_c}% "
                f"(must be 100); rows {row_ids}"
            ),
            proposed_fix_action=(
                "adjust per-row share_pct values so cross-row sum equals "
                "100; covers all 4 base patterns + 1 overlay per "
                "doctrine §6 (deep_partner+overlay needs an override row "
                "reshaping the composition)"
            ),
            severity="high",
            notes=(
                "unified across-rows invariant per Wave R+2 rewrite "
                "(D-IH-86-EJ/EK); supersedes the prior per-pattern "
                "branched logic (deep_partner per-row + orchestration "
                "across-rows + custom skip)"
            ),
        ))
        issues += 1

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-03-SPLIT-SUMS-TO-100",
            subject_path=rel_path,
            verdict="pass",
            severity="low",
            notes=(
                f"all {len(grouped)} engagement(s) respect the unified "
                "across-rows sum-to-100 invariant (4 base patterns + "
                "1 overlay; per doctrine §6 Wave R+2 rewrite)"
            ),
        ))
    return findings


def _check_cs04_default_split_audit() -> list[CollaboratorShareAuditRow]:
    """CS-04: composition-based default-split audit per base pattern + overlay.

    Per Wave R+2 rewrite (D-IH-86-EJ/EL), CS-04 branches on (a) the
    base ``share_pattern`` resolved at engagement scope and (b) the
    presence/absence of a ``share_overlay`` sibling row. For each
    engagement, the appropriate per-pattern + per-composition default-
    anchor helper(s) are applied. Any deviation requires a non-empty
    ``share_override_decision_id`` on the deviating row(s).

    Composition table (per doctrine §6 Wave R+2):

      bd_intro_only (multi-row): aggregate must hold (85/15);
        helper = ``bd_intro_default_split_holds``.
      joint_venture_aventure (multi-row): aggregate must hold (50/50);
        helper = ``joint_venture_default_split_holds``.
      consulting_direct (solo, no overlay): row must hold (100/0);
        helper = ``consulting_direct_solo_default_holds``.
      consulting_direct + bd_commission_overlay: base row must hold
        (85/0) per ``consulting_direct_with_overlay_default_holds``;
        overlay row must hold (0/15) per
        ``bd_commission_overlay_default_holds``.
      deep_partner_65_35 (solo, no overlay): row must hold (65/35);
        helper = ``default_split_holds``.
      deep_partner_65_35 + bd_commission_overlay: NO clean default
        (composition sum = 115); base row MUST carry an override
        decision regardless of value.

    Verdict: WARN at INFO ramp; FAIL on --strict.
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    grouped = _group_share_rows_by_engagement(rows)
    issues = 0

    for eid, eng_rows in grouped.items():
        base_rows, overlay_rows = _split_eng_rows_by_overlay(eng_rows)
        if not base_rows:
            # Pure-overlay engagement is structurally invalid; CS-09
            # surfaces it (overlay-base pairing). Skip CS-04 silently.
            continue

        # Resolve the base pattern at engagement scope. Mixed patterns
        # within a single engagement are out-of-scope for CS-04 (CS-03 /
        # CS-09 surface the structural defect); skip silently.
        base_patterns = {
            (r.get("share_pattern") or DEFAULT_SHARE_PATTERN).strip()
            for _i, r in base_rows
        }
        if len(base_patterns) != 1:
            continue
        base_pattern = next(iter(base_patterns))
        if not share_pattern_is_valid(base_pattern):
            # CS-08 catches the enum drift; CS-04 cannot branch safely.
            continue
        has_overlay = bool(overlay_rows)

        # Aggregate the base-row percentages (used for multi-row anchors
        # like bd_intro_only + joint_venture_aventure where each row
        # represents one party's slice).
        h_total = sum(int(r.get("holistika_share_pct") or "0") for _i, r in base_rows)
        c_total = sum(int(r.get("collaborator_share_pct") or "0") for _i, r in base_rows)

        # Helper: every base row carries an override -> deviation is
        # operator-ratified; CS-04 passes the engagement.
        base_decision_ids = [
            (r.get("share_override_decision_id") or "").strip()
            for _i, r in base_rows
        ]
        engagement_has_base_override = any(base_decision_ids)

        # Branch per base pattern -----------------------------------------
        if base_pattern == "bd_intro_only":
            if bd_intro_default_split_holds(h_total, c_total):
                pass  # default-clean
            elif engagement_has_base_override:
                pass  # operator-ratified deviation
            else:
                row_ids = ", ".join(
                    (r.get("share_id") or f"row_{i}").strip()
                    for i, r in base_rows
                )
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-04-DEFAULT-65-35-AUDIT",
                    subject_path=rel_path,
                    subject_row_id=eid,
                    verdict="warn",
                    drift_summary=(
                        f"bd_intro_only engagement {eid!r}: aggregate "
                        f"({h_total}/{c_total}) deviates from default "
                        f"({DEFAULT_BD_INTRO_HOLISTIKA_PCT}/"
                        f"{DEFAULT_BD_INTRO_COLLABORATOR_PCT}) without "
                        f"share_override_decision_id on any row "
                        f"({row_ids})"
                    ),
                    proposed_fix_action=(
                        "mint a DECISION_REGISTER row ratifying the "
                        "deviation, then populate "
                        "share_override_decision_id on ≥ 1 base row"
                    ),
                    severity="medium",
                    notes=(
                        "doctrine §6 bd_intro_only aggregate default "
                        "(85/15); INFO at Wave R+2 ramp"
                    ),
                ))
                issues += 1

        elif base_pattern == "joint_venture_aventure":
            if joint_venture_default_split_holds(h_total, c_total):
                pass
            elif engagement_has_base_override:
                pass
            else:
                row_ids = ", ".join(
                    (r.get("share_id") or f"row_{i}").strip()
                    for i, r in base_rows
                )
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-04-DEFAULT-65-35-AUDIT",
                    subject_path=rel_path,
                    subject_row_id=eid,
                    verdict="warn",
                    drift_summary=(
                        f"joint_venture_aventure engagement {eid!r}: "
                        f"aggregate ({h_total}/{c_total}) deviates from "
                        f"default ({DEFAULT_JOINT_VENTURE_HOLISTIKA_PCT}/"
                        f"{DEFAULT_JOINT_VENTURE_COLLABORATOR_PCT}) "
                        f"without share_override_decision_id ({row_ids})"
                    ),
                    proposed_fix_action=(
                        "mint a DECISION_REGISTER row ratifying the "
                        "deviation, then populate "
                        "share_override_decision_id on ≥ 1 base row"
                    ),
                    severity="medium",
                    notes=(
                        "doctrine §6 joint_venture_aventure aggregate "
                        "default (50/50); INFO at Wave R+2 ramp"
                    ),
                ))
                issues += 1

        elif base_pattern == "consulting_direct":
            # Solo (no overlay) vs with-overlay -- different anchors.
            if len(base_rows) != 1:
                # Multi-row consulting_direct is structurally unusual;
                # CS-03 surfaces sum issues. Skip per-row anchor here.
                continue
            i, r = base_rows[0]
            pcts = _safe_share_pcts(r)
            if pcts is None:
                continue
            h, c = pcts
            rid = (r.get("share_id") or f"row_{i}").strip()
            decision_id = (r.get("share_override_decision_id") or "").strip()
            if not has_overlay:
                # Solo consulting_direct anchor: (100/0).
                if consulting_direct_solo_default_holds(h, c):
                    pass
                elif decision_id:
                    pass
                else:
                    findings.append(CollaboratorShareAuditRow(
                        check_code="CS-04-DEFAULT-65-35-AUDIT",
                        subject_path=rel_path,
                        subject_row_id=rid,
                        verdict="warn",
                        drift_summary=(
                            f"consulting_direct solo row {i} ({rid}): "
                            f"({h}/{c}) deviates from default "
                            f"({DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_SOLO}/"
                            f"{DEFAULT_CONSULTING_DIRECT_COLLABORATOR_PCT_SOLO}) "
                            "without share_override_decision_id"
                        ),
                        proposed_fix_action=(
                            "mint a DECISION_REGISTER row ratifying the "
                            "deviation, then populate "
                            "share_override_decision_id"
                        ),
                        severity="medium",
                        notes=(
                            "doctrine §6 consulting_direct solo "
                            "default (100/0); INFO at Wave R+2 ramp"
                        ),
                    ))
                    issues += 1
            else:
                # consulting_direct + overlay -> base anchor (85/0).
                if consulting_direct_with_overlay_default_holds(h, c):
                    pass
                elif decision_id:
                    pass
                else:
                    findings.append(CollaboratorShareAuditRow(
                        check_code="CS-04-DEFAULT-65-35-AUDIT",
                        subject_path=rel_path,
                        subject_row_id=rid,
                        verdict="warn",
                        drift_summary=(
                            f"consulting_direct + overlay base row {i} "
                            f"({rid}): ({h}/{c}) deviates from default "
                            f"({DEFAULT_CONSULTING_DIRECT_HOLISTIKA_PCT_WITH_OVERLAY}"
                            "/0) without share_override_decision_id"
                        ),
                        proposed_fix_action=(
                            "mint a DECISION_REGISTER row ratifying the "
                            "deviation, then populate "
                            "share_override_decision_id"
                        ),
                        severity="medium",
                        notes=(
                            "doctrine §6 consulting_direct+overlay base "
                            "anchor (85/0); INFO at Wave R+2 ramp"
                        ),
                    ))
                    issues += 1

        elif base_pattern == "deep_partner_65_35":
            if len(base_rows) != 1:
                continue
            i, r = base_rows[0]
            pcts = _safe_share_pcts(r)
            if pcts is None:
                continue
            h, c = pcts
            rid = (r.get("share_id") or f"row_{i}").strip()
            decision_id = (r.get("share_override_decision_id") or "").strip()
            if has_overlay:
                # deep_partner + overlay = 115 sum; no clean default.
                # Base row MUST carry an override regardless of value.
                if decision_id:
                    pass
                else:
                    findings.append(CollaboratorShareAuditRow(
                        check_code="CS-04-DEFAULT-65-35-AUDIT",
                        subject_path=rel_path,
                        subject_row_id=rid,
                        verdict="warn",
                        drift_summary=(
                            f"deep_partner_65_35 base row {i} ({rid}) "
                            "paired with bd_commission_overlay: this "
                            "composition has NO clean default "
                            "(65/35 + 0/15 = 115); base row MUST "
                            "carry share_override_decision_id "
                            f"(current: {h}/{c})"
                        ),
                        proposed_fix_action=(
                            "mint a DECISION_REGISTER row ratifying the "
                            "adjusted composition, then populate "
                            "share_override_decision_id on the base row"
                        ),
                        severity="medium",
                        notes=(
                            "doctrine §6 deep_partner+overlay has no "
                            "clean default per pattern composition table"
                        ),
                    ))
                    issues += 1
            else:
                # Solo deep_partner anchor: (65/35).
                if default_split_holds(h, c):
                    pass
                elif decision_id:
                    pass
                else:
                    findings.append(CollaboratorShareAuditRow(
                        check_code="CS-04-DEFAULT-65-35-AUDIT",
                        subject_path=rel_path,
                        subject_row_id=rid,
                        verdict="warn",
                        drift_summary=(
                            f"deep_partner_65_35 solo row {i} ({rid}): "
                            f"({h}/{c}) deviates from default "
                            f"({DEFAULT_HOLISTIKA_SHARE_PCT}/"
                            f"{DEFAULT_COLLABORATOR_SHARE_PCT}) without "
                            "share_override_decision_id"
                        ),
                        proposed_fix_action=(
                            "mint a DECISION_REGISTER row ratifying the "
                            "deviation, then populate "
                            "share_override_decision_id"
                        ),
                        severity="medium",
                        notes=(
                            "doctrine §6 deep_partner_65_35 solo "
                            "default (65/35); INFO at Wave R+2 ramp"
                        ),
                    ))
                    issues += 1

        # Overlay-row default audit ---------------------------------------
        # Independent of base pattern: every bd_commission_overlay row
        # should hold (0/15) unless an override is present.
        for i, r, overlay_kind in overlay_rows:
            if overlay_kind != "bd_commission_overlay":
                # CS-08 catches unknown overlay enum values; skip here.
                continue
            pcts = _safe_share_pcts(r)
            if pcts is None:
                continue
            h, c = pcts
            rid = (r.get("share_id") or f"row_{i}").strip()
            decision_id = (r.get("share_override_decision_id") or "").strip()
            if bd_commission_overlay_default_holds(h, c):
                continue
            if decision_id:
                continue
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-04-DEFAULT-65-35-AUDIT",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="warn",
                drift_summary=(
                    f"bd_commission_overlay row {i} ({rid}): ({h}/{c}) "
                    f"deviates from default (0/"
                    f"{DEFAULT_BD_COMMISSION_OVERLAY_PCT}) without "
                    "share_override_decision_id"
                ),
                proposed_fix_action=(
                    "mint a DECISION_REGISTER row ratifying the overlay "
                    "deviation, then populate share_override_decision_id"
                ),
                severity="medium",
                notes=(
                    "doctrine §6 bd_commission_overlay anchor (0/15); "
                    "INFO at Wave R+2 ramp"
                ),
            ))
            issues += 1

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-04-DEFAULT-65-35-AUDIT",
            subject_path=rel_path,
            verdict="pass",
            severity="low",
            notes=(
                f"all {len(rows)} SHARE_REGISTRY rows across "
                f"{len(grouped)} engagement(s) respect composition-based "
                "default-split audit (4 base patterns + 1 overlay per "
                "doctrine §6 Wave R+2 rewrite)"
            ),
        ))
    return findings


def _check_cs05_bill_mode_default() -> list[CollaboratorShareAuditRow]:
    """CS-05: bill_mode deviations from default must carry decision FK."""
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(VENDOR_BILLED_CSV)
    issues = 0
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        rid = (row.get("vendor_billing_id") or f"row_{i}").strip()
        sc = (row.get("holistika_service_class") or "").strip()
        bm = (row.get("bill_mode") or "").strip()
        if not sc or not bm:
            continue
        if sc not in DEFAULT_BILL_MODE_PER_SERVICE_CLASS:
            continue  # CS-01 captures unknown enum
        if bill_mode_matches_default(sc, bm):
            continue
        decision_id = (row.get("bill_mode_decision_id") or "").strip()
        if not decision_id:
            default_bm = DEFAULT_BILL_MODE_PER_SERVICE_CLASS[sc]
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-05-BILL-MODE-DEFAULT-CONSISTENCY",
                subject_path=str(VENDOR_BILLED_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
                subject_row_id=rid,
                verdict="warn",
                drift_summary=(
                    f"vendor row {i} ({rid}): service_class={sc} default "
                    f"bill_mode={default_bm} but row uses bill_mode={bm} "
                    "without bill_mode_decision_id"
                ),
                proposed_fix_action=(
                    "either align bill_mode with default OR mint a "
                    "DECISION_REGISTER row + populate bill_mode_decision_id"
                ),
                severity="medium",
                notes="doctrine §2.2 deviation gate; INFO at Wave R+1",
            ))
            issues += 1
    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-05-BILL-MODE-DEFAULT-CONSISTENCY",
            subject_path=str(VENDOR_BILLED_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
            verdict="pass",
            severity="low",
            notes=(
                f"all {len(rows)} vendor rows either default bill_mode or "
                "carry bill_mode_decision_id"
            ),
        ))
    return findings


def _check_cs06_rate_within_market_band() -> list[CollaboratorShareAuditRow]:
    """CS-06: collaborator_billed_rate within +/- tolerance of typical rate."""
    findings: list[CollaboratorShareAuditRow] = []
    share_rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rate_rows = _read_csv_rows(MARKET_RATE_CSV)
    override_rows = _read_csv_rows(RATE_OVERRIDES_CSV)

    # Index market-rate references by role_class (first match wins; richer
    # role x region x experience match handled by the runbook on real data)
    typical_by_role: dict[str, float] = {}
    for r in rate_rows:
        rc = (r.get("role_class") or "").strip()
        try:
            typical = float(r.get("rate_typical_per_hour") or "0")
        except ValueError:
            continue
        if rc and typical > 0 and rc not in typical_by_role:
            typical_by_role[rc] = typical

    # Index active market_rate_excursion overrides by engagement_id
    excursion_engagements: set[str] = set()
    for o in override_rows:
        kind = (o.get("override_kind") or "").strip()
        status = (o.get("status") or "").strip()
        if kind == "market_rate_excursion" and status == "active":
            eng = (o.get("engagement_id") or "").strip()
            if eng:
                excursion_engagements.add(eng)

    issues = 0
    for i, raw in enumerate(share_rows, start=2):
        row = _normalise_row(raw)
        rid = (row.get("share_id") or f"row_{i}").strip()
        rc = (row.get("collaborator_role_class") or "").strip()
        eng = (row.get("engagement_id") or "").strip()
        try:
            actual = float(row.get("collaborator_billed_rate") or "0")
        except ValueError:
            continue
        if not rc or actual <= 0:
            continue
        typical = typical_by_role.get(rc)
        if typical is None:
            continue  # no reference -> CS-06 skips silently (informational gap)
        if rate_within_market_band(actual, typical):
            continue
        if eng in excursion_engagements:
            continue  # covered by an active override
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-06-RATE-WITHIN-MARKET-BAND",
            subject_path=str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
            subject_row_id=rid,
            verdict="warn",
            drift_summary=(
                f"share row {i} ({rid}): rate={actual} for role={rc} outside "
                f"+/-{MARKET_RATE_VARIANCE_TOLERANCE_PCT}% of typical={typical}; "
                "no active market_rate_excursion override"
            ),
            proposed_fix_action=(
                "either align rate with market band OR mint a "
                "COLLABORATOR_RATE_OVERRIDES row with "
                "override_kind=market_rate_excursion + decision_id FK"
            ),
            severity="medium",
            notes="doctrine §2.3 deviation gate; INFO at Wave R+1",
        ))
        issues += 1

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-06-RATE-WITHIN-MARKET-BAND",
            subject_path=str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
            verdict="pass",
            severity="low",
            notes=(
                f"all {len(share_rows)} share rows either within market band, "
                "covered by active override, or no market-rate reference"
            ),
        ))
    return findings


def _check_cs08_share_pattern_enum() -> list[CollaboratorShareAuditRow]:
    """CS-08: every SHARE_REGISTRY row's share_pattern + share_overlay +
    methodology_readiness must each be a recognised enum value.

    Per-enum semantics:
      * ``share_pattern``: empty OR not in VALID_SHARE_PATTERNS → FAIL
        (this is the per-row commercial-shape declaration; missing it
        means CS-03 + CS-04 cannot branch correctly).
      * ``share_overlay``: empty is valid (no overlay declared);
        non-empty value not in VALID_SHARE_OVERLAYS → FAIL.
      * ``methodology_readiness``: empty OR not in
        VALID_METHODOLOGY_READINESS → FAIL (CS-09 coherence check
        depends on this enum being well-formed).

    Multiple offending enums on a single row each produce their own
    finding so the operator sees the full disposition surface in one
    pass (rather than fixing one and re-running to discover the next).

    Originally introduced at Wave R+1 Commit 2b-ext per D-IH-86-DE
    (share_pattern only). Extended at Wave R+2 Commit 3.3 per
    D-IH-86-EL (3-enum coverage; share_overlay + methodology_readiness
    added alongside the 4-base + 1-overlay model rewrite).
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    issues = 0

    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        rid = (row.get("share_id") or f"row_{i}").strip()
        pattern = (row.get("share_pattern") or "").strip()
        overlay = (row.get("share_overlay") or "").strip()
        readiness = (row.get("methodology_readiness") or "").strip()

        # --- share_pattern enum (required; FAIL on empty or unknown) ---
        if not pattern:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-08-SHARE-PATTERN-ENUM-VALIDITY",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"share row {i} ({rid}): share_pattern is empty; must be "
                    f"one of {sorted(VALID_SHARE_PATTERNS)}"
                ),
                proposed_fix_action=(
                    f"populate share_pattern with the closest matching enum "
                    f"value (default: {DEFAULT_SHARE_PATTERN})"
                ),
                severity="high",
                notes="enum membership prerequisite for CS-03 + CS-04 branching",
            ))
            issues += 1
        elif not share_pattern_is_valid(pattern):
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-08-SHARE-PATTERN-ENUM-VALIDITY",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"share row {i} ({rid}): share_pattern={pattern!r} not in "
                    f"{sorted(VALID_SHARE_PATTERNS)}"
                ),
                proposed_fix_action=(
                    "either correct the typo OR extend VALID_SHARE_PATTERNS "
                    "+ doctrine §2.3 with a new pattern (operator-gated)"
                ),
                severity="high",
                notes=(
                    "unknown share_pattern values break CS-03 sum-to-100 + "
                    "CS-04 default-audit branching"
                ),
            ))
            issues += 1

        # --- share_overlay enum (optional; FAIL only on unknown non-empty) ---
        if overlay and not share_overlay_is_valid(overlay):
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-08-SHARE-PATTERN-ENUM-VALIDITY",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"share row {i} ({rid}): share_overlay={overlay!r} not in "
                    f"{sorted(VALID_SHARE_OVERLAYS)} (empty is valid)"
                ),
                proposed_fix_action=(
                    "either clear share_overlay (no overlay declared) OR "
                    "extend VALID_SHARE_OVERLAYS + doctrine §2.3 with a new "
                    "overlay code (operator-gated)"
                ),
                severity="high",
                notes=(
                    "unknown share_overlay values break CS-09 overlay-base "
                    "pairing validity check"
                ),
            ))
            issues += 1

        # --- methodology_readiness enum (required; FAIL on empty or unknown) ---
        if not readiness:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-08-SHARE-PATTERN-ENUM-VALIDITY",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"share row {i} ({rid}): methodology_readiness is empty; "
                    f"must be one of {sorted(VALID_METHODOLOGY_READINESS)}"
                ),
                proposed_fix_action=(
                    "populate methodology_readiness with the operator-ratified "
                    "value (default for new collaborators: methodology_naive)"
                ),
                severity="high",
                notes=(
                    "enum membership prerequisite for CS-09 methodology-pattern "
                    "coherence check"
                ),
            ))
            issues += 1
        elif not methodology_readiness_is_valid(readiness):
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-08-SHARE-PATTERN-ENUM-VALIDITY",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"share row {i} ({rid}): methodology_readiness="
                    f"{readiness!r} not in "
                    f"{sorted(VALID_METHODOLOGY_READINESS)}"
                ),
                proposed_fix_action=(
                    "either correct the typo OR extend "
                    "VALID_METHODOLOGY_READINESS + doctrine §2.4 with a new "
                    "readiness value (operator-gated)"
                ),
                severity="high",
                notes=(
                    "unknown methodology_readiness values break CS-09 "
                    "coherence check"
                ),
            ))
            issues += 1

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-08-SHARE-PATTERN-ENUM-VALIDITY",
            subject_path=rel_path,
            verdict="pass",
            severity="low",
            notes=(
                f"all {len(rows)} SHARE_REGISTRY rows carry valid "
                f"share_pattern + share_overlay + methodology_readiness "
                f"enum values"
            ),
        ))
    return findings


def _check_cs09_overlay_base_pairing_validity() -> list[CollaboratorShareAuditRow]:
    """CS-09: overlay rows must pair with a permissible base share_pattern
    (per VALID_OVERLAY_BASE_PAIRINGS) AND every row's
    methodology_readiness must permit its share_pattern (per
    METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS).

    Two layered audit lanes:

      (a) **Overlay-base pairing.** For each overlay row in an
          engagement, verify that AT LEAST ONE sibling base row at the
          same engagement_id carries a share_pattern permitted by
          VALID_OVERLAY_BASE_PAIRINGS[overlay_code]. Missing or
          mis-paired base anchors produce a FAIL: an overlay without a
          permissible base is structurally meaningless (overlays add
          economic mass on top of a base; they cannot exist alone).

      (b) **Methodology-pattern coherence.** For each row, verify the
          collaborator's declared methodology_readiness state permits
          the row's share_pattern via methodology_permits_share_pattern.
          A methodology_naive collaborator anchoring at
          deep_partner_65_35 is the canonical violation (the 35%
          collaborator share presumes methodology contribution; a naive
          collaborator cannot fulfil the doctrinal premise).

    Rows where CS-08 already flagged the share_pattern /
    share_overlay / methodology_readiness enum as invalid are skipped
    by this check — CS-08 catches enum membership; CS-09 catches
    semantic coherence between well-formed enums.

    Added at Wave R+2 Commit 3.3 per D-IH-86-EL alongside the 4-base
    + 1-overlay model rewrite. Per RULE 5 INFO-ramp posture: launches
    at FAIL severity for FAIL findings (the structural-incoherence
    findings are not tolerable) but the validator overall stays at
    INFO ramp until Stage 2 promotion criteria met.
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    issues = 0

    # Group by engagement for the overlay-base pairing pass.
    grouped = _group_share_rows_by_engagement([_normalise_row(r) for r in rows])

    # --- Lane A: overlay-base pairing per engagement ---
    for engagement_id, eng_rows in sorted(grouped.items()):
        base_rows, overlay_rows = _split_eng_rows_by_overlay(eng_rows)

        # Collect valid base share_patterns for this engagement (skip
        # rows with invalid share_pattern enum; CS-08 already flagged them).
        base_patterns: list[str] = []
        for _i, base_row in base_rows:
            pat = (base_row.get("share_pattern") or "").strip()
            if pat and share_pattern_is_valid(pat):
                base_patterns.append(pat)

        for line_no, overlay_row, overlay_code in overlay_rows:
            rid = (overlay_row.get("share_id") or f"row_{line_no}").strip()

            # CS-08 will have flagged unknown overlay codes; skip here.
            if not share_overlay_is_valid(overlay_code):
                continue

            # No base rows for this engagement → overlay floats alone.
            if not base_patterns:
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
                    subject_path=rel_path,
                    subject_row_id=rid,
                    verdict="fail",
                    drift_summary=(
                        f"share row {line_no} ({rid}): share_overlay="
                        f"{overlay_code!r} declared but engagement "
                        f"{engagement_id!r} has zero base rows; overlay "
                        f"cannot exist without a permissible base anchor"
                    ),
                    proposed_fix_action=(
                        "either author the missing base row (one of "
                        f"{sorted(VALID_OVERLAY_BASE_PAIRINGS.get(overlay_code, frozenset()))}) "
                        "OR remove the overlay row if no base applies"
                    ),
                    severity="high",
                    notes=(
                        "overlay rows add economic mass on top of a base; "
                        "they are structurally meaningless without one"
                    ),
                ))
                issues += 1
                continue

            # Validate pairing: at least one base must be in the
            # permitted set for this overlay code.
            if not overlay_base_pairing_is_valid(overlay_code, base_patterns):
                permitted = sorted(
                    VALID_OVERLAY_BASE_PAIRINGS.get(overlay_code, frozenset())
                )
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
                    subject_path=rel_path,
                    subject_row_id=rid,
                    verdict="fail",
                    drift_summary=(
                        f"share row {line_no} ({rid}): share_overlay="
                        f"{overlay_code!r} pairs with engagement "
                        f"{engagement_id!r} base patterns={base_patterns} "
                        f"but only {permitted} are permitted"
                    ),
                    proposed_fix_action=(
                        f"either change the base share_pattern to one of "
                        f"{permitted} OR remove the overlay row OR amend "
                        "VALID_OVERLAY_BASE_PAIRINGS in akos/hlk_collaborator_share.py "
                        "+ doctrine §2.3 (operator-gated)"
                    ),
                    severity="high",
                    notes=(
                        "incompatible overlay-base pairing breaks the "
                        "doctrinal overlay-stacking model"
                    ),
                ))
                issues += 1

    # --- Lane B: methodology-pattern coherence per row ---
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        rid = (row.get("share_id") or f"row_{i}").strip()
        pattern = (row.get("share_pattern") or "").strip()
        readiness = (row.get("methodology_readiness") or "").strip()

        # CS-08 already flags missing/unknown enums; skip incoherent rows
        # here so we don't double-report the same defect.
        if not pattern or not share_pattern_is_valid(pattern):
            continue
        if not readiness or not methodology_readiness_is_valid(readiness):
            continue

        if not methodology_permits_share_pattern(readiness, pattern):
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"share row {i} ({rid}): methodology_readiness="
                    f"{readiness!r} does not permit share_pattern="
                    f"{pattern!r} per "
                    "METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS"
                ),
                proposed_fix_action=(
                    "either (a) revise share_pattern to one permitted by the "
                    "collaborator's current readiness, OR (b) advance the "
                    "collaborator's methodology_readiness (e.g., to "
                    "methodology_in_progress or methodology_trained) via a "
                    "ratified onboarding milestone, OR (c) author a "
                    "share_override_decision_id in COLLABORATOR_RATE_OVERRIDES "
                    "with operator narrative justifying the deviation"
                ),
                severity="high",
                notes=(
                    "methodology-pattern coherence is the structural "
                    "premise of the share-split commercial logic"
                ),
            ))
            issues += 1

    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-09-OVERLAY-BASE-PAIRING-VALIDITY",
            subject_path=rel_path,
            verdict="pass",
            severity="low",
            notes=(
                f"all {len(rows)} SHARE_REGISTRY rows: overlay rows pair "
                f"with permissible bases AND every row's "
                f"methodology_readiness permits its share_pattern"
            ),
        ))
    return findings


def _check_cs07_override_expiry() -> list[CollaboratorShareAuditRow]:
    """CS-07: active overrides past expires_at must flip to status=expired."""
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(RATE_OVERRIDES_CSV)
    today = _today()
    issues = 0
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        rid = (row.get("override_id") or f"row_{i}").strip()
        status = (row.get("status") or "").strip()
        expires_at = (row.get("expires_at") or "").strip()
        if not expires_at:
            continue  # no expiry policy on this row
        if status == "active" and expires_at < today:
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-07-OVERRIDE-EXPIRY-AUDIT",
                subject_path=str(RATE_OVERRIDES_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
                subject_row_id=rid,
                verdict="warn",
                drift_summary=(
                    f"override row {i} ({rid}): expires_at={expires_at} (past); "
                    f"status=active (should be expired)"
                ),
                proposed_fix_action="flip status to expired (auto-remediation candidate)",
                severity="low",
                notes="advisory; runbook may auto-remediate in a future cycle",
            ))
            issues += 1
    if issues == 0:
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-07-OVERRIDE-EXPIRY-AUDIT",
            subject_path=str(RATE_OVERRIDES_CSV.relative_to(REPO_ROOT)).replace("\\", "/"),
            verdict="pass",
            severity="low",
            notes=f"all {len(rows)} override rows either unexpired or already status=expired/archived",
        ))
    return findings


# Probe registry ---------------------------------------------------------

CHECK_REGISTRY: dict[str, Callable[[], list[CollaboratorShareAuditRow]]] = {
    "CS-01-STRUCTURAL-VALIDATION": _check_cs01_structural,
    "CS-02-CROSS-CSV-FK-RESOLUTION": _check_cs02_cross_csv_fk,
    "CS-03-SPLIT-SUMS-TO-100": _check_cs03_split_sums_to_100,
    "CS-04-DEFAULT-65-35-AUDIT": _check_cs04_default_split_audit,
    "CS-05-BILL-MODE-DEFAULT-CONSISTENCY": _check_cs05_bill_mode_default,
    "CS-06-RATE-WITHIN-MARKET-BAND": _check_cs06_rate_within_market_band,
    "CS-07-OVERRIDE-EXPIRY-AUDIT": _check_cs07_override_expiry,
    "CS-08-SHARE-PATTERN-ENUM-VALIDITY": _check_cs08_share_pattern_enum,
    "CS-09-OVERLAY-BASE-PAIRING-VALIDITY": _check_cs09_overlay_base_pairing_validity,
}


# Orchestration ----------------------------------------------------------


def run_audit(
    audit_trigger: str = "on_demand",
    audited_by: str = "agent:cli",
) -> CollaboratorShareAuditReport:
    """Run all 9 checks (CS-01..CS-09) and return the aggregate report."""
    all_findings: list[CollaboratorShareAuditRow] = []
    for code in sorted(CHECK_REGISTRY):
        probe = CHECK_REGISTRY[code]
        try:
            all_findings.extend(probe())
        except (OSError, RuntimeError, ValueError) as exc:
            logger.exception("probe %s failed: %s", code, exc)
            all_findings.append(CollaboratorShareAuditRow(
                check_code=code,  # type: ignore[arg-type]
                subject_path="PROBE-INTERNAL-ERROR",
                verdict="fail",
                drift_summary=f"probe raised: {exc!r}",
                proposed_fix_action="investigate validator internals",
                severity="high",
                notes="validator bug; report does not represent audit state",
            ))

    counts = {"pass": 0, "warn": 0, "fail": 0, "skip": 0}
    for f in all_findings:
        counts[f.verdict] = counts.get(f.verdict, 0) + 1

    today = _today()
    return CollaboratorShareAuditReport(
        report_id=f"collaborator-share-audit-{today}",
        audit_trigger=audit_trigger,  # type: ignore[arg-type]
        audited_at=today,
        audited_by=audited_by,
        findings=all_findings,
        pass_count=counts["pass"],
        warn_count=counts["warn"],
        fail_count=counts["fail"],
        skip_count=counts["skip"],
        total_findings=len(all_findings),
    )


def render_markdown(report: CollaboratorShareAuditReport) -> str:
    """Operator-readable markdown table."""
    lines = [
        f"# Collaborator Share Audit — {report.audited_at}",
        "",
        f"- **Report ID**: `{report.report_id}`",
        f"- **Audit trigger**: `{report.audit_trigger}`",
        f"- **Audited by**: `{report.audited_by}`",
        f"- **Total findings**: {report.total_findings} "
        f"(pass={report.pass_count}, warn={report.warn_count}, "
        f"fail={report.fail_count}, skip={report.skip_count})",
        "",
        "## Findings",
        "",
        "| Check | Subject | Verdict | Severity | Drift / proposed fix |",
        "|:---|:---|:---|:---|:---|",
    ]
    for f in report.findings:
        bits: list[str] = []
        if f.drift_summary:
            bits.append(f"**drift:** {f.drift_summary}")
        if f.proposed_fix_action:
            bits.append(f"**fix:** {f.proposed_fix_action}")
        if f.notes:
            bits.append(f"_{f.notes}_")
        rhs = " <br>".join(bits) or "—"
        subject_short = (
            f.subject_path.split("/")[-1] if "/" in f.subject_path
            else f.subject_path
        )
        if f.subject_row_id:
            subject_short = f"{subject_short} [`{f.subject_row_id}`]"
        lines.append(
            f"| `{f.check_code}` | `{subject_short}` | "
            f"{f.verdict} | {f.severity} | {rhs} |"
        )
    lines.append("")
    lines.append(
        "> Generated by `scripts/validate_collaborator_share.py` per "
        "`COLLABORATOR_SHARE_DOCTRINE.md` §5."
    )
    return "\n".join(lines) + "\n"


def self_test() -> int:
    """Pydantic fixture validation; zero-cost; wired into release-gate."""
    fixture = CollaboratorShareAuditRow(
        check_code="CS-01-STRUCTURAL-VALIDATION",
        subject_path="docs/references/.../COLLABORATOR_SHARE_REGISTRY.csv",
        verdict="pass",
        severity="low",
        notes="self-test fixture",
    )
    rep = CollaboratorShareAuditReport(
        report_id=f"collaborator-share-audit-{_today()}-selftest",
        audit_trigger="pre_commit_self_test",
        audited_at=_today(),
        audited_by="self_test",
        findings=[fixture],
        pass_count=1,
        warn_count=0,
        fail_count=0,
        skip_count=0,
        total_findings=1,
    )
    if rep.total_findings != 1 or rep.pass_count != 1:
        return 1
    if len(CHECK_REGISTRY) != 9:
        return 2
    if set(CHECK_REGISTRY.keys()) != VALID_COLLABORATOR_SHARE_CHECK_CODES:
        return 3
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test", action="store_true",
        help="validate Pydantic fixtures; exit 0/non-zero only",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="exit non-zero on any fail/warn (FAIL ramp posture)",
    )
    parser.add_argument(
        "--report", type=Path, default=None,
        help="optional path for the markdown audit report",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="emit JSON report to stdout (machine-readable)",
    )
    parser.add_argument(
        "--audit-trigger",
        choices=["pre_commit_self_test", "csv_mint", "wave_close", "on_demand"],
        default="on_demand",
    )
    parser.add_argument("--audited-by", default="agent:cli")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    if not args.json:
        print("\n  COLLABORATOR_SHARE Validator")
        print("  " + "=" * 50)

    report = run_audit(audit_trigger=args.audit_trigger, audited_by=args.audited_by)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_markdown(report), encoding="utf-8")

    if args.json:
        json.dump(report.model_dump(), sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(
            f"  Total findings: {report.total_findings} "
            f"(pass={report.pass_count}, warn={report.warn_count}, "
            f"fail={report.fail_count}, skip={report.skip_count})"
        )
        for f in report.findings:
            mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL", "skip": "SKIP"}[f.verdict]
            print(f"    [{mark}] {f.check_code}: {f.notes or f.drift_summary or ''}")

    fail_any = report.fail_count > 0
    warn_any = report.warn_count > 0
    if args.strict and (fail_any or warn_any):
        print(
            "  STRICT MODE FAIL: surfaced fail/warn findings; remediate or "
            "escalate per COLLABORATOR_SHARE_DOCTRINE.md §5.",
            file=sys.stderr,
        )
        return 1
    if fail_any:
        # CS-01..03 are structural / invariant; always FAIL even at INFO ramp
        # because they would corrupt downstream calculations.
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
