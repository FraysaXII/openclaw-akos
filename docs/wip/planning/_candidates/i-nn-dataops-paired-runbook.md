---
candidate_id: I-NN-DATAOPS-PAIRED-RUNBOOK
title: DataOps paired runbook — scripts/dataops_quality_check.py for DATAOPS_DISCIPLINE.md status:charter → status:active flip
status: candidate
authored: 2026-05-21
last_review: 2026-05-21
parent_initiatives: [86]
related_initiatives: [79, 80, 85]
priority: 3
language: en
audience: J-OP;J-AIC
access_level: 3
parent_lane: I86 Wave M Cluster B (engrave-properly mint of 4 Quality Fabric specialty canonicals)
charter_decisions:
  - D-IH-86-BU  # Cluster B engrave-properly OVERRIDE
  - D-IH-86-AZ  # original forward-charter of DataOps specialty
forward_charter_authority: D-IH-86-BU (operator override 2026-05-21: "As we sweep we clean and mint properly")
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/DATAOPS_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - .cursor/rules/akos-dataops-discipline.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
linked_ops_action_ids:
  - OPS-86-9  # Wave N+ paired-runbook deferral umbrella
---

# I-NN-DATAOPS-PAIRED-RUNBOOK — paired runbook for DataOps discipline

> **Spawned by I86 Wave M Cluster B engrave-properly mint** (2026-05-21). The `DATAOPS_DISCIPLINE.md` canonical landed at `status:charter` with 7 quality dimensions and a paired Cursor rule, but no executable runbook yet. Per [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (SOP + executable runbook pairing), the specialty canonical cannot flip to `status:active` until its paired runbook ships. This candidate names the runbook scope.

## 1. Activation gates

- **A1.** Operator approves promotion from `_candidates/` to `docs/wip/planning/<NN>-dataops-paired-runbook/master-roadmap.md`.
- **A2.** `DATAOPS_DISCIPLINE.md` reviewed at 90-day cadence per `last_review` and operator-validated as the right 7-dimension shape (status stays `charter` until A1 + A2 + A3 met).
- **A3.** No higher-priority I86-cluster initiative blocks the Wave N capacity slot.

## 2. Scope

- **Mint** [`scripts/dataops_quality_check.py`](../../../../scripts/dataops_quality_check.py) executing the 7-dimension data quality bar from `DATAOPS_DISCIPLINE.md` §2:
  - DATA-01 canonical-CSV SSOT integrity (Pydantic load + FK resolution).
  - DATA-02 Pydantic SSOT model coverage (every canonical CSV has a `akos/hlk_*_csv.py` model).
  - DATAOPS-03 validator coverage (every canonical CSV has a `scripts/validate_*.py` wired into `release-gate.py`).
  - DATA-04 mirror parity (Supabase `compliance.*_mirror` row counts match git CSV row counts).
  - DATA-05 FK integrity (every FK column resolves; no orphans).
  - DATA-06 freshness cadence (every canonical CSV `last_review` ≤ 90 days OR carries explicit deferral note).
  - DATA-07 observability hooks (every mirror has a Sentry breadcrumb for sync failures).
- **Mint** `akos/hlk_dataops_quality_check.py` — Pydantic SSOT model `DataOpsQualityFinding` (frozen; Literal enums for dimension_code + severity + verdict).
- **Mint** `tests/test_dataops_quality_check.py` — ≥ 14 tests (one valid + one invalid per dimension) under `@pytest.mark.dataops`.
- **Wire** `validate_dataops_quality_check_self_test` into [`config/verification-profiles.json`](../../../../config/verification-profiles.json) `pre_commit` profile.
- **Wire** `run_dataops_quality_check_self_test` into [`scripts/release-gate.py`](../../../../scripts/release-gate.py).
- **Flip** `DATAOPS_DISCIPLINE.md` frontmatter `status: charter` → `status: active`.
- **Flip** [`HOLISTIKA_QUALITY_FABRIC.md`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md) §6 row for DataOps `status` column `charter` → `active`.

## 3. Effort estimate

- ~3 person-days for the runbook + Pydantic model + tests + wiring.
- ~1 person-day for the `status: active` flip + cross-reference updates.
- Total: ~4 person-days. RICE-effort 0.8 person-weeks.

## 4. Cross-references

- Parent OPS: [`OPS-86-9`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) — Wave N+ paired-runbook deferral umbrella.
- Sibling candidates: `i-nn-mktops-paired-runbook.md` + `i-nn-techops-paired-runbook.md` + `i-nn-ux-paired-sop.md` (same Wave M Cluster B parentage; sequence flexibly within Wave N+).
- Rule: [`akos-dataops-discipline.mdc`](../../../../.cursor/rules/akos-dataops-discipline.mdc) — the discipline this runbook operationalises.
- Rule: [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 — pairing contract.
- Decision: [`D-IH-86-BU`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — Cluster B engrave-properly OVERRIDE.
