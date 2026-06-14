-- I96 — align hlk-erp getCurrentUser() with middleware auth path
--
-- Root cause: remote holistika_ops.user_role_mapping still carried the pre-P1.6
-- admin_read policy (EXISTS subquery on the same table), so PostgREST reads hit
-- 42P17 infinite recursion while SECURITY DEFINER current_access_level() worked.
--
-- 1) Re-apply I62 P1.6 admin_read fix (idempotent).
-- 2) Add current_user_role_mapping() RPC for full-row resolution without RLS.

drop policy if exists user_role_mapping_admin_read on holistika_ops.user_role_mapping;

create policy user_role_mapping_admin_read
  on holistika_ops.user_role_mapping
  for select
  to authenticated
  using (holistika_ops.current_access_level() >= 6);

create or replace function holistika_ops.current_user_role_mapping()
returns setof holistika_ops.user_role_mapping
language sql
stable
security definer
set search_path = public, holistika_ops, auth
as $$
  select *
  from holistika_ops.user_role_mapping
  where user_id = auth.uid()
  limit 1;
$$;

comment on function holistika_ops.current_user_role_mapping is
  'I96 — returns the caller''s user_role_mapping row; SECURITY DEFINER so RLS recursion on admin_read does not gate it.';

grant execute on function holistika_ops.current_user_role_mapping() to authenticated, anon, service_role;

create or replace function public.current_user_role_mapping()
returns setof holistika_ops.user_role_mapping
language sql
stable
security definer
set search_path = public, holistika_ops, auth
as $$
  select * from holistika_ops.current_user_role_mapping();
$$;

grant execute on function public.current_user_role_mapping() to authenticated, anon, service_role;

notify pgrst, 'reload schema';
