---
purpose: working space for CORPINT-research artefacts that are not yet promoted to canonical
access_level: 5
audience: operator + cleared collaborators + agents
register: internal
governance: D-IH-66-P (intelligence working-space), D-IH-66-M (dual-register contract)
created: 2026-05-08
status: active
---

# `docs/wip/intelligence/` — CORPINT-research working space

This is the **internal working space** for CORPINT-research artefacts produced by Holistika's research methodology. It holds three classes of working artefact, all of which carry the **internal register** (counterparty, elicitation, reliability grading, intelligence collection, intelligence report, approach techniques, baseline reality assessment) and are **never** rendered directly to non-cleared audiences.

## What lives here

### 1. Per-engagement counterparty briefs (in-flight)

Pre-engagement work-in-progress for an upcoming counterparty interaction (investor pitch, advisor onboarding, ENISA review, partner kickoff, customer discovery). Files use the naming convention:

```
docs/wip/intelligence/<YYYY-MM-DD>-<counterparty-slug>/
├── counterparty-brief.md        # baseline reality assessment
├── elicitation-plan.md          # intended approach techniques
├── source-grade.csv             # per-source reliability grading (Admiralty A-F × 1-6)
└── notes/                       # raw transcripts (post-redaction)
```

When the engagement closes (deck delivered, partner signed, ENISA submitted), the artefacts are either:

- **Archived** to `docs/_assets/transcripts/` (post-redaction; brand-voice pattern source per P1) **and / or**
- **Promoted** to a per-engagement `.counterparty-brief.md` companion alongside the deck under `docs/references/hlk/v3.0/_assets/advops/<engagement-slug>/` (per I66 P6 deck companion structure).

### 2. Reusable elicitation templates (per-audience)

Stored under `docs/wip/intelligence/_templates/`:

- `elicitation-template-investor.md` — discovery questions tuned for investor counterparties.
- `elicitation-template-customer-sme.md` — discovery questions for SME customer engagements.
- `elicitation-template-advisor.md` — onboarding-call elicitation for incoming advisors.
- `elicitation-template-enisa.md` — evidence-gathering checklist for ENISA evidence body.
- `elicitation-template-partner.md` — partner-fit elicitation.
- `elicitation-template-recruiter.md` — recruiter / hiring-manager elicitation.

Templates evolve with each engagement; the SOP-IO_ELICITATION_DISCIPLINE_001 process (P3) governs their use.

### 3. Per-engagement intelligence reports (in-flight)

Working drafts of intelligence reports — the structured deliverable produced after a counterparty interaction. These are the **internal-register form** of what becomes a customer-facing engagement report or a research brief in the external register. They are governed by SOP-IO_INTELLIGENCE_REPORT_001 (P3) which encodes the BLUF / source-grading / ICD-203-aligned structure (adapted, not literal).

## What does **not** live here

- **External-register artefacts.** Decks, dossiers, founder bios, press kits, public copy — all of these go under `docs/references/hlk/v3.0/_assets/advops/` (decks/dossiers/companions) or sibling repos (`boilerplate/`, `hlk-erp/`).
- **Canonical SOPs.** The four HUMINT-derived SOPs (`SOP-IO_*_001.md`) live in `docs/references/hlk/v3.0/Admin/O5-1/Operations/IntelligenceOps/`, not here.
- **Canonical patterns.** Brand-voice patterns belong in `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_*_PATTERNS.md`. This working space sources patterns; it does not store them.
- **Personal data.** Per the dual-register contract, redaction is a precondition for **any** transcript or note that survives the engagement window. Raw audio / unredacted transcripts must not enter this directory; they live in operator-private storage outside the repo.

## Access discipline

- **Access level: 5** (operator + cleared collaborators + named agents under explicit invocation).
- **No agent autonomous browsing.** Agents read this directory only when explicitly invoked with a counterparty-engagement task referencing a specific subdirectory.
- **No mirror to runtime.** Unlike `compliance/` mirrored CSVs, this working space is git-only. It is never replicated to Supabase, Neo4j, or any operator-surface query layer.
- **Redaction-first.** Any artefact entering this directory must be redacted: PII removed, third-party-named entities anonymised, financial figures rounded or removed, identifying timestamps generalised. The redaction discipline is governed by SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001 §"Redaction protocol".

## Cross-references

- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) — dual-register canonical (P1); §3 translation table is the SSOT for register translation.
- [`.cursor/rules/akos-brand-baseline-reality.mdc`](../../../.cursor/rules/akos-brand-baseline-reality.mdc) — rule governing register selection in agent-authored prose.
- [`scripts/validate_brand_baseline_reality_drift.py`](../../../scripts/validate_brand_baseline_reality_drift.py) — drift gate that asserts internal-register tokens never leak to external surfaces.
- IntelligenceOps SOPs (P3): `docs/references/hlk/v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_*.md`.
- D-IH-66-P (this working-space decision) in `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md`.
