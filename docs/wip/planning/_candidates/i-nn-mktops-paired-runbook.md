---
candidate_id: I-NN-MKTOPS-PAIRED-RUNBOOK
title: MKTOps paired runbook — scripts/mktops_campaign_quality_check.py for MKTOPS_DISCIPLINE.md status:charter → status:active flip
status: candidate
authored: 2026-05-21
last_review: 2026-05-21
parent_initiatives: [86]
related_initiatives: [66, 70, 72, 79]
priority: 3
language: en
audience: J-OP;J-AIC
access_level: 3
parent_lane: I86 Wave M Cluster B (engrave-properly mint of 4 Quality Fabric specialty canonicals)
charter_decisions:
  - D-IH-86-BU
  - D-IH-86-AZ
forward_charter_authority: D-IH-86-BU (operator override 2026-05-21: "As we sweep we clean and mint properly")
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/MKTOPS_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md
  - .cursor/rules/akos-mktops-discipline.mdc
  - .cursor/rules/akos-brand-baseline-reality.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
linked_ops_action_ids:
  - OPS-86-9
---

# I-NN-MKTOPS-PAIRED-RUNBOOK — paired runbook for MKTOps discipline

> **Spawned by I86 Wave M Cluster B engrave-properly mint** (2026-05-21). [`MKTOPS_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/MKTOPS_DISCIPLINE.md) landed at `status:charter` with 7 marketing-quality dimensions and a paired Cursor rule, but no executable runbook yet. This candidate names the runbook scope.

## 1. Activation gates

- **A1.** Operator approves promotion from `_candidates/` to `docs/wip/planning/<NN>-mktops-paired-runbook/master-roadmap.md`.
- **A2.** First operator-validated campaign artefact set lands (brief + creative + landing page + measurement) for ≥ 1 audience class so the runbook has real input to validate against.
- **A3.** Brand voice + persona registries stable (no churn in last 30 days).

## 2. Scope

- **Mint** [`scripts/mktops_campaign_quality_check.py`](../../../../scripts/mktops_campaign_quality_check.py) executing the 7-dimension marketing quality bar:
  - MKT-01 brief quality (audience + channel + outcome named; persona FK resolves).
  - MKT-02 creative brand-canon adherence (translates to external register per `BRAND_BASELINE_REALITY_MATRIX.md`).
  - MKT-03 landing-page UX-translation (consumes UX discipline 7-dimension bar for the page primitive).
  - MKT-04 adapter status currency (CRM + email + scheduling + attribution adapter status `active` for the chosen channels).
  - MKT-05 persona FK integrity (every targeted persona resolves against `PERSONA_REGISTRY.csv`).
  - MKT-06 voice consistency (jargon-audit per `BRAND_JARGON_AUDIT.md` §4 passes for external-tagged artefacts).
  - MKT-07 measurement (every campaign declares its conversion event + measurement adapter slot).
- **Mint** `akos/hlk_mktops_quality_check.py` — Pydantic SSOT model.
- **Mint** `tests/test_mktops_campaign_quality_check.py` — ≥ 14 tests under `@pytest.mark.mktops`.
- **Wire** into `verification-profiles.json` + `release-gate.py`.
- **Flip** `MKTOPS_DISCIPLINE.md` `status: charter` → `status: active`.
- **Flip** `HOLISTIKA_QUALITY_FABRIC.md` §6 row for MKTOps `status` column.

## 3. Effort estimate

- ~4 person-days for the runbook + Pydantic + tests + wiring (slightly more than DataOps because of adapter-registry cross-FK lookups).
- ~1 person-day for the `status:active` flip + cross-references.
- Total: ~5 person-days. RICE-effort 1.0 person-week.

## 4. Cross-references

- Parent OPS: [`OPS-86-9`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv).
- Sibling candidates: `i-nn-dataops-paired-runbook.md` + `i-nn-techops-paired-runbook.md` + `i-nn-ux-paired-sop.md`.
- Rule: [`akos-mktops-discipline.mdc`](../../../../.cursor/rules/akos-mktops-discipline.mdc).
- Rule: [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — MKT-02 grounding.
- Decision: [`D-IH-86-BU`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
