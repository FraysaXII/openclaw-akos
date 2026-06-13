---
title: Brand-domain + naming — options research (WIP) + governance-harmonization gap
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP;J-AIC
access_level: 5
authored: 2026-05-31
last_review: 2026-05-31
status: research-incomplete
role_owner: Brand & Narrative Manager
accountable_role: CMO (Marketing area director)
responsible_roles: Brand & Narrative Manager; Legal Counsel; System Owner/Domain Specialist
consulted_roles: Founder (up-chain; retains new-mark trademark-filing gate per SOP Step 6); MKT/GTM
informed_roles: Operations
raci_principle: Accountability sits at the area-director level even for thin areas; escalating to Founder/siblings to compensate bloats those roles.
linked_decisions:
  - D-IH-86-FK
parent_plan: routing_and_wiring_788b66e3.plan.md (I92 + emergent §16; brand-domain governance executed early via the active I86 coordinator as D-IH-86-FK)
research_status_note: >-
  Naming taste bar NOT yet met (operator 2026-05-31). This note captures the availability
  reality + the governance-harmonization gap; the naming options continue under a properly
  governed path (below). Domain decision DEFERRED — keep holistikaresearch.com for now.
---

> **Domain note (2026-06-13):** The string `holistika.com` is **not** Holistika's product domain (external party). §1–§3 below are naming-research availability notes only — **not** live hosts. Product SSOT: `holistikaresearch.com` per [SUBDOMAINS_REGISTRY.md](../../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md).

# Brand-domain + naming — options (WIP) + the governance gap

> Operator framing 2026-05-31: the domain-name candidates did not meet the taste bar; the
> deeper issue is that this topic is **not properly wired/governed** — "the quality bar has
> not been met maybe we lack capabilities or we have not properly harmonized them." This note
> is the durable artifact so the topic is **not lost tomorrow**. Decision is the operator's.

## 1. Availability reality (Vercel MCP, read-only — no purchases)

- **Taken on every premium TLD:** `holistika.com`, `.ai`, `.co`, `.io`, `.app`, `.tech`, `.org`; also `hlk.ai`.
- **Available:** `getholistika.com` ($11.25/yr), `holistika.dev` ($9.99/yr).
- `holistika.com` is owned by a third party; GoDaddy brokerage quoted >$5k + owner ask (operator: felt impossible).

## 2. External best practice (2026)

`.com` = trust/enterprise + resale gold standard; `.ai` = AI-native signal but saturating; `.co` ≈ as trusted as `.com`; keep the **exact brand string** (a variant on a weak TLD splits AI entity authority); short / pronounceable / spellable / memorable / trademarkable; domain is the *fourth* filter after trademark. A `.com` with **brand root + category descriptor** (i.e. `holistikaresearch.com`) is a **strong** AI-entity signal.

## 3. Options + recommendation (DEFERRED per operator)

