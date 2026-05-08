---
language: en
status: charter
initiative: 66-brand-vision-ops-sweep
report_kind: scope-compendium
last_review: 2026-05-08
---

# I66 Scope Compendium

The full IN/OUT catalog. When an agent or operator says "is this in scope?", this file answers.

## Phase-by-phase delivery list

### P0 — Charter + carry-over commits + Impeccable upgrade (3-3.5 days)

**IN.**
- This 7-file folder under `docs/wip/planning/66-brand-vision-ops-sweep/`.
- 5 carry-over commits across 2 sibling repos:
  - `hlk-erp/PRODUCT.md` — sub-mark phrasing fix (Round 2 carry-over).
  - `boilerplate/PRODUCT.md` — initial creation (Round 2 carry-over).
  - `boilerplate/DESIGN.md` — initial creation (Round 2 carry-over).
  - `hlk-erp/BASELINE_REALITY.md` — Round 3 scaffold.
  - `boilerplate/BASELINE_REALITY.md` — Round 3 scaffold.
- `.cursor/skills/impeccable/SKILL.md` upgrade to v3.1 with BASELINE_REALITY.md as 5th setup gate.
- `.cursor/skills/impeccable/scripts/load-context.mjs` upgrade.
- `INITIATIVE_REGISTRY.csv` charter row for I66.
- `CHANGELOG.md` `[Unreleased]` entry for P0.
- One commit per repo per phase per `akos-governance-remediation.mdc`.

**OUT.** Any P1+ canonical or rule.

### P1 — Canon hardening + voice + logo audit + baseline-reality + abbreviations + transcript curation (7-8 days)

**IN.**
- 6 new BRAND_* canonicals: BRAND_ARCHITECTURE.md, BRAND_VISION.md, BRAND_LOGO_SYSTEM.md, BRAND_BASELINE_REALITY_MATRIX.md, BRAND_ABBREVIATIONS.md, BRAND_FRENCH_PATTERNS.md.
- Major rewrite of BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.
- Substantive enrichment of BRAND_SPANISH_PATTERNS from 14+ Spanish transcripts.
- Updates to BRAND_VOICE_FOUNDATION (Tier-1 + Tier-2), BRAND_DO_DONT, BRAND_JARGON_AUDIT (HLK rule), BRAND_REGISTER_MATRIX (baseline-reality cross-ref + internal-vocabulary-restricted column), BRAND_VISUAL_PATTERNS (theme asymmetry).
- Curation of 20+ transcripts to `docs/_assets/transcripts/` with full frontmatter (date, language, audience, topic, lens-tags = voice + funnel).
- Logo audit decisions encoded: Hi monogram primary, HOLÍSTIKA Research wordmark formal, RGB-rings deprecated, stylized-vs-prose split rule.
- BRAND_BASELINE_REALITY_MATRIX dual-register columns codified: per audience-x-topic row contains internal-vocabulary-(restricted) + external-vocabulary-(canonical).

**OUT.**
- Italian voice canonical (no audience signal).
- Portuguese voice canonical (deferred; tracked).
- Photography / illustration system.
- Logo redesign — only audit + decisions, no new design work.
- Per-product visual canon (those live in product-specific docs).

### P2 — 4 drift gates + 2 new rules + 2 rule updates (3-4 days)

**IN.**
- `scripts/validate_brand_canon_drift.py` (HSL token equality across boilerplate/globals.css + hlk-erp/DESIGN.md + boilerplate/DESIGN.md + akos/hlk_pdf_render.py).
- `scripts/validate_brand_jargon.py` (rendered DOM scan for BRAND_JARGON_AUDIT §4 forbidden tokens incl. HLK abbreviation rule).
- `scripts/validate_brand_voice_register.py` (asserts FR/ES copy on boilerplate aligns with BRAND_REGISTER_MATRIX rows).
- `scripts/validate_brand_baseline_reality_drift.py` (asserts every external-facing artifact cites a baseline-reality matrix entry per target audience).
- All 4 wired into `scripts/release-gate.py`.
- `tests/test_validate_brand_canon_drift.py` + 3 sibling tests.
- `.cursor/rules/akos-agent-checkpoint-discipline.mdc` (new; alwaysApply).
- `.cursor/rules/akos-brand-baseline-reality.mdc` (new; alwaysApply).
- `.cursor/rules/akos-docs-config-sync.mdc` updated (sync triggers for P1 canonicals).
- `.cursor/rules/akos-planning-traceability.mdc` updated (I67-scaffold pattern + checkpoint cross-reference).
- Deliberate-drift demo report.

