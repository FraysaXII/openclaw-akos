---
report_id: i84-advops-engagement-scoping-2026-05-17
authored: 2026-05-17
author: System Owner (with agent assistance) via I86 Wave 2 §3.5 / I84 Wave A1 successor pick-up
phase: pre-P4
initiative: INIT-OPENCLAW_AKOS-84
classification: operator-readable scoping recommendation (not a binding engagement decision)
access_level: 4
language: en
linked_decisions: [D-IH-84-A, D-IH-84-B, D-IH-84-D]
linked_risks: [R-IH-84-NEW-ADVOPS, R-IH-84-NEW-CURSOR-TOS-VELOCITY]
linked_evidence:
  - docs/wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md
  - docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/checkpoints/sc-i84-p1p2-complete-2026-05-17.md
source_taxonomy: holistika-internal-research-synthesis
confidence_level: B2
---

# I84 ADVOPS engagement scoping recommendation (pre-P4)

> **Purpose.** Per `R-IH-84-NEW-ADVOPS` (surfaced in [`sc-i84-p1p2-complete-2026-05-17.md`](checkpoints/sc-i84-p1p2-complete-2026-05-17.md) §7 risk surfacing) — an operator-readable scoping note recommending **formal ADVOPS engagement** of Legal Counsel across **four disciplines** BEFORE the I84 P4 batched ratification fires `D-IH-84-B` (AKOS substrate baseline) and `D-IH-84-D` (Madeira productization shape). This is a **scoping recommendation**, not a binding engagement decision; the operator decides at P5 whether to engage now, defer, or proceed without.
>
> Engagement workflow per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) (ADVOPS plane; workstream `hol_opera_ws_5`). The four disciplines named below map to the ADVOPS taxonomy in [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — the row authoring the engagement-state lookup operators consult when commissioning external counsel.

## 1. Trigger — why this scoping note exists now

Three convergent triggers surface this recommendation at this point in the I84 lifecycle, BEFORE the P4 batched architectural-shape ratification fires:

1. **Regulatory + ToS forecast findings.** [`regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) §6 (aggregate findings) names four substrate-affecting regulatory topics whose 2026-Q3+ trajectory materially weighs on `D-IH-84-B` and `D-IH-84-D`: EU AI Act provider-vs-deployer enforcement (2026-08-02), GDPR-as-SaaS DPA cascading, Cursor SDK MSA + ToS evolution (likely GA transition 2026-Q3/Q4 per `[ext]`), and IP-indemnity carve-outs across SDKs. Each of the four §2.5 / §3.5 / §4.5 / §5.4 sub-sections of the forecast explicitly recommends ADVOPS engagement on its topic.

2. **Risk-register entries pending mint.** Two risks were surfaced in the I84 P1+P2 checkpoint that warrant addition to [`risk-register.md`](../risk-register.md) at the next operator-approved register edit:
   - `R-IH-84-NEW-ADVOPS` (likelihood: medium; impact: high) — ratifying `D-IH-84-B` and `D-IH-84-D` without formal ADVOPS engagement on the four-discipline framework exposes Holistika to material regulatory friction that compounds across the binding-substrate window.
   - `R-IH-84-NEW-CURSOR-TOS-VELOCITY` (likelihood: high; impact: medium) — Cursor SDK ToS in beta likely changes materially at GA; ratifying B2 or B3 against pre-GA terms commits to a contract surface that shifts.

3. **Substrate-baseline + productization-shape coupling.** Per [`p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) §4 finding #5 — `D-IH-84-D` productization shape maps to substrate class. **D2 hosted-agent** triggers EU AI Act provider obligations (Annex III applicability); **D1 library-only** sidesteps; **D3 hybrid** is mixed. The two decisions are not independent on the regulatory axis, and a binding ratification of either without ADVOPS evidence carries asymmetric forward-cost: provider-obligations remediation post-D2 is materially more expensive than D1 → D2 promotion later with the regulatory homework already done.

The convergence point is the P4 batched ratification gate. ADVOPS engagement is the canonical pathway for converting the `B2` confidence forecasts in [`regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) into `A1` binding legal interpretation that the P4 ratification can rely on.

## 2. Four-discipline scope

Per the ADVOPS workflow in [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) and the canonical lookup [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — recommended engagement spans four disciplines. Per discipline: target counsel profile, concrete questions, deliverable from the engagement, and the I84 decision the engagement output feeds.

### 2.1 EU AI Act counsel

- **Target profile.** EU-qualified Legal Counsel with active EU AI Act 2024/1689 practice. Preferred jurisdiction profile aligned with Holistika's primary EU operating footprint (jurisdiction-specific advisor list lives in operator-managed GOI/POI register; identity mapping is off-repo).
- **Concrete questions to surface in the engagement letter.**
  1. Under the Act's provider-vs-deployer split, what is Holistika's classification today (a) when using GPAI models via API for internal AKOS operations, (b) when wrapping LLMs in OpenClaw / Cursor SDK / hybrid agent runtimes for own use, (c) when productizing Madeira as B2B SaaS for external customer use? Map each scenario to Article 16 (provider obligations) / Article 26 (deployer obligations) / Article 25 (downstream provider passthrough).
  2. Which Madeira customer-facing flows could trigger an Annex III high-risk classification, and what is the conformity-assessment + technical-documentation + post-market-monitoring overhead per scenario? Specifically address: employment / recruitment flows (not in current scope; forecasted), access-to-essential-services (forecasted via KiRBe vertical expansion), and law-enforcement / migration / democratic-process flows (out of scope; documenting for completeness).
  3. As a non-EU-established entity, what authorised-representative requirements apply under Article 22 if D2 (hosted-agent Madeira) productizes? Recommend candidate representative profiles + indicative cost envelope.
  4. What pre-compliance engineering investment (transparency documentation per Article 13, risk-management system per Article 9, data-governance per Article 10, technical-documentation per Article 11) is recommended now vs deferrable to D2 activation?
- **Deliverable from engagement.** A 3-5-page binding memo addressing each question with citations to Act articles + recitals; identifies which D-IH-84-B / D-IH-84-D options have the lowest, highest, and most uncertain regulatory profiles; recommends pre-emptive engineering investment ordered by NPV.
- **Decision fed.** `D-IH-84-B` (substrate baseline; informs B1 vs B2 vs B3 weighing); `D-IH-84-D` (productization shape; informs D1 vs D2 vs D3 weighing).

### 2.2 GDPR / DPA counsel

- **Target profile.** EU-qualified privacy counsel with active DPA-drafting practice (controller-processor + sub-processor) for B2B SaaS clients. Could be the same firm as §2.1 EU AI Act counsel if the firm carries both practices.
- **Concrete questions.**
  1. Review Cursor SDK + Anysphere DPA template (current as of `2026-Q2 [ext]`) against Article 28 minimum content + Holistika's posture as controller (when used internally) or processor (when Madeira routes customer data through Cursor SDK). Identify gaps: EU data residency commitments, sub-processor change notification cadence, audit rights, deletion-on-termination shape.
  2. Draft a customer-facing Madeira DPA template (Holistika as processor) aligned with enterprise customer norms (audit rights, sub-processor change notification timelines ≤ 30 days, SCC integration for non-EU customers, deletion-on-termination + data-return).
  3. Confirm the sub-processor cascade structure for each D-IH-84-B option: (B1) customer ↔ Holistika ↔ LLM provider only; (B2) customer ↔ Holistika ↔ Anysphere ↔ Anysphere's LLM sub-processors; (B3) hybrid per-flow routing. For each, identify added DPA-cascade-complexity costs and customer-procurement friction.
  4. Frontier-LLM-provider DPA review (OpenAI / Anthropic / Google) — confirm sub-processor lists are current; flag any provisions that constrain Holistika's customer-DPA template downstream.
- **Deliverable.** A consolidated DPA package: (a) Cursor SDK DPA risk memo + redline if mitigations needed; (b) customer-facing Madeira DPA template ready for first enterprise customer engagement; (c) sub-processor cascade decision-table per substrate choice.
- **Decision fed.** `D-IH-84-B` (DPA cascade complexity is part of substrate weighing); `D-IH-84-D` (D2/D3 productization requires customer-facing DPA in place).

### 2.3 IP / IT counsel (intellectual-property + technology contracting)

- **Target profile.** Legal Counsel with active practice in SaaS IP-indemnification + AI-output IP-claims defense + technology-license drafting. Preferred jurisdiction: covers Holistika's primary operating + at least the EU + US litigation surface.
- **Concrete questions.**
  1. Compare IP-indemnity scope across the candidate substrate vendors (OpenAI "Copyright Shield", Anthropic Claude indemnification clause, Google Vertex AI Generative AI Indemnification, Cursor SDK pass-through-to-underlying-model, open-weights-models no-vendor-indemnity per `[ext]`). For each, identify conditions, exclusions, cap structure, and notice obligations.
  2. For each `D-IH-84-B` option (B1/B2/B3) crossed with each customer-facing-prose flow (decks, proposals, dossiers, marketing copy, brand voice generation), recommend the optimal substrate routing for IP-exposure minimisation. Confirm whether B3 hybrid's per-flow-routing pattern is contractually enforceable (i.e., can OpenClaw policy backend reliably route customer-facing prose through the indemnified provider regardless of operator-selected frontend).
  3. For `D-IH-84-D` D2/D3 customer-facing productization, draft the Holistika-customer indemnity flow-down: which upstream indemnities pass through; what cap / exclusion structure; what additional Holistika-side indemnity (if any) is commercially-defensible.
  4. Cursor SDK license-separation enforceability (cross-references [`i74-brand-tooling-productization.md`](../../_candidates/i74-brand-tooling-productization.md) `C-74-4`): if `@holistika/madeira-agent` ships as `D1` library AND ships embedded as a backend service for Cursor SDK customers, does the license-separation language in Cursor MSA conflict with the library distribution model?
- **Deliverable.** (a) IP-indemnity scope matrix per substrate (the comparison table promoted to canonical); (b) per-flow routing recommendation table (which flow uses which substrate for which jurisdiction); (c) customer-indemnity flow-down clause + cap structure recommendation; (d) license-separation enforceability memo.
- **Decision fed.** `D-IH-84-B` (per-flow IP-routing strengthens B3 hybrid case); `D-IH-84-D` (customer-facing productization requires indemnity flow-down); `i74 C-74-4` (license-separation enforceability is the I74 productization gating evidence).

### 2.4 Jurisdictional fiscal counsel

- **Target profile.** Tax + corporate-structuring counsel qualified in Holistika's primary operating jurisdiction(s). Could be a separate engagement from §2.1-§2.3 (different professional discipline).
- **Concrete questions.**
  1. For each Madeira productization shape (`D-IH-84-D` D1 library license vs D2 hosted SaaS subscription vs D3 hybrid), what is the optimal corporate-structuring posture (Holistika main entity vs subsidiary vs separate operating entity per product line)? Considers VAT / cross-border-service VAT / withholding / transfer-pricing.
  2. For each substrate vendor relationship (`D-IH-84-B` B1/B2/B3), what fiscal implications arise (e.g., Anysphere cross-border-service VAT for B2/B3; per-token spend tax-treatment for token-billed providers)?
  3. Recommend customer-billing structure per Madeira shape: B2B SaaS subscription (D2), library license fee (D1), hybrid commercial model (D3). Per shape: invoicing entity, currency, payment terms, jurisdictional VAT treatment.
  4. Identify any product / sub-mark trademark filings that should accompany Madeira productization (cross-references [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) Nice-class scope analysis).
- **Deliverable.** (a) per-shape fiscal-posture memo with corporate-structuring recommendation; (b) customer-billing structure template per shape; (c) trademark-filing recommendation cross-referenced to existing Branded-House posture.
- **Decision fed.** `D-IH-84-D` (productization shape has fiscal implications independent of regulatory + IP axes); future I74 P4 productization-mechanics initiative.

## 3. Timeline and cost-class envelope (qualitative)

This section frames **qualitative** cost-class + timeline; per-firm proposals are operator-managed (per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) §"Discipline routing" — pricing + counsel selection are off-repo operator-managed concerns; this dossier surfaces shape, not bids).

### 3.1 Timeline

- **Discovery + counsel selection** — 1-2 weeks. Operator engages with target firms per discipline; reviews proposals; signs engagement letters. Per discipline this may overlap (one firm covers §2.1 + §2.2 = single proposal; §2.3 IP often single firm; §2.4 fiscal separate firm).
- **Engagement execution** — 3-6 weeks for §2.1-§2.3 (regulatory + DPA + IP scope is substantial); 2-3 weeks for §2.4 fiscal. Engagements can run in parallel after selection.
- **Deliverable review + ratification feed** — 1 week (operator reviews per-discipline memo + cross-checks against P1/P2 substrate evidence + draws conclusions for P4).

Total: **6-10 calendar weeks** from operator green-light to P4 batched ratification fully informed. P4 ratification can proceed earlier with explicit acknowledgement of incomplete ADVOPS coverage (per Option D in §4 below).

### 3.2 Cost-class envelope (qualitative; per-discipline)

- **§2.1 EU AI Act counsel** — initial scoping memo: low-thousands EUR (envelope; verify per firm). Binding opinion with Annex-III applicability analysis: low-five-figure EUR per scenario. Authorised-representative ongoing retainer (if D2 ratifies): additional separate ongoing engagement.
- **§2.2 GDPR/DPA counsel** — Cursor SDK DPA review: low-thousands EUR. Customer-facing Madeira DPA template authoring: mid-four-figure to low-five-figure EUR depending on template complexity + redline cycles.
- **§2.3 IP/IT counsel** — comparison memo + per-flow routing recommendation: mid-four-figure to low-five-figure EUR. License-separation enforceability memo: low-four-figure EUR. Customer-facing indemnity flow-down clause + cap structure: low-four-figure EUR per scenario.
- **§2.4 Jurisdictional fiscal counsel** — per-shape fiscal posture memo + corporate-structuring recommendation: mid-four-figure to low-five-figure EUR. Trademark filing analysis: separate consultation; per-Nice-class fees per jurisdiction (filing costs vs counsel time).

**Aggregate qualitative envelope.** Operator should expect a total ADVOPS engagement on the order of **low-five-figure EUR per discipline for initial scoping engagement**, with **multipliers for binding-opinion depth** and **separate retainers** if ongoing engagement (e.g., authorised representative) is required. Per-firm proposals reset the envelope; this is a qualitative-shape recommendation only.

**Risk-adjusted ratio.** Per `R-IH-84-NEW-ADVOPS` impact (high) — substrate-baseline + productization-shape ratification without ADVOPS coverage exposes Holistika to remediation costs (regulatory penalties, IP claim defense, customer churn from DPA-failure) that scale into six-figure or seven-figure EUR. Pre-emptive ADVOPS investment is order-of-magnitude cheaper than reactive remediation.

## 4. Forward actions (canonicals the engagement updates)

The engagement output feeds the I84 P4 ratification + populates several canonical surfaces. Per the ADVOPS rule and Initiative 21 ADVOPS canonical pattern:

### 4.1 Update [`ADVISER_OPEN_QUESTIONS.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_OPEN_QUESTIONS.csv)

For each concrete question listed in §2.1-§2.4 above, append a row with: `question_id`, `discipline`, `question_text`, `engagement_id` (populated when engagement letter signed), `status` (`open` / `engaged` / `answered` / `withdrawn`), `decision_fed` (D-IH-84-B / D-IH-84-D / etc.), `expected_answer_date`. Per the rule: the discipline row in [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) pre-fills `canonical_role` + `default_process_item_id` so per-question authoring stays light.

### 4.2 Update [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) if a discipline is missing

The four-discipline framework above maps to existing rows in [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) (Legal / Fiscal / IP / Banking / Certification / Notary per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) plane summary). If EU AI Act counsel warrants a sub-discipline distinct from generic Legal (e.g., specialist enforcement-jurisdiction practice), surface as a new row at the canonical-CSV gate (operator approval required).

