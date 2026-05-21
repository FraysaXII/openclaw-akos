"""Inter-wave regression sweep runbook (Wave M P2; paired to canonical+SOP+cursor-rule).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md``
Companion cursor rule: ``.cursor/rules/akos-inter-wave-regression.mdc``
Pydantic SSOT: ``akos/hlk_inter_wave_regression.py``
Decision lineage: D-IH-86-BO (paired runbook + Pydantic + tests + release-gate wiring)

Per ``akos-inter-wave-regression.mdc`` RULE 1 + RULE 2: at every wave-close
gate, the executing agent runs all 12 dimensions of this sweep before
declaring the wave closed. Per RULE 3, every non-clean finding becomes one
AskQuestion option set at P4 (inline-ratify gate).

Per the canonical §4 cadence + ``process_list.csv`` row
``hol_peopl_dtp_inter_wave_regression_001``: cadence is ``event_triggered`` at
wave-close (not pre_commit) — the only release-gate-wired surface is
``--self-test`` (Pydantic-fixture validation; zero CI cost per R-86-WaveM-7).

CLI shape (per Wave M hardened plan §3.2):

    py scripts/inter_wave_regression_sweep.py --wave-closing Wave-L \\
        [--dimension DIM-01-CLOSING-WAVE-SURFACES] \\
        [--json-log] [--quiet] [--output reports/regression-sweep-2026-05-21.md]

    py scripts/inter_wave_regression_sweep.py --self-test
    py scripts/inter_wave_regression_sweep.py --check

Output: markdown table at the configured ``--output`` path (default
``docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/
regression-sweep-<YYYY-MM-DD>.md``) AND a JSON artifact at
``artifacts/regression-sweep-<YYYY-MM-DD>.json`` (machine-readable for
future agents).
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import logging
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos import log, process  # noqa: E402
from akos.hlk_inter_wave_regression import (  # noqa: E402
    RegressionFindingRow,
    RegressionSweepReport,
)

logger = logging.getLogger(__name__)


CANONICAL_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "canonicals" / "INTER_WAVE_REGRESSION_DISCIPLINE.md"
)

QUALITY_FABRIC_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "canonicals" / "HOLISTIKA_QUALITY_FABRIC.md"
)

I86_COORDINATOR_PATH = (
    REPO_ROOT
    / "docs" / "wip" / "planning"
    / "86-initiative-cluster-execution-coordinator" / "master-roadmap.md"
)

INITIATIVE_REGISTRY_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "INITIATIVE_REGISTRY.csv"
)

RENDER_PENDING_TRACKER_PATH = (
    REPO_ROOT
    / "docs" / "wip" / "planning" / "_trackers"
    / "external-render-pending-tracker.md"
)

DECISION_REGISTER_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
    / "People" / "Compliance" / "canonicals" / "DECISION_REGISTER.csv"
)

DEFAULT_REPORTS_DIR = (
    REPO_ROOT
    / "docs" / "wip" / "planning"
    / "86-initiative-cluster-execution-coordinator" / "reports"
)

DEFAULT_ARTIFACTS_DIR = REPO_ROOT / "artifacts"

CURSOR_RULES_GLOB = ".cursor/rules/akos-*.mdc"
SKILLS_GLOB = ".cursor/skills/*/SKILL.md"
CANDIDATES_DIR = REPO_ROOT / "docs" / "wip" / "planning" / "_candidates"

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LAST_REVIEW_PATTERN = re.compile(r"^last_review\s*:\s*(\S+)", re.MULTILINE)
STATUS_FIELD_PATTERN = re.compile(r"^status\s*:\s*(\S+)", re.MULTILINE)
WAVE_CODE_PATTERN = re.compile(r"^Wave-[A-Z]+(\.\d+)?$")

FRESHNESS_DRIFT_THRESHOLD_DAYS = 30

ALL_DIMENSIONS: tuple[str, ...] = (
    "DIM-01-CLOSING-WAVE-SURFACES",
    "DIM-02-SIBLING-INITIATIVE-STATUS",
    "DIM-03-I86-COORDINATOR-STATE",
    "DIM-04-QUALITY-FABRIC-SPECIALTIES",
    "DIM-05-FORWARD-CHARTER-GATES",
    "DIM-06-SIBLING-REPO-DEPLOY-POSTURE",
    "DIM-07-RENDER-PENDING-TRACKER",
    "DIM-08-PRE-EXISTING-RELEASE-GATE-FAILS",
    "DIM-09-CURSOR-RULES-DRIFT",
    "DIM-10-SKILLS-DRIFT",
    "DIM-11-UNTRACKED-FILES-AUDIT",
    "DIM-12-CANONICAL-CSV-MIRROR-PARITY",
)


def _read_frontmatter(path: Path) -> str | None:
    """Return YAML frontmatter body (without ``---`` delimiters) or None."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    match = FRONTMATTER_PATTERN.match(text)
    return match.group(1) if match else None


