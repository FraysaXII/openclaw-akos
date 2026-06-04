"""Tests for ODCS export from DATA_CONTRACT_REGISTRY (I93 P3)."""

from __future__ import annotations

import csv
from pathlib import Path

from akos.hlk_data_contract_csv import CSV_PATH_RELATIVE
from akos.hlk_data_contract_odcs import (
    ODCS_API_VERSION,
    contract_row_to_odcs,
    validate_odcs_document,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / CSV_PATH_RELATIVE


def test_contract_row_to_odcs_seed_structure() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        row = next(csv.DictReader(fh))
    doc = contract_row_to_odcs(row)
    assert doc["apiVersion"] == ODCS_API_VERSION
    assert doc["id"] == row["contract_id"]
    assert doc["servers"]["production"]["environment"] == row["data_surface"]
    assert validate_odcs_document(doc) == []


def test_export_all_seed_contracts_valid() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 4
    for row in rows:
        errors = validate_odcs_document(contract_row_to_odcs(row))
        assert errors == [], f"{row['contract_id']}: {errors}"


def test_export_script_self_test() -> None:
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/export_data_contract_odcs.py", "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
