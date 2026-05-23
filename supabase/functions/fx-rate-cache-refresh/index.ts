/**
 * Edge Function — fx-rate-cache-refresh
 *
 * Initiative 81 Phase 2 Bundle B-2b (D-IH-81-W under D-IH-81-G umbrella, 2026-05-23).
 *
 * Per R2 (ECB-authoritative + Stripe FX Quote sidecar) — fetches today's ECB daily reference
 * rates and UPSERTs them into holistika_ops.fx_rate_cache.
 *
 * INVOCATION: scheduled via Supabase cron (recommended: every weekday at 17:00 UTC, just
 * after ECB publishes the day's rates around 16:00 CET). Manual invocation via
 *   curl -X POST -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
 *        https://<project>.supabase.co/functions/v1/fx-rate-cache-refresh
 *
 * SOURCE: ECB Statistical Data Warehouse SDMX endpoint
 *   https://data-api.ecb.europa.eu/service/data/EXR/D.<CCY>.EUR.SP00.A
 *   Returns CSV with the latest daily rate (or a small window when requested).
 *
 * IDEMPOTENCY: PK on (currency_pair, effective_date) — re-runs same day are no-ops.
 *
 * CONCURRENCY: single-instance; if another invocation overlaps the writes use
 *   ON CONFLICT DO UPDATE so the last writer wins (same-day rates from same source).
 *
 * FAILURES:
 *   - ECB endpoint 5xx: log + emit FX_CACHE_STALE OPS row only after Nth consecutive failure
 *     (the worker's stale-cache OPS emit is the operator signal; the fetch function logs
 *     warnings but does not fight the situation alone).
 *   - currency pair missing from ECB response: skip + log warning (worker falls through to
 *     Stripe FX quote at write time).
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";

// =============================================================================
// §1 — Currency pairs to refresh (mirror VALID_CURRENCY_CODES minus EUR)
// =============================================================================

const CURRENCIES_TO_FETCH = ["USD", "GBP", "CHF"] as const;
const ECB_SDMX_BASE = "https://data-api.ecb.europa.eu/service/data/EXR/D";

interface FetchResult {
  currency: string;
  pair: string;
  effective_date: string;
  rate: string | null;
  source_url: string;
  error: string | null;
}

// =============================================================================
// §2 — Fetch one currency's latest daily rate from ECB SDMX endpoint
// =============================================================================

async function fetchEcbRate(currency: string): Promise<FetchResult> {
  // SDMX-CSV returns YYYY-MM-DD + rate columns; we request the last business day.
  // Endpoint format: /service/data/EXR/D.<CCY>.EUR.SP00.A?lastNObservations=1&format=csvdata
  const url =
    `${ECB_SDMX_BASE}.${currency}.EUR.SP00.A?lastNObservations=1&format=csvdata`;
  const pair = `${currency}/EUR`;

  try {
    const resp = await fetch(url, {
      headers: { Accept: "text/csv" },
      signal: AbortSignal.timeout(10_000),
    });

    if (!resp.ok) {
      return {
        currency,
        pair,
        effective_date: "",
        rate: null,
        source_url: url,
        error: `ECB SDMX returned HTTP ${resp.status}`,
      };
    }

    const text = await resp.text();
    // SDMX-CSV format: header row + data rows. Find TIME_PERIOD + OBS_VALUE columns.
    const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
    if (lines.length < 2) {
      return { currency, pair, effective_date: "", rate: null, source_url: url, error: "empty ECB response" };
    }

    const header = lines[0].split(",");
    const dateIdx = header.findIndex((h) => h.trim() === "TIME_PERIOD");
    const valueIdx = header.findIndex((h) => h.trim() === "OBS_VALUE");
    if (dateIdx < 0 || valueIdx < 0) {
      return {
        currency,
        pair,
        effective_date: "",
        rate: null,
        source_url: url,
        error: `ECB CSV missing TIME_PERIOD / OBS_VALUE columns (got: ${header.join(",")})`,
      };
    }

    // Read last data row.
    const lastRow = lines[lines.length - 1].split(",");
    const effectiveDate = lastRow[dateIdx]?.trim() ?? "";
    const obsValueRaw = lastRow[valueIdx]?.trim() ?? "";

    // ECB rate is EUR/CCY direction (1 EUR = X CCY); we need CCY/EUR (1 CCY = Y EUR).
    // Invert: rate_to_store = 1 / obs_value.
    const obsNum = Number(obsValueRaw);
    if (!Number.isFinite(obsNum) || obsNum <= 0) {
      return {
        currency,
        pair,
        effective_date: effectiveDate,
        rate: null,
        source_url: url,
        error: `invalid OBS_VALUE '${obsValueRaw}'`,
      };
    }
    const invertedRate = (1 / obsNum).toFixed(8);

    return {
      currency,
      pair,
      effective_date: effectiveDate,
      rate: invertedRate,
      source_url: url,
      error: null,
    };
  } catch (err) {
    return {
      currency,
      pair,
      effective_date: "",
      rate: null,
      source_url: url,
      error: err instanceof Error ? err.message : String(err),
    };
  }
}

// =============================================================================
// §3 — UPSERT one rate into holistika_ops.fx_rate_cache
// =============================================================================

interface UpsertOutcome {
  pair: string;
  effective_date: string;
  upserted: boolean;
  error: string | null;
}

// deno-lint-ignore no-explicit-any
async function upsertRate(supabase: any, fr: FetchResult): Promise<UpsertOutcome> {
  if (fr.error || !fr.rate || !fr.effective_date) {
    return { pair: fr.pair, effective_date: fr.effective_date, upserted: false, error: fr.error ?? "rate or date missing" };
  }
  const row = {
    currency_pair: fr.pair,
    effective_date: fr.effective_date,
    rate: fr.rate,
    source: "ecb_daily",
    source_url: fr.source_url,
    fetched_at: new Date().toISOString(),
  };
  const { error } = await supabase
    .schema("holistika_ops")
    .from("fx_rate_cache")
    .upsert(row, { onConflict: "currency_pair,effective_date" });
  if (error) {
    return { pair: fr.pair, effective_date: fr.effective_date, upserted: false, error: error.message };
  }
  return { pair: fr.pair, effective_date: fr.effective_date, upserted: true, error: null };
}

// =============================================================================
// §4 — Deno.serve entry point
// =============================================================================

Deno.serve(async (req) => {
  const startedAt = new Date().toISOString();

  // Permit-only POST (the Supabase scheduler uses POST).
  if (req.method !== "POST" && req.method !== "GET") {
    return new Response(JSON.stringify({ error: "method_not_allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!supabaseUrl || !supabaseServiceKey) {
    return new Response(
      JSON.stringify({ error: "missing_env", detail: "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY required" }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }

  const supabase = createClient(supabaseUrl, supabaseServiceKey);

  console.log(
    JSON.stringify({ source: "fx-rate-cache-refresh", note: "starting refresh", currencies: CURRENCIES_TO_FETCH }),
  );

  // Fetch all currencies in parallel; ECB is rate-limited but this is 3 requests.
  const fetches = await Promise.all(CURRENCIES_TO_FETCH.map(fetchEcbRate));
  const upserts: UpsertOutcome[] = [];
  for (const fr of fetches) {
    const outcome = await upsertRate(supabase, fr);
    upserts.push(outcome);
    if (outcome.error) {
      console.warn(
        JSON.stringify({
          source: "fx-rate-cache-refresh",
          note: "rate upsert failed",
          pair: outcome.pair,
          error: outcome.error,
        }),
      );
    } else {
      console.log(
        JSON.stringify({
          source: "fx-rate-cache-refresh",
          note: "rate upserted",
          pair: outcome.pair,
          effective_date: outcome.effective_date,
        }),
      );
    }
  }

  const completedAt = new Date().toISOString();
  const summary = {
    source: "fx-rate-cache-refresh",
    started_at: startedAt,
    completed_at: completedAt,
    currencies_attempted: CURRENCIES_TO_FETCH.length,
    currencies_upserted: upserts.filter((u) => u.upserted).length,
    failures: upserts.filter((u) => u.error).map((u) => ({ pair: u.pair, error: u.error })),
  };
  console.log(JSON.stringify({ ...summary, note: "refresh complete" }));

  return new Response(JSON.stringify(summary), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
});
