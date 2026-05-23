"""Tests for akos.hlk_finops_ledger SSOT + scripts/validate_finops_ledger.py validator.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).

Covers:
- SSOT module constants: 14-column tuple + 3 enum frozensets present + non-empty.
- Pydantic RegisteredFactRow accepts valid rows + rejects invalid rows
  (counterparty_id slug, currency enum, fact_type enum, fx_source enum,
   amount_minor non-negative, effective_date ISO format).
- Validator script (scripts/validate_finops_ledger.py) exits 0 against synthetic facts.
- Validator script exits 0 in --strict mode when synthetic facts are clean (B-2a baseline).

These tests run under the default `py scripts/test.py all` collection via the implicit
`tests/test_*.py` glob.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_finops_ledger import (  # noqa: E402
    REGISTERED_FACT_FIELDNAMES,
    VALID_CURRENCY_CODES,
    VALID_FACT_TYPES,
    VALID_FX_SOURCES,
    VALID_RESOLUTION_STRATEGIES,
    RegisteredFactRow,
)


# -----------------------------------------------------------------------------
# SSOT constants
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestSsotConstants:
    def test_registered_fact_fieldnames_has_14_columns(self) -> None:
        assert len(REGISTERED_FACT_FIELDNAMES) == 14

    def test_registered_fact_fieldnames_contains_b2a_extensions(self) -> None:
        # B-2a added: amount_minor_eur, fx_rate_ecb, fx_rate_stripe, fx_source
        for col in ("amount_minor_eur", "fx_rate_ecb", "fx_rate_stripe", "fx_source"):
            assert col in REGISTERED_FACT_FIELDNAMES, f"Missing B-2a column: {col}"

    def test_valid_fact_types_non_empty(self) -> None:
        assert len(VALID_FACT_TYPES) >= 10  # I19 originals + B-2 Stripe extensions

    def test_valid_fx_sources_non_empty(self) -> None:
        assert len(VALID_FX_SOURCES) == 5

    def test_valid_resolution_strategies_non_empty(self) -> None:
        assert len(VALID_RESOLUTION_STRATEGIES) == 5

    def test_valid_currency_codes_non_empty(self) -> None:
        assert "EUR" in VALID_CURRENCY_CODES
        assert "USD" in VALID_CURRENCY_CODES


# -----------------------------------------------------------------------------
# Pydantic row validation
# -----------------------------------------------------------------------------


def _valid_row(**overrides) -> dict:
    base = {
        "counterparty_id": "finops_stripe",
        "stripe_customer_id": None,
        "stripe_subscription_id": None,
        "fact_type": "reconciliation_snapshot",
        "currency": "EUR",
        "amount_minor": 5000,
        "amount_minor_eur": 5000,
        "effective_date": "2026-05-23",
        "fx_rate_ecb": None,
        "fx_rate_stripe": None,
        "fx_source": "identity_eur",
        "metadata": {},
        "source_reference": "test:synthetic",
    }
    base.update(overrides)
    return base


@pytest.mark.unit
class TestRegisteredFactRowValid:
    def test_valid_eur_native_row(self) -> None:
        row = RegisteredFactRow.model_validate(_valid_row())
        assert row.currency == "EUR"

    def test_valid_usd_with_fx(self) -> None:
        row = RegisteredFactRow.model_validate(_valid_row(
            currency="USD",
            amount_minor=10000,
            amount_minor_eur=9302,
            fx_rate_ecb="0.93020000",
            fx_source="ecb_daily",
        ))
        assert row.fx_source == "ecb_daily"

    def test_unresolved_counterparty_id_sentinel_accepted(self) -> None:
        row = RegisteredFactRow.model_validate(_valid_row(counterparty_id="UNRESOLVED"))
        assert row.counterparty_id == "UNRESOLVED"

    def test_stripe_charge_succeeded_fact_type(self) -> None:
        row = RegisteredFactRow.model_validate(_valid_row(
            fact_type="charge_succeeded",
            stripe_customer_id="cus_test_123",
        ))
        assert row.fact_type == "charge_succeeded"


@pytest.mark.unit
class TestRegisteredFactRowInvalid:
    def test_invalid_counterparty_id_slug(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(counterparty_id="HasUpperCase"))

    def test_invalid_currency(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(currency="ZWD"))

    def test_invalid_fact_type(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(fact_type="bogus_type"))

    def test_invalid_fx_source(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(fx_source="oracle_db"))

    def test_negative_amount_minor(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(amount_minor=-100))

    def test_invalid_effective_date_format(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(effective_date="May 23, 2026"))

    def test_missing_source_reference(self) -> None:
        with pytest.raises(ValidationError):
            RegisteredFactRow.model_validate(_valid_row(source_reference=""))


# -----------------------------------------------------------------------------
# Validator CLI smoke
# -----------------------------------------------------------------------------


class TestValidatorCli:
    def test_validator_exits_zero_default_mode(self) -> None:
        """Validator runs clean against synthetic facts in default (INFO) mode."""
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate_finops_ledger.py")],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        assert "PASS" in result.stdout or "INFO" in result.stdout

    def test_validator_exits_zero_strict_mode(self) -> None:
        """Validator runs clean against synthetic facts in --strict mode (B-2a baseline)."""
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate_finops_ledger.py"), "--strict"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        assert "PASS" in result.stdout
