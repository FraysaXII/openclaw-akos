---
sop_id: SOP-BRAND_DOMAIN_NAMING_001
title: Brand-Name and Domain Naming Decision — composing brand fit, trademark clearance, and domain topology
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: tbi_mkt_prc_brand_domain_naming_001
role_owner: Brand & Narrative Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-86-FK (brand-domain naming governance harmonization; this SOP mint + composed RACI)
  - D-IH-66-A (Branded House architecture)
  - D-IH-62-P (subdomain topology)
linked_initiative: I86
created: 2026-05-31
last_review: 2026-05-31
sister_sops:
  - SOP-TRADEMARK_NAMING_GOVERNANCE_001
  - SOP-BRAND_CANON_MAINTENANCE_001
---

# SOP-BRAND_DOMAIN_NAMING_001 — Brand-Name and Domain Naming Decision

> **CMO-accountable composition SOP.** Joins the three brand-name + domain governance capabilities that already exist but were never wired together — brand architecture (Marketing), trademark clearance (Legal), domain topology (Tech) — into one decision flow. It **orchestrates**, it does not duplicate: each silo's own SOP/registry stays the SSOT for its step. Minted because a brand-domain decision missed the quality bar not for lack of doctrine but for lack of composition (D-IH-86-FK). The *how* (worked craft) lives in the paired [`brand-naming-craft`](../../../../../../.cursor/skills/brand-naming-craft/SKILL.md) skill.

## 1. Purpose and scope

In scope: any decision about a **brand name** (new sub-mark / product brand) or the **domain** that carries a brand (primary brand domain, showcase/demo host, GTM domain), where the decision needs brand-fit + legal-clearance + domain-topology coherence at once.

Without composition, the failure modes are: a name chosen for domain availability that fails trademark clearance; a domain wired without brand-architecture coherence; a "broken/old" public surface that was actually an ungoverned public-vs-authenticated split; accountability escalated to the Founder because no area-director owned the decision.

Out of scope: the per-mark trademark filing mechanics (that is `SOP-TRADEMARK_NAMING_GOVERNANCE_001`, invoked at Step 2); the quarterly brand-canon review (`SOP-BRAND_CANON_MAINTENANCE_001`); DNS record mechanics (Cloudflare dashboard / `DNS_RECORDS.md`).

## 2. RACI (operator-ratified 2026-05-31 — area-director accountability)

| Role | RACI | Why |
|:---|:---|:---|
| **CMO** (Marketing area director) | **Accountable** | Brand-name + domain is a Marketing-area decision. Brand & Narrative Manager represents the CMO chain; CMO reports to Founder, so the chain is preserved without escalating accountability upward. |
| Brand & Narrative Manager | Responsible | Name proposal + brand-architecture fit. |
| Legal Counsel | Responsible | Trademark clearance (Step 2). |
| System Owner / Domain Specialist | Responsible | Domain availability + topology + DNS (Step 3). |
| Founder | Consulted | Up-chain; **retains the new-mark trademark-filing approval gate** (`SOP-TRADEMARK_NAMING_GOVERNANCE_001` Step 6). |
| MKT / GTM | Consulted | Channel + go-to-market implications of the name/domain. |
| Operations | Informed | — |

**Principle (reusable across areas):** each area's governance accountability lives at its **area-director** level even when the area is currently thin. Escalating to the Founder or sibling areas to compensate for a weak area bloats those roles.

## 3. Cadence

`on_demand` (per-decision). Trigger: a new sub-mark / product brand is proposed, OR a primary/showcase/GTM domain decision is needed, OR a rename is considered.

## 4. The composed decision flow (run in order)

### Step 1 — Brand-architecture fit (Marketing; Brand & Narrative Manager)
Place the candidate in the Branded House per [`BRAND_ARCHITECTURE.md`](canonicals/BRAND_ARCHITECTURE.md): umbrella (`Holistika`) / sub-mark / product brand. Reject register-collapse: forbidden short-forms per [`BRAND_ABBREVIATIONS.md`](canonicals/BRAND_ABBREVIATIONS.md); paired forms allowed. Map the voice tier per `BRAND_REGISTER_MATRIX.md`. **Gate:** a candidate that fails brand fit never reaches clearance.

### Step 2 — Trademark clearance (Legal; Legal Counsel) — only for a new mark
For a **new sub-mark or product brand**, invoke [`SOP-TRADEMARK_NAMING_GOVERNANCE_001`](../../People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md) in full (collision-risk grade -> EUIPO/OEPM/WIPO clearance -> filing strategy -> **Founder hard pause at its Step 6** -> filing). For a **domain-only decision on an existing mark**, trademark is settled — consult Legal only on cross-jurisdiction domain conflicts and proceed to Step 3. **Domain is the fourth filter, after clearance** — do not commit to a name before it clears.