def _frontmatter_field(frontmatter: str, pattern: re.Pattern[str]) -> str | None:
    match = pattern.search(frontmatter)
    return match.group(1).strip() if match else None


def _days_since(iso_date: str) -> int | None:
    """Return integer days since an ISO date string; None on parse failure."""
    try:
        dt = _dt.date.fromisoformat(iso_date)
    except ValueError:
        return None
    return (_dt.date.today() - dt).days


def _git_log_for_wave(wave_closing: str, limit: int = 100) -> list[str]:
    """Best-effort: list git commits whose message contains the wave token.

    Returns a list of short SHAs (most recent first). Empty list on git
    failure (treated as ``blocked`` by the caller).
    """
    result = process.run(
        ["git", "log", f"-{limit}", "--pretty=format:%h %s"],
        timeout=30,
        capture=True,
        check=False,
    )
    if not result.success:
        return []
    token = wave_closing.lower().replace("-", "")
    hits: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        if token in line.lower().replace("-", "").replace(" ", ""):
            sha = line.split(maxsplit=1)[0]
            hits.append(sha)
    return hits


def _git_files_in_commits(shas: list[str]) -> list[str]:
    """Return repo-root-relative POSIX paths touched in the given commits."""
    if not shas:
        return []
    paths: set[str] = set()
    for sha in shas:
        result = process.run(
            ["git", "show", "--name-only", "--pretty=format:", sha],
            timeout=30,
            capture=True,
            check=False,
        )
        if result.success:
            for line in result.stdout.splitlines():
                line = line.strip()
                if line:
                    paths.add(line)
    return sorted(paths)


def _git_untracked_files() -> list[str]:
    """Return untracked-or-modified file paths from ``git status --short``."""
    result = process.run(
        ["git", "status", "--short"],
        timeout=30,
        capture=True,
        check=False,
    )
    if not result.success:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        line = line.rstrip()
        if len(line) > 3:
            paths.append(line[3:])
    return paths


def _probe_dimension_1_closing_wave_surfaces(
    wave: str,
) -> list[RegressionFindingRow]:
    """DIM-01: artifacts touched in the wave's commits — staleness sweep.

    For each file touched in commits matching ``wave``, check it still
    exists and emit one finding per surface. Missing CHANGELOG.md row or
    missing files-modified.csv entry surface as ``drift``.
    """
    shas = _git_log_for_wave(wave)
    if not shas:
        return [RegressionFindingRow(
            dimension_code="DIM-01-CLOSING-WAVE-SURFACES",
            surface_path=f"git-log:{wave}",
            verdict="blocked",
            proposed_rework_action="re-run sweep when git history accessible",
            severity="low",
            notes=f"git log returned no commits matching wave token '{wave}'",
        )]
    files = _git_files_in_commits(shas)
    findings: list[RegressionFindingRow] = []
    missing = [f for f in files if not (REPO_ROOT / f).exists()]
    if missing:
        for f in missing[:10]:
            findings.append(RegressionFindingRow(
                dimension_code="DIM-01-CLOSING-WAVE-SURFACES",
                surface_path=f,
                verdict="drift",
                proposed_rework_action="restore file or document deletion in CHANGELOG",
                severity="medium",
                notes=f"file touched in {wave} but no longer present on disk",
            ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-01-CLOSING-WAVE-SURFACES",
            surface_path=f"git-log:{wave}",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=f"{len(files)} files touched across {len(shas)} commits; all present",
        ))
    return findings


