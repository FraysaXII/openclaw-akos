---
title: Evidence Class Gate Discipline (draft)
language: en
intellectual_kind: people-canonical
status: charter
audience: J-OP;J-AIC
authored: 2026-06-14
last_review: 2026-06-14
last_review_by: PMO
last_review_decision_id: D-IH-90-EVIDENCE-GATE
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-90-EVIDENCE-GATE
linked_canonicals:
  - UAT_DISCIPLINE.md
  - RESEARCH_ACTION_DISCIPLINE.md
  - HOLISTIKA_QUALITY_FABRIC.md
linked_runbooks:
  - scripts/validate_evidence_class_gate.py
  - scripts/validate_research_action.py
  - scripts/validate_uat_report.py
  - scripts/validate_aic_capability_implementation_matrix.py
linked_cursor_rules:
  - .cursor/rules/akos-evidence-class-gate.mdc
linked_skills:
  - .cursor/skills/evidence-class-gate-craft/SKILL.md
companion_to:
  - SOP-PEOPLE_EVIDENCE_CLASS_GATE_001.md
forward_charters:
  - EVIDENCE_CLASS_REGISTRY.csv vault promotion (P4c operator CSV gate)
  - UAT-FM-13 sibling UI browser manifest (P4b worked example first)
---

# Evidence Class Gate Discipline (draft)

> Cross-cutting People doctrine: **claims require proof class + artifact**.
> Validators check shape; this discipline checks that the *right* proof backs each claim.

## 1. Purpose

Holistika agents and operators routinely produce artifacts that *look* complete: CSVs exist,
validators pass, closure UAT has 11 sections. That is **git_shape** evidence only. Strategic
and experiential claims need stronger proof or honest FAIL/PWF.

This discipline binds:

- Research source ledgers
- Closure UAT PASS verdicts (forward from 2026-06-14)
- ACIM `implemented` + `confirmed` cells
- Initiative registry closure
- (Planned) sibling-repo UI browser manifests

## 2. Evidence classes

See `akos/evidence_class_gate.py` and draft registry
`docs/wip/planning/90-routing-and-wiring/drafts/EVIDENCE_CLASS_REGISTRY.draft.csv`.

Agents MUST pick exactly one primary class per closure claim. Secondary proof may appear in
§3 Mechanical evidence but the frontmatter `evidence_class` names the **gating** proof.

## 3. Mandatory frontmatter (closure UAT PASS)

When `verdict: PASS` and `last_review` ≥ `2026-06-14`:

```yaml
evidence_class: browser_experiential   # enum from §2
evidence_proof_ref: artifacts/uat-screenshots/i96-research-center-2026-06-11/MANIFEST.json
```

Validator finding: **UAT-FM-12-PASS-WITHOUT-EVIDENCE-CLASS**.

## 4. Research ledger honesty

One row per real external URL base. Hash fragments (`#N`) used to inflate row counts are
**forbidden**. Machine strip: `scripts/strip_padded_source_ledger.py`.

Finding codes: **RA-EC-01** (padding), **RA-EC-02** (duplicate base).

## 5. ACIM proof tokens

Forward `implemented` + `confirmed` rows must cite at least one of:

- Non-empty `tool_catalog_ref` pointing at repo path
- Non-empty `realisation_refs` (USE_CASE_ARCHIVE FK)
- Notes tokens `evidence_class=` and optionally `evidence_proof_ref=`

## 6. Initiative closure

`INITIATIVE_REGISTRY.status=closed` with `closed_at` ≥ watershed requires latest
`uat-*.md` with PASS or PWF; PASS rows must satisfy §3.

## 7. Promotion

Draft lives under `docs/wip/planning/90-routing-and-wiring/drafts/` until operator
ratifies vault promotion (P4c). Until then, mechanical enforcement in Phase A is binding.

## 8. Cross-references

- Governance design: `docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-governance-design-2026-06-14.md`
- I90 charter: `docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-charter-2026-06-14.md`
