# I84 — Decision log

> Per [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar" — inline preview table lives in [`master-roadmap.md`](master-roadmap.md) §5. Full per-decision rationale below. DECISION_REGISTER.csv canonical rows are operator-pending at P0 close (canonical-CSV gate per [`akos-governance-remediation.mdc`](../../../.cursor/rules/akos-governance-remediation.mdc) §"HLK compliance governance").

## D-IH-84-A — I84 mega-charter scope (3-question architecture)

- **Question**: What is the shape of the founder-directive's Research-area substrate-and-commercialization-intelligence initiative?
- **Owner**: Founder + Research-area Lead (KM Officer interim per [`i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md) §3 Strand C pre-Research-Director) + System Owner.
- **Ratified**: 2026-05-16 inline-ratify batched gate (3 questions per [`inline-ratify-craft/SKILL.md`](../../../.cursor/skills/inline-ratify-craft/SKILL.md)).
- **Decision**: (Q1) Option D hybrid — standalone I84 + continuous Research-area discipline as closure deliverable + supersedes I12+I13 + unlocks I76 Strand A. (Q2) Option D paired-three-tier — AGENTIC_FRAMEWORK_LANDSCAPE extension + new SUBSTRATE_REGISTRY.csv + quarterly Tier-1 WIP cadence reports. (Q3) Option C hybrid — shape decisions ratified at I84 P4 + execution decisions deferred to each owning initiative's P0.
- **Close-out**: P0 (this commit lands the charter package).
- **Cross-references**: master-roadmap §1 + §2 + §3 + §10.

## D-IH-84-B — AKOS substrate-baseline-choice

- **Question**: Does AKOS stay on `OpenClaw` (Holistika-internal wrapper) as its substrate baseline, migrate toward Cursor-SDK-backed runtime, or operate hybrid (Cursor SDK as frontend agent-execution runtime + OpenClaw as policy + observability layer)?
- **Owner**: Founder + System Owner + Tech Lead.
- **Status entering**: proposed (substantive ratification depends on P1 audit dossier evidence + P3 §7 OpenClaw / LlamaIndex / Cursor-SDK retrospective + P4 batched ratification).
- **Ratified**: 2026-05-17 inline-ratify P4 batched gate; operator delegated craft per inline-ratify-craft Principle 6 + executive-call-per-operator-delegation recovery posture. Operator framing verbatim: *"craft this with your best expertise and our best tech and knowledge to govern this whole process and make the cursor sdk part as retractable as possible. our end goal is to fully govern our own space. even though we are not into model training we want to govern our applications and its infrastructure as soon as we can. that's why a deep llamaindex or similar infrastructure is our end goal when we know how to wire maintain upgrade adapt and build everything ourselves. I trust you can browse our context and intent to craft the best solution"*.
- **Decision**: **B5 — Bridge-with-strict-retractability + deep-self-owned-substrate as strategic endgame** (novel framing surfaced at P4 from operator delegation; encoded as `decision_source: agent_executive_call_per_operator_delegation` per `inline-ratify-craft/SKILL.md` Principle 6).
- **Architecture** (the craft the operator delegated):
  - **Tactical layer (today through 2026-Q4)**: B3-shaped hybrid — Cursor SDK MAY serve as a frontend agent-execution surface AND OpenClaw thin-adapter remains the policy + observability + provider-abstraction backend. The Cursor SDK surface is governed by an **explicit retractability architecture**:
    - All Cursor-SDK-specific code paths sit behind a single integration boundary (proposed at `akos/cursor_sdk_adapter.py` or equivalent; not minted in this commit; future I-NN charter).
    - The boundary contract is the **same provider interface that `akos/model_catalog.py` already implements** — no Cursor-SDK-specific types leak into AKOS-core modules (`akos/api.py`, `akos/runpod_provider.py`, `akos/policy.py`, etc.).
    - Any operator-facing capability achievable via Cursor SDK MUST also be achievable via the OpenClaw thin-adapter path (parity is the retractability gate). If a capability is Cursor-SDK-only, it does not ship.
    - No Cursor-SDK-specific data persists in canonical CSVs or Supabase mirrors (no `cursor_sdk_*` columns; no Cursor SDK identifiers in `SUBSTRATE_REGISTRY.csv` rows except as substrate row metadata in the existing `aic_pattern_role` column — which IS retractable since changing the row value to `not-applicable` is a one-CSV-edit operation).
    - Vendor-license + ToS exposure is contained: any Cursor SDK use requires the ADVOPS engagement framework (R-IH-84-NEW-ADVOPS) to clear EU AI Act provider-vs-deployer classification + IP-indemnity carve-out review before binding (gates exposed in `advops-engagement-scoping-2026-05-17.md`).
  - **Strategic layer (2026-Q4+ trajectory)**: AKOS substrate evolves toward **deep self-owned infrastructure** — LlamaIndex (or a successor open-source substrate of equivalent depth) as the orchestration anchor, surrounded by Holistika-authored adapters + policy gates + observability + provider abstractions. The criterion for "we know how to wire / maintain / upgrade / adapt / build everything ourselves" becomes the strategic-readiness gate. Cursor SDK reverts to optional operator-DX layer (or is fully retracted) once the deep self-owned substrate is operationally mature.
  - **The retractability axiom is the binding architectural principle**: every Cursor-SDK integration decision passes through "can we remove this in one sprint and degrade to OpenClaw-only?" If no, the integration does not ship. This axiom makes B5 distinct from a naive B3 — B3 has no explicit retractability gate; B5 makes retractability a first-class architectural concern.
- **Why B5 rather than B1 / B2 / B3 / B3-conditional / B-defer**:
  - **B1** (stay-OpenClaw) misses the Cursor 3 Glass operator-DX capability flagged by the founder 2026-05-16 as competitive window — discards a tactical lever the operator wants captured.
  - **B2** (migrate-Cursor-SDK) directly violates the operator's self-governance principle ("we want to govern our applications and its infrastructure"); vendor lock-in to Anysphere is the opposite of "fully govern our own space"; rejected on principle.
  - **B3** (vanilla hybrid) lacks the explicit retractability architecture; sets up a future migration cost when the strategic-endgame trigger fires. B5 closes that gap by encoding retractability as a first-class architectural axiom from day one.
  - **B3-conditional** (defer binding until ADVOPS clears) was a procedural option, not an architectural option; ADVOPS engagement is now in scope as `advops-engagement-scoping-2026-05-17.md` (R-IH-84-NEW-ADVOPS); B5 absorbs the ADVOPS-gate behavior into its tactical-layer integration discipline without deferring the architectural ratification.
  - **B-defer** (defer to next quarterly cycle) was rejected because I76 / I74 / I83 / I82 are blocked on this; the deferral cost compounds.
- **Substrate-registry encoding**: existing rows `SUBS-PATTERN-OPENCLAW-THIN-ADAPTER` (B1 anchor; remains in-production) + `SUBS-PATTERN-HYBRID-CURSOR-OPENCLAW` (B3/B5 anchor; flips status from `forecasted` to `pilot` upon next audit cycle when first integration ships; deferred to I85 candidate). A new pattern row `SUBS-PATTERN-DEEP-SELF-OWNED-LLAMAINDEX-CENTRIC` representing the strategic endgame is forward-charter (operator-pending tranche) — not minted in this commit because the architectural shape is more aspirational than concrete in 2026-Q2; mints when the deep-self-owned-substrate architecture clarifies, likely as part of an I85+ scope.
- **Close-out**: P4 batched inline-ratify gate (this entry).
- **Cross-references**: [`SUBSTRATE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) L4 (LlamaIndex strategic-endgame anchor) + L17 (OpenClaw thin-adapter tactical anchor) + L18 (Cursor-OpenClaw hybrid forecasted pattern); [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) §4 principle 1 (methodology-portability non-negotiable) + §4 principle 2 (incremental evolution over discontinuous migration) — B5 honors both principles; [`regulatory-tos-forecast.md`](../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) §6 + §7 (ADVOPS engagement); [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) §1 OpenClaw row (tactical anchor); founder framing 2026-05-17 P4 verbatim above.

## D-IH-84-C — AIC framing F1-F5 binding choice (closes I76 C-76-1)

- **Question**: Which framing does the AIC pattern adopt — F1 supervised sub-agents (Cursor-style), F2 peer companions (CrewAI-style), F3 ad-hoc dispatchers (LangGraph-style), F4 single-agent rich-tools (Claude Code-style), or F5 hybrid per-task?
- **Owner**: Founder + System Owner.
- **Status entering**: proposed (the C-76-1 conundrum I76 candidate was waiting for; per [`i76-madeira-elevation.md`](../_candidates/i76-madeira-elevation.md) §2: *"deliberately not pre-committing to one because the operator explicitly asked for outside research first"*).
- **Ratified**: 2026-05-17 inline-ratify P4 batched gate.
- **Decision**: **F5 — Hybrid; per-task operator picks**.
- **Rationale** (per inline-ratify-craft Principle 2 — recorded inline):
  - Preserves the I76 candidate's F1-F5 framing as a choice-surface rather than collapsing to a single binding — matches the operator's actual workflow where some tasks are supervised (F1 — multi-agent ratification chains), some are peer (F2 — pair-design conversations), some are dispatcher-shaped (F3 — KiRBe-class ingestor pipelines per D-IH-84-E narrowing), and some are single-agent-rich-tools (F4 — Cursor IDE itself + Madeira-as-method).
  - Coupling with D-IH-84-B B5: the retractability-with-self-governance principle naturally accommodates F5 because the hybrid substrate exposes multiple agentic patterns through the same provider abstraction — F5 is the agentic-pattern analog of B5's substrate-pattern hybrid posture.
  - Substrate-registry encoding: `SUBSTRATE_REGISTRY.csv` `aic_pattern_role` column values across the 18 rows confirm F5 is supportable — supervisor (Cursor SDK + OpenAI Agents SDK), peer (CrewAI + AG2), dispatcher (LangGraph + LangChain), single-agent-rich-tools (Claude Code SDK + VercelAI SDK), not-applicable (LlamaIndex + Ollama + Groq + Letta) are all currently in inventory; no single F1-F4 choice can be enforced without rejecting half the substrates the operator already uses.
  - I76 P0 receives a clean F5 ratification and is free to focus on **per-pattern instantiation** decisions (which task-classes default to F1 vs F2 vs F3 vs F4 in the operator's day-to-day) rather than the meta-decision of which single framing to adopt.
- **Close-out**: P4 batched inline-ratify gate (this entry); ratified row writes back to [`i76-madeira-elevation.md`](../_candidates/i76-madeira-elevation.md) §2 + §6 as **D-IH-76-A pre-ratification** at P5 cascade (cross-area-unlock-handoff report).
- **Cross-references**: I76 candidate §2 + §3 Strand A + Strand C; [`SUBSTRATE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) `aic_pattern_role` column across all 18 rows; [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) §1 (AIC framing question is structurally different from substrate question + LLM-choice question; F5 preserves the orthogonality).

## D-IH-84-D — MADEIRA productization shape (closes I74 C-74-3)

- **Question**: Does MADEIRA ship in productized form as (a) library-only (`@holistika/madeira-agent` consumed by external LLM-stack), (b) agent-only (hosted-MADEIRA-as-service), or (c) hybrid library + agent platform?
- **Owner**: Founder + Brand Manager + Tech Lead.
- **Status entering**: proposed.
- **Ratified**: 2026-05-17 inline-ratify P4 batched gate.
- **Decision**: **D3 — Hybrid: library for technically-mature customers + hosted agent for less-technical customers**.
- **Rationale** (per inline-ratify-craft Principle 2 — recorded inline):
  - Preserves market-segmentation flexibility: library entry-point (`@holistika/madeira-agent`) lowers customer-acquisition friction for the technically-mature customers who already have an LLM stack and prefer composition; hosted-agent path captures premium revenue from less-technical customers who want a managed experience.
  - Maps cleanly to **both** TRIGGER-1 (MADEIRA productized data-detached → hosted-agent path activates when ≥3 external orgs request it per [`MADEIRA-AKOS/STATUS.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md) §3) AND TRIGGER-2 (AKOS-as-library → library path activates when ≥2 external orgs request it). D1 / D2 each ignore one trigger.
  - Coupling with D-IH-84-B B5: the hybrid productization shape mirrors the hybrid substrate shape — library customers operate on their own substrate (any of the LlamaIndex-anchored open-source stack the B5 self-governance principle endorses); hosted-agent customers operate on Holistika's substrate (which is itself the B5 retractable-tactical + self-owned-strategic posture). The two layers are coherent.
  - Substrate-registry encoding: `SUBSTRATE_REGISTRY.csv` `madeira_productization_role` column already supports D3 by enumerating `backend-only` (Ollama / Groq for the hosted-agent path) + `library-import` (LangChain / LangGraph / LlamaIndex / CrewAI for the library path) + `agent-runtime` (OpenClaw + Cursor SDK + Claude Code SDK + OpenAI Agents SDK for the hosted-agent path) + `not-applicable` (LlamaIndex / Ollama / Groq / Letta in their pure-infra roles) — the enum was authored at P3a anticipating D3.
- **Close-out**: P4 batched inline-ratify gate (this entry); ratified row writes back to [`i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md) §4 as **D-IH-74-D pre-ratification** at P5 cascade.
- **Cross-references**: I74 candidate §2 + §3 + §6 spin-out triggers; [`MADEIRA-AKOS/STATUS.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md) §3 TRIGGER table; [`competitive-layer-positioning.md`](../../intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md) (Glean / Notion / Anthropic Projects positioning analysis — D3 captures both the library-for-developers and the hosted-platform-for-end-users market patterns the competitive landscape exhibits).

## D-IH-84-E — KiRBe framework-class-narrowing (closes I83 C-83-1 to 2-finalist)

- **Question**: Of the ~10 substrate candidates (the existing AGENTIC_FRAMEWORK_LANDSCAPE 8 + Cursor SDK + Claude Code SDK + OpenAI Agents SDK + LlamaIndex-as-currently-used + others surfaced by P1), which 2 finalists does KiRBe-ingestor narrow to for its P0 framework choice (per [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) C-83-1)?
- **Owner**: Tech Lead + System Owner.
- **Status entering**: proposed.
- **Rationale shape**: The narrowing is a SHAPE decision (which 2 are finalists + why); the EXECUTION decision between the 2 is deferred to I83 P0 owning initiative.
- **Ratified**: 2026-05-17 inline-ratify P4 batched gate + 2026-05-17 inline-ratify P4 follow-up gate (operator asked for narrowing-help; agent presented analysis weighted against D-IH-84-B B5 self-governance principle; operator ratified the recommended pair).
- **Decision**: **E1 — LlamaIndex-continue + LangGraph-workflow** (2 finalists; I83 P0 picks between them as the orchestration partner).
- **Rationale** (per inline-ratify-craft Principle 2 — recorded inline):
  - Best fit for KiRBe's INGESTOR role: KiRBe is fundamentally a pipeline-shaped service (data sources → vault), not a team-shaped service. LangGraph's dispatcher pattern (per [`SUBSTRATE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) L3 `aic_pattern_role=dispatcher`) matches the workflow-orchestration shape ingestors need; CrewAI's peer pattern (L6 `aic_pattern_role=peer`) is a weaker fit for a headless ingestion pipeline. Cursor SDK (L10 `license_class=proprietary-saas`) directly violates the D-IH-84-B B5 self-governance + retractability principle ratified above — ruled out for KiRBe long-term.
  - Both finalists are **open-source MIT** (license_class=open-source-mit) — aligned with B5 self-governance + retractability + no-vendor-lock-in long-term direction.
  - LlamaIndex anchor preserves KiRBe substrate continuity per [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/SUBSTRATE_LANDSCAPE_DOCTRINE.md) §4 principle 2 ("substrate continuity favors incremental evolution over discontinuous migration"). KiRBe is currently on LlamaIndex per founder framing 2026-05-16 — incremental upgrade path via LangGraph workflows is structurally lower-risk than discontinuous migration to a non-LlamaIndex orchestration.
  - LangGraph addition matches F3 dispatcher in the F5 per-task framing ratified at D-IH-84-C above — KiRBe's ingestor workflows are exactly the F3-shaped tasks the F5 hybrid accommodates without conflict.
  - Per past-poc-translation-matrix.md §5.3 explicit recommendation (the Tier-1 WIP analysis that informed the original framing in the SUBSTRATE_REGISTRY notes column at row L3 — *"KiRBe-narrowing-to-2-finalists candidate per D-IH-84-E (LlamaIndex-continue + LangGraph-workflow)"*).
- **The 2 finalists at I83 P0 decision-surface**:
  1. **LlamaIndex** (`SUBS-RUN-LLAMA-LLAMAINDEX`; framework-library-python; langchain-native; MIT; active) — the persistence + retrieval-augmented-generation anchor.
  2. **LangGraph** (`SUBS-LANGCHAIN-AI-LANGGRAPH`; orchestration-engine; langchain-native; MIT; active; pilot integration state) — the workflow-orchestration overlay on top of LlamaIndex (LangGraph natively composes with LlamaIndex via the langchain-native tool protocol).
  - I83 P0 may also choose to use BOTH in composition (LlamaIndex-for-retrieval + LangGraph-for-workflow-orchestration) — the "pick between them" framing should be read as "pick the primary orchestration anchor; the other one may compose alongside as needed." This composition pattern is the most likely I83 P0 outcome, but the SHAPE decision here is to narrow the universe to these 2 substrates.
- **Close-out**: P4 batched inline-ratify gate + P4 follow-up gate (this entry); ratified row writes back to [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) C-83-1 as the narrowed-to-2 choice at P5 cascade.
- **Cross-references**: I83 candidate §4 C-83-1; [`SUBSTRATE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) L3 (LangGraph row) + L4 (LlamaIndex row); [`past-poc-translation-matrix.md`](../../intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md) §5.3 (original recommendation source).

## D-IH-84-F — SUBSTRATE_REGISTRY.csv column shape

- **Question**: What is the 18-column schema for the new dimensional canonical?
- **Owner**: Data Architect + System Owner.
- **Status entering**: proposed (column-shape draft below; finalised at P2 canonical-CSV gate).
- **Proposed columns** (18; matches files-modified.csv 18-col precedent):
  1. `substrate_id` (PK; format `SUBS-<vendor-slug>-<name-slug>`).
  2. `name` (human-readable).
  3. `vendor` (corporate vendor name).
  4. `runtime_shape` (enum: `agent-sdk-typescript` / `agent-sdk-python` / `agent-sdk-rest` / `framework-library-python` / `framework-library-typescript` / `hosted-agent-platform` / `inference-provider` / `orchestration-engine`).
  5. `persistence_model` (enum: `ephemeral` / `session-scoped` / `persistent` / `cloud-managed`).
  6. `tool_protocol` (enum: `mcp` / `openai-functions` / `anthropic-tools` / `cursor-native` / `langchain-native` / `native-only`).
  7. `multi_tenant_ready` (bool).
  8. `license_class` (enum: `proprietary-saas` / `open-weights-model` / `open-source-mit` / `open-source-apache` / `open-source-other` / `commercial-license`).
  9. `status` (enum: `active` / `candidate` / `experimental` / `deprecated` / `forecasted`).
  10. `cost_class` (enum: `token-billed` / `seat-billed` / `gpu-hour-billed` / `bring-your-own-key` / `free-tier-only` / `hybrid`).
  11. `pricing_unit` (free text; e.g. "$0.25/M tokens + $40/seat/mo").
  12. `founder_principle_alignment` (enum: `principle-2.1` / ... / `principle-2.7` / `multiple` / `none`; FK to FOUNDER_METHODOLOGY_VERSIONING.md principles).
  13. `akos_integration_state` (enum: `in-production` / `pilot` / `forecasted` / `blocked` / `rejected`).
  14. `madeira_productization_role` (enum: `backend-only` / `library-import` / `agent-runtime` / `not-applicable` / `forecasted`).
  15. `aic_pattern_role` (enum: `supervisor` / `sub-agent` / `peer` / `dispatcher` / `single-agent-rich-tools` / `not-applicable`).
  16. `last_audit_date` (date).
  17. `audit_source_url` (string).
  18. `notes` (text).
- **Close-out**: P2 canonical-CSV gate (operator pause point).
- **Cross-references**: master-roadmap §4 P2 deep section; existing dimensional canonicals at [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/).

## D-IH-84-G — SUBSTRATE_LANDSCAPE_DOCTRINE.md authoring posture

- **Question**: How does the new Research-area canonical [`SUBSTRATE_LANDSCAPE_DOCTRINE.md`](../../references/hlk/v3.0/Admin/O5-1/Research/Methodology/canonicals/) frame substrate-as-discipline-of-disciplines?
- **Owner**: Holistik Researcher + KM Officer + System Owner.
- **Status entering**: proposed.
- **Posture**: Apply the People-DoD pattern (per [`akos-people-discipline-of-disciplines.mdc`](../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) Rule 3) recursively to Research-area. The argument: Research is itself a discipline-of-disciplines — the meta-discipline that audits which substrates (technical artefacts) earn the right to canonical status. SUBSTRATE_LANDSCAPE_DOCTRINE is the Research-area complement to the Tech-Lab side [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md), paired the way [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) (People why) is paired with AGENTIC_FRAMEWORK_LANDSCAPE.md (Tech-Lab how).
- **Close-out**: P6 inline-ratify gate.

## D-IH-84-H — Quarterly cadence + Research-area owner-activation interim

- **Question**: What is the cadence of the continuous substrate-audit discipline + who owns it pre-Research-Director hire?
- **Owner**: Founder + Research Director (or KM Officer interim).
- **Status entering**: proposed.
- **Default**: Quarterly cadence (per Q1 Option D framing — matches engagement-template-promotion cadence per [`i72-...` §Strand D.2 Process Catalog](../72-marketing-area-governance-and-persona-registry-expansion/master-roadmap.md)). Owner: KM Officer interim, with Founder co-sign per quarterly cycle, until Research Director hires (per [`i75-research-area-governance.md`](../_candidates/i75-research-area-governance.md) Strand C activation).
- **Close-out**: P6 inline-ratify gate.

## D-IH-84-I — Execution sequencing posture (parallel-with-I81 foundation track)

- **Question**: How does I84 execution sequence against the surrounding I8x cluster (I81 KB integrity foundation + I82 Capability doctrine + I83 KiRBe ingestor)?
- **Owner**: Founder + System Owner + PMO.
- **Ratified**: 2026-05-16 inline-ratify batched gate (Q1 + Q2 sequencing-strategy questions).
- **Decision**: Q1 Option B (Foundation-first parallel) + Q2 Option B (Opportunistic side-channel slotting). Concretely:
  - **Wave 1 (weeks 1-2)**: I81 P0+P1 (vault integrity baseline) runs **IN TRUE PARALLEL** with I84 P1 (substrate-landscape audit). Both pure desk-research; zero canonical-CSV conflicts.
  - **Wave 2 (weeks 2-4)**: I81 P2+P3 (layout migration + named-milestone schema mint) runs in parallel with I84 P2+P3 (SUBSTRATE_REGISTRY mint + AGENTIC_FRAMEWORK_LANDSCAPE extension). **Coordination point**: I81 P3 named-milestone schema ratification (`D-IH-81-H`) must land **before I84 P5 cross-area cascade** so the cascade uses native named-milestone form (e.g. `I76-AIC-FRAMING-RATIFY` not `I76 Strand A`). If I81 P3 slips, I84 P5 either waits or ships with magic-number references + migrates as part of I81 P3 Wave 1 migration commits.
  - **Wave 3 (weeks 4-5)**: I84 P4 batched ratification fires (D-IH-84-B/C/D/E) IN PARALLEL with I82 P0+P1 (doctrine prose + Talent activation gate).
  - **Wave 4-5 (weeks 5-9)**: I82 P2-P4 (consumes I81 P1 `kb-integrity-matrix-*`) → I83 P0 charter (both gates green: I82 P4 USE_CASE_ARCHIVE exists + I84 P4 D-IH-84-E framework narrowing ratified).
- **Side-channel slotting (Q2 Option B)**:
  - I77 (Impeccable brand-bridge refresh) fires this week as quiet 5-6h quick-win (zero cluster conflict).
  - I75 P0 charter at end of I84 P1 (so I75 governance frame is ready BEFORE I84 P6 mints the first Research-area canonical pair).
  - I76 P0 charter within 1 week of I84 P4 D-IH-84-C ratification.
  - I74 P0 charter within 1 week of I84 P4 D-IH-84-D ratification.
- **Rationale**: I81 vault integrity is foundational but its desk-research phase (P1) has **zero hard dependency** on I84; conversely I84 P1 substrate-research is **time-sensitive** (founder-directive 2026-05-16 named Cursor SDK beta competitive window). Sequential I81→I84 would erode 2-3 weeks of competitive intelligence for no integrity gain. Parallel-track preserves both.
- **Risk acceptance**: 2 cognitive contexts at peak during Wave 2 (I81 layout migration + I84 SUBSTRATE_REGISTRY mint). Mitigation: distinct role_owners per track (System Owner + Data Architect on I81 layout; Research Lead + Tech Lead on I84 substrate); per-initiative pause-record discipline keeps contexts auditable.
- **Close-out**: P0 (this commit lands the sequencing posture). Wave-1 launch confirmed when I81 P0 charter ships (next operator session per the 2026-05-16 plan).
- **Cross-references**: [`INITIATIVE_DEPENDENCIES.md`](../_templates/INITIATIVE_DEPENDENCIES.md) §3.7 "I81 + I84 parallel-track posture"; [`master-roadmap.md`](master-roadmap.md) §1 Operating story (parallel-track callout); 2026-05-16 inline-ratify Q1+Q2 batched gate.

## D-IH-84-CLOSURE — Initiative closure

- **Question**: I84 closure ratification.
- **Owner**: Founder + System Owner.
- **Close-out**: P8 closure UAT pause point.
