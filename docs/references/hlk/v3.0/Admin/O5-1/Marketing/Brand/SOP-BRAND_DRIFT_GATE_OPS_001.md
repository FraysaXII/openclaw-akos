---
sop_id: SOP-BRAND_DRIFT_GATE_OPS_001
title: Brand Drift Gate Operations
version: 1.0
status: active
classification: canonical
access_level: 4
language: en
register: internal
process_id: tbi_mkt_prc_drift_gate_ops_001
role_owner: Brand Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-66-J (drift gates wired into release-gate as INFO until source-fixes land)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
sister_sops:
  - SOP-BRAND_CANON_MAINTENANCE_001
  - SOP-BRAND_VOICE_DRIFT_TRIAGE_001
  - SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001
---

# SOP-BRAND_DRIFT_GATE_OPS_001 — Brand Drift Gate Operations

> Brand-Manager-owned **quarterly process** that operates the 4 brand drift gates: tracks signal trajectory, promotes soft-INFO gates to hard-FAIL when source-fixes land, deprecates findings when underlying canon changes.

## 1. Purpose

The 4 brand drift gates (`validate_brand_canon_drift.py`, `validate_brand_jargon.py`, `validate_brand_voice_register.py`, `validate_brand_baseline_reality_drift.py`) are not "set and forget" — they are operational instruments that need ongoing tuning:

- Soft-INFO gates need to be **promoted** to hard-FAIL once their source-fixes land (P5 / P6 deliverables).
- New canon additions (sub-marks, products, abbreviations) need to flow into the gates' parsers.
- Spurious-signal patterns need to be triaged and either resolved (canon update) or suppressed (allowlist update).

This SOP governs the operational discipline for the gates themselves.

## 2. Cadence

**Quarterly** (4 cycles per year). Synchronised with `SOP-BRAND_CANON_MAINTENANCE_001` quarterly cycle (this SOP runs after canon maintenance because canon changes drive gate behaviour).

Out-of-cycle on:

- I66 P5 closure (canonical "promote brand_jargon to strict").
- I66 P6 closure (canonical "promote brand_baseline_reality to strict").
- I66 P7 closure (canonical "promote brand_vision_drift to strict" + new gates).
- New drift gate added by a future I-NN.

## 3. Inputs

- Current `release-gate.py` strict-mode environment-flag posture (`AKOS_BRAND_*_STRICT` flags).
- Last-quarter signal counts per gate (per `SOP-BRAND_VOICE_DRIFT_TRIAGE_001` monthly reports + canon maintenance quarterly reports).
- I66 phase closure status.
- New canon additions since last cycle.

## 4. Process steps

### Step 1 — Strict-mode promotion review (15 min)

For each soft-INFO drift gate:

- **`validate_brand_jargon.py`** — eligible for strict-mode promotion when: (a) I66 P5 has closed; (b) every "require-source-fix" hit has been resolved; (c) deferred hits are explicitly accepted as long-term defers (e.g., `app/dashboard/` legacy is permanently exempt). Flip via `AKOS_BRAND_JARGON_STRICT=1` in CI environment.
- **`validate_brand_voice_register.py`** — eligible when: (a) I66 P5 has closed; (b) `boilerplate/messages/{en,es,fr}.json` are clean. Flip via `AKOS_BRAND_VOICE_REGISTER_STRICT=1`.
- **`validate_brand_baseline_reality_drift.py`** — eligible when: (a) I66 P6 has closed (decks land with proper companion structure); (b) all advops decks have valid `.objections.md` + `.counterparty-brief.md` companions where required. Flip via `AKOS_BRAND_BASELINE_REALITY_STRICT=1`.

Document the promotion decision (and rationale for non-promotion) in the quarterly report.

### Step 2 — Canonical allowlist sync (15 min)

`scripts/validate_brand_jargon.py` carries a `CANONICAL_ALLOWLIST` set (e.g., "Holistika", "HLK Tech Lab", "MADEIRA", "KiRBe"). When new sub-marks or products are introduced (via canonical canon update), this allowlist must be expanded. Step 2 confirms the allowlist matches the current sub-mark + product brand inventory per `BRAND_ARCHITECTURE.md`.

### Step 3 — Spurious-signal triage (30 min)

For signal patterns that have repeatedly classified as "defer" across ≥ 2 quarters: either accept as permanent (codify in the validator's exclusion patterns) or escalate to canon update. Recurring "defer" without resolution is a sign the validator is over-strict.

### Step 4 — Per-gate test coverage check (15 min)

Confirm `tests/test_validate_brand_drift_gates.py` still passes (27 tests). New canon additions sometimes break test fixtures (e.g., a new BRAND canonical added to `REQUIRED_CANONICALS` list breaks the test that asserts the count). Update tests where needed.

### Step 5 — File quarterly review report (10 min)

Under `docs/wip/planning/<active-brand-ops-initiative>/reports/`:

```
brand-drift-gate-ops-<YYYY-Q[1-4]>.md
```

Containing: per-gate signal counts + delta, strict-mode promotion decisions, allowlist updates, spurious-signal triage outcomes.

## 5. Outputs

- Quarterly review report (Step 5 file).
- Updated `CANONICAL_ALLOWLIST` in `validate_brand_jargon.py` (when new sub-marks / products land).
- Updated `release-gate.py` strict-mode environment-flag defaults (when promotions land).
- Updated test fixtures where canon additions warrant.

## 6. Anti-patterns

- **Premature strict-promotion.** Flipping a gate to strict-FAIL before all source-fixes land = blocked CI, frustrated developers, and likely a quick reverter back to soft-INFO. Promote only when promotion criteria are met.
- **Allowlist over-eagerness.** Adding tokens to the allowlist as a shortcut to silence signals (rather than fixing the actual surface). The allowlist exists for **canonical brand entities only**, not for "we don't want to fix this".
- **Test rot.** Letting test fixtures drift from canon. The tests are part of the validator's contract; rot in tests means rot in the validator.

## 7. Cross-references

- Sister SOPs: [`SOP-BRAND_CANON_MAINTENANCE_001.md`](SOP-BRAND_CANON_MAINTENANCE_001.md), [`SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md`](SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md), [`SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md`](SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md).
- Drift gates: [`scripts/validate_brand_canon_drift.py`](../../../../../../scripts/validate_brand_canon_drift.py), [`validate_brand_jargon.py`](../../../../../../scripts/validate_brand_jargon.py), [`validate_brand_voice_register.py`](../../../../../../scripts/validate_brand_voice_register.py), [`validate_brand_baseline_reality_drift.py`](../../../../../../scripts/validate_brand_baseline_reality_drift.py).
- Test suite: [`tests/test_validate_brand_drift_gates.py`](../../../../../../tests/test_validate_brand_drift_gates.py).
- D-IH-66-J (gate strictness model).
