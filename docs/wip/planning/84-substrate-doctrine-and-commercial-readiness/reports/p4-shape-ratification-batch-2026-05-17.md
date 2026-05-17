---
language: en
classification: phase_ratification_record
initiative: INIT-OPENCLAW_AKOS-84
phase: P4
authored: 2026-05-17
role_owner: Holistik Researcher (executor) + Founder (ratifier) + System Owner (co-signer)
gate_type: inline-ratify (batched)
linked_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-C, D-IH-84-D, D-IH-84-E]
linked_canonicals:
  - SUBSTRATE_REGISTRY.csv
  - SUBSTRATE_LANDSCAPE_DOCTRINE.md
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - MADEIRA-AKOS/STATUS.md
---

# I84 P4 — Architectural shape ratification batch (2026-05-17)

> **Phase scope**: ratify the 4 load-bearing architectural shape decisions (D-IH-84-B / C / D / E) using P1+P2+P3 evidence as input. Per Q3 ratification (D-IH-84-A Option C hybrid): SHAPE decisions ratify here; EXECUTION decisions defer to each owning initiative's P0.
>
> **Pattern applied**: inline-ratify batched gate per [`.cursor/rules/akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) + [`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md). 4 decisions in 1 AskQuestion call + 1 follow-up AskQuestion for D-IH-84-E narrowing (operator asked for help deciding).

## 1. Pre-flight evidence sweep (per inline-ratify-craft Principle 1)

Before posing the P4 batched question, the executor ran the following evidence sweep:

