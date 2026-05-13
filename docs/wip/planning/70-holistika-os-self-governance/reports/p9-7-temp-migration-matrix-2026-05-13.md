---
language: en
status: ratified
canonical: false
role_owner: Operations
classification: planning_artifact
intellectual_kind: migration_matrix
ssot: false
authored: 2026-05-13
ratified: 2026-05-13
---

# I70 P9.7 — Temp folder migration matrix (deferred-completion)

> Authored at I70 P9.7 (§9.13 in plan `holistika_os_self-governance_foundation_63841b81`)
> per the inline-ratify pattern (`.cursor/rules/akos-inline-ratification.mdc` + plan A14).
> Source enumeration: `git ls-files --others --exclude-standard temp-move-or-delete-hlk-business-context/`
> = **69 entries** (matches plan §9.13 Step 1 `wc -l` expected count).

## 1. Bucket distribution per FOUNDER_CORPUS_INVENTORY 8-section schema

| corpus_section | files | engagement_id (if any) | target_root |
|:---|---:|:---|:---|
| CVs | 2 | — (operator-only) | `v3.0/Admin/O5-1/People/Compliance/canonicals/people-files/operator/` (per Q1 ratify) |
| Engagements — Asesoría Hostelería | 14 | `eng_2026_asesoria_hosteleria` | `v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/` |
| Engagements — EFA Académie | 16 | `eng_2026_efa_collab` (+ cross-link to `eng_2026_suez_webuy`) | `v3.0/Think Big/Clients/2026-efa-collab/` (NEW folder) + cross-engagement `2026-suez-webuy/00-internal/source-materials/efa/` |
| Engagements — ShadowGPU | 2 | `eng_2026_shadowgpu_inbound` | `v3.0/Think Big/Clients/2026-shadowgpu-inbound/00-internal/source-materials/transcripts/` (NEW folder) |
| Engagements — Internal Service Mgmt SSOT | 8 | `eng_2026_internal_service_management_ssot` | `v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/` (NEW folder) |
| Engagements — Websitz / Rushly | 4 (Use case 1) + 23 (Use case 2) = 27 | `eng_2026_websitz_use_case_2_rushly` (archived) | `v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/` (NEW folder; archived engagement) |
| **TOTAL** | **69** | | |

## 2. Per-file migration matrix

Columns: `source_path | corpus_section | target_path | proposed_action | retention_class | confidentiality | engagement_link | notes`. `proposed_action` ∈ {`move`, `move+rename`, `move+cross-link`, `review`}.

### 2.1 CVs (2 files)

> Q1 + Q2 ratify (2026-05-13): my initial proposal placed CVs at `People/00-internal/cvs/`, mirroring the engagement-pack `00-internal/01-operator-pack/02-customer-pack/` convention. Operator (Q1 strategic ask) flagged this as wrong — the engagement-pack slug system was authored for client-facing deliverables, not People-area governance artifacts. Correct placement is `People/Compliance/canonicals/people-files/<person-slug>/` (Compliance owns canonical artifacts; one folder per person scales to team). For the operator (currently single-founder), slug = `operator`; Fayçal_Njoya is the operator. Diacritic is preserved per Q2 (modern filesystems handle UTF-8 fine; folder slug stays kebab-case for git+URL safety).

| source_path | corpus_section | target_path | action | retention | conf. | engagement | notes |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `temp-…/CV LinkedinProfile.pdf` | CVs | `v3.0/Admin/O5-1/People/Compliance/canonicals/people-files/operator/CV_LinkedIn_Profile.pdf` | move+rename | operator-only | confidential | (none) | Renamed for filesystem safety (space stripped, "Linkedin" → "LinkedIn"). Cross-link from `FOUNDER_TRAJECTORY_INTERNAL.md` per H3. |
| `temp-…/Fayçal Njoya CV - EN.pdf` | CVs | `v3.0/Admin/O5-1/People/Compliance/canonicals/people-files/operator/Fayçal_Njoya_CV_EN.pdf` | move+rename | operator-only | confidential | (none) | Diacritic preserved (Q2 ratify); spaces → underscores for filesystem safety. Per H3 explicit name in CV inventory. |

### 2.2 Asesoría Hostelería (14 files)

Audio transcripts (5):

