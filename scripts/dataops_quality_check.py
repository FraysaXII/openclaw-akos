"""DataOps quality check runbook (paired to DATAOPS_DISCIPLINE.md).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md``
Pydantic SSOT: ``akos/hlk_dataops_quality.py``
Companion cursor rule: ``.cursor/rules/akos-dataops-discipline.mdc``

I90 P3c (OPS-86-19): ships ``--self-test`` chassis + stub full-sweep probes that emit
``skip`` until mirror emit / FDW / Supabase advisor live checks land at event cadence.

CLI::

    py scripts/dataops_quality_check.py --self-test
    py scripts/dataops_quality_check.py --sweep [--data-surface canonical_csv]
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
    DATAOPS_FINDING_FIELDNAMES,
    DATAOPS_SWEEP_FIELDNAMES,
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

_MCP_DEFER_REASON = (
    "Live probe deferred; fires at canonical-CSV mint / mirror-sync / FDW-addition "
    "cadence per DATAOPS_DISCIPLINE.md section 4 + akos-holistika-operations.mdc"
)


def _probe_stub(dimension_code: str) -> DataOpsFindingRow:
    return DataOpsFindingRow(
        dimension_code=dimension_code,  # type: ignore[arg-type]
        surface_path=str(CANONICAL_PATH.relative_to(REPO_ROOT)),
        verdict="skip",
        proposed_rework_action="",
        severity="low",
        notes=_MCP_DEFER_REASON,
    )


PROBE_REGISTRY: dict[str, callable] = {
    "DATA-01-FK-INTEGRITY": lambda: _probe_stub("DATA-01-FK-INTEGRITY"),
    "DATA-02-MIRROR-PARITY": lambda: _probe_stub("DATA-02-MIRROR-PARITY"),
    "DATA-03-FDW-HEALTH": lambda: _probe_stub("DATA-03-FDW-HEALTH"),
    "DATA-04-PIPELINE-FRESHNESS": lambda: _probe_stub("DATA-04-PIPELINE-FRESHNESS"),
    "DATA-05-SCHEMA-DRIFT": lambda: _probe_stub("DATA-05-SCHEMA-DRIFT"),
    "DATA-06-LINEAGE": lambda: _probe_stub("DATA-06-LINEAGE"),
    "DATA-07-QUALITY-METRICS": lambda: _probe_stub("DATA-07-QUALITY-METRICS"),
}


def run_sweep(data_surface: str = "canonical_csv") -> DataOpsSweepReport:
    findings: list[DataOpsFindingRow] = []
    for code in sorted(PROBE_REGISTRY.keys()):
        findings.append(PROBE_REGISTRY[code]())
    counts = {v: 0 for v in ("clean", "drift", "gap", "blocked", "skip")}
    for row in findings:
        counts[row.verdict] += 1
    return DataOpsSweepReport(
        report_id=f"dataops-quality-{_dt.date.today().isoformat()}",
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
    if not CANONICAL_PATH.is_file():
        logger.error("FAIL: canonical missing at %s", CANONICAL_PATH)
        return 1

    sweep = run_sweep()
    if sweep.total_findings != 7 or sweep.skip_count != 7:
        logger.error(
            "FAIL: stub sweep expected 7 skip findings, got total=%d skip=%d",
            sweep.total_findings,
            sweep.skip_count,
        )
        return 1

    logger.info(
        "PASS: dataops_quality_check self-test — finding=%s report=%s probes=%d",
        sample_finding.dimension_code,
        sample_report.report_id,
        len(PROBE_REGISTRY),
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Validate Pydantic chassis + probe registry")
    parser.add_argument("--check", action="store_true", help="Alias for --self-test")
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run stub 7-dimension sweep (all probes skip until live wiring)",
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

    if args.sweep:
        report = run_sweep(args.data_surface)
        for row in report.findings:
            print(f"{row.dimension_code}\t{row.verdict}\t{row.notes}")
        print(
            f"TOTAL findings={report.total_findings} skip={report.skip_count} "
            f"surface={report.data_surface}"
        )
        return 0

    logger.info("INFO: no operation; use --self-test or --sweep")
    return 0


if __name__ == "__main__":
    sys.exit(main())
