---
evidence_id: regulatory-tos-forecast-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 §3.5 Option D execution
classification: intelligence (working-space; not canonical SSOT)
access_level: 5
language: en
target_initiatives: [INIT-OPENCLAW_AKOS-84]
target_strands:
  - I84 P1 Layer 1 Thread C (regulatory + ToS)
  - I84 P4 D-IH-84-B (AKOS substrate-baseline-choice; regulatory exposure informs vendor risk)
  - I84 P4 D-IH-84-D (MADEIRA productization shape; per-jurisdiction ToS informs library-vs-agent)
  - ADVOPS (legal / fiscal adviser engagement — cross-area handoff per akos-adviser-engagement.mdc)
confidence_level: B2
source_taxonomy: holistika-internal-research-synthesis
---

# Regulatory + ToS forecast — Tier-1 WIP (2026-Q2)

> **Scope.** Per [master-roadmap §3 P1 Layer 1 thread C](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) — four regulatory + ToS topics whose 2026-2027 trajectory directly affects the substrate-baseline ratification at `D-IH-84-B`. The analysis is **forecast**, not legal advice — formal legal review by Holistika's Legal Counsel + jurisdictional fiscal advisers (per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) ADVOPS workflow) is the canonical pathway for any binding interpretation. This dossier surfaces the **shape** of the regulatory risks so the P4 ratification weighs them; it does not substitute for ADVOPS engagement.

## 1. Audit scope and confidence posture

Four regulatory topics per master-roadmap §3 P1 thread C list:

1. **EU AI Act provider-vs-deployer 2026 enforcement** — codified obligations differ markedly between AI providers (e.g., OpenAI, Anthropic) and AI deployers (e.g., Holistika using an agent-SDK substrate); enforcement enters teeth phase 2026-Q3+.
2. **GDPR-as-SaaS DPA cascading** — when a SaaS vendor (e.g., Cursor, Anthropic, OpenAI) processes EU personal data on behalf of Holistika, the GDPR Article 28 DPA cascades through the agent runtime; transcripts that quote AKOS canonicals containing personal data inherit the obligation.
3. **Cursor MSA evolution forecast** — Anysphere's Master Services Agreement and Cursor SDK terms are evolving rapidly through the 2025-2026 product growth phase; the SDK ToS specifically is beta-state and likely to change materially before GA.
4. **IP-indemnity carve-outs across SDKs** — frontier LLM providers (OpenAI, Anthropic, Google) ship varying degrees of customer indemnification against IP infringement claims arising from model output; the indemnity scope materially affects the safety profile of using a given substrate for customer-facing prose.

Confidence `B2` throughout. **All four topics warrant formal legal review** at the master-roadmap-grade P1 + before any binding D-IH-84-B ratification. ADVOPS engagement is the canonical surface per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc); this dossier is shape-evidence, not advice.

## 2. EU AI Act provider-vs-deployer 2026 enforcement

### 2.1 The regulatory shape

The EU AI Act (Regulation (EU) 2024/1689) entered into force 2024-08-01 with staggered application dates `[ext]`:

- **2025-02-02**: prohibitions on banned AI practices (subliminal manipulation, social scoring, real-time biometric ID in public spaces, etc.) `[ext]`.
- **2025-08-02**: GPAI (general-purpose AI) provider obligations begin (transparency, training-data summaries, copyright compliance) `[ext]`.
- **2026-08-02**: high-risk AI system obligations begin (conformity assessment, risk management, data governance, transparency, human oversight, post-market monitoring) `[ext]`.
- **2027-08-02**: full application across all categories `[ext]`.

The Act distinguishes:
- **Provider** — entity that develops AI or places it on the market under its own name (e.g., OpenAI placing GPT-4 on the market; Anthropic placing Claude on the market).
- **Deployer** — entity that uses an AI system under its own authority (e.g., Holistika deploying Madeira built on Cursor SDK or OpenClaw).

### 2.2 Holistika's likely classification

