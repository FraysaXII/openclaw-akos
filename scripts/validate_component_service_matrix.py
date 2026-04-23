#!/usr/bin/env python3
"""Validate COMPONENT_SERVICE_MATRIX.csv against org, process_list, and REPOSITORIES_REGISTRY.

Usage: py scripts/validate_component_service_matrix.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_component_service_csv import COMPONENT_SERVICE_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
MATRIX_CSV = HLK_COMPLIANCE / "COMPONENT_SERVICE_MATRIX.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
PROC_CSV = HLK_COMPLIANCE / "process_list.csv"
REGISTRY_MD = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Envoy Tech Lab"
    / "Repositories"
    / "REPOSITORIES_REGISTRY.md"
)

COMPONENT_KINDS = {
    "repository",
    "saas",
    "data_platform",
    "integration",
    "edge_function",
    "library",
    "infrastructure",
    "observability",
    "client_runtime",
    "other",
}
LIFECYCLE = {"experimental", "active", "constrained", "sunset", "retired"}
STEWARD = {
    "MAROPS",
    "DEVOPS",
    "DATAOPS",
    "PMSMO",
    "LEGOPS",
    "FINOPS",
    "GTMOPS",
    "SECOPS",
    "other",
}
API_EXPOSURE = {"none", "internal", "partner", "public"}
INTEGRATION = {"push", "pull", "batch", "stream", "event", "manual", "n_a"}
DATA_CLASS = {"public", "internal", "confidential", "restricted", ""}
ENV_SCOPE = {"dev", "staging", "prod", "multi", "local_only"}
SLO_TIER = {"best_effort", "standard", "critical"}
LEGAL = {"y", "n", ""}


def load_registry_slugs() -> set[str]:
    text = REGISTRY_MD.read_text(encoding="utf-8")
    slugs: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|--"):
            continue
        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p]
        if len(parts) < 2:
            continue
        slug = parts[0]
        if slug in ("repo_slug", "-----------"):
            continue
        if re.match(r"^[\w.-]+$", slug):
            slugs.add(slug)
    return slugs


def load_org_roles() -> set[str]:
    with open(ORG_CSV, encoding="utf-8", newline="") as f:
        return {r["role_name"].strip() for r in csv.DictReader(f) if r.get("role_name")}


def load_process_ids() -> set[str]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        return {r["item_id"].strip() for r in csv.DictReader(f) if r.get("item_id")}


def pipe_ids(s: str) -> list[str]:
    s = (s or "").strip()
    if not s:
        return []
    return [x.strip() for x in s.split("|") if x.strip()]


def main() -> int:
    print("\n  COMPONENT_SERVICE_MATRIX Validator")
    print("  " + "=" * 40)
    if not MATRIX_CSV.is_file():
        print("  FAIL: COMPONENT_SERVICE_MATRIX.csv not found")
        return 1

    org_roles = load_org_roles()
    proc_ids = load_process_ids()
    reg_slugs = load_registry_slugs()

    with open(MATRIX_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COMPONENT_SERVICE_FIELDNAMES:
            print("  FAIL: header mismatch")
            print(f"    expected: {COMPONENT_SERVICE_FIELDNAMES}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    errors: list[str] = []
    seen_ids: dict[str, int] = {}
    seen_names: dict[str, int] = {}

    all_component_ids = {r.get("component_id", "").strip() for r in rows if r.get("component_id")}

    for i, row in enumerate(rows, start=2):
        cid = (row.get("component_id") or "").strip()
        cname = (row.get("component_name") or "").strip()
        if not cid:
            errors.append(f"row {i}: empty component_id")
            continue
        seen_ids[cid] = seen_ids.get(cid, 0) + 1
        if cname:
            seen_names[cname] = seen_names.get(cname, 0) + 1

        kind = (row.get("component_kind") or "").strip()
        if kind and kind not in COMPONENT_KINDS:
            errors.append(f"row {i} {cid}: invalid component_kind {kind!r}")

        ls = (row.get("lifecycle_status") or "").strip()
        if ls and ls not in LIFECYCLE:
            errors.append(f"row {i} {cid}: invalid lifecycle_status {ls!r}")

        sod = (row.get("steward_ops_domain") or "").strip()
        if sod and sod not in STEWARD:
            errors.append(f"row {i} {cid}: invalid steward_ops_domain {sod!r}")

        for col in ("primary_owner_role", "secondary_owner_role", "escalation_owner_role"):
            v = (row.get(col) or "").strip()
            if v and v not in org_roles:
                errors.append(f"row {i} {cid}: {col} {v!r} not in baseline_organisation")

        rs = (row.get("repo_slug") or "").strip()
        if rs and rs not in reg_slugs:
            errors.append(f"row {i} {cid}: repo_slug {rs!r} not in REPOSITORIES_REGISTRY.md")

        ae = (row.get("api_exposure") or "").strip()
        if ae and ae not in API_EXPOSURE:
            errors.append(f"row {i} {cid}: invalid api_exposure {ae!r}")

        ip = (row.get("integration_pattern") or "").strip()
        if ip and ip not in INTEGRATION:
            errors.append(f"row {i} {cid}: invalid integration_pattern {ip!r}")

        dc = (row.get("data_classification") or "").strip()
        if dc not in DATA_CLASS:
            errors.append(f"row {i} {cid}: invalid data_classification {dc!r}")

        es = (row.get("environment_scope") or "").strip()
        if es and es not in ENV_SCOPE:
            errors.append(f"row {i} {cid}: invalid environment_scope {es!r}")

        st = (row.get("slo_tier") or "").strip()
        if st and st not in SLO_TIER:
            errors.append(f"row {i} {cid}: invalid slo_tier {st!r}")

        lh = (row.get("legal_hold") or "").strip().lower()
        if lh not in LEGAL:
            errors.append(f"row {i} {cid}: invalid legal_hold {lh!r}")

        al = (row.get("access_level_data") or "").strip()
        if al:
            try:
                n = int(al)
                if n < 0 or n > 6:
                    errors.append(f"row {i} {cid}: access_level_data must be 0-6")
            except ValueError:
                errors.append(f"row {i} {cid}: access_level_data not int")

        pid = (row.get("primary_process_item_id") or "").strip()
        if pid and pid not in proc_ids:
            errors.append(f"row {i} {cid}: primary_process_item_id {pid!r} not in process_list")

        for x in pipe_ids(row.get("related_process_item_ids", "")):
            if x not in proc_ids:
                errors.append(f"row {i} {cid}: related_process_item_id {x!r} not in process_list")

        pc = (row.get("parent_component_id") or "").strip()
        if pc and pc not in all_component_ids:
            errors.append(f"row {i} {cid}: parent_component_id {pc!r} not found (ordering?)")

        for d in pipe_ids(row.get("depends_on_component_ids", "")):
            if d not in all_component_ids:
                errors.append(f"row {i} {cid}: depends_on_component_ids references missing {d!r}")

    for cid, c in seen_ids.items():
        if c > 1:
            errors.append(f"duplicate component_id {cid!r} ({c} times)")
    for cname, c in seen_names.items():
        if c > 1:
            errors.append(f"duplicate component_name {cname!r} ({c} times)")

    if errors:
        print("  FAIL")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        print(f"\n  Total: {len(errors)} errors")
        return 1

    print(f"  PASS ({len(rows)} components)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
