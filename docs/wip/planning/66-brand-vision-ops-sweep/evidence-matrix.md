---
language: en
status: charter
initiative: 66-brand-vision-ops-sweep
report_kind: evidence-matrix
last_review: 2026-05-08
---

# I66 Evidence Matrix

Per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc), every phase must show evidence at three levels:

1. **Mechanical** — can be verified by a script.
2. **Documentary** — produces a dated artifact under `reports/`.
3. **Operator** — requires a human reading + approval at a pause point.

If a phase advances without one of the three, the phase is incomplete.

## P0 — Charter + carry-over commits + Impeccable upgrade (Pause #1)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| Folder exists with 7 governance files | `ls docs/wip/planning/66-brand-vision-ops-sweep/` shows master-roadmap, decision-log, asset-classification, evidence-matrix, risk-register, journeys, scope-compendium | Mechanical |
| 20 D-IH-66-* decisions logged | `decision-log.md` contains entries A through T | Mechanical |
| 10 risks logged | `risk-register.md` contains entries R-IH-66-1 through 10 | Mechanical |
| 7 audience journeys logged | `journeys-2026-05-08.md` contains operator + investor + advisor + ENISA + partner + recruiter + customer | Mechanical |
| Impeccable upgrade | `.cursor/skills/impeccable/SKILL.md` includes "5th setup gate: BASELINE_REALITY.md"; `load-context.mjs` reads BASELINE_REALITY.md | Mechanical (grep + node load) |
| 3 carry-over commits in 2 sibling repos | `hlk-erp` HEAD includes "Think Big sub-mark fix"; `boilerplate` HEAD includes 2 commits for PRODUCT.md + DESIGN.md | Mechanical (git log) |
| 2 BASELINE_REALITY scaffolds | `hlk-erp/BASELINE_REALITY.md` + `boilerplate/BASELINE_REALITY.md` exist with section skeletons | Mechanical |
| CHANGELOG entry | `CHANGELOG.md` `[Unreleased]` includes I66 P0 line | Mechanical |
| Operator approves charter | `reports/p0-pause-record-2026-05-XX.md` exists; operator signature line present | Operator |

## P1 — Canon hardening + voice + logo audit + baseline-reality + abbreviations + transcript curation (Pause #2)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| 6 new BRAND_* canonicals | All files exist in `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` | Mechanical |
| BRAND_HIERARCHY rewrite | Diff shows ≥40% prose changed; new "Branded House" mermaid diagram present | Mechanical (line-count + grep) |
| 20+ transcripts curated | `docs/_assets/transcripts/` ≥20 files; each has frontmatter (date, language, audience, topic, lens-tags) | Mechanical |
| BRAND_SPANISH_PATTERNS substantive enrichment | Diff shows ≥3 new sections; ≥30 new pattern entries | Mechanical |
| BRAND_FRENCH_PATTERNS canonical | New file with ≥3 sections + ≥15 pattern entries | Mechanical |
| BRAND_BASELINE_REALITY_MATRIX dual register | Per-row schema includes both `internal-vocabulary-(restricted)` + `external-vocabulary-(canonical)` columns | Mechanical |
| BRAND_LOGO_SYSTEM audit decisions | All 4 logo decisions present (Hi monogram primary, HOLÍSTIKA wordmark formal, RGB-rings deprecated, stylized-vs-prose split) | Mechanical |
| BRAND_ABBREVIATIONS HLK governance | Allowed/forbidden table for HLK + MA + KB + EV + TB + TL | Mechanical |
| Cross-references coherent | `validate_hlk.py` passes | Mechanical |
| Phase report | `reports/p1-canon-hardening-2026-05-XX.md` exists | Documentary |
| Operator approves canon | `reports/p1-pause-record-2026-05-XX.md` operator signature | Operator |

## P2 — 4 drift gates + 2 new rules + 2 rule updates (Pause #3)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| `validate_brand_canon_drift.py` exists + passes | Script + `tests/test_validate_brand_canon_drift.py` green | Mechanical |
| `validate_brand_jargon.py` exists + passes | Script + tests green | Mechanical |
| `validate_brand_voice_register.py` exists + passes | Script + tests green | Mechanical |
| `validate_brand_baseline_reality_drift.py` exists + passes | Script + tests green | Mechanical |
| All 4 wired into `release-gate.py` | `grep "validate_brand_" scripts/release-gate.py` returns ≥4 matches | Mechanical |
| `akos-agent-checkpoint-discipline.mdc` exists with always-apply | `head -1 .cursor/rules/akos-agent-checkpoint-discipline.mdc` shows alwaysApply: true | Mechanical |
| `akos-brand-baseline-reality.mdc` exists with always-apply | Same | Mechanical |
| `akos-docs-config-sync.mdc` updated | Diff shows new sync triggers | Mechanical |
| `akos-planning-traceability.mdc` updated | Diff shows I67-scaffold-pattern + checkpoint cross-reference | Mechanical |
| Deliberate-drift demo | `reports/p2-drift-gate-fake-drift-demo-2026-05-XX.md` shows agent introduced one drift in each gate's domain; CI failed; reverted | Documentary |
| Operator approves gates | `reports/p2-pause-record-2026-05-XX.md` operator signature | Operator |