- Read [`master-roadmap.md`](../master-roadmap.md) §3 P4 deep section + §5 decision-log preview + §6 risk preview.
- Read [`decision-log.md`](../decision-log.md) full D-IH-84-A through D-IH-84-I rationale (and the option sets for B/C/D/E).
- Read [`sc-i84-p1p2-complete-2026-05-17.md`](checkpoints/sc-i84-p1p2-complete-2026-05-17.md) §4 (outstanding work) + §7 (new risks surfaced by Tier-1 WIP dossier).
- Re-read [`p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md) §4.6 + §4.7 (Devin/Replit reclassification) + Madeira-positioning sections that bear on D-IH-84-D.
- Re-read [`p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) scenario analyses that inform D-IH-84-B.
- Re-read [`competitive-layer-positioning.md`](../../../intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md) (informs D-IH-84-D).
- Re-read [`regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) §4.3 + §6 + §7 (Cursor SDK ToS forecast + ADVOPS triggers that bear on D-IH-84-B).
- Re-read [`past-poc-translation-matrix.md`](../../../intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md) §5.3 (KiRBe substrate-continuity argument that bears on D-IH-84-E).
- Re-read [`SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) 18 rows (B1/B2/B3 anchors at L17/L10/L18; F1-F4 framings encoded in `aic_pattern_role` column across 18 rows; D1/D2/D3 productization roles encoded in `madeira_productization_role` column; E candidates at L3 + L4).
- Re-read [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) §1 (substrate-question structurally orthogonal to LLM-choice + AIC-framing questions) + §4 (substrate-continuity doctrine; methodology-portability axiom) + §5 (AKOS-substrate ≠ Madeira-substrate optimization functions).
- Re-read [`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) pre-flight checklist (Principle 1-6 walkthrough + bad-pattern audit).

The sweep collapsed several plausible-on-paper options into clear leaders:
- **B**: B1 vs B2 vs B3 vs B3-conditional vs B-defer → operator-delegated novel B5 (executive call recovery posture).
- **C**: F5 was the structural option once `aic_pattern_role` column was inventoried across 18 rows — no single F1-F4 could be enforced without rejecting half the inventory.
- **D**: D3 was clearly indicated by TRIGGER-1 + TRIGGER-2 dual mapping in MADEIRA-AKOS/STATUS.md §3 (D1 ignores TRIGGER-1; D2 ignores TRIGGER-2; D3 captures both).
- **E**: E1 was clearly indicated by past-poc-translation-matrix.md §5.3 explicit recommendation; E4 was structurally precluded by D-IH-84-B B5 self-governance + retractability principle (Cursor SDK license_class=proprietary-saas conflicts).

## 2. The 4 inline-ratify gates (the AskQuestion call)

### 2.1 D-IH-84-B — AKOS substrate-baseline-choice

**Question posed**: "AKOS substrate-baseline-choice — what is AKOS made of going forward?"

**Options surfaced** (5): B1 stay-OpenClaw / B2 migrate-Cursor-SDK / B3 hybrid (recommended pending evidence) / B3-conditional (defer binding until ADVOPS clears) / B-defer (defer to Q3).

**Operator answer**: novel framing — "option D but craft this with your best expertise and our best tech and knowledge to govern this whole process and make the cursor sdk part as retractable as possible. our end goal is to fully govern our own space. even though we are not into model training we want to govern our applications and its infrastructure as soon as we can. that's why a deep llamaindex or similar infrastructure is our end goal when we know how to wire maintain upgrade adapt and build everything ourselves. I trust you can browse our context and intent to craft the best solution"

**Ratified**: **B5 — Bridge-with-strict-retractability (tactical) + deep-self-owned-LlamaIndex-or-similar-substrate (strategic endgame)**. Encoded as `decision_source: agent_executive_call_per_operator_delegation` per inline-ratify-craft §"Pitfall: I have run the evidence sweep but I do not see clear options" recovery posture (operator explicitly delegated craft with a clear principle).

**Architecture detail** in [`decision-log.md` D-IH-84-B](../decision-log.md). Summary:
- **Tactical (today through 2026-Q4)**: B3-shaped hybrid (Cursor SDK frontend + OpenClaw policy backend) with the **retractability axiom** as binding architectural principle. All Cursor-SDK code paths sit behind a single integration boundary (`akos/cursor_sdk_adapter.py` proposed, not yet minted); same provider interface as `akos/model_catalog.py`; no Cursor-SDK-specific types leak into AKOS-core; parity with OpenClaw thin-adapter path is the retractability gate; ADVOPS engagement is the contract-surface gate.
- **Strategic (2026-Q4+ trajectory)**: deep self-owned substrate (LlamaIndex or successor open-source) as the orchestration anchor; Cursor SDK reverts to optional operator-DX layer (or full retraction) once self-owned substrate is operationally mature.

### 2.2 D-IH-84-C — AIC framing F1-F5 binding choice

**Question posed**: "AIC framing F1-F5 binding choice — which agentic pattern does Holistika adopt as the load-bearing AIC shape (closes I76 C-76-1)?"

**Options surfaced** (6): F1 / F2 / F3 / F4 / F5 (recommended) / F-defer.

**Operator answer**: `Selected option(s) f5-hybrid-per-task`.

**Ratified**: **F5 — Hybrid; per-task operator picks**.

**Rationale** (per inline-ratify-craft Principle 2): preserves the I76 candidate F1-F5 framing as a choice-surface; matches operator's actual workflow where different tasks call for different patterns; couples cleanly with D-IH-84-B B5 (hybrid substrate exposes multiple agentic patterns through same provider abstraction). `SUBSTRATE_REGISTRY.csv` `aic_pattern_role` column across 18 rows already supports F5 — no single F1-F4 could be enforced without rejecting half the inventory.

I76 P0 receives a clean F5 ratification and is free to focus on **per-pattern instantiation** decisions (which task-classes default to which framing) rather than the meta-decision.

### 2.3 D-IH-84-D — MADEIRA productization shape

**Question posed**: "MADEIRA productization shape — how does MADEIRA ship when productized (closes I74 C-74-3)?"

**Options surfaced** (5): D1 library-only / D2 agent-only / D3 hybrid (recommended) / D-shape-only (defer execution) / D-defer (defer to I74).

**Operator answer**: `Selected option(s) d3-hybrid-library-and-agent`.

**Ratified**: **D3 — Hybrid: library for technically-mature customers + hosted agent for less-technical customers**.

**Rationale** (per inline-ratify-craft Principle 2): preserves market-segmentation flexibility; library entry-point lowers customer-acquisition friction; hosted-agent captures premium revenue. Maps cleanly to BOTH TRIGGER-1 (hosted-agent-when-≥3-external-orgs-request-data-detached) AND TRIGGER-2 (library-when-≥2-external-orgs-request-AKOS-as-library) per [`MADEIRA-AKOS/STATUS.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md) §3 — D1 ignores TRIGGER-1; D2 ignores TRIGGER-2; D3 captures both. Couples cleanly with D-IH-84-B B5 — hybrid productization mirrors hybrid substrate; library customers operate on their own substrate, hosted-agent customers operate on Holistika's B5-retractable-tactical + self-owned-strategic substrate.

`SUBSTRATE_REGISTRY.csv` `madeira_productization_role` column already supports D3 (backend-only + library-import + agent-runtime + not-applicable enum values authored at P3a anticipating D3).

### 2.4 D-IH-84-E — KiRBe framework-class-narrowing (initial gate + follow-up)

**Initial question posed**: "KiRBe framework-class-narrowing — which 2 finalists does KiRBe-ingestor narrow to for its P0 framework choice (closes I83 C-83-1 to 2-finalist)?"

