"""I70 P9.7 — temp folder corpus migration executor.

Reads the per-file migration matrix authored at
``docs/wip/planning/70-holistika-os-self-governance/reports/p9-7-temp-migration-matrix-2026-05-13.md``
(human-readable audit artifact) and executes the moves via ``git mv`` so
``git log --follow`` preserves history.

Per A2 file-deletion safety contract: ``--dry-run`` is the DEFAULT mode.
``--execute`` must be passed explicitly to actually perform the moves.

Manifest source. The matrix-file is the human-readable source of truth; this
script embeds the same manifest as a Python list (so edits stay in lock-step
with the matrix-file). When the matrix is amended via inline-ratify
``AskQuestion``, both this script + the matrix file get updated in the same
commit.

Idempotence. Re-running with no changes is a no-op (skip rows where source
no longer exists AND target already exists; warn on partial states).

Usage::

    py scripts/migrate_temp_corpus.py --dry-run    # preview the 69 git mv
    py scripts/migrate_temp_corpus.py --execute    # apply the moves

Refs: plan §9.13, A2, A14, H1.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMP_ROOT = REPO / "temp-move-or-delete-hlk-business-context"

# (source_relative, target_relative) tuples. Source paths are relative to
# TEMP_ROOT; target paths are relative to REPO. Diacritics preserved as
# operator-ratified at Q2 of the inline-ratify gate. Ratified 2026-05-13.

MIGRATIONS: list[tuple[str, str]] = [
    # ------------------------------------------------------------------
    # 2.1 CVs (Q1 strategic correction: People/Compliance/canonicals/people-files/operator/)
    # ------------------------------------------------------------------
    (
        "CV LinkedinProfile.pdf",
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/people-files/operator/CV_LinkedIn_Profile.pdf",
    ),
    (
        "Fayçal Njoya CV - EN.pdf",
        "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/people-files/operator/Fayçal_Njoya_CV_EN.pdf",
    ),
    # ------------------------------------------------------------------
    # 2.2 Asesoría Hostelería — 14 files
    # ------------------------------------------------------------------
    # Audio transcripts (5)
    (
        "Asesoria Hosteleria/2026-08-04 - Kick-Off Asesoría Hostelería.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-08-04-kick-off-asesoria-hosteleria.m4a.md",
    ),
    (
        "Asesoria Hosteleria/2026-10-05 - Consultoría Hostelería - Admin Course - 4.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-10-05-admin-course-04.m4a.md",
    ),
    (
        "Asesoria Hosteleria/2026-12-04 - Consultoría Hostelería - Admin Course - 1.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-12-04-admin-course-01.m4a.md",
    ),
    (
        "Asesoria Hosteleria/2026-12-04 - Consultoría Hostelería - Estudio de Mercado y PESTEL - 2.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-12-04-pestel-research-02.m4a.md",
    ),
    (
        "Asesoria Hosteleria/2026-30-04 - Consultoría Hostelería - Admin Course - 3.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-04-30-admin-course-03.m4a.md",
    ),
    # gdrive Project Cameroon GTM (9)
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/Finance/Placeholder - Billing Plan - Revenue and Costs Transactions - Profits and Loses Balance Sheet.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/finance/billing-plan-and-pnl-placeholder.xlsx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/Marketing/Placeholder - Channels - Buyer persona - Brand Persona.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/marketing/channels-personas-placeholder.docx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/Marketing/Placeholder - Editorial Calendar - Per channel message.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/marketing/editorial-calendar-placeholder.xlsx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/Marketing/Placeholder - Leads and Customers.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/marketing/leads-and-customers-placeholder.xlsx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/People - HR/People - Profiles - Internal and External employee profiles costs and tarifs.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/people-hr/people-profiles-rates.xlsx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/Project - Operations/Placeholder - Process Inventory - Backlog and Project Plan with Gantt.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/project-operations/process-inventory-and-gantt-placeholder.xlsx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/Business Plan/Tech - Data/Placeholder - Main Standard Operating Process (Manual) for business operator no IT  - Single Source of Truth.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/business-plan/tech-data/main-sop-manual-placeholder.docx",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/References - Research/5 Forces porter en hôtellerie - FR - Vue client B2B.pdf",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/references-research/5-forces-porter-hotellerie-b2b.fr.pdf",
    ),
    (
        "Asesoria Hosteleria/gdrive/Project Cameroon Hospitality Go-To-Market/References - Research/Plan GTM Consultoría Hotelera Camerún.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/gdrive/project-cameroon-gtm/references-research/plan-gtm-consultoria-hotelera-camerun.es.docx",
    ),
    # ------------------------------------------------------------------
    # 2.3 EFA Académie — 16 files (split: 11 to 2026-efa-collab/, 5 to 2026-suez-webuy/)
    # ------------------------------------------------------------------
    # EFA-org context → 2026-efa-collab/ (11 files)
    (
        "EFA/EFA ACCADEMIE Logo png.png",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/brand-assets/efa-academie-logo.source.png",
    ),
    (
        "EFA/EFA ACCADEMIE sur fonds Blancs.png",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/brand-assets/efa-academie-logo-on-white.source.png",
    ),
    (
        "EFA/PRESENTATION CREATION ET JOIE.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/presentation-creation-et-joie.docx",
    ),
    (
        "EFA/PRESENTATION CREATION ET JOIE.docx.pdf",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/presentation-creation-et-joie.pdf",
    ),
    (
        "EFA/08-04-2026 19.02 - EFA project prospection.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-08-efa-project-prospection.mp3",
    ),
    (
        "EFA/08-04-2026 19.02 - EFA project prospection.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-08-efa-project-prospection.mp3.md",
    ),
    (
        "EFA/2026-04-17 19.46 - Holistika Research - Researcher Onboarding.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-17-holistika-research-researcher-onboarding.mp3",
    ),
    (
        "EFA/2026-04-17 19.46 - Holistika Research - Researcher Onboarding.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-04-17-holistika-research-researcher-onboarding.mp3.md",
    ),
    (
        "EFA/2026-12-12 - Holistika Research - Business Developer Onboarding.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-12-12-business-developer-onboarding.m4a.md",
    ),
    (
        "EFA/WhatsApp Audio 2026-05-10 at 18.20.47.opus.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-05-10-whatsapp-audio-18-20-47.opus.mp3.md",
    ),
    (
        "EFA/WhatsApp Audio 2026-05-10 at 18.21.10.opus.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-05-10-whatsapp-audio-18-21-10.opus.mp3.md",
    ),
    # SUEZ-specific (EFA-authored) → 2026-suez-webuy/00-internal/source-materials/efa/ (5 files)
    (
        "EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 1.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-01.m4a.md",
    ),
    (
        "EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 3.m4a.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-03.m4a.md",
    ),
    (
        "EFA/CDC_WeBuy_SUEZ.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/efa/CDC_WeBuy_SUEZ.docx",
    ),
    (
        "EFA/CDC_WeBuy_SUEZ.docx.pdf",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/efa/CDC_WeBuy_SUEZ.pdf",
    ),
    (
        "EFA/Mode opératoire - Process de passage de commande WeBuy.pdf",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/efa/mode-operatoire-passage-commande-webuy.fr.pdf",
    ),
    # ------------------------------------------------------------------
    # 2.4 ShadowGPU — 2 files (Q7 ratify: Clients/, not Marketing/Brand/AV/Advisers/)
    # ------------------------------------------------------------------
    (
        "ShadowGPU/27-02-2026 15.11 shadow gpu x holistika meeting.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-shadowgpu-inbound/00-internal/source-materials/transcripts/2026-02-27-shadowgpu-x-holistika-meeting.mp3",
    ),
    (
        "ShadowGPU/27-02-2026 15.11 shadow gpu x holistika meeting.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-shadowgpu-inbound/00-internal/source-materials/transcripts/2026-02-27-shadowgpu-x-holistika-meeting.mp3.md",
    ),
    # ------------------------------------------------------------------
    # 2.5 Internal Service Mgmt SSOT — 8 files (Q8 ratify: long slug; productization deferred to I73)
    # ------------------------------------------------------------------
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/Finance/Placeholder - Billing Plan and Costs.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/finance/billing-plan-and-costs-placeholder.xlsx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/Marketing/Placeholder - Channels - Buyer persona - Brand Persona.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/marketing/channels-personas-placeholder.docx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/Marketing/Placeholder - Editorial Calendar - Per channel message.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/marketing/editorial-calendar-placeholder.xlsx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/Marketing/Placeholder - Leads and Customers.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/marketing/leads-and-customers-placeholder.xlsx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/People - HR/People - Profiles - Internal and External employee profiles costs and tarifs.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/people-hr/people-profiles-rates.xlsx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/Project - Operations/Placeholder - Process Inventory - Backlog and Project Plan with Gantt.xlsx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/project-operations/process-inventory-and-gantt-placeholder.xlsx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/Business Plan/Tech - Data/Placeholder - Main Standard Operating Process (Manual) for business operator no IT  - Single Source of Truth.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/business-plan/tech-data/main-sop-manual-placeholder.docx",
    ),
    (
        "Think Big - Service Management SSOT/Project Baseline - Go-To-Market/References - Research/Placeholder - GTM PHESTEL Research.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-internal-service-management-ssot/00-internal/source-materials/project-baseline-gtm/references-research/gtm-phestel-research-placeholder.docx",
    ),
    # ------------------------------------------------------------------
    # 2.6 Websitz / Rushly — 27 files (Q9 ratify: collapse UC1+UC2 under one folder)
    # ------------------------------------------------------------------
    # UC1 (shopify) — 4 files
    (
        "Websitz/Use case 1 (shopify)/16-03-2026 21.09 - Holistika x Websitz x EFA.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-1-shopify/transcripts/2026-03-16-holistika-x-websitz-x-efa.mp3",
    ),
    (
        "Websitz/Use case 1 (shopify)/16-03-2026 21.09 - Holistika x Websitz x EFA.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-1-shopify/transcripts/2026-03-16-holistika-x-websitz-x-efa.mp3.md",
    ),
    (
        "Websitz/Use case 1 (shopify)/23-03-2026 20.03 - Holistika x Websitz - Cart Bundle App review.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-1-shopify/transcripts/2026-03-23-cart-bundle-app-review.mp3",
    ),
    (
        "Websitz/Use case 1 (shopify)/23-03-2026 20.03 - Holistika x Websitz - Cart Bundle App review.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-1-shopify/transcripts/2026-03-23-cart-bundle-app-review.mp3.md",
    ),
    # UC2 (Rushly) — 23 files
    (
        "Websitz/Use case 2/2026-04-01 15.33 - presentation projet 2.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-01-presentation-projet-2.mp3",
    ),
    (
        "Websitz/Use case 2/2026-04-01 15.33 - presentation projet 2.mp3.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-01-presentation-projet-2.mp3.md.docx",
    ),
    (
        "Websitz/Use case 2/Rushly_Cahier_des_charges_v2.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/cahier-des-charges/Rushly_CDC_v2.docx",
    ),
    (
        "Websitz/Use case 2/Rushly_Cahier_des_charges_v2.docx.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/cahier-des-charges/Rushly_CDC_v2.md",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.51.40.opus.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-51-40.opus.mp3",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.51.40.opus.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-51-40.opus.mp3.md",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.52.26.opus.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-52-26.opus.mp3",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-02 at 21.52.26.opus.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-02-whatsapp-audio-21-52-26.opus.mp3.md",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.51.29.opus.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-51-29.opus.mp3",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.51.29.opus.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-51-29.opus.mp3.md",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.52.34.opus.mp3",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-52-34.opus.mp3",
    ),
    (
        "Websitz/Use case 2/WhatsApp Audio 2026-04-07 at 15.52.34.opus.mp3.md",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/transcripts/2026-04-07-whatsapp-audio-15-52-34.opus.mp3.md",
    ),
    (
        "Websitz/Use case 2/agentic-artificial-intelligence.pdf",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/references/agentic-artificial-intelligence.pdf",
    ),
    (
        "Websitz/Use case 2/gdrive/Kick-off message.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/kick-off-message.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/rushly_mvp_roadmap_3cd96613.plan.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/rushly_mvp_roadmap_3cd96613.plan.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.fr.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.fr.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-only/rushly_internal_effort_and_revenue_estimate.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/01_Project_Overview.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/01_Project_Overview.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/02_Shared_Decisions_And_Open_Items.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/02_Shared_Decisions_And_Open_Items.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/03_Status_And_Next_Steps.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/03_Status_And_Next_Steps.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/04_Websitz_Inputs_And_Dependencies.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/04_Websitz_Inputs_And_Dependencies.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/Plan de faisabilite et aspects de produit.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/plan-de-faisabilite-et-aspects-de-produit.md.docx",
    ),
    (
        "Websitz/Use case 2/gdrive/websitz-use-case-2-rushly-shared/README.md.docx",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/00-internal/source-materials/use-case-2-rushly/gdrive/websitz-use-case-2-rushly-shared/README.md.docx",
    ),
    # ------------------------------------------------------------------
    # 2.7 Untracked audio sources (10 files; gitignored *.m4a and *.opus)
    #
    # These are paired with already-migrated .md transcripts; co-locate at the
    # same target folder so the audio<->transcript association is preserved
    # locally. They remain gitignored at the new location (extension-globbed
    # by .gitignore L154-155) so they won't leak into the git index.
    # Captured outside the matrix file because they don't appear in
    # ``git ls-files --others`` (gitignored). Migration discovered them at
    # post-execute --dry-run sweep on 2026-05-13 17:55 and extended the
    # manifest in the same atomic commit.
    # ------------------------------------------------------------------
    (
        "Asesoria Hosteleria/2026-08-04 - Kick-Off Asesoría Hostelería.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-08-04-kick-off-asesoria-hosteleria.m4a",
    ),
    (
        "Asesoria Hosteleria/2026-10-05 - Consultoría Hostelería - Admin Course - 4.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-10-05-admin-course-04.m4a",
    ),
    (
        "Asesoria Hosteleria/2026-12-04 - Consultoría Hostelería - Admin Course - 1.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-12-04-admin-course-01.m4a",
    ),
    (
        "Asesoria Hosteleria/2026-12-04 - Consultoría Hostelería - Estudio de Mercado y PESTEL - 2.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-12-04-pestel-research-02.m4a",
    ),
    (
        "Asesoria Hosteleria/2026-30-04 - Consultoría Hostelería - Admin Course - 3.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/00-internal/source-materials/transcripts/2026-04-30-admin-course-03.m4a",
    ),
    (
        "EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 1.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-01.m4a",
    ),
    (
        "EFA/2026-12-12 - Holistika Research - Business Developer - EFA x GDF SUEZ We Buy - Proposal Briefing - 3.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/efa/2026-12-12-efa-suez-webuy-proposal-briefing-03.m4a",
    ),
    (
        "EFA/2026-12-12 - Holistika Research - Business Developer Onboarding.m4a",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-12-12-business-developer-onboarding.m4a",
    ),
    (
        "EFA/WhatsApp Audio 2026-05-10 at 18.20.47.opus",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-05-10-whatsapp-audio-18-20-47.opus",
    ),
    (
        "EFA/WhatsApp Audio 2026-05-10 at 18.21.10.opus",
        "docs/references/hlk/v3.0/Think Big/Clients/2026-efa-collab/00-internal/source-materials/transcripts/2026-05-10-whatsapp-audio-18-21-10.opus",
    ),
]


def _resolve_source(source: Path) -> Path | None:
    """Resolve ``source`` against the filesystem, tolerating NFC vs NFD
    diacritic encodings. Returns the actual filesystem path, or None if neither
    form exists.

    Some temp-folder paths (e.g., "Fayçal", "Asesoría", "Consultoría", "Mode
    opératoire") were captured by Drive sync in NFD (combining-mark) form;
    Python source literals are NFC by default. Both encodings render
    identically; we just need to find which one the filesystem stores.
    """
    if source.exists():
        return source
    parent = source.parent
    if not parent.exists():
        return None
    target_name = source.name
    nfc_name = unicodedata.normalize("NFC", target_name)
    nfd_name = unicodedata.normalize("NFD", target_name)
    for entry in parent.iterdir():
        entry_nfc = unicodedata.normalize("NFC", entry.name)
        if entry_nfc == nfc_name or entry.name == nfd_name or entry.name == target_name:
            return entry
    return None


def _git_mv(source: Path, target: Path, *, dry_run: bool) -> bool:
    """Move ``source`` -> ``target`` via filesystem rename + git add.
    Creates parent dirs. Returns True on success (or no-op skip), False on
    hard error.
    """
    rel_src = source.relative_to(REPO).as_posix()
    rel_dst = target.relative_to(REPO).as_posix()

    resolved_src = _resolve_source(source)
    if resolved_src is None:
        if target.exists():
            print(f"  [skip] already migrated: {rel_dst}")
            return True
        print(f"  [WARN] source missing AND target missing: {rel_src} -> {rel_dst}")
        return False
    source = resolved_src

    if target.exists():
        print(f"  [WARN] target exists, source still present: {rel_src} -> {rel_dst}")
        return False

    target.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        print(f"  [DRY] git mv {rel_src!r} -> {rel_dst!r}")
        return True

    # Use ``git mv`` so the index records a rename (preserves --follow history).
    # Source is currently UNTRACKED (per git_status); ``git mv`` would refuse to
    # move an untracked file, so we use plain Path.rename() + ``git add`` for
    # the target. This still gives clean history because the source was never
    # in the index — there's no rename to preserve, only a fresh add.
    try:
        source.rename(target)
    except OSError as e:
        print(f"  [ERR] rename failed: {rel_src} -> {rel_dst}: {e}", file=sys.stderr)
        return False

    print(f"  [ok] moved {rel_src!r} -> {rel_dst!r}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="I70 P9.7 — temp folder corpus migration executor (per A2)."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", default=True, help="(default) preview without writing")
    group.add_argument("--execute", action="store_true", help="actually move files")
    args = parser.parse_args()

    dry_run = not args.execute

    if not TEMP_ROOT.exists():
        print(f"[abort] temp root not found: {TEMP_ROOT}", file=sys.stderr)
        return 1

    print(f"[migrate-temp-corpus] {len(MIGRATIONS)} planned moves; dry_run={dry_run}")
    print(f"[migrate-temp-corpus] temp root = {TEMP_ROOT.relative_to(REPO).as_posix()}")
    print()

    ok = 0
    skipped = 0
    failed = 0
    for src_rel, tgt_rel in MIGRATIONS:
        source = TEMP_ROOT / src_rel
        target = REPO / tgt_rel
        result = _git_mv(source, target, dry_run=dry_run)
        if result:
            if not source.exists() and target.exists() and not dry_run:
                ok += 1
            elif dry_run:
                ok += 1
            else:
                skipped += 1
        else:
            failed += 1

    print()
    print(f"[migrate-temp-corpus] summary: ok={ok}, skipped={skipped}, failed={failed}, total={len(MIGRATIONS)}")

    if not dry_run and failed == 0:
        # ``git add`` the new locations so they're tracked. The temp folder
        # contents were untracked in the index — the moves create new
        # untracked paths that we now stage.
        print("[migrate-temp-corpus] staging new paths via git add ...")
        # Stage the entire docs/references/hlk/v3.0/ tree to capture all new
        # subfolders + files in one go (idempotent; unchanged paths are no-ops).
        try:
            subprocess.run(
                ["git", "add", "docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/people-files/",
                 "docs/references/hlk/v3.0/Think Big/Clients/"],
                cwd=REPO, check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"[migrate-temp-corpus] git add failed: {e}", file=sys.stderr)
            return 1
        print("[migrate-temp-corpus] staged")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
