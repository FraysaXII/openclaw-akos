---
intellectual_kind: scope_overlap_deferred_decision_criterion
parent_initiative: INIT-OPENCLAW_AKOS-76
tracked_initiative: INIT-OPENCLAW_AKOS-11
sharing_label: internal_only
authored: 2026-05-19
last_review: 2026-05-19
inception_decision_id: D-IH-76-C
linked_decisions:
  - D-IH-76-A   # I76 charter inception
  - D-IH-86-O   # Option 5 default posture
  - D-IH-76-C  # this criterion's ratification (D-IH-76-C per DECISION_ID_STANDARD_RE)
linked_canonicals:
  - docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md
authoritative_anchor: docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md
ratifies_tracker_gate: §3.2 (I11 consolidation gate at I76 P3 entry)
chosen_framing: E (ratify-criterion-now-defer-decision-to-evidence; novel framing ratified 2026-05-19)
fires_at: I76 P3 entry (when SOP-TECH_MADEIRA_PERSISTENCE_001 + SOP-TECH_MADEIRA_PERSONALITY_001 are authored)
language: en
status: ratified
ratified_at: 2026-05-19
ratified_by: Founder (Wave H entry inline-streaming W3-C; skip = recommended-default lock per inline-ratify-craft skill; 70%/40% bands locked; pre-measurement 67% projects PARALLEL auto-decision at I76 P3 entry)
role_owner: System Owner
co_owner_role: Founder
---

# I11 — Consolidation deferred-decision criterion (Wave H entry; chosen framing E)

> Ratifies scope-overlap-tracker [`§3.2 I11 consolidation gate`](../../_trackers/i11-i13-i17-scope-overlap-tracker.md) per the Wave H entry inline-ratify gate (2026-05-19). The operator chose **Option E (novel framing — ratify-criterion-now-defer-decision-to-evidence)** over A/B/C/D. This document does NOT decide I11's fate today; it ratifies the CRITERION by which the fate will be determined when execution reaches I76 P3 entry. The decision then fires automatically from the criterion + I76 P1+P3 actual output.

## 1. Why ratify-criterion-now

The I11 consolidation question is genuinely undecidable today because I76 P1+P3 SOPs haven't been authored yet. We don't know whether [SOP-TECH_MADEIRA_PERSISTENCE_001](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/SOP-TECH_MADEIRA_PERSISTENCE_001.md) (forward path) + [SOP-TECH_MADEIRA_PERSONALITY_001](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/SOP-TECH_MADEIRA_PERSONALITY_001.md) (forward path) will cover most of what I11's ops-copilot does today (→ MERGE makes sense), or will leave significant I11 scope uncovered (→ PARALLEL makes sense).

Three classical resolutions and their failure modes:

- **Decide now blindly** (Option A/B/C/D) — risks shipping a wrong consolidation that's hard to reverse once I11 is closed.
- **Defer entirely to I76 P3 entry** (default Option C "remain parallel") — operator must re-ratify mid-execution; chat-flow interruption per Wave H W3-C inline-streaming norm; but better than blind upfront.
- **Ratify the CRITERION now + auto-fire at P3** (Option E novel framing) — operator engages once now to define the rule; execution auto-applies the rule at P3 entry based on actual evidence; no mid-execution re-ratify needed unless the rule itself surfaces a tie / ambiguity.

Option E is the cleanest application of the *evidence-dependent* dimension of the inline-ratify-craft skill: the operator decides ABOUT the decision space, not within it.

## 2. The criterion (proposed at Wave H entry; ratify-pending)

**Coverage measurement**:

Coverage = (number of I11 ops-copilot use-cases covered by I76 P3 SOPs + I76 P1 SOPs) / (total I11 ops-copilot use-cases inventoried at this moment).

- **Numerator**: count I11 use-cases that are explicitly addressed by either SOP-TECH_MADEIRA_PERSISTENCE_001 or SOP-TECH_MADEIRA_PERSONALITY_001 or MADEIRA_MODE_PARITY.md (I76 P1). "Explicitly addressed" = the SOP names the use-case in §Scope / §Coverage / §Use-cases or an analogous section, OR provides a runbook that operationalises the use-case end-to-end.
- **Denominator**: inventoried I11 use-cases per the I11 master-roadmap + UAT report from 2026-04-15. Inventoried at this commit; frozen for measurement at I76 P3 entry. Approximate inventory: 8-12 use-cases (drafts, checklists, clearer Orchestrator handoffs, intent-routing exemplars, semantic exemplars, regex safety, methodology-context lookups, persistence patterns, personality variants, brand-voice register checks, decision-register batch posting, IntelligenceOps handoff). Authoritative inventory will be locked in §3 below at this triage's ratification.

**Threshold**: 70% (proposed at Wave H entry; ratify-pending — operator may set higher / lower).

**Decision rule**:

| Coverage at I76 P3 entry | Auto-decision | Rationale |
|:---:|:---|:---|
| ≥ 70% | **B — MERGE I11 INTO I76** | High overlap; carry-forward I11 deliverables as P3 inputs; close I11 with merge decision. |
| 40% ≤ Coverage < 70% | **C — REMAIN PARALLEL** (tracker default) | Significant uncovered I11 scope; both stay active; clean defer to future cycle. |
| < 40% | **D — FORWARD-CHARTER TO I76b** | I11 has substantial scope I76 P1+P3 doesn't touch; mint I76b for the joint scope neither owns. |
| Tie at boundary (e.g., 69-71%) | **Inline-ratify the tiebreaker** (one AskQuestion gate at I76 P3 entry) | Boundary cases benefit from operator judgement rather than mechanical rule application. |

