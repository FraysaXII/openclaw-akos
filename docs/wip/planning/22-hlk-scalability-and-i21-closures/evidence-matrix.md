# Initiative 22 — Evidence Matrix

Tracks the source artifacts behind each phase deliverable so reviewers can audit the provenance of decisions and changes.

## Phase → evidence map

| Phase | Deliverable | Source / evidence |
|:-----:|:-----------|:------------------|
| P0 | Initiative folder bootstrap | This roadmap, decision log (D-IH-1..D-IH-7), asset classification, baseline validator runs (`validate_hlk`, `validate_hlk_vault_links`, `validate_hlk_km_manifests`) |
| P1 | `compliance/README.md` | Initiative-21 outputs (`PRECEDENCE.md` rows 28–31, 51–54), `akos-holistika-operations.mdc` planes table, plan §"Scalability charter" |
| P1 | `PRECEDENCE.md` "Layout convention (forward)" | Same as above + plan §D-IH-1, D-IH-2 |
| P1 | `HLK_KM_TOPIC_FACT_SOURCE.md` `paths.mermaid` slot | `validate_hlk_km_manifests.py` (existing `raster_relative` parser) + plan §D-IH-3 |
| P2 | `_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/` move | Existing `_assets/advops/topic_external_adviser_handoff.{manifest.md,md,png}`; KM manifest validator confirms raster + sha256 still resolve after `git mv` |
| P3 | Program-folder READMEs | Existing `FOUNDER_*` documents under Legal / Compliance / Operations PMO; cross-linked to Initiative-21 SSOT (`ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`, `GOI_POI_REGISTER.csv`) |
| P4 | Extended GOI/POI `class` enum | `akos/hlk_goipoi_csv.py` (header), `validate_goipoi_register.py` (existing enum), plan §D-IH-5 |
| P4 | "Onboarding a new program" SOP subsection | D-CH-8 from Initiative-21 (engagement-keyed registers); current GOI/POI seed rows; plan §D-IH-5 |
| P5 | `topic_external_adviser_handoff.mmd` | Initiative-21 SSOTs (`ADVISER_ENGAGEMENT_DISCIPLINES.csv`, `GOI_POI_REGISTER.csv`, `ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`) and the four `compliance.*_mirror` tables |
| P5 | `scripts/render_km_diagrams.py` | `mmdc` (Mermaid CLI) docs + `mermaid.ink` HTTP API (public); `_p6_make_topic_png.py` (legacy helper, deleted in Initiative 21) for prior-art on PNG byte-emission |
| P5 | Manifest `file_sha256` refresh | New PNG sha256 from rendered output; replaces placeholder hash `93967c33...` |
| P6 | WeasyPrint integration | WeasyPrint pip docs; existing `scripts/export_adviser_handoff.py` Markdown output (`build_markdown`); plan §D-IH-4 |
| P6 | `requirements-export.txt` | Plan §D-IH-4 (opt-in dependency principle) |
| P6 | `export_adviser_handoff_pdf_smoke` profile | Existing `export_adviser_handoff_smoke` profile in `config/verification-profiles.json` |
| P7 | Live Supabase apply | Migrations `supabase/migrations/20260429081{728,734,754,800}_i21_compliance_*.sql` (renamed from `20260428190{000,100,200,300}_*` to match remote ledger after MCP apply); staging `scripts/sql/i21_phase1_staging/*.sql`; user-supabase MCP (`apply_migration`, `execute_sql`, `list_tables`, `get_advisors`) |
| P7 | Seed upsert bundle | `scripts/sync_compliance_mirrors_from_csv.py --output artifacts/sql/i21_compliance_mirror_upsert.sql` (full emit) |
| P7 | Row-count probe | `SELECT count(*) FROM compliance.<table>` against the four mirrors; expected: 6, 6, 12, 1 |
| P8 | Re-eval-trigger template | `SOP-HLK_TRANSCRIPT_REDACTION_001.md` §7; `decision-log.md` D-CH-2 (Initiative 21); plan §D-IH-6 |
| P8 | Initiative-21 UAT row C update | `uat-adviser-handoff-20260428.md` (existing) |
| P9 | Docs sync | `akos-docs-config-sync.mdc` triggers; ARCHITECTURE/USER_GUIDE/CHANGELOG/CONTRIBUTING current state |
| P10 | UAT report | All preceding evidence + final validator outputs |

## Cross-references

- Plan: `~/.cursor/plans/scalable_hlk_hierarchy_plus_i21_closures_5efb0b1a.plan.md`
- Initiative 21 master roadmap: [`21-hlk-adviser-engagement-and-goipoi/master-roadmap.md`](../21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)
- Initiative 21 decision log: [`21-hlk-adviser-engagement-and-goipoi/decision-log.md`](../21-hlk-adviser-engagement-and-goipoi/decision-log.md)
- Cursor rules: [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc), [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc), [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc), [`akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc), [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc)
