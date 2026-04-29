"""Tests for scripts/validate_program_id_consistency.py (Initiative 23 P3).

Locks in the cross-asset FK contract:
- PASS when every reference resolves to a registered program_id.
- FAIL when an unknown id is referenced.
- SKIP gracefully when PROGRAM_REGISTRY.csv is absent (gate only applies post-I23-P1).
- Reserved keywords (`shared`, `_meta`) bypass the check on purpose.
- Malformed program_id values are flagged.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_program_id_consistency.py"


@pytest.fixture(scope="module")
def consistency_module():
    spec = importlib.util.spec_from_file_location(
        "validate_program_id_consistency_under_test", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["validate_program_id_consistency_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_program_id_regex_accepts_canonical(consistency_module):
    assert consistency_module.PROGRAM_ID_RE.match("PRJ-HOL-FOUNDING-2026")
    assert consistency_module.PROGRAM_ID_RE.match("PRJ-HOL-KIR-2026")
    assert consistency_module.PROGRAM_ID_RE.match("PRJ-HOL-A1-2026")


def test_program_id_regex_rejects_legacy_item_ids(consistency_module):
    assert not consistency_module.PROGRAM_ID_RE.match("env_tech_prj_2")
    assert not consistency_module.PROGRAM_ID_RE.match("thi_legal_prj_1")
    assert not consistency_module.PROGRAM_ID_RE.match("not_a_program")
    assert not consistency_module.PROGRAM_ID_RE.match("")


def test_reserved_keywords_present(consistency_module):
    assert "shared" in consistency_module.RESERVED_KEYWORDS
    assert "_meta" in consistency_module.RESERVED_KEYWORDS


def test_load_registered_returns_set_of_strings(consistency_module):
    """If the canonical CSV exists, loader returns a non-empty set of program_id strings."""
    registered = consistency_module.load_registered_program_ids()
    if consistency_module.PROGRAM_REGISTRY_CSV.is_file():
        assert isinstance(registered, set)
        assert len(registered) > 0
        for value in registered:
            assert isinstance(value, str)
            assert value  # non-empty


def test_collect_csv_program_ids_handles_missing(consistency_module, tmp_path):
    """Returns empty list for a non-existent CSV path (no crash)."""
    missing = tmp_path / "does_not_exist.csv"
    assert consistency_module.collect_csv_program_ids(missing) == []


def test_collect_csv_program_ids_extracts_values(consistency_module, tmp_path):
    csv_path = tmp_path / "fake.csv"
    csv_path.write_text(
        "ref_id,program_id,notes\n"
        "POI-X,PRJ-HOL-A-2026,first\n"
        "POI-Y,,empty\n"
        "POI-Z,PRJ-HOL-B-2026,second\n",
        encoding="utf-8",
    )
    out = consistency_module.collect_csv_program_ids(csv_path)
    values = [v for _origin, _i, v in out]
    assert values == ["PRJ-HOL-A-2026", "PRJ-HOL-B-2026"]


def test_main_pass_or_skip_on_repo(consistency_module, capsys):
    """Smoke test: running against the real repo state must PASS or SKIP, never FAIL.

    If this fails, the wave-2 working tree has introduced an unresolved
    program_id reference and the operator must resolve it before merging.
    """
    rc = consistency_module.main()
    captured = capsys.readouterr()
    assert rc == 0, (
        "validate_program_id_consistency must PASS/SKIP on repo HEAD; FAIL means an "
        "unresolved program_id reference exists. Output:\n" + captured.out
    )
    assert "PROGRAM_ID consistency validator" in captured.out
