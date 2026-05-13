# KiRBe Sync Contract

**Status**: Section 2 rewritten for 16 mirrors (Initiative 32 P7); §11 cross-repo contract added.
**Date**: 2026-04-30 (rewrite); original draft 2026-04-03
**Source**: Database audit of `full_dump.sql` + canonical vault analysis + AKOS PRECEDENCE.md (16 canonical mirrors as of I32)
**Related**: D-IH-32-G (freeze until I32-P7), D-IH-32-K (cross-repo contract), D-IH-32-M (KiRBe Neo4j stays separate from AKOS Neo4j), D-IH-32-P (bilingual cover-emails for handoff)

---

## 1. Database Schema Inventory

The Supabase database contains **117 tables** across **10 schemas**:

| Schema | Tables | Role |
|--------|--------|------|
| `public` | 36 | Core business data: baseline_organisation, processes, facts, intel, documents, vectors |
| `compliance` | 4 | Frozen taxonomy: access_level, confidence_level, source_category, source_level |
| `compliance_001` | 2 | SOP ingestion: sop_documents, sop_sections |
| `kirbe` | 32 | KiRBe platform: vaults, documents, vectors, ingestion, org memberships, billing |
| `llamaindexagent` | 4 | Legacy LlamaIndex agent state: agent_states, function_calls, workflows |
| `gemini_fastapi` | 1 | Legacy Gemini integration: chat_sessions |
| `auth` | 23 | Supabase auth (managed) |
| `storage` | 8 | Supabase storage (managed) |
| `realtime` | 3 | Supabase realtime (managed) |
| `supabase_functions` | 2 | Edge functions (managed) |

## 2. Stable Machine-Key Policy (NBT.1)

| Entity Type | Key Field | Format | Authority |
|-------------|-----------|--------|-----------|
| Org roles | `org_id` | `org_NNN` | `baseline_organisation.csv` |
| Process items | `item_id` | `{prefix}_dtp_{NNN}` | `process_list.csv` |
| Access levels | UUID | UUID v4 | `access_levels.md` |
| Confidence levels | UUID | UUID v4 | `confidence_levels.md` |
| Source categories | UUID + enum | UUID + `source_category` enum | `source_taxonomy.md` |
| Source levels | UUID | UUID v4 | `source_taxonomy.md` |

All machine keys originate in the canonical vault files. The database receives them via sync, never generates them.

## 2. Canonical-to-KiRBe Propagation Ownership (Initiative 32 P7 rewrite — 16 mirrors)

### Direction of Authority

```
AKOS canonical vault (docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/)
    |
    v  (one-way sync, canonical always wins per PRECEDENCE.md)
    |
Supabase compliance.* mirrors (server-side; service_role only; deny anon + authenticated)
    |
    v  (RLS-scoped read-only; KiRBe ingests via its service_role-scoped sync job)
    |
KiRBe Supabase (downstream consumer; never writes to compliance.*)
```

### The 16 canonical mirrors (post-Initiative 32 close)

KiRBe consumes these read-only via Supabase RLS. Per Q6 (operator decision pending), the consumption pattern is RLS read-only by default; versioned JSON snapshot is the alternative for environments without Postgres access.

