---
title: I90 P4 — Evidence-class gate charter
last_review: 2026-06-14
audience: J-OP;J-AIC
status: active
ratifying_decisions:
  - D-IH-90-EVIDENCE-GATE
---

# Evidence-class gate charter (I90 Phase 4)

Operator ratification 2026-06-14: **shape-PASS is not intent proof.** Validators that
only check CSV headers, row counts, and FK resolution must not be treated as closure
evidence for research ledgers, closure UAT, capability implementation claims, or
initiative closure.

This phase adds a **platform spine** under Initiative 90 (routing and wiring ordnance)
so MADEIRA and AIC execution cannot re-close work on mechanical green alone.

## Problem statement

I100 exposed the failure mode at scale: a 780-row source ledger passed
`validate_research_action.py` while **463 rows were synthetic hash-padding** on the
same vendor doc bases (`#1`, `#2`, …). The same pattern appeared in I96 Track D
(browser/experiential UAT treated as optional after automated smoke passed).

## Evidence classes (SSOT: `akos/evidence_class_gate.py`)

| Class | What it proves | Typical proof artifact |
|:---|:---|:---|
| `git_shape` | Schema/header/FK/shape validators | Validator stdout or HLK umbrella run row |
| `url_verify` | External URL reachable (HEAD/GET) | Probe log or research-action `--url-probe` output |
| `live_probe` | Runtime/deploy probe succeeded | `dataops_quality_check.py` or deploy-health artifact |
| `browser_experiential` | Operator-visible UI journey | `artifacts/uat-screenshots/` bundle + MANIFEST |
| `operator_ratify` | Explicit operator decision | `DECISION_REGISTER` row + AskQuestion record |
| `meta_regression` | Intent-ranked regression after validator change | `intent_ranked_regression.py` report |

## Watershed

**2026-06-14** — forward artifacts on or after this date are fail-closed:

- Research source ledgers: no hash-padding; no duplicate external URL bases
- Closure UAT **PASS**: requires `evidence_class` + `evidence_proof_ref` in frontmatter
- ACIM rows `implemented` + `confirmed`: require proof ref (tool path, realisation, or notes tokens)
- Initiative `closed` with `closed_at` ≥ watershed: closure UAT must PASS/PWF with evidence bar on PASS

Historical initiatives (closed before watershed) remain exempt from initiative closure cross-check.

## Tranche 1 deliverables (this commit)

1. `akos/evidence_class_gate.py` — enum + helpers
2. `scripts/validate_evidence_class_gate.py` — initiative closure cross-check + self-test
3. `scripts/strip_padded_source_ledger.py` — machine strip for padded ledgers
4. Extensions: `validate_research_action.py`, `validate_uat_report.py` (UAT-FM-12),
   `validate_aic_capability_implementation_matrix.py`
5. HLK umbrella + `pre_commit_fast` wiring

Governance (P4a): [`evidence-class-gate-governance-design-2026-06-14.md`](evidence-class-gate-governance-design-2026-06-14.md)

## Tranche 2 (scheduled — not dropped)

End-to-end vertical slice on **hlk-erp Preview** (Vercel + Cloudflare + GitHub path):
deploy-health + browser experiential + live registry reconcile. Tracked as I90 P4b /
I96+I100 cross-link after Tranche 1 validators green.

## Cross-references

- Research integrity audit: `docs/wip/intelligence/lab-component-ecosystem-governance-2026-06-14/source-ledger-integrity-audit-2026-06-14.md`
- Automation intent gap synthesis: `docs/wip/intelligence/lab-component-ecosystem-governance-2026-06-14/research-synthesis-automation-intent-gap-2026-06-14.md`
- I100 reopen: `D-IH-100-REOPEN` — initiative stays **active** until honest ledger + harmonization + experiential proof
- MADEIRA experiential pack: `docs/wip/intelligence/aic-madeira-experiential-uat-2026-06-11/`
- HCAM orchestration: `docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/`

## Verification

```powershell
py scripts/validate_evidence_class_gate.py --self-test
py scripts/strip_padded_source_ledger.py --ledger docs/wip/intelligence/lab-component-ecosystem-governance-2026-06-14/source-ledger.csv --write
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/lab-component-ecosystem-governance-2026-06-14/source-ledger.csv
py scripts/validate_hlk.py
py -m pytest tests/test_validate_research_action.py tests/test_evidence_class_gate.py -v
```