**Options surfaced** (5): E1 LlamaIndex+LangGraph (recommended) / E2 LlamaIndex+CrewAI / E3 LangGraph-only-discontinue-LlamaIndex / E4 Cursor SDK + LlamaIndex (novel) / E-defer.

**Operator answer**: "I like A, B and somehow D even. can you help me decide?" — explicit request for follow-up inline-ratify with agent analysis weighted against B5.

**Follow-up question posed** (per inline-ratify-craft §"Pitfall: the operator answers ambiguously or with mixed signals"): "Given your D-IH-84-B commitment to 'full govern our own space + deep LlamaIndex-or-similar endgame + Cursor-SDK-retractable', which 2 KiRBe finalists should we narrow to (I83 P0 picks between the 2)?"

**Follow-up options surfaced** (4): E1 (recommended; reasons grounded in B5 + structural fit + past-poc recommendation) / E2 (operator's B-option; cost analysis) / E1+E2 keep-3-finalists (novel framing honoring A+B simultaneously) / E4 (operator's D-option; explicit B5 conflict surfaced).

**Operator answer**: `Selected option(s) e1-langgraph-finalist-pair`.

**Ratified**: **E1 — LlamaIndex-continue + LangGraph-workflow** (2 finalists; I83 P0 picks between them as the orchestration partner; composition of both is the likely I83 P0 outcome).

**Rationale**: detailed in [`decision-log.md` D-IH-84-E](../decision-log.md). Summary: best fit for KiRBe's INGESTOR role (pipeline-shaped); both open-source MIT aligned with B5; LangGraph dispatcher pattern matches F3 in F5 framing; substrate continuity per SUBSTRATE_LANDSCAPE_DOCTRINE.md §4 principle 2; past-poc-translation-matrix.md §5.3 explicit recommendation match.

## 3. Cascade summary (cross-decision coupling)

The 4 ratified decisions are tightly coupled and mutually reinforcing (which is why the batched gate was the correct pattern per inline-ratify-craft Principle 5):

| Coupling | Concrete shape |
|:---|:---|
| B5 ↔ C (substrate ↔ framing) | B5 hybrid substrate exposes multiple agentic patterns through same provider abstraction → F5 per-task is the natural agentic-pattern analog of B5's substrate-pattern hybrid |
| B5 ↔ D (substrate ↔ productization) | B5 retractable-tactical + self-owned-strategic mirrors D3 library-for-mature + hosted-for-less-technical; hosted-agent path operates on Holistika's B5 substrate |
| B5 ↔ E (substrate ↔ KiRBe framework) | B5 self-governance + open-source endgame ruled out E4 (Cursor SDK, proprietary-SaaS); LlamaIndex + LangGraph both MIT-open-source align with B5 |
| C ↔ E (framing ↔ KiRBe) | F5 per-task framing accommodates F3 dispatcher pattern naturally; KiRBe ingestor workflows are F3-shaped tasks the F5 framing handles cleanly |
| D ↔ E (productization ↔ KiRBe) | D3 library path can ship KiRBe-style ingestors as library components; hosted-agent path can offer KiRBe-as-service variant; both consume LlamaIndex+LangGraph anchor |

The cascade landed coherently with no internal contradictions.

## 4. Downstream cascade (operator-pending forward-charter)

Per Q3 D-IH-84-A Option C hybrid posture: SHAPE landed at P4 (above); EXECUTION decisions stay with each owning initiative's P0. The P5 cross-area cascade [`cross-area-unlock-handoff-2026-05-17.md`](cross-area-unlock-handoff-2026-05-17.md) details the per-candidate downstream impact:

- **I76 Madeira elevation candidate** — receives F5 ratification as D-IH-76-A pre-ratification; C-76-1 closes; I76 P0 charter is free to focus on per-pattern instantiation (which tasks default to F1 vs F2 vs F3 vs F4 in operator workflow).
- **I74 brand-tooling productization candidate** — receives D3 ratification as D-IH-74-D pre-ratification; C-74-3 closes; I74 P0 charter is free to focus on library API surface + hosted-agent runtime architecture decisions.
- **I83 AI archivist + KiRBe ingestor candidate** — receives E1 ratification (narrowing to 2 finalists: LlamaIndex + LangGraph) as C-83-1 closure; I83 P0 charter is free to focus on the orchestration anchor pick + composition pattern.
- **I82 Holistika capability doctrine candidate** — `CAPABILITY_REGISTRY` columns extend to include `substrate_id` FK to `SUBSTRATE_REGISTRY` for capabilities that name an underlying technical substrate.

