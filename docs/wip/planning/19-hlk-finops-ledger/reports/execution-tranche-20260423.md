# Initiative 19 — Execution tranche (2026-04-23)

## Repo verification

| Check | Result |
|-------|--------|
| `pytest tests/test_i19_finops_sql_bundle.py` | Run in CI / locally |
| `npx supabase migration list` | Local / remote must include `*_i19_finops_ledger_phase1.sql` after push |

## Deliverables

| Artifact | Path |
|----------|------|
| Staging (up) | `scripts/sql/i19_phase1_staging/20260423_i19_finops_ledger_phase1_up.sql` |
| Staging (rollback) | `scripts/sql/i19_phase1_staging/20260423_i19_finops_ledger_phase1_rollback.sql` |
| Migration | `supabase/migrations/20260423014326_i19_finops_ledger_phase1.sql` (ledger id set by apply path; reconcile rename per [`supabase/migrations/README.md`](../../../../../supabase/migrations/README.md)) |

## Remote apply (2026-04-23)

**Applied:** Supabase MCP `apply_migration` — ledger version **`20260423014326`** / `i19_finops_ledger_phase1`. Git file **`20260423014326_i19_finops_ledger_phase1.sql`** matches `npx supabase migration list` (local / remote).

**Post-DDL:** `finops.registered_fact` exists (**RLS on**, **0** rows); `get_advisors` (security) — treat **delta** vs prior snapshot when closing Phase 1 UAT.
