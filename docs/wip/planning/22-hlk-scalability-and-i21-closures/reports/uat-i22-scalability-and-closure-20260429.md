# UAT — Initiative 22 Scalable HLK hierarchy + i21 closures

**Date**: 2026-04-29  
**Operator owner**: Founder (Holistika) / PMO  
**Scope**: All phases P0–P10 of [`master-roadmap.md`](../master-roadmap.md).  
**Source git sha at apply time**: `71eb3985c58492dcea5dd8524493ab912b386a1f`.

---

## 1. Operator approval gates (per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc))

| Gate | Phase | Description | Approval evidence | Status |
|:----:|:-----:|:-----------|:------------------|:-------|
| **G-1** | P4 | Extended `class` enum in `validate_goipoi_register.py` (read-only forward addition; no existing-row impact) | `decision-log.md` D-IH-5; backwards compatible (existing 6 rows unchanged) | **APPROVED** |
| **G-2** | P7 | Live Supabase DDL apply via MCP `apply_migration` (parity with files in `supabase/migrations/`) | `decision-log.md` D-IH-7; evidence `reports/p7-supabase-apply-evidence.md`; remote `schema_migrations` ledger updated | **APPROVED** |
| **G-3** | P7 | Seed DML via `service_role` `execute_sql` (deny-`anon`/`authenticated` posture preserved) | Same as above; row counts match CSV (6/6/12/1) | **APPROVED** |
| **G-4** | P6 | Opt-in WeasyPrint/fpdf2 dependency in `requirements-export.txt` (separate file; default install footprint unchanged) | `decision-log.md` D-IH-4; `config/verification-profiles.json` adds `export_adviser_handoff_pdf_smoke` | **APPROVED** |

`baseline_organisation.csv` and `process_list.csv` were **not** modified in this initiative.

---

## 2. Verification matrix

Run on host: `Windows 10.0.26200`, `python3.14t.exe`, repo HEAD `71eb3985c58492dcea5dd8524493ab912b386a1f`.

