"""Tests for akos.hlk_finops_ledger.resolve_counterparty_id + compute_fx_snapshot.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).

Per R1 (engagement-model-aware router) + R2 (ECB+Stripe FX snapshot) in the Bundle B-2
architecture report.

Coverage:
- resolve_counterparty_id: 4 resolution strategies + unresolved sentinel + OPS payload
- compute_fx_snapshot: EUR-native + ECB-hit + Stripe-fallback + unavailable paths
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_finops_ledger import (  # noqa: E402
    compute_fx_snapshot,
    resolve_counterparty_id,
)


# -----------------------------------------------------------------------------
# resolve_counterparty_id — strategy ladder
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestResolveCounterpartyId:
    def test_metadata_engagement_id_high_confidence(self) -> None:
        result = resolve_counterparty_id(
            stripe_customer_id="cus_test_001",
            stripe_metadata={"hlk_engagement_id": "ENG-2026-CLI-001"},
        )
        assert result.strategy_used == "metadata_engagement_id"
        assert result.confidence == "high"
        assert result.counterparty_id != "UNRESOLVED"
        assert result.ops_register_payload is None

    def test_metadata_billing_plane_medium_confidence(self) -> None:
        # billing_plane carries counterparty slug directly (e.g. real consultancy slug).
        # 'kirbe' / 'holistika' are sentinel values that fall through; use a real-shaped slug.
        result = resolve_counterparty_id(
            stripe_customer_id="cus_test_002",
            stripe_metadata={"hlk_billing_plane": "openai_subscription"},
        )
        assert result.strategy_used == "metadata_billing_plane"
        # Per impl: billing_plane = medium confidence (engagement_id = high)
        assert result.confidence == "medium"

    def test_stripe_customer_link_lookup_path(self) -> None:
        # cus_-prefixed customer id with no metadata routes to stripe_customer_link lookup
        # (low confidence; emits OPS payload signaling worker should perform SQL lookup)
        result = resolve_counterparty_id(
            stripe_customer_id="cus_orphan_999",
            stripe_metadata={},
        )
        assert result.strategy_used == "stripe_customer_link_lookup"
        assert result.confidence == "low"
        assert result.counterparty_id == "UNRESOLVED"
        assert result.ops_register_payload is not None
        # OPS payload uses 'ops_class' per implementation
        assert "ops_class" in result.ops_register_payload

    def test_manual_review_when_no_inputs(self) -> None:
        # Only triggers manual_review when neither metadata nor stripe_customer_id provides a hook
        result = resolve_counterparty_id(
            stripe_customer_id=None,
            stripe_metadata=None,
        )
        assert result.strategy_used == "manual_review"
        assert result.confidence == "unresolved"
        assert result.counterparty_id == "UNRESOLVED"
        assert result.ops_register_payload is not None
        assert result.ops_register_payload.get("severity") == "high"

    def test_billing_plane_sentinels_fall_through(self) -> None:
        # 'holistika' and 'kirbe' are sentinel routes (not counterparty slugs); fall to next tier
        result = resolve_counterparty_id(
            stripe_customer_id=None,
            stripe_metadata={"hlk_billing_plane": "holistika"},
        )
        # No cus_id either → falls all the way to manual_review
        assert result.counterparty_id == "UNRESOLVED"
        assert result.strategy_used == "manual_review"

    def test_metadata_takes_precedence_over_lookup(self) -> None:
        # If metadata has engagement_id, it should win over any other resolution path
        result = resolve_counterparty_id(
            stripe_customer_id="cus_test_xyz",
            stripe_metadata={
                "hlk_engagement_id": "ENG-PRIORITY",
                "hlk_billing_plane": "kirbe_saas",
            },
        )
        assert result.strategy_used == "metadata_engagement_id"

    def test_engagement_model_id_hint_accepted(self) -> None:
        # When caller pre-resolves the engagement_model, function should accept the hint
        result = resolve_counterparty_id(
            stripe_customer_id="cus_test_003",
            stripe_metadata={"hlk_engagement_id": "ENG-2026-SAAS-001"},
            engagement_model_id="eng_model_saas_subscription",
        )
        assert result.confidence in ("high", "medium")


# -----------------------------------------------------------------------------
# compute_fx_snapshot — currency conversion
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestComputeFxSnapshot:
    def test_eur_native_no_fx_lookup(self) -> None:
        snap = compute_fx_snapshot(
            amount_minor=5000,
            currency="EUR",
            effective_date="2026-05-23",
        )
        assert snap.fx_source == "identity_eur"
        assert snap.amount_minor_eur == 5000
        assert snap.fx_rate_ecb is None
        assert snap.fx_rate_stripe is None

    def test_usd_with_ecb_lookup(self) -> None:
        snap = compute_fx_snapshot(
            amount_minor=10000,  # $100 USD
            currency="USD",
            effective_date="2026-05-23",
            ecb_rate_lookup={("USD/EUR", "2026-05-23"): "0.93020000"},
        )
        assert snap.fx_source == "ecb_daily"
        assert snap.fx_rate_ecb == "0.93020000"
        # 10000 minor * 0.9302 ≈ 9302 minor EUR
        assert snap.amount_minor_eur == 9302

    def test_usd_with_stripe_fallback(self) -> None:
        snap = compute_fx_snapshot(
            amount_minor=10000,
            currency="USD",
            effective_date="2026-05-23",
            ecb_rate_lookup={},
            stripe_fx_quote="0.93000000",
        )
        assert snap.fx_source == "stripe_fx_quote"
        assert snap.fx_rate_stripe == "0.93000000"
        assert snap.amount_minor_eur == 9300

    def test_ecb_and_stripe_both_recorded(self) -> None:
        # When both are available, ECB should be authoritative AND Stripe captured in sidecar
        snap = compute_fx_snapshot(
            amount_minor=10000,
            currency="USD",
            effective_date="2026-05-23",
            ecb_rate_lookup={("USD/EUR", "2026-05-23"): "0.93020000"},
            stripe_fx_quote="0.93100000",
        )
        assert snap.fx_source == "ecb_daily"
        assert snap.fx_rate_ecb == "0.93020000"
        # Stripe rate recorded in sidecar even when ECB wins
        assert snap.fx_rate_stripe == "0.93100000"

    def test_usd_no_source_signals_manual_override_sentinel(self) -> None:
        # When neither ECB nor Stripe quote available, impl returns manual_override sentinel
        # so caller can decide whether to write UNRESOLVED or raise (per impl §5 Tier 3 comment)
        snap = compute_fx_snapshot(
            amount_minor=10000,
            currency="USD",
            effective_date="2026-05-23",
            ecb_rate_lookup={},
        )
        assert snap.amount_minor_eur is None
        assert snap.fx_source == "manual_override"

    def test_null_amount_returns_null_eur(self) -> None:
        snap = compute_fx_snapshot(
            amount_minor=None,
            currency="USD",
            effective_date="2026-05-23",
            ecb_rate_lookup={("USD/EUR", "2026-05-23"): "0.93020000"},
        )
        assert snap.amount_minor_eur is None

    def test_previous_day_ecb_fallback_one_day_back(self) -> None:
        # compute_fx_snapshot Tier 2 only checks effective_date - 1 day (exact yesterday)
        # for arbitrary lookback windows use apply_fx_fallback_ladder (tested in test_hlk_fx_rate.py)
        snap = compute_fx_snapshot(
            amount_minor=10000,
            currency="USD",
            effective_date="2026-05-23",
            ecb_rate_lookup={("USD/EUR", "2026-05-22"): "0.92000000"},  # 1 day behind
        )
        assert snap.fx_source == "ecb_previous_day_fallback"
        assert snap.fx_rate_ecb == "0.92000000"
