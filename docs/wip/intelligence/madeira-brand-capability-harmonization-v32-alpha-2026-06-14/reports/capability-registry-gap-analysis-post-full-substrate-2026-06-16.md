---
intellectual_kind: gap_analysis
phase: post_full_substrate
authored: 2026-06-16
baseline: capability-registry-gap-analysis-post-sweep-2026-06-15.md
operator_gate: inline-ratify D-IH-76-R
---

# Capability registry — post full substrate backfill (103/103)

> **Functional name:** proof that every row in the “what Holistika can do” map now names **which runtime realizes it** — required for your alpha-0 sign-off ratify.

## Metric delta

| Metric | Post-GCI (2026-06-15) | Post full sweep (2026-06-16) | Δ |
|:---|:---:|:---:|:---:|
| Registry rows | 103 | 103 | — |
| Empty `substrate_id` | 83 | **0** | −83 |
| Validator FAIL on empty FK | Active MADEIRA only | **All rows** | D-IH-76-R ramp |

## Backfill method

| Layer | Rule |
|:---|:---|
| L1 domain default | Nine `l1_domain` → primary substrate (Cursor SDK, OpenClaw, KiRBe, Vercel SDK, etc.) |
| Semantic overrides | 21 capability IDs with finer mapping (e.g. graph/KiRBe → `SUBS-HOLISTIKA-KIRBE`, lab → direct-runtime pattern) |
| Audit | Touched rows → `last_review_decision_id=D-IH-76-R`, `methodology_version_at_review=v3.2` |

## Verification

```powershell
py scripts/validate_capability_registry.py
py scripts/validate_hlk.py
```

## Residual (scheduled, not dropped)

| Gap | Posture |
|:---|:---|
| ACIM 31/103 proof rows | Phase-2 ACIM expansion for non-alpha capabilities |
| Supabase capability mirror DML | Holistika ops lattice |
| Semantic override disputes | Operator may amend individual FK via inline-ratify |