| source_path | target_path | action | notes |
|:---|:---|:---|:---|
| `temp-…/Asesoria Hosteleria/2026-08-04 - Kick-Off Asesoría Hostelería.m4a.md` | `v3.0/…/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-08-04-kick-off-asesoria-hosteleria.m4a.md` | move+rename | Kick-off transcript. |
| `temp-…/Asesoria Hosteleria/2026-10-05 - Consultoría Hostelería - Admin Course - 4.m4a.md` | `…/transcripts/2026-10-05-admin-course-04.m4a.md` | move+rename | Admin course session 4. |
| `temp-…/Asesoria Hosteleria/2026-12-04 - Consultoría Hostelería - Admin Course - 1.m4a.md` | `…/transcripts/2026-12-04-admin-course-01.m4a.md` | move+rename | Admin course session 1. |
| `temp-…/Asesoria Hosteleria/2026-12-04 - Consultoría Hostelería - Estudio de Mercado y PESTEL - 2.m4a.md` | `…/transcripts/2026-12-04-pestel-research-02.m4a.md` | move+rename | PESTEL session 2. |
| `temp-…/Asesoria Hosteleria/2026-30-04 - Consultoría Hostelería - Admin Course - 3.m4a.md` | `…/transcripts/2026-04-30-admin-course-03.m4a.md` | move+rename | Date format normalized YYYY-MM-DD. |

gdrive Project Cameroon GTM (9 files); preserve subfolder structure under `…/source-materials/gdrive/project-cameroon-gtm/`:

| source_path | target_path | action |
|:---|:---|:---|
| `…/Business Plan/Finance/Placeholder - Billing Plan - Revenue and Costs Transactions - Profits and Loses Balance Sheet.xlsx` | `…/gdrive/project-cameroon-gtm/business-plan/finance/billing-plan-and-pnl-placeholder.xlsx` | move+rename |
| `…/Business Plan/Marketing/Placeholder - Channels - Buyer persona - Brand Persona.docx` | `…/gdrive/project-cameroon-gtm/business-plan/marketing/channels-personas-placeholder.docx` | move+rename |
| `…/Business Plan/Marketing/Placeholder - Editorial Calendar - Per channel message.xlsx` | `…/gdrive/project-cameroon-gtm/business-plan/marketing/editorial-calendar-placeholder.xlsx` | move+rename |
| `…/Business Plan/Marketing/Placeholder - Leads and Customers.xlsx` | `…/gdrive/project-cameroon-gtm/business-plan/marketing/leads-and-customers-placeholder.xlsx` | move+rename |
| `…/Business Plan/People - HR/People - Profiles - Internal and External employee profiles costs and tarifs.xlsx` | `…/gdrive/project-cameroon-gtm/business-plan/people-hr/people-profiles-rates.xlsx` | move+rename |
| `…/Business Plan/Project - Operations/Placeholder - Process Inventory - Backlog and Project Plan with Gantt.xlsx` | `…/gdrive/project-cameroon-gtm/business-plan/project-operations/process-inventory-and-gantt-placeholder.xlsx` | move+rename |
| `…/Business Plan/Tech - Data/Placeholder - Main Standard Operating Process (Manual) for business operator no IT  - Single Source of Truth.docx` | `…/gdrive/project-cameroon-gtm/business-plan/tech-data/main-sop-manual-placeholder.docx` | move+rename |
| `…/References - Research/5 Forces porter en hôtellerie - FR - Vue client B2B.pdf` | `…/gdrive/project-cameroon-gtm/references-research/5-forces-porter-hotellerie-b2b.fr.pdf` | move+rename |
| `…/References - Research/Plan GTM Consultoría Hotelera Camerún.docx` | `…/gdrive/project-cameroon-gtm/references-research/plan-gtm-consultoria-hotelera-camerun.es.docx` | move+rename |

### 2.3 EFA Académie (16 files; split across `2026-efa-collab/` and `2026-suez-webuy/00-internal/source-materials/efa/`)

EFA-as-org / EFA brand / EFA cobranding context → `2026-efa-collab/` (NEW engagement folder):

