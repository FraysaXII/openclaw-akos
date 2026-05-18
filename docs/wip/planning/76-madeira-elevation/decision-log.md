---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: decision_log
phase: P0
initiative: INIT-OPENCLAW_AKOS-76
authored: 2026-05-18
last_review: 2026-05-18
role_owner: System Owner
co_owner_role: PMO
ssot: false
companion_to:
  - master-roadmap.md
  - risk-register.md
  - asset-classification.md
  - evidence-matrix.md
  - files-modified.csv
---

# I76 — Decision Log

> Workspace mirror of I76 charter-time and runtime decisions. Canonical row for each lands in [`DECISION_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) at the same commit; this file carries full rationale + decision_source per the I80 / I79 P0 precedent.

## Round 1 — P0 charter (2026-05-18)

### D-IH-76-A — I76 charter inception (Wave A 2026-05-18 promotion under Option D)

**Question.** Should I76 be promoted from candidate to active in this Wave A push, given the candidate-file activation criteria (a) I84 closed (DONE), (b) I11/I13/I17 scope-overlap review (operator-driven), (c) operator chooses to promote — and given the operator's prior aborted promotion at D-IH-86-F superseded by D-IH-86-G on 2026-05-17?

**Decision.** Yes — promote I76 today, under Option D from the A1 inline-ratify gate (full P0..P6 charter + minted scope-overlap-tracker for I11/I13/I17 + companion blocker-trackers for I74/I75/I83). The scope-overlap review (criterion b) is folded into a tracked artifact (`docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md`) with three per-sibling consolidation ratify gates fired at I76 P4, rather than as a single P0 gate. This preserves I11/I13/I17 visibility in INITIATIVE_REGISTRY (their rows stay active) until consolidation is ratified per-phase.

**Rationale.** (a) D-IH-84-C pre-ratified F5 (Hybrid; per-task operator picks) — the load-bearing AICs framing question is closed; charter is mostly mechanical from there. (b) D-IH-84-D pre-ratified D3 (Hybrid library + agent platform) — substrate shape inheritable. (c) Operator's A0 ratify of Option 5 default posture (novel-framing-with-blocker-trackers when conflict surfaces) makes scope-overlap-tracker the right governance shape for criterion (b), not a blocking pre-promotion gate. (d) I76 is the prerequisite asset for I74 Strand C productization per i74-brand-tooling-productization.md §1; advancing I76 today means I74 productization can ship downstream when TRIGGER-2 fires.

**Decision_source.** operator_inline_explicit_via_askquestion (Wave A1 gate, Option D — novel framing).

**Reversibility.** Medium — promotion can be reverted via a follow-on D-IH-76-* row if execution surfaces blocking conflicts; but the registry rollover is non-trivial (review-stamp dimension, dependency map, sibling INIT row notes).

**Linked decisions.** Inherits from D-IH-84-C (F5 framing) + D-IH-84-D (D3 substrate) + D-IH-86-G (active-promotion discipline corrected from D-IH-86-F). Forward-charters D-IH-76-B..H + D-IH-76-CLOSURE.

### D-IH-86-O — Default posture shift (Option 5 / novel-framing-with-blocker-trackers)

**Question.** Should the inline-ratify gate response posture default to Option 5 (novel framing — typically a governance-shape artifact like blocker-tracker / scope-overlap-tracker / coverage-gap-tracker) when the agent's evidence sweep surfaces architectural conflict between operator stated intent and existing canonical constraints?

**Decision.** Yes — Option 5 / novel-framing-with-blocker-trackers becomes the default posture going forward for any ratify gate that surfaces architectural conflict. The trigger condition is conflict between operator-stated intent (e.g., Bundle D scope) and existing canonical constraints (candidate-file activation gates, prerequisite chains, risk-register critical risks). The response is to surface the conflict via a novel-framing option that introduces a governance-shape artifact preserving operator intent visibility WITHOUT silently overriding existing constraints. The pattern is to be formalized as a Cursor rule [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) (or equivalent name) at end of this push.

**Rationale.** Operator at A0 gate verbatim: *"option E [Option 5] ... I'd like you to be on guard for other tasks that have conflict or other topics in which Option E/5 is applicable; that will be the default way to go forward because it'll make you surface other questions and that's how we will work together human and AI to make this flawless."* This compounds the architecture-challenge cycle from "operator picks one of N" to "operator picks the path that preserves visibility AND respects existing constraints." Mirrors the I80 P3 inline-ratify-craft skill Principle 6 (welcome novel framings when they unlock paths the operator had not considered).

**Decision_source.** operator_inline_explicit_via_askquestion (Wave A0 gate, Option 5).

**Reversibility.** Low — the posture shift is durable (codified via Cursor rule mint at end of this push); but the rule itself can be amended in a follow-on initiative if posture proves miscalibrated.

**Linked decisions.** Operationalised by D-IH-76-A (first application). Mirrors the precedent of I79 P3b Strand C split (D-IH-79-L) where novel-framing emerged in inline-ratify and got captured as durable cross-area pattern.

## Round 2 — Forward (deferred to phase ratify gates)

D-IH-76-B..D-IH-76-CLOSURE will mint at their respective close-out phases per the master-roadmap §"Decisions (preview)" table. This file appends each decision row at its decision-time commit.