## 5. ADVOPS engagement implication

The B5 ratification incorporates the ADVOPS contract-surface gate into its tactical-layer integration discipline: any Cursor SDK use requires the ADVOPS engagement framework to clear EU AI Act provider-vs-deployer classification + IP-indemnity carve-out review before binding. The [`advops-engagement-scoping-2026-05-17.md`](advops-engagement-scoping-2026-05-17.md) report (authored at I84 P5 scope alongside this P4 batch) details the 4-discipline framework (EU AI Act counsel + GDPR/DPA counsel + IP/IT counsel + jurisdictional fiscal) and the operator-action surface.

Operator decision on whether to engage ADVOPS now (Q3 2026) or defer to first concrete Cursor SDK integration (Q4 2026) is forward-charter — not in P4 scope.

## 6. Forward-charter — operator-pending items

The P4 ratifications produce forward-charter items that need operator action to land (not in P4 scope; tracked here for traceability):

1. **DECISION_REGISTER.csv canonical rows for D-IH-84-B / C / D / E** — per [`.cursor/rules/akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc) §"HLK compliance changes" the canonical row mints when an operator-approved tranche fires; the P0 charter tranche included these 4 rows as operator-pending (per master-roadmap §7). Recommend bundle with the next operator-approved canonical-CSV tranche.
2. **INITIATIVE_REGISTRY.csv I84 row mint + I12/I13 supersession flip** — operator-pending forward-charter (master-roadmap §7).
3. **OPS_REGISTER.csv 8 I84 rows** — operator-pending forward-charter (master-roadmap §7).
4. **D-IH-84-CLOSURE row** — minted at P8 closure (separate ratification event; deferred per master-roadmap §5 decision-log preview row "deferred").
5. **`process_list.csv` row `env_tech_dtp_substrate_landscape_mtnce_001`** — required by SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md to promote from `status: review` to `status: active` per SOP-META ordering. Operator-pending tranche.
6. **Per-candidate D-IH-NN-X pre-ratification rows** — D-IH-76-A (F5 framing for AICs in I76), D-IH-74-D (D3 productization for I74), D-IH-83-A (LlamaIndex anchor for KiRBe; LangGraph composition partner; both narrowed-to-2) — land at each candidate's P0 charter when promoted; not in I84 scope.

## 7. Validation

Pre-foreground-commit validators (run sequentially during this chat):

- `py scripts/validate_hlk.py` — PASS at every checkpoint of this chat (pre-P4, post-decision-log, post-P4-report). One advisory warning persists on closed-initiative I77 master-roadmap missing `closed_at` companion (pre-existing per checkpoint §3; not caused by P4).
- `py scripts/validate_substrate_registry.py` — PASS (18 rows; no change at P4).
- `py scripts/validate_compliance_schema_drift.py` — PASS (no canonical CSV schema changes at P4).

Post-foreground-commit validators (deferred to subagent return when CSV updates land):

- `py scripts/release-gate.py` — to run after subagent completes its scope and all P4-substituted skeletons are in place.

## 8. Cross-references

- [`decision-log.md`](../decision-log.md) — full per-decision rationale for D-IH-84-B / C / D / E.
- [`master-roadmap.md`](../master-roadmap.md) §3 P4 deep section — phase contract this P4 batch fulfilled.
- [`sc-i84-p1p2-complete-2026-05-17.md`](checkpoints/sc-i84-p1p2-complete-2026-05-17.md) — pre-P4 checkpoint that surfaced the gate.
- [`p1-substrate-landscape-2026-05-17.md`](p1-substrate-landscape-2026-05-17.md) + [`p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) — P1+P2 evidence base.
- [`competitive-layer-positioning.md`](../../../intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md) + [`regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) + [`past-poc-translation-matrix.md`](../../../intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md) — Tier-1 WIP threads that informed the ratifications.
- [`SUBSTRATE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) — 18-row canonical state-of-record (no changes at P4).
- [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) — Research-area doctrine (no changes at P4).
- [`cross-area-unlock-handoff-2026-05-17.md`](cross-area-unlock-handoff-2026-05-17.md) — P5 cross-area cascade (consumes this P4 ratification).
- [`advops-engagement-scoping-2026-05-17.md`](advops-engagement-scoping-2026-05-17.md) — ADVOPS scoping (informs B5 contract-surface gate).
- [`.cursor/skills/inline-ratify-craft/SKILL.md`](../../../../.cursor/skills/inline-ratify-craft/SKILL.md) — craft principles applied at every gate of this batch.
