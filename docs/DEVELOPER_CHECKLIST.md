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
| 4 | `py scripts/browser-smoke.py --playwright` | Browser smoke; on Windows crash-prone hosts this may return SKIP instead of FAIL. If **`release-gate`** fails only on this step with **exit 1**, read scenario details: architect/executor checks use **control plane** `GET /agents` (not OpenClaw gateway DOM). Exit **2** in `release-gate` is treated as a soft pass (worker/browser unavailable). |
| 5 | `py -m pytest tests/test_api.py -v` | FastAPI control plane smoke |
| 6 | `py scripts/release-gate.py` | Unified gate must report PASS (includes HLK vault validation). Optional: `AKOS_EVAL_RUBRIC=1` adds offline `run-evals.py` rubric slice. |
| 6a | `py scripts/run-evals.py run --suite pathc-research-spine --mode rubric` | When changing eval suites or `akos/eval_harness.py` |
| 7 | `py scripts/validate_hlk.py` | HLK canonical vault integrity (also run by release gate) |
| 7a | `py scripts/validate_hlk_vault_links.py` | Internal v3.0 markdown link integrity (also run by release gate) |
| 7b | `py scripts/merge_gtm_into_process_list.py` | Optional: merge GTM candidate CSV into `process_list.csv` after operator approval (`--write` applies) |
| 7c | `py scripts/refine_gtm_process_hierarchy.py` | Optional: Pattern 2 cluster parents + `item_name` cleanup on existing GTM rows (`--write` applies) |
| 8 | `py scripts/validate_hlk_km_manifests.py` | HLK KM visual manifests under `docs/references/hlk/v3.0/_assets/**/*.manifest.md` (run when those files change) |
| 9 | `py scripts/resolve-mcporter-paths.py` | If mcporter.json was copied manually (resolves placeholder paths) |

If you changed gateway tool policy, also verify the template uses gateway core IDs (`read`, `write`, `edit`, `apply_patch`, `exec`, etc.) and exposes MCP plugin tools through `tools.alsoAllow` rather than legacy `tools.allow`.

### Planning initiative closure (`docs/wip/planning/`)

When you mark an initiative **complete** or write a **phase completion** report: follow **`.cursor/rules/akos-planning-traceability.mdc`**. If the plan promised **browser**, **dashboard WebChat**, **Langfuse UI**, **Docker Desktop settings**, or other **manual** checks, add dated **`reports/uat-*.md`** with per-step PASS / SKIP / N/A (or link `docs/uat/` plus a stub with outcomes). **Playwright smoke** (step 4 above) is automated parity; it does **not** by itself replace qualitative UAT rows unless the initiative explicitly says so.

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
| `docs/ARCHITECTURE.md` (HLK) | Changes to `akos/hlk.py`, `akos/hlk_graph_model.py`, `akos/hlk_neo4j.py`, `akos/hlk_vault_links.py`, `akos/graph_stack.py`, `scripts/serve-api.py`, or `/hlk/*` and `/hlk/graph/*` API endpoints |
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

On Windows, `browser-smoke.py` isolates browser launches in subprocess workers. The parent parses `JSON_RESULTS:` from worker stdout **even when the worker exits non-zero** (failed scenarios vs misleading “unavailable”). If no engine emits parseable JSON, scenarios SKIP and the script exits `2` (release gate treats that as a soft PASS with a warning). Includes `hlk_graph_explorer` HTTP/DOM checks.

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
5. `py -m pytest tests/test_api.py -v`
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
