---
language: en
status: active
initiative: INIT-OPENCLAW_AKOS-86
authored: 2026-05-16
last_review: 2026-05-17
role_owner: PMO
---

# I86 — Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---:|:---:|:---|
| R-IH-86-1 | PMO bandwidth collapses under ten parallel sibling contexts | med | high | D-IH-86-B event pulse + wave spotlight facilitation + blocker-overflow only when necessary |
| R-IH-86-2 | Wave spotlight handoff drops narrative between waves | med | med | One-paragraph handoff file per wave close under `reports/` |
| R-IH-86-3 | 14-day quiet floor hides a silently stalled sibling | low | high | OPS_REGISTER aging + OPERATOR_INBOX review |
| R-IH-86-4 | D-IH-86-D cross-check misses a soft dependency | med | med | Explicit §3.8 dep-map read each closure + sibling closure pause records |
| R-IH-86-5 | `_candidates/i86-*.md` redirect stub diverges from folder rename | low | low | Grep for `86-initiative-cluster` on renames |
| R-IH-86-6 | I86 planning churn blocks sibling execution | low | med | I86 commits stay planning-meta + register rows; no vault canonical mints |
| R-IH-86-7 | Notes-prefix parse rots silently (typos; non-canonical separators; unknown ids) | med | high | Validator `validate_initiative_program_anchors.py` fails CI on malformed or unknown anchors; Stage B promotes to first-class column (D-IH-86-J). **CLOSED at P3** — column-read default + FK block in `validate_initiative_registry.py` make this fail-loud |
| R-IH-86-8 | `PRJ-HOL-*` ids leak into adviser-external surfaces | low | high | BBR drift-gate token extension D-IH-86-L; P3 widened scan scope to adviser dossiers + founder-filed + adviser-handoff prose; persona-view layer enforces REDACTED rendering at I89 implementation. **MITIGATED at P3** — validator surfaces leaks at authoring time; render-time enforcement in I89 |
| R-IH-86-9 | Stage A advisory-only validator does not block bad merges | med | med | Operator may set release-gate to strict by promoting INFO row to PASS/FAIL when coverage is complete (current 24/24 active rows anchored). **CLOSED at P2** — `validate_initiative_registry.py` FK block now fail-loud against PROGRAM_REGISTRY |
| R-IH-86-10 | CSV ↔ Supabase mirror schema drift between P2 closure and operator-side migration apply (CSV has `program_anchors` column; mirror does not yet; emitted SQL would fail until apply) | med | low | Tolerable window ≤ 1 week. `compliance_mirror_emit` continues to produce valid SQL; ON CONFLICT UPDATE clauses fail-fast at apply-time (no silent drift). Mitigation: P2 pause record §3 item 5 + P3 closure pause record §4 item 2 make the operator-side apply sequence explicit |
| R-IH-86-11 | I89 candidate forward-charter rots in `_candidates/` without a clear promotion trigger | med | med | D-IH-86-N explicitly cites I89 as the implementation vehicle; planning README `_candidates/` review cadence (per `akos-planning-traceability.mdc`) surfaces stale candidates; OPS-86-4 stays open until I89 promotes (acts as a tracking pin) |
| R-IH-86-12 | OPS-86-5 (ADVOPS BBR triage) gets lost between I86 closure and ADVOPS engagement next-pass | low | med | OPS-86-5 row carries explicit owner (Brand & Narrative Manager + ADVOPS co-owner), evidence path (UAT report), and runbook (`validate_brand_baseline_reality_drift.py`). The BBR validator surfaces the same leaks every release-gate run, so the issue cannot rot silently |
