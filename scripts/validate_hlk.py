#!/usr/bin/env python3
"""HLK canonical vault validator (Initiative 32 P1: dispatcher graph + structured JSON report).

Deterministic checks against baseline_organisation.csv and process_list.csv:
- CSV parseability with Pydantic models
- Referential integrity (role_owner resolves against org baseline)
- Graph integrity (0 broken parent refs, 0 orphans)
- Granularity canon (project/workstream/process/task only)
- No duplicate item_id or org_id
- Unique item_name per item_id (required for parent-id resolution)
- All projects have at least one child

Plus a per-CSV dispatcher graph that delegates to specialised validators
(component_service_matrix, finops, goipoi, adviser, filed_instruments,
program_registry, topic_registry, persona_registry, channel_touchpoint,
sourcing_register, language_frontmatter).

Usage:
    py scripts/validate_hlk.py            # legacy human-readable output, exit 0/1
    py scripts/validate_hlk.py --json     # structured JSON report on stdout, exit 0/1
                                          # (CLI exit code preserved per D-IH-32-F)

The ``--json`` flag is the I32 P1 addition. Default behaviour is unchanged so
every existing caller (CI, agents, operator scripts) keeps working without
modification (R-32-1 mitigation: backward-compatible CLI is non-negotiable).

The structured report emitted by ``--json`` matches the field contract in
``akos.hlk_validation_run.VALIDATION_RUN_FIELDNAMES`` and is consumable by a
future ``compliance.validation_runs`` Postgres mirror writer (P1-A4 ships the
DDL; mirror writes are not part of every developer-local invocation).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.io import REPO_ROOT
from akos.hlk_process_csv import ambiguous_item_names, item_name_uniqueness_errors
from akos.hlk_validation_run import VALID_STATUSES
from akos.models import OrgRole, ProcessItem

HLK_DIR = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
ORG_CSV = HLK_DIR / "baseline_organisation.csv"
PROC_CSV = HLK_DIR / "process_list.csv"

VALID_GRANULARITIES = {"project", "workstream", "process", "task"}
ALIAS_ROLE_OWNERS = {"Process Owner", "TBD"}


def load_org() -> list[dict]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_proc() -> list[dict]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def check_org_parse(rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows, start=2):
        try:
            OrgRole.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as e:
            errors.append(f"org row {i} ({row.get('role_name', '?')}): {e}")
    return errors


def check_proc_parse(rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows, start=2):
        try:
            ProcessItem.model_validate({k: (v or "") for k, v in row.items() if k})
        except Exception as e:
            errors.append(f"proc row {i} ({row.get('item_id', '?')}): {e}")
    return errors


def check_role_owner_integrity(proc_rows: list[dict], org_names: set[str]) -> list[str]:
    errors = []
    for row in proc_rows:
        owner = row.get("role_owner", "").strip()
        if owner and owner not in org_names and owner not in ALIAS_ROLE_OWNERS:
            errors.append(f"{row.get('item_id', '?')}: role_owner '{owner}' not in baseline org")
    return errors


def check_graph_integrity(proc_rows: list[dict]) -> tuple[list[str], list[str]]:
    names = {row["item_name"].strip() for row in proc_rows if row.get("item_name")}
    broken = []
    orphans = []
    for row in proc_rows:
        p1 = row.get("item_parent_1", "").strip()
        gran = row.get("item_granularity", "").strip()
        if p1 and p1 not in names:
            broken.append(f"{row.get('item_id', '?')}: parent '{p1}' not found")
        if not p1 and gran != "project":
            orphans.append(f"{row.get('item_id', '?')}: non-project without parent")
    return broken, orphans


def check_granularity(proc_rows: list[dict]) -> list[str]:
    errors = []
    for row in proc_rows:
        g = row.get("item_granularity", "").strip().lower()
        if g and g not in VALID_GRANULARITIES:
            errors.append(f"{row.get('item_id', '?')}: invalid granularity '{g}'")
    return errors


def check_duplicate_ids(proc_rows: list[dict]) -> list[str]:
    seen: dict[str, int] = {}
    dupes = []
    for row in proc_rows:
        iid = row.get("item_id", "").strip()
        if iid:
            seen[iid] = seen.get(iid, 0) + 1
    for iid, count in seen.items():
        if count > 1:
            dupes.append(f"item_id '{iid}' appears {count} times")
    return dupes


def check_duplicate_org_ids(org_rows: list[dict]) -> list[str]:
    seen: dict[str, int] = {}
    dupes = []
    for row in org_rows:
        oid = row.get("org_id", "").strip()
        if oid:
            seen[oid] = seen.get(oid, 0) + 1
    for oid, count in seen.items():
        if count > 1:
            dupes.append(f"org_id '{oid}' appears {count} times")
    return dupes


def check_parent_id_consistency(proc_rows: list[dict]) -> list[str]:
    """When item_parent_*_id is set, it must resolve to item_name; strict id required for unique parent names."""
    by_id = {(row.get("item_id") or "").strip(): row for row in proc_rows if row.get("item_id")}
    amb = ambiguous_item_names([{k: (v or "") for k, v in r.items()} for r in proc_rows])
    errors: list[str] = []
    for row in proc_rows:
        iid = (row.get("item_id") or "").strip()
        gran = (row.get("item_granularity") or "").strip()
        for num in ("1", "2"):
            pname = (row.get(f"item_parent_{num}") or "").strip()
            pid = (row.get(f"item_parent_{num}_id") or "").strip()
            if pid:
                target = by_id.get(pid)
                if not target:
                    errors.append(f"{iid}: item_parent_{num}_id '{pid}' not found")
                elif (target.get("item_name") or "").strip() != pname:
                    errors.append(
                        f"{iid}: item_parent_{num}_id '{pid}' points to wrong item_name "
                        f"(expected {pname!r}, got {(target.get('item_name') or '').strip()!r})"
                    )
            if gran == "project":
                if pid:
                    errors.append(f"{iid}: project row must not set item_parent_{num}_id")
                continue
            if pname and pname not in amb and not pid:
                errors.append(f"{iid}: item_parent_{num} set to unique name {pname!r} but item_parent_{num}_id empty")
    return errors


def check_projects_have_children(proc_rows: list[dict]) -> list[str]:
    names = {row["item_name"].strip() for row in proc_rows if row.get("item_name")}
    parents_used = {row["item_parent_1"].strip() for row in proc_rows if row.get("item_parent_1")}
    errors = []
    for row in proc_rows:
        if row.get("item_granularity", "").strip() == "project":
            pname = row.get("item_name", "").strip()
            if pname not in parents_used:
                errors.append(f"project '{pname}' has no children")
    return errors


def _load_design_pattern_ids() -> set[str]:
    """Return the set of valid pattern_id values from PEOPLE_DESIGN_PATTERN_REGISTRY.csv.

    Empty set when the file is missing, which causes any populated
    inherited_pattern_id cell to fail FK resolution (correct fail-closed posture).
    Per I79 P6 D-IH-79-E (process-singularity FK lever).
    """
    pattern_csv = HLK_DIR / "dimensions" / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
    if not pattern_csv.exists():
        return set()
    out: set[str] = set()
    with open(pattern_csv, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            pid = (row.get("pattern_id") or "").strip()
            if pid:
                out.add(pid)
    return out


def check_inherited_pattern_id_fk(proc_rows: list[dict]) -> list[str]:
    """FK resolution for ``inherited_pattern_id`` against PEOPLE_DESIGN_PATTERN_REGISTRY.

    Empty cells are valid (the column is nullable). Populated cells must resolve.
    Per I79 P6 D-IH-79-E (the "process singularity" lever — countable adoption surface).
    """
    valid_ids = _load_design_pattern_ids()
    errors: list[str] = []
    for row in proc_rows:
        ipid = (row.get("inherited_pattern_id") or "").strip()
        if not ipid:
            continue
        if not valid_ids:
            errors.append(
                f"item_id={row.get('item_id', '?')!r} carries inherited_pattern_id="
                f"{ipid!r} but PEOPLE_DESIGN_PATTERN_REGISTRY.csv could not be loaded"
            )
            continue
        if ipid not in valid_ids:
            errors.append(
                f"item_id={row.get('item_id', '?')!r} carries inherited_pattern_id={ipid!r} "
                f"which does not resolve to any pattern_id in PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
            )
    return errors


def _git_sha() -> str:
    """Return short commit SHA, or 'dirty' on any failure (no git, detached, etc.)."""
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=2,
        )
        if r.returncode == 0:
            sha = r.stdout.strip()
            # Detect uncommitted changes; mark with -dirty suffix.
            r2 = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, cwd=REPO_ROOT, timeout=2,
            )
            if r2.returncode == 0 and r2.stdout.strip():
                return f"{sha}-dirty"
            return sha
    except Exception:
        pass
    return "dirty"


def _make_run_row(
    run_id: str,
    validator_name: str,
    started_at_iso: str,
    duration_ms: int,
    status: str,
    exit_code: int,
    row_count: int = 0,
    error_count: int = 0,
    drift_detected: bool = False,
    notes: str = "",
    git_sha_value: str | None = None,
) -> dict:
    """Build one validation_runs row dict matching VALIDATION_RUN_FIELDNAMES."""
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status {status!r}; must be one of {VALID_STATUSES}")
    return {
        "run_id": run_id,
        "validator_name": validator_name,
        "started_at": started_at_iso,
        "duration_ms": duration_ms,
        "status": status,
        "exit_code": exit_code,
        "row_count": row_count,
        "error_count": error_count,
        "drift_detected": drift_detected,
        "git_sha": git_sha_value if git_sha_value is not None else _git_sha(),
        "host": socket.gethostname()[:64],
        "notes": notes,
    }


def _delegate_subprocess(
    name: str, validator_path: Path, run_id: str, run_rows: list[dict], git_sha_value: str
) -> int:
    """Invoke a per-CSV validator script and append a structured row to run_rows.

    Returns the validator exit code so the dispatcher preserves legacy fail-fast.
    Stdout/stderr forwarding matches the legacy behaviour exactly.
    """
    started = time.time()
    started_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started))
    r = subprocess.run([sys.executable, str(validator_path)], capture_output=True, text=True)
    print(r.stdout, end="")
    if r.stderr:
        print(r.stderr, end="", file=sys.stderr)
    duration_ms = int((time.time() - started) * 1000)
    status = "pass" if r.returncode == 0 else "fail"
    run_rows.append(_make_run_row(
        run_id=run_id,
        validator_name=name,
        started_at_iso=started_iso,
        duration_ms=duration_ms,
        status=status,
        exit_code=r.returncode,
        notes="dispatched subprocess",
        git_sha_value=git_sha_value,
    ))
    return r.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="HLK canonical vault validator")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured per-validator JSON report on stdout (I32 P1).",
    )
    args = parser.parse_args()

    # I32 P1: structured collector — populated regardless of --json so the dispatcher
    # contract is uniform. Human-readable output is the default; --json flips stdout
    # to JSON-only (no banner, no per-check lines) so the report is machine-parseable.
    run_id = str(uuid.uuid4())
    git_sha_value = _git_sha()
    dispatch_started_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    run_rows: list[dict] = []

    if not args.json:
        print("\n  HLK Canonical Vault Validator")
        print("  " + "=" * 40)

    org_rows = load_org()
    proc_rows = load_proc()
    org_names = {row["role_name"].strip() for row in org_rows if row.get("role_name")}

    all_errors: list[str] = []
    inline_started = time.time()
    checks = [
        ("Org CSV parse", check_org_parse(org_rows)),
        ("Process CSV parse", check_proc_parse(proc_rows)),
        ("Role owner integrity", check_role_owner_integrity(proc_rows, org_names)),
        ("Granularity canon", check_granularity(proc_rows)),
        ("Duplicate item_id", check_duplicate_ids(proc_rows)),
        ("Duplicate org_id", check_duplicate_org_ids(org_rows)),
        ("Unique item_name", item_name_uniqueness_errors(proc_rows)),
        ("Projects have children", check_projects_have_children(proc_rows)),
    ]

    broken, orphans = check_graph_integrity(proc_rows)
    checks.append(("Broken parent refs", broken))
    checks.append(("Orphan items", orphans))
    checks.append(("Parent id consistency", check_parent_id_consistency(proc_rows)))
    checks.append(("Inherited pattern_id FK", check_inherited_pattern_id_fk(proc_rows)))

    for name, errors in checks:
        status = "PASS" if not errors else "FAIL"
        if not args.json:
            print(f"  {name:30s} {status}")
            if errors:
                for e in errors[:5]:
                    print(f"    - {e}")
                if len(errors) > 5:
                    print(f"    ... and {len(errors) - 5} more")
        if errors:
            all_errors.extend(errors)
        # Emit one row per inline check (slug-cased validator_name).
        run_rows.append(_make_run_row(
            run_id=run_id,
            validator_name="inline_" + name.lower().replace(" ", "_"),
            started_at_iso=dispatch_started_iso,
            duration_ms=0,  # inline checks share one batch; per-check timing is sub-millisecond
            status="pass" if not errors else "fail",
            exit_code=0 if not errors else 1,
            row_count=len(proc_rows) if "Process" in name or "item" in name.lower() else len(org_rows),
            error_count=len(errors),
            notes="inline check (baseline_organisation + process_list)",
            git_sha_value=git_sha_value,
        ))

    inline_duration_ms = int((time.time() - inline_started) * 1000)
    # Annotate the first inline row with the batch duration (so summing duration_ms
    # is informational; per-row duration is 0 for the rest of the batch).
    if run_rows:
        run_rows[0]["duration_ms"] = inline_duration_ms

    if not args.json:
        print()
        print(f"  Org roles:    {len(org_rows)}")
        print(f"  Process items: {len(proc_rows)}")
        print()

    if all_errors:
        if not args.json:
            print(f"  OVERALL: FAIL ({len(all_errors)} errors)")
        else:
            json.dump({
                "run_id": run_id,
                "started_at": dispatch_started_iso,
                "git_sha": git_sha_value,
                "host": socket.gethostname()[:64],
                "overall_status": "fail",
                "runs": run_rows,
            }, sys.stdout, indent=2, sort_keys=True)
            sys.stdout.write("\n")
        return 1

    # I32 P1: dispatcher graph — each branch delegates to a per-CSV validator.
    # Validators not yet shipped on disk SKIP gracefully (the .is_file() guard
    # preserves the legacy behaviour). _delegate_subprocess records the result
    # in run_rows for the structured report.

    scripts_dir = Path(__file__).resolve().parent

    # Per-CSV dispatch table: (label_for_run, validator_filename, optional_csv_existence_check)
    # When CSV check is None, the validator always runs (e.g., language frontmatter).
    dispatch: list[tuple[str, str, str, Path | None]] = [
        ("COMPONENT_SERVICE_MATRIX", "validate_component_service_matrix.py",
         "validate_component_service_matrix", HLK_DIR / "techops" / "COMPONENT_SERVICE_MATRIX.csv"),
        # I81 P2 T1 (D-IH-81-Q under D-IH-81-G umbrella, 2026-05-23): moved to finops/.
        ("FINOPS_COUNTERPARTY_REGISTER", "validate_finops_counterparty_register.py",
         "validate_finops_counterparty_register", HLK_DIR / "finops" / "FINOPS_COUNTERPARTY_REGISTER.csv"),
        # I32 P7 (D-IH-32-D): GOI/POI relocated from compliance/ to compliance/dimensions/.
        # The csv_gate honours the new canonical path. The validator script itself
        # keeps a deprecation-alias fallback (one cycle) for the legacy path.
        ("GOI_POI_REGISTER", "validate_goipoi_register.py",
         "validate_goipoi_register", HLK_DIR / "dimensions" / "GOI_POI_REGISTER.csv"),
        ("ADVISER_ENGAGEMENT_DISCIPLINES", "validate_adviser_disciplines.py",
         "validate_adviser_disciplines",
         # I81 P2 T2 (D-IH-81-R under D-IH-81-G umbrella, 2026-05-23): moved to advops/.
         (HLK_DIR / "advops" / "ADVISER_ENGAGEMENT_DISCIPLINES.csv")
         if (HLK_DIR / "advops" / "ADVISER_ENGAGEMENT_DISCIPLINES.csv").is_file()
         else HLK_DIR / "ADVISER_ENGAGEMENT_DISCIPLINES.csv"),
        ("ADVISER_OPEN_QUESTIONS", "validate_adviser_questions.py",
         "validate_adviser_questions",
         (HLK_DIR / "advops" / "ADVISER_OPEN_QUESTIONS.csv")
         if (HLK_DIR / "advops" / "ADVISER_OPEN_QUESTIONS.csv").is_file()
         else HLK_DIR / "ADVISER_OPEN_QUESTIONS.csv"),
        # I81 P2 T3 (D-IH-81-S, 2026-05-23): CSV + script + Pydantic + mirror table renamed; dispatcher entry uses new validator path with deprecation-alias resolution for CSV path.
        ("FILED_INSTRUMENTS", "validate_filed_instruments.py",
         "validate_filed_instruments",
         (HLK_DIR / "advops" / "FILED_INSTRUMENTS.csv")
         if (HLK_DIR / "advops" / "FILED_INSTRUMENTS.csv").is_file()
         else HLK_DIR / "FOUNDER_FILED_INSTRUMENTS.csv"),
        ("PROGRAM_REGISTRY", "validate_program_registry.py",
         "validate_program_registry", HLK_DIR / "dimensions" / "PROGRAM_REGISTRY.csv"),
        # PROGRAM_ID_CONSISTENCY runs after PROGRAM_REGISTRY (Initiative 23 P3 rule).
        ("PROGRAM_ID_CONSISTENCY", "validate_program_id_consistency.py",
         "validate_program_id_consistency", HLK_DIR / "dimensions" / "PROGRAM_REGISTRY.csv"),
        ("TOPIC_REGISTRY", "validate_topic_registry.py",
         "validate_topic_registry", HLK_DIR / "dimensions" / "TOPIC_REGISTRY.csv"),
        ("PERSONA_REGISTRY", "validate_persona_registry.py",
         "validate_persona_registry", HLK_DIR / "dimensions" / "PERSONA_REGISTRY.csv"),
        ("CHANNEL_TOUCHPOINT_REGISTRY", "validate_channel_touchpoint_registry.py",
         "validate_channel_touchpoint_registry", HLK_DIR / "dimensions" / "CHANNEL_TOUCHPOINT_REGISTRY.csv"),
        ("SOURCING_REGISTER", "validate_sourcing_register.py",
         "validate_sourcing_register", HLK_DIR / "dimensions" / "SOURCING_REGISTER.csv"),
        # Initiative 32 P2 - Skill registry (7th canonical dimension).
        ("SKILL_REGISTRY", "validate_skill_registry.py",
         "validate_skill_registry", HLK_DIR / "dimensions" / "SKILL_REGISTRY.csv"),
        # Initiative 72 P2 - Engagement template registry (sibling canonical at Operations/RevOps/canonicals/dimensions/ per D-IH-72-Y; D-IH-72-F sibling pattern).
        ("ENGAGEMENT_TEMPLATE_REGISTRY", "validate_engagement_template_registry.py",
         "validate_engagement_template_registry",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "RevOps" / "canonicals" / "dimensions" / "ENGAGEMENT_TEMPLATE_REGISTRY.csv"),
        # Initiative 72 P3 - Engagement template promotion gate (paired with SOP-ENGAGEMENT_TEMPLATE_PROMOTION_001.md per akos-executable-process-catalog.mdc Rule 1).
        ("ENGAGEMENT_TEMPLATE_PROMOTION", "validate_engagement_template_promotion.py",
         "validate_engagement_template_promotion",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "RevOps" / "canonicals" / "dimensions" / "ENGAGEMENT_TEMPLATE_REGISTRY.csv"),
        # Initiative 72 P6 - IntelligenceOps register (sibling canonical at Research/Intelligence/canonicals/dimensions/ per D-IH-72-H; not GOI_POI col-extension).
        ("INTELLIGENCEOPS_REGISTER", "validate_intelligenceops_register.py",
         "validate_intelligenceops_register",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Research" / "Intelligence" / "canonicals" / "dimensions" / "INTELLIGENCEOPS_REGISTER.csv"),
        # Initiative 72 P9 - 8 adapter registries (Normalized Adapter Pattern per D-IH-72-O + D-IH-72-T MarTech breadth + D-IH-72-W feature-flag pattern).
        ("ADAPTER_REGISTRIES", "validate_adapter_registries.py",
         "validate_adapter_registries",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Operations" / "RevOps" / "canonicals" / "dimensions" / "REVOPS_ADAPTER_REGISTRY.csv"),
        # Initiative 72 P9 - process_list pairing gate (per D-IH-72-U: every cadence-bound process_list row points at a paired SOP+runbook).
        ("PROCESS_LIST_PAIRING", "validate_process_list_pairing.py",
         "validate_process_list_pairing", HLK_DIR / "process_list.csv"),
        # Initiative 77 P4.C - Rendering Pipeline Registry (orphan-rendering-pipeline governance discovery per D-IH-77-I).
        ("RENDERING_PIPELINE_REGISTRY", "validate_rendering_pipeline_registry.py",
         "validate_rendering_pipeline_registry",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Envoy Tech Lab" / "canonicals" / "dimensions" / "RENDERING_PIPELINE_REGISTRY.csv"),
        # Initiative 85 P1 - Audience Registry (narrow FK index for audience: [J-*] frontmatter per D-IH-85-A,B).
        ("AUDIENCE_REGISTRY", "validate_audience_registry.py",
         "validate_audience_registry", HLK_DIR / "dimensions" / "AUDIENCE_REGISTRY.csv"),
        # Initiative 32 P3 - Touchpoint-kit cell registry (with FS-vs-CSV drift detector).
        ("TOUCHPOINT_KIT_CELL_REGISTRY", "validate_touchpoint_kit_cells.py",
         "validate_touchpoint_kit_cells", HLK_DIR / "dimensions" / "TOUCHPOINT_KIT_CELL_REGISTRY.csv"),
        # Initiative 32 P4 - Policy register (RLS + service_role rotation + redaction + PII scope).
        ("POLICY_REGISTER", "validate_policy_register.py",
         "validate_policy_register", HLK_DIR / "dimensions" / "POLICY_REGISTER.csv"),
        # Initiative 32 P7 - Repo health snapshot (D-IH-32-L pull-based extraction).
        ("REPO_HEALTH_SNAPSHOT", "validate_repo_health_snapshot.py",
         "validate_repo_health_snapshot", HLK_DIR / "REPO_HEALTH_SNAPSHOT.csv"),
        # Initiative 47 P1 - Persona scenario registry (UAT scenario library; D-IH-47-A SSOT).
        ("PERSONA_SCENARIO_REGISTRY", "validate_persona_scenario_registry.py",
         "validate_persona_scenario_registry", HLK_DIR / "dimensions" / "PERSONA_SCENARIO_REGISTRY.csv"),
        # Initiative 73 P1 - Engagement Model Registry (sibling dimension at People Operations per D-IH-73-C;
        # 7-class taxonomy per D-IH-73-D; not GOI/POI or ENGAGEMENT_REGISTRY col-extension).
        ("ENGAGEMENT_MODEL_REGISTRY", "validate_engagement_model_registry.py",
         "validate_engagement_model_registry",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "People Operations" / "canonicals" / "dimensions" / "ENGAGEMENT_MODEL_REGISTRY.csv"),
        # Initiative 86 Wave R+1 Commit 2b + Commit 2b-ext - COLLABORATOR_SHARE umbrella validator
        # (13th Quality Fabric specialty per D-IH-86-DA + D-IH-86-DE). Single dispatch over 5
        # sibling CSVs (COLLABORATOR_SHARE_REGISTRY with share_pattern enum column +
        # HOLISTIKA_VENDOR_SERVICES_BILLED + PARTNER_OVERLAP_EXCLUSION_CLAUSES +
        # COLLABORATOR_MARKET_RATE_REFERENCE + COLLABORATOR_RATE_OVERRIDES) executing the 8 CS-*
        # checks (CS-01..CS-08; CS-03 + CS-04 branch per share_pattern; CS-08 audits enum
        # membership). Gate keyed off the primary COLLABORATOR_SHARE_REGISTRY.csv presence;
        # missing primary CSV => umbrella SKIPs. INFO ramp at mint per akos-collaborator-share.mdc
        # RULE 5 — promotes to FAIL at Wave R+3 once first non-trivial engagement settles + operator
        # ratifies. Runs without --strict here (so the umbrella stays INFO advisory inside
        # validate_hlk); release-gate.py + pre_commit invoke the self-test mode independently for
        # the always-on zero-cost circuit-breaker.
        ("COLLABORATOR_SHARE", "validate_collaborator_share.py",
         "validate_collaborator_share",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "People Operations" / "canonicals" / "dimensions" / "COLLABORATOR_SHARE_REGISTRY.csv"),
        # Initiative 79 P2 - People Design Pattern Registry (CSV registry mode; jargon-scan mode invoked separately
        # via verification-profiles.json profile design_pattern_registry_jargon_scan + pre_commit composition).
        # Codifies People-as-discipline-of-disciplines per D-IH-79-A/C/D + anti-jargon drift gate per D-IH-79-N.
        ("PEOPLE_DESIGN_PATTERN_REGISTRY", "validate_design_pattern_registry.py",
         "validate_design_pattern_registry", HLK_DIR / "dimensions" / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"),
        # Initiative 80 P6.5 - Knowledge Pairing Registry (documentation-relationship registry).
        # Per D-IH-80-H: governs paired-file / index-entry / doctrine-companion relationships across
        # the AKOS canonical vault. Forward-charters Supabase mirror + hlk-erp panel + AI Archivist (I83).
        ("KNOWLEDGE_PAIRING_REGISTRY", "validate_knowledge_pairing_registry.py",
         "validate_knowledge_pairing_registry", HLK_DIR / "dimensions" / "KNOWLEDGE_PAIRING_REGISTRY.csv"),
        # Initiative 84 P3 - Substrate Registry (substrate doctrine SSOT per D-IH-84-A/F/G).
        # 18-column schema + 8 enum frozensets; canonical-CSV gate seeded with 18 rows
        # (8 framework + 7 agent-SDK + 3 architectural-posture); Research-area paired
        # with SUBSTRATE_LANDSCAPE_DOCTRINE.md at Research/Methodology/canonicals/.
        ("SUBSTRATE_REGISTRY", "validate_substrate_registry.py",
         "validate_substrate_registry", HLK_DIR / "dimensions" / "SUBSTRATE_REGISTRY.csv"),
        # Initiative 93 P2 - Data Contract Registry (ODCS-aligned producer-consumer SSOT).
        # Per D-IH-93-D: federated governance + contract standard; quality_rules reference DATA-01..07.
        ("DATA_CONTRACT_REGISTRY", "validate_data_contract_registry.py",
         "validate_data_contract_registry",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Data"
         / "Governance" / "canonicals" / "dimensions" / "DATA_CONTRACT_REGISTRY.csv"),
        ("METRICS_REGISTRY", "validate_metrics_registry.py",
         "validate_metrics_registry",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Data"
         / "Architecture" / "canonicals" / "dimensions" / "METRICS_REGISTRY.csv"),
        ("BI_CONSUMER_REGISTRY", "validate_bi_consumer_registry.py",
         "validate_bi_consumer_registry",
         REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "Data"
         / "Governance" / "canonicals" / "dimensions" / "BI_CONSUMER_REGISTRY.csv"),
        ("CAPABILITY_REGISTRY", "validate_capability_registry.py",
         "validate_capability_registry", HLK_DIR / "dimensions" / "CAPABILITY_REGISTRY.csv"),
        ("CAPABILITY_CONFIDENCE_REGISTRY", "validate_capability_confidence_registry.py",
         "validate_capability_confidence_registry",
         HLK_DIR / "dimensions" / "CAPABILITY_CONFIDENCE_REGISTRY.csv"),
        ("USE_CASE_ARCHIVE", "validate_use_case_archive.py",
         "validate_use_case_archive",
         HLK_DIR / "dimensions" / "USE_CASE_ARCHIVE.csv"),
        ("AIC_REGISTRY", "validate_aic_registry.py",
         "validate_aic_registry",
         HLK_DIR / "dimensions" / "AIC_REGISTRY.csv"),
        ("MADEIRA_AIC_PER_TASK_REGISTRY", "validate_madeira_aic_per_task.py",
         "validate_madeira_aic_per_task",
         HLK_DIR / "dimensions" / "MADEIRA_AIC_PER_TASK_REGISTRY.csv"),
        ("AIC_CAPABILITY_IMPLEMENTATION_MATRIX",
         "validate_aic_capability_implementation_matrix.py",
         "validate_aic_capability_implementation_matrix",
         HLK_DIR / "dimensions" / "AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv"),
        # Initiative 86 Wave K + L - 4-layer output architecture beneath the 5-axis Quality Fabric.
        # Composite validator covers Layer 1 OUTPUT_TYPE_REGISTRY + Layer 2 ARTIFACT_CLASS_REGISTRY +
        # Layer 3 COMPONENT_PRIMITIVE_REGISTRY in one pass. Also FK-resolves
        # ARTIFACT_CLASS.output_type_codes and ARTIFACT_CLASS.typical_audience_codes and
        # COMPONENT_PRIMITIVE.parent_artifact_class_codes across the 3 layers and into
        # AUDIENCE_REGISTRY. Per D-IH-86-BB (Wave K mint) + D-IH-86-BG (Wave L Pydantic + mirror).
        # Gate keyed off OUTPUT_TYPE_REGISTRY.csv presence; if missing, all 3 layers SKIP.
        ("OUTPUT_ARCHITECTURE_REGISTRIES", "validate_output_architecture_registries.py",
         "validate_output_architecture_registries", HLK_DIR / "dimensions" / "OUTPUT_TYPE_REGISTRY.csv"),
        # Initiative 59 P1 - HLK governance dimensions (5 new CSVs + 3 sync gates).
        # REPOSITORY_REGISTRY first because INITIATIVE_REGISTRY FKs into it.
        ("REPOSITORY_REGISTRY", "validate_repository_registry.py",
         "validate_repository_registry", HLK_DIR / "REPOSITORY_REGISTRY.csv"),
        ("REPOSITORY_REGISTRY_MD_CSV_SYNC", "validate_repository_registry_md_csv_sync.py",
         "validate_repository_registry_md_csv_sync", HLK_DIR / "REPOSITORY_REGISTRY.csv"),
        ("CYCLE_REGISTER", "validate_cycle_register.py",
         "validate_cycle_register", HLK_DIR / "CYCLE_REGISTER.csv"),
        ("DECISION_REGISTER", "validate_decision_register.py",
         "validate_decision_register", HLK_DIR / "DECISION_REGISTER.csv"),
        ("INITIATIVE_REGISTRY", "validate_initiative_registry.py",
         "validate_initiative_registry", HLK_DIR / "INITIATIVE_REGISTRY.csv"),
        ("INITIATIVE_REGISTRY_FRONTMATTER_SYNC", "validate_initiative_registry_frontmatter_sync.py",
         "validate_initiative_registry_frontmatter_sync", HLK_DIR / "INITIATIVE_REGISTRY.csv"),
        # Initiative 86 P1 — INITIATIVE_REGISTRY -> PROGRAM_REGISTRY anchor prefix (D-IH-86-H).
        # Stage A: validates the "Program anchors:" prefix in notes; Stage B (I86 P2 / D-IH-86-J)
        # promotes anchors to a first-class column. Validator no-ops rows without the prefix.
        ("INITIATIVE_PROGRAM_ANCHORS", "validate_initiative_program_anchors.py",
         "validate_initiative_program_anchors", HLK_DIR / "INITIATIVE_REGISTRY.csv"),
        ("OPS_REGISTER", "validate_ops_register.py",
         "validate_ops_register", HLK_DIR / "OPS_REGISTER.csv"),
        ("DECISION_REGISTER_DECISION_LOG_MD_SYNC", "validate_decision_register_decision_log_md_sync.py",
         "validate_decision_register_decision_log_md_sync", HLK_DIR / "DECISION_REGISTER.csv"),
        # I59 P2 — frontmatter-side enforcement. No CSV gate; scans planning workspace directly.
        # Advisory mode by default (warnings printed; not failing); becomes strict at I59 P10.
        ("MASTER_ROADMAP_FRONTMATTER", "validate_master_roadmap_frontmatter.py",
         "validate_master_roadmap_frontmatter", None),
        # LANGUAGE_FRONTMATTER has no CSV gate; it scans the vault directly.
        ("LANGUAGE_FRONTMATTER", "validate_hlk_language_frontmatter.py",
         "validate_hlk_language_frontmatter", None),
    ]

    for label, fname, run_label, csv_gate in dispatch:
        validator_path = scripts_dir / fname
        # If the CSV gate is set and missing: SKIP (legacy behaviour).
        if csv_gate is not None and not csv_gate.is_file():
            run_rows.append(_make_run_row(
                run_id=run_id,
                validator_name=run_label,
                started_at_iso=dispatch_started_iso,
                duration_ms=0,
                status="skipped",
                exit_code=0,
                notes=f"csv gate not present: {csv_gate.name}",
                git_sha_value=git_sha_value,
            ))
            continue
        # If the validator script is itself missing: SKIP gracefully (legacy behaviour
        # for the language frontmatter validator).
        if not validator_path.is_file():
            run_rows.append(_make_run_row(
                run_id=run_id,
                validator_name=run_label,
                started_at_iso=dispatch_started_iso,
                duration_ms=0,
                status="skipped",
                exit_code=0,
                notes=f"validator script not present: {fname}",
                git_sha_value=git_sha_value,
            ))
            continue

        # Special-case the language frontmatter validator: legacy code only printed
        # the trailing summary block (file list is too verbose).
        if run_label == "validate_hlk_language_frontmatter":
            started = time.time()
            started_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started))
            r = subprocess.run([sys.executable, str(validator_path)], capture_output=True, text=True)
            if not args.json:
                print("\n".join(r.stdout.splitlines()[-9:]))
            if r.stderr and r.returncode != 0:
                print(r.stderr, end="", file=sys.stderr)
            duration_ms = int((time.time() - started) * 1000)
            run_rows.append(_make_run_row(
                run_id=run_id,
                validator_name=run_label,
                started_at_iso=started_iso,
                duration_ms=duration_ms,
                status="pass" if r.returncode == 0 else "fail",
                exit_code=r.returncode,
                notes="dispatched subprocess (stdout summary only)",
                git_sha_value=git_sha_value,
            ))
            if r.returncode != 0:
                if not args.json:
                    print(f"  {label}: FAIL")
                else:
                    json.dump({
                        "run_id": run_id,
                        "started_at": dispatch_started_iso,
                        "git_sha": git_sha_value,
                        "host": socket.gethostname()[:64],
                        "overall_status": "fail",
                        "runs": run_rows,
                    }, sys.stdout, indent=2, sort_keys=True)
                    sys.stdout.write("\n")
                return 1
            if not args.json:
                print(f"  {label}: PASS")
            continue

        # Standard subprocess delegation: forward stdout/stderr verbatim, record row.
        # When --json is set, suppress per-validator stdout to keep the JSON output clean.
        started = time.time()
        started_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started))
        r = subprocess.run([sys.executable, str(validator_path)], capture_output=True, text=True)
        if not args.json:
            print(r.stdout, end="")
            if r.stderr:
                print(r.stderr, end="", file=sys.stderr)
        elif r.stderr and r.returncode != 0:
            print(r.stderr, end="", file=sys.stderr)
        duration_ms = int((time.time() - started) * 1000)
        run_rows.append(_make_run_row(
            run_id=run_id,
            validator_name=run_label,
            started_at_iso=started_iso,
            duration_ms=duration_ms,
            status="pass" if r.returncode == 0 else "fail",
            exit_code=r.returncode,
            notes="dispatched subprocess",
            git_sha_value=git_sha_value,
        ))
        if r.returncode != 0:
            if not args.json:
                print(f"  {label}: FAIL")
            else:
                json.dump({
                    "run_id": run_id,
                    "started_at": dispatch_started_iso,
                    "git_sha": git_sha_value,
                    "host": socket.gethostname()[:64],
                    "overall_status": "fail",
                    "runs": run_rows,
                }, sys.stdout, indent=2, sort_keys=True)
                sys.stdout.write("\n")
            return 1
        if not args.json:
            print(f"  {label}: PASS")

    if args.json:
        json.dump({
            "run_id": run_id,
            "started_at": dispatch_started_iso,
            "git_sha": git_sha_value,
            "host": socket.gethostname()[:64],
            "overall_status": "pass",
            "runs": run_rows,
        }, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print("  OVERALL: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
