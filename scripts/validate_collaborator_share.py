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
    Behaviour branches on ``share_pattern``:
      - deep_partner_65_35: per-row holistika_share_pct +
        collaborator_share_pct must equal 100. FAIL on deviation.
      - orchestration_broker_thin_margin: ACROSS-ROWS sum-to-100 invariant
        per engagement_id. The sum of (holistika_share_pct + collaborator_share_pct)
        over all rows sharing the engagement_id must equal exactly 100.
        FAIL on deviation. Catches the "Holistika orchestrates a deal with
        multiple hired collaborators each carrying a slice" shape.
      - custom: per-row check skipped (operator carries the math
        invariant); however every custom row must carry a non-empty
        ``share_override_decision_id`` (also enforced by CS-04).

  CS-04 DEFAULT-SPLIT AUDIT
    Behaviour branches on ``share_pattern``:
      - deep_partner_65_35: every row whose split deviates from the doctrine
        default (DEFAULT_HOLISTIKA_SHARE_PCT,
        DEFAULT_COLLABORATOR_SHARE_PCT) must carry a non-empty
        ``share_override_decision_id`` FK.
      - orchestration_broker_thin_margin: every engagement_id whose total
        Holistika margin deviates from
        ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT (6%) must carry
        ``share_override_decision_id`` on AT LEAST ONE row of the
        engagement.
      - custom: every row must carry ``share_override_decision_id``
        (custom split is by definition non-default and ratify-required).
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

  CS-08 SHARE PATTERN ENUM VALIDITY
    Every SHARE_REGISTRY row's ``share_pattern`` value must be a member of
    VALID_SHARE_PATTERNS ({deep_partner_65_35,
    orchestration_broker_thin_margin, custom}). FAIL on unknown value.
    Added at Wave R+1 Commit 2b-ext per D-IH-86-DE (operator
    ratification Q1-b 2026-05-25).

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
    DEFAULT_BILL_MODE_PER_SERVICE_CLASS,
    DEFAULT_COLLABORATOR_SHARE_PCT,
    DEFAULT_HOLISTIKA_SHARE_PCT,
    DEFAULT_SHARE_PATTERN,
    HOLISTIKA_VENDOR_SERVICES_BILLED_FIELDNAMES,
    MARKET_RATE_VARIANCE_TOLERANCE_PCT,
    ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT,
    PARTNER_OVERLAP_EXCLUSION_CLAUSES_FIELDNAMES,
    VALID_COLLABORATOR_SHARE_CHECK_CODES,
    VALID_SHARE_PATTERNS,
    CollaboratorMarketRateReferenceRow,
    CollaboratorRateOverrideRow,
    CollaboratorShareAuditReport,
    CollaboratorShareAuditRow,
    CollaboratorShareRegistryRow,
    HolistikaVendorServicesBilledRow,
    PartnerOverlapExclusionClauseRow,
    bill_mode_matches_default,
    default_split_holds,
    orchestration_broker_default_margin_holds,
    orchestration_broker_sum_holds,
    rate_within_market_band,
    share_pattern_is_valid,
    split_sums_to_100,
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


