---
sop_id: SOP-BRAND_CANON_MAINTENANCE_001
title: Brand Canon Maintenance
version: 1
status: active
classification: canonical
access_level: 4
register: internal
language: en
process_id: tbi_mkt_prc_brand_canon_mtnce_001
role_owner: Brand Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-66-J (drift gates wired into release-gate)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-BRAND_VOICE_DRIFT_TRIAGE_001
  - SOP-BRAND_REGISTER_MATRIX_REVIEW_001
  - SOP-BRAND_JARGON_AUDIT_REVIEW_001
---

# SOP-BRAND_CANON_MAINTENANCE_001 — Brand Canon Maintenance

> Brand-Manager-owned **quarterly process** that keeps the 13 BRAND_*.md canonicals coherent. Sister SOPs handle specific dimensions (voice drift, register matrix, jargon audit); this SOP is the **master quarterly review** that orchestrates them.

## 1. Purpose

Ensure the 13 P0+P1 BRAND canonicals continue to:

- Cross-reference each other accurately (no broken internal links).
- Reflect current brand reality (no orphaned references to deprecated structures).
- Pass `validate_brand_canon_drift.py` strict-FAIL verdict.
- Drive the 4 drift gates (`validate_brand_*`) toward continually-tightening signal.

## 2. Cadence

**Quarterly** (4 cycles per year). Aligned with the calendar quarter-end.

Trigger out-of-cycle review when:

- A canonical is materially edited (≥ 25% line-count change).
- A new sub-mark or product mark is introduced.
- A drift-gate signal flips from soft-INFO to hard-FAIL.
- An operator-flagged customer/investor/advisor interaction reveals a brand-message gap.

## 3. Inputs

- The 13 BRAND_*.md canonicals under `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/` and the trademark-scope canonical under `.../People/Legal/`.
- `validate_brand_canon_drift.py` latest output.
- `validate_brand_jargon.py`, `validate_brand_voice_register.py`, `validate_brand_baseline_reality_drift.py` last-quarter signals.
- Recent customer / investor / advisor / partner / recruiter engagement intelligence reports (per SOP-IO_INTELLIGENCE_REPORT_001).
- Recent press / public-content drift observations.

## 4. Process steps

### Step 1 — Validator review (15 min)

Run all 4 brand drift gates; record current signal counts. Identify which signals are:
- New (since last quarter).
- Unchanged (still present, indicating a P5 / P6 cleanup item still pending).
- Resolved (no longer firing).

### Step 2 — Cross-reference integrity (15 min)

Spot-check that the 13 canonicals' "Cross-references" sections still resolve and remain bidirectional (every cross-ref has a matching back-ref).

### Step 3 — Sub-mark / product reality check (10 min)

Confirm `BRAND_ARCHITECTURE.md` Branded House diagram still matches reality (sub-marks introduced, deprecated, renamed). If mismatch, this SOP triggers a tranche update; SOP does not auto-edit canon.

### Step 4 — Engagement-derived drift detection (20 min)

Read the last quarter's intelligence reports (sample of 3-5). For each:
- Did the engagement reveal a brand-message that was unclear or mis-translated?
- Did the counterparty react to a specific brand element (logo, slogan, sub-mark name) in a way that flags drift?
- Are there patterns across multiple engagements?

### Step 5 — File quarterly review report (10 min)

Under `docs/wip/planning/<active-initiative-slug>/reports/` (or a dedicated brand-ops directory if one is established post-I66):

```
brand-canon-quarterly-review-<YYYY-Q[1-4]>.md
```

Containing: signal counts, cross-ref integrity status, sub-mark-reality status, engagement-drift findings, recommended canonical updates (if any).

### Step 6 — Operator review and tranche dispatch (variable)

Review the quarterly report with operator. If recommended canonical updates exist, package as a tranche per the canonical-CSV gate pattern (or for non-CSV canonicals, a regular reviewable PR).

## 5. Outputs

- Quarterly review report (Step 5 file).
- Possibly a recommended-canonical-edits tranche.
- Updated `last_review:` frontmatter date on any canonical that was reviewed without changes.

## 6. Cross-references

- Sister SOPs: [`SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md`](SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md), `SOP-BRAND_REGISTER_MATRIX_REVIEW_001.md` (P3-followup), `SOP-BRAND_JARGON_AUDIT_REVIEW_001.md` (P3-followup).
- Drift gates: [`scripts/validate_brand_canon_drift.py`](../../../../../../scripts/validate_brand_canon_drift.py), `validate_brand_jargon.py`, `validate_brand_voice_register.py`, `validate_brand_baseline_reality_drift.py`.
- D-IH-66-J in `docs/wip/planning/66-brand-vision-ops-sweep/decision-log.md`.
