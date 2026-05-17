---
report_id: i84-cross-area-unlock-handoff-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 / I84 Wave B1 successor pick-up
phase: P5 (pre-staged; awaits P4 substitution)
initiative: INIT-OPENCLAW_AKOS-84
classification: cross-area cascade summary (pre-stage; carries post-P4 substitution blocks)
access_level: 4
language: en
linked_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-C, D-IH-84-D, D-IH-84-E]
target_candidates:
  - i76-madeira-elevation.md
  - i74-brand-tooling-productization.md
  - i83-ai-archivist-and-kirbe-ingestor.md
  - i82-holistika-capability-doctrine-and-commercial-readiness.md
source_taxonomy: holistika-internal-research-synthesis
confidence_level: B2
---

# I84 P5 cross-area cascade handoff (pre-stage)

> **Pre-stage purpose.** Per master-roadmap section 3 P5 — translate P4 ratifications into cross-area downstream unlocks for the four candidate initiatives that gate on I84 outputs. This document **pre-stages** the per-candidate cascade summary so that once the operator answers `D-IH-84-B/C/D/E` at the I84 P4 batched inline-ratify gate, the parent agent can substitute the placeholder blocks below and (separately) edit the candidate stub files themselves.
>
> Per [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) section "When NOT to use" + Q3 Option C hybrid ratification (per `decision-log.md` `D-IH-84-A`): the SHAPE decisions ratify at I84 P4; the EXECUTION decisions defer to each owning initiative's P0. This handoff respects that boundary — it cites SHAPE outcomes; it does NOT mint EXECUTION decisions for downstream initiatives.
>
> **What this document DOES**: cite per-candidate the unblocking I84 output + the conundrum(s) it closes + the downstream owning initiative's P0 entry posture.
>
> **What this document DOES NOT**: edit the candidate stub files. Those edits stay with the parent agent post-P4 (per the I84 Wave B1 contract: pre-stage the report; defer the stub edits to operator-answer-time).

## 1. Cascade architecture overview

The cascade flows from the I84 P4 batched ratification outcomes (sections 2-5 below per candidate) to the four downstream candidate stubs:

```
I84 P4 batched ratification (D-IH-84-B/C/D/E)
    |
    +--> I76 (MADEIRA elevation)         <-- D-IH-84-C AIC framing F1-F5 closes C-76-1
    |       + Strand A external research deliverable substituted by I84 P1 audit dossier
    |
    +--> I74 (brand-tooling productization) <-- D-IH-84-D MADEIRA productization shape closes C-74-3
    |       + Cursor SDK ToS analysis (from regulatory-tos-forecast.md) informs C-74-4
    |
    +--> I83 (AI archivist + KiRBe ingestor) <-- D-IH-84-E KiRBe framework narrowing closes C-83-1
    |       (to 2-finalist; KiRBe-P0 picks between them)
    |
    +--> I82 (capability doctrine + commercial readiness)
            <-- SUBSTRATE_REGISTRY FK target extension for CAPABILITY_REGISTRY rows
            that name an underlying technical substrate
```

The four candidates have different unblocking profiles per the SHAPE/EXECUTION split: I76 + I74 + I83 each have a specific conundrum that I84 P4 closes; I82 has a register-shape extension (new FK column) rather than a conundrum-close.

## 2. I76 — MADEIRA elevation (target candidate stub: [`i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md))

### 2.1 What I84 closes for I76

- **Strand A external research deliverable** — I76 candidate section 3 named external substrate research as a pre-charter prerequisite. The I84 P1 audit dossier at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md) + the Tier-1 WIP threads (competitive + regulatory + past-PoC) + the founding-cycle quarterly report at [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md) collectively SUBSTITUTE for Strand A's external-research deliverable.
- **C-76-1 AIC framing pre-charter ratification** — I76 candidate section 2 named the F1-F5 AIC framing conundrum as the pre-charter blocking decision. The I84 P4 `D-IH-84-C` ratification closes this for I76 P0.