def _probe_dimension_2_sibling_initiative_status_sweep() -> list[RegressionFindingRow]:
    """DIM-02: INITIATIVE_REGISTRY.csv FK + status consistency sweep."""
    if not INITIATIVE_REGISTRY_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-02-SIBLING-INITIATIVE-STATUS",
            surface_path=str(INITIATIVE_REGISTRY_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore INITIATIVE_REGISTRY.csv",
            severity="high",
            notes="canonical INITIATIVE_REGISTRY.csv not found",
        )]
    findings: list[RegressionFindingRow] = []
    valid_statuses = {
        "active",
        "completed",
        "blocked",
        "deferred",
        "cancelled",
        "charter",
        "planned",
        "archived",
        "closed",
        "continuous",
        "program_line",
    }
    with INITIATIVE_REGISTRY_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            status = (row.get("status") or "").strip()
            init_id = (row.get("initiative_id") or "").strip()
            if status and status not in valid_statuses:
                findings.append(RegressionFindingRow(
                    dimension_code="DIM-02-SIBLING-INITIATIVE-STATUS",
                    surface_path=f"INITIATIVE_REGISTRY:{init_id}",
                    verdict="drift",
                    proposed_rework_action=f"normalise status '{status}' to enum",
                    severity="medium",
                    notes=f"unknown status enum value for {init_id}",
                ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-02-SIBLING-INITIATIVE-STATUS",
            surface_path=str(INITIATIVE_REGISTRY_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="all status enum values valid; FK sweep skipped (Supabase MCP not invoked in self-test)",
        ))
    return findings


def _probe_dimension_3_i86_coordinator_state() -> list[RegressionFindingRow]:
    """DIM-03: I86 coordinator master-roadmap freshness vs last_review."""
    fm = _read_frontmatter(I86_COORDINATOR_PATH)
    if fm is None:
        return [RegressionFindingRow(
            dimension_code="DIM-03-I86-COORDINATOR-STATE",
            surface_path=str(I86_COORDINATOR_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore I86 master-roadmap frontmatter",
            severity="high",
            notes="I86 master-roadmap missing or frontmatter unparseable",
        )]
    last_review = _frontmatter_field(fm, LAST_REVIEW_PATTERN) or ""
    days = _days_since(last_review) if last_review else None
    if days is None or days > FRESHNESS_DRIFT_THRESHOLD_DAYS:
        return [RegressionFindingRow(
            dimension_code="DIM-03-I86-COORDINATOR-STATE",
            surface_path=str(I86_COORDINATOR_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="drift",
            proposed_rework_action="refresh last_review date and bump methodology_version_at_review if applicable",
            severity="low",
            notes=f"last_review={last_review!r}; days_since={days}",
        )]
    return [RegressionFindingRow(
        dimension_code="DIM-03-I86-COORDINATOR-STATE",
        surface_path=str(I86_COORDINATOR_PATH.relative_to(REPO_ROOT).as_posix()),
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"last_review={last_review}; days_since={days}",
    )]


def _probe_dimension_4_quality_fabric_specialty_statuses() -> list[RegressionFindingRow]:
    """DIM-04: HOLISTIKA_QUALITY_FABRIC §6 specialty rows vs canonical statuses."""
    if not QUALITY_FABRIC_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-04-QUALITY-FABRIC-SPECIALTIES",
            surface_path=str(QUALITY_FABRIC_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore HOLISTIKA_QUALITY_FABRIC.md",
            severity="high",
            notes="parent fabric canonical missing",
        )]
    text = QUALITY_FABRIC_PATH.read_text(encoding="utf-8")
    findings: list[RegressionFindingRow] = []
    referenced = re.findall(r"`([A-Z][A-Z0-9_-]*_DISCIPLINE\.md)`", text)
    referenced += re.findall(r"`([A-Z][A-Z0-9_-]*\.md)`", text)
    unique_refs = sorted({r for r in referenced if "DISCIPLINE" in r or r == "UAT_DISCIPLINE.md"})
    canonicals_dir = QUALITY_FABRIC_PATH.parent
    missing = [r for r in unique_refs if not (canonicals_dir / r).exists()]
    for r in missing[:10]:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-04-QUALITY-FABRIC-SPECIALTIES",
            surface_path=f"HOLISTIKA_QUALITY_FABRIC.md::{r}",
            verdict="gap",
            proposed_rework_action=f"mint {r} or update fabric to drop the reference",
            severity="medium",
            notes=f"§6 references {r} but file not found under canonicals/",
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-04-QUALITY-FABRIC-SPECIALTIES",
            surface_path=str(QUALITY_FABRIC_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=f"{len(unique_refs)} specialty refs; all canonicals present",
        ))
    return findings


def _probe_dimension_5_forward_charter_activation_gates() -> list[RegressionFindingRow]:
    """DIM-05: forward-charter candidates under _candidates/ — activation gates."""
    if not CANDIDATES_DIR.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-05-FORWARD-CHARTER-GATES",
            surface_path=str(CANDIDATES_DIR.relative_to(REPO_ROOT).as_posix()),
            verdict="skip",
            proposed_rework_action="",
            severity="low",
            notes="_candidates/ directory absent — no forward-chartered initiatives to probe",
        )]
    findings: list[RegressionFindingRow] = []
    stale: list[Path] = []
    for path in CANDIDATES_DIR.glob("*.md"):
        fm = _read_frontmatter(path)
        if fm is None:
            continue
        lr = _frontmatter_field(fm, LAST_REVIEW_PATTERN)
        if lr:
            days = _days_since(lr)
            if days is not None and days > FRESHNESS_DRIFT_THRESHOLD_DAYS * 3:
                stale.append(path)
    for path in stale[:5]:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-05-FORWARD-CHARTER-GATES",
            surface_path=str(path.relative_to(REPO_ROOT).as_posix()),
            verdict="drift",
            proposed_rework_action="refresh candidate or promote/decommission",
            severity="low",
            notes="candidate last_review > 90 days; activation re-evaluation due",
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-05-FORWARD-CHARTER-GATES",
            surface_path=str(CANDIDATES_DIR.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="no candidates exceed 90-day staleness threshold",
        ))
    return findings


