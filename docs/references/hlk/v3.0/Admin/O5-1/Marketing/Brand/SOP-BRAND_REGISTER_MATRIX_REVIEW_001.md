---
sop_id: SOP-BRAND_REGISTER_MATRIX_REVIEW_001
title: Register Matrix Per-Audience Review
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: tbi_mkt_prc_register_matrix_review_001
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
  - SOP-BRAND_CANON_MAINTENANCE_001
  - SOP-BRAND_VOICE_DRIFT_TRIAGE_001
  - SOP-BRAND_JARGON_AUDIT_REVIEW_001
---

# SOP-BRAND_REGISTER_MATRIX_REVIEW_001 — Register Matrix Per-Audience Review

> Brand-Manager-owned **bi-annual process** that re-aligns the per-audience register entries in [`BRAND_REGISTER_MATRIX.md`](BRAND_REGISTER_MATRIX.md) and [`BRAND_BASELINE_REALITY_MATRIX.md`](BRAND_BASELINE_REALITY_MATRIX.md) against observed engagement reality.

## 1. Purpose

The 7 audience rows (investor, customer-SME, advisor, ENISA, partner, recruiter, LATAM-customer) drift over time as the audience pool shifts (new investor preferences, new customer-SME segments, new partner tiers, new ENISA review patterns). This SOP catches that drift before it becomes engagement-quality drift.

## 2. Cadence

**Bi-annual** (2 cycles per year, aligned with Q1 and Q3 quarter-ends).

Trigger out-of-cycle on:

- New audience class introduced (e.g., a regulatory body other than ENISA enters the active surface).
- Material shift in an audience's signature pattern observed across ≥ 3 engagement intelligence reports in the same quarter.
- New language locale introduced (FR-CA, ES-MX, PT-BR, etc.).

## 3. Inputs

- `BRAND_REGISTER_MATRIX.md` and `BRAND_BASELINE_REALITY_MATRIX.md` current state.
- Last 6 months of engagement intelligence reports (per `SOP-IO_INTELLIGENCE_REPORT_001`) — sample of 5-10 across audiences.
- Last 6 months of customer / advisor / investor / partner CRM signal aggregations.
- `validate_brand_voice_register.py` and `validate_brand_baseline_reality_drift.py` last-cycle outputs.

## 4. Process steps

### Step 1 — Audience-pattern delta extraction (30 min)

For each of the 7 audience rows, sample 1-2 recent intelligence reports and extract: (a) signature opening phrases the counterparty uses; (b) signature closing rituals; (c) preferred-form-of-address (Sr./Sra./vous/usted/tu/etc.); (d) topic-vocabulary shifts vs the matrix entry.

### Step 2 — Diff against current matrix entries (15 min)

For each audience, compare extracted patterns against the matrix entry. Flag rows where ≥ 2 signature patterns have shifted.

### Step 3 — Apply updates (30-60 min)

Where row drift is confirmed, edit the matrix entry. Material edits go through the canonical-update tranche pattern (operator review + drift gate verification).

### Step 4 — File bi-annual review report (15 min)

Under `docs/wip/planning/<active-brand-ops-initiative>/reports/`:

```
brand-register-matrix-review-<YYYY-H[1-2]>.md
```

Containing: per-audience delta summary, applied edits, deferred edits with rationale.

## 5. Outputs

- Bi-annual review report (Step 4 file).
- Updated `BRAND_REGISTER_MATRIX.md` and `BRAND_BASELINE_REALITY_MATRIX.md` rows where drift confirmed.
- Updated `last_review:` frontmatter dates.

## 6. Anti-patterns

- **Sample-of-1 over-fit.** A single counterparty's quirk does not warrant a matrix update; ≥ 3 independent samples needed.
- **Pre-emptive translation.** Edits to BRAND_BASELINE_REALITY_MATRIX.md must preserve the dual-register structure (internal column intact) — never collapse to single column.

## 7. Cross-references

- Sister SOPs: [`SOP-BRAND_CANON_MAINTENANCE_001.md`](SOP-BRAND_CANON_MAINTENANCE_001.md) (master quarterly orchestrator), [`SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md`](SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md) (monthly soft-INFO triage).
- Drift gates: [`scripts/validate_brand_voice_register.py`](../../../../../../scripts/validate_brand_voice_register.py), [`scripts/validate_brand_baseline_reality_drift.py`](../../../../../../scripts/validate_brand_baseline_reality_drift.py).
- D-IH-66-D (FR + ES voice canonicals deepened).
