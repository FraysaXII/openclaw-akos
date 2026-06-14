# I99 — EG-5 implementation spec (2026-06-13)

**Initiative:** I99 Supabase Platform EG-5 Tranche (`INIT-OPENCLAW_AKOS-99`)  
**Parent:** I95 L1 Supabase ecosystem governance (`D-IH-95-G`)  
**Ratified strategy:** Option B — full EG-5 tranche + Advisor enabled + I96 first consumer

---

## Scope

### In scope (P0–P7)

| Module | Registry ID | P0–P7 deliverable |
|:---|:---|:---|
| **Auth** | SUPA-MOD-22 | Hook/provider registry; blessed-repo SSR contract; I96 redirect fix path |
| **Realtime** | SUPA-MOD-21 | Publication + channel registry; I96 freshness strip wiring spec |
| **Storage** | SUPA-MOD-23 | Bucket/path RLS registry; GTM asset delivery posture |
| **Advisor** | (MCP tool) | Read-only `get_advisors` in MCP; post-DDL reconcile checklist in P1 |

### Out of scope (scheduled elsewhere)

| Item | Posture | Owner |
|:---|:---|:---|
| EG-4 RLS posture validator | **scheduled** I99 P6 | I99 P6 paired with Advisor findings |

> **Note (2026-06-13):** Operator expanded P5 to cover **all eight** previously `ungoverned` module registry rows (D-IH-99-D). Items below are now **in P5 tranche**, not deferred.

| Module | Registry ID | P5 target status |
|:---|:---|:---|
| kirbe schema | SUPA-MOD-07 | `reference-only` (document app-owned boundary) |
| Edge secrets | SUPA-MOD-12 | `partial` + secrets path manifest |
| pg_vector | SUPA-MOD-17 | `partial` (hosted enabled per P1; I83 consumer) |
| Database Webhooks | SUPA-MOD-20 | `partial` or explicit defer row in registry |
| seed SQL | SUPA-MOD-26 | `partial` (mint or stub `seed.sql`) |

---

## Execution order

1. **P1 — MCP inventory reconcile**  
   Run `list_migrations`, `list_extensions`, `get_advisors`; diff against `SUPABASE_MODULE_REGISTRY.csv` and prod-lag notes in `supabase/migrations/README.md`.

2. **P2 — Auth (I96 consumer first)** — **DONE** draft 2026-06-13  
   - Spec: [`reports/auth-registry-and-i96-consumer-spec-2026-06-13.md`](reports/auth-registry-and-i96-consumer-spec-2026-06-13.md)  
   - Draft: [`drafts/SUPABASE_AUTH_REGISTRY.draft.csv`](drafts/SUPABASE_AUTH_REGISTRY.draft.csv)  
   - Canonical mint + validator at **P5** AskQuestion gate.

3. **P3 — Realtime (I96 freshness strip first)** — **DONE** draft 2026-06-13  
   - Spec: [`reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md`](reports/realtime-publication-and-i96-freshness-spec-2026-06-13.md)  
   - Draft: [`drafts/SUPABASE_REALTIME_REGISTRY.draft.csv`](drafts/SUPABASE_REALTIME_REGISTRY.draft.csv)  
   - Publication DDL + canonical mint at **P5** gate; hlk-erp subscribe at **I96 B2.4**.

4. **P4 — Storage (GTM + operator evidence)** — **DONE** draft 2026-06-13  
   - Spec: [`reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md`](reports/storage-bucket-and-gtm-asset-spec-2026-06-13.md)  
   - Draft: [`drafts/SUPABASE_STORAGE_REGISTRY.draft.csv`](drafts/SUPABASE_STORAGE_REGISTRY.draft.csv)  
   - Bucket DDL + canonical mint at **P5** gate.

5. **P5 — Canonical CSV tranche (operator gate)** — **DONE** 2026-06-13 (**D-IH-99-J**)  
   - **EG-5 core:** Auth, Realtime, Storage registries + module flips.  
   - **Also in tranche:** Edge secrets, pg_vector, Database Webhooks, kirbe schema, seed SQL — partial/reference-only posture.  
   - **Follow-up (scheduled):** Realtime publication migration `20260613150000_i99_realtime_publication_i96_i62.sql` — operator SQL gate; Storage bucket DDL separate gate.

---

## Two-plane rules (non-negotiable)

- DDL proposals → `supabase/migrations/` → operator SQL gate → apply.  
- Registry/mirror rows → CSV emit → `compliance_mirror_emit` → operator apply.  
- MCP: SELECT + Advisor only until P5 processes exist.

---

## Verification

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/supabase-platform-features-holistika-impact-2026-06-13/source-ledger.csv
py scripts/validate_hlk.py
py scripts/validate_initiative_registry_frontmatter_sync.py
```

---

## Cross-references

- Master roadmap: [`../master-roadmap.md`](../master-roadmap.md)
- Research synthesis: [`../../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/research-synthesis-2026-06-13.md`](../../../intelligence/supabase-platform-features-holistika-impact-2026-06-13/research-synthesis-2026-06-13.md)
- Operator SQL gate: [`../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
