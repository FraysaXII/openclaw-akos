---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
---

# Three-plane field mapping

Machine-keyed crosswalk: Govern → Mirror → Execute → Experience.

| Govern (AKOS git) | Supabase mirror | KiRBe execute | ERP experience |
|:---|:---|:---|:---|
| `docs/wip/intelligence/*/source-ledger.csv` | — (future `research.*` views) | Vault doc + `SRC-{pack}-{seq}` tag | Ledger summary panel (row counts, prong breakdown) |
| `INTELLIGENCEOPS_REGISTER.csv` | `intelligenceops_register_mirror` (when emitted) | Re-ingest on STALE | Radar queue panel + **freshness strip radar badge** |
| Methodology canonicals under `Research/Methodology/` | compliance mirrors (indirect via vault path) | Hybrid search index | KiRBe search panel |
| `RESEARCH_RADAR_DISCIPLINE` sweep output | — | Embedding refresh job | `next_verify_by` strip |
| Mirror emit timestamps | `intelligenceops_register_mirror` + future heartbeat view | — | Realtime → freshness strip — **canonical** [`SUPABASE_REALTIME_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_REALTIME_REGISTRY.csv) (I99 P5 **D-IH-99-J**); hlk-erp subscribe at **I96 B2.4** |
| `PRECEDENCE.md` / process_list | `process_list_mirror` | Read-only context | Process count badge |
| Session recap / I96 roadmap | — | — | WIP pack list (GitHub Contents) |

## SRC tag convention

See [`src-tagging-contract.md`](src-tagging-contract.md).

## Staleness

See [`staleness-loop-spec.md`](staleness-loop-spec.md).

## Authority rules

1. Git canonical wins over mirror (PRECEDENCE.md)
2. KiRBe never writes `compliance.*`
3. ERP is read-only v1 — no canonical edits from UI
