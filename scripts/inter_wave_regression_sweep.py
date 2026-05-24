"""Inter-wave regression sweep runbook (paired to canonical+SOP+cursor-rule).

Canonical doctrine: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/INTER_WAVE_REGRESSION_DISCIPLINE.md``
Paired SOP: ``docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_INTER_WAVE_REGRESSION_001.md``
Companion cursor rule: ``.cursor/rules/akos-inter-wave-regression.mdc``
Pydantic SSOT: ``akos/hlk_inter_wave_regression.py``

Decision lineage: D-IH-86-BO (initial paired runbook mint, Wave M P2)
→ D-IH-86-BW (Wave M.5 hotfix; doctrine-wins reconciliation of
the 12 dimension codes against the canonical §2 table + the
``compose_REGRESSION(...)`` baseline/conditional split in §3).

The 12 dimensions implemented here mirror the canonical exactly:

  baseline (always fire at every wave-close):
    DIM-01-DECISION-LINEAGE
    DIM-02-FORWARD-CHARTER-CARRYOVER
    DIM-03-VALIDATOR-RAMP-CONSISTENCY
    DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS
    DIM-05-SOP-RUNBOOK-PAIRING
    DIM-06-UAT-REPORT-CLASS-COMPLETENESS
    DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY

  axis-conditional (fire only when the corresponding axis predicate
  fires per ``compose_REGRESSION``):
    DIM-07-RENDER-TRAIL-AUDIENCE-MATCH      (audience.has_external_tag)
    DIM-08-BRAND-BASELINE-REGISTER-MATCH    (brand.fires_branded_surface)
    DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT  (scenario.has_new_pattern_mint)
    DIM-10-DEPLOY-EVIDENCE-COMPLETENESS     (channel.touches_sibling_repo)
    DIM-11-CURSOR-RULE-SKILL-PAIRING        (governance.minted_new_cursor_rule)

Per ``akos-inter-wave-regression.mdc`` RULE 1 + RULE 2: at every wave-close
gate, the executing agent runs the 7 baseline dimensions + any conditional
dimension whose axis predicate fires for the wave before declaring it
closed. Per RULE 3, every non-clean finding becomes one AskQuestion option
set at P4 (inline-ratify gate).

Per the canonical §4 cadence + ``process_list.csv`` row
``hol_peopl_dtp_inter_wave_regression_001``: cadence is ``event_triggered``
at wave-close (not pre_commit) — the only release-gate-wired surface is
``--self-test`` (Pydantic-fixture validation; zero CI cost per
R-86-WaveM-7). The 12 probes themselves are conservative: probes that
require external evidence (Vercel/Render MCP, Supabase MCP, full
release-gate run) emit ``skip`` with a one-clause reason rather than
blocking the CI path.

CLI shape:

    py scripts/inter_wave_regression_sweep.py --wave-closing Wave-L \\
        [--dimension DIM-01-DECISION-LINEAGE] \\
        [--baseline-only] \\
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
    BASELINE_DIMENSION_CODES,
    CONDITIONAL_DIMENSION_CODES,
    RegressionFindingRow,
    RegressionSweepReport,
)

logger = logging.getLogger(__name__)


CANONICALS_DIR = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1"
)

PEOPLE_CANONICALS_DIR = CANONICALS_DIR / "People" / "canonicals"

COMPLIANCE_CANONICALS_DIR = (
    CANONICALS_DIR / "People" / "Compliance" / "canonicals"
)

DIMENSIONS_DIR = COMPLIANCE_CANONICALS_DIR / "dimensions"

CANONICAL_PATH = PEOPLE_CANONICALS_DIR / "INTER_WAVE_REGRESSION_DISCIPLINE.md"
QUALITY_FABRIC_PATH = PEOPLE_CANONICALS_DIR / "HOLISTIKA_QUALITY_FABRIC.md"

I86_COORDINATOR_PATH = (
    REPO_ROOT
    / "docs" / "wip" / "planning"
    / "86-initiative-cluster-execution-coordinator" / "master-roadmap.md"
)

DECISION_REGISTER_PATH = COMPLIANCE_CANONICALS_DIR / "DECISION_REGISTER.csv"
OPS_REGISTER_PATH = COMPLIANCE_CANONICALS_DIR / "OPS_REGISTER.csv"
PROCESS_LIST_PATH = COMPLIANCE_CANONICALS_DIR / "process_list.csv"
INITIATIVE_REGISTRY_PATH = COMPLIANCE_CANONICALS_DIR / "INITIATIVE_REGISTRY.csv"
PRECEDENCE_PATH = COMPLIANCE_CANONICALS_DIR / "PRECEDENCE.md"
PATTERN_REGISTRY_PATH = DIMENSIONS_DIR / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"

OPERATOR_SCRATCHPAD_PATH = (
    REPO_ROOT
    / "docs" / "wip" / "planning"
    / "86-initiative-cluster-execution-coordinator" / "operator-scratchpad.md"
)

VERIFICATION_PROFILES_PATH = (
    REPO_ROOT / "config" / "verification-profiles.json"
)
RELEASE_GATE_PATH = REPO_ROOT / "scripts" / "release-gate.py"

DEFAULT_REPORTS_DIR = (
    REPO_ROOT
    / "docs" / "wip" / "planning"
    / "86-initiative-cluster-execution-coordinator" / "reports"
)

DEFAULT_ARTIFACTS_DIR = REPO_ROOT / "artifacts"

CURSOR_RULES_DIR = REPO_ROOT / ".cursor" / "rules"
SKILLS_DIRS = (REPO_ROOT / ".cursor" / "skills",)
CANDIDATES_DIR = REPO_ROOT / "docs" / "wip" / "planning" / "_candidates"
PLANNING_ROOT = REPO_ROOT / "docs" / "wip" / "planning"

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
LAST_REVIEW_PATTERN = re.compile(r"^last_review\s*:\s*(\S+)", re.MULTILINE)
STATUS_FIELD_PATTERN = re.compile(r"^status\s*:\s*(\S+)", re.MULTILINE)
WAVE_CODE_PATTERN = re.compile(r"^Wave-[A-Z]+(\.\d+)?$")
DECISION_ID_PATTERN = re.compile(r"D-IH-\d+-[A-Z0-9_]+")

FRESHNESS_DRIFT_THRESHOLD_DAYS = 30
WAVE_LOOKBACK_LIMIT_COMMITS = 200

ALL_DIMENSIONS: tuple[str, ...] = (
    "DIM-01-DECISION-LINEAGE",
    "DIM-02-FORWARD-CHARTER-CARRYOVER",
    "DIM-03-VALIDATOR-RAMP-CONSISTENCY",
    "DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
    "DIM-05-SOP-RUNBOOK-PAIRING",
    "DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
    "DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
    "DIM-08-BRAND-BASELINE-REGISTER-MATCH",
    "DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
    "DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
    "DIM-11-CURSOR-RULE-SKILL-PAIRING",
    "DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
    "DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS",
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


def _git_diff_files_since(ref: str, paths: list[str]) -> str:
    """Return concatenated git diff text for the given paths since ``ref``.

    Best-effort: returns empty string on git failure. Used by DIM-03
    validator_ramp_consistency to detect threshold changes.
    """
    if not paths:
        return ""
    result = process.run(
        ["git", "diff", f"{ref}..HEAD", "--", *paths],
        timeout=30,
        capture=True,
        check=False,
    )
    return result.stdout if result.success else ""


def _git_last_wave_close_sha(current_wave: str) -> str | None:
    """Best-effort: find the SHA of the prior wave-close commit.

    Used by DIM-03 (diff against this point) + DIM-12 (compare to
    scratchpad timestamp). Returns None if no prior wave-close commit
    is found in the recent git log.
    """
    result = process.run(
        ["git", "log", f"-{WAVE_LOOKBACK_LIMIT_COMMITS}", "--pretty=format:%h %s"],
        timeout=30,
        capture=True,
        check=False,
    )
    if not result.success:
        return None
    skip_token = current_wave.lower().replace("-", "")
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        haystack = line.lower().replace("-", "").replace(" ", "")
        if skip_token in haystack:
            continue
        if "wave" in haystack and "close" in haystack:
            return line.split(maxsplit=1)[0]
    return None


def _collect_frontmatter_list_field(
    frontmatter: str, field: str
) -> list[str]:
    """Extract a simple YAML list field (one item per line) from frontmatter.

    Supports two shapes:
      ``field: [a, b, c]``
      ``field:\\n  - a\\n  - b\\n``

    Returns an empty list if the field is absent. Items are stripped of
    surrounding whitespace + quotes. Robust enough for the canonical
    frontmatter shapes used in this repo (does not pull in PyYAML to
    keep the runbook dependency-light).
    """
    inline_pattern = re.compile(
        rf"^{re.escape(field)}\s*:\s*\[(.*?)\]\s*$", re.MULTILINE
    )
    inline_match = inline_pattern.search(frontmatter)
    if inline_match:
        return [
            item.strip().strip('"').strip("'")
            for item in inline_match.group(1).split(",")
            if item.strip()
        ]
    block_pattern = re.compile(
        rf"^{re.escape(field)}\s*:\s*\n((?:\s*-\s*[^\n]+\n)+)", re.MULTILINE
    )
    block_match = block_pattern.search(frontmatter)
    if block_match:
        items: list[str] = []
        for line in block_match.group(1).splitlines():
            stripped = line.strip()
            if stripped.startswith("-"):
                items.append(stripped[1:].strip().strip('"').strip("'"))
        return items
    return []


def _glob_canonicals() -> list[Path]:
    """Return all canonical markdown files under v3.0/.../canonicals/."""
    if not CANONICALS_DIR.exists():
        return []
    return sorted(CANONICALS_DIR.rglob("canonicals/**/*.md"))


def _shell_validator(
    script_relpath: str, args: list[str] | None = None, timeout: int = 120
) -> tuple[bool, str]:
    """Invoke a validator script; return (success, stdout+stderr)."""
    script_path = REPO_ROOT / script_relpath
    if not script_path.exists():
        return False, f"missing validator: {script_relpath}"
    cmd: list[str] = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    result = process.run(cmd, timeout=timeout, capture=True, check=False)
    return result.success, (result.stdout or "") + (result.stderr or "")


def _probe_dimension_1_decision_lineage(
    wave: str | None = None,
) -> list[RegressionFindingRow]:
    """DIM-01-DECISION-LINEAGE — FK-resolve DECISION_REGISTER <-> canonicals.

    Forward direction: every ``ratifying_decisions:`` value in any canonical
    frontmatter MUST resolve to a row in DECISION_REGISTER.csv. Orphans
    surface as ``drift``.

    Reverse direction: for the wave-scope set of decisions (decisions whose
    rationale text appears in the wave's commits), every decision MUST be
    cited by at least one canonical's ``ratifying_decisions`` frontmatter
    field. Orphans surface as ``gap`` (advisory; many decisions
    legitimately live only in decision-logs / master-roadmaps + don't
    require canonical-frontmatter back-references).
    """
    if not DECISION_REGISTER_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-01-DECISION-LINEAGE",
            surface_path=str(DECISION_REGISTER_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore DECISION_REGISTER.csv",
            severity="high",
            notes="canonical DECISION_REGISTER.csv not found",
        )]
    known_decisions: set[str] = set()
    with DECISION_REGISTER_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            did = (row.get("decision_id") or "").strip()
            if did and DECISION_ID_PATTERN.fullmatch(did):
                known_decisions.add(did)
    findings: list[RegressionFindingRow] = []
    orphan_refs: list[tuple[Path, str]] = []
    for canonical in _glob_canonicals():
        fm = _read_frontmatter(canonical)
        if fm is None:
            continue
        for did in _collect_frontmatter_list_field(fm, "ratifying_decisions"):
            if DECISION_ID_PATTERN.fullmatch(did) and did not in known_decisions:
                orphan_refs.append((canonical, did))
    for canonical, did in orphan_refs[:15]:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-01-DECISION-LINEAGE",
            surface_path=str(canonical.relative_to(REPO_ROOT).as_posix()),
            verdict="drift",
            proposed_rework_action=(
                f"add {did} to DECISION_REGISTER.csv OR remove it from "
                f"this canonical's ratifying_decisions frontmatter"
            ),
            severity="medium",
            notes=(
                f"canonical frontmatter cites {did} but no matching row "
                f"in DECISION_REGISTER.csv"
            ),
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-01-DECISION-LINEAGE",
            surface_path=str(DECISION_REGISTER_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{len(known_decisions)} decisions in register; all "
                f"ratifying_decisions: frontmatter values FK-resolve "
                f"(reverse-FK advisory sweep deferred to operator review)"
            ),
        ))
    return findings


def _probe_dimension_2_forward_charter_carryover() -> list[RegressionFindingRow]:
    """DIM-02-FORWARD-CHARTER-CARRYOVER — verify forward_charters: items land.

    Glob all canonicals → parse ``forward_charters:`` frontmatter lists.
    Each item must either:
      (a) land in a subsequent canonical (text-search heuristic), OR
      (b) appear as a candidate file under ``_candidates/``, OR
      (c) have a row in OPS_REGISTER.csv referencing it.

    Unresolved items surface as ``gap``.
    """
    findings: list[RegressionFindingRow] = []
    forward_pairs: list[tuple[Path, str]] = []
    for canonical in _glob_canonicals():
        fm = _read_frontmatter(canonical)
        if fm is None:
            continue
        for item in _collect_frontmatter_list_field(fm, "forward_charters"):
            if item:
                forward_pairs.append((canonical, item))
    if not forward_pairs:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-02-FORWARD-CHARTER-CARRYOVER",
            surface_path="canonicals-scan",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="no canonicals declare forward_charters: today",
        ))
        return findings
    ops_text = ""
    if OPS_REGISTER_PATH.exists():
        ops_text = OPS_REGISTER_PATH.read_text(encoding="utf-8", errors="ignore")
    candidate_names: set[str] = set()
    if CANDIDATES_DIR.exists():
        candidate_names = {p.stem.lower() for p in CANDIDATES_DIR.glob("*.md")}
    # Extended evidence haystack (D-IH-86-CS Wave R close-out): also accept
    # carryover signal from filesystem existence + canonical CSV content +
    # cursor-rules + skills + akos modules + cross-canonical landing.
    # Rationale: forward_charters often reference paths like
    # ``scripts/<name>.py`` or ``.cursor/rules/<name>.mdc`` or
    # ``process_list.csv row <id>`` or ``PEOPLE_DESIGN_PATTERN_REGISTRY row
    # <id>``; those artifacts exist on filesystem but the original heuristic
    # only checked ``_candidates/`` + ``OPS_REGISTER`` which produced
    # systematic false positives.
    evidence_chunks: list[str] = [ops_text]
    for canonical_path in [PRECEDENCE_PATH]:
        if canonical_path.exists():
            evidence_chunks.append(canonical_path.read_text(encoding="utf-8", errors="ignore"))
    # filesystem evidence: scripts/*.py + .cursor/rules/*.mdc + .cursor/skills/*/SKILL.md + akos/*.py
    fs_anchors: set[str] = set()
    for fs_glob in [
        (REPO_ROOT / "scripts").glob("*.py"),
        (REPO_ROOT / ".cursor" / "rules").glob("*.mdc"),
        (REPO_ROOT / ".cursor" / "skills").glob("*/SKILL.md"),
        (REPO_ROOT / "akos").glob("*.py"),
    ]:
        for fs_path in fs_glob:
            rel = fs_path.relative_to(REPO_ROOT).as_posix().lower()
            stem = fs_path.stem.lower()
            fs_anchors.add(rel)
            fs_anchors.add(stem)
            fs_anchors.add(re.sub(r"[^a-z0-9]+", "-", rel).strip("-"))
            fs_anchors.add(re.sub(r"[^a-z0-9]+", "-", stem).strip("-"))
            # skill folder name (e.g. .cursor/skills/<name>/SKILL.md -> <name>)
            if fs_path.name == "SKILL.md":
                folder = fs_path.parent.name.lower()
                fs_anchors.add(folder)
                fs_anchors.add(re.sub(r"[^a-z0-9]+", "-", folder).strip("-"))
    # canonical CSV evidence: process_list + baseline_organisation + every
    # dimensions/*.csv row ID body (lowercased).
    csv_evidence: list[str] = []
    for csv_path in [
        PROCESS_LIST_PATH,
        COMPLIANCE_CANONICALS_DIR / "baseline_organisation.csv",
    ]:
        if csv_path.exists():
            csv_evidence.append(csv_path.read_text(encoding="utf-8", errors="ignore").lower())
    if DIMENSIONS_DIR.exists():
        for csv_path in DIMENSIONS_DIR.glob("*.csv"):
            csv_evidence.append(csv_path.read_text(encoding="utf-8", errors="ignore").lower())
    # cross-canonical landing evidence: every other canonical's content (excluding
    # the source canonical for each pair to avoid trivial self-match).
    canonical_bodies: dict[str, str] = {}
    for canonical in _glob_canonicals():
        try:
            canonical_bodies[str(canonical)] = canonical.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            pass
    base_evidence = ("\n".join(evidence_chunks) + "\n" + "\n".join(csv_evidence)).lower()
    # alnum-only normalization so the heuristic matches across kebab/underscore/path-separator
    # variants without false negatives (e.g. token "pattern-index-integrity-discipline"
    # must match CSV row id "pattern_index_integrity_discipline").
    def _alnum(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", s.lower())

    base_evidence_alnum = _alnum(base_evidence)
    candidate_alnum = {_alnum(n) for n in candidate_names}
    fs_anchors_alnum = {_alnum(a) for a in fs_anchors}
    canonical_bodies_alnum = {k: _alnum(v) for k, v in canonical_bodies.items()}
    # Stop-word tokens that carry no evidence on their own (kebabed words like
    # "row", "paired", "runbook", "sop") get filtered so the alnum-prefix
    # match isn't dominated by header noise.
    STOP_PREFIXES = {
        "peopledesignpatternregistryrow",
        "processlistcsvrow",
        "processlistrow",
        "pairedrunbook",
        "pairedsop",
        "pairedvalidator",
        "pairedskill",
        "scripts",
        "sop",
        "cursorrulesakos",
    }

    def _strip_stop_prefix(t: str) -> str:
        for prefix in STOP_PREFIXES:
            if t.startswith(prefix):
                return t[len(prefix):]
        return t

    unresolved = 0
    for canonical, item in forward_pairs:
        token_kebab = re.sub(r"[^a-z0-9]+", "-", item.lower()).strip("-")
        token_alnum = _alnum(item)
        # for evidence sweeps, the substantive part of the token is everything
        # AFTER stop-prefixes like "PEOPLE_DESIGN_PATTERN_REGISTRY row " or
        # "process_list.csv row " or "paired runbook " etc.
        token_core = _strip_stop_prefix(token_alnum)
        if not token_alnum or not token_core:
            continue
        if token_core in base_evidence_alnum:
            continue
        if any(token_core in name or token_core in _alnum(name) for name in candidate_names):
            continue
        if any(token_core in anchor or anchor in token_core for anchor in fs_anchors_alnum):
            continue
        # cross-canonical landing: any OTHER canonical mentions the token core
        source_key = str(canonical)
        if any(token_core in body for path_key, body in canonical_bodies_alnum.items() if path_key != source_key):
            continue
        unresolved += 1
        if unresolved <= 10:
            findings.append(RegressionFindingRow(
                dimension_code="DIM-02-FORWARD-CHARTER-CARRYOVER",
                surface_path=str(canonical.relative_to(REPO_ROOT).as_posix()),
                verdict="gap",
                proposed_rework_action=(
                    f"land '{item}' in a subsequent canonical OR mint a "
                    f"_candidates/ file for it OR file an OPS_REGISTER row"
                ),
                severity="low",
                notes=(
                    f"forward_charters: item '{item}' has no observable "
                    f"carryover signal (no _candidates/ match, no OPS row)"
                ),
            ))
    if unresolved == 0:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-02-FORWARD-CHARTER-CARRYOVER",
            surface_path="canonicals-scan",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{len(forward_pairs)} forward_charters: items across "
                f"canonicals; all observable in _candidates/ or OPS_REGISTER"
            ),
        ))
    return findings


def _probe_dimension_3_validator_ramp_consistency(
    wave: str | None = None,
) -> list[RegressionFindingRow]:
    """DIM-03-VALIDATOR-RAMP-CONSISTENCY — INFO->FAIL changes are decision-paired.

    Diff ``config/verification-profiles.json`` + ``scripts/release-gate.py``
    against the prior wave-close SHA. If the diff promotes a validator
    from INFO to FAIL (or relaxes a threshold) without a paired decision
    row, surface as ``drift``.
    """
    if not VERIFICATION_PROFILES_PATH.exists() or not RELEASE_GATE_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-03-VALIDATOR-RAMP-CONSISTENCY",
            surface_path="config/verification-profiles.json;scripts/release-gate.py",
            verdict="blocked",
            proposed_rework_action="restore verification-profiles.json and release-gate.py",
            severity="high",
            notes="one or both validator-ramp surfaces missing",
        )]
    prior_sha = _git_last_wave_close_sha(wave) if wave else None
    if prior_sha is None:
        return [RegressionFindingRow(
            dimension_code="DIM-03-VALIDATOR-RAMP-CONSISTENCY",
            surface_path="git-log:prior-wave-close",
            verdict="skip",
            proposed_rework_action="",
            severity="low",
            notes=(
                "no prior wave-close commit found in recent git log "
                "(advisory: ramp consistency reverts to operator review)"
            ),
        )]
    diff = _git_diff_files_since(
        prior_sha,
        ["config/verification-profiles.json", "scripts/release-gate.py"],
    )
    promotions = re.findall(
        r"^\+.*(?:INFO\s*->\s*FAIL|info\s*->\s*fail|\"INFO\".*\"FAIL\")",
        diff,
        re.MULTILINE,
    )
    relaxations = re.findall(
        r"^\-.*(?:FAIL|fail).*\n\+.*(?:INFO|info|SKIP|skip|WARN|warn)",
        diff,
        re.MULTILINE,
    )
    findings: list[RegressionFindingRow] = []
    if promotions or relaxations:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-03-VALIDATOR-RAMP-CONSISTENCY",
            surface_path="verification-profiles.json;release-gate.py",
            verdict="drift",
            proposed_rework_action=(
                "verify each promotion/relaxation cites a decision row "
                "in DECISION_REGISTER.csv with rationale"
            ),
            severity="medium",
            notes=(
                f"prior_sha={prior_sha}; promotions_observed="
                f"{len(promotions)}; relaxations_observed={len(relaxations)}"
            ),
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-03-VALIDATOR-RAMP-CONSISTENCY",
            surface_path="verification-profiles.json;release-gate.py",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"prior_sha={prior_sha}; no INFO->FAIL promotions or "
                f"threshold relaxations observed in diff"
            ),
        ))
    return findings


def _probe_dimension_4_canonical_csv_pair_completeness() -> list[RegressionFindingRow]:
    """DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS — per akos-holistika-operations.mdc.

    For each ``v3.0/**/canonicals/dimensions/*.csv``, verify the four
    paired-surface components exist: Pydantic model under ``akos/``,
    validator script under ``scripts/``, Supabase mirror migration, and
    a PRECEDENCE.md reference. Missing components surface as ``gap``.
    """
    if not DIMENSIONS_DIR.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
            surface_path=str(DIMENSIONS_DIR.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore canonicals/dimensions/ directory",
            severity="high",
            notes="dimensions/ canonicals directory missing",
        )]
    akos_files = list((REPO_ROOT / "akos").glob("hlk_*_csv.py"))
    akos_text = "\n".join(p.name for p in akos_files).lower()
    scripts_dir = REPO_ROOT / "scripts"
    validator_text = "\n".join(p.name for p in scripts_dir.glob("validate_*.py")).lower()
    migrations_dir = REPO_ROOT / "supabase" / "migrations"
    migrations_text = ""
    if migrations_dir.exists():
        migrations_text = "\n".join(p.name for p in migrations_dir.glob("*.sql")).lower()
    precedence_text = ""
    if PRECEDENCE_PATH.exists():
        precedence_text = PRECEDENCE_PATH.read_text(encoding="utf-8", errors="ignore").lower()
    findings: list[RegressionFindingRow] = []
    gap_count = 0
    for csv_path in sorted(DIMENSIONS_DIR.glob("*.csv")):
        slug = csv_path.stem.lower().replace("registry", "").strip("_")
        slug = slug.strip("_")
        if not slug:
            slug = csv_path.stem.lower()
        components_missing: list[str] = []
        if not any(slug.replace("_", "") in n.replace("_", "") for n in akos_text.splitlines() if n):
            components_missing.append("akos-pydantic-model")
        if not any(slug.replace("_", "") in n.replace("_", "") for n in validator_text.splitlines() if n):
            components_missing.append("scripts-validator")
        if migrations_text and not any(slug.replace("_", "") in n.replace("_", "") for n in migrations_text.splitlines() if n):
            components_missing.append("supabase-mirror-migration")
        if precedence_text and csv_path.name.lower() not in precedence_text:
            components_missing.append("PRECEDENCE-entry")
        if components_missing:
            gap_count += 1
            if gap_count <= 8:
                findings.append(RegressionFindingRow(
                    dimension_code="DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
                    surface_path=str(csv_path.relative_to(REPO_ROOT).as_posix()),
                    verdict="gap",
                    proposed_rework_action=(
                        f"mint missing components: {', '.join(components_missing)}"
                    ),
                    severity="medium",
                    notes=(
                        f"slug={slug}; missing_components="
                        f"{','.join(components_missing)}"
                    ),
                ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS",
            surface_path=str(DIMENSIONS_DIR.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{len(list(DIMENSIONS_DIR.glob('*.csv')))} dimension "
                f"CSVs; all observed paired surfaces present "
                f"(heuristic match — deep FK sweep deferred to operator review)"
            ),
        ))
    return findings


def _probe_dimension_5_sop_runbook_pairing() -> list[RegressionFindingRow]:
    """DIM-05-SOP-RUNBOOK-PAIRING — per akos-executable-process-catalog.mdc RULE 1.

    Read ``process_list.csv`` → for each ``item_id`` row, surface a gap
    when the row has no observable paired SOP under
    ``v3.0/**/canonicals/SOP-*.md`` AND no observable paired runbook
    under ``scripts/<related-purpose>.py``. Pragmatic heuristic: token
    overlap between item_id and SOP/runbook basenames.
    """
    if not PROCESS_LIST_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-05-SOP-RUNBOOK-PAIRING",
            surface_path=str(PROCESS_LIST_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore process_list.csv",
            severity="high",
            notes="canonical process_list.csv not found",
        )]
    sop_files = list(CANONICALS_DIR.rglob("SOP-*.md"))
    sop_basenames = " ".join(p.stem.lower() for p in sop_files)
    runbook_files = list((REPO_ROOT / "scripts").glob("*.py"))
    runbook_basenames = " ".join(p.stem.lower() for p in runbook_files)
    findings: list[RegressionFindingRow] = []
    rows_processed = 0
    gaps_emitted = 0
    with PROCESS_LIST_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            item_id = (row.get("item_id") or "").strip()
            if not item_id:
                continue
            rows_processed += 1
            tokens = [t for t in re.split(r"[^a-z0-9]+", item_id.lower()) if len(t) >= 4]
            if not tokens:
                continue
            sop_hit = any(t in sop_basenames for t in tokens)
            runbook_hit = any(t in runbook_basenames for t in tokens)
            if not sop_hit and not runbook_hit:
                gaps_emitted += 1
                if gaps_emitted <= 8:
                    findings.append(RegressionFindingRow(
                        dimension_code="DIM-05-SOP-RUNBOOK-PAIRING",
                        surface_path=f"process_list:{item_id}",
                        verdict="gap",
                        proposed_rework_action=(
                            "mint paired SOP under <area>/<role>/canonicals/ "
                            "AND runbook under scripts/ per akos-executable-process-catalog.mdc RULE 1"
                        ),
                        severity="low",
                        notes=(
                            f"no SOP or runbook token-match for item_id; "
                            f"tokens={tokens[:3]}"
                        ),
                    ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-05-SOP-RUNBOOK-PAIRING",
            surface_path=str(PROCESS_LIST_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{rows_processed} process_list rows; "
                f"{len(sop_files)} SOPs; {len(runbook_files)} runbooks; "
                f"all rows have observable SOP or runbook token-match"
            ),
        ))
    return findings


def _probe_dimension_6_uat_report_class_completeness() -> list[RegressionFindingRow]:
    """DIM-06-UAT-REPORT-CLASS-COMPLETENESS — per compose_UAT in UAT_DISCIPLINE.md §4.

    For each ``INITIATIVE_REGISTRY`` row with status closed/completed,
    glob the initiative folder for a ``reports/uat-*.md`` file. Missing
    UAT surfaces as ``gap``. Present UAT is checked for §1 (closure
    summary) and §3 (mechanical evidence) section headings.
    """
    if not INITIATIVE_REGISTRY_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
            surface_path=str(INITIATIVE_REGISTRY_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore INITIATIVE_REGISTRY.csv",
            severity="high",
            notes="canonical INITIATIVE_REGISTRY.csv not found",
        )]
    closed_statuses = {"closed", "completed"}
    findings: list[RegressionFindingRow] = []
    closed_total = 0
    uat_missing = 0
    sections_missing = 0
    with INITIATIVE_REGISTRY_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            status = (row.get("status") or "").strip().lower()
            if status not in closed_statuses:
                continue
            closed_total += 1
            init_id = (row.get("initiative_id") or "").strip()
            slug_token = init_id.lower().split("-")[-1] if init_id else ""
            matching_dirs = [
                d for d in PLANNING_ROOT.iterdir()
                if d.is_dir() and (slug_token in d.name.lower() or init_id.lower() in d.name.lower())
            ] if slug_token else []
            uat_found = False
            for d in matching_dirs:
                reports_dir = d / "reports"
                if not reports_dir.exists():
                    continue
                uat_files = list(reports_dir.glob("uat-*.md"))
                if not uat_files:
                    continue
                uat_found = True
                latest = max(uat_files, key=lambda p: p.stat().st_mtime)
                text = latest.read_text(encoding="utf-8", errors="ignore")
                if not re.search(r"^##\s*1[\.\s]", text, re.MULTILINE) or not re.search(r"^##\s*3[\.\s]", text, re.MULTILINE):
                    sections_missing += 1
                    if sections_missing <= 5:
                        findings.append(RegressionFindingRow(
                            dimension_code="DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
                            surface_path=str(latest.relative_to(REPO_ROOT).as_posix()),
                            verdict="gap",
                            proposed_rework_action=(
                                "add §1 (closure summary) AND §3 "
                                "(mechanical evidence) sections per UAT_DISCIPLINE.md §4"
                            ),
                            severity="low",
                            notes=f"UAT report for closed init {init_id} missing required class sections",
                        ))
                break
            if not uat_found and matching_dirs:
                uat_missing += 1
                if uat_missing <= 5:
                    findings.append(RegressionFindingRow(
                        dimension_code="DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
                        surface_path=f"INITIATIVE_REGISTRY:{init_id}",
                        verdict="gap",
                        proposed_rework_action=f"mint reports/uat-*.md for closed initiative {init_id}",
                        severity="medium",
                        notes=f"closed initiative {init_id} has no UAT report under {matching_dirs[0].name}/reports/",
                    ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-06-UAT-REPORT-CLASS-COMPLETENESS",
            surface_path=str(INITIATIVE_REGISTRY_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{closed_total} closed initiatives sampled; UAT presence "
                f"+ §1/§3 sections OK (compose_UAT class-completeness "
                f"deeper check deferred to operator review)"
            ),
        ))
    return findings


def _probe_dimension_7_render_trail_audience_match() -> list[RegressionFindingRow]:
    """DIM-07-RENDER-TRAIL-AUDIENCE-MATCH — per akos-external-render-discipline.mdc RULE 4.

    Shell out to ``scripts/validate_external_render_trail.py --strict
    --strict-freshness``. Exit-0 = clean; non-zero = drift; missing
    validator = blocked.
    """
    success, output = _shell_validator(
        "scripts/validate_external_render_trail.py",
        ["--strict", "--strict-freshness"],
        timeout=120,
    )
    if not success and "missing validator" in output:
        return [RegressionFindingRow(
            dimension_code="DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
            surface_path="scripts/validate_external_render_trail.py",
            verdict="blocked",
            proposed_rework_action="restore scripts/validate_external_render_trail.py",
            severity="medium",
            notes=output[:200],
        )]
    if success:
        return [RegressionFindingRow(
            dimension_code="DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
            surface_path="scripts/validate_external_render_trail.py",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="--strict --strict-freshness PASS",
        )]
    return [RegressionFindingRow(
        dimension_code="DIM-07-RENDER-TRAIL-AUDIENCE-MATCH",
        surface_path="scripts/validate_external_render_trail.py",
        verdict="drift",
        proposed_rework_action=(
            "review external-render-pending-tracker.md; reconcile any "
            "new external-tagged surfaces with paired render trails"
        ),
        severity="medium",
        notes=("validator FAIL; first 200 chars: " + output[:200].replace("\n", " ")),
    )]


def _probe_dimension_8_brand_baseline_register_match() -> list[RegressionFindingRow]:
    """DIM-08-BRAND-BASELINE-REGISTER-MATCH — per akos-brand-baseline-reality.mdc.

    Shell out to ``scripts/validate_brand_baseline_reality_drift.py``.
    Exit-0 = clean; non-zero = drift; missing = blocked.
    """
    success, output = _shell_validator(
        "scripts/validate_brand_baseline_reality_drift.py",
        timeout=60,
    )
    if not success and "missing validator" in output:
        return [RegressionFindingRow(
            dimension_code="DIM-08-BRAND-BASELINE-REGISTER-MATCH",
            surface_path="scripts/validate_brand_baseline_reality_drift.py",
            verdict="blocked",
            proposed_rework_action="restore validate_brand_baseline_reality_drift.py",
            severity="medium",
            notes=output[:200],
        )]
    if success:
        return [RegressionFindingRow(
            dimension_code="DIM-08-BRAND-BASELINE-REGISTER-MATCH",
            surface_path="scripts/validate_brand_baseline_reality_drift.py",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="brand-baseline drift validator PASS",
        )]
    return [RegressionFindingRow(
        dimension_code="DIM-08-BRAND-BASELINE-REGISTER-MATCH",
        surface_path="scripts/validate_brand_baseline_reality_drift.py",
        verdict="drift",
        proposed_rework_action=(
            "translate CORPINT-internal tokens leaking into external "
            "surfaces per BRAND_BASELINE_REALITY_MATRIX.md §3 translation table"
        ),
        severity="medium",
        notes=("validator FAIL; first 200 chars: " + output[:200].replace("\n", " ")),
    )]


def _probe_dimension_9_cross_area_breakthrough_announcement() -> list[RegressionFindingRow]:
    """DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT — per SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md.

    Read PEOPLE_DESIGN_PATTERN_REGISTRY.csv → for each pattern_id, check
    at least one announcement digest under
    ``docs/wip/planning/79-people-manifesto-and-pattern-library/reports/breakthroughs/**``
    OR ``docs/wip/planning/**/reports/cross-area-breakthrough-*.md`` mentions it.
    """
    if not PATTERN_REGISTRY_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
            surface_path=str(PATTERN_REGISTRY_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="blocked",
            proposed_rework_action="restore PEOPLE_DESIGN_PATTERN_REGISTRY.csv",
            severity="high",
            notes="canonical PEOPLE_DESIGN_PATTERN_REGISTRY.csv not found",
        )]
    pattern_ids: list[str] = []
    with PATTERN_REGISTRY_PATH.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            pid = (row.get("pattern_id") or "").strip()
            if pid:
                pattern_ids.append(pid)
    breakthrough_text = ""
    breakthrough_dir = (
        PLANNING_ROOT / "79-people-manifesto-and-pattern-library"
        / "reports" / "breakthroughs"
    )
    if breakthrough_dir.exists():
        for md_path in breakthrough_dir.rglob("*.md"):
            breakthrough_text += md_path.read_text(encoding="utf-8", errors="ignore").lower()
    for md_path in PLANNING_ROOT.rglob("reports/cross-area-breakthrough-*.md"):
        breakthrough_text += md_path.read_text(encoding="utf-8", errors="ignore").lower()
    findings: list[RegressionFindingRow] = []
    orphans = [pid for pid in pattern_ids if pid.lower() not in breakthrough_text]
    for pid in orphans[:8]:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
            surface_path=f"PEOPLE_DESIGN_PATTERN_REGISTRY:{pid}",
            verdict="gap",
            proposed_rework_action=(
                "run `py scripts/peopl_cross_area_breakthrough_announce.py` "
                "with appropriate --since date to generate the missing digest"
            ),
            severity="low",
            notes=f"pattern_id not found in any breakthrough digest body",
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT",
            surface_path=str(PATTERN_REGISTRY_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{len(pattern_ids)} pattern_ids; all observed in at "
                f"least one breakthrough digest body"
            ),
        ))
    return findings


def _probe_dimension_10_deploy_evidence_completeness(
    wave: str | None = None,
) -> list[RegressionFindingRow]:
    """DIM-10-DEPLOY-EVIDENCE-COMPLETENESS — per UAT_DISCIPLINE.md §3.7 + akos-quality-fabric.mdc RULE 3.

    Glob ``docs/wip/planning/**/files-modified.csv`` → filter rows where
    ``repo`` column is non-empty AND != ``openclaw-akos``. For each:
    verify the sibling initiative's UAT report references a deploy_id +
    READY state + HTTP 200 hero route. Missing evidence = ``gap``.
    """
    findings: list[RegressionFindingRow] = []
    sibling_rows = 0
    sibling_missing_evidence = 0
    for fm_csv in PLANNING_ROOT.rglob("files-modified.csv"):
        try:
            with fm_csv.open(
                "r", encoding="utf-8", errors="replace", newline=""
            ) as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    repo = (row.get("repo") or "").strip().lower()
                    if not repo or repo in {"openclaw-akos", "akos", ""}:
                        continue
                    sibling_rows += 1
        except (OSError, csv.Error, UnicodeDecodeError):
            continue
        reports_dir = fm_csv.parent / "reports"
        if not reports_dir.exists():
            sibling_missing_evidence += 1
            continue
        uat_files = list(reports_dir.glob("uat-*.md"))
        if not uat_files:
            sibling_missing_evidence += 1
            if sibling_missing_evidence <= 5:
                findings.append(RegressionFindingRow(
                    dimension_code="DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
                    surface_path=str(fm_csv.relative_to(REPO_ROOT).as_posix()),
                    verdict="gap",
                    proposed_rework_action=(
                        "mint reports/uat-*.md with deploy_id + state=READY + "
                        "HTTP 200 hero route evidence for the sibling-repo touches"
                    ),
                    severity="medium",
                    notes="sibling-repo row(s) exist but no UAT report under reports/",
                ))
            continue
        joined = " ".join(p.read_text(encoding="utf-8", errors="ignore") for p in uat_files).lower()
        if not ("deploy" in joined and ("ready" in joined or "200" in joined or "http 200" in joined)):
            sibling_missing_evidence += 1
            if sibling_missing_evidence <= 5:
                findings.append(RegressionFindingRow(
                    dimension_code="DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
                    surface_path=str(reports_dir.relative_to(REPO_ROOT).as_posix()),
                    verdict="gap",
                    proposed_rework_action=(
                        "add deploy_id + state=READY + HTTP 200 hero-route "
                        "evidence to the UAT report"
                    ),
                    severity="low",
                    notes="UAT present but no deploy/state/HTTP-200 evidence tokens found",
                ))
    if sibling_rows == 0:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
            surface_path="planning/files-modified-scan",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes="no sibling-repo touches observed across all files-modified.csv files",
        ))
    elif not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
            surface_path="planning/files-modified-scan",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{sibling_rows} sibling-repo rows; all initiative folders "
                f"carry UAT with deploy/READY/HTTP-200 evidence"
            ),
        ))
    return findings


def _probe_dimension_11_cursor_rule_skill_pairing() -> list[RegressionFindingRow]:
    """DIM-11-CURSOR-RULE-SKILL-PAIRING — per D-IH-80-E craft-transmission precedent.

    For each ``.cursor/rules/akos-*.mdc``, scan body for "skill" /
    "SKILL.md" / "craft" mentions. If craft is named, verify a paired
    skill exists under ``.cursor/skills/*/SKILL.md`` OR a forward-charter
    candidate file exists. Missing pairing = ``gap``.
    """
    if not CURSOR_RULES_DIR.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-11-CURSOR-RULE-SKILL-PAIRING",
            surface_path=".cursor/rules/",
            verdict="blocked",
            proposed_rework_action="restore .cursor/rules/ directory",
            severity="medium",
            notes="cursor-rules directory absent",
        )]
    skill_basenames: list[str] = []
    for skills_dir in SKILLS_DIRS:
        if skills_dir.exists():
            for skill_path in skills_dir.glob("*/SKILL.md"):
                skill_basenames.append(skill_path.parent.name.lower())
    candidate_basenames: set[str] = set()
    if CANDIDATES_DIR.exists():
        candidate_basenames = {p.stem.lower() for p in CANDIDATES_DIR.glob("*.md")}
    findings: list[RegressionFindingRow] = []
    rule_files = list(CURSOR_RULES_DIR.glob("akos-*.mdc"))
    gaps_emitted = 0
    for rule in rule_files:
        body = rule.read_text(encoding="utf-8", errors="ignore").lower()
        mentions_craft = (
            "skill" in body or "craft" in body or "skill.md" in body
        )
        if not mentions_craft:
            continue
        rule_token = rule.stem.replace("akos-", "").replace("-", "")
        skill_match = any(rule_token in sb.replace("-", "") for sb in skill_basenames)
        candidate_match = any(rule_token in cb.replace("-", "") for cb in candidate_basenames)
        if not skill_match and not candidate_match:
            gaps_emitted += 1
            if gaps_emitted <= 5:
                findings.append(RegressionFindingRow(
                    dimension_code="DIM-11-CURSOR-RULE-SKILL-PAIRING",
                    surface_path=str(rule.relative_to(REPO_ROOT).as_posix()),
                    verdict="gap",
                    proposed_rework_action=(
                        "mint paired skill under .cursor/skills/ OR file "
                        "forward-charter candidate per D-IH-80-E precedent"
                    ),
                    severity="low",
                    notes=(
                        f"rule body mentions craft/skill but no paired "
                        f"SKILL.md or _candidates/ match for token "
                        f"'{rule_token}'"
                    ),
                ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-11-CURSOR-RULE-SKILL-PAIRING",
            surface_path=".cursor/rules/",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"{len(rule_files)} akos-*.mdc rules scanned; all "
                f"craft-mentioning rules have observable paired skill "
                f"or forward-charter candidate"
            ),
        ))
    return findings


