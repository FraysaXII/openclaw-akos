---
sop_id: SOP-BRAND_JARGON_AUDIT_REVIEW_001
title: Jargon Audit Registry Update
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: tbi_mkt_prc_jargon_audit_review_001
role_owner: Brand & Narrative Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-66-J (drift gates wired into release-gate)
  - D-IH-66-N (abbreviation governance)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-BRAND_CANON_MAINTENANCE_001
  - SOP-BRAND_VOICE_DRIFT_TRIAGE_001
---

# SOP-BRAND_JARGON_AUDIT_REVIEW_001 — Jargon Audit Registry Update

> Brand-Manager-owned **quarterly process** that maintains [`BRAND_JARGON_AUDIT.md`](BRAND_JARGON_AUDIT.md) §4 (forbidden tokens) + [`BRAND_ABBREVIATIONS.md`](BRAND_ABBREVIATIONS.md) (short-form registry) against newly observed external-prose drift.

## 1. Purpose

The forbidden-token + abbreviation registries drive the `validate_brand_jargon.py` drift gate. As new internal codenames emerge (new initiative IDs, new internal sub-mark short-forms, new stack-jargon dependencies introduced), these registries need to absorb them. As external-prose patterns evolve, deprecated tokens may need to be retired.

## 2. Cadence

**Quarterly** (4 cycles per year). Out-of-cycle on:

- New internal codename or sub-mark introduced (immediate add to forbidden list).
- New stack dependency introduced in `boilerplate/` or `hlk-erp/` that warrants abbreviation governance.
- A drift-gate signal cluster reveals a missing forbidden token.

## 3. Inputs

- `BRAND_JARGON_AUDIT.md` §4.1 + §4.2 current state.
- `BRAND_ABBREVIATIONS.md` §2 current state.
- `validate_brand_jargon.py` last-quarter signal report (per `SOP-BRAND_VOICE_DRIFT_TRIAGE_001`).
- Last quarter's pull-request titles + commit messages (where new codenames or stack dependencies often first appear).
- Last 3 months of public-channel posts (LinkedIn, blog, deck content) for newly-introduced phrases.

## 4. Process steps

### Step 1 — New-codename surveillance (15 min)

Scan recent commits + PRs + initiative folders for new abbreviations or codenames. Common patterns: `*_OPS`, `*_REGISTRY`, `*_MIRROR`, internal CSV slugs, new sub-mark working titles. Record candidates.

### Step 2 — Stack-dependency surveillance (15 min)

Scan recent `boilerplate/` and `hlk-erp/` `package.json` / `requirements.txt` deltas for newly-introduced dependencies. New library names appearing in source as imports rarely reach external prose, but their associated marketing terms (e.g., a vendor's product name) sometimes do — these warrant §4.2 entries.

### Step 3 — Validate proposed additions against existing patterns (15 min)

For each candidate token: confirm it doesn't conflict with the canonical-allowlist in [`scripts/validate_brand_jargon.py`](../../../../../../scripts/validate_brand_jargon.py) (e.g., a new sub-mark name should be added to the allowlist, not the forbidden list).

### Step 4 — Apply tranche to canonicals (15 min)

Edit `BRAND_JARGON_AUDIT.md` §4.1 / §4.2 + `BRAND_ABBREVIATIONS.md` §2 with the new entries. Each new entry follows the canonical bullet format (`- \`<token>\` — <human description>`) so the parser picks it up automatically.

### Step 5 — Deprecation review (10 min)

Identify forbidden tokens that have not produced any drift-gate signal in ≥ 4 quarters and are not actively cited internally. Candidates for retirement (move to a "historical" subsection, do not silently delete — preserves the institutional memory of "we used to call this X").

### Step 6 — File quarterly review report (10 min)

Under `docs/wip/planning/<active-brand-ops-initiative>/reports/`:

```
brand-jargon-audit-review-<YYYY-Q[1-4]>.md
```

Containing: new tokens added, deprecation candidates, drift-gate signal delta vs last quarter.

## 5. Outputs

- Quarterly review report (Step 6 file).
- Updated `BRAND_JARGON_AUDIT.md` §4.1 / §4.2 + `BRAND_ABBREVIATIONS.md` §2.
- Updated `last_review:` frontmatter dates.
- Re-run of `validate_brand_jargon.py` to confirm new tokens parse correctly.

## 6. Anti-patterns

- **Eager-add.** Adding a token to the forbidden list because it appeared once. The threshold is: appears in ≥ 2 different internal contexts AND has a plausible external-prose leakage path.
- **Silent retirement.** Deleting a deprecated token row without leaving an institutional-memory record. Move to historical subsection instead.
- **Allowlist drift.** Not updating `CANONICAL_ALLOWLIST` in `validate_brand_jargon.py` when a new brand sub-mark or product is introduced — the validator will then false-positive on that token.

## 7. Cross-references

- Sister SOPs: [`SOP-BRAND_CANON_MAINTENANCE_001.md`](SOP-BRAND_CANON_MAINTENANCE_001.md), [`SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md`](SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md).
- Drift gate: [`scripts/validate_brand_jargon.py`](../../../../../../scripts/validate_brand_jargon.py).
- D-IH-66-J (drift gate strictness model), D-IH-66-N (abbreviation governance).
