---
intellectual_kind: cross_area_tech_propagation_report
sharing_label: internal_only
audience: J-OP
authored: 2026-05-29
last_review: 2026-05-29
ratifying_decisions:
  - D-IH-75-G   # Research area logic change (this session's canonical edits)
  - D-IH-86-FH  # IntelligenceOps radar freshness columns
  - D-IH-86-EJ  # Collaborator-share 4-base+1-overlay rewrite
status: active
role_owner: System Owner
co_owner_role: PMO
language: en
discovery_method: supabase-mcp-readonly + git-canonical-count
prod_project: swrmqpelgoblaquequzb  # Supabase "MasterData"
---

# Cross-area Tech propagation — prod-mirror integrity sweep (2026-05-29)

> **Operator framing (2026-05-29):** *"Care with forgetting about our core
> components by the way like supabase, neo4j … that's a cross area with Tech
> you need to design correctly. i caught this one myself. please do the same
> with others, as soon as the commits land. … i want everything in production,
> not staging, nor preview, prod."*

This report is the standing answer to that instruction. Every canonical-CSV
change in git has a **Tech-area consequence** (a Supabase mirror table; a Neo4j
projection). Committing to git is **not** "in production" — the mirror must
reflect it. This sweep checks that consequence after the Wave R+5 + clean-slate
commits landed, and it codifies a reusable checklist so the check is never
skipped again.

## 1 — TL;DR (what I found, in plain terms)

The prod database (**MasterData** on Supabase) is **materially behind git** —
not because of one missed step, but because two propagation lanes silently
stopped running:

