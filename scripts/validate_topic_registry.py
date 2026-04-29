#!/usr/bin/env python3
"""Validate `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv`.

Initiative 25 P2 (D-IH-12). Enforces:

- **Header parity** with `TOPIC_REGISTRY_FIELDNAMES`.
- **`topic_id`** unique; matches `^topic_[a-z0-9_]{2,64}$`.
- **`topic_class`**, **`lifecycle_status`**, **`plane`** within enums.
- **`primary_owner_role`** FK-resolves into `baseline_organisation.csv`.
- **`program_id`** is `shared` OR resolves into `PROGRAM_REGISTRY.csv`.
- **`manifest_path`** resolves to an existing file (when non-empty).
- **Cycle detection** on `parent_topic` (single-edge tree) and `depends_on`
  (DAG) via DFS.
- **Forward-reference policy**: every `topic_id` referenced in
  `parent_topic`, `related_topics`, `depends_on`, `subsumes`, `subsumed_by`
  must resolve to a row in the same file.

Exits 0 on PASS, 1 on FAIL. Hooked into `scripts/validate_hlk.py` after
`validate_program_id_consistency.py`. SKIPs gracefully when the registry
is absent.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_topic_registry_csv import TOPIC_REGISTRY_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
TOPIC_REGISTRY_CSV = HLK_COMPLIANCE / "dimensions" / "TOPIC_REGISTRY.csv"
PROGRAM_REGISTRY_CSV = HLK_COMPLIANCE / "dimensions" / "PROGRAM_REGISTRY.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"

TOPIC_CLASSES = {
    "process_map",
    "architecture",
    "wireframe",
    "methodology_map",
    "manifesto",
    "evidence_pack",
    "brand_asset",
    "other",
}
LIFECYCLE_STATUS = {"proposed", "active", "paused", "closed", "superseded"}
PLANES = {"advops", "finops", "mktops", "techops", "marops", "devops", "ops", "shared"}

TOPIC_ID_RE = re.compile(r"^topic_[a-z0-9_]{2,64}$")


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {row["role_name"].strip() for row in csv.DictReader(f) if row.get("role_name")}


def load_program_ids() -> set[str]:
    if not PROGRAM_REGISTRY_CSV.is_file():
        return set()
    with open(PROGRAM_REGISTRY_CSV, encoding="utf-8", newline="") as f:
        return {row["program_id"].strip() for row in csv.DictReader(f) if row.get("program_id")}


def split_semicolon_list(value: str) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(";") if part.strip()]


def detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """DFS-based cycle detection. Returns the cycle path if found, else None."""
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
    print("\n  TOPIC_REGISTRY Validator")
    print("  " + "=" * 40)
    if not TOPIC_REGISTRY_CSV.is_file():
        print("  SKIP: TOPIC_REGISTRY.csv not found (Initiative 25 not yet shipped)")
        return 0

    org_roles = load_org_roles()
    program_ids = load_program_ids()

    errors: list[str] = []
    with open(TOPIC_REGISTRY_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(TOPIC_REGISTRY_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(TOPIC_REGISTRY_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    topic_ids: set[str] = set()
    for i, row in enumerate(rows, start=2):
        tid = (row.get("topic_id") or "").strip()
        if not tid:
            errors.append(f"row {i}: empty topic_id")
            continue
        if not TOPIC_ID_RE.match(tid):
            errors.append(f"row {i}: topic_id must match ^topic_[a-z0-9_]{{2,64}}$: {tid!r}")
        if tid in topic_ids:
            errors.append(f"row {i}: duplicate topic_id {tid}")
        topic_ids.add(tid)

        title = (row.get("title") or "").strip()
        if not title:
            errors.append(f"row {i}: empty title")

        klass = (row.get("topic_class") or "").strip()
        if klass not in TOPIC_CLASSES:
            errors.append(f"row {i}: invalid topic_class {klass!r}; expected one of {sorted(TOPIC_CLASSES)}")

        lifecycle = (row.get("lifecycle_status") or "").strip()
        if lifecycle not in LIFECYCLE_STATUS:
            errors.append(f"row {i}: invalid lifecycle_status {lifecycle!r}")

        plane = (row.get("plane") or "").strip()
        if plane not in PLANES:
            errors.append(f"row {i}: invalid plane {plane!r}")

        owner = (row.get("primary_owner_role") or "").strip()
        if not owner:
            errors.append(f"row {i}: empty primary_owner_role")
        elif owner not in org_roles:
            errors.append(f"row {i}: primary_owner_role {owner!r} not in baseline_organisation.csv")

        prog = (row.get("program_id") or "").strip()
        if not prog:
            errors.append(f"row {i}: empty program_id (use 'shared' for cross-program topics)")
        elif prog != "shared" and prog not in program_ids:
            errors.append(f"row {i}: program_id {prog!r} not in PROGRAM_REGISTRY.csv (and not 'shared')")

        manifest = (row.get("manifest_path") or "").strip()
        if manifest:
            if ".." in manifest:
                errors.append(f"row {i}: manifest_path must not contain '..': {manifest!r}")
            elif not (REPO_ROOT / manifest).is_file():
                errors.append(f"row {i}: manifest_path does not resolve to an existing file: {manifest!r}")

    # Forward references + cycles
    parent_graph: dict[str, list[str]] = {tid: [] for tid in topic_ids}
    depends_graph: dict[str, list[str]] = {tid: [] for tid in topic_ids}
    for i, row in enumerate(rows, start=2):
        tid = (row.get("topic_id") or "").strip()
        if not tid:
            continue
        for ref_field, target_graph in (
            ("parent_topic", parent_graph),
            ("related_topics", None),
            ("depends_on", depends_graph),
            ("subsumes", None),
            ("subsumed_by", None),
        ):
            value = (row.get(ref_field) or "").strip()
            if ref_field == "parent_topic":
                refs = [value] if value else []
            else:
                refs = split_semicolon_list(value)
            for ref in refs:
                if ref not in topic_ids:
                    errors.append(
                        f"row {i}: {ref_field} references unknown topic_id {ref!r}"
                    )
                if target_graph is not None and ref in topic_ids:
                    target_graph[tid].append(ref)

    parent_cycle = detect_cycle(parent_graph)
    if parent_cycle:
        errors.append(f"parent_topic forms a cycle: {' -> '.join(parent_cycle)}")
    depends_cycle = detect_cycle(depends_graph)
    if depends_cycle:
        errors.append(f"depends_on forms a cycle: {' -> '.join(depends_cycle)}")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print(f"  Topics:         {len(topic_ids)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
