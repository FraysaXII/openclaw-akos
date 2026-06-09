---
authored: 2026-06-10
tranche: I95-T5
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L1-EG-3
decision_ids:
  - D-IH-95-G
---

# P0 research — I95 L1 EG-3 Supabase registries

Planner-quality evidence packet before EG-3 registry mint.

## Internal evidence sweep

| Source | Trust | Finding |
|:---|:---|:---|
| [`SUPABASE_ECOSYSTEM_GOVERNANCE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md) §3 | SSOT | EG-3 mints edge-fn CSV + cron CSV + extension manifest; closes SUPA-MOD-11/14/15/19 |
| [`SUPABASE_MODULE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_MODULE_REGISTRY.csv) | SSOT | MOD-11 partial (3 functions); MOD-14/15 partial/ungoverned; MOD-19 partial — all name registry gaps |
| [`supabase/functions/`](../../../../supabase/functions/) | Repo | 3 deployable functions: `stripe-webhook-handler`, `finops-writer-worker`, `fx-rate-cache-refresh` (+ `_shared` helpers) |
| [`20260524005543_…finops_writer_worker_cron_schedule.sql`](../../../../supabase/migrations/20260524005543_i81_p2_b2c_finops_writer_worker_cron_schedule.sql) | Migration | Job `finops_writer_worker_every_minute` → `* * * * *` → finops-writer-worker |
| [`20260524005706_…fx_rate_cache_cron_schedule.sql`](../../../../supabase/migrations/20260524005706_i81_p2_b2c_fx_rate_cache_cron_schedule.sql) | Migration | Job `fx_rate_cache_refresh_daily` → `30 15 * * *` → fx-rate-cache-refresh |
| [`20260524000000_…finops_writer_substrate.sql`](../../../../supabase/migrations/20260524000000_i81_p2_b2_finops_writer_substrate.sql) | Migration | `CREATE EXTENSION IF NOT EXISTS pgmq` — only explicit extension DDL in repo |
| [`RPA_ADAPTER_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/dimensions/RPA_ADAPTER_REGISTRY.csv) | SSOT | `holistika_edge` → stripe-webhook-handler only; finops/fx workers not adapter-registered (forward gap) |
| [`SUPABASE_API_EXPOSURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_API_EXPOSURE.md) | Precedent | EG-2 markdown SSOT + module promotion — replicate shape for extension manifest |
| [`supabase-eg2-execution-2026-06-07.md`](supabase-eg2-execution-2026-06-07.md) | Report | EG-3..5 explicitly deferred post EG-2 |

## Live surface inventory (repo-only; no MCP this tranche)

| Class | Count | IDs / names |
|:---|:---:|:---|
| Edge Functions | 3 | stripe-webhook-handler, finops-writer-worker, fx-rate-cache-refresh |
| pg_cron jobs | 2 | finops_writer_worker_every_minute, fx_rate_cache_refresh_daily |
| Extensions (AKOS-relevant) | 5 | pgmq (DDL in repo), pg_cron + pg_net (cron SQL only), wrappers (I18 FDW), vector (forward/I46) |

## Novelty test (applied-research RULE 2)

EG-3 registries are **refinement** of the EG-1 module inventory + EG-2 exposure-doc pattern (D-IH-95-G). No novel framing — **external citation optional**.

## Disposition plan

| Item | Disposition | Rationale |
|:---|:---|:---|
| Mint 3 edge-fn rows | **deterministic-fix-now** | Matches live `supabase/functions/` |
| Mint 2 cron rows | **deterministic-fix-now** | Matches I81 cron migrations |
| Extension manifest | **deterministic-fix-now** | Documents ext posture; pg_cron CREATE EXTENSION remains forward debt in `gap` column |
| RPA adapter gaps (2/3 functions) | **defer-OPS** | Out of EG-3 scope; note in registry `notes` |
| Cron anon-key-in-SQL | **document-gap** | SOC finding; rotation forward debt — do not rewrite migrations this tranche |
| process_list / baseline CSV | **out-of-scope** | No operator gate triggered |

## Tranche 5 scope boundary

**In:** Three registries + validators + module-registry promotion + PRECEDENCE + cluster map + files-modified + CHANGELOG.

**Out:** DDL migrations, RPA_ADAPTER rows, cron SQL refactor (key rotation), EG-4/EG-5, OPS-95-2.