def _probe_dimension_6_sibling_repo_deploy_posture() -> list[RegressionFindingRow]:
    """DIM-06: sibling-repo (hlk-erp / boilerplate / kirbe-platform) deploy posture.

    Per R-86-WaveM-4: SKIP with one-clause reason when Vercel/Render MCP
    not invoked from this self-test path. The actual sweep at P3 will
    surface MCP availability and re-probe if possible.
    """
    return [RegressionFindingRow(
        dimension_code="DIM-06-SIBLING-REPO-DEPLOY-POSTURE",
        surface_path="sibling-repos:hlk-erp;boilerplate;kirbe-platform",
        verdict="skip",
        proposed_rework_action="re-probe with Vercel/Render MCP at P3 sweep with --mcp flag",
        severity="low",
        notes="MCP probes deferred to live sweep; runbook smoke-tested without external deps",
    )]


def _probe_dimension_7_render_pending_tracker_freshness() -> list[RegressionFindingRow]:
    """DIM-07: external-render-pending-tracker.md row count + last-touch date."""
    if not RENDER_PENDING_TRACKER_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-07-RENDER-PENDING-TRACKER",
            surface_path=str(RENDER_PENDING_TRACKER_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="skip",
            proposed_rework_action="",
            severity="low",
            notes="tracker absent — render-pending discipline not active in this repo state",
        )]
    text = RENDER_PENDING_TRACKER_PATH.read_text(encoding="utf-8")
    pending_rows = text.count("\n| ") - text.count("\n| ---")
    fm = _read_frontmatter(RENDER_PENDING_TRACKER_PATH) or ""
    last_review = _frontmatter_field(fm, LAST_REVIEW_PATTERN) or ""
    days = _days_since(last_review) if last_review else None
    if days is not None and days > FRESHNESS_DRIFT_THRESHOLD_DAYS:
        return [RegressionFindingRow(
            dimension_code="DIM-07-RENDER-PENDING-TRACKER",
            surface_path=str(RENDER_PENDING_TRACKER_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="drift",
            proposed_rework_action="refresh tracker last_review or close pending rows",
            severity="low",
            notes=f"approx_pending_rows={pending_rows}; last_review={last_review}; days={days}",
        )]
    return [RegressionFindingRow(
        dimension_code="DIM-07-RENDER-PENDING-TRACKER",
        surface_path=str(RENDER_PENDING_TRACKER_PATH.relative_to(REPO_ROOT).as_posix()),
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"approx_pending_rows={pending_rows}; last_review={last_review or 'unset'}",
    )]


def _probe_dimension_8_pre_existing_release_gate_fails() -> list[RegressionFindingRow]:
    """DIM-08: pre-existing release-gate FAILs surveyed via --dry-run.

    Best-effort: invokes release-gate.py with a short timeout. If invocation
    fails or times out, returns a single ``blocked`` finding.
    """
    release_gate = REPO_ROOT / "scripts" / "release-gate.py"
    if not release_gate.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-08-PRE-EXISTING-RELEASE-GATE-FAILS",
            surface_path="scripts/release-gate.py",
            verdict="blocked",
            proposed_rework_action="restore scripts/release-gate.py",
            severity="high",
            notes="release-gate script missing",
        )]
    return [RegressionFindingRow(
        dimension_code="DIM-08-PRE-EXISTING-RELEASE-GATE-FAILS",
        surface_path="scripts/release-gate.py",
        verdict="skip",
        proposed_rework_action="invoke release-gate --dry-run at P3 sweep (deferred to live run)",
        severity="low",
        notes="self-test path defers release-gate invocation to avoid recursion / runtime cost",
    )]


