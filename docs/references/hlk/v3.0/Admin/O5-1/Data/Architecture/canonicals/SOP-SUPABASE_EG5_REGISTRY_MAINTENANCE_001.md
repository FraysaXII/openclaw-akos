---
title: SOP — Supabase EG-5 Registry Maintenance
language: en
intellectual_kind: data-sop
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - System Owner
last_review: 2026-06-13
last_review_decision_id: D-IH-99-J
status: active
register: internal
linked_canonicals:
  - ../Architecture/canonicals/SUPABASE_ECOSYSTEM_GOVERNANCE.md
  - ../Architecture/canonicals/dimensions/SUPABASE_AUTH_REGISTRY.csv
  - ../Architecture/canonicals/dimensions/SUPABASE_REALTIME_REGISTRY.csv
  - ../Architecture/canonicals/dimensions/SUPABASE_STORAGE_REGISTRY.csv
  - ../Architecture/canonicals/dimensions/SUPABASE_MODULE_REGISTRY.csv
---

# SOP — Supabase EG-5 Registry Maintenance

> Maintains the **Auth**, **Realtime**, and **Storage** Supabase registries minted at I99 P5
> (decision **D-IH-99-J** — the EG-5 canonical CSV tranche). Covers provider rows, publication
> subscriptions, bucket paths, Analytics/Iceberg links, and Vector platform boundaries.

## Purpose

Keep Supabase platform surfaces governable from git: every Auth provider, Realtime subscription,
and Storage bucket/path change gets a registry row before hosted Dashboard edits land.

## Scope

- `SUPABASE_AUTH_REGISTRY.csv` — providers, redirects, hooks, SMTP, consumer bindings
- `SUPABASE_REALTIME_REGISTRY.csv` — publications, channels, I96 freshness strip bindings
- `SUPABASE_STORAGE_REGISTRY.csv` — buckets, RLS classes, git-first UAT posture, Analytics + Vector links
- Paired updates to `SUPABASE_MODULE_REGISTRY.csv` when module posture changes

Out of scope: KiRBe embedding table DDL (kirbe schema — app-owned); Neo4j T3 graph (I91/I93).

## Inputs

- Initiative spec under `docs/wip/planning/99-supabase-platform-eg5-tranche/reports/`
- Operator SQL gate evidence when publication or bucket DDL applies
- `baseline_organisation.csv` for `owner_role` resolution

## Steps

1. **Draft in wip** — add rows to `docs/wip/planning/99-supabase-platform-eg5-tranche/drafts/` during planning phases.
2. **Validate drafts** — run the three `validate_supabase_*_registry.py --self-test` scripts and row-uniqueness checks.
3. **Operator gate** — canonical CSV mint requires inline-ratify per `akos-inline-ratification.mdc`.
4. **Promote** — copy drafts to vault `dimensions/` paths; wire validators in `validate_hlk.py` if new dimensions added.
5. **Module flip** — update `SUPABASE_MODULE_REGISTRY.csv` `repo_artifact` + `governed_status` in same commit.
6. **Hosted apply** — publication DDL and bucket creates go through `supabase/migrations/` + operator SQL gate (separate from registry mint).
7. **Verify** — `py scripts/validate_hlk.py` + `py scripts/validate_supabase_module_registry.py`.

## Outputs

- Updated registry CSVs with decision IDs in `last_review_decision_id`
- PASS from HLK validators
- Optional migration file for Realtime publication or Storage buckets

## Failure modes

| Failure | Response |
|:---|:---|
| Duplicate row ID | Fix draft before mint; validators fail on duplicate `*_row_id` |
| owner_role not in baseline | Add role line or pick existing owner |
| Hosted drift without git row | Add `drift` posture row; reconcile at SQL gate |
| Secret in registry notes | Remove — SOC invariant; paths only for Edge secrets |

## Cross-references

- Ecosystem doctrine: `SUPABASE_ECOSYSTEM_GOVERNANCE.md`
- Multi-store alignment: `docs/wip/planning/99-supabase-platform-eg5-tranche/reports/multi-store-data-plane-alignment-2026-06-13.md`
- Paired runbooks: `scripts/validate_supabase_auth_registry.py`, `validate_supabase_realtime_registry.py`, `validate_supabase_storage_registry.py`
- process_list: `hol_data_dtp_supabase_eg5_registry_001`