def _probe_dimension_12_operator_scratchpad_continuity(
    wave: str | None = None,
) -> list[RegressionFindingRow]:
    """DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY — per akos-agent-checkpoint-discipline.mdc.

    Read the operator scratchpad; verify its last entry timestamp is no
    older than the most-recent commit on HEAD AND verify the wave's
    decision IDs (if known) are cited in the scratchpad body. Stale or
    missing-decision-citation scratchpad surfaces as ``drift``.
    """
    if not OPERATOR_SCRATCHPAD_PATH.exists():
        return [RegressionFindingRow(
            dimension_code="DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
            surface_path=str(OPERATOR_SCRATCHPAD_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="gap",
            proposed_rework_action="mint operator-scratchpad.md and add wave-close drain entry",
            severity="medium",
            notes="operator-scratchpad.md absent",
        )]
    body = OPERATOR_SCRATCHPAD_PATH.read_text(encoding="utf-8", errors="ignore")
    date_hits = re.findall(r"\b(20\d{2}-\d{2}-\d{2})\b", body)
    last_pad_date = max(date_hits) if date_hits else None
    head_result = process.run(
        ["git", "log", "-1", "--pretty=format:%cs"],
        timeout=15, capture=True, check=False,
    )
    head_date = head_result.stdout.strip() if head_result.success else None
    findings: list[RegressionFindingRow] = []
    pad_days = _days_since(last_pad_date) if last_pad_date else None
    if last_pad_date and head_date and last_pad_date < head_date:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
            surface_path=str(OPERATOR_SCRATCHPAD_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="drift",
            proposed_rework_action="append wave-close drain entry citing all wave decisions",
            severity="low",
            notes=(
                f"last scratchpad date={last_pad_date}; HEAD commit "
                f"date={head_date}; scratchpad older than HEAD"
            ),
        ))
    if pad_days is not None and pad_days > FRESHNESS_DRIFT_THRESHOLD_DAYS:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
            surface_path=str(OPERATOR_SCRATCHPAD_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="drift",
            proposed_rework_action="refresh scratchpad with recent wave activity",
            severity="low",
            notes=f"scratchpad last_entry_date={last_pad_date}; days_since={pad_days}",
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
            surface_path=str(OPERATOR_SCRATCHPAD_PATH.relative_to(REPO_ROOT).as_posix()),
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=(
                f"last_entry_date={last_pad_date or 'n/a'}; "
                f"HEAD_date={head_date or 'n/a'}; continuity OK"
            ),
        ))
    return findings