**OUT.**
- Visual-regression testing (out of brand-canon scope; in CI rule).
- Performance regression (Lighthouse already in CI).
- Accessibility regression (Playwright + axe in CI).

### P3 — Operations integration (5-6 days)

**IN.**
- ~16 process_list.csv rows (annual brand-architecture review, drift remediation, voice parity audit, lab-to-service promotion, lab-to-product promotion, trademark filing tracking, brand request intake, brand approval workflow, drift incident response, manifesto publishing cadence, service offering quarterly review, sales playbook update, community network management, agent brand digest refresh, counterparty baseline assessment cadence, intelligence-report cadence).
- 3 sub-mark Lead rows in baseline_organisation.csv (Holistika R&S Lead, Think Big Lead, HLK Tech Lab Lead).
- New canonical `SERVICE_OFFERING_CATALOG.md` (6 services × 3 arms × 3 tiers).
- 11 new SOPs (BRAND_REQUEST_INTAKE, BRAND_APPROVAL_WORKFLOW, BRAND_DRIFT_INCIDENT_RESPONSE, MANIFESTO_PUBLISHING, USE_CASE_PROMOTION, COMMUNITY_NETWORK_MANAGEMENT, AGENT_BRAND_DIGEST, COUNTERPARTY_BASELINE_ASSESSMENT, ELICITATION_DISCIPLINE, COUNTERPARTY_RELIABILITY_GRADING, INTELLIGENCE_REPORT). 4 of these are HUMINT FM 2-22.3 derived (internal-only register).
- `docs/wip/intelligence/` working-space creation (INDEX.md + templates/ + 2026-05-08-i66-illustrative/).
- SOP-META_PROCESS_MGMT_001 cross-reference updates.
- `compliance.process_list_mirror` + `compliance.baseline_organisation_mirror` re-emit.

**OUT.**
- Implementation of any of those processes — only the canonical rows + SOPs, not execution.
- Org-chart visualization (existing baseline_organisation tooling).

### P4 — Trademark + ready-to-sign forms + legal-template suite (5-6 days)

**IN.**
- Clearance reports (EUIPO + OEPM) for 5 marks: Holistika, HLK Tech Lab, MADEIRA, KiRBe, ENVOY (+ Think Big stretch).
- Filing strategy canonical with Nice classes (35 + 42 + 9 baseline; 41 + 16 + 38 stretch), jurisdiction sequence, validated official-fee numbers.
- Filing prep packets per mark per jurisdiction.
- Ready-to-sign EUIPO TM-1 forms + OEPM equivalent forms per mark per jurisdiction (5 marks × 2 jurisdictions = ~7-8 forms total accounting for EUIPO covering ES).
- Legal template suite: MSA, SOW, NDA mutual, NDA one-way, DPA (per GDPR Art. 28 + 32).
- Privacy / Terms / Cookies refresh on boilerplate.
- Operator-handoff package: `reports/p4-operator-handoff-2026-05-XX.md` with 3-step "sign + pay + submit" instructions.

**OUT.**
- Filing the trademarks at the registry — operator-driven, tracked in OPS_REGISTER post-handoff.
- Legal counsel of record selection — operator decision.
- IP litigation strategy.
- Patent filings.

### P5 — Public surfaces rewrite + boilerplate code (6 days)

