---
title: I90 P4b — Preview vertical slice (evidence-class gate)
last_review: 2026-06-14
audience: J-OP;J-AIC
status: scheduled
carryover_posture: scheduled
activation_trigger: P4a governance drafts reviewed; hlk-erp Preview deploy reachable
---

# Phase B — hlk-erp Preview end-to-end proof

**Carryover posture:** scheduled for I90 P4b (not dropped) — starts after operator
skims governance design; tracked in I90 master-roadmap §P4.

## Goal

One **vertical slice** that proves the evidence-class gate on a real consumer surface —
not more registry minting.

## Critical path

| Step | Evidence class | Artifact |
|:---|:---|:---|
| 1. Vercel Preview deploy green | `live_probe` | deploy-health checklist output |
| 2. Cloudflare zone / DNS posture | `live_probe` | zone registry reconcile note |
| 3. GitHub CI posture | `git_shape` | `GITHUB_REPO_CI_POSTURE_REGISTRY` + CI run link |
| 4. Browser journey (Research Center or shell) | `browser_experiential` | `artifacts/uat-screenshots/i96-preview-*` manifest |
| 5. Optional registry reconcile | `live_probe` | `lab_platform_registry_reconcile.py` output (when probes wired) |

## Initiatives touched

- **I96** — Research Center experiential UAT (reopen track; FAIL → target PWF/PASS with proof)
- **I100** — lab platform registries (reconcile only; no re-close)
- **Deploy-health discipline** — Failure catalogue steps 1–4

## PASS bar for slice closure report

Draft UAT or supplement under `docs/wip/planning/90-routing-and-wiring/reports/` with:

```yaml
evidence_class: browser_experiential
evidence_proof_ref: artifacts/uat-screenshots/<bundle>/MANIFEST.json
```

## Out of scope (this slice)

- Vault promotion of `EVIDENCE_CLASS_REGISTRY.csv` (P4c operator gate)
- I100 harmonization CSV merge (I100 active; separate tranche)
- FM-13 FAIL ramp (needs one clean manifest first)

## Commands (when executing)

```powershell
# Deploy smoke — consumer repo per deploy-health craft
py scripts/browser-smoke.py --playwright

# Evidence gate regression
py scripts/validate_evidence_class_gate.py
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/lab-component-ecosystem-governance-2026-06-14/source-ledger.csv
```

## Cross-references

- Governance design: [`evidence-class-gate-governance-design-2026-06-14.md`](evidence-class-gate-governance-design-2026-06-14.md)
- I96 production UAT: `docs/wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-production-2026-06-14.md`