- **(1) Acquire `holistika.com` via brokerage** — exact-match `.com`, the entity-coherence + GTM winner. Get a *real* quote (don't assume impossible).
- **(2) `getholistika.com` ($11.25)** — cheap `.com` bridge; mild "get" friction.
- **(3) Keep `holistikaresearch.com`** — a strong entity signal; only weakness is verbal/channel length → mitigate with a short consistent handle. **Operator choice for now.**
- **(4) `holistika.dev` ($9.99)** — exact string but `.dev` mis-signals "dev tool"; not as primary (operator noted the misunderstanding risk).
- **(5) Coined rebrand** — avoid mid-GTM (splits entity authority).

**Recommendation:** keep `holistikaresearch.com` for now; defensively register `getholistika.com` + `holistika.dev` (~$21/yr insurance, operator action); pursue a real `holistika.com` brokerage quote as the strategic MKT decision. Operator will choose a domain when one meets the taste bar; naming proposals continue under the governed path (§5).

## 4. The governance gap (the real finding — harmonization, not absence)

The pieces exist but are **siloed + unrated + un-composed + not agent-wired**:

- **Legal** owns naming: `SOP-TRADEMARK_NAMING_GOVERNANCE_001.md` + `CAP-HOL-LGL-PRC-TRADEMARK-NAMING-GOVERNANCE-001` — with a **duplicate** row `CAP-THI-LEGAL-DTP-303` (same process).
- **Marketing/Brand** owns architecture: `BRAND_ARCHITECTURE.md` (Branded House) + `BRAND_ABBREVIATIONS.md` + brand-canon/voice processes.
- **Tech** owns topology: `SUBDOMAINS_REGISTRY.md` + `validate_subdomains_registry.py` + DNS tasks (Domain Specialist). DNS lives in Cloudflare; registrar GoDaddy.
- **Capability maturity:** all related rows `i81_verdict: partial` + `seed_v1_unrated` confidence `1.0`; `HOLISTIKA_CAPABILITY_DOCTRINE.md` still `status: review`; I82 P3-P7 (real ratings) planned.
- **Genuine gaps:** (a) **domain *strategy*** capability (vs DNS topology) — none; (b) a **make/buy/outsource frame** in the capability doctrine — none; (c) an **agent naming/domain craft skill** — none.

**Diagnosis:** primarily a **harmonization gap**; secondarily a **capability-maturity gap**. Not an absence of doctrine.

## 5. Governance wiring + RACI (MINTED 2026-05-31 via D-IH-86-FK)

A composed, agent-wired "brand-name + domain decision" path that spans the three silos:

- **RACI (operator-corrected 2026-05-31 — accountability at the AREA-DIRECTOR level, not escalated to Founder):** **Accountable:** **CMO** (Marketing area director; Brand & Narrative Manager represents the CMO chain; CMO reports to Founder, so the chain is preserved without bloating the Founder role). **Responsible:** Brand & Narrative Manager (naming proposals + brand fit) · Legal Counsel (trademark clearance) · System Owner / Domain Specialist (DNS topology + `SUBDOMAINS_REGISTRY`). **Consulted:** Founder (up-chain; **retains the new-mark trademark-filing approval gate** per SOP Step 6) · MKT/GTM. **Informed:** Operations.
- **Principle (reusable, operator 2026-05-31):** each area's governance accountability lives at its **area-director** level even when the area is currently thin — escalating to the Founder or sibling areas to compensate for a weak area bloats those roles. Craft RACI with this accuracy across all areas (candidate broader People/org-governance principle).
- **Four fixes — MINTED 2026-05-31 (operator-approved; canonical-CSV/SOP/doctrine gate cleared) via D-IH-86-FK:**
  1. **[DONE]** Composed `SOP-BRAND_DOMAIN_NAMING_001.md` (Marketing/Brand) + process row `tbi_mkt_prc_brand_domain_naming_001` joining `BRAND_ARCHITECTURE` + `SOP-TRADEMARK_NAMING_GOVERNANCE_001` + `SUBDOMAINS_REGISTRY` into one governed brand-name+domain decision flow with the RACI above.
  2. **[DONE]** Deduped `CAP-THI-LEGAL-DTP-303` (now `lifecycle_status: deprecated`) → canonical `CAP-HOL-LGL-PRC-TRADEMARK-NAMING-GOVERNANCE-001` in `CAPABILITY_REGISTRY.csv`.
  3. **[DONE (frame) / DEFERRED (registry row)]** Added the **make/buy/outsource** frame to `HOLISTIKA_CAPABILITY_DOCTRINE.md` §8.5. The separate domain-*strategy* `CAPABILITY_REGISTRY` row is deferred to the Capability Curator via I82's own flow (real confidence rating, not a seed) to avoid stepping on I82's mid-flight mint.
  4. **[DONE]** Minted `.cursor/skills/brand-naming-craft/SKILL.md` composing `BRAND_ARCHITECTURE` + `BRAND_ABBREVIATIONS` + the Legal SOP + `SUBDOMAINS_REGISTRY` + the make/buy frame + the naming bar.
- **Confidence:** real ratings land when I82 P3 runs (replaces the seed `1.0`).

## 6. Cross-references

- Plan: `routing_and_wiring_788b66e3.plan.md` (I92 P0.5 + emergent §16). Ratifying decision realized as **D-IH-86-FK** (`DECISION_REGISTER.csv`) — executed early via the active I86 coordinator since I92 is not yet chartered; when I92 charters it adopts D-IH-86-FK as a pre-charter governing decision.
- `BRAND_ARCHITECTURE.md`; `BRAND_ABBREVIATIONS.md`; `SOP-TRADEMARK_NAMING_GOVERNANCE_001.md`; `SUBDOMAINS_REGISTRY.md`; `HOLISTIKA_CAPABILITY_DOCTRINE.md`; `CAPABILITY_REGISTRY.csv` + `CAPABILITY_CONFIDENCE_REGISTRY.csv`.
- `akos-brand-baseline-reality.mdc`; `akos-applied-research-discipline.mdc` (this note's grounding).
