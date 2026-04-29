# Initiative 24 — Asset Classification

## Canonical (edit-here-first)

| Asset | Path | Owner / Notes |
|:------|:-----|:--------------|
| Brand voice charter, archetype, narrative pillars | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_VOICE_FOUNDATION.md` (P0a) | Brand Manager (CMO chain); scaffold until YAML Section 2 filled |
| Brand register matrix (relationship × channel → register) | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_REGISTER_MATRIX.md` (P0a) | Same; same status |
| Brand do/don't | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_DO_DONT.md` (P0a) | Same; same status |
| Methodology SOP (4 layers) | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` (P1) | Brand Manager + PMO joint; cites brand foundation |
| Composer script | `scripts/compose_adviser_message.py` (P4) | DX surface; emits drafts only — never sends |
| Composer tests | `tests/test_compose_adviser_message.py` (P4) | Voice precedence + brand foundation token resolution + multi-format parity + restricted filter |
| `GOI_POI_REGISTER.csv` (extended schema) | `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` (P2) | 3 new optional columns: `voice_register`, `language_preference`, `pronoun_register` |
| `akos/hlk_goipoi_csv.py` (extended FIELDNAMES) | `akos/hlk_goipoi_csv.py` (P2) | Backwards-compatible add |

## New tooling extensions

| Asset | Path | Notes |
|:------|:-----|:------|
| Sync flag | `scripts/sync_compliance_mirrors_from_csv.py --goipoi-register-only` (existing) re-emits with new columns | UPSERT shape updated to include new columns |
| Mirror DDL staging | `scripts/sql/i24_phase1_staging/<ts>_i24_compliance_goipoi_register_mirror_alter_{up,rollback}.sql` (P2) | ALTER + rollback |
| Mirror DDL migration | `supabase/migrations/<ts>_i24_compliance_goipoi_register_mirror_alter.sql` (P2) | Promoted from staging; ledger parity preserved |
| Per-discipline templates | `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/templates/email/*.md` (P3) | **Conventions, not canonical** — no PRECEDENCE row |
| Multi-format export | `scripts/export_adviser_handoff.py --format html|text` (P5) | Adds HTML and plain-text outputs |
| Verify profile | `config/verification-profiles.json` `export_adviser_handoff_html_smoke` (P5) | New |

## Mirrored / derived (do not hand-edit)

| Asset | Path | Sync direction |
|:------|:-----|:---------------|
| `compliance.goipoi_register_mirror` (extended) | Live Supabase | `GOI_POI_REGISTER.csv` → MCP `apply_migration` ALTER (DDL) + `execute_sql` UPDATE (DML, `service_role`) |

## Reference-only (historical / evidence)

| Asset | Path | Notes |
|:------|:-----|:------|
| P2 mirror ALTER evidence | `reports/p2-mirror-alter-evidence.md` | MCP timestamps, advisor warnings, before/after row counts |
| P6 real-email send evidence | `reports/uat-adviser-email-sent-<DATE>.md` | OPERATOR-PENDING — created when G-24-3 fires |
| UAT report | `reports/uat-i24-communication-methodology-<DATE>.md` | PASS/SKIP/N/A per row; closure record |
