"""Tests for scripts/probe_compliance_mirror_drift.py (Initiative 23 P4).

Locks in the operator-pasted drift probe contract:
- `--emit-sql` produces a single SELECT block covering all tracked mirrors.
- `count_csv_rows` is correct (header excluded).
- `csv_counts` skips mirrors whose canonical CSV is absent.
- `cmd_verify` SKIPs gracefully (rc=0) when no probe artifact exists.
- `cmd_verify` PASSes when canonical and live counts match across all mirrors.
- `cmd_verify` FAILs when any mirror is in drift.
- Reading malformed JSON yields a clean FAIL, not a Python traceback.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "probe_compliance_mirror_drift.py"


@pytest.fixture(scope="module")
def probe_module():
    spec = importlib.util.spec_from_file_location(
        "probe_compliance_mirror_drift_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["probe_compliance_mirror_drift_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_mirror_contract_covers_expected_tables(probe_module):
    """All currently-shipped compliance mirrors must be in the contract."""
    expected = {
        "compliance.process_list_mirror",
        "compliance.baseline_organisation_mirror",
        "compliance.finops_counterparty_register_mirror",
        "compliance.goipoi_register_mirror",
        "compliance.adviser_engagement_disciplines_mirror",
        "compliance.adviser_open_questions_mirror",
        "compliance.founder_filed_instruments_mirror",
        "compliance.program_registry_mirror",
    }
    actual = {table for table, _csv, _key in probe_module.MIRROR_CONTRACT}
    assert expected == actual, f"contract drift: {expected ^ actual}"


def test_mirror_contract_count_keys_are_unique(probe_module):
    keys = [k for _t, _c, k in probe_module.MIRROR_CONTRACT]
    assert len(keys) == len(set(keys)), "count_keys must be unique"


def test_emit_sql_contains_every_mirror(probe_module):
    sql = probe_module.emit_sql()
    for table, _csv, key in probe_module.MIRROR_CONTRACT:
        assert table in sql, f"{table} missing from emitted SQL"
        assert f"'{key}'" in sql, f"{key} key literal missing"
    assert "UNION ALL" in sql
    assert sql.rstrip().endswith(";")


def test_count_csv_rows_excludes_header(probe_module, tmp_path):
    csv_path = tmp_path / "fake.csv"
    csv_path.write_text("col1,col2\nA,B\nC,D\nE,F\n", encoding="utf-8")
    assert probe_module.count_csv_rows(csv_path) == 3


def test_count_csv_rows_handles_empty(probe_module, tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("col1,col2\n", encoding="utf-8")
    assert probe_module.count_csv_rows(csv_path) == 0


def test_count_csv_rows_handles_missing(probe_module, tmp_path):
    assert probe_module.count_csv_rows(tmp_path / "nope.csv") is None


def test_csv_counts_skips_missing_csv(probe_module, monkeypatch, tmp_path):
    """If a mirror's canonical CSV doesn't exist, that key is excluded from csv_counts."""
    fake_contract = [
        ("compliance.fake_mirror", tmp_path / "missing.csv", "fake_rows"),
    ]
    monkeypatch.setattr(probe_module, "MIRROR_CONTRACT", fake_contract)
    out = probe_module.csv_counts()
    assert out == {}


def test_cmd_verify_skips_when_no_artifact(probe_module, monkeypatch, tmp_path, capsys):
    """No probe artifact present -> exit 0 with operator-runbook pointer (graceful SKIP)."""
    monkeypatch.setattr(probe_module, "ARTIFACTS_DIR", tmp_path / "empty_dir")
    rc = probe_module.cmd_verify(None)
    assert rc == 0
    captured = capsys.readouterr()
    assert "SKIP" in captured.out
    assert "Operator runbook" in captured.out


def test_cmd_verify_passes_when_counts_match(probe_module, monkeypatch, tmp_path, capsys):
    """When live counts equal canonical CSV row counts for every mirror, PASS."""
    csv_path = tmp_path / "alpha.csv"
    csv_path.write_text("col1\na\nb\nc\n", encoding="utf-8")
    monkeypatch.setattr(
        probe_module,
        "MIRROR_CONTRACT",
        [("compliance.alpha_mirror", csv_path, "alpha_rows")],
    )
    artifact = tmp_path / "mirror-drift-test.json"
    artifact.write_text(
        json.dumps([{"table_name": "alpha_rows", "row_count": "3"}]),
        encoding="utf-8",
    )
    rc = probe_module.cmd_verify(artifact)
    captured = capsys.readouterr()
    assert rc == 0, captured.out
    assert "PASS" in captured.out


def test_cmd_verify_fails_on_drift(probe_module, monkeypatch, tmp_path, capsys):
    """When live count diverges from canonical CSV, FAIL (rc=1)."""
    csv_path = tmp_path / "alpha.csv"
    csv_path.write_text("col1\na\nb\nc\nd\n", encoding="utf-8")  # 4 rows
    monkeypatch.setattr(
        probe_module,
        "MIRROR_CONTRACT",
        [("compliance.alpha_mirror", csv_path, "alpha_rows")],
    )
    artifact = tmp_path / "mirror-drift-test.json"
    artifact.write_text(
        json.dumps([{"table_name": "alpha_rows", "row_count": "3"}]),  # live=3, csv=4
        encoding="utf-8",
    )
    rc = probe_module.cmd_verify(artifact)
    captured = capsys.readouterr()
    assert rc == 1
    assert "FAIL" in captured.out
    assert "drift" in captured.out


def test_cmd_verify_handles_malformed_json(probe_module, tmp_path, capsys):
    """Malformed JSON in the probe artifact yields a clean FAIL, not a traceback."""
    artifact = tmp_path / "mirror-drift-test.json"
    artifact.write_text("{ not valid json", encoding="utf-8")
    rc = probe_module.cmd_verify(artifact)
    captured = capsys.readouterr()
    assert rc == 1
    assert "not valid JSON" in captured.out


def test_cmd_verify_rejects_non_array_payload(probe_module, tmp_path, capsys):
    """The probe artifact must be a JSON array; an object rejection is graceful."""
    artifact = tmp_path / "mirror-drift-test.json"
    artifact.write_text(json.dumps({"row_count": 1}), encoding="utf-8")
    rc = probe_module.cmd_verify(artifact)
    captured = capsys.readouterr()
    assert rc == 1
    assert "JSON array" in captured.out


def test_cmd_emit_sql_prints_runbook(probe_module, capsys):
    rc = probe_module.cmd_emit_sql()
    captured = capsys.readouterr()
    assert rc == 0
    assert "execute_sql" in captured.out
    assert "artifacts/probes/mirror-drift-" in captured.out