| # | Gate | Command | Result | Notes |
|:--|:-----|:--------|:-------|:------|
| 1 | HLK canonical vault | `py scripts/validate_hlk.py` | **PASS** (OVERALL: PASS) | All 7 sub-validators pass: org / process / GOI/POI(6) / disciplines(6) / questions(12) / instruments(1) / FINOPS / components(97) |
| 2 | Vault links | `py scripts/validate_hlk_vault_links.py` | **PASS** | No broken internal `.md` links across the relocated `_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/` paths and the new `programs/<program_id>/` subfolder READMEs |
| 3 | KM manifests | `py scripts/validate_hlk_km_manifests.py` | **PASS** | New manifest at `_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/topic_external_adviser_handoff.manifest.md` validated alongside the 8 grandfathered km-pilot manifests; `file_sha256=3302eb9d…` matches the freshly rendered PNG |
| 4 | GOI/POI standalone | `py scripts/validate_goipoi_register.py` | **PASS** | 6 rows; extended `class` enum recognised |
| 5 | Disciplines standalone | `py scripts/validate_adviser_disciplines.py` | **PASS** | 6 rows |
| 6 | Open questions standalone | `py scripts/validate_adviser_questions.py` | **PASS** | 12 rows |
| 7 | Filed instruments standalone | `py scripts/validate_founder_filed_instruments.py` | **PASS** | 1 row |
| 8 | Mirror count preflight | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` | **PASS** | `process_list_rows=1091`, `goipoi_register_rows=6`, `adviser_engagement_disciplines_rows=6`, `adviser_open_questions_rows=12`, `founder_filed_instruments_rows=1` |
| 9 | Compliance mirror emit profile | `py scripts/verify.py compliance_mirror_emit` | **PASS** | Writes `artifacts/sql/compliance_mirror_upsert.sql` (~2.07 MB, includes Initiative-21 register upserts) |
| 10 | Adviser handoff smoke (MD) | `py scripts/verify.py export_adviser_handoff_smoke` | **PASS** | `artifacts/exports/handoff-smoke.md` (8543 bytes) |
| 11 | Adviser handoff smoke (PDF) | `py scripts/verify.py export_adviser_handoff_pdf_smoke` | **PASS** | Renders via fpdf2 fallback (Windows: WeasyPrint native libs absent); `artifacts/exports/handoff-smoke.pdf` ≈ 58 KB |
| 12 | Live Supabase mirror probe | MCP `execute_sql` row-count probe | **PASS** | Live counts: `adviser_engagement_disciplines_mirror=6`, `adviser_open_questions_mirror=12`, `founder_filed_instruments_mirror=1`, `goipoi_register_mirror=6` (parity with CSV) |
| 13 | Mermaid renderer smoke | `py scripts/render_km_diagrams.py docs/.../topic_external_adviser_handoff.mmd --update-manifest` | **PASS** | `mermaid.ink` HTTP fallback path (mmdc not on PATH) wrote PNG (295 743 bytes) + SVG (56 752 bytes); manifest `file_sha256` updated atomically |
| 14 | Migration ledger parity | `list_migrations` MCP probe + local file rename | **PASS** | Remote ledger versions `20260429081{728,734,754,800}` match local filenames after rename (per Initiative 18 D-GTM-DB-5 / `supabase/migrations/README.md` parity rule) |
| 15 | Security advisor | MCP `get_advisors --type security` | **PASS for new mirrors** | No findings reference any of the four new `compliance.*_mirror` tables. Pre-existing INFO-level lints unrelated to this initiative |

### Manual review items

| Item | Result | Notes |
|:-----|:-------|:------|
| `_assets/advopps/` retired; new `_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/` populated | **PASS** | 5 companion files present (`.manifest.md`, `.md`, `.mmd`, `.png`, `.svg`); old folder removed |
| Old placeholder PNG replaced by real Mermaid-rendered diagram | **PASS** | Diagram now shows the SSOT/mirror/plane/dimension/export topology with named GOI/POI rows |
| `programs/<program_id>/README.md` subfolders created under Legal, Compliance, Operations/PMO | **PASS** | Each role-folder root retains existing `FOUNDER_*` / `ENISA_*` files with a back-pointer admonition |
| `compliance/README.md` documents the deprecation alias map for legacy flat files | **PASS** | Used by `PRECEDENCE.md` "Layout convention (forward)" subsection |
| Initiative 21 UAT row C marked "DEFERRED — trigger not met" with re-eval contract | **PASS** | Updated row links to `re-eval-trigger.md` template under this initiative's `reports/` |

### SKIP / N/A

| Item | Reason |
|:-----|:-------|
| Physical relocation of `FINOPS_*`, `COMPONENT_SERVICE_MATRIX.csv`, `process_list.csv`, `baseline_organisation.csv` | **OUT OF SCOPE** per master roadmap §"Out of scope (explicit)" — convention documented in `compliance/README.md`; physical move reserved for a dedicated initiative when blast-radius is acceptable |
| Renaming `FOUNDER_FILED_INSTRUMENTS.csv` → `FILED_INSTRUMENTS.csv` | **DEFERRED** with alias documented in `compliance/README.md` |
| `git filter-repo` history rewrite | **DEFERRED — trigger not met** per D-IH-6; re-eval contract in `re-eval-trigger.md` |
| Pandoc PDF rendering | **OPTIONAL** — fpdf2 is the default Windows path; pandoc remains an external escape hatch |
| `supabase db push` from the operator's CLI | Operator runs `supabase migration list` post-link to confirm parity; ledger is already in sync via the MCP `apply_migration` path |

---

## 3. Closure

- All 11 todos in the initiative plan (P0–P10) are **completed**.
- `master-roadmap.md` will receive a closure note pointing at this report.
- Initiative 21 master roadmap and UAT will be cross-linked: row C ("git filter-repo") moves from "DEFERRED" to "DEFERRED — trigger not met" with a link to `re-eval-trigger.md`; rows for live Supabase apply and PDF rendering both move to **CLOSED — DONE**.
- Cursor-rules hygiene: [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) gains the forward layout convention pointer; [`akos-docs-config-sync.mdc`](../../../../.cursor/rules/akos-docs-config-sync.mdc) lists triggers for `compliance/README.md`, `_assets/README.md`, `programs/<program_id>/README.md`, `scripts/render_km_diagrams.py`, and `requirements-export.txt`. The cursor-rules hygiene checkbox in this UAT is **CONFIRMED**.
- No new pre-existing test failures attributable to Initiative 22. The two `tests/validate_configs.py` failures pre-date Initiative 21 and remain out of scope.

**Recommended follow-ups (not blocking closure):**

1. Run `supabase link --project-ref swrmqpelgoblaquequzb` from the operator's machine and `supabase migration list` to confirm both columns match for all rows (a one-off CLI parity check after the MCP-driven apply).
2. When the FINOPS or TECHOPS planes add a second canonical CSV register, schedule a dedicated initiative to physically relocate `FINOPS_COUNTERPARTY_REGISTER.csv`, `COMPONENT_SERVICE_MATRIX.csv`, `GOI_POI_REGISTER.csv`, and the four ADVOPS CSVs into `compliance/<plane>/` subfolders per the deprecation alias map. Forward additions already use the new layout.
3. Install `mmdc` (`npm i -g @mermaid-js/mermaid-cli`) on operator or CI machines for offline KM diagram rendering. The `mermaid.ink` HTTP fallback works but creates a runtime network dependency for re-renders.
4. Install GTK3 runtime on Windows operator workstations to enable WeasyPrint's higher-fidelity PDF path; fpdf2 will continue to serve as the pure-Python default until then.
5. Re-evaluate D-IH-6 (`git filter-repo`) only when the trigger contract in [`re-eval-trigger.md`](re-eval-trigger.md) actually fires.