def _check_cs03_split_sums_to_100() -> list[CollaboratorShareAuditRow]:
    """CS-03: per-pattern sum-to-100 invariant.

    deep_partner_65_35: per-row sum-to-100.
    orchestration_broker_thin_margin: across-rows sum-to-100 per engagement_id.
    custom: skipped (CS-04 takes responsibility via mandatory override FK).
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    issues = 0
    grouped = _group_share_rows_by_engagement(rows)
    handled_engagement_ids: set[str] = set()

    # Per-row check for deep_partner_65_35 rows -------------------------
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        pattern = (row.get("share_pattern") or DEFAULT_SHARE_PATTERN).strip()
        rid = (row.get("share_id") or f"row_{i}").strip()
        if pattern != "deep_partner_65_35":
            continue
        pcts = _safe_share_pcts(row)
        if pcts is None:
            continue
        h, c = pcts
        if not split_sums_to_100(h, c):
            findings.append(CollaboratorShareAuditRow(
                check_code="CS-03-SPLIT-SUMS-TO-100",
                subject_path=rel_path,
                subject_row_id=rid,
                verdict="fail",
                drift_summary=(
                    f"deep_partner row {i} ({rid}): {h}% + {c}% = {h + c}% "
                    "(must be 100)"
                ),
                proposed_fix_action="adjust the two share_pct values to sum to 100",
                severity="high",
                notes=(
                    "invariant: deep_partner_65_35 closes margin on the row; "
                    "for orchestration shapes use share_pattern="
                    "orchestration_broker_thin_margin"
                ),
            ))
            issues += 1

    # Across-rows check for orchestration_broker_thin_margin engagements --
    for eid, eng_rows in grouped.items():
        patterns = {
            (r.get("share_pattern") or DEFAULT_SHARE_PATTERN).strip()
            for _i, r in eng_rows
        }
        if patterns != {"orchestration_broker_thin_margin"}:
            continue
        pct_pairs: list[tuple[int, int]] = []
        any_invalid = False
        for _i, r in eng_rows:
            pcts = _safe_share_pcts(r)
            if pcts is None:
                any_invalid = True
                break
            pct_pairs.append(pcts)
        if any_invalid or not pct_pairs:
            continue
        handled_engagement_ids.add(eid)
        if not orchestration_broker_sum_holds(pct_pairs):
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
                    f"orchestration engagement {eid!r}: across-rows total "
                    f"{total_h}% Holistika + {total_c}% collaborator = "
                    f"{total_h + total_c}% (must be 100); rows {row_ids}"
                ),
                proposed_fix_action=(
                    "adjust the per-row share_pct values so cross-row sum "
                    "equals 100; doctrine §2.1 orchestration variant"
                ),
                severity="high",
                notes=(
                    "across-rows invariant: orchestration_broker_thin_margin "
                    "spreads the 100% across multiple collaborators"
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
                f"all SHARE_REGISTRY rows respect per-pattern sum-to-100 "
                f"invariant (deep_partner per-row + "
                f"{len(handled_engagement_ids)} orchestration engagements "
                f"across-rows; custom-pattern rows skipped per doctrine §2.1)"
            ),
        ))
    return findings


def _check_cs04_default_split_audit() -> list[CollaboratorShareAuditRow]:
    """CS-04: per-pattern default-split audit.

    deep_partner_65_35: non-default 65/35 row requires share_override_decision_id.
    orchestration_broker_thin_margin: per-engagement Holistika-total deviation
        from 6% requires share_override_decision_id on ≥1 row.
    custom: every row requires share_override_decision_id.
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    issues = 0
    grouped = _group_share_rows_by_engagement(rows)

    # deep_partner_65_35 per-row + custom per-row checks -----------------
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        pattern = (row.get("share_pattern") or DEFAULT_SHARE_PATTERN).strip()
        rid = (row.get("share_id") or f"row_{i}").strip()
        decision_id = (row.get("share_override_decision_id") or "").strip()

        if pattern == "deep_partner_65_35":
            pcts = _safe_share_pcts(row)
            if pcts is None:
                continue
            h, c = pcts
            if default_split_holds(h, c):
                continue
            if not decision_id:
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-04-DEFAULT-65-35-AUDIT",
                    subject_path=rel_path,
                    subject_row_id=rid,
                    verdict="warn",
                    drift_summary=(
                        f"deep_partner row {i} ({rid}): split ({h}/{c}) "
                        f"deviates from default ({DEFAULT_HOLISTIKA_SHARE_PCT}/"
                        f"{DEFAULT_COLLABORATOR_SHARE_PCT}) without "
                        "share_override_decision_id"
                    ),
                    proposed_fix_action=(
                        "mint a DECISION_REGISTER row ratifying the "
                        "deviation, then populate share_override_decision_id"
                    ),
                    severity="medium",
                    notes=(
                        "doctrine §2.1 deep_partner deviation gate; "
                        "INFO at Wave R+1; promotes to FAIL on --strict"
                    ),
                ))
                issues += 1
        elif pattern == "custom":
            if not decision_id:
                findings.append(CollaboratorShareAuditRow(
                    check_code="CS-04-DEFAULT-65-35-AUDIT",
                    subject_path=rel_path,
                    subject_row_id=rid,
                    verdict="warn",
                    drift_summary=(
                        f"custom-pattern row {i} ({rid}): custom rows require "
                        "share_override_decision_id on every row"
                    ),
                    proposed_fix_action=(
                        "mint a DECISION_REGISTER row ratifying the custom "
                        "split, then populate share_override_decision_id"
                    ),
                    severity="medium",
                    notes=(
                        "doctrine §2.1 custom variant: no automatic math "
                        "invariant, so each row must be operator-ratified"
                    ),
                ))
                issues += 1

    # orchestration_broker_thin_margin per-engagement check --------------
    for eid, eng_rows in grouped.items():
        patterns = {
            (r.get("share_pattern") or DEFAULT_SHARE_PATTERN).strip()
            for _i, r in eng_rows
        }
        if patterns != {"orchestration_broker_thin_margin"}:
            continue
        pct_pairs: list[tuple[int, int]] = []
        any_invalid = False
        for _i, r in eng_rows:
            pcts = _safe_share_pcts(r)
            if pcts is None:
                any_invalid = True
                break
            pct_pairs.append(pcts)
        if any_invalid or not pct_pairs:
            continue
        if orchestration_broker_default_margin_holds(pct_pairs):
            continue
        decision_ids = [
            (r.get("share_override_decision_id") or "").strip()
            for _i, r in eng_rows
        ]
        if any(decision_ids):
            continue
        total_h = sum(p[0] for p in pct_pairs)
        row_ids = ", ".join(
            (r.get("share_id") or f"row_{i}").strip()
            for i, r in eng_rows
        )
        findings.append(CollaboratorShareAuditRow(
            check_code="CS-04-DEFAULT-65-35-AUDIT",
            subject_path=rel_path,
            subject_row_id=eid,
            verdict="warn",
            drift_summary=(
                f"orchestration engagement {eid!r}: total Holistika margin "
                f"{total_h}% deviates from default "
                f"{ORCHESTRATION_BROKER_DEFAULT_HOLISTIKA_TOTAL_PCT}%; no "
                f"share_override_decision_id on any row ({row_ids})"
            ),
            proposed_fix_action=(
                "mint a DECISION_REGISTER row ratifying the margin "
                "deviation, then populate share_override_decision_id on at "
                "least one engagement row"
            ),
            severity="medium",
            notes=(
                "doctrine §2.1 orchestration default-margin gate; "
                "INFO at Wave R+1; promotes to FAIL on --strict"
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
                f"all {len(rows)} SHARE_REGISTRY rows respect per-pattern "
                "default-split audit (deep_partner row-local; orchestration "
                "engagement-aggregate; custom requires override on every row)"
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
    """CS-08: every SHARE_REGISTRY row's share_pattern must be a recognised
    VALID_SHARE_PATTERNS enum value. FAIL on unknown value.

    Added at Wave R+1 Commit 2b-ext per D-IH-86-DE.
    """
    findings: list[CollaboratorShareAuditRow] = []
    rows = _read_csv_rows(SHARE_REGISTRY_CSV)
    rel_path = str(SHARE_REGISTRY_CSV.relative_to(REPO_ROOT)).replace("\\", "/")
    issues = 0
    for i, raw in enumerate(rows, start=2):
        row = _normalise_row(raw)
        pattern = (row.get("share_pattern") or "").strip()
        rid = (row.get("share_id") or f"row_{i}").strip()
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
            continue
        if not share_pattern_is_valid(pattern):
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
                    "+ doctrine §2.1 with a new pattern (operator-gated)"
                ),
                severity="high",
                notes=(
                    "unknown share_pattern values break CS-03 sum-to-100 + "
                    "CS-04 default-audit branching"
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
                f"share_pattern values from {sorted(VALID_SHARE_PATTERNS)}"
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
}


# Orchestration ----------------------------------------------------------


def run_audit(
    audit_trigger: str = "on_demand",
    audited_by: str = "agent:cli",
) -> CollaboratorShareAuditReport:
    """Run all 7 checks and return the aggregate report."""
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
    if len(CHECK_REGISTRY) != 8:
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
