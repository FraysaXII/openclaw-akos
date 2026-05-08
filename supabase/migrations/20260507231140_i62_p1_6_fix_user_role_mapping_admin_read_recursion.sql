-- I62 P1.6 — fix infinite-recursion in user_role_mapping_admin_read RLS policy
--
-- The original policy queried holistika_ops.user_role_mapping FROM WITHIN a
-- policy ON holistika_ops.user_role_mapping, which Postgres rejected with
-- 42P17 "infinite recursion detected in policy for relation user_role_mapping".
-- PostgREST surfaced this as an HTTP 500 to every authenticated read.
--
-- Replacing the self-referencing EXISTS check with the SECURITY DEFINER helper
-- holistika_ops.current_access_level() breaks the recursion: the helper bypasses
-- RLS by running as its definer, so the inner read is not policy-evaluated.
--
-- Per the AKOS PRECEDENCE.md "canonical CSV gates" rule: the policy is repaired
-- with the same intent (level >= 6 = admin can read all), no semantic change.

drop policy if exists user_role_mapping_admin_read on holistika_ops.user_role_mapping;

create policy user_role_mapping_admin_read
  on holistika_ops.user_role_mapping
  for select
  to authenticated
  using (holistika_ops.current_access_level() >= 6);

notify pgrst, 'reload schema';
