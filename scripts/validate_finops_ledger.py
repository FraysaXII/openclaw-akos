#!/usr/bin/env python3
"""Validate FINOPS ledger Pydantic contract + counterparty resolution + FX snapshot logic.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).

This validator exercises akos.hlk_finops_ledger.RegisteredFactRow + resolve_counterparty_id() +
compute_fx_snapshot() against a synthetic fact stream (representative Stripe webhook events +
counterparty resolution + FX conversion ladder) to ensure the Python SSOT is self-consistent
before the Edge Function worker (Bundle B-2b) goes live.

Per CONTRIBUTING.md Python Code Standards. Per akos-holistika-operations.mdc validator pattern.

Unlike most validators in scripts/validate_*.py which exercise canonical CSV rows, this validator
has NO canonical CSV input — finops.registered_fact is an operational database table, not git SSOT.
The validator instead runs the synthetic-fact suite to verify schema invariants + tests that the
FK to FINOPS_COUNTERPARTY_REGISTER.csv resolves for representative cases.

Usage:
    py scripts/validate_finops_ledger.py
    py scripts/validate_finops_ledger.py --strict   # exit non-zero on warnings

Per R5 (release-gate INFO ramp): runs at INFO until Bundle B-2c lands; promotes to FAIL after
synthetic fact + live Stripe AT round-trip succeeds in production (per D-IH-81-W closure).

See:
- ``akos/hlk_finops_ledger.py`` for the Pydantic SSOT this validator exercises.
- ``akos/hlk_fx_rate.py`` for the FX cache lookup + fallback ladder helpers.
- ``akos/hlk_ops_register_emit.py`` for the OPS_REGISTER emit shape this validator round-trips.
- ``tests/test_validate_finops_ledger.py`` for the assertions backing this validator.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from akos.hlk_finops_ledger import (
    REGISTERED_FACT_FIELDNAMES,
    VALID_FACT_TYPES,
    VALID_FX_SOURCES,
    VALID_RESOLUTION_STRATEGIES,
    RegisteredFactRow,
    compute_fx_snapshot,
    resolve_counterparty_id,
)
from akos.hlk_fx_rate import (
    apply_fx_fallback_ladder,
    convert_eur_base_to_src_to_eur,
    detect_fx_divergence,
)
from akos.hlk_ops_register_emit import OPS_REGISTER_FIELDNAMES, emit_ops_register_row
from akos.io import REPO_ROOT

# Canonical CSV location (post-I81 P2 T1 move per D-IH-81-Q)
HLK_COMPLIANCE = REPO_ROOT / "docs" / "references" / "hlk" / "v3.0" / "Admin" / "O5-1" / "People" / "Compliance" / "canonicals"
FINOPS_COUNTERPARTY_CSV = HLK_COMPLIANCE / "finops" / "FINOPS_COUNTERPARTY_REGISTER.csv"
_FINOPS_COUNTERPARTY_CSV_LEGACY = HLK_COMPLIANCE / "FINOPS_COUNTERPARTY_REGISTER.csv"
if not FINOPS_COUNTERPARTY_CSV.is_file() and _FINOPS_COUNTERPARTY_CSV_LEGACY.is_file():
    FINOPS_COUNTERPARTY_CSV = _FINOPS_COUNTERPARTY_CSV_LEGACY


def _load_counterparty_slugs() -> set[str]:
    """Return all counterparty_id slugs in FINOPS_COUNTERPARTY_REGISTER.csv (for FK validation)."""
    if not FINOPS_COUNTERPARTY_CSV.is_file():
        return set()
    with open(FINOPS_COUNTERPARTY_CSV, encoding="utf-8", newline="") as f:
        return {r["counterparty_id"].strip() for r in csv.DictReader(f) if r.get("counterparty_id")}


def _synthetic_facts() -> list[dict[str, Any]]:
    """Return representative synthetic facts covering each fact_type + FX scenario."""
    # Synthetic counterparty_id slugs MUST exist in FINOPS_COUNTERPARTY_REGISTER.csv (finops_* prefix
    # per the canonical slug convention seeded at Bundle B-1, D-IH-81-U); if synthetic slugs drift from
    # the register, --strict mode fails the FK check.
    return [
        # EUR-native fact (no FX conversion)
        {
            "counterparty_id": "finops_stripe",
            "stripe_customer_id": "cus_test_eur",
            "stripe_subscription_id": None,
            "fact_type": "charge_succeeded",
            "currency": "EUR",
            "amount_minor": 5000,
            "amount_minor_eur": 5000,
            "effective_date": "2026-05-23",
            "fx_rate_ecb": None,
            "fx_rate_stripe": None,
            "fx_source": "identity_eur",
            "metadata": {"hlk_billing_plane": "holistika"},
            "source_reference": "stripe_event:evt_synthetic_eur",
        },
        # USD fact (ECB conversion)
        {
            "counterparty_id": "finops_openai",
            "stripe_customer_id": None,
            "stripe_subscription_id": None,
            "fact_type": "invoice_paid",
            "currency": "USD",
            "amount_minor": 10000,
            "amount_minor_eur": 9302,
            "effective_date": "2026-05-23",
            "fx_rate_ecb": "0.93020000",
            "fx_rate_stripe": "0.93100000",
            "fx_source": "ecb_daily",
            "metadata": {"source": "operator_reconciliation"},
            "source_reference": "operator_reconciliation:OpenAI-May2026",
        },
        # Reconciliation snapshot (non-Stripe; budget_line family)
        {
            "counterparty_id": "finops_at_pymes",
            "stripe_customer_id": None,
            "stripe_subscription_id": None,
            "fact_type": "contract_value_estimate",
            "currency": "EUR",
            "amount_minor": 250000,
            "amount_minor_eur": 250000,
            "effective_date": "2026-05-23",
            "fx_rate_ecb": None,
            "fx_rate_stripe": None,
            "fx_source": "identity_eur",
            "metadata": {"contract_ref": "AT-Pymes-Layer-a-2026-Q2-engagement"},
            "source_reference": "contract_doc:./AT-Pymes-engagement-2026-Q2.pdf",
        },
        # UNRESOLVED counterparty (failed resolution → manual review)
        {
            "counterparty_id": "UNRESOLVED",
            "stripe_customer_id": "cus_test_unknown",
            "stripe_subscription_id": None,
            "fact_type": "charge_succeeded",
            "currency": "USD",
            "amount_minor": 1000,
            "amount_minor_eur": 930,
            "effective_date": "2026-05-23",
            "fx_rate_ecb": "0.93020000",
            "fx_rate_stripe": None,
            "fx_source": "ecb_daily",
            "metadata": {},
            "source_reference": "stripe_event:evt_synthetic_unresolved",
        },
    ]


def _validate_synthetic_facts() -> tuple[int, list[str]]:
    """Validate each synthetic fact against RegisteredFactRow + FK to FINOPS_COUNTERPARTY_REGISTER."""
    errors: list[str] = []
    facts = _synthetic_facts()
    counterparty_slugs = _load_counterparty_slugs()

    for i, fact in enumerate(facts, start=1):
        try:
            RegisteredFactRow.model_validate(fact)
        except Exception as exc:
            errors.append(f"synthetic fact #{i}: Pydantic validation failed: {exc}")
            continue

        cp_id = fact["counterparty_id"]
        if cp_id != "UNRESOLVED" and counterparty_slugs and cp_id not in counterparty_slugs:
            errors.append(
                f"synthetic fact #{i}: counterparty_id {cp_id!r} not present in FINOPS_COUNTERPARTY_REGISTER.csv "
                f"(loaded {len(counterparty_slugs)} slugs)"
            )

    return len(facts), errors


def _validate_resolve_counterparty_id() -> list[str]:
    """Exercise the 4-strategy resolution ladder."""
    errors: list[str] = []

    # Strategy 1: metadata_engagement_id (highest confidence)
    result = resolve_counterparty_id(
        stripe_customer_id="cus_test_1",
        stripe_metadata={"hlk_engagement_id": "rcdlegal"},
    )
    if result.strategy_used != "metadata_engagement_id" or result.confidence != "high":
        errors.append(f"Strategy 1 (engagement_id) failed: {result}")

    # Strategy 2: metadata_billing_plane (medium)
    result = resolve_counterparty_id(
        stripe_customer_id="cus_test_2",
        stripe_metadata={"hlk_billing_plane": "openai"},
    )
    if result.strategy_used != "metadata_billing_plane" or result.confidence != "medium":
        errors.append(f"Strategy 2 (billing_plane) failed: {result}")

    # Strategy 2 sentinel: 'holistika' / 'kirbe' should fall through
    result = resolve_counterparty_id(
        stripe_customer_id="cus_test_3",
        stripe_metadata={"hlk_billing_plane": "holistika"},
    )
    if result.counterparty_id != "UNRESOLVED":
        errors.append(f"Strategy 2 'holistika' sentinel should fall through to UNRESOLVED: {result}")

    # Strategy 3: stripe_customer_link_lookup
    result = resolve_counterparty_id(
        stripe_customer_id="cus_test_4",
        stripe_metadata={},
    )
    if result.strategy_used != "stripe_customer_link_lookup":
        errors.append(f"Strategy 3 (stripe_customer_link_lookup) failed: {result}")
    if result.ops_register_payload is None:
        errors.append(f"Strategy 3 should emit ops_register_payload hint: {result}")

    # Strategy 4: manual_review (no inputs)
    result = resolve_counterparty_id(stripe_customer_id=None, stripe_metadata=None)
    if result.strategy_used != "manual_review" or result.confidence != "unresolved":
        errors.append(f"Strategy 4 (manual_review) failed: {result}")
    if result.ops_register_payload is None or result.ops_register_payload.get("severity") != "high":
        errors.append(f"Strategy 4 should emit high-severity OPS payload: {result}")

    return errors


def _validate_fx_snapshot() -> list[str]:
    """Exercise the FX snapshot computation + fallback ladder."""
    errors: list[str] = []

    # EUR-native (identity)
    snap = compute_fx_snapshot(amount_minor=5000, currency="EUR", effective_date="2026-05-23")
    if snap.fx_source != "identity_eur" or snap.amount_minor_eur != 5000:
        errors.append(f"EUR identity failed: {snap}")

    # USD with ECB cache hit
    lookup = {("USD/EUR", "2026-05-23"): "0.92500000"}
    snap = compute_fx_snapshot(amount_minor=10000, currency="USD", effective_date="2026-05-23", ecb_rate_lookup=lookup)
    if snap.fx_source != "ecb_daily" or snap.amount_minor_eur != 9250:
        errors.append(f"USD ecb_daily failed: {snap}")

    # USD with previous-day fallback
    lookup = {("USD/EUR", "2026-05-22"): "0.92500000"}
    snap = compute_fx_snapshot(amount_minor=10000, currency="USD", effective_date="2026-05-23", ecb_rate_lookup=lookup)
    if snap.fx_source != "ecb_previous_day_fallback" or snap.amount_minor_eur != 9250:
        errors.append(f"USD previous-day-fallback failed: {snap}")

    # USD with Stripe fallback (ECB unavailable)
    snap = compute_fx_snapshot(
        amount_minor=10000, currency="USD", effective_date="2026-05-23", ecb_rate_lookup={},
        stripe_fx_quote="0.93000000",
    )
    if snap.fx_source != "stripe_fx_quote" or snap.amount_minor_eur != 9300:
        errors.append(f"USD stripe_fx_quote failed: {snap}")

    # None amount_minor (non-amount metadata fact)
    snap = compute_fx_snapshot(amount_minor=None, currency="USD", effective_date="2026-05-23")
    if snap.amount_minor_eur is not None:
        errors.append(f"None amount should produce None EUR: {snap}")

    return errors


def _validate_fallback_ladder() -> list[str]:
    """Exercise the apply_fx_fallback_ladder ladder semantics."""
    errors: list[str] = []

    # EUR identity
    res = apply_fx_fallback_ladder("EUR", "2026-05-23", {})
    if res.source != "identity_eur":
        errors.append(f"EUR ladder identity failed: {res}")

    # Walk-back fallback (7 days)
    lookup = {("USD/EUR", "2026-05-16"): "0.92000000"}
    res = apply_fx_fallback_ladder("USD", "2026-05-23", lookup, max_ecb_lookback_days=7)
    if res.source != "ecb_previous_day_fallback" or res.days_behind != 7:
        errors.append(f"7-day walk-back failed: {res}")

    # Beyond lookback window — should fall to Stripe
    lookup = {("USD/EUR", "2026-05-10"): "0.92000000"}  # 13 days ago
    res = apply_fx_fallback_ladder("USD", "2026-05-23", lookup, stripe_fx_quote="0.93", max_ecb_lookback_days=7)
    if res.source != "stripe_fx_quote":
        errors.append(f"Beyond-lookback Stripe fallback failed: {res}")

    # No matches at all
    res = apply_fx_fallback_ladder("USD", "2026-05-23", {})
    if res.source != "unavailable":
        errors.append(f"No-match unavailable failed: {res}")

    return errors


def _validate_fx_divergence_detector() -> list[str]:
    """Exercise FX divergence detection at the 0.5% threshold."""
    errors: list[str] = []

    # Tight match (no divergence)
    diverges, pct = detect_fx_divergence("0.93000000", "0.93100000")
    if diverges:
        errors.append(f"Tight match should not diverge: {pct}%")

    # Wide divergence (>0.5%)
    diverges, pct = detect_fx_divergence("0.93000000", "0.94000000")
    if not diverges:
        errors.append(f"1% divergence should fire: {pct}%")

    # One side None → no divergence
    diverges, _ = detect_fx_divergence("0.93000000", None)
    if diverges:
        errors.append("None rate should not produce divergence")

    return errors


def _validate_eur_base_inversion() -> list[str]:
    """Verify ECB EUR-base → SRC/EUR inversion is correct."""
    errors: list[str] = []
    # USD example: ECB says 1 EUR = 1.075 USD → 1 USD = 0.93023 EUR
    result = convert_eur_base_to_src_to_eur("1.075")
    expected = "0.93023256"
    if result != expected:
        errors.append(f"USD inversion: expected {expected}, got {result}")
    return errors


def _validate_ops_register_emit() -> list[str]:
    """Round-trip an OPS_REGISTER row through emit_ops_register_row()."""
    errors: list[str] = []
    try:
        row = emit_ops_register_row(
            ops_action_id="OPS-81-99",
            originating_initiative_id="INIT-OPENCLAW_AKOS-81",
            owner_class="system",
            owner_role="Business Controller",
            summary="Synthetic OPS row from validator round-trip",
            linked_decision_ids="D-IH-81-V",
            rice_reach="1", rice_impact="2", rice_confidence_pct="100", rice_effort_person_weeks="1",
        )
        if set(row.keys()) != set(OPS_REGISTER_FIELDNAMES):
            errors.append(f"emit_ops_register_row keys mismatch OPS_REGISTER_FIELDNAMES")
        if not row.get("rice_score"):
            errors.append("rice_score should be computed when all components present")
    except Exception as exc:
        errors.append(f"emit_ops_register_row round-trip failed: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings (default: INFO).")
    args = parser.parse_args()

    print("\n  FINOPS Ledger Validator (B-2a substrate)")
    print("  " + "=" * 40)

    # Self-checks on fieldnames / enums (Pydantic SSOT integrity)
    if len(REGISTERED_FACT_FIELDNAMES) != 14:
        print(f"  FAIL: REGISTERED_FACT_FIELDNAMES has {len(REGISTERED_FACT_FIELDNAMES)} cols; expected 14")
        return 1

    if not VALID_FX_SOURCES or not VALID_RESOLUTION_STRATEGIES or not VALID_FACT_TYPES:
        print("  FAIL: enum frozensets are empty")
        return 1

    if len(OPS_REGISTER_FIELDNAMES) != 24:
        print(f"  FAIL: OPS_REGISTER_FIELDNAMES has {len(OPS_REGISTER_FIELDNAMES)} cols; expected 24")
        return 1

    print(f"  REGISTERED_FACT_FIELDNAMES: {len(REGISTERED_FACT_FIELDNAMES)} columns (14 expected)")
    print(f"  VALID_FACT_TYPES: {len(VALID_FACT_TYPES)} enum values")
    print(f"  VALID_FX_SOURCES: {len(VALID_FX_SOURCES)} enum values")
    print(f"  VALID_RESOLUTION_STRATEGIES: {len(VALID_RESOLUTION_STRATEGIES)} enum values")

    n_facts, fact_errors = _validate_synthetic_facts()
    print(f"  Synthetic facts validated: {n_facts}")

    resolve_errors = _validate_resolve_counterparty_id()
    fx_snap_errors = _validate_fx_snapshot()
    ladder_errors = _validate_fallback_ladder()
    div_errors = _validate_fx_divergence_detector()
    eur_inv_errors = _validate_eur_base_inversion()
    ops_emit_errors = _validate_ops_register_emit()

    all_errors = (
        fact_errors + resolve_errors + fx_snap_errors + ladder_errors
        + div_errors + eur_inv_errors + ops_emit_errors
    )

    if all_errors:
        print(f"\n  Errors ({len(all_errors)}):")
        for e in all_errors:
            print(f"    - {e}")
        if args.strict:
            return 1
        else:
            print("\n  INFO mode: errors surfaced but not failing CI (per D-IH-81-V INFO ramp).")
            print("  Promote to FAIL after Bundle B-2c lands + live Stripe AT round-trip succeeds.")
            return 0

    print("\n  PASS: all synthetic facts + resolution strategies + FX ladder + OPS emit round-tripped clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
