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
- **Options under consideration** (refined at P4 with P1 evidence):
  - **B1** — Stay on OpenClaw. Rationale: existing wrapper carries Holistika-specific policy + observability hooks; substrate-portability dimension (per AGENTIC_FRAMEWORK_LANDSCAPE.md §2 new dimension) is met by OpenClaw's thin-adapter design.
  - **B2** — Migrate to Cursor SDK runtime + abandon OpenClaw. Rationale: Cursor 3 "Glass" reframes the IDE as agent-execution-runtime with multi-agent + multi-repo + parallel-agent-fleet capabilities OpenClaw does not have. Cost: vendor lock-in to Anysphere; license/ToS exposure; OpenClaw's policy + observability hooks need re-implementation as Cursor SDK middlewares.
  - **B3** — Hybrid (recommended pending P1 evidence): Cursor SDK as the operator-facing agent runtime + OpenClaw retained as the policy + observability layer behind the SDK. Best-of-both; Cursor SDK frontend benefits + OpenClaw policy gates preserved. Cost: integration surface between the two layers needs explicit architecture; OpenClaw must be repackaged as middleware compatible with Cursor SDK's agent lifecycle.
- **Close-out**: P4 batched inline-ratify gate.
- **Cross-references**: [`AGENTIC_FRAMEWORK_LANDSCAPE.md` §1 OpenClaw row](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md); P1 audit dossier `agent-sdk-comparison-matrix.md`; P3 §7 retrospective; founder framing 2026-05-16 — *"why we're currently on OpenClaw instead of our own build like Madeira was in the LlamaIndex days like KiRBe still is"*.

## D-IH-84-C — AIC framing F1-F5 binding choice (closes I76 C-76-1)

- **Question**: Which framing does the AIC pattern adopt — F1 supervised sub-agents (Cursor-style), F2 peer companions (CrewAI-style), F3 ad-hoc dispatchers (LangGraph-style), F4 single-agent rich-tools (Claude Code-style), or F5 hybrid per-task?
- **Owner**: Founder + System Owner.
- **Status entering**: proposed (the C-76-1 conundrum I76 candidate was waiting for; per [`i76-madeira-elevation.md`](../_candidates/i76-madeira-elevation.md) §2: *"deliberately not pre-committing to one because the operator explicitly asked for outside research first"*).
- **Options under consideration** (per I76 §2 enumeration, validated against P1 audit findings):
  - **F1** — AICs as supervised sub-agents (Cursor `subagent_types` + Anthropic research-agents pattern).
  - **F2** — AICs as peer companions (CrewAI + AutoGen group-chat pattern).
  - **F3** — AICs as ad-hoc dispatchers (LangGraph tool-call subgraphs).
  - **F4** — No AICs; MADEIRA solo with rich tools (Claude Code-style single-agent).
  - **F5** — Hybrid; per-task operator picks.
- **Close-out**: P4 batched inline-ratify gate; ratified row writes back to [`i76-madeira-elevation.md`](../_candidates/i76-madeira-elevation.md) §2 + §6 as D-IH-76-A pre-ratification.
- **Cross-references**: I76 candidate §2 + §3 Strand A + Strand C; P1 audit `agent-sdk-comparison-matrix.md` (each SDK row gets an `aic_pattern_role` analysis attribute).

## D-IH-84-D — MADEIRA productization shape (closes I74 C-74-3)

- **Question**: Does MADEIRA ship in productized form as (a) library-only (`@holistika/madeira-agent` consumed by external LLM-stack), (b) agent-only (hosted-MADEIRA-as-service), or (c) hybrid library + agent platform?
- **Owner**: Founder + Brand Manager + Tech Lead.
- **Status entering**: proposed.
- **Options under consideration** (per [`i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md) §2 + the TRIGGER-1 / TRIGGER-2 distinction at [`MADEIRA-AKOS/STATUS.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md)):
  - **D1** — Library-only (`@holistika/madeira-agent` as Python + TypeScript packages; consumer brings their own LLM stack). Maps to TRIGGER-2 (AKOS-as-library) primarily.
  - **D2** — Agent-only (hosted MADEIRA SaaS service; Holistika operates the LLM stack on customer's behalf). Maps to TRIGGER-1 (MADEIRA productized data-detached) primarily.
  - **D3** — Hybrid library + agent platform (library for technically-mature customers; hosted agent for less-technical customers). Captures both triggers.
- **Close-out**: P4 batched inline-ratify gate; ratified row writes back to [`i74-brand-tooling-productization.md`](../_candidates/i74-brand-tooling-productization.md) §4 as D-IH-74-D pre-ratification.
- **Cross-references**: I74 candidate §2 + §3 + §6 spin-out triggers; [`MADEIRA-AKOS/STATUS.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/MADEIRA-AKOS/STATUS.md) §3 TRIGGER table; P1 audit `competitive-layer-positioning.md` (Glean / Notion / Anthropic Projects competitive positioning informs productization shape).

## D-IH-84-E — KiRBe framework-class-narrowing (closes I83 C-83-1 to 2-finalist)

- **Question**: Of the ~10 substrate candidates (the existing AGENTIC_FRAMEWORK_LANDSCAPE 8 + Cursor SDK + Claude Code SDK + OpenAI Agents SDK + LlamaIndex-as-currently-used + others surfaced by P1), which 2 finalists does KiRBe-ingestor narrow to for its P0 framework choice (per [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) C-83-1)?
- **Owner**: Tech Lead + System Owner.
- **Status entering**: proposed.
- **Rationale shape**: The narrowing is a SHAPE decision (which 2 are finalists + why); the EXECUTION decision between the 2 is deferred to I83 P0 owning initiative.
- **Close-out**: P4 batched inline-ratify gate; ratified row writes back to [`i83-ai-archivist-and-kirbe-ingestor.md`](../_candidates/i83-ai-archivist-and-kirbe-ingestor.md) C-83-1 as the narrowed-to-2 choice.
- **Cross-references**: I83 candidate §4 C-83-1; P1 audit `agent-sdk-comparison-matrix.md` (KiRBe-specific scoring on the `knowledge-base infrastructure` axis per AGENTIC_FRAMEWORK_LANDSCAPE §2 dimensions).

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
