# Initiative 14 — Holistika internal GTM and marketing operations (HLK-aligned)

**Status:** active (execution started 2026-04-17).  
**Authoritative expanded spec:** Full Cursor plan + YAML todos — [`reference/internal_gtm_marketing_ops_574ae9de.plan.md`](reference/internal_gtm_marketing_ops_574ae9de.plan.md) (git); local copy may live under `%USERPROFILE%\.cursor\plans\` — re-copy to `reference/` when § Phased execution changes ([`reference/README.md`](reference/README.md)).  
**Governance:** [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md), [SOP-META_PROCESS_MGMT_001.md](../../../references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md), [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc).

## Supabase DB governance (2026-04-21) — execution alignment

**Authoritative Cursor plan (out of repo):** `%USERPROFILE%\.cursor\plans\supabase_db_governance_ssot_a48da8e6.plan.md` — do not edit from automation; git carries the **implementation** below.

| Phase (plan backlog) | Deliverable |
|:---------------------|:------------|
| 1–2 | [`supabase/migrations/`](../../../supabase/migrations/) + [`supabase/README.md`](../../../supabase/README.md); parity map in [`supabase/migrations/README.md`](../../../supabase/migrations/README.md) |
| 3 | Ledger parity: `supabase link` + `migration list`; if drift, prove SQL equivalence then **rename** git `supabase/migrations/<version>_*.sql` to remote prefixes (or `migration repair` per gate) |
| 4 | [`operator-sql-gate.md`](reports/operator-sql-gate.md) — `migration list` before `db push`, break-glass + pull/repair |
| 5 | Profile **`compliance_mirror_emit`** in [`config/verification-profiles.json`](../../../config/verification-profiles.json) |
| 6 | [`docs/ARCHITECTURE.md`](../../../ARCHITECTURE.md), [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md), [`docs/reference/DEV_VERIFICATION_REFERENCE.md`](../../../reference/DEV_VERIFICATION_REFERENCE.md), [`docs/guides/understanding_verification.md`](../../../guides/understanding_verification.md) |
| 7 | This initiative **decision-log** rows **D-GTM-DB-1…5**; Initiative 16 **D-16-7** |

## Initiative 14 — status snapshot (2026-04-18)

**Unified plan implementation (strategic narrative + Next.js attribution + Wave E scaffolding)**

- **Reference-only docs:** [`reports/strategic-gtm-narrative-reference.md`](reports/strategic-gtm-narrative-reference.md), [`reports/event-attribution-blueprint-reference.md`](reports/event-attribution-blueprint-reference.md).
- **Next.js repos:** Public marketing site — application handoff [`docs/web/holistika-research-nextjs/README.md`](../../../web/holistika-research-nextjs/README.md) (GTM/dataLayer Wave E1 + contact API snippets; not under Initiative `reports/`). Holistika ERP — [`reports/TEAM_SOTA_HLK_ERP.md`](reports/TEAM_SOTA_HLK_ERP.md).
- **Charter decisions:** [D-GTM-0-1](decision-log.md) / [D-GTM-0-2](decision-log.md) resolved — [`reports/phase-0-charter.md`](reports/phase-0-charter.md) updated.
- **Registry inventory:** Research themes in [`reports/process-list-gtm-inventory-and-next-tranches.md`](reports/process-list-gtm-inventory-and-next-tranches.md) §3a (candidates only).
- **C3 vs D1 order:** [D-GTM-C3-ORDER](decision-log.md) — **four weekly forums (C3) start after** contact UAT (D1) is credible; [`reports/wave-c-weekly-metrics-forum-log.md`](reports/wave-c-weekly-metrics-forum-log.md), [`reports/EXECUTION-BACKLOG.md`](reports/EXECUTION-BACKLOG.md).
- **Wave D1 UAT:** Mock customer **Alex Rivera** — browser contact submit **PASS** in [`reports/uat-holistika-contact-funnel-20260417.md`](reports/uat-holistika-contact-funnel-20260417.md); GTM/CRM/inbox/ERP rows **PENDING** operator; [D-GTM-D1-UAT](decision-log.md) open.
- **Phase 3 production DDL:** [D-GTM-3-1](decision-log.md) **done** — post-deploy snapshot [`reports/supabase-stripe-health-check-20260418.md`](reports/supabase-stripe-health-check-20260418.md) (mirrors populated; Stripe webhook Dashboard confirmation remains routine ops).
- **Wave E:** [`reports/EXECUTION-BACKLOG.md`](reports/EXECUTION-BACKLOG.md) — E1–E4 rows; Stripe README marketing metadata; `lib/gtm-data-layer.ts` + intake form hook (verbatim in [`docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md`](../../../web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md)).

**Single Cursor plan:** `%USERPROFILE%\.cursor\plans\initiative_14_unified.plan.md` (do not edit plan file from repo automation).

---

## Initiative 14 — status snapshot (2026-04-17)

**Completed (repo evidence — this governance repo)**

- **Initiative home:** this folder — [`master-roadmap.md`](master-roadmap.md), [`decision-log.md`](decision-log.md), [`evidence-matrix.md`](evidence-matrix.md); row in [`docs/wip/planning/README.md`](../../../wip/planning/README.md).
- **Phase 1 — CSV:** Three merged rows `holistika_gtm_dtp_001`–`003` in [`process_list.csv`](../../../references/hlk/compliance/process_list.csv); candidates in [`candidates/process_list_tranche_holistika_internal.csv`](candidates/process_list_tranche_holistika_internal.csv); merge via [`scripts/merge_process_list_tranche.py`](../../../../scripts/merge_process_list_tranche.py) + [`tests/test_merge_process_list_tranche.py`](../../../../tests/test_merge_process_list_tranche.py) (distinct from MADEIRA-oriented [`merge_gtm_into_process_list.py`](../../../../scripts/merge_gtm_into_process_list.py)).
- **Phase 2 — v3.0 SOPs:** Five files under `docs/references/hlk/v3.0/Admin/O5-1/` — Growth (`SOP-GTM_INBOUND_SLA_001`, `SOP-GTM_QUALIFICATION_001`, `SOP-GTM_BD_HANDOFF_001`), Brand/Copywriter (`SOP-GTM_AGENCY_PARTNER_WORKFLOW_001`), PMO (`SOP-GTM_WEEKLY_METRICS_REVIEW_001`), each extended with **Execution runbook** / RACI; vault links to `process_list.csv` use `.../hlk/compliance/process_list.csv` (relative depth varies by folder).
- **Phase 3 — documentation only (not prod DDL):** [`reports/sql-proposal-stack-20260417.md`](reports/sql-proposal-stack-20260417.md) — concrete DDL for `compliance.process_list_mirror`, `compliance.baseline_organisation_mirror`, `holistika_ops` stub, RLS/grants, verification queries, rollback; still **no** `apply_migration` until operator gate ([`operator-sql-gate.md`](reports/operator-sql-gate.md)).
- **Execution packaging:** [`reports/EXECUTION-BACKLOG.md`](reports/EXECUTION-BACKLOG.md) (Waves A–D); [`reports/process-list-gtm-inventory-and-next-tranches.md`](reports/process-list-gtm-inventory-and-next-tranches.md) (anchors + **candidate** task rows, not merged).
- **TEAM_SOTA:** [`reports/TEAM_SOTA_HLK_ERP.md`](reports/TEAM_SOTA_HLK_ERP.md), [`reports/TEAM_SOTA_KIRBE.md`](reports/TEAM_SOTA_KIRBE.md).
- **Docs/tests sync:** [`CHANGELOG.md`](../../../../CHANGELOG.md), [`docs/USER_GUIDE.md`](../../../../USER_GUIDE.md), [`docs/ARCHITECTURE.md`](../../../../ARCHITECTURE.md), [`docs/DEVELOPER_CHECKLIST.md`](../../../../DEVELOPER_CHECKLIST.md) as shipped on the branch.
- **Gates run for the tranche:** `py scripts/validate_hlk.py` (1069 process items), `py scripts/validate_hlk_vault_links.py`, `pytest tests/test_merge_process_list_tranche.py`.

**Insights to carry forward (governance)**

- **Split “Phase 3 docs” vs “Phase 3 execute”:** Narrative mirror DDL in the expanded plan is **superseded for exact SQL** by [`sql-proposal-stack-20260417.md`](reports/sql-proposal-stack-20260417.md); keep the plan for *why*; edit DDL only in the proposal file until approved.
- **CSV enrichment:** Prefer **task-level** children under existing `holistika_gtm_*` parents and SOP depth before new process rows; use the inventory report for **candidate** tranches—operator approval before merge.
- **Phase 4 UAT:** Stub exists ([`uat-holistika-contact-funnel-20260417.md`](reports/uat-holistika-contact-funnel-20260417.md)); Wave D in EXECUTION-BACKLOG references the same file (alias `uat-holistika-gtm-webchat-stub` retired).

**To execute next (continuation)**

- **Waves C–D (repo pack 2026-04-17):** [`reports/wave-c-d-roundup-20260417.md`](reports/wave-c-d-roundup-20260417.md) — C1/C2/D2 done in git; **C3** (four weekly forums) and **D1** (live UAT rows) remain operator-run. Ordered backlog: [`EXECUTION-BACKLOG.md`](reports/EXECUTION-BACKLOG.md).
- Remaining **stack** todos in the plan YAML (`kirbe-supabase-gap`, `masterdata-live-inventory`, `stripe-billing-ssot`, `deprecate-legacy-public`, `monitoring-governance`, `phase3b-integrations-mcp-later`) map to B-waves and KiRBe repo work, not to new CSV rows.

**Full plan mirror (YAML todos + § Phased execution)**

- [`reference/internal_gtm_marketing_ops_574ae9de.plan.md`](reference/internal_gtm_marketing_ops_574ae9de.plan.md) — see [`reference/README.md`](reference/README.md) for sync contract.

## Goal

Governed **internal-first** GTM + marketing ops: git **`process_list.csv` / `baseline_organisation.csv`** SSOT; v3.0 SOPs; Supabase mirrors + `holistika_ops`-style company billing (not KiRBe SaaS); Holistika ERP as operator shell; two standalone **TEAM_SOTA_*** instruction docs for `hlk-erp` and `kirbe` repos.

## Asset classification (HLK)

| Class | In scope |
|:------|:---------|
| **Canonical** | `process_list.csv`, `baseline_organisation.csv` (when tranche approved), `docs/references/hlk/v3.0/` SOPs added under this initiative |
| **Mirrored / derived** | Supabase MasterData, KiRBe — after operator-approved SQL |
| **Reference-only** | [`docs/references/hlk/business-intent/`](../../../references/hlk/business-intent/) transcripts |

## Phase dependency chain

- **Phase 0** → **Phase 1**: Gap list and tranche scope (new `item_id`s vs reuse). **Phase 0** → **Phase 4**: Crosswalk baseline for copy drift.
- **Phase 1** → **Phase 2**: Stable `item_id`s for SOP metadata. **Phase 1** → **Phase 3**: Mirror ingest. **Phase 1** → **Phase 5**: Stable graph inputs.
- **Phase 2** → **Phase 3** (soft gate): Primary v3.0 SOPs drafted before heavy stack work.
- **Phase 3** → **Phase 4** (optional): Live routing for end-to-end contact UAT; if stack lags, Phase 4 can still fix static copy.
- **Phase 3** → **Phase 5** (conditional): If Neo4j/KiRBe reads Supabase mirrors, ingest must exist; if git CSV–only, Phase 1 stability suffices.

```mermaid
flowchart TB
  P0[Phase0_charter_crosswalk]
  P1[Phase1_CSV_tranche]
  P2[Phase2_v3_SOPs]
  P3[Phase3_stack_mirrors]
  P4[Phase4_web_uat]
  P5[Phase5_KM_graph]
  P0 --> P1
  P0 --> P4
  P1 --> P2
  P1 --> P3
  P1 --> P5
  P2 --> P3
  P3 --> P4
  P3 --> P5
