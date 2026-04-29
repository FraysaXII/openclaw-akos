# Developer Checklist

Per [CONTRIBUTING.md](../CONTRIBUTING.md), run this phase checklist before every commit that touches features or tooling.

## Pre-commit Checks

### Tests and Gates

| Step | Command | Purpose |
|:-----|:--------|:--------|
| 1 | `py scripts/legacy/verify_openclaw_inventory.py` | Strict full AKOS inventory must pass (`OVERALL: PASS`) |
| 2 | `py scripts/check-drift.py` | No drift (repo vs runtime), including agent/A2A inventory, legacy `tools.allow`, and unknown runtime tool IDs |
| 3 | `py scripts/test.py all` | Full regression suite passes |
| 3a | `py scripts/test.py graph` | HLK graph lane (`pytest -m graph`); use with Bolt env + `pytest -m "graph and neo4j"` when changing Neo4j wiring |
| 4 | `py scripts/browser-smoke.py --playwright` | Browser smoke; HTTP path includes **Scenario 0 registry** scenarios (`scenario0_*`) against live `serve-api`. On Windows + **Python 3.14+** preview builds, Playwright Chromium may **crash** (`0xC0000005`); use **Python 3.12.x** for the venv that runs Playwright, or rely on HTTP-only + Cursor IDE Browser MCP for dashboard UAT. If **`release-gate`** fails only on this step with **exit 1**, read scenario details: architect/executor checks use **control plane** `GET /agents` (not OpenClaw gateway DOM). Exit **2** in `release-gate` is treated as a soft pass (worker/browser unavailable). |
| 5 | `py -m pytest tests/test_api.py tests/test_madeira_interaction.py -v` | FastAPI control plane + Madeira interaction mode smoke |
| 6 | `py scripts/release-gate.py` | Unified gate must report PASS (includes HLK vault validation). Optional: `AKOS_EVAL_RUBRIC=1` adds offline `run-evals.py` rubric slice. |
| 6a | `py scripts/run-evals.py run --suite pathc-research-spine --mode rubric` | When changing eval suites or `akos/eval_harness.py` |
| 7 | `py scripts/validate_hlk.py` | HLK canonical vault integrity — includes **`COMPONENT_SERVICE_MATRIX.csv`** and **`FINOPS_COUNTERPARTY_REGISTER.csv`** checks when those files exist (also run by release gate) |
| 7a | `py scripts/validate_hlk_vault_links.py` | Internal v3.0 markdown link integrity (also run by release gate) |
| 7b | `py scripts/merge_gtm_into_process_list.py` | Optional: merge GTM candidate CSV into `process_list.csv` after operator approval (`--write` applies) |
| 7c | `py scripts/merge_process_list_tranche.py` | Optional: merge a **canonical-column** candidate CSV (same header as `process_list.csv`) after operator approval (`--candidate path --write`) |
| 7d | `py scripts/verify.py compliance_mirror_emit` | **Preferred:** Initiative 14/16/21 mirror emit — preflight `--count-only` then writes `artifacts/sql/compliance_mirror_upsert.sql` (review before DB apply). Now also covers **GOI/POI**, **adviser disciplines/questions**, and **founder filed instruments** (Initiative 21). Requires DDL on target DB ([`supabase/migrations/`](../supabase/migrations/)). Run `py scripts/validate_hlk.py` / release gate when CSVs change first. |
| 7d-alt | `py scripts/sync_compliance_mirrors_from_csv.py` | Advanced: same script as 7d with manual `--count-only` / `--output` / `--finops-counterparty-register-only` / `--goipoi-register-only` / `--adviser-disciplines-only` / `--adviser-questions-only` / `--founder-filed-instruments-only` flags (argv SSOT for operators is profile **`compliance_mirror_emit`**) |
| 7e | `py scripts/verify.py export_adviser_handoff_smoke` | **Initiative 21 / P7:** render the External Adviser Engagement (ADVOPS) handoff bundle for **all disciplines** as Markdown to `artifacts/exports/handoff-smoke.md`. Operator runs before sending real handoffs. Underlying script: `py scripts/export_adviser_handoff.py --discipline {legal,fiscal,ip,banking,certification,notary,all} --format {md,pdf} --out <path>`. Reads SSOTs `ADVISER_ENGAGEMENT_DISCIPLINES.csv`, `GOI_POI_REGISTER.csv`, `ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`. |
| 7e-pdf | `py scripts/verify.py export_adviser_handoff_pdf_smoke` | **Initiative 22 / P6:** PDF output of the same bundle. Renderer chain: WeasyPrint → fpdf2 → pandoc. Optional install: `py -m pip install --only-binary=:all: -r requirements-export.txt`. SKIPs gracefully when no renderer is available (writes markdown only). |
| 7f | `py scripts/render_km_diagrams.py <path>.mmd --update-manifest` | **Initiative 22 / P5:** render an HLK KM Mermaid source to deterministic PNG + SVG sidecars and refresh the manifest's `file_sha256`. Uses `mmdc` if on PATH, falls back to the public `mermaid.ink` HTTP API otherwise. |
| 7e | `py scripts/stripe_set_billing_plane.py` | Optional (Initiative 14 Wave B3): set Stripe `metadata.hlk_billing_plane` on a test Customer/Subscription — requires `STRIPE_SECRET_KEY` in env (not committed) |
| 7f | `py scripts/verify_phase3_mirror_schema.py` | Optional (Initiative 14 Wave B): run [`verify_staging.sql`](../scripts/sql/i14_phase3_staging/verify_staging.sql) via `psql` when `DATABASE_URL` or `SUPABASE_DB_URL` is set; use `--skip-if-no-db` in environments without Postgres |
| 7g | `py scripts/refine_gtm_process_hierarchy.py` | Optional: Pattern 2 cluster parents + `item_name` cleanup on existing GTM rows (`--write` applies) |
| 8 | `py scripts/validate_hlk_km_manifests.py` | HLK KM visual manifests under `docs/references/hlk/v3.0/_assets/**/*.manifest.md` (run when those files change) |
| 9 | `py scripts/resolve-mcporter-paths.py` | If mcporter.json was copied manually (resolves placeholder paths) |

