-- I62 P1.5 — public.current_access_level() wrapper
--
-- The Supabase JS client defaults supabase.rpc(<name>) to the public schema.
-- I62 P1 placed the function in holistika_ops, so callers in middleware.ts
-- and lib/auth/server.ts always saw the function as "missing" and fell back
-- to access_level=0, redirecting authenticated operators to /auth/role-resolve.
--
-- This wrapper stays SECURITY DEFINER so it bypasses RLS exactly the same way
-- as holistika_ops.current_access_level() (the underlying check).
--
-- Discovered while wiring the dev-preview sign-in path on 2026-05-07.

create or replace function public.current_access_level()
  returns smallint
  language sql
  stable
  security definer
  set search_path to 'public', 'holistika_ops', 'auth'
as $$
  select holistika_ops.current_access_level();
$$;

grant execute on function public.current_access_level() to anon, authenticated, service_role;
