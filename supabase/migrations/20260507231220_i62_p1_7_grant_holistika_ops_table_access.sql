-- I62 P1.7 — grant table-level permissions on holistika_ops.* to API roles
--
-- Companion to the public-schema views in 20260507231025: the views are
-- security_invoker, so the calling role (authenticated/service_role) needs
-- the matching SELECT/INSERT/UPDATE grants on the underlying tables.
-- Without this grant, the views surfaced HTTP 403 "permission denied for
-- table user_role_mapping" rather than respecting the RLS policies.
--
-- Grants exposed to anon are limited to USAGE on the schema only; row-level
-- access still depends on RLS predicates on the underlying tables.

grant usage on schema holistika_ops to authenticated, anon, service_role;

grant select on holistika_ops.user_role_mapping to authenticated, service_role;
grant select, insert on holistika_ops.audit_log to authenticated, service_role;
grant select, insert, update, delete on holistika_ops.user_preferences to authenticated, service_role;
grant select, insert, update on holistika_ops.notifications to authenticated, service_role;

notify pgrst, 'reload schema';
