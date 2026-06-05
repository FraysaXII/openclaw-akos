"""DataOps quality check runbook (paired to DATAOPS_DISCIPLINE.md).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md``
Pydantic SSOT: ``akos/hlk_dataops_quality.py``
Companion cursor rule: ``.cursor/rules/akos-dataops-discipline.mdc``

I90 P3c (OPS-86-19): ships ``--self-test`` chassis + stub full-sweep probes that emit
``skip`` until mirror emit / FDW / Supabase advisor live checks land at event cadence.

I93 P6: ``--data-fam <FAMILY>`` runs family-scoped probe subsets; COMPLIANCE-MIRROR runs
repo-native OPS-86-15 parity (DDL migration + sync emit symbols).

CLI::

    py scripts/dataops_quality_check.py --self-test
    py scripts/dataops_quality_check.py --sweep [--data-surface canonical_csv]
    py scripts/dataops_quality_check.py --data-fam COMPLIANCE-MIRROR
"""
from __future__ import annotations

import argparse
import datetime as _dt
import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402
from akos.hlk_dataops_quality import (  # noqa: E402
    DATA_FAM_PROBE_PROFILES,
    DATAOPS_FINDING_FIELDNAMES,
    DATAOPS_SWEEP_FIELDNAMES,
    FINOPS_MIRROR_TARGETS,
    I18_FINOPS_MIRROR_MIGRATION_BASENAME,
    I93_P6_MIRROR_MIGRATION_BASENAME,
    OPS_86_15_MIRROR_TARGETS,
    VALID_DATA_FAM_CODES,
    VALID_DATAOPS_DIMENSION_CODES,
    DataOpsFindingRow,
    DataOpsSweepReport,
    fixture_dataops_finding_row,
    fixture_dataops_sweep_report,
)

logger = logging.getLogger(__name__)

CANONICAL_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md"
)
MIGRATIONS_DIR = REPO_ROOT / "supabase" / "migrations"
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_compliance_mirrors_from_csv.py"

_MCP_DEFER_REASON = (
    "Live probe deferred; fires at canonical-CSV mint / mirror-sync / FDW-addition "
    "cadence per DATAOPS_DISCIPLINE.md section 4 + akos-holistika-operations.mdc"
)


def _probe_stub(dimension_code: str, notes: str | None = None) -> DataOpsFindingRow:
    return DataOpsFindingRow(
        dimension_code=dimension_code,  # type: ignore[arg-type]
        surface_path=str(CANONICAL_PATH.relative_to(REPO_ROOT)),
        verdict="skip",
        proposed_rework_action="",
        severity="low",
        notes=notes or _MCP_DEFER_REASON,
    )


def _probe_ops8615_mirror_parity() -> DataOpsFindingRow:
    """Repo-native OPS-86-15 closure check (I93 P6 MIRROR-2)."""
    migration_path = MIGRATIONS_DIR / I93_P6_MIRROR_MIGRATION_BASENAME
    sync_text = SYNC_SCRIPT.read_text(encoding="utf-8") if SYNC_SCRIPT.is_file() else ""
    gaps: list[str] = []
    if not migration_path.is_file():
        gaps.append(f"missing migration {I93_P6_MIRROR_MIGRATION_BASENAME}")
    else:
        mig = migration_path.read_text(encoding="utf-8")
        for _csv, table, emit_sym in OPS_86_15_MIRROR_TARGETS:
            if table not in mig:
                gaps.append(f"DDL missing compliance.{table}")
            if emit_sym not in sync_text:
                gaps.append(f"sync missing {emit_sym}")
    if gaps:
        return DataOpsFindingRow(
            dimension_code="DATA-02-MIRROR-PARITY",
            surface_path=str(migration_path.relative_to(REPO_ROOT)) if migration_path.is_file() else "supabase/migrations/",
            verdict="gap",
            proposed_rework_action="Apply I93 P6 migration + sync emit pack",
            severity="high",
            notes="; ".join(gaps),
        )
    return DataOpsFindingRow(
        dimension_code="DATA-02-MIRROR-PARITY",
        surface_path=str(migration_path.relative_to(REPO_ROOT)),
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"OPS-86-15: {len(OPS_86_15_MIRROR_TARGETS)} mirror targets have DDL + emit symbols",
    )


def _probe_finops_mirror_parity() -> DataOpsFindingRow:
    """Repo-native FINOPS counterparty mirror parity (I88 F3 / FIN-02)."""
    migration_path = MIGRATIONS_DIR / I18_FINOPS_MIRROR_MIGRATION_BASENAME
    sync_text = SYNC_SCRIPT.read_text(encoding="utf-8") if SYNC_SCRIPT.is_file() else ""
    gaps: list[str] = []
    if not migration_path.is_file():
        gaps.append(f"missing migration {I18_FINOPS_MIRROR_MIGRATION_BASENAME}")
    else:
        mig = migration_path.read_text(encoding="utf-8")
        for _csv, table, emit_sym in FINOPS_MIRROR_TARGETS:
            if table not in mig:
                gaps.append(f"DDL missing compliance.{table}")
            if emit_sym not in sync_text:
                gaps.append(f"sync missing {emit_sym}")
    if gaps:
        return DataOpsFindingRow(
            dimension_code="DATA-02-MIRROR-PARITY",
            surface_path=str(migration_path.relative_to(REPO_ROOT)) if migration_path.is_file() else "supabase/migrations/",
            verdict="gap",
            proposed_rework_action="Verify I18 finops mirror migration + sync emit",
            severity="high",
            notes="; ".join(gaps),
        )
    return DataOpsFindingRow(
        dimension_code="DATA-02-MIRROR-PARITY",
        surface_path=str(migration_path.relative_to(REPO_ROOT)),
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"FINOPS-SPINE: {len(FINOPS_MIRROR_TARGETS)} mirror target has DDL + emit symbol",
    )


