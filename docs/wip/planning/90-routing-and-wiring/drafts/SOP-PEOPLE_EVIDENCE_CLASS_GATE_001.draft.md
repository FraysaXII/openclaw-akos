---
title: SOP — Evidence Class Gate Governance (draft)
language: en
status: draft
role_owner: PMO
process_id: hol_peopl_dtp_evidence_class_gate_001
audience: J-OP;J-AIC
linked_canonicals:
  - EVIDENCE_CLASS_GATE_DISCIPLINE.md
linked_runbooks:
  - scripts/validate_evidence_class_gate.py
cadence: event_triggered
---

# SOP-PEOPLE_EVIDENCE_CLASS_GATE_001 (draft)

## 1. Scope

Applies when any agent or operator:

- Authors or closes a research `source-ledger.csv`
- Sets closure UAT `verdict: PASS` on/after 2026-06-14
- Marks ACIM cell `implemented` + `confirmed`
- Flips `INITIATIVE_REGISTRY` to `closed`

## 2. AC-HUMAN (operator / role-owner)

1. Read claim surface in draft registry row (ECB-NNNN).
2. Pick evidence class matching real proof (not aspirational).
3. Ensure `evidence_proof_ref` path exists before PASS.
4. For initiative close: confirm closure UAT path in initiative folder.
5. Ratify vault promotion at P4c CSV gate.

## 3. AC-AUTOMATION (AIC / CI)

1. `py scripts/validate_evidence_class_gate.py --self-test` — pre_commit_fast.
2. Component validators enforce per-surface rules (research / UAT / ACIM).
3. `py scripts/validate_hlk.py` — umbrella includes EVIDENCE_CLASS_GATE row.
4. On ledger rebuild: `py scripts/strip_padded_source_ledger.py --ledger <path> --write`.

## 4. Escalation

| Signal | Action |
|:---|:---|
| RA-EC-01/02 on ledger | Strip + rebuild; never manual row verify |
| UAT-FM-12 | Add frontmatter or downgrade verdict to FAIL/PWF |
| ACIM proof missing | Add tool path or notes tokens; do not lower confidence |
| Initiative close blocked | Fix closure UAT or reopen initiative |

## 5. Paired canonical

Promote with `EVIDENCE_CLASS_GATE_DISCIPLINE.md` and `EVIDENCE_CLASS_REGISTRY.csv`
in single operator-approved commit per SOP-META CSV-before-SOP order.
