"""Tests for PEOPLE_DESIGN_PATTERN_REGISTRY.csv + akos.hlk_design_pattern_csv + validator
(Initiative 79 P2; D-IH-79-A/C/D pattern library + D-IH-79-N anti-jargon drift gate).

Covers:
- The canonical CSV header matches the SSOT ``DESIGN_PATTERN_FIELDNAMES`` tuple.
- Each row Pydantic-validates against ``DesignPatternRow`` (Literal enums, slug regex,
  ISO-date last_review, FK regex on ratifying_decision_id + originating_initiative_id,
  Markdown anchor regex on pattern_md_anchor).
- Every ``consumer_areas`` semicolon-token is in ``VALID_CONSUMER_AREAS``.
- Every ``pattern_class`` is in ``VALID_PATTERN_CLASSES``.
- Every ``discipline_origin`` is in ``VALID_DISCIPLINE_ORIGINS``.
- Every ``status`` is in ``VALID_STATUSES``.
- The validator script (``scripts/validate_design_pattern_registry.py``) exits 0
  in registry mode against the canonical CSV.
- The validator script exits 0 in ``--jargon-scan`` mode (anti-jargon drift gate).
- Invalid input pairs are rejected: bad pattern_id slug, bad pattern_class enum,
  malformed last_review date, malformed pattern_md_anchor.

These tests run under the default ``py scripts/test.py all`` collection via the
implicit ``tests/test_*.py`` glob.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_design_pattern_csv import (  # noqa: E402
    DESIGN_PATTERN_FIELDNAMES,
    VALID_CONSUMER_AREAS,
    VALID_DISCIPLINE_ORIGINS,
    VALID_PATTERN_CLASSES,
    VALID_STATUSES,
    DesignPatternRow,
)

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People"
    / "Compliance" / "canonicals" / "dimensions"
    / "PEOPLE_DESIGN_PATTERN_REGISTRY.csv"
)
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_design_pattern_registry.py"


def _read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_exists() -> None:
    assert CSV_PATH.is_file(), f"canonical CSV missing at {CSV_PATH}"


def test_csv_header_matches_fieldnames_tuple() -> None:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert tuple(header) == DESIGN_PATTERN_FIELDNAMES, (
        "PEOPLE_DESIGN_PATTERN_REGISTRY.csv header drifted from "
        "DESIGN_PATTERN_FIELDNAMES SSOT tuple"
    )


def test_csv_column_count_is_15() -> None:
    """D-IH-79-D 15-column schema (pattern metadata + FKs + acceptance criteria
    + lifecycle metadata + last-review-stamp pair).
    """
    assert len(DESIGN_PATTERN_FIELDNAMES) == 15, (
        f"expected 15-column schema; got {len(DESIGN_PATTERN_FIELDNAMES)}"
    )


def test_at_least_one_row_per_pattern_class_seeded() -> None:
    """The seed registry should exercise breadth across the 11-class taxonomy
    (10 original from I79 P2 + ``documentation_layering`` from I80 P1 D-IH-80-G).
    A minimum of 5 distinct pattern_class values must appear in the seed data.
    """
    rows = _read_rows()
    classes = {(r.get("pattern_class") or "").strip() for r in rows}
    assert len(classes) >= 5, (
        f"seed registry too narrow; only {len(classes)} pattern_class values present: {sorted(classes)}"
    )


def test_documentation_layering_class_in_enum() -> None:
    """I80 P1 D-IH-80-G: ``documentation_layering`` must be in the pattern_class enum
    as the 11th class anchoring ``pattern_sop_addendum_split``.
    """
    assert "documentation_layering" in VALID_PATTERN_CLASSES, (
        "documentation_layering missing from VALID_PATTERN_CLASSES; "
        "I80 P1 D-IH-80-G enum extension not applied"
    )


def test_pattern_class_enum_size_is_17() -> None:
    """Pattern_class enum has exactly 17 members
    (10 original from I79 P2 + ``documentation_layering`` from I80 P1 +
    ``output_architecture_hierarchy`` from I86 Wave L +
    ``inter_wave_regression_cadence`` from I86 Wave M P1 +
    ``quality_fabric_specialty_canonical`` from I86 Wave M P5 Cluster B umbrella +
    ``index_integrity_cadence`` from I86 Wave N P3 INDEX_INTEGRITY mint +
    ``area_governance`` from I93 P0/P1 D-IH-93-B +
    ``intent_ranked_regression_cadence`` from I88 D-IH-88-F intent-ranked regression).
    """
    assert len(VALID_PATTERN_CLASSES) == 17, (
        f"expected 17-class pattern_class taxonomy; got {len(VALID_PATTERN_CLASSES)}: "
        f"{sorted(VALID_PATTERN_CLASSES)}"
    )


def test_area_governance_class_in_enum() -> None:
    """I93 P0/P1 D-IH-93-B: ``area_governance`` must be in the pattern_class enum
    anchoring ``pattern_area_buildout`` (the area-governance meta-process). The CSV
    + wired validator already accepted it; the enum lagged until the I88
    intent-ranked regression surfaced the dual-SSOT drift 2026-06-05.
    """
    assert "area_governance" in VALID_PATTERN_CLASSES, (
        "area_governance missing from VALID_PATTERN_CLASSES; "
        "I93 P0/P1 D-IH-93-B enum extension not applied"
    )


def test_intent_ranked_regression_cadence_class_in_enum() -> None:
    """I88 D-IH-88-F: ``intent_ranked_regression_cadence`` must be in the
    pattern_class enum as the 17th class anchoring
    ``pattern_intent_ranked_regression`` (the value layer above the inter-wave
    regression cadence).
    """
    assert "intent_ranked_regression_cadence" in VALID_PATTERN_CLASSES, (
        "intent_ranked_regression_cadence missing from VALID_PATTERN_CLASSES; "
        "I88 D-IH-88-F enum extension not applied"
    )


def test_index_integrity_cadence_class_in_enum() -> None:
    """I86 Wave N P3 D-IH-86-CD: ``index_integrity_cadence`` must be in the
    pattern_class enum as the 15th class anchoring the INDEX_INTEGRITY 11th
    Quality Fabric specialty mint (sister to ``inter_wave_regression_cadence``
    at Wave M P1).
    """
    assert "index_integrity_cadence" in VALID_PATTERN_CLASSES, (
        "index_integrity_cadence missing from VALID_PATTERN_CLASSES; "
        "I86 Wave N P3 D-IH-86-CD enum extension not applied"
    )


def test_output_architecture_hierarchy_class_in_enum() -> None:
    """I86 Wave L D-IH-86-BE: ``output_architecture_hierarchy`` must be in the
    pattern_class enum as the 12th class anchoring
    ``pattern_4layer_output_architecture_below_quality_fabric``.
    """
    assert "output_architecture_hierarchy" in VALID_PATTERN_CLASSES, (
        "output_architecture_hierarchy missing from VALID_PATTERN_CLASSES; "
        "I86 Wave L D-IH-86-BE enum extension not applied"
    )


def test_pattern_sop_addendum_split_row_present() -> None:
    """I80 P1: the ``pattern_sop_addendum_split`` row must be present in the
    canonical CSV with pattern_class ``documentation_layering`` (D-IH-80-B + D-IH-80-G).
    """
    rows = _read_rows()
    matches = [r for r in rows if r.get("pattern_id") == "pattern_sop_addendum_split"]
    assert len(matches) == 1, (
        f"expected exactly one pattern_sop_addendum_split row; got {len(matches)}"
    )
    row = matches[0]
    assert row["pattern_class"] == "documentation_layering", (
        f"pattern_sop_addendum_split.pattern_class expected 'documentation_layering'; "
        f"got {row['pattern_class']!r}"
    )
    assert row["ratifying_decision_id"] == "D-IH-80-B", (
        f"pattern_sop_addendum_split.ratifying_decision_id expected 'D-IH-80-B'; "
        f"got {row['ratifying_decision_id']!r}"
    )
    assert row["originating_initiative_id"] == "INIT-OPENCLAW_AKOS-80", (
        f"pattern_sop_addendum_split.originating_initiative_id expected "
        f"'INIT-OPENCLAW_AKOS-80'; got {row['originating_initiative_id']!r}"
    )


def test_every_row_pydantic_validates() -> None:
    rows = _read_rows()
    errors: list[str] = []
    for i, r in enumerate(rows, start=2):
        try:
            DesignPatternRow.model_validate({k: (v or "") for k, v in r.items() if k})
        except ValidationError as exc:
            errors.append(f"row {i} ({r.get('pattern_id', '?')}): {exc}")
    assert not errors, "Pydantic validation errors:\n" + "\n".join(errors)


def test_all_pattern_classes_in_enum() -> None:
    rows = _read_rows()
    for r in rows:
        assert r["pattern_class"] in VALID_PATTERN_CLASSES, (
            f"row {r['pattern_id']}: pattern_class {r['pattern_class']!r} not in "
            f"{sorted(VALID_PATTERN_CLASSES)}"
        )


def test_all_discipline_origins_in_enum() -> None:
    rows = _read_rows()
    for r in rows:
        assert r["discipline_origin"] in VALID_DISCIPLINE_ORIGINS, (
            f"row {r['pattern_id']}: discipline_origin {r['discipline_origin']!r} not in "
            f"{sorted(VALID_DISCIPLINE_ORIGINS)}"
        )


def test_all_statuses_in_enum() -> None:
    rows = _read_rows()
    for r in rows:
        assert r["status"] in VALID_STATUSES, (
            f"row {r['pattern_id']}: status {r['status']!r} not in {sorted(VALID_STATUSES)}"
        )


def test_every_consumer_areas_token_in_enum() -> None:
    """consumer_areas is semicolon-separated; every token must be a known consumer area."""
    rows = _read_rows()
    errors: list[str] = []
    for r in rows:
        tokens = [t.strip() for t in (r.get("consumer_areas") or "").split(";") if t.strip()]
        for tok in tokens:
            if tok not in VALID_CONSUMER_AREAS:
                errors.append(
                    f"row {r['pattern_id']}: consumer_areas token {tok!r} not in "
                    f"{sorted(VALID_CONSUMER_AREAS)}"
                )
    assert not errors, "consumer_areas token errors:\n" + "\n".join(errors)


def test_invalid_pattern_id_slug_rejected() -> None:
    """pattern_id must match ^pattern_[a-z0-9_]+$; uppercase / no-prefix rejected."""
    bad = _valid_payload() | {"pattern_id": "BadPattern"}
    with pytest.raises(ValidationError):
        DesignPatternRow.model_validate(bad)


def test_invalid_pattern_class_rejected() -> None:
    bad = _valid_payload() | {"pattern_class": "not_a_real_class"}
    with pytest.raises(ValidationError):
        DesignPatternRow.model_validate(bad)


def test_invalid_last_review_date_rejected() -> None:
    bad = _valid_payload() | {"last_review": "not-a-date"}
    with pytest.raises(ValidationError):
        DesignPatternRow.model_validate(bad)


def test_invalid_pattern_md_anchor_rejected() -> None:
    """Anchor must match ^#pattern-[a-z0-9-]+$; no underscore + no leading hash rejected."""
    bad = _valid_payload() | {"pattern_md_anchor": "pattern-no-leading-hash"}
    with pytest.raises(ValidationError):
        DesignPatternRow.model_validate(bad)