Holistika's typical activity profile vis-à-vis the substrates:
- Using LLMs (Claude, GPT, Llama via Groq, etc.) → **deployer** of GPAI.
- Wrapping LLMs in agent-runtime (OpenClaw / Cursor SDK / etc.) for own use → **deployer** of an AI system.
- Productizing Madeira as B2B SaaS for clients to use → **provider** of an AI system (under Holistika's name); if classified as high-risk under Annex III, full provider obligations apply.

Per the founder-directive 2026-05-16 productization scope, the most exposed scenario is the **D2 (hosted-agent) productization shape** under D-IH-84-D — Holistika becomes a provider of an AI system used by external organisations. Annex III high-risk categories most relevant: (a) employment/recruitment if Madeira ever screens CVs (out-of-scope today; out-of-scope forecasted); (b) access to essential services if Madeira powers customer-facing finance / health / education flows (out-of-scope today; potential forecasted via KiRBe vertical expansion).

### 2.3 Substrate implications

| Substrate choice | EU AI Act exposure | Mitigation |
|:---|:---|:---|
| **OpenClaw thin-adapter (B1)** | Deployer-only (Holistika never becomes provider unless productizing). Lowest baseline exposure. | Documented internal AI policy (data governance, oversight); deployer obligations apply only when EU operators use the system. |
| **Cursor SDK (B2)** | Deployer; same as B1 if Cursor SDK is the runtime. Anysphere as the AI system provider carries provider-side obligations. | Same as B1. Additional ToS review (Cursor SDK ToS likely shifts liability to deployers; see §4 below). |
| **Hybrid (B3)** | Same as B1 + B2; deployer-only at this layer. | Same as B1. |
| **D2 (MADEIRA-as-SaaS)** | **Provider** obligations trigger. If classified high-risk, full Annex III conformity assessment + data governance + technical documentation + human oversight + post-market monitoring required. Substantial compliance overhead. | Avoid Annex III high-risk classifications (don't ship for employment / essential-services / law-enforcement use); document the system per Article 11; appoint authorised representative if non-EU establishment (Holistika is non-EU; an EU rep would be needed). |
| **D1 (MADEIRA-as-library)** | Lower provider exposure since the library shape disclaims being an AI system per se; consumer integrates it into their own system. **However**: GPAI obligations may still cascade if library is considered a GPAI component. Likely intermediate exposure. | Document library outputs + capabilities + risks per GPAI transparency rules; require consumers to handle deployer obligations on their integrated systems. |

### 2.4 Forecast (2026-2027)

- **2026-08-02 high-risk enforcement begins**: enforcement-capacity ramp-up phase; significant administrative friction expected; member state implementation varies.
- **2027-08-02 full application**: meaningful penalties begin (up to 7% global turnover for prohibitions; 3% for high-risk obligations) `[ext]`.
- **Frontier model provider behavior**: GPAI providers (OpenAI, Anthropic, Google) likely tighten ToS provisions shifting deployer obligations onto customers; pre-emptive engineering investment in transparency + governance documentation is recommended.

### 2.5 ADVOPS recommendation

Formal engagement of EU AI Act counsel before D2 productization ratification (per `D-IH-84-D` analysis). Specifically: (a) Annex III applicability analysis for any Madeira customer-facing flow; (b) authorised-representative requirements for Holistika as non-EU-established provider; (c) integration with existing GDPR Article 28 DPAs per §3 below.

## 3. GDPR-as-SaaS DPA cascading

### 3.1 The regulatory shape

Under GDPR Article 28 `[ext]`, when a controller (Holistika) uses a processor (e.g., Cursor backend, OpenAI API, Claude API) to process personal data, a Data Processing Agreement (DPA) is required. The DPA specifies:
- Purpose + duration + categories of personal data processed.
- Sub-processor list + sub-processor change notification rights.
- Security measures (technical + organisational).
- Data deletion + return at end of processing.
- Audit rights.

When Holistika productizes Madeira (`D-IH-84-D` D2 or D3), Holistika itself becomes a processor for its customers (controllers); the DPA cascades from customer ↓ Holistika ↓ Cursor / OpenAI / Anthropic (sub-processors).

### 3.2 Cascading shape per substrate

```
Customer (controller)
  └→ Holistika (processor; via Madeira)
       └→ Cursor / Anthropic / OpenAI (sub-processor; via SDK)
            └→ Anyone they themselves sub-process to
```

Each layer requires:
- A DPA in place upstream (customer → Holistika DPA at minimum).
- Approval to add or change the layers downstream (customer typically retains right to object to sub-processor changes).
- Notification cascade when sub-processor changes; if a customer objects, Holistika must either replace the sub-processor or release the customer from the contract.

### 3.3 Substrate implications

| Substrate choice | DPA cascading complexity | Notes |
|:---|:---|:---|
| **B1 OpenClaw + LLM provider** | Simple — Holistika ↔ LLM provider DPA only; no Cursor / Anysphere layer | Lowest DPA complexity |
| **B2 Cursor SDK** | Higher — Holistika ↔ Anysphere ↔ Anysphere's LLM sub-processors. Cascade is one layer deeper. | Anysphere must publish + maintain sub-processor list + DPA |
| **B3 Hybrid** | Same as B2 | OpenClaw policy backend doesn't change DPA shape; the data-processing layer is the Cursor SDK frontend |
| **D2 SaaS Madeira** | Holistika as processor for customers; cascades downward from there | Adds customer-↔-Holistika DPA layer on top of Holistika-↔-substrate DPA |

### 3.4 Forecast

- **Cursor / Anysphere DPA maturity**: Cursor SDK is beta; DPA template likely exists but may lack specific provisions (e.g., EU data residency commitments, sub-processor change notification timelines aligned with enterprise customer norms). Likely tightens through 2026-2027.
- **Frontier-model providers**: OpenAI / Anthropic / Google all maintain mature DPAs; sub-processor lists publicly available; well-tested in enterprise procurement.
- **Pre-emptive engineering**: maintaining clear provenance trail of which canonical content gets quoted to which substrate enables responding to GDPR access / deletion requests; the AKOS-as-SSOT discipline (canonicals in git; mirrors derived) is structurally well-positioned vs ad-hoc-in-vendor-store patterns.

### 3.5 ADVOPS recommendation

Formal GDPR / DPA cascade review before D-IH-84-D D2/D3 ratification. Particularly: (a) Cursor SDK DPA review (if B2 or B3 ratifies); (b) customer-facing Madeira DPA template authored under [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) ADVOPS workflow; (c) sub-processor change notification cadence aligned with enterprise customer norms.

## 4. Cursor MSA evolution forecast

### 4.1 The contract surface

Anysphere's contracts for Cursor as of 2026-Q2 `[ext]` include:
- **Cursor MSA (Master Services Agreement)** — covers the Cursor IDE subscription (Pro / Business / Enterprise tiers).
- **Cursor SDK Terms of Service** — separate from MSA; covers programmatic use of Cursor's agent infrastructure (currently beta).
- **Cursor Enterprise SOC 2 / data residency** — separate enterprise-tier provisions for compliance customers.

The SDK ToS is the load-bearing contract surface for `D-IH-84-B` ratification.

### 4.2 Known SDK ToS shape (2026-Q2)

Per `[ext]` Cursor public ToS (subject to verification at master-roadmap-grade P1):
- Beta-software disclaimer (no service-level guarantees; substantial changes possible).
- Customer responsible for content + outputs (Anysphere disclaims responsibility for what agents produce).
- License: limited revocable license to use the SDK; no source access.
- Data: Anysphere processes prompts + outputs to provide the service; opt-out of training-data use available in business tiers.
- Termination: Anysphere can terminate access with notice; customer obligation to remove all SDK uses post-termination.

### 4.3 Forecast (2026-2027)

- **GA transition (likely 2026-Q3 or Q4 per `[ext]`)**: SDK ToS likely tightens for production-grade use; SLA introduced for paid tiers; pricing model may shift from beta-free to per-call or per-seat.
- **Enterprise tier maturity**: Cursor Business tier already exists ($40/user) `[ext]`; full enterprise tier with SOC 2 + BAA + DPA likely 2026-Q4 / 2027-Q1.
- **Competitive pressure**: Anthropic + OpenAI both ship competing agent-SDK offerings; pressure on Cursor MSA terms to remain attractive (lower lock-in language; more permissive data handling; more competitive pricing).

### 4.4 Substrate implications

| Scenario | Implication for B2/B3 |
|:---|:---|
| GA transition with substantive ToS changes | Need to re-ratify D-IH-84-B against new MSA terms; potentially within 6-12 months of B2/B3 selection |
| Anysphere acquired or pivots | Substrate continuity risk; mitigation = OpenClaw policy backend preserves AKOS-side migration path |
| Pricing shifts to per-call | Cost class moves from `seat-billed` to potentially less predictable; budget impact |
| Stricter data-handling tier requirements for enterprise customers | Forces Cursor Enterprise tier adoption (higher cost; better DPA) |

### 4.5 ADVOPS recommendation

Formal Cursor MSA + SDK ToS review before B2 or B3 ratification per D-IH-84-B. Specifically: (a) liability allocation review (customer-responsible-for-outputs interaction with EU AI Act provider obligations); (b) termination + data-deletion review; (c) sub-processor + data-residency provisions for any EU customer engagements.

## 5. IP-indemnity carve-outs across SDKs

### 5.1 The regulatory shape

When an LLM produces output, the output may include text that resembles or reproduces training-data content. If the training data was IP-protected (e.g., copyrighted code, copyrighted prose) and the LLM output is used in commercial production, the customer could face IP infringement claims from the original rights-holder.

Frontier LLM providers offer varying degrees of customer indemnification against such claims:

| Provider | Indemnity scope (2026-Q2 per `[ext]`) | Notes |
|:---|:---|:---|
| **OpenAI** | "Copyright Shield" — defends business customers against IP infringement claims arising from ChatGPT / API output | Conditions: must have applied OpenAI safety mitigations + not have submitted infringing input |
| **Anthropic** | Indemnification clause in Claude API customer agreement; scope similar to OpenAI | Conditions: must use Claude through official API not via reverse-engineered access |
| **Google (Gemini)** | "Generative AI Indemnification" — covers Vertex AI customers | Conditions: must use specific covered models; not use customer-provided prompts that trigger infringement |
| **Cursor** | Cursor SDK does not currently offer first-party IP indemnification (passes through to underlying model provider) `[ext]` | If Composer 2 = Moonshot Kimi 2.5 per founder framing 2026-05-16, indemnity scope = whatever Moonshot offers (likely lower than frontier-Western providers) |
| **Open-weights models (Llama, Kimi)** | No vendor indemnity; customer carries IP risk | Mitigation: defensive license review of model training corpus + customer's own legal posture |

### 5.2 Substrate implications

| Substrate choice | IP-indemnity profile | Notes |
|:---|:---|:---|
| **OpenClaw thin-adapter (B1)** with LLM provider | Inherits whatever the underlying provider offers; Holistika can choose providers with strongest indemnity (OpenAI, Anthropic, Google) | Strongest profile; supports customer-facing prose generation |
| **Cursor SDK (B2)** with Anysphere-managed model | Inherits Anysphere's posture (pass-through to underlying; Moonshot Kimi 2.5 less mature than Western frontier providers) | Weaker profile; less suitable for customer-facing prose without additional safeguards |
| **Hybrid (B3)** | Configurable per workflow — Cursor SDK frontend for development; OpenClaw backend can route customer-facing-prose flows through indemnified provider | Best-of-both; complexity in policy enforcement |
| **D2 MADEIRA-as-SaaS** | Customer agreement must specify indemnity flow-down or exclusion; Holistika carries risk if customer-facing outputs cause IP claims | Substantial liability surface; pricing must reflect; ADVOPS engagement mandatory |

### 5.3 Forecast (2026-2027)

- **Indemnity standardisation**: industry pressure pushing toward minimum indemnity terms for enterprise customers; frontier providers may extend scope.
- **Open-weights model trajectory**: as open-weights models mature (Llama, Kimi, etc.), customer-carried IP risk likely codified into customer DPAs; price/indemnity trade-off becomes explicit.
- **Cursor SDK indemnity offering**: likely added to Business or Enterprise tier as part of GA push; verify at master-roadmap-grade P1 update.

### 5.4 ADVOPS recommendation

Formal IP-indemnity review per substrate per use-case before D-IH-84-B ratification. Specifically: (a) for any flows generating customer-facing prose (decks, proposals, dossiers, marketing copy), substrate selection should prefer providers with strong indemnity; (b) Cursor SDK uses for internal-developer tooling have lower IP exposure (no customer-facing output) — substrate-choice can vary by flow.

## 6. Aggregate findings (4 observations)

1. **EU AI Act 2026-08-02 high-risk enforcement is the most significant forecasted regulatory event.** D-IH-84-D D2 (productized Madeira) substantially exposes Holistika to provider obligations; D1 substantially reduces exposure. **Implication for P4 ratification**: D1 has lower regulatory friction than D2; this is a material input to the productization-shape decision separate from competitive analysis in [`competitive-layer-positioning.md`](competitive-layer-positioning.md).

2. **GDPR DPA cascading complexity scales with substrate-layer depth.** B1 (OpenClaw direct to LLM) has simplest DPA cascade; B2/B3 add a layer (through Cursor SDK to Anysphere to Anysphere's sub-processors). For customer-facing productization (D2/D3), the cascade extends downward to Holistika's customers. **Implication for P4 ratification**: D2 + B2/B3 has highest DPA complexity; ADVOPS engagement timeline must account for the contract-set assembly effort.

3. **Cursor SDK ToS is the load-bearing contract surface for B2 / B3 ratification.** ToS is beta-state; GA transition likely 2026-Q3/Q4 with material changes; commitment to B2 or B3 without formal MSA + SDK ToS review carries meaningful contract risk. **Recommended mitigation**: defer formal D-IH-84-B B2/B3 ratification until Cursor SDK ToS reaches GA or until Anysphere provides written assurance on key terms (data residency, sub-processor cadence, termination data return, IP indemnity).

4. **IP indemnity profile favors frontier Western providers (OpenAI / Anthropic / Google) for customer-facing output flows.** Cursor SDK's pass-through-to-underlying-model indemnity is weakest for the Moonshot Kimi 2.5 backed flows; for customer-facing-prose generation, route through indemnified providers regardless of substrate. **Implication**: hybrid policy at the OpenClaw layer (B3 architecture; per-flow routing of customer-facing prose to indemnified provider) provides a structural safeguard B2-pure does not.

## 7. Implications for `D-IH-84-B` substrate-baseline ratification

The regulatory analysis adds three considerations to the substrate-choice that the [`p2-substrate-scorecard-2026-05-17.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) dimensions did not fully capture:

1. **Regulatory friction is non-trivial for B2 (Cursor SDK pure migration) due to ToS beta-state + DPA cascade depth + weaker IP indemnity. The recommended-pending-evidence B3 hybrid default per `decision-log.md` D-IH-84-B is strengthened by these findings** — B3's OpenClaw policy backend provides per-flow routing capability that mitigates IP-indemnity exposure on customer-facing flows.

2. **D-IH-84-D productization shape has regulatory implications independent of substrate choice.** D2 (hosted SaaS) triggers EU AI Act provider obligations; D1 (library) sidesteps; D3 (hybrid) is mixed. **Recommended**: surface this independent axis at the P4 batched ratification — operator may want to ratify D-IH-84-D separately from D-IH-84-B given the differing regulatory profiles.

3. **ADVOPS engagement is recommended BEFORE D-IH-84-B and D-IH-84-D ratification.** Per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) workflow: engage EU AI Act counsel + GDPR/DPA counsel + IP/IT counsel via the standard 4-discipline framework. The engagement output feeds the P4 ratification with binding interpretation of the four regulatory topics in §2-§5 above. **This is an addition to the master-roadmap §4 P4 deep section's verification matrix.**

## 8. Cross-references

- [I84 master-roadmap](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) §3 P1 Layer 1 thread C — the deliverable contract.
- [I84 P1 audit report](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) — paired audit (Thread A scope).
- [I84 P2 scorecard](../../planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) — scorecard dimensions; regulatory friction is not explicitly scored but informs lock-in + governance-fit dimensions.
- [`competitive-layer-positioning.md`](competitive-layer-positioning.md) — paired Thread B; competitive + regulatory together inform `D-IH-84-D` productization-shape ratification.
- [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) — ADVOPS workflow for formal legal review.
- [`SOP-EXTERNAL_REPO_BLESSING_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) — adviser engagement and disciplines mapping.
- EU AI Act (Regulation (EU) 2024/1689) — full text via https://eur-lex.europa.eu (verification needed at ADVOPS engagement).
- GDPR Article 28 — controller-processor + sub-processor obligations.
- Cursor MSA + SDK ToS — Anysphere public terms (verification needed at master-roadmap-grade P1 update).

## 9. Provenance and confidence labels

Authored as Tier-1 WIP per master-roadmap §3 P1 thread C. Confidence `B2` (Holistika-internal-research-synthesis from agent training corpus). **All four regulatory topics require formal legal review** via ADVOPS engagement before any binding D-IH-84-B / D-IH-84-D ratification. This dossier surfaces shape; legal counsel provides advice.

The four `[ext]` flags throughout (EU AI Act dates; SDK pricing; ToS specifics; indemnity scope) should be re-verified by Holistika Legal Counsel + jurisdictional fiscal/IP advisers per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) workflow before treating as binding. Tier-1 WIP classification per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md).