### 2.2 What stays with I76 P0

- The full AIC architecture authoring + per-framing implementation design (the EXECUTION layer; per Q3 Option C hybrid SHAPE/EXECUTION split).
- The C-76-2 through C-76-7 conundrums per I76 candidate section 5 (persistence shape, mode parity, tool catalog, sub-agents-or-not, etc.).
- Promotion criteria gate: operator promotes I76 candidate to active when ready post-cascade.

### 2.3 Stub-edit landed for `i76-madeira-elevation.md` (substituted 2026-05-17; commit `3900787`)

D-IH-84-C ratified as **F5 — Hybrid; per-task operator picks** at the I84 P4 batched gate. Parent agent landed a **non-destructive cascade header** on the i76 candidate stub in commit `3900787` (`feat(i84): P4 batched ratification - decision-log + report + candidate-stub cascade for D-IH-84-B/C/D/E`). The header note:

- Cites D-IH-84-C closure + D-IH-76-A pre-ratification (F5 framing).
- Substitutes I76 Strand A external-research deliverable with the I84 P1 audit dossier + Tier-1 WIP threads (Q2 2026) at [`docs/wip/intelligence/substrate-audit-2026-Q2/`](../../../intelligence/substrate-audit-2026-Q2/).
- Refreshes promotion criteria: I76 now promotes when (a) I84 closes — DONE, (b) I11 / I13 / I17 scope-overlap review completes (operator-driven), (c) operator chooses to promote.
- Names F5 as the I76 P0 starting point (rather than a discovery-led F1-F5 question).

Operator-pending forward-charter at I76 P0 charter time:
- Mint `D-IH-76-A` row in I76 decision register inheriting from `D-IH-84-C`.
- Edit Strand A body + Section 2 conundrum table to reference the cascade (optional; the header note already cites — body edits are I76-P0-time work).

### 2.4 Cross-references

- I76 candidate: [`docs/wip/planning/_candidates/i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md)
- I84 P4 decision: `decision-log.md` D-IH-84-C
- I84 P1 audit (substitutes I76 Strand A): [`reports/p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md)
- I84 founding-cycle quarterly: [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md)

## 3. I74 — brand-tooling productization (target candidate stub: [`i74-brand-tooling-productization.md`](../../_candidates/i74-brand-tooling-productization.md))

### 3.1 What I84 closes for I74

- **C-74-3 MADEIRA gate-criteria conundrum** — I74 candidate Strand C named the library-vs-agent-vs-hybrid (`@holistika/madeira-agent` packaging shape) conundrum as the pre-execution decision. The I84 P4 `D-IH-84-D` ratification closes this for I74 P4.
- **C-74-4 license-separation enforceability informed by Cursor SDK ToS** — the I84 Tier-1 WIP [`regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) section 4 + section 5 analyses of Cursor MSA + SDK ToS evolution + IP indemnity carve-outs inform C-74-4 license-separation enforceability. The operator-validated "embedding as backend service is allowed" clarification per I74 candidate context flows through this analysis.
- **D2 vs D1 vs D3 productization shape evidence** — the I84 P2 scorecard finding #5 + the competitive-layer-positioning section 6 analysis (D2 hosted-agent collides directly with Glean + Anthropic Projects; D1 library-only sidesteps; D3 hybrid hedges) supply the strategic-positioning evidence for the I74 productization shape ratification.

### 3.2 What stays with I74 P4

- The full per-package authoring + per-shape implementation design (`@holistika/akos-brand` + `@holistika/akos-render` + `@holistika/madeira-agent` packaging).
- The C-74-1 + C-74-2 + C-74-5 + remaining conundrums per I74 candidate section 4.
- Promotion criteria gate: operator promotes I74 candidate to active when ready post-cascade.

### 3.3 Stub-edit landed for `i74-brand-tooling-productization.md` (substituted 2026-05-17; commit `3900787`)

D-IH-84-D ratified as **D3 — Hybrid library + agent platform** at the I84 P4 batched gate. Parent agent landed a **non-destructive cascade header** on the i74 candidate stub in commit `3900787`. The header note:

- Cites D-IH-84-D closure + D-IH-74-D pre-ratification (D3 shape).
- Closes C-74-3 MADEIRA gate-criteria conundrum.
- Informs C-74-4 license-separation enforceability via the regulatory + ADVOPS analyses.
- Cross-links [`reports/advops-engagement-scoping-2026-05-17.md`](advops-engagement-scoping-2026-05-17.md) ADVOPS engagement recommendation as the pre-binding contract-surface gate.
- Frees I74 P0 charter to focus on library API surface + hosted-agent runtime architecture rather than productization-shape meta-decision.

Operator-pending forward-charter at I74 P0 charter time:
- Mint `D-IH-74-D` row in I74 decision register inheriting from `D-IH-84-D`.
- Edit Strand C body + Section 4 conundrum table to reference the cascade (optional body-level work).
- Schedule ADVOPS engagement per Options A-D in the scoping note before binding any Cursor SDK integration architecture.

### 3.4 Cross-references

- I74 candidate: [`docs/wip/planning/_candidates/i74-brand-tooling-productization.md`](../../_candidates/i74-brand-tooling-productization.md)
- I84 P4 decision: `decision-log.md` D-IH-84-D
- I84 regulatory analysis: [`docs/wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) sections 4-5
- I84 competitive analysis: [`docs/wip/intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md`](../../../intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md) section 6