| # | Mirror table (compliance.* schema) | Source CSV | Sync direction | RLS posture | Consumer role |
|---|------------------------------------|------------|----------------|-------------|---------------|
| 1 | `process_list_mirror` | `process_list.csv` | Canonical → mirror | Deny anon + authenticated; service_role only | `service_role` (KiRBe sync job) |
| 2 | `baseline_organisation_mirror` | `baseline_organisation.csv` | Canonical → mirror | Same as above | `service_role` |
| 3 | `finops_counterparty_register_mirror` | `FINOPS_COUNTERPARTY_REGISTER.csv` | Canonical → mirror | Same | `service_role` |
| 4 | `goipoi_register_mirror` | `dimensions/GOI_POI_REGISTER.csv` (relocated I32 P7) | Canonical → mirror | Same; PII obfuscation (POL-PII-GOIPOI-DISPLAY-NAME-OBFUSCATION) | `service_role` |
| 5 | `adviser_engagement_disciplines_mirror` | `ADVISER_ENGAGEMENT_DISCIPLINES.csv` | Canonical → mirror | Same | `service_role` |
| 6 | `adviser_open_questions_mirror` | `ADVISER_OPEN_QUESTIONS.csv` | Canonical → mirror | Same | `service_role` |
| 7 | `founder_filed_instruments_mirror` | `FOUNDER_FILED_INSTRUMENTS.csv` | Canonical → mirror | Same | `service_role` |
| 8 | `program_registry_mirror` | `dimensions/PROGRAM_REGISTRY.csv` | Canonical → mirror | Same | `service_role` |
| 9 | `topic_registry_mirror` | `dimensions/TOPIC_REGISTRY.csv` | Canonical → mirror | Same | `service_role` |
| 10 | `persona_registry_mirror` | `dimensions/PERSONA_REGISTRY.csv` (I31 P2.1) | Canonical → mirror | Same | `service_role` |
| 11 | `channel_touchpoint_registry_mirror` | `dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` (I31 P3) | Canonical → mirror | Same | `service_role` |
| 12 | `sourcing_register_mirror` | `dimensions/SOURCING_REGISTER.csv` (I31 P5.2) | Canonical → mirror | Same | `service_role` |
| 13 | `validation_runs` | (operational; no source CSV — written by `validate_hlk.py --json` ingest) | Operational write | Deny anon + authenticated; service_role only | `service_role` (CI / cron) |
| 14 | `skill_registry_mirror` | `dimensions/SKILL_REGISTRY.csv` (I32 P2) | Canonical → mirror | Same; tenant_scope='shared' until I34 | `service_role` |
| 15 | `touchpoint_kit_cell_mirror` | `dimensions/TOUCHPOINT_KIT_CELL_REGISTRY.csv` (I32 P3) | Canonical → mirror | Same; FS-vs-CSV drift enforced canonical-side | `service_role` |
| 16 | `policy_register_mirror` | `dimensions/POLICY_REGISTER.csv` (I32 P4) | Canonical → mirror | Same; self-referential (POL-RLS-POLICY-REGISTER-MIRROR-I32) | `service_role` |

Plus 1 operational mirror introduced in I32 P7:

| # | Mirror table | Purpose | RLS posture | Consumer role |
|---|--------------|---------|-------------|---------------|
| 17 | `repo_health_snapshot_mirror` | Append-only weekly pull-based snapshot of external Holistika repo state (D-IH-32-L) | Deny anon + authenticated; service_role only | `service_role` (AKOS-side cron only; KiRBe does NOT read or write this) |

### Table-Level Ownership (legacy section retained for reference)

| DB Table | Canonical Source | Sync Direction | Notes |
|----------|-----------------|----------------|-------|
| `public.baseline_organisation` | `baseline_organisation.csv` | Canonical -> DB | Row count must match |
| `compliance.access_level` | `access_levels.md` | Canonical -> DB | UUID-keyed |
| `compliance.confidence_level` | `confidence_levels.md` | Canonical -> DB | UUID-keyed |
| `compliance.source_category` | `source_taxonomy.md` | Canonical -> DB | Enum + UUID |
| `compliance.source_level` | `source_taxonomy.md` | Canonical -> DB | UUID-keyed |
| `compliance_001.sop_documents` | `v3.0/` SOP markdown files | Canonical -> DB | Markdown-first authoring |
| `compliance_001.sop_sections` | Derived from sop_documents | Canonical -> DB | Sections extracted at sync time |
| `public.standard_process` | `process_list.csv` | Canonical -> DB | May need schema reconciliation |
| `public.rules` | Not yet defined | Canonical -> DB | Currently empty, pending policy |
| `public.fact_table` | Intelligence matrix | Canonical -> DB | Forensic data, needs review |
| `kirbe.*` (platform tables) | KiRBe app state | App-managed | Not synced from canonical vault. **Per D-IH-32-M**: KiRBe's local Neo4j (vault search graph) is independent of the AKOS Neo4j governance projection; do NOT cross-merge. |
| `auth.*`, `storage.*` | Supabase managed | N/A | Infrastructure only |

### Conflict Resolution

1. **Canonical wins**: When canonical and DB disagree, resync from canonical.
2. **Log the incident**: Record what drifted, when, and the resolution.
3. **Never mutate canonical from DB state**: The DB is a mirror, not an authoring surface.

