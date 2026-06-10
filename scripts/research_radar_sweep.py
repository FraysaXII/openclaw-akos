#!/usr/bin/env python3
"""Research Radar freshness sweep (paired runbook for SOP-RESEARCH_RADAR_001).

``process_list.csv`` row ``hol_resea_dtp_research_radar_001`` (D-IH-86-FG).

Reads per-row decay from ``INTELLIGENCEOPS_REGISTER.csv`` (volatility_class,
staleness_days, staleness_posture, next_verify_by) and substrate
``last_audit_date`` against ``SUBSTRATE_VOLATILITY_PROFILES`` in
``akos/hlk_research_radar.py``. Cadence is never a global constant.

Usage::

    py scripts/research_radar_sweep.py
    py scripts/research_radar_sweep.py --json
    py scripts/research_radar_sweep.py --include-substrate
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_intelligenceops_register_csv import INTELLIGENCEOPS_REGISTER_FIELDNAMES  # noqa: E402
from akos.hlk_research_radar import (  # noqa: E402
    IntelligenceOpsRadarRow,
    RadarFreshnessFinding,
    RadarFreshnessReport,
    SUBSTRATE_REGISTRY_PATH,
    SUBSTRATE_VOLATILITY_PROFILES,
    parse_iso_date,
)
from akos.hlk_substrate_registry_csv import SUBSTRATE_REGISTRY_FIELDNAMES  # noqa: E402
from akos.io import REPO_ROOT as AKOS_REPO_ROOT  # noqa: E402
from akos.log import setup_logging  # noqa: E402

LOG = logging.getLogger("research_radar_sweep")

INTELLIGENCEOPS_PATH = (
    AKOS_REPO_ROOT
    / "docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions"
    / "INTELLIGENCEOPS_REGISTER.csv"
)

VERDICT_FRESH = "FRESH"
VERDICT_DUE = "DUE"
VERDICT_STALE = "STALE"
VERDICT_NO_THRESHOLD = "NO_THRESHOLD"
VERDICT_SKIPPED = "SKIPPED"


def _today() -> date:
    return datetime.now(timezone.utc).date()


def _classify(
    *,
    last_verified: date | None,
    next_verify_by: date | None,
    staleness_days: int | None,
    today: date,
) -> str:
    if staleness_days is None:
        return VERDICT_NO_THRESHOLD
    if next_verify_by and today > next_verify_by:
        return VERDICT_STALE
    if last_verified is None:
        return VERDICT_DUE
    age = (today - last_verified).days
    if age > staleness_days:
        return VERDICT_STALE
    if next_verify_by and today >= next_verify_by:
        return VERDICT_DUE
    if age >= max(staleness_days - 7, 0):
        return VERDICT_DUE
    return VERDICT_FRESH


def sweep_intelligenceops(today: date) -> list[RadarFreshnessFinding]:
    findings: list[RadarFreshnessFinding] = []
    if not INTELLIGENCEOPS_PATH.is_file():
        LOG.error("INTELLIGENCEOPS_REGISTER missing: %s", INTELLIGENCEOPS_PATH)
        return findings

    with INTELLIGENCEOPS_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != INTELLIGENCEOPS_REGISTER_FIELDNAMES:
            LOG.error("INTELLIGENCEOPS_REGISTER header mismatch")
            return findings
        for raw in reader:
            row = IntelligenceOpsRadarRow.model_validate(raw)
            if row.lifecycle_status == "deprecated":
                findings.append(
                    RadarFreshnessFinding(
                        target_key=row.register_id,
                        source_register="INTELLIGENCEOPS_REGISTER",
                        verdict=VERDICT_SKIPPED,
                        notes=f"lifecycle_status={row.lifecycle_status}",
                    )
                )
                continue
            last = parse_iso_date(row.last_review_at)
            nvb = parse_iso_date(row.next_verify_by)
            days = row.resolved_staleness_days()
            verdict = _classify(
                last_verified=last,
                next_verify_by=nvb,
                staleness_days=days,
                today=today,
            )
            findings.append(
                RadarFreshnessFinding(
                    target_key=row.register_id,
                    source_register="INTELLIGENCEOPS_REGISTER",
                    verdict=verdict,
                    staleness_posture=row.staleness_posture,
                    last_verified_at=row.last_review_at,
                    next_verify_by=row.next_verify_by,
                    staleness_days=days,
                    volatility_class=row.volatility_class,
                    notes=row.target_id,
                )
            )
    return findings


def sweep_substrate(today: date) -> list[RadarFreshnessFinding]:
    findings: list[RadarFreshnessFinding] = []
    path = SUBSTRATE_REGISTRY_PATH
    if not path.is_file():
        LOG.warning("SUBSTRATE_REGISTRY missing: %s", path)
        return findings

    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != SUBSTRATE_REGISTRY_FIELDNAMES:
            LOG.error("SUBSTRATE_REGISTRY header mismatch")
            return findings
        for raw in reader:
            sid = raw.get("substrate_id", "")
            status = raw.get("status", "")
            if status in {"deprecated", "rejected"}:
                findings.append(
                    RadarFreshnessFinding(
                        target_key=sid,
                        source_register="SUBSTRATE_REGISTRY",
                        verdict=VERDICT_SKIPPED,
                        notes=f"status={status}",
                    )
                )
                continue
            profile = SUBSTRATE_VOLATILITY_PROFILES.get(sid)
            if profile is None:
                findings.append(
                    RadarFreshnessFinding(
                        target_key=sid,
                        source_register="SUBSTRATE_REGISTRY",
                        verdict=VERDICT_SKIPPED,
                        notes="no SUBSTRATE_VOLATILITY_PROFILES entry",
                    )
                )
                continue
            last = parse_iso_date(raw.get("last_audit_date", ""))
            days = profile.staleness_days
            if profile.staleness_posture == "none" or days is None:
                verdict = VERDICT_NO_THRESHOLD
            else:
                verdict = _classify(
                    last_verified=last,
                    next_verify_by=None,
                    staleness_days=days,
                    today=today,
                )
            findings.append(
                RadarFreshnessFinding(
                    target_key=sid,
                    source_register="SUBSTRATE_REGISTRY",
                    verdict=verdict,
                    staleness_posture=profile.staleness_posture,
                    last_verified_at=raw.get("last_audit_date", ""),
                    staleness_days=days,
                    volatility_class=profile.volatility_class,
                    notes=raw.get("name", ""),
                )
            )
    return findings


def build_report(
    findings: list[RadarFreshnessFinding],
    *,
    swept_by: str,
) -> RadarFreshnessReport:
    counts = {VERDICT_FRESH: 0, VERDICT_DUE: 0, VERDICT_STALE: 0, VERDICT_NO_THRESHOLD: 0, VERDICT_SKIPPED: 0}
    for f in findings:
        counts[f.verdict] = counts.get(f.verdict, 0) + 1
    return RadarFreshnessReport(
        report_id=f"radar-sweep-{datetime.now(timezone.utc).strftime('%Y%m%d')}",
        swept_at=datetime.now(timezone.utc).isoformat(),
        swept_by=swept_by,
        findings=tuple(findings),
        fresh_count=counts.get(VERDICT_FRESH, 0),
        due_count=counts.get(VERDICT_DUE, 0),
        stale_count=counts.get(VERDICT_STALE, 0),
        no_threshold_count=counts.get(VERDICT_NO_THRESHOLD, 0),
        skipped_count=counts.get(VERDICT_SKIPPED, 0),
        total_findings=len(findings),
    )


def render_table(report: RadarFreshnessReport) -> str:
    lines = [
        "",
        "  Research Radar Sweep",
        "  " + "=" * 40,
        f"  Report: {report.report_id}",
        f"  Fresh: {report.fresh_count}  Due: {report.due_count}  "
        f"Stale: {report.stale_count}  No-threshold: {report.no_threshold_count}  "
        f"Skipped: {report.skipped_count}",
        "",
        f"  {'Target':<32} {'Register':<24} {'Verdict':<14} Posture",
        "  " + "-" * 90,
    ]
    for f in report.findings:
        if f.verdict in {VERDICT_STALE, VERDICT_DUE}:
            lines.append(
                f"  {f.target_key:<32} {f.source_register:<24} {f.verdict:<14} {f.staleness_posture}"
            )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON report to stdout")
    parser.add_argument(
        "--include-substrate",
        action="store_true",
        help="Include SUBSTRATE_REGISTRY last_audit_date checks",
    )
    args = parser.parse_args(argv)

    today = _today()
    findings = sweep_intelligenceops(today)
    if args.include_substrate:
        findings.extend(sweep_substrate(today))

    report = build_report(findings, swept_by="scripts/research_radar_sweep.py")
    if args.json:
        print(json.dumps(report.model_dump(), indent=2))
    else:
        print(render_table(report))
        if report.stale_count:
            LOG.warning("Stale targets: %s", report.stale_count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
