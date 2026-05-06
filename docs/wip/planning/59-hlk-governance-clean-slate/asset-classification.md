---
language: en
status: active
initiative: 59-hlk-governance-clean-slate
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-06
---

# Initiative 59 — Asset classification

Per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). I59 ships P0 + P1 + P2 + P3 + P4 + P5 + P6 + P7 + P8 + P9 + P10 (engineering); operator-content forks into I60 candidate (process_list mints).

## Canonical (edit here first)

### New compliance dimensions (P1)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `REPOSITORY_REGISTRY.csv` (NEW) | `docs/references/hlk/compliance/REPOSITORY_REGISTRY.csv` | P1.1 — promote markdown SSOT to governed CSV; PRIMARY KEY: `repo_slug`. | New `validate_repository_registry.py` + new sync gate `validate_repository_registry_md_csv_sync.py` + `compliance_mirror_emit` row + KM manifest |
| `INITIATIVE_REGISTRY.csv` (NEW) | `docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv` | P1.2 — central registry for every initiative across repos; PRIMARY KEY: `initiative_id` (`INIT-{REPO_SLUG}-{NN}`); FKs: `repo_slug` → REPOSITORY_REGISTRY, `cycle_id` → CYCLE_REGISTER, `inception_decision_id` / `closure_decision_id` → DECISION_REGISTER, `manifests_processes` → process_list (semicolon-list FK; nullable). | New `validate_initiative_registry.py` + new sync gate `validate_initiative_registry_frontmatter_sync.py` + `compliance_mirror_emit` row + KM manifest |
| `OPS_REGISTER.csv` (NEW) | `docs/references/hlk/compliance/OPS_REGISTER.csv` | P1.3 — formalize OPS-XX-Y items; PRIMARY KEY: `ops_action_id`; FKs: `originating_initiative_id` / `forwarded_to_initiative_id` → INITIATIVE_REGISTRY, `gate_id` → GATE_LEDGER, `linked_decision_ids` → DECISION_REGISTER. | New `validate_ops_register.py` + `compliance_mirror_emit` row + KM manifest |
| `CYCLE_REGISTER.csv` (NEW) | `docs/references/hlk/compliance/CYCLE_REGISTER.csv` | P1.4 — coordinating cycles; PRIMARY KEY: `cycle_id` (`CYC-{NN}`); covers `coordinating_initiative_id` + `coordinated_initiative_ids` (semicolon-list). | New `validate_cycle_register.py` + `compliance_mirror_emit` row + KM manifest |
| `DECISION_REGISTER.csv` (NEW) | `docs/references/hlk/compliance/DECISION_REGISTER.csv` | P1.5 — every D-IH-XX-Y decision; PRIMARY KEY: `decision_id`; FKs: `linked_initiative_ids` → INITIATIVE_REGISTRY, `linked_ops_action_ids` → OPS_REGISTER, `linked_policies` → POLICY_REGISTER. | New `validate_decision_register.py` + new sync gate `validate_decision_register_decision_log_md_sync.py` + `compliance_mirror_emit` row + KM manifest |

