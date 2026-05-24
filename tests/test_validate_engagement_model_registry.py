"""Tests for ENGAGEMENT_MODEL_REGISTRY.csv + akos.hlk_engagement_model_csv + validator
(Initiative 73 P1; D-IH-73-C sibling-dimension + D-IH-73-D 7-class taxonomy).

Covers:
- The canonical CSV header matches the SSOT `ENGAGEMENT_MODEL_FIELDNAMES` tuple.
- The seven D-IH-73-D classes are all present in the CSV (taxonomy completeness).
- Each row Pydantic-validates against `EngagementModelRow` (enum, slug, int bounds).
- Per-class enum row content matches the operator-ratified default at D-IH-73-H..M.
- The `outsourced_helper` row carries D-IH-73-E SOC posture (low_trust + access_level=1).
- The `operator_self` row carries D-IH-73-D baseline (internal SOC + access_level=6).
- The validator script (`scripts/validate_engagement_model_registry.py`) exits 0
  against the canonical CSV.
- Invalid input pairs are rejected: bad slug, bad enum, out-of-range access_level.

These tests are registered under the `engagement` lane via the implicit
`tests/test_*.py` collection (the `engagement` group is added to scripts/test.py
GROUPS at I73 P1 commit-time). Default `py scripts/test.py all` covers them.
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

from akos.hlk_engagement_model_csv import (  # noqa: E402
    ENGAGEMENT_MODEL_FIELDNAMES,
    VALID_COUNTERPARTY_RESOLUTION_STRATEGIES,
    VALID_IP_CLAUSE_CLASSES,
    VALID_KNOWLEDGE_ACCESS_LEVELS,
    VALID_PAYMENT_CADENCES,
    VALID_RETRIBUTION_PATTERNS,
    VALID_SOC_POSTURES,
    VALID_STATUSES,
    EngagementModelRow,
)

CSV_PATH = (
    REPO_ROOT
    / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "People Operations"
    / "canonicals" / "dimensions" / "ENGAGEMENT_MODEL_REGISTRY.csv"
)
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_engagement_model_registry.py"

# Operator-ratified D-IH-73-D 7-class taxonomy
EXPECTED_CLASSES = (
    "eng_model_hourly_consultant",
    "eng_model_milestone_consultant",
    "eng_model_percentage_collaborator",
    "eng_model_apprentice_learner",
    "eng_model_investor_advisor",
    "eng_model_outsourced_helper",
    "eng_model_operator_self",
)

# Bundle B-2c (D-IH-81-X) — counterparty-routing extensions extend the people-
# taxonomy to a unified counterparty-routing taxonomy. SaaS subscription is
# active (KiRBe forward); RPP vendor + one-off invoice are planned (promote
# when first real instance fires).
EXPECTED_B2C_EXTENSION_CLASSES = (
    "eng_model_saas_subscription",
    "eng_model_rpp_vendor",
    "eng_model_one_off_invoice",
)

# B-2c operator-ratified resolution-strategy mapping (b2c-enum-a):
# 4 rows -> metadata_engagement_id (hourly/milestone/percentage/outsourced)
# 3 rows -> manual_review (apprentice/investor/operator_self)
# saas_subscription -> stripe_customer_link_lookup
# rpp_vendor        -> rpp_payout_attribution (FORWARD-CHARTER)
# one_off_invoice   -> metadata_billing_plane
EXPECTED_RESOLUTION_STRATEGY_BY_ID: dict[str, str] = {
    "eng_model_hourly_consultant":      "metadata_engagement_id",
    "eng_model_milestone_consultant":   "metadata_engagement_id",
    "eng_model_percentage_collaborator": "metadata_engagement_id",
    "eng_model_apprentice_learner":     "manual_review",
    "eng_model_investor_advisor":       "manual_review",
    "eng_model_outsourced_helper":      "metadata_engagement_id",
    "eng_model_operator_self":          "manual_review",
    "eng_model_saas_subscription":      "stripe_customer_link_lookup",
    "eng_model_rpp_vendor":             "rpp_payout_attribution",
    "eng_model_one_off_invoice":        "metadata_billing_plane",
}


def _read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_csv_exists():
    assert CSV_PATH.is_file(), f"canonical CSV missing at {CSV_PATH}"


def test_csv_header_matches_fieldnames_tuple():
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)
    assert tuple(header) == ENGAGEMENT_MODEL_FIELDNAMES, (
        "ENGAGEMENT_MODEL_REGISTRY.csv header drifted from ENGAGEMENT_MODEL_FIELDNAMES SSOT tuple"
    )


def test_csv_column_count_is_17():
    """B-2c (D-IH-81-X) bumped schema 16->17 by appending
    `counterparty_resolution_strategy`. Pre-B-2c the schema was 16 columns
    (matched sibling ENGAGEMENT_REGISTRY.csv); post-B-2c it carries the
    routing-strategy column the FINOPS resolver consumes.
    """
    assert len(ENGAGEMENT_MODEL_FIELDNAMES) == 17, (
        f"expected 17-column schema (B-2c D-IH-81-X); got {len(ENGAGEMENT_MODEL_FIELDNAMES)}"
    )


def test_counterparty_resolution_strategy_is_last_column():
    """B-2c (D-IH-81-X) — col was appended at position 17 (last)."""
    assert ENGAGEMENT_MODEL_FIELDNAMES[-1] == "counterparty_resolution_strategy"


def test_seven_classes_present():
    rows = _read_rows()
    ids = {(r.get("engagement_model_id") or "").strip() for r in rows}
    assert set(EXPECTED_CLASSES) <= ids, (
        f"D-IH-73-D 7-class taxonomy incomplete; missing {set(EXPECTED_CLASSES) - ids}"
    )


def test_b2c_extension_classes_present():
    """B-2c (D-IH-81-X b2c-rows-c) — 3 new rows extending people-taxonomy
    to unified counterparty-routing taxonomy.
    """
    rows = _read_rows()
    ids = {(r.get("engagement_model_id") or "").strip() for r in rows}
    assert set(EXPECTED_B2C_EXTENSION_CLASSES) <= ids, (
        f"B-2c extension classes incomplete; missing "
        f"{set(EXPECTED_B2C_EXTENSION_CLASSES) - ids}"
    )


def test_total_class_count_is_ten():
    """7 original (D-IH-73-D) + 3 B-2c extensions (D-IH-81-X) = 10."""
    rows = _read_rows()
    assert len(rows) == 10, f"expected 10 rows (7 original + 3 B-2c); got {len(rows)}"


def test_every_row_carries_resolution_strategy_per_b2c_enum_a():
    """B-2c (D-IH-81-X b2c-enum-a) — every row's resolution strategy matches
    the operator-ratified mapping. NOT NULL invariant (col is required).
    """
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    errors: list[str] = []
    for eng_model_id, expected_strategy in EXPECTED_RESOLUTION_STRATEGY_BY_ID.items():
        actual = rows.get(eng_model_id, {}).get("counterparty_resolution_strategy", "")
        if actual != expected_strategy:
            errors.append(
                f"{eng_model_id}: expected {expected_strategy!r}, got {actual!r}"
            )
    assert not errors, "B-2c resolution-strategy drift:\n" + "\n".join(errors)


def test_all_resolution_strategies_in_enum():
    """Every row's counterparty_resolution_strategy is in
    VALID_COUNTERPARTY_RESOLUTION_STRATEGIES (NOT NULL invariant + enum-bound).
    """
    rows = _read_rows()
    for r in rows:
        strategy = r.get("counterparty_resolution_strategy", "")
        assert strategy, f"row {r['engagement_model_id']}: empty resolution strategy"
        assert strategy in VALID_COUNTERPARTY_RESOLUTION_STRATEGIES, (
            f"row {r['engagement_model_id']}: strategy {strategy!r} not in "
            f"{sorted(VALID_COUNTERPARTY_RESOLUTION_STRATEGIES)}"
        )


def test_every_row_pydantic_validates():
    rows = _read_rows()
    errors: list[str] = []
    for i, r in enumerate(rows, start=2):
        try:
            EngagementModelRow.model_validate({k: (v or "") for k, v in r.items() if k})
        except ValidationError as exc:
            errors.append(f"row {i}: {exc}")
    assert not errors, "Pydantic validation errors:\n" + "\n".join(errors)


def test_outsourced_helper_carries_d_ih_73_e_soc_posture():
    """D-IH-73-E: outsourced_helper carries low_trust SOC, access_level=1,
    work_product_scope_only knowledge, outsourced_workproduct_only IP clause."""
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    row = rows["eng_model_outsourced_helper"]
    assert row["soc_posture"] == "low_trust"
    assert row["access_level_default"] == "1"
    assert row["knowledge_access_level"] == "work_product_scope_only"
    assert row["ip_clause_class"] == "outsourced_workproduct_only"
    assert row["payment_cadence"] == "per_hour_capped"


def test_operator_self_carries_baseline_internal_posture():
    """D-IH-73-D operator baseline: operator_self carries internal SOC,
    access_level=6, full_internal knowledge, operator_owns_all IP clause."""
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    row = rows["eng_model_operator_self"]
    assert row["soc_posture"] == "internal"
    assert row["access_level_default"] == "6"
    assert row["knowledge_access_level"] == "full_internal"
    assert row["ip_clause_class"] == "operator_owns_all"
    assert row["payment_cadence"] == "none"


def test_apprentice_learner_carries_training_posture():
    """D-IH-73-K apprentice: training_only SOC, access_level=3 (Internal),
    training_curriculum_only knowledge, training_recipient IP clause."""
    rows = {(r["engagement_model_id"]).strip(): r for r in _read_rows()}
    row = rows["eng_model_apprentice_learner"]
    assert row["soc_posture"] == "training_only"
    assert row["access_level_default"] == "3"
    assert row["knowledge_access_level"] == "training_curriculum_only"
    assert row["ip_clause_class"] == "training_recipient"
    assert row["payment_cadence"] == "barter_continuous"


def test_all_status_values_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["status"] in VALID_STATUSES, (
            f"row {r['engagement_model_id']}: status {r['status']!r} not in {sorted(VALID_STATUSES)}"
        )


def test_all_retribution_patterns_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["retribution_pattern"] in VALID_RETRIBUTION_PATTERNS


def test_all_soc_postures_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["soc_posture"] in VALID_SOC_POSTURES


def test_all_ip_clause_classes_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["ip_clause_class"] in VALID_IP_CLAUSE_CLASSES


def test_all_knowledge_access_levels_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["knowledge_access_level"] in VALID_KNOWLEDGE_ACCESS_LEVELS


def test_all_payment_cadences_in_enum():
    rows = _read_rows()
    for r in rows:
        assert r["payment_cadence"] in VALID_PAYMENT_CADENCES


def _valid_payload_skeleton(**overrides: object) -> dict[str, object]:
    """B-2c (D-IH-81-X) — produces a minimum-VALID payload (all 17 cols populated)
    so negative tests can perturb exactly one field. Without this skeleton, every
    test would silently fail on "missing counterparty_resolution_strategy" rather
    than on the perturbed field's expected ValidationError.
    """
    base: dict[str, object] = {
        "engagement_model_id": "eng_model_test_baseline",
        "engagement_model_name": "Test",
        "retribution_pattern": "hourly",
        "retribution_unit": "hour",
        "typical_duration": "test",
        "access_level_default": "3",
        "soc_posture": "cleared",
        "ip_clause_class": "standard_consultant",
        "knowledge_access_level": "full_by_engagement",
        "onboarding_pattern": "x",
        "offboarding_pattern": "x",
        "payment_cadence": "per_hour",
        "legal_template_default": "x",
        "historical_examples": "",
        "status": "active",
        "notes": "",
        "counterparty_resolution_strategy": "metadata_engagement_id",
    }
    base.update(overrides)
    return base


def test_valid_payload_skeleton_passes():
    """Sanity: the skeleton itself MUST validate, otherwise negative tests are
    measuring the wrong thing (i.e. tripping on skeleton issues, not on the
    perturbation under test).
    """
    EngagementModelRow.model_validate(_valid_payload_skeleton())


def test_invalid_slug_rejected():
    """Slug must match ^eng_model_[a-z0-9_]+$; uppercase / no-prefix rejected."""
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(
            _valid_payload_skeleton(engagement_model_id="Bad-Slug")
        )


def test_invalid_enum_rejected():
    """Unknown retribution_pattern must be rejected by Literal type."""
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(
            _valid_payload_skeleton(
                engagement_model_id="eng_model_test_bad_enum",
                retribution_pattern="not_a_valid_pattern",
            )
        )


def test_invalid_access_level_rejected():
    """access_level_default must be int 0-6; 7 is rejected (Secret+1 out of range)."""
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(
            _valid_payload_skeleton(
                engagement_model_id="eng_model_test_bad_access",
                access_level_default="7",
            )
        )


def test_invalid_resolution_strategy_rejected():
    """B-2c (D-IH-81-X) — unknown counterparty_resolution_strategy is rejected
    by the Literal type. NOT NULL invariant enforced by the field being
    required (no default).
    """
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(
            _valid_payload_skeleton(
                engagement_model_id="eng_model_test_bad_strategy",
                counterparty_resolution_strategy="not_a_valid_strategy",
            )
        )


def test_missing_resolution_strategy_rejected():
    """B-2c (D-IH-81-X) — NOT NULL invariant: omitting
    `counterparty_resolution_strategy` raises ValidationError (no default).
    """
    payload = _valid_payload_skeleton(
        engagement_model_id="eng_model_test_missing_strategy"
    )
    del payload["counterparty_resolution_strategy"]
    with pytest.raises(ValidationError):
        EngagementModelRow.model_validate(payload)


def test_validator_script_exits_zero():
    """End-to-end: the validator CLI exits 0 on the canonical CSV."""
    if not VALIDATOR_PATH.is_file():
        pytest.skip(f"validator script not present at {VALIDATOR_PATH}")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"validator failed (exit={result.returncode}):\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