| source_path | target_path | action | notes |
|:---|:---|:---|:---|
| `…/EFA/EFA ACCADEMIE Logo png.png` | `…/2026-efa-collab/00-internal/brand-assets/efa-academie-logo.source.png` | review | `_external_marks/efa-academie-logo.png` already exists in SUEZ folder; this is the SOURCE before processing. Recommend: keep both (source + processed). Spot-check Q11. |
| `…/EFA/EFA ACCADEMIE sur fonds Blancs.png` | `…/2026-efa-collab/00-internal/brand-assets/efa-academie-logo-on-white.source.png` | review | Same as above. |
| `…/EFA/PRESENTATION CREATION ET JOIE.docx` | `…/2026-efa-collab/00-internal/source-materials/presentation-creation-et-joie.docx` | move+rename | EFA mission/values deck ("Création et joie"). |
| `…/EFA/PRESENTATION CREATION ET JOIE.docx.pdf` | `…/2026-efa-collab/00-internal/source-materials/presentation-creation-et-joie.pdf` | move+rename | PDF export of above. |
| `…/EFA/08-04-2026 19.02 - EFA project prospection.mp3` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-08-efa-project-prospection.mp3` | move+rename | Date format normalized. |
| `…/EFA/08-04-2026 19.02 - EFA project prospection.mp3.md` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-08-efa-project-prospection.mp3.md` | move+rename | Transcript paired with above. |
| `…/EFA/2026-04-17 19.46 - Holistika Research - Researcher Onboarding.mp3` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-17-holistika-research-researcher-onboarding.mp3` | move+rename | Researcher onboarding for EFA-Holistika joint research arm. |
| `…/EFA/2026-04-17 19.46 - Holistika Research - Researcher Onboarding.mp3.md` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-17-holistika-research-researcher-onboarding.mp3.md` | move+rename | Transcript paired. |
| `…/EFA/2026-12-12 - Holistika Research - Business Developer Onboarding.m4a.md` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-12-12-business-developer-onboarding.m4a.md` | move+rename | Business developer onboarding. |
| `…/EFA/WhatsApp Audio 2026-05-10 at 18.20.47.opus.mp3.md` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-05-10-whatsapp-audio-18-20-47.opus.mp3.md` | move+rename | General comms; no source `.opus.mp3` paired in temp (transcript-only). |
| `…/EFA/WhatsApp Audio 2026-05-10 at 18.21.10.opus.mp3.md` | `…/2026-efa-collab/00-internal/source-materials/transcripts/2026-05-10-whatsapp-audio-18-21-10.opus.mp3.md` | move+rename | Same. |

EFA materials specifically tied to the SUEZ × WeBuy engagement → `2026-suez-webuy/00-internal/source-materials/efa/`:

| source_path | target_path | action | notes |
|:---|:---|:---|:---|
| `…/EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 1.m4a.md` | `…/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-01.m4a.md` | move+rename | SUEZ-specific proposal briefing. |
| `…/EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 3.m4a.md` | `…/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-03.m4a.md` | move+rename | SUEZ-specific proposal briefing 3 (briefing 2 absent in temp). |
| `…/EFA/CDC_WeBuy_SUEZ.docx` | `…/2026-suez-webuy/00-internal/source-materials/efa/CDC_WeBuy_SUEZ.docx` | move | SUEZ × WeBuy cahier des charges authored by EFA. Cross-link from `eng_2026_efa_collab` notes. |
| `…/EFA/CDC_WeBuy_SUEZ.docx.pdf` | `…/2026-suez-webuy/00-internal/source-materials/efa/CDC_WeBuy_SUEZ.pdf` | move+rename | PDF export of above. |
| `…/EFA/Mode opératoire - Process de passage de commande WeBuy.pdf` | `…/2026-suez-webuy/00-internal/source-materials/efa/mode-operatoire-passage-commande-webuy.fr.pdf` | move+rename | SUEZ × WeBuy operating procedure (FR). |

### 2.4 ShadowGPU (2 files)

| source_path | target_path | action | notes |
|:---|:---|:---|:---|
| `…/ShadowGPU/27-02-2026 15.11 shadow gpu x holistika meeting.mp3` | `…/2026-shadowgpu-inbound/00-internal/source-materials/transcripts/2026-02-27-shadowgpu-x-holistika-meeting.mp3` | move+rename | First meeting; cited in `GOI-SUP-SHGPU-2026` (D-IH-70-AC). |
| `…/ShadowGPU/27-02-2026 15.11 shadow gpu x holistika meeting.mp3.md` | `…/2026-shadowgpu-inbound/00-internal/source-materials/transcripts/2026-02-27-shadowgpu-x-holistika-meeting.mp3.md` | move+rename | Transcript paired. |

### 2.5 Internal Service Management SSOT (8 files)

All Project Baseline GTM placeholder files mirror the Asesoría Cameroon-GTM gdrive structure (consistent template); preserve under `…/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/`:

| source_path | target_path | action |
|:---|:---|:---|
| `…/Project Baseline - Go-To-Market/Business Plan/Finance/Placeholder - Billing Plan and Costs.xlsx` | `…/project-baseline-gtm/business-plan/finance/billing-plan-and-costs-placeholder.xlsx` | move+rename |
| `…/Business Plan/Marketing/Placeholder - Channels - Buyer persona - Brand Persona.docx` | `…/project-baseline-gtm/business-plan/marketing/channels-personas-placeholder.docx` | move+rename |
| `…/Business Plan/Marketing/Placeholder - Editorial Calendar - Per channel message.xlsx` | `…/project-baseline-gtm/business-plan/marketing/editorial-calendar-placeholder.xlsx` | move+rename |
| `…/Business Plan/Marketing/Placeholder - Leads and Customers.xlsx` | `…/project-baseline-gtm/business-plan/marketing/leads-and-customers-placeholder.xlsx` | move+rename |
| `…/Business Plan/People - HR/People - Profiles - Internal and External employee profiles costs and tarifs.xlsx` | `…/project-baseline-gtm/business-plan/people-hr/people-profiles-rates.xlsx` | move+rename |
| `…/Business Plan/Project - Operations/Placeholder - Process Inventory - Backlog and Project Plan with Gantt.xlsx` | `…/project-baseline-gtm/business-plan/project-operations/process-inventory-and-gantt-placeholder.xlsx` | move+rename |
| `…/Business Plan/Tech - Data/Placeholder - Main Standard Operating Process (Manual) for business operator no IT  - Single Source of Truth.docx` | `…/project-baseline-gtm/business-plan/tech-data/main-sop-manual-placeholder.docx` | move+rename |
| `…/References - Research/Placeholder - GTM PHESTEL Research.docx` | `…/project-baseline-gtm/references-research/gtm-phestel-research-placeholder.docx` | move+rename |

### 2.6 Websitz / Rushly (27 files; one engagement folder, two use cases)

Use case 1 (shopify) — 4 files → `…/2026-websitz-rushly/00-internal/source-materials/use-case-1-shopify/transcripts/`:

| source_path | target_path | action | notes |
|:---|:---|:---|:---|
| `…/Websitz/Use case 1 (shopify)/16-03-2026 21.09 - Holistika x Websitz x EFA.mp3` | `…/use-case-1-shopify/transcripts/2026-03-16-holistika-x-websitz-x-efa.mp3` | move+rename | Three-party meeting; cross-link to `eng_2026_efa_collab`. |
| `…/Websitz/Use case 1 (shopify)/16-03-2026 21.09 - Holistika x Websitz x EFA.mp3.md` | `…/use-case-1-shopify/transcripts/2026-03-16-holistika-x-websitz-x-efa.mp3.md` | move+rename | Transcript paired. |
| `…/Websitz/Use case 1 (shopify)/23-03-2026 20.03 - Holistika x Websitz - Cart Bundle App review.mp3` | `…/use-case-1-shopify/transcripts/2026-03-23-cart-bundle-app-review.mp3` | move+rename | Competitor review (Cart Bundle App); evidence base for D-IH-70-AC `competitor_intelligence_target` deferral. |
| `…/Websitz/Use case 1 (shopify)/23-03-2026 20.03 - Holistika x Websitz - Cart Bundle App review.mp3.md` | `…/use-case-1-shopify/transcripts/2026-03-23-cart-bundle-app-review.mp3.md` | move+rename | Transcript paired. |

Use case 2 (Rushly) — 23 files → `…/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/`:

| source_path | target_path | action | notes |
|:---|:---|:---|:---|
| `…/Websitz/Use case 2/2026-04-01 15.33 - presentation projet 2.mp3` | `…/use-case-2-rushly/transcripts/2026-04-01-presentation-projet-2.mp3` | move+rename | Project 2 presentation (kick-off). |
| `…/Websitz/Use case 2/2026-04-01 15.33 - presentation projet 2.mp3.md.docx` | `…/use-case-2-rushly/transcripts/2026-04-01-presentation-projet-2.mp3.md.docx` | move+rename | Transcript export (docx wrapper). |
| `…/Websitz/Use case 2/Rushly_Cahier_des_charges_v2.docx` | `…/use-case-2-rushly/cahier-des-charges/Rushly_CDC_v2.docx` | move+rename | Rushly CDC v2. |
| `…/Websitz/Use case 2/Rushly_Cahier_des_charges_v2.docx.md` | `…/use-case-2-rushly/cahier-des-charges/Rushly_CDC_v2.md` | move+rename | Markdown extraction of CDC v2. |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.51.40.opus.mp3` | `…/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-51-40.opus.mp3` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.51.40.opus.mp3.md` | `…/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-51-40.opus.mp3.md` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.52.26.opus.mp3` | `…/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-52-26.opus.mp3` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.52.26.opus.mp3.md` | `…/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-52-26.opus.mp3.md` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.51.29.opus.mp3` | `…/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-51-29.opus.mp3` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.51.29.opus.mp3.md` | `…/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-51-29.opus.mp3.md` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.52.34.opus.mp3` | `…/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-52-34.opus.mp3` | move+rename | |
| `…/Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.52.34.opus.mp3.md` | `…/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-52-34.opus.mp3.md` | move+rename | |
| `…/Websitz/Use case 2/agentic-artificial-intelligence.pdf` | `…/use-case-2-rushly/references/agentic-artificial-intelligence.pdf` | move | External research PDF reference (not authored by us); kept with engagement source-materials. |
| `…/Websitz/Use case 2/gdrive/Kick-off message.docx` | `…/use-case-2-rushly/gdrive/kick-off-message.docx` | move+rename | |
| `…/Websitz/Use case 2/gdrive/rushly_mvp_roadmap_3cd96613.plan.md.docx` | `…/use-case-2-rushly/gdrive/rushly_mvp_roadmap_3cd96613.plan.md.docx` | move | Plan file (already kebab-cased upstream). |
| `…/Websitz/Use case 2/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.fr.md.docx` | `…/use-case-2-rushly/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.fr.md.docx` | move | |
| `…/Websitz/Use case 2/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.md.docx` | `…/use-case-2-rushly/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.md.docx` | move | |
| `…/Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/01_Project_Overview.md.docx` | `…/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/01_Project_Overview.md.docx` | move | |
| `…/Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/02_Shared_Decisions_And_Open_Items.md.docx` | `…/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/02_Shared_Decisions_And_Open_Items.md.docx` | move | |
| `…/Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/03_Status_And_Next_Steps.md.docx` | `…/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/03_Status_And_Next_Steps.md.docx` | move | |
| `…/Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/04_Websitz_Inputs_And_Dependencies.md.docx` | `…/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/04_Websitz_Inputs_And_Dependencies.md.docx` | move | |
| `…/Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/Plan de faisabilite et aspects de produit.md.docx` | `…/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/plan-de-faisabilite-et-aspects-de-produit.md.docx` | move+rename | |
| `…/Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/README.md.docx` | `…/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/README.md.docx` | move | |

## 3. Spot-check sampling strategy (12 rows for inline AskQuestion)

Per plan §9.13 Step 3: 2 from CVs + 2 from each engagement bucket (5 buckets × 2 = 10) + 2 misc = 14. Compressed to **12** spot-check rows distributed across all 6 buckets:

- Q1: CV LinkedIn rename
- Q2: CV Fayçal rename
- Q3: Asesoría transcript date-normalization
- Q4: Asesoría gdrive Cameroon-GTM subfolder preservation
- Q5: EFA brand-asset duplication question (`review` action)
- Q6: EFA cross-engagement split (CDC_WeBuy_SUEZ → SUEZ folder vs EFA folder)
- Q7: ShadowGPU placement (Clients/ vs Marketing/Brand/AV/Advisers/)
- Q8: Internal Service Mgmt SSOT folder slug (`2026-internal-service-management-ssot/`)
- Q9: Websitz folder collapse (Use case 1 + Use case 2 under one `2026-websitz-rushly/` folder)
- Q10: agentic-AI PDF placement (engagement reference vs Research/Intelligence/external-references/)
- Q11: EFA logos `_external_marks/` already populated — keep source PNGs in EFA folder or skip-and-delete?
- Q12: Holistika×Websitz×EFA tri-party meeting — Websitz folder primary, EFA cross-link

## 4. Audit log

- 2026-05-13 17:30 — Matrix authored after `git ls-files` enumeration confirms 69 entries.
- 2026-05-13 17:35 — Inline-ratify gate opens via `AskQuestion` (12 spot-check rows).
- 2026-05-13 17:55 — Operator ratifications received per question:
  - **Q1 (CV LinkedIn)**: approve **with strategic correction** — agent's `People/00-internal/cvs/` was wrong (engagement-pack slug, not people-area). Corrected to `People/Compliance/canonicals/people-files/operator/CV_LinkedIn_Profile.pdf`. Forward-compatible: `people-files/<person-slug>/` scales to team (one folder per person, holding all their CVs + onboarding + departure paperwork when applicable).
  - **Q2 (Fayçal CV)**: `keep_diacritic` — `Fayçal_Njoya_CV_EN.pdf` (UTF-8 filename; folder slug `operator` kebab-case clean).
  - **Q3 (Asesoría transcripts)**: `approve` — date+slug normalisation across all 5 transcript .md files.
  - **Q4 (Asesoría gdrive)**: `approve` — subfolder preservation + slug normalisation. **Strategic deferral** flagged by operator: region (Cameroon) is a governance dimension that needs separate treatment ("differentiate others' interests in Cameroon than ours"; operator has personal Cameroon collaborator network distinct from Asesoría's customer-facing GTM project). Deferred to follow-up: extend `engagement_registry` (or new dimensions table) with `region` column, capture operator's personal Cameroon GOIs as distinct rows from `eng_2026_asesoria_hosteleria` counterparties. Tracked under **I72 scope-extension or new I73 charter** (see §6 strategic deferrals).
  - **Q5 (EFA brand assets)**: `efa_brand_assets` — file source PNGs in `2026-efa-collab/00-internal/brand-assets/` as `*.source.png` variants (preserves audit trail; SUEZ `_external_marks/` keeps the customer-facing processed copies).
  - **Q6 (EFA cross-engagement split)**: `approve_split` — SUEZ-specific (CDC, Mode opératoire, EFA×SUEZ proposal briefings) → SUEZ folder; EFA-org context (logos, CRÉATION ET JOIE deck, EFA-recruitment transcripts) → EFA folder.
  - **Q7 (ShadowGPU)**: `clients` (option A) — Clients/2026-shadowgpu-inbound/ confirmed. **Strategic correction by operator**: ShadowGPU is a **supplier candidate where we are the early-adopter customer**, not a `collaborator-inbound` advisor and never an investor. Engagement happened because operator (as researcher/strategist) chose early-adopter posture per Porter's 5-forces analysis. Operator already routed RunPod as preferred GPU/cloud supplier (lower deploy friction); ShadowGPU may stay as backup or sunset. Deferred follow-up: (a) review `eng_2026_shadowgpu_inbound.engagement_class` — `collaborator-inbound` is imprecise; better: `vendor-trial` or `supplier-evaluation-as-customer` (new class for I72 enum extension); (b) add `GOI-SUP-RUNPOD-2026` row to GOI_POI_REGISTER (currently missing — RunPod is the active preferred supplier); (c) cross-link both ShadowGPU and RunPod GOI rows to a `SOURCING_REGISTER.csv` when first paid invoice lands. Plan §9.13's `Marketing/Brand/AV/Advisers/` placement (where AV = audiovisual) was a stale pre-engagement-registry default — overridden by the engagement-registry-promotion convention (every active engagement_registry row → a Clients/ folder). Tracked under **I72 scope-extension** (see §6).
  - **Q8 (SMO SSOT slug)**: agent recommends + flags **strategic deferral** — operator clarified these 8 files are NOT internal SMO canonicals; they are a **customer-facing GTM-template prototype** (productized starter knowledge-base for SMB customers; future MADEIRA-AKOS-style product). For *this* commit, agent files at `Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/` (matches `eng_2026_internal_service_management_ssot` engagement_registry row + plan §9.13 line 3298). Future-state placement: `v3.0/Think Big/Products/<madeira-customer-template-slug>/` once productization initiative formalises (likely **I74 Brand-tooling productization line** per existing AIC scope D-IH-70-V, or a sibling I73 if AKOS-as-library scope dilution risk surfaces). Strategic asks captured at §6 + §7 below.
  - **Q9 (Websitz collapse)**: `collapse` — one folder, two subfolders (`use-case-1-shopify/` + `use-case-2-rushly/`).
  - **Q10 (agentic-AI PDF)**: `with_engagement` — file under `2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/references/`.
  - **Q11 (Holistika×Websitz×EFA tri-party)**: `websitz_primary` — Websitz folder primary, EFA cross-link in notes.
  - **Q12 (executor)**: `approve` — full sequence (matrix → --dry-run → --execute → validators → `git rm temp/` → atomic commit).

## 6. Strategic deferrals captured during inline-ratify (operator-flagged)

The Q4 + Q7 + Q8 ratifications surfaced three structural decisions that are **out of P9.7 scope** but must be tracked so they don't drop. None block the migration commit; all are recorded here as forward-references to existing/upcoming initiatives. The operator explicitly asked for "strategic decisions and guidance" on Q8 — agent's synthesised recommendations are below.

### 6.1 Region as a governance dimension (Q4)

- **Operator framing**: "Region is a dimension we should govern as I always say when I do a research intel or PESTEL analysis. … differentiate others' interests in Cameroon than ours."
- **Current state**: no `region` column on `engagement_registry`, `goipoi_register`, or any other dimension table. Cameroon shows up only in free-text notes (`Asesoría Hostelería Cameroon GTM` engagement name + Cameroon-GTM gdrive folder name).
- **Agent recommendation**: **defer to I72 scope-extension** OR a new I73 ("Region/territory governance"). Concretely: add `region_iso_3166_2` column to `goipoi_register` (e.g., `CM` for Cameroon, `ES` for Spain, `FR` for France) + `regions_active` ARRAY column to `engagement_registry`. This lets PESTEL analyses bind to regions structurally, and disambiguates operator's personal CM network from customer-facing CM-GTM engagements via `goipoi_register.client_internal_flag` (already exists) + `region_iso_3166_2`.
- **No action this commit.** Folded into §6.4 strategic-summary deliverable.

### 6.2 ShadowGPU engagement class + missing RunPod row (Q7)

- **Operator framing**: ShadowGPU is a **supplier where we are the customer (early adopter)**, not a `collaborator-inbound` advisor and never an investor. RunPod is the current preferred GPU/cloud supplier.
- **Issues**:
  1. `engagement_class=collaborator-inbound` for `eng_2026_shadowgpu_inbound` is imprecise. Better: `vendor-trial` or `supplier-evaluation-as-customer` (new class).
  2. RunPod has no GOI/POI row despite being the active preferred supplier — gap surfaced today.
  3. No `SOURCING_REGISTER.csv` exists yet to track per-supplier commercial state (trial/active/sunset/churned).
- **Agent recommendation**: **defer all three to I72 scope-extension** (already gated_operator). Specifically:
  - Add `vendor-trial` (and possibly `supplier-evaluation-as-customer` if we want explicit early-adopter framing) to the `engagement_class` enum at I72 P-N (charter session needed first).
  - Author `GOI-SUP-RUNPOD-2026` row at I72 alongside the IntelligenceOps register schema work.
  - Author `SOURCING_REGISTER.csv` at I72 (or I74 if it's productization-adjacent) once first paid GPU/cloud invoice lands (currently both ShadowGPU and RunPod are in evaluation/free-tier mode per operator).
- **No action this commit.** Migration files as `Clients/2026-shadowgpu-inbound/` per ratify; engagement-class re-classification is post-hoc.

### 6.3 Customer-facing GTM-template productization (Q8 — most strategic ask)

- **Operator framing**: "It's a template of the knowledge base gdrive structure I intend to serve to customers. It's a prototype so maybe that's not the best place for this. The goal is to streamline GTM operations for small customers/entrepreneurs who have the minimum governance to GTM without our jargon, easy to operate, without that many values to fill, easy to maintain… and of course I didn't still refine this product yet (even us are reworking the knowledge base). Apart from that, this will also have the byproduct of letting us build an agent madeira-type for people."
- **Agent's strategic synthesis** (operator asked explicitly for "strategic decisions and guidance and expertise"):

  **What this artifact is.** The 8 Project Baseline GTM placeholder files form a **customer-deliverable starter pack**: a stripped-down, jargon-free knowledge-base template that an SMB customer can self-populate after a short onboarding. It is *not* internal SMO canonical material — `SOP-SERVICE_MGMT_001.md` + `SERVICE_CATALOG.csv` + `SLA_MATRIX.md` (the actual SMO canonicals) live under `Operations/SMO/canonicals/` and govern *Holistika's* service delivery. The temp-folder placeholders govern *the customer's* GTM, packaged as a sellable artifact.

  **Why this matters for OS shape.** This is a **second AIC-class deliverable** (per D-IH-70-V parent class) sitting alongside MADEIRA-AKOS productization and the I74 brand-tooling line. Agent recommends naming it provisionally **MADEIRA-CUSTOMER-TEMPLATE** (or shorter: **MCT**) until operator chooses a brand name. Three properties make it AIC-class:
  1. *Externally consumable*: shipped to customers as part of GTM-consulting engagement deliverables.
  2. *Structurally separable from internal canonicals*: customer doesn't see Holistika's SMO/SOP-SERVICE_MGMT internals.
  3. *Productization candidate*: today an 8-file template; tomorrow an agent-driven onboarding flow ("madeira-type for people") that populates the template by interviewing the customer.

  **Recommended OS placement (forward state).** A new top-level **`v3.0/Think Big/Products/`** branch sibling to `Clients/`. Inside: one folder per product (`madeira-akos/`, `madeira-customer-template/`, `brand-tooling-line/`, etc.). Each product folder mirrors the engagement-pack convention but adapted: `00-source/` (the source-of-truth template), `01-customer-deliverable/` (the version shipped), `_versions/` (semantic-versioned releases).

  **Why not move now (this commit):**
  - The engagement_registry already created `eng_2026_internal_service_management_ssot` and the plan §9.13 explicitly maps these 8 files there. Re-routing mid-commit would deviate from the inline-ratify scope (Q12 already approved the atomic commit shape).
  - The Products/ branch doesn't exist yet; creating it requires operator-ratified naming + folder structure (governance event in its own right; out of scope for a temp-migration commit).
  - The engagement label "Internal Service Management SSOT" misnames the artifact, but **fixing the label requires re-thinking the engagement_registry vs. product_registry distinction**, which is itself a strategic decision deserving a dedicated session.

  **Recommended next action (post-P9.7):** Open a new initiative — **I73 (Productization-area governance: Products/ branch + product_registry table + MADEIRA-CUSTOMER-TEMPLATE migration)** — that:
  1. Authors `v3.0/Think Big/Products/README.md` + branch.
  2. Adds `product_registry.csv` canonical (parallel to `engagement_registry.csv`) under `Operations/PMO/canonicals/`.
  3. Migrates the 8 GTM-template files from `Clients/2026-internal-service-management-ssot/` → `Products/madeira-customer-template/00-source/`.
  4. Reclassifies `eng_2026_internal_service_management_ssot` → either deletes the row (if there's no actual internal *engagement* and it was just a label-of-convenience for the template) OR keeps it as the internal "we use the template ourselves to test it" engagement.
  5. Adds product-onboarding-agent scope to the **Madeira-line** roadmap (the "agent madeira-type for people" the operator referenced).

  **Why this maps to the AIC framework.** D-IH-70-V already established AIC = "AKOS Implementation Class" = parent for externally-consumable deliverables. MADEIRA-CUSTOMER-TEMPLATE fits the AIC pattern: source canonical lives in our repo + ships to customers in a stripped form. I73 is **the third AIC-line** (after MADEIRA-AKOS-as-library + I74 brand-tooling).

- **No action this commit** beyond filing per ratified Q8 long-slug. Deferral captured here + in §6.4 strategic summary.

### 6.4 Strategic-summary deliverable (post-commit)

After the P9.7 atomic commit lands, agent will surface a brief strategic-summary message in chat (not a separate file) capturing:
1. Region governance dimension (§6.1) — fold into I72 scope-extension.
2. ShadowGPU engagement class + RunPod GOI row + SOURCING_REGISTER (§6.2) — fold into I72 scope-extension.
3. Productization-area governance + MADEIRA-CUSTOMER-TEMPLATE (§6.3) — propose new **I73** initiative for operator ratification at I71 P0 charter session (or its own kick-off chat).

Operator decides at I71 P0 whether to fold these into existing slots or open new I-numbers.

## 7. Cross-references

- Plan §9.13 (Phase 9.7 deferred-completion).
- `.cursor/rules/akos-inline-ratification.mdc` (A14 inline-ratify pattern).
- `FOUNDER_CORPUS_INVENTORY.md` (8-section corpus schema).
- `ENGAGEMENT_REGISTRY.csv` (6 engagement rows; 5 of 6 receive temp-folder source materials; ShadowGPU class reclassification deferred to I72).
- `GOI_POI_REGISTER.csv` `GOI-SUP-SHGPU-2026` (cites the ShadowGPU meeting transcript file as evidence; RunPod row deferred to I72).
- `SOP-SERVICE_MGMT_001.md` + `SERVICE_CATALOG.csv` (SMO charter; orthogonal to the customer-facing GTM-template prototype filed under `2026-internal-service-management-ssot/`; productization migration deferred to proposed I73).
- D-IH-70-V (AIC parent class) — the framework I73 productization-area governance extends.

## 5. Cross-references

- Plan §9.13 (Phase 9.7 deferred-completion).
- `.cursor/rules/akos-inline-ratification.mdc` (A14 inline-ratify pattern).
- `FOUNDER_CORPUS_INVENTORY.md` (8-section corpus schema).
- `ENGAGEMENT_REGISTRY.csv` (6 engagement rows; 5 of 6 receive temp-folder source materials).
- `GOI_POI_REGISTER.csv` `GOI-SUP-SHGPU-2026` (cites the ShadowGPU meeting transcript file as evidence).