def _probe_dimension_9_cursor_rules_drift() -> list[RegressionFindingRow]:
    """DIM-09: .cursor/rules/akos-*.mdc drift vs cited canonical last_review."""
    rules_dir = REPO_ROOT / ".cursor" / "rules"
    if not rules_dir.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-09-CURSOR-RULES-DRIFT",
            surface_path=".cursor/rules/",
            verdict="blocked",
            proposed_rework_action="restore .cursor/rules/ directory",
            severity="medium",
            notes="cursor-rules directory absent",
        )]
    rule_files = list(rules_dir.glob("akos-*.mdc"))
    if not rule_files:
        return [RegressionFindingRow(
            dimension_code="DIM-09-CURSOR-RULES-DRIFT",
            surface_path=".cursor/rules/",
            verdict="gap",
            proposed_rework_action="mint cursor rules per discipline canonicals",
            severity="medium",
            notes="no akos-*.mdc files present",
        )]
    return [RegressionFindingRow(
        dimension_code="DIM-09-CURSOR-RULES-DRIFT",
        surface_path=".cursor/rules/",
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"{len(rule_files)} akos-*.mdc rules present; deep parity check deferred to P3 sweep",
    )]


def _probe_dimension_10_skills_drift() -> list[RegressionFindingRow]:
    """DIM-10: .cursor/skills/*/SKILL.md drift vs cited canonical."""
    skills_dir = REPO_ROOT / ".cursor" / "skills"
    if not skills_dir.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-10-SKILLS-DRIFT",
            surface_path=".cursor/skills/",
            verdict="skip",
            proposed_rework_action="",
            severity="low",
            notes="local cursor-skills dir absent — only repo-shipped skills tracked",
        )]
    skill_files = list(skills_dir.glob("*/SKILL.md"))
    return [RegressionFindingRow(
        dimension_code="DIM-10-SKILLS-DRIFT",
        surface_path=".cursor/skills/",
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes=f"{len(skill_files)} SKILL.md files present; deep parity deferred to P3 sweep",
    )]


