# Initiative 24 — Evidence Matrix

## Phase → evidence map

| Phase | Deliverable | Source / evidence |
|:-----:|:-----------|:------------------|
| P0 | Initiative folder bootstrap | This roadmap; decision log (D-IH-10/11/17/24-A); asset classification; risk register; reports/ |
| P0a | Brand foundation MDs (scaffold) | YAML Section 2 schema in `operator-answers-wave2.yaml`; Wave-2 plan §"Backfill discipline" T3 tier |
| P1 | Methodology SOP (4 layers) | Wave-2 plan §"D-IH-10"; existing PMO/Compliance SOP patterns under `v3.0/Admin/O5-1/Operations/PMO/` and `v3.0/Admin/O5-1/People/Compliance/` |
| P1 | process_list.csv tranche | Initiative 21 P3 precedent for adding ADVOPS-related process rows under `thi_mkt_prj_1`; G-24-2 operator approval gate |
| P2 | GOI/POI ALTER + backfill | Initiative 21 P7 precedent (mirror DDL apply via MCP); Initiative 22 P7 ledger-parity rule for migration filename rename |
| P2 | Voice columns enum + defaults | Wave-2 plan §"D-IH-11"; YAML Section 3 (operator-filled defaults for the 6 existing GOI/POI rows) |
| P3 | Per-discipline templates | Wave-2 plan §"P3 — Per-discipline templates"; `BRAND_REGISTER_MATRIX.md` (post-P0a) for the (relationship, channel) lookup |
| P4 | Composer script | Existing `scripts/export_adviser_handoff.py` patterns + `_redact_helper_p2.py` patterns + `akos/hlk_goipoi_csv.py` field contract |
| P4 | Composer tests | Existing `tests/test_*.py` patterns; new tests for voice precedence + brand-foundation token resolution + multi-format parity + `restricted` filter |
| P5 | Multi-format export | Existing `--format md\|pdf` pattern; markdown library + WeasyPrint for HTML; plain-text rendering via stdlib |
| P6 (deferred) | Real adviser email send | Pre-flight checklist (G-24-3); off-repo recipient identity store; operator SMTP path |
| P7 | Docs sync | `akos-docs-config-sync.mdc` triggers for the new files |
| P8 | UAT report | All preceding evidence + final validator outputs |

## Decision evidence

- **D-IH-10** Four layers — brand-craft is pre-existing operator knowledge; methodology layers atop canonical CSVs and per-discipline templates.
- **D-IH-11** Voice columns on GOI/POI — minimal extension; no new CSV; mirror ALTER is non-destructive.
- **D-IH-17** Brand foundation prerequisite — operator's lived protocols are SSOT; agent's role is scaffold + propagation + drift detection.
- **D-IH-24-A** Scaffold-now / content-later — unblocks Initiative 24 P1+P2+P4+P5 from operator-interview gating without inventing brand craft.

## Cross-references

- Plan: `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md`
- Initiative 21 (ADVOPS plane + GOI/POI dimension)
- Initiative 22a (operator-answers YAML + scaffolder)
- Initiative 23 (program registry — composer recipients via FK to PROGRAM_REGISTRY)
- Cursor rules: `akos-adviser-engagement.mdc`, `akos-holistika-operations.mdc`, `akos-docs-config-sync.mdc`
