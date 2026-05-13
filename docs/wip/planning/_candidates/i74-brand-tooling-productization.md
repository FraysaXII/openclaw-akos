---
candidate_id: I74
title: Brand-tooling productization (TRIGGER-2 OS-library fork preparation)
status: candidate
authored: 2026-05-12
parent_initiative: 70 (closing scaffold)
priority: 4
---

# I74 candidate — Brand-tooling productization

## 1. Scope

Preparation for the **TRIGGER-2 (AKOS-as-library consumed externally)** OS-migration scenario per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §15.2 + `MADEIRA-AKOS/STATUS.md` §3:
- Extract brand-discipline canonicals (BRAND_VOICE_FOUNDATION + BRAND_REGISTER_MATRIX + BRAND_FRENCH_PATTERNS + BRAND_SPANISH_PATTERNS + BRAND_COPYWRITING_DISCIPLINE + BRAND_GANTT_DISCIPLINE + BRAND_MULTILINGUAL_CONTRACT + BRAND_COUNTERPARTY_README_CONTRACT) into a portable library form.
- Extract render pipeline (`scripts/render_*_engagement_pdfs.py` + `akos/hlk_pdf_render.py`) as a reusable Python package (`@holistika/akos-brand` or similar).
- Extract validator rule packs (post-I71 ship) as importable validators.
- License posture (per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`; non-Holistika orgs cannot use Holistika brand marks but can use the discipline as a methodology).
- Extract MADEIRA agent-companion pattern as `@holistika/madeira-agent` (productized form post-AKOS-complete-enough trigger per HLK_ERP_ARCHITECTURE §8).

## 2. Why priority 4 (later)

- TRIGGER-2 drift signal is **2+ external requests for AKOS doctrine without source-fork**. Today: 0 such requests. Trigger is reactive.
- Productization requires post-I70 + post-I71 + post-I72 mature canonical state (validators + engagement template promotion machine + RevOps engagement-rhythm).
- Library packaging is significant engineering effort (semver discipline + dependency management + distribution channel + documentation).

## 3. Spin-out trigger conditions

- TRIGGER-2 fires (2+ external requests for AKOS doctrine consumption).
- I70 + I71 + I72 + I73 closed.
- Founder + Brand Manager approval (license posture + brand boundaries).
- HLK Tech Lab capacity available (per WORKSPACE_BLUEPRINT_HOLISTIKA §16.3 HLK Tech Lab -> productization transition).

## 4. Cross-references

- WORKSPACE_BLUEPRINT_HOLISTIKA §15.2 — TRIGGER-2 (AKOS-as-library consumed externally) + Scenario B (full OS-library fork).
- MADEIRA-AKOS/STATUS.md §3 — TRIGGER-2 details + Scenario B activation.
- HLK_ERP_ARCHITECTURE §8 — AKOS-complete-enough trigger gates MADEIRA productization.
- BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md — license posture for non-Holistika orgs.
- D-IH-70-V (P2.5 sub-decision) — AIC-as-category framing; MADEIRA productization vector.