1. **Schema lane (migrations):** the prod migration ledger stops at
   **2026-05-24**. Three committed migrations from the last five days were
   **never applied to prod**:
   - the collaborator-share mirror tables (5 tables) — **absent** from prod;
   - the collaborator-share enum rewrite (4-base + 1-overlay);
   - the IntelligenceOps **radar-freshness columns** (this session's research-radar work).
2. **Data lane (mirror rows):** the row-sync that copies canonical CSV rows into
   the `*_mirror` tables has not run since **~early May**. Prod has **51**
   decisions; git has **466**. Same shape across every governed register.

None of this is destructive or urgent-broken — the **canonical CSVs in git are
the source of truth and are correct**. But the *projections other systems read*
(ERP panels, dashboards, any consumer of `compliance.*_mirror`) are stale.
That is precisely the "lots of work, but it's not in production" failure mode.

## 2 — The gap, quantified (read-only Supabase MCP, 2026-05-29)

Prod project `swrmqpelgoblaquequzb` ("MasterData"), schema `compliance`:

| Mirror table | Prod rows | Git canonical | Drift | Schema current? |
|:---|---:|---:|---:|:---|
| `decision_register_mirror` | 51 | 466 | **−415** | yes |
| `ops_register_mirror` | 22 | 136 | **−114** | yes |
| `process_list_mirror` | 1100 | 1186 | **−86** | yes |
| `initiative_registry_mirror` | 51 | 74 | **−23** | yes |
| `substrate_registry_mirror` | 18 | 22 | **−4** | yes |
| `intelligenceops_register_mirror` | 0 | 4 | **−4** | **NO — radar columns missing** |
| `collaborator_share_registry_mirror` (+4 siblings) | — | 1+ | table **absent** | **NO — migration unapplied** |

Migration ledger last applied: `20260524130000_i81_p2_b2b_pgmq_rpc_wrappers_role_lockdown`.

**Unapplied committed migrations (all additive / idempotent — low blast radius):**

| File | Effect | Risk |
|:---|:---|:---|
| `supabase/migrations/20260525000000_…collaborator_share_mirrors.sql` | `CREATE TABLE IF NOT EXISTS` × 5 | none (new tables) |
| `supabase/migrations/20260526000000_…collaborator_share_enum_amend.sql` | `ADD COLUMN IF NOT EXISTS` + constraint swap on the (empty) collaborator-share tables | none (empty tables) |
| `supabase/migrations/20260529120000_i75_intelligenceops_radar_freshness_columns.sql` | `ADD COLUMN IF NOT EXISTS` × 4 (nullable) on the (empty) intelligenceops mirror | none (additive, empty table) |

## 3 — Why I did not auto-apply it (the honest blocker)

The disciplined fix runs into a credential wall, not a caution wall:

- **`npx supabase db push`** is the clean way to apply committed migration files
  (it preserves each file's version in the ledger). My environment has **no
  Supabase CLI, no `SUPABASE_ACCESS_TOKEN`, and no `SUPABASE_DB_PASSWORD`** — so
  I cannot run it. The project *is* linked (`supabase/.temp/project-ref` →
  `swrmqpelgoblaquequzb`), so on a credentialed machine it is one command.
- **MCP `apply_migration`** would work, but it assigns its **own** ledger
  timestamp — drifting from the committed file versions and breaking
  `supabase migration list` parity. Per `akos-holistika-operations.mdc`, that is
  break-glass only. Creating ledger drift to fix data drift trades one
  governance debt for another, so I did not.
- **MCP `execute_sql`** can apply mirror DML, but the full re-sync is hundreds of
  KB of upserts per large table — that is the `psql` path, run with the same
  credentials.

So the bulk fix is genuinely a **credentialed operator operation**. I caught it,
quantified it, staged it, and wrote the runbook below.

## 4 — The runbook (3 commands; you have the credentials)

Run from repo root with the Supabase CLI authenticated (`supabase login` or
`SUPABASE_ACCESS_TOKEN` set) and the DB password available.

```bash
# 1. Apply the 3 pending additive migrations to prod (clean, version-preserving).
npx supabase db push

# 2. Emit the full mirror DML (idempotent upserts) from canonical CSVs.
py scripts/sync_compliance_mirrors_from_csv.py --output artifacts/sql/prod-resync-2026-05-29.sql

# 3. Apply the emitted DML to prod (psql, or the dashboard SQL editor in batches).
#    Connection string from: Supabase dashboard → Project Settings → Database.
psql "$PROD_CONNECTION_STRING" -f artifacts/sql/prod-resync-2026-05-29.sql
```

**Verify after:**

```sql
select 'decision' t, count(*) from compliance.decision_register_mirror
union all select 'ops', count(*) from compliance.ops_register_mirror
union all select 'process_list', count(*) from compliance.process_list_mirror;
-- expect 466 / 136 / 1186
```

Then run `get_advisors` (security) via the Supabase MCP to confirm the new
collaborator-share tables inherited the correct RLS (`service_role` only;
`anon`/`authenticated` revoked — the migration sets this, this is a belt-and-braces check).

**Note (IntelligenceOps data lane):** `sync_compliance_mirrors_from_csv.py` has
**no `--intelligenceops` emit path** yet, so step 2 will not populate the 4
radar rows. That emit helper is a small follow-up (see §6 OPS row).

## 5 — Neo4j projection (the other core component you named)

The HLK graph projection (`scripts/sync_hlk_neo4j.py` → Neo4j) reads the same
canonical CSVs. It is a **second** propagation lane with the same staleness risk.
I could not check its live state (no Neo4j credentials in this environment). It
belongs in the same standing checklist (§7) and the same OPS sweep. When the
Supabase lane is re-synced, the Neo4j projection should be re-run in the same
pass so the two stay coherent.

## 6 — RACI for this propagation (founder-delegated PM model)

| Activity | Responsible | Accountable | Consulted | Informed |
|:---|:---|:---|:---|:---|
| Catch + quantify drift (this report) | Agent (PMO-delegated) | Operator | — | System Owner |
| Apply migrations + mirror sync (runbook §4) | Operator (credentials) | Operator | System Owner | Tech |
| `--intelligenceops` emit helper | Agent / AIC | System Owner | — | Operator |
| Neo4j re-projection | Operator / AIC | System Owner | — | Tech |
| Standing sweep wiring (§7) | Agent / AIC | System Owner | PMO | Operator |

OPS rows filed (see `OPS_REGISTER.csv`): the mirror re-sync + the intelligenceops
emit helper + the Neo4j re-projection are tracked there so they do not evaporate.

## 7 — Standing cross-area Tech propagation checklist (do the same with others)

So this is **never silently forgotten again**, every wave-close / canonical-CSV
mint inherits this check (folds into the inter-wave regression sweep
`deploy_evidence_completeness` dimension as a forward extension):

1. **Which canonical CSVs changed this wave?** (git diff on `…/canonicals/**`).
2. **Does each have a Supabase mirror?** (`compliance.<name>_mirror`). If a new
   CSV: was its mirror DDL migration authored **and applied**?
3. **Is the mirror schema current?** (any `ADD COLUMN` migration since last sync
   applied to prod? — `list_migrations` vs `supabase/migrations/`).
4. **Is the mirror data current?** (`select count(*)` vs git row count).
5. **Does it surface in Neo4j?** If yes, re-run the projection.
6. **Does a consumer read it?** (ERP panel, dashboard, KiRBe, RPA) — note the
   downstream so staleness impact is visible.
7. **Record the result** in the wave UAT §3 mechanical-evidence as a
   prod-parity row (not just "validators PASS locally").

The lesson: **local `validate_hlk.py` PASS ≠ in production.** The mirror is the
production surface for a canonical CSV; the check above closes the gap between
"committed" and "live" that this sweep just found.

## 8 — Cross-references

- Discovery: Supabase MCP `list_projects` / `list_migrations` / `execute_sql` (read-only), 2026-05-29.
- Two-plane SQL gate: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"Operator SQL gate".
- Migration parity map: [`supabase/migrations/README.md`](../../../../supabase/migrations/README.md).
- Mirror emit runbook: [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py).
- Pending migrations: `supabase/migrations/20260525000000…`, `20260526000000…`, `20260529120000…`.
- Wave R+5 close UAT: [`uat-wave-r-plus-5-close-2026-05-29.md`](uat-wave-r-plus-5-close-2026-05-29.md).
