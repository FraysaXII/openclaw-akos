# MasterData Supabase inventory (read-only snapshot)

**Date:** 2026-04-17  
**Project:** `MasterData` (`swrmqpelgoblaquequzb`, EU Central)

| Observation | Notes |
|---------------|--------|
| `public."Process list"` | **0 rows** — legacy v2.4 shell; git `process_list.csv` is SSOT |
| `baseline_organisation` (public) | **49 rows** — stale vs git canonical |
| `standard_process` / `workflows` / `workstreams` | Legacy — **deprecate** per plan |
| `kirbe.monitoring_logs` | **~2.67M rows** — retention/partition/cost governance required |
| Duplicate vectors | `public.data_kirbe_document_vectors_1536` vs `kirbe.*` — consolidate to **`kirbe.*`** |

**Reconciliation:** Run diff vs `py scripts/validate_hlk.py` output after mirror ingest ships.
