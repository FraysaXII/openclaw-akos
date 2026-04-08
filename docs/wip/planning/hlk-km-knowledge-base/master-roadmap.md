# HLK governed KM — workspace master roadmap

**Initiative slug:** `hlk-km-knowledge-base`  
**Status:** In progress (P0–P2 execution)  
**Date:** 2026-04-08  

**Source plan (workspace, do not treat as canonical vault):** `.cursor/plans/hlk_km_topic-fact-source_3745f5d0.plan.md` — governs Topic–Fact–Source, Output 1 manifests, PMO Trello registry, and optional manifest validation.

---

## Asset classification (per PRECEDENCE)

| Class | Paths | Rule |
|-------|--------|------|
| **Canonical** | `docs/references/hlk/compliance/` (including `HLK_KM_TOPIC_FACT_SOURCE.md`, CSVs, taxonomy MD), `docs/references/hlk/v3.0/` role-owned MD, `v3.0/_assets/` with manifests | Author here first; git is SSOT for CI |
| **Mirrored** | Google Drive under Research & Logic (v3.0 + historical siblings), KiRBe / Supabase | Sync from canonical; do not invert authority |
| **Reference-only** | `docs/references/hlk/Research & Logic/` in this repo | Historical packaging; not active vault root |
| **Non-canonical planning** | This folder (`docs/wip/planning/hlk-km-knowledge-base/`), `docs/wip/hlk-km/research-synthesis-*.md` | Traceability and working synthesis until promoted per [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md) |

Full contract: [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md).

---

## Decision log

| ID | Question | Options | Decision |
|----|----------|---------|----------|
| D1 | Where do Output 1 binaries live? | `static/`, per-role folders, `_assets/` root | Single root `v3.0/_assets/<topic_id>/`; pilot uses `v3.0/_assets/km-pilot/` |
| D2 | Trello backlog authority | Trello as SSOT vs registry index | Registry in PMO is canonical **index** only; Trello never SSOT |
| D3 | Manifest validation in release gate | Add to `release-gate.py` vs standalone script | Standalone `scripts/validate_hlk_km_manifests.py`; operators run when touching manifests; full matrix in DEVELOPER_CHECKLIST |
| D4 | Incomplete Trello ids in registry | Fabricate ids vs explicit pending | Use `*pending trello_card_id*` until export refresh |

---

## Verification matrix

Use the **full** repo-standard gate set from [DEVELOPER_CHECKLIST.md](../../../DEVELOPER_CHECKLIST.md), including:

- `py scripts/legacy/verify_openclaw_inventory.py`
- `py scripts/check-drift.py`
- `py scripts/test.py all`
- `py scripts/browser-smoke.py --playwright`
- `py -m pytest tests/test_api.py -v`
- `py scripts/release-gate.py`
- `py scripts/validate_hlk.py` — **required** when canonical compliance CSVs or taxonomy change
- `py scripts/validate_hlk_km_manifests.py` — **required** when adding or editing `v3.0/_assets/**/*.manifest.md`

This plan does not narrow the governed matrix.

---

## Evidence matrix

| Observation | Evidence | Action |
|-------------|----------|--------|
| Drive vs git vault roots were easy to confuse | Operator sync to wrong subtree | Documented in `PRECEDENCE.md` and `v3.0/index.md` (Repository vs Google Drive) |
| External backlog mapping looked second-class | Prior wording | PMO `RESEARCH_BACKLOG_TRELLO_REGISTRY.md` as canonical index + wip planning folder |

---

## Phasing (summary)

| Phase | Exit criteria |
|-------|----------------|
| P0 | KM contract, precedence/index updates, templates, PMO registry, SOP-META alignment, this roadmap |
| P1 | Pilot Output 1 set with manifests + stubs under `_assets/km-pilot/` |
| P2 | Registry rows + 3–5 wip syntheses linked; promotion toward v3.0 per lifecycle |
| P3 | `validate_hlk_km_manifests.py` + checklist documentation |

Reports: [reports/phase-p0-report.md](reports/phase-p0-report.md).  
**Follow-up / re-run (no duplicate effort):** [reports/km-plan-followup-checklist.md](reports/km-plan-followup-checklist.md).