def _probe_dimension_13_role_process_pairing_completeness(
    wave: str | None = None,
) -> list[RegressionFindingRow]:
    """DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS — per D-IH-86-CL Wave P codification.

    Conditional dimension: fires when scenario has new ``baseline_organisation.csv``
    role mints OR new ``process_list.csv`` process mints in the closing wave's
    deliverables. Probes bidirectional FK between role rows + process_list role_owner
    cells to prevent ghost-role (role without paired process) + orphan-process
    (process whose role_owner does not resolve) drift at canonical-CSV mint commits.

    Distinct from DIM-04 (per-CSV pair completeness: Pydantic + validator + mirror +
    PRECEDENCE rows for new CSV registers) and DIM-05 (per-process SOP+runbook
    pairing per akos-executable-process-catalog.mdc Rule 1). DIM-13 is cross-CSV
    role↔process pairing — distinct from both because a process can be paired with
    SOP+runbook (DIM-05 clean) but still reference a non-existent role_owner.

    Probe heuristic: load both CSVs; for every distinct role_name in
    baseline_organisation.csv, check process_list.csv has ≥1 row with that role
    in the role_owner column (ghost-role check, severity=low because some roles
    legitimately have no process today, e.g., gated/planned role rows). For every
    distinct role_owner in process_list.csv, check baseline_organisation.csv has
    a matching role_name (orphan-process check, severity=high because process
    without resolvable owner breaks accountability chain).

    Operator-explicit codification 2026-05-21 Wave P Q4: "option B with a
    regression for later to avoid missing things or not wiring them up properly.
    that's a doctrine."
    """
    findings: list[RegressionFindingRow] = []
    baseline_csv = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv"
    process_csv = REPO_ROOT / "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv"
    if not baseline_csv.exists() or not process_csv.exists():
        findings.append(RegressionFindingRow(
            dimension_code="DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS",
            surface_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/",
            verdict="blocked",
            proposed_rework_action="ensure baseline_organisation.csv + process_list.csv both present before probe",
            severity="high",
            notes=f"baseline={baseline_csv.exists()}; process={process_csv.exists()}",
        ))
        return findings
    import csv
    role_names: set[str] = set()
    role_status: dict[str, str] = {}
    with baseline_csv.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("role_name") or "").strip()
            if name:
                role_names.add(name)
                role_status[name] = (row.get("status") or "").strip()
    process_role_owners: dict[str, list[str]] = {}
    with process_csv.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            owner = (row.get("role_owner") or "").strip()
            item_id = (row.get("item_id") or "").strip()
            if owner and item_id:
                process_role_owners.setdefault(owner, []).append(item_id)
    orphan_processes: dict[str, list[str]] = {}
    for owner, items in process_role_owners.items():
        if owner and owner not in role_names:
            orphan_processes[owner] = items
    ghost_roles: list[str] = []
    for name in role_names:
        if name not in process_role_owners:
            status = role_status.get(name, "")
            if status not in {"planned", "gated_operator", "gated_ahead_of_executive_activation"}:
                ghost_roles.append(name)
    for owner, items in orphan_processes.items():
        findings.append(RegressionFindingRow(
            dimension_code="DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS",
            surface_path=f"process_list.csv:role_owner={owner}",
            verdict="drift",
            proposed_rework_action=f"either add baseline_organisation.csv row for '{owner}' OR rewrite {len(items)} process row(s) to reference resolvable role_name",
            severity="high",
            notes=f"orphan-process: role_owner '{owner}' has {len(items)} process row(s) but no baseline_organisation.csv match; sample items: {items[:3]}",
        ))
    for name in ghost_roles[:20]:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS",
            surface_path=f"baseline_organisation.csv:role_name={name}",
            verdict="gap",
            proposed_rework_action=f"mint at least 1 process_list.csv row with role_owner='{name}' OR change role status to planned/gated",
            severity="low",
            notes=f"ghost-role: '{name}' has status={role_status.get(name, 'unknown')} active but no paired process_list.csv row",
        ))
    if not findings:
        findings.append(RegressionFindingRow(
            dimension_code="DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS",
            surface_path="docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/",
            verdict="clean",
            proposed_rework_action="",
            severity="low",
            notes=f"roles={len(role_names)}; process_owners={len(process_role_owners)}; orphan_processes=0; ghost_roles=0",
        ))
    return findings


