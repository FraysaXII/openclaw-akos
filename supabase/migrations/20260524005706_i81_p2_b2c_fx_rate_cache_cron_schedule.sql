-- Initiative 81 Phase 2 Bundle B-2c — schedule fx-rate-cache-refresh daily.
--
-- Architecture R2 (ECB FX cache): the worker daily fetches USD/EUR + GBP/EUR +
-- CHF/EUR from ECB Eurostat REST API and upserts into holistika_ops.fx_rate_cache
-- so the writer worker has a stable per-day source of truth even when ECB API
-- is briefly unavailable.
--
-- Cadence: daily at 15:30 UTC = 16:30 CET (ECB publishes ~16:00 CET so this gives
-- 30min slack for ECB API to settle). On weekends + holidays the function gracefully
-- handles "no business day" by reusing the most recent rate already cached.
--
-- The cron job uses the anon key (verify_jwt=true accepts any valid JWT;
-- function reads env-supplied SUPABASE_SERVICE_ROLE_KEY for the DB write).
--
-- Idempotency: cron.schedule(jobname, ...) is upsert by jobname; safe to re-apply.

SELECT cron.schedule(
  'fx_rate_cache_refresh_daily',
  '30 15 * * *',
  $$
  SELECT net.http_post(
    url := 'https://swrmqpelgoblaquequzb.supabase.co/functions/v1/fx-rate-cache-refresh',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'apikey', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3cm1xcGVsZ29ibGFxdWVxdXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYwOTMxMjMsImV4cCI6MjAxMTY2OTEyM30.sEoHMDmwX27URkGL0rr79J3_CnQhKmd_5xEAAJ25fA0',
      'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3cm1xcGVsZ29ibGFxdWVxdXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYwOTMxMjMsImV4cCI6MjAxMTY2OTEyM30.sEoHMDmwX27URkGL0rr79J3_CnQhKmd_5xEAAJ25fA0'
    ),
    body := '{}'::jsonb
  );
  $$
);
