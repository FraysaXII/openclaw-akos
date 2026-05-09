---
sop_id: SOP-BRAND_VOICE_DRIFT_TRIAGE_001
title: Brand Voice Drift Triage
version: 1.0
status: active
classification: canonical
access_level: 4
register: internal
language: en
process_id: tbi_mkt_prc_voice_drift_triage_001
role_owner: Brand Manager
role_parent_1: CMO
area: MKT
entity: Holistika
governance:
  - D-IH-66-J (drift gates wired into release-gate)
linked_initiative: I66
created: 2026-05-08
last_review: 2026-05-08
---

# SOP-BRAND_VOICE_DRIFT_TRIAGE_001 — Brand Voice Drift Triage

> Brand-Manager-owned **monthly process** that triages soft-INFO signals from the brand drift gates. Each signal is classified and routed: accept-canon-change, require-source-fix, or defer.

## 1. Purpose

The 4 drift gates (`validate_brand_canon_drift.py`, `validate_brand_jargon.py`, `validate_brand_voice_register.py`, `validate_brand_baseline_reality_drift.py`) produce ongoing soft-INFO signals during the I66 P5+P6 cleanup window. This SOP governs how those signals are triaged so they stay actionable, not noise.

## 2. Cadence

**Monthly** (12 cycles per year). Aligned with the first working day of the calendar month.

Trigger out-of-cycle review when:

- Soft-INFO signal count rises by ≥ 50% month-over-month.
- A drift gate's strict-via-env flag is being considered for permanent activation.
- An operator-led brand intervention happens (logo refresh, sub-mark introduction, public-content publish).

## 3. Inputs

- Latest output of all 4 brand drift gates (run with `--json-log` for parseable output).
- Last month's triage report.
- Currently-open boilerplate / hlk-erp / advops PRs that may resolve some signals.

## 4. Process steps

### Step 1 — Run all 4 gates and collect signals (5 min)

```
py scripts/validate_brand_canon_drift.py --json-log > /tmp/brand-canon.json
py scripts/validate_brand_jargon.py --json-log > /tmp/brand-jargon.json
py scripts/validate_brand_voice_register.py --json-log > /tmp/brand-voice.json
py scripts/validate_brand_baseline_reality_drift.py --json-log > /tmp/brand-baseline.json
```

Aggregate signal count: total hits across all four gates.

### Step 2 — Classify each unique signal (15-30 min)

For each unique forbidden token / pattern hit (de-duplicated by `<gate>:<token>`):

- **Accept-canon-change**: The signal reveals that the canon is wrong — the token actually IS canonical brand language now (e.g., a previously-deprecated term was re-adopted). Action: file a tranche updating the relevant canonical; remove the token from the forbidden list.
- **Require-source-fix**: The signal is correct — the public surface uses forbidden language and should be rewritten. Action: file an issue / PR against the consumer repo (boilerplate / hlk-erp / advops) to fix the surface.
- **Defer**: The signal is correct but the cost of fixing exceeds the benefit right now (e.g., legacy `app/dashboard/` content scheduled for deprecation). Action: document the defer reason + sunset date.

### Step 3 — Route action items (5 min)

- Accept-canon-change → file an OPS_REGISTER row + dispatch to next quarterly canon maintenance cycle.
- Require-source-fix → open an issue in the consumer repo with `area: brand-drift` label + cite this triage report.
- Defer → record in the triage report's "deferred signals" section with date and sunset criteria.

### Step 4 — File monthly triage report (10 min)

Under (TBD location — likely `docs/wip/planning/<brand-ops-initiative>/reports/` once a dedicated brand-ops initiative is chartered):

```
brand-voice-drift-triage-<YYYY-MM>.md
```

Containing:
- Signal counts per gate (this month + delta vs last month).
- Classified signals (accept-canon / require-source-fix / defer).
- Action items dispatched.
- Deferred signals with sunset criteria.

### Step 5 — Strict-mode promotion review (5 min)

Once per quarter, evaluate whether each soft-INFO gate should be promoted to strict-FAIL (via the relevant `AKOS_BRAND_*_STRICT=1` flag in `release-gate.py`). Promote when:
- All "require-source-fix" signals from the gate have been resolved.
- The deferred signals are explicitly accepted as long-term defers.
- The gate has been signal-stable for ≥ 1 quarter.

## 5. Outputs

- Monthly triage report (Step 4 file).
- Routed action items (issues, OPS rows, defer entries).
- Updated soft-INFO → strict-FAIL promotion plan (Step 5).

## 6. Cross-references

- Sister SOPs: [`SOP-BRAND_CANON_MAINTENANCE_001.md`](SOP-BRAND_CANON_MAINTENANCE_001.md) (master quarterly orchestration).
- Drift gates: see SOP-BRAND_CANON_MAINTENANCE §6.
- D-IH-66-J (gate strictness model).
