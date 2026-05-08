---
language: en
status: charter
initiative: 66-brand-vision-ops-sweep
report_kind: asset-classification
last_review: 2026-05-08
---

# I66 Asset Classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md), every asset I66 touches falls into exactly one of: **Canonical**, **Mirrored / Derived**, **Reference-only**, or **Working-space**.

## Canonical (edit here first; all consumers cite back)

### New canonicals (created in I66)

| Asset | Phase | Authority | SSOT path |
|:---|:---|:---|:---|
| `BRAND_ARCHITECTURE.md` | P1 | Founder + Brand Manager | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `BRAND_VISION.md` | P1 | Founder | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `BRAND_LOGO_SYSTEM.md` | P1 | Founder + Brand Manager | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `BRAND_BASELINE_REALITY_MATRIX.md` | P1 | Founder | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `BRAND_ABBREVIATIONS.md` | P1 | Brand Manager | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `BRAND_FRENCH_PATTERNS.md` | P1 | Founder + Voice Lead | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `SERVICE_OFFERING_CATALOG.md` | P3 | Founder + Sub-mark Leads | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Services/` |
| `TRADEMARK_FILING_STRATEGY_2026-05.md` | P4 | Founder + Legal Counsel | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Legal/` |
| `LEGAL_TEMPLATES_v1/` (MSA + SOW + NDA mutual + NDA one-way + DPA) | P4 | Legal Counsel | `docs/references/hlk/v3.0/Admin/O5-1/Operations/Legal/` |
| `FOUNDER_BIO.md` | P6 | Founder | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `PRESS_KIT.md` | P6 | Brand Manager | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |
| `ONBOARDING_KIT.md` | P6 | People + Brand Manager | `docs/references/hlk/v3.0/Admin/O5-1/Operations/BrandOps/` |

### Modified canonicals (substantive rewrite)

| Asset | Phase | Change |
|:---|:---|:---|
| `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` | P1 | Major rewrite for Branded House + trademark filing strategy |
| `BRAND_VOICE_FOUNDATION.md` | P1 | Tier-1 + Tier-2 sub-mark voice register expansions; cross-reference baseline-reality + abbreviations |
| `BRAND_DO_DONT.md` | P1 | New entries for sub-mark voice tier, abbreviation use, baseline-reality citation |
| `BRAND_JARGON_AUDIT.md` | P1 | §4 forbidden tokens extended for HLK abbreviation rule |
| `BRAND_REGISTER_MATRIX.md` | P1 | Cross-reference baseline-reality matrix; new column for "internal-vocabulary-restricted" |
| `BRAND_SPANISH_PATTERNS.md` | P1 | Substantial enrichment from 14+ Spanish transcripts |
| `BRAND_VISUAL_PATTERNS.md` | P1 | Document boilerplate dark vs hlk-erp system theme asymmetry |
| `process_list.csv` | P3 | 16 new rows |
| `baseline_organisation.csv` | P3 | 3 new sub-mark Lead rows (Holistika R&S Lead, Think Big Lead, HLK Tech Lab Lead) |
| `SOP-META_PROCESS_MGMT_001.md` | P3 | Cross-reference 11 new SOPs |
| `INITIATIVE_REGISTRY.csv` | P0 + P8 | Charter row P0; close + I67 charter rows P8 |
| `DECISION_REGISTER.csv` | P8 | 20 D-IH-66-* rows mirrored |
| `OPS_REGISTER.csv` | P4 + P8 | Trademark-filing handoff rows; brand-template-suite rollout rows |

### New SOPs (P3)

| SOP | Domain | Source |
|:---|:---|:---|
| `SOP-BRAND_REQUEST_INTAKE_001.md` | BrandOps | Internal |
| `SOP-BRAND_APPROVAL_WORKFLOW_001.md` | BrandOps | Internal |
| `SOP-BRAND_DRIFT_INCIDENT_RESPONSE_001.md` | BrandOps | Internal |
| `SOP-MANIFESTO_PUBLISHING_001.md` | BrandOps | Internal |
| `SOP-USE_CASE_PROMOTION_001.md` | LabOps | Internal |
| `SOP-COMMUNITY_NETWORK_MANAGEMENT_001.md` | BrandOps | Internal |
| `SOP-AGENT_BRAND_DIGEST_001.md` | AgentOps | Internal |
| `SOP-COUNTERPARTY_BASELINE_ASSESSMENT_001.md` | IntelligenceOps | HUMINT FM 2-22.3 Ch.7 |
| `SOP-ELICITATION_DISCIPLINE_001.md` | IntelligenceOps | HUMINT FM 2-22.3 Ch.9 |
| `SOP-COUNTERPARTY_RELIABILITY_GRADING_001.md` | IntelligenceOps | HUMINT FM 2-22.3 App.B |
| `SOP-INTELLIGENCE_REPORT_001.md` | IntelligenceOps | HUMINT FM 2-22.3 Ch.10 |

### New cursor rules (P2)

