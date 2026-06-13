"""Validator for the 9 adapter registries (Initiative 72 P9 + I93 P5b RPA).

Per `D-IH-72-O` (Normalized Adapter Pattern + status metadata) +
`D-IH-72-T` (MarTech adapter breadth) + `D-IH-72-W` (feature-flag pattern
with TODO markers).

Exit code 0 PASS, 1 FAIL.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_adapter_registry_csv import (  # noqa: E402
    ADAPTER_REGISTRY_FIELDNAMES,
    REGISTRY_CLASSES,
    REGISTRY_PATHS,
    VALID_ADAPTER_KINDS,
    VALID_FEATURE_FLAGS,
    VALID_STATUSES,
)
from akos.hlk_infonomics_register import (  # noqa: E402
    VALID_HANDOFF_COST_BANDS,
    VALID_REVOPS_VALUE_STREAM_IDS,
)

ADAPTER_ID_RE = re.compile(r"^[a-z0-9_]{3,80}$")
TODO_MARKER_RE = re.compile(r"^TODO\[[A-Za-z0-9_\-:]+\]$")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    by_class: dict[str, dict[str, int]] = {}

    for cls_name, rel_path in REGISTRY_PATHS.items():
        path = REPO_ROOT / rel_path
        if not path.exists():
            errors.append(f"Adapter registry {cls_name} missing at {rel_path}")
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if tuple(reader.fieldnames or ()) != ADAPTER_REGISTRY_FIELDNAMES:
                errors.append(
                    f"{cls_name} schema mismatch: header={reader.fieldnames!r} expected={list(ADAPTER_REGISTRY_FIELDNAMES)!r}"
                )
                continue
            class_counts = by_class.setdefault(cls_name, {"active": 0, "inactive": 0, "planned": 0, "experimental": 0, "deprecated": 0})
            for line_no, row in enumerate(reader, start=2):
                aid = row.get("adapter_id", "")
                if not ADAPTER_ID_RE.match(aid):
                    errors.append(f"{cls_name} L{line_no}: adapter_id {aid!r} fails regex {ADAPTER_ID_RE.pattern}")
                rc = row.get("registry_class", "")
                if rc != cls_name:
                    errors.append(f"{cls_name} L{line_no} {aid}: registry_class {rc!r} != owning file class {cls_name!r}")
                if rc not in REGISTRY_CLASSES:
                    errors.append(f"{cls_name} L{line_no} {aid}: registry_class {rc!r} not in {sorted(REGISTRY_CLASSES)}")
                kind = row.get("adapter_kind", "")
                if kind not in VALID_ADAPTER_KINDS:
                    errors.append(f"{cls_name} L{line_no} {aid}: adapter_kind {kind!r} not in {sorted(VALID_ADAPTER_KINDS)}")
                st = row.get("status", "")
                if st not in VALID_STATUSES:
                    errors.append(f"{cls_name} L{line_no} {aid}: status {st!r} not in {sorted(VALID_STATUSES)}")
                else:
                    class_counts[st] = class_counts.get(st, 0) + 1
                ff = row.get("feature_flag", "")
                if ff not in VALID_FEATURE_FLAGS:
                    errors.append(f"{cls_name} L{line_no} {aid}: feature_flag {ff!r} not in {sorted(VALID_FEATURE_FLAGS)}")
                sp = row.get("linked_sop_path", "")
                if sp and not TODO_MARKER_RE.match(sp):
                    p2 = REPO_ROOT / sp
                    if not p2.exists():
                        warnings.append(f"{cls_name} L{line_no} {aid}: linked_sop_path {sp!r} does not resolve (paired SOP authoring may be deferred per D-IH-72-W)")
                hcb = (row.get("handoff_cost_band") or "").strip()
                if hcb and hcb not in VALID_HANDOFF_COST_BANDS:
                    errors.append(
                        f"{cls_name} L{line_no} {aid}: handoff_cost_band {hcb!r} invalid"
                    )
                vsid = (row.get("value_stream_id") or "").strip()
                if vsid and vsid not in VALID_REVOPS_VALUE_STREAM_IDS:
                    errors.append(
                        f"{cls_name} L{line_no} {aid}: value_stream_id {vsid!r} invalid"
                    )
                if cls_name == "REVOPS":
                    if not hcb:
                        errors.append(f"{cls_name} L{line_no} {aid}: handoff_cost_band required for REVOPS")
                    if not vsid:
                        errors.append(f"{cls_name} L{line_no} {aid}: value_stream_id required for REVOPS")

    print()
    print("  ADAPTER_REGISTRIES Validator")
    print("  =" * 25)
    for cls in sorted(REGISTRY_CLASSES):
        counts = by_class.get(cls, {})
        print(f"  {cls:<14}: {counts}")
    if warnings:
        print()
        print(f"  Warnings: {len(warnings)} (informational; per D-IH-72-W TODO markers + paired SOPs deferred)")
    if errors:
        print()
        print(f"  ERRORS:")
        for e in errors:
            print(f"    - {e}")
        print("  FAIL")
        return 1
    print("  PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
