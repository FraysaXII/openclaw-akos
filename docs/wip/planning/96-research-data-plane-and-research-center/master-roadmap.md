---
initiative_id: INIT-OPENCLAW_AKOS-96
initiative_slug: 96-research-data-plane-and-research-center
title: "I96 — Research Data Plane + Research Center Program"
status: active
program_line: true
authored: 2026-06-11
last_review: 2026-06-11
inception_decision_id: D-IH-96-A
owner_role: System Owner
co_owner_roles:
  - Lead Researcher
  - PMO
parent_initiatives:
  - INIT-OPENCLAW_AKOS-86
related_initiatives:
  - INIT-OPENCLAW_AKOS-75
  - INIT-OPENCLAW_AKOS-83
  - INIT-OPENCLAW_AKOS-88
  - INIT-OPENCLAW_AKOS-92
  - INIT-OPENCLAW_AKOS-95
linked_decisions:
  - D-IH-96-A
  - D-IH-75-G
language: en
audience: J-OP;J-AIC
program_anchors:
  - PRJ-HOL-DAT-2026
  - PRJ-HOL-PGF-2026
authoritative_plan: docs/wip/planning/96-research-data-plane-and-research-center/master-roadmap.md
research_lanes:
  - docs/wip/intelligence/akos-automation-os-governance-2026-06-10/
  - docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/
promoted_from: docs/wip/planning/_candidates/i-nn-research-data-management-and-feed-delivery.md
---

# I96 — Research Data Plane + Research Center Program

> **Program coordinator** for the three-plane research stack: **Govern** (AKOS git) → **Execute** (KiRBe) → **Experience** (HLK-ERP Research Center). Absorbs session work from 2026-06-10–11 (methodology mint, SSOT discipline, Automation OS R1–R6, holistic-agentic R3) into governed planning traceability. Promotes candidate [`i-nn-research-data-management-and-feed-delivery.md`](../_candidates/i-nn-research-data-management-and-feed-delivery.md) (STORE/RECALL/SHARE per `D-IH-75-G`).

## Three planes

| Plane | System | Role |
|:---|:---|:---|
| Govern | AKOS | Canon, ledgers, radar, disciplines, HCAM graph |
| Execute | KiRBe (`root_cd/kirbe`) | Ingest, hybrid search, embeddings, jobs |
| Experience | HLK-ERP (`root_cd/hlk-erp`) | Research Center UI at `/research-center` |

## Four tracks

| Track | Scope | Status entering I96-P0 |
|:---|:---|:---|
| **A** | Automation OS R7–R12 + D4 | R6 done (483/950 rows) |
| **B** | Research data plane (field mapping, inventory, staleness, SRC tags) | Spec mint at P1–P3 |
| **C** | KiRBe ledger→vault ingest contract | Handoff to I83 P2/P3 |
| **D** | ERP Research Center v1 (four panels) | **v1 PWF complete** (2026-06-12); **v2 insight machine chartered** |

## Phase shape

