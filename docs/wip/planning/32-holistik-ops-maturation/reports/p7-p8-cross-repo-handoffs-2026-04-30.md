---
language: en
status: complete
initiative: 32-holistik-ops-maturation
report_kind: phase-report
phase: P7+P8+P11-equivalents
program_id: shared
plane: ops
authority: Founder + System Owner + PMO
last_review: 2026-04-30
---

# P7 + P8 + P11 — Cross-repo extraction discipline + KiRBe deep handoff + ERP deep handoff + Boilerplate registration

**Date:** 2026-04-30
**Status:** COMPLETED. **14/14 cross-repo tests PASS** + all prior phase tests still green. 7-file ERP bundle shipped + 3 PR patches + 6 bilingual cover-emails (D-IH-32-P).

This report consolidates three v0.2 phases (cross-repo extraction P8 + KiRBe deep handoff P9 + ERP deep handoff P10 + Boilerplate registration P11) into the two existing todo IDs `p7-kirbe-handoff` and `p8-erp-handoff` per the agreed mapping.

## Cross-repo extraction substrate (v0.2 P8)

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P8-A1** | EXTERNAL_REPO_CONTRACT_TEMPLATE.md | DONE | [`docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/EXTERNAL_REPO_CONTRACT_TEMPLATE.md). Spells out 3 invariants + 5 do-not + 1 do rules + cross-references; all surfaces FK-validated. |
| **P8-A2** | akos-mirror.mdc cursor rule template | DONE | [`.cursor/rules/akos-mirror-template.mdc`](../../../../.cursor/rules/akos-mirror-template.mdc). `alwaysApply: true`; references AKOS via stable GitHub URLs (works on every developer's machine). |
| **P8-A3** | REPO_HEALTH_SNAPSHOT.csv + akos contract + validator | DONE | CSV at canonical compliance/ (10-field schema); [`akos/hlk_repo_health_csv.py`](../../../../akos/hlk_repo_health_csv.py); [`scripts/validate_repo_health_snapshot.py`](../../../../scripts/validate_repo_health_snapshot.py) with `repo_slug` FK to REPOSITORIES_REGISTRY. |
| **P8-A4** | Mirror DDL + reseed | DONE (staged) | [`supabase/migrations/20260430233400_i32_repo_health_snapshot_mirror.sql`](../../../../supabase/migrations/20260430233400_i32_repo_health_snapshot_mirror.sql); composite PK `(repo_slug, snapshot_date)` for append-only history; partial index for "missing contract" dashboard query. |
| **P8-A5** | snapshot_external_repos.py reads local clones | DONE | [`scripts/snapshot_external_repos.py`](../../../../scripts/snapshot_external_repos.py). Reads `c:\Users\Shadow\cd_shadow\root_cd\<repo>` defaults; overrideable via `AKOS_EXTERNAL_REPO_ROOTS` env JSON. First snapshot wrote 3 rows (boilerplate / hlk-erp / kirbe-platform). |
| **P8-A6** | 3 PR-ready patches | DONE | [`reports/external-repo-seed-prs/{kirbe,hlk-erp,boilerplate}.patch`](external-repo-seed-prs/). Boilerplate patch is light-touch (no `.cursor/rules/` deployment per D-IH-32-N). |
| **P8-A7** | First weekly snapshot row per repo | DONE | All 3 rows in `REPO_HEALTH_SNAPSHOT.csv` show `has_external_repo_contract=false` baseline (PR patches not yet merged on the external repos); jargon-violation baseline 6 / 23 / 56 across the 3 repos. |
| **P8-A8/A9** | REPOSITORIES_REGISTRY column + akos-docs-config-sync triggers | DONE | Registry extended with 2 new rows (`hlk-erp` + `boilerplate`) + new `reference` class definition; `kirbe-platform` row enriched with v1.2 reality from E11. |
| **P8-A10** | Tests | DONE | 14 tests in [`tests/test_repo_health_snapshot.py`](../../../../tests/test_repo_health_snapshot.py): all PASS. |

## KiRBe deep handoff (v0.2 P9)

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P9-A1** | Sync contract §2 rewrite | DONE | [`config/sync/kirbe-sync-contract.md`](../../../../config/sync/kirbe-sync-contract.md) §2 enumerates all **16 mirrors** with `sync_direction; rls_posture; consumer_role` + table for the 17th `repo_health_snapshot_mirror` (AKOS-cron-only). |
| **P9-A2** | Sync contract §11 cross-repo | DONE | New `## 11. Cross-repo contract` section codifies D-IH-32-K + the 3-invariant / 5-do-not / 1-do rule reference + the 4 things explicitly NOT changed (billing-plane, LlamaIndex, local Neo4j, existing 36 cursor rules). |
| **P9-A3** | 6-section handoff memo | DONE | [`reports/kirbe-handoff-memo-2026-04-30.md`](kirbe-handoff-memo-2026-04-30.md). Sections: 1 new dimensions, 2 contract status, 3 language frontmatter discipline, 4 billing-plane unchanged, 5 webhook idempotency fixture (citing POL-RLS-FINOPS-DENY-ANON), 6 service_role rotation cadence (citing POL-SERVICE-ROLE-ROTATION-QUARTERLY). Plus Q6 operator question for KiRBe team. |
| **P9-A4** | Architecture audit memo | DONE | [`reports/kirbe-architecture-audit-2026-04-30.md`](kirbe-architecture-audit-2026-04-30.md). Confirms v1.2 reality (E11) across 11 capability rows + recommends **5 architecture-level deltas** (persona-aware vault search; channel-tagged ingestion provenance; tenant-facing skill dashboard tile = MADEIRA-SaaS bridge; KiRBe Neo4j stays separate per D-IH-32-M; cite policy_id from POLICY_REGISTER on every kirbe.* RLS rule) + **3 things to NOT change** (billing-plane, LlamaIndex, local Neo4j). |
| **P9-A5** | KiRBe-specific PR patch refinement | DONE | `reports/external-repo-seed-prs/kirbe.patch` includes KiRBe-specific repo identity (kirbe-platform / System Owner / [../KiRBe/](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/KiRBe/) vault doc root). |
| **P9-A6** | TEAM_SOTA_KIRBE extension (deferred to next-rev) | DEFERRED | Per the audit memo, TEAM_SOTA_KIRBE will gain §11 + §12 + §13 after KiRBe team merges the PR patch. Out of I32 closure scope; will land as a follow-up edit. |
| **P9-A7** | Dated KiRBe acknowledgement | OPERATOR-PENDING | Operator forwards the bilingual cover-emails (P9-A8) and captures the team's reply. |
| **P9-A8** | Bilingual cover-email drafts | DONE | EN: [`kirbe-cover-email-en.md`](external-repo-seed-prs/kirbe-cover-email-en.md). ES: [`kirbe-cover-email-es.md`](external-repo-seed-prs/kirbe-cover-email-es.md). Both pass jargon-audit (no internal codenames in the body). |

## ERP deep handoff (v0.2 P10) + Boilerplate registration (v0.2 P11)

| ID | Action | Status | Evidence |
|:---|:-------|:-------|:---------|
| **P10-A1..A6** | 6 bundle artifacts | DONE | [`reports/erp-handoff-bundle-2026-04-30/`](erp-handoff-bundle-2026-04-30/) folder: 00-README + 01-mirror-schema-map (16 mirrors with example queries) + 02-five-axis-integration-spec (persona / channel / distance / language patterns for ERP screens) + 03-operator-sql-gate-pointer + 04-localisation-policy-pointer + 05-changelog-snippet (jargon-audit clean) + 06-team-sota-pointer. **7 files total**. |
| **P10-A7** | ERP architecture audit memo | DONE | [`reports/erp-architecture-audit-2026-04-30.md`](erp-architecture-audit-2026-04-30.md). Uses E13 (`data-ssot.mdc` drift) and E14 (stale `other_documentation/`). **6 architecture-level deltas** (adopt language frontmatter; adopt akos-mirror.mdc per Q10 supersession; replace `other_documentation/kirbe/` with pointer; replace `other_documentation/hlk/` with pointer; ERP screens read mirrors via Supabase views not lib/types.ts; adopt 5-axis integration spec). **5 things to NOT change** (Next.js patterns, theme tokens, chart wrapper, Supabase Auth, hooks/components/lib pattern). |
| **P10-A8** | ERP-specific PR patch | DONE | `reports/external-repo-seed-prs/hlk-erp.patch` includes hlk-erp-specific repo identity + cites the Q10 supersession recommendation. |
| **P10-A9** | TEAM_SOTA_HLK_ERP extension (deferred) | DEFERRED | Per the audit memo, TEAM_SOTA_HLK_ERP will gain §10 + §11 + §12 after ERP team merges the PR patch. Out of I32 closure scope. |
| **P10-A10** | Dated ERP acknowledgement | OPERATOR-PENDING | Operator forwards the bilingual cover-emails (P10-A11). |
| **P10-A11** | Bilingual cover-email drafts | DONE | EN: [`hlk-erp-cover-email-en.md`](external-repo-seed-prs/hlk-erp-cover-email-en.md). ES: [`hlk-erp-cover-email-es.md`](external-repo-seed-prs/hlk-erp-cover-email-es.md). Both pass jargon-audit. |
| **P11-A1..A6** | Boilerplate reference-only registration | DONE | New row in [`REPOSITORIES_REGISTRY.md`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) (`class=reference`, vault_doc_root=—, notes citing D-IH-32-N). New `reference` class definition documented. Light boilerplate.patch (EXTERNAL_REPO_CONTRACT.md only; no akos-mirror.mdc per D-IH-32-N). Bilingual cover-emails [`boilerplate-cover-email-{en,es}.md`](external-repo-seed-prs/) — short and to the point ("light-touch reference registration; no further action needed"). |

## Verification

- `py scripts/snapshot_external_repos.py --check-only` → reports 3 rows (boilerplate / hlk-erp / kirbe-platform); no write
- `py scripts/snapshot_external_repos.py` → wrote 3 rows to `REPO_HEALTH_SNAPSHOT.csv`
- `py scripts/validate_repo_health_snapshot.py` → PASS at 3 rows
- `py scripts/validate_topic_registry.py` → PASS at **27 rows** (added topic_repo_health_snapshot in P7)
- `py scripts/validate_hlk.py` → PASS; new lines: "REPO_HEALTH_SNAPSHOT: PASS" added to dispatch output
- `py -m pytest tests/test_repo_health_snapshot.py -v` → **14 passed in 4.07s**

## Notes

- **The cross-repo extraction discipline is real and pull-based** (D-IH-32-L). AKOS owns the cron / on-demand snapshot. External repos consume canonicals read-only via `compliance.*_mirror`. Nothing flows from external to AKOS as authoring.
- **3 PR patches + 6 cover-emails** are review-ready in `reports/external-repo-seed-prs/`. The operator forwards them; we don't auto-open PRs (per D-IH-32-P resolution).
- **Boilerplate is genuinely light-touch** (D-IH-32-N): only 1 file lands at the boilerplate repo root (no cursor rule mirror because no `.cursor/rules/` exists). The embedded Obsidian snapshot is explicitly NOT canonical; Initiative 43 (deferred) replaces it with a pointer.
- **KiRBe v1.2 reality is fully captured** (E11) and the 5 architecture deltas are **non-blocking** recommendations. None of the 5 touch the substrates that are working: billing-plane discipline, LlamaIndex pipeline, local Neo4j (D-IH-32-M).
- **HLK-ERP latent drifts are surfaced** (E13 `data-ssot.mdc` contradiction; E14 stale `other_documentation/`) and both have a Q10 supersession-style fix that respects the ERP team's ownership of their own rulepack.
- **Validator caught a real issue mid-execution**: my first snapshot CSV used local folder names (`kirbe`, `boilerplate`, `hlk-erp`) but the `repo_slug` FK validator required REPOSITORIES_REGISTRY.md slugs (`kirbe-platform` for the KiRBe row). Fixed by adding the 2 missing rows to REPOSITORIES_REGISTRY and updating the snapshot script's slug map. Real-world cross-CSV FK enforcement working end-to-end.

## Next phase

P9 (consolidated todo `p9-madeira-eval`) — Madeira eval harness wiring + 5 skill drift canaries.