### 4.3 Update [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv)

Per engagement: file the engagement letter as a filed instrument with `instrument_id`, `discipline`, `filing_date`, `counterparty` (FK to [`GOI_POI_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv) once the counsel firm is registered as a GOI), and `linked_decisions` (D-IH-84-B / D-IH-84-D / etc.).

### 4.4 Register the counsel firm in [`GOI_POI_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv)

Per the GOI/POI knowledge dimension — each counsel firm is registered with `ref_id` (`GOI-LEGAL-<SLUG>-2026` / `GOI-FISCAL-<SLUG>-2026` / etc.). Identity mapping (real name ↔ ref_id) stays off-repo per `D-CH-2` forward-only privacy posture.

### 4.5 Feed the engagement-output memo into the P4 ratification evidence stack

The engagement deliverable per discipline (§2.1-§2.4) becomes evidence-stack input for the P4 batched ratification (`D-IH-84-B/C/D/E`). Per [`master-roadmap.md`](../master-roadmap.md) §3 P4 — the batched ratification's evidence stack is intended to include the regulatory + IP + fiscal axes; ADVOPS engagement promotes those axes from `B2` Holistika-internal-research-synthesis to `A1` binding legal interpretation.

### 4.6 Operator approval gate

This scoping note **does not** authorise engagement. Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) ADVOPS engagement of external counsel is operator-gated. The operator may:

- **Option A — Engage all four disciplines now.** Recommended if P4 ratification is on a 2-3 month horizon and full ADVOPS coverage is desired before substrate-baseline + productization-shape commitments lock in.
- **Option B — Engage §2.1 + §2.3 only (regulatory + IP) now; defer §2.2 + §2.4 to post-P4.** Hybrid: addresses the highest-impact uncertainty (regulatory exposure + IP-indemnity) before P4; defers DPA + fiscal to the post-P4 productization initiative (I74 owning).
- **Option C — Engage §2.1 only now; defer §2.2 + §2.3 + §2.4.** Minimum-viable ADVOPS coverage: addresses the most material regulatory event (EU AI Act 2026-08-02 high-risk enforcement) and accepts incremental risk on the other three axes.
- **Option D — Defer all ADVOPS engagement; proceed to P4 with `B2`-confidence regulatory shape.** Accepts `R-IH-84-NEW-ADVOPS` + `R-IH-84-NEW-CURSOR-TOS-VELOCITY` materially; P4 ratification carries explicit "ADVOPS-pending" qualifier; downstream remediation cost is the explicit trade-off.

## 5. Cross-references

- [`regulatory-tos-forecast.md`](../../../intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) — the Tier-1 WIP analysis whose §2.5 + §3.5 + §4.5 + §5.4 sub-sections each recommend ADVOPS engagement; this scoping note aggregates those recommendations.
- [`sc-i84-p1p2-complete-2026-05-17.md`](checkpoints/sc-i84-p1p2-complete-2026-05-17.md) §7 — the operator-facing risk surfacing where `R-IH-84-NEW-ADVOPS` was first noted.
- [`master-roadmap.md`](../master-roadmap.md) §3 P4 — the batched ratification gate whose evidence stack this engagement informs; §6 R-IH-84-1 through R-IH-84-7 — the pre-existing risk preview that R-IH-84-NEW-ADVOPS + R-IH-84-NEW-CURSOR-TOS-VELOCITY append to.
- [`decision-log.md`](../decision-log.md) D-IH-84-B + D-IH-84-D — the load-bearing decisions the engagement output informs.
- [`p2-substrate-scorecard-2026-05-17.md`](p2-substrate-scorecard-2026-05-17.md) §4 finding #5 — the substrate-class to productization-shape mapping that surfaces the regulatory-axis asymmetry.
- [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) — ADVOPS workflow + canonical-CSV pattern; this scoping note follows the rule.
- [`ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_ENGAGEMENT_DISCIPLINES.csv) — discipline lookup; the four-discipline framework above maps to existing rows.
- [`ADVISER_OPEN_QUESTIONS.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/ADVISER_OPEN_QUESTIONS.csv) — open-questions register; engagement-output per-question rows append here.
- [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/FOUNDER_FILED_INSTRUMENTS.csv) — engagement-letter filing register.
- [`GOI_POI_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv) — counsel firm registration as GOI.
- [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md) — PMO SOP for adviser engagement lifecycle; this scoping note is the I84-specific evidence input for an SOP-driven engagement.
- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — existing trademark posture; §2.4 fiscal engagement cross-references for trademark-filing recommendations.

## 6. Provenance and confidence labels

Authored at I84 Wave A1 (parallel-to-P4-foreground gate per I86 successor-pickup) 2026-05-17. Confidence `B2` (Holistika-internal-research-synthesis); the regulatory + IP + fiscal shape estimates in §2 + §3 promote to `A1` only via the recommended ADVOPS engagement. This is a **scoping recommendation**, not advice — operator-gated activation per §4.6.

Cost envelopes in §3.2 are **qualitative** order-of-magnitude estimates; per-firm proposals are off-repo + operator-managed per [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) §"Forward-only privacy posture". No real counsel firm names, no real cost figures, no real engagement-letter content in this dossier — those are operator-managed and live off-repo per `D-CH-2`.

Tier-2 planning classification per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md). Not canonical until promoted via operator-approved ADVOPS engagement-letter signing + ADVISER_OPEN_QUESTIONS.csv row appends per §4.1.
