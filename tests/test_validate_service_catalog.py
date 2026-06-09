"""Tests for SERVICE_CATALOG.csv + validate_service_catalog (P95-GOV-4)."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_service_catalog_csv import (  # noqa: E402
    SERVICE_CATALOG_FIELDNAMES,
    ServiceCatalogRow,
)

CSV_PATH = (
    REPO_ROOT
    / "docs/references/hlk/v3.0/Admin/O5-1/Operations/SMO/canonicals/SERVICE_CATALOG.csv"
)
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_service_catalog.py"


def test_header_matches_fieldnames_tuple() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        assert list(csv.DictReader(fh).fieldnames or []) == list(SERVICE_CATALOG_FIELDNAMES)


def test_canonical_rows_pydantic_validate() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            ServiceCatalogRow.model_validate({k: (v or "") for k, v in row.items()})


def test_invalid_service_id_rejected() -> None:
    sample = {
        "service_id": "INVALID",
        "name": "Example",
        "customer_facing_description": "Desc",
        "delivery_role_primary": "SMO",
        "delivery_role_secondary": "",
        "cost_model": "Forfait",
        "sla_tier": "Tier 2 (Standard)",
        "active_engagements": "x",
        "status": "active",
        "notes": "",
    }
    with pytest.raises(ValidationError):
        ServiceCatalogRow.model_validate(sample)


def test_validator_script_passes_on_canonical_csv() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_validator_self_test() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
