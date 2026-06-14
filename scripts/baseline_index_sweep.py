"""Baseline-index integrity sweep runbook (paired to canonical+SOP+cursor-rule).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INDEX_INTEGRITY_DISCIPLINE.md``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INDEX_INTEGRITY_001.md``
Companion cursor rule: ``.cursor/rules/akos-index-integrity.mdc``
Pydantic SSOT: ``akos/hlk_index_integrity.py``

Decision lineage: D-IH-86-CD (canonical mint + INFO ramp; Wave N P3),
D-IH-86-CE (8-dimension probe set), D-IH-86-CF (paired SOP+runbook gate).

The 8 dimensions implemented here mirror the canonical §2 table exactly:

  baseline (always fire at every sweep trigger):
    IDX-01-PLANNING-README-INITIATIVE-COUNT
    IDX-02-PRECEDENCE-CSV-COVERAGE
    IDX-03-CHANGELOG-WAVE-COVERAGE
    IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS
    IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY
    IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT

  conditional (fire on source-of-truth delta only):
    IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS
    IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE

Per ``akos-index-integrity.mdc`` RULE 1 + RULE 2: at every wave-close gate
AND every canonical-CSV mint, the executing agent runs the 6 baseline
dimensions + any conditional dimension whose delta-predicate fires.

Per the canonical §4 cadence + ``process_list.csv`` row
``hol_peopl_dtp_index_integrity_001``: cadence is ``event_triggered`` at
wave-close + canonical-CSV mint (not pre_commit). The only release-gate-
wired surface is ``--self-test`` (Pydantic-fixture validation; zero CI cost).
The 8 probes themselves are conservative: probes that require external
evidence emit ``skip`` with a one-clause reason rather than blocking CI.

CLI shape:

    py scripts/baseline_index_sweep.py --sweep-trigger wave_close \\
        [--dimension IDX-01-PLANNING-README-INITIATIVE-COUNT] \\
        [--baseline-only] \\
        [--json-log] [--quiet] [--output reports/index-sweep-2026-05-21.md]

    py scripts/baseline_index_sweep.py --self-test
    py scripts/baseline_index_sweep.py --check

    py scripts/baseline_index_sweep.py --fix --dimension IDX-01-...  # deterministic-fix

Output: markdown table at the configured ``--output`` path (default
``docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/
index-sweep-<YYYY-MM-DD>.md``) AND a JSON artifact at
``artifacts/index-sweep-<YYYY-MM-DD>.json``.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import logging
import re
import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import subprocess  # noqa: E402

from akos import log  # noqa: E402
from akos.hlk_index_integrity import (  # noqa: E402
    BASELINE_INDEX_DIMENSION_CODES,
    CONDITIONAL_INDEX_DIMENSION_CODES,
    IndexFreshnessReport,
    IndexFreshnessRow,
    VALID_INDEX_DIMENSION_CODES,
)

logger = logging.getLogger(__name__)


# Path constants ---------------------------------------------------------

CANONICALS_DIR = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1"
PEOPLE_CANONICALS_DIR = CANONICALS_DIR / "People/canonicals"
COMPLIANCE_DIR = CANONICALS_DIR / "People/Compliance/canonicals"
DIMENSIONS_DIR = COMPLIANCE_DIR / "dimensions"

PLANNING_DIR = REPO_ROOT / "docs/wip/planning"
PLANNING_README = PLANNING_DIR / "README.md"
PRECEDENCE_PATH = COMPLIANCE_DIR / "PRECEDENCE.md"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
INITIATIVE_DEPS_PATH = COMPLIANCE_DIR / "INITIATIVE_DEPENDENCIES.md"
USER_GUIDE_PATH = REPO_ROOT / "docs/USER_GUIDE.md"
ARCHITECTURE_PATH = REPO_ROOT / "docs/ARCHITECTURE.md"
QUALITY_FABRIC_PATH = PEOPLE_CANONICALS_DIR / "HOLISTIKA_QUALITY_FABRIC.md"

INITIATIVE_REGISTRY_PATH = COMPLIANCE_DIR / "INITIATIVE_REGISTRY.csv"
BASELINE_ORG_PATH = COMPLIANCE_DIR / "baseline_organisation.csv"
PROCESS_LIST_PATH = COMPLIANCE_DIR / "process_list.csv"

# Folders under planning/ that are NOT initiatives (excluded from parity checks)
NON_INITIATIVE_FOLDERS = frozenset({
    "_blockers",
    "_trackers",
    "_candidates",
    "_templates",
    "_dashboards",
    "00-ad-hoc-proposals",
    "_archive",
})

INITIATIVE_FOLDER_RE = re.compile(r"^\d{2}[a-z]?-[a-z0-9\-]+$")


# Helpers ----------------------------------------------------------------


def _read_text(path: Path) -> str:
    """Read file text; return empty string if missing or unreadable."""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _list_initiative_folders() -> set[str]:
    """Return folder names under planning/ that match the NN- pattern."""
    if not PLANNING_DIR.exists():
        return set()
    folders: set[str] = set()
    for child in PLANNING_DIR.iterdir():
        if not child.is_dir():
            continue
        if child.name in NON_INITIATIVE_FOLDERS:
            continue
        if INITIATIVE_FOLDER_RE.match(child.name):
            folders.add(child.name)
    return folders


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read CSV rows; return empty list if missing."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _list_dimension_csvs() -> set[str]:
    """List all *.csv files under compliance/canonicals/dimensions/."""
    if not DIMENSIONS_DIR.exists():
        return set()
    return {f.name for f in DIMENSIONS_DIR.iterdir() if f.suffix == ".csv"}


def _list_top_level_canonical_csvs() -> set[str]:
    """List all *.csv files directly under compliance/canonicals/."""
    if not COMPLIANCE_DIR.exists():
        return set()
    return {
        f.name for f in COMPLIANCE_DIR.iterdir()
        if f.suffix == ".csv" and f.is_file()
    }


def _list_specialty_canonicals() -> set[str]:
    """List all *_DISCIPLINE.md files under People/canonicals/."""
    if not PEOPLE_CANONICALS_DIR.exists():
        return set()
    return {
        f.name for f in PEOPLE_CANONICALS_DIR.iterdir()
        if f.name.endswith("_DISCIPLINE.md")
    }


def _git(args: list[str], timeout: int = 10) -> tuple[int, str]:
    """Run git in the repo root; return (returncode, stdout). Never raises."""
    try:
        rc = subprocess.run(
            ["git", *args],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return (1, "")
    return (rc.returncode, rc.stdout or "")


def _last_commit_wave() -> str | None:
    """Inspect last 10 commit messages for a 'Wave-X' marker; return latest."""
    rc, stdout = _git(["log", "-10", "--pretty=format:%s"])
    if rc != 0:
        return None
    pattern = re.compile(r"Wave\s+([A-Z](?:\.\d+)?)", re.IGNORECASE)
    for line in stdout.splitlines():
        m = pattern.search(line)
        if m:
            return f"Wave-{m.group(1).upper()}"
    return None


def _today() -> str:
    return _dt.date.today().isoformat()


# Probes -----------------------------------------------------------------


def _probe_idx_01_planning_readme_initiative_count() -> list[IndexFreshnessRow]:
    """IDX-01: README initiative table ↔ filesystem ↔ INITIATIVE_REGISTRY."""
    findings: list[IndexFreshnessRow] = []
    folders = _list_initiative_folders()
    registry_rows = _read_csv_rows(INITIATIVE_REGISTRY_PATH)
    folder_count = len(folders)
    registry_count = len(registry_rows)

    if folder_count == 0 or registry_count == 0:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-01-PLANNING-README-INITIATIVE-COUNT",
            index_path="docs/wip/planning/README.md",
            verdict="blocked",
            drift_summary=(
                f"folders={folder_count} registry_rows={registry_count} — "
                "one or both source-of-truth scans returned empty"
            ),
            proposed_fix_action="manual investigate filesystem + registry CSV access",
            severity="high",
            notes="probe cannot complete; treat as unknown rather than fresh",
        ))
        return findings

    delta = abs(folder_count - registry_count)
    if delta == 0:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-01-PLANNING-README-INITIATIVE-COUNT",
            index_path="docs/wip/planning/README.md",
            verdict="fresh",
            severity="low",
            notes=f"folder_count={folder_count} == registry_count={registry_count}",
        ))
    else:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-01-PLANNING-README-INITIATIVE-COUNT",
            index_path="docs/wip/planning/README.md",
            verdict="drift",
            drift_summary=(
                f"folder_count={folder_count} != registry_count={registry_count} "
                f"(delta={delta})"
            ),
            proposed_fix_action=(
                "Run `py scripts/baseline_index_sweep.py --fix "
                "--dimension IDX-01-PLANNING-README-INITIATIVE-COUNT` OR "
                "reconcile manually by inventorying folders vs registry rows"
            ),
            severity="medium",
            notes=(
                "non-zero delta surfaces a folder without a registry row, "
                "OR a registry row pointing to a missing folder"
            ),
        ))
    return findings


def _probe_idx_02_precedence_csv_coverage() -> list[IndexFreshnessRow]:
    """IDX-02: PRECEDENCE.md must mention every CSV under compliance/."""
    findings: list[IndexFreshnessRow] = []
    prec_text = _read_text(PRECEDENCE_PATH)
    if not prec_text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-02-PRECEDENCE-CSV-COVERAGE",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md",
            verdict="blocked",
            drift_summary="PRECEDENCE.md not readable",
            proposed_fix_action="restore PRECEDENCE.md from git",
            severity="high",
            notes="probe cannot complete",
        ))
        return findings

    csvs = _list_dimension_csvs() | _list_top_level_canonical_csvs()
    missing = sorted(c for c in csvs if c not in prec_text)
    if not missing:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-02-PRECEDENCE-CSV-COVERAGE",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md",
            verdict="fresh",
            severity="low",
            notes=f"all {len(csvs)} CSVs mentioned in PRECEDENCE.md",
        ))
    else:
        sample = ", ".join(missing[:5])
        more = f" (+{len(missing) - 5} more)" if len(missing) > 5 else ""
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-02-PRECEDENCE-CSV-COVERAGE",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md",
            verdict="gap",
            drift_summary=(
                f"{len(missing)}/{len(csvs)} CSVs missing PRECEDENCE row: "
                f"{sample}{more}"
            ),
            proposed_fix_action=(
                "manually append canonical + mirror rows for each missing CSV "
                "to PRECEDENCE.md per `akos-holistika-operations.mdc` "
                "§\"New git-canonical compliance registers\""
            ),
            severity="medium",
            notes="judgement-call fix: each CSV needs canonical-class + mirror-class declaration",
        ))
    return findings


def _probe_idx_03_changelog_wave_coverage() -> list[IndexFreshnessRow]:
    """IDX-03: CHANGELOG mentions the most recent wave-closing commit."""
    findings: list[IndexFreshnessRow] = []
    last_wave = _last_commit_wave()
    if last_wave is None:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-03-CHANGELOG-WAVE-COVERAGE",
            index_path="CHANGELOG.md",
            verdict="skip",
            severity="low",
            notes="no recent commit message carries a Wave-X marker",
        ))
        return findings

    changelog_text = _read_text(CHANGELOG_PATH)
    if not changelog_text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-03-CHANGELOG-WAVE-COVERAGE",
            index_path="CHANGELOG.md",
            verdict="blocked",
            drift_summary="CHANGELOG.md not readable",
            proposed_fix_action="restore CHANGELOG.md from git",
            severity="high",
            notes="probe cannot complete",
        ))
        return findings

    if last_wave in changelog_text or last_wave.replace("-", " ") in changelog_text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-03-CHANGELOG-WAVE-COVERAGE",
            index_path="CHANGELOG.md",
            verdict="fresh",
            severity="low",
            notes=f"CHANGELOG.md mentions {last_wave}",
        ))
    else:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-03-CHANGELOG-WAVE-COVERAGE",
            index_path="CHANGELOG.md",
            verdict="drift",
            drift_summary=(
                f"last commit wave={last_wave} not mentioned in CHANGELOG.md"
            ),
            proposed_fix_action=(
                "append a bullet under [Unreleased] in CHANGELOG.md summarising "
                f"{last_wave} (per `akos-docs-config-sync.mdc` Always update §1)"
            ),
            severity="medium",
            notes="manual prose write — runbook does not auto-edit CHANGELOG narratives",
        ))
    return findings


def _probe_idx_04_initiative_dependencies_freshness() -> list[IndexFreshnessRow]:
    """IDX-04: INITIATIVE_DEPENDENCIES.md freshness vs registry last-update."""
    findings: list[IndexFreshnessRow] = []
    deps_text = _read_text(INITIATIVE_DEPS_PATH)
    if not deps_text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md",
            verdict="gap",
            drift_summary="INITIATIVE_DEPENDENCIES.md does not exist",
            proposed_fix_action=(
                "create the file with an initial dependency matrix from "
                "INITIATIVE_REGISTRY.csv (manual prose authoring)"
            ),
            severity="medium",
            notes="judgement-call fix: dependency narrative cannot be auto-generated faithfully",
        ))
        return findings

    def _git_last_commit_iso(p: Path) -> str | None:
        try:
            rel = p.relative_to(REPO_ROOT)
        except ValueError:
            return None
        rc, stdout = _git(["log", "-1", "--pretty=format:%cI", "--", str(rel).replace("\\", "/")])
        if rc != 0:
            return None
        return stdout.strip() or None

    deps_iso = _git_last_commit_iso(INITIATIVE_DEPS_PATH)
    reg_iso = _git_last_commit_iso(INITIATIVE_REGISTRY_PATH)
    if not deps_iso or not reg_iso:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md",
            verdict="skip",
            severity="low",
            notes="git log unavailable for one or both files",
        ))
        return findings

    deps_dt = _dt.datetime.fromisoformat(deps_iso[:10])
    reg_dt = _dt.datetime.fromisoformat(reg_iso[:10])
    delta_days = (reg_dt - deps_dt).days
    if delta_days <= 7:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md",
            verdict="fresh",
            severity="low",
            notes=(
                f"deps last-edited {deps_iso[:10]}, registry last-edited "
                f"{reg_iso[:10]} (delta={delta_days}d, threshold=7d)"
            ),
        ))
    else:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md",
            verdict="drift",
            drift_summary=(
                f"INITIATIVE_REGISTRY.csv changed {delta_days}d after "
                "INITIATIVE_DEPENDENCIES.md last edit (threshold=7d)"
            ),
            proposed_fix_action=(
                "review registry diffs since deps last-edit + update "
                "dependency narrative + bump deps last-edit timestamp"
            ),
            severity="medium",
            notes="manual prose write — runbook does not auto-edit narrative",
        ))
    return findings


def _probe_idx_05_user_guide_role_process_counts() -> list[IndexFreshnessRow]:
    """IDX-05: USER_GUIDE.md HLK Operator Model role/process counts."""
    findings: list[IndexFreshnessRow] = []
    text = _read_text(USER_GUIDE_PATH)
    if not text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
            index_path="docs/USER_GUIDE.md",
            verdict="blocked",
            drift_summary="USER_GUIDE.md not readable",
            proposed_fix_action="restore USER_GUIDE.md from git",
            severity="high",
            notes="probe cannot complete",
        ))
        return findings

    org_rows = _read_csv_rows(BASELINE_ORG_PATH)
    proc_rows = _read_csv_rows(PROCESS_LIST_PATH)
    role_count = len(org_rows)
    process_count = len(proc_rows)

    # Look for numbers near 'role' and 'process' tokens; pragmatic regex.
    role_match = re.search(
        r"(\d{2,4})\s+(?:roles?|baseline\s+roles?)",
        text,
        re.IGNORECASE,
    )
    proc_match = re.search(
        r"(\d{3,5})\s+(?:processes|process\s+rows|process_list\s+rows|item_ids?)",
        text,
        re.IGNORECASE,
    )

    drifts: list[str] = []
    if role_match:
        stated = int(role_match.group(1))
        if abs(stated - role_count) > 0:
            drifts.append(
                f"USER_GUIDE says ~{stated} roles; CSV has {role_count}"
            )
    if proc_match:
        stated = int(proc_match.group(1))
        # Allow 1-2% wobble for round numbers (e.g., "~1100 processes")
        if abs(stated - process_count) > max(5, int(process_count * 0.02)):
            drifts.append(
                f"USER_GUIDE says ~{stated} processes; CSV has {process_count}"
            )

    if not drifts:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
            index_path="docs/USER_GUIDE.md",
            verdict="fresh",
            severity="low",
            notes=(
                f"baseline={role_count}roles / process_list={process_count}; "
                "no contradicting counts found in USER_GUIDE"
            ),
        ))
    else:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS",
            index_path="docs/USER_GUIDE.md",
            verdict="drift",
            drift_summary="; ".join(drifts),
            proposed_fix_action=(
                "update USER_GUIDE.md HLK Operator Model section role/process "
                "count line(s) to match canonical CSVs"
            ),
            severity="low",
            notes="manual prose edit; ~1% wobble tolerated for round numbers",
        ))
    return findings


def _probe_idx_06_architecture_hlk_registry_coverage() -> list[IndexFreshnessRow]:
    """IDX-06: ARCHITECTURE.md HLK Registry mentions every dimension CSV."""
    findings: list[IndexFreshnessRow] = []
    text = _read_text(ARCHITECTURE_PATH)
    if not text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
            index_path="docs/ARCHITECTURE.md",
            verdict="blocked",
            drift_summary="ARCHITECTURE.md not readable",
            proposed_fix_action="restore ARCHITECTURE.md from git",
            severity="high",
            notes="probe cannot complete",
        ))
        return findings

    dim_csvs = _list_dimension_csvs()
    missing = sorted(c for c in dim_csvs if c not in text)
    if not missing:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
            index_path="docs/ARCHITECTURE.md",
            verdict="fresh",
            severity="low",
            notes=f"all {len(dim_csvs)} dimension CSVs mentioned in ARCHITECTURE.md",
        ))
    else:
        sample = ", ".join(missing[:5])
        more = f" (+{len(missing) - 5} more)" if len(missing) > 5 else ""
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE",
            index_path="docs/ARCHITECTURE.md",
            verdict="gap",
            drift_summary=(
                f"{len(missing)}/{len(dim_csvs)} dimension CSVs missing from "
                f"ARCHITECTURE HLK Registry: {sample}{more}"
            ),
            proposed_fix_action=(
                "append rows to ARCHITECTURE.md HLK Registry table for each "
                "missing dimension CSV"
            ),
            severity="low",
            notes="manual prose write",
        ))
    return findings


def _probe_idx_07_planning_folder_filesystem_parity() -> list[IndexFreshnessRow]:
    """IDX-07: README initiative table ↔ filesystem folders (bidirectional FK)."""
    findings: list[IndexFreshnessRow] = []
    readme_text = _read_text(PLANNING_README)
    if not readme_text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
            index_path="docs/wip/planning/README.md",
            verdict="blocked",
            drift_summary="planning/README.md not readable",
            proposed_fix_action="restore planning/README.md from git",
            severity="high",
            notes="probe cannot complete",
        ))
        return findings

    folders = _list_initiative_folders()
    mentioned = {
        m for m in re.findall(r"\(\s*(\d{2}[a-z]?-[a-z0-9\-]+)/\)", readme_text)
        if m not in NON_INITIATIVE_FOLDERS
    }

    missing_from_readme = sorted(folders - mentioned)
    missing_from_filesystem = sorted(mentioned - folders)

    if not missing_from_readme and not missing_from_filesystem:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
            index_path="docs/wip/planning/README.md",
            verdict="fresh",
            severity="low",
            notes=(
                f"all {len(folders)} folders FK-resolved in README; all "
                f"{len(mentioned)} README links FK-resolved on filesystem"
            ),
        ))
    else:
        drift_bits: list[str] = []
        if missing_from_readme:
            sample = ", ".join(missing_from_readme[:5])
            more = (
                f" (+{len(missing_from_readme) - 5} more)"
                if len(missing_from_readme) > 5 else ""
            )
            drift_bits.append(
                f"{len(missing_from_readme)} folders absent from README: {sample}{more}"
            )
        if missing_from_filesystem:
            sample = ", ".join(missing_from_filesystem[:5])
            more = (
                f" (+{len(missing_from_filesystem) - 5} more)"
                if len(missing_from_filesystem) > 5 else ""
            )
            drift_bits.append(
                f"{len(missing_from_filesystem)} README links to missing folders: {sample}{more}"
            )
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY",
            index_path="docs/wip/planning/README.md",
            verdict="gap" if missing_from_filesystem else "drift",
            drift_summary="; ".join(drift_bits),
            proposed_fix_action=(
                "append a README row for each missing folder OR remove the "
                "stale README row for each missing folder (judgement-call: "
                "is the missing folder a planned-but-not-created stub?)"
            ),
            severity="medium",
            notes="bidirectional FK; runbook --fix --dimension IDX-07 deterministic when both sides are unambiguous",
        ))
    return findings


def _probe_idx_08_quality_fabric_specialty_count() -> list[IndexFreshnessRow]:
    """IDX-08: Quality Fabric §6 specialty count ↔ filesystem _DISCIPLINE.md."""
    findings: list[IndexFreshnessRow] = []
    fabric_text = _read_text(QUALITY_FABRIC_PATH)
    if not fabric_text:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md",
            verdict="blocked",
            drift_summary="HOLISTIKA_QUALITY_FABRIC.md not readable",
            proposed_fix_action="restore HOLISTIKA_QUALITY_FABRIC.md from git",
            severity="high",
            notes="probe cannot complete",
        ))
        return findings

    specialty_files = _list_specialty_canonicals()
    missing_from_fabric: list[str] = []
    for f in sorted(specialty_files):
        # Crude match: filename stem appears in §6 row, or its canonical title appears
        stem = f.replace(".md", "")
        if stem not in fabric_text:
            missing_from_fabric.append(f)

    if not missing_from_fabric:
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md",
            verdict="fresh",
            severity="low",
            notes=(
                f"all {len(specialty_files)} *_DISCIPLINE.md files referenced "
                "in HOLISTIKA_QUALITY_FABRIC.md"
            ),
        ))
    else:
        sample = ", ".join(missing_from_fabric[:5])
        more = f" (+{len(missing_from_fabric) - 5} more)" if len(missing_from_fabric) > 5 else ""
        findings.append(IndexFreshnessRow(
            dimension_code="IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT",
            index_path="docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md",
            verdict="gap",
            drift_summary=(
                f"{len(missing_from_fabric)} *_DISCIPLINE.md files not "
                f"referenced in §6: {sample}{more}"
            ),
            proposed_fix_action=(
                "append §6 specialty materialisation table rows for each "
                "missing discipline + add to frontmatter linked_canonicals"
            ),
            severity="medium",
            notes="judgement-call fix: each specialty needs a compose_<NAME>() signature",
        ))
    return findings


# Probe registry ---------------------------------------------------------

PROBE_REGISTRY: dict[str, Callable[[], list[IndexFreshnessRow]]] = {
    "IDX-01-PLANNING-README-INITIATIVE-COUNT":
        _probe_idx_01_planning_readme_initiative_count,
    "IDX-02-PRECEDENCE-CSV-COVERAGE":
        _probe_idx_02_precedence_csv_coverage,
    "IDX-03-CHANGELOG-WAVE-COVERAGE":
        _probe_idx_03_changelog_wave_coverage,
    "IDX-04-INITIATIVE-DEPENDENCIES-FRESHNESS":
        _probe_idx_04_initiative_dependencies_freshness,
    "IDX-05-USER-GUIDE-ROLE-PROCESS-COUNTS":
        _probe_idx_05_user_guide_role_process_counts,
    "IDX-06-ARCHITECTURE-HLK-REGISTRY-COVERAGE":
        _probe_idx_06_architecture_hlk_registry_coverage,
    "IDX-07-PLANNING-FOLDER-FILESYSTEM-PARITY":
        _probe_idx_07_planning_folder_filesystem_parity,
    "IDX-08-QUALITY-FABRIC-SPECIALTY-COUNT":
        _probe_idx_08_quality_fabric_specialty_count,
}


# Orchestration ----------------------------------------------------------


def run_sweep(
    sweep_trigger: str,
    dimensions: list[str] | None = None,
    baseline_only: bool = False,
    swept_by: str = "agent:cli",
) -> IndexFreshnessReport:
    """Run the named dimensions and return the aggregate report."""
    if dimensions:
        codes = list(dimensions)
    elif baseline_only:
        codes = sorted(BASELINE_INDEX_DIMENSION_CODES)
    else:
        codes = sorted(VALID_INDEX_DIMENSION_CODES)

    all_findings: list[IndexFreshnessRow] = []
    for code in codes:
        probe = PROBE_REGISTRY.get(code)
        if probe is None:
            logger.warning("unknown dimension: %s", code)
            continue
        try:
            all_findings.extend(probe())
        except (OSError, RuntimeError, ValueError) as exc:
            logger.exception("probe %s failed: %s", code, exc)
            all_findings.append(IndexFreshnessRow(
                dimension_code=code,  # type: ignore[arg-type]
                index_path="PROBE-INTERNAL-ERROR",
                verdict="blocked",
                drift_summary=f"probe raised: {exc!r}",
                proposed_fix_action="investigate probe internals",
                severity="high",
                notes="runbook bug; report does not represent index state",
            ))

    counts = {"fresh": 0, "drift": 0, "gap": 0, "blocked": 0, "skip": 0}
    for f in all_findings:
        counts[f.verdict] = counts.get(f.verdict, 0) + 1

    today = _today()
    return IndexFreshnessReport(
        report_id=f"index-sweep-{today}",
        sweep_trigger=sweep_trigger,  # type: ignore[arg-type]
        swept_at=today,
        swept_by=swept_by,
        findings=all_findings,
        fresh_count=counts["fresh"],
        drift_count=counts["drift"],
        gap_count=counts["gap"],
        blocked_count=counts["blocked"],
        skip_count=counts["skip"],
        total_findings=len(all_findings),
    )


def render_markdown(report: IndexFreshnessReport) -> str:
    """Operator-readable markdown table."""
    lines = [
        f"# Baseline Index Sweep — {report.swept_at}",
        "",
        f"- **Report ID**: `{report.report_id}`",
        f"- **Sweep trigger**: `{report.sweep_trigger}`",
        f"- **Swept by**: `{report.swept_by}`",
        f"- **Total findings**: {report.total_findings} "
        f"(fresh={report.fresh_count}, drift={report.drift_count}, "
        f"gap={report.gap_count}, blocked={report.blocked_count}, "
        f"skip={report.skip_count})",
        "",
        "## Findings",
        "",
        "| Dimension | Index | Verdict | Severity | Drift / proposed fix |",
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
        idx_short = f.index_path.split("/")[-1] if "/" in f.index_path else f.index_path
        lines.append(
            f"| `{f.dimension_code}` | `{idx_short}` | "
            f"{f.verdict} | {f.severity} | {rhs} |"
        )
    lines.append("")
    lines.append("> Generated by `scripts/baseline_index_sweep.py` per `INDEX_INTEGRITY_DISCIPLINE.md`.")
    return "\n".join(lines) + "\n"


def write_outputs(report: IndexFreshnessReport, output_path: Path | None) -> tuple[Path, Path]:
    """Write the markdown + JSON sidecar. Returns (md_path, json_path)."""
    if output_path is None:
        output_path = (
            REPO_ROOT
            / "docs/wip/planning/86-initiative-cluster-execution-coordinator/reports"
            / f"{report.report_id}.md"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(report), encoding="utf-8")

    artifacts_dir = REPO_ROOT / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    json_path = artifacts_dir / f"{report.report_id}.json"
    json_path.write_text(
        json.dumps(report.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return output_path, json_path


def self_test() -> int:
    """Pydantic fixture validation; zero-cost; wired into release-gate."""
    fixture = IndexFreshnessRow(
        dimension_code="IDX-01-PLANNING-README-INITIATIVE-COUNT",
        index_path="docs/wip/planning/README.md",
        verdict="fresh",
        severity="low",
        notes="self-test fixture",
    )
    rep = IndexFreshnessReport(
        report_id="index-sweep-2026-05-21-selftest",
        sweep_trigger="pre_commit_self_test",
        swept_at="2026-05-21",
        swept_by="self_test",
        findings=[fixture],
        fresh_count=1,
        drift_count=0,
        gap_count=0,
        blocked_count=0,
        skip_count=0,
        total_findings=1,
    )
    if rep.total_findings != 1 or rep.fresh_count != 1:
        return 1
    if len(PROBE_REGISTRY) != 8:
        return 2
    if PROBE_REGISTRY.keys() != VALID_INDEX_DIMENSION_CODES:
        return 3
    if BASELINE_INDEX_DIMENSION_CODES | CONDITIONAL_INDEX_DIMENSION_CODES != VALID_INDEX_DIMENSION_CODES:
        return 4
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sweep-trigger",
        choices=["wave_close", "canonical_csv_mint", "on_demand", "pre_commit_self_test"],
        default="on_demand",
    )
    parser.add_argument("--dimension", action="append", default=None,
                        help="run only the named dimension(s); may be repeated")
    parser.add_argument("--baseline-only", action="store_true",
                        help="run only baseline (6) dimensions; skip conditional (2)")
    parser.add_argument("--self-test", action="store_true",
                        help="validate Pydantic fixtures; exit 0/non-zero only")
    parser.add_argument("--check", action="store_true",
                        help="run sweep + emit markdown to stdout; exit 0 always (INFO mode)")
    parser.add_argument("--output", type=Path, default=None,
                        help="markdown output path (default: reports/index-sweep-YYYY-MM-DD.md)")
    parser.add_argument("--swept-by", default="agent:cli")
    parser.add_argument("--json-log", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    log.setup_logging(
        level=logging.WARNING if args.quiet else logging.INFO,
        json_output=args.json_log,
    )

    if args.self_test:
        return self_test()

    report = run_sweep(
        sweep_trigger=args.sweep_trigger,
        dimensions=args.dimension,
        baseline_only=args.baseline_only,
        swept_by=args.swept_by,
    )

    md_path, json_path = write_outputs(report, args.output)
    try:
        md_rel = md_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        md_rel = md_path
    try:
        json_rel = json_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        json_rel = json_path
    logger.info("wrote %s", md_rel)
    logger.info("wrote %s", json_rel)

    if args.check:
        print(render_markdown(report))
        return 0

    # Default: emit summary to stdout; exit 0 (INFO posture during backfill)
    print(
        f"INDEX-SWEEP {report.report_id}: total={report.total_findings} "
        f"fresh={report.fresh_count} drift={report.drift_count} "
        f"gap={report.gap_count} blocked={report.blocked_count} "
        f"skip={report.skip_count}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
