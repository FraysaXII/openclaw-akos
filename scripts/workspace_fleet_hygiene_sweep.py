#!/usr/bin/env python3
"""Multi-repo fleet hygiene sweep — worktree + CI content + standing OPS rechecks.

Drift gates (``check-drift.py``, bless sha256 sidecars) catch SSOT hash mismatch.
This runbook catches **what operators and agents left uncommitted**, **unpushed**,
**stale in OPS_REGISTER**, or **missing from CI workflow content**.

Standing watch list (agent default; operator need not repeat each session):
- ``OPS-81-1`` — I81 vault-integrity observation cadence
- ``OPS-86-1`` — I86 cluster coordination
- ``OPS-86-9`` — TechOps / DataOps / MKTOPS / UX runbook threads
- ``OPS-90-6`` — KiRBe GDrive pairing forward

CLI::

    py scripts/workspace_fleet_hygiene_sweep.py --self-test
    py scripts/workspace_fleet_hygiene_sweep.py --sweep
    py scripts/workspace_fleet_hygiene_sweep.py --sweep --strict   # sibling dirty -> FAIL

Exit codes:
    0 — no FAIL-severity findings (WARN/drift allowed unless ``--strict``)
    1 — one or more FAIL-severity findings
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log  # noqa: E402
from akos.hlk_fleet_hygiene import (  # noqa: E402
    DEFAULT_GOVERNED_REPO_SLUGS,
    FLEET_FINDING_FIELDNAMES,
    FLEET_SWEEP_FIELDNAMES,
    STANDING_OPS_STALE_DAYS,
    STANDING_OPS_WATCH_IDS,
    VALID_FLEET_DIMENSION_CODES,
    FleetFindingRow,
    FleetSweepReport,
    fixture_fleet_finding_row,
    fixture_fleet_sweep_report,
)
from akos.io import REPO_ROOT as AKOS_ROOT  # noqa: E402

logger = logging.getLogger(__name__)

REGISTRY_CSV = (
    AKOS_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/REPOSITORY_REGISTRY.csv"
)
OPS_CSV = (
    AKOS_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv"
)

DEFAULT_REPO_PATHS: dict[str, Path] = {
    "openclaw-akos": AKOS_ROOT,
    "boilerplate": Path(r"c:\Users\Shadow\cd_shadow\root_cd\boilerplate"),
    "hlk-erp": Path(r"c:\Users\Shadow\cd_shadow\root_cd\hlk-erp"),
    "kirbe-platform": Path(r"c:\Users\Shadow\cd_shadow\root_cd\kirbe"),
}

# Mirrored from check_external_repo_ci_posture.py (content check, not bless sha256).
REQUIRED_CI_JOBS = ("lint", "typecheck", "audit", "build")


def _extract_ci_job_names(workflow_text: str) -> list[str]:
    in_jobs = False
    job_names: list[str] = []
    for line in workflow_text.splitlines():
        if not line:
            continue
        if not in_jobs:
            if line.strip() == "jobs:":
                in_jobs = True
            continue
        if line and not line[0].isspace() and line.strip().endswith(":"):
            break
        m = re.match(r"^\s{2}([A-Za-z_][\w-]*):\s*$", line)
        if m:
            job_names.append(m.group(1))
    return job_names


def _required_jobs_satisfied(job_names: list[str]) -> list[str]:
    tokens: set[str] = set()
    for name in job_names:
        for tok in re.split(r"[-_]", name):
            if tok:
                tokens.add(tok.lower())
    return [j for j in REQUIRED_CI_JOBS if j not in tokens]


def _ci_presence_notes(repo_path: Path) -> tuple[str, str]:
    """Return (verdict, notes) for FLEET-03 CI content."""
    ci_yml = repo_path / ".github" / "workflows" / "ci.yml"
    if not ci_yml.is_file():
        return "gap", f"{ci_yml} missing"
    text = ci_yml.read_text(encoding="utf-8", errors="ignore")
    job_names = _extract_ci_job_names(text)
    missing = _required_jobs_satisfied(job_names)
    if missing:
        return "gap", f"ci.yml missing job tokens {missing} (jobs={job_names})"
    for rel in (".github/dependabot.yml", ".github/CODEOWNERS"):
        if not (repo_path / rel).is_file():
            return "gap", f"{rel} missing"
    return "clean", f"ci.yml jobs OK ({job_names})"


def _resolve_repo_paths() -> dict[str, Path]:
    override = os.environ.get("AKOS_EXTERNAL_REPO_ROOTS")
    if override:
        try:
            data = json.loads(override)
            return {"openclaw-akos": AKOS_ROOT, **{k: Path(v) for k, v in data.items()}}
        except Exception:
            pass
    return DEFAULT_REPO_PATHS


def _git(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *cmd],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def _probe_worktree(slug: str, repo_path: Path) -> list[FleetFindingRow]:
    findings: list[FleetFindingRow] = []
    if not repo_path.is_dir() or not (repo_path / ".git").exists():
        findings.append(
            FleetFindingRow(
                dimension_code="FLEET-01-WORKTREE",
                surface_path=slug,
                verdict="skip",
                severity="low",
                notes=f"local path missing or not a git repo: {repo_path}",
                proposed_rework_action="Clone or set AKOS_EXTERNAL_REPO_ROOTS",
            )
        )
        return findings

    sb = _git(["status", "-sb"], repo_path)
    porcelain = _git(["status", "--porcelain"], repo_path)
    branch_line = (sb.stdout or "").strip().splitlines()[0] if sb.stdout else ""
    dirty_lines = [ln for ln in (porcelain.stdout or "").splitlines() if ln.strip()]

    modified = sum(1 for ln in dirty_lines if ln.startswith(" M") or ln.startswith("M "))
    untracked = sum(1 for ln in dirty_lines if ln.startswith("??"))
    staged = sum(1 for ln in dirty_lines if ln.startswith("A ") or ln.startswith("M ") or ln.startswith("D "))

    if dirty_lines:
        severity: str = "high" if slug == "openclaw-akos" else "medium"
        sample = "; ".join(dirty_lines[:8])
        if len(dirty_lines) > 8:
            sample += f"; … +{len(dirty_lines) - 8} more"
        findings.append(
            FleetFindingRow(
                dimension_code="FLEET-01-WORKTREE",
                surface_path=slug,
                verdict="drift",
                severity=severity,  # type: ignore[arg-type]
                notes=f"{branch_line} | dirty={len(dirty_lines)} (M={modified} staged={staged} ??={untracked}) | {sample}",
                proposed_rework_action="Commit or stash WIP; push when ready; update sibling PR if governed",
            )
        )
    else:
        findings.append(
            FleetFindingRow(
                dimension_code="FLEET-01-WORKTREE",
                surface_path=slug,
                verdict="clean",
                severity="low",
                notes=branch_line or "clean",
            )
        )

    ahead = behind = 0
    if "..." in branch_line:
        lr = _git(["rev-list", "--left-right", "--count", "@{u}...HEAD"], repo_path)
        if lr.returncode == 0 and lr.stdout.strip():
            parts = lr.stdout.strip().split()
            if len(parts) == 2:
                behind, ahead = int(parts[0]), int(parts[1])
        if ahead > 0:
            findings.append(
                FleetFindingRow(
                    dimension_code="FLEET-02-PUBLISH-DRIFT",
                    surface_path=slug,
                    verdict="drift",
                    severity="high" if slug == "openclaw-akos" else "medium",  # type: ignore[arg-type]
                    notes=f"{ahead} commit(s) ahead of upstream; {behind} behind",
                    proposed_rework_action="git push origin <branch>",
                )
            )
        elif branch_line and "[ahead" in branch_line:
            findings.append(
                FleetFindingRow(
                    dimension_code="FLEET-02-PUBLISH-DRIFT",
                    surface_path=slug,
                    verdict="drift",
                    severity="medium",
                    notes=branch_line,
                    proposed_rework_action="git push origin <branch>",
                )
            )
        else:
            findings.append(
                FleetFindingRow(
                    dimension_code="FLEET-02-PUBLISH-DRIFT",
                    surface_path=slug,
                    verdict="clean",
                    severity="low",
                    notes="in sync with upstream or no upstream",
                )
            )
    else:
        findings.append(
            FleetFindingRow(
                dimension_code="FLEET-02-PUBLISH-DRIFT",
                surface_path=slug,
                verdict="skip",
                severity="low",
                notes="no upstream tracking branch",
            )
        )

    return findings


def _probe_ci_content(slug: str, repo_path: Path) -> FleetFindingRow:
    if not repo_path.is_dir():
        return FleetFindingRow(
            dimension_code="FLEET-03-CI-CONTENT",
            surface_path=slug,
            verdict="skip",
            severity="low",
            notes="repo path missing",
        )
    verdict, notes = _ci_presence_notes(repo_path)
    if verdict == "gap":
        return FleetFindingRow(
            dimension_code="FLEET-03-CI-CONTENT",
            surface_path=slug,
            verdict="gap",
            severity="high",
            notes=notes,
            proposed_rework_action="Restore required CI jobs/files per SOP-CICD_BASELINE_001",
        )
    return FleetFindingRow(
        dimension_code="FLEET-03-CI-CONTENT",
        surface_path=slug,
        verdict="clean",
        severity="low",
        notes=notes,
    )


def _parse_iso_date(value: str) -> _dt.date | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return _dt.date.fromisoformat(value[:10])
    except ValueError:
        return None


def _probe_standing_ops() -> list[FleetFindingRow]:
    findings: list[FleetFindingRow] = []
    if not OPS_CSV.is_file():
        findings.append(
            FleetFindingRow(
                dimension_code="FLEET-04-STANDING-OPS",
                surface_path=str(OPS_CSV.relative_to(AKOS_ROOT)),
                verdict="blocked",
                severity="high",
                notes="OPS_REGISTER.csv missing",
            )
        )
        return findings

    today = _dt.date.today()
    with OPS_CSV.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            ops_id = (row.get("ops_action_id") or "").strip()
            if ops_id not in STANDING_OPS_WATCH_IDS:
                continue
            status = (row.get("status") or "").strip().lower()
            if status != "open":
                continue
            last_review = _parse_iso_date(row.get("last_review_at") or "")
            evidence = (row.get("evidence_path") or "").strip()
            runbook = (row.get("operator_runbook_path") or "").strip()
            title = (row.get("title") or ops_id)[:80]
            age_days = (today - last_review).days if last_review else 9999
            evidence_ok = bool(evidence) and (AKOS_ROOT / evidence).is_file()
            if age_days > STANDING_OPS_STALE_DAYS:
                verdict = "drift"
                severity = "medium"
                action = f"Refresh last_review_at + evidence for {ops_id}"
            elif not evidence_ok and evidence:
                verdict = "gap"
                severity = "medium"
                action = f"Evidence path missing on disk: {evidence}"
            else:
                verdict = "clean"
                severity = "low"
                action = ""
            findings.append(
                FleetFindingRow(
                    dimension_code="FLEET-04-STANDING-OPS",
                    surface_path=ops_id,
                    verdict=verdict,  # type: ignore[arg-type]
                    severity=severity,  # type: ignore[arg-type]
                    notes=(
                        f"{title} | last_review={last_review or 'n/a'} ({age_days}d) | "
                        f"runbook={runbook or 'n/a'} | evidence={'ok' if evidence_ok else evidence or 'missing'}"
                    ),
                    proposed_rework_action=action,
                )
            )
    return findings


def run_sweep() -> FleetSweepReport:
    findings: list[FleetFindingRow] = []
    repo_paths = _resolve_repo_paths()

    for slug in sorted(DEFAULT_GOVERNED_REPO_SLUGS):
        path = repo_paths.get(slug, AKOS_ROOT if slug == "openclaw-akos" else Path())
        findings.extend(_probe_worktree(slug, path))
        if slug in {"hlk-erp", "kirbe-platform"}:
            findings.append(_probe_ci_content(slug, path))

    findings.extend(_probe_standing_ops())

    counts = {v: 0 for v in ("clean", "drift", "gap", "blocked", "skip")}
    for row in findings:
        counts[row.verdict] += 1

    return FleetSweepReport(
        report_id=f"fleet-hygiene-{_dt.date.today().isoformat()}",
        swept_at=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        findings=tuple(findings),
        clean_count=counts["clean"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(findings),
    )


def _severity_to_exit(row: FleetFindingRow, strict: bool) -> str:
    """Return FAIL, WARN, or PASS for exit aggregation."""
    if row.verdict in ("gap", "blocked"):
        return "FAIL"
    if row.verdict == "drift":
        if row.dimension_code == "FLEET-01-WORKTREE" and row.surface_path == "openclaw-akos":
            return "FAIL"
        if strict:
            return "FAIL"
        return "WARN"
    return "PASS"


def self_test() -> int:
    sample_finding = fixture_fleet_finding_row()
    sample_report = fixture_fleet_sweep_report()

    if len(FLEET_FINDING_FIELDNAMES) != 6:
        logger.error("FAIL: FLEET_FINDING_FIELDNAMES len=%d", len(FLEET_FINDING_FIELDNAMES))
        return 1
    if len(FLEET_SWEEP_FIELDNAMES) != 10:
        logger.error("FAIL: FLEET_SWEEP_FIELDNAMES len=%d", len(FLEET_SWEEP_FIELDNAMES))
        return 1
    if not VALID_FLEET_DIMENSION_CODES >= {"FLEET-01-WORKTREE", "FLEET-04-STANDING-OPS"}:
        logger.error("FAIL: VALID_FLEET_DIMENSION_CODES incomplete")
        return 1
    if not REGISTRY_CSV.is_file():
        logger.error("FAIL: REPOSITORY_REGISTRY.csv missing")
        return 1
    if not OPS_CSV.is_file():
        logger.error("FAIL: OPS_REGISTER.csv missing")
        return 1

    logger.info(
        "PASS: workspace_fleet_hygiene_sweep self-test — finding=%s report=%s dims=%d watch_ops=%d",
        sample_finding.dimension_code,
        sample_report.report_id,
        len(VALID_FLEET_DIMENSION_CODES),
        len(STANDING_OPS_WATCH_IDS),
    )
    return 0


def _write_artifacts(report: FleetSweepReport) -> Path:
    out_dir = AKOS_ROOT / "artifacts" / "fleet-hygiene"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = report.report_id
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"
    json_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")

    lines = [
        f"# Fleet hygiene sweep — {report.report_id}",
        "",
        f"- **Swept at:** {report.swept_at}",
        f"- **Totals:** clean={report.clean_count} drift={report.drift_count} "
        f"gap={report.gap_count} blocked={report.blocked_count} skip={report.skip_count}",
        "",
        "| Dimension | Surface | Verdict | Severity | Notes |",
        "|:---|:---|:---|:---|:---|",
    ]
    for row in report.findings:
        note = row.notes.replace("|", "\\|")[:120]
        lines.append(
            f"| {row.dimension_code} | `{row.surface_path}` | {row.verdict} | "
            f"{row.severity} | {note} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check", action="store_true", help="Alias for --self-test")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat sibling-repo dirty worktrees as FAIL (default: WARN)",
    )
    parser.add_argument("--write-artifacts", action="store_true", default=True)
    parser.add_argument("--no-write-artifacts", action="store_false", dest="write_artifacts")
    args = parser.parse_args()

    log.setup_logging(level=logging.INFO)

    if args.self_test or args.check:
        return self_test()

    if not args.sweep:
        parser.print_help()
        return 2

    report = run_sweep()
    fail_count = warn_count = 0
    for row in report.findings:
        level = _severity_to_exit(row, args.strict)
        if level == "FAIL":
            fail_count += 1
            logger.error("[%s] %s — %s", row.dimension_code, row.surface_path, row.notes[:200])
        elif level == "WARN":
            warn_count += 1
            logger.warning("[%s] %s — %s", row.dimension_code, row.surface_path, row.notes[:200])

    if args.write_artifacts:
        md_path = _write_artifacts(report)
        logger.info("Wrote %s", md_path.relative_to(AKOS_ROOT))

    logger.info(
        "Fleet hygiene: clean=%d drift=%d gap=%d blocked=%d skip=%d | FAIL=%d WARN=%d",
        report.clean_count,
        report.drift_count,
        report.gap_count,
        report.blocked_count,
        report.skip_count,
        fail_count,
        warn_count,
    )
    return 1 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main())
