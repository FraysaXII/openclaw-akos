# UAT — Adviser Engagement plane + GOI/POI dimension (Initiative 21)

**Date**: 2026-04-28  
**Operator owner**: Founder (Holistika) / PMO  
**Scope**: All phases P0–P9 of [`master-roadmap.md`](../master-roadmap.md).

---

## 1. Operator approval gates (process_list / baseline tranches)

Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc), each new `process_list.csv` row tranche requires explicit operator approval before the corresponding v3.0 SOPs land (SOP-META order). The decision log in [`decision-log.md`](../decision-log.md) (D-CH-1..D-CH-8) plus initiative roadmap constitute the approval record:

| Tranche | Rows added | Owner | Approval evidence | Status |
|:--------|:-----------|:------|:------------------|:-------|
| **P1 — GOI/POI maintenance** | `hol_peopl_dtp_303` | Compliance | `decision-log.md` D-CH-3, D-CH-6, D-CH-7; SOP `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001` | **APPROVED** |
| **P2 — Transcript redaction** | `hol_peopl_dtp_304` | Compliance | `decision-log.md` D-CH-2; SOP `SOP-HLK_TRANSCRIPT_REDACTION_001`; report [`p2-redaction-diff.md`](p2-redaction-diff.md) | **APPROVED** |
| **P3 — ADVOPS workstream + disciplines** | `hol_opera_ws_5`, `hol_opera_dtp_311` | PMO | `decision-log.md` D-CH-1, D-CH-8; SOP `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001`; cursor rule `akos-adviser-engagement.mdc` | **APPROVED** |
| **P4 — Adviser open questions register maintenance** | `hol_opera_dtp_312` | PMO/Legal | `decision-log.md` D-CH-4, D-CH-6; SSOT cutover documented in PRECEDENCE row | **APPROVED** |
| **P5 — Filed instruments register maintenance** | `thi_legal_dtp_304` | Legal Counsel | `decision-log.md` D-CH-5, D-CH-6; SSOT cutover documented in PRECEDENCE row | **APPROVED** |
| **Baseline org changes** | _none_ | — | No new role added; existing `role_name` values reused for `role_owner` / `canonical_role` / `primary_owner_role` | **N/A** |

> **Note** — All five `process_list.csv` row tranches were **merged in the same execution branch** before the corresponding v3.0 SOPs / vault MD updates referenced their `item_id`s, complying with the SOP-META invariant.

---

## 2. Verification matrix

Run on host: `Windows 10.0.26200`, `python3.14t.exe`, repo HEAD `71eb3985c58492dcea5dd8524493ab912b386a1f`.

| # | Gate | Command | Result | Notes |
|:--|:-----|:--------|:-------|:------|
| 1 | HLK canonical vault | `py scripts/validate_hlk.py` | **PASS** (OVERALL: PASS) | All 7 sub-validators (org, processes, GOI/POI, disciplines, questions, instruments, FINOPS, components) pass |
| 2 | Vault links | `py scripts/validate_hlk_vault_links.py` | **PASS** | No broken internal `.md` links |
| 3 | KM manifests | `py scripts/validate_hlk_km_manifests.py` | **PASS** | New manifest `topic_external_adviser_handoff.manifest.md` validated alongside existing 8 km-pilot manifests |
| 4 | GOI/POI standalone | `py scripts/validate_goipoi_register.py` | **PASS** | 6 rows |
| 5 | Disciplines standalone | `py scripts/validate_adviser_disciplines.py` | **PASS** | 6 rows |
| 6 | Open questions standalone | `py scripts/validate_adviser_questions.py` | **PASS** | 12 rows (Q-LEG-001..009 + Q-FIS-001..003) |
| 7 | Filed instruments standalone | `py scripts/validate_founder_filed_instruments.py` | **PASS** | 1 row (`INST-LEG-ESCRITURA-DRAFT-2026`) |
| 8 | Mirror count preflight | `py scripts/sync_compliance_mirrors_from_csv.py --count-only` | **PASS** | `process_list_rows=1091`, `goipoi_register_rows=6`, `adviser_engagement_disciplines_rows=6`, `adviser_open_questions_rows=12`, `founder_filed_instruments_rows=1` |
| 9 | Compliance mirror emit profile | `py scripts/verify.py compliance_mirror_emit` | **PASS** | Writes `artifacts/sql/compliance_mirror_upsert.sql` (operator review before DB apply) |
| 10 | Adviser handoff smoke | `py scripts/verify.py export_adviser_handoff_smoke` | **PASS** | Writes `artifacts/exports/handoff-smoke.md` (8543 bytes) |
| 11 | Export MD (single discipline) | `py scripts/export_adviser_handoff.py --discipline legal --format md --out artifacts/exports/legal-handoff-2026-04-28.md` | **PASS** | Renders cover, sharing legend, fact pattern, instruments, questions, exhibits |
| 12 | `process_list.csv` header | `py scripts/check_process_list_header.py` | **PASS** | 21 columns (matches `PROCESS_LIST_FIELDNAMES`) |
| 13 | Sync compliance mirrors smoke tests | `py -m pytest tests/test_sync_compliance_mirrors_from_csv.py -v` | **PASS** | 4 tests (count-only assertion updated to 1091 + new register row counts) |
| 14 | Release gate | `py scripts/release-gate.py` | **SOFT FAIL — pre-existing only** | Initiative 21 lanes (HLK, header, vault links, drift, browser, API, inventory) all PASS. Failures are **pre-existing** in `tests/validate_configs.py` (`sandbox.mode` literal `'all'` vs legacy `'strict'`, unrelated to Initiative 21 — see CHANGELOG entry "Terminology — ShadowGPU vs ShadowPC (2026-04-24)") |

