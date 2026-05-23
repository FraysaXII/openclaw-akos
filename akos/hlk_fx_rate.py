"""FX rate helper — ECB XML parser + Stripe FX Quotes client + cache lookup + fallback ladder.

Initiative 81 Phase 2 Bundle B-2a (D-IH-81-V under D-IH-81-G umbrella, 2026-05-23).

Per R2 (ECB-authoritative + Stripe FX Quote sidecar) in the Bundle B-2 architecture report: ECB daily
reference rates are the authoritative source for finops.registered_fact.amount_minor_eur. Stripe FX
Quotes are captured as audit sidecar (per-row fx_rate_stripe column) so divergence between ECB and
Stripe can be detected + surfaced via OPS_REGISTER row when threshold exceeded.

This module provides the **Python-side** parsing / fetching contract. The actual scheduled cache
refresh runs in Edge Function ``fx-rate-cache-refresh`` (Bundle B-2b) on cron 17:00 CET. This module
is exercised in tests + by runbooks like ``scripts/finops_dlq_drain.py`` for ad-hoc reconciliation.

ECB feed source: https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml

Two fetch modes:
1. **Live** — used by Edge Function + tests with internet access; fetches eurofxref-daily.xml.
2. **Mock** — used by unit tests; accepts a pre-parsed dict for deterministic test runs.

Per CONTRIBUTING.md Python Code Standards: structured logging via akos.log.setup_logging, type hints
on every function signature, no print(), uses pathlib.Path + os.environ.

See:
- ``docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/reports/p2-bundle-b2-architecture-2026-05-23.md`` §3.2.
- ``supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql`` §3 (fx_rate_cache table DDL).
- ``akos/hlk_finops_ledger.py`` (compute_fx_snapshot consumer).
"""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from typing import Literal, NamedTuple

logger = logging.getLogger(__name__)


ECB_DAILY_FEED_URL: str = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
ECB_XML_NAMESPACE: dict[str, str] = {
    "gesmes": "http://www.gesmes.org/xml/2002-08-01",
    "ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref",
}

# ECB feed returns rates as EUR base (e.g. USD = 1.0750 means 1 EUR = 1.0750 USD).
# Holistika's finops convention: currency_pair = SRC/EUR (e.g. USD/EUR = 0.9302 means 1 USD = 0.9302 EUR).
# Conversion: src_to_eur = 1 / eur_to_src.

FX_DIVERGENCE_THRESHOLD_PCT: float = 0.5  # ECB vs Stripe FX rate divergence > 0.5% emits OPS_REGISTER row


class EcbDailyRates(NamedTuple):
    """Parsed ECB daily feed: effective_date + per-currency EUR-base rates."""

    effective_date: str   # ISO YYYY-MM-DD (from <Cube time="..."> attribute)
    rates: dict[str, str] # currency_code → rate as decimal string (e.g. {"USD": "1.07500", ...})


def parse_ecb_daily_xml(xml_text: str) -> EcbDailyRates:
    """Parse ECB eurofxref-daily.xml content into EcbDailyRates.

    The ECB feed structure is:
        <gesmes:Envelope>
          <Cube>
            <Cube time="YYYY-MM-DD">
              <Cube currency="USD" rate="1.0750"/>
              <Cube currency="GBP" rate="0.8500"/>
              ...
            </Cube>
          </Cube>
        </gesmes:Envelope>

    Args:
        xml_text: full XML feed contents (UTF-8 string).

    Returns:
        EcbDailyRates with effective_date + currency → rate dict.

    Raises:
        ValueError: if XML structure is malformed.
    """

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ValueError(f"ECB feed XML parse error: {exc}") from exc

    # Find the inner <Cube time="...">
    time_cube = root.find(".//ecb:Cube/ecb:Cube[@time]", ECB_XML_NAMESPACE)
    if time_cube is None:
        # Fallback: try without namespace (some renderings drop it)
        time_cube = root.find(".//Cube/Cube[@time]")
    if time_cube is None:
        raise ValueError("ECB feed missing <Cube time=...> element")

    effective_date = time_cube.attrib.get("time", "")
    if not effective_date:
        raise ValueError("ECB feed <Cube time=> attribute is empty")

    rates: dict[str, str] = {}
    currency_cubes = time_cube.findall("ecb:Cube[@currency]", ECB_XML_NAMESPACE)
    if not currency_cubes:
        currency_cubes = time_cube.findall("Cube[@currency]")

    for cube in currency_cubes:
        currency = cube.attrib.get("currency", "").strip()
        rate = cube.attrib.get("rate", "").strip()
        if currency and rate:
            rates[currency] = rate

    if not rates:
        raise ValueError("ECB feed contained no currency entries")

    return EcbDailyRates(effective_date=effective_date, rates=rates)