## 4. I83 — AI archivist + KiRBe ingestor (target candidate stub: [`i83-ai-archivist-and-kirbe-ingestor.md`](../../_candidates/i83-ai-archivist-and-kirbe-ingestor.md))

### 4.1 What I84 closes for I83

- **C-83-1 framework-class-narrowing conundrum** — I83 candidate section 4 named the substrate-class narrowing as the pre-charter decision. The I84 P4 `D-IH-84-E` ratification closes this to **2 finalists** (likely `SUBS-RUN-LLAMA-LLAMAINDEX` continue + `SUBS-LANGCHAIN-AI-LANGGRAPH` workflow per past-PoC translation matrix section 5.3 analysis + scorecard section 4 finding #5).
- **Letta as candidate memory-layer pair** — `SUBS-LETTA-LETTA` flagged in past-PoC translation matrix section 5.3 as potential complementary layer (not finalist substitute; orthogonal memory layer); KiRBe-P0 evaluates per product-roadmap.

### 4.2 What stays with I83 P0

- The execution choice between the 2 finalists (KiRBe-P0 picks based on product-roadmap fit).
- Whether to add Letta as a complementary memory layer (KiRBe-P0 evaluates).
- The full archivist + ingestor architecture + implementation design.
- The C-83-2 through C-83-N remaining conundrums per I83 candidate section 4.
- Promotion criteria gate: operator promotes I83 candidate to active when ready post-cascade.

### 4.3 Stub-edit landed for `i83-ai-archivist-and-kirbe-ingestor.md` (substituted 2026-05-17; commit `3900787`)

D-IH-84-E ratified as **E1 — LlamaIndex-continue + LangGraph-workflow** (2 finalists; I83 P0 picks between them or composes both) at the I84 P4 batched gate (initial gate + follow-up gate; operator asked for narrowing-help; agent presented B5-grounded analysis; operator ratified E1). Parent agent landed a **non-destructive cascade header** on the i83 candidate stub in commit `3900787`. The header note:

- Cites D-IH-84-E closure + D-IH-83-A pre-ratification (E1 narrowing).
- Names both finalists (`SUBS-RUN-LLAMA-LLAMAINDEX` + `SUBS-LANGCHAIN-AI-LANGGRAPH`) with substrate-row citations.
- Surfaces the likely composition outcome (LlamaIndex-for-retrieval + LangGraph-for-workflow-orchestration via langchain-native tool protocol).
- Notes `SUBS-LETTA-LETTA` as candidate memory-layer pair (orthogonal; KiRBe P0 evaluates).
- Rules out Cursor SDK + LlamaIndex (the operator's "somehow D" preference) per the B5 self-governance + retractability + open-source principle ratified at D-IH-84-B.

Operator-pending forward-charter at I83 P0 charter time:
- Mint `D-IH-83-A` row in I83 decision register inheriting from `D-IH-84-E`.
- Edit Section 4 C-83-1 + add Section 4 Letta-as-memory-pair note (optional body-level work).
- KiRBe P0 picks primary orchestration anchor or composes both finalists.

### 4.4 Cross-references

- I83 candidate: [`docs/wip/planning/_candidates/i83-ai-archivist-and-kirbe-ingestor.md`](../../_candidates/i83-ai-archivist-and-kirbe-ingestor.md)
- I84 P4 decision: `decision-log.md` D-IH-84-E
- I84 past-PoC analysis: [`docs/wip/intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md`](../../../intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md) section 5.3 (KiRBe narrowing analysis)
- I84 scorecard finding #5: [`reports/p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) section 4

## 5. I82 — capability doctrine + commercial readiness (target candidate stub: [`i82-holistika-capability-doctrine-and-commercial-readiness.md`](../../_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md))

### 5.1 What I84 contributes to I82

I82 is structurally different from I76 / I74 / I83 — it doesn't have a specific conundrum that I84 P4 closes. Instead, I84 contributes a **register-shape extension**: SUBSTRATE_REGISTRY becomes a candidate FK target for CAPABILITY_REGISTRY rows that name an underlying technical substrate.

- **CAPABILITY_REGISTRY column-spec extension** — per I82 candidate section 2a (capability register column shape), capabilities that depend on a specific technical substrate (e.g., "capability X depends on `SUBS-Y-Z`") can FK to SUBSTRATE_REGISTRY via a new `substrate_id` column. The capability-as-product positioning informs whether the FK is mandatory (capability names a substrate) or optional (substrate-agnostic capability).
- **Substrate evidence for capability-as-product positioning** — the I84 P1 + P2 + Tier-1 WIP analyses inform capabilities-that-depend-on-substrate positioning at scale (e.g., "MADEIRA capability X requires Cursor SDK substrate; pricing reflects vendor pass-through cost").

### 5.2 What stays with I82 P0-P4

- The CAPABILITY_REGISTRY column-shape ratification (operator-gated canonical-CSV gate at I82 P2 per the I82 candidate scope).
- The capability rows themselves (operator-gated canonical-CSV mint per discipline).
- The commercial readiness analysis (independent of I84 substrate evidence in scope).

### 5.3 Stub-edit landed for `i82-holistika-capability-doctrine-and-commercial-readiness.md` (substituted 2026-05-17; commit `3900787`)

All 4 D-IH-84-B/C/D/E ratifications relevant as evidence inputs to I82 (per Section 5.2 above — I82 doesn't have a specific conundrum that I84 P4 closes; it has a register-shape extension). Parent agent landed a **non-destructive cascade header** on the i82 candidate stub in commit `3900787`. The header note:

- Cites the I84 P4 batched ratification + the I84 P3b live 18-row SUBSTRATE_REGISTRY canonical (+ Supabase mirror) as the FK target now live.
- Specifies the CAPABILITY_REGISTRY column-spec extension: nullable `substrate_id` FK to SUBSTRATE_REGISTRY for capabilities that name an underlying technical substrate (e.g., "capability X depends on substrate Y"); leave blank for substrate-agnostic methodology capabilities.
- Surfaces the queryability gain (e.g., "all capabilities that depend on LlamaIndex" / "all capabilities exposed via OpenClaw thin-adapter").
- Confirms no I82 promotion-criteria changes; just a column-spec refresh consumed at I82 P0 charter.

Operator-pending forward-charter at I82 P0 charter time:
- Incorporate the `substrate_id` FK column into the `CAPABILITY_REGISTRY.csv` mint scope (P2 facet 2a).
- Author the substrate-agnostic-vs-substrate-named semantics in the I82 doctrine prose (P1 doctrine authoring).
- Cross-link the I84 founding-cycle 2026-Q2 quarterly report for substrate-cost evidence informing capability pricing positioning.

### 5.4 Cross-references

- I82 candidate: [`docs/wip/planning/_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md`](../../_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md)
- I84 P4 decisions: `decision-log.md` D-IH-84-B/C/D/E (all four are evidence inputs to I82)
- SUBSTRATE_REGISTRY canonical: [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv)
- I84 founding-cycle quarterly: [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md)

## 6. Internal-link integrity (pre-stage check)

This report pre-stages the cross-area cascade. Internal-link integrity for the candidate-stub edits will be verified at parent-agent edit time (post-P4). For this pre-stage report:

- All 4 candidate stubs (i76, i74, i83, i82) exist at the cited paths (verified via Glob discovery during Wave B1 authoring).
- All 6 upstream I84 evidence sources cited (P1 audit, P2 scorecard, ADVOPS scoping, founding-cycle Q2, 3 Tier-1 WIP threads) exist and were authored in prior waves.
- All 4 D-IH-84-B/C/D/E decision IDs are registered in `decision-log.md` per the I84 P0 charter.
- SUBSTRATE_REGISTRY canonical exists at the cited path with 18 rows live (per I84 P3b canonical-CSV gate).

## 7. Cross-references

- [`master-roadmap.md`](../master-roadmap.md) section 3 P5 — the deliverable contract this report serves.
- [`decision-log.md`](../decision-log.md) D-IH-84-A (Q3 Option C SHAPE/EXECUTION split) + D-IH-84-B/C/D/E (the 4 ratifications cascade flows from).
- [`risk-register.md`](../risk-register.md) R-IH-84-4 (cross-area cascade over-reach risk) — mitigated by the explicit SHAPE-not-EXECUTION posture in sections 2.2 / 3.2 / 4.2 / 5.2 above.
- [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) section "When NOT to use" — the rule that drives the SHAPE-not-EXECUTION posture this cascade respects.
- [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) — the cross-area handoff SOP this cascade follows.
- I76 candidate: [`docs/wip/planning/_candidates/i76-madeira-elevation.md`](../../_candidates/i76-madeira-elevation.md)
- I74 candidate: [`docs/wip/planning/_candidates/i74-brand-tooling-productization.md`](../../_candidates/i74-brand-tooling-productization.md)
- I83 candidate: [`docs/wip/planning/_candidates/i83-ai-archivist-and-kirbe-ingestor.md`](../../_candidates/i83-ai-archivist-and-kirbe-ingestor.md)
- I82 candidate: [`docs/wip/planning/_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md`](../../_candidates/i82-holistika-capability-doctrine-and-commercial-readiness.md)
- I84 evidence stack: [`reports/p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md), [`reports/p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md), [`reports/advops-engagement-scoping-2026-05-17.md`](advops-engagement-scoping-2026-05-17.md), [`docs/wip/intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md`](../../../intelligence/substrate-audit-2026-Q2/2026-Q2-substrate-audit.md), [`docs/wip/intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md`](../../../intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md), [`docs/wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md), [`docs/wip/intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md`](../../../intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md)

## 8. Provenance

Pre-staged at I84 Wave B1 (parallel-to-P4-foreground gate per I86 successor-pickup) 2026-05-17. Confidence `B2` for the pre-stage analysis; the per-candidate cascade specifics promote to higher confidence once the operator answers D-IH-84-B/C/D/E at the P4 gate and the parent agent substitutes the placeholder blocks above + edits the candidate stub files.

**Operator gate.** Per master-roadmap section 3 P5 — PAUSE POINT #3 operator confirms the cascade lands cleanly. This pre-stage gives the operator the cascade-shape preview before the substantive cascade fires; substantive cascade (stub-edits) waits on P4 + the explicit operator approval at PAUSE POINT #3.
