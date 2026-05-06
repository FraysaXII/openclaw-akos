---
language: en
status: active
initiative: 59-hlk-governance-clean-slate
report_kind: risk-register
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-06
---

# Initiative 59 — Risk register

| ID | Risk | Likelihood | Severity | Mitigation | Owner |
|:---|:-----|:-----------|:---------|:-----------|:------|
| **R-59-1** | Status audit (P3) misclassifies an initiative — e.g., flips a genuinely active one to `program_line` and the operator stops noticing it | Low | Medium | Each P3 row carries per-row rationale in `reports/p3-status-audit-2026-05-06.md`. Operator approves all ~50 rows in G-59-B (one batch). Reverting a misclassification is a single CSV edit + frontmatter flip. The seven-value enum is forward-compat: ambiguous cases default to `active` not `program_line` | System Owner |
| **R-59-2** | `render_wip_dashboard.py` section split (P2) breaks existing dashboard determinism (sha256 changes between runs) | Low | Low | Existing determinism gate runs at every commit (`render_wip_dashboard.py --check-only`). Tests in `tests/test_render_wip_dashboard.py` extended to cover all 7 sections. Revert is a single function-body change | System Owner |
| **R-59-3** | `OPERATOR_INBOX.md` (P4) drifts from `OPS_REGISTER.csv` after subsequent ops-list edits | Low | Low | Determinism gate via `render_operator_inbox.py --check-only` mirrors the dashboard pattern. Tests assert sort order (RICE desc) is stable. Inbox is auto-rendered, never hand-edited (top-of-file warning + .gitattributes if needed) | System Owner |
| **R-59-4** | `INITIATIVE_REGISTRY.csv` and individual `master-roadmap.md` files drift in steady state (a future operator edits one and forgets the other) | Med | Med | New `validate_initiative_registry_frontmatter_sync.py` runs in CI release-gate; fails if status / closed_at / cycle_id mismatch. Per `.cursor/rules/akos-docs-config-sync.mdc` doc-sync triggers, every PR touching `master-roadmap.md` must update CSV in same commit | System Owner |
| **R-59-5** | FK violations between new dimensions (e.g., `INITIATIVE_REGISTRY.cycle_id` references a `CYC-XX` not in `CYCLE_REGISTER.csv`) | Low | High | Each `validate_*_registry.py` checks all FKs against the target CSV at validation time. CI fails on orphan FK. Tests cover both happy path AND orphan-FK rejection | System Owner |
| **R-59-6** | Mirror-emit (P1.7) breaks RLS on `compliance.*_mirror` tables and Supabase MasterData advisor surfaces ERROR-level findings | Low | High | Each migration includes `ALTER TABLE compliance.*_mirror ENABLE ROW LEVEL SECURITY;` + `CREATE POLICY ... TO authenticated;` per established 17-mirror pattern. Mirror tests in `tests/test_sync_compliance_mirrors_from_csv_new_dims.py` assert RLS policies present. Rollback per migration is `DROP TABLE` | System Owner |
| **R-59-7** | Mass status flip in P3 (~50 master-roadmaps in one commit) creates merge conflicts with concurrent branches | Med | Low | Per phase = one commit. P3 lands as one large but mechanical commit; concurrent branches rebase cleanly because changes are scoped to frontmatter only. If a concurrent branch is touching the same files mid-flight, rebase + force-push the I59 branch | System Owner |
| **R-59-8** | New SOPs (`SOP-INITIATIVE_GOVERNANCE_001.md` + `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md`) authored at scope creep — try to standardize too much | Med | Med | Both SOPs at `status: review` until G-59-D. Operator can ratify both, partial-ratify one, or send back for revision. SOP-META precedent (`SOP-META_PROCESS_MGMT_001.md` reviewed once, ratified at v3.0 inception) shows this approval gate is established | System Owner |
| **R-59-9** | P1 (5 HLK dimensions atomic commit) effort drift due to scope-of-five — pattern reuse less mechanical than expected | Med | Low | P1 has six independent sub-phases (P1.1 REPOSITORY / P1.2 INITIATIVE / P1.3 OPS / P1.4 CYCLE / P1.5 DECISION / P1.6 SOPs / P1.7 dispatch wiring + mirror emit). If one sub-phase blocks (e.g., DECISION FK design proves complex), the others ship independently. Closure can land with 4/5 dimensions if needed; the 5th deferral becomes I59.5 follow-on. Prefer all-or-nothing if budget allows | System Owner |
| **R-59-10** | Operator approval-gate fatigue: G-59-A/B/C/D may overwhelm operator review capacity | Med | Low | Total operator review time estimated ~2h spread (G-59-A ~30min: design + asset-classification + draft SOP TOC; G-59-B ~30min: 50 INITIATIVE_REGISTRY rows; G-59-C ~45min: 16 OPS + 4 CYCLE + 47 DECISION rows; G-59-D ~15min: 2 SOP ratifications). All seed reports come pre-ranked + cross-referenced. If operator pushback triggers re-batching, gates can fold into a single G-59-A+B+C combined review at P9 | System Owner |
| **R-59-11** | Markdown↔CSV sync drift in steady state (after I59 closes; future cycles edit one without the other) | Low | Med | Three sync validators in CI release-gate: `validate_repository_registry_md_csv_sync.py`, `validate_initiative_registry_frontmatter_sync.py`, `validate_decision_register_decision_log_md_sync.py`. Plus `.cursor/rules/akos-docs-config-sync.mdc` updated in P9 to add explicit doc-sync trigger for these pairs. Failure mode reported as warning (DECISION_REGISTER) or hard-fail (others) per their criticality | System Owner |
| **R-59-12** | I60 candidate scope creep — operator wants process_list mints in I59 instead of waiting | Low | Low | `.cursor/rules/akos-governance-remediation.mdc` is unambiguous: process_list mints require operator approval AND program-tranche grouping AND `validate_hlk.py` PASS. I59 P8 produces the proposal artifact + draft SOP at `status: review`; the actual mint cycle is I60 with its own G-60-A through G-60-F per-tranche gates. If operator wants to fast-track, propose I60 in next sitting | System Owner |
| **R-59-13** | DECISION_REGISTER seed (P3) audit incomplete — old initiatives' decision-logs only partially audited; rows missing | Low | Low | P3 audit covers active + recent-closed initiatives (~30 decisions; high-leverage). Older closed initiatives (e.g., I02 / I07 / I15) get header-only rows in P3 to satisfy FK validation; full decision audit is a forward task as needed. CSV append is idempotent later | System Owner |

