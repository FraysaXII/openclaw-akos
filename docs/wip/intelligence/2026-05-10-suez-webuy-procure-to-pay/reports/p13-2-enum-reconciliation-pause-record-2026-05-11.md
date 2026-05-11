---
language: en
status: active
phase: P13.2
phase_kind: pause-record
parent_initiative: workspace-blueprint-2026
related_initiative_intelligence: 2026-05-10-suez-webuy-procure-to-pay
authored: 2026-05-11
role_owner: PMO
gate_kind: canonical-CSV-gate
gate_class: definitional (no CSV mutation)
companion_to:
  - ../checkpoints/p13-0-canonical-dig-2026-05-11.md
  - ../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md
---

# P13.2 — GOI/POI class-enum reconciliation pause record

> **PAUSE GATE #1 of two for the P13 workspace-blueprint initiative.** Per [`akos-governance-remediation.mdc`](../../../../../.cursor/rules/akos-governance-remediation.mdc) canonical-CSV gate discipline. This record captures the decision matrix and the operator confirmation. Decision encoded as **D-W13-C** in the closure ledger.

## The question

[`scripts/validate_goipoi_register.py`](../../../../../scripts/validate_goipoi_register.py) lines 34-52 currently accept BOTH `collaborator` (Initiative 21 seed set) AND `partner` (Initiative 22 P4 extension) as `class` enum values. The drift question: are they duplicates, or do they encode a real distinction?

Examination of [`GOI_POI_REGISTER.csv`](../../../../../docs/references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv) (10 data rows as of 2026-05-11):

- Two rows use `partner` (the EFA pair: `GOI-PRT-EFA-2026` + `POI-PRT-EFA-LEAD-2026`).
- Zero rows use `collaborator`.

The SOP [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §4.7 lists both with terse single-line descriptions but does not sharpen the boundary. The result: an operator adding a new informal-collaborator row has no canonical guidance on whether `collaborator` or `partner` is correct; the validator silently accepts either.

## Decision matrix

| Option | Decision | Trade-off |
|:---|:---|:---|
| **A (recommended)** | Keep both; sharpen definitions in the SOP via a "Class enum maturity ramp" section; cross-link the validator inline doc | Preserves historical rows; encodes a real distinction (informal vs strategic); zero CSV mutation; zero validator code change |
| B | Drop `collaborator`; collapse all such rows into `partner` | Simpler enum; loses early-stage signal; would force re-classifying any future informal-collaborator row as `partner` (overstates commitment) |
| C | Drop `partner`; collapse all such rows into `collaborator` | Reverses D-12-7 (which classed EFA as `partner` per the co-branding host/guest posture); breaks the brand-cobranding semantic; would require EFA row mutation |

## Operator decision

**Option A confirmed** (pre-approved in the P13 plan; embedded in this pause record as the canonical decision artifact).

Rationale: there is a real maturity distinction between informal one-project collaboration (no contract, no co-branding, no maintenance commitment) and strategic recurring partnership (contractual, co-branded per [`BRAND_COBRANDING_PATTERN.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md), maintenance-bearing). Collapsing either way loses signal. The fix is doctrinal: sharpen the SOP definitions; no row mutation needed.

## Sharpened definitions (to be encoded in SOP §4.10)

### `collaborator`

A relationship that is **all four of**:

- **Informal** — no written contract, no MoU, no LOI.
- **Single-project** — engagement is one-off; no commitment to repeat.
- **No co-branding** — Holistika does not appear alongside the counterparty's marks in any rendered surface; the counterparty does not appear in `_external_marks/` of any Think Big engagement folder.
- **No maintenance commitment** — neither party is on the hook for ongoing capacity, response SLAs, or product-evolution alignment.

Typical examples: a one-off referral source for a single customer intro; an unpaid advisor who reviews a single document; a community contributor to a single research artifact.

If ANY of the four conditions fails, the row is `partner`, not `collaborator`.

### `partner`

A relationship that is **at least three of**:

- **Strategic** — both parties expect the relationship to repeat across multiple projects.
- **Contractual** — there is a written contract, MoU, LOI, or persistent commercial framework.
- **Co-branding posture** — host/guest brand assets cohabit per [`BRAND_COBRANDING_PATTERN.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_COBRANDING_PATTERN.md); the counterparty's marks may appear in `_external_marks/` of relevant engagement folders.
- **Capacity or maintenance commitment** — at least one party commits to ongoing capacity, response SLAs, or product-evolution alignment.

Canonical example: `GOI-PRT-EFA-2026` (EFA Académie) — strategic since October 2025, contractual via the SUEZ engagement schedule, co-branded host/guest per D-12-7, and the partner lead has committed to assume post-launch operational maintenance of the SUEZ procure-to-pay automation (proposal §3 posture A).

If the row is unsure, default to `collaborator` (lower bar; preserves the option to promote later). The maturity ramp is one-directional: rows promote from `collaborator` → `partner` when conditions strengthen; they do not demote.

## Files mutated as a result of this decision

1. [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) — append §4.10 "Class enum maturity ramp — `collaborator` vs `partner`" with the sharpened definitions above and the one-directional ramp rule.
2. [`scripts/validate_goipoi_register.py`](../../../../../scripts/validate_goipoi_register.py) — extend the inline doc on the `CLASSES` set (around line 31) to cross-link the new SOP §4.10. No code change.

## Files NOT mutated

- [`docs/references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv`](../../../../references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv) — zero row mutation. EFA pair stays `partner`. No row currently uses `collaborator`; no row will be promoted/demoted by this gate.
- [`akos/hlk_goipoi_csv.py`](../../../../../akos/hlk_goipoi_csv.py) — field contract unchanged.
- [`supabase/migrations/`](../../../../../supabase/migrations/) — mirror DDL unchanged.

## Verification

- `py scripts/validate_hlk_vault_links.py` — PASS expected (only SOP cross-link added).
- `py scripts/validate_hlk.py` — PASS expected (definitions-only; no enum change; pre-existing I68 `D-IH-66-AC` row failure is independent — documented in P13.0 §7).

## Closure ledger

- **Decision ID:** D-W13-C
- **Decision:** Keep both `collaborator` + `partner`; sharpen via SOP §4.10 maturity ramp; cross-link from validator inline doc
- **Status:** Confirmed
- **Date:** 2026-05-11
- **Encoded in:** [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §4.10 (this commit)

End of P13.2 pause record.
