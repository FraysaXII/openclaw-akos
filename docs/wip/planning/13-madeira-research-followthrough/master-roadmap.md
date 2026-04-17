# Initiative 13 — MADEIRA research follow-through (SOTA-aligned)

**Status:** active (execution started 2026-04-17).  
**Related:** [Initiative 12 — external research + triage](../12-madeira-research-request/master-roadmap.md); [Initiative 11 — Madeira ops copilot](../11-madeira-ops-copilot/master-roadmap.md); HLK governance [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md).

## Goal

Turn Initiative **12** triage findings (F1–F8, section 5 UX hypotheses) into **repo changes**: intent exemplars + golden benchmark, clearer escalation / handoff copy, documentation alignment (verbose, Ollama `num_ctx`), and auditable before/after evidence — **without** widening Madeira write tools.

**Evidence rubric (source):** [`reports/research-vendor-deliverables-triage.md`](../12-madeira-research-request/reports/research-vendor-deliverables-triage.md).

## Asset classification (HLK)

| Class | In scope |
|:------|:---------|
| **Canonical** | No edits to `baseline_organisation.csv` / `process_list.csv`. |
| **Mirrored / derived** | `config/intent-exemplars.json`, `akos/intent.py` (`_ROUTE_MESSAGES` only if copy changes), `prompts/base/MADEIRA_BASE.md`, `prompts/overlays/OVERLAY_MADEIRA_OPS.md` (if touched), `tests/fixtures/intent_golden.json`, initiative `reports/`. |
| **Reference-only** | Initiative 12 vendor markdown — not SSOT. |

## Decision log

| ID | Decision |
|----|----------|
| D-MRF-1 | **Operator Paths 1–4** (AKOS) stay distinct from Holistika **methodology pillars** in all copy; see triage section 3. |
| D-MRF-2 | **No new regex** routes in `akos/intent.py` for F1 — exemplar bank + prompts only (D-OPS-4). |
| D-MRF-3 | **Before/after:** golden intent tests + optional embedding benchmark artifacts under `reports/`; qualitative WebChat rows reference [`docs/uat/hlk_admin_smoke.md`](../../../uat/hlk_admin_smoke.md) where applicable. |

## Governed verification matrix

Full gate set: [`docs/DEVELOPER_CHECKLIST.md`](../../../DEVELOPER_CHECKLIST.md) — inventory verify, drift, `py scripts/test.py all`, targeted pytest, `py scripts/release-gate.py`, `py scripts/browser-smoke.py --playwright` when relevant; `py scripts/validate_hlk.py` only if compliance assets change (not expected).

**UAT vs automated:** Per [`.cursor/rules/akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc), record dated outcomes under [`reports/`](reports/) for operator/WebChat qualitative rows.

## Reports

- Intent benchmark protocol and artifacts: [`reports/README.md`](reports/README.md)
- Optional UAT: `reports/uat-madeira-research-followthrough-<YYYYMMDD>.md`