def _probe_finops_fk_integrity() -> DataOpsFindingRow:
    ledger = REPO_ROOT / "scripts/validate_finops_ledger.py"
    register = (
        REPO_ROOT
        / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/finops"
        / "FINOPS_COUNTERPARTY_REGISTER.csv"
    )
    gaps: list[str] = []
    if not ledger.is_file():
        gaps.append("missing scripts/validate_finops_ledger.py")
    if not register.is_file():
        gaps.append("missing FINOPS_COUNTERPARTY_REGISTER.csv")
    if gaps:
        return DataOpsFindingRow(
            dimension_code="DATA-01-FK-INTEGRITY",
            surface_path=str(register.relative_to(REPO_ROOT)) if register.is_file() else "finops/",
            verdict="gap",
            proposed_rework_action="Restore FINOPS register + ledger validator",
            severity="high",
            notes="; ".join(gaps),
        )
    return DataOpsFindingRow(
        dimension_code="DATA-01-FK-INTEGRITY",
        surface_path=str(register.relative_to(REPO_ROOT)),
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes="FINOPS-SPINE: counterparty register SSOT + validate_finops_ledger.py present",
    )


def _probe_finops_quality_metrics() -> DataOpsFindingRow:
    validators = (
        "scripts/validate_finops_ledger.py",
        "scripts/validate_pricing_tier_registry.py",
        "scripts/validate_finops_tax_calendar.py",
    )
    missing = [v for v in validators if not (REPO_ROOT / v).is_file()]
    if missing:
        return DataOpsFindingRow(
            dimension_code="DATA-07-QUALITY-METRICS",
            surface_path="scripts/",
            verdict="gap",
            proposed_rework_action="Wire missing FINOPS validators",
            severity="medium",
            notes="; ".join(missing),
        )
    return DataOpsFindingRow(
        dimension_code="DATA-07-QUALITY-METRICS",
        surface_path="scripts/validate_finops_ledger.py",
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"FINOPS-SPINE: {len(validators)} plane validators present",
    )


FAMILY_PROBE_OVERRIDES: dict[str, dict[str, callable]] = {
    "FINOPS-SPINE": {
        "DATA-01-FK-INTEGRITY": _probe_finops_fk_integrity,
        "DATA-02-MIRROR-PARITY": _probe_finops_mirror_parity,
        "DATA-07-QUALITY-METRICS": _probe_finops_quality_metrics,
    },
}


PROBE_REGISTRY: dict[str, callable] = {
    "DATA-01-FK-INTEGRITY": lambda: _probe_stub("DATA-01-FK-INTEGRITY"),
    "DATA-02-MIRROR-PARITY": _probe_ops8615_mirror_parity,
    "DATA-03-FDW-HEALTH": lambda: _probe_stub("DATA-03-FDW-HEALTH"),
    "DATA-04-PIPELINE-FRESHNESS": lambda: _probe_stub("DATA-04-PIPELINE-FRESHNESS"),
    "DATA-05-SCHEMA-DRIFT": lambda: _probe_stub("DATA-05-SCHEMA-DRIFT"),
    "DATA-06-LINEAGE": lambda: _probe_stub("DATA-06-LINEAGE"),
    "DATA-07-QUALITY-METRICS": lambda: _probe_stub("DATA-07-QUALITY-METRICS"),
}


