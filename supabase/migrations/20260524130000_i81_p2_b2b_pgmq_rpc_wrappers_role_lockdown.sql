-- D-IH-81-X follow-up (B-2c live deploy 2026-05-24): lock down B-2b pgmq RPC wrappers.
--
-- Advisor [get_advisors security] surfaced 10 WARN findings on
-- 20260524100000_i81_p2_b2b_pgmq_rpc_wrappers — the 5 SECURITY DEFINER
-- functions were grantable to anon + authenticated by default (via PUBLIC).
--
-- That's a real PostgREST exposure: anon could call /rest/v1/rpc/pgmq_send_finops_writer
-- + enqueue arbitrary event-ids into the FINOPS writer queue.
--
-- Lock them down to service_role-only. The Edge Functions invoke under
-- service_role auth so the worker pipeline keeps working; PostgREST surface
-- for anon + authenticated is fully revoked.
--
-- This is the B-2b follow-up landed at the B-2c live-deploy gate per the
-- advisor finding; backfills to D-IH-81-X (single closure decision).

REVOKE EXECUTE ON FUNCTION public.pgmq_send_finops_writer(text) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.pgmq_read_finops_writer(integer, integer) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.pgmq_delete_finops_writer(bigint) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.pgmq_archive_finops_writer(bigint) FROM PUBLIC, anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.pgmq_read_finops_dlq(integer, integer) FROM PUBLIC, anon, authenticated;

GRANT EXECUTE ON FUNCTION public.pgmq_send_finops_writer(text) TO service_role;
GRANT EXECUTE ON FUNCTION public.pgmq_read_finops_writer(integer, integer) TO service_role;
GRANT EXECUTE ON FUNCTION public.pgmq_delete_finops_writer(bigint) TO service_role;
GRANT EXECUTE ON FUNCTION public.pgmq_archive_finops_writer(bigint) TO service_role;
GRANT EXECUTE ON FUNCTION public.pgmq_read_finops_dlq(integer, integer) TO service_role;
