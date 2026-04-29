# Changelog

All notable changes to the OpenCLAW-AKOS project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Initiative 25 P3 + P4 + P5 + P6 + P7 + P8 + P9 — Topic graph render, wikilinks, PMO hub auto-gen, ENISA backfill, .mmd-first rule, batch render, closure (2026-04-29)** — **Initiative 25 closed (P0–P9).** Topics are now first-class governed entities. P0+P1+P2+Pgraph landed earlier in [PR #19](https://github.com/FraysaXII/openclaw-akos/pull/19); this PR ships the remaining phases. **P3** — [`scripts/render_topic_graph.py`](scripts/render_topic_graph.py) reads `dimensions/TOPIC_REGISTRY.csv` and emits `_assets/_meta/topic_graph.{mmd,png,svg}` (4 topics clustered into 3 subgraphs by `program_id`; 2 cross-cluster edges); reuses `render_km_diagrams.py` for the PNG/SVG pipeline; idempotent. **P4** — Obsidian wikilink secondary nav adopted in topic companion `.md` (proof in `topic_enisa_evidence.md`); explicitly out-of-scope for `validate_hlk_vault_links.py` per D-IH-12. **P5** — [`scripts/render_pmo_hub.py`](scripts/render_pmo_hub.py) emits the stakeholder index between `<!-- BEGIN_AUTOGEN section_id=pmo_stakeholder_index_v1 ... -->` / `<!-- END_AUTOGEN ... sha256=<hex> -->` markers in [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md); refuse-to-write on missing markers; sha256 drift detection; idempotent; verify profile `render_pmo_hub_smoke`. **P6** (G-25-2) — ENISA backfill ships `topic_enisa_evidence.{mmd,manifest.md,md,png,svg}` under `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/`; row in `TOPIC_REGISTRY.csv`; topic edge `topic_enisa_evidence depends_on topic_external_adviser_handoff` registered in CSV + projected into Neo4j as `:DEPENDS_ON`. **P7** — `.mmd`-first P0 rule extension to [`akos-planning-traceability.mdc`](.cursor/rules/akos-planning-traceability.mdc) per D-IH-13: initiatives producing or modifying a Topic must commit the `.mmd` source-of-truth in P0 alongside `master-roadmap.md`; consume-only initiatives exempt. **P8** — [`scripts/render_km_diagrams.py`](scripts/render_km_diagrams.py) gains `--all` (batch render every `.mmd` under `_assets/`) + `--dry-run` (no writes; prints what would render); `_render_one` extracted as helper; `_discover_mmd_sources` walks the assets root and skips `.git/`; verify profile `render_km_diagrams_batch_smoke`. **P9** — Dated [`reports/uat-i25-topic-graph-20260429.md`](docs/wip/planning/25-hlk-topic-graph-and-km-scalability/reports/uat-i25-topic-graph-20260429.md) with verification matrix (validate_hlk PASS / vault links PASS / km manifests PASS / 29/29 pytest PASS / topic graph render PASS / PMO hub auto-gen PASS / batch render PASS / wikilinks adopted / `.mmd`-first rule applied / ENISA backfill complete); master-roadmap closure note covering all 11 phases; cursor-rules-hygiene checkbox CONFIRMED. New tests at [`tests/test_render_topic_graph.py`](tests/test_render_topic_graph.py) (11 tests), [`tests/test_render_km_diagrams_batch.py`](tests/test_render_km_diagrams_batch.py) (10 tests), [`tests/test_render_pmo_hub.py`](tests/test_render_pmo_hub.py) (8 tests). New verify profiles in [`config/verification-profiles.json`](config/verification-profiles.json): `render_topic_graph_smoke`, `render_km_diagrams_batch_smoke`.

- **Initiative 26 P2 + P3 + P5 — service_role rotation runbook + WeasyPrint GTK3 + I26 closure (2026-04-29)** — **Initiative 26 closed (P0+P1+P2+P3+P5 done; P4 explicitly DEFERRED with persistent trigger contract).** P2 ships [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) §6.1: quarterly cadence (last business day of each quarter; D-IH-26-D), 5-step procedure (dashboard roll → credential-store update → drift-probe smoke → log to I26 decision-log → rollback path), SOC discipline (never log key value, never paste into terminal history). P3 ships [`CONTRIBUTING.md`](CONTRIBUTING.md) §"WeasyPrint GTK3 install (Windows)": GTK3 runtime install + smoke command + transparent fallback to fpdf2 path when GTK3 absent (D-IH-26-C). P4 stays DEFERRED — KIR onboarding closed without surfacing file-naming friction that would trigger the cascade; persistent template at [`reports/re-eval-trigger-compliance-plane-relocation.md`](docs/wip/planning/26-hlk-ops-hardening/reports/re-eval-trigger-compliance-plane-relocation.md) carries the trigger contract. P5 UAT: dated [`reports/uat-i26-ops-hardening-20260429.md`](docs/wip/planning/26-hlk-ops-hardening/reports/uat-i26-ops-hardening-20260429.md) with verification matrix, phase deliverables shipped, operator follow-ups (mmdc install + GTK3 install + first quarterly rotation Q3 2026), cursor-rules-hygiene checkbox CONFIRMED. Master-roadmap closure note covering all in-scope phases. Wave-2 ops-debt fully captured: every deferred decision has a persistent template; every operator runbook lives at the right canonical surface.

- **Initiative 26 P0 + P1 — ops-hardening bootstrap + persistent re-eval-trigger templates + pinned mmdc CI runbook (2026-04-29)** — Bootstraps Initiative 26 with the standard six artifacts at [`docs/wip/planning/26-hlk-ops-hardening/`](docs/wip/planning/26-hlk-ops-hardening/) (master-roadmap, decision-log with D-IH-26-A..E, asset-classification, evidence-matrix, risk-register, reports/). P0 ships **3 persistent re-eval-trigger templates** that capture deferral contracts from Wave-2 decisions: [`re-eval-trigger-finops-techops-second-csv.md`](docs/wip/planning/26-hlk-ops-hardening/reports/re-eval-trigger-finops-techops-second-csv.md) (D-IH-14: FINOPS third use case OR TECHOPS second register), [`re-eval-trigger-compliance-plane-relocation.md`](docs/wip/planning/26-hlk-ops-hardening/reports/re-eval-trigger-compliance-plane-relocation.md) (D-IH-15: program 2 friction OR second CSV in plane), [`re-eval-trigger-graph-mcp-tooling-promotion.md`](docs/wip/planning/26-hlk-ops-hardening/reports/re-eval-trigger-graph-mcp-tooling-promotion.md) (D-IH-18: 5+ UAT sessions showing graph reliance + 30+ days driver stability + 3+ deterministic sync runs). Each template carries trigger conditions, evidence schema, force-action checklist, cursor-rule guardrails. P1 ships the **pinned `mmdc@^11` install runbook** in [`CONTRIBUTING.md`](CONTRIBUTING.md): operator workstation install + Linux CI extras (`libgbm1`, `fonts-liberation`, `fonts-noto-color-emoji`, `--no-sandbox`); rationale documented in D-IH-26-A (non-pinned installs render Mermaid 10 vs 11 differently due to default theme + edge-routing changes) and D-IH-26-B (puppeteer-bundled Chromium silently crashes without the apt extras on Ubuntu CI). P2 (service_role quarterly rotation), P3 (WeasyPrint GTK3 Windows runbook), P4 (conditional `compliance/<plane>/` relocation — DEFERRED per D-IH-26-E), P5 (UAT + closure) follow.

- **Initiative 23 P6 + P7 + P8 — KiRBe onboarding + closure (2026-04-29)** — Closes Initiative 23 (all 9 phases). P6 onboarding ships 6 evidence-based KiRBe role-folder READMEs at `docs/references/hlk/v3.0/Admin/O5-1/{Tech/System Owner,Data/Architecture,Data/Governance,Finance/Business Controller,People,Operations/PMO}/programs/PRJ-HOL-KIR-2026/README.md` (Compliance/Legal/Marketing remain on-demand per the evidence-based table — no KiRBe-specific `process_list.csv` rows for those chains today). One KM topic asset (`docs/references/hlk/v3.0/_assets/techops/PRJ-HOL-KIR-2026/topic_kirbe_billing_plane_routing/`) with `.mmd` source-of-truth + manifest + companion + rendered PNG/SVG (sha256 `779e9f8e616b4e41…`) **proves the layout convention works at N=2 programs** (the success criterion for the Initiative 22 forward layout). [`docs/references/hlk/v3.0/index.md`](docs/references/hlk/v3.0/index.md) §"Program-scoped casework" extended to list both `PRJ-HOL-FOUNDING-2026` (3 folders) and `PRJ-HOL-KIR-2026` (6 folders). G-23-2 satisfied by existing `env_tech_prj_2 KiRBe Platform` row in `process_list.csv`; G-23-3 N/A (no new role required). The `consumes_program_ids` edge `PRJ-HOL-KIR-2026 → PRJ-HOL-FOUNDING-2026` is registered in CSV and projected into Neo4j as `:CONSUMES`. **P4 drift probe surfaced AND fixed real drift**: `compliance.process_list_mirror=1083` vs canonical CSV=1091 (8-row delta — Initiative 21 ADVOPS tranche + Initiative 18/19 finance rows that were never re-seeded after row count changed); all 8 rows re-seeded via MCP `execute_sql` with `service_role`; live mirror now reports 1091 = CSV; `compliance_mirror_drift_probe` now PASSes 8/8. P7 doc sync: [`CONTRIBUTING.md`](CONTRIBUTING.md) gains the drift-probe operator runbook section; [`master-roadmap.md`](docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md) status set to **Closed (2026-04-29)** with closure note covering all 9 phases. P8 UAT: dated [`reports/uat-i23-program-registry-20260429.md`](docs/wip/planning/23-hlk-program-registry-and-program-2/reports/uat-i23-program-registry-20260429.md) with results table, P6 onboarding evidence, operator follow-ups, cursor-rules-hygiene checkbox CONFIRMED. **D-IH-23-B**: product programs use 3-letter `program_code` as the slug (`PRJ-HOL-KIR-2026`, not `PRJ-HOL-KIRBE-2026`); casework programs keep the long form (`PRJ-HOL-FOUNDING-2026`). Verification: `validate_hlk.py` PASS (12 programs / 1091 processes / 65 roles); `validate_hlk_vault_links.py` PASS; `validate_hlk_km_manifests.py` PASS; 37/37 pytest PASS; `compliance_mirror_drift_probe` PASS (8/8 mirrors at parity after the i21/i18 reseed). Initiative 22 stays closed.

- **Initiative 23 P3 + P4 + P5 — cross-asset validator + mirror drift probe + cross-program glossary (2026-04-29)** — Closes the validators / drift / glossary slice of Initiative 23 (Program Registry). New [`scripts/validate_program_id_consistency.py`](scripts/validate_program_id_consistency.py) (P3) scans every `program_id` reference in `GOI_POI_REGISTER.csv` / `ADVISER_OPEN_QUESTIONS.csv` / `FOUNDER_FILED_INSTRUMENTS.csv` / `_assets/<plane>/<program_id>/<topic_id>/` / vault `programs/<program_id>/` folders and asserts each resolves to a row in `dimensions/PROGRAM_REGISTRY.csv`; integrated into [`scripts/validate_hlk.py`](scripts/validate_hlk.py) and SKIPs gracefully when the registry is absent. New [`scripts/probe_compliance_mirror_drift.py`](scripts/probe_compliance_mirror_drift.py) (P4) emits a `UNION ALL` `SELECT` covering all 8 currently-shipped compliance mirrors; operator pastes the JSON result into `artifacts/probes/mirror-drift-<YYYYMMDD>.json`; `--verify` (default) compares live counts against canonical CSV row counts and reports row-by-row PASS/FAIL; SKIPs gracefully when no fresh artifact exists. New verify profile `compliance_mirror_drift_probe` in [`config/verification-profiles.json`](config/verification-profiles.json). New [`docs/reference/glossary-cross-program.md`](docs/reference/glossary-cross-program.md) (P5) — flat lookup for program codes, discipline codes, sensitivity bands, sharing labels, GOI/POI class taxonomy, status enums, voice registers; canonical sources cited per family. [`docs/GLOSSARY.md`](docs/GLOSSARY.md) gains "Program", "Cross-program glossary", and "Drift probe" rows. Tests: [`tests/test_validate_program_id_consistency.py`](tests/test_validate_program_id_consistency.py) (7 tests covering regex, reserved keywords, FK loading, repo PASS/SKIP), [`tests/test_probe_compliance_mirror_drift.py`](tests/test_probe_compliance_mirror_drift.py) (13 tests covering contract coverage, SQL emission, csv_counts, verify PASS/FAIL/SKIP semantics, malformed-payload handling). Source scripts hardened against `relative_to(REPO_ROOT)` failure on tmp paths.

- **Initiative 22a — Post-closure follow-ups + Wave-2 bootstrap (2026-04-29)** — Lands the unblocking artifacts for Wave-2 (Initiatives 23-26) without reopening the closed I22 folder. New folder [`docs/wip/planning/22a-i22-post-closure-followups/`](docs/wip/planning/22a-i22-post-closure-followups/) carries: (a) operator-pasted slots for the `supabase migration list` parity check + pinned `mmdc@^11` install in [`reports/post-closure-followups-20260429.md`](docs/wip/planning/22a-i22-post-closure-followups/reports/post-closure-followups-20260429.md); (b) a documented **DO-NOT-ADD** recommendation for the FINOPS / TECHOPS second-CSV question (re-eval triggers deferred to I26-P0 templates); (c) the **operator-answers YAML** at [`operator-answers-wave2.yaml`](docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml) — single source of all Wave-2 operator decisions across 5 sections (Program Registry × 12 rows pre-filled with derivable values + sentinels for Tier-3 cells; Brand voice foundation; GOI/POI voice profiles × 6; KiRBe duality confirmations; G-24-3 founder sign-off), filled in batched sittings (~5-7h total); (d) the **scaffolder** [`scripts/wave2_backfill.py`](scripts/wave2_backfill.py) with `--check-only` (sentinel scan; always exit 0; informational), `--dry-run` (refuses if target sections carry sentinels), `--section <name>` (process one section), `--allow-pending` (partial pass during operator review); validator-enforced `__OPERATOR_CONFIRM__` sentinels make it structurally impossible to merge a canonical CSV with placeholder cells; (e) verify profile `wave2_backfill_check` in [`config/verification-profiles.json`](config/verification-profiles.json); (f) tests at [`tests/test_wave2_backfill.py`](tests/test_wave2_backfill.py) lock in sentinel detection, section gating, the shipped YAML contract (12 programs, unique `^[A-Z]{3}$` codes), and write-mode refusal semantics. Planning README slot 27 reserved for the deferred `process_list.csv` per-plane re-architecture so Wave-2 (23-26) lands contiguously. Cursor-rules sync row added to [`akos-docs-config-sync.mdc`](.cursor/rules/akos-docs-config-sync.mdc) for the scaffolder + YAML.

- **Initiative 22 — Scalable HLK hierarchy + Initiative 21 closures (2026-04-29)** — Establishes a forward `<plane> × <program_id> × <topic_id>` layout convention so the canonical surfaces stop being coupled to one program. New canonical README at [`docs/references/hlk/compliance/README.md`](docs/references/hlk/compliance/README.md) (deprecation-alias map for legacy flat files); [`PRECEDENCE.md`](docs/references/hlk/compliance/PRECEDENCE.md) gains a "Layout convention (forward)" subsection; [`HLK_KM_TOPIC_FACT_SOURCE.md`](docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md) gains the `paths.mermaid` slot, source-of-truth rule, and `_assets/<plane>/<program_id>/<topic_id>/` directory convention. KM topic relocated under the new layout: `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/` now holds `topic_external_adviser_handoff.{manifest.md,md,mmd,png,svg}` (the placeholder PNG is replaced by a real Mermaid-rendered diagram, 295 KB PNG + 56 KB SVG, sha256 `3302eb9d595442c4…`). New deterministic CLI [`scripts/render_km_diagrams.py`](scripts/render_km_diagrams.py) (mmdc preferred, mermaid.ink HTTP fallback) writes both raster and vector and updates manifest sha256 atomically. Vault role-folders gain a **`programs/<program_id>/README.md`** convention under Legal, Compliance, and Operations/PMO; existing `FOUNDER_*` / `ENISA_*` files at the role-folder root receive a back-pointer admonition (no link breakage). [`v3.0/index.md`](docs/references/hlk/v3.0/index.md) now documents "Program-scoped casework" under the promotion ladder. [`scripts/validate_goipoi_register.py`](scripts/validate_goipoi_register.py) extends the `class` enum to `client`, `partner`, `investor`, `regulator`, `vendor`, `media` for multi-program reuse; [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) gains §4.7 (class taxonomy disambiguation) and §4.8 ("Onboarding a new program"). [`scripts/export_adviser_handoff.py`](scripts/export_adviser_handoff.py) now renders **PDF** via WeasyPrint (best CSS fidelity, requires native Cairo/Pango) → fpdf2 (pure-Python, zero native deps) → pandoc (external) chain; new `requirements-export.txt` opt-in deps; new verification profile `export_adviser_handoff_pdf_smoke` in [`config/verification-profiles.json`](config/verification-profiles.json). Initiative-21 deferred actions closed: live Supabase apply via user-supabase MCP `apply_migration` for the four `compliance.*_mirror` DDL files plus `execute_sql` seed DML (`service_role`); migration filenames renamed to match remote `schema_migrations` ledger (`20260429081{728,734,754,800}_i21_compliance_*.sql`) per the Initiative 18 ledger-parity rule; row counts validated against CSV (6 / 6 / 12 / 1); evidence in [`docs/wip/planning/22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md`](docs/wip/planning/22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md). `git filter-repo` posture re-affirmed as **DEFERRED — trigger not met** with documented re-eval contract in [`docs/wip/planning/22-hlk-scalability-and-i21-closures/reports/re-eval-trigger.md`](docs/wip/planning/22-hlk-scalability-and-i21-closures/reports/re-eval-trigger.md). Initiative folder [`docs/wip/planning/22-hlk-scalability-and-i21-closures/`](docs/wip/planning/22-hlk-scalability-and-i21-closures/) with master roadmap, decision log (D-IH-1..D-IH-7), asset classification, evidence matrix, and reports.

- **Initiative 21 — Adviser Engagement plane + GOI/POI dimension (2026-04-28)** — New ADVOPS plane (External Adviser Engagement) parallel to MKTOPS/FINOPS/OPS/TECHOPS for Legal / Fiscal / IP / Banking / Certification / Notary engagements. Four new canonical CSVs under [`docs/references/hlk/compliance/`](docs/references/hlk/compliance/): **`GOI_POI_REGISTER.csv`** (knowledge dimension for Groups/Persons of Interest with deterministic obfuscation; raw mapping off-repo), **`ADVISER_ENGAGEMENT_DISCIPLINES.csv`** (disciplines lookup), **`ADVISER_OPEN_QUESTIONS.csv`** (graduates `FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md` to SSOT; vault MD becomes derived per-discipline view), **`FOUNDER_FILED_INSTRUMENTS.csv`** (graduates `FOUNDER_FILED_INSTRUMENT_REGISTER.md` to SSOT; vault MD becomes derived per-discipline view). Akos field contracts: `akos/hlk_goipoi_csv.py`, `akos/hlk_adviser_disciplines_csv.py`, `akos/hlk_adviser_questions_csv.py`, `akos/hlk_founder_filed_instruments_csv.py`. Validators: `scripts/validate_goipoi_register.py`, `scripts/validate_adviser_disciplines.py`, `scripts/validate_adviser_questions.py`, `scripts/validate_founder_filed_instruments.py` (all integrated into `scripts/validate_hlk.py`). Mirrors: `compliance.{goipoi_register,adviser_engagement_disciplines,adviser_open_questions,founder_filed_instruments}_mirror` with deny-`anon`/`authenticated` + `service_role` grant; DDL `supabase/migrations/20260429081{728,734,754,800}_i21_compliance_*.sql` (filenames renamed to match remote `schema_migrations` ledger after the Initiative 22 P7 apply via user-supabase MCP) with parity staging in `scripts/sql/i21_phase1_staging/`. `sync_compliance_mirrors_from_csv.py`: flags `--goipoi-register-only`, `--adviser-disciplines-only`, `--adviser-questions-only`, `--founder-filed-instruments-only`; `--count-only` reports new row counts. `PRECEDENCE.md` updated with canonical + mirror rows. New plane SOP [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md), router [`EXTERNAL_ADVISER_ROUTER.md`](docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md), Compliance SOPs [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md), [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md). KM Topic-Fact-Source manifest [`docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/topic_external_adviser_handoff.manifest.md`](docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/adviser_handoff/topic_external_adviser_handoff.manifest.md) + companion stub (relocated under plane × program × topic convention by Initiative 22 P2). Export deliverable [`scripts/export_adviser_handoff.py`](scripts/export_adviser_handoff.py) (Markdown primary, optional PDF via `pandoc`); verification profile **`export_adviser_handoff_smoke`** in [`config/verification-profiles.json`](config/verification-profiles.json). New cursor rule [`akos-adviser-engagement.mdc`](.cursor/rules/akos-adviser-engagement.mdc) wired into [`akos-holistika-operations.mdc`](.cursor/rules/akos-holistika-operations.mdc) planes table. `process_list.csv`: workstream **`hol_opera_ws_5`** + **`hol_opera_dtp_311`**, **`hol_opera_dtp_312`**, **`hol_peopl_dtp_303`**, **`hol_peopl_dtp_304`**, **`thi_legal_dtp_304`** rows. Adviser-call transcripts in `docs/references/hlk/business-intent/delete-legal-transcripts/` redacted forward-only with GOI/POI substitutions; full `git filter-repo` history rewrite deferred per **D-CH-2**. Initiative folder [`docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/`](docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/) with master-roadmap, decision-log (D-CH-1..D-CH-8), asset-classification, evidence-matrix, and reports.

- **Initiative 19 — FINOPS ledger Phase 1 (2026-04-23)** — Schema **`finops`**, table **`finops.registered_fact`** (governed operational facts; `service_role`-only DML); staging **`scripts/sql/i19_phase1_staging/`**; migration **`20260423014326_i19_finops_ledger_phase1.sql`**; **`docs/wip/planning/19-hlk-finops-ledger/`**; **`PRECEDENCE.md`** mirrored row; **`tests/test_i19_finops_sql_bundle.py`**. Initiative 18 migration ledger file renamed to **`20260423014144_i18_finops_counterparty_mirror_cutover.sql`** to match remote `schema_migrations` after Dashboard/MCP apply.

- **Initiative 18 — FINOPS counterparty SSOT + Stripe FDW (2026-04-23)** — Canonical **`docs/references/hlk/compliance/FINOPS_COUNTERPARTY_REGISTER.csv`**; **`akos/hlk_finops_counterparty_csv.py`**; **`scripts/validate_finops_counterparty_register.py`** and **`validate_hlk.py`** hook. Migration **`20260423014144_i18_finops_counterparty_mirror_cutover.sql`** (counterparty mirror, vendor mirror cutover, **`holistika_ops.stripe_customer_link.finops_counterparty_id`**, optional **`stripe_gtm`** privilege hardening); staging **`scripts/sql/i18_phase1_staging/`**. **`sync_compliance_mirrors_from_csv.py`:** **`--finops-counterparty-register-only`**, full emit includes counterparty upserts, **`finops_counterparty_register_rows`** in **`--count-only`**. **`process_list.csv`:** **`FINOPS and counterparty economics`**, **`thi_finan_dtp_303`–`307`**, **`thi_finan_dtp_308`** (Stripe FDW), **`thi_finan_dtp_309`**. Vault **`SOP-HLK_FINOPS_COUNTERPARTY_REGISTER_MAINTENANCE_001.md`**; vendor SOP stubbed. **`PRECEDENCE.md`**, **`sql-proposal-stack-20260417.md`** §7, ERP handoff, **`docs/wip/planning/18-hlk-finops-counterparty-stripe/`**. Removed **`FINOPS_VENDOR_REGISTER.csv`**, **`akos/hlk_finops_vendor_csv.py`**, **`scripts/validate_finops_vendor_register.py`**. Tests: **`tests/test_i18_finops_sql_bundle.py`**.

### Changed

- **Terminology — ShadowGPU vs ShadowPC (2026-04-24)** — First-class docs (`ARCHITECTURE`, `USER_GUIDE` §8.8, `README`, `GLOSSARY`), `gpu-shadow.env.example`, GPU/`openstack_provider` strings, and related planning notes now use **ShadowGPU** for the OpenStack cloud GPU service and **ShadowPC** only for the local machine product. Runtime profile name `gpu-shadow` is unchanged. **`config/openclaw.json.example`:** `agents.defaults.sandbox.mode` is `all` to match the OpenClaw CLI schema (rejects `strict`).

- **ARCHITECTURE** — `tools.exec` / Path B bullet updated for `sandbox.mode: all` (OpenClaw-allowed values).

- **Holistika operations rule (2026-04-23)** — [`.cursor/rules/akos-holistika-operations.mdc`](.cursor/rules/akos-holistika-operations.mdc): **`finops.*`** in scope; FINOPS plane row cites Initiative 19; **Schema responsibilities** bullet for `finops.registered_fact` posture (no FK to compliance mirror; `service_role` writes).

- **Supabase migration ledger parity (2026-04-21)** — Renamed Holistika CLI migration files to match remote `schema_migrations` (`20260418165339`, `20260418183239`, `20260418193915`, `20260420202847`); pre-`db push` gate and rename-vs-repair workflow in [`supabase/migrations/README.md`](supabase/migrations/README.md), [`supabase/README.md`](supabase/README.md), [`docs/DEVELOPER_CHECKLIST.md`](docs/DEVELOPER_CHECKLIST.md), [`operator-sql-gate.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) § Supabase governance, [`docs/reference/DEV_VERIFICATION_REFERENCE.md`](docs/reference/DEV_VERIFICATION_REFERENCE.md), [`docs/guides/understanding_verification.md`](docs/guides/understanding_verification.md), [`master-roadmap.md`](docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md) (phases 3/4/7 + **D-GTM-DB-5**); Initiative 16 [**D-16-7**](docs/wip/planning/16-hlk-finops-vendor-ssot/decision-log.md) cross-ref **D-GTM-DB-5**. Cursor plan `supabase_db_governance_ssot_a48da8e6`: **D-DB-5**, **Migration ledger parity** section, todo `migration-list-parity`.

### Added

- **Cursor rule — Holistika operations (2026-04-23)** — [`.cursor/rules/akos-holistika-operations.mdc`](.cursor/rules/akos-holistika-operations.mdc): **any** Holistika ops plane (MKTOPS/GTM, FINOPS, MAROPS/TECHOPS stewardship vs DDL); two-plane DDL vs compliance mirror DML; [`operator-sql-gate.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md); inventory-before-greenfield for Wrappers/FDW; `compliance` / `holistika_ops` / `kirbe` / FDW; git-canonical register pattern (FINOPS, component matrix, future SSOT CSVs); MCP advisors and PostgREST exposure. **Removed** `.cursor/rules/akos-supabase-holistika-data-plane.mdc` (superseded by this file). [`.cursor/rules/akos-planning-traceability.mdc`](.cursor/rules/akos-planning-traceability.mdc): Cursor plan vs `master-roadmap.md` and **rules hygiene on initiative close**. [`.cursor/rules/akos-docs-config-sync.mdc`](.cursor/rules/akos-docs-config-sync.mdc): sync rows for Cursor rules + `supabase/migrations` + staging SQL. [`.cursor/rules/akos-governance-remediation.mdc`](.cursor/rules/akos-governance-remediation.mdc): Supabase pointer under HLK compliance.

- **Supabase migration SSOT + compliance mirror verify profile (2026-04-21)** — [`supabase/migrations/`](supabase/migrations/) (i14/i16 DDL parity with `scripts/sql/*_staging/`; i16 timestamp `20260420202847`); [`supabase/migrations/README.md`](supabase/migrations/README.md); [`supabase/README.md`](supabase/README.md); profile **`compliance_mirror_emit`** in [`config/verification-profiles.json`](config/verification-profiles.json) (`py scripts/verify.py compliance_mirror_emit` → `artifacts/sql/compliance_mirror_upsert.sql`); [`artifacts/sql/README.md`](artifacts/sql/README.md); `.gitignore` `artifacts/sql/*.sql`; [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) § Supabase schema and compliance mirror governance; [`docs/DEVELOPER_CHECKLIST.md`](docs/DEVELOPER_CHECKLIST.md); [`docs/reference/DEV_VERIFICATION_REFERENCE.md`](docs/reference/DEV_VERIFICATION_REFERENCE.md); [`docs/guides/understanding_verification.md`](docs/guides/understanding_verification.md); [`CONTRIBUTING.md`](CONTRIBUTING.md); [`operator-sql-gate.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md); decision-log [**D-GTM-DB-1…4**](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md), [**D-16-7**](docs/wip/planning/16-hlk-finops-vendor-ssot/decision-log.md); [`master-roadmap.md`](docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md) plan alignment table.

- **Initiative 17 — Madeira Cursor mode parity (2026-04-21)** — `madeiraInteractionMode` (`ask` \| `plan_draft`) on `AkosState`; `akos/madeira_interaction.py`; `GET`/`POST` `/agents/madeira/interaction-mode` and `GET` `/madeira/control`; `OVERLAY_MADEIRA_PLAN_DRAFT.md` plus Orchestrator/Architect handoff overlays in `config/model-tiers.json`; JSON Schema `config/schemas/madeira-plan-handoff.schema.json`; bootstrap / `switch-model` / `sync-runtime` redeploy Madeira SOUL after global variant; log-watcher + Langfuse metadata for `madeira_interaction_mode`, `read_file_repeated`, plan banner flag; `docs/wip/planning/17-madeira-cursor-mode-parity/`; `tests/test_madeira_interaction.py`; `static/madeira_control.html`.

- **Initiative 16 — FINOPS vendor SSOT (2026-04-20)** — Canonical **`docs/references/hlk/compliance/FINOPS_VENDOR_REGISTER.csv`**; **`akos/hlk_finops_vendor_csv.py`**; **`scripts/validate_finops_vendor_register.py`** and **`validate_hlk.py`** hook. Staging DDL **`scripts/sql/i16_phase3_staging/`** for **`compliance.finops_vendor_register_mirror`** (RLS deny `anon`/`authenticated`, `service_role` grant). **`sync_compliance_mirrors_from_csv.py`:** **`--finops-vendor-register-only`** and **`finops_vendor_register_rows`** in **`--count-only`**. **`process_list.csv`:** **`thi_finan_ws_4`**, **`thi_finan_dtp_303`–`307`**. Vault **`SOP-HLK_FINOPS_VENDOR_REGISTER_MAINTENANCE_001.md`** (Finance / Business Controller). **`PRECEDENCE.md`** canonical + mirrored rows; **`sql-proposal-stack-20260417.md`** §7. WIP **`docs/wip/planning/16-hlk-finops-vendor-ssot/`** (decision log, evidence matrix, execution report, ERP handoff). Initiative 15 **D-15-6** + component matrix SOP **§A.3** (libraries SSOT: repo default, matrix exceptions only). **`docs/wip/planning/README.md`** row **16**.

- **HLK API lifecycle and component matrix (2026-04-20)** — Canonical **`docs/references/hlk/compliance/COMPONENT_SERVICE_MATRIX.csv`** (97 rows seeded from legacy Matriz *components* sheet via `scripts/ingest_matriz_componentes_to_matrix.py`); **`akos/hlk_component_service_csv.py`** (`COMPONENT_SERVICE_FIELDNAMES`); **`scripts/validate_component_service_matrix.py`** and integration into **`scripts/validate_hlk.py`**. **`process_list.csv`:** workstream **`env_tech_ws_api_1`**, processes/tasks **`env_tech_dtp_306`–`309`**, **`311`–`313`**, plus instruction cross-links on **`env_tech_dtp_292`**, **`293`**, **`244`**; **IT Catalog** **`env_tech_dtp_156`** description update. Vault SOPs under **`docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/`**: **`SOP-HLK_API_LIFECYCLE_MANAGEMENT_001.md`**, **`SOP-HLK_COMPONENT_SERVICE_MATRIX_MAINTENANCE_001.md`**, and v0.1 anchors **`SOP-MCP_SERVER_DEFINITION.md`**, **`SOP-ENVOYLAB_REFACTOR_ARCHITECTURE_001.md`**, showcase stubs, **`SOP-DYNAMIC_DOCUMENT_REDACTION_001.md`**. **`REPOSITORIES_REGISTRY.md`:** columns **`api_spec_pointer`**, **`api_topic_id`**. **`PRECEDENCE.md`** row for the matrix. Initiative **`docs/wip/planning/15-hlk-api-lifecycle-governance/`** (decision log, execution report, process-tree mermaid). **`requirements.txt`:** **`openpyxl`** for spreadsheet ingest. Removed repo-root **`Matriz componentes.xlsx`** after extraction (original retained by operators off-repo).

### Documentation

- **Initiative 14 — contact CAPTCHA (Turnstile) Phase A + B (2026-04-19)** — [`contact-lead-ingest-spec.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md): `session_metadata` audit + nullable `captcha_provider` / `captcha_verified_at`; [D-GTM-CONTACT-CAPTCHA](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md). DDL [`20260419_holistika_ops_lead_intake_captcha_columns_up.sql`](scripts/sql/i14_phase3_staging/20260419_holistika_ops_lead_intake_captcha_columns_up.sql) + rollback; web handoff [`contact-api-implementation.md`](docs/web/holistika-research-nextjs/contact-api-implementation.md), [`TEAM_SOTA_HLK_WEB.md`](docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md) §3/§6.5.

- **Initiative 14 — contact lead ingest (2026-04-18)** — [`contact-lead-ingest-spec.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/contact-lead-ingest-spec.md); [`scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql`](scripts/sql/i14_phase3_staging/20260418_holistika_ops_lead_intake_up.sql) + rollback; [D-GTM-CONTACT-INGEST](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md). **Frontend team:** copy-paste source and env instructions live under [`docs/web/holistika-research-nextjs/`](docs/web/holistika-research-nextjs/README.md) (`contact-api-implementation.md`, `TEAM_SOTA_HLK_WEB.md`), not in Initiative `reports/`. [`evidence-matrix.md`](docs/wip/planning/14-holistika-internal-gtm-mops/evidence-matrix.md); [`crm-minimum-fields-supabase.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/crm-minimum-fields-supabase.md) pointer.

- **Docs — public web handoff split from Initiative 14 (2026-04-18)** — Holistika Research Next.js instructions moved to [`docs/web/holistika-research-nextjs/`](docs/web/holistika-research-nextjs/README.md). [`reports/TEAM_SOTA_HLK_WEB.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_HLK_WEB.md) is a short pointer only; process specs stay under `docs/wip/planning/14-holistika-internal-gtm-mops/reports/`.

- **Initiative 14 — prod DDL + team handoff (2026-04-18)** — [D-GTM-3-1](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md) marked done; [`supabase-stripe-health-check-20260418.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/supabase-stripe-health-check-20260418.md) **Supabase MCP** row counts + Edge Function version; **Stripe MCP** account id + documented webhook-list limitation. [D-GTM-C3-ORDER](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md): weekly forums (C3) after contact UAT (D1). UAT: [`uat-holistika-contact-funnel-20260417.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/uat-holistika-contact-funnel-20260417.md) E2E journeys A/B + MCP evidence. Web team: [`docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md`](docs/web/holistika-research-nextjs/TEAM_SOTA_HLK_WEB.md) **ProjectIntakeForm** §5.4 table + `gtm-data-layer` header. [`evidence-matrix.md`](docs/wip/planning/14-holistika-internal-gtm-mops/evidence-matrix.md) and [`reports/README.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/README.md) updated.

- **Initiative 14 — unified plan (2026-04-18)** — Reference docs [`strategic-gtm-narrative-reference.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/strategic-gtm-narrative-reference.md) and [`event-attribution-blueprint-reference.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/event-attribution-blueprint-reference.md); charter decisions [D-GTM-0-1](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md) / [D-GTM-0-2](docs/wip/planning/14-holistika-internal-gtm-mops/decision-log.md); process inventory §3a (research themes); [`EXECUTION-BACKLOG.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/EXECUTION-BACKLOG.md) **Wave E**; [`master-roadmap.md`](docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md) snapshot 2026-04-18. [`supabase/functions/stripe-webhook-handler/README.md`](supabase/functions/stripe-webhook-handler/README.md): optional marketing metadata for attribution. **Holistika Research Next.js site** (separate clone: `root_cd/boilerplate`): `lib/gtm-data-layer.ts` and `ProjectIntakeForm` dataLayer + `event_id` for GTM/Meta dedupe (Wave E1).

- **Initiative 14 — Waves C–D (GTM)** — [`docs/wip/planning/14-holistika-internal-gtm-mops/reports/wave-c-d-roundup-20260417.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/wave-c-d-roundup-20260417.md): SLA **D-GTM-C1** (4 business hours), CRM mapping [`crm-minimum-fields-supabase.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/crm-minimum-fields-supabase.md), weekly metrics log template, [`gtm-sop-vault-index.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/gtm-sop-vault-index.md); UAT stub URLs ([`uat-holistika-contact-funnel-20260417.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/uat-holistika-contact-funnel-20260417.md)); [`EXECUTION-BACKLOG.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/EXECUTION-BACKLOG.md) status updates. **C3 / D1** remain pending until PMO forums and live UAT.

- **`supabase/functions/stripe-webhook-handler/README.md`** — Operator section **How to set `hlk_billing_plane`**; post-secrets checklist; [`stripe_set_billing_plane.py`](scripts/stripe_set_billing_plane.py).

### Changed

- **`supabase/functions/stripe-webhook-handler`** — **`hlk_billing_plane` only** (removed `akos_billing_plane`). Subscription lifecycle: **inherits from Customer** when unset on subscription (`subscription_plane_source` in logs). **GTM / marketing ops** events: `invoice.*`, `checkout.session.completed`, `payment_intent.*`, `charge.*`, `billing_portal.session.created`; structured JSON logs (`source: stripe_webhook`); Holistika upsert when plane matches. README: GTM framing, exact Dashboard event name list.

### Added

- **`scripts/stripe_set_billing_plane.py`** — Set Stripe `metadata.hlk_billing_plane` on Customer or Subscription (`STRIPE_SECRET_KEY` in env).
- **`package.json` + local Supabase CLI** — `npm install` adds the **Supabase CLI** (devDependency); use `npm run supabase -- …` on Windows because `pip install supabase` is the Python client only. Documented in [`supabase/functions/stripe-webhook-handler/README.md`](supabase/functions/stripe-webhook-handler/README.md).

- **Initiative 14 — Wave B (staging DDL + Stripe routing, repo artifacts)** — [`scripts/sql/i14_phase3_staging/`](scripts/sql/i14_phase3_staging/README.md): `20260417_i14_phase3_up.sql`, rollback, `verify_staging.sql`, optional legacy-public deprecation template; [`scripts/verify_phase3_mirror_schema.py`](scripts/verify_phase3_mirror_schema.py); [`supabase/functions/stripe-webhook-handler/`](supabase/functions/stripe-webhook-handler/README.md) (two billing planes: `kirbe` vs `holistika_ops`). Round-up: [`docs/wip/planning/14-holistika-internal-gtm-mops/reports/wave-b-roundup-20260417.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/wave-b-roundup-20260417.md). Live Supabase/Stripe execution remains operator-gated.

- **`scripts/sync_compliance_mirrors_from_csv.py`** — Initiative 14 Wave A3: generates PostgreSQL upsert statements for `compliance.process_list_mirror` and `compliance.baseline_organisation_mirror` from canonical CSVs (`--count-only`, `--output`); [`tests/test_sync_compliance_mirrors_from_csv.py`](tests/test_sync_compliance_mirrors_from_csv.py). Documented in [`sql-proposal-stack-20260417.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md), [`EXECUTION-BACKLOG.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/EXECUTION-BACKLOG.md), [`docs/DEVELOPER_CHECKLIST.md`](docs/DEVELOPER_CHECKLIST.md) §7d.

- **Initiative 14 — status snapshot in master-roadmap** — [`docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md`](docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md) includes § **Initiative 14 — status snapshot (2026-04-17)** (completed deliverables, governance insights, continuation via EXECUTION-BACKLOG); authoritative spec pointer updated to git [`reference/internal_gtm_marketing_ops_574ae9de.plan.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reference/internal_gtm_marketing_ops_574ae9de.plan.md).

- **Initiative 14 — Cursor plan sync** — Git mirror [`docs/wip/planning/14-holistika-internal-gtm-mops/reference/internal_gtm_marketing_ops_574ae9de.plan.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reference/internal_gtm_marketing_ops_574ae9de.plan.md) (2026-04-17 snapshot: status section, YAML todos, DDL authority pointer, Phase 1 merge script correction); [`reference/README.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reference/README.md) updated.

- **Initiative 14 — execution-grade follow-up (2026-04-17)** — [`reports/sql-proposal-stack-20260417.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/sql-proposal-stack-20260417.md): concrete PostgreSQL DDL for `compliance.*` mirrors and `holistika_ops` stub, RLS/grants, verification queries, rollback; [`reports/EXECUTION-BACKLOG.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/EXECUTION-BACKLOG.md); [`reports/process-list-gtm-inventory-and-next-tranches.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/process-list-gtm-inventory-and-next-tranches.md). GTM SOPs gain **Execution runbook** sections and corrected `hlk/compliance` relative links.

- **Initiative 14 — Holistika internal GTM / marketing ops** — [`docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md`](docs/wip/planning/14-holistika-internal-gtm-mops/master-roadmap.md): phase dependency + mermaid + governance reports; **three** new `process_list.csv` rows (`holistika_gtm_dtp_001`–`003`) via [`scripts/merge_process_list_tranche.py`](scripts/merge_process_list_tranche.py); five v3.0 SOPs under `docs/references/hlk/v3.0/Admin/O5-1/` (Growth, Brand/Copywriter, PMO); standalone [`reports/TEAM_SOTA_HLK_ERP.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_HLK_ERP.md) and [`reports/TEAM_SOTA_KIRBE.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/TEAM_SOTA_KIRBE.md); [`tests/test_merge_process_list_tranche.py`](tests/test_merge_process_list_tranche.py). Planning index: [`docs/wip/planning/README.md`](docs/wip/planning/README.md).

- **Initiative 13 — MADEIRA research follow-through** — [`docs/wip/planning/13-madeira-research-followthrough/master-roadmap.md`](docs/wip/planning/13-madeira-research-followthrough/master-roadmap.md): intent exemplar expansion for acronym-heavy HLK phrasing (`config/intent-exemplars.json`); golden routing corpus [`tests/fixtures/intent_golden.json`](tests/fixtures/intent_golden.json) + [`tests/test_intent_golden.py`](tests/test_intent_golden.py); [`scripts/intent_benchmark.py`](scripts/intent_benchmark.py); clearer escalation `operator_message` strings (`akos/intent.py`) and Madeira **AKOS operator paths** (Path 1–4) + acronym disambiguation + dashboard handoff language (`prompts/base/MADEIRA_BASE.md`, `prompts/overlays/OVERLAY_MADEIRA_OPS.md`, `prompts/MADEIRA_PROMPT.md`); [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) §5.2; [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) prompt-tiering cross-link; reports under [`docs/wip/planning/13-madeira-research-followthrough/reports/`](docs/wip/planning/13-madeira-research-followthrough/reports/) (intent benchmark, doc-accuracy, UAT stub). Planning index: [`docs/wip/planning/README.md`](docs/wip/planning/README.md). **`OVERLAY_MADEIRA_OPS.md` tightened** so standard/full Madeira assembled prompts stay ≤ `bootstrapMaxChars` (20 000) and `assemble-prompts.py` exits 0.

### Documentation

- **Cursor rules — planning / HLK sync** — [`.cursor/rules/akos-docs-config-sync.mdc`](.cursor/rules/akos-docs-config-sync.mdc), [`.cursor/rules/akos-governance-remediation.mdc`](.cursor/rules/akos-governance-remediation.mdc), [`.cursor/rules/akos-planning-traceability.mdc`](.cursor/rules/akos-planning-traceability.mdc): initiative `master-roadmap.md` and `docs/wip/planning/README.md` sync contracts; SOP-META CSV-before-SOP order and baseline tranche gates; `master-roadmap.md` contents (dependency narrative, mermaid, phase-at-a-glance); per-tranche CSV operator approval; mermaid ID hygiene. Index note: [`docs/wip/planning/99-proposals/cursor-rules-planning-sync-patch-20260417.md`](docs/wip/planning/99-proposals/cursor-rules-planning-sync-patch-20260417.md).

- **Planning — Initiative 12** — [`docs/wip/planning/12-madeira-research-request/research-request-madeira.md`](docs/wip/planning/12-madeira-research-request/research-request-madeira.md): external research-team request (use cases, technology, frameworks, user journeys) plus Holistika/HLK governance context; [`master-roadmap.md`](docs/wip/planning/12-madeira-research-request/master-roadmap.md); index row in [`docs/wip/planning/README.md`](docs/wip/planning/README.md). **Updates:** system-of-record table with self-contained summaries per artefact; **HLK Operator Model** subsection with Paths 1–4 (inquiry → vault operator workflow → swarm coordination → optional ops prose) so the handoff is not truncated at a §24 reference.

- **Planning — Initiative 12 (vendor triage)** — [`docs/wip/planning/12-madeira-research-request/reports/research-vendor-deliverables-triage.md`](docs/wip/planning/12-madeira-research-request/reports/research-vendor-deliverables-triage.md): governed triage of vendor research markdown (evidence rubric; disambiguation of operator Paths 1–4 vs Holistika methodology “pillars”; UAT cross-check vs Initiative 11; testable UX hypotheses; pointers to SECURITY section 8a and Initiative 11 roadmap). **Section 8** addendum: classified top findings (observed vs desk), resolvable footnotes, Initiative 11 UAT accuracy (S1–S3 PASS (spec), S4 PASS (automated)); **section 8.1** maintenance contract; **commissioning handoff** prioritisation table (F5–F8 / F1–F3 / F4 / F9–F10). [`master-roadmap.md`](docs/wip/planning/12-madeira-research-request/master-roadmap.md): decision **D-RR-3** (section 8 addendum locus); follow-on initiatives must use full [`docs/DEVELOPER_CHECKLIST.md`](docs/DEVELOPER_CHECKLIST.md) gate set and **`.cursor/rules/akos-planning-traceability.mdc`** UAT contract when qualitative sign-off is in scope.


### Changed

- **Initiative 14 — EXECUTION-BACKLOG** — [`reports/EXECUTION-BACKLOG.md`](docs/wip/planning/14-holistika-internal-gtm-mops/reports/EXECUTION-BACKLOG.md): Wave **A2** marked **done** (Phase 1 merge + ongoing dry-run/`--write` discipline; verification via `test_merge_process_list_tranche` + `validate_hlk`).

- **Initiative 10 — UAT** — [`docs/wip/planning/10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md`](docs/wip/planning/10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md): **2026-04-15** addendum — Scenario 0 steps **6–7 PASS** (Browser MCP: `hlk_search` + `akos_route_request` / admin escalation visible) after **no concurrent `ollama run`** during WebChat; **supersedes** **2026-04-18** steps **6–7 SKIP** for that retry. Earlier **2026-04-18** addendum — step **5 PASS**; steps **6–7** were **SKIP** (Ollama timeouts when CLI warm-up competed with gateway). [`SESSION_TROUBLESHOOTING.md`](docs/wip/planning/10-madeira-eval-hardening/reports/SESSION_TROUBLESHOOTING.md) covers queue + Ollama + Playwright.

- **`scripts/browser-smoke.py`** — Longer default HTTP timeout (`AKOS_BROWSER_SMOKE_HTTP_TIMEOUT`, default 30s); Playwright `dashboard_health` probes API **`/health`** instead of Swagger **`/docs`**; Windows worker order **chromium → msedge → firefox**; **Scenario 0 registry** HTTP scenarios (`scenario0_hlk_cto`, `scenario0_hlk_research_area`, `scenario0_hlk_kirbe_children`, `scenario0_admin_escalation`) aligned to [`docs/uat/hlk_admin_smoke.md`](docs/uat/hlk_admin_smoke.md) REST parity.

- **Initiative 10 — Phase 6 UAT evidence** — [`docs/wip/planning/10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md`](docs/wip/planning/10-madeira-eval-hardening/reports/uat-madeira-path-bc-browser-20260416.md): initial PASS/SKIP/N/A table (gateway-down run) **plus** dated **addendum** (live loopback + Scenario 0 steps 1–2 entrypoint PASS, pytest parity PASS, steps 3–7 SKIP for qualitative WebChat, HTTP smoke partial / Playwright SKIP). Cross-links: [`phase-completion-report.md`](docs/wip/planning/10-madeira-eval-hardening/reports/phase-completion-report.md), [`master-roadmap.md`](docs/wip/planning/10-madeira-eval-hardening/master-roadmap.md), [`docs/uat/hlk_admin_smoke.md`](docs/uat/hlk_admin_smoke.md), [`docs/wip/planning/README.md`](docs/wip/planning/README.md). **Further addendum** records Cursor IDE Browser MCP rows for Scenario 0 steps 3–4 (step 5 SKIP: queue timeout).

### Added

- **Initiative 11 — Madeira ops copilot** — [`docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md`](docs/wip/planning/11-madeira-ops-copilot/master-roadmap.md): `prompts/overlays/OVERLAY_MADEIRA_OPS.md` on Madeira **standard/full** only (`config/model-tiers.json`); intent exemplars for day-to-day phrasing (`config/intent-exemplars.json` `other` + `hlk_lookup`); UAT stub [`reports/uat-madeira-ops-copilot-20260415.md`](docs/wip/planning/11-madeira-ops-copilot/reports/uat-madeira-ops-copilot-20260415.md); **SECURITY.md** §8a defers `memory_store` scratch until threat-modeled.

- **`tests/test_browser_smoke_scenario0_evaluators.py`** — Unit tests for Scenario 0 golden evaluators loaded from `scripts/browser-smoke.py`.

### Documentation

- **Planning / UAT traceability** — [`docs/wip/README.md`](docs/wip/README.md), [`docs/DEVELOPER_CHECKLIST.md`](docs/DEVELOPER_CHECKLIST.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), [`docs/uat/hlk_admin_smoke.md`](docs/uat/hlk_admin_smoke.md); **[`.cursor/rules/akos-planning-traceability.mdc`](.cursor/rules/akos-planning-traceability.mdc)** — Scenario 0 HTTP registry slice in `browser-smoke.py`, Playwright on Python 3.14 vs **3.12**, Cursor IDE Browser MCP for dashboard UAT. Companion proposal: [`docs/wip/planning/99-proposals/cursor-rules-uat-evidence-instructions.md`](docs/wip/planning/99-proposals/cursor-rules-uat-evidence-instructions.md).

- **Planning** — Initiative **10** (Madeira eval hardening) marked **complete** in `docs/wip/planning/10-madeira-eval-hardening/` with [`reports/phase-completion-report.md`](docs/wip/planning/10-madeira-eval-hardening/reports/phase-completion-report.md); planning index row **10** updated.

### Fixed

- **`scripts/adhoc/_apply_branding.py`** — Stops writing `gateway.controlUi` (OpenClaw 2026.4.x rejects unknown nested keys and can block gateway startup).

- **`doctor.py --repair-gateway`** — When upstream recovery does not reach HTTP+RPC health, print probe state and operator hints (`gateway logs`, port 18789, dashboard). When hints are available from `akos.runtime`, also print **recovery_hints** (status + RPC excerpt + keyword-filtered log tail: pricing timeout, WebSocket 1006).

- **Browser smoke Phase 2** — `architect_tools_ui` and `executor_approval_hint` now validate against **control plane** `GET /agents` (JSON SSOT) like `agent_visibility`, instead of brittle OpenClaw Control UI copy on `GATEWAY_URL/agents` (which false-failed under msedge / OpenClaw version drift).

### Added

- **Initiative 10 — Madeira eval hardening** — Planning mirror `docs/wip/planning/10-madeira-eval-hardening/master-roadmap.md` (indexed from `docs/wip/planning/README.md`): Path B+C gateway SSOT narrative, Windows/Docker operator runway, eval harness layout.

- **`akos/eval_harness.py` + suite `pathc-research-spine`** — Manifest-driven rubric tasks under `tests/evals/suites/`; `scripts/run-evals.py` subcommands `list` / `run`; `LangfuseReporter.trace_eval_outcome()`; optional `AKOS_EVAL_RUBRIC=1` slice in `scripts/release-gate.py`; `tests/evals/README.md`; `py scripts/test.py evals`.

- **Initiative 09 — OpenClaw hygiene** — Planning mirror `docs/wip/planning/09-openclaw-hygiene/master-roadmap.md` (indexed from `docs/wip/planning/README.md`): gateway SSOT alignment with OpenClaw 2026.4.x schema, security-audit interpretation (USER_GUIDE §14.3), SOUL/bootstrap operator path (§3.3.1), `openclaw update` checklist in CONTRIBUTING. **Supersession note** in that roadmap points to initiative 10 for current Path B+C SSOT.

- **`scipy`** — Declared in root `requirements.txt` for graph / numeric helpers aligned with the HLK graph stack.

- **Workspace scaffold README** — Documents that `py scripts/bootstrap.py` Phase 4 (`deploy_soul_prompts`) writes all five `SOUL.md` files after `assemble-prompts.py`, alongside `switch-model.py`.

- **Initiative 08 — runtime / operator / graph stack** — Planning SSOT `docs/wip/planning/08-python-runtime-deployment/master-roadmap.md` (indexed from `docs/wip/planning/README.md`).
- **`akos/graph_stack.py` + serve-api supervision** — `scripts/serve-api.py` optionally starts Streamlit `hlk_graph_explorer.py` as a **child process** when `NEO4J_*` is non-placeholder and Bolt is reachable; `--no-graph-explorer`, `AKOS_GRAPH_EXPLORER=0`, `--open`; background **validate-then-sync** for canonical CSV fingerprints (`AKOS_NEO4J_AUTO_SYNC`, `AKOS_NEO4J_SYNC_POLL_SECONDS`, `AKOS_NEO4J_SYNC_WATCH`, `AKOS_NEO4J_SYNC_WITH_DOCUMENTS`); `GET /health` gains `graph_explorer` and `neo4j_mirror`; `neo4j_env_non_placeholder()` in `akos/hlk_neo4j.py`; `reset_neo4j_driver_cache()` after sync; debounced mirror kick from `GET /hlk/graph/summary`.
- **Operator / test / CI** — `scripts/akos_operator.py` thin dispatcher; `scripts/test.py` group `graph` (`pytest -m graph`); `neo4j` pytest marker; `tests/test_graph_stack.py`; optional **`Dockerfile`**; **`.github/workflows/neo4j-graph-integration.yml`** manual job with Neo4j service + sync + `pytest -m neo4j`.
- **`load_model_workflow_ssot()`** — `akos/model_catalog.py` reads `config/model-tiers.json` as the tier × variant overlay SSOT.

### Changed

- **OpenClaw gateway SSOT (`config/openclaw.json.example`)** — **Path B:** `agents.defaults.sandbox.mode: strict` and **`tools.exec.host: sandbox`** with allowlist exec security. **Path C:** removed **`web_search`** / **`web_fetch`** from Orchestrator and Architect `alsoAllow`; Architect keeps coarse **`browser`**. Removed **`gateway.controlUi`**. `akos.models`: `SandboxDefaults`, **`ExecConfig.host`** default **`sandbox`**, **`LangfuseTraceContext`** gains **`research_surface`** and eval metadata fields. `config/environments/dev-local.json` sets **`thinkingDefault: medium`** for DeepSeek R1 dev-local. Prompt bases (`ORCHESTRATOR_BASE`, `ARCHITECT_BASE`) document the research spine; USER_GUIDE §14.3a–b; SECURITY audit summary; `scripts/doctor.py` Windows Docker/WSL WARNs.

- **Capability matrix** — Orchestrator/Architect drop ambient web tools; Architect lists coarse **`browser`** for policy alignment with gateway.

- **Gateway recovery UX** — `recover_gateway_service()` uses a short post-`gateway start` sleep, default **150s** wait window, `fetch_gateway_status` + `probe_gateway_rpc_detail`, and builds **`GatewayRecoveryResult.recovery_hints`** from status output, optional **File log(s):** tail (filtered), and RPC capture (aligned with observability / SOC: no unconstrained log dumps).

- **Python packaging** — Root **`pyproject.toml`** adds `[project]` `requires-python = ">=3.10"` and pytest markers; **`.python-version`** pins **3.13** for dev; **`openstacksdk`** moved to **`requirements-openstack.txt`** (core `requirements.txt` stays lean).
- **HLK role neighbourhood (mirror vs SSOT)** — `GET /hlk/graph/role/{role_name}/neighbourhood` resolves names via the HLK registry, returns **`mirror_sync_hint`** when Neo4j has no `Role` node yet, and Neo4j matching tolerates legacy **`05-1` → `O5-1`**. Streamlit `scripts/hlk_graph_explorer.py` and static `static/hlk_graph_explorer.html` surface the sync hint instead of a raw JSON blob when the API reports `not_found`.
- **HLK graph zoom landmarks** — `static/hlk_graph_explorer.html` and `static/streamlit_components/hlk_vis_network/index.html` show **hub names only when zoomed out** (largest vis `size` first, hysteresis on scale) so operators can orient before zooming in; full labels return when zoomed in. Streamlit `graph_engine` help notes `streamlit-agraph` cannot attach this behaviour.
- **HLK HTML graph explorer** — `static/hlk_graph_explorer.html` now mirrors the Streamlit canvas conventions: **PARENT_OF**/**OWNED_BY**-based **node sizing** (children / degree / balanced), **edge abbrev + tooltips + colours/widths**, **node hue nudge** by stable id, legend swatches, **edge label mode** (auto/always/hover-only), and **sessionStorage** for those prefs (re-render without re-fetch).
- **Python dependencies** — Moved `runpod` from `requirements.txt` to optional `requirements-gpu.txt` so `pip install -r requirements.txt` succeeds on platforms where `cryptography` has no wheel yet (for example Windows with Python 3.14 free-threaded). RunPod flows remain a no-op until `pip install -r requirements-gpu.txt`; README and USER_GUIDE document the two-step install.
- **HLK Graph Explorer (Streamlit) UX** — `scripts/hlk_graph_explorer.py` now covers **force vs tree** hierarchical layout (with `REPORTS_TO` cycle fallback), **semantic node/edge colour + legend**, **edge labels/tooltips/thickness**, **node sizing** (PARENT_OF / OWNED_BY / degree / balanced), **lock layout**, **favicon** (`static/hlk_graph_explorer_favicon.png`), **selection expander**, and sidebar **`graph_engine`** (`streamlit-agraph` vs **`vis_component`** local bundle under `static/streamlit_components/hlk_vis_network/` for drag-end pin / magnetic MVP). Prior explorer notes (bulk discovery, preset v2, shell links, glossary) remain; USER_GUIDE + ARCHITECTURE updated.
- **HLK PMO portfolio SSOT + registry hygiene** — `TOPIC_PMO_CLIENT_DELIVERY_HUB.md` portfolio row links `hol_opera_dtp_310` and in-repo `external/` transcripts. **`baseline_organisation.csv`**: Chief Business Officer `role_name` **`O5-1`** (letter O) and official description. **`process_list.csv`**: new process **`hol_opera_dtp_310`** *PMO project portfolio SSOT* under Program Management. **`scripts/merge_gtm_into_process_list.py`**: removed legacy `05-1` parent mapping. UTF-8 exports under `docs/wip/planning/04-holistika-company-formation/external/` (pre-kicks, founder report export, ENISA kick-off parts) with genericized external individual names. `access_levels.md` / `ARCHITECTURE.md` process count (1,066). `FOUNDER_INCORPORATION_KNOWLEDGE_INDEX.md` anchor for `hol_opera_dtp_310`. USER_GUIDE PMO hub pointer unchanged in substance.

### Added

- **HLK Graph Explorer vis Streamlit component** — Checked-in `static/streamlit_components/hlk_vis_network/index.html` (vis-network CDN + minimal Streamlit `postMessage` bridge) so operators can opt into **dragEnd**-driven **pin** state without forking Streamlit; session-round-trips `selectedId`, `pinnedIds`, and `positions` for the same neighbourhood JSON as `streamlit-agraph`.
- **HLK graph closeout (control plane + DI)** — `GET /hlk/graph/explorer` serves `static/hlk_graph_explorer.html` (vis-network CDN); `OVERLAY_HLK_GRAPH.md` + `config/model-tiers.json` standard/full wiring; compact `OVERLAY_HLK_COMPACT.md` forbids `hlk_graph_*` in prompt ladder; graph bullets removed from `MADEIRA_BASE.md` / `MADEIRA_PROMPT.md` (graph docs via overlay on larger tiers). `scripts/browser-smoke.py` parses worker `JSON_RESULTS` on non-zero exit; exit `2` when no parseable JSON; `release-gate` treats `2` as soft PASS; `tests/test_browser_smoke_parse.py`. USER_GUIDE §9.10 production ops; SOP §9.1a; `.github/workflows/neo4j-graph-integration.yml` stub; evidence `reports/uat-neo4j-graph-evidence-20260415.md`.
- **HLK Neo4j graph projection (mirrored)** — CSV-derived `Role` / `Process` graph in Neo4j via `akos/hlk_graph_model.py`, `akos/hlk_neo4j.py`, and `scripts/sync_hlk_neo4j.py` (`--with-documents` for v3.0 `Document` + `LINKS_TO`). OpenClaw env bootstrap helper `bootstrap_openclaw_process_env()` in `akos/io.py`. REST `GET /hlk/graph/summary`, `/hlk/graph/process/{item_id}/neighbourhood`, `/hlk/graph/role/{role_name}/neighbourhood`; MCP `scripts/hlk_graph_mcp_server.py`; `openclaw-plugins/akos-runtime-tools` bridges; `config/mcporter.json.example` `hlk-graph` server; optional `compose.neo4j.yml` and `scripts/hlk_graph_explorer.py` (Streamlit). Vault link CI: `scripts/validate_hlk_vault_links.py` + `akos/hlk_vault_links.py` wired into `scripts/release-gate.py`. Planning initiative `docs/wip/planning/07-hlk-neo4j-graph-projection/`. `PRECEDENCE.md` mirrored row for Neo4j; `NEO4J_*` placeholders in all `config/environments/*.env.example`.
- **HLK process list parent IDs and program layer** — Canonical `process_list.csv` gains **`item_parent_2_id`** / **`item_parent_1_id`** (dual-written with existing name columns). Shared column order and resolution live in **`akos/hlk_process_csv.py`**; **`scripts/backfill_process_parent_ids.py`** upgrades or repairs rows; **`scripts/migrate_process_list_program_layer.py`** inserts optional **`hlk_prog_*`** program workstreams under MADEIRA Platform and Think Big Operational Excellence. Registry exposes children by stable parent id (**`HlkRegistry.get_process_tree_by_parent_id`**) and **`GET /hlk/processes/id/{item_id}/tree`**. **`scripts/validate_hlk.py`** enforces id–name consistency (strict parent ids for uniquely named parents; project rows must not set parent ids). Semantic reviews: `docs/wip/planning/02-hlk-on-akos-madeira/reports/process-list-program-layer-semantic-review-20260415.md`, `process-list-parent-id-semantic-review-20260415.md`.
- **HLK duplicate `item_name` cleanup** — Added **`scripts/dedupe_ambiguous_process_item_names.py`** (operator-run; **`--report`** lists collisions) to disambiguate legacy display-name collisions so parent ids resolve everywhere; **`akos.hlk_process_csv.item_name_uniqueness_errors`** and **`scripts/validate_hlk.py`** check **Unique item_name**; **`scripts/backfill_process_parent_ids.py`** fails fast on duplicates. USER_GUIDE §24.3.4 documents **`PROCESS_LIST_FIELDNAMES`**; **`PRECEDENCE.md`** process baseline row notes uniqueness and the canonical asset table structure is corrected.
- **HLK `process_list.csv` maintenance SOP** — Vault **`SOP-PMO_PROCESS_LIST_CSV_MAINTENANCE_001.md`** (column contract, forks, duplicate-name workflow with **`--suggest`**, tooling); **`suggest_item_id_renames_for_duplicate_names`** in **`akos/hlk_process_csv.py`**; **`scripts/check_process_list_header.py`** and release-gate step; USER_GUIDE / vault index / ARCHITECTURE / vault promotion SOP cross-links.
- **GTM Pattern 2 hierarchy refinement** — Added `scripts/refine_gtm_process_hierarchy.py` to insert deterministic English **cluster** process rows (`gtm_cl_*`) from Trello path prefixes, rewire `item_parent_1` / `item_parent_2` for all promoted GTM rows, and sanitize code-like `item_name` values into operator-readable English with symbols preserved in `description`. Updated planning matrix (`trello-list-to-workstream-matrix.md`), PMO vault promotion SOP, and vault index process counts. Semantic review: `docs/wip/planning/02-hlk-on-akos-madeira/reports/gtm-process-list-semantic-review-20260414.md`.
- **HLK GTM process registry merge** — Harmonized PMO/Trello-derived GTM candidate rows into `docs/references/hlk/compliance/process_list.csv` (English workstream parents under Holistika Research, MADEIRA Platform, Think Big Operational Excellence, marketing, and people projects); excluded Tier C `To Do` / `gtm_backlog*` rows; added PMO promotion gate SOP and anchor process `gtm_pm_st_promo`. Planning matrix: `docs/wip/planning/02-hlk-on-akos-madeira/reports/trello-list-to-workstream-matrix.md`. Merge driver: `scripts/merge_gtm_into_process_list.py --write` (requires prior operator approval on canonical CSV tranches).
- **Langfuse production metadata** — `LangfuseTraceContext` in `akos/models.py`, merged metadata + key normalization + optional `LANGFUSE_TRACE_SAMPLE_RATE` in `akos/telemetry.py`; `scripts/log-watcher.py` passes `hlk_surface=log_watcher` and EU-AIA pointers; `scripts/langfuse_list_traces_by_tag.py` for trace-id export; metadata contract documented in `docs/ARCHITECTURE.md` with USER_GUIDE §12.2.0 / SOP Phase 10 note; EU-AIA checklist evidence row `LF-META-1`.
- **Madeira read-only browser observation** — Gateway `alsoAllow` adds `browser_snapshot` and `browser_screenshot` for Madeira (no coarse `browser` token); mirrored in `config/agent-capabilities.json`; threat model `docs/wip/planning/02-hlk-on-akos-madeira/reports/madeira-write-browser-threat-model.md`.
- **KiRBe sync dry-run** — `scripts/kirbe_sync_daemon.py` fingerprints canonical HLK CSVs (+ optional `validate_hlk.py`), gated `--apply` stub; design `reports/kirbe-sync-daemon-design.md`; tests `tests/test_kirbe_sync_daemon.py` and `py scripts/test.py kirbe`.
- **Holistika P1 docs** — `reports/founder-incorporation-section7-structured-table.md`, `reports/phase-1-track-checklist.md`; registry `REG.008` updated for in-repo P1 closure.
- **CSV tranche gate** — Operator approval template `reports/canonical-csv-tranche-operator-approval-template.md` (no canonical CSV edits without recorded approval).
- **Planning backlog registry (`06`)** — Cross-initiative backlog SSOT at `docs/wip/planning/06-planning-backlog-registry/master-roadmap.md` with `reports/` for proxy-UAT notes; `docs/wip/planning/README.md` index row **06**.
- **Holistika company formation program (`04`)** — Promoted to active execution artifacts: `docs/wip/planning/04-holistika-company-formation/master-roadmap.md` and `phase-1-plan.md` (governance framing + verification matrix reference).
- **Madeira expansion phase stubs (`02`)** — `phase-madeira-write-browser-plan.md`, `phase-kirbe-sync-daemons-plan.md`, and `phase-canonical-csv-tranche-plan.md` (Executor+HITL, KiRBe daemons, approval-gated CSV) linked from the consolidated plan and backlog registry.
- **Madeira read-only hardening** — Compact-tier overlays `OVERLAY_HLK_COMPACT.md` and `OVERLAY_STARTUP_COMPACT.md` for Madeira; `execution_escalate` intent for code/browser/MCP/multi-step execution via `akos_route_request` / `akos/intent.py`; `sequential_thinking` on Madeira allowlist; workspace scaffold `madeira/memory/README.md` and recursive scaffold deploy for `memory/`; log-watcher grounding flags and real-time eval alerts (`madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination`); USER_GUIDE security audit subsection and multi-model HLK admin smoke matrix. Traceability: `docs/wip/planning/02-hlk-on-akos-madeira/reports/madeira-readonly-hardening.md`.
- **HLK Envoy repository hub** — Canonical registry `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` with policy README and `platform/`, `internal/`, `client-delivery/` stubs; `Think Big/README.md` for non-repo client artifacts; PMO pilot topic `TOPIC_PMO_CLIENT_DELIVERY_HUB.md`; vault `index.md` entity-placement guidance; `TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md` “Linked Git repositories” section; `PRECEDENCE.md` canonical/mirrored rows and “GitHub repositories vs vault authority”; planning traceability `docs/wip/planning/05-hlk-vault-envoy-repos/phase-1-plan.md`.
- **HLK KM follow-up (hygiene + UAT)** — Reconciled PMO Trello registry ids to the primary board export; added `PMO/imports/` with `trello_board_67697e19_primary.json`, `trello_board_67697e19_archive_slice.json`, and full formatted export; moved wip KM syntheses to `docs/wip/hlk-km/`; added `docs/wip/README.md` and `docs/wip/planning/99-proposals/` for loose plan files; relocated repo-root `_*.py` scratch scripts to `scripts/adhoc/`; HLK admin smoke **Scenario 8** for KM validators and registry checks; [km-plan-followup-checklist.md](docs/wip/planning/03-hlk-km-knowledge-base/reports/km-plan-followup-checklist.md) for incremental work without redoing the baseline rollout.
- **HLK governed KM (Topic–Fact–Source)** — Canonical contract `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md`, vault index updates, topic template and visual manifest example under Compliance, PMO `RESEARCH_BACKLOG_TRELLO_REGISTRY.md`, Output 1 pilot bundle under `v3.0/_assets/km-pilot/`, workspace roadmap `docs/wip/planning/03-hlk-km-knowledge-base/`, five `docs/wip/hlk-km/research-synthesis-*.md` stubs linked from the registry; Trello exports under PMO `imports/` with primary/archive split, and `scripts/validate_hlk_km_manifests.py` for manifest frontmatter and raster path checks.
- **HLK founder-governance case layer** — Add canonical case docs for entity-formation decisions, capitalization posture, ENISA evidence, trademark scope, Research-vs-Tech-Lab separation, and the founder-governance lifecycle/promotion ladder under role-owned `v3.0` paths.
- **HLK founder-governance SOPs** — Add canonical `v3.0` drafts for `Founder Entity Formation Readiness`, `Trademark and Naming Governance`, `Founder-to-Company Funding Path`, and `ENISA Readiness and Evidence Pack` under the role-owned Legal, Finance/Taxes, and Compliance paths.
- **HLK founder-governance registry rows** — Register matching workstreams/processes in `docs/references/hlk/compliance/process_list.csv` for founder entity formation, trademark control, founder funding, and ENISA readiness (baseline before the GTM tranche; see Unreleased GTM merge entry for current inventory).
- **Windows gateway port recovery** — `akos.runtime.recover_gateway_service()` now clears stale TCP listeners on port `18789` via `netstat`/`taskkill` after `gateway stop` on Windows, aligning with the `py scripts/doctor.py --repair-gateway` operator path and reducing post-reboot manual rescue.
- **Planning traceability** — `docs/wip/planning/02-hlk-on-akos-madeira/phase-7-plan.md` and `reports/phase-7-report.md` record the Gateway and GPU Recovery Hardening rollout (env contract, Windows supervision, operator runbooks).
- **ShadowPC OpenStack GPU provider** -- `akos/openstack_provider.py` provides full lifecycle management (instance creation, floating IP, security groups, teardown, spot termination detection) for Shadow's OpenStack GPU infrastructure (RTX A4500/RTX 2000 Ada). Config: `gpu-shadow.json` overlay, `gpu-shadow.env.example`, `OpenStackInstanceConfig` Pydantic model in `akos/models.py`.
- **`deploy-shadow` GPU CLI subcommand** -- `scripts/gpu.py deploy-shadow` provisions a vLLM instance on ShadowPC OpenStack with cloud-init bootstrapping, health polling, and `switch-model.py gpu-shadow` integration. Interactive menu updated with ShadowPC as option 3.
- **`vllm-shadow` gateway provider** -- `openclaw.json.example` now declares a `vllm-shadow` provider block with `${VLLM_SHADOW_URL}` env substitution, parallel to `vllm-runpod`.
- **AWQ weight quantization support** -- `PodConfig.build_vllm_command()` now emits `--quantization`, `--enforce-eager`, and `--max-num-batched-tokens` flags when configured via `envVars`. `CatalogEntry` gains a `quantization` field.
- **DeepSeek R1 70B AWQ catalog entry** -- `config/model-catalog.json` adds `casperhansen/deepseek-r1-distill-llama-70b-awq` (70GB VRAM at AWQ vs 140GB at bf16), making 70B inference feasible on 2x A100-80GB with KV cache headroom.
- **HLK branding** -- Gateway control UI title set to "HLK Intelligence Platform" via `gateway.controlUi.title`. Agent identity blocks renamed to "HLK Orchestrator", "HLK Architect", etc. FastAPI title changed to "HLK Operations Platform". Placeholder HLK logo generated at `static/hlk-logo.png`.

### Changed

- **HLK graph explorer (UX + OPS + browse)** — [`static/hlk_graph_explorer.html`](static/hlk_graph_explorer.html): stepped journey; summary **cards**; **registry pickers** from `/hlk/areas`, `/hlk/roles`, `/hlk/processes`, `/hlk/processes/id/{id}/tree`, `/hlk/search` (SSOT via REST only); area filter, project/child selects, search hits; shared **depth** + **node limit** sliders; role/process **Draw graph** actions; operator-friendly API-key copy; palette aligned with org boilerplate dark HSL tokens; vis-network physics off after stabilize; `data-testid` hooks. [`scripts/serve-api.py`](scripts/serve-api.py) **preflight bind** + `USER_GUIDE` §9.10 hint. [`scripts/browser-smoke.py`](scripts/browser-smoke.py) marker checks. [`docs/SOP.md`](docs/SOP.md) §9.1a; initiative [`07` **D6**](docs/wip/planning/07-hlk-neo4j-graph-projection/master-roadmap.md); Browser MCP evidence [`uat-graph-explorer-browser-20260415.md`](docs/wip/planning/07-hlk-neo4j-graph-projection/reports/uat-graph-explorer-browser-20260415.md). [`scripts/hlk_graph_explorer.py`](scripts/hlk_graph_explorer.py) Streamlit app aligned with HTML explorer: sidebar URL/token, metrics snapshot, area/role and project/child/search pickers, shared depth/limit, `agraph` rendering, manual ID fallback. **`py scripts/hlk_graph_explorer.py`** now re-execs `python -m streamlit run` (avoids bare-mode / session-state errors); `httpx` **connection refused** returns an in-app error instead of a traceback.
- **Neo4j Aura / TLS** — `get_neo4j_driver()` honors optional `NEO4J_TRUST` / `NEO4J_CA_BUNDLE` (`neo4j+s` → `neo4j+ssc` rewrite when trust is relaxed; ASCII-only warning logs for Windows consoles). With **`neo4j+ssc://` / `bolt+ssc://` already in `NEO4J_URI`**, redundant `NEO4J_TRUST=all` no longer emits a misleading warning. USER_GUIDE §9.10 prefers explicit `neo4j+ssc` when needed; `prod-cloud.env.example` notes omitting `NEO4J_TRUST` in that case. `scripts/browser-smoke.py` accepts **`AKOS_BROWSER_SMOKE_API_URL`** when the API runs on a non-default port. Operator runbook [`cursor-browser-mcp-graph-explorer.md`](docs/wip/planning/07-hlk-neo4j-graph-projection/reports/cursor-browser-mcp-graph-explorer.md) links Cursor’s browser-tools MCP install page.
- **SECURITY.md** — §4a notes CDN egress for `GET /hlk/graph/explorer` (vis-network via jsDelivr).
- **MCP inventory tests / README** — `tests/conftest.py` `EXPECTED_MCP_SERVERS` includes `hlk-graph` (matches `config/mcporter.json.example`); README Integration Layer counts **12** MCP servers and lists **HLK Graph MCP**.
- **HLK graph docs sweep** — `CONTRIBUTING.md` optional deps (`neo4j`, `streamlit`, `streamlit-agraph`), `docs/references/hlk/v3.0/index.md` platform compatibility row, `.cursor/rules/akos-docs-config-sync.mdc` trigger table, `docs/uat/hlk_admin_smoke.md` Scenario 9 (optional Neo4j path).
- **HLK Envoy `REPOSITORIES_REGISTRY.md`** — Set `madeira-hlk-runtime` to `FraysaXII/openclaw-akos`; set `kirbe-platform` to `FraysaXII/kirbe` (operator-confirmed KiRBe application repo).
- **Madeira planning coherence** — `docs/wip/planning/02-hlk-on-akos-madeira/master-roadmap.md` reconciled with read-only hardening closure + `06` registry; `MADEIRA_HARDENING_CONSOLIDATED_PLAN.md` out-of-scope/follow-up sections now point at expansion phase plans.
- **Madeira traceability mirror** — Agent-proxy Lane B runbook + Langfuse UAT pointer; KM follow-up checklist links the `06` registry.
- **Planning folder layout** — Renamed `docs/wip/planning/*` initiative directories to prefixed paths: `01-akos-full-roadmap/`, `02-hlk-on-akos-madeira/`, `03-hlk-km-knowledge-base/`, `04-holistika-company-formation/`, `05-hlk-vault-envoy-repos/`, `99-proposals/` (was `_proposals/`). Inbound links and [docs/wip/planning/README.md](docs/wip/planning/README.md) (numbered index) updated; `.cursor/rules/akos-planning-traceability.mdc` and [docs/wip/README.md](docs/wip/README.md) describe the `NN-` convention. **Madeira consolidated plan** lives at [docs/wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md](docs/wip/planning/02-hlk-on-akos-madeira/MADEIRA_HARDENING_CONSOLIDATED_PLAN.md) (Part B *UAT lane ordering*); traceability mirror and `hlk_admin_smoke.md` cross-link use the same prefix.
- **SECURITY.md** — OpenClaw gateway security audit operator step now links directly to [docs/USER_GUIDE.md](docs/USER_GUIDE.md) §14.3 (cadence, `--deep`, `--fix`).
- **Madeira traceability mirror** — `docs/wip/planning/02-hlk-on-akos-madeira/reports/madeira-readonly-hardening.md` adds post-bootstrap verification (2026-04-14), phase→commit mapping, and Scenario 0 REST vs WebChat UAT lanes.
- **HLK admin smoke UAT** — `docs/uat/hlk_admin_smoke.md` documents automated parity checks (pytest + assemble) and a **browser UAT** subsection (dashboard / Cursor IDE browser, tool-capable model requirement, clean session, API port 8420) alongside [`dashboard_smoke.md`](docs/uat/dashboard_smoke.md).
- **Cursor rules (AKOS)** — `.cursor/rules/akos-docs-config-sync.mdc`, `akos-governance-remediation.mdc`, and `akos-planning-traceability.mdc` updated for HLK KM (`HLK_KM_TOPIC_FACT_SOURCE.md`, `validate_hlk_km_manifests.py`, `v3.0/_assets` manifests) and governed `docs/wip` layout (`README.md`, `planning/99-proposals/`, `hlk-km/`).
- **Bootstrap OpenCLaw detection** — `scripts/bootstrap.py` preflight uses `akos.runtime.resolve_openclaw_cli()` so `openclaw.cmd` / `openclaw.exe` npm shims match `scripts/doctor.py` on Windows.
- **Profile switch diagnostics** — `scripts/switch-model.py` logs the resolved OpenCLaw executable and surfaces repair hints when gateway recovery is incomplete.

### Fixed

- **RunPod VRAM saturation** -- Pod config (`gpu-runpod-pod.json`) switched from bf16 full-precision to AWQ-quantized model variant, `MAX_NUM_SEQS` reduced from 128 to 64, `ENFORCE_EAGER` enabled. Eliminates the 75/80 GB VRAM alert on 2x A100-SXM4-80GB pods.

### Fixed (Phase 6 Runtime Remediation)

- **RunPod serverless AWQ startup regressions** -- normalized runtime defaults to `DTYPE=float16` for AWQ and forced non-JIT worker settings (`KV_CACHE_DTYPE=auto`, `VLLM_ATTENTION_BACKEND=TRITON_ATTN`) to prevent repeated worker boot failures (`nvcc`/FlashInfer-related crashes) on `runpod/worker-v1-vllm`.
- **Serverless overlay hardening** -- `_update_serverless_overlay_json()` now enforces RunPod worker compatibility defaults when `runpod/worker-v1-vllm` is used, so model-catalog overrides cannot silently reintroduce unstable settings.
- **Orchestrator startup scaffold recovery** -- added `config/workspace-scaffold/orchestrator/WORKFLOW_AUTO.md` and wired tests/docs so workspace startup context remains deterministic after compaction/restart cycles.
- **Shadow tenant compatibility** -- OpenStack deployment now omits unset `security_groups` / `key_name` values, aligns the default image/flavor/network to the live tenant inventory, and tolerates projects where security-group creation is forbidden by policy.
- **`dev-local` overlay drift** -- restored the documented medium-tier local default (`ollama/deepseek-r1:14b` with `qwen3:8b` fallback) so post-reboot local recovery no longer lands on the weaker fallback by default.

### Fixed (NBT and Flagship Residuals)

- **Langfuse SDK v4 migration** -- `akos/telemetry.py` rewritten from v3 `trace()`/`generation()`/`score()` API (silently broken on SDK v4) to v4 `start_as_current_observation()`/`propagate_attributes()`/`span.score()` API. Traces now actually appear in the Langfuse dashboard.
- **Langfuse auth verification** -- `scripts/test-langfuse-trace.py` now calls `auth_check()` before sending, so credential/region mismatches fail loudly instead of printing false success.
- **Swapped Langfuse keys fixed** -- `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` were swapped in `~/.openclaw/.env`; corrected so `pk-lf-*` is the public key.
- **Langfuse reporter shutdown** -- `LangfuseReporter.shutdown()` added for clean export; `log-watcher.py` uses it on exit.

### Added (NBT and Flagship Residuals)

- **Semantic intent classifier** -- `akos/embeddings.py` (Ollama `nomic-embed-text` embedding client) + `akos/intent.py` rewritten to use cosine-similarity routing against `config/intent-exemplars.json` exemplar bank, with regex fallback. Scales to new domains by adding exemplars, not regex patterns.
- **GTM route type** -- `gtm_project` route added to the intent classifier for go-to-market/product/launch pipeline queries.
- **Trello GTM ingestion** -- `scripts/ingest-trello.py` maps Trello board structure to candidate `process_list.csv` rows (726 rows from the GTM board) for operator review before canonical commit.
- **KiRBe sync contract** -- `config/sync/kirbe-sync-contract.md` defines stable machine-key policy (NBT.1), canonical-to-KiRBe ownership (NBT.2), table-level sync direction, conflict resolution, stale row cleanup list, and deterministic replay design (NBT.4).
- **Model UAT comparison matrix** -- `docs/wip/planning/02-hlk-on-akos-madeira/reports/model-uat-comparison-matrix.md` documents per-model GPU performance, tool-calling support, and escalation behavior on local RTX 2000 Ada (15GB VRAM).

### Fixed (Madeira Flagship Hardening)

- Madeira startup recovery now has deterministic dated continuity notes under `workspace-*/memory/YYYY-MM-DD.md`, reducing post-compaction file-audit friction and giving the live runtime concrete recovery targets instead of missing-path drift.
- `config/eval/langfuse.env` and `config/eval/langfuse.env.example` were removed from the repo contract. Langfuse secrets now resolve from process env or `~/.openclaw/.env`, while non-secret watcher settings live in `config/openclaw.json.example` `diagnostics.logWatcher` and bootstrap sidecar sync.
- `scripts/log-watcher.py` now reviews Madeira session transcripts for answer-quality telemetry, mirrors local jsonl evidence under `~/.openclaw/telemetry/`, and emits answer-quality traces in addition to startup compliance and alert traces.
- Madeira now exposes `akos_route_request` as a deterministic runtime helper for HLK/search/finance/admin route classification, while the live `qwen3:8b` admin branch remains classified as a model-specific residual rather than silently treated as healthy.
- `scripts/doctor.py` and `scripts/check-drift.py` now enforce the new Langfuse secret authority and flag legacy repo-local Langfuse env files as drift.

### Added (MADEIRA Runtime UX Stabilization)

- **Madeira agent** — fifth agent (`id: "madeira"`) as the user-facing dashboard entrypoint for HLK operations. Read-only lookup assistant with a dedicated workspace (`~/.openclaw/workspace-madeira`), scaffold (`config/workspace-scaffold/madeira/`), and all 3 prompt variants.
- **MADEIRA_BASE.md** — lookup-first prompt contract: Lookup Mode (default, tool-backed answers), Summary Mode (multi-tool synthesis), Escalation Mode (delegate to Orchestrator for admin tasks).
- **Gateway contract validation** — `akos/tools.py`, `scripts/doctor.py`, and `scripts/check-drift.py` now share gateway core/plugin tool semantics, detect legacy `tools.allow`, and flag unknown runtime tool IDs.
- **Dashboard UAT scenario** (Scenario 0 in `docs/uat/hlk_admin_smoke.md`) — verifies Madeira answers HLK questions directly via tools in the browser dashboard.

### Changed (MADEIRA Runtime UX Stabilization)

- Agent count updated from 4 to 5 across all docs (ARCHITECTURE.md, USER_GUIDE.md, SOP.md, CHANGELOG.md).
- Prompt assembly now produces 15 files (5 agents x 3 variants) instead of 12.
- `config/model-tiers.json` — MADEIRA added to HLK and startup compliance overlay agent lists for standard and full variants.
- `config/agent-capabilities.json` — `madeira` role added with read-only HLK + finance + memory tools.
- `config/openclaw.json.example` — `madeira` in `agents.list` and `tools.agentToAgent.allow`; gateway tool blocks now use core IDs plus `alsoAllow` for MCP plugins.
- `akos/io.py` — `AGENT_WORKSPACES` and `agent_scaffold_map` include MADEIRA.
- `scripts/assemble-prompts.py` — `AGENTS` dict includes MADEIRA.
- `scripts/bootstrap.py` — legacy `tools.allow` entries are migrated into `alsoAllow`, while profile selection stays derived from `agent-capabilities.json`.

### Fixed (Madeira Gateway Alignment Remediation)

- `config/openclaw.json.example` no longer mixes gateway core IDs with AKOS logical tool names in agent tool policies.
- `openclaw-plugins/akos-runtime-tools` now registers the `hlk_*` and `finance_*` runtime tool IDs that Madeira and the other agents reference through `tools.alsoAllow`, closing the config-only/runtime-missing gap.
- `config/openclaw.json.example` now pins trusted OpenClaw plugin IDs in `plugins.allow`, so the runtime bridge is explicit instead of relying on auto-loaded local plugin discovery.
- `akos/api.py` now exposes read-only `/finance/*` endpoints so the runtime bridge can reuse the existing finance service instead of duplicating provider logic.
- `akos/io.py`, `scripts/bootstrap.py`, `scripts/doctor.py`, and `scripts/check-drift.py` now deploy and verify the repo-managed OpenClaw plugin bridge under `~/.openclaw/extensions`.
- `scripts/browser-smoke.py`, `tests/test_api.py`, `tests/test_live_smoke.py`, and `tests/test_e2e_pipeline.py` now lock the 5-agent runtime contract instead of the older 4-agent layout.
- `prompts/MADEIRA_PROMPT.md` now exists as the compact Madeira prompt, matching the base prompt and startup contract.

### Fixed (Madeira Lookup Hardening)

- `akos/hlk.py` now resolves normalized role/process queries deterministically, ranks `hlk_search` results, and exposes `best_role` / `best_process` fields so lookup agents do not have to infer canonical winners from raw mixed search output.
- Madeira now uses a narrower `minimal` runtime profile with curated read/memory/HLK/finance access, reducing non-canonical fallback surface while preserving startup and lookup support.
- `akos/api.py` now returns live agent-specific drift issues from `GET /agents/{id}/capability-drift` instead of placeholder empty results.
- Prompt parity hardening now aligns Madeira’s lookup ladder with same-turn search retry, and updates the base startup prompts to use the current `read` tool name.
- Executor and Verifier now expose `browser` explicitly in the gateway template, matching their policy/docs-driven validation responsibilities.

### Added (HLK CI/CD Hardening -- Phase 5)

- **HLK validation script** (`scripts/validate_hlk.py`) -- 9 deterministic checks: CSV parse, role_owner integrity, graph integrity, granularity canon, duplicate IDs, project-has-children. Integrated into `scripts/release-gate.py` as a mandatory gate step.
- **Expanded HLK test coverage** -- 3 new test classes in `tests/test_hlk.py`: `TestHlkIntegrity` (referential + graph integrity), `TestHlkProvenance` (structural provenance), `TestHlkApiEdgeCases` (path traversal, XSS, special characters).
- **Externalization decision**: HLK stays internal to AKOS (tight coupling with vault CSVs and `akos/io.py`; revisit when a second consumer outside this repo needs direct imports).

### Added (HLK Admin UX -- Phase 4)

- **HLK Operator Model** in USER_GUIDE -- session vs workspace vs vault distinction, day-to-day MADEIRA usage guide, knowledge addition and baseline maintenance flows, vault structure reference, quick reference card.
- **HLK UAT smoke scenarios** (`docs/uat/hlk_admin_smoke.md`) -- 7 scenarios covering role lookup, area navigation, process tree, gap detection, search, admin workflow, and session-vs-vault discipline.

### Added (HLK MADEIRA Entry Surface -- Phase 3)

- **HLK MCP server** (`scripts/hlk_mcp_server.py`) -- 8 read-only tools for vault registry lookups: `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`, `hlk_projects`, `hlk_gaps`, `hlk_search`. FastMCP + stdio transport.
- **OVERLAY_HLK.md** -- prompt overlay teaching agents about the HLK vault structure, canonical source rules, compliance taxonomy, and tool usage. Registered in `model-tiers.json` for standard and full variants across all 5 agents.
- **HLK admin workflow** (`config/workflows/hlk_admin.md`) -- structured workflow for organisation and process management with approval gates before CSV edits.
- **HLK tool registration** -- 8 `hlk_*` tools added to `agent-capabilities.json` (all 5 roles), `permissions.json` (autonomous), and `mcporter.json.example`.

### Added (HLK Domain Service -- Phase 2)

- **HLK Pydantic domain models** in `akos/models.py` — `OrgRole`, `ProcessItem`, `HlkResponse` envelope, and constrained types (`AccessLevel`, `ConfidenceLevel`, `SourceCategory`, `ProcessGranularity`).
- **HLK registry service** (`akos/hlk.py`) — `HlkRegistry` class reads canonical vault CSVs and serves typed lookups: role/chain/area, process/tree/project, gap detection, and fuzzy search. Lazy singleton pattern matching `FinanceService`.
- **HLK API endpoints** in `akos/api.py` — 10 read-only endpoints under `/hlk/*`: roles, role chain, areas, processes, project summary, process tree, gaps, and search. Protected by `AKOS_API_KEY`.
- **HLK test suite** (`tests/test_hlk.py`) — model parsing, registry lookups, chain traversal, gap detection, search, and FastAPI endpoint validation. Registered as `hlk` test group in `scripts/test.py`.

### Added (Runtime, Planning, and Finance UX Hardening)

- **HLK planning system** — reusable personal Cursor skill (`hlk-planning-system`) plus workspace traceability rule for mirroring execution-relevant plans and reports into `docs/wip/planning/NN-<initiative-slug>/` (see [planning/README.md](docs/wip/planning/README.md)).
- **Finnhub-backed symbol search** in `akos/finance.py` — `finance_search` now uses Finnhub fuzzy company-name search when `FINNHUB_API_KEY` is configured, with yfinance fallback.
- **Derived quote context** in `QuoteData` — `change_amount` and `change_percent` added for better briefing UX without changing tool names.
- **GPU serverless model picker wiring** — `deploy_serverless` now uses the model catalog and stores active serverless infra state.
- **Doctor runtime checks** — local Ollama readiness probe and runtime env lookup from `~/.openclaw/.env`.
- **New test runner groups** — `telemetry` and `router` added to `scripts/test.py`.

### Changed (Runtime, Planning, and Finance UX Hardening)

- **Bootstrap tool translation** now preserves gateway-compatible `alsoAllow` / `deny` fields from `config/openclaw.json.example` while deriving each agent's runtime profile from `config/agent-capabilities.json`.
- **Bootstrap MCP deployment** now refreshes deployed `~/.mcporter/mcporter.json` from the resolved repo template when content drifts.
- **Provider auth config** for `ollama` and `vllm-runpod` is now env-backed in `config/openclaw.json.example`; environment templates include the required placeholders.
- **RunPod operator UX** in `scripts/gpu.py` now frames local vs serverless vs dedicated pod as a guided choice with cost and deployment summaries.
- **Release gate** now includes strict inventory verification and explicit API smoke tests in addition to tests, drift, and browser smoke.
- **Test-count references** updated from `234+` to `300+` in canonical docs and runner copy.

### Fixed (Runtime, Planning, and Finance UX Hardening)

- **False mcporter drift** in `check-drift.py` — compares resolved deployed content against the resolved repo template instead of flagging path-resolution differences as drift.
- **Gateway config startup failure** when `RUNPOD_API_KEY` is newly referenced but missing from an existing `~/.openclaw/.env` — bootstrap now backfills missing env placeholders.
- **Doctor false failure** for placeholder `VLLM_RUNPOD_URL=http://localhost:8000/v1` — now treated as not configured rather than an unreachable live endpoint.

### Added (Finance Research MCP)

- **Finance MCP server** (`scripts/finance_mcp_server.py`) — read-only financial data tools (`finance_quote`, `finance_search`, `finance_sentiment`) exposed via FastMCP over stdio.
- **`akos/finance.py`** — `FinanceService` with yfinance + Alpha Vantage backends, TTL caching (60s quotes, 300s sentiment), graceful degradation when backends or API keys are absent.
- **Finance response envelope** (`FinanceResponse`, `QuoteData`, `SearchResult`, `SentimentItem`) in `akos/models.py` — schema-locked Pydantic models shared by the MCP server and tests.
- **Generalized `resolve_mcporter_paths()`** in `akos/io.py` — now resolves any repo-local `scripts/*.py` MCP server path during bootstrap (not just `mcp_akos_server.py`).
- **`yfinance>=0.2.36`** added to `requirements.txt` (optional — finance MCP degrades gracefully without it).
- Finance tool IDs (`finance_quote`, `finance_search`, `finance_sentiment`) added to `config/permissions.json` (autonomous) and `config/agent-capabilities.json` (all five roles).

### Added (RunPod + Langfuse Production Overhaul — Phases 0-5)

- **GPU Infrastructure CLI** (`scripts/gpu.py`) for zero-copy-paste RunPod pod/serverless deployment, PodManager REST API, auto tensor-parallel-size, activeInfra state tracking.
- **Dual-mode RunPod support** — `gpu-runpod-pod` environment profile for dedicated pod mode alongside existing serverless. `PodConfig` Pydantic model and `scripts/setup-runpod-pod.py` provisioning script (Phase 1).
- **`probe_vllm_health()`** — HTTP health probe for dedicated vLLM pods, consumed by doctor and the `/health` API endpoint (Phase 2).
- **`FailoverRouter`** in `akos/router.py` — automatic provider failover with 3-failure threshold and `INFRA_FAILOVER_TRIGGERED` SOC alert. vLLM status surfaced in `/health` API (Phase 2).
- **Langfuse environment tagging** — traces tagged with active environment name for multi-env observability (Phase 0).
- **`scripts/test-langfuse-trace.py`** — smoke test for Langfuse trace connectivity (Phase 0).
- **DX metric wiring** — `trace_metric()` for request counts and latency; `trace_alert()` forwards SOC alerts to Langfuse; `startup_compliance` success path wired; `run-evals.py` `_report_to_langfuse()` for dry-run (Phase 3).
- **`check_runpod_readiness()`** in `doctor.py` — validates config, API key, and vLLM probe for dedicated pods (Phase 4).
- **`check_langfuse_readiness()`** in `doctor.py` — validates credentials and SDK init (Phase 4).
- **`tests/test_telemetry.py`** — 14 tests covering init, trace_request, trace_startup_compliance, trace_alert, trace_metric, normalize_env, flush (Phase 5).
- **`tests/test_router.py`** — 10 tests covering failover threshold, recovery, and multi-provider routing (Phase 5).

### Added (Model Catalog + vLLM Image Overhaul)

- **Model Catalog** (`config/model-catalog.json`, `akos/model_catalog.py`) — SSOT for GPU-deployable models mapping HuggingFace IDs to VRAM, parsers, GPU defaults. 8 models: DeepSeek R1 70B, DeepSeek V3, Llama 3.1 70B/8B, QwQ 32B, Qwen 2.5 72B, Mistral Large 123B, Hermes 3 70B.
- **Interactive model picker** in `scripts/gpu.py deploy-pod` — numbered model/GPU selection driven by catalog VRAM data, replaces hardcoded 70B-only logic.
- **`_ensure_env_placeholders()`** in `scripts/gpu.py` — re-asserts placeholder env vars after deployment so OpenClaw `${VAR}` substitution never crashes on empty values.
- **`_upsert_env_line()`** — generic env file insert-or-update helper, replaces inline `.env` manipulation in deploy flow.

### Changed (Model Catalog + vLLM Image Overhaul)

- **Container image** changed from `runpod/pytorch:2.8.0-py3.11-cuda12.8.1-devel-ubuntu22.04` to `vllm/vllm-openai:latest` — image ENTRYPOINT handles `python -m vllm.entrypoints.openai.api_server`, so `dockerStartCmd` now passes only CLI flags.
- **`PodConfig.containerDiskGb`** added (default 100, min 20) for explicit container disk sizing.
- **`build_vllm_command()`** no longer emits `python -m ...` prefix; `--served-model-name` auto-derives from `modelName.split("/")[-1]`; conditional `--reasoning-parser` and `--chat-template` flags added.
- **`PodManager.create_pod()`** default image and container disk updated to match new image.
- **`MAX_MODEL_LEN`** default reduced to 32768 in `gpu-runpod-pod.json` for reliable 2x A100-80GB operation with fp8 KV cache.
- **vLLM health probe** now sends `User-Agent: akos-gpu-cli/1.0` and `Accept: application/json` headers for reverse proxy compatibility.
- **Env placeholder values** hardened: `OLLAMA_GPU_URL` defaults to `http://localhost:11434` (was empty), `VLLM_RUNPOD_URL` defaults to `http://localhost:8000/v1` (was empty) in all `.env.example` files.
- **Env loading** in `gpu.py` now filters empty values (`if v:` guard) to prevent overwriting real credentials with blanks.
- **Deploy flow** uses `_save_key_to_env()` for both repo and `~/.openclaw/.env` writes, replacing inline file manipulation.

### Fixed (RunPod + Langfuse Production Overhaul — Phase 0)

- **`VLLM_RUNPOD_URL`** missing `/openai/v1` suffix — requests to dedicated pods now target the correct OpenAI-compatible endpoint.
- **`log-watcher.py --once`** mode was not exiting after single pass.
- **Health interval** was hardcoded to 60s — now configurable.

### Added

- **`OVERLAY_STARTUP_COMPLIANCE.md`** — new prompt overlay for medium+ model tiers with recency rule (re-read startup files within 5 messages), invariant check, and good/bad examples. Registered in `config/model-tiers.json` for both `standard` and `full` variants across all five agents.
- **`trace_startup_compliance()`** method on `LangfuseReporter` — scored Langfuse traces (`startup_compliance: 0.0/1.0`) for Post-Compaction Audit events.
- **Langfuse environment placeholders** (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`) in all three `config/environments/*.env.example` files.
- **Post-Compaction Audit detection** in `scripts/log-watcher.py` — detects gateway audit entries and traces them to Langfuse.
- **Langfuse scoring** in `scripts/run-evals.py` — creates scored eval traces when Langfuse credentials are configured.

### Changed

- **Session Startup in all 5 base prompts** hardened with SOTA enforcement patterns: explicit `read()` tool-call syntax, `CRITICAL` / `MUST` gate, self-correction mandate, and "do NOT mention internal steps" directive.
- **`scripts/serve-api.py`** now loads Langfuse credentials from process env or `~/.openclaw/.env` for accurate `/health` Langfuse status.
- **`scripts/run-evals.py`** upgraded from stub to functional Langfuse integration (loads env, creates reporter, reports scores).

### Added (Phase 9)

- **Committed Modelfiles** for Ollama `num_ctx` configuration (`config/ollama/Modelfile.qwen3-8b`, `Modelfile.deepseek-r1-14b`). Aligns `num_ctx` to tier `contextBudget` (16384 for small, 32768 for medium).
- **`deepseek-r1:14b`** (14B medium-tier model) registered in SSOT provider config with `contextWindow: 32768`, `reasoning: true`.
- **Ollama Flash Attention + KV cache quantization** env vars in `dev-local.env.example` (`OLLAMA_FLASH_ATTENTION=1`, `OLLAMA_KV_CACHE_TYPE=q8_0`).
- **RunPod vLLM production optimization** — 17 production-grade `envVars` in `gpu-runpod.json`: FP8 KV cache, prefix caching, tool-call parser (`deepseek_v3`), reasoning parser (`deepseek_r1`), chunked prefill, optimized concurrency.
- **`fallbacks` field** in model config for provider failover chains across all three environments (`dev-local`, `gpu-runpod`, `prod-cloud`).
- **Pydantic `RunPodEndpointConfig` validators** — warns when `ENABLE_AUTO_TOOL_CHOICE` is true but `TOOL_CALL_PARSER` is unset, and when `TENSOR_PARALLEL_SIZE` exceeds `len(gpuIds)`.
- **Env placeholder coverage test** — `TestEnvPlaceholderCoverage` in `validate_configs.py` asserts all `${VAR}` in SSOT are defined in every `*.env.example` file.
- **Ollama model count assertion** — `test_ollama_model_count` locks the expected 4 Ollama models in the SSOT.

### Changed (Phase 9)

- **`dev-local` environment** upgraded from small tier (`ollama/qwen3:8b`, thinking off) to medium tier (`ollama/deepseek-r1:14b`, thinking low) for reliable multi-step tool calling.
- **`gpu-runpod.json`** envVars upgraded from 4 basic settings to 17 production-grade settings with `maxWorkers: 3`.
- **Pydantic `ModelRef`** extended with `fallbacks: list[str]` field (backward-compatible default `[]`).

### Fixed (Phase 9)

- **`prod-cloud.env.example`** missing placeholder env vars (`OLLAMA_API_KEY`, `OLLAMA_GPU_URL`, `VLLM_RUNPOD_URL`) that caused gateway crash on environment switch.
- **`gpu-runpod.env.example`** missing placeholder env vars (`OLLAMA_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) that caused gateway crash on environment switch.

### Added (prior)

- **Governance remediation baseline ledger** — `docs/SOP.md` now records the locked constraints, reproducible baseline commands, captured Phase 0 outputs, and frozen acceptance criteria for phases 1-6.
- **Known issues** in `docs/uat/dashboard_smoke.md` — Version display mismatch, no-nodes (system.exe), config schema resolution notes.
- **Troubleshooting** in `docs/USER_GUIDE.md` §17 — "No nodes with system.exe available" (Nodes page) with fixes (sandbox/gateway host or pair a node).
- **Playwright integration** — `scripts/browser-smoke.py` supports `--playwright` and `--headed` for DOM-based UAT (dashboard health, agent visibility, Swagger health, Architect tools UI, Executor approval hint, workflow launch). HTTP-only mode when Playwright not installed.
- **Browser test group** — `py scripts/test.py browser` runs browser smoke; release gate invokes it when Playwright is available.
- **Custom AKOS MCP** — `scripts/mcp_akos_server.py` exposes `akos_health()`, `akos_agents()`, `akos_status()` for control plane self-check. Bootstrap deploys with resolved path.
- **MCP documentation** — GitHub commit retrieval (GITHUB_TOKEN, future `search_commits`, `show_commit`), cursor-ide-browser (Cursor IDE built-in, optional), Custom AKOS MCP setup in USER_GUIDE.
- **Phase-by-phase checklist** — `docs/DEVELOPER_CHECKLIST.md` pre-commit checklist (test, drift, browser smoke, release gate, CHANGELOG, docs).

- **`resolve_mcporter_paths()`** — shared helper in `akos/io.py` for idempotent cross-platform MCP path resolution. Exported in `akos/__init__.py`.
- **`scripts/resolve-mcporter-paths.py`** — standalone operator script to fix placeholder paths (`/opt/openclaw/workspace`) in `~/.mcporter/mcporter.json`. Supports `--config`, `--dry-run`.
- **Config metadata convention** — `CONTRIBUTING.md` documents that `_note`/`_comment` keys in JSON configs are documentation-only metadata.
- **`_note` in `openclaw.json.example`** — logging block documents Linux vs Windows path.
- **Session config alignment test** — `TestSessionConfigExampleAlignment` in `validate_configs.py` catches future model/example key drift.
- **Strict inventory verifier** — `scripts/legacy/verify_openclaw_inventory.py` added to enforce exact provider/model/agent/A2A contract with per-check PASS/FAIL output.
- **Runtime status normalization tests** — `tests/test_runtime_contract.py` validates deterministic runtime contract semantics.
- **Sensitive-key signal tests** — `tests/test_sensitive_key_signals.py` locks informational vs actionable schema signal behavior without exposing secret values.
- **Bootstrap inventory regression test** — `tests/test_bootstrap_full_inventory.py` ensures unresolved env vars never remove provider blocks.

### Changed

- **Config schema alignment** — `config/openclaw.json.example` and `akos/models.py` updated to OpenClaw v2026.2.x schema: `targetAllowlist` → `allow`, `pingPongTurns` → `maxPingPongTurns`, `session.typing` → `session.typingMode`, `suppressToolErrorWarnings` → `suppressToolErrors`. Resolves "Unrecognized key" validation errors on Config page.
- **Complete session key fix** — `openclaw.json.example` lines 173-174 now use `maxPingPongTurns` and `typingMode` (previously missed in the schema alignment commit).
- **Browser Windows resilience** — `scripts/browser-smoke.py` tries Microsoft Edge first on Windows, falls back to bundled Chromium then Firefox; returns SKIP (not crash) when all browsers fail.
- **Bootstrap auto-resolves** — `phase_mcp` re-resolves existing `~/.mcporter/mcporter.json` paths automatically (idempotent, no flag needed).
- **Playwright Phase 2** — `scripts/browser-smoke.py` architect_tools_ui and executor_approval_hint now navigate to `/agents`, use agent card selectors ("Architect (Read-Only Planner)", "Executor (Read-Write Builder)"), wait for networkidle, and return clearer failure messages.
- **requirements.txt** — Added `playwright>=1.40`, `mcp>=1.0.0` for browser-smoke and Custom AKOS MCP.
- **bootstrap** — MCP phase resolves absolute path for `mcp_akos_server.py` in deployed mcporter.json.
- **Runtime diagnostics contract** — `scripts/doctor.py` now normalizes `Runtime: unknown` to healthy when RPC probe/listener evidence is healthy, and verifies determinism across repeated probes.
- **Bootstrap provider policy** — `scripts/bootstrap.py` now force-syncs full provider inventory from `config/openclaw.json.example` and emits warnings for unresolved env-backed inputs instead of stripping providers.
- **Sensitive-key diagnostics clarity** — `scripts/doctor.py` classifies schema-sensitive key paths into `[config/schema] info` (env-backed/runtime-managed) or `[config/schema] action` (non-env-backed).
- **Browser smoke resilience on Windows** — `scripts/browser-smoke.py` runs Playwright browser attempts in isolated worker subprocesses so native crashes become SKIP/fallback results rather than process crashes.
- **Bootstrap env-file seeding** — `scripts/bootstrap.py` now auto-seeds `~/.openclaw/.env` from `config/environments/dev-local.env.example` when unresolved provider env vars are detected and no `.env` exists, preventing gateway `MissingEnvVarError` crashes on first run.
- **Provider apiKey format** — `config/openclaw.json.example` now uses `${VAR}` string substitution for `openai` and `anthropic` apiKeys (matching `baseUrl` convention) instead of `{source: "env", id: "VAR"}` objects, which OpenClaw 2026.2.x validates eagerly.
- **Explicit baseUrl for cloud providers** — `openai` and `anthropic` provider blocks in the template now include explicit `baseUrl` fields (`https://api.openai.com/v1`, `https://api.anthropic.com`) required by OpenClaw 2026.2.x schema validation.
- **dev-local.env.example** — Now defines all env vars referenced in the template (`OLLAMA_GPU_URL`, `VLLM_RUNPOD_URL`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) with safe placeholders.
- **Provider namespace fix** — `ollama-local` renamed to `ollama` in `openclaw.json.example`, tests, and docs so the provider key matches the `ollama/` prefix used in all model strings. Resolves `Unknown model: ollama/qwen3:8b` on gateway startup.
- **Native Ollama API mode** — Local Ollama providers (`ollama`, `ollama-gpu`) switched from `api: "openai-completions"` to `api: "ollama"` and `baseUrl` dropped the `/v1` suffix, per upstream docs requiring native API for reliable tool calling.

---

## [0.5.0] -- 2026-03-08

Gateway runtime wiring (Option B): bootstrap as translation layer between AKOS SSOT and OpenClaw runtime enforcement.

### Added

- **Per-agent tool profiles** in `openclaw.json.example` — Orchestrator and Architect: `minimal` profile with explicit allowlists; Executor: `coding`; Verifier: `coding` with deny for write_file, delete_file, git_push, git_commit.
- **Top-level tools config** — exec security (allowlist, on-miss, sandbox), loop detection (warning/critical/circuit-breaker thresholds), agent-to-agent (enabled, target allowlist).
- **Session and browser config** — session scope, idle reset (60 min), typing mode, agent-to-agent ping-pong; browser headless, SSRF policy (dangerouslyAllowPrivateNetwork: false).
- **Bootstrap translation layer** — `_sync_tool_profiles_from_capability_matrix()` reads `config/agent-capabilities.json` and translates to per-agent OpenClaw `tools` blocks (profile, allow, deny).
- **Pydantic models** — `AgentToolProfile`, `ExecConfig`, `LoopDetectionConfig`, `AgentToAgentConfig`, `SessionConfig`, `BrowserConfig` in `akos/models.py`.
- **Drift detection** — `check_tool_profiles()` verifies tool profile alignment, exec security, loop detection, agent-to-agent per capability matrix.
- **Doctor script** — `check_gateway_tool_config()` for tool profile alignment, exec security mode, loop detection, browser SSRF policy.
- **AKOS / OpenClaw Responsibility Matrix** in `docs/ARCHITECTURE.md` — full component ownership map.
- **Bootstrap Translation Layer** and **Gateway Runtime Wiring** documentation in ARCHITECTURE.md, SOP.md, USER_GUIDE.md, SECURITY.md.

### Changed

- **Version bump**: `akos/__init__.py` 0.4.0 -> 0.5.0.
- **Integration layer** in README: "8 MCP servers" -> "8 MCP servers + gateway-enforced tool profiles".
- **Gateway-agnostic design** bullet and responsibility matrix link in README.

---

## [0.4.1] -- 2026-03-08

Bugfix release addressing 10 issues found during browser UAT testing.

### Fixed

- **Gateway crash on missing env vars** -- bootstrap now strips provider blocks with unresolved `${VAR}` references (e.g., `${OLLAMA_GPU_URL}`) when the env var is not set. Only configured providers are written to live `openclaw.json`.
- **Only 2 of 4 agents in dashboard** -- bootstrap now force-syncs `agents.list` from the template, ensuring all 4 agents (Orchestrator, Architect, Executor, Verifier) are always present regardless of pre-existing config.
- **Unknown config keys in `openclaw doctor`** -- AKOS-specific keys (`logging`, `permissions`, `gateway.host`) are now extracted into a separate `~/.openclaw/akos-config.json` sidecar file instead of being written to the gateway config.
- **Missing session directories** -- bootstrap now creates `~/.openclaw/agents/<id>/sessions/` for all 4 agents.
- **Gateway health probe timeout** -- reduced from 5s to 2s to avoid delaying `/health` responses when gateway is down.

### Added

- **Swagger API tags** -- 22 endpoints grouped into 8 categories (Health, Agents, Runtime, Context, RunPod, Metrics, Prompts, Checkpoints) for better Swagger UI navigation.
- **`/runtime/drift` description** -- added summary and description to the drift endpoint in Swagger.
- **`/status` hint** -- returns actionable guidance when no environment is selected.
- **Bootstrap variant logging** -- logs which prompt variant (compact/standard/full) was deployed.

---

## [0.4.0] -- 2026-03-08

Major upgrade synthesizing 7 improvement proposals into a 9-phase execution ladder.
Transforms the system from a well-architected scaffold into a productized, self-verifying,
policy-enforced, workflow-native agent platform. 193 tests (191 pass, 2 skipped live).

### Added

#### Phase 0 -- Runtime Convergence
- Bootstrap now deploys all 4 agent workspaces (Orchestrator, Architect, Executor, Verifier); previously only Architect and Executor were created.
- Scaffold files (IDENTITY.md, MEMORY.md, HEARTBEAT.md) deployed to all workspaces during bootstrap via `deploy_scaffold_files()`.
- Real HTTP gateway health probe replacing the static `"unknown"` stub in `/health`.
- Cross-platform MCP path resolution in bootstrap -- `mcporter.json` is generated with OS-appropriate paths instead of hardcoded `/opt/openclaw/workspace`.
- Bearer token API authentication via `AKOS_API_KEY` environment variable on all endpoints except `/health`.
- `--api-key` flag on `scripts/serve-api.py` for CLI-based auth configuration.
- `scripts/check-drift.py` -- runtime drift detector comparing repo state against live runtime.
- `/runtime/drift` API endpoint for programmatic drift detection.
- `akos/io.py`: `resolve_workspace_path()` for cross-platform path resolution, `deploy_scaffold_files()` for workspace hydration.
- `drift` test group in `scripts/test.py`.

#### Phase 1 -- Self-Verifying Agents
- Post-edit verification protocol in Executor: mandatory lint/test after every file write.
- Loop detection in Orchestrator and Executor: escalates to user after 3 identical failures.
- Proactive memory hygiene directive in all 4 agent base prompts.
- Package manager enforcement in Executor: never manually edit dependency files.
- Cost-aware tool heuristics in Orchestrator: prefer smallest set of high-signal calls.

#### Phase 2 -- Structured Planning Protocol
- `prompts/overlays/OVERLAY_PLAN_TODOS.md` -- structured planning overlay with conditional triggers (plan when multi-file/complex, skip when trivial).
- `RULES.md` scaffold in all 4 workspace scaffolds for user-defined conventions.
- RULES.md session-start directive in all base prompts: agents read and apply user rules.
- Conditional tasklist triggers in Orchestrator base prompt.
- OVERLAY_PLAN_TODOS wired into `standard` (Orchestrator, Architect) and `full` (+ Executor) tiers.

#### Phase 3 -- Role-Safe Capability Enforcement
- `config/agent-capabilities.json` -- role capability matrix as SSOT for per-agent tool access.
- `akos/policy.py` -- policy engine for loading capability matrix, generating tool profiles, and checking drift.
- `/agents/{id}/policy` API endpoint returning effective tool policy for any agent.
- `/agents/{id}/capability-drift` API endpoint for runtime capability audit.

#### Phase 4 -- Semantic Code Intelligence
- `prompts/overlays/OVERLAY_RESEARCH.md` -- research protocol with citation requirements, source usage, and context efficiency rules.
- LSP MCP server entry in `mcporter.json.example` (`@akos/mcp-lsp-server`) for type-aware code navigation.
- Code-search MCP server entry (`@akos/mcp-code-search`) for semantic code search via ripgrep + tree-sitter.
- Code intelligence directives in Architect base prompt (go-to-definition, find-references, diagnostics).
- OVERLAY_RESEARCH wired into `full` tier for Architect.

#### Phase 5 -- Dashboard-First UX and Workflows
- 6 reusable workflow definitions in `config/workflows/`:
  - `analyze_repo.md` -- Architect + Orchestrator codebase analysis
  - `implement_feature.md` -- Architect + Executor + Verifier feature implementation
  - `verify_changes.md` -- Verifier verification suite
  - `browser_smoke.md` -- Verifier browser-based smoke test
  - `deploy_check.md` -- Architect + Verifier deployment readiness
  - `incident_review.md` -- Architect + Orchestrator root cause analysis

#### Phase 7 -- Deployment Pipeline and Operational Tooling
- `scripts/doctor.py` -- one-command system health check (gateway, workspaces, SOUL.md, MCP, RunPod, Langfuse, permissions).
- `scripts/sync-runtime.py` -- hydrate runtime from repo SSOT (assembles prompts, deploys scaffolds and SOUL.md).
- `scripts/release-gate.py` -- unified release gate running full test suite + drift check with PASS/FAIL verdict.

#### Phase 8 -- Evaluation Release Gates
- `tests/test_live_smoke.py` -- opt-in live provider smoke tests (`@pytest.mark.live`, requires `AKOS_LIVE_SMOKE=1`).
- `docs/uat/dashboard_smoke.md` -- 6 canonical browser smoke scenarios (dashboard_health, agent_visibility, architect_read_only, executor_approval_flow, workflow_launch, prompt_injection_refusal).
- `live` test group in `scripts/test.py`.
- `live` pytest marker registered in `pyproject.toml`.

### Changed

- **Version bump**: `akos/__init__.py` version `0.3.0` -> `0.4.0`, FastAPI app version updated.
- **Bootstrap**: creates all 4 workspaces (was 2), deploys scaffold files, generates resolved `mcporter.json`.
- **API authentication**: all endpoints except `/health` now enforce bearer token when `AKOS_API_KEY` is set.
- **Model tiers**: `config/model-tiers.json` updated with OVERLAY_PLAN_TODOS in standard/full and OVERLAY_RESEARCH in full.
- **MCP topology**: expanded from 6 to 8 servers (added `lsp`, `code-search`).
- **Conftest**: `EXPECTED_MCP_SERVERS` updated to 8.
- **Test assertion**: relaxed Architect-vs-Executor size comparison (Executor now legitimately larger due to operational directives).
- Updated `docs/ARCHITECTURE.md`, `README.md`, `CONTRIBUTING.md`, `docs/USER_GUIDE.md` for v0.4.0.

### Fixed

- `RunPodEndpointConfig` was duplicated in both `akos/models.py` and `akos/runpod_provider.py`; removed the duplicate from `runpod_provider.py` (now imports from `models.py`).
- `ToolRegistry` and `ToolInfo` were not exported from `akos/__init__.py`; now included in `__all__`.
- Gateway health always returned `"unknown"`; now performs real HTTP probe to `127.0.0.1:18789`.

### Security

- API endpoints protected by bearer token authentication (opt-in via `AKOS_API_KEY`).
- Role capability matrix enforces tool access at the configuration layer, not just via prompt instructions.
- Architect denied write/shell/browser-mutate tools in `agent-capabilities.json`.

---

## [0.3.0] -- 2026-03-08

Major upgrade expanding the dual-agent system into a production-grade multi-agent LLMOS with
capabilities drawn from Cursor, Manus, Devin, Replit, and v0. 191 tests pass.

### Added

- **Orchestrator Agent**: task decomposition, parallel delegation, progress tracking, error escalation.
- **Verifier Agent**: lint/test/build/browser validation, fix suggestions with HIGH/MEDIUM/LOW confidence, 3-attempt escalation.
- **RunPod deep integration**: `akos/runpod_provider.py` typed SDK wrapper with endpoint lifecycle, health monitoring, scaling, inference, GPU discovery. Full `gpu-runpod.json` profile. Auto-provision on `switch-model.py`. Health monitoring in `log-watcher.py`.
- **FastAPI control plane**: `akos/api.py` with 12 endpoints (`/health`, `/status`, `/switch`, `/agents`, `/runpod/health`, `/runpod/scale`, `/metrics`, `/alerts`, `/prompts/assemble`, `/checkpoints`, `/checkpoints/restore`, `/logs` WebSocket). `scripts/serve-api.py` launcher.
- **MCP expansion**: 3 new servers (memory, filesystem, fetch) -- total 6.
- **Dynamic tool registry**: `akos/tools.py` with HITL classification from `permissions.json`.
- **Workspace checkpoints**: `akos/checkpoints.py` for snapshot/restore via tarballs.
- **Context compression**: `OVERLAY_CONTEXT_MANAGEMENT.md` for large+ models.
- **Deployment/Multi-Task/Browser-First** response modes in prompts.
- **EU AI Act** checklist updated with RunPod, Verifier, and checkpoint evidence.
- **Tests**: `test_runpod_provider.py` (21), `test_api.py` (13), `test_checkpoints.py` (9), `test_e2e_pipeline.py` (18). Total: 191.
- **Docs**: `docs/USER_GUIDE.md` comprehensive 21-section product manual.

### Changed

- Executor error recovery upgraded from 2-retry abort to 3-retry Verifier-guided loop.
- `model-tiers.json` updated with per-agent overlay filters for 4 agents.
- `config/permissions.json` expanded to 15 autonomous + 18 approval-gated tools.
- All documentation rewritten for 4-agent model.

---

## [0.2.0] -- 2026-03-02

Established the `akos/` orchestration library, multi-model architecture, and observability stack.

### Added

- **`akos/` library**: `models.py` (Pydantic schemas), `io.py` (shared I/O), `log.py` (structured JSON logging), `process.py` (subprocess hardening with timeouts), `state.py` (deployment state tracking), `telemetry.py` (Langfuse integration), `alerts.py` (SOC alert evaluation).
- **Multi-model tier registry**: `config/model-tiers.json` with small/medium/large/sota tiers.
- **Prompt tiering**: base + overlay assembly (`scripts/assemble-prompts.py`) producing compact/standard/full variants.
- **Multi-provider config**: 5 provider blocks in `openclaw.json.example` (ollama, ollama-gpu, openai, anthropic, vllm-runpod).
- **Environment profiles**: `dev-local`, `gpu-runpod`, `prod-cloud` with `.env.example` + `.json` overlay pairs.
- **Cross-platform switch-model**: `scripts/switch-model.py` with atomic config merge, prompt deploy, gateway restart, rollback safety.
- **Cross-platform bootstrap**: `scripts/bootstrap.py` (Python, any OS) complementing `bootstrap.ps1`.
- **Langfuse telemetry**: `scripts/log-watcher.py` with `--dry-run` and `--once` flags, later extended to the `~/.openclaw/.env` + local-mirror contract.
- **Alert evaluation engine**: `akos/alerts.py` with real-time pattern matching and periodic baseline checks.
- **Agent-filtered overlays**: `OVERLAY_REASONING.md` for Architect/Orchestrator only in standard+ tiers.
- **EU AI Act checklist** updated with verification dates and Langfuse evidence.
- **Session Startup** blocks in SOUL.md prompts and workspace scaffold to eliminate ENOENT errors.

### Changed

- SOUL.md prompts hardened for small models: under 40 lines, `MUST` directives, word-count limits, decision tables.
- Ollama `num_ctx` documentation and Modelfile guidance added.
- All scripts standardized on `akos/` library imports (no more duplicated helpers).

### Fixed

- Cross-platform path handling across Windows, macOS, and Linux.
- Type hints added throughout `akos/` library.
- Duplicated helper functions consolidated into `akos/io.py`.
- Langfuse import compatibility with Python 3.14.

---

## [0.1.0] -- 2026-03-01

Initial implementation scaffolding -- dual-agent architecture wired into live OpenCLAW runtime.

### Added

- **SOP**: comprehensive Standard Operating Procedure (Sections 1.0--8.0) with 33 traceable tasks across 6 phases.
- **LLMOS config scaffolding**: `openclaw.json.example`, `mcporter.json.example`, `permissions.json`, `logging.json`, `intelligence-matrix-schema.json`.
- **Dual-agent prompts**: `ARCHITECT_PROMPT.md` (read-only planner) and `EXECUTOR_PROMPT.md` (read-write builder).
- **Security**: `vet-install.sh` safe skill installation wrapper via `skillvet`.
- **70 validation tests**: JSON integrity, Pydantic model validation, cross-file references, secret scanning, SOP task coverage.
- **Live wiring**: dual-agent architecture connected to `~/.openclaw/openclaw.json` with `agents.list` schema.
- **Identity schema corrections**: object format (not string path), SOUL.md workspace pattern, thinkingDefault for Ollama.
- **Tool visibility**: `verboseDefault: "on"` and adaptive response modes.
- **MCP servers**: sequential-thinking, playwright, github (3 initial servers).
- **EU AI Act compliance**: initial checklist in `config/compliance/eu-ai-act-checklist.json`.
- **Bootstrap**: `scripts/bootstrap.ps1` for Windows PowerShell.

### Documentation

- `docs/SOP.md` -- full Standard Operating Procedure.
- `docs/ARCHITECTURE.md` -- Four-Layer LLMOS architecture.
- `SECURITY.md` -- Zero-Trust security policy.
- `CONTRIBUTING.md` -- contribution guidelines.
- `README.md` -- project overview and quick start.

---

## [0.0.1] -- 2026-03-01

Project inception.

### Added

- Initial commit: enterprise LLMOS blueprint document (`docs/SOP.md`).
- Repository structure established.
- MIT License.

---

[0.4.0]: https://github.com/FraysaXII/openclaw-akos/compare/v0.3.0...feature/phase-4-8-full-v04
[0.3.0]: https://github.com/FraysaXII/openclaw-akos/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/FraysaXII/openclaw-akos/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/FraysaXII/openclaw-akos/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/FraysaXII/openclaw-akos/releases/tag/v0.0.1
