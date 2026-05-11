---
language: en
status: active
phase: P13.4
phase_kind: pause-record
parent_initiative: workspace-blueprint-2026
related_initiative_intelligence: 2026-05-10-suez-webuy-procure-to-pay
authored: 2026-05-11
role_owner: PMO
gate_kind: canonical-CSV-gate
gate_class: structural (CSV mutation + mirror DDL)
companion_to:
  - ../checkpoints/p13-0-canonical-dig-2026-05-11.md
  - p13-2-enum-reconciliation-pause-record-2026-05-11.md
---

# P13.4 — Canonical-CSV tranche pause record

> **PAUSE GATE #2 of two for the P13 workspace-blueprint initiative.** Per [`akos-governance-remediation.mdc`](../../../../../.cursor/rules/akos-governance-remediation.mdc) canonical-CSV gate discipline. This record captures TWO decisions confirmed in a single combined tranche: (a) related-party Asesoría placement; (b) trainee role placement. Decisions encoded as **D-W13-D** and **D-W13-E** in the closure ledger.

## Sub-decision (a) — Asesoría Hostelería (sister's family SME) placement

### The question

The operator's sister runs a family hospitality-advisory SME. The relationship is an outbound customer engagement (Holistika provides methodology) AND a related-party relationship (operator's family). Where does this row land, and how is "related-party" expressed schema-wise?

### Decision matrix

| Option | Decision | Trade-off |
|:---|:---|:---|
| **A (recommended)** | Add row as `class=client_org` under `Think Big/Clients/`; introduce optional `related_party` boolean column on `GOI_POI_REGISTER.csv`; lay folder skeleton from outbound template | Transparent; precedent for future related-party rows (board members, family partners, advisor friendships); methodology validation surface preserved |
| B | Treat as sub-entity under Holistika Research SL | Legal entanglement; ENISA-track risk (the parent legal entity should not absorb related-party operations); also wrong shape — sister's SME is independent, not a Holistika department |
| C | Outside HLK entirely (personal arrangement) | Loses methodology validation surface; the engagement is real work and should be tracked; SOC norms require disclosure where ownership ties exist |

### Operator decision

**Option A confirmed.**

Rationale: a `related_party` boolean column expresses the disclosure cleanly without forcing a special class. The `class=client_org` correctly captures the engagement shape; `related_party=true` triggers the SOC posture (disclosure in `00-internal/related-party-disclosure.md`); the folder template gives the engagement a normal `Think Big/Clients/` home. Default-empty backwards-compatible column means no existing row needs mutation.

## Sub-decision (b) — Holistik Researcher trainee placement

### The question

Trainees are real positions in the Holistika apprentice ramp; they execute under `Holistik Researcher` supervision and rotate. Where do they belong in `baseline_organisation.csv`?

### Decision matrix

| Option | Decision | Trade-off |
|:---|:---|:---|
| **A (recommended)** | Add `Holistik Researcher Trainee` row (`reports_to=Holistik Researcher`, `access_level=2`, rates 25/35/50, `area=Research`, `entity=Holistika`); no `responsible_processes` (trainees execute under supervisor's process_id) | Inherits SOP supervision contract; clean ramp to Holistik Researcher; doesn't churn baseline when trainees rotate (one row, not per-person) |
| B | Treat as external collaborators (not in baseline) | Bypasses access controls; orphan SOP path; misrepresents the apprentice model |
| C | Hire directly as `Lead Researcher` candidate (skip trainee tier) | Loses the apprentice model; not realistic for current cadence |

### Operator decision

**Option A confirmed.**

Rationale: a single canonical row for the position (not per-person) gives access control + SOP supervision contract + rate transparency without baseline churn when trainees rotate. Rates 25/35/50 sit below the supervising `Holistik Researcher` (60/80/100), capturing the apprentice tier. `access_level=2` (Public + General) constrains access; supervisor process attribution is implicit via `reports_to=Holistik Researcher`.

## Files mutated as a result of this combined tranche

### Canonical CSVs

1. [`docs/references/hlk/compliance/baseline_organisation.csv`](../../../../references/hlk/compliance/baseline_organisation.csv) — append `Holistik Researcher Trainee` row.
2. [`docs/references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv`](../../../../references/hlk/compliance/dimensions/GOI_POI_REGISTER.csv) — add `related_party` column (default empty for all existing 10 rows); append `GOI-CUS-ASES-2026` row with `related_party=true`.

### Field contracts and validators

3. [`akos/hlk_goipoi_csv.py`](../../../../../akos/hlk_goipoi_csv.py) — append `"related_party"` to `GOIPOI_REGISTER_FIELDNAMES` tuple.
4. [`scripts/validate_goipoi_register.py`](../../../../../scripts/validate_goipoi_register.py) — add `RELATED_PARTY = {"", "true", "false"}` enum + per-row validation.

### Tests

5. [`tests/test_validate_goipoi_register.py`](../../../../../tests/test_validate_goipoi_register.py) — new test file covering: column present; default empty backwards-compatible; enum validation; GOI-CUS-ASES-2026 row carries `related_party=true`; validator script exits 0.

### Mirror DDL

6. New migration: [`supabase/migrations/<timestamp>_p13_4_goipoi_related_party.sql`](../../../../../supabase/migrations/) — `ALTER TABLE compliance.goipoi_register_mirror ADD COLUMN IF NOT EXISTS related_party TEXT;` (default NULL; backwards-compatible). Pattern mirrors I24 P2 and I31 P2.2 alter migrations.

### Precedence and folder skeleton

7. [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../../references/hlk/compliance/PRECEDENCE.md) — annotate the GOI/POI register canonical row with the `related_party` column addition.
8. New folder skeleton: `docs/references/hlk/v3.0/Think Big/Clients/2026-asesoria-hosteleria/` populated from the P13.3 outbound template. P13.4 lays the GOI/POI row + the folder shell only; substantive content lands when engagement starts.

## Verification

- `py scripts/validate_goipoi_register.py` — PASS (extended enum; backwards-compatible defaults).
- `py scripts/validate_hlk_vault_links.py` — PASS (only internal links; folder skeleton + cross-links).
- `py scripts/sync_compliance_mirrors_from_csv.py --goipoi-register-only --count-only` — PASS (count matches expanded row count: 11 rows = 10 existing + 1 new).
- `py -m pytest tests/test_validate_goipoi_register.py -v` — PASS (new tests).
- `py -m pytest tests/test_goipoi_distance_extension.py -v` — PASS (existing tests, regression check).

The pre-existing `validate_hlk.py` failure on `INIT-OPENCLAW_AKOS-68 / D-IH-66-AC` (documented in P13.0 §7) remains independent — P13.4 does not touch `INITIATIVE_REGISTRY.csv`.

## Closure ledger

- **Decision IDs:** D-W13-D (Asesoría placement) + D-W13-E (trainee placement)
- **Status:** Both confirmed (combined tranche)
- **Date:** 2026-05-11
- **Encoded in:** files listed in "Files mutated" above

End of P13.4 pause record.
