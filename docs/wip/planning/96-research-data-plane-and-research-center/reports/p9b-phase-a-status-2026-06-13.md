---
initiative_id: INIT-OPENCLAW_AKOS-96
report_kind: phase-a-status
parent_phase: P9b-figma-hifi
authored: 2026-06-13
status: implemented_pending_verify
audience: J-OP;J-AIC
sibling_repo: root_cd/hlk-erp
prerequisite: p9b-prong-ssot-fix-2026-06-13.md
---

# P9b Phase A — visual polish status (2026-06-13)

> **Outcome:** Phase A broken fixes and Impeccable items **A-B1..A-B5** and **IF-01..IF-10** are implemented in the HLK-ERP sibling repo (`root_cd/hlk-erp`). `npm run typecheck` PASS. Operator localhost walk + screenshot manifest still required before Phase A is **closed** and Phase B starts.

## Prerequisite cleared (AKOS)

[`p9b-prong-ssot-fix-2026-06-13.md`](p9b-prong-ssot-fix-2026-06-13.md) — Automation OS + holistic-agentic ledgers use `BL-*` only; commit `92f30471`.

## Phase A disposition matrix

| ID | Requirement | Status | Evidence (hlk-erp) |
|:---|:---|:---|:---|
| **A-B1** | Freshness pills dark-mode safe | **Done** | `components/research-center/freshness-strip.tsx` — semantic `border-border bg-muted/50` + tone borders |
| **A-B2** | No `fixture` badge on card face | **Done** | `insight-card-rail.tsx` — cards use live remediation only; Gate B (D-IH-96-G) |
| **A-B3** | Primary CTA runs action, not drawer | **Done** | `handlePrimaryCta` — runbook copy + toast; artifact opens link |
| **A-B4** | v1 accordion collapsed default | **Done** | `v1-panels-accordion.tsx` — `defaultValue=""` + optional session expand |
| **A-B5** | POV Select @375 | **Done** | `pov-switcher.tsx` — `Select` below `sm`, horizontal scroll `ToggleGroup` at `sm+` |
| **IF-01** | Token-based freshness pills | **Done** | Same as A-B1 |
| **IF-02** | Varied vertical rhythm | **Done** | `research-center-client.tsx` — header `space-y-4`, rail `mt-6`, accordion `mt-10 border-t` |
| **IF-03** | No hero metrics on operator default | **Done** | `ledger-summary-panel.tsx` — inline `text-sm` stats inside accordion only |
| **IF-04** | Remediation full-width stack | **Done** | `insight-card-rail.tsx` — `flex flex-col gap-3` when remediation-first |
| **IF-05** | Govern paths in T3 collapsible | **Done** | Drawer `Audit details (technical paths)` collapsible |
| **IF-06** | Short hero copy | **Done** | Single-line subtitle; audit note only on accordion trigger |
| **IF-07** | Responsive POV | **Done** | Same as A-B5 |
| **IF-08** | ≤7 card cap | **Done** | `CARD_CAP = 7` + overflow link to audit panels |
| **IF-09** | Lens empty states | **Done** | `lens-empty-state.tsx` — live-only empty UX (Gate B × IF-09 resolution) |
| **IF-10** | Copy feedback on runbook CTA | **Done** | `sonner` toast + `active:scale-[0.98]` on buttons |

## Mechanical verification (execution seat)

```powershell
cd root_cd/hlk-erp
npm run typecheck   # PASS 2026-06-13
npm run lint        # PASS (unrelated command-palette hook warning)
npx playwright test --grep research-center
```

## Still required to **close** Phase A

| Step | Owner | Why |
|:---|:---|:---|
| Localhost walk @ 375 / 768 / 1280 | Operator | P9b revision plan §Phase A.3 — experiential bar, not typecheck alone |
| Dark + light theme spot-check | Operator | IF-01 acceptance |
| Commit hlk-erp Research Center v2 bundle | Execution seat | Sibling repo currently uncommitted |
| Update check-links index | Execution seat | After screenshots land |

## What we do next (not optional framing)

| Step | Do? | Reason |
|:---|:---|:---|
| **Phase B** journey components | **NO until Phase A operator verify** | Plan hard-sequences A → B; avoids building on unratified craft |
| **Phase C Figma refresh** | **NO until A+B** | R-P9b-01 drift mitigation |
| **P10-T2 resume** | **NO until P9b revision complete** | Master roadmap binding |

## Cross-references

- Revision plan: [`p9b-revision-tranche-plan-2026-06-12.md`](p9b-revision-tranche-plan-2026-06-12.md)
- Visual audit baseline: [`p9b-visual-audit-2026-06-12.md`](p9b-visual-audit-2026-06-12.md)
- Operator index: [`operator-check-links-2026-06-12.md`](operator-check-links-2026-06-12.md)
