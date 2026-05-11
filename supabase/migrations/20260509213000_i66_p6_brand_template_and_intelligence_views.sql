-- I66 P6 — governance.brand_template_registry + governance.engagement_intelligence_view
--
-- Read-side projections for the P6 operator panels in hlk-erp:
--   /governance/brand-templates
--   /governance/intelligence
--
-- Canonical sources remain in git:
--   docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_TEMPLATE_REGISTRY.md
--   docs/wip/intelligence/README.md

CREATE SCHEMA IF NOT EXISTS governance;

GRANT USAGE ON SCHEMA governance TO authenticated, anon, service_role;

CREATE OR REPLACE VIEW governance.brand_template_registry AS
SELECT *
FROM (
  VALUES
    ('tpl_email_signature_standard','active','_assets/advops/shared/email-signatures/EMAIL_SIGNATURES.md','all external','legal-plain','Brand Manager','SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001','manual + jargon','2026-05-09'::date),
    ('tpl_sequence_investor','active','_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#investor-sequence','investor','Tier-1','Brand Manager','BRAND_BASELINE_REALITY_MATRIX.md','manual + jargon','2026-05-09'::date),
    ('tpl_sequence_customer_sme','active','_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#customer-sme-sequence','customer-SME','Tier-2 practical','Brand Manager','SOP-ENG_DISCOVERY_QUESTIONNAIRE_001','manual + jargon','2026-05-09'::date),
    ('tpl_sequence_advisor','active','_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#advisor-sequence','advisor','concise Tier-1','Brand Manager','ADVOPS + baseline reality','manual + jargon','2026-05-09'::date),
    ('tpl_sequence_partner','active','_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#partner-sequence','partner','Tier-2 partnership','Brand Manager','SERVICE_OFFERING_CATALOG.md','manual + jargon','2026-05-09'::date),
    ('tpl_sequence_recruiter','active','_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#recruiter-sequence','recruiter / candidate','practical hiring','Talent + Brand Manager','FOUNDER_BIO.md','manual + jargon','2026-05-09'::date),
    ('tpl_sequence_enisa','active','_assets/advops/shared/sequences/SEQUENCE_TEMPLATES.md#enisa-sequence','ENISA reviewer','formal evidence','Brand Manager + Legal Counsel','TRADEMARK_FILING_STRATEGY_2026-05.md','manual + jargon','2026-05-09'::date),
    ('deck_investor_12_slide','active','_assets/advops/shared/decks/investor-12-slide.deck.md','investor','Tier-1','Brand Manager','FOUNDER_BIO.md + BRAND_VISION.md','jargon + companion drift','2026-05-09'::date),
    ('deck_sales_8_slide','active','_assets/advops/shared/decks/sales-8-slide.deck.md','customer-SME','Tier-2 practical','Brand Manager','SERVICE_OFFERING_CATALOG.md','jargon + companion drift','2026-05-09'::date),
    ('deck_advisor_4_slide','active','_assets/advops/shared/decks/advisor-4-slide.deck.md','advisor','concise Tier-1','Brand Manager','ADVOPS + FOUNDER_BIO.md','jargon + companion drift','2026-05-09'::date),
    ('deck_partner_6_slide','active','_assets/advops/shared/decks/partner-6-slide.deck.md','strategic partner','Tier-2 partnership','Brand Manager','SERVICE_OFFERING_CATALOG.md','jargon + companion drift','2026-05-09'::date),
    ('deck_enisa_8_slide','active','_assets/advops/shared/decks/enisa-8-slide.deck.md','ENISA reviewer','formal evidence','Brand Manager + Legal Counsel','trademark + tech-lab canon','jargon + companion drift','2026-05-09'::date),
    ('deck_recruiter_6_slide','active','_assets/advops/shared/decks/recruiter-6-slide.deck.md','recruiter / candidate','practical hiring','Talent + Brand Manager','FOUNDER_BIO.md','jargon + companion drift','2026-05-09'::date),
    ('tpl_founder_bio','active','Admin/O5-1/People/FOUNDER_BIO.md','all external','audience-specific','Talent','SOP-PEOPLE_FOUNDER_BIO_001','jargon + baseline reality','2026-05-09'::date),
    ('tpl_press_kit','active','_assets/advops/shared/press-kit/PRESS_KIT.md','press / public','plain formal','Brand Manager','BRAND_ARCHITECTURE.md','manual + jargon','2026-05-09'::date),
    ('tpl_onboarding_kit','active','_assets/advops/shared/onboarding/ONBOARDING_KIT.md','collaborator / hire','internal-to-external bridge','Talent + Brand Manager','FOUNDER_BIO.md + BRAND_BASELINE_REALITY_MATRIX.md','manual + jargon','2026-05-09'::date),
    ('tpl_proposal','active','_assets/advops/shared/proposals/PROPOSAL_TEMPLATE.md','paid client','Tier-2 practical or Tier-1 evidence','Brand Manager','SOP-ENG_PROPOSAL_001','jargon + baseline reality','2026-05-09'::date),
    ('tpl_engagement_playbook','active','_assets/advops/shared/engagement/ENGAGEMENT_PLAYBOOK.md','client / operator','mixed section-specific','Holistik Researcher + Brand Manager','SOP-ENG_ENGAGEMENT_DESIGN_001','manual + baseline reality','2026-05-09'::date)
) AS t(template_id, status, source_path, audience, voice_tier, owner, governed_by, drift_check, last_review);

