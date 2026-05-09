---
sop_id: SOP-PEOPLE_FOUNDER_BIO_001
title: Founder Bio Canonical Maintenance
version: 1.0
status: active
classification: canonical
access_level: 4
register: external (with internal-register annotations)
language: en
process_id: tbi_ppl_prc_founder_bio_mtnce_001
role_owner: Talent
role_parent_1: CPO
area: People
entity: Think Big
governance:
  - D-IH-66-S (founder bio canonical with track-record + per-audience FAQ)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
content_canonical: docs/references/hlk/v3.0/Admin/O5-1/People/FOUNDER_BIO.md (P6 deliverable)
---

# SOP-PEOPLE_FOUNDER_BIO_001 — Founder Bio Canonical Maintenance

> Talent-owned **quarterly process** that maintains the canonical founder bio: bio prose + per-audience FAQ + anonymised track-record. Drift-gate-checked against the external-register canon.

## 1. Purpose

The founder bio is the most-frequently-rendered piece of Holistika content (every deck, every pitch, every recruiter interaction, every advisor onboarding, every press contact uses some variant of it). This SOP keeps the canonical bio + its audience-specific renderings coherent across:

- The investor pitch (12-slide deck).
- The advisor onboarding deck (4-slide).
- The recruiter / hiring deck (P6 deliverable).
- The press kit (P6 deliverable).
- The boilerplate `/manifiesto/holistika` page (P5 deliverable).
- Recurring email signatures (P6 deliverable).
- Any LinkedIn / public-profile renderings.

## 2. Cadence

**Quarterly** (4 cycles per year). Out-of-cycle on:

- Material change in founder's external-facing track record (new role, new public engagement, new advisor position, new public publication).
- Significant change in Holistika's operational reality (new sub-mark introduced, new product launched, major engagement closed publicly).
- An external interaction reveals the bio is outdated or mis-positioned for a specific audience.

## 3. Inputs

- The canonical `FOUNDER_BIO.md` (P6 deliverable; canonical lives at `docs/references/hlk/v3.0/Admin/O5-1/People/FOUNDER_BIO.md`).
- Per-audience FAQ entries (P6 deliverable; co-located with FOUNDER_BIO.md).
- Anonymised track-record canonical (P6 deliverable; the founder's pre-Holistika engagements rendered in external register, free of confidential client / employer names).
- Recent founder-touched engagement intelligence reports (per SOP-IO_INTELLIGENCE_REPORT_001 — input for "what audiences are reacting to in the bio").
- All current external surfaces that quote or link to the bio.

## 4. Process steps

### Step 1 — Sync check across surfaces (15 min)

Confirm every external surface (deck, page, email signature, LinkedIn, etc.) is rendering the **current** bio version. Flag any surface that has drifted (older bio version live in production).

### Step 2 — Audience-FAQ relevance review (15 min)

For each of the 7 audience FAQs (investor, customer-SME, advisor, ENISA, partner, recruiter, LATAM-customer):

- Are the questions still the most-asked questions for this audience?
- Are the answers still accurate?
- Has any new question pattern emerged (per recent engagement intelligence reports) that warrants adding?

### Step 3 — Track-record currency review (10 min)

Confirm anonymised track-record entries are:

- **Current** (engagements within the relevant horizon — typically 3-5 years for early-career; 7-10 for mid-career).
- **Properly anonymised** (no client names, no employer names beyond what's already public, no specific dollar figures).
- **Reliable** (the engagement actually went the way the entry describes — counter-narrative entries are more credible than uniformly-positive ones).

### Step 4 — Drift-gate verification (5 min)

Run `validate_brand_jargon.py` and `validate_brand_baseline_reality_drift.py` against the bio + FAQ + track-record canonicals (these files are external-register and must pass strictly). The bio's own content should never include internal-register tokens.

### Step 5 — File quarterly review report (10 min)

Under `docs/references/hlk/v3.0/Admin/O5-1/People/reports/` (create if not existing):

```
founder-bio-quarterly-review-<YYYY-Q[1-4]>.md
```

Containing: surface-sync status, audience-FAQ updates, track-record updates, drift-gate verdict.

### Step 6 — Apply updates (variable)

Edit the canonical files; cascade through external surfaces (or file PRs against consumer repos to re-sync).

## 5. Outputs

- Quarterly review report (Step 5 file).
- Updated canonical FOUNDER_BIO.md, audience-FAQ, anonymised track-record (when changes are needed).
- Updated `last_review:` frontmatter on canonical files.
- Cascaded updates to external surfaces (boilerplate page, decks, email signatures, etc.).

## 6. Anti-patterns

- **Stale-track-record discipline-collapse** — leaving 5+-year-old engagements as the headline track-record entries when more-recent work exists. Track-record is freshest-first.
- **Audience-FAQ generic-collapse** — collapsing all 7 audience FAQs into one "Frequently Asked Questions" doc. The audience-specificity is the value; the FAQ is per-audience or it's nothing.
- **Anonymisation lapse** — accidentally re-introducing client names from internal-register notes into external-register track-record entries. The track-record IS external-register; verify per `validate_brand_baseline_reality_drift.py`.

## 7. Cross-references

- Canonical: `FOUNDER_BIO.md` (P6 deliverable; in-progress).
- [`BRAND_BASELINE_REALITY_MATRIX.md`](../../Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) — per-audience external register.
- [`scripts/validate_brand_jargon.py`](../../../../../../scripts/validate_brand_jargon.py), [`scripts/validate_brand_baseline_reality_drift.py`](../../../../../../scripts/validate_brand_baseline_reality_drift.py) — drift gates.
- D-IH-66-S in `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md`.
- I66 P6 (deck templates + email signatures + founder bio canonical).