**IN.**
- Rewrite of all 5 manifesto entries: `/manifiesto/holistika`, `/manifiesto/madeira`, `/manifiesto/madeira-agent`, `/manifiesto/kirbe`, `/manifiesto/envoy`. Each Tier-2 register-aligned.
- Home page hero + flywheel reframe: replace flat connection line with circular SVG flywheel; update copy.
- `/services` page rewrite as 6 × 3 matrix consuming SERVICE_OFFERING_CATALOG.
- `/tech-lab` page rewrite (lab-as-credibility narrative).
- New `/how-we-work` page (lab → channel pipeline).
- New `/vision` page (curated public subset of BRAND_VISION via public-region markers).
- Code fixes: indigo / slate drift in `app/manifiesto/data.ts` + `components/home/entities-section.tsx`.
- Full EN / ES / FR i18n parity for all rewritten + new pages.
- SiteFooter trademark-posture line: "Holistika is a brand of Holistika Research SL. Holistika™ + MADEIRA™ + KiRBe™ + Think Big™ + HLK Tech Lab™ — applications pending."
- `boilerplate/public/robots.txt` updated to noindex `/dashboard` + `/auth/*` (per D-IH-66-H).
- hlk-erp chrome change: move color-mode picker from settings drawer to operator app-bar (per D-IH-66-G).

**OUT.**
- Migrating `boilerplate/lib/theme/defaultTheme="dark"` → `"system"` (per D-IH-66-G).
- Decommissioning `/dashboard` + `/(authapp)/login` on boilerplate (per D-IH-66-H; deferred to separate initiative).
- Photography refresh (no asset budget).
- Component library refactor.
- New pages beyond /how-we-work + /vision.

### P6 — Marketing-ops + sales-ops template suite (7 days)

**IN.**
- Email signature templates (5+ role-specific).
- 6 outbound email sequence templates: welcome, intake, post-discovery, post-engagement, dossier-companion, calendly-confirmation.
- 6 slide deck templates each shipping with 3 files (`.md`, `.objections.md`, `.counterparty-brief.md`):
  - investor (12 slides)
  - sales (8 slides)
  - advisor (4 slides)
  - partner (4 slides)
  - ENISA (8 slides)
  - recruiter (6 slides)
- Stationery package: letterhead + business card + one-pager.
- FOUNDER_BIO.md canonical: long / medium / short × EN / ES / FR + per-audience FAQ reservoir + methodology track-record block (anonymized fitness-franchise per D-IH-66-Q).
- PRESS_KIT.md canonical: logos package + boilerplate prose + founder bio + per-audience FAQ.
- ONBOARDING_KIT.md canonical: welcome + brand digest + canonicals tour + Cursor / MCP setup.
- SOP-DISCOVERY_QUESTIONNAIRE_001 (HUMINT-grounded; external-register translated).
- PROPOSAL_TEMPLATE.md (3-tier).
- ENGAGEMENT_PLAYBOOK.md.
- Supabase view `governance.brand_template_registry_view` (joins canonicals → operator surface).
- Supabase view `governance.engagement_intelligence_view` (joins `docs/wip/intelligence/INDEX.md` → operator surface; access_level: 5).
- New operator panel `/governance/brand-templates` (AccessLevel ≥ 5).
- New operator panel `/governance/intelligence` (AccessLevel ≥ 5).
- Mission Control tile additions or chip updates as needed (one chip per panel).

**OUT.**
- Asset-management system (Notion / DAM).
- CRM tooling decision (in I67 DP-3).
- Marketing-automation tooling decision (in I67 DP-3).
- Pricing tier validation methodology (in I67 DP-5).

### P7 — Vision + dossier-companion drift gates (1-2 days)

**IN.**
- `scripts/validate_brand_vision_drift.py` (BRAND_VISION public-region ↔ boilerplate `/vision/page.tsx` prose equality).
- `scripts/validate_dossier_companion_drift.py` (dossier render output voice-and-figure-parity with `/manifiesto/holistika` + `/vision`).
- Both wired into release-gate.
- Tests + deliberate-drift verification.

**OUT.**
- New canonicals (none in P7).

### P8 — UAT + closure + I67 RevOps Discovery scaffold (5 days)

