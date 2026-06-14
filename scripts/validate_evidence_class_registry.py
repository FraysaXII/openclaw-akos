#!/usr/bin/env python3
"""Validate EVIDENCE_CLASS_REGISTRY.csv + PROOF_ADAPTER_REGISTRY.csv (I90 P4c)."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.evidence_class_gate import CORE_EVIDENCE_CLASSES  # noqa: E402
from akos.hlk_evidence_class_registry import (  # noqa: E402
    DEPRECATED_EVIDENCE_CLASS_REGISTRY_PATHS,
    EVIDENCE_CLASS_REGISTRY_CSV_RELATIVE,
    EVIDENCE_CLASS_REGISTRY_FIELDNAMES,
    PROOF_ADAPTER_REGISTRY_CSV_RELATIVE,
    PROOF_ADAPTER_REGISTRY_FIELDNAMES,
    VALID_ADAPTER_STATUSES,
    VALID_BINDING_STATUSES,
    VALID_SEVERITIES,
    EvidenceClassRegistryRow,
    ProofAdapterRegistryRow,
)
from pydantic import ValidationError


def validate(repo_root: Path | None = None) -> tuple[bool, list[str], list[str]]:
    root = repo_root or REPO_ROOT
    errors: list[str] = []
    warnings: list[str] = []
    for rel in DEPRECATED_EVIDENCE_CLASS_REGISTRY_PATHS:
        if (root / rel).is_file():
            warnings.append(f"deprecated SSOT copy still present: {rel} (remove; see PATH_ALIAS_EVIDENCE_REGISTRIES.md)")
    ecb_path = root / EVIDENCE_CLASS_REGISTRY_CSV_RELATIVE
    pad_path = root / PROOF_ADAPTER_REGISTRY_CSV_RELATIVE

    adapter_ids: set[str] = set()
    adapter_classes: dict[str, str] = {}
    if pad_path.is_file():
        with pad_path.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            if tuple(reader.fieldnames or ()) != PROOF_ADAPTER_REGISTRY_FIELDNAMES:
                errors.append(f"PROOF_ADAPTER_REGISTRY header mismatch: {reader.fieldnames}")
                return False, errors, warnings
            for idx, raw in enumerate(reader, start=2):
                try:
                    ProofAdapterRegistryRow(**raw)
                except ValidationError as exc:
                    errors.append(f"PROOF_ADAPTER L{idx}: {exc}")
                    continue
                aid = raw["adapter_id"]
                if aid in adapter_ids:
                    errors.append(f"PROOF_ADAPTER L{idx}: duplicate {aid}")
                adapter_ids.add(aid)
                if raw["status"] not in VALID_ADAPTER_STATUSES:
                    errors.append(f"PROOF_ADAPTER L{idx}: invalid status {raw['status']!r}")
                runbook = root / raw["runbook_path"]
                if raw["status"] == "active" and not runbook.is_file():
                    errors.append(
                        f"PROOF_ADAPTER L{idx}: active adapter {aid} missing runbook {raw['runbook_path']}"
                    )
                adapter_classes[aid] = raw["evidence_class"]

    if not ecb_path.is_file():
        return False, [f"missing {ECB_PATH_display(ecb_path)}"], warnings

    seen_bindings: set[str] = set()
    with ecb_path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != EVIDENCE_CLASS_REGISTRY_FIELDNAMES:
            errors.append(f"EVIDENCE_CLASS_REGISTRY header mismatch: {reader.fieldnames}")
            return False, errors, warnings
        for idx, raw in enumerate(reader, start=2):
            try:
                EvidenceClassRegistryRow(**raw)
            except ValidationError as exc:
                errors.append(f"EVIDENCE_CLASS L{idx}: {exc}")
                continue
            bid = raw["binding_id"]
            if bid in seen_bindings:
                errors.append(f"EVIDENCE_CLASS L{idx}: duplicate {bid}")
            seen_bindings.add(bid)
            if raw["severity"] not in VALID_SEVERITIES:
                errors.append(f"EVIDENCE_CLASS L{idx}: invalid severity {raw['severity']!r}")
            if raw["status"] not in VALID_BINDING_STATUSES:
                errors.append(f"EVIDENCE_CLASS L{idx}: invalid status {raw['status']!r}")
            ec = raw["evidence_class"]
            if ec not in CORE_EVIDENCE_CLASSES and raw["status"] == "active":
                # extension class must appear on an adapter row
                if ec not in adapter_classes.values():
                    errors.append(
                        f"EVIDENCE_CLASS L{idx}: active extension class {ec!r} "
                        "missing PROOF_ADAPTER_REGISTRY row"
                    )
            pad = (raw.get("proof_adapter_id") or "").strip()
            if pad and pad not in adapter_ids:
                errors.append(f"EVIDENCE_CLASS L{idx}: proof_adapter_id {pad!r} unresolved")
            vscript = root / raw["validator_script"]
            if raw["status"] == "active" and not vscript.is_file():
                errors.append(
                    f"EVIDENCE_CLASS L{idx}: active binding missing validator {raw['validator_script']}"
                )

    return not errors, errors, warnings


def ECB_PATH_display(p: Path) -> str:
    try:
        return p.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(p)


def self_test() -> int:
    ok, errors, warnings = validate()
    for w in warnings:
        print(f"WARN: {w}")
    if not ok:
        print("FAIL: evidence-class registry self-test")
        for e in errors[:20]:
            print(f"  - {e}")
        return 1
    classes = __import__("akos.evidence_class_gate", fromlist=["load_valid_evidence_classes"]).load_valid_evidence_classes()
    assert "ux_lighthouse_audit" in classes
    print(f"PASS: evidence-class registry ({len(classes)} evidence classes)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    ok, errors, warnings = validate()
    for w in warnings:
        print(f"WARN: {w}")
    if ok:
        print("PASS: validate_evidence_class_registry")
        return 0
    print(f"FAIL: validate_evidence_class_registry ({len(errors)} errors)")
    for e in errors[:30]:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
