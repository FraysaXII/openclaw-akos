---
evidence_id: past-poc-translation-matrix-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 §3.5 Option D execution
classification: intelligence (working-space; not canonical SSOT)
access_level: 5
language: en
target_initiatives: [INIT-OPENCLAW_AKOS-84]
target_strands:
  - I84 P1 Layer 1 Thread D (past-PoC translation matrix)
  - I84 P3 §7 (OpenClaw/LlamaIndex/Cursor-SDK retrospective)
  - I84 P4 D-IH-84-B (substrate baseline; past-PoC evidence informs migration cost)
  - I84 P4 D-IH-84-E (KiRBe framework narrowing; KiRBe-still-on-LlamaIndex is the load-bearing input)
confidence_level: A2
source_taxonomy: holistika-internal-canonical-cross-reference
---

# Past-PoC translation matrix — Tier-1 WIP (2026-Q2)

> **Scope.** Per [master-roadmap §3 P1 Layer 1 thread D](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) — retrospective synthesis of Holistika's prior agent / Madeira / KiRBe / R&L PoCs, translated to v3.1 substrate decisions. Five lineage rows: I10 closure + I11 active + I12+I13 superseded + KiRBe-still-on-LlamaIndex + R&L v2.7 framework references. Confidence higher than other Tier-1 threads (`A2` Holistika-internal-canonical-cross-reference) because the source material is repo-internal canonicals, not external vendor claims.

## 1. Audit scope and confidence posture

Five lineage rows analysed:

1. **I10 — Madeira eval hardening** (closed 2026-04-15): substrate-side artifacts + learnings translatable to v3.1.
2. **I11 — Madeira ops copilot** (active since 2026-04-15): the currently-active Madeira shape; substrate-touching surfaces.
3. **I12 + I13 — Madeira research request + follow-through** (superseded by I84 per master-roadmap §1): lineage shape + why I84 supersedes.
4. **KiRBe-still-on-LlamaIndex**: the parallel-track KiRBe substrate continuity per founder framing 2026-05-16; informs D-IH-84-E.
5. **R&L v2.7 framework references**: methodology-versioning + Holistika business-logic framework as substrate-decision-relevant historical foundation.

Confidence `A2` Holistika-internal-canonical-cross-reference (the source material is canonical SOPs, decision logs, master-roadmaps, vault structure — not external vendor claims). Some forward translation interpretations carry `B2` flag noted inline.

## 2. I10 — Madeira eval hardening (closed)

### 2.1 Lineage overview

| Attribute | Value |
|:---|:---|
| Initiative | [INIT-OPENCLAW_AKOS-10](../../planning/10-madeira-eval-hardening/master-roadmap.md) |
| Status | **closed** 2026-04-15 |
| Closure decision | D-IH-10-CLOSURE |
| Substrate touched | OpenClaw + Path B sandbox + LangChain (via OpenClaw upstream) + Langfuse v4 telemetry |
| Cursor plan source | `~/.cursor/plans/madeira_b+c_and_sota_eval.plan.md` (operator-side; not in repo) |

### 2.2 Substrate-relevant decisions (canonical D-IH-10-* rows)

