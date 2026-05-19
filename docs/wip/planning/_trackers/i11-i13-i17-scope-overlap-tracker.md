---
intellectual_kind: scope_overlap_tracker
sharing_label: internal_only
parent_initiative: INIT-OPENCLAW_AKOS-76
tracked_initiatives:
  - INIT-OPENCLAW_AKOS-11
  - INIT-OPENCLAW_AKOS-13
  - INIT-OPENCLAW_AKOS-17
authored: 2026-05-18
last_review: 2026-05-18
next_review_trigger: I76 P4 entry (AICs implementation phase)
linked_decisions:
  - D-IH-76-A
  - D-IH-86-O
  - D-IH-84-C
status: active
role_owner: System Owner
co_owner_role: Founder
language: en
---

# I11 / I13 / I17 — Scope-Overlap Tracker

> Governance-shape artifact minted at I76 P0 charter per Option D ratify (A1 inline-ratify gate 2026-05-18) and Option 5 default posture (D-IH-86-O). The tracker preserves I11/I13/I17 visibility in INITIATIVE_REGISTRY (their rows stay active) while consolidation decisions are deferred to per-phase ratify gates at I76 P4. Replaces the otherwise-blocking i76 candidate-file promotion criterion (b) "I11/I13/I17 scope-overlap review (operator-driven)" — the review now happens INSIDE I76, not as gating pre-promotion.

## 1. Why this tracker exists

I76 is the MADEIRA elevation initiative — operator-interaction quality at Cursor-grade. Today the operator's interaction with MADEIRA runs across three active initiatives:

- **I11 — MADEIRA day-to-day ops copilot** (60% completion per I86 handoff §2; PMO owner; awaits I76 elevation per its own master-roadmap).
- **I13 — MADEIRA research follow-through** (active per i76 candidate §10; consumes IntelligenceOps SOPs migrated under Research/Intelligence per `D-IH-70-W`).
- **I17 — MADEIRA Cursor mode parity (Ask / Plan / Run)** (40% completion per I86 handoff §2; lower priority; resumes when MADEIRA Mission Control I62 lands).

I76 by definition extends, supersedes, or runs parallel to all three. The candidate file conundrum C-76-5 names the question explicitly: *"does I76 supersede them, extend them, or run parallel? Default = run parallel (I76 is the elevation layer; I11/I13/I17 are the substrate)."*

A single up-front P0 ratify of "supersede / extend / parallel" for all three at once would over-commit operator attention to a decision that has phase-specific tradeoffs:

