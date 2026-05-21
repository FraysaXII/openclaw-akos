---
candidate_id: I-NN-UX-PAIRED-SOP
title: UX paired SOP — SOP-PEOPLE_UX_RESEARCH_001.md for UX_DISCIPLINE.md status:charter → status:active flip
status: candidate
authored: 2026-05-21
last_review: 2026-05-21
parent_initiatives: [86]
related_initiatives: [66, 72, 79]
priority: 3
language: en
audience: J-OP;J-AIC
access_level: 3
parent_lane: I86 Wave M Cluster B (engrave-properly mint of 4 Quality Fabric specialty canonicals)
charter_decisions:
  - D-IH-86-BU
  - D-IH-86-AX  # original Wave J forward-charter of UX specialty
forward_charter_authority: D-IH-86-BU (operator override 2026-05-21: "As we sweep we clean and mint properly")
linked_canonicals:
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/UX_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
  - .cursor/rules/akos-ux-discipline.mdc
  - .cursor/rules/akos-external-render-discipline.mdc
  - .cursor/skills/impeccable/SKILL.md
linked_ops_action_ids:
  - OPS-86-9
---

# I-NN-UX-PAIRED-SOP — paired SOP for UX discipline

> **Spawned by I86 Wave M Cluster B engrave-properly mint** (2026-05-21). [`UX_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/UX_DISCIPLINE.md) landed at `status:charter` with 7 UX dimensions and a paired Cursor rule. Unlike the DataOps/MKTOps/TechOps siblings, the paired surface here is a **SOP** (not a runbook script) because UX research is human-led with agent-assist via the [`impeccable`](../../../../.cursor/skills/impeccable/SKILL.md) skill — the executable layer is the skill, not a Python validator.

## 1. Activation gates

- **A1.** Operator approves promotion from `_candidates/` to `docs/wip/planning/<NN>-ux-paired-sop/master-roadmap.md`.
- **A2.** ≥ 3 channel-specific UX doctrine pages (e.g., `UX_WEB_DOCTRINE.md` + `UX_PDF_DOCTRINE.md` + `UX_SLIDE_DOCTRINE.md`) reach `status:active` so the SOP has channel-specific guidance to reference (the SOP names the **process** of running UX research; the channel doctrines name the **per-medium quality bar**).
- **A3.** ≥ 1 operator-validated UX research session completed for a real Holistika artefact so the SOP captures lived practice not hypothetical structure.

## 2. Scope

- **Mint** [`SOP-PEOPLE_UX_RESEARCH_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_UX_RESEARCH_001.md) at `status:active` per the impeccable-template shape:
  - **Purpose**: when to run UX research + what classes of decision it informs.
  - **Scope**: which Holistika surfaces (web routes / PDFs / decks / emails / ERP panels) the SOP applies to.
  - **Inputs**: artefact-to-validate + target audience class(es) + channel context + research goal.
  - **Steps**: (1) frame the research question per `UX_DISCIPLINE.md` 7 dimensions; (2) pick the method (heuristic walk / a11y audit / 5-user usability test / analytics replay / Sentry session replay); (3) execute with the [`impeccable`](../../../../.cursor/skills/impeccable/SKILL.md) skill + persona-as-evaluator pattern; (4) record findings in dimension-tagged format; (5) propose remediations with effort estimates; (6) inline-ratify with operator per `akos-inline-ratification.mdc`.
  - **Outputs**: dated `reports/ux-research-<artefact>-<YYYY-MM-DD>.md` per initiative + remediation backlog rows.
  - **Failure modes**: research-as-ornament (no remediations land); research-too-late (post-ship); research-against-wrong-audience (persona FK mismatch); skill-bypass (writing UX findings without invoking impeccable skill craft).
  - **Cross-references**: UX_DISCIPLINE.md + impeccable skill + akos-external-render-discipline.mdc + persona registry.
- **Mint** ≥ 1 channel-specific doctrine page (e.g., `UX_WEB_DOCTRINE.md`) at `status:charter` as a starter; full set deferred to A2 cadence.
- **Flip** `UX_DISCIPLINE.md` `status: charter` → `status: active`.
- **Flip** `HOLISTIKA_QUALITY_FABRIC.md` §6 row for UX `status` column.
- **Append** SOP row to `process_list.csv` (`hol_peopl_dtp_ux_research_001` per the row-id convention) per `akos-executable-process-catalog.mdc` Rule 1.

## 3. Effort estimate

- ~3 person-days for the SOP draft + 1 channel doctrine page + operator review cycle.
- ~1 person-day for the `process_list.csv` row + cross-references.
- Total: ~4 person-days. RICE-effort 0.8 person-weeks.

## 4. Cross-references

- Parent OPS: [`OPS-86-9`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv).
- Sibling candidates: `i-nn-dataops-paired-runbook.md` + `i-nn-mktops-paired-runbook.md` + `i-nn-techops-paired-runbook.md`.
- Rule: [`akos-ux-discipline.mdc`](../../../../.cursor/rules/akos-ux-discipline.mdc).
- Rule: [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) — UX-02 channel adaptation grounding.
- Skill: [`impeccable`](../../../../.cursor/skills/impeccable/SKILL.md) — the agent-assist executable layer.
- Decision: [`D-IH-86-BU`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
