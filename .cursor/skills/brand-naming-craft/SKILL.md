---
name: brand-naming-craft
description: Use when proposing, evaluating, or governing a brand NAME or its DOMAIN in this AKOS workspace — a new sub-mark or product brand, a primary brand domain, a showcase/demo host, or any GTM naming decision. Composes the three governance silos that already exist but are unwired — brand architecture (Marketing), trademark clearance (Legal), and domain topology (Tech) — into one accurate decision flow with the correct RACI, so naming work meets the quality bar instead of falling between areas. Triggers on phrases like brand name, sub-mark, product brand, naming candidate, brand domain, domain strategy, showcase domain, trademark clearance, wordmark, GTM domain, rename, holistikaresearch.com, register a domain, domain availability. Pairs with SOP-TRADEMARK_NAMING_GOVERNANCE_001 (the Legal process) + BRAND_ARCHITECTURE.md + SUBDOMAINS_REGISTRY.md; this skill is the composed HOW.
ratifying_decisions: D-IH-86-FK; D-IH-66-A; D-IH-62-P
authored: 2026-05-31
version: 1.0.0
---

# Brand-Naming Craft

> Minted because the quality bar on a brand-domain task was missed — not for lack of doctrine, but because brand naming (Legal), brand architecture (Marketing), and domain topology (Tech) were **governed in three silos and never composed**. This skill is the composed path. Read it before proposing any brand name or domain.

## The RACI (operator-corrected 2026-05-31 — area-director accountability)

- **Accountable: CMO** (Marketing area director). Brand & Narrative Manager represents the CMO chain; CMO reports to Founder, so the chain is preserved without escalating accountability to the Founder.
- **Responsible:** Brand & Narrative Manager (name proposal + brand fit) · Legal Counsel (trademark clearance) · System Owner / Domain Specialist (domain topology + DNS).
- **Consulted:** Founder (up-chain; **retains the new-mark trademark-filing approval gate** — `SOP-TRADEMARK_NAMING_GOVERNANCE_001` Step 6) · MKT/GTM.
- **Informed:** Operations.
- **Principle (reusable):** each area's governance accountability lives at its **area-director** level even when the area is currently thin. Escalating to the Founder or sibling areas to compensate for a weak area **bloats** those roles. Craft RACI with this accuracy across areas.

## The composed decision flow (the four silos, joined)

Run these in order; do not skip to domains before the name clears brand + trademark.

### 1. Brand fit (Marketing — `BRAND_ARCHITECTURE.md` + `BRAND_ABBREVIATIONS.md`)
- Place the candidate in the Branded House: umbrella (`Holistika`) / sub-mark (`Holistika R&S` · `Think Big` · `HLK Tech Lab`) / product brand (`MADEIRA` · `KiRBe` · `ENVOY` · …). The umbrella never disappears behind a sub-brand.
- Reject register-collapse: forbidden short-forms per `BRAND_ABBREVIATIONS.md` (e.g. bare `HLK`/`MA`/`KB`/`TB`); paired forms (`HLK Tech Lab`) are allowed.
- Map the voice tier (Tier-1 master vs Tier-2 sub-mark) per `BRAND_REGISTER_MATRIX.md`.

### 2. Trademark clearance (Legal — `SOP-TRADEMARK_NAMING_GOVERNANCE_001`)
- For a **new sub-mark or product brand**, this is mandatory: the 8-step Legal process (collision-risk grade → EUIPO/OEPM/WIPO clearance → filing strategy → **Founder + Brand Manager hard pause at Step 6** → filing). Domain is the *fourth* filter, after trademark clears (do not fall in love with a name before clearance).
- For a **domain-only** decision on an existing mark (e.g. choosing the primary `Holistika` domain), trademark is already settled — proceed to step 3, Consult Legal only on cross-jurisdiction domain conflicts.

### 3. Domain availability + topology (Tech — `SUBDOMAINS_REGISTRY.md` + Vercel/Cloudflare)
- Check availability + price with the Vercel MCP `check_domain_availability_and_price` (read-only; never auto-purchase — registration is an operator action).
- Topology lives in `SUBDOMAINS_REGISTRY.md` (the I62 canon: `erp.*` = authenticated operator / `madeira.*` = public demo with `demo.*` + **no service-role key** + brand CI / `status.*` = public). **DNS is in Cloudflare** (registrar GoDaddy); there is **no Cloudflare MCP** provisioned — DNS record changes go via the Cloudflare dashboard or `wrangler`/API; the Vercel custom-domain side is MCP-verifiable. Update the registry row through a PR (`validate_subdomains_registry.py` gates it).

### 4. Make / buy / broker (the "do we have it or build/buy it" frame)
- A premium-TLD exact-match name is often taken. Decide explicitly: **coin** a new mark (Legal clearance + cheap domain), **buy/broker** the exact `.com` (get a real quote — don't assume "impossible"), or **keep + improve** the current domain. Record the decision; do not let it drift.

## The naming bar (grounded in 2026 external research)

- Keep the **exact brand string** across every surface — a variant on a weak TLD splits AI entity authority.
- `.com` = trust/enterprise + resale gold; `.co` ≈ as trusted now; `.ai` = AI-native signal but saturating; `.dev`/`.xyz` mis-signal or weaken. A `.com` with **brand root + category descriptor** (e.g. `holistikaresearch.com`) is a *strong* AI-entity signal — its only weakness is verbal/channel length.
- Short · pronounceable · spellable · memorable · trademarkable — in that order. Domain availability is the fourth filter, after trademark clearance.

## Anti-patterns

- **Domain-before-name / logo-before-clearance** — sunk-cost pressure to ship a name that hasn't cleared trademark. Clear first.
- **Naming without Brand Manager** (or without the CMO-accountable RACI) — produces register/architecture drift.
- **Treating the demo host as the real ERP** — `erp.*` is the authenticated workspace; the public demo is a *separate* showcase host (`demo.*`, no service-role key). Never collapse them.
- **Register-collapse** — bare forbidden short-forms or internal-jargon leakage to an external surface (`validate_brand_jargon.py` / `validate_brand_baseline_reality_drift.py`).
- **Escalating accountability to the Founder** to prop up a thin area — keep it at the area-director (CMO) level.
- **Coined rebrand mid-GTM** — splits entity authority + costs authority-rebuild; avoid unless strategically chosen.

## Cross-references

- The WHEN/process: [`SOP-TRADEMARK_NAMING_GOVERNANCE_001.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md).
- Brand architecture: [`BRAND_ARCHITECTURE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ARCHITECTURE.md) + [`BRAND_ABBREVIATIONS.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_ABBREVIATIONS.md) + `BRAND_REGISTER_MATRIX.md`.
- Domain topology: [`SUBDOMAINS_REGISTRY.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md) + `validate_subdomains_registry.py`.
- Capability frame: [`HOLISTIKA_CAPABILITY_DOCTRINE.md`](../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_CAPABILITY_DOCTRINE.md) §8.5 "Make / buy / outsource frame" (added per D-IH-86-FK).
- Worked memo: `docs/wip/intelligence/brand-domain-naming-2026-05-31/brand-domain-options-and-governance-gap.md`.
- Sister skills: [`brand-baseline-reality-craft`](../brand-baseline-reality-craft/SKILL.md) (register translation) · [`external-render-craft`](../external-render-craft/SKILL.md) (external surfaces).
- Decisions: D-IH-86-FK (this mint) · D-IH-66-A (Branded House) · D-IH-62-P (subdomain topology).