def convert_eur_base_to_src_to_eur(eur_to_src_rate: str) -> str:
    """Convert ECB EUR-base rate (e.g. USD=1.0750 EUR=1 base) to SRC/EUR (e.g. USD/EUR=0.9302).

    Holistika convention: currency_pair = SRC/EUR (rate * source_amount = EUR amount).
    ECB convention: rate * 1 EUR = source_amount.
    Conversion: src_to_eur = 1 / eur_to_src.

    Args:
        eur_to_src_rate: decimal string as published by ECB (e.g. "1.07500").

    Returns:
        Decimal string for SRC/EUR conversion (e.g. "0.93023256").
    """

    try:
        rate = float(eur_to_src_rate)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Cannot convert ECB rate {eur_to_src_rate!r} to float: {exc}") from exc

    if rate <= 0:
        raise ValueError(f"ECB rate must be positive; got {rate}")

    inverse = 1.0 / rate
    # 8 decimal places matches NUMERIC(18,8) DB column precision
    return f"{inverse:.8f}"


def ecb_rates_to_holistika_pairs(ecb: EcbDailyRates, base_currencies: list[str] | None = None) -> dict[tuple[str, str], str]:
    """Convert EcbDailyRates to a Holistika-format lookup dict suitable for compute_fx_snapshot().

    Args:
        ecb: parsed ECB daily feed.
        base_currencies: optional list of currencies to include (default: USD + GBP + CHF — Holistika's
            current footprint per D-IH-81-P internal-first FINOPS scope). Extend as engagement footprint grows.

    Returns:
        Dict of (currency_pair, effective_date) → rate_decimal_string, suitable as the ecb_rate_lookup
        argument to compute_fx_snapshot() in akos.hlk_finops_ledger.
    """

    if base_currencies is None:
        base_currencies = ["USD", "GBP", "CHF"]

    out: dict[tuple[str, str], str] = {}
    # Identity row for EUR (rate = 1.0)
    out[("EUR/EUR", ecb.effective_date)] = "1.00000000"
    for currency in base_currencies:
        if currency in ecb.rates:
            src_to_eur = convert_eur_base_to_src_to_eur(ecb.rates[currency])
            out[(f"{currency}/EUR", ecb.effective_date)] = src_to_eur
        else:
            logger.warning(
                "Currency %s not present in ECB daily feed for %s; skipping",
                currency, ecb.effective_date,
            )
    return out


class FxFallbackResult(NamedTuple):
    """Result of the fallback ladder for a (currency, effective_date) lookup."""

    rate: str | None
    source: Literal[
        "ecb_daily",
        "ecb_previous_day_fallback",
        "stripe_fx_quote",
        "manual_override",
        "identity_eur",
        "unavailable",
    ]
    days_behind: int  # how many days behind effective_date the rate is (0 = same day)