| Decision | Substrate implication |
|:---|:---|
| **D-B (Path B SSOT)** — `agents.defaults.sandbox.mode` + `tools.exec.host: sandbox` in openclaw.json.example | Codified OpenClaw as the substrate-layer surface for sandbox-mode discipline; informed sandbox-mode posture (Docker Desktop on Windows; WSL2 alternate). The class-#1 failure observed in [`openclaw-observed-symptoms-2026-05-16.md`](openclaw-observed-symptoms-2026-05-16.md) is a direct consequence of this decision when Docker Desktop is unavailable. |
| **D-C (Path C research spine)** — `web_search` / `web_fetch` removed from orchestrator + architect; research spine = HLK MCP → optional graph → browser → escalation | Codified MCP-server-per-vendor as the integration-layer pattern; informs the AGENTIC_FRAMEWORK_LANDSCAPE §3 MCP posture matrix; competitive analysis vs Composio (per [`competitive-layer-positioning.md`](competitive-layer-positioning.md) §4.1) anchors here |
| **D-UI** — Remove `gateway.controlUi` from SSOT (upstream schema rejection) | Bootstrap-drift symptom: OpenClaw upstream schema changed; AKOS-side SSOT had to adapt. Pattern recurring concern for OpenClaw thin-adapter substrate per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 risk column |
| **D-EVAL** — Suite manifests under `tests/evals/suites/`; rubric mode; Langfuse v4 via `akos.telemetry.LangfuseReporter` | Codified Langfuse as the eval/observability substrate; informs `D-IH-84-B` baseline (any substrate choice must preserve Langfuse v4 integration) |

### 2.3 Translation to v3.1

Translatable learnings:

1. **Sandbox-mode is the operational-friction surface for OpenClaw.** Class #1 failure mode in observed-symptoms file = Docker Desktop dependency. Substrate-baseline choice should weigh this — B2 Cursor SDK has different sandbox model (Cursor-managed agent execution); B3 hybrid inherits Cursor-managed sandbox at frontend + OpenClaw policy at backend.
2. **Research-spine MCP pattern survives any substrate choice.** HLK MCP → graph → browser → escalation is substrate-agnostic; B1/B2/B3 all preserve this surface.
3. **Langfuse v4 telemetry integration is the load-bearing observability surface.** Per Cursor-rule [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract", any substrate must produce telemetry consumable by Langfuse. B1 maintains via OpenClaw built-in; B2 needs new integration; B3 inherits from B1 backend path.
4. **Eval harness pattern (rubric mode + Langfuse + categorical research_surface metadata) is the regression-prevention discipline that should apply at any substrate transition.** Recommend: pre-flight + post-flight eval suite run at any substrate migration (B1 → B3 or B1 → B2).

## 3. I11 — Madeira ops copilot (active)

### 3.1 Lineage overview

| Attribute | Value |
|:---|:---|
| Initiative | [INIT-OPENCLAW_AKOS-11](../../planning/11-madeira-ops-copilot/master-roadmap.md) |
| Status | **active** since 2026-04-15 |
| Substrate touched | OpenClaw (overlay) + prompts/overlays/OVERLAY_MADEIRA_OPS.md + config/agent-capabilities.json |
| Architecture | Overlay-only; Madeira never writes to canonical HLK assets |

### 3.2 Substrate-relevant decisions (canonical D-OPS-* rows)

| Decision | Substrate implication |
|:---|:---|
| **D-OPS-1** — Ops overlay on standard + full prompt variants only; compact tier unchanged | Codified prompt-tiering pattern; substrate must preserve tier-aware prompt loading. All three B1/B2/B3 candidates support this; not a differentiator |
| **D-OPS-2** — Permission truth in `config/agent-capabilities.json`; prompts do not add write tools | Codified RBAC-as-config-not-prompt pattern; per AGENTIC_FRAMEWORK_LANDSCAPE §3 MCP postures = Madeira ops sits at **suggest** posture by default. Cursor SDK's `subagent_types` model can preserve this with proper agent definition; OpenClaw preserves natively |
| **D-OPS-3** — `memory_store` for scratch artifacts deferred | Codified ephemeral-only persistence default; relevant to `C-76-3` (MADEIRA persistence shape) per [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §5 — if Letta substrate adopted, this decision revisited |
| **D-OPS-4** — Intent routing: semantic exemplars expanded; regex safety for admin_escalate + execution_escalate | Codified intent-routing pattern; substrate must support pluggable intent-classification; all three B-options compatible |

### 3.3 Translation to v3.1

Translatable learnings:

1. **Overlay-only architecture is substrate-portable.** I11's design (Madeira-as-overlay-on-base-prompts; permission-truth-in-config; no write tools added at prompt layer) ports cleanly to any substrate B1/B2/B3 because the design separates content (overlay), permissions (config), and runtime (substrate).
2. **Madeira at suggest posture (no decide) is the established pattern.** Per AGENTIC_FRAMEWORK_LANDSCAPE.md §3 posture matrix + [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) §4 cadence. Any substrate ratification must preserve this posture; Cursor SDK's `subagent_types` model supports posture-per-agent-type configuration aligned with this.
3. **Persistence deferral creates I76 C-76-3 entry point.** The I11 `D-OPS-3` deferred decision is the same conundrum I76 C-76-3 names. Letta substrate is the candidate library for resolving this; pairs with any F-framing (F1-F5).

## 4. I12 + I13 — Madeira research request + follow-through (superseded by I84)

### 4.1 Lineage overview

| Attribute | Value |
|:---|:---|
| Initiatives | [I12](../../planning/12-madeira-research-request/master-roadmap.md), [I13](../../planning/13-madeira-research-followthrough/master-roadmap.md) |
| Status | **superseded** by I84 per [master-roadmap §1 + §10](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) |
| Substrate touched | Vendor-handoff lineage (external research vendor; not directly substrate-touching) |
| Reason superseded | I12 + I13 were **vendor-handoff lineage** (commission external research from a vendor; integrate output). I84 supersedes with **internal Research-area continuous discipline** that produces dated quarterly substrate-audit reports |

### 4.2 What I84 replaces

| I12 + I13 pattern | I84 replacement |
|:---|:---|
| Single vendor-handoff cycle producing a research dossier | Continuous internal cadence per master-roadmap §3 P6 — `SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` (quarterly; paired runbook) |
| Output as one-time consumable document | Output as `SUBSTRATE_REGISTRY.csv` rows + `SUBSTRATE_LANDSCAPE_DOCTRINE.md` canonical (per master-roadmap §3 P2 + P6) |
| Vendor relationship management overhead | Research-area internal discipline; KM Officer + Founder interim ownership per `D-IH-84-H` until Research Director hires |
| Quality dependent on vendor selection + ToR scoping | Quality dependent on Research-area discipline + repeat cycles + AKOS-canonical-cross-reference confidence rating per [`confidence_levels.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md) |

### 4.3 Translation to v3.1

Translatable learnings:

1. **Single vendor-handoff produces brittle intelligence.** I12 / I13 lineage demonstrated that one-time external research doesn't keep pace with substrate-landscape velocity (the founder-named "Cursor SDK in beta" competitive window is exactly the kind of fast-moving evidence a single dossier loses currency on within months).
2. **The supersession is the right move.** I84's continuous-cadence pattern with SUBSTRATE_REGISTRY as the registry-shape persistence layer is structurally well-positioned to keep substrate intelligence current. The forward-charter benefit: each quarterly cycle ALTER's `SUBSTRATE_REGISTRY` rows in place rather than producing a fresh dossier that competes with prior ones.
3. **Continuous cadence implies a paired runbook.** Per [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1, the SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001 must ship with a paired `scripts/peopl_research_substrate_audit_cadence.py` runbook. This is master-roadmap §3 P6 deliverable.

## 5. KiRBe-still-on-LlamaIndex (parallel-track substrate continuity)

### 5.1 Lineage overview

Per founder framing 2026-05-16: *"why we're currently on OpenClaw instead of our own build like Madeira was in the LlamaIndex days like KiRBe still is"*. KiRBe is Holistika's RAG-shaped product that **never migrated off the LlamaIndex-era substrate pattern**; it runs the MADEIRA-direct pattern (per [`p1-substrate-landscape-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) §5.3) — build-your-own runtime on framework primitives.

### 5.2 Why KiRBe didn't migrate

Inferred from repo state + founder framing (confidence `B2`):
- **Product profile is RAG-shaped, not orchestration-shaped.** KiRBe's load-bearing axis is the KB infrastructure dimensions per AGENTIC_FRAMEWORK_LANDSCAPE.md §2 — LlamaIndex's RAG primitives are the natural fit; migration to an orchestration-layer substrate (OpenClaw, Cursor SDK) would add complexity without addressing KiRBe's actual product needs.
- **Per-tenant persistence model is mature on LlamaIndex.** KiRBe runs index-per-tenant + persistent vector storage; LlamaIndex's index-as-persistence model is well-suited.
- **No operational pressure to migrate.** Unlike AKOS-side where OpenClaw thin-adapter emerged from a deliberate governance posture (Holistika-internal wrapper; quarterly re-bless), KiRBe has stable customer relationships on the existing substrate; migration cost > benefit.

### 5.3 Translation to v3.1 + D-IH-84-E framework-narrowing

**D-IH-84-E** (KiRBe framework-class-narrowing to 2 finalists) per [`decision-log.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/decision-log.md):

| Candidate finalist | Rationale |
|:---|:---|
| **LlamaIndex-continue** | Status quo; zero migration cost; product-fit established; persistence model stable; team familiarity |
| **LangGraph-workflow** | Forward-charter alternative; adds stateful-workflow capability (per LangGraph's load-bearing differentiator); preserves LangChain-ecosystem-compat for retrieval primitives (LlamaIndex has LangChain adapters); migration cost moderate |

Two non-finalists (per scorecard P2 §4 finding #5 + this analysis):

| Non-finalist | Why excluded |
|:---|:---|
| **Cursor SDK** | Vendor-runtime; KiRBe doesn't need operator-facing UX layer (KiRBe IS a product, not a developer tool); WEAK governance fit (per P2 §2.1 D1 row); high lock-in (per P2 §2.4); no product-fit advantage |
| **OpenClaw** | Orchestration-shaped; doesn't add value to KiRBe's RAG-shaped workload; would force KiRBe to maintain two substrate dependencies (LlamaIndex for RAG + OpenClaw for orchestration) without product-justified need |

**Letta** is a potential addition layer (not a finalist substitute; complementary memory layer): if KiRBe's product roadmap adds per-user persistent memory (e.g., chat history across sessions), Letta is the canonical library candidate per P1 §4.5.

**Recommended P4 ratification for D-IH-84-E**: narrow to (LlamaIndex-continue + LangGraph-workflow) finalists. KiRBe P0 owning initiative picks between them based on product-roadmap fit. Letta tracked as potential complementary addition.

## 6. R&L v2.7 framework references

### 6.1 Lineage overview

The Research & Logic v2.7 folder ([`docs/references/hlk/Research & Logic/`](../../../references/hlk/Research%20%26%20Logic/)) carries Holistika's historical framework documents (pre-v3.0 vault):

- **`Holistika Research v2.7/Admin/` + `GTM/`** — v2.7-era methodology splits.
- **`Logic Change log.docx`** — predecessor to the current [`LOGIC_CHANGE_LOG.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/LOGIC_CHANGE_LOG.md).
- **`Holistika_ A Framework for Business Logic and Growth.docx`** — methodology framework foundation.
- **`Holistik_v1.3/`** — even earlier vault version (pre-v2.7).
- **`previous-project-for-product-owner-example-only/`** — historical client engagement reference.

The v2.7 → v3.0 vault transition was the Holistika methodology consolidation; v3.0 canonicals (`baseline_organisation.csv`, `process_list.csv`, `compliance/dimensions/*.csv`) supersede v2.7 docx documents per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md).