## P3 — Operations integration (Pause #4 — CSV gate)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| 16 process_list.csv rows added | Diff shows 16 new rows; each has process_id, role_owner, frequency, classification | Mechanical |
| 3 baseline_organisation.csv rows added | Diff shows 3 new rows for sub-mark Leads | Mechanical |
| SERVICE_OFFERING_CATALOG canonical | New file present with 6 services × 3 arms × 3 tiers matrix | Mechanical |
| 11 new SOPs | All 11 files present in correct domain folders (BrandOps + LabOps + AgentOps + IntelligenceOps) | Mechanical |
| HUMINT-derived SOPs cite source | grep "HUMINT FM 2-22.3" in 4 IntelligenceOps SOPs returns 4 matches | Mechanical |
| `docs/wip/intelligence/` working space | Folder + INDEX.md + templates/ + 2026-05-08-i66-illustrative/ all present | Mechanical |
| SOP-META cross-references | `validate_hlk.py` passes; SOP-META updated with 11 new SOP entries | Mechanical |
| `compliance.process_list_mirror` updated | `compliance_mirror_emit` job ran; row count matches CSV | Mechanical |
| `compliance.baseline_organisation_mirror` updated | Same | Mechanical |
| Phase report | `reports/p3-ops-integration-2026-05-XX.md` exists | Documentary |
| **CSV gate operator approval** | `reports/p3-csv-gate-pause-record-2026-05-XX.md` operator signature line; CSV diff explicitly approved per `akos-governance-remediation.mdc` | **Operator (CSV gate)** |

