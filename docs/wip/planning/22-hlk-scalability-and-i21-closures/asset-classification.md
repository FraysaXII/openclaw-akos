# Initiative 22 — Asset Classification

Classification follows [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md) and the new layout convention introduced in P1 of this initiative.

## Canonical (edit-here-first)

| Asset | Path | Owner / Notes |
|:------|:-----|:--------------|
| Forward-layout convention | `docs/references/hlk/compliance/README.md` (P1 — new) | Compliance / Data Architecture; documents `compliance/<plane>/`, `_assets/<plane>/<program_id>/<topic_id>/`, `<role>/programs/<program_id>/` axes |
| `_assets` directory contract | `docs/references/hlk/v3.0/_assets/README.md` (P2 — new) | Compliance; how to add a new program / plane / topic; references `HLK_KM_TOPIC_FACT_SOURCE.md` |
| Mermaid source for ADVOPS topic | `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/topic_external_adviser_handoff.mmd` (P5 — new) | PMO; renders to PNG/SVG via `scripts/render_km_diagrams.py` |
| Topic manifest (re-pathed) | same folder, `topic_external_adviser_handoff.manifest.md` (P2 — moved) | PMO; gains `paths.mermaid` slot, refreshed `file_sha256` |
| Topic companion stub (re-pathed) | same folder, `topic_external_adviser_handoff.md` (P2 — moved) | PMO; updated relative paths |
| KM contract | `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md` (P1 — extended) | Data Architecture; adds `paths.mermaid` slot and the directory convention |
| GOI/POI maintenance SOP | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` (P4 — extended) | Compliance; adds program-onboarding subsection |
| GOI/POI validator | `scripts/validate_goipoi_register.py` (P4 — extended) | DevOps / Compliance; extends `class` enum |
| Program-folder READMEs | `docs/references/hlk/v3.0/Admin/O5-1/{People/Legal,People/Compliance,Operations/PMO}/programs/PRJ-HOL-FOUNDING-2026/README.md` (P3 — new) | Respective role owners |

## New tooling (canonical, deterministic)

| Asset | Path | Notes |
|:------|:-----|:------|
| KM diagram renderer | `scripts/render_km_diagrams.py` (P5 — new) | Reads `.mmd`; renders `.png` + `.svg` via `mmdc` if on PATH else via `mermaid.ink` HTTP API; idempotent |
| WeasyPrint export path | `scripts/export_adviser_handoff.py` (P6 — extended) | Adds Markdown→HTML→PDF via WeasyPrint when available; falls back to existing pandoc message |
| Optional dependencies | `requirements-export.txt` (P6 — new) | `weasyprint`; not installed by default; documented in `CONTRIBUTING.md` |
| PDF smoke profile | `config/verification-profiles.json` (P6 — extended) | New profile `export_adviser_handoff_pdf_smoke` |

## Mirrored / derived (do not hand-edit)

| Asset | Path | Sync direction |
|:------|:-----|:---------------|
| `compliance.goipoi_register_mirror` | Live Supabase (P7 — applied) | `GOI_POI_REGISTER.csv` → MCP `apply_migration` (DDL) + `execute_sql` (DML, service_role) |
| `compliance.adviser_engagement_disciplines_mirror` | Live Supabase (P7 — applied) | Same |
| `compliance.adviser_open_questions_mirror` | Live Supabase (P7 — applied) | Same |
| `compliance.founder_filed_instruments_mirror` | Live Supabase (P7 — applied) | Same |
| Rendered KM artefacts | `topic_external_adviser_handoff.{png,svg}` (P5 — generated) | Source = `.mmd`; do not hand-edit; regenerate with `scripts/render_km_diagrams.py` |

## Reference-only (historical / evidence)

| Asset | Path | Notes |
|:------|:-----|:------|
| Initiative 21 UAT | `docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/reports/uat-adviser-handoff-20260428.md` (P8 — annotated) | Row C updated to "DEFERRED — trigger not met"; cross-links Initiative 22 |
| Re-evaluation trigger template | `docs/wip/planning/22-.../reports/re-eval-trigger.md` (P8 — new) | Empty template until a trigger fires |
| Supabase apply evidence | `docs/wip/planning/22-.../reports/p7-supabase-apply-evidence.md` (P7 — new) | Timestamps, advisor warnings, row counts, source git sha |
| UAT report | `docs/wip/planning/22-.../reports/uat-i22-scalability-and-closure-YYYYMMDD.md` (P10 — new) | PASS/SKIP/N/A per row; closure record |

## Out-of-repo

- Raw transcript audio (`.mp3`, `.m4a`) and unredacted markdown originals — operator-managed Drive per [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) §8.
- Real-name ↔ `ref_id` identity-mapping table — operator-managed.
