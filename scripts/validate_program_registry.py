#!/usr/bin/env python3
"""Validate `docs/references/hlk/compliance/dimensions/PROGRAM_REGISTRY.csv`.

Initiative 23 P1 (D-IH-8 + D-IH-9). Enforces:

- **Header parity** with `PROGRAM_REGISTRY_FIELDNAMES`.
- **`program_id`** matches `^PRJ-HOL-[A-Z0-9-]+-\\d{4}$` and is unique.
- **`program_code`** matches `^[A-Z]{3}$` and is unique.
- **`lifecycle_status`**, **`risk_class`**, **`default_plane`** are within enums.
- **Date format**: `start_date` and `target_close_date` are ISO `YYYY-MM-DD`
  or one of `{open, unknown}`.
- **`process_item_id`** (when non-empty) FK-resolves into `process_list.csv`
  `item_id` of `item_granularity = project`.
- **`primary_owner_role`** FK-resolves into `baseline_organisation.csv` `role_name`.
- **Forward-reference policy (STRICT)**: every `program_id` referenced in
  `parent_program_id`, `consumes_program_ids`, `produces_for_program_ids`,
  `subsumes_program_ids` must resolve to a row in the same file. The flag
  `--allow-forward-references=ID1;ID2` is a single-commit escape hatch.
- **Cycle detection** on `parent_program_id` (single-edge tree) and
  `consumes_program_ids` (DAG) via DFS.

Usage:

    py scripts/validate_program_registry.py
    py scripts/validate_program_registry.py --allow-forward-references=PRJ-HOL-X-2026

Exits 0 on PASS, 1 on FAIL. Hooked into `scripts/validate_hlk.py` when the
file exists.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_program_registry_csv import PROGRAM_REGISTRY_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
PROGRAM_REGISTRY_CSV = HLK_COMPLIANCE / "dimensions" / "PROGRAM_REGISTRY.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
PROC_CSV = HLK_COMPLIANCE / "process_list.csv"

LIFECYCLE_STATUS = {"proposed", "active", "paused", "closed", "superseded"}
RISK_CLASS = {"low", "medium", "high", "critical"}
DEFAULT_PLANE = {"advops", "finops", "mktops", "techops", "marops", "devops", "ops"}

PROGRAM_ID_RE = re.compile(r"^PRJ-HOL-[A-Z0-9-]+-\d{4}$")
PROGRAM_CODE_RE = re.compile(r"^[A-Z]{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SPECIAL_DATES = {"open", "unknown"}


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {row["role_name"].strip() for row in csv.DictReader(f) if row.get("role_name")}


def load_project_item_ids() -> set[str]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return {
            row["item_id"].strip()
            for row in csv.DictReader(f)
            if row.get("item_granularity", "").strip() == "project" and row.get("item_id")
        }


def split_semicolon_list(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """Return a cycle path if one exists, else None. DFS with three-color marking."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in graph}
    parent: dict[str, str | None] = {n: None for n in graph}

    def dfs(start: str) -> list[str] | None:
        stack: list[tuple[str, int]] = [(start, 0)]
        color[start] = GRAY
        while stack:
            node, idx = stack.pop()
            neighbors = graph.get(node, [])
            if idx >= len(neighbors):
                color[node] = BLACK
                continue
            stack.append((node, idx + 1))
            neighbor = neighbors[idx]
            if neighbor not in color:
                continue
            if color[neighbor] == GRAY:
                cycle = [neighbor, node]
                cur = parent.get(node)
                while cur and cur != neighbor:
                    cycle.append(cur)
                    cur = parent.get(cur)
                if cur == neighbor:
                    cycle.append(neighbor)
                cycle.reverse()
                return cycle
            if color[neighbor] == WHITE:
                color[neighbor] = GRAY
                parent[neighbor] = node
                stack.append((neighbor, 0))
        return None

    for node in graph:
        if color[node] == WHITE:
            cycle = dfs(node)
            if cycle is not None:
                return cycle
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--allow-forward-references",
        type=str,
        default="",
        help="Semicolon list of program_ids exempt from forward-reference check (single-commit escape hatch)",
    )
    args = parser.parse_args()

    print("\n  PROGRAM_REGISTRY Validator")
    print("  " + "=" * 40)
    if not PROGRAM_REGISTRY_CSV.is_file():
        print("  SKIP: PROGRAM_REGISTRY.csv not found (Initiative 23 not yet shipped)")
        return 0

    org_roles = load_org_roles()
    proj_ids = load_project_item_ids()
    allow_forward = {x.strip() for x in args.allow_forward_references.split(";") if x.strip()}
    if allow_forward:
        print(f"  WARNING: --allow-forward-references in use for {sorted(allow_forward)}")
        print("           This is a single-commit escape hatch; the next commit MUST clear it.")

    errors: list[str] = []
    with open(PROGRAM_REGISTRY_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(PROGRAM_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(PROGRAM_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    program_ids: set[str] = set()
    program_codes: set[str] = set()
    for i, row in enumerate(rows, start=2):
        pid = (row.get("program_id") or "").strip()
        if not pid:
            errors.append(f"row {i}: empty program_id")
            continue
        if not PROGRAM_ID_RE.match(pid):
            errors.append(f"row {i}: program_id must match PRJ-HOL-<TOPIC>-<YYYY>: {pid!r}")
        if pid in program_ids:
            errors.append(f"row {i}: duplicate program_id {pid}")
        program_ids.add(pid)

        code = (row.get("program_code") or "").strip()
        if not PROGRAM_CODE_RE.match(code):
            errors.append(f"row {i}: program_code must match ^[A-Z]{{3}}$: {code!r}")
        if code in program_codes:
            errors.append(f"row {i}: duplicate program_code {code}")
        program_codes.add(code)

        lifecycle = (row.get("lifecycle_status") or "").strip()
        if lifecycle not in LIFECYCLE_STATUS:
            errors.append(f"row {i}: invalid lifecycle_status {lifecycle!r}; expected one of {sorted(LIFECYCLE_STATUS)}")

        risk = (row.get("risk_class") or "").strip()
        if risk not in RISK_CLASS:
            errors.append(f"row {i}: invalid risk_class {risk!r}; expected one of {sorted(RISK_CLASS)}")

        plane = (row.get("default_plane") or "").strip()
        if plane not in DEFAULT_PLANE:
            errors.append(f"row {i}: invalid default_plane {plane!r}; expected one of {sorted(DEFAULT_PLANE)}")

        for date_field in ("start_date", "target_close_date"):
            value = (row.get(date_field) or "").strip()
            if not value:
                errors.append(f"row {i}: empty {date_field}")
            elif value not in SPECIAL_DATES and not DATE_RE.match(value):
                errors.append(
                    f"row {i}: {date_field} must be ISO YYYY-MM-DD or one of {sorted(SPECIAL_DATES)}: {value!r}"
                )

        item_id = (row.get("process_item_id") or "").strip()
        if item_id and item_id not in proj_ids:
            errors.append(
                f"row {i}: process_item_id {item_id!r} not in process_list.csv item_granularity=project rows"
            )

        owner = (row.get("primary_owner_role") or "").strip()
        if not owner:
            errors.append(f"row {i}: empty primary_owner_role")
        elif owner not in org_roles:
            errors.append(f"row {i}: primary_owner_role {owner!r} not in baseline_organisation.csv")

    # Forward-reference policy + cycle detection
    parent_graph: dict[str, list[str]] = {pid: [] for pid in program_ids}
    consumes_graph: dict[str, list[str]] = {pid: [] for pid in program_ids}
    for i, row in enumerate(rows, start=2):
        pid = (row.get("program_id") or "").strip()
        if not pid:
            continue
        for ref_field, target_graph in (
            ("parent_program_id", parent_graph),
            ("consumes_program_ids", consumes_graph),
            ("produces_for_program_ids", None),
            ("subsumes_program_ids", None),
        ):
            value = (row.get(ref_field) or "").strip()
            refs = split_semicolon_list(value) if ref_field != "parent_program_id" else ([value] if value else [])
            for ref in refs:
                if ref not in program_ids and ref not in allow_forward:
                    errors.append(
                        f"row {i}: {ref_field} references unknown program_id {ref!r} "
                        f"(not in registry; not in --allow-forward-references)"
                    )
                if target_graph is not None and ref in program_ids:
                    target_graph[pid].append(ref)

    parent_cycle = detect_cycle(parent_graph)
    if parent_cycle:
        errors.append(f"parent_program_id forms a cycle: {' -> '.join(parent_cycle)}")
    consumes_cycle = detect_cycle(consumes_graph)
    if consumes_cycle:
        errors.append(f"consumes_program_ids forms a cycle: {' -> '.join(consumes_cycle)}")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Programs:       {len(program_ids)}")
    print(f"  Codes unique:   {len(program_codes)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
