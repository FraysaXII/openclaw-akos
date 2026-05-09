---
phase: P3
phase_name: Ops, process, organization, catalog, SOPs
half: 2 (closure)
initiative: I66
date: 2026-05-09
status: complete
operator_pause: pre-P4
gate_kind: standard_phase_pause
governance: akos-agent-checkpoint-discipline.mdc, akos-governance-remediation.mdc, SOP-META_PROCESS_MGMT_001 §4.2-4.3
supersedes_partially: p3-pause-record-2026-05-08.md (P3 Half 1; canonical-CSV gate cleared)
---

# I66 P3 Half 2 closure — pause record (2026-05-09)

> P3 closure record. The canonical-CSV gate (mandatory pause point #4) was operator-cleared via the 2026-05-08 review of the tranche proposal. Operator decision **D-IH-66-R** rewrote the tranche scope (no `baseline_organisation.csv` touch; sub-marks remain a brand-naming + delivery-mode framework, not org-chart roles). All 16 process rows + 4 project anchors applied; 8 remaining SOPs drafted; all 16 SOPs promoted to `status: active`.

## Summary

P3 closes with the operationalisation of P0+P1+P2 brand canon now mechanically enforced through:

- **20 new rows** in `process_list.csv` (4 project anchors + 16 leaf processes), governed by **16 active SOPs**.
- **0 new rows** in `baseline_organisation.csv` per **D-IH-66-R** (the operator decision that sub-marks are brand-naming + delivery-mode framework, not org-chart roles).
- **`SERVICE_OFFERING_CATALOG.md` canonical** in P1 brand-canon folder operationalising the 6×3 service matrix.
- **`docs/wip/intelligence/`** working space for CORPINT-research artefacts.
- **`BRAND_ARCHITECTURE.md` §8** explicitly encoding the sub-mark accountability decision (sunset criteria documented for when to revisit).

## Mechanical evidence — P3 Half 2 (this commit)

### Files created (8 new SOPs)

| Path | Lines | Status | Maps to process row |
|:---|---:|:---:|:---|
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_REGISTER_MATRIX_REVIEW_001.md` | ~75 | active | B3 |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_JARGON_AUDIT_REVIEW_001.md` | ~100 | active | B4 |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md` | ~95 | active | B15 |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_DRIFT_GATE_OPS_001.md` | ~110 | active | B16 |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_IP_REGISTER_MAINTENANCE_001.md` | ~80 | active | B13 |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_DISCOVERY_QUESTIONNAIRE_001.md` | ~110 | active | B9 |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_PROPOSAL_001.md` | ~135 | active | B10 |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/Engagement/SOP-ENG_ENGAGEMENT_DESIGN_001.md` | ~125 | active | B11 |

Plus a new `Operations/Engagement/` folder (sister to `Operations/IntelligenceOps/` from P3 Half 1).

### Files modified

| Path | Changes |
|:---|:---|
| `docs/references/hlk/compliance/process_list.csv` | **+20 rows** (4 project anchors + 16 leaf processes); row count 1,107 → 1,127. |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ARCHITECTURE.md` | **+§8 "Sub-mark accountability — the org-ownership note"** encoding D-IH-66-R; renumbered §8 Maintenance → §9 Maintenance; §7 SERVICE_OFFERING_CATALOG path corrected to `Marketing/Brand/SERVICE_OFFERING_CATALOG.md` (was: `Operations/PMO/SERVICE_OFFERING_CATALOG.md`). |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/IntelligenceOps/SOP-IO_*.md` (×4) | Frontmatter promoted: `version: 0.1` → `1.0`, `status: draft` → `active`. |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-BRAND_CANON_MAINTENANCE_001.md` + `SOP-BRAND_VOICE_DRIFT_TRIAGE_001.md` | Same promotion. |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Legal/SOP-LEGAL_TRADEMARK_MONITORING_001.md` | Same promotion. |
| `docs/references/hlk/v3.0/Admin/O5-1/People/SOP-PEOPLE_FOUNDER_BIO_001.md` | Same promotion. |
| `CHANGELOG.md` | New `[Unreleased]` entry summarising P3 closure. |

### Files unchanged (intentional)

- **`docs/references/hlk/compliance/baseline_organisation.csv`** — row count remains 66 per D-IH-66-R (no sub-mark Lead rows added).

### Validators (P3 closure self-verification)

| Command | Verdict |
|:---|:---|
| `py scripts/validate_hlk.py` | **PASS** — 20 new rows + referential integrity preserved (every `role_owner` resolves; every `item_parent_1_id` resolves to a project anchor in same tranche) |
| `py scripts/validate_brand_canon_drift.py` | **PASS** — 13 canonicals present + dual-register contract clean |
| `py scripts/validate_brand_baseline_reality_drift.py` | **PASS** — dual-register contract holds; 7 internal tokens checked |
| `py scripts/validate_initiative_registry.py` | **PASS** |
| `py -m pytest tests/test_validate_brand_drift_gates.py` | **27/27 PASS** |

## Documentary evidence — P3 closure

### Decisions encoded in P3

| Decision ID | Encoded in | Status |
|:---|:---|:---|
| **D-IH-66-E** (service catalog operationalisation) | [`SERVICE_OFFERING_CATALOG.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SERVICE_OFFERING_CATALOG.md) (P3 Half 1) + 16 leaf process rows referencing it (P3 Half 2) | **encoded** |
| **D-IH-66-F** (IntelligenceOps SOPs) | 4 IntelligenceOps SOPs at `status: active` + 4 process rows | **encoded** |
| **D-IH-66-G** (Engagement ops SOPs) | 3 Engagement SOPs at `status: active` + 3 process rows | **encoded** |
| **D-IH-66-P** (intelligence working space) | `docs/wip/intelligence/` (P3 Half 1) | **encoded** |
| **D-IH-66-R** (sub-mark accountability — no Engagement Manager / no sub-mark Lead roles) | `BRAND_ARCHITECTURE.md` §8 + 0 baseline rows + adjusted process row owners | **encoded across 3 surfaces** |
| **D-IH-66-S** (founder bio canonical maintenance) | `SOP-PEOPLE_FOUNDER_BIO_001.md` (P3 Half 1, now active) + B14 process row | **encoded** |
| **D-IH-66-T** (P6 governance.brand_template_registry view forward-reference) | `SOP-BRAND_TEMPLATE_REGISTRY_MTNCE_001.md` cites the P6 view | **forward-referenced for P6** |

Cumulative: 17 of the planned 20 D-IH-66-* decisions are now encoded (P0-P3). Remaining for P4-P8: D-IH-66-H/U/V/W (P4 trademark + legal templates), and final-cycle decisions for I67 scaffold (P8).

### SOP-META compliance verification

Per `SOP-META_PROCESS_MGMT_001.md` §4.2-4.3 (CSV before SOP for net-new `item_id`s):

- ✓ `process_list.csv` rows applied **before** SOP frontmatter promoted to `status: active` (within the same commit, but mechanically: CSV apply ran first; SOP promotion ran second).
- ✓ Every promoted SOP has a `process_id:` frontmatter field that resolves to a real `item_id` in `process_list.csv`.
- ✓ Every newly-added `process_list.csv` row's `description` field cites the governing SOP by ID + name.

## Pre-P4 self-checkpoint

### What I have read

- The full I66 master plan (carried over from P0).
- All 13 P1 brand canonicals (carried over from P1+P2).
- All 4 brand drift gates' source code (carried over from P2).
- `process_list.csv` schema + dominant-pattern rows (P3 Half 1 reconnaissance).
- `baseline_organisation.csv` schema + role hierarchy + access-level conventions (P3 Half 1 reconnaissance).
- `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` (P1) — input for P4 trademark filing strategy.

### What I have authored — cumulative I66 P0-P3

- **P0**: 8 governance files + Impeccable v3.1 + 5 sibling-repo bridges.
- **P1**: 5 new + 2 rewritten + 4 cross-ref BRAND canonicals + transcripts working space.
- **P2**: 4 drift validators + 27 tests + 2 new + 2 updated cursor rules.
- **P3 Half 1**: Service catalog + intelligence working space + 8/11 SOPs (4 HUMINT full + 4 brand/legal/people scaffolds) + canonical CSV tranche proposal.
- **P3 Half 2 (this commit)**: 20 process_list rows applied + 8 additional SOPs drafted + 16 SOPs promoted to active + BRAND_ARCHITECTURE §8 sub-mark accountability note.

**Total I66 LOC**: ~9,000 lines of governed Markdown + Python + canonical CSV row writes across 4 phases.

### What is outstanding for P4

P4 (5-6d) — Trademark clearance + legal templates + boilerplate legal-page refresh:

1. **EUIPO + OEPM trademark clearance** for 5 marks per `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`:
   - `Holistika` (umbrella; class 35 + 41 + 42).
   - `Holistika R&S`, `Think Big`, `HLK Tech Lab` (3 sub-marks; class 35 + 42).
   - `MADEIRA`, `KiRBe`, `ENVOY`, `InfraMonitor`, `Financial Analyst` (5 product marks; class 9 + 42).
2. **Filing strategy** — per-mark + per-jurisdiction filing decision tree (file as Madrid Protocol from EUIPO?; file separately in OEPM?; file in additional jurisdictions where Holistika operates?).
3. **Filing prep packets** — per-mark filing string + class scope + goods/services list + conflict-clearance evidence.
4. **Ready-to-sign filing forms** — EUIPO TM-1 template + OEPM equivalent (operator-extension scope per the operator's P4 push-back in the original plan acceptance).
5. **Legal template suite** — MSA / SOW / NDA / DPA templates aligned with Branded House architecture (single legal entity Holistika Research SL contracting; sub-marks named in scope, not as parties).
6. **Privacy / terms / cookies refresh** on `boilerplate/app/privacy/`, `boilerplate/app/terms/`, `boilerplate/app/cookies/` — per the P5 boilerplate rewrite scope, but legal text drafted in P4.
7. **Operator-handoff package** — what counsel needs to file, in what order, with what supporting evidence.

### What I have decided not to do (out of P3 scope)

- **Ship Engagement Manager role row** — DEFERRED per D-IH-66-R; the role is not introduced because the founder is the de facto Engagement Manager at current org size.
- **Ship Copy / AV / Design role rows under Brand Manager** — DEFERRED. The operator flagged in their decision message that the brand manager team has implicit additional roles (Copy, AV, Design); these are likely future I-NN scope when actual hires happen. Not in I66 scope.
- **Auto-populate `process_list.csv` `instructions` column with SOP file paths** — the SOP cross-link is currently in the SOP frontmatter (`process_id:`) and in the `description` field of the process row (cites SOP by ID + name). The `instructions:` column is left empty for now per existing-row convention.

### First three concrete next actions for P4

1. **Read** `BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md` §"frozen filing strings" + §"per-jurisdiction filing matrix" carefully; build a per-mark trademark-clearance worklist.
2. **Conduct** OSINT trademark clearance using EUIPO eSearch + OEPM Sitadex portals; record per-mark clearance status (collision risks, similar marks, opposition history).
3. **Draft** the per-mark filing prep packet (one packet per mark — 5 packets total) under `docs/wip/planning/66-brand-vision-ops-sweep/reports/p4-trademark-filing-prep/<mark-slug>/`.

## Operator approval checklist (pre-P4 entry)

Operator confirms before P4 begins:

1. ☐ All 20 new `process_list.csv` rows + 16 active SOPs read correctly and represent the intended operational doctrine.
2. ☐ The D-IH-66-R decision (no sub-mark Lead rows; sub-marks as brand-naming + delivery-mode framework) is reflected correctly in `BRAND_ARCHITECTURE.md` §8 with appropriate sunset criteria.
3. ☐ The 4 project anchor structure (`tbi_mkt_prj_brand_governance_001`, `hol_res_prj_intelligence_ops_001`, `hol_res_prj_engagement_ops_001`, `hol_lgl_prj_brand_legal_001`) is acceptable; no merging or splitting needed.
4. ☐ The `Operations/IntelligenceOps/` + `Operations/Engagement/` folder structure is the right home for these SOPs (vs. a flatter structure under `Marketing/` or `Research/`).
5. ☐ The 7 deferred items (Engagement Manager role, Copy/AV/Design roles, instructions-column auto-population, etc.) are correctly scoped as out-of-I66.
6. ☐ P4 entry approved (trademark clearance + filing strategy + filing prep packets + ready-to-sign forms + legal templates + boilerplate legal-page refresh — substantial scope).

## Cross-references

- I66 master-roadmap: `docs/wip/planning/66-brand-vision-ops-sweep/master-roadmap.md` §"P3 — Ops, process, organization, catalog, SOPs"
- P0 / P1 / P2 / P3 Half 1 pause records: [p0](p0-pause-record-2026-05-08.md), [p1](p1-pause-record-2026-05-08.md), [p2](p2-pause-record-2026-05-08.md), [p3-h1](p3-pause-record-2026-05-08.md)
- Tranche proposal (P3 Half 1): [`p3-canonical-csv-tranche-proposal-2026-05-08.md`](p3-canonical-csv-tranche-proposal-2026-05-08.md) — historical context; the actual applied tranche differs per D-IH-66-R (no baseline rows; B9-B11 role-owner adjustments).
- Decision log: D-IH-66-E, F, G, P, R, S, T encoded across P3 surfaces.