### 6.2 Substrate-relevance

The v2.7 references are **substrate-agnostic** — they are methodology + business-logic framework documents that any substrate can consume as reference material. They are NOT executable PoCs that need translating to v3.1 substrate.

However, they inform the **MADEIRA-as-methodology** posture per [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §1: *"MADEIRA is the founder method — the personal research-and-decision discipline that produces v3.x of the Holistika OS."* The v2.7 → v3.0 transition demonstrates that:

1. **Methodology evolves; substrate must accommodate evolution.** The v2.7 framework was authored in Word-format; v3.0 is Markdown-in-git + Pydantic canonicals + Supabase mirrors. The substrate transition (Word docs → git+CSV+Supabase) was driven by methodology maturity. Forward-charter implication: future methodology evolution (v3.1, v4.0) may require substrate evolution (e.g., graph-database mirrors per I76 / I88 future initiatives); substrate-choice at D-IH-84-B should not lock in a substrate that resists future methodology evolution.

2. **Format-portability is the load-bearing requirement.** v2.7 Word docs are preserved as reference-only because the content (methodology) outlasted the format (Word). The same will be true of v3.0 Markdown — the canonical content will outlast its representation. Substrate-choice at D-IH-84-B should preserve format-portability — OpenClaw + Cursor SDK + Hybrid all preserve Markdown-in-git; vendor-managed-state alternatives that pull canonicals into proprietary stores degrade this.

3. **The methodology framework is the differentiator.** Per [`competitive-layer-positioning.md`](competitive-layer-positioning.md) §2 — Glean / Notion AI / Anthropic Projects competitors don't own a methodology; Holistika does. The R&L v2.7 framework is the evidence that Holistika has been methodology-shaped from v1.3 onward. Substrate-choice should preserve methodology-shape; substrate that homogenises Madeira into a generic AI assistant erodes the differentiator.

## 7. Aggregate findings (4 observations)

1. **AKOS substrate continuity has been remarkably durable across vault generations (v1.3 → v2.7 → v3.0).** Each generation has preserved the methodology while migrating the substrate (Word → Markdown → CSV+Pydantic+Supabase). The pattern: **methodology is the source of truth; substrate is the implementation; substrate transitions are operationally costly but methodologically-preservable**. This pattern bears on D-IH-84-B: any chosen substrate should preserve methodology-portability through future vault generations.

2. **OpenClaw thin-adapter substrate emerged from deliberate governance posture, not technical necessity.** Per I10 D-B (sandbox mode + tools.exec.host) + I11 D-OPS-2 (permission truth in config) the OpenClaw substrate is engineered for governance. The sandbox-mode operational friction observed in [`openclaw-observed-symptoms-2026-05-16.md`](openclaw-observed-symptoms-2026-05-16.md) is a consequence of this design choice (Docker dependency is the price of sandbox isolation). **Translation**: B3 hybrid that preserves OpenClaw policy backend retains the governance discipline; B2 pure-Cursor-SDK migration loses it.

3. **KiRBe-still-on-LlamaIndex is structurally correct, not an oversight.** KiRBe's product profile (RAG-shaped) matches LlamaIndex's design; the absence of migration to OpenClaw reflects rational product-fit, not technical debt. **D-IH-84-E should narrow KiRBe candidates to LlamaIndex-continue + LangGraph-workflow finalists** (per §5.3 analysis); Cursor SDK + OpenClaw are not KiRBe-fit substrates.

4. **I12 / I13 supersession is methodologically sound.** Single vendor-handoff produces brittle intelligence; continuous Research-area discipline + registry-shaped persistence + paired runbook (per master-roadmap §3 P6) is the right replacement pattern. **Forward-charter**: the cadence-runbook pattern is a paired-SOP+runbook reference instance per [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1; future Research-area cadences (e.g., competitive-landscape, regulatory-landscape) can follow the same shape.

## 8. Implications for `D-IH-84-B` (substrate baseline) + `D-IH-84-E` (KiRBe narrowing)

The past-PoC analysis adds three considerations to the substrate-baseline ratification:

1. **Substrate-continuity track record favors OpenClaw retention (B1 or B3) over pure migration (B2).** AKOS substrate has been incrementally evolved across vault generations; B1/B3 preserve the OpenClaw substrate continuity; B2 is a discontinuity that loses governance-design accumulated in I10/I11. **Recommendation**: P4 ratification framing should explicitly weigh continuity-vs-discontinuity as a separate axis from the scorecard's 6 dimensions.

2. **Methodology-portability is a separate axis the scorecard did not explicitly score.** v1.3 → v2.7 → v3.0 evolution evidence shows substrate must preserve format-portability for methodology to evolve cleanly. **Recommendation**: surface this as a sub-dimension under "governance fit" (D1) in any scorecard refinement (Option B from the P3-entry inline-AskQuestion).

3. **KiRBe narrowing to LlamaIndex-continue + LangGraph-workflow is well-evidenced.** Per §5.3 analysis. **Recommendation**: D-IH-84-E P4 ratification can land with this narrowing as the proposed default; KiRBe P0 owning initiative ratifies the execution choice.

## 9. Cross-references

- [I84 master-roadmap](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) §3 P1 Layer 1 thread D — the deliverable contract.
- [I84 P1 audit report](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) — paired audit (Thread A scope; MADEIRA-direct pattern row §5.3).
- [I84 P2 scorecard](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) — scorecard dimensions; methodology-portability axis not explicitly scored (recommendation in §8 #2 above).
- [I10 master-roadmap](../../planning/10-madeira-eval-hardening/master-roadmap.md) — closed initiative; substrate-relevant decisions D-B / D-C / D-UI / D-EVAL.
- [I11 master-roadmap](../../planning/11-madeira-ops-copilot/master-roadmap.md) — active initiative; substrate-relevant decisions D-OPS-1/2/3/4.
- [I12 master-roadmap](../../planning/12-madeira-research-request/master-roadmap.md) — superseded by I84.
- [I13 master-roadmap](../../planning/13-madeira-research-followthrough/master-roadmap.md) — superseded by I84.
- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — §1 OpenClaw + LlamaIndex rows; §2 KB infrastructure dimensions; §3 MCP postures.
- [`openclaw-observed-symptoms-2026-05-16.md`](openclaw-observed-symptoms-2026-05-16.md) — operational evidence informing OpenClaw retention vs migration tradeoff.
- [`competitive-layer-positioning.md`](competitive-layer-positioning.md) §2 — Glean / Notion / Anthropic positioning; methodology-as-differentiator framing.
- [`regulatory-tos-forecast.md`](regulatory-tos-forecast.md) §4-§5 — Cursor SDK ToS + IP indemnity; informs B3 backend routing pattern.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) — People-side why; Madeira as named-role footnote.
- [`i76-madeira-elevation.md`](../../planning/_candidates/i76-madeira-elevation.md) §1 + §2 + §5 (C-76-3 persistence) — Madeira methodology-shape; AIC framings.
- [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 — paired SOP+runbook pattern; informs §4.3 #3.
- [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) — vault classification.
- [`confidence_levels.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/confidence_levels.md) — A2 confidence rating for canonical-cross-reference sourcing.

## 10. Provenance and confidence labels

Authored as Tier-1 WIP per master-roadmap §3 P1 thread D. Confidence `A2` (Holistika-internal-canonical-cross-reference) higher than other Tier-1 threads because source material is repo-internal canonicals (I10/I11/I12/I13 master-roadmaps, AGENTIC_FRAMEWORK_LANDSCAPE.md, PRECEDENCE.md, founder framing 2026-05-16 directive in I84 master-roadmap §1).

Some forward-translation interpretations carry `B2` flag noted inline (e.g., §5.2 "Why KiRBe didn't migrate" is inferred from repo state + founder framing).

Tier-1 WIP classification per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md). Not canonical until D-IH-84-E ratification at master-roadmap §3 P4 batched gate.
