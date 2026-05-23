-- =============================================================================
-- Initiative 81 Phase 2 Bundle B-2b — pgmq RPC wrappers for Edge Function access
--
-- Decision: D-IH-81-W under D-IH-81-G umbrella (operator b2b-test-b + b2b-wh-b
-- ratification, 2026-05-23).
--
-- Architecture: per Bundle B-2 architecture report §3.3 (R3 pgmq DLQ).
--
-- WHY this migration is needed (B-2a landed pgmq queues but no callable wrappers):
--   PostgREST (the layer Supabase Edge Functions reach the DB through) cannot call
--   schema-qualified functions like `pgmq.send` directly via the supabase-js .rpc()
--   bridge — it expects functions in the exposed schema (default: public) OR a
--   security_definer wrapper. pgmq itself does not auto-expose its operations.
--
--   This migration ships 4 thin SECURITY DEFINER wrappers under the public schema:
--     - pgmq_send_finops_writer(p_event_id text) → bigint  (enqueue)
--     - pgmq_read_finops_writer(p_qty int, p_vt int) → setof pgmq.message_record  (read batch)
--     - pgmq_delete_finops_writer(p_msg_id bigint) → boolean  (ack message)
--     - pgmq_archive_finops_writer(p_msg_id bigint) → boolean  (move to DLQ)
--
--   Each wrapper is locked to service_role only — the anon and authenticated
--   roles cannot enqueue / dequeue FINOPS events through the API surface.
--
-- Reversibility: drop the 4 functions; pgmq queues themselves remain intact.
--   No data loss on rollback (B-2c writes only enrich; messages stay queued).
-- =============================================================================

-- §1 — Enqueue wrapper (called by stripe-webhook-handler FINOPS branch)
CREATE OR REPLACE FUNCTION public.pgmq_send_finops_writer(p_event_id text)
RETURNS bigint
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pgmq
AS $$
DECLARE
  v_msg_id bigint;
BEGIN
  IF p_event_id IS NULL OR length(p_event_id) = 0 THEN
    RAISE EXCEPTION 'pgmq_send_finops_writer: p_event_id is required';
  END IF;
  SELECT pgmq.send('finops_writer_queue', jsonb_build_object('stripe_event_id', p_event_id))
  INTO v_msg_id;
  RETURN v_msg_id;
END;
$$;

REVOKE ALL ON FUNCTION public.pgmq_send_finops_writer(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.pgmq_send_finops_writer(text) TO service_role;
COMMENT ON FUNCTION public.pgmq_send_finops_writer(text) IS
  'B-2b D-IH-81-W: enqueue Stripe event id onto pgmq.finops_writer_queue. service_role only.';

-- §2 — Read-batch wrapper (called by finops-writer-worker scheduled trigger)
-- Returns up to p_qty messages, each locked for p_vt seconds (visibility timeout).
CREATE OR REPLACE FUNCTION public.pgmq_read_finops_writer(p_qty int DEFAULT 10, p_vt int DEFAULT 60)
RETURNS TABLE (msg_id bigint, read_ct int, enqueued_at timestamptz, vt timestamptz, message jsonb)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pgmq
AS $$
BEGIN
  IF p_qty IS NULL OR p_qty <= 0 OR p_qty > 100 THEN
    p_qty := 10;
  END IF;
  IF p_vt IS NULL OR p_vt <= 0 OR p_vt > 600 THEN
    p_vt := 60;
  END IF;
  RETURN QUERY SELECT m.msg_id, m.read_ct, m.enqueued_at, m.vt, m.message
               FROM pgmq.read('finops_writer_queue', p_vt, p_qty) AS m;
END;
$$;

REVOKE ALL ON FUNCTION public.pgmq_read_finops_writer(int, int) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.pgmq_read_finops_writer(int, int) TO service_role;
COMMENT ON FUNCTION public.pgmq_read_finops_writer(int, int) IS
  'B-2b D-IH-81-W: read up to p_qty messages from pgmq.finops_writer_queue with p_vt second visibility. service_role only.';

-- §3 — Delete wrapper (ack successful processing)
CREATE OR REPLACE FUNCTION public.pgmq_delete_finops_writer(p_msg_id bigint)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pgmq
AS $$
DECLARE
  v_result boolean;
BEGIN
  IF p_msg_id IS NULL OR p_msg_id <= 0 THEN
    RAISE EXCEPTION 'pgmq_delete_finops_writer: p_msg_id is required and positive';
  END IF;
  SELECT pgmq.delete('finops_writer_queue', p_msg_id) INTO v_result;
  RETURN v_result;
END;
$$;

REVOKE ALL ON FUNCTION public.pgmq_delete_finops_writer(bigint) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.pgmq_delete_finops_writer(bigint) TO service_role;
COMMENT ON FUNCTION public.pgmq_delete_finops_writer(bigint) IS
  'B-2b D-IH-81-W: ack a finops_writer_queue message after successful processing. service_role only.';

-- §4 — Archive wrapper (move exhausted-retry messages to DLQ)
CREATE OR REPLACE FUNCTION public.pgmq_archive_finops_writer(p_msg_id bigint)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pgmq
AS $$
DECLARE
  v_result boolean;
  v_message jsonb;
BEGIN
  IF p_msg_id IS NULL OR p_msg_id <= 0 THEN
    RAISE EXCEPTION 'pgmq_archive_finops_writer: p_msg_id is required and positive';
  END IF;

  -- Read the message body first so we can re-send to the DLQ.
  SELECT message INTO v_message
  FROM pgmq.q_finops_writer_queue
  WHERE msg_id = p_msg_id
  LIMIT 1;

  IF v_message IS NULL THEN
    RETURN false;
  END IF;

  -- Send to DLQ, then delete from primary queue.
  PERFORM pgmq.send('finops_writer_dlq', v_message);
  SELECT pgmq.delete('finops_writer_queue', p_msg_id) INTO v_result;
  RETURN v_result;
END;
$$;

REVOKE ALL ON FUNCTION public.pgmq_archive_finops_writer(bigint) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.pgmq_archive_finops_writer(bigint) TO service_role;
COMMENT ON FUNCTION public.pgmq_archive_finops_writer(bigint) IS
  'B-2b D-IH-81-W: move an exhausted-retry message from finops_writer_queue to finops_writer_dlq. service_role only.';

-- §5 — DLQ inspection wrapper (operator runbook scripts/finops_dlq_drain.py reads through this)
CREATE OR REPLACE FUNCTION public.pgmq_read_finops_dlq(p_qty int DEFAULT 10, p_vt int DEFAULT 0)
RETURNS TABLE (msg_id bigint, read_ct int, enqueued_at timestamptz, vt timestamptz, message jsonb)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, pgmq
AS $$
BEGIN
  IF p_qty IS NULL OR p_qty <= 0 OR p_qty > 1000 THEN
    p_qty := 10;
  END IF;
  -- DLQ inspection defaults p_vt=0 (no visibility timeout; just peek).
  RETURN QUERY SELECT m.msg_id, m.read_ct, m.enqueued_at, m.vt, m.message
               FROM pgmq.read('finops_writer_dlq', GREATEST(p_vt, 1), p_qty) AS m;
END;
$$;

REVOKE ALL ON FUNCTION public.pgmq_read_finops_dlq(int, int) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.pgmq_read_finops_dlq(int, int) TO service_role;
COMMENT ON FUNCTION public.pgmq_read_finops_dlq(int, int) IS
  'B-2b D-IH-81-W: inspect messages in finops_writer_dlq for operator drain runbook. service_role only.';
