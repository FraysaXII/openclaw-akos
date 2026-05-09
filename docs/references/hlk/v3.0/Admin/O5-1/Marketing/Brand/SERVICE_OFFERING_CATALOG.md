---
canonical: true
status: active
classification: canonical
access_level: 4
language: en
audience: operator + boilerplate authors + sales + advisors + investors
register: external (with internal sub-register annotations)
governance: D-IH-66-E (Branded House service matrix), D-IH-66-A (Branded House architecture)
created: 2026-05-08
linked_initiative: I66
linked_decisions:
  - D-IH-66-A
  - D-IH-66-B
  - D-IH-66-E
supersedes: docs/references/hlk/v3.0/Admin/O5-1/Marketing/services/* (informal scattered prose)
---

# Service Offering Catalog — the 6 × 3 matrix

This is the **canonical** Holistika service catalog. It is the SSOT for any external rendering of "what Holistika does", including the boilerplate `/services` page (P5), the `/manifiesto` entries, the deck "what we do" slides (P6), and the founder bio "current engagements" line (P6). Drift between this catalog and any external rendering is governed by the I66 P7 `validate_brand_vision_drift.py` gate.

The catalog is structured as a **6 × 3 matrix**:

- **6 service domains** (rows) — the substantive areas where Holistika applies its methodology.
- **3 delivery modes** (columns) — the operational arms (sub-marks) that deliver the work.

The matrix is intentionally rectangular: every cell is a valid offering. Empty cells are deliberate (the corresponding sub-mark does not deliver that domain), not gaps to be filled.

## The 6 service domains (rows)

Per D-IH-66-E, the six domains are the layered application of Holistika's methodology pillars (Process Engineering, Business Engineering, Factor Combination, Foresight) to recurring counterparty needs.

### 1. Process Engineering

The discipline of making operational processes legible, governed, and improvable. Includes process discovery (mapping the latent process from the team's actual behaviour, not the documented prose), process governance (encoding ownership / cadence / quality criteria into repeatable artefacts), and process improvement (instrumented, evidence-based change with rollback discipline).

**Counterparty signal**: "we know we have processes but they live in people's heads", "we keep re-doing the same kind of work and re-discovering the same problems", "every new hire takes [N] months to get productive because the system isn't legible".

**Internal-register anchor**: Process Engineering is the institutional memory of HLK's research methodology — it is what the founder applies to every counterparty engagement before any other work begins.

### 2. Business Engineering

The discipline of treating the business itself as an engineered system: financial flows, customer flows, operational flows, capability flows. Includes business model decomposition, unit economics modelling, GTM-system design, and the integration of those four flows into a coherent operating model.

**Counterparty signal**: "we're scaling but the unit economics get worse as we grow", "we hit a wall translating product traction into revenue", "we know what we sell but don't know what we are".

**Internal-register anchor**: Business Engineering is the application of CORPINT-research to the firm itself — same source-grading discipline, applied internally rather than to a counterparty.

### 3. Factor Combination

The discipline of identifying, isolating, and re-combining the operating factors of a counterparty's situation to surface non-obvious opportunities. Draws explicitly from systems thinking, second-order economics, and the academic literature on combinatorial innovation. Distinct from "strategy consulting" in that the output is an explicit combinatorial graph of factors, not a deck of conclusions.

**Counterparty signal**: "we know the pieces but can't see the picture", "every advisor gives us different advice and we can't reconcile them", "we need someone who will look at us as a system, not as a problem-list".

**Internal-register anchor**: Factor Combination is the methodology layer that produces the **research brief** (external register) from the **intelligence collection** (internal register).

### 4. Foresight

The discipline of mapping plausible futures, near and far, with explicit reasoning chains. Includes scenario development, weak-signal detection, technology forecasting, regulatory forecasting, and the integration of those into actionable near-term decisions ("if you believe X, here's the no-regret move").

**Counterparty signal**: "we need to make a 5-year decision but only see 18 months out", "we can't tell if [emerging trend] is real or hype", "we keep getting blindsided by adjacent moves".

**Internal-register anchor**: Foresight is the application of source-graded intelligence collection to forward-looking questions, with explicit reliability disclosure on each scenario.

### 5. Tech Lab Integrations

Engineering work that operationalises the above four. Builds the technical artefacts (infrastructure, data plumbing, agent systems, evaluation pipelines) that take a methodology engagement from "deck" to "running system". Includes Holistika's own product stack (MADEIRA, KiRBe, ENVOY, InfraMonitor, Financial Analyst) plus bespoke client-side technical work.

**Counterparty signal**: "the strategy lands but the execution doesn't have the technical scaffolding to hold it", "we have the tools but they don't speak to each other", "we need an AI / agent / data system but don't want a vendor — we want a partner".

**Internal-register anchor**: Tech Lab Integrations is the engineering arm of the methodology — the layer where the research output becomes a system that runs in production.

### 6. Capability Building & Operator Coaching

Knowledge-transfer work. Where the previous five domains deliver outcomes for the counterparty, this domain transfers the underlying methodology to the counterparty's own team. Includes operator workshops, methodology coaching, embedded-advisor engagements, and structured handoff packages.

**Counterparty signal**: "we don't want to keep paying you for this — teach us to do it ourselves", "we have a team but they need methodology depth", "we want this capability internally for the long term".

**Internal-register anchor**: Capability Building is the controlled diffusion of Holistika's research methodology — chosen carefully (some methodology surface stays proprietary; some is intentionally open).

## The 3 delivery modes (columns)

Per D-IH-66-A and D-IH-66-B, the three operational arms are the sub-marks that deliver the work. Each sub-mark is an **operating mode**, not a separate company; all three are delivered under the single legal entity `Holistika Research SL`.

### A. Holistika R&S — Research & Strategy

The **research-first**, **strategy-first** delivery mode. Engagements are structured around the methodology pillars, deliver a research brief / strategy document / decision memo as the primary artefact, and operate at investor, advisor, and senior-operator counterparty levels.

**Voice tier**: Tier-1 (operator-led, evidence-grounded, specific). Per `BRAND_REGISTER_MATRIX.md` and `BRAND_ARCHITECTURE.md` §"Sub-mark voice tier".

### B. Think Big — Strategy Operationalisation

The **operations**, **growth**, and **GTM-execution** delivery mode. Engagements take a strategy or research brief (often from a prior R&S engagement, sometimes from the counterparty's existing thinking) and operationalise it: GTM systems, marketing operations, sales operations, growth experiments. Distinct from R&S in that the deliverable is an **operating system**, not a memo.

**Voice tier**: Tier-2 (warmer, action-oriented, growth-fluent). Per `BRAND_ARCHITECTURE.md` §"Sub-mark voice tier".

### C. HLK Tech Lab — Engineering & Technical Integration

The **engineering** delivery mode. Engagements build the technical artefacts: infrastructure, data systems, agent / AI integrations, evaluation pipelines, custom Holistika product implementations (MADEIRA, KiRBe, ENVOY). Distinct from Think Big in that the deliverable is a **technical system that runs**, not an operational playbook.

**Voice tier**: Tier-2 (technical, precise, AI-fluent). Per `BRAND_ARCHITECTURE.md` §"Sub-mark voice tier".

## The 6 × 3 matrix

External-register catalog. Internal-register annotations are in italics inside each cell.

| Domain ↓ × Mode → | A. Holistika R&S | B. Think Big | C. HLK Tech Lab |
|:---|:---|:---|:---|
| **1. Process Engineering** | Process discovery briefs; methodology-led process audits; institutional-memory artefacts. *Internal: structured-elicitation engagements.* | Process operationalisation; SOP rollout; cadence / governance / quality-criteria deployment in the operator's team. *Internal: bridging research-brief outputs to live ops.* | Process automation; workflow engines; agent-driven repetitive-task execution; instrumented process metrics. *Internal: technical scaffolding under the methodology layer.* |
| **2. Business Engineering** | Business-model decomposition; unit-economics modelling; GTM-system design briefs. *Internal: applying CORPINT-research to the firm itself.* | GTM system implementation; marketing-ops + sales-ops integration; growth experiment design. *Internal: external-register translation of internal "intelligence collection on ourselves".* | Financial-systems integration; data-pipeline plumbing; revenue-instrumentation; agent-driven financial-analyst surfaces (Financial Analyst 2026 product). |
| **3. Factor Combination** | Combinatorial decision briefs; second-order risk analyses; contradiction-reconciliation memos. *Internal: research-brief output of intelligence-collection engagements.* | Strategy-into-portfolio operationalisation; multi-channel orchestration; capability-mix experimentation. | Combinatorial-graph software surfaces; agent-driven scenario simulators; Knowledge Repository integrations (KiRBe product). |
| **4. Foresight** | Scenario briefs; weak-signal monitoring; regulatory / technology forecasts. *Internal: forward-looking source-graded intelligence reports.* | — *(empty cell — Think Big does not deliver pure-foresight work)* | Foresight automation: weak-signal monitoring agents; regulatory-change watchers; agent-driven scenario surfaces. |
| **5. Tech Lab Integrations** | — *(empty cell — R&S does not deliver pure-engineering work)* | Tech-led growth experiments; technical-marketing systems; analytics-stack integration. | MADEIRA / KiRBe / ENVOY / InfraMonitor / Financial Analyst implementations; bespoke AI / agent integrations; data infrastructure; evaluation pipelines. |
| **6. Capability Building & Operator Coaching** | Methodology workshops; embedded-advisor engagements; operator coaching at the strategy level. | Operator coaching at the operational level; GTM-systems training; growth-team enablement. | Engineering-team enablement; AI / agent literacy; methodology-to-tooling translation training. |

## How counterparties enter the matrix

Per D-IH-66-E, the catalog is **substrate, not menu**: counterparties enter the matrix at one cell (the cell that matches their declared need) and almost always end up engaging across multiple cells. The boilerplate `/services` page (P5) renders this as a navigable matrix, not a list of disconnected service items.

The 5 representative paths through the matrix:

1. **Investor-thesis path**: Cell 2A → cell 3A → cell 6A. Investor-stage business engineering (model + unit economics) → factor combination on the path-to-scale → operator coaching for the funded round.
2. **SME-operator path**: Cell 1A → cell 1B → cell 5C. Process discovery → process operationalisation → workflow-automation tech.
3. **Foresight-led path**: Cell 4A → cell 3A → cell 4C. Scenario brief → factor combination on the future state → foresight automation surfaces.
4. **Tech-led path**: Cell 5C → cell 1C → cell 6C. Technical integration → process automation → engineering-team enablement.
5. **Hybrid (most common)**: Multi-cell engagement chartered as a phased program with explicit cell-to-cell transitions documented in the engagement playbook (P6).

## Pricing posture (external register)

The external register treats engagements as **scoped** (fixed-price, fixed-duration, fixed-deliverable) or **embedded** (continuous-presence, retained-capability) or **transformational** (large multi-cell programs). Pricing is **never** quoted in this catalog — pricing lives in per-engagement proposal templates (P6).

Internal-register: the SOP-OPS_PRICING_FRAMEWORK_001 (deferred to a future I-NN) governs how scope translates to internal cost-recovery + margin discipline. Out of scope for I66.

## Cross-references

- [`BRAND_ARCHITECTURE.md`](BRAND_ARCHITECTURE.md) — the Branded House diagram + sub-mark voice tier table that this catalog elaborates.
- [`BRAND_VISION.md`](BRAND_VISION.md) — the methodology pillars (Process Engineering, Business Engineering, Factor Combination, Foresight) that anchor rows 1-4.
- [`BRAND_BASELINE_REALITY_MATRIX.md`](BRAND_BASELINE_REALITY_MATRIX.md) — per-audience register; this catalog uses the external register only.
- [`BRAND_VOICE_FOUNDATION.md`](BRAND_VOICE_FOUNDATION.md) — voice rules for any rendering of this catalog.
- I66 P5 deliverable: boilerplate `/services` rewrite renders this catalog as a navigable matrix.
- I66 P6 deliverable: engagement playbook governs the 5 representative paths above.
- I66 P3 deliverable (this phase): introduces the 16 process_list rows that **operationalise** this catalog (each row maps to one or more cells).
- D-IH-66-E in `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md`.
