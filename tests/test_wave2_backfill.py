"""Tests for scripts/wave2_backfill.py.

Locks in the bootstrap contract:
- Sentinel detection is exact (string equality, not substring).
- Section gating is honoured (--section restricts target).
- Write mode refuses on pending sentinels by default; --allow-pending bypasses.
- The shipped operator-answers-wave2.yaml parses, has all 5 sections, and
  carries pre-filled values + sentinels per the plan.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAFFOLDER_PATH = REPO_ROOT / "scripts" / "wave2_backfill.py"
ANSWERS_PATH = (
    REPO_ROOT
    / "docs"
    / "wip"
    / "planning"
    / "22a-i22-post-closure-followups"
    / "operator-answers-wave2.yaml"
)


@pytest.fixture(scope="module")
def scaffolder_module():
    """Import scripts/wave2_backfill.py as a module."""
    spec = importlib.util.spec_from_file_location(
        "wave2_backfill_under_test", SCAFFOLDER_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["wave2_backfill_under_test"] = module
    spec.loader.exec_module(module)
    return module


def test_sentinel_constant(scaffolder_module):
    assert scaffolder_module.SENTINEL == "__OPERATOR_CONFIRM__"


def test_count_sentinels_string(scaffolder_module):
    assert scaffolder_module.count_sentinels("__OPERATOR_CONFIRM__") == 1
    assert scaffolder_module.count_sentinels("not a sentinel") == 0
    # Substring should NOT match — exact equality only.
    assert scaffolder_module.count_sentinels("__OPERATOR_CONFIRM__ extra") == 0


def test_count_sentinels_nested(scaffolder_module):
    payload = {
        "a": "__OPERATOR_CONFIRM__",
        "b": "ok",
        "c": [
            "__OPERATOR_CONFIRM__",
            {"d": "__OPERATOR_CONFIRM__"},
        ],
        "e": {"f": {"g": "__OPERATOR_CONFIRM__"}},
    }
    assert scaffolder_module.count_sentinels(payload) == 4


def test_section_status_filled(scaffolder_module):
    data = {"programs": {"PRJ-A": {"program_code": "AAA", "lifecycle_status": "active"}}}
    sentinels, leaves = scaffolder_module.section_status(data, "programs")
    assert sentinels == 0
    assert leaves == 2


def test_section_status_pending(scaffolder_module):
    data = {
        "programs": {
            "PRJ-A": {
                "program_code": "AAA",
                "lifecycle_status": "__OPERATOR_CONFIRM__",
            }
        }
    }
    sentinels, leaves = scaffolder_module.section_status(data, "programs")
    assert sentinels == 1
    assert leaves == 2


def test_section_status_absent(scaffolder_module):
    sentinels, leaves = scaffolder_module.section_status({}, "programs")
    assert (sentinels, leaves) == (0, 0)


def test_resolve_target_sections_default(scaffolder_module):
    # Default returns all sections except meta.
    targets = scaffolder_module._resolve_target_sections(None)
    assert "meta" not in targets
    assert "programs" in targets
    assert "brand_voice" in targets
    assert "goi_poi_voice" in targets
    assert "kirbe_duality" in targets
    assert "g_24_3_signoff" in targets


def test_resolve_target_sections_filter(scaffolder_module):
    assert scaffolder_module._resolve_target_sections("programs") == ["programs"]


def test_resolve_target_sections_unknown(scaffolder_module):
    with pytest.raises(SystemExit):
        scaffolder_module._resolve_target_sections("not_a_section")


def test_shipped_yaml_parses_and_has_5_sections(scaffolder_module):
    """The operator-answers-wave2.yaml shipped today must parse and carry all 5 sections."""
    if not ANSWERS_PATH.is_file():
        pytest.skip("operator-answers-wave2.yaml not present (pre-bootstrap repo state)")
    data = scaffolder_module.load_answers(ANSWERS_PATH)
    for required in (
        "meta",
        "programs",
        "brand_voice",
        "goi_poi_voice",
        "kirbe_duality",
        "g_24_3_signoff",
    ):
        assert required in data, f"missing top-level section: {required}"


def test_shipped_yaml_programs_has_12_rows(scaffolder_module):
    """Section 1 must have 12 programs (11 from process_list + PRJ-HOL-FOUNDING-2026)."""
    if not ANSWERS_PATH.is_file():
        pytest.skip("operator-answers-wave2.yaml not present")
    data = scaffolder_module.load_answers(ANSWERS_PATH)
    programs = data["programs"]
    assert isinstance(programs, dict)
    assert len(programs) == 12, f"expected 12 program rows, got {len(programs)}"
    # PRJ-HOL-FOUNDING-2026 must be the only one without a process_item_id.
    founding = programs["PRJ-HOL-FOUNDING-2026"]
    assert founding["process_item_id"] == ""
    assert founding["program_code"] == "FND"
    # Sample existing process row has FK back to process_list.
    kirbe = programs["env_tech_prj_2"]
    assert kirbe["process_item_id"] == "env_tech_prj_2"
    assert kirbe["program_code"] == "KIR"


def test_shipped_yaml_program_codes_unique(scaffolder_module):
    """Validator rule: program_code is unique across rows + matches ^[A-Z]{3}$."""
    import re

    if not ANSWERS_PATH.is_file():
        pytest.skip("operator-answers-wave2.yaml not present")
    data = scaffolder_module.load_answers(ANSWERS_PATH)
    codes = [row["program_code"] for row in data["programs"].values()]
    pattern = re.compile(r"^[A-Z]{3}$")
    for code in codes:
        assert pattern.match(code), f"program_code {code!r} fails ^[A-Z]{{3}}$"
    assert len(codes) == len(set(codes)), "program_code values must be unique"


def test_check_only_does_not_raise_on_pending(scaffolder_module, capsys):
    """--check-only must always exit 0 even when sentinels remain."""
    if not ANSWERS_PATH.is_file():
        pytest.skip("operator-answers-wave2.yaml not present")
    data = scaffolder_module.load_answers(ANSWERS_PATH)
    rc = scaffolder_module.cmd_check_only(data)
    assert rc == 0
    captured = capsys.readouterr()
    assert "sentinel scan" in captured.out


def test_dry_run_blocks_on_pending(scaffolder_module, capsys):
    """--dry-run must refuse when target section carries sentinels."""
    if not ANSWERS_PATH.is_file():
        pytest.skip("operator-answers-wave2.yaml not present")
    data = scaffolder_module.load_answers(ANSWERS_PATH)
    rc = scaffolder_module.cmd_dry_run(data, section_filter="programs")
    # At bootstrap time, programs section has many sentinels; must block.
    assert rc == 1, "--dry-run should refuse while sentinels remain in target section"
    captured = capsys.readouterr()
    assert "BLOCKED" in captured.out


def test_write_refuses_pending_without_flag(scaffolder_module, capsys):
    """Full write must refuse on sentinels unless --allow-pending is set."""
    if not ANSWERS_PATH.is_file():
        pytest.skip("operator-answers-wave2.yaml not present")
    data = scaffolder_module.load_answers(ANSWERS_PATH)
    rc = scaffolder_module.cmd_write(data, section_filter="programs", allow_pending=False)
    assert rc == 1
    captured = capsys.readouterr()
    assert "REFUSED" in captured.out
