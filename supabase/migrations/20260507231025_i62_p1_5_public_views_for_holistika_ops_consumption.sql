-- I62 P1.5 — public-schema views over holistika_ops.* for app-side consumption
--
-- Rationale: hlk-erp app code calls supabase.from('user_role_mapping') and
-- equivalent for audit_log / user_preferences / notifications. The Supabase
-- JS client's default schema is `public`, and PostgREST does not expose
-- `holistika_ops` on the REST API. Without these views, the client returned
-- HTTP 404 for every read of these tables, the operator layout treated the
-- empty result as "no role mapping", and every authenticated session was
-- redirected to /auth/role-resolve regardless of access_level.
--
-- security_invoker = true preserves the existing RLS policies on the base
-- tables (no privilege escalation; the calling user's own GUC/JWT is what
-- evaluates the policy predicate).

create or replace view public.user_role_mapping with (security_invoker = true) as
  select * from holistika_ops.user_role_mapping;

create or replace view public.audit_log with (security_invoker = true) as
  select * from holistika_ops.audit_log;

create or replace view public.user_preferences with (security_invoker = true) as
  select * from holistika_ops.user_preferences;

create or replace view public.notifications with (security_invoker = true) as
  select * from holistika_ops.notifications;

grant select on public.user_role_mapping, public.audit_log, public.user_preferences, public.notifications
  to anon, authenticated, service_role;
grant insert, update on public.user_preferences, public.notifications
  to authenticated, service_role;
grant insert on public.audit_log to authenticated, service_role;

notify pgrst, 'reload schema';
