---
phase: P4
phase_name: Trademark + legal templates
initiative: I66
date: 2026-05-09
status: complete
operator_pause: pre-P5
package_kind: operator_handoff
governance: D-IH-66-H (agent role ends at "ready-to-sign"), D-IH-66-U (filing scope), D-IH-66-W (legal template suite)
---

# I66 P4 — Operator Handoff Package (2026-05-09)

> The agent's P4 deliverables are **ready-to-sign** per D-IH-66-H. This handoff package tells the operator exactly what counsel + filing agent + the operator themself need to do, in what order, with what supporting evidence, to convert P4 into filed trademarks + executed legal templates + published privacy/terms/cookies.

## What was shipped in P4 (this commit)

### Canonical legal documents (3)

| File | Purpose |
|:---|:---|
| [`v3.0/Admin/O5-1/People/Legal/TRADEMARK_FILING_STRATEGY_2026-05.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/TRADEMARK_FILING_STRATEGY_2026-05.md) | Master filing strategy: per-mark clearance worklist + per-mark filing strategy decision (EUIPO / OEPM / both; word / design; Nice scope) + ready-to-sign filing form data for 7 marks × ~10 filings + counsel handoff checklist + post-filing operations roadmap. |
| [`v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-TRADEMARK_NAMING_GOVERNANCE_001.md) | Per-introduction SOP for adding a new sub-mark or product brand to the portfolio (8-step process from naming candidate to filed mark, with mandatory operator-pause-point at Step 6). |
| (cross-canonical update) [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md) | No edits required — its forward-references to TRADEMARK_FILING_STRATEGY_2026-05.md (now created) + SOP-TRADEMARK_NAMING_GOVERNANCE_001.md (now created) all resolve. |

### Legal template suite (4)

Under [`v3.0/Admin/O5-1/People/Legal/_templates/`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/_templates/):

| Template | Purpose |
|:---|:---|
| [`LEGAL_TEMPLATE_MSA.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/_templates/LEGAL_TEMPLATE_MSA.md) | Master Services Agreement — 11 sections + Branded House anchoring (Holistika Research SL is sole contracting party; sub-marks named as delivery modes). |
| [`LEGAL_TEMPLATE_SOW.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/_templates/LEGAL_TEMPLATE_SOW.md) | Per-engagement Statement of Work — operationalises the proposal under SOP-ENG_PROPOSAL_001 into binding contract. References service catalog cells. |
| [`LEGAL_TEMPLATE_NDA.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/_templates/LEGAL_TEMPLATE_NDA.md) | Mutual NDA — typically executed before discovery + elicitation per SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT step 2. |
| [`LEGAL_TEMPLATE_DPA.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/_templates/LEGAL_TEMPLATE_DPA.md) | GDPR Article 28 Data Processing Agreement — Holistika as Processor of Client data. Includes Annex I/II/III templates. |

### Boilerplate legal-page drafts (3) — input for P5

Under [`reports/p4-boilerplate-legal-pages/`](p4-boilerplate-legal-pages/):

| File | Target route in boilerplate |
|:---|:---|
| [`privacy-policy-2026-05.md`](p4-boilerplate-legal-pages/privacy-policy-2026-05.md) | `boilerplate/app/privacy/page.tsx` |
| [`terms-of-service-2026-05.md`](p4-boilerplate-legal-pages/terms-of-service-2026-05.md) | `boilerplate/app/terms/page.tsx` |
| [`cookie-policy-2026-05.md`](p4-boilerplate-legal-pages/cookie-policy-2026-05.md) | `boilerplate/app/cookies/page.tsx` |

These are EN canonical drafts. P5 (boilerplate rewrite) translates to ES + FR per `BRAND_SPANISH_PATTERNS.md` / `BRAND_FRENCH_PATTERNS.md` voice rules and integrates into the consumer repo.

## What the operator must do next (sequenced)

### Track 1 — Trademark filings (1-3 weeks operator-driven)

**Step 1.1 — Engage filing agent / IP counsel** (operator decision; ~1 week)

- Choose between (a) Spanish IP boutique firm (cheaper; OEPM-fluent) or (b) EU-wide IP firm (more expensive; full-stack EUIPO + OEPM + Madrid Protocol). For 7 marks × 2 jurisdictions, recommendation: Spanish boutique with EUIPO experience.
- Sign engagement letter with chosen firm.
- Issue Power of Attorney (PoA) per the firm's template.

**Step 1.2 — Per-mark clearance searches** (counsel-driven; ~1 week)

- Counsel runs the 6-step clearance template per `TRADEMARK_FILING_STRATEGY_2026-05.md` §3 for each of the 7 marks.
- Pre-search collision-risk grades per `TRADEMARK_FILING_STRATEGY_2026-05.md` §3 expectations:
  - Holistika / Holistika R&S / KiRBe — low risk; standard searches.
  - HLK Tech Lab — medium; full searches.
  - Think Big / MADEIRA / ENVOY — high; full searches + collision-class identification.
- Per-mark output: `clearance-<mark-slug>-2026-05.md` document (operator may request these be stored in `_assets/legal/trademark-clearance/` for git tracking; or operator-private storage if counsel prefers).

**Step 1.3 — Filing-day budget validation** (operator decision; ~1 day)