| Phase | Purpose | Deliverable | Verification |
|:---|:---|:---|:---|
| **P0** | Initiative mint + session incorporation | Standard artifacts + session-incorporation report | Planning README row; recap parent → I96 |
| **P0E** | Exploration matrix E1–E10 | `reports/exploration-matrix-2026-06-11.md` | No TBD in load-bearing rows |
| **P1** | Three-plane doctrine + field mapping | `three-plane-architecture.md`, `three-plane-field-mapping.md` | I88 Research OPS cross-link |
| **P2** | Data-consumer inventory | `reports/data-consumer-inventory-2026-06-11.md` (OPS-86-29) | DAMA lens complete |
| **P3** | Staleness loop + SRC tagging | `staleness-loop-spec.md`, `src-tagging-contract.md` | Radar hook documented |
| **P4** | TECH_AUTOMATION_REGISTRY alignment | Crosswalk in evidence-matrix; D5/D6 prep | `validate_research_action.py` |
| **P5** | KiRBe ingest contract | `ledger-to-vault-ingest-contract.md` | I83 handoff ack |
| **P6** | ERP page spec | `reports/research-center-page-spec-2026-06-11.md` | Operator inline-ratify |
| **P7** | ERP v1 implementation | `root_cd/hlk-erp` four-panel Research Center | **PASS-WITH-FOLLOWUP** (2026-06-12) — 21-screenshot manifest, auth fixed, Impeccable KiRBe relabel; [`uat-i96-research-center-browser-2026-06-11.md`](reports/uat-i96-research-center-browser-2026-06-11.md) |
| **P8-insight** | Track D v2 — topic research (not initiative-prefixed) | [`governed-actionable-analytics-surfaces-2026-06-12/`](../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/) | `validate_research_action.py` on 32-row ledger |
| **P9-pov-spec** | Track D v2 — POV spec ratify | [`research-center-page-spec-v2-2026-06-12.md`](reports/research-center-page-spec-v2-2026-06-12.md) + Excalidraw + AIC design pipeline handoff | **complete** (operator re-ratify 2026-06-12) |
| **P9b-figma-hifi** | Track D v2 — Figma hi-fi + GOJ disposition | [`governed-operator-journey-ux-uat-2026-06-12/`](../../intelligence/governed-operator-journey-ux-uat-2026-06-12/) + Figma frames + operator inline-ratify | **revision in_progress** — operator rejected first ratify 2026-06-12; [`p9b-revision-tranche-plan-2026-06-12.md`](reports/p9b-revision-tranche-plan-2026-06-12.md) (Phases A–D); blocks P10-T2 |
| **P10-v2-build** | Track D v2 — HLK-ERP implementation | POV switcher, insight rail, BFF `/insights` | **P10-T1 done**; **P10-T2 PAUSED** until P9b hi-fi ratified |
| **P11-v2-uat** | Track D v2 — experiential UAT | [`uat-i96-research-center-v2-charter-2026-06-12.md`](reports/uat-i96-research-center-v2-charter-2026-06-12.md) | Per-lens MCP manifest |
| **P8** | Automation OS R12 + D4 | 950-row ledger + `implementation-spec-2026-06-11.md` | Operator D4 ratification |
| **P9** | Holistic-agentic R4–R12 resume | WIP lane under I96 tracking | D4 unblocks |
| **P10** | Multi-channel feed (optional) | OPS-86-30 MVP | Deferred if P7 browser UAT not PASS |
| **P11** | Index integrity + I95 sweep hook | Sweep report; `artifacts/index-sweep` disposition | `validate_index_freshness.py` |
| **P12** | Program checkpoint UAT | `reports/uat-i96-p0-program-mint-2026-06-11.md` | Initiative stays **active** until Tracks B–D closure |

## Persistence rules

