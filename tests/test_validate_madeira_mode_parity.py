"""Tests for scripts/validate_madeira_mode_parity.py and akos/hlk_madeira_mode.py per I76 P1."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from akos.hlk_madeira_mode import (
    CANONICAL_MODE_SPECS,
    CANONICAL_REGISTRY,
    MadeiraModeRegistry,
    MadeiraModeSpec,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_madeira_mode_parity.py"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_madeira_mode_parity", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("validate_madeira_mode_parity", module)
    spec.loader.exec_module(module)
    return module


@pytest.mark.hlk
class TestMadeiraModeRegistry:
    def test_canonical_registry_has_5_modes(self):
        assert len(CANONICAL_REGISTRY.modes) == 5

    def test_canonical_registry_ids(self):
        ids = {s.mode_id for s in CANONICAL_REGISTRY.modes}
        assert ids == {"ask", "plan", "agent", "debug", "methodology"}

    def test_registry_by_id_returns_spec(self):
        spec = CANONICAL_REGISTRY.by_id("methodology")
        assert spec.rbac_posture == "methodology-checkpoint"
        assert spec.persistence_default == "persistent-across-sessions"

    def test_registry_by_id_unknown_raises(self):
        with pytest.raises(KeyError):
            CANONICAL_REGISTRY.by_id("unknown")  # type: ignore[arg-type]

    def test_registry_rejects_4_modes(self):
        with pytest.raises(ValidationError):
            MadeiraModeRegistry(modes=CANONICAL_MODE_SPECS[:4])

    def test_registry_rejects_6_modes(self):
        with pytest.raises(ValidationError):
            MadeiraModeRegistry(modes=CANONICAL_MODE_SPECS + (CANONICAL_MODE_SPECS[0],))

    def test_invalid_mode_id_rejected(self):
        with pytest.raises(ValidationError):
            MadeiraModeSpec(
                mode_id="bogus",  # type: ignore[arg-type]
                name="Bogus",
                added_by="I76 P1",
                rbac_posture="full",
                persistence_default="per-task",
            )

    def test_invalid_rbac_posture_rejected(self):
        with pytest.raises(ValidationError):
            MadeiraModeSpec(
                mode_id="ask",
                name="Ask",
                added_by="I17 P1",
                rbac_posture="root",  # type: ignore[arg-type]
                persistence_default="ephemeral",
            )

    def test_invalid_persistence_default_rejected(self):
        with pytest.raises(ValidationError):
            MadeiraModeSpec(
                mode_id="ask",
                name="Ask",
                added_by="I17 P1",
                rbac_posture="read",
                persistence_default="forever",  # type: ignore[arg-type]
            )

    def test_invalid_added_by_rejected(self):
        with pytest.raises(ValidationError):
            MadeiraModeSpec(
                mode_id="ask",
                name="Ask",
                added_by="I99 P1",  # type: ignore[arg-type]
                rbac_posture="read",
                persistence_default="ephemeral",
            )

    def test_spec_is_frozen(self):
        spec = CANONICAL_MODE_SPECS[0]
        with pytest.raises(ValidationError):
            spec.rbac_posture = "full"  # type: ignore[misc]

    def test_extra_field_rejected(self):
        with pytest.raises(ValidationError):
            MadeiraModeSpec(
                mode_id="ask",
                name="Ask",
                added_by="I17 P1",
                rbac_posture="read",
                persistence_default="ephemeral",
                surprise="boom",  # type: ignore[call-arg]
            )


@pytest.mark.hlk
class TestValidatorParse:
    def test_canonical_sop_exists(self):
        from akos.hlk_madeira_mode import CANONICAL_REGISTRY  # noqa: F401

        validator = _load_validator_module()
        assert validator.SOP_PATH.is_file(), f"SOP missing at {validator.SOP_PATH}"

    def test_parse_extracts_5_specs_from_canonical_sop(self):
        validator = _load_validator_module()
        sop_text = validator.SOP_PATH.read_text(encoding="utf-8")
        parsed = validator.parse_mode_table(sop_text)
        assert len(parsed) == 5
        ids = {s.mode_id for s in parsed}
        assert ids == {"ask", "plan", "agent", "debug", "methodology"}

    def test_validate_canonical_sop_returns_zero(self):
        validator = _load_validator_module()
        result = validator.validate(validator.SOP_PATH, strict=False)
        assert result == 0

    def test_validate_missing_file_returns_two(self, tmp_path):
        validator = _load_validator_module()
        missing = tmp_path / "nonexistent.md"
        result = validator.validate(missing, strict=False)
        assert result == 2

    def test_validate_invalid_structure_returns_two(self, tmp_path):
        validator = _load_validator_module()
        bad_sop = tmp_path / "bad.md"
        bad_sop.write_text("# no table here\n\njust prose\n", encoding="utf-8")
        result = validator.validate(bad_sop, strict=False)
        assert result == 2

    def test_validate_swapped_rbac_returns_one(self, tmp_path):
        validator = _load_validator_module()
        bad_sop = tmp_path / "swapped.md"
        bad_sop.write_text(
            "# preamble\n"
            "```\n"
            "mode_id        | name          | added_by   | rbac_posture            | persistence_default\n"
            "---------------+---------------+------------+-------------------------+---------------------\n"
            "ask            | Ask           | I17 P1     | full                    | ephemeral\n"
            "plan           | Plan          | I17 P1     | read + plan-write       | plan-doc-scoped\n"
            "agent          | Agent         | I17 P1     | full                    | per-task\n"
            "debug          | Debug         | I76 P1     | read + observability    | session-scoped\n"
            "methodology    | Methodology   | I76 P1     | methodology-checkpoint  | persistent-across-sessions\n"
            "```\n",
            encoding="utf-8",
        )
        result = validator.validate(bad_sop, strict=False)
        assert result == 1
