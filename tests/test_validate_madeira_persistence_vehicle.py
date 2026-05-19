"""Tests for scripts/validate_madeira_persistence_vehicle.py and akos/hlk_madeira_persistence_vehicle.py per I76 P3."""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from akos.hlk_madeira_persistence_vehicle import (
    MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES,
    MadeiraPersistenceVehicleRegistry,
    MadeiraPersistenceVehicleRow,
)


pytestmark = pytest.mark.compliance


REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = (
    REPO_ROOT
    / "docs"
    / "references"
    / "hlk"
    / "v3.0"
    / "Admin"
    / "O5-1"
    / "Envoy Tech Lab"
    / "canonicals"
    / "dimensions"
    / "MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv"
)


def _import_validator():
    spec = importlib.util.spec_from_file_location(
        "_test_vmpv",
        REPO_ROOT / "scripts" / "validate_madeira_persistence_vehicle.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_test_vmpv"] = module
    spec.loader.exec_module(module)
    return module


def _valid_row(**overrides) -> dict:
    base: dict = {
        "vehicle_id": "vehicle_test_one",
        "vehicle_name": "Test vehicle",
        "vehicle_path": "docs/wip/test/<NN>/file.md",
        "vehicle_scope": "cross_session",
        "target_audience": "operator_plus_aics",
        "write_authority": "madeira_writes_flagged",
        "read_cadence": "every_session",
        "staleness_days": 30,
        "staleness_posture": "cite_and_flag",
        "provenance": "git_tracked_md",
        "memory_class": "procedural",
        "owner_role": "PMO",
        "topic_ids": "",
        "depends_on_vehicle_ids": "",
        "status": "active",
        "added_at": "2026-05-19",
        "last_review_at": "2026-05-19",
        "last_review_by": "System Owner",
        "methodology_version_at_review": "v3.0",
        "last_review_decision_id": "D-IH-76-F",
        "notes": "",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Pydantic row tests — basic + happy path
# ---------------------------------------------------------------------------


def test_minimal_valid_row_parses() -> None:
    row = MadeiraPersistenceVehicleRow(**_valid_row())
    assert row.vehicle_id == "vehicle_test_one"


def test_fieldnames_tuple_is_21_columns() -> None:
    assert len(MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES) == 21


# ---------------------------------------------------------------------------
# vehicle_id pattern
# ---------------------------------------------------------------------------


def test_vehicle_id_pattern_enforced() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="bad-id-with-dash"))


def test_vehicle_id_must_have_prefix() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="no_prefix_id"))


def test_vehicle_id_uppercase_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="vehicle_BAD"))


# ---------------------------------------------------------------------------
# Enum-typed fields
# ---------------------------------------------------------------------------


def test_invalid_vehicle_scope_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(vehicle_scope="forever"))


def test_invalid_write_authority_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(write_authority="anyone"))


def test_invalid_read_cadence_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(read_cadence="hourly"))


def test_invalid_provenance_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(provenance="wiki"))


def test_invalid_memory_class_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(memory_class="metaphysical"))


def test_invalid_status_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(status="released"))


def test_invalid_methodology_version_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(methodology_version_at_review="v2.7"))


def test_invalid_decision_id_format_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(last_review_decision_id="D76F"))


def test_invalid_iso_date_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(added_at="May 19 2026"))


# ---------------------------------------------------------------------------
# target_audience semicolon-list validation
# ---------------------------------------------------------------------------


def test_target_audience_single_value_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(**_valid_row(target_audience="operator_private"))
    assert row.target_audience == "operator_private"


def test_target_audience_semicolon_list_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(
        **_valid_row(target_audience="operator_plus_aics;external_handoff")
    )
    assert ";" in row.target_audience


def test_target_audience_invalid_entry_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(
            **_valid_row(target_audience="operator_plus_aics;public")
        )


def test_target_audience_duplicate_entries_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(
            **_valid_row(target_audience="operator_private;operator_private")
        )


def test_target_audience_empty_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(target_audience=""))


# ---------------------------------------------------------------------------
# topic_ids format
# ---------------------------------------------------------------------------


def test_topic_ids_empty_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(**_valid_row(topic_ids=""))
    assert row.topic_ids == ""


def test_topic_ids_valid_pattern_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(
        **_valid_row(topic_ids="topic_madeira_platform;topic_governance_moat")
    )
    assert "topic_madeira_platform" in row.topic_ids


def test_topic_ids_bad_pattern_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(topic_ids="not_a_topic"))


def test_topic_ids_uppercase_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(**_valid_row(topic_ids="topic_BAD"))


# ---------------------------------------------------------------------------
# depends_on_vehicle_ids self-FK + format
# ---------------------------------------------------------------------------


def test_depends_on_empty_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(**_valid_row(depends_on_vehicle_ids=""))
    assert row.depends_on_vehicle_ids == ""


def test_depends_on_self_reference_rejected() -> None:
    with pytest.raises(ValidationError) as exc:
        MadeiraPersistenceVehicleRow(
            **_valid_row(
                vehicle_id="vehicle_self_ref",
                depends_on_vehicle_ids="vehicle_self_ref",
            )
        )
    assert "self-dependency" in str(exc.value)


def test_depends_on_invalid_pattern_rejected() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(
            **_valid_row(depends_on_vehicle_ids="bad-id-with-dash")
        )


# ---------------------------------------------------------------------------
# Stale-constraint detection: staleness_days + staleness_posture alignment
# ---------------------------------------------------------------------------


