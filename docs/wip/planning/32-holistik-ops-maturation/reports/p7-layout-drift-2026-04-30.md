---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P7
program_id: shared
plane: ops
authority: System Owner + Compliance + Brand Manager
last_review: 2026-04-30
---

# P7 — Layout drift fixes (mapped to consolidated todo `p6-layout-drift`)

**Date:** 2026-04-30
**Status:** COMPLETED. Both files relocated via `git mv` (history preserved). All validators green. **10/10 alias tests PASS**. Deprecation aliases active in code for 1 cycle.

## Action items

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P7-A1** | git mv GOI_POI_REGISTER.csv → compliance/dimensions/ | DONE | `git status --short` shows `R  docs/references/hlk/compliance/GOI_POI_REGISTER.csv -> docs/references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv`. Updates: [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md) row points at new path with D-IH-32-D citation; [`compliance/README.md`](../../../references/hlk/compliance/README.md) deprecation-alias map row marked **MOVED I32 P7**; [`akos/hlk_goipoi_csv.py`](../../../../akos/hlk_goipoi_csv.py) docstring + header-keep-in-sync comment updated; [`scripts/validate_goipoi_register.py`](../../../../scripts/validate_goipoi_register.py) `GOIPOI_CSV` constant + `GOIPOI_CSV_LEGACY` alias-fallback; [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) `_GOIPOI_CSV_NEW` + `_GOIPOI_CSV_LEGACY` resolution; [`scripts/validate_hlk.py`](../../../../scripts/validate_hlk.py) dispatcher entry. |
| **P7-A2** | git mv SOP-HLK_LOCALISATION_001.md → Marketing/Brand/ | DONE | `git status --short` shows the rename. The validator script (`scripts/validate_hlk_language_frontmatter.py`) does NOT depend on the SOP path — it scans the vault directly — so no script-side alias is needed. |
| **P7-A3** | Update existing references | DONE | All canonical references updated: PRECEDENCE.md, compliance/README.md, akos contract, validator script, sync script, dispatcher. The vault link validator confirms no broken internal `.md` links after both moves. |
| **P7-A4** | Vault link validator green | DONE | `py scripts/validate_hlk_vault_links.py` → PASS (no broken internal .md links). |

## Verification

- `py scripts/validate_hlk.py` → PASS (12 programs / 1093 processes / 65 roles / 26 topics / 16 personas / 10 channels / 1 vendor / 5 skills / 15 cells / 14 policies / 150 MD files with language)
- `py scripts/validate_hlk_vault_links.py` → PASS
- `py scripts/validate_goipoi_register.py` → PASS at 6 rows, with new `GOIPOI_CSV` pointing to `dimensions/GOI_POI_REGISTER.csv`
- `py -m pytest tests/test_layout_aliases.py -v` → **10 passed in 4.26s**

## Notes

- **Deprecation aliases are forward-compatible only.** The validator and sync scripts ship with `if not NEW.is_file() and LEGACY.is_file(): use LEGACY` logic. After the relocation today, the new path exists and the legacy path is empty, so the alias is dormant. If a future operator accidentally `git revert`s the relocation, the alias kicks in and validators continue to pass — the alias is a forward-compatibility safety net, not a duplicate.
- **One-cycle policy**: aliases are removed in Initiative 33. Future external repos that hard-code the legacy path get one initiative cycle to update.
- **The 2 SOPs that actually cite GOI/POI by relative path** (`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`, `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001`) use plain text references like "the GOI/POI register" or `compliance.goipoi_register_mirror`, not file-system relative paths. The vault link validator scanned 150 files and found zero broken internal `.md` links — confirming nothing pointed at the legacy CSV path via Markdown link.
- **Localisation SOP move is cleaner than expected**: validator script lives in Tech (where the executor runs), SOP body moves to Brand (where policy ownership belongs). The validator does not load the SOP; the SOP cites the validator. Two-way cross-reference preserved by README + PRECEDENCE.md.
- **`compliance/README.md` updated** with the full enumeration of every CSV now living under `dimensions/` (10 rows: GOI/POI relocated + 6 prior + 3 new from I32 P2/P3/P4 + POC_TO_COMMERCIAL_MAP from I29). Anyone reading the README sees the full state at a glance.

## Next phase

P8 — Cross-repo extraction discipline + KiRBe deep handoff + ERP deep handoff + Boilerplate reference registration (mapped to consolidated todos `p7-kirbe-handoff` and `p8-erp-handoff`; absorbs the v0.2 P8/P11 phases).
