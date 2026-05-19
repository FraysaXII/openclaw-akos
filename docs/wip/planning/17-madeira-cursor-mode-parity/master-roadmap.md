---
language: en
status: closed
initiative_id: INIT-OPENCLAW_AKOS-17
last_review: 2026-05-19
closed_at: 2026-05-19
closure_decision_id: D-IH-17-CLOSURE
---
# Initiative 17 — MADEIRA Cursor mode parity (Ask / Plan / Run)

**Status:** **closed 2026-05-19** at I76 P1 closure per per-deliverable triage (D-IH-76-B → D-IH-17-CLOSURE). Substrate distributed: 6 deliverables merged into [I76 P1 MADEIRA_MODE_PARITY.md](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/MADEIRA_MODE_PARITY.md) §2 substrate-inheritance section; 2 forward-chartered (pytest+log-watcher to I68 P3; executor_harness to I78); 2 decommissioned (3-mode `/madeira/control` UI + swarm overlay docs). 5-mode taxonomy (Ask + Plan + Agent + Debug + Methodology) supersedes 3-mode (Ask + Plan + Run). See [I17 per-deliverable triage](../76-madeira-elevation/reports/i17-deliverable-triage-2026-05-19.md) for the substrate-handling map.  
**Authoritative Cursor plan (out-of-repo):** `C:\Users\Shadow\.cursor\plans\madeira_unified_cursor_parity_b436652c.plan.md` (do not edit from automation)  
**Optional git mirror:** [`reference/CURSOR_PLAN_POINTER.md`](reference/CURSOR_PLAN_POINTER.md) · **Eval fusion mirror:** [`reference/MADEIRA_AGENTIC_EVAL_FUSION.md`](reference/MADEIRA_AGENTIC_EVAL_FUSION.md)

## Phase dependency chain

- **Phase 0** locks taxonomy, handoff schema, context-economics policy, and wip coverage matrix so later code/docs do not drift.
- **Phase 1** threads `madeiraInteractionMode` through the AKOS control plane and operator UI (`/madeira/control`), redeploying Madeira `SOUL.md` with the correct prompt variant + Plan overlay.
- **Phase 2** extends golden / log-watcher signals for mode contracts and anti-bloat heuristics.
- **Phase 3** documents swarm consumption of structured handoffs (Orchestrator / Architect overlays); mutations remain Executor-gated.
- **Phase 4** hardens **agentic eval parity** (UC-ID catalog SSOT, `madeira-operator-coverage` rubric suite, jsonschema handoff validation, Scenario 0 HTTP extensions, trajectory JSONL fixtures, strict release lane prose, optional Executor pytest oracle).

## Phase dependency diagram

```mermaid
flowchart LR
  p0[Phase0_TaxonomySchemas]
  p1[Phase1_GatewayUI]
  p2[Phase2_EvalsTelemetry]
  p3[Phase3_SwarmHandoff]
  p4[Phase4_EvalUATHardening]
  p0 --> p1
  p1 --> p2
  p2 --> p3
  p3 --> p4
```

## Phase at a glance

| Phase | Purpose | Key deliverable |
|:-----:|---------|-----------------|
| 0 | Contracts + governance artifacts | `contracts/`, `schemas/`, coverage matrix, context economics |
| 1 | Control plane + UX | `madeiraInteractionMode` API, `/madeira/control`, SOUL redeploy |
| 2 | Reliability | pytest + log-watcher fields |
| 3 | Swarm | Orchestrator/Architect overlays + docs |
| 4 | Eval + UAT hardening | UC matrix, eval suite, jsonschema, browser-smoke Scenario 0 extensions, Tier 3 UAT doc, optional `executor_harness` |

## Asset classification

Default scope is **platform / prompts / AKOS API** (non-canonical). If any phase edits `process_list.csv`, `baseline_organisation.csv`, or net-new v3.0 SOPs for new `item_id`s, follow [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md) and operator approval gates.

## Verification matrix

Per phase close-out: `py scripts/check-drift.py`, `py scripts/test.py all` or targeted `py -m pytest`, and `py scripts/release-gate.py` when changes are release-affecting. WebChat qualitative rows require a dated `reports/uat-*.md` per [`.cursor/rules/akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc).

## Sync rule

When the Cursor plan phases change materially, update this file’s narrative and diagram to match.
