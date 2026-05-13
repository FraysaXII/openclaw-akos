#!/usr/bin/env python3
"""Initiative 59 P3 — apply the status-audit YAML to master-roadmaps + REGISTRY CSVs.

Reads the audit YAML produced in P3 (one entry per initiative) and:

1. **Frontmatter side**: for every ``docs/wip/planning/<NN>-<slug>/master-roadmap.md``
   adds or updates the YAML frontmatter to include the I59 taxonomy ``status:``
   plus the required companion fields per
   ``akos.planning.status_taxonomy.REQUIRED_COMPANION_FIELDS``. Existing
   non-conflicting frontmatter keys are preserved verbatim.

2. **CSV side (bulk seed)**: writes one row per audited initiative into
   ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`` (status + last_review
   + decision FKs + cycle FK) and one row per ``ops_action_id`` reference into
   ``docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv`` (status='open' for
   forwarded references unless the audit marks them otherwise).

The script is **idempotent**: running it again with the same YAML produces the
same outputs (text-stable diff). It is also **dry-run by default** — without
``--write`` it prints the proposed changes and exits 0 without touching files.

Usage::

    py scripts/apply_status_audit.py <audit.yaml>            # dry-run
    py scripts/apply_status_audit.py <audit.yaml> --write    # apply

Cycle / decision register seeding is performed by sibling scripts
(``seed_cycle_register.py``, ``seed_decision_register.py``) so this script
can stay focused on the audit -> initiatives + ops application.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_initiative_registry_csv import INITIATIVE_REGISTRY_FIELDNAMES
from akos.hlk_ops_register_csv import OPS_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT
from akos.planning.status_taxonomy import (
    REQUIRED_COMPANION_FIELDS,
    VALID_INITIATIVE_STATUSES,
)

PLANNING_DIR = REPO_ROOT / "docs" / "wip" / "planning"
HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
INITIATIVE_REGISTRY_CSV = HLK_COMPLIANCE / "INITIATIVE_REGISTRY.csv"
OPS_REGISTER_CSV = HLK_COMPLIANCE / "OPS_REGISTER.csv"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+?)$", re.MULTILINE)
FOLDER_PREFIX_RE = re.compile(r"^(\d{2,3}[a-z]?)-")
DEFAULT_REPO_SLUG = "openclaw-akos"
DEFAULT_OWNER_ROLE = "PMO"


def _repo_slug_to_id_segment(repo_slug: str) -> str:
    """Convert ``openclaw-akos`` → ``OPENCLAW_AKOS`` for INIT- id construction."""
    return repo_slug.upper().replace("-", "_")


def _folder_to_init_id(folder: str, repo_slug: str = DEFAULT_REPO_SLUG) -> str:
    """Derive ``INIT-OPENCLAW_AKOS-NN`` from folder name like ``58-cycle-2-multi-track-forward``."""
    m = FOLDER_PREFIX_RE.match(folder)
    if not m:
        raise ValueError(f"folder {folder!r} does not start with a numeric prefix")
    return f"INIT-{_repo_slug_to_id_segment(repo_slug)}-{m.group(1).upper()}"


def _build_id_map(initiatives: list[dict[str, object]]) -> dict[str, str]:
    """Return ``{snake_case_id: INIT-OPENCLAW_AKOS-NN}`` map across the audit."""
    out: dict[str, str] = {}
    for a in initiatives:
        snake = str(a.get("initiative_id") or "").strip()
        folder = str(a.get("folder") or "").strip()
        if not snake or not folder:
            continue
        out[snake] = _folder_to_init_id(folder)
    return out


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str, str]:
    """Return ``(fm_dict, fm_block_raw, body_text)`` for a markdown file.

    ``fm_dict`` is empty when frontmatter is absent.
    ``fm_block_raw`` is the YAML lines between the fences (no fences).
    ``body_text`` is the markdown content after the closing fence (or the
    full text if no frontmatter exists).
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, "", text
    raw = m.group(1)
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        loaded = {}
    if not isinstance(loaded, dict):
        loaded = {}
    return loaded, raw, text[m.end():]