- The I17 mode-parity question is sharpest at I76 P1 (when I76 mints the 5 mode definitions; if I17's existing mode parity work is sufficient, I76 P1 is mostly a re-anchoring; if not, I17 deliverables consolidate into I76).
- The I11 ops-copilot question is sharpest at I76 P3-P4 (when I76 ships the operator UX + persistence + AICs F5 dispatcher; if I11 has working copilot deliverables, the consolidation question is "do they merge into the elevated MADEIRA or stay as legacy code-path").
- The I13 research-follow-through question is sharpest at I76 P4 (when AICs F5 dispatcher per-task picks; if F5 includes a research-follow-through task class, consolidation is natural; otherwise I13 stays parallel).

So this tracker fragments the consolidation question into three per-sibling ratify gates, each fired at the I76 phase where the question is sharpest. Each gate picks from a four-option set: **decommission** / **merge into I76** / **remain parallel as legacy code-path** / **forward-charter to I76b**.

## 2. Per-sibling scope-overlap inventory

| Sibling | Owner | Status | Scope summary | I76 phase where sharpest | Default consolidation framing |
|:---|:---|:---|:---|:---|:---|
| **I11 — MADEIRA day-to-day ops copilot** | PMO | active 60% | Daily ops support; consumed by every Cursor session that runs HLK governance work; informs methodology mode persistence shape. | **I76 P3** (operator UX + persistence) | merge-into-I76 (if P3 SOPs subsume I11's copilot deliverables) OR remain-parallel (if I11 has methodology-specific work I76 P3 doesn't cover) |
| **I13 — MADEIRA research follow-through** | PMO | active | IntelligenceOps SOP migration consumed by Research area; AICs F5 may include research-follow-through task class. | **I76 P4** (AICs F5 dispatcher) | merge-into-I76 (if F5 task-class registry includes research-follow-through) OR remain-parallel (if I13's IntelligenceOps work stays distinct from MADEIRA core) |
| **I17 — MADEIRA Cursor mode parity (Ask / Plan / Run)** | PMO | active 40% | Mode parity baseline; foundational substrate for I76's 5-mode taxonomy (Ask + Plan + Agent + Debug + Methodology). | **I76 P1** (mode parity baseline) | decommission-or-merge (I76 P1 directly supersedes I17 scope; the 5-mode taxonomy IS the elevated mode parity) OR forward-charter-to-I76b (if I17's substrate mode-parity work surfaces issues that warrant a follow-on initiative) |

## 3. Per-phase consolidation ratify gates (forward-chartered)

The tracker defers three ratify gates to specific I76 phases. Each gate is an inline-ratify call at the phase entry; the operator picks per-sibling. None are pre-promotion blockers.

### 3.1 I17 consolidation gate (fires at I76 P1 entry)

**Question.** I76 P1 mints 5 mode SOPs (Ask + Plan + Agent + Debug + Methodology). I17 P1-P3 already shipped Ask/Plan/Run mode parity baseline. Should I17:

- **A — Decommission** (close I17 with closure decision; I76 P1 deliverables fully supersede I17's work)
- **B — Merge into I76** (carry-forward I17 P1-P3 deliverables as I76 P1 input; close I17 with merge decision)
- **C — Remain parallel as legacy code-path** (I17 stays active; I76 P1 documents how I76 modes relate to I17 modes; legacy path supports operators not yet on the elevated MADEIRA)
- **D — Forward-charter to I76b** (I17 work has gaps I76 P1 doesn't cover; mint I76b-mode-parity-followup as candidate; close I17 with forward-charter decision)

**Ratify trigger.** I76 P1 entry — the agent fires this gate before authoring the 5 mode SOPs so the I17 deliverables are correctly handled.

**Default if not ratified before P1 entry.** Option B (merge); the agent carries forward I17 deliverables as P1 input and explicitly cites them in the new SOPs.

**Status.** **Ratified 2026-05-19 — Option E (per-deliverable triage; novel framing).** See [`docs/wip/planning/76-madeira-elevation/reports/i17-deliverable-triage-2026-05-19.md`](../76-madeira-elevation/reports/i17-deliverable-triage-2026-05-19.md). Triage classifies 10 I17 deliverables: 6 substrate-worthy (merge into I76 P1 input); 2 obsolete (decommission 3-mode UI + swarm overlays); 2 forward-charter (pytest+log-watcher to I68 P3; executor_harness to I78). I17 INITIATIVE_REGISTRY row flips `active` → `closed` at I76 P1 closure with `D-IH-17-CLOSURE`.

### 3.2 I11 consolidation gate (fires at I76 P3 entry)

**Question.** I76 P3 mints SOP-TECH_MADEIRA_PERSISTENCE_001 + SOP-TECH_MADEIRA_PERSONALITY_001 covering operator UX + persistence + personality. I11 has been delivering a day-to-day ops copilot in the same operator-experience space. Should I11:

- **A — Decommission**
- **B — Merge into I76** (I11 deliverables become P3 inputs)
- **C — Remain parallel as legacy code-path** (I11 covers ops-copilot use-cases I76 P3 doesn't address; both stay active)
- **D — Forward-charter to I76b**

**Ratify trigger.** I76 P3 entry.

**Default if not ratified before P3 entry.** Option C (remain parallel); the safest default given I11's ops-copilot scope may legitimately exceed I76 P3's mode-shape scope.

**Status.** **Ratified 2026-05-19 — Option E (criterion-now-defer-decision-to-evidence; novel framing).** See [`docs/wip/planning/76-madeira-elevation/reports/i11-consolidation-criterion-2026-05-19.md`](../76-madeira-elevation/reports/i11-consolidation-criterion-2026-05-19.md). Criterion: coverage = (I11 use-cases addressed by I76 P1+P3 SOPs) / (12 inventoried use-cases). Threshold 70% MERGE / 40-70 PARALLEL / < 40% FORWARD-CHARTER-TO-I76b ; tie at boundary = inline-ratify. Pre-measurement at this ratification: 67% (8 of 12) projects **PARALLEL** auto-decision when I76 P3 entry fires. Final measurement uses actual SOP §Scope coverage at P3 entry.

### 3.3 I13 consolidation gate (fires at I76 P4 entry)

**Question.** I76 P4 mints MADEIRA_AIC_PER_TASK_REGISTRY.csv + SOP-TECH_MADEIRA_AIC_DISPATCH_001. I13 has been delivering MADEIRA research follow-through (IntelligenceOps SOP migration consumed by Research area). Should I13:

- **A — Decommission**
- **B — Merge into I76** (research-follow-through becomes a task class in MADEIRA_AIC_PER_TASK_REGISTRY)
- **C — Remain parallel as legacy code-path** (I13's IntelligenceOps work is Research-area-specific; not properly a MADEIRA core question)
- **D — Forward-charter to I76b**

**Ratify trigger.** I76 P4 entry.

**Default if not ratified before P4 entry.** Option B (merge as task class); research-follow-through is a natural F5 dispatcher case.

**Status.** Open; awaits I76 P4 entry.

## 4. Tracker status update cadence

- **Per I76 phase entry**: agent fires the relevant 3.X ratify gate; tracker updates §3.X status from "open" to "ratified — option {X}" with the operator-confirmed decision.
- **At I76 closure (P6)**: tracker rolls up all 3 gate outcomes; if all 3 closed cleanly (decommission OR merge), tracker can be archived to `docs/wip/planning/_trackers/_archived/`. If any gate forward-chartered to I76b, tracker stays active and the I76b candidate stub mints with this tracker as its parent_dependency.

## 5. Cross-references

- [I76 master-roadmap](../76-madeira-elevation/master-roadmap.md) — parent initiative; see §"Phase deep sections" for P1/P3/P4 entry triggers.
- [I76 decision-log](../76-madeira-elevation/decision-log.md) — D-IH-76-A inception decision authorising this tracker.
- [I11 master-roadmap](../11-madeira-ops-copilot/master-roadmap.md), [I13 master-roadmap](../13-madeira-research-followthrough/master-roadmap.md), [I17 master-roadmap](../17-madeira-cursor-mode-parity/master-roadmap.md) — tracked siblings.
- [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) §"Default-posture shift" (D-IH-86-O codification) — pattern this tracker instantiates.
- D-IH-86-O — default posture (Option 5 / blocker-trackers) ratifying this tracker pattern as durable governance shape going forward.