If you changed gateway tool policy, also verify the template uses gateway core IDs (`read`, `write`, `edit`, `apply_patch`, `exec`, etc.) and exposes MCP plugin tools through `tools.alsoAllow` rather than legacy `tools.allow`.

### Planning initiative closure (`docs/wip/planning/`)

When you mark an initiative **complete** or write a **phase completion** report: follow **`.cursor/rules/akos-planning-traceability.mdc`**. If the plan promised **browser**, **dashboard WebChat**, **Langfuse UI**, **Docker Desktop settings**, or other **manual** checks, add dated **`reports/uat-*.md`** with per-step PASS / SKIP / N/A (or link `docs/uat/` plus a stub with outcomes). **Playwright smoke** (step 4 above) is automated parity; it does **not** by itself replace qualitative UAT rows unless the initiative explicitly says so.

### Holistika Supabase (schema vs mirrors)

| Step | Command | Purpose |
|:-----|:--------|:--------|
| CLI essentials | `npx supabase login`, `npx supabase link --project-ref <REF>`, `npx supabase migration new …`, `npx supabase db push`, `npx supabase migration list` | Pinned CLI via `npx`; canonical contract in [`SOP-HLK_TOOLING_STANDARDS_001.md`](references/hlk/v3.0/Admin/O5-1/Tech/System%20Owner/SOP-HLK_TOOLING_STANDARDS_001.md) §3.1; DDL ledger in [`supabase/migrations/`](../supabase/migrations/); operator runbook in [`supabase/README.md`](../supabase/README.md) |
| Migration ledger parity | `npx supabase migration list` (after `link`) | Local and Remote columns must match before `npx supabase db push`; rename Git migration prefixes to remote versions or use `npx supabase migration repair` per [`supabase/migrations/README.md`](../supabase/migrations/README.md) |
| Mirror SQL emit | `py scripts/verify.py compliance_mirror_emit` | Data plane only; not a substitute for `validate_hlk.py` |

### Documentation Updates

