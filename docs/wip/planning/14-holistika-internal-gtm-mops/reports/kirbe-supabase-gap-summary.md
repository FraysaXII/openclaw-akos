# KiRBe + Supabase gap summary

**Date:** 2026-04-17

| Gap | Evidence | Action |
|-----|----------|--------|
| `kirbe_source_type` enum | No Meta/Google Ads/etc. | Extend with `api_connector` + JSONB **or** strict `web`/`database` provenance |
| CSV mirrors | `yy_all_in_one` lacks full HLK CSV sync | Idempotent ingest from openclaw-akos CSVs; `validate_hlk.py` gate |
| Marketing facts | Document-centric today | Optional `marketing_raw_events` / facts tables + RLS |
| Agent MCP | — | **Phase 3b** after connector registry |

**KiRBe repo SSOT:** `root_cd/kirbe/supabase/sql/yy_all_in_one.sql` — coordinate migrations with this initiative.
