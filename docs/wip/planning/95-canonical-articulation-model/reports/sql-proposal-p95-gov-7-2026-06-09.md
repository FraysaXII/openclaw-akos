---
tranche_id: P95-GOV-7
tranche_class: canonical_csv_mint
ratifying_decisions:
  - D-IH-95-B
  - D-IH-93-D
  - D-IH-93-I
  - D-IH-88-E
reversibility_class: medium
proposal_only: true
---

# Operator SQL gate — P95-GOV-7 forward-charter mirror DDL

**Date:** 2026-06-09  
**Tranche:** Promote six forward-charter compliance mirrors from git DDL (apply **not** executed in this tranche)

## Discover (read-only)

| Check | Command / surface | Expected |
|:---|:---|:---|
| Remote migration ledger | `npx supabase migration list --linked` | No local-only `2026060912*` rows applied yet |
| Table absence pre-apply | MCP `list_tables` / `information_schema` SELECT | `pricing_tier_registry_mirror`, `finops_performance_obligation_registry_mirror`, `finops_tax_calendar_mirror`, `data_contract_registry_mirror`, `rpa_adapter_registry_mirror`, `component_service_matrix_mirror` absent or empty |
| RLS posture | `pg_policies` SELECT | After apply: deny `anon` + `authenticated`; `service_role` GRANT only |

## Proposed DDL (git SSOT)

| Migration file | Mirror table(s) |
|:---|:---|
| `20260609120000_p95_gov7_finance_registry_mirrors.sql` | `compliance.pricing_tier_registry_mirror`, `compliance.finops_performance_obligation_registry_mirror`, `compliance.finops_tax_calendar_mirror` |
| `20260609120100_p95_gov7_data_contract_registry_mirror.sql` | `compliance.data_contract_registry_mirror` |
| `20260609120200_p95_gov7_rpa_adapter_registry_mirror.sql` | `compliance.rpa_adapter_registry_mirror` |
| `20260609120300_p95_gov7_component_service_matrix_mirror.sql` | `compliance.component_service_matrix_mirror` |

Enum CHECK constraints align with Pydantic / `VALID_*` frozensets (`py scripts/validate_pydantic_mirror_enum_ssot.py`).

## Rollback (operator break-glass)

```sql
BEGIN;
DROP TABLE IF EXISTS compliance.component_service_matrix_mirror;
DROP TABLE IF EXISTS compliance.rpa_adapter_registry_mirror;
DROP TABLE IF EXISTS compliance.data_contract_registry_mirror;
DROP TABLE IF EXISTS compliance.finops_tax_calendar_mirror;
DROP TABLE IF EXISTS compliance.finops_performance_obligation_registry_mirror;
DROP TABLE IF EXISTS compliance.pricing_tier_registry_mirror;
COMMIT;
```

Then `supabase migration repair` to mark the four versions reverted if they were applied.

## Apply path (post-approval)

1. `npx supabase db push --linked` (four migrations only; ledger must be clean preflight).
2. `py scripts/verify.py compliance_mirror_emit` → operator-reviewed DML apply per [`docs/guides/holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md).
3. Row-count parity: `py scripts/validate_mirror_emit_contract.py`.

## RLS summary

All six tables: `ENABLE ROW LEVEL SECURITY`; policies `{table}_deny_authenticated` + `{table}_deny_anon` (`USING (false)`); `REVOKE ALL FROM PUBLIC`; `GRANT ALL TO service_role`.

**Status:** PROPOSED — mechanical validators green in git; prod apply deferred to operator gate.