def test_invalid_decision_fk_rejected() -> None:
    bad = _valid_payload() | {"ratifying_decision_id": "not-a-decision"}
    with pytest.raises(ValidationError):
        DesignPatternRow.model_validate(bad)


def test_invalid_initiative_fk_rejected() -> None:
    bad = _valid_payload() | {"originating_initiative_id": "INIT-WRONG-FORMAT"}
    with pytest.raises(ValidationError):
        DesignPatternRow.model_validate(bad)


def test_validator_script_registry_mode_exits_zero() -> None:
    """End-to-end: the validator CLI exits 0 in registry mode on the canonical CSV."""
    if not VALIDATOR_PATH.is_file():
        pytest.skip(f"validator script not present at {VALIDATOR_PATH}")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"validator (registry mode) failed (exit={result.returncode}):\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )


def test_validator_script_jargon_scan_mode_exits_zero() -> None:
    """End-to-end: --jargon-scan mode exits 0 against People canonicals (D-IH-79-N)."""
    if not VALIDATOR_PATH.is_file():
        pytest.skip(f"validator script not present at {VALIDATOR_PATH}")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--jargon-scan"],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"validator (jargon-scan mode) failed (exit={result.returncode}):\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )


def _valid_payload() -> dict[str, str]:
    """Minimal valid payload for negative tests; all fields populated correctly."""
    return {
        "pattern_id": "pattern_test_fixture",
        "pattern_name": "Test Fixture Pattern",
        "pattern_class": "register_dimension",
        "discipline_origin": "compliance",
        "consumer_areas": "marketing;research",
        "ratifying_decision_id": "D-IH-79-A",
        "originating_initiative_id": "INIT-OPENCLAW_AKOS-79",
        "pattern_md_anchor": "#pattern-test-fixture",
        "canonical_artifact_path": "docs/references/hlk/v3.0/test/",
        "acceptance_criteria_human": "human can run by reading SOP",
        "acceptance_criteria_automation": "validator passes",
        "status": "active",
        "last_review": "2026-05-15",
        "last_review_by": "Test Owner",
        "notes": "",
    }
