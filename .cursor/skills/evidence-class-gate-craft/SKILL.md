---
name: Evidence Class Gate Craft
description: >-
  Use when binding a completion claim to proof — research source ledger govern,
  closure UAT PASS frontmatter, ACIM implemented+confirmed rows, initiative
  close, or extending evidence-class validators. Triggers on evidence_class,
  evidence_proof_ref, RA-EC-01, UAT-FM-12, validate_evidence_class_gate,
  strip_padded_source_ledger, shape-PASS vs intent proof, hash-padding ledger,
  or I90 P4 evidence gate. Pairs with .cursor/rules/akos-evidence-class-gate.mdc
  (WHEN); this skill is HOW.
---

# Evidence Class Gate Craft

## Principle 1 — Name the proof before the verdict

Write `evidence_class` + `evidence_proof_ref` **before** `verdict: PASS`. The proof file
must exist (or the validator output must be capturable to `artifacts/evidence-gate/`).

| Claim type | Prefer class | Avoid |
|:---|:---|:---|
| Validator-only closure | `git_shape` | Calling UI done |
| Screenshot journey | `browser_experiential` | Self-test only |
| Deploy/platform check | `live_probe` | Lint green |
| Operator sign-off | `operator_ratify` | Agent default |
| Post-validator edit | `meta_regression` | Skipping ICS sweep |

## Principle 2 — Strip dishonest ledgers mechanically

After seed scripts or bulk imports:

```powershell
py scripts/strip_padded_source_ledger.py --ledger docs/wip/intelligence/<pack>/source-ledger.csv --write
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/<pack>/source-ledger.csv
```

Never ask the operator to verify hundreds of padded rows.

## Principle 3 — Disposition table

| Finding | Fix |
|:---|:---|
| RA-EC-01 hash padding | Strip script; fix seed generator |
| RA-EC-02 duplicate base | Dedupe in source script |
| UAT-FM-12 missing class | Add frontmatter or use FAIL/PWF |
| ACIM proof missing | Add `tool_catalog_ref` path |
| Initiative close blocked | Amend closure UAT or keep `active` |

## Principle 4 — Phase B experiential bar

For sibling-repo UI (hlk-erp Preview): capture manifest under
`artifacts/uat-screenshots/<slug>-<date>/MANIFEST.json`; set
`evidence_class: browser_experiential` on eventual PASS.

## Cross-references

- Governance design: `docs/wip/planning/90-routing-and-wiring/reports/evidence-class-gate-governance-design-2026-06-14.md`
- Registry draft: `docs/wip/planning/90-routing-and-wiring/drafts/EVIDENCE_CLASS_REGISTRY.draft.csv`