1. Recursive SSOT look-back every tranche ([`SSOT_REGISTRY_AUDIT_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/SSOT_REGISTRY_AUDIT_DISCIPLINE.md))
2. Update [`session-recap-2026-06-10.md`](../../intelligence/akos-automation-os-governance-2026-06-10/session-recap-2026-06-10.md) after each tranche
3. One commit per phase where practical
4. No canonical CSV mint without AskQuestion

## Verification matrix (golden path)

```powershell
py scripts/verify.py pre_commit_fast
py scripts/validate_hlk.py
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv
py scripts/validate_research_radar.py --self-test
py scripts/check-drift.py
```

## P7 browser UAT bar (operator-ratified 2026-06-12)

Track D ships UI in the sibling repo **HLK-ERP**. Browser experiential sign-off is **non-deferrable** — mechanical validators and Playwright anonymous smoke are necessary but not sufficient.

| Rule | Detail |
|:---|:---|
| **Verdict posture** | **PASS-WITH-FOLLOWUP** — v1 experiential bar met 2026-06-12; v2 insight machine chartered (P8–P11) |
| **Workflow order** | **Localhost first:** `http://localhost:3010/sign-in?next=%2Fresearch-center` → magic-link → panel walk → screenshots |
| **Production SSL** | `https://erp.holistikaresearch.com/research-center` blocked in Cursor MCP browser (-107) — remediate separately; does not excuse skipping localhost |
| **Evidence manifest** | `artifacts/uat-screenshots/i96-research-center-<YYYY-MM-DD>/` + sha256 sidecar per planning traceability §browser-evidence audit-trail |
| **Viewports** | 375 / 768 / 1280 (I68 baseline) |
| **Accessibility** | axe on `/research-center` post-login |
| **Impeccable** | Full P7 bar — live browser snapshots + audit disposition (KiRBe hybrid search fix or honest relabel) |
| **Design preview** | AIC-owned mockup/prototype (Figma primary; Excalidraw+ interim) before operator ratify — see MADEIRA experiential UAT charter |

Cross-ref: [`reports/uat-i96-research-center-browser-2026-06-11.md`](reports/uat-i96-research-center-browser-2026-06-11.md), [`docs/wip/intelligence/aic-madeira-experiential-uat-2026-06-11/charter.md`](../../intelligence/aic-madeira-experiential-uat-2026-06-11/charter.md).

## Track D v2 — Insight machine (operator guidance 2026-06-12)

v1 proved the Experience plane shell (auth + four panels + PWF UAT). v2 shifts to **dashboards as insight machines**: multi-POV lenses, actionable insight cards with governed CTAs, drill-down to three-plane artifacts.

| Item | Path |
|:---|:---|
| Topic research pack (analytics) | [`docs/wip/intelligence/governed-actionable-analytics-surfaces-2026-06-12/`](../../intelligence/governed-actionable-analytics-surfaces-2026-06-12/) (I96 consumer; D-IH-95-H move) |
| Topic research pack (journey + UAT loop) | [`docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/`](../../intelligence/governed-operator-journey-ux-uat-2026-06-12/) — **GOJ-UX-UAT** content disposition + ratify LOOP |
| Page spec v2 | [`reports/research-center-page-spec-v2-2026-06-12.md`](reports/research-center-page-spec-v2-2026-06-12.md) |
| UAT v2 charter | [`reports/uat-i96-research-center-v2-charter-2026-06-12.md`](reports/uat-i96-research-center-v2-charter-2026-06-12.md) |
| Operator session index | [`reports/operator-check-links-2026-06-12.md`](reports/operator-check-links-2026-06-12.md) |

**v1 gaps driving v2:** ledger 0 rows on localhost, empty radar queue, KiRBe red without remediation card, no drill-down, single layout for all roles (manifest `18`–`20`).

**POV lenses:** Director / Operator / Auditor / Finance / Compliance.

**P9 status (2026-06-12):** **complete** — operator re-ratify after research rework; Excalidraw scene `2yBmIbavOEj`; AIC design pipeline handoff (execution seat mints Figma; operator ratifies preview only); Tremor spike closed (shadcn Card wins).

**P9b status (2026-06-13):** **Phase A complete** (operator-ratified visual polish — [`p9b-phase-a-status-2026-06-13.md`](reports/p9b-phase-a-status-2026-06-13.md)). **Phase B+C in progress** — unified insight-machine tranche ([`research-center-phase-bc-tranche-plan-2026-06-12.md`](reports/research-center-phase-bc-tranche-plan-2026-06-12.md)): hlk-erp journey widgets (Operator+Director T2) + Figma matrix refresh + experiential UAT ladder L0–L3 ratify gate. **P10-T2 PAUSED** until B+C operator inline-ratify. Prong SSOT complete ([`p9b-prong-ssot-fix-2026-06-13.md`](reports/p9b-prong-ssot-fix-2026-06-13.md)).

**P10 status:** **T1 complete** (remediation cards, POV switcher, drawer shell @ localhost:3010). **T2 PAUSED** until P9b **revision** closes (Figma + localhost operator ratify after Phases A–D).

**Prong SSOT (2026-06-13):** **complete** — Automation OS + holistic-agentic ledgers rewritten to `BL-*`; validator enforces baseline IDs. Report: [`p9b-prong-ssot-fix-2026-06-13.md`](reports/p9b-prong-ssot-fix-2026-06-13.md). **I97** `INFONOMICS_DISCIPLINE` closed — Track D economics consumes per **D-IH-96-J**.

**Next gate:** Phase B+C operator inline-ratify (Figma five lenses + localhost journey smoke L1–L3 per [`research-center-experiential-uat-ladder-2026-06-12.md`](reports/research-center-experiential-uat-ladder-2026-06-12.md)) → Phase D manifest → P10-T2 → P11 UAT.

