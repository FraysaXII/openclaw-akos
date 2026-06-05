---
initiative_id: INIT-OPENCLAW_AKOS-94
language: en
last_review: 2026-06-05
---

# I94 — Asset classification (per PRECEDENCE.md)

- **Canonical (P0 — edit-here-first):** `INITIATIVE_REGISTRY.csv` (I94 row), `DECISION_REGISTER.csv` (D-IH-94-*), `OPS_REGISTER.csv` (any I94 OPS rows).
- **Canonical doctrine (P1):** `AREA_GOVERNANCE_DISCIPLINE.md` v2, `LOGIC_CHANGE_LOG.md` entry, `akos/hlk_area_completeness.py` v2.
- **Canonical CSV gates (P4/P7 — explicit operator approval):** `baseline_organisation.csv` (Legal-as-area, entity axis, role rows), `process_list.csv` (area-process tranches), `PEOPLE_DESIGN_PATTERN_REGISTRY.csv` (kind/entity pattern), `CANONICAL_REGISTRY.csv` (moved disciplines).
- **Mirrored / derived:** `compliance.*_mirror` tables affected by P4/P7 path moves; WIP_DASHBOARD (auto-rendered).
- **Reference (planning-internal):** the research action under `docs/wip/intelligence/area-completeness-doctrine-2026-06-05/`; this folder's reports.
- **Engineering surface (CONTRIBUTING.md governed):** `akos/hlk_area_completeness.py`, `scripts/validate_area_completeness.py`, tests.

## Canonical CSV gate note

Per `akos-baseline-governance.mdc`: changes to `baseline_organisation.csv` / `process_list.csv`
require explicit operator approval before commit + `validate_hlk.py` in the verification matrix.
P4 (drift moves) and P7 (sub-folder remediation) each carry a per-area gate; no bulk move lands
without review.
