---
initiative_id: INIT-OPENCLAW_AKOS-94
language: en
last_review: 2026-06-05
---

# I94 — Evidence matrix

| Phase | Deliverable evidence | Verification gate | Acceptance |
|:---|:---|:---|:---|
| **P0** | Research action (131 sources) + this charter + INITIATIVE/DECISION rows | `validate_research_action.py` PASS; `validate_hlk.py` OVERALL PASS | Operator round-1/2/3 ratifications (D-IH-94-A) |
| **P1** | `AREA_GOVERNANCE_DISCIPLINE.md` v2 + `hlk_area_completeness.py` v2 + validator v2 + `LOGIC_CHANGE_LOG` | `validate_area_completeness.py --matrix` deterministic; Data/Finance critical-at-L3 hold; pytest | Operator doctrine review (D-IH-94-B) |
| **P2** | Updated I93 gap tracker + 5 area plans + Finance F4 + Legal plan with v2 acceptance criteria | `validate_hlk_vault_links` PASS; master-roadmap frontmatter validator PASS | Any-seat executable check |
| **P3** | Operations PMBOK-domain reframe + IntelligenceOps relocation | `validate_hlk.py` PASS post-move | Operator gate (D-IH-94-C) |
| **P4** | People/Compliance methodology consolidation + MKTOPS/TECHOPS/DATAOPS/UX migration | `validate_hlk.py` + `validate_hlk_vault_links` PASS | Operator canonical-CSV/file-move gate |
| **P5** | Entity axis + Envoy rework (research-first: source ledger + synthesis) | `validate_research_action.py` PASS; matrix sees Envoy | Operator gate (D-IH-94-E) |
| **P6** | Legal 8th-area + LegalOps design (research-first: source ledger + synthesis) | `validate_research_action.py` PASS; Legal scored | Operator gate (D-IH-94-D) |
| **P7** | AREA-16 sub-folder=role validator + Finance/Marketing/Tech/Data/Research remediation | new validator self-test PASS; `validate_hlk.py` PASS | Operator per-area gate |
| **P8** | DATA regression report against v2 + Finance re-score | `validate_area_completeness.py --matrix`; inter-wave sweep | Closures hold |
| **P9** | Closure UAT (11-section) + LOGIC_CHANGE_LOG finalize + breakthrough digest | `validate_uat_report.py` PASS; golden path | Operator closure (D-IH-94-CLOSURE) |
