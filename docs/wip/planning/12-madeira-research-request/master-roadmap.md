# Initiative 12 — MADEIRA external research request

**Status:** active (handoff document published).  
**Related:** [Initiative 11 — Madeira ops copilot](../11-madeira-ops-copilot/master-roadmap.md); HLK governance [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md).

## Goal

Publish a **single briefing** for an external research team to discover use cases, technology fit, frameworks, and user journeys for MADEIRA — without prescribing product themes. Canonical copy: [`research-request-madeira.md`](research-request-madeira.md).

## Asset classification (HLK)

| Class | In scope |
|:------|:---------|
| **Canonical** | No edits to `baseline_organisation.csv` / `process_list.csv` as part of this initiative. |
| **Mirrored / derived** | This folder (`research-request-madeira.md`, `master-roadmap.md`), [`docs/wip/planning/README.md`](../README.md) index row. |
| **Reference-only** | Vendor research markdown in this folder (e.g. `Researching Madeira AI Assistant.md`, `Researching MADEIRA Assistant in AKOS.md`) — not SSOT; read with [`reports/research-vendor-deliverables-triage.md`](reports/research-vendor-deliverables-triage.md). |

## Decision log

| ID | Decision |
|----|----------|
| D-RR-1 | Research briefing lives in `docs/wip/planning/12-madeira-research-request/research-request-madeira.md`; initiative **12** reserved in planning index. |
| D-RR-2 | Governed **vendor deliverables triage** published: [`reports/research-vendor-deliverables-triage.md`](reports/research-vendor-deliverables-triage.md) (evidence rubric, operator paths vs methodology pillars, UAT cross-check vs Initiative 11, UX hypotheses, governance pointers only). |
| D-RR-3 | **Classified addendum** (findings F1–F10, footnotes, commissioning handoff table) lives in **section 8** of that triage doc; maintain per section 7 and **section 8.1** when research updates. |

## Governed verification matrix

No repository code or compliance CSV changes for **this** initiative.

**Follow-on initiatives** (prompt/UX, gateway, swarm, integration, or any work under `config/`, `akos/`, `scripts/`, or canonical HLK assets) **must not** narrow the repo gate set: use the full matrix in [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) (including `validate_hlk.py` / `validate_hlk_km_manifests.py` when compliance assets or Output 1 manifests are in scope).

**UAT vs automated:** If a child roadmap promises **dashboard WebChat**, **Cursor Browser MCP**, **Langfuse UI**, or similar operator sign-off, record dated outcomes under `docs/wip/planning/<NN-initiative-slug>/reports/` per **`.cursor/rules/akos-planning-traceability.mdc`** — automated smoke alone is not sufficient for those rows.

## Post-research (not part of initiative closure)

After external findings exist: prioritise prompt/UX vs gateway vs swarm vs integration work in a backlog (commissioning party). **Triage** for how to read vendor follow-ups: [`reports/research-vendor-deliverables-triage.md`](reports/research-vendor-deliverables-triage.md).
