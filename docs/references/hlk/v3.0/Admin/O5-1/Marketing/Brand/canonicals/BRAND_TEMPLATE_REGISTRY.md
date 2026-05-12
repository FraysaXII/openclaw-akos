---
canonical: true
status: active
classification: canonical
access_level: 4
language: en
register: internal
role_owner: Brand Manager
area: MKT
entity: Think Big
process_id: tbi_mkt_prc_template_registry_mtnce_001
linked_initiative: I66
linked_decisions:
  - D-IH-66-AD
  - D-IH-66-Q
  - D-IH-66-S
governance:
  - SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001
  - BRAND_BASELINE_REALITY_MATRIX.md
  - BRAND_REGISTER_MATRIX.md
last_review: 2026-05-09
---

# BRAND_TEMPLATE_REGISTRY

> Canonical index of reusable brand, sales, advisory, hiring, and engagement templates. P6 creates the Markdown/YAML source files; the future `governance.brand_template_registry` view mirrors this registry for operator panels.

## 1. Registry Contract

Each template row must answer:

- **Where is the source?** Git path to the canonical template.
- **Who is it for?** Audience and voice tier.
- **What canon does it cite?** Brand, baseline-reality, service catalog, founder bio, legal, or engagement SOP.
- **How is drift checked?** Validator or manual review path.
- **What is its status?** `draft`, `active`, `stale`, `deprecated`, or `operator_private`.

## 2. Template Inventory

| template_id | status | source_path | audience | voice_tier | owner | governed_by | drift_check |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `tpl_email_signature_standard` | active | `_assets/advops/shared/email-signatures/EMAIL_SIGNATURES.md` | all external | legal-plain | Brand Manager | SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001 | manual + jargon |
| `tpl_sequence_investor` | active | `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#investor-sequence` | investor | Tier-1 | Brand Manager | BRAND_BASELINE_REALITY_MATRIX.md | manual + jargon |
| `tpl_sequence_customer_sme` | active | `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#customer-sme-sequence` | customer-SME | Tier-2 practical | Brand Manager | SOP-ENG_DISCOVERY_QUESTIONNAIRE_001 | manual + jargon |
| `tpl_sequence_advisor` | active | `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#advisor-sequence` | advisor | concise Tier-1 | Brand Manager | ADVOPS + baseline reality | manual + jargon |
| `tpl_sequence_partner` | active | `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#partner-sequence` | partner | Tier-2 partnership | Brand Manager | SERVICE_OFFERING_CATALOG.md | manual + jargon |
| `tpl_sequence_recruiter` | active | `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#recruiter-sequence` | recruiter / candidate | practical hiring | Talent + Brand Manager | FOUNDER_BIO.md | manual + jargon |
| `tpl_sequence_enisa` | active | `_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#enisa-sequence` | ENISA reviewer / public-funds advisor | formal evidence | Brand Manager + Legal Counsel | TRADEMARK_FILING_STRATEGY_2026-05.md | manual + jargon |
| `deck_investor_12_slide` | active | `_assets/advops/shared/decks/investor-12-slide.deck.md` | investor | Tier-1 | Brand Manager | FOUNDER_BIO.md + BRAND_VISION.md | jargon + companion drift |
| `deck_sales_8_slide` | active | `_assets/advops/shared/decks/sales-8-slide.deck.md` | customer-SME | Tier-2 practical | Brand Manager | SERVICE_OFFERING_CATALOG.md | jargon + companion drift |
| `deck_advisor_4_slide` | active | `_assets/advops/shared/decks/advisor-4-slide.deck.md` | advisor | concise Tier-1 | Brand Manager | ADVOPS + FOUNDER_BIO.md | jargon + companion drift |
| `deck_partner_6_slide` | active | `_assets/advops/shared/decks/partner-6-slide.deck.md` | strategic partner | Tier-2 partnership | Brand Manager | SERVICE_OFFERING_CATALOG.md | jargon + companion drift |
| `deck_enisa_8_slide` | active | `_assets/advops/shared/decks/enisa-8-slide.deck.md` | ENISA reviewer | formal evidence | Brand Manager + Legal Counsel | trademark + tech-lab canon | jargon + companion drift |
| `deck_recruiter_6_slide` | active | `_assets/advops/shared/decks/recruiter-6-slide.deck.md` | recruiter / candidate | practical hiring | Talent + Brand Manager | FOUNDER_BIO.md | jargon + companion drift |
| `tpl_founder_bio` | active | `Admin/O5-1/People/FOUNDER_BIO.md` | all external | audience-specific | Talent | SOP-PEOPLE_FOUNDER_BIO_001 | jargon + baseline reality |
| `tpl_press_kit` | active | `_assets/advops/shared/press-kit/PRESS_KIT.md` | press / public | plain formal | Brand Manager | BRAND_ARCHITECTURE.md | manual + jargon |
| `tpl_onboarding_kit` | active | `_assets/advops/shared/onboarding/ONBOARDING_KIT.md` | collaborator / hire | practical internal-to-external bridge | Talent + Brand Manager | FOUNDER_BIO.md + BRAND_BASELINE_REALITY_MATRIX.md | manual + jargon |
| `tpl_proposal` | active | `_assets/advops/shared/proposals/PROPOSAL_TEMPLATE.md` | paid client | Tier-2 practical or Tier-1 evidence | Brand Manager | SOP-ENG_PROPOSAL_001 | jargon + baseline reality |
| `tpl_engagement_playbook` | active | `_assets/advops/shared/engagement/ENGAGEMENT_PLAYBOOK.md` | client / operator | mixed, section-specific | Holistik Researcher + Brand Manager | SOP-ENG_ENGAGEMENT_DESIGN_001 | manual + baseline reality |

## 3. Companion Contract For Decks

Every deck has three files:

1. `<name>.deck.md` — external-register deck content.
2. `<name>.objections.md` — operator-private objection handling; may cite baseline-reality internal vocabulary.
3. `<name>.counterparty-brief.md` — operator-private audience briefing; may cite internal register and must never be sent externally.

Deck companions are intentionally exempted from external-register drift checks where the validator allows it. The deck file itself is not exempt.

## 4. Promotion Rules

Templates may become publicly linked only when:

- The relevant audience journey is operator-approved.
- The template has a current registry row.
- The template's source canon has not changed since last sync.
- Drift checks pass or an explicit operator-private exemption is recorded.

This rule especially applies to `/services` and `/how-we-work`: D-IH-66-AD keeps them direct-access until I67 makes the promotion decision.

## 5. Maintenance

Maintained quarterly by `SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001`. P6 seeds this Markdown registry. The future `governance.brand_template_registry` view must preserve at least these columns:

- `template_id`
- `status`
- `source_path`
- `audience`
- `voice_tier`
- `owner`
- `governed_by`
- `drift_check`
- `last_review`