| File | When to update |
|:-----|:----------------|
| `CHANGELOG.md` | Add entry under [Unreleased] or version |
| `README.md` | Version refs, new capabilities |
| `docs/ARCHITECTURE.md` | New components, diagrams |
| `docs/SOP.md` | New procedures (e.g., 9.12 Browser UAT) |
| `docs/USER_GUIDE.md` | New sections, UX changes |
| `SECURITY.md` | New deps, controls |
| `config/workspace-scaffold/README.md` | If scaffold changes |
| `CONTRIBUTING.md` | New test groups, deps |
| `docs/ARCHITECTURE.md` (Model Catalog) | Changes to `config/model-catalog.json` fields or `akos/model_catalog.py` |
| `docs/USER_GUIDE.md` (GPU deployment) | Changes to `scripts/gpu.py` subcommands or deploy flow |
| `docs/USER_GUIDE.md` (Finance MCP) | Changes to `akos/finance.py` or `scripts/finance_mcp_server.py` |
| `docs/ARCHITECTURE.md` (Finance) | Changes to finance response models or MCP tool signatures |
| `docs/ARCHITECTURE.md` (HLK) | Changes to `akos/hlk.py`, `akos/hlk_graph_model.py`, `akos/hlk_neo4j.py`, `akos/hlk_vault_links.py`, `akos/hlk_component_service_csv.py`, `akos/graph_stack.py`, `scripts/serve-api.py`, or `/hlk/*` and `/hlk/graph/*` API endpoints |
| `docs/references/hlk/v3.0/**/*.md` (links) | Run `py scripts/validate_hlk_vault_links.py` when editing cross-links |
| `docs/references/hlk/compliance/` | Changes to canonical vault CSVs or compliance taxonomy documents |
| `docs/references/hlk/v3.0/_assets/**/*.manifest.md` | Run `py scripts/validate_hlk_km_manifests.py`; update companion stubs if `source_id` changes |

## Playwright Setup (Optional)

For browser smoke DOM mode:

```bash
pip install playwright
playwright install chromium
py scripts/browser-smoke.py --playwright
```

On Windows, `browser-smoke.py` isolates browser launches in subprocess workers (engine order **chromium → msedge → firefox**). The parent parses `JSON_RESULTS:` from worker stdout **even when the worker exits non-zero** (failed scenarios vs misleading “unavailable”). If no engine emits parseable JSON, scenarios SKIP and the script exits `2` (release gate treats that as a soft PASS with a warning). Includes `hlk_graph_explorer` HTTP/DOM checks and **Scenario 0** HLK REST golden scenarios after Phase 1 dashboard checks.

## MCP Requirements

- **GitHub MCP:** Set `GITHUB_TOKEN` for repo metadata and future commit retrieval.
- **Custom AKOS MCP:** Requires `pip install mcp httpx`. Bootstrap deploys with resolved path.
- **Finance Research MCP:** Requires `pip install mcp yfinance`. Optional `ALPHA_VANTAGE_KEY` for sentiment and optional `FINNHUB_API_KEY` for better company-name search. Bootstrap deploys with resolved path.
- **HLK Registry MCP:** Requires `pip install mcp`. Read-only vault lookups over canonical CSVs. 8 tools: `hlk_role`, `hlk_role_chain`, `hlk_area`, `hlk_process`, `hlk_process_tree`, `hlk_projects`, `hlk_gaps`, `hlk_search`. Bootstrap deploys with resolved path.
- **cursor-ide-browser:** Cursor IDE built-in; enable in Cursor Settings if desired. Not required for AKOS.

## Workflow By Stage

### Before Commit

1. `py scripts/legacy/verify_openclaw_inventory.py`
2. `py scripts/check-drift.py`
3. `py scripts/test.py all`
4. `py scripts/browser-smoke.py --playwright`
5. `py -m pytest tests/test_api.py tests/test_madeira_interaction.py -v`
6. `py scripts/release-gate.py`

### Before PR / Merge

- Confirm the working tree is clean and drift-free
- Confirm docs were updated for any config, script, model, or rule change
- Confirm the release gate still passes after the final rebase or merge from main

### If The Gateway Seems Unhealthy

1. `py scripts/doctor.py`
2. `py scripts/check-drift.py`
3. `openclaw gateway status`
4. `py scripts/doctor.py --repair-gateway` (on Windows, also clears stale TCP listeners on 18789 after `gateway stop`)
5. If MCP behavior looks stale, re-run `py scripts/bootstrap.py --skip-ollama`
