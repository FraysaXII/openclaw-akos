---
initiative_id: INIT-OPENCLAW_AKOS-74
title: I74 Brand-tooling productization (TRIGGER-2 OS-library fork preparation)
status: active
authored: 2026-05-21
last_review: 2026-05-21
inception_decision_id: D-IH-74-A
owner_role: Brand & Narrative Manager
co_owner_role: CTO
authority: Founder + Brand & Narrative Manager + CTO
language: en
parent_dependency:
  - INIT-OPENCLAW_AKOS-70
  - INIT-OPENCLAW_AKOS-86
sibling_initiatives:
  - INIT-OPENCLAW_AKOS-71
  - INIT-OPENCLAW_AKOS-72
  - INIT-OPENCLAW_AKOS-73
  - INIT-OPENCLAW_AKOS-76
linked_decisions:
  - D-IH-74-A
  - D-IH-86-CC
  - D-IH-74-D
  - D-IH-84-D
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/MADEIRA-AKOS/STATUS.md
authoritative_plan: docs/wip/planning/74-brand-tooling-productization/master-roadmap.md
methodology_version_at_authoring: v3.1
program_anchors:
  - PRJ-HOL-MAD-2026
  - PRJ-HOL-INF-2026
---

# I74 — Brand-tooling productization (TRIGGER-2 OS-library fork preparation)

> **Status: active** (promoted 2026-05-21 under I86 Wave O via OVERRIDE `D-IH-86-CC`; speculative-promotion debt explicitly accepted — TRIGGER-2 zero-count overridden so charter can stage library + agent platform architecture in advance of first external request). Inception ratified by `D-IH-74-A`. Charter scaffold per `as-far-as-possible-with-defaults` pace clause; full P0 charter expansion happens at this initiative's own first wave.

## Lineage (why I74 promotes now under OVERRIDE)

