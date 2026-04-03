# HLK On AKOS Madeira Roadmap

**Source plan**: `C:\Users\Shadow\.cursor\plans\hlk_madeira_proposal_3a66dc35.plan.md`
**Status**: Working copy for workspace traceability; original 6-phase HLK-on-AKOS program complete, active follow-on now tracked by the flagship Madeira program
**Canonical source**: Original roadmap source above for phases 0-5; active follow-on execution is superseded by `C:\Users\Shadow\.cursor\plans\madeira_flagship_hardening_4f22c4ab.plan.md`

---

This file mirrors the current HLK on AKOS roadmap so the workspace has a traceable in-repo copy under `docs/wip/planning/`.

The roadmap covers:

- vault-first source-of-truth strategy for HLK
- KiRBe and Supabase as structured mirror and query layer
- compliance baseline freeze and remediation
- MADEIRA as the operator-facing entrypoint
- workspace, session, and long-lived knowledge discipline
- scalability, DX, UX, verification, and release hardening
- data-entry acceleration with canonical-vault-first discipline

## Traceability Notes

- Use this copy for workspace traceability and progress context.
- Keep the Cursor plan as the canonical source unless the user explicitly promotes this document.
- Store milestone or phase reports in the sibling `reports/` directory.
- Do not treat this `docs/wip` copy as release documentation.

## Original Program View

```mermaid
flowchart LR
  phase0["P0 Proposal And Traceability"] --> phase1["P1 Vault And Compliance Baseline"]
  phase1 --> phase2["P2 Registry And HLK Services"]
  phase2 --> phase3["P3 MADEIRA Entry Surface"]
  phase3 --> phase4["P4 Workspace And Admin UX"]
  phase4 --> phase5["P5 CI/CD And Hardening"]
```

## Original Program Phases

1. Phase 0: Proposal, scope freeze, and traceability -- COMPLETE
2. Phase 1: Canonical vault and compliance baseline remediation -- COMPLETE
3. Phase 2: HLK domain service and registry projection -- COMPLETE
4. Phase 3: MADEIRA entry surface -- COMPLETE
5. Phase 4: Admin UX, workspace management, and session discipline -- COMPLETE
6. Phase 5: CI/CD, hardening, and externalization decision -- COMPLETE

## Current Execution Update

Phase 1 is no longer the active bottleneck. `reports/phase-1-report.md` is **GO** and remains the authoritative in-repo completion note for the canonical vault freeze.

The gateway-alignment remediation is no longer the active bottleneck. Its report remains the authoritative in-repo closure note for the runtime bridge/tool-registration defect.

The active execution follow-up is the Madeira Flagship Hardening program, which supersedes the earlier lookup-hardening-only track and closes the next-layer drift between:

- HLK lookup semantics (`akos/hlk.py`)
- Madeira prompt behavior and runtime tool surface
- live browser UAT answer quality
- agent-specific drift visibility (`GET /agents/{id}/capability-drift`)
- repo-wide prompt/runtime parity for similar agent defects
- Langfuse traceability, env-source normalization, and answer-quality telemetry
- finance-lane UX hardening if the same defect pattern appears there
- the next baseline/compliance tranche boundary for KiRBe sync automation
- release-facing documentation and planning/report traceability

Reference artifacts:

- `C:\Users\Shadow\.cursor\plans\madeira_ultimate_agent_e97ddcd9.plan.md`
- `C:\Users\Shadow\.cursor\plans\madeira_lookup_hardening_a13d1a4e.plan.md`
- `C:\Users\Shadow\.cursor\plans\madeira_flagship_hardening_4f22c4ab.plan.md`
- `reports/madeira-runtime-ux-report.md`
- `reports/madeira-gateway-alignment-remediation-report.md`
- `reports/madeira-lookup-hardening-report.md`
- `reports/madeira-flagship-hardening-report.md`
- `reports/next-baseline-kirbe-sync-boundary-proposal.md`

## Active Residual Backlog

