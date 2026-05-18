---
language: en
status: active
canonical: false
classification: way_of_working
intellectual_kind: asset_classification
phase: P0
initiative: INIT-OPENCLAW_AKOS-76
authored: 2026-05-18
last_review: 2026-05-18
role_owner: System Owner
companion_to:
  - master-roadmap.md
ssot: false
---

# I76 — Asset Classification

> Workspace mirror of I76 asset classification per [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md). Required by `akos-planning-traceability.mdc` Governance Content Requirements when an initiative touches HLK compliance assets.

## Classification table

| Asset | Class | Authoritative path | Edit rule | Drift handling |
|:---|:---|:---|:---|:---|
| INITIATIVE_REGISTRY row I76 | canonical | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv` | Edit at canonical path; mirror auto-emits via `compliance_mirror_emit` profile. | If drift detected (mirror disagrees), canonical wins; resync mirror. |
| DECISION_REGISTER rows D-IH-76-A..H + D-IH-76-CLOSURE + D-IH-86-O | canonical | `DECISION_REGISTER.csv` | Edit at canonical path; one row per decision; full rationale in companion `decision-log.md`. | Same as above. |
| OPS_REGISTER rows OPS-76-1..N + OPS-86-6 | canonical | `OPS_REGISTER.csv` | Edit at canonical path. | Same as above. |
| MADEIRA_TOOL_RBAC.csv (P2) | canonical | `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/` | Edit at canonical path; Pydantic model in `akos/hlk_madeira_tool_csv.py` enforces schema; validator at `scripts/validate_madeira_tool_rbac.py`. | Mirror to `compliance.madeira_tool_rbac_mirror` (Supabase) per `akos-holistika-operations.mdc` two-plane model. |
| MADEIRA_AIC_PER_TASK_REGISTRY.csv (P4) | canonical | `docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/dimensions/` | Edit at canonical path; Pydantic model + validator. | Same. |
| MADEIRA_MODE_PARITY.md + MADEIRA_METHODOLOGY_MODE.md (P1) | canonical | `Envoy Tech Lab/canonicals/` | Edit at canonical path; review-stamp dimension applied per I71 P4. | n/a (markdown SSOT; no automated mirror). |
| SOP-TECH_MADEIRA_PERSISTENCE_001.md + SOP-TECH_MADEIRA_PERSONALITY_001.md (P3) | canonical | `Envoy Tech Lab/canonicals/` | Paired SOP+runbook per `akos-executable-process-catalog.mdc` Rule 1. Each SOP cites its runbook path in §"Cross-references"; runbook docstring cites its SOP path. | n/a. |
| SOP-TECH_MADEIRA_AIC_DISPATCH_001.md (P4) | canonical | `Envoy Tech Lab/canonicals/` | Same. | n/a. |
| `scripts/madeira_persistence_check.py` + `scripts/madeira_personality_check.py` + `scripts/madeira_aic_dispatch.py` | canonical | `scripts/` | Paired runbooks per Rule 1. Type hints + structured logging per `CONTRIBUTING.md` Python Code Standards; tests under `tests/test_madeira_*.py`. | n/a (Python SSOT; tested by `scripts/test.py madeira` group). |
| `akos/hlk_madeira_*_csv.py` Pydantic models | canonical | `akos/` | Field tuple matches CSV header exactly per `akos-holistika-operations.mdc` "New git-canonical compliance registers" pattern. | n/a (Python SSOT). |
| `scripts/validate_madeira_*.py` | canonical | `scripts/` | Wired into `validate_hlk.py` + `release-gate.py` + `verification-profiles.json` `pre_commit`. | n/a. |
| `docs/wip/planning/76-madeira-elevation/` (this folder) | planning (authoritative for I76) | This folder | Authoritative per frontmatter `authoritative_plan` field. No out-of-repo Cursor plan companion needed (I76 is small enough to live entirely in repo, mirrors I80 precedent). | n/a (planning files; not mirrored). |
| `docs/wip/planning/_trackers/i11-i13-i17-scope-overlap-tracker.md` | planning (governance-shape artifact) | `_trackers/` | Edit at this file; ratify gates close into per-phase I76 decisions; new pattern minted as governance shape per A0 Option 5 default posture. | n/a (planning; not mirrored). |
| `docs/wip/planning/_blockers/i74-promotion-blocker-tracker.md` (companion mint at this commit) | planning (governance-shape artifact) | `_blockers/` | Edit at this file; conditions resolve via I74 candidate-file gate firing (TRIGGER-2). | n/a. |
| `docs/wip/planning/_blockers/i75-promotion-blocker-tracker.md` (companion mint) | planning | Same | Conditions resolve via I72 P0 + I73 P0 + Research Director hire. | n/a. |
| `docs/wip/planning/_blockers/i83-promotion-blocker-tracker.md` (companion mint) | planning | Same | Conditions resolve via I82 P4 closure. | n/a. |
| MADEIRA-AKOS/STATUS.md | mirrored (status reflection of I76 progress) | `Envoy Tech Lab/MADEIRA-AKOS/STATUS.md` | Update at canonical path when I76 phases close; STATUS.md is reference doc. | If drift detected, update STATUS.md to reflect canonical I76 INITIATIVE_REGISTRY row state. |
| AGENTIC_FRAMEWORK_LANDSCAPE.md | reference (cross-area) | `Envoy Tech Lab/canonicals/` | Tech Lab owns; I76 references but does not edit. | If LandScape adds frameworks, I76 review-stamp in P5 UAT for compatibility. |
| HOLISTIKA_AGENTIC_DOCTRINE.md | reference (People area cross-link) | `People/canonicals/` | People area owns; I76 references but does not edit. Anti-jargon discipline applies to I76 prose per RULE 4. | If People doctrine refines, I76 review-stamp in P5 UAT for alignment. |
| Cursor session transcripts (operator's own MADEIRA sessions) | reference | `agent-transcripts/` | Read-only audit material; consumed by Langfuse + UAT analysis. | n/a. |

## Cross-references

- [`PRECEDENCE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md) — full asset-class taxonomy (canonical / mirrored / reference-only).
- [`akos-holistika-operations.mdc`](../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers (pattern)" — for the MADEIRA_TOOL_RBAC + MADEIRA_AIC_PER_TASK CSVs.
- [`akos-planning-traceability.mdc`](../../../.cursor/rules/akos-planning-traceability.mdc) §"Per-initiative file-changes CSV (mandatory)" — files-modified.csv schema.
- [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 — paired SOP+runbook discipline.
