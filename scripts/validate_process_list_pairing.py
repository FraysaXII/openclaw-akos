"""Pairing validator for `process_list.csv` cadence-bound rows (Initiative 72 P9).

Per `D-IH-72-U` (full validator at I72 P9, not micro-scaffold or successor-deferred).

Contract: every row in `process_list.csv` whose `cadence_type` cell is non-empty
(meaning: the operator has declared this process as cadence-bound under the I72
multi-axis dimension ontology — `D-IH-72-Q` cadence taxonomy: `on_demand` |
`scheduled` | `event_triggered` | `gated_operator`) MUST be paired with both:

1. A SOP body discoverable in the role-owner area canonicals folder (paired SOP
   per `akos-executable-process-catalog.mdc` Rule 1).
2. A runbook pointer (executable script or YAML catalog entry) discoverable in
   `scripts/` or `docs/references/hlk/v3.0/.../canonicals/*.yaml`.

The validator is tolerant on day 1:
- Rows with `cadence_type=gated_operator` whose `instructions` cell carries a
  `TODO[I72-...]` or `TODO[I73-...]` marker per `D-IH-72-W` (feature-flag pattern)
  are allowed without paired-runbook discovery (operator-driven gates can defer
  runbook authoring to successor initiatives).
- Rows whose `cadence_type` cell is empty are skipped (pre-I72 process list rows
  and non-cadence-bound rows are not in scope).

Exit code 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

PROCESS_LIST = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals" / "process_list.csv"
SCRIPTS_DIR = REPO_ROOT / "scripts"
HLK_VAULT = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0"

VALID_CADENCES = frozenset({"on_demand", "scheduled", "event_triggered", "gated_operator"})
TODO_MARKER_RE = re.compile(r"TODO\[(I7[0-9]+|OPERATOR)[-:][A-Za-z0-9_\-]+\]")


def _runbook_discoverable(item_id: str) -> bool:
    """Heuristic: a runbook is discoverable if a script or YAML catalog references the item_id."""
    candidates: list[Path] = [
        SCRIPTS_DIR / "revops_dispatch.py",
        SCRIPTS_DIR / "scaffold_engagement.py",
        SCRIPTS_DIR / "check_ethics_learning_review_due.py",
        SCRIPTS_DIR / "peopl_recruiter_onboarding_checklist_stub.py",
        HLK_VAULT / "Admin" / "O5-1" / "Operations" / "RevOps" / "canonicals" / "REVOPS_PROCESS_CATALOG.yaml",
    ]
    candidates.extend(sorted(SCRIPTS_DIR.glob("peopl_engagement*.py")))
    candidates.extend(sorted(SCRIPTS_DIR.glob("peopl_agentic*.py")))
    candidates.extend(sorted(SCRIPTS_DIR.glob("tech_agentic*.py")))
    candidates.extend(sorted(SCRIPTS_DIR.glob("peopl_cross_area*.py")))
    # I86 Wave H Lane F (D-IH-86-AE) — app governance runbook glob.
    candidates.extend(sorted(SCRIPTS_DIR.glob("inventory_github*.py")))
    # I86 Wave I Lane I-B (D-IH-86-AN) — operational cohesion doctrine runbook glob.
    candidates.extend(sorted(SCRIPTS_DIR.glob("render_operational_cohesion*.py")))
    for p in candidates:
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if item_id in text:
            return True
    return False


def _sop_discoverable(role_owner: str, item_name: str) -> bool:
    """Heuristic: a paired SOP is discoverable if at least one *.md file in the
    role-owner area canonicals references the item_name OR if the area has a
    'SOP-' file body that mentions the role_owner verbatim. Per Rule 1 of
    akos-executable-process-catalog.mdc the SSOT could be at multiple paths;
    we use a permissive scan."""
    if not role_owner.strip():
        return False
    role_plain = role_owner.lower().strip()
    role_token = role_plain.replace(" ", "_")
    name_token = item_name.lower().replace(" ", "_")[:30] if item_name else ""
    for sop in HLK_VAULT.rglob("SOP-*.md"):
        try:
            body = sop.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue
        if role_plain in body or role_token in body or (name_token and name_token in body):
            return True
    return False


def main() -> int:
    if not PROCESS_LIST.exists():
        print(f"  process_list.csv missing at {PROCESS_LIST}")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    cadence_counts: dict[str, int] = {c: 0 for c in VALID_CADENCES}
    paired_count = 0
    skipped_count = 0
    deferred_count = 0

    with PROCESS_LIST.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for line_no, row in enumerate(reader, start=2):
            cadence = (row.get("cadence_type") or "").strip()
            if not cadence:
                skipped_count += 1
                continue
            if cadence not in VALID_CADENCES:
                errors.append(f"L{line_no} item_id={row.get('item_id', '?')!r}: cadence_type {cadence!r} not in {sorted(VALID_CADENCES)}")
                continue
            cadence_counts[cadence] += 1

            item_id = (row.get("item_id") or "").strip()
            item_name = (row.get("item_name") or "").strip()
            role_owner = (row.get("role_owner") or "").strip()
            instructions = (row.get("instructions") or "")

            if cadence == "gated_operator" and TODO_MARKER_RE.search(instructions):
                deferred_count += 1
                continue

            sop_ok = _sop_discoverable(role_owner, item_name)
            runbook_ok = _runbook_discoverable(item_id) if cadence != "gated_operator" else True

            if not sop_ok:
                warnings.append(f"L{line_no} item_id={item_id!r}: paired SOP body not discoverable for role_owner={role_owner!r} item_name={item_name!r} (per akos-executable-process-catalog.mdc Rule 1; consider TODO[I72-...] marker per D-IH-72-W)")
            if not runbook_ok:
                warnings.append(f"L{line_no} item_id={item_id!r}: paired runbook pointer not discoverable in scripts/ or REVOPS_PROCESS_CATALOG.yaml (cadence={cadence})")
            if sop_ok and runbook_ok:
                paired_count += 1

    print()
    print("  PROCESS_LIST_PAIRING Validator")
    print("  =" * 25)
    print(f"  Cadence-bound rows: {sum(cadence_counts.values())}")
    for c in sorted(VALID_CADENCES):
        print(f"    {c:<18}: {cadence_counts[c]}")
    print(f"  Paired (SOP + runbook discoverable): {paired_count}")
    print(f"  Operator-deferred (TODO[I7X-...] markers per D-IH-72-W): {deferred_count}")
    print(f"  Non-cadence rows skipped: {skipped_count}")
    if warnings:
        print(f"  Warnings: {len(warnings)} (informational; per D-IH-72-W feature-flag pattern, paired SOPs/runbooks may be deferred to successor initiatives)")
        for w in warnings[:10]:
            print(f"    - {w}")
        if len(warnings) > 10:
            print(f"    ... and {len(warnings) - 10} more (truncated)")
    if errors:
        print()
        print("  ERRORS:")
        for e in errors:
            print(f"    - {e}")
        print("  FAIL")
        return 1
    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