The flagship follow-on is currently responsible for closing these residuals before merge/clean-slate reset:

- live escalation UX drift on restructuring/admin prompts
- startup / post-compaction audit friction in long-lived sessions
- Langfuse no-trace operability gap and env-source redesign
- repo-wide prompt/runtime parity gaps adjacent to Madeira
- roadmap / matrix / planning-traceability contradictions
- next baseline/compliance tranche boundary definition for KiRBe automation

Current report status:

- `reports/madeira-flagship-hardening-report.md` is the authoritative in-repo closure note for this superseding follow-on and records a **GO WITH RESIDUAL** verdict.
- `reports/next-baseline-kirbe-sync-boundary-proposal.md` is the handoff artifact for the next baseline/compliance tranche.

## Phase 1 Historical Focus

Phase 1 was the original bottleneck and remains the most important historical baseline for long-term scalability, but it is no longer the active execution bottleneck.

Desired outcome:

- the HLK directory becomes the canonical authored source of truth
- KiRBe becomes the structured mirror, not the primary authoring system
- compliance taxonomy is frozen and documented
- baseline organisation and process structures are normalized enough for downstream ingestion

## Imported Context

Related systems and references reinforce the roadmap direction:

- `obsidian-reader-main` shows reusable MADEIRA patterns:
  - central persona plus capability contract
  - tool-first orchestration
  - separate routing, ingestion, and storage concerns
  - domain-specific system-message packs
- the same codebase also shows anti-patterns to avoid:
  - monolithic service files
  - duplicated prompt sources
  - brittle router logic
- embedded KiRBe, frontend, and ERP references inside `docs/references/hlk/` reinforce:
  - HATEOAS and typed integration surfaces
  - Supabase RLS and server-only secret handling
  - explicit admin workflows and data-entry UX
  - markdown-first authoring with structured downstream mirrors

## Phase 1 Historical Gap Report

### Gap Summary

- Historical note: the items below were the pre-remediation gap conditions that drove Phase 1 and should now be read alongside `reports/phase-1-report.md`, not as the current active backlog.

- `baseline_organisation` is semantically incomplete:
  - the reviewed SQL dump shows **41** rows still using the placeholder `Role description to be defined based on best practices from our internal research.`
  - the CSV mirror only represents the short baseline columns and not the richer fields already present in the typed KiRBe schema
- `public.rules` exists but is currently empty
- governance-sensitive roles need explicit access review rather than silent acceptance
- the process baseline includes:
  - **4** rows with `TBD` entity and area values
  - **72** rows using inconsistent `Process` or `Task` casing instead of the SOP's lowercase canonical granularity
- relationship stability is still fragile because several links depend on `role_name` rather than stable IDs
- structured SOP ingestion exists, but the markdown-to-DB pipeline is not yet documented as an operational contract

### Source References

- `C:\Users\Shadow\full_dump.sql`
- [baseline_organisation_rows (4).csv](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/Holistika%20Research%20v2.7/Admin/CBO/O5-1/CPO/Compliance/Organisation/baseline_organisation_rows%20(4).csv)
- [process_list_1 - process_list_1.csv](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/Holistika%20Research%20v2.7/Admin/CBO/Envoy%20Tech%20Lab/Tech%20Lab%20ShowCases/KiRBe%20-%20One%20Storage%20For%20All%20UIs/kirbe_docs/documentation-hlk/process_list_1%20-%20process_list_1.csv)
- [SOP-META_PROCESS_MGMT_001.md](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md)
- [supabase (9).ts](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/Holistika%20Research%20v2.7/Admin/CBO/Envoy%20Tech%20Lab/Tech%20Lab%20ShowCases/KiRBe%20-%20One%20Storage%20For%20All%20UIs/kirbe_docs/kirbe_sops/supabase%20(9).ts)

## Phase 1 Execution Checklist