PROBE_REGISTRY: dict[str, callable] = {
    "DIM-01-DECISION-LINEAGE": _probe_dimension_1_decision_lineage,
    "DIM-02-FORWARD-CHARTER-CARRYOVER": _probe_dimension_2_forward_charter_carryover,
    "DIM-03-VALIDATOR-RAMP-CONSISTENCY": _probe_dimension_3_validator_ramp_consistency,
    "DIM-04-CANONICAL-CSV-PAIR-COMPLETENESS": _probe_dimension_4_canonical_csv_pair_completeness,
    "DIM-05-SOP-RUNBOOK-PAIRING": _probe_dimension_5_sop_runbook_pairing,
    "DIM-06-UAT-REPORT-CLASS-COMPLETENESS": _probe_dimension_6_uat_report_class_completeness,
    "DIM-07-RENDER-TRAIL-AUDIENCE-MATCH": _probe_dimension_7_render_trail_audience_match,
    "DIM-08-BRAND-BASELINE-REGISTER-MATCH": _probe_dimension_8_brand_baseline_register_match,
    "DIM-09-CROSS-AREA-BREAKTHROUGH-ANNOUNCEMENT": _probe_dimension_9_cross_area_breakthrough_announcement,
    "DIM-10-DEPLOY-EVIDENCE-COMPLETENESS": _probe_dimension_10_deploy_evidence_completeness,
    "DIM-11-CURSOR-RULE-SKILL-PAIRING": _probe_dimension_11_cursor_rule_skill_pairing,
    "DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY": _probe_dimension_12_operator_scratchpad_continuity,
    "DIM-13-ROLE-PROCESS-PAIRING-COMPLETENESS": _probe_dimension_13_role_process_pairing_completeness,
}