def test_staleness_posture_none_with_days_set_rejected() -> None:
    """posture=none + staleness_days set -> stale-constraint detected."""
    with pytest.raises(ValidationError) as exc:
        MadeiraPersistenceVehicleRow(
            **_valid_row(staleness_days=30, staleness_posture="none")
        )
    assert "staleness" in str(exc.value).lower()


def test_staleness_posture_cite_with_days_null_rejected() -> None:
    """posture=cite_and_flag + staleness_days null -> staleness threshold missing."""
    with pytest.raises(ValidationError) as exc:
        MadeiraPersistenceVehicleRow(
            **_valid_row(staleness_days=None, staleness_posture="cite_and_flag")
        )
    assert "staleness" in str(exc.value).lower()


def test_staleness_posture_refuse_with_days_null_rejected() -> None:
    """posture=refuse_without_ratify + staleness_days null -> threshold missing."""
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(
            **_valid_row(staleness_days=None, staleness_posture="refuse_without_ratify")
        )


def test_staleness_posture_none_with_days_null_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(
        **_valid_row(staleness_days=None, staleness_posture="none")
    )
    assert row.staleness_days is None
    assert row.staleness_posture == "none"


def test_staleness_posture_cite_with_days_set_accepted() -> None:
    row = MadeiraPersistenceVehicleRow(
        **_valid_row(staleness_days=90, staleness_posture="cite_and_flag")
    )
    assert row.staleness_days == 90


def test_staleness_days_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        MadeiraPersistenceVehicleRow(
            **_valid_row(staleness_days=0, staleness_posture="cite_and_flag")
        )


# ---------------------------------------------------------------------------
# Registry-level validation
# ---------------------------------------------------------------------------


def test_registry_rejects_duplicate_vehicle_ids() -> None:
    row1 = MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="vehicle_a"))
    row2 = MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="vehicle_a"))
    with pytest.raises(ValidationError) as exc:
        MadeiraPersistenceVehicleRegistry(rows=(row1, row2))
    assert "duplicate vehicle_id" in str(exc.value)


def test_registry_accepts_distinct_rows() -> None:
    row1 = MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="vehicle_a"))
    row2 = MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="vehicle_b"))
    registry = MadeiraPersistenceVehicleRegistry(rows=(row1, row2))
    assert len(registry.rows) == 2


def test_registry_depends_on_closure_unknown_rejected() -> None:
    row1 = MadeiraPersistenceVehicleRow(
        **_valid_row(
            vehicle_id="vehicle_a",
            depends_on_vehicle_ids="vehicle_does_not_exist",
        )
    )
    with pytest.raises(ValidationError) as exc:
        MadeiraPersistenceVehicleRegistry(rows=(row1,))
    assert "unknown vehicles" in str(exc.value)


def test_registry_depends_on_closure_known_accepted() -> None:
    row1 = MadeiraPersistenceVehicleRow(**_valid_row(vehicle_id="vehicle_parent"))
    row2 = MadeiraPersistenceVehicleRow(
        **_valid_row(
            vehicle_id="vehicle_child", depends_on_vehicle_ids="vehicle_parent"
        )
    )
    registry = MadeiraPersistenceVehicleRegistry(rows=(row1, row2))
    assert len(registry.rows) == 2


# ---------------------------------------------------------------------------
# CSV header + integration tests against the real seed CSV
# ---------------------------------------------------------------------------


def test_canonical_csv_header_matches() -> None:
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames == list(MADEIRA_PERSISTENCE_VEHICLE_FIELDNAMES)


def test_canonical_csv_all_rows_parse() -> None:
    """All 16 seed rows parse + registry-level closure resolves."""
    assert CSV_PATH.is_file(), f"missing {CSV_PATH}"
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        raw_rows = list(reader)
    assert len(raw_rows) == 16, f"expected 16 seed rows, got {len(raw_rows)}"

    parsed = []
    for raw in raw_rows:
        coerced = {k: v for k, v in raw.items() if isinstance(k, str)}
        sd = (raw.get("staleness_days") or "").strip()
        coerced["staleness_days"] = int(sd) if sd else None
        parsed.append(MadeiraPersistenceVehicleRow(**coerced))
    MadeiraPersistenceVehicleRegistry(rows=tuple(parsed))


def test_canonical_csv_no_duplicate_vehicle_ids() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        ids = [(r.get("vehicle_id") or "").strip() for r in reader]
    assert len(ids) == len(set(ids))


# ---------------------------------------------------------------------------
# Validator script smoke
# ---------------------------------------------------------------------------


def test_validator_passes_on_real_csv_default() -> None:
    """Default mode: FK miss is advisory WARN; exit 0."""
    vmpv = _import_validator()
    result = vmpv.main([])
    assert result == 0


def test_validator_strict_mode_passes_when_d_ih_76_f_resolves() -> None:
    """Strict mode passes when D-IH-76-F is in DECISION_REGISTER.csv.

    Before D-IH-76-F is appended to the register, this test will see exit 1
    (16 FK misses promoted to FAIL). Once the I76 P3 commit lands the decision
    row, the test passes.
    """
    vmpv = _import_validator()
    decision_ids = vmpv._load_decision_ids()
    if "D-IH-76-F" not in decision_ids:
        pytest.skip("D-IH-76-F not yet in DECISION_REGISTER.csv (pre-commit state)")
    assert vmpv.main(["--strict"]) == 0