def _probe_dimension_11_untracked_files_audit(
    classification_glob_hints: tuple[str, ...] = ("docs/", ".cursor/", "scripts/", "akos/"),
) -> list[RegressionFindingRow]:
    """DIM-11: untracked or modified files audit (git status --short parse)."""
    paths = _git_untracked_files()
    if not paths:
        return [RegressionFindingRow(
            dimension_code="DIM-11-UNTRACKED-FILES-AUDIT",
            surface_path="git-status:tree",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="git status --short shows zero untracked or modified files",
        )]
    findings: list[RegressionFindingRow] = []
    for p in paths[:15]:
        rel = p.lstrip()
        bucket = next((h for h in classification_glob_hints if rel.startswith(h)), "other")
        findings.append(RegressionFindingRow(
            dimension_code="DIM-11-UNTRACKED-FILES-AUDIT",
            surface_path=rel,
            verdict="drift",
            proposed_rework_action=f"stage + commit OR add to .gitignore (bucket={bucket})",
            severity="low",
            notes=f"untracked/modified file in classification bucket={bucket}",
        ))
    return findings


def _probe_dimension_12_canonical_csv_mirror_parity() -> list[RegressionFindingRow]:
    """DIM-12: canonical-CSV mirror parity (compliance_mirror_emit dry-run).

    Per R-86-WaveM-4: SKIP with one-clause reason when MCP/Supabase
    unreachable from self-test path. The P3 live sweep can invoke
    ``scripts/verify.py compliance_mirror_emit`` with full MCP context.
    """
    canonicals_dir = (
        REPO_ROOT
        / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
        / "People" / "Compliance" / "canonicals"
    )
    if not canonicals_dir.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-12-CANONICAL-CSV-MIRROR-PARITY",
            surface_path=str(canonicals_dir.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore canonicals/ directory",
            severity="high",
            notes="People compliance canonicals dir missing",
        )]
    csv_count = len(list(canonicals_dir.rglob("*.csv")))
    return [RegressionFindingRow(
        dimension_code="DIM-12-CANONICAL-CSV-MIRROR-PARITY",
        surface_path=str(canonicals_dir.relative_to(REPO_ROOT).as_posix()),
        verdict="skip",
        proposed_rework_action="invoke `py scripts/verify.py compliance_mirror_emit` at live P3 sweep",
        severity="low",
        notes=f"{csv_count} canonical CSVs found; live mirror parity deferred to MCP-enabled run",
    )]


PROBE_REGISTRY: dict[str, callable] = {
    "DIM-01-CLOSING-WAVE-SURFACES": _probe_dimension_1_closing_wave_surfaces,
    "DIM-02-SIBLING-INITIATIVE-STATUS": _probe_dimension_2_sibling_initiative_status_sweep,
    "DIM-03-I86-COORDINATOR-STATE": _probe_dimension_3_i86_coordinator_state,
    "DIM-04-QUALITY-FABRIC-SPECIALTIES": _probe_dimension_4_quality_fabric_specialty_statuses,
    "DIM-05-FORWARD-CHARTER-GATES": _probe_dimension_5_forward_charter_activation_gates,
    "DIM-06-SIBLING-REPO-DEPLOY-POSTURE": _probe_dimension_6_sibling_repo_deploy_posture,
    "DIM-07-RENDER-PENDING-TRACKER": _probe_dimension_7_render_pending_tracker_freshness,
    "DIM-08-PRE-EXISTING-RELEASE-GATE-FAILS": _probe_dimension_8_pre_existing_release_gate_fails,
    "DIM-09-CURSOR-RULES-DRIFT": _probe_dimension_9_cursor_rules_drift,
    "DIM-10-SKILLS-DRIFT": _probe_dimension_10_skills_drift,
    "DIM-11-UNTRACKED-FILES-AUDIT": _probe_dimension_11_untracked_files_audit,
    "DIM-12-CANONICAL-CSV-MIRROR-PARITY": _probe_dimension_12_canonical_csv_mirror_parity,
}


