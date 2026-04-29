# Initiative 24 — Communication Methodology + Eloquence-Layer Composer

**Folder:** `docs/wip/planning/24-hlk-communication-methodology/`  
**Status:** P0 + P0a-scaffold + P1 in progress (2026-04-29)  
**Authoritative Cursor plan:** `~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md` §"Initiative 24".  
**Bootstrap dependency:** Initiative 22a (`operator-answers-wave2.yaml` Sections 2 + 3 + 5).

## Outcome

Promote operator's lived brand-craft into a governed canonical foundation, then build a 4-layer methodology (brand → concept → use-case → eloquence) and a composer script that fuses all four into per-discipline outbound messages — culminating (operator-gated) in the actual founder-incorporation adviser email.

## Phase plan

| Phase | Purpose | Key deliverable |
|:-----:|:--------|:----------------|
| **P0** | Bootstrap initiative folder + 6 standard artifacts | This roadmap; decision log (D-IH-10/11/17); asset classification; evidence matrix; risk register; reports/ |
| **P0a** | Brand foundation alignment (D-IH-17) | `BRAND_VOICE_FOUNDATION.md` + `BRAND_REGISTER_MATRIX.md` + `BRAND_DO_DONT.md` under `v3.0/Admin/O5-1/Marketing/Brand/`. Scaffold-staged until operator fills YAML Section 2; SOP cites the foundation, never invents. |
| **P1** | 4-layer methodology SOP (G-24-2) | `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`; `process_list.csv` tranche under `thi_mkt_prj_1`. |
| **P2** | GOI/POI mirror DDL ALTER (G-24-1) | Extend `GOI_POI_REGISTER.csv` with `voice_register`, `language_preference`, `pronoun_register`; staging + Supabase migration; MCP `apply_migration`. |
| **P3** | Per-discipline templates (conventions, not canonical) | `templates/email/*.md` shells with brand-foundation token references. |
| **P4** | 4-layer composer script + tests | `scripts/compose_adviser_message.py` + `tests/test_compose_adviser_message.py`. |
| **P5** | Multi-format export | `scripts/export_adviser_handoff.py` `--format html|text`; `export_adviser_handoff_html_smoke` profile. |
| **P6** | **Send real adviser email (G-24-3 IRREVERSIBLE)** | **OPERATOR-GATED — deferred.** Operator finalises pre-flight checklist + drops sign-off in YAML Section 5 + sends. |
| **P7** | Docs/rules sync | ARCHITECTURE/USER_GUIDE/CHANGELOG/CONTRIBUTING; cursor-rules triggers. |
| **P8** | UAT + closure | Verification matrix; dated UAT report; closure note. |

## Operator approval gates

| Gate | Phase | What it covers |
|:----:|:-----:|:---------------|
| **G-24-1** | P2 | `ALTER TABLE compliance.goipoi_register_mirror` (3 nullable columns) via MCP |
| **G-24-2** | P1 | `process_list.csv` named tranche `thi_mkt_dtp_NN` "Communication methodology maintenance" |
| **G-24-3** | P6 | **Real adviser email send (IRREVERSIBLE)** — pre-flight checklist signed; operator finalises + sends |

## Verification matrix

- `py scripts/validate_hlk.py` (each phase touching CSVs)
- `py scripts/validate_goipoi_register.py` (P2 — 3 new optional columns)
- `py scripts/validate_program_id_consistency.py` (any new GOI/POI rows must reference registered programs)
- `py scripts/wave2_backfill.py --section brand_voice --dry-run` (after operator fills Section 2)
- `py scripts/wave2_backfill.py --section goi_poi_voice` (after Section 3 complete)
- `py -m pytest tests/test_compose_adviser_message.py -v` (P4)
- `py scripts/verify.py export_adviser_handoff_smoke` + `_pdf_smoke` + `_html_smoke` (P5)
- MCP `execute_sql` row-count probe for `compliance.goipoi_register_mirror` after ALTER

## Out of scope

- Topic graph extension (Initiative 25).
- Ops hardening (Initiative 26).
- **Sending an automatic email** — composer always emits a draft; operator finalises + sends (G-24-3).
- **Authoring brand voice from scratch** (D-IH-17 — we cite operator's lived protocols, not invent).

## Cross-references

- [decision-log.md](decision-log.md)
- [asset-classification.md](asset-classification.md)
- [evidence-matrix.md](evidence-matrix.md)
- [risk-register.md](risk-register.md)
- Initiative 23 (program registry — KIR + FOUNDING used as composer recipients): [`23-hlk-program-registry-and-program-2/`](../23-hlk-program-registry-and-program-2/master-roadmap.md)
- Initiative 22a wave-2 bootstrap: [`22a-i22-post-closure-followups/`](../22a-i22-post-closure-followups/master-roadmap.md)
