---
language: en
status: active
initiative: 96-research-data-plane-and-research-center
report_kind: sql-discovery
program_id: holistika_ops
plane: data
authority: System Owner + Data Architect (CDO lane)
last_review: 2026-06-13
---

# Supabase live DB health discovery — auth user creation blocker

> **Operator SQL gate applies.** Read-only discovery first; any DROP/fix runs through [`operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md).

## Symptom

Supabase Dashboard → Authentication → Users → **Add user** →  
`Failed to create user: Database error creating new user`

This blocks **new** Preview UAT identities. Existing users (e.g. `fay.njoya@gmail.com`) may still work via password reset.

## Canonical vs drift (what AKOS git owns)

| Asset class | In git (`supabase/migrations/`) | On live project |
|:---|:---|:---|
| `holistika_ops.*` tables, RLS, RPC | Yes — I62, I96 RPC | Should match after `db push` |
| `auth.users` triggers / hooks | **No** — not in AKOS migrations | **Unknown — inspect live** |
| Auth hooks in `config.toml` | Commented out locally | Remote may differ |
| Lovable / manual SQL | Not in git | **Common drift source** |

**Data Architect referent:** canonical schema = git migrations + [`SUPABASE_MODULE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_MODULE_REGISTRY.csv). Live-only triggers are **drift** until captured in a migration or explicitly retired.

## Discovery SQL (run in Supabase SQL Editor)

**Confirmed on MasterData (`swrmqpelgoblaquequzb`) 2026-06-13 via Supabase MCP:**

| Trigger | Function | Effect |
|:---|:---|:---|
| `on_auth_user_created` | `public.handle_public_user()` | Inserts into `public.users` on every new auth user |
| `on_auth_user_created_kirbe` | `kirbe.handle_new_auth_user()` | Calls `kirbe.provision_user(new.id, true)` |

Both are **live drift** (not in AKOS `supabase/migrations/`). Either can cause **Database error creating new user** when insert/provision fails.

**M0 user check (Preview UAT — no new user needed):**

```sql
SELECT u.id, u.email, urm.access_level, urm.status
FROM auth.users u
LEFT JOIN holistika_ops.user_role_mapping urm ON urm.user_id = u.id
WHERE lower(u.email) = lower('fay.njoya@gmail.com');
-- Expected: access_level >= 4, status active (found: org_017, level 6, active ✓)
```

```sql
-- 1) Triggers on auth.users (most common cause)
SELECT tgname AS trigger_name,
       pg_get_triggerdef(t.oid) AS definition
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE n.nspname = 'auth' AND c.relname = 'users' AND NOT t.tgisinternal;

-- 2) Functions referenced by those triggers (check SECURITY DEFINER)
SELECT p.proname, p.prosecdef AS security_definer, n.nspname
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.proname ILIKE '%user%' OR p.proname ILIKE '%auth%'
ORDER BY n.nspname, p.proname;

-- 3) Recent Postgres errors (correlate with Dashboard → Logs → Postgres)
--    Reproduce: try Add user, then refresh logs within 2 minutes.
```

## Mitigation ladder (max safe today — no full migration)

| Step | Action | Risk |
|:---|:---|:---|
| **M0** | Use **existing** Auth user; reset password; insert `user_role_mapping` | Low — unblocks I96 Preview UAT |
| **M1** | Identify failing trigger from Postgres log + query (1) | Read-only |
| **M2** | If trigger is orphan (profiles insert, etc.): **disable or fix** with `SECURITY DEFINER` + operator approval | Medium — document in decision log |
| **M3** | Capture fix in AKOS migration **or** retirement note in this report | Restores SSOT |
| **M4** | Run `get_advisors` (security) post-change | I95 / DataOps posture |
| **DEFER** | New Supabase project + data migration | High cost — only if M2 fails or auth schema corrupted |

## System Owner + Data Architect duties (governed referent)

1. **Inventory** — quarterly: triggers on `auth.*`, edge functions touching signup, Auth hook URLs in Dashboard.
2. **Parity** — `supabase migration list` vs production (see [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md)).
3. **No silent Lovable SQL** — anything not in git is drift; either migrate in or drop with evidence.
4. **Two-plane rule** — DDL via migrations; CSV mirrors via emit/apply — unchanged.

## Full DB clean migration (deferred)

Operator noted possible future greenfield project when budget/time allow. **Not today.** Track as OPS forward item under I95 EG-5 or a future `_candidates` promotion when auth trigger debt exceeds M2 repair.

## Next operator actions

1. Run discovery SQL (1) — paste trigger names here or to agent (no secrets).
2. Supabase → Logs → Postgres while reproducing Add user.
3. If `fay.njoya@gmail.com` exists: M0 path in [domain/CICD SSOT](research-center-domain-and-cicd-ssot-2026-06-13.md) § Dev sign-in troubleshooting.

## I99 Auth hook registry (canonical — D-IH-99-J)

Live triggers on `auth.users` are catalogued in [`SUPABASE_AUTH_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_AUTH_REGISTRY.csv):

| Row | Trigger | Disposition |
|:---|:---|:---|
| SUPA-AUTH-11 | `public.handle_public_user()` | **drift** — migrate to git or retire at operator gate |
| SUPA-AUTH-12 | `kirbe.handle_new_auth_user()` | **drift** — KiRBe boundary; M2 disposition |

See [`../../99-supabase-platform-eg5-tranche/decision-log.md`](../../99-supabase-platform-eg5-tranche/decision-log.md) D-IH-99-E / D-IH-99-J.