def _emit_frontmatter(fm: dict[str, object], body: str) -> str:
    """Render ``fm`` as a YAML frontmatter block followed by ``body``.

    Order: well-known canonical keys first (``language``, ``status``, …) so
    the resulting file is readable; remaining keys preserved in insertion
    order. Excludes empty / None values. Uses ``yaml.safe_dump`` for each
    value so prose containing colons or special characters round-trips
    safely.
    """
    canonical_order = (
        "language",
        "status",
        "initiative",
        "initiative_id",
        "report_kind",
        "program_id",
        "plane",
        "authority",
        "last_review",
        "closed_at",
        "closure_decision_id",
        "archived_at",
        "superseded_by",
        "continuous_rationale",
        "cadence",
        "gated_on",
        "operator_action",
    )
    ordered: dict[str, object] = {}
    for k in canonical_order:
        if k in fm and fm[k] not in (None, "", []):
            ordered[k] = fm[k]
    for k, v in fm.items():
        if k in ordered or v in (None, "", []):
            continue
        ordered[k] = v
    yaml_block = yaml.safe_dump(
        ordered,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=10**6,
    ).rstrip()
    return "---\n" + yaml_block + "\n---\n" + body


def _build_frontmatter(
    existing: dict[str, object],
    audit: dict[str, object],
    id_map: dict[str, str],
) -> dict[str, object]:
    """Merge audit values into existing frontmatter per the I59 taxonomy.

    Ensures ``language: en`` is present, sets ``status:`` to the audited value,
    populates required companion fields, and updates ``last_review``. Resolves
    snake_case ids in ``superseded_by`` to canonical INIT- ids using ``id_map``.
    Existing non-conflicting keys are preserved.
    """
    out = dict(existing)
    out.setdefault("language", "en")
    out["status"] = audit["inferred_status"]
    required = REQUIRED_COMPANION_FIELDS.get(audit["inferred_status"], ())
    for field in required:
        v = audit.get(field)
        if v not in (None, ""):
            out[field] = v
    if audit.get("closed_at"):
        out["closed_at"] = audit["closed_at"]
    if audit.get("closure_decision_id"):
        out["closure_decision_id"] = audit["closure_decision_id"]
    if audit.get("archived_at"):
        out["archived_at"] = audit["archived_at"]
    if audit.get("superseded_by"):
        sb = str(audit["superseded_by"]).strip()
        out["superseded_by"] = id_map.get(sb, sb)
    if audit.get("last_review"):
        out["last_review"] = audit["last_review"]
    folder = str(audit.get("folder") or "")
    if folder:
        out["initiative_id"] = _folder_to_init_id(folder)
    return out


def _apply_frontmatter(
    audit: dict[str, object],
    id_map: dict[str, str],
) -> tuple[Path, str | None, str | None]:
    """Return ``(path, before, after)`` — ``after`` is None if no changes needed."""
    folder = PLANNING_DIR / str(audit["folder"])
    path = folder / "master-roadmap.md"
    if not path.is_file():
        return path, None, None
    text = path.read_text(encoding="utf-8")
    fm, _, body = _parse_frontmatter(text)
    new_fm = _build_frontmatter(fm, audit, id_map)
    new_text = _emit_frontmatter(new_fm, body)
    if new_text == text:
        return path, text, None
    return path, text, new_text


def _cycle_id_for_folder(folder: str) -> str:
    if folder.startswith("57-"):
        return "CYC-57"
    if folder.startswith("58-"):
        return "CYC-58"
    if folder.startswith("59-"):
        return "CYC-59"
    return ""


def _emit_initiative_row(audit: dict[str, object], id_map: dict[str, str]) -> dict[str, str]:
    folder = str(audit["folder"])
    status = str(audit["inferred_status"])
    init_id = _folder_to_init_id(folder)
    last_review = str(audit.get("last_review") or "")
    closure_decision_id = str(audit.get("closure_decision_id") or "")
    superseded_snake = str(audit.get("superseded_by") or "").strip()
    superseded_by = id_map.get(superseded_snake, superseded_snake) if superseded_snake else ""
    folder_path = f"docs/wip/planning/{folder}/"
    closed_at = str(audit.get("closed_at") or "")
    archived_at = str(audit.get("archived_at") or "")
    row: dict[str, str] = {
        "initiative_id": init_id,
        "repo_slug": DEFAULT_REPO_SLUG,
        "folder_path": folder_path,
        "title": str(audit.get("title") or ""),
        "status": status,
        "cycle_id": _cycle_id_for_folder(folder),
        "owner_role": DEFAULT_OWNER_ROLE,
        "inception_date": "",
        "last_review": last_review,
        "closed_at": closed_at,
        "archived_at": archived_at,
        "superseded_by": superseded_by,
        "continuous_rationale": str(audit.get("continuous_rationale") or ""),
        "cadence": str(audit.get("cadence") or ""),
        "gated_on": str(audit.get("gated_on") or ""),
        "operator_action": str(audit.get("operator_action") or ""),
        "inception_decision_id": "",
        "closure_decision_id": closure_decision_id,
        "manifests_processes": "",
        "linked_topic_ids": "",
        "notes": "seeded by I59 P3 audit pass",
    }
    return {fn: row.get(fn, "") for fn in INITIATIVE_REGISTRY_FIELDNAMES}


