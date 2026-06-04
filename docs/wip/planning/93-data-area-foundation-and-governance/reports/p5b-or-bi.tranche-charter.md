---
tranche_id: i93-p5b-bi-integration-full-pack
tranche_class: internal_governance
tranche_title: I93 P5b — BI/integration governance full pack + component matrix tranche
audiences_named:
  - J-OP
  - J-AIC
channels_named:
  - CHAN-WEB-DASHBOARD
scenarios_named:
  - data_steward_runs_bi_integration_readiness_before_p6
  - engagement_scaffold_converts_suez_demo_spec_to_stream_b
brand_register: internal-corpint
ratifying_decisions:
  - D-IH-93-I
  - D-IH-93-D
is_atomic_commit: true
reversibility_class: medium
reversibility_rationale: Amended D-IH-93-I + new canonicals revert cleanly; matrix row adds are additive; Power Platform dedupe is notes-only.
closing_loop_test: py scripts/synthesis_before_tranche_check.py --check-charter reports/p5b-or-bi.tranche-charter.md PASS + py scripts/bi_integration_readiness_check.py --self-test PASS + py scripts/validate_hlk.py OVERALL PASS
recipient_fallback_channel: n/a — internal governance tranche
operator_framing_quote: execute the BI/integration full pack before P6 DATA-FAM
---

# I93 P5b tranche charter — BI/integration full pack

## Scope (in)

- Amend `D-IH-93-I` from not-now → Postgres-native warehouse + tiered BI consumers.
- Mint `DATA_BI_GOVERNANCE.md`, `DATA_INTEGRATION_PLANE.md`.
- Mint `BI_CONSUMER_REGISTRY.csv`, `RPA_ADAPTER_REGISTRY.csv` (9th adapter class).
- Mint `SOP-DATA_ENGAGEMENT_INTEGRATION_SCAFFOLD_001.md`, `SOP-DATA_SUEZ_STREAM_B_LIBELLE_001.md`.
- Mint `scripts/bi_integration_readiness_check.py`, `scripts/validate_bi_consumer_registry.py`.
- COMPONENT_SERVICE_MATRIX tranche (Langfuse, Neo4j, hlk-erp, Metabase, Power BI, Edge, etc.).
- `DATA_ARCHITECTURE.md` §9 Supabase module table.
- Index updates: CANONICAL_REGISTRY, PRECEDENCE, KNOWLEDGE_PAIRING, DATA_CONTRACT seed.

## Scope (out)

- Snowflake/BigQuery primary warehouse build.
- Analytics Buckets until GA.
- Client-tenant Power Automate flow implementation inside AKOS.
- Composio adoption.

## Verification

```powershell
py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/93-data-area-foundation-and-governance/reports/p5b-or-bi.tranche-charter.md
py scripts/bi_integration_readiness_check.py --self-test
py scripts/validate_bi_consumer_registry.py
py scripts/validate_adapter_registries.py
py scripts/validate_component_service_matrix.py
py scripts/validate_hlk.py
py -m pytest tests/test_bi_integration_readiness_check.py -v
```
