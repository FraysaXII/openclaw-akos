"""Tests for akos.hlk_fx_rate — ECB XML parser + Stripe FX Quote fallback ladder.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).

Per R2 (ECB-authoritative + Stripe FX Quote sidecar) in the Bundle B-2 architecture report.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from akos.hlk_fx_rate import (  # noqa: E402
    EcbDailyRates,
    apply_fx_fallback_ladder,
    convert_eur_base_to_src_to_eur,
    detect_fx_divergence,
    ecb_rates_to_holistika_pairs,
    parse_ecb_daily_xml,
)


# -----------------------------------------------------------------------------
# Sample ECB daily feed XML (truncated, representative)
# -----------------------------------------------------------------------------

_SAMPLE_ECB_XML = """<?xml version="1.0" encoding="UTF-8"?>
<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
  <gesmes:subject>Reference rates</gesmes:subject>
  <gesmes:Sender>
    <gesmes:name>European Central Bank</gesmes:name>
  </gesmes:Sender>
  <Cube>
    <Cube time="2026-05-23">
      <Cube currency="USD" rate="1.0750"/>
      <Cube currency="GBP" rate="0.8520"/>
      <Cube currency="CHF" rate="0.9650"/>
      <Cube currency="JPY" rate="165.50"/>
    </Cube>
  </Cube>