The candidate file [`docs/wip/planning/_candidates/i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md) names TRIGGER-2 (≥2 external orgs request AKOS doctrine consumption) as the prerequisite. Per `D-IH-86-CC` Wave O OVERRIDE, the operator chose Option C — accept speculative-promotion debt; promote I74 now so library + hosted-agent architecture can be staged in advance of the first external request landing.

`D-IH-74-D` was pre-ratified at I84 P4 via `D-IH-84-D` (D3 = Hybrid library + agent platform). Strand C (`@holistika/madeira-agent`) shape gate closed. I74 P0 charter inherits D-IH-74-D and is free to focus on library API surface + hosted-agent runtime architecture decisions rather than the productization-shape meta-decision.

The corresponding blocker-tracker at [`docs/wip/planning/_blockers/i74-promotion-blocker-tracker.md`](../_blockers/i74-promotion-blocker-tracker.md) is **closed** at this commit per Wave O OVERRIDE; tracker file should be marked superseded by D-IH-86-CC at next housekeeping wave.

## Operating story

I70 P5-P7 produced a brand-discipline canon-set that is **portable methodology** rather than a Holistika-only artifact (7 tic families + 5-level confidence ladder × 4-quadrant audience matrix + 3-file bilingual README pattern + engagement-counterparty README contract + per-locale register matrix). I71 makes this canon **enforceable** via four validator packs. The next governance question is whether the canon is also **distributable**: can a non-Holistika org consume the brand-discipline as a methodology library?

The license posture is set in `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`: **the brand marks are Holistika's; the discipline is portable methodology**. Productization shape:

- A library (e.g. `@holistika/akos-brand`) that exports the **rules** (validators + rule-pack YAMLs) without the **identity** (no Holistika logos / palette / counter-cover marks).
- A second library (`@holistika/madeira-agent` or similar) that productizes the AIC-as-category MADEIRA agent-companion pattern per D-IH-74-D = D3 hybrid library + agent platform.
- License documentation distinguishing **methodology consumption** (free / open) from **brand-mark licensing** (Holistika-only).

## Phase shape (proposed; ratified at P0)

| Phase | Purpose | Deliverable | Effort | Pause-point |
|:---|:---|:---|---:|:---|
| **P0** | Charter + architectural decisions (Strand A library API + Strand C agent platform shape) | D-IH-74-A..F; OPS-74-1..4 | 2d | standard |
| **P1** | `@holistika/akos-brand` library MVP (validators + rule-pack YAMLs; no brand-identity assets) | npm package skeleton; license docs; methodology overview | 3-5d | standard |
| **P2** | `@holistika/madeira-agent` library MVP per D3 hybrid (library exports + hosted-agent runtime skeleton) | second npm package; runtime architecture doc | 3-5d | **canonical-CSV gate** (ADVOPS license posture review per `regulatory-tos-forecast.md` §6 + §7) |
| **P3** | License separation enforceability validation (ADVOPS engagement per `advops-engagement-scoping-2026-05-17.md`) | License contract + IP-indemnity carve-out doc | 2d | **legal-template handoff** (mandatory per `akos-agent-checkpoint-discipline.mdc`) |
| **P4** | External pilot (first external org consumes library; UAT against TRIGGER-2 first-request) | Pilot report; library feedback loop integrated | 3d | standard |
| **P5** | Closure + GA / scale-up forward-charter | Closure pause record; UAT report | 0.5d | closure-mega-ratify |

Total estimated effort: **13-19 days** for library + hosted-agent MVP; GA + ongoing maintenance is post-closure operations work.

## Decisions preview

| ID | Question | Owner | Status entering | Close-out |
|:---|:---|:---|:---|:---|
| **D-IH-74-A** | I74 mega-charter scope — library + hosted-agent MVP + external pilot | Brand Manager + Tech Lab Lead | RATIFIED via D-IH-86-CC OVERRIDE | this commit |
| **D-IH-74-B** | Library API surface (which validators + which rule-packs ship in @holistika/akos-brand v1) | Brand Manager + Tech Lab Lead | Proposed | P0 |
| **D-IH-74-C** | Hosted-agent runtime architecture (TypeScript-native? AKOS-mirror? hybrid?) | Tech Lab Lead + System Owner | Proposed | P0 |
| **D-IH-74-D** | Productization shape (library / agent platform / hybrid) | Brand Manager + Tech Lab Lead | RATIFIED via D-IH-84-D (D3 hybrid) | inherited |
| **D-IH-74-E** | License enforceability (methodology vs brand-marks; ADVOPS engagement required) | Founder + Legal | Proposed | P3 (legal-template handoff) |
| **D-IH-74-F** | TRIGGER-2 deferred-charter posture (charter now; await external request as activation signal for P4 pilot) | Founder | RATIFIED via D-IH-86-CC OVERRIDE | this commit |

## Risks (top 5)

| ID | Risk | L | I | Mitigation |
|:---|:---|:---:|:---:|:---|
| **R-IH-74-1** | Speculative productization without TRIGGER-2 firing (per candidate §1 + §6) | High | Medium | Accept per D-IH-86-CC OVERRIDE; library + agent platform shipped at MVP only; P4 pilot deferred until TRIGGER-2 fires (≥2 external orgs request) |
| **R-IH-74-2** | License separation enforceability unclear (brand-marks vs methodology) | Medium | High | Mandatory ADVOPS engagement at P3 per `regulatory-tos-forecast.md` §6 + §7 |
| **R-IH-74-3** | Hosted-agent runtime competes with Holistika's own internal use of MADEIRA | Low | High | Architecture decision at P0 (D-IH-74-C); shared substrate vs forked substrate is operator-ratified |
| **R-IH-74-4** | I71/I72/I73 not yet closed when I74 promotes | Medium | Medium | Per D-IH-86-CC OVERRIDE accepted; I71/I72/I73 closure tracking continues in their own initiatives |
| **R-IH-74-5** | HLK Tech Lab capacity not available | Medium | High | P0 capacity assessment; if blocked, defer P1+ to next operator cycle |

## Closure criteria

- Charter (P0..P5) ratified.
- `@holistika/akos-brand` v1 published (or pre-published; license docs complete).
- `@holistika/madeira-agent` v1 architecture complete (per D-IH-74-D = D3 hybrid).
- ADVOPS license-enforceability sign-off recorded.
- One external pilot completed (or P4 deferred pending TRIGGER-2 first-request).
- Closure UAT report at `reports/uat-i74-closure-<YYYY-MM-DD>.md`.

## Cross-references

- Candidate: [`i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md).
- Promotion override: `D-IH-86-CC` (Wave O OVERRIDE).
- Shape pre-ratification: `D-IH-84-D` (D3 hybrid library + agent platform).
- Blocker-tracker (closed at this commit): [`i74-promotion-blocker-tracker.md`](../_blockers/i74-promotion-blocker-tracker.md).
- ADVOPS prerequisite: [`regulatory-tos-forecast.md`](../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) §6 + §7.
- Cluster coordinator: [I86](../86-initiative-cluster-execution-coordinator/master-roadmap.md).
- Governing rules: [`akos-mirror-template.mdc`](../../../.cursor/rules/akos-mirror-template.mdc), [`akos-brand-baseline-reality.mdc`](../../../.cursor/rules/akos-brand-baseline-reality.mdc), [`akos-agent-checkpoint-discipline.mdc`](../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc).