## 4. Stale/Orphan Rows to Clean (NBT.5 input)

| Table | Issue | Action |
|-------|-------|--------|
| `public.rules` | Empty (0 rows) | Define policy authoring path or remove table |
| `public.test_*` (5 tables) | Test/dev artifacts | Drop on clean rebuild |
| `public.users2` | Legacy duplicate | Drop on clean rebuild |
| `public.example_csv` | Sample data | Drop on clean rebuild |
| `public.rag_2`, `public.nods_page` | Legacy experiments | Drop on clean rebuild |
| `llamaindexagent.*` | Legacy agent state | Archive then drop |
| `gemini_fastapi.*` | Legacy Gemini state | Archive then drop |
| `public.data_document_vectors` | Legacy vectors | Drop after KiRBe migration |
| `public.document_vectors` | Legacy vectors | Drop after KiRBe migration |
| `public.madeira_document_store` | Legacy Madeira store | Archive then drop |
| `public.madeira_index_store` | Legacy Madeira index | Archive then drop |

## 5. Deterministic Replay Design (NBT.4)

Future sync automation should follow these principles:

1. **Idempotent**: Running the sync twice produces the same result.
2. **Traceable**: Each sync run produces a log entry with row counts, diffs, and timestamp.
3. **Rebuildable**: The DB can be rebuilt entirely from canonical vault files + sync scripts.
4. **Gated**: Canonical edits require operator approval per `PRECEDENCE.md` before sync propagates them.
5. **Testable**: `py scripts/validate_hlk.py` validates the canonical side; a future `validate_kirbe_sync.py` validates the DB side.

## 6. Approval Gate

All sync operations and DB cleanup actions described here are gated behind explicit operator approval per `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md`. No automated sync runs until the stable-key policy is frozen and the operator confirms the cleanup list.

## 11. Cross-repo contract (NEW Initiative 32 P7, D-IH-32-K)

KiRBe (alongside `boilerplate` and `hlk-erp`) is governed by the AKOS-published **EXTERNAL_REPO_CONTRACT.md** (template at `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md`). The 1-page contract instance lands at the KiRBe repo root via the I32 P7 PR patch (`reports/external-repo-seed-prs/kirbe.patch`) and codifies:

- **3 invariants** (non-negotiable): language frontmatter on every canonical MD; brand-jargon audit on external prose; git-canonical for source code, mirror-derived for HLK doctrine.
- **5 do-not rules**: do not author HLK CSVs locally; do not denormalise mirror data into local schemas as SSOT; do not skip the operator SQL gate; do not embed AKOS HLK content as code comments; do not invent persona / channel / sourcing / skill / topic / program / GOI/POI IDs locally.
- **1 do rule**: read AKOS canonicals via `compliance.*_mirror` (RLS read-only) or via the dated handoff bundle.

A small `.cursor/rules/akos-mirror.mdc` cursor rule lands alongside the contract (template at `.cursor/rules/akos-mirror-template.mdc` in AKOS) so cursor sessions in the KiRBe repo always have the AKOS HLK doctrine reminder loaded (`alwaysApply: true`).

AKOS observes KiRBe weekly via `scripts/snapshot_external_repos.py` writing one row to `compliance.repo_health_snapshot_mirror` (`repo_slug=kirbe-platform`). 4-consecutive-week regressions trigger Initiative 42 (cross-repo CI integration).

**Things explicitly NOT changed by I32 P7 + this rewrite:**

- KiRBe billing-plane discipline (`hlk_billing_plane` metadata, `kirbe.*` vs `holistika_ops.*` separation) — unchanged.
- KiRBe LlamaIndex pipeline and reader composition — unchanged.
- KiRBe local Neo4j (vault search graph, per `kirbe/.cursor/rules/60-graphdb-neo4j.mdc`) — stays independent of AKOS Neo4j (D-IH-32-M reaffirmed in I46 P1 [`NEO4J_STRATEGY.md`](../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md): AKOS Neo4j = governance KG; KiRBe Neo4j = vault search; do not cross-merge. Two independent stores, two independent lifecycles, two independent cost lines.).
- KiRBe's existing 36 cursor rules — unchanged; akos-mirror.mdc adds, does not replace.
