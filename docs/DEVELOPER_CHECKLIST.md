# Developer Checklist

Per [CONTRIBUTING.md](../CONTRIBUTING.md), run this phase checklist before every commit that touches features or tooling.

## Pre-commit Checks

### Tests and Gates

| Step | Command | Purpose |
|:-----|:--------|:--------|
| 1 | `py scripts/legacy/verify_openclaw_inventory.py` | Strict full AKOS inventory must pass (`OVERALL: PASS`) |
| 2 | `py scripts/check-drift.py` | No drift (repo vs runtime) |
| 3 | `py scripts/test.py all` | Full regression suite passes |
| 4 | `py scripts/browser-smoke.py --playwright` | Browser smoke; on Windows crash-prone hosts this may return SKIP instead of FAIL |
| 5 | `py -m pytest tests/test_api.py -v` | FastAPI control plane smoke |
| 6 | `py scripts/release-gate.py` | Unified gate must report PASS |
| 7 | `py scripts/resolve-mcporter-paths.py` | If mcporter.json was copied manually (resolves placeholder paths) |

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
| `docs/ARCHITECTURE.md` (HLK) | Changes to `akos/hlk.py`, HLK domain models, or `/hlk/*` API endpoints |
| `docs/references/hlk/compliance/` | Changes to canonical vault CSVs or compliance taxonomy documents |

## Playwright Setup (Optional)

For browser smoke DOM mode:

```bash
pip install playwright
playwright install chromium
py scripts/browser-smoke.py --playwright
```

On Windows, `browser-smoke.py` isolates browser launches in subprocess workers so native Playwright crashes (`0xC0000005`) become explicit SKIP outcomes instead of crashing the gate process.

## MCP Requirements

- **GitHub MCP:** Set `GITHUB_TOKEN` for repo metadata and future commit retrieval.
- **Custom AKOS MCP:** Requires `pip install mcp httpx`. Bootstrap deploys with resolved path.
- **Finance Research MCP:** Requires `pip install mcp yfinance`. Optional `ALPHA_VANTAGE_KEY` for sentiment and optional `FINNHUB_API_KEY` for better company-name search. Bootstrap deploys with resolved path.
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
4. `openclaw gateway restart`
5. If MCP behavior looks stale, re-run `py scripts/bootstrap.py --skip-ollama`
