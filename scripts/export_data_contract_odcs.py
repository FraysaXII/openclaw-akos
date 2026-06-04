#!/usr/bin/env python3
"""Export DATA_CONTRACT_REGISTRY.csv rows to ODCS v3.1 YAML (I93 P3).

Git CSV remains SSOT; output is a **read-oriented projection** for OpenMetadata
import/validate (see DATA_CATALOG_INTEGRATION_POSTURE.md).

Usage::

    py scripts/export_data_contract_odcs.py --self-test
    py scripts/export_data_contract_odcs.py --output-dir build/odcs-contracts
    py scripts/export_data_contract_odcs.py --stdout
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_data_contract_csv import CSV_PATH_RELATIVE, DataContractRegistryRow  # noqa: E402
from akos.hlk_data_contract_odcs import contract_row_to_odcs, validate_odcs_document  # noqa: E402

CSV_PATH = REPO_ROOT / CSV_PATH_RELATIVE


def _load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _dump_yaml(doc: dict) -> str:
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("PyYAML required for ODCS export (pip install pyyaml)") from exc
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)


def run_self_test() -> int:
    sample = {
        "contract_id": "DC-HOL-SELF-TEST-001",
        "producer_process_id": "env_tech_dtp_dataops_quality_001",
        "producer_area": "Tech",
        "consumer_area_ids": "Data",
        "data_surface": "mirror_table",
        "schema_ref": "compliance.example_mirror",
        "semantics_ref": "self-test",
        "sla_freshness": "24h",
        "sla_availability": "99%",
        "quality_rules": "DATA-01;DATA-02",
        "classification": "internal",
        "retention_policy_ref": "",
        "version": "0.0.1",
        "status": "draft",
        "owner_role": "Data Steward",
        "last_review_at": "2026-06-04",
        "last_review_by": "Data Governance Lead",
        "last_review_decision_id": "D-IH-93-D",
        "methodology_version_at_review": "v3.1",
        "notes": "self-test",
    }
    doc = contract_row_to_odcs(sample)
    errors = validate_odcs_document(doc)
    if errors:
        print("FAIL self-test:", errors)
        return 1
    yaml_text = _dump_yaml(doc)
    if "apiVersion: v3.1.0" not in yaml_text:
        print("FAIL self-test: missing apiVersion in YAML output")
        return 1
    print("PASS self-test (ODCS v3.1 YAML structure)")
    return 0


def export_rows(output_dir: Path | None, stdout: bool, as_json: bool) -> int:
    rows = _load_rows()
    if not rows:
        print("WARN: no contract rows")
        return 0

    errors: list[str] = []
    documents: list[dict] = []
    for row in rows:
        doc = contract_row_to_odcs(row)
        doc_errors = validate_odcs_document(doc)
        if doc_errors:
            errors.extend(f"{row.get('contract_id')}: {e}" for e in doc_errors)
            continue
        documents.append(doc)

    if errors:
        print("FAIL export validation:")
        for err in errors:
            print(f"  - {err}")
        return 1

    if as_json:
        print(json.dumps(documents, indent=2))
        return 0

    if stdout:
        for doc in documents:
            print("---")
            print(_dump_yaml(doc))
        return 0

    assert output_dir is not None
    output_dir.mkdir(parents=True, exist_ok=True)
    for doc in documents:
        cid = doc["id"]
        path = output_dir / f"{cid.lower()}.odcs.yaml"
        path.write_text(_dump_yaml(doc), encoding="utf-8")
    print(f"PASS exported {len(documents)} ODCS contract(s) to {output_dir.relative_to(REPO_ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Export data contracts to ODCS v3.1 YAML")
    parser.add_argument("--self-test", action="store_true", help="Run structural self-test")
    parser.add_argument("--output-dir", type=Path, help="Write one YAML file per contract_id")
    parser.add_argument("--stdout", action="store_true", help="Print YAML documents to stdout")
    parser.add_argument("--json", action="store_true", help="Print JSON array to stdout")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.json or args.stdout:
        return export_rows(None, stdout=args.stdout, as_json=args.json)
    if args.output_dir:
        return export_rows(args.output_dir, stdout=False, as_json=False)
    parser.error("Specify --self-test, --stdout, --json, or --output-dir")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
