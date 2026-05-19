---
intellectual_kind: scope_overlap_per_deliverable_triage
parent_initiative: INIT-OPENCLAW_AKOS-76
tracked_initiative: INIT-OPENCLAW_AKOS-17
sharing_label: internal_only
authored: 2026-05-19
last_review: 2026-05-19
inception_decision_id: D-IH-76-B
linked_decisions:
  - D-IH-76-A   # I76 charter inception
  - D-IH-86-O   # Option 5 default posture
  - D-IH-76-B  # this triage's ratification (D-IH-76-B per DECISION_ID_STANDARD_RE)
linked_canonicals:
  - docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md
authoritative_anchor: docs/wip/planning/17-madeira-cursor-mode-parity/master-roadmap.md
ratifies_tracker_gate: §3.1 (I17 consolidation gate at I76 P1 entry)
chosen_framing: E (per-deliverable triage; novel framing ratified 2026-05-19)
language: en
status: ratified
ratified_at: 2026-05-19
ratified_by: Founder (Wave H entry inline-streaming W3-C; skip = recommended-default lock per inline-ratify-craft skill)
role_owner: System Owner
co_owner_role: Founder
---

# I17 — Per-deliverable triage (Wave H entry; chosen framing E)

> Ratifies scope-overlap-tracker [`§3.1 I17 consolidation gate`](../../_trackers/i11-i13-i17-scope-overlap-tracker.md) per the Wave H entry inline-ratify gate (2026-05-19). The operator chose **Option E (novel framing — per-deliverable triage)** over A/B/C/D — rejecting the binary "all of I17 in one consolidation" framing in favor of per-deliverable classification. This document inventories I17's Phase 0..4 deliverables individually, classifies each as **substrate-worthy** (merge into I76 P1 input) / **obsolete** (decommission) / **own-initiative-worthy** (forward-charter to I76b or successor), and proposes the resulting handling per deliverable.

## 1. Why per-deliverable triage

The default tracker framing (Option B "merge all") and the binary alternatives (A decommission / C parallel / D forward-charter) all treat I17 as a single consolidation atom. Empirically the I17 deliverables span multiple distinct work-classes:

- **Mode-taxonomy + schema substrate** (Phase 0 + part of Phase 1) — directly informs what [I76 P1](../master-roadmap.md#p1--mode-parity-baseline-1-2-days) produces.
- **Control-plane wiring + SOUL redeploy** (Phase 1) — implementation detail that I76 P1 will need but in a different shape (5-mode taxonomy vs I17's 3-mode taxonomy).
- **CICD reliability** (Phase 2) — orthogonal observability concern.
- **Swarm overlay docs** (Phase 3) — superseded by I76 P3 personality SOPs + I76 P4 AICs dispatcher.
- **Eval/UAT infrastructure** (Phase 4) — substrate-worthy for validating I76 P1 mode-parity behavior.

Treating all 5 phases under one consolidation decision would either lose substrate-worthy work (if we pick A/decommission) or carry forward obsolete swarm overlay docs (if we pick B/merge). Per-deliverable triage preserves what's valuable + discards what's superseded + forward-charters what doesn't belong.

## 2. Per-deliverable triage table

| I17 deliverable | Phase | What it contains | Classification | Handling at I76 P1 |
|:---|:---:|:---|:---:|:---|
| Contracts + schemas + coverage matrix + context economics | 0 | Mode-shape contracts; handoff JSON schemas; UC coverage matrix; context-window budgeting policy | **substrate-worthy** | Merge into I76 P1 [`MADEIRA_MODE_PARITY.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/MADEIRA_MODE_PARITY.md) (forward path) as substrate input; cite I17 Phase 0 contracts explicitly. |
| `madeiraInteractionMode` API + `/madeira/control` UI | 1 | Control-plane API for mode switching; operator UI for mode selection; SOUL prompt overlay redeploy | **substrate-worthy (API shape)** ; **decommission (3-mode UI; superseded)** | Carry forward the API shape (5 modes instead of 3); decommission the 3-mode `/madeira/control` UI in favor of the 5-mode equivalent that I76 P1 implies (UI rebuild is implementation detail downstream of MADEIRA_MODE_PARITY.md ratification). |
| SOUL redeploy with mode-specific prompts | 1 | Prompt variants per mode; mode-specific affordances at SOUL boot | **substrate-worthy (pattern)** | Carry forward the per-mode-prompt pattern; I76 P1 SOPs supersede the 3-mode prompt set with 5-mode equivalents. |
| pytest mode contracts + log-watcher fields | 2 | Test suite for mode-parity contracts; observability fields in Langfuse traces | **own-initiative-worthy / orthogonal** | Forward-charter to [I68 P3 Visual regression + observability rollout](../../68-cicd-discipline-and-observability-maturity/master-roadmap.md) successor — this is a CICD/observability concern, not a MADEIRA mode-shape concern. I17's pytest + log-watcher fields land as input to I68 P3's MADEIRA observability lane (or its successor if I68 P3 doesn't activate in cluster window). |
| Orchestrator/Architect/Executor swarm overlays + docs | 3 | Multi-agent swarm role overlays for MADEIRA's Orchestrator/Architect/Executor split; swarm hand-off docs | **obsolete (superseded by I76 P3 + P4)** | Decommission. I76 P3 [`SOP-TECH_MADEIRA_PERSONALITY_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/SOP-TECH_MADEIRA_PERSONALITY_001.md) (forward path) covers the personality aspect; I76 P4 MADEIRA_AIC_PER_TASK_REGISTRY.csv covers the per-task dispatcher aspect. Swarm split is no longer the canonical MADEIRA shape. |
| UC-ID catalog SSOT + `madeira-operator-coverage` eval rubric | 4 | Use-case catalog as eval substrate; coverage rubric suite | **substrate-worthy** | Carry forward as I76 P1 verification substrate. The `validate_madeira_mode_parity.py` validator stub (P1 §Verification) consumes UC-ID catalog directly. |
| Scenario 0 HTTP extensions + jsonschema handoff validation | 4 | Browser-smoke Scenario 0 extensions; jsonschema validation of handoff JSON | **substrate-worthy** | Carry forward. I76 P1 mode-parity validation in CI can extend Scenario 0 with mode-switch coverage. |
| Trajectory JSONL fixtures + optional `executor_harness` pytest oracle | 4 | LLM-trajectory fixtures for eval; optional pytest oracle for executor behavior | **substrate-worthy (fixtures)** ; **forward-charter (executor_harness)** | Carry fixtures forward; forward-charter `executor_harness` to I78 (Brand-voice LLM-as-judge) sibling since the oracle pattern is more aligned with LLM-judge eval than with MADEIRA mode-parity. |
| Tier 3 UAT doc | 4 | Strict release-lane UAT prose | **substrate-worthy** | Carry forward; I76 P5 5-engagement UAT can adopt the Tier 3 UAT shape. |

## 3. Net classification rollup

- **Substrate-worthy (merge into I76 P1 input)**: 6 deliverables — contracts/schemas/coverage/context; API shape; per-mode-prompt pattern; UC-ID catalog + rubric; Scenario 0 extensions; trajectory fixtures + Tier 3 UAT doc.
- **Obsolete (decommission)**: 2 deliverables — 3-mode `/madeira/control` UI; swarm overlay docs.
- **Forward-charter to successor**: 2 deliverables — pytest + log-watcher (to I68 P3); `executor_harness` (to I78).
- **No I76b mint required** — I17's content distributes cleanly into I76 P1 + I68 + I78 + decommission without leaving a residue that needs its own successor initiative.

## 4. Decision rule (deferred until I76 P1 lands)

Per this triage's ratification:

1. **I17 status flip**: at I76 P1 closure, I17 INITIATIVE_REGISTRY row flips from `active` → `closed` with closure decision `D-IH-17-CLOSURE` citing this triage as the substrate-handling map. The forward-chartered deliverables (pytest/log-watcher to I68; executor_harness to I78) land in those siblings' file-changes csv with cross-reference to this triage.
2. **Scope-overlap-tracker §3.1 status update**: from `open; awaits I76 P1 entry` to `ratified — per-deliverable triage (Option E) — see reports/i17-deliverable-triage-2026-05-19.md`.
3. **I76 P1 SOP authoring**: explicitly cites the substrate-worthy deliverables by name in [`MADEIRA_MODE_PARITY.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/MADEIRA_MODE_PARITY.md) §"Substrate inheritance from I17" so the merge provenance is auditable.

## 5. Cross-references

- Parent initiative: [I76 MADEIRA elevation](../master-roadmap.md)
- Tracked sibling: [I17 master-roadmap](../../17-madeira-cursor-mode-parity/master-roadmap.md)
- Scope-overlap-tracker: [I11/I13/I17](../../_trackers/i11-i13-i17-scope-overlap-tracker.md) §3.1
- Forward-charter targets: [I68 master-roadmap](../../68-cicd-discipline-and-observability-maturity/master-roadmap.md) (pytest + log-watcher), [I78 master-roadmap](../../78-brand-voice-llm-as-judge/master-roadmap.md) (executor_harness)
- Governing rules: [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc), [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc)
- Governing decisions: D-IH-76-A (charter), D-IH-86-O (Option 5 default posture), D-IH-76-B (this triage's ratification)
