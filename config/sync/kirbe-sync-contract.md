# KiRBe Sync Contract

**Status**: Draft for next tranche
**Date**: 2026-04-03
**Source**: Database audit of `full_dump.sql` + canonical vault analysis

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

## 3. Canonical-to-KiRBe Propagation Ownership (NBT.2)

### Direction of Authority

```
Canonical vault (docs/references/hlk/compliance/)
    |
    v  (one-way sync, canonical always wins)
    |
KiRBe Supabase (downstream mirror)
```

### Table-Level Ownership

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
| `kirbe.*` (platform tables) | KiRBe app state | App-managed | Not synced from canonical vault |
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

All sync operations and DB cleanup actions described here are gated behind explicit operator approval per `docs/references/hlk/compliance/PRECEDENCE.md`. No automated sync runs until the stable-key policy is frozen and the operator confirms the cleanup list.
