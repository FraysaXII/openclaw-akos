---
title: Substrate Landscape Doctrine
language: en
intellectual_kind: research-area-canonical
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - System Owner
  - Holistik Researcher
  - KM Officer
last_review: 2026-05-17
last_review_by: System Owner
ratifying_decisions:
  - D-IH-84-A
  - D-IH-84-G
status: review
register: internal
linked_canonicals:
  - AGENTIC_FRAMEWORK_LANDSCAPE.md
  - HOLISTIKA_AGENTIC_DOCTRINE.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md
linked_runbooks:
  - scripts/peopl_research_substrate_audit_cadence.py
linked_processes:
  - env_tech_dtp_substrate_landscape_mtnce_001
companion_to:
  - ../../../../Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md
  - ../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md
---

# Substrate Landscape Doctrine

> The Research-area side of the substrate governance triangle. This canonical carries the **why** behind which substrates earn the right to canonical status — the discipline of auditing, scoring, and choosing the technical substrates Holistika commits to. Where the Tech Lab side [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) lists the **how** (framework rows + KB infrastructure dimensions + MCP postures), and the People side [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) explains the **what** (agentic-as-DoD), this canonical names the **why which** — the doctrine of substrate selection itself.

Per `D-IH-84-G` (Research-area discipline-of-disciplines posture; ratified 2026-05-16 inline) — Research is the **meta-discipline** that audits which substrates earn canonical status. The audit lives in `SUBSTRATE_REGISTRY.csv` ([`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv)). The cadence lives in [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md). This doctrine lives here.

---

## §1 The substrate question

A substrate is **what AKOS is made of** at the technical layer. It is the runtime + library + adapter pattern that the operator's daily work executes on. As of 2026-Q2, AKOS runs on the OpenClaw thin-adapter pattern over upstream frameworks (per AGENTIC_FRAMEWORK_LANDSCAPE.md §1 OpenClaw row). KiRBe runs on the MADEIRA-direct pattern over LlamaIndex (per founder framing 2026-05-16). Madeira-as-method runs on whichever substrate the operator's day-to-day Cursor session uses.

The substrate question is **not the same as the LLM-choice question**. LLM choice is which model serves a given turn (Claude / GPT / Llama-via-Groq / Kimi-via-Groq, etc.); substrate choice is the runtime + library + adapter pattern that surrounds the LLM. The two are orthogonal: any substrate can serve any LLM behind the same provider-abstraction surface (`akos/model_catalog.py`).

The substrate question is also **not the same as the AIC framing question** (per [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) Madeira footnote + [`i76-madeira-elevation.md`](../../../../../../wip/planning/_candidates/i76-madeira-elevation.md) §2 F1-F5). AIC framing is whether agents are supervised / peer / dispatcher / single / hybrid; substrate is what each agent runs on. But the two ARE **coupled empirically** — some substrates favor some framings (Cursor SDK favors F1 supervised; CrewAI favors F2 peer; LangGraph favors F3 dispatcher; Claude Code SDK favors F4 single).

## §2 Why Research owns the substrate audit

Per [`akos-people-discipline-of-disciplines.mdc`](../../../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) Rule 3 applied recursively to Research-area: People is the discipline-of-disciplines that mints the patterns; Research is the meta-discipline that audits which substrates earn canonical status. The two operate at different levels:

- **People** mints the **patterns** that other areas inherit (engagement-model registry; paired SOP+runbook; persona registry; classification lattice; substrate audit cadence shape). The patterns are doctrinal abstractions.
- **Research** mints the **substrate evidence** that grounds the pattern instantiations. The evidence is empirical claims about which technical artefact does what.

This split avoids a structural conflict: People canonicals are deliberately anti-jargon (per `D-IH-79-N` drift gate); substrate evidence carries legitimate technical jargon (framework names, runtime tokens, ToS specifics). Research is the legitimate jargon home — the meta-discipline that catalogs technical substrates without polluting People's clarity-first canonicals.

Tech Lab carries the **operational** side of the substrate (the AGENTIC_FRAMEWORK_LANDSCAPE.md framework rows + MCP postures + integration matrix; the day-to-day operator-facing surface). Research carries the **methodological** side (the audit cadence; the comparison-matrix discipline; the regulatory-and-competitive-context analysis; the past-PoC translation discipline). The two pair like People-side `HOLISTIKA_AGENTIC_DOCTRINE.md` pairs with Tech-Lab-side `AGENTIC_FRAMEWORK_LANDSCAPE.md`.

## §3 The audit shape (5 elements)

Every substrate-audit cycle (default quarterly per [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md) when minted at status:review post-this-doctrine) produces five outputs:

1. **Substrate landscape audit** — per-substrate structured rows covering: name, vendor, runtime_shape, persistence_model, tool_protocol, license_class, status, cost_class, akos_integration_state, madeira_productization_role, aic_pattern_role, last_audit_date, audit_source_url, notes. The Q2 2026 audit lives at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md`](../../../../../../wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p1-substrate-landscape-2026-05-17.md) (17 substrates × 18 columns).

2. **Substrate scorecard** — per-substrate per-dimension scoring across the 6 governance dimensions: governance fit, operator-runtime maturity, cost, lock-in risk, AKOS-as-SSOT compatibility, MADEIRA elevation alignment. The Q2 2026 scorecard lives at [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md`](../../../../../../wip/planning/84-substrate-doctrine-and-commercial-readiness/reports/p2-substrate-scorecard-2026-05-17.md) (17 substrates × 6 dimensions; 5-level qualitative scoring).

3. **Competitive-layer positioning** — per-competitor analysis of vendors whose products overlap or could displace Holistika's market positioning. The Q2 2026 analysis lives at [`docs/wip/intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md`](../../../../../../wip/intelligence/substrate-audit-2026-Q2/competitive-layer-positioning.md) (8 competitors × structured rows).

4. **Regulatory + ToS forecast** — per-regulatory-topic analysis of substrate-relevant law + contract surfaces. The Q2 2026 analysis lives at [`docs/wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md`](../../../../../../wip/intelligence/substrate-audit-2026-Q2/regulatory-tos-forecast.md) (EU AI Act + GDPR-as-SaaS DPA + Cursor MSA + IP-indemnity). Recommends ADVOPS engagement per `D-IH-84-B/D` discipline.

5. **Past-PoC translation matrix** — per-prior-initiative analysis of substrate learnings translatable to current version. The Q2 2026 analysis lives at [`docs/wip/intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md`](../../../../../../wip/intelligence/substrate-audit-2026-Q2/past-poc-translation-matrix.md) (I10/I11/I12/I13 + KiRBe-still-on-LlamaIndex + R&L v2.7 framework references).

Each output cycle promotes registered substrates to `SUBSTRATE_REGISTRY.csv` ([`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv)) as the canonical-state-of-record. Registry rows are appended or `ALTER`'d in place per the SOP cadence; old reports are retained as dated evidence under `docs/wip/intelligence/substrate-audit-YYYY-QN/` per [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §17 Tier-1 WIP convention.