def _emit_ops_rows(audited: list[dict[str, object]], id_map: dict[str, str]) -> list[dict[str, str]]:
    """One row per (initiative, ops_action_id) pair seen in the audit.

    De-duplicated on ``ops_action_id`` (later occurrences keep the originating
    initiative_id of the *first* occurrence; subsequent occurrences are
    treated as references and skipped — the originating initiative owns it).
    """
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for a in audited:
        folder = str(a.get("folder") or "")
        if not folder:
            continue
        init_id = _folder_to_init_id(folder)
        for ops_id in a.get("ops_action_ids") or []:
            ops_str = str(ops_id).strip()
            if not ops_str or ops_str in seen:
                continue
            seen.add(ops_str)
            row: dict[str, str] = {
                "ops_action_id": ops_str,
                "title": "",
                "originating_initiative_id": init_id,
                "forwarded_to_initiative_id": "",
                "owner_class": "operator",
                "owner_role": DEFAULT_OWNER_ROLE,
                "status": "open",
                "rice_score": "",
                "rice_impact": "",
                "linked_decision_ids": "",
                "linked_policies": "",
                "originating_at": str(a.get("last_review") or ""),
                "closed_at": "",
                "notes": "seeded by I59 P3 audit pass; verify owner_class + RICE",
            }
            out.append({fn: row.get(fn, "") for fn in OPS_REGISTER_FIELDNAMES})
    return out


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_yaml", type=Path, help="Path to the P3 audit YAML")
    parser.add_argument("--write", action="store_true", help="Apply changes (otherwise dry-run)")
    args = parser.parse_args()

    if not args.audit_yaml.is_file():
        print(f"error: audit YAML not found: {args.audit_yaml}", file=sys.stderr)
        return 1
    with args.audit_yaml.open(encoding="utf-8") as f:
        audit_doc = yaml.safe_load(f) or {}
    initiatives = audit_doc.get("initiatives") or []
    if not initiatives:
        print("error: no 'initiatives:' block in YAML", file=sys.stderr)
        return 1

    id_map = _build_id_map(initiatives)
    fm_changes: list[tuple[Path, str | None]] = []
    init_rows: list[dict[str, str]] = []
    bad: list[str] = []
    for a in initiatives:
        status = a.get("inferred_status")
        if status not in VALID_INITIATIVE_STATUSES:
            bad.append(f"{a.get('folder')}: invalid status '{status}'")
            continue
        path, _, after = _apply_frontmatter(a, id_map)
        fm_changes.append((path, after))
        init_rows.append(_emit_initiative_row(a, id_map))

    ops_rows = _emit_ops_rows(initiatives, id_map)

    fm_drift = sum(1 for _, after in fm_changes if after is not None)

    print()
    print("  apply_status_audit")
    print("  ========================================")
    print(f"  Initiatives in audit:       {len(initiatives)}")
    print(f"  Master-roadmap drift:       {fm_drift}")
    print(f"  INITIATIVE_REGISTRY rows:   {len(init_rows)}")
    print(f"  OPS_REGISTER rows:          {len(ops_rows)}")
    if bad:
        print(f"  Audit errors: {len(bad)}")
        for b in bad:
            print(f"    - {b}")
        return 1

    if not args.write:
        print()
        print("  DRY-RUN: pass --write to apply the changes.")
        if fm_drift:
            print()
            print("  Master-roadmaps that would change:")
            for path, after in fm_changes[:50]:
                if after is not None:
                    print(f"    - {path.relative_to(REPO_ROOT)}")
            if fm_drift > 50:
                print(f"    ... and {fm_drift - 50} more")
        return 0

    for path, after in fm_changes:
        if after is None:
            continue
        path.write_text(after, encoding="utf-8")
    _write_csv(INITIATIVE_REGISTRY_CSV, INITIATIVE_REGISTRY_FIELDNAMES, init_rows)
    _write_csv(OPS_REGISTER_CSV, OPS_REGISTER_FIELDNAMES, ops_rows)
    print()
    print("  WROTE:")
    print(f"    {fm_drift} master-roadmaps updated (frontmatter)")
    print(f"    {INITIATIVE_REGISTRY_CSV.relative_to(REPO_ROOT)} ({len(init_rows)} rows)")
    print(f"    {OPS_REGISTER_CSV.relative_to(REPO_ROOT)} ({len(ops_rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