COMMENT ON VIEW governance.brand_template_registry IS
  'I66 P6 - read-side projection of BRAND_TEMPLATE_REGISTRY.md for the /governance/brand-templates operator panel. Git remains canonical.';

GRANT SELECT ON governance.brand_template_registry TO authenticated, service_role;

CREATE OR REPLACE VIEW governance.engagement_intelligence_view AS
SELECT *
FROM (
  VALUES
    ('investor','docs/wip/intelligence/_templates/elicitation-template-investor.md','investor-12-slide.counterparty-brief.md','investor-12-slide.objections.md','J-IN','ready','Founder credibility, market thesis, moat, capital efficiency'),
    ('customer-sme','docs/wip/intelligence/_templates/elicitation-template-customer-sme.md','sales-8-slide.counterparty-brief.md','sales-8-slide.objections.md','J-CU','ready','Outcome clarity, price predictability, confidentiality, time-to-value'),
    ('advisor','docs/wip/intelligence/_templates/elicitation-template-advisor.md','advisor-4-slide.counterparty-brief.md','advisor-4-slide.objections.md','J-AD','ready','Clear ask, scope, closure rhythm, responsiveness'),
    ('partner','docs/wip/intelligence/_templates/elicitation-template-partner.md','partner-6-slide.counterparty-brief.md','partner-6-slide.objections.md','J-PT','ready','Complementary scope, ownership clarity, execution reliability'),
    ('enisa','docs/wip/intelligence/_templates/elicitation-template-enisa.md','enisa-8-slide.counterparty-brief.md','enisa-8-slide.objections.md','J-ENISA','ready','Technological component, scalability, employment, capital efficiency'),
    ('recruiter','docs/wip/intelligence/_templates/elicitation-template-recruiter.md','recruiter-6-slide.counterparty-brief.md','recruiter-6-slide.objections.md','J-RC','ready','Role scope, first 90 days, compensation clarity, operating seriousness'),
    ('latam-customer','docs/wip/intelligence/_templates/elicitation-template-latam-customer.md','sales-8-slide.counterparty-brief.md','sales-8-slide.objections.md','J-CU','ready','Spanish-register fit, outcome clarity, trust and handoff')
) AS t(audience_slug, elicitation_template_path, counterparty_brief_template, objections_template, baseline_row, status, decision_criteria);

COMMENT ON VIEW governance.engagement_intelligence_view IS
  'I66 P6 - read-side projection of per-audience intelligence templates and deck companions for /governance/intelligence. Git remains canonical.';

GRANT SELECT ON governance.engagement_intelligence_view TO authenticated, service_role;

NOTIFY pgrst, 'reload schema';