- Counsel issues a written quote breaking out: (a) office fees per mark per jurisdiction; (b) preparation fees per mark; (c) submission fees; (d) post-filing monitoring fees; (e) opposition-response retainer.
- Validates the provisional estimate (~€5,500–€7,800 office fees per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` §5) against current EUIPO/OEPM fee schedule.
- Operator approves total budget.

**Step 1.4 — Filing submission** (counsel-driven; ~1 day)

- Counsel transcribes data from `TRADEMARK_FILING_STRATEGY_2026-05.md` §5 into EUIPO TM-1 portal + OEPM portal.
- Counsel submits. Records filing receipts + filing numbers.
- Updates `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` §3 table with `filing_number` and `filed_at` fields per row (operator commits this update).

**Step 1.5 — Post-filing monitoring** (recurring; governed by SOP-LEGAL_TRADEMARK_MONITORING_001)

- Examination: 1-3 months. Counsel responds to formal/substantive objections.
- Publication / opposition window: 2-3 months. ENVOY (M7) is the highest-risk mark for opposition.
- Registration grant: typical 4-9 months total.

### Track 2 — Legal template adoption (1 week operator + counsel)

**Step 2.1 — Counsel review of 4 templates** (counsel-driven; 2-3 days)

- Counsel reviews each of MSA / SOW / NDA / DPA against:
  - Spanish contract law specifics.
  - EU GDPR + DPA requirements (Annex II Technical & Organisational Measures must be filled in for actual DPA execution).
  - Counterparty-jurisdiction-specific tweaks (LATAM, FR, EN-US clients may need additional clauses).
- Counsel produces redlined versions. Operator + counsel iterate to v1.1 of each template.

**Step 2.2 — Annex II — Technical & Organisational Measures** (operator + Tech Lab; 1-2 days)

- Compile Holistika's standard TOMs document covering: encryption-at-rest, encryption-in-transit, access controls, backup procedures, incident response, sub-processor list.
- Reference architecture per existing `hlk-erp` and `kirbe` security postures.
- Attach as DPA Annex II.

**Step 2.3 — Sub-processor list (DPA Annex III)** (operator; 1 day)

- List currently-engaged sub-processors with locations: cloud hosting (Vercel + Render + Supabase + Neo4j), email infrastructure, project management, telephony, etc.
- Document each sub-processor's GDPR posture (DPA executed with the sub-processor; transfer mechanism for non-EEA).

**Step 2.4 — Template repository commit** (operator; 1 day)

- Once counsel-approved v1.1, commit the post-counsel-review versions back to `_templates/` with `version: 1.1` and `last_review:` updated.
- Operator may choose to keep v1.0 templates as historical reference.

### Track 3 — Boilerplate legal-page integration (P5 work; 1-3 days within P5 scope)

**Step 3.1 — P5 translates EN drafts to ES + FR** (within P5 scope; not P4)
**Step 3.2 — P5 renders into boilerplate `app/{privacy,terms,cookies}/page.tsx`** (within P5 scope)
**Step 3.3 — Cookie-consent banner integration** (within P5 scope; pairs with cookie-policy draft)

These three steps are P5 deliverables, not P4. P4 produces the input drafts; P5 integrates.

## Operator approval checklist (pre-P5 entry)

Before P5 begins, operator confirms:

1. ☐ The 7-mark filing strategy is correct (EUIPO + OEPM combinations; Nice classes; word vs design distinctions).
2. ☐ The OEPM-only filing decision for `Think Big` is acceptable given collision risk + narrow Nice scope; Spain-only protection accepted.
3. ☐ The Nice 9 + 42 narrow scope for `MADEIRA` (excluding wines/food/tourism/etc.) is acceptable given collision-driven mitigation.
4. ☐ The 4 legal templates are starting drafts and will go through counsel review before any client signing.
5. ☐ The 3 boilerplate legal-page drafts are EN-canonical input for P5; counsel will review the published versions before going live.
6. ☐ Track 1 (trademark filings) is operator-driven outside P4 scope; agent's role ends at "ready-to-sign" per D-IH-66-H.
7. ☐ Track 2 (legal template adoption) is operator-driven outside P4 scope.
8. ☐ Track 3 (boilerplate legal-page integration) is P5 scope.
9. ☐ P5 entry approved (boilerplate rewrite: 5 manifesto entries + home flywheel SVG + /services 6×3 matrix + /tech-lab + /how-we-work + /vision + indigo/slate fix + EN/ES/FR i18n parity + SiteFooter trademark posture).

## Cumulative I66 status

| Phase | Status | Commits |
|:---:|:---|:---|
| P0 | ✓ | charter |
| P1 | ✓ | `63d84e0` canon |
| P2 | ✓ | drift gates + cursor rules |
| P3 | ✓ | 16 process rows + 16 active SOPs + D-IH-66-R + D-IH-66-X follow-up |
| **P4** | **✓ closed (this commit)** | trademark strategy + 4 legal templates + 3 boilerplate legal drafts + naming-governance SOP |
| P5 | ⏸ awaiting operator signal | — |
| P6–P8 | pending | — |

**Decisions encoded cumulatively (P0–P4)**: ~22 of 20+ D-IH-66-* (now includes D-IH-66-H, U, V, W in addition to P0-P3 set).

## Cross-references

- I66 master-roadmap: `master-roadmap.md` §"P4 — Trademark + legal templates".
- Sister phase records: [P0](p0-pause-record-2026-05-08.md), [P1](p1-pause-record-2026-05-08.md), [P2](p2-pause-record-2026-05-08.md), [P3 H1](p3-pause-record-2026-05-08.md), [P3 H2 closure](p3-closure-pause-record-2026-05-09.md).
- Architectural anchor: [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md).
- D-IH-66-H, U, V, W in `decision-log.md`.