## §4 The doctrine of substrate continuity

AKOS substrate evolution has been demonstrably durable across vault generations (v1.3 → v2.7 → v3.0); each generation preserved the methodology while migrating the substrate (Word docs → Markdown-in-git → CSV+Pydantic+Supabase). This pattern is the **load-bearing doctrine**: methodology is the source of truth; substrate is the implementation; substrate transitions are operationally costly but methodologically-preservable.

Three principles follow:

1. **Methodology-portability is a non-negotiable axis.** Any substrate considered for canonical status must preserve the operator's ability to evolve the methodology without forced substrate migration. Substrates that lock methodology into proprietary vendor-managed state (e.g., closed transcript storage that cannot export to git-canonicals) are rejected on this axis regardless of other scoring.

2. **Substrate continuity favors incremental evolution over discontinuous migration.** Per the past-PoC translation matrix (Thread D of the Q2 2026 audit), AKOS substrate has been incrementally evolved with OpenClaw thin-adapter emerging from deliberate I10/I11 governance posture (Path B sandbox + RBAC-as-config + permission truth). Discontinuous migrations (e.g., pure-Cursor-SDK migration that abandons OpenClaw) lose governance-design accumulated across initiatives; the burden of proof for discontinuity is high.

3. **The substrate audit must run faster than the substrate landscape changes.** Per the founder framing 2026-05-16 (*"the fact that even Cursor SDK is in beta is something we need to capitalize"*), substrate intelligence has competitive-window value when current; quarterly cadence is the default with explicit ad-hoc updates when material substrate events occur (e.g., GA transitions, major version bumps, regulatory enforcement dates).

## §5 The Madeira-substrate question is structurally different from the AKOS-substrate question

A specific principle worth naming explicitly: **the substrate AKOS runs on is not necessarily the substrate Madeira ships on**. AKOS is Holistika's own operating system; Madeira (when productized) is a product distributed to customers. The two have different substrate optimization functions:

- **AKOS substrate** optimizes for governance fit + cost + lock-in resistance + methodology continuity. Holistika controls the substrate choice end-to-end; the operator-facing UX matters but is balanced against governance discipline.
- **Madeira substrate** optimizes for operator-interaction polish + customer-ready UX + productization-shape fit. The substrate must compete with Glean / Anthropic Projects / Cursor itself for "intelligence layer beneath the interface" positioning.