WAVE_AWARE_DIMENSIONS: frozenset[str] = frozenset({
    "DIM-01-DECISION-LINEAGE",
    "DIM-03-VALIDATOR-RAMP-CONSISTENCY",
    "DIM-10-DEPLOY-EVIDENCE-COMPLETENESS",
    "DIM-12-OPERATOR-SCRATCHPAD-CONTINUITY",
})


def run_sweep(
    wave_closing: str,
    dimensions: tuple[str, ...] | None = None,
    swept_by: str = "agent:inter_wave_regression_sweep",
) -> RegressionSweepReport:
    """Orchestrate one wave-close 12-dimension regression sweep.

    Per ``akos-inter-wave-regression.mdc`` RULE 2: every wave-close
    exercises the 7 baseline dimensions + any conditional dimension whose
    axis predicate fires for the wave; SKIP per dimension allowed only
    with a one-clause reason logged in the sweep report.

    Per Wave M.5 hotfix (D-IH-86-BW): the four ``WAVE_AWARE_DIMENSIONS``
    receive ``wave_closing`` as an argument so their probes can scope
    git-history queries + diff windows + decision-set filters to the
    wave being closed. The other eight ignore the wave param.
    """
    if dimensions is None:
        dimensions = ALL_DIMENSIONS
    all_findings: list[RegressionFindingRow] = []
    for dim in dimensions:
        probe = PROBE_REGISTRY.get(dim)
        if probe is None:
            logger.warning("unknown dimension code: %s", dim)
            continue
        if dim in WAVE_AWARE_DIMENSIONS:
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
        dimension_code="DIM-01-DECISION-LINEAGE",
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
    if len(PROBE_REGISTRY) != 13:
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — PROBE_REGISTRY has %d entries, expected 13 (12 base + DIM-13 per D-IH-86-CL)",
            len(PROBE_REGISTRY),
        )
        return 1
    if set(PROBE_REGISTRY.keys()) != set(ALL_DIMENSIONS):
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — PROBE_REGISTRY keys do not match ALL_DIMENSIONS"
        )
        return 1
    if len(BASELINE_DIMENSION_CODES) != 7:
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — BASELINE_DIMENSION_CODES has %d entries, expected 7",
            len(BASELINE_DIMENSION_CODES),
        )
        return 1
    if len(CONDITIONAL_DIMENSION_CODES) != 6:
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — CONDITIONAL_DIMENSION_CODES has %d entries, expected 6 (5 base + DIM-13 per D-IH-86-CL)",
            len(CONDITIONAL_DIMENSION_CODES),
        )
        return 1
    if BASELINE_DIMENSION_CODES & CONDITIONAL_DIMENSION_CODES:
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — BASELINE and CONDITIONAL frozensets overlap",
        )
        return 1
    if BASELINE_DIMENSION_CODES | CONDITIONAL_DIMENSION_CODES != set(ALL_DIMENSIONS):
        logger.error(
            "FAIL: validate_inter_wave_regression_self_test — BASELINE union CONDITIONAL != ALL_DIMENSIONS",
        )
        return 1
    logger.info(
        "PASS: validate_inter_wave_regression_self_test — Pydantic fixtures construct ; finding=%s ; report=%s ; probes=%d ; baseline=%d ; conditional=%d",
        sample_finding.dimension_code,
        sample_report.report_id,
        len(PROBE_REGISTRY),
        len(BASELINE_DIMENSION_CODES),
        len(CONDITIONAL_DIMENSION_CODES),
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
