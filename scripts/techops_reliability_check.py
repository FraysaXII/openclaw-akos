"""TechOps reliability check runbook (paired to TECHOPS_DISCIPLINE.md).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md``
Pydantic SSOT: ``akos/hlk_techops_reliability.py``
Companion cursor rule: ``.cursor/rules/akos-techops-discipline.mdc``

I90 P3b (OPS-86-9): ships ``--self-test`` chassis + stub full-sweep probes that emit
``skip`` until Vercel / Render / Supabase / Sentry MCP live checks land at deploy cadence.

CLI::

    py scripts/techops_reliability_check.py --self-test
    py scripts/techops_reliability_check.py --sweep [--service-tier production]
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
from akos.hlk_techops_reliability import (  # noqa: E402
    TECHOPS_FINDING_FIELDNAMES,
    TECHOPS_SWEEP_FIELDNAMES,
    VALID_TECHOPS_DIMENSION_CODES,
    TechOpsFindingRow,
    TechOpsSweepReport,
    fixture_techops_finding_row,
    fixture_techops_sweep_report,
)

logger = logging.getLogger(__name__)

CANONICAL_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/TECHOPS_DISCIPLINE.md"
)

_MCP_DEFER_REASON = (
    "MCP live probe deferred; fires at deploy/observability cadence per "
    "TECHOPS_DISCIPLINE.md section 4 + akos-deploy-health.mdc"
)


def _probe_stub(dimension_code: str) -> TechOpsFindingRow:
    return TechOpsFindingRow(
        dimension_code=dimension_code,  # type: ignore[arg-type]
        surface_path=str(CANONICAL_PATH.relative_to(REPO_ROOT)),
        verdict="skip",
        proposed_rework_action="",
        severity="low",
        notes=_MCP_DEFER_REASON,
    )


PROBE_REGISTRY: dict[str, callable] = {
    "TECH-01-UPTIME-SLO": lambda: _probe_stub("TECH-01-UPTIME-SLO"),
    "TECH-02-CORE-WEB-VITALS": lambda: _probe_stub("TECH-02-CORE-WEB-VITALS"),
    "TECH-03-ERROR-BUDGET": lambda: _probe_stub("TECH-03-ERROR-BUDGET"),
    "TECH-04-DEPLOY-POSTURE": lambda: _probe_stub("TECH-04-DEPLOY-POSTURE"),
    "TECH-05-SECURITY-POSTURE": lambda: _probe_stub("TECH-05-SECURITY-POSTURE"),
    "TECH-06-OBSERVABILITY-EVIDENCE": lambda: _probe_stub("TECH-06-OBSERVABILITY-EVIDENCE"),
    "TECH-07-INCIDENT-MANAGEMENT": lambda: _probe_stub("TECH-07-INCIDENT-MANAGEMENT"),
}


def run_sweep(service_tier: str = "production") -> TechOpsSweepReport:
    findings: list[TechOpsFindingRow] = []
    for code in sorted(PROBE_REGISTRY.keys()):
        findings.append(PROBE_REGISTRY[code]())
    counts = {v: 0 for v in ("clean", "drift", "gap", "blocked", "skip")}
    for row in findings:
        counts[row.verdict] += 1
    return TechOpsSweepReport(
        report_id=f"techops-reliability-{_dt.date.today().isoformat()}",
        service_tier=service_tier,  # type: ignore[arg-type]
        swept_at=_dt.date.today().isoformat(),
        swept_by="techops_reliability_check.py",
        findings=tuple(findings),
        clean_count=counts["clean"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(findings),
    )


def self_test() -> int:
    sample_finding = fixture_techops_finding_row()
    sample_report = fixture_techops_sweep_report()

    if len(TECHOPS_FINDING_FIELDNAMES) != 6:
        logger.error("FAIL: TECHOPS_FINDING_FIELDNAMES len=%d expected 6", len(TECHOPS_FINDING_FIELDNAMES))
        return 1
    if len(TECHOPS_SWEEP_FIELDNAMES) != 11:
        logger.error("FAIL: TECHOPS_SWEEP_FIELDNAMES len=%d expected 11", len(TECHOPS_SWEEP_FIELDNAMES))
        return 1
    if len(PROBE_REGISTRY) != 7:
        logger.error("FAIL: PROBE_REGISTRY has %d entries, expected 7", len(PROBE_REGISTRY))
        return 1
    if set(PROBE_REGISTRY.keys()) != set(VALID_TECHOPS_DIMENSION_CODES):
        logger.error("FAIL: PROBE_REGISTRY keys != VALID_TECHOPS_DIMENSION_CODES")
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
        "PASS: techops_reliability_check self-test — finding=%s report=%s probes=%d",
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
        help="Run stub 7-dimension sweep (all probes skip until MCP wiring)",
    )
    parser.add_argument(
        "--service-tier",
        default="production",
        choices=["production", "staging", "preview", "internal_dev"],
    )
    args = parser.parse_args()

    log.setup_logging(level=logging.INFO)

    if args.self_test or args.check:
        return self_test()

    if args.sweep:
        report = run_sweep(args.service_tier)
        for row in report.findings:
            print(f"{row.dimension_code}\t{row.verdict}\t{row.notes}")
        print(
            f"TOTAL findings={report.total_findings} skip={report.skip_count} "
            f"tier={report.service_tier}"
        )
        return 0

    logger.info("INFO: no operation; use --self-test or --sweep")
    return 0


if __name__ == "__main__":
    sys.exit(main())