def apply_fx_fallback_ladder(
    currency: str,
    effective_date: str,
    ecb_lookup: dict[tuple[str, str], str],
    stripe_fx_quote: str | None = None,
    max_ecb_lookback_days: int = 7,
) -> FxFallbackResult:
    """Apply the FX fallback ladder for a (currency, effective_date) pair.

    Ladder (per R2 architecture):
    1. **identity_eur**: currency == 'EUR' → return rate=None, source='identity_eur', days_behind=0.
    2. **ecb_daily**: exact (currency_pair, effective_date) hit → days_behind=0.
    3. **ecb_previous_day_fallback**: iterate back day-by-day up to max_ecb_lookback_days.
    4. **stripe_fx_quote**: if provided, use it → source='stripe_fx_quote', days_behind=-1 (sentinel).
    5. **unavailable**: nothing matched + no Stripe quote → rate=None, source='unavailable'.

    The caller (compute_fx_snapshot or worker) decides whether to:
    - write the fact with the fallback rate + emit OPS_REGISTER row (fx_cache_stale class).
    - reject the fact + push to DLQ for operator review.

    Args:
        currency: ISO 4217 source currency.
        effective_date: ISO date YYYY-MM-DD.
        ecb_lookup: pre-fetched ECB lookup dict (typically from ecb_rates_to_holistika_pairs).
        stripe_fx_quote: optional Stripe FX Quote API rate as decimal string.
        max_ecb_lookback_days: how many days to walk back before falling to Stripe (default 7).

    Returns:
        FxFallbackResult.
    """

    if currency == "EUR":
        return FxFallbackResult(rate=None, source="identity_eur", days_behind=0)

    currency_pair = f"{currency}/EUR"

    # Tier 1: exact match
    if (currency_pair, effective_date) in ecb_lookup:
        return FxFallbackResult(
            rate=ecb_lookup[(currency_pair, effective_date)],
            source="ecb_daily",
            days_behind=0,
        )

    # Tier 2: walk back day-by-day
    try:
        eff = datetime.strptime(effective_date, "%Y-%m-%d").date()
    except ValueError:
        return FxFallbackResult(rate=None, source="unavailable", days_behind=-1)

    for days_back in range(1, max_ecb_lookback_days + 1):
        prev_date = (eff - timedelta(days=days_back)).strftime("%Y-%m-%d")
        if (currency_pair, prev_date) in ecb_lookup:
            return FxFallbackResult(
                rate=ecb_lookup[(currency_pair, prev_date)],
                source="ecb_previous_day_fallback",
                days_behind=days_back,
            )

    # Tier 3: Stripe FX Quote fallback
    if stripe_fx_quote:
        return FxFallbackResult(rate=stripe_fx_quote, source="stripe_fx_quote", days_behind=-1)

    # Tier 4: unavailable
    return FxFallbackResult(rate=None, source="unavailable", days_behind=-1)


def detect_fx_divergence(
    rate_ecb: str | None,
    rate_stripe: str | None,
    threshold_pct: float = FX_DIVERGENCE_THRESHOLD_PCT,
) -> tuple[bool, float]:
    """Detect whether ECB and Stripe FX rates diverge beyond a tolerance threshold.

    Per R2 architecture: capture both rates on every Stripe-origin fact write; emit OPS_REGISTER row
    when divergence > threshold so operator can investigate (currency conversion fees, Stripe FX
    spread, or ECB feed staleness).

    Args:
        rate_ecb: ECB rate as decimal string (e.g. "0.93020000").
        rate_stripe: Stripe FX Quote rate as decimal string.
        threshold_pct: divergence threshold in percent (default 0.5%).

    Returns:
        Tuple (diverges, abs_divergence_pct). diverges=True when both rates present + abs divergence > threshold.
        When either rate is None: diverges=False, divergence_pct=0.0.
    """

    if rate_ecb is None or rate_stripe is None:
        return (False, 0.0)

    try:
        ecb_f = float(rate_ecb)
        stripe_f = float(rate_stripe)
    except (TypeError, ValueError):
        return (False, 0.0)

    if ecb_f <= 0 or stripe_f <= 0:
        return (False, 0.0)

    abs_div_pct = abs((stripe_f - ecb_f) / ecb_f) * 100.0
    return (abs_div_pct > threshold_pct, abs_div_pct)