These optimization functions can converge (hybrid pattern per `D-IH-84-B` Option B3 — Cursor SDK frontend for operator-interaction polish + OpenClaw policy backend for governance discipline) but they CAN also diverge (e.g., AKOS stays on OpenClaw thin-adapter while Madeira productizes as `@holistika/madeira-agent` library — D1 productization shape per `D-IH-84-D`). Per the I74 + I76 candidate framings, the Madeira-substrate question gets resolved at I76 P0 (post-`D-IH-84-C` AIC framing ratification) + I74 P4 (post-`D-IH-84-D` productization shape ratification); the AKOS-substrate question resolves at I84 P4 `D-IH-84-B` ratification.

## §6 Cross-references back to the agentic triangle

This canonical is one corner of the substrate governance triangle. The other two corners:

- **The how** — [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md). Framework rows; KB infrastructure dimensions; MCP postures; tooling matrix. Tech Lab maintains; Research consults at audit cycles.
- **The why and what (agentic)** — [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md). Agentic as discipline-of-disciplines; Madeira role-class; consent-to-consume; KB-access posture. Cross-references this canonical when its claims depend on which substrate enables which agentic posture.

The triangle is load-bearing across the three areas. Substrate landscape doctrine (this canonical) is the youngest corner — minted at I84 P3 from `D-IH-84-G`. Quarterly cadence per `D-IH-84-H` keeps it fresh; cross-area breakthrough propagation per [`SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md`](../../../People/canonicals/SOP-PEOPLE_CROSS_AREA_BREAKTHROUGH_001.md) pings the Tech Lab landscape canonical when the substrate audit produces material change.

## §7 Maintenance

Owned by **Research Lead** (or **KM Officer** + **Founder** interim per `D-IH-84-H` ratification pending Research Director hire — see [`i75-research-area-governance.md`](../../../../../../wip/planning/_candidates/i75-research-area-governance.md) Strand C). Co-authors: **System Owner**, **Tech Lead**. Cadence: quarterly review default per `D-IH-84-H`; off-cycle revision when:

- Material substrate event (GA transition, major version bump, regulatory enforcement date).
- New substrate emerges that warrants canonical row mint.
- Existing substrate sunsets or migrates status to `deprecated`.
- Cross-area breakthrough propagation pings from Tech Lab (`AGENTIC_FRAMEWORK_LANDSCAPE.md` extension) or People (`HOLISTIKA_AGENTIC_DOCTRINE.md` revision).

Verified mechanically by [`scripts/validate_substrate_registry.py`](../../../../../../../../scripts/validate_substrate_registry.py) (registry-row validator; enforces 18-column schema + 8 enum frozensets) + the paired runbook [`scripts/peopl_research_substrate_audit_cadence.py`](../../../../../../../../scripts/peopl_research_substrate_audit_cadence.py) per `D-IH-84-G` + master-roadmap §3 P6 contract (cadence runbook lands when SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md is minted; status:review until process_list.csv row mint per SOP-META ordering).

## §8 Cross-references

- [`AGENTIC_FRAMEWORK_LANDSCAPE.md`](../../../../Envoy%20Tech%20Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md) — Tech-Lab how.
- [`HOLISTIKA_AGENTIC_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md) — People why-and-what.
- [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../../People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) — People manifesto framing.
- [`SUBSTRATE_REGISTRY.csv`](../../../People/Compliance/canonicals/dimensions/SUBSTRATE_REGISTRY.csv) — canonical state-of-record (companion to this doctrine).
- [`SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md`](SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md) — paired SOP (forthcoming at master-roadmap §3 P6 closure; status:review until process_list row mint).
- [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md`](../../../../../../wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md) — I84 initiative; this canonical is its P6 deliverable (minted at P3 per operator Option A ratification 2026-05-17 ahead of original phase order).
- [`PRECEDENCE.md`](../../../People/Compliance/canonicals/PRECEDENCE.md) — registers this canonical as canonical status:review.
- [`akos-people-discipline-of-disciplines.mdc`](../../../../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) Rule 3 — discipline-of-disciplines pattern (applied recursively to Research-area).

## §9 Status

**status: review** per master-roadmap §3 P6 + SOP-META ordering. Promotes to **status: active** after the process_list.csv row `env_tech_dtp_substrate_landscape_mtnce_001` is minted (operator-gated tranche; not in this commit). Promotion authorisation: Founder + Research Lead (or KM Officer interim per `D-IH-84-H`).