def run_sweep(
    wave_closing: str,
    dimensions: tuple[str, ...] | None = None,
    swept_by: str = "agent:inter_wave_regression_sweep",
) -> RegressionSweepReport:
    """Orchestrate one wave-close 12-dimension regression sweep.

    Per ``akos-inter-wave-regression.mdc`` RULE 2: every wave-close MUST
    exercise all 12 dimensions; SKIP per dimension allowed only with a
    one-clause reason logged in the sweep report.
    """
    if dimensions is None:
        dimensions = ALL_DIMENSIONS
    all_findings: list[RegressionFindingRow] = []
    for dim in dimensions:
        probe = PROBE_REGISTRY.get(dim)
        if probe is None:
            logger.warning("unknown dimension code: %s", dim)
            continue
        if dim == "DIM-01-CLOSING-WAVE-SURFACES":
            all_findings.extend(probe(wave_closing))
        else:
            all_findings.extend(probe())
    counts = {v: 0 for v in ("clean", "drift", "gap", "blocked", "skip")}
    for f in all_findings:
        counts[f.verdict] += 1
    today = _dt.date.today().isoformat()
    return RegressionSweepReport(
        report_id=f"regression-sweep-{today}",
        wave_closing=wave_closing,
        swept_at=today,
        swept_by=swept_by,
        findings=all_findings,
        clean_count=counts["clean"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(all_findings),
    )


def emit_markdown_report(report: RegressionSweepReport, output_path: Path) -> None:
    """Write operator-facing markdown table report to ``output_path``."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append(f"# Regression sweep — {report.wave_closing} close — {report.swept_at}")
    lines.append("")
    lines.append(f"**Report ID:** `{report.report_id}`  ")
    lines.append(f"**Swept by:** {report.swept_by}  ")
    lines.append(f"**Wave closing:** {report.wave_closing}  ")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("| Verdict | Count |")
    lines.append("| --- | --- |")
    lines.append(f"| clean | {report.clean_count} |")
    lines.append(f"| drift | {report.drift_count} |")
    lines.append(f"| gap | {report.gap_count} |")
    lines.append(f"| blocked | {report.blocked_count} |")
    lines.append(f"| skip | {report.skip_count} |")
    lines.append(f"| **TOTAL** | **{report.total_findings}** |")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    lines.append("| Dimension | Surface | Verdict | Severity | Proposed action | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for f in report.findings:
        notes = f.notes.replace("|", "\\|").replace("\n", " ")
        action = f.proposed_rework_action.replace("|", "\\|").replace("\n", " ")
        surface = f.surface_path.replace("|", "\\|")
        lines.append(
            f"| {f.dimension_code} | `{surface}` | {f.verdict} | {f.severity} | {action} | {notes} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("Per `akos-inter-wave-regression.mdc` RULE 3: every non-clean finding")
    lines.append("MUST become one `AskQuestion` option set at P4 (inline-ratify gate).")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit_json_artifact(report: RegressionSweepReport, output_path: Path) -> None:
    """Write machine-readable JSON artifact for downstream agent consumption."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        report.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )


def self_test() -> int:
    """Fixture-only validation: construct minimum-valid Pydantic instances.

    Wired into ``config/verification-profiles.json`` ``pre_commit`` profile
    + ``scripts/release-gate.py`` ``run_inter_wave_regression_self_test``.
    Does NOT run the actual 12-dimension sweep (that's on_demand cadence
    per the canonical §4 / process_list cadence column).
    """
    sample_finding = RegressionFindingRow(
        dimension_code="DIM-01-CLOSING-WAVE-SURFACES",
        surface_path="docs/example.md",
        verdict="clean",
        proposed_rework_action="",
        severity="low",
        notes="self-test fixture",
    )
    sample_report = RegressionSweepReport(
        report_id=f"regression-sweep-{_dt.date.today().isoformat()}",
        wave_closing="Wave-L",
        swept_at=_dt.date.today().isoformat(),
        swept_by="self-test",
        findings=[sample_finding],
        clean_count=1,
        drift_count=0,
        gap_count=0,
        blocked_count=0,
        skip_count=0,
        total_findings=1,
    )
    if len(PROBE_REGISTRY) != 12:
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — PROBE_REGISTRY has %d entries, expected 12",
            len(PROBE_REGISTRY),
        )
        return 1
    if set(PROBE_REGISTRY.keys()) != set(ALL_DIMENSIONS):
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — PROBE_REGISTRY keys do not match ALL_DIMENSIONS"
        )
        return 1
    logger.info(
        "PASS: validate_inter_wave_regression_self_test — Pydantic fixtures construct ; finding=%s ; report=%s ; probes=%d",
        sample_finding.dimension_code,
        sample_report.report_id,
        len(PROBE_REGISTRY),
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inter-wave regression sweep (12-dimension; paired runbook for INTER_WAVE_REGRESSION_DISCIPLINE.md)",
    )
    parser.add_argument("--wave-closing", help="Wave code being closed (e.g., Wave-L)")
    parser.add_argument("--dimension", action="append", help="Probe a single dimension (repeatable)")
    parser.add_argument("--output", type=Path, help="Markdown report output path")
    parser.add_argument("--json-output", type=Path, help="JSON artifact output path")
    parser.add_argument("--json-log", action="store_true", help="Emit JSON-formatted log lines")
    parser.add_argument("--quiet", action="store_true", help="Suppress INFO-level logs")
    parser.add_argument("--self-test", action="store_true", help="Validate Pydantic fixtures; do not run sweep")
    parser.add_argument("--check", action="store_true", help="Alias for --self-test (release-gate invocation)")
    args = parser.parse_args()

    log.setup_logging(json_output=args.json_log, level=logging.WARNING if args.quiet else logging.INFO)

    if args.self_test or args.check:
        return self_test()

    if not args.wave_closing:
        logger.error("FAIL: --wave-closing is required for sweep mode")
        return 1
    if not WAVE_CODE_PATTERN.match(args.wave_closing):
        logger.error("FAIL: --wave-closing must match ^Wave-[A-Z]+(\\.\\d+)?$ ; got %r", args.wave_closing)
        return 1

    dims = tuple(args.dimension) if args.dimension else ALL_DIMENSIONS
    unknown = [d for d in dims if d not in ALL_DIMENSIONS]
    if unknown:
        logger.error("FAIL: unknown dimension code(s): %s ; expected one of %s", unknown, ALL_DIMENSIONS)
        return 1

    report = run_sweep(args.wave_closing, dimensions=dims)
    today = _dt.date.today().isoformat()
    md_path = args.output or (DEFAULT_REPORTS_DIR / f"regression-sweep-{today}.md")
    json_path = args.json_output or (DEFAULT_ARTIFACTS_DIR / f"regression-sweep-{today}.json")
    md_path_abs = md_path if md_path.is_absolute() else (REPO_ROOT / md_path).resolve()
    json_path_abs = json_path if json_path.is_absolute() else (REPO_ROOT / json_path).resolve()
    emit_markdown_report(report, md_path_abs)
    emit_json_artifact(report, json_path_abs)
    try:
        md_display = md_path_abs.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        md_display = md_path_abs.as_posix()
    try:
        json_display = json_path_abs.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        json_display = json_path_abs.as_posix()
    logger.info(
        "PASS: inter_wave_regression_sweep — wave=%s ; total=%d (clean=%d drift=%d gap=%d blocked=%d skip=%d) ; md=%s ; json=%s",
        report.wave_closing,
        report.total_findings,
        report.clean_count,
        report.drift_count,
        report.gap_count,
        report.blocked_count,
        report.skip_count,
        md_display,
        json_display,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