**IN.**
- Operator UAT walkthrough across all canonicals + public artifacts; live review of `/manifiesto/*` + `/how-we-work` + `/vision` on Vercel preview.
- All 9 drift gates green locally.
- `release-gate.py` final run.
- Cycle closeout report.
- CHANGELOG synthesis (promote `[Unreleased]` to current version).
- USER_GUIDE updates (new panels documented; Brand operator model section refreshed).
- ARCHITECTURE updates (Brand canon + Baseline Reality + Branded House diagram).
- SOP updates (11 new SOPs cross-referenced).
- INITIATIVE_REGISTRY: I66 closed, I67 chartered.
- DECISION_REGISTER mirror with 20 D-IH-66-* rows + D-IH-66-CLOSURE.
- OPS_REGISTER updates (trademark-handoff + brand-template-rollout rows).
- AKOS dashboard refresh (`/governance` + `/planning` panels).
- I67 RevOps Discovery scaffold: 6 files in `docs/wip/planning/67-revops-discovery/`:
  - `charter.md` (research-first scope; working title challengeable)
  - `research-brief.md` (mandatory inputs + external research + operator interviews)
  - `starting-hypotheses.md` (deliberately near-empty tree of `[UNKNOWN]` markers)
  - `decision-points.md` (8 operator-blocking decisions)
  - `sources-and-prior-art.md` (transcripts curated by funnel-mining lens, I66 outputs, public benchmarks)
  - `AGENT_INSTRUCTIONS.md` (six binding mandates)

**OUT.**
- I67 actual phase scoping — that's the next agent's first task post-research.
- Migration of any I66 working-space content into I67 — they share `docs/_assets/transcripts/`, but I67 owns its own working space.

## Cross-cutting in-scope across all phases

- **Documentation sync per phase per `akos-docs-config-sync.mdc`:** CHANGELOG entry; relevant USER_GUIDE / ARCHITECTURE / SOP page updates.
- **Mirror sync after canonical CSV edits per `akos-holistika-operations.mdc`:** `compliance_mirror_emit` job; no megabyte migrations.
- **Pause record per phase per `akos-planning-traceability.mdc`:** dated `reports/<phase>-pause-record-YYYY-MM-DD.md` operator-signed.
- **Self-checkpoint reports per `akos-agent-checkpoint-discipline.mdc` (once that rule lands in P2):** dated observations under `reports/checkpoints/`.

## Cross-cutting out-of-scope across all phases

- **Migration / decommission of `boilerplate/` legacy areas** (`/dashboard`, `/(authapp)/login`) — declared OOS per D-IH-66-H.
- **CRM / marketing-automation / DAM tooling selection** — moved to I67 DP-3.
- **Pricing tier validation methodology** — moved to I67 DP-5.
- **Channel + content cadence** — moved to I67 starting-hypotheses.
- **Partner-deal economics formalization** — moved to I67 DP-6.
- **KPI selection + dashboards** — moved to I67 DP-7.

## Deferred to separate initiatives

- **Italian + Portuguese voice canonicals** — defer until audience signal exists.
- **Photography / illustration system** — defer until budget exists.
- **Component library refactor on boilerplate** — defer; `boilerplate/PRODUCT.md` Section 8 declares legacy areas; component-library refactor is a separate engineering initiative.
- **InfraMonitor 2026 + Financial Analyst 2026 product canon** — separate product initiatives.
- **A11y audit beyond WCAG 2.2 AA** — defer; current target is 2.2 AA per Impeccable setup.

## Quick scope-test heuristics

If unsure whether something is in scope:

1. Does it touch `BRAND_*` canonicals or sub-mark architecture? → IN if P1.
2. Does it produce a drift gate or cursor rule for brand canon? → IN if P2.
3. Does it add a process_list row, baseline_organisation row, SOP, or service offering? → IN if P3.
4. Does it touch trademark filings, legal templates, privacy / terms / cookies? → IN if P4.
5. Does it rewrite a public boilerplate page or fix indigo/slate drift? → IN if P5.
6. Does it produce email / deck / bio / press / onboarding / sales-ops / 2 new operator panels? → IN if P6.
7. Does it produce a vision-drift or dossier-companion drift gate? → IN if P7.
8. Does it close I66 or scaffold I67? → IN if P8.
9. Otherwise: out of scope. Surface as a backlog candidate; do not silently extend.