| Rule | Always-applied? | Scope |
|:---|:---:|:---|
| `.cursor/rules/akos-agent-checkpoint-discipline.mdc` | yes | All agent sessions on initiatives ≥3 phases or ≥2 calendar weeks |
| `.cursor/rules/akos-brand-baseline-reality.mdc` | yes | All external-facing prose generation; enforces baseline-reality citation |

### Modified cursor rules (P2)

| Rule | Change |
|:---|:---|
| `.cursor/rules/akos-docs-config-sync.mdc` | Sync triggers for 6 new BRAND_* canonicals + SERVICE_OFFERING_CATALOG + 11 new SOPs |
| `.cursor/rules/akos-planning-traceability.mdc` | I67-scaffold-at-closure pattern + agent-checkpoint cross-reference |

### New skills upgrade (P0)

| Asset | Change |
|:---|:---|
| `.cursor/skills/impeccable/SKILL.md` | v3.0 → v3.1: BASELINE_REALITY.md as 5th setup gate |
| `.cursor/skills/impeccable/scripts/load-context.mjs` | Reads BASELINE_REALITY.md |

## Mirrored / Derived (regenerated from canon, never hand-edited as the truth)

| Asset | Source canon | Phase |
|:---|:---|:---|
| `compliance.repository_registry_mirror` (Supabase) | `repository_registry.csv` | P0 |
| `compliance.process_list_mirror` (Supabase) | `process_list.csv` | P3 |
| `compliance.baseline_organisation_mirror` (Supabase) | `baseline_organisation.csv` | P3 |
| `governance.brand_template_registry_view` (Supabase view) | `BRAND_*` canonicals + `LEGAL_TEMPLATES_v1/` + decks index | P6 |
| `governance.engagement_intelligence_view` (Supabase view) | `docs/wip/intelligence/INDEX.md` | P6 |
| `boilerplate/app/manifiesto/data.ts` | 5 manifesto canonicals | P5 |
| `boilerplate/app/services/page.tsx` | `SERVICE_OFFERING_CATALOG.md` | P5 |
| `boilerplate/app/vision/page.tsx` | `BRAND_VISION.md` public-region markers | P5 |
| `boilerplate/app/how-we-work/page.tsx` | `BRAND_ARCHITECTURE.md` flywheel section | P5 |
| `boilerplate/components/layout/SiteFooter.tsx` (trademark posture line) | `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` | P5 |
| `hlk-erp/app/(operator)/governance/brand-templates/page.tsx` | `governance.brand_template_registry_view` | P6 |
| `hlk-erp/app/(operator)/governance/intelligence/page.tsx` | `governance.engagement_intelligence_view` + `docs/wip/intelligence/` | P6 |
| `hlk-erp/lib/types/governance.ts` (extension) | New views | P6 |
| `hlk-erp/lib/auth/route-matrix.ts` (new routes; AccessLevel ≥ 5) | Internal | P6 |
| `boilerplate/i18n/messages/{en,es,fr}/manifiesto/*.json` | Manifesto canonicals | P5 |

## Reference-only (read-only inputs to I66; never re-classified)

| Asset | Use |
|:---|:---|
| `docs/_assets/transcripts/2026-04-17-researcher-onboarding.md` | Voice + funnel input (curated P1) |
| `docs/_assets/transcripts/2026-12-12-bd-onboarding.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-02-prekick-alcance.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-06-prekick-fiscal.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-08-04-kickoff-enisa-1.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-08-04-kickoff-enisa-2.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-08-04-kickoff-asesoria-hosteleria.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-12-04-consultoria-hosteleria-admin-1.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-30-04-consultoria-hosteleria-admin-3.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-12-04-consultoria-hosteleria-pestel.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-01-presentation-projet-2.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-08-efa-prospection.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-08-nfq-purview.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-03-23-websitz-cart-bundle.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-07-whatsapp-15-51.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-07-whatsapp-15-52.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-02-whatsapp-21-51.md` | Voice + funnel input |
| `docs/_assets/transcripts/2026-04-02-whatsapp-21-52.md` | Voice + funnel input |
| `docs/_assets/transcripts/Rushly_Cahier_des_charges_v2.md` | Voice + funnel input |
| `HUMINT FM 2-22.3 (US Army, Sept 2006)` | SOP source citation only; not redistributed |
| `docs/wip/planning/66-brand-vision-ops-sweep/` (this folder) | I66 charter |

## Working-space (operator-time-bounded; archived at engagement close)

| Asset | Lifetime |
|:---|:---|
| `docs/wip/intelligence/2026-05-08-i66-illustrative/` | Illustrative; permanent training reference |
| `docs/wip/intelligence/<engagement>/` | Per-engagement; archived 90d after engagement close |
| `docs/wip/planning/67-revops-discovery/` | I67 lifetime |

## Drift-prevention contract

This asset classification table is the source of truth for what I66 may edit. If a phase touches an asset NOT listed here, that's a scope-creep signal — the agent must surface it as a self-checkpoint observation, not silently extend.

If a phase claims to be "complete" but a Mirrored / Derived asset has not been regenerated from its source, the phase is incomplete.

If a Reference-only asset is being edited by an I66 phase, the phase is misclassified — pause and re-classify.