## P4 — Trademark + ready-to-sign forms + legal-template suite (Pause #5)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| Clearance reports for 5 marks | `reports/p4-trademark-clearance-EUIPO-2026-05-XX.md` + `reports/p4-trademark-clearance-OEPM-2026-05-XX.md` per mark | Documentary |
| Filing strategy canonical | `TRADEMARK_FILING_STRATEGY_2026-05.md` present with Nice classes, jurisdiction sequence, validated official-fee numbers | Mechanical |
| Ready-to-sign forms | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Legal/TRADEMARK_FILING_FORMS_2026-05/` contains TM-1 EUIPO + OEPM forms per applicable mark | Mechanical |
| Legal templates | MSA, SOW, NDA mutual, NDA one-way, DPA all present | Mechanical |
| GDPR DPA cross-reference | DPA cites GDPR Art. 28 + Art. 32 explicitly | Mechanical (grep) |
| Privacy / Terms / Cookies refresh | Boilerplate files updated with new corporate posture | Mechanical |
| Operator handoff package | `reports/p4-operator-handoff-2026-05-XX.md` present with 3-step "sign + pay + submit" instructions | Documentary |
| Operator approves filings | `reports/p4-pause-record-2026-05-XX.md` operator signature | Operator |

## P5 — Public surfaces rewrite + boilerplate code (Pause #6 — live review)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| 5 manifesto entries rewritten | All 5 prose files updated; voice-tested via `validate_brand_voice_register.py` | Mechanical |
| Home flywheel SVG | New circular flywheel replacing flat connection line; mermaid + SVG asset shipped | Mechanical |
| `/services` 6×3 matrix page | New page consuming SERVICE_OFFERING_CATALOG | Mechanical |
| `/tech-lab` rewrite | Diff shows ≥40% prose changed; lab-as-credibility narrative | Mechanical |
| `/how-we-work` page | New page with lab-channel pipeline diagram | Mechanical |
| `/vision` page | New page consuming BRAND_VISION public-region markers | Mechanical |
| Indigo / slate drift fixed | grep `indigo` + `slate` in `app/manifiesto/data.ts` + `entities-section.tsx` returns 0 matches | Mechanical |
| EN/ES/FR i18n parity | Each new page has all three locales; `next-intl` validation passes | Mechanical |
| SiteFooter trademark posture | Footer prose includes "Holistika is a brand of Holistika Research SL. Holistika™ + MADEIRA™ + KiRBe™ + Think Big™ + HLK Tech Lab™ — applications pending." | Mechanical (grep) |
| Vercel preview ready | Production-grade preview deployment URL captured | Mechanical (gh CLI) |
| **Operator live review** | `reports/p5-pause-record-2026-05-XX.md` operator signs after clicking through every new page; cookie-mode + reduced-motion + dark/light verified | **Operator (subjective live review)** |

## P6 — Marketing-ops + sales-ops template suite (Pause #7)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| Email signatures per role | 5+ role-specific signatures present | Mechanical |
| 6 outbound email sequence templates | Welcome / intake / post-discovery / post-engagement / dossier-companion / calendly-confirmation | Mechanical |
| 6 decks each with 3 files | investor + sales + advisor + partner + ENISA + recruiter; each has `.md` + `.objections.md` + `.counterparty-brief.md` | Mechanical (file count = 18) |
| Stationery package | letterhead + business card + one-pager all present in `Admin/O5-1/Operations/BrandOps/STATIONERY/` | Mechanical |
| Founder bio canonical | `FOUNDER_BIO.md` with long/medium/short × EN/ES/FR + per-audience FAQ + methodology track-record | Mechanical |
| Press kit | `PRESS_KIT.md` with logos + boilerplate prose + bio + FAQ | Mechanical |
| Onboarding kit | `ONBOARDING_KIT.md` with welcome doc + brand digest + canonicals tour + Cursor / MCP setup | Mechanical |
| Discovery questionnaire SOP | `SOP-DISCOVERY_QUESTIONNAIRE_001.md` (HUMINT-grounded) | Mechanical |
| Proposal template | `PROPOSAL_TEMPLATE.md` | Mechanical |
| Engagement playbook | `ENGAGEMENT_PLAYBOOK.md` | Mechanical |
| `governance.brand_template_registry_view` | Supabase view ships; `compliance_mirror_emit` job runs | Mechanical |
| `governance.engagement_intelligence_view` | Same | Mechanical |
| 2 new operator panels | `/governance/brand-templates` + `/governance/intelligence` reachable; AccessLevel ≥ 5 enforced | Mechanical (Playwright + RBAC test) |
| Operator approves suite | `reports/p6-pause-record-2026-05-XX.md` operator signature | Operator |

## P7 — Vision + dossier-companion drift gates (Pause #8)

| Gate | Evidence | Verifier |
|:---|:---|:---|
| `validate_brand_vision_drift.py` exists + passes | Script + tests | Mechanical |
| `validate_dossier_companion_drift.py` exists + passes | Script + tests | Mechanical |
| Both wired into release-gate.py | `grep` returns ≥2 new matches | Mechanical |
| Deliberate-drift verification | `reports/p7-drift-gate-fake-drift-demo-2026-05-XX.md` shows fake drift in `BRAND_VISION.md` public-region; CI failed; reverted | Documentary |
| Operator approves | `reports/p7-pause-record-2026-05-XX.md` operator signature | Operator |

## P8 — UAT + closure + I67 scaffold

| Gate | Evidence | Verifier |
|:---|:---|:---|
| Operator UAT walkthrough | `reports/uat-i66-2026-05-XX.md` exists with dated outcomes for every audience journey + every gated artefact | Operator (per `akos-planning-traceability.mdc`) |
| All 9 drift validators green locally | `reports/p8-verification-matrix-2026-05-XX.md` includes all 9 outputs | Documentary |
| `release-gate.py` green | Final run output captured | Mechanical |
| Cycle closeout report | `reports/cycle-closeout-i66-2026-05-XX.md` exists | Documentary |
| CHANGELOG synthesized | I66 entry promoted from `[Unreleased]` to current version | Mechanical |
| USER_GUIDE updated | New panels documented; Brand operator model section refreshed | Mechanical |
| ARCHITECTURE updated | Brand canon + Baseline Reality + Branded House diagram added | Mechanical |
| SOP updated | 11 new SOPs cross-referenced | Mechanical |
| INITIATIVE_REGISTRY closed | `validate_initiative_registry.py` confirms I66 closed + I67 chartered | Mechanical |
| DECISION_REGISTER mirrored | `validate_decision_register.py` confirms 20 D-IH-66-* rows | Mechanical |
| OPS_REGISTER updated | Trademark-handoff + brand-template-rollout rows present | Mechanical |
| I67 scaffold | All 6 files in `docs/wip/planning/67-revops-discovery/` present + research-first posture verified | Mechanical |
| AKOS dashboards refreshed | `/governance` + `/planning` panels show I66 closed + I67 chartered | Operator |

## Cross-cutting checkpoints

| Checkpoint | Evidence |
|:---|:---|
| Every phase produces ≥1 dated `reports/*.md` artifact | Mechanical (file count check) |
| Every phase produces ≥1 CHANGELOG entry | Mechanical |
| Every phase ends with operator pause record | Operator |
| Agent self-checkpoints documented inline in master-roadmap or in `reports/` as observations | Documentary |
| No `governance.unknown` repo health rows for I66's commits | Mechanical |
