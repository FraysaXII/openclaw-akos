---
sop_id: SOP-TRADEMARK_NAMING_GOVERNANCE_001
title: Trademark Naming Governance — adding new sub-marks or product brands
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: hol_lgl_prc_trademark_naming_governance_001
role_owner: Legal Counsel
role_parent_1: CPO
area: Legal
entity: Holistika
governance:
  - D-IH-66-A (Branded House architecture)
  - D-IH-66-C (per-jurisdiction filing matrix)
  - D-IH-66-V (sub-mark/product-brand introduction governance)
linked_initiative: I66
created: 2026-05-09
last_review: 2026-05-09
sister_sops:
  - SOP-LEGAL_TRADEMARK_MONITORING_001
  - SOP-LEGAL_IP_REGISTER_MAINTENANCE_001
---

# SOP-TRADEMARK_NAMING_GOVERNANCE_001 — Trademark Naming Governance

> Legal-Counsel-owned **per-introduction process** that governs the addition of a new sub-mark or product brand into Holistika's trademark portfolio. Sister to `SOP-LEGAL_TRADEMARK_MONITORING_001` (which monitors existing marks) and `SOP-LEGAL_IP_REGISTER_MAINTENANCE_001` (which maintains the standing register).

## 1. Purpose and scope

When the Founder + Brand Manager identify a need for a **new sub-mark** (a fourth operational arm beyond Holistika R&S / Think Big / HLK Tech Lab) or **new product brand** (beyond MADEIRA / KiRBe / ENVOY / InfraMonitor / Financial Analyst), this SOP governs the process from **naming candidate** to **filed mark**.

Without this SOP, the failure modes are:

- A naming candidate is committed to (logo created, copy written, public surfaces deployed) before a clearance search reveals a fatal collision.
- A new mark is filed in classes inconsistent with the Branded House architecture.
- A new mark is named in a register-collapsing form (forbidden short-form per `BRAND_ABBREVIATIONS.md`; or external-register leakage of internal vocabulary).

Out of scope: post-filing opposition response (covered by `SOP-LEGAL_TRADEMARK_MONITORING_001`); renewal calendar (same).

## 2. Cadence

**Per-introduction** (no fixed cadence). Trigger: Founder or Brand Manager proposes a new sub-mark or product brand.

## 3. Inputs

- Naming candidate (string — wordmark form).
- Proposed positioning: sub-mark vs product brand.
- Proposed Nice class scope (target goods/services).
- `BRAND_ARCHITECTURE.md` and `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` (architectural constraints).
- `BRAND_ABBREVIATIONS.md` (short-form governance).
- `BRAND_LOGO_SYSTEM.md` (if a design mark is also proposed).

## 4. Process steps

### Step 1 — Naming candidate review (15 min)

Before any clearance search, validate the candidate against canonical constraints:

- **Branded House compatibility**: Does the candidate fit as a sub-mark (delivery-mode-specific) or product brand (technology product)? Reject if it would conflict with the umbrella `Holistika` (e.g., "Holistika Plus" reads as a tier of the umbrella, not a separate mark).
- **Abbreviation governance** (per `BRAND_ABBREVIATIONS.md`): Is the candidate a forbidden short-form (HLK, MA, KB, EV, TB, TL, HRS standalone)? Reject. Is it a paired form (e.g., "HLK Tech Lab") that complies with §2.1? Allowed.
- **Visual canonicals** (per `BRAND_LOGO_SYSTEM.md`): Does the candidate require a paired wordmark with the umbrella (per Tier-2 sub-mark visual rules)? Document.
- **Voice tier mapping** (per `BRAND_REGISTER_MATRIX.md`): Which tier (Tier-1 R&S vs Tier-2 ops/tech) does this mark live in? Document.

### Step 2 — Pre-search collision-risk assessment (30 min)

Without yet running clearance, assess collision risk based on the candidate's properties:

- **Generic-phrase risk**: How common is the candidate phrase in business/motivational/technology literature? (Think Big = high; KiRBe = low.)
- **Geographic-name risk**: Does the candidate share any geographic-name (city, region, country)? (MADEIRA = high; ENVOY = nil.)
- **Existing-product-name risk**: Quick Google search for `<candidate>` + industry keywords. Flag any operating company in similar Nice scope.
- **Cultural-translation risk**: Does the candidate carry unintended meaning in any target-market language (Spanish, French, German, Portuguese)? Brand Manager review.

Output: a **collision-risk grade** (low / medium / high / very-high) that drives the clearance search depth + filing strategy.

### Step 3 — Formal clearance search (60-180 min, scaled to risk grade)

Per `TRADEMARK_FILING_STRATEGY_2026-05.md` §3, run the standard clearance template:

1. EUIPO eSearch — exact + 1-edit-distance + phonetic similarity.
2. OEPM Sitadex — same.
3. WIPO Madrid Monitor — international register.
4. EU corporate-register cross-reference.
5. Domain-name cross-reference.
6. Common-law usage scan (Google).

Document each search's hits in a per-mark `clearance-<mark-slug>-<YYYY-MM>.md` under `_assets/legal/trademark-clearance/`.

### Step 4 — Filing-strategy decision (30 min, founder + counsel)

Based on collision-risk grade + clearance findings:

- **Low/no collision**: standard EUIPO + OEPM both jurisdictions; broad Nice scope.
- **Medium collision**: EUIPO + OEPM both; narrower Nice scope per the high-risk classes; coexistence-agreement template prepared in case opposition surfaces.
- **High collision**: EUIPO-only OR OEPM-only (national-scope-only); narrow Nice scope; brand protection in unclaimed jurisdictions via use-in-trade.
- **Very-high collision**: defer filing; brand-protect via use-in-trade only; revisit when commercial validation justifies the cost of fighting opposition.

Document the decision + rationale in `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` (append to §3 or dedicated section for the new mark).

### Step 5 — Filing prep (60 min, counsel)

Per `TRADEMARK_FILING_STRATEGY_2026-05.md` §5 template, produce ready-to-sign data for the new mark:

- Frozen filing string.
- Applicant block (Holistika Research SL).
- Per-jurisdiction Nice classes + goods/services translations (EN for EUIPO; ES for OEPM).
- Disclaimers / limitations (e.g., for high-collision marks — explicit class-exclusion language).

### Step 6 — Operator approval gate (founder + Brand Manager)

Before filing, founder + Brand Manager confirm:

1. Naming candidate is brand-coherent (passes Step 1 governance).
2. Collision-risk grade is acceptable for the filing strategy chosen (Step 4).
3. Filing-day budget is allocated (per `BRAND_HIERARCHY` §5 fee guidance + filing-agent quote).
4. Operator-side power-of-attorney is in place.

This is a **mandatory hard pause** per `akos-agent-checkpoint-discipline.mdc` — new trademark filings warrant operator-pause-point review.

### Step 7 — Filing submission (counsel-driven)

Counsel transcribes Step 5 data into EUIPO TM-1 / OEPM portal, submits, captures filing receipt + filing number, updates the IP register (per `SOP-LEGAL_IP_REGISTER_MAINTENANCE_001`).

### Step 8 — Post-filing (governed by sister SOPs)

Hand off to:

- `SOP-LEGAL_TRADEMARK_MONITORING_001` — quarterly status + opposition + renewal calendar.
- `SOP-LEGAL_IP_REGISTER_MAINTENANCE_001` — quarterly register snapshot.

## 5. Outputs

- Per-mark naming review record (Step 1 output).
- Per-mark clearance search record (Step 3 output).
- Filing-strategy decision in BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md (Step 4 output).
- Per-mark filing-prep packet in TRADEMARK_FILING_STRATEGY (or appended) (Step 5 output).
- Filing receipt + filing number (Step 7 output).
- IP register update (Step 8 output).

## 6. Anti-patterns

- **Logo-first commit.** Designing a logo before clearance is complete creates sunk-cost pressure to file even if collision risk surfaces. Always do clearance before visual investment.
- **Class-bloat filing.** Filing in many Nice classes "just in case" is expensive (per-class fees) and generates opposition risk in classes where Holistika doesn't actually operate. Always file the narrowest scope that captures actual product use.
- **Naming-without-Brand-Manager.** Founder-driven naming without Brand Manager sign-off can produce marks that conflict with voice tier / register matrix / abbreviation governance. Brand Manager is a non-skippable Step 1 reviewer.
- **Skipping Step 6 operator gate.** Filings are budget-material + brand-strategy-material; never skip the founder approval pause.

## 7. Cross-references

- [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) — architectural constraints.
- [`TRADEMARK_FILING_STRATEGY_2026-05.md`](TRADEMARK_FILING_STRATEGY_2026-05.md) — per-mark filing-prep template.
- [`BRAND_ABBREVIATIONS.md`](../../Marketing/Brand/BRAND_ABBREVIATIONS.md) — short-form governance.
- [`BRAND_LOGO_SYSTEM.md`](../../Marketing/Brand/BRAND_LOGO_SYSTEM.md) — visual canonicals.
- Sister SOPs: `SOP-LEGAL_TRADEMARK_MONITORING_001.md`, `SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md`.
- D-IH-66-A (Branded House), D-IH-66-V (this SOP introduction).
