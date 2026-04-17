# `kirbe.monitoring_logs` governance

**Risk:** ~2.67M rows — unbounded growth affects cost and query latency.

**Controls:**

- Retention policy (time-based purge or partition).
- Indexes on hot filters.
- Cost budget alert.
- **SOP:** what may be logged (no secrets; categories only in operator docs).

**Ref:** [Supabase shared responsibility](https://supabase.com/docs/guides/platform/shared-responsibility-model).