1. `P1.CANON.1` Define canonical precedence between markdown, CSV, KiRBe, and SQL dumps.
2. `P1.COMP.1` Freeze access level, confidence level, source category, and source level semantics.
3. `P1.ORG.1` Reconcile baseline organisation authoring shape with `role_full_description`, `responsible_processes`, and `components_used`.
4. `P1.ORG.2` Review governance-sensitive role access semantics.
5. `P1.ORG.3` Fill placeholder role descriptions from the research corpus.
6. `P1.PROC.1` Normalize process hierarchy, granularity casing, and TBD handling.
7. `P1.PROC.2` Define stable machine IDs vs display-name policy.
8. `P1.SOP.1` Define markdown-to-structured-SOP ingestion contract.
9. `P1.SYNC.1` Define deterministic vault-to-KiRBe and Drive sync contract.

## Phase 1 Ordered Dependency Plan

1. `P1.DEP.1` Canonical precedence and asset classification
2. `P1.DEP.2` Compliance baseline freeze
3. `P1.DEP.3` Baseline organisation contract reconciliation
4. `P1.DEP.4` Governance-sensitive role review
5. `P1.DEP.5` Process canon normalization
6. `P1.DEP.6` Stable key and cross-file linking policy
7. `P1.DEP.7` Markdown-to-structured-SOP pipeline contract
8. `P1.DEP.8` Vault-to-KiRBe sync contract
9. `P1.DEP.9` Data-entry acceleration batches

### Why this order

- The first three steps freeze meaning and ownership.
- The next three steps normalize structure and relationships.
- The last three steps make sync and fast data entry safe.

Recommended first data-entry batches after the minimum freeze:

- governance and executive roles
- compliance and people operations
- finance and PMO
- data and tech
- broader process coverage after key role and taxonomy stability

## File-Level Targets For Phase 1

- [baseline_organisation_rows.txt](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/compliance/baseline_organisation_rows.txt)
- [baseline_organisation_rows (4).csv](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/Holistika%20Research%20v2.7/Admin/CBO/O5-1/CPO/Compliance/Organisation/baseline_organisation_rows%20(4).csv)
- [process_list_1.csv](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/compliance/process_list_1.csv)
- [process_list_1 - process_list_1.csv](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/Holistika%20Research%20v2.7/Admin/CBO/Envoy%20Tech%20Lab/Tech%20Lab%20ShowCases/KiRBe%20-%20One%20Storage%20For%20All%20UIs/kirbe_docs/documentation-hlk/process_list_1%20-%20process_list_1.csv)
- [SOP-META_PROCESS_MGMT_001.md](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/compliance/SOP-META_PROCESS_MGMT_001.md)
- [supabase (9).ts](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/Holistika%20Research%20v2.7/Admin/CBO/Envoy%20Tech%20Lab/Tech%20Lab%20ShowCases/KiRBe%20-%20One%20Storage%20For%20All%20UIs/kirbe_docs/kirbe_sops/supabase%20(9).ts)
- `C:\Users\Shadow\full_dump.sql`
- [docs/references/hlk/Research & Logic/](C:/Users/Shadow/cd_shadow/openclaw-akos/docs/references/hlk/Research%20&%20Logic/)

## Related Planning Artifacts

- [baseline-remediation-matrix.md](baseline-remediation-matrix.md) -- gap inventory, data-entry queue, vault target structure
- [reports/phase-0-report.md](reports/phase-0-report.md) -- planning phase completion (GO)
- [reports/phase-1-report.md](reports/phase-1-report.md) -- phase completion report (**GO**)
- [reports/madeira-runtime-ux-report.md](reports/madeira-runtime-ux-report.md) -- prior Madeira runtime stabilization report
- [reports/madeira-gateway-alignment-remediation-report.md](reports/madeira-gateway-alignment-remediation-report.md) -- gateway/prompt/runtime/doc remediation report

## Execution Convention

- One commit per phase
- Use the governed verification matrix after behavioral changes
- Create or update a report in `reports/` when a phase starts, completes, or is blocked
- Keep the canonical Cursor plan and this workspace mirror synchronized when the roadmap materially changes