### Step 3 — Domain availability + topology (Tech; System Owner / Domain Specialist)
Check availability + price with the Vercel MCP `check_domain_availability_and_price` (read-only; **never auto-purchase** — registration is an operator action). Resolve topology against [`SUBDOMAINS_REGISTRY.md`](../../Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md): `erp.*` = authenticated operator workspace / `madeira.*` (showcase project) = public demo with `demo.*` data + **no service-role key** + brand-jargon CI / `status.*` = public. **DNS is in Cloudflare** (registrar GoDaddy); there is no Cloudflare MCP provisioned — DNS record changes go via the Cloudflare dashboard / API, while the Vercel custom-domain binding is MCP-verifiable. Any registry change is a PR (`validate_subdomains_registry.py` gates it). **Reconcile drift**: if a live subdomain disagrees with the registry, that is a drift incident to fix, not to ignore.

### Step 4 — Make / buy / broker decision (CMO accountable)
Decide explicitly, and record it: **coin** a new mark (cheap domain + Legal clearance), **buy/broker** the exact premium-TLD `.com` (get a real quote — do not assume "impossible"), or **keep + improve** the current domain. This is the make/buy frame from `HOLISTIKA_CAPABILITY_DOCTRINE.md` §"Make / buy / outsource frame" applied to the brand-domain capability.

## 5. Acceptance criteria (paired per akos-executable-process-catalog Rule 1)

- **AC-HUMAN:** a human OR an AIC role_owner (Brand & Narrative Manager under CMO) can run Steps 1-4 from this SOP + the `brand-naming-craft` skill without invoking any script, surfacing the Step-2 Founder gate and the Step-4 make/buy decision via inline-ratify.
- **AC-AUTOMATION:** the existing validators enforce the mechanical parts unattended — `validate_subdomains_registry.py` (topology), `validate_brand_jargon.py` + `validate_brand_baseline_reality_drift.py` (register), and the Vercel MCP availability check. No new runbook script is minted; the automation is the composition of existing gates.

## 6. Outputs

- Brand-fit record (Step 1); trademark clearance + filing-strategy record (Step 2, via the Legal SOP); domain availability + topology decision + any `SUBDOMAINS_REGISTRY` PR (Step 3); make/buy/broker decision record (Step 4); a decision row when the choice is governance-material.

## 7. Anti-patterns

- **Domain-before-name / logo-before-clearance.** Clear trademark before committing.
- **Naming without the CMO-accountable RACI.** Produces register/architecture drift.
- **Treating the public demo host as the real ERP.** They are separate surfaces (`demo.*`, no service-role key).
- **Escalating accountability to the Founder** to prop up a thin area — keep it at CMO level.
- **Silo-hopping without composition** — running one silo's SOP and skipping the others is exactly the gap this SOP closes.

## 8. Cross-references

- Composed silos: [`BRAND_ARCHITECTURE.md`](canonicals/BRAND_ARCHITECTURE.md) + [`BRAND_ABBREVIATIONS.md`](canonicals/BRAND_ABBREVIATIONS.md) (Marketing) · [`SOP-TRADEMARK_NAMING_GOVERNANCE_001`](../../People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md) (Legal) · [`SUBDOMAINS_REGISTRY.md`](../../Envoy%20Tech%20Lab/Repositories/SUBDOMAINS_REGISTRY.md) (Tech).
- Make/buy frame: [`HOLISTIKA_CAPABILITY_DOCTRINE.md`](../../People/canonicals/HOLISTIKA_CAPABILITY_DOCTRINE.md) §"Make / buy / outsource frame".
- Paired skill (the *how*): [`brand-naming-craft`](../../../../../../.cursor/skills/brand-naming-craft/SKILL.md).
- Sister SOPs: `SOP-BRAND_CANON_MAINTENANCE_001`, `SOP-TRADEMARK_NAMING_GOVERNANCE_001`.
- Process row: `tbi_mkt_prc_brand_domain_naming_001` in `process_list.csv`.
- Worked memo: `docs/wip/intelligence/brand-domain-naming-2026-05-31/brand-domain-options-and-governance-gap.md`.
- Decisions: D-IH-86-FK (this mint) · D-IH-66-A (Branded House) · D-IH-62-P (subdomain topology).
