-- Reverse-imported 2026-05-04 (D-IH-OPS-1 / D-IH-OPS-3) from
-- supabase_migrations.schema_migrations[20260418165339].statements on project
-- swrmqpelgoblaquequzb (MasterData). The body was applied to the remote
-- ledger via Dashboard / break-glass before this folder existed; git is now
-- SSOT going forward. Every statement is idempotent
-- (CREATE INDEX IF NOT EXISTS, CREATE OR REPLACE FUNCTION, REVOKE/GRANT)
-- so re-applying via supabase db push is a no-op.
--
-- See docs/wip/planning/22a-i22-post-closure-followups/reports/sql-proposal-supabase-parity-20260504.md.

create index if not exists idx_monitoring_logs_created_at
  on kirbe.monitoring_logs (created_at desc);

create or replace function kirbe.cleanup_monitoring_logs(
  retention_days integer default 30,
  batch_limit bigint default 50000
)
returns bigint
language plpgsql
security definer
set search_path = kirbe, pg_temp
as $$
declare
  deleted bigint;
begin
  if retention_days is null or retention_days < 1 then
    raise exception 'retention_days must be >= 1';
  end if;
  if batch_limit is null or batch_limit < 1 then
    raise exception 'batch_limit must be >= 1';
  end if;
  with doomed as (
    select ctid
    from kirbe.monitoring_logs
    where created_at < (now() - (retention_days || ' days')::interval)
    limit batch_limit
  )
  delete from kirbe.monitoring_logs m
  using doomed d
  where m.ctid = d.ctid;
  get diagnostics deleted = row_count;
  return deleted;
end;
$$;

comment on function kirbe.cleanup_monitoring_logs(integer, bigint) is
  'Deletes up to batch_limit rows with created_at older than retention_days. service_role only.';

revoke all on function kirbe.cleanup_monitoring_logs(integer, bigint) from public;
grant execute on function kirbe.cleanup_monitoring_logs(integer, bigint) to service_role;
