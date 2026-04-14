# Phase 1 plan: HLK v3.0 Envoy repository hub + entity placement

**Initiative slug:** `hlk-vault-envoy-repos`  
**Status:** In execution  
**Date:** 2026-04-09  

**Source plan (Cursor):** `.cursor/plans/hlk_vault_repo_hub_f3b5cb56.plan.md` — do not treat as canonical vault content.

---

## Asset classification (per [PRECEDENCE.md](../../../../docs/references/hlk/compliance/PRECEDENCE.md))

| Class | Paths | Rule |
|-------|--------|------|
| **Canonical** | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/`, updates to `v3.0/index.md`, optional `PRECEDENCE.md` clarification | Author here first |
| **Mirrored** | GitHub repository file trees | SSOT on GitHub; vault holds registry rows and topic `source` pointers unless submodule approved |
| **Reference-only** | `docs/references/hlk/Research & Logic/` | Promote into v3.0; do not edit in place |
| **Non-canonical planning** | This folder | Traceability only |

---

## Decision log

| ID | Question | Options | Decision |
|----|----------|---------|----------|
| D1 | Where is code SSOT? | Vault vs GitHub | GitHub remains SSOT; vault holds registry + topic links unless submodule justified |
| D2 | Entity split | Think Big vs Envoy | Envoy Tech Lab = repository hub; Think Big = non-repo commercial/delivery artifacts + cross-links |
| D3 | KM contract change? | New manifest fields vs registry only | Registry + template section only; no new Obsidian tag roots without `HLK_KM_TOPIC_FACT_SOURCE.md` revision |
| D4 | process_list.csv | Add repo onboarding now | Defer until operator-approved repeatable process exists |

---

## Verification matrix

Use the **full** repo-standard gate set from [DEVELOPER_CHECKLIST.md](../../../../DEVELOPER_CHECKLIST.md), including when shipping to a release branch:

- `py scripts/legacy/verify_openclaw_inventory.py`
- `py scripts/check-drift.py`
- `py scripts/test.py all`
- `py scripts/browser-smoke.py --playwright`
- `py -m pytest tests/test_api.py -v`
- `py scripts/release-gate.py`
- `py scripts/validate_hlk.py` — required when canonical compliance CSVs or taxonomy change; recommended after HLK doc restructure
- `py scripts/validate_hlk_km_manifests.py` — required when `v3.0/_assets/**/*.manifest.md` change

This plan does not narrow the governed matrix.

---

## Deliverables (execution checklist)

- [x] `Envoy Tech Lab/Repositories/README.md` + `REPOSITORIES_REGISTRY.md` + `platform/`, `internal/`, `client-delivery/` subfolders
- [x] `v3.0/index.md` updated (Envoy repo hub, Think Big scope)
- [x] `Think Big/README.md` + PMO pilot topic index
- [x] `TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md` — Linked Git repositories section
- [x] `PRECEDENCE.md` — GitHub vs vault + registry authority
- [x] `docs/USER_GUIDE.md` §24, `docs/ARCHITECTURE.md` HLK blurb, `CHANGELOG.md`, `README.md`

**Report:** `reports/phase-1-report.md` when this phase closes.