### Manual review items

| Item | Result | Notes |
|:-----|:-------|:------|
| Redacted transcripts contain no raw private names or personal paths | **PASS** | Per [`p2-redaction-diff.md`](p2-redaction-diff.md); residual binary masquerading file `2026-04-06 - Pre-Kick-Off - Constitución Sociedad - Fiscal.m4a.md` flagged in SOP and skipped by redactor |
| Sample exported handoff (MD) reviewed for correctness | **PASS** | `artifacts/exports/handoff-smoke.md` shows 6 disciplines, 6 GOI/POI rows, 1 filed instrument, 12 open questions across LEG/FIS, exhibits resolve to existing files |
| Cursor rule `akos-adviser-engagement.mdc` applies to ADVOPS globs | **PASS** | Verified by `globs:` matching `docs/references/hlk/compliance/ADVISER_*.csv`, `docs/references/hlk/compliance/GOI_POI_REGISTER.csv`, plane SOP, router, and export script |

### SKIP / N/A

| Item | Reason |
|:-----|:-------|
| Live Supabase mirror DDL apply | **CLOSED — DONE (Initiative 22 P7, 2026-04-29)** | All four `compliance.*_mirror` tables applied via user-supabase MCP `apply_migration` and seeded via `execute_sql` (`service_role`). Row counts match CSV (6 / 6 / 12 / 1). Migration filenames renamed for ledger parity. Evidence: [`docs/wip/planning/22-.../reports/p7-supabase-apply-evidence.md`](../../22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md). |
| PDF rendering of the handoff bundle | **CLOSED — DONE (Initiative 22 P6, 2026-04-29)** | `--format pdf` now renders via WeasyPrint (preferred) or fpdf2 (pure-Python fallback); `pandoc` remains an external escape hatch. New verify profile `export_adviser_handoff_pdf_smoke`. Optional install: `py -m pip install --only-binary=:all: -r requirements-export.txt`. |
| `git filter-repo` history rewrite | **DEFERRED — trigger not met (Initiative 22 P8, 2026-04-29)** per **D-CH-2** / **D-IH-6**. Re-eval contract: see [`docs/wip/planning/22-.../reports/re-eval-trigger.md`](../../22-hlk-scalability-and-i21-closures/reports/re-eval-trigger.md). Triggers: a `restricted` POI in commit history without a public reference, **or** counsel issuing a privilege-protection demand. Neither has fired; forward-only redaction continues. |

---

## 3. Closure

- All 10 todos in the initiative plan (P0–P9) are **completed**.
- `master-roadmap.md` will receive a **closure note** referencing this report and confirming the cursor-rules checkbox per [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc).
- No new pre-existing test failures attributable to Initiative 21. The two `tests/validate_configs.py` failures pre-date this initiative and track separately under the ShadowGPU/ShadowPC terminology change recorded in the **Changed** section of `CHANGELOG.md` (2026-04-24).

**Recommended follow-ups (not blocking closure):**

1. Apply Initiative 21 mirror DDL on staging Supabase, then run `py scripts/verify.py compliance_mirror_emit` against the live target to seed the four new mirrors.
2. Refresh `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md` stakeholder index to render as a derived view from `GOI_POI_REGISTER.csv` (currently it remains a hand-maintained narrative; SSOT is the CSV).
3. Decide on PDF tooling (pandoc + pdflatex/weasyprint) and add a `--format pdf` smoke step to `verification-profiles.json` once a tooling stack is approved by the operator.
4. Re-evaluate D-CH-2 (filter-repo deferral) when the next batch of transcripts is ingested — confirm none introduce new restricted POIs that are not already public-referenced in current history.