## Cycle-3 specific risks

These risks are particular to I59 (the first time we run a clean-slate-cycle initiative shape) and either dissolve or stabilize after closure:

- **R-59-cycle3-A** — First initiative to mint **five dimensions atomically**. Predecessor (I58 B.4 ship of 3 dimensions in one commit) was successful but smaller. If atomic ship proves too risky (e.g., one validator failure during release-gate cascades), fall back to two-commit split (REPOSITORY+INITIATIVE first; OPS+CYCLE+DECISION second) — both can ship within P1 with same operator approval at G-59-A. Mitigation: closure UAT explicitly cites D-IH-59-A as the all-or-nothing rationale.
- **R-59-cycle3-B** — First time agent runs telemetry promotion script "in operator's stead" without explicit per-merge approval. Per `D-IH-59-J`, P7 produces proposals + triage report + OPS-59-1 row; agent does NOT auto-merge. If operator pushback materializes ("I'd rather schedule this myself"), revert P7 commit (proposals are gitignored; only commit cost is the triage report markdown). Mitigation: P7 evidence report explicitly documents the proposal-only behavior + the auto-merge-forbidden boundary.
- **R-59-cycle3-C** — First time mass-status flip applies the **new** taxonomy values to ~50 existing initiatives. Before this cycle, `status:` field was free-form. If the new validator catches existing values that don't match (e.g., `In execution` from I29 frontmatter), validator MUST migrate them automatically OR be loosened to advisory mode for one cycle. Mitigation: validator is permissive of unknown values (warns, not fails) for one cycle; P3 explicitly migrates known free-form values to enum equivalents.

## Risks that are *not* in scope (deliberately deferred)

- **R-OUT-1** — Authoring `process_list.csv` row mints. Per `.cursor/rules/akos-governance-remediation.mdc` requires operator approval per tranche; I60 candidate handles.
- **R-OUT-2** — `RUNTIME_INVENTORY.csv` / `EVIDENCE_MATRIX_ROWS.csv` / `RISK_REGISTER_ROWS.csv` as future dimensions. Forward agenda; not I59.
- **R-OUT-3** — Replacing `decision-log.md` with CSV-only DECISION_REGISTER. Per D-IH-59-B; markdown stays canonical for prose.
- **R-OUT-4** — `scripts/scaffold_initiative.py` (mint next initiative_id; create folder; seed artefacts; append CSV row). Per D-IH-59-L stretch goal; defer to I60+ if effort budget exceeded.
- **R-OUT-5** — Adding new HLK roles to `baseline_organisation.csv`. Per D-IH-59-M; existing roles cover.
- **R-OUT-6** — OPS-58-2 (OpenAI key rotation; operator 1-min paste). Operator-content; stays in OPERATOR_INBOX.
- **R-OUT-7** — OPS-58-4 (GraphRAG live wiring). Operator-funded compute window; stays in OPERATOR_INBOX.
