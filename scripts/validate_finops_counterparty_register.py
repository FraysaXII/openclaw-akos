#!/usr/bin/env python3
"""Validate FINOPS_COUNTERPARTY_REGISTER.csv against org, process_list, registry, optional matrix.

Usage: py scripts/validate_finops_counterparty_register.py
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_finops_counterparty_csv import FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES
from akos.io import REPO_ROOT

HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "compliance"
FINOPS_CSV = HLK_COMPLIANCE / "FINOPS_COUNTERPARTY_REGISTER.csv"
ORG_CSV = HLK_COMPLIANCE / "baseline_organisation.csv"
PROC_CSV = HLK_COMPLIANCE / "process_list.csv"
MATRIX_CSV = HLK_COMPLIANCE / "COMPONENT_SERVICE_MATRIX.csv"
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

COUNTERPARTY_TYPES = {"vendor", "customer", "partner"}
SERVICE_CATEGORIES = {
    "cloud_compute",
    "saas",
    "data_platform",
    "media",
    "legal",
    "payments",
    "productivity",
    "observability",
    "other",
    "na",
}
BILLING_MODELS = {"subscription", "usage", "retainer", "mixed", "na"}
COMMERCIAL_SEGMENTS = {"b2b", "b2c", "nonprofit", "public_sector", "other", "na"}
REVENUE_MODELS = {"subscription", "usage", "mixed", "services", "other", "na"}
STATUS_SET = {"eval", "active", "sunset"}
PCI_SCOPE = {"none", "pii", "pci", "mixed"}
CONFIDENCE_LEVELS = {"1", "2", "3"}

BANNED_HEADER_FRAGMENTS = (
    "amount",
    "price_",
    "_usd",
    "_eur",
    "_gbp",
    "invoice_",
    "cost_total",
    "monthly_spend",
)


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


def load_process_meta() -> tuple[set[str], dict[str, dict[str, str]]]:
    with open(PROC_CSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    ids = {r["item_id"].strip() for r in rows if r.get("item_id")}
    by_id = {r["item_id"].strip(): r for r in rows if r.get("item_id")}
    return ids, by_id


def load_component_ids() -> set[str]:
    if not MATRIX_CSV.is_file():
        return set()
    with open(MATRIX_CSV, encoding="utf-8", newline="") as f:
        return {r["component_id"].strip() for r in csv.DictReader(f) if r.get("component_id")}


def main() -> int:
    print("\n  FINOPS_COUNTERPARTY_REGISTER Validator")
    print("  " + "=" * 40)
    if not FINOPS_CSV.is_file():
        print("  FAIL: FINOPS_COUNTERPARTY_REGISTER.csv not found")
        return 1

    for frag in BANNED_HEADER_FRAGMENTS:
        for h in FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES:
            if frag in h.lower():
                print(f"  FAIL: field name '{h}' contains banned fragment '{frag}'")
                return 1

    org_roles = load_org_roles()
    proc_ids, proc_by_id = load_process_meta()
    reg_slugs = load_registry_slugs()
    comp_ids = load_component_ids()

    errors: list[str] = []
    with open(FINOPS_CSV, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES):
            print("  FAIL: header mismatch")
            print(f"    expected: {list(FINOPS_COUNTERPARTY_REGISTER_FIELDNAMES)}")
            print(f"    got:      {reader.fieldnames}")
            return 1
        rows = list(reader)

    seen: set[str] = set()
    for i, r in enumerate(rows, start=2):
        cid = (r.get("counterparty_id") or "").strip()
        if not cid:
            errors.append(f"row {i}: empty counterparty_id")
            continue
        if cid in seen:
            errors.append(f"row {i}: duplicate counterparty_id {cid}")
        seen.add(cid)
        if not re.match(r"^[a-z0-9][a-z0-9_-]{1,127}$", cid):
            errors.append(f"row {i}: counterparty_id must be slug-like lowercase: {cid!r}")

        ctype = (r.get("counterparty_type") or "").strip()
        if ctype not in COUNTERPARTY_TYPES:
            errors.append(f"row {i}: invalid counterparty_type {ctype!r}")

        cat = (r.get("service_category") or "").strip()
        bm = (r.get("billing_model") or "").strip()
        seg = (r.get("commercial_segment") or "").strip()
        rev = (r.get("revenue_model") or "").strip()

        if ctype in ("vendor", "partner"):
            if cat not in SERVICE_CATEGORIES or cat == "na":
                errors.append(
                    f"row {i}: service_category required for type={ctype} (non-na enum): {cat!r}"
                )
            if bm not in BILLING_MODELS or bm == "na":
                errors.append(
                    f"row {i}: billing_model required for type={ctype} (non-na): {bm!r}"
                )
            if seg != "na":
                errors.append(f"row {i}: commercial_segment must be na for type={ctype}")
            if rev != "na":
                errors.append(f"row {i}: revenue_model must be na for type={ctype}")
        elif ctype == "customer":
            if cat != "na":
                errors.append(f"row {i}: service_category must be na for customer rows")
            if bm != "na":
                errors.append(f"row {i}: billing_model must be na for customer rows")
            if seg not in COMMERCIAL_SEGMENTS or seg == "na":
                errors.append(
                    f"row {i}: commercial_segment required for customer; invalid or na: {seg!r}"
                )
            if rev not in REVENUE_MODELS or rev == "na":
                errors.append(
                    f"row {i}: revenue_model required for customer; invalid or na: {rev!r}"
                )

        role = (r.get("role_owner") or "").strip()
        if role not in org_roles:
            errors.append(f"row {i}: role_owner {role!r} not in baseline_organisation")

        pid = (r.get("process_item_id") or "").strip()
        if pid not in proc_ids:
            errors.append(f"row {i}: process_item_id {pid!r} not in process_list")
        else:
            prow = proc_by_id.get(pid, {})
            if not prow.get("item_id", "").startswith("thi_finan_"):
                errors.append(
                    f"row {i}: process_item_id {pid} should be Finance subtree (thi_finan_*) for this register"
                )

        rs = (r.get("repo_slug") or "").strip()
        if rs and rs not in reg_slugs:
            errors.append(f"row {i}: repo_slug {rs!r} not in REPOSITORIES_REGISTRY")

        comp_id = (r.get("component_id") or "").strip()
        if comp_id:
            if not comp_ids:
                errors.append(f"row {i}: component_id set but COMPONENT_SERVICE_MATRIX.csv missing")
            elif comp_id not in comp_ids:
                errors.append(f"row {i}: component_id {comp_id!r} not in COMPONENT_SERVICE_MATRIX")

        st = (r.get("status") or "").strip()
        if st not in STATUS_SET:
            errors.append(f"row {i}: invalid status {st!r}")

        pci = (r.get("pci_phi_pii_scope") or "").strip()
        if pci not in PCI_SCOPE:
            errors.append(f"row {i}: invalid pci_phi_pii_scope {pci!r}")

        conf = (r.get("confidence_level") or "").strip()
        if conf not in CONFIDENCE_LEVELS:
            errors.append(f"row {i}: confidence_level must be 1, 2, or 3; got {conf!r}")

        pointer = (r.get("contract_doc_pointer") or "").strip()
        if pointer and ".." in pointer:
            errors.append(f"row {i}: contract_doc_pointer must not contain '..'")

        notes = (r.get("notes") or "").lower()
        if re.search(r"\b\d+[.,]\d{2}\s*(usd|eur|gbp|\$)\b", notes):
            errors.append(f"row {i}: notes may not contain currency amounts")

    if errors:
        print(f"  FAIL: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"    - {e}")
        if len(errors) > 25:
            print(f"    ... and {len(errors) - 25} more")
        return 1

    print(f"  Rows validated: {len(rows)}")
    print("  PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