## 3. I11 use-case inventory (frozen at this triage's ratification)

Pulled from [I11 master-roadmap](../../11-madeira-ops-copilot/master-roadmap.md) §Goal + [I11 UAT report](../../11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md) + decision-log D-OPS-1..4:

| # | Use-case | Source | Coverage candidate (I76 SOP that might address it) |
|:---:|:---|:---|:---|
| 1 | Drafts (deck slides; cover emails; decision-row text) | I11 §Goal | MADEIRA_MODE_PARITY (Methodology mode); SOP-TECH_MADEIRA_PERSISTENCE (drafts as persistent context) |
| 2 | Checklists (pre-commit gates; pre-push gates; pre-release gates) | I11 §Goal | MADEIRA_MODE_PARITY (Methodology mode checkpoint discipline) |
| 3 | Clearer Orchestrator handoffs (multi-agent role hand-off prose) | I11 §Goal | I76 P4 MADEIRA_AIC_PER_TASK_REGISTRY (forward; not P1+P3 directly) |
| 4 | Intent routing exemplars (regex + semantic) | D-OPS-4 | MADEIRA_TOOL_CATALOG (I76 P2; not P1+P3 directly) |
| 5 | Methodology-context lookups (HLK_lookup intent) | D-OPS-4 | MADEIRA_METHODOLOGY_MODE (I76 P1) |
| 6 | Persistence patterns (when does memory persist) | D-OPS-3 | SOP-TECH_MADEIRA_PERSISTENCE (I76 P3) — direct |
| 7 | Personality variants (operator-voice mirror; neutral default) | D-OPS-1 (overlay tier) | SOP-TECH_MADEIRA_PERSONALITY (I76 P3) — direct |
| 8 | Brand-voice register checks (CORPINT internal / translated external) | I11 §Goal (implied via overlay) | SOP-TECH_MADEIRA_PERSONALITY (I76 P3) — direct via [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) |
| 9 | Decision-register batch posting (auto-generate D-IH-NN-X rows from session evidence) | I11 §Goal (implied) | MADEIRA_METHODOLOGY_MODE (I76 P1) |
| 10 | IntelligenceOps handoff (research-follow-through context) | I11 §References | I76 P4 + I13 consolidation (forward; not P1+P3 directly) |
| 11 | Permission truth + capability config | D-OPS-2 | MADEIRA_TOOL_CATALOG (I76 P2; not P1+P3 directly) |
| 12 | LOGIC_CHANGE_LOG candidate-row generation | implied via methodology framing | MADEIRA_METHODOLOGY_MODE (I76 P1) |

**Total inventory**: 12 use-cases.

**Pre-measurement preview** (based on which SOP the use-case maps to):

- Use-cases addressed by I76 P1+P3 directly: #1, #2, #5, #6, #7, #8, #9, #12 — **8 of 12 = 67%**.
- Use-cases addressed only by I76 P2 (TOOL_CATALOG, not in P1+P3 scope per criterion §2): #4, #11.
- Use-cases addressed only by I76 P4 (AIC_PER_TASK_REGISTRY): #3, #10.

**Pre-measurement coverage estimate at I76 P3 entry: 67%** — falls in the 40-70% PARALLEL band per the criterion. Final measurement uses actual SOP §Scope coverage at I76 P3 entry, which may differ if SOPs end up addressing #4/#11 (TOOL_CATALOG use-cases) or #3/#10 (AIC use-cases) implicitly.

## 4. Operator-visible options to refine the criterion

The operator may want to adjust before ratifying:

- **Threshold**: 70% is the proposed default. Higher (e.g., 80%) skews toward parallel; lower (e.g., 60%) skews toward merge.
- **Numerator scope**: currently includes only P1 + P3 SOPs per the tracker §3.2 framing. Could widen to include I76 P2 (TOOL_CATALOG) or P4 (AIC_PER_TASK_REGISTRY) for a more generous merge bar — but that drifts from the tracker §3.2 framing of "I76 P3 vs I11" specifically.
- **Decision band widths**: 40% / 70% are the proposed band edges. Could be 50% / 75% (tighter merge bar) or 30% / 65% (looser).
- **Tiebreaker**: currently "inline-ratify". Could be "default to PARALLEL on tie" (no operator action needed) or "default to MERGE on tie" (more aggressive consolidation).

## 5. Cross-references

- Parent initiative: [I76 MADEIRA elevation](../master-roadmap.md)
- Tracked sibling: [I11 master-roadmap](../../11-madeira-ops-copilot/master-roadmap.md)
- Scope-overlap-tracker: [I11/I13/I17](../../_trackers/i11-i13-i17-scope-overlap-tracker.md) §3.2
- Sibling triage: [I17 per-deliverable triage](i17-deliverable-triage-2026-05-19.md)
- Governing rules: [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc), [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc)
- Governing decisions: D-IH-76-A (charter), D-IH-86-O (Option 5 default posture), D-IH-76-C (this criterion's ratification)