```

## Phase 0–5 at a glance

- **Phase 0** — Charter + website/service `item_id` crosswalk + business-intent synthesis + link to company formation; **no CSV edit**.
- **Phase 1** — Operator-approved `process_list.csv` tranche; [`scripts/merge_process_list_tranche.py`](../../../../scripts/merge_process_list_tranche.py) + [`candidates/process_list_tranche_holistika_internal.csv`](candidates/process_list_tranche_holistika_internal.csv); dry-run → `validate_hlk.py` → `--write` after approval.
- **Phase 2** — 3–5 v3.0 SOPs (CMO / Brand / Growth / PMO owners); SOP-META `item_id` metadata; procedure text only.
- **Phase 3** — CSV → Supabase mirrors, KiRBe migrations, `holistika_ops` vs `kirbe.*`, ERP links, integration catalog; operator-approved SQL only.
- **Phase 4** — Website/collateral drift fixes; dated `uat-*.md` if in scope.
- **Phase 5** — Topic–Fact–Source; Neo4j/KiRBe rebuild when canonical stable.

Full **Reassessed scope / Prerequisites / Deliverables / Verification** per phase: Cursor plan § Phased execution (initiative copy is a curated mirror).

## Decision log

See [`decision-log.md`](decision-log.md).

## Governed verification matrix

Full gate set: [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) — including `py scripts/validate_hlk.py` when compliance assets change, `py scripts/validate_hlk_vault_links.py` when `v3.0/**/*.md` links change, `py scripts/validate_hlk_km_manifests.py` if `_assets` manifests change.

## Reports

| Report | Purpose |
|--------|---------|
| [`reports/README.md`](reports/README.md) | Index |
| [`reports/phase-0-charter.md`](reports/phase-0-charter.md) | Phase 0 charter |
| [`reports/website-service-crosswalk.md`](reports/website-service-crosswalk.md) | Public claims → `item_id` |
| [`reports/business-intent-synthesis.md`](reports/business-intent-synthesis.md) | Transcript themes |
| [`reports/phase-1-tranche-report.md`](reports/phase-1-tranche-report.md) | CSV tranche dry-run / merge status |
| [`reports/sql-proposal-stack-20260417.md`](reports/sql-proposal-stack-20260417.md) | Phase 3 SQL proposal: concrete DDL/RLS/rollback (no execute until approval) |
| [`reports/EXECUTION-BACKLOG.md`](reports/EXECUTION-BACKLOG.md) | Ordered tasks (Waves A–E) with verification; Wave A3 sync = [`sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) |
| [`reports/strategic-gtm-narrative-reference.md`](reports/strategic-gtm-narrative-reference.md) | Strategic GTM narrative (reference-only) |
| [`reports/event-attribution-blueprint-reference.md`](reports/event-attribution-blueprint-reference.md) | Event + attribution blueprint (reference-only) |
| [`reports/wave-b-roundup-20260417.md`](reports/wave-b-roundup-20260417.md) | Wave B repo vs operator checklist; handoff before Waves C–D |
| [`reports/wave-c-d-roundup-20260417.md`](reports/wave-c-d-roundup-20260417.md) | Waves C–D: SLA + CRM doc + vault index vs C3/D1 operator completion |
| [`reports/process-list-gtm-inventory-and-next-tranches.md`](reports/process-list-gtm-inventory-and-next-tranches.md) | Existing GTM anchors + candidate next tranche (operator gate) |
| [`reports/kirbe-supabase-gap-summary.md`](reports/kirbe-supabase-gap-summary.md) | KiRBe gap |
| [`reports/masterdata-supabase-inventory.md`](reports/masterdata-supabase-inventory.md) | MasterData inventory |
| [`reports/operator-sql-gate.md`](reports/operator-sql-gate.md) | Pre-read + workflow |
| [`reports/stripe-billing-two-planes.md`](reports/stripe-billing-two-planes.md) | KiRBe SaaS vs Holistika company |
| [`reports/deprecate-legacy-public-proposal.md`](reports/deprecate-legacy-public-proposal.md) | Legacy tables |
| [`reports/monitoring-logs-governance.md`](reports/monitoring-logs-governance.md) | `monitoring_logs` |
| [`reports/phase3b-mcp-deferral.md`](reports/phase3b-mcp-deferral.md) | MCP later |
| [`reports/uat-holistika-contact-funnel-20260417.md`](reports/uat-holistika-contact-funnel-20260417.md) | Phase 4 UAT (mock customer E2E + operator rows) |
| [`reports/supabase-stripe-health-check-20260418.md`](reports/supabase-stripe-health-check-20260418.md) | Post-prod DDL Supabase + Stripe snapshot |
| [`reports/phase-5-km-checklist.md`](reports/phase-5-km-checklist.md) | Phase 5 |
| [`reports/TEAM_SOTA_HLK_WEB.md`](reports/TEAM_SOTA_HLK_WEB.md) | Pointer to [`docs/web/holistika-research-nextjs/`](../../../web/holistika-research-nextjs/README.md) (public site handoff lives outside Initiative 14) |
| [`reports/TEAM_SOTA_HLK_ERP.md`](reports/TEAM_SOTA_HLK_ERP.md) | Standalone SOTA (hlk-erp) |
| [`reports/TEAM_SOTA_KIRBE.md`](reports/TEAM_SOTA_KIRBE.md) | Standalone SOTA (kirbe) |

## Related

- [Initiative 04 — company formation](../04-holistika-company-formation/) (ENISA / legal alignment)