</gesmes:Envelope>
"""


# -----------------------------------------------------------------------------
# ECB XML parsing
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestParseEcbXml:
    def test_parses_effective_date(self) -> None:
        result = parse_ecb_daily_xml(_SAMPLE_ECB_XML)
        assert result.effective_date == "2026-05-23"

    def test_parses_all_currencies(self) -> None:
        result = parse_ecb_daily_xml(_SAMPLE_ECB_XML)
        assert "USD" in result.rates
        assert "GBP" in result.rates
        assert "CHF" in result.rates
        assert "JPY" in result.rates
        assert result.rates["USD"] == "1.0750"

    def test_malformed_xml_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_ecb_daily_xml("not valid xml")

    def test_xml_missing_time_cube_raises(self) -> None:
        bad_xml = "<?xml version='1.0'?><root></root>"
        with pytest.raises(ValueError):
            parse_ecb_daily_xml(bad_xml)


# -----------------------------------------------------------------------------
# Holistika-format conversion
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestEurBaseInversion:
    def test_usd_inversion(self) -> None:
        # ECB: 1 EUR = 1.075 USD  →  1 USD = 0.93023... EUR
        result = convert_eur_base_to_src_to_eur("1.075")
        assert result == "0.93023256"

    def test_gbp_inversion(self) -> None:
        # ECB: 1 EUR = 0.85 GBP  →  1 GBP = 1.17647... EUR
        result = convert_eur_base_to_src_to_eur("0.85")
        assert result == "1.17647059"

    def test_zero_rate_raises(self) -> None:
        with pytest.raises(ValueError):
            convert_eur_base_to_src_to_eur("0")

    def test_negative_rate_raises(self) -> None:
        with pytest.raises(ValueError):
            convert_eur_base_to_src_to_eur("-1.0")

    def test_non_numeric_raises(self) -> None:
        with pytest.raises(ValueError):
            convert_eur_base_to_src_to_eur("not_a_number")


@pytest.mark.unit
class TestEcbToHolistikaPairs:
    def test_default_base_currencies(self) -> None:
        ecb = parse_ecb_daily_xml(_SAMPLE_ECB_XML)
        pairs = ecb_rates_to_holistika_pairs(ecb)
        # Should include EUR/EUR identity + USD/EUR + GBP/EUR + CHF/EUR (default)
        assert ("EUR/EUR", "2026-05-23") in pairs
        assert ("USD/EUR", "2026-05-23") in pairs
        assert ("GBP/EUR", "2026-05-23") in pairs
        assert ("CHF/EUR", "2026-05-23") in pairs
        # JPY not in default list
        assert ("JPY/EUR", "2026-05-23") not in pairs

    def test_eur_identity_is_one(self) -> None:
        ecb = parse_ecb_daily_xml(_SAMPLE_ECB_XML)
        pairs = ecb_rates_to_holistika_pairs(ecb)
        assert pairs[("EUR/EUR", "2026-05-23")] == "1.00000000"

    def test_custom_base_currencies(self) -> None:
        ecb = parse_ecb_daily_xml(_SAMPLE_ECB_XML)
        pairs = ecb_rates_to_holistika_pairs(ecb, base_currencies=["JPY"])
        # JPY now included; USD not (since not in custom list)
        assert ("JPY/EUR", "2026-05-23") in pairs
        assert ("USD/EUR", "2026-05-23") not in pairs


# -----------------------------------------------------------------------------
# Fallback ladder
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestFallbackLadder:
    def test_eur_returns_identity(self) -> None:
        res = apply_fx_fallback_ladder("EUR", "2026-05-23", {})
        assert res.source == "identity_eur"
        assert res.days_behind == 0

    def test_ecb_daily_exact_hit(self) -> None:
        lookup = {("USD/EUR", "2026-05-23"): "0.93020000"}
        res = apply_fx_fallback_ladder("USD", "2026-05-23", lookup)
        assert res.source == "ecb_daily"
        assert res.days_behind == 0
        assert res.rate == "0.93020000"

    def test_previous_day_fallback(self) -> None:
        lookup = {("USD/EUR", "2026-05-20"): "0.92000000"}
        res = apply_fx_fallback_ladder("USD", "2026-05-23", lookup)
        assert res.source == "ecb_previous_day_fallback"
        assert res.days_behind == 3

    def test_lookback_window_respected(self) -> None:
        # Rate is 10 days behind; default max_ecb_lookback_days=7 → should fall through
        lookup = {("USD/EUR", "2026-05-13"): "0.92000000"}
        res = apply_fx_fallback_ladder("USD", "2026-05-23", lookup)
        assert res.source == "unavailable"

    def test_stripe_fallback_when_ecb_empty(self) -> None:
        res = apply_fx_fallback_ladder(
            "USD", "2026-05-23", {}, stripe_fx_quote="0.93000000",
        )
        assert res.source == "stripe_fx_quote"
        assert res.rate == "0.93000000"

    def test_unavailable_when_nothing_matches(self) -> None:
        res = apply_fx_fallback_ladder("USD", "2026-05-23", {})
        assert res.source == "unavailable"
        assert res.rate is None

    def test_invalid_date_returns_unavailable(self) -> None:
        res = apply_fx_fallback_ladder("USD", "not-a-date", {})
        assert res.source == "unavailable"


# -----------------------------------------------------------------------------
# Divergence detector
# -----------------------------------------------------------------------------


@pytest.mark.unit
class TestDivergenceDetector:
    def test_tight_match_does_not_diverge(self) -> None:
        diverges, pct = detect_fx_divergence("0.93000000", "0.93100000")
        # ~0.107% divergence, under 0.5% threshold
        assert not diverges
        assert pct < 0.5

    def test_wide_divergence_fires(self) -> None:
        diverges, pct = detect_fx_divergence("0.93000000", "0.95000000")
        # ~2.15% divergence
        assert diverges
        assert pct > 0.5

    def test_none_rates_do_not_diverge(self) -> None:
        diverges, pct = detect_fx_divergence(None, "0.93000000")
        assert not diverges
        assert pct == 0.0

    def test_zero_rate_handled(self) -> None:
        diverges, pct = detect_fx_divergence("0", "0.93000000")
        assert not diverges
        assert pct == 0.0

    def test_custom_threshold(self) -> None:
        # 0.5% divergence with 0.1% threshold should fire
        diverges, _ = detect_fx_divergence("0.93000000", "0.93465000", threshold_pct=0.1)
        assert diverges