def run_sweep(
    data_surface: str = "canonical_csv",
    *,
    data_fam: str | None = None,
) -> DataOpsSweepReport:
    if data_fam:
        codes = DATA_FAM_PROBE_PROFILES.get(data_fam)
        if not codes:
            raise ValueError(f"unknown data-fam: {data_fam}")
        dimension_codes = list(codes)
    else:
        dimension_codes = sorted(PROBE_REGISTRY.keys())

    overrides = FAMILY_PROBE_OVERRIDES.get(data_fam or "", {})
    findings: list[DataOpsFindingRow] = []
    for code in dimension_codes:
        probe_fn = overrides.get(code) or PROBE_REGISTRY.get(code)
        if probe_fn is None:
            findings.append(_probe_stub(code, notes=f"no probe registered for {code}"))
        else:
            findings.append(probe_fn())

    counts = {v: 0 for v in ("clean", "drift", "gap", "blocked", "skip")}
    for row in findings:
        counts[row.verdict] += 1
    fam_suffix = f"-{data_fam.lower()}" if data_fam else ""
    return DataOpsSweepReport(
        report_id=f"dataops-quality{fam_suffix}-{_dt.date.today().isoformat()}",
        data_surface=data_surface,  # type: ignore[arg-type]
        swept_at=_dt.date.today().isoformat(),
        swept_by="dataops_quality_check.py",
        findings=tuple(findings),
        clean_count=counts["clean"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(findings),
    )


def self_test() -> int:
    sample_finding = fixture_dataops_finding_row()
    sample_report = fixture_dataops_sweep_report()

    if len(DATAOPS_FINDING_FIELDNAMES) != 6:
        logger.error("FAIL: DATAOPS_FINDING_FIELDNAMES len=%d expected 6", len(DATAOPS_FINDING_FIELDNAMES))
        return 1
    if len(DATAOPS_SWEEP_FIELDNAMES) != 11:
        logger.error("FAIL: DATAOPS_SWEEP_FIELDNAMES len=%d expected 11", len(DATAOPS_SWEEP_FIELDNAMES))
        return 1
    if len(PROBE_REGISTRY) != 7:
        logger.error("FAIL: PROBE_REGISTRY has %d entries, expected 7", len(PROBE_REGISTRY))
        return 1
    if set(PROBE_REGISTRY.keys()) != set(VALID_DATAOPS_DIMENSION_CODES):
        logger.error("FAIL: PROBE_REGISTRY keys != VALID_DATAOPS_DIMENSION_CODES")
        return 1
    if len(DATA_FAM_PROBE_PROFILES) != 8:
        logger.error("FAIL: DATA_FAM_PROBE_PROFILES has %d families, expected 8", len(DATA_FAM_PROBE_PROFILES))
        return 1
    if set(DATA_FAM_PROBE_PROFILES.keys()) != set(VALID_DATA_FAM_CODES):
        logger.error("FAIL: DATA_FAM_PROBE_PROFILES keys != VALID_DATA_FAM_CODES")
        return 1
    if not CANONICAL_PATH.is_file():
        logger.error("FAIL: canonical missing at %s", CANONICAL_PATH)
        return 1

    sweep = run_sweep()
    if sweep.total_findings != 7 or sweep.skip_count != 6:
        logger.error(
            "FAIL: default sweep expected 7 findings (6 skip + 1 clean mirror), got total=%d skip=%d clean=%d",
            sweep.total_findings,
            sweep.skip_count,
            sweep.clean_count,
        )
        return 1

    fam_sweep = run_sweep("mirror_table", data_fam="COMPLIANCE-MIRROR")
    if fam_sweep.total_findings != 3:
        logger.error("FAIL: COMPLIANCE-MIRROR sweep expected 3 findings, got %d", fam_sweep.total_findings)
        return 1
    if fam_sweep.gap_count > 0:
        logger.error("FAIL: COMPLIANCE-MIRROR mirror parity probe reported gap")
        return 1

    finops_sweep = run_sweep("mirror_table", data_fam="FINOPS-SPINE")
    if finops_sweep.total_findings != 3:
        logger.error("FAIL: FINOPS-SPINE sweep expected 3 findings, got %d", finops_sweep.total_findings)
        return 1
    if finops_sweep.gap_count > 0:
        logger.error("FAIL: FINOPS-SPINE probe reported gap")
        return 1

    logger.info(
        "PASS: dataops_quality_check self-test — finding=%s report=%s probes=%d families=%d",
        sample_finding.dimension_code,
        sample_report.report_id,
        len(PROBE_REGISTRY),
        len(DATA_FAM_PROBE_PROFILES),
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Validate Pydantic chassis + probe registry")
    parser.add_argument("--check", action="store_true", help="Alias for --self-test")
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run dimension sweep (all dimensions or --data-fam subset)",
    )
    parser.add_argument(
        "--data-fam",
        choices=sorted(VALID_DATA_FAM_CODES),
        help="Run DATA-FAM-scoped probe profile (I93 P6)",
    )
    parser.add_argument(
        "--data-surface",
        default="canonical_csv",
        choices=[
            "canonical_csv",
            "mirror_table",
            "fdw_projection",
            "manifest_md",
            "pydantic_ssot",
            "observability_evidence",
        ],
    )
    args = parser.parse_args()

    log.setup_logging(level=logging.INFO)

    if args.self_test or args.check:
        return self_test()

    if args.sweep or args.data_fam:
        report = run_sweep(args.data_surface, data_fam=args.data_fam)
        for row in report.findings:
            print(f"{row.dimension_code}\t{row.verdict}\t{row.notes}")
        print(
            f"TOTAL findings={report.total_findings} clean={report.clean_count} "
            f"gap={report.gap_count} skip={report.skip_count} surface={report.data_surface}"
        )
        return 1 if report.gap_count > 0 or report.drift_count > 0 or report.blocked_count > 0 else 0

    logger.info("INFO: no operation; use --self-test or --sweep or --data-fam")
    return 0


if __name__ == "__main__":
    sys.exit(main())