### New SOPs (P1.6)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `SOP-INITIATIVE_GOVERNANCE_001.md` (NEW; `status: review`) | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.md` | P1.6 — initiative lifecycle reference (bootstrap / status / closure / archive); 7-value taxonomy explained; FK dictionary; pivot to G-59-D activation | KM manifest at `docs/references/hlk/v3.0/_assets/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_GOVERNANCE_001.manifest.md` |
| `SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` (NEW; `status: review`) | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.md` | P1.6 — process_list integration recipe; tranche rules; mint authority chain; G-60-A through G-60-F gate definitions | KM manifest at `docs/references/hlk/v3.0/_assets/Admin/O5-1/Operations/PMO/SOP-INITIATIVE_PROCESS_HARMONISATION_001.manifest.md` |

### New scripts (P1 + P2 + P4 + P5 + P7)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `validate_repository_registry.py` (NEW) | `scripts/validate_repository_registry.py` | P1.1 — Pydantic + FK + uniqueness validator | Test in `tests/test_validate_repository_registry.py` |
| `validate_repository_registry_md_csv_sync.py` (NEW) | `scripts/validate_repository_registry_md_csv_sync.py` | P1.1 — sync gate (markdown↔CSV row count + columns) | Test in `tests/test_validate_repository_registry_md_csv_sync.py` |
| `validate_initiative_registry.py` (NEW) | `scripts/validate_initiative_registry.py` | P1.2 — Pydantic + FK + uniqueness validator | Test in `tests/test_validate_initiative_registry.py` |
| `validate_initiative_registry_frontmatter_sync.py` (NEW) | `scripts/validate_initiative_registry_frontmatter_sync.py` | P1.2 + P2 — frontmatter↔CSV sync gate | Test in `tests/test_validate_initiative_registry_frontmatter_sync.py` |
| `validate_ops_register.py` (NEW) | `scripts/validate_ops_register.py` | P1.3 — Pydantic + FK validator | Test in `tests/test_validate_ops_register.py` |
| `validate_cycle_register.py` (NEW) | `scripts/validate_cycle_register.py` | P1.4 — Pydantic + FK + uniqueness validator | Test in `tests/test_validate_cycle_register.py` |
| `validate_decision_register.py` (NEW) | `scripts/validate_decision_register.py` | P1.5 — Pydantic + FK validator | Test in `tests/test_validate_decision_register.py` |
| `validate_decision_register_decision_log_md_sync.py` (NEW) | `scripts/validate_decision_register_decision_log_md_sync.py` | P1.5 — decision-log.md↔CSV sync (advisory; warns if MD has decisions not in CSV) | Test in `tests/test_validate_decision_register_decision_log_md_sync.py` |
| `validate_hlk.py` (MODIFIED) | `scripts/validate_hlk.py` | P1.7 — register all 5 new validators + 3 sync gates in dispatch | Existing `tests/test_validate_hlk.py` |
| `sync_compliance_mirrors_from_csv.py` (MODIFIED) | `scripts/sync_compliance_mirrors_from_csv.py` | P1.7 — emit helpers for the 5 new mirrors | New tests in `tests/test_sync_compliance_mirrors_from_csv_new_dims.py` |
| `akos/hlk_repository_registry_csv.py` (NEW) | `akos/hlk_repository_registry_csv.py` | P1.1 — Pydantic schema | Imported by validator |
| `akos/hlk_initiative_registry_csv.py` (NEW) | `akos/hlk_initiative_registry_csv.py` | P1.2 — Pydantic schema | Imported by validator |
| `akos/hlk_ops_register_csv.py` (NEW) | `akos/hlk_ops_register_csv.py` | P1.3 — Pydantic schema | Imported by validator |
| `akos/hlk_cycle_register_csv.py` (NEW) | `akos/hlk_cycle_register_csv.py` | P1.4 — Pydantic schema | Imported by validator |
| `akos/hlk_decision_register_csv.py` (NEW) | `akos/hlk_decision_register_csv.py` | P1.5 — Pydantic schema | Imported by validator |
| `akos/planning/__init__.py` (NEW) | `akos/planning/__init__.py` | P2 — package init | None |
| `akos/planning/status_taxonomy.py` (NEW) | `akos/planning/status_taxonomy.py` | P2 — `InitiativeStatus` enum + companion-field rules; SSOT for both frontmatter validator + INITIATIVE_REGISTRY schema | New tests in `tests/test_planning_status_taxonomy.py` |
| `scripts/render_wip_dashboard.py` (MODIFIED) | `scripts/render_wip_dashboard.py` | P2 — section split (Active / Gated-external / Gated-operator / Continuous / Program-line / Closed / Archived) | Existing `tests/test_render_wip_dashboard.py` extended |
| `scripts/render_operator_inbox.py` (NEW) | `scripts/render_operator_inbox.py` | P4 — render `OPERATOR_INBOX.md` from OPS_REGISTER.csv where status=open AND owner_class IN (operator, mixed) | New tests in `tests/test_render_operator_inbox.py` |
| `scripts/check_active_initiative_freshness.py` (NEW) | `scripts/check_active_initiative_freshness.py` | P5 — read INITIATIVE_REGISTRY.csv; flag rows with `status='active' AND now() - last_review > 14 days` | New tests in `tests/test_check_active_initiative_freshness.py` |
| `akos/eval_harness/judge.py` (MODIFIED) | `akos/eval_harness/judge.py` | P6 — `_heuristic_persona_fit` resolves persona context from `scenario.persona_id` | New tests in `tests/test_judge_persona_fit_offline.py` |
| `scripts/judge_calibration_burn.py` (MODIFIED) | `scripts/judge_calibration_burn.py` | P6 — wire persona resolution into score() call | Re-run A.1+A.2 burns from I58 |
| `scripts/promote_telemetry_to_scenario.py` (RUN) | `scripts/promote_telemetry_to_scenario.py` | P7 — execute (no script changes); produce proposals + triage report | Existing tests |
| `scripts/release-gate.py` (MODIFIED) | `scripts/release-gate.py` | P4 + P5 — informational hooks for inbox + freshness canary | Existing tests + new informational footer tests |

### Modified canonical (P3 audit + status flips + closure UATs)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| ~50 master-roadmap.md frontmatter | `docs/wip/planning/<NN>-<slug>/master-roadmap.md` | P3 — apply 7-value taxonomy + companion fields | New `validate_master_roadmap_status.py` (or extension to existing frontmatter validator) |
| `docs/wip/planning/02-llamaindex-judge-mvp/master-roadmap.md` | (same) | P3.7 — flip to `status: closed` with `closed_at: 2026-05-06` | New closure UAT `reports/uat-i59-close-i02-2026-05-06.md` |
| `docs/wip/planning/07-multi-judge-and-cost-discipline/master-roadmap.md` | (same) | P3.7 — flip to `status: closed` with `closed_at: 2026-05-06`; cite I52 + I57 closures as evidence | New closure UAT `reports/uat-i59-close-i07-2026-05-06.md` |
| `docs/wip/planning/15-deck-shadow-storytelling/master-roadmap.md` | (same) | P3.7 — flip to `status: closed` with `closed_at: 2026-05-06`; cite I54 closure as evidence | New closure UAT `reports/uat-i59-close-i15-2026-05-06.md` |
| `docs/wip/planning/09-runpod-vllm-bringup/master-roadmap.md` | (same) | P3.8 — flip to `status: archived` with `archived_at: 2026-05-06` + `superseded_by: I10` | Cite I10 master-roadmap as supersession evidence |
| `docs/wip/planning/22a-i22-post-closure-followups/master-roadmap.md` | (same) | P3.10 — flip F-22a-EMIT-1 + F-22a-EMIT-2 status from `Open` to `Done` (already implemented in I22a P5/P7 commits) | `wip_dashboard_render_smoke` |
| `docs/wip/planning/55-supabase-mirror-parity/master-roadmap.md` | (same) | P3.10 — flip OPS-55-1 P1 status from `Open` to `Done` (already implemented in I58 D.x commits) | `wip_dashboard_render_smoke` |
| `docs/wip/planning/<various>/master-roadmap.md` | (same) | P3.6 — re-status long-running initiatives per the new taxonomy: I04/I06/I08/I12/I14/I17/I22/I24/I26/I33/I34/I40/I44/I47/I56 | Per-initiative `last_review: 2026-05-06` |

### New canonical reports (P0 + P1 through P10)

| Asset | Path |
|:------|:-----|
| `reports/p0-bootstrap-2026-05-06.md` | This commit |
| `reports/p1-hlk-dimensions-2026-05-06.md` | P1 |
| `reports/p2-status-taxonomy-2026-05-06.md` | P2 |
| `reports/p3-status-audit-2026-05-06.md` + 5 seed reports | P3 |
| `reports/uat-i59-close-i02-2026-05-06.md` | P3.7 |
| `reports/uat-i59-close-i07-2026-05-06.md` | P3.7 |
| `reports/uat-i59-close-i15-2026-05-06.md` | P3.7 |
| `reports/p4-operator-inbox-2026-05-06.md` | P4 |
| `reports/p5-freshness-canary-2026-05-06.md` | P5 |
| `reports/p6-ops-58-3-rubric-fix-2026-05-06.md` | P6 |
| `reports/p7-telemetry-triage-2026-05-06.md` | P7 |
| `reports/p8-process-list-harmonisation-proposal-2026-05-06.md` | P8 |
| `reports/p9-doc-pass-2026-05-06.md` | P9 |
| `reports/uat-i59-clean-slate-2026-05-06.md` | P10 |

### Modified docs (P9)

| Asset | Path | Touch point |
|:------|:-----|:------------|
| `docs/USER_GUIDE.md` | (same) | P9 — taxonomy + governance + decision-register + process harmonisation subsections |
| `docs/ARCHITECTURE.md` | (same) | P9 — state-model subsection |
| `docs/wip/planning/README.md` | (same) | P0 — row 59 + I60/I61 candidate placeholders; P9 — top blurb update |
| `CHANGELOG.md` | (same) | P0 — bootstrap entry; P9 — full I59 closure entry |
| `docs/SOP.md` | (same) | P9 — pointer to OPERATOR_INBOX.md |
| `docs/references/hlk/compliance/PRECEDENCE.md` | (same) | P1 — 5 new canonical rows + 2 new SOP rows |

### Modified canonical (Operator Inbox SSOT)

| Asset | Path | Touch point |
|:------|:-----|:------------|
| `docs/wip/planning/OPERATOR_INBOX.md` (NEW) | (same) | P4 — auto-rendered from OPS_REGISTER.csv |
| `docs/wip/planning/WIP_DASHBOARD.md` | (same) | P2 + P3 — section split (7 sections matching taxonomy enum) + status flips picked up |

## Mirrored / derived (Supabase)

| Asset | Path | Touch point |
|:------|:-----|:------------|
| `compliance.repository_registry_mirror` | Supabase migration `supabase/migrations/<NN>_repository_registry_mirror.sql` | P1.1 — DDL + RLS |
| `compliance.initiative_registry_mirror` | Supabase migration | P1.2 |
| `compliance.ops_register_mirror` | Supabase migration | P1.3 |
| `compliance.cycle_register_mirror` | Supabase migration | P1.4 |
| `compliance.decision_register_mirror` | Supabase migration | P1.5 |

Mirror DML uses `compliance_mirror_emit`; **no megabyte migration files**. Per `.cursor/rules/akos-holistika-operations.mdc` "Two-plane model".

## Reference-only (do not edit; cite when relevant)

| Asset | Path |
|:------|:-----|
| `docs/references/hlk/compliance/PRECEDENCE.md` (existing) | Read for canonical-vs-mirrored-vs-reference classification |
| `.cursor/rules/akos-mirror-template.mdc` (existing) | Read for cross-repo precedence + brand-jargon audit |
| `.cursor/rules/akos-governance-remediation.mdc` (existing) | Read for canonical CSV gates + commit and phase discipline |
| `.cursor/rules/akos-planning-traceability.mdc` (existing) | Read for UAT vs automated smoke discipline |
| `docs/wip/planning/58-cycle-2-multi-track-forward/` (closed predecessor) | Read for cycle-2 pattern; D-IH-58-A through K decisions |
| `docs/references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md` | Read for CSV-before-SOP order |

## Out of scope (deliberately deferred)

- Authoring `process_list.csv` row mints (operator-content; I60 candidate per D-IH-59-F).
- Authoring missing decision-log entries from old commit messages (best-effort only; CSV append is idempotent later).
- Adding new HLK roles to `baseline_organisation.csv` (per D-IH-59-M; existing roles cover).
- Moving WIP_DASHBOARD.md / OPERATOR_INBOX.md / README.md under a `_governance/` subfolder (per D-IH-59-M; cosmetic; would invalidate cross-references).
- Replacing per-initiative `decision-log.md` with CSV-only DECISION_REGISTER (per D-IH-59-B; markdown stays canonical for prose).
- `RUNTIME_INVENTORY.csv` / `EVIDENCE_MATRIX_ROWS.csv` / `RISK_REGISTER_ROWS.csv` (forward dimension candidates; not in I59).
- `scripts/scaffold_initiative.py` (D-IH-59-L stretch goal; defers to I60+ if effort budget exceeded).
