-- Initiative 81 Phase 2 Bundle B-2c — schedule finops-writer-worker every minute.
--
-- Architecture R3 (pgmq DLQ + retry): Stripe webhook handler enqueues onto
-- pgmq.finops_writer_queue, this worker drains it. visibility timeout 90s in
-- the worker prevents overlap; MAX_BATCH=25 messages per invocation; idempotent.
--
-- Cadence: every minute (matches the file-header recommendation in
-- supabase/functions/finops-writer-worker/index.ts line 13).
--
-- The cron job uses the anon key (verify_jwt=true accepts any valid JWT;
-- worker re-derives a service-role client from env to do the DB work).

SELECT cron.schedule(
  'finops_writer_worker_every_minute',
  '* * * * *',
  $$
  SELECT net.http_post(
    url := 'https://swrmqpelgoblaquequzb.supabase.co/functions/v1/finops-writer-worker',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'apikey', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3cm1xcGVsZ29ibGFxdWVxdXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYwOTMxMjMsImV4cCI6MjAxMTY2OTEyM30.sEoHMDmwX27URkGL0rr79J3_CnQhKmd_5xEAAJ25fA0',
      'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN3cm1xcGVsZ29ibGFxdWVxdXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTYwOTMxMjMsImV4cCI6MjAxMTY2OTEyM30.sEoHMDmwX27URkGL0rr79J3_CnQhKmd_5xEAAJ25fA0'
    ),
    body := '{}'::jsonb
  );
  $$
);
