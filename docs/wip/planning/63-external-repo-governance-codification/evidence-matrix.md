---
language: en
status: charter
initiative: 63-external-repo-governance-codification
report_kind: evidence-matrix
last_review: 2026-05-06
---

# Evidence matrix — Initiative 63

| Phase | Evidence | Source | Result |
|:---|:---|:---|:---|
| P0 | Charter folder created with 5 governance artefacts + 1 report | This folder | PASS |
| P0 | `docs/wip/planning/README.md` lists I63 | `docs/wip/planning/README.md` | PASS |
| P0 | `EXTERNAL_REPO_CONTRACT.md` cross-references I63 | `c:/Users/Shadow/cd_shadow/root_cd/hlk-erp/EXTERNAL_REPO_CONTRACT.md` | PASS |
| P1 | Three SOPs at `status: review` with valid frontmatter | v3.0 vault paths in master-roadmap | PENDING |
| P1 | `validate_hlk.py` clean | `py scripts/validate_hlk.py` | PENDING |
| P1 | `validate_hlk_vault_links.py` clean | `py scripts/validate_hlk_vault_links.py` | PENDING |
| P2 | KM manifest stubs under `_assets/techops/` | `_assets/techops/SOP-EXTERNAL_REPO_*.manifest.md` | PENDING |
| P2 | `validate_hlk_km_manifests.py` clean | `py scripts/validate_hlk_km_manifests.py` | PENDING |
| P3 | Operator review of `reports/csv-proposal-2026-05-06.md` | (operator action) | PENDING |
| P4 | `process_list.csv` rows minted | `docs/references/hlk/compliance/process_list.csv` | PENDING |
| P4 | `REPOSITORY_REGISTRY.csv` columns added | Same | PENDING |
| P5 | SOPs promoted to `status: active` | v3.0 vault | PENDING |
| P6 | Cursor rule extended | `.cursor/rules/akos-mirror-template.mdc` | PENDING |
| P6 | `release-gate.py` final pass | `py scripts/release-gate.py` | PENDING |

UAT artefacts under `reports/uat-i63-*.md` get added when the corresponding
phase ships.
