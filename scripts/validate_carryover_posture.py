"""Validator for work-item carryover posture index (I98 P0).

Paired index: ``docs/wip/planning/_trackers/carryover-posture-index.md``
SSOT enum: ``akos/planning/carryover_posture.py``

Posture per I98 ramp:

- ``--self-test``  : fixture validation; exit 0 on PASS
- ``--index PATH`` : validate index table rows; INFO advisory (exit 0 unless --strict)
- ``--strict``     : exit non-zero on findings
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.planning.carryover_posture import (  # noqa: E402
    REQUIRED_COMPANION_FIELDS,
    VALID_CARRYOVER_POSTURES,
    is_valid_posture,
    required_companion_fields,
)

DEFAULT_INDEX = (
    REPO_ROOT / "docs/wip/planning/_trackers/carryover-posture-index.md"
)

INDEX_TABLE_HEADER = (
    "| index_id | posture | item_id | target / successor | activation_trigger | "
    "next_review | owner | discoverability_path |"
)
INDEX_ROW_RE = re.compile(
    r"^\|\s*(CO-\d+-\d+)\s*\|\s*([a-z_]+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*`?([^|`]+)`?\s*\|"
)


def self_test() -> int:
    """Run Pydantic-free fixture checks on the SSOT module."""
    errors: list[str] = []
    if len(VALID_CARRYOVER_POSTURES) != 7:
        errors.append(f"expected 7 postures, got {len(VALID_CARRYOVER_POSTURES)}")
    for posture, fields in REQUIRED_COMPANION_FIELDS.items():
        if not is_valid_posture(posture):
            errors.append(f"REQUIRED_COMPANION_FIELDS key invalid: {posture}")
        if posture == "scheduled" and "discoverability_path" not in fields:
            errors.append("scheduled must require discoverability_path")
        if posture == "scheduled" and "next_review_trigger" not in fields:
            errors.append("scheduled must require next_review_trigger")
    if required_companion_fields("bogus"):
        errors.append("unknown posture should return empty companion tuple")
    if errors:
        for e in errors:
            print(f"SELF-TEST FAIL: {e}", file=sys.stderr)
        return 1
    print("validate_carryover_posture: self-test PASS (7 postures + companion map)")
    return 0


def _parse_index_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_table = False
    for line in text.splitlines():
        if line.strip() == INDEX_TABLE_HEADER:
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                if rows:
                    break
                continue
            if ":---" in line or line.strip() == "|":
                continue
            m = INDEX_ROW_RE.match(line.strip())
            if not m:
                continue
            rows.append(
                {
                    "index_id": m.group(1).strip(),
                    "posture": m.group(2).strip(),
                    "item_id": m.group(3).strip(),
                    "target": m.group(4).strip(),
                    "activation_trigger": m.group(5).strip(),
                    "next_review": m.group(6).strip(),
                    "owner": m.group(7).strip(),
                    "discoverability_path": m.group(8).strip().strip("`"),
                }
            )
    return rows


def validate_index(path: Path) -> list[str]:
    findings: list[str] = []
    if not path.is_file():
        return [f"index file missing: {path.relative_to(REPO_ROOT)}"]
    text = path.read_text(encoding="utf-8")
    rows = _parse_index_rows(text)
    if not rows:
        findings.append("no index rows parsed from Active index rows table")
        return findings
    seen_ids: set[str] = set()
    for row in rows:
        idx = row["index_id"]
        if idx in seen_ids:
            findings.append(f"duplicate index_id: {idx}")
        seen_ids.add(idx)
        posture = row["posture"]
        if not is_valid_posture(posture):
            findings.append(f"{idx}: invalid posture '{posture}'")
            continue
        if not row["discoverability_path"]:
            findings.append(f"{idx}: missing discoverability_path")
        if posture in ("scheduled", "forward_charter", "overlap_pending", "blocked", "monitoring"):
            if not row["activation_trigger"] or row["activation_trigger"] == "—":
                findings.append(f"{idx}: {posture} requires activation_trigger")
            if not row["next_review"] or row["next_review"] == "—":
                findings.append(f"{idx}: {posture} requires next_review (staleness guard)")
            if not row["owner"] or row["owner"] == "—":
                findings.append(f"{idx}: {posture} requires owner")
        if posture == "scheduled" and (not row["target"] or row["target"] == "—"):
            findings.append(f"{idx}: scheduled requires target / successor column")
        disc = row["discoverability_path"]
        if disc and not disc.startswith("docs/"):
            findings.append(f"{idx}: discoverability_path should be repo-relative docs/ path")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--index", type=Path, default=None, help="path to carryover-posture-index.md")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    index_path = args.index or DEFAULT_INDEX
    findings = validate_index(index_path)
    if findings:
        print(f"validate_carryover_posture: {len(findings)} finding(s) on {index_path.name}")
        for f in findings:
            print(f"  - {f}")
        if args.strict:
            return 1
    else:
        rows = _parse_index_rows(index_path.read_text(encoding="utf-8"))
        print(f"validate_carryover_posture: index PASS ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
