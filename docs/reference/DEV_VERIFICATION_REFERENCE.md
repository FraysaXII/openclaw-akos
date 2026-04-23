# Developer verification reference

Single source of truth for **orchestrated** pre-commit and eval policy: [config/verification-profiles.json](../../config/verification-profiles.json). The interactive runner is [scripts/verify.py](../../scripts/verify.py) (`py scripts/verify.py pre_commit`).

## Golden-path commands (memorize these)

| Intent | Command |
|:-------|:--------|
| List verification profiles | `py scripts/verify.py --list` |
| Run the full default pre-commit chain (see registry) | `py scripts/verify.py pre_commit` |
| Compliance mirror SQL emit (Initiative 14/18) | `py scripts/verify.py compliance_mirror_emit` |
| Holistika Supabase migration ledger (DDL plane) | `npx supabase migration list` after `supabase link` | **Not** a `verify.py` profile. Local and Remote columns must match before `db push`; reconcile per [`supabase/migrations/README.md`](../../supabase/migrations/README.md) and [`supabase/README.md`](../../supabase/README.md) |
| Preview steps without running | `py scripts/verify.py pre_commit --dry-run` |
| Pytest by topic | `py scripts/test.py --list` then e.g. `py scripts/test.py madeira` or `py scripts/test.py intent` |
| All governance rubric eval suites (same set as `AKOS_EVAL_RUBRIC=1` in release gate) | `py scripts/run-evals.py run --governance-rubric` |
| Single eval suite | `py scripts/run-evals.py run --suite <suite_id> --mode rubric` |

`pre_commit` in [config/verification-profiles.json](../../config/verification-profiles.json) is equivalent to the former manual sequence: strict inventory, drift, `test.py all`, browser smoke with Playwright, API + Madeira pytest smoke, and `release-gate.py`.

## Eval and release gate

- **Offline rubric slice (governance list):** `py scripts/run-evals.py run --governance-rubric` — suite ids come from `eval_rubric_governance_suites` in the config file (not hardcoded in docs).
- **Release gate with rubric:** set `AKOS_EVAL_RUBRIC=1` when running `py scripts/release-gate.py` to include the same governance rubric pass.

## Optional tools (on demand)

| Step | Command | Purpose |
|:------|:--------|:--------|
| HLK graph lane | `py scripts/test.py graph` | After Neo4j/HLK graph work; with Bolt: `py -m pytest -m "graph and neo4j"` when `NEO4J_*` is set |
| Executor oracle (not default CI) | `py scripts/verify.py optional_executor_harness` with `AKOS_EXECUTOR_HARNESS=1` | See [CONTRIBUTING.md](../../CONTRIBUTING.md) |
| GTM / process list merge | `py scripts/merge_gtm_into_process_list.py` | After operator approval (`--write` applies) |
| Process list tranche | `py scripts/merge_process_list_tranche.py` | `--candidate path --write` after operator approval |
| Initiative 14/18 SQL mirror emit (preferred) | `py scripts/verify.py compliance_mirror_emit` | Writes `artifacts/sql/compliance_mirror_upsert.sql`; run after HLK gates when CSVs changed |
| Initiative 14/18 SQL mirror emit (manual argv) | `py scripts/sync_compliance_mirrors_from_csv.py` | `--count-only`, `--output`, or `--finops-counterparty-register-only` — prefer the profile above for SSOT |
| Stripe billing plane | `py scripts/stripe_set_billing_plane.py` | Needs `STRIPE_SECRET_KEY` (not committed) |
| Staging DB mirror check | `py scripts/verify_phase3_mirror_schema.py` | With `DATABASE_URL` or `SUPABASE_DB_URL` |
| GTM hierarchy refine | `py scripts/refine_gtm_process_hierarchy.py` | Optional `--write` |
| HLK KM manifests | `py scripts/validate_hlk_km_manifests.py` | When `v3.0/_assets/**/*.manifest.md` change |
| mcporter paths | `py scripts/resolve-mcporter-paths.py` | After manual `mcporter.json` copy |

## Gateway tool policy

If you changed gateway tool policy, ensure the template uses gateway core IDs (`read`, `write`, `edit`, `apply_patch`, `exec`, etc.) and exposes MCP plugin tools through `tools.alsoAllow` rather than legacy `tools.allow`.

## Playwright (browser smoke DOM)

```bash
pip install playwright
playwright install chromium
py scripts/browser-smoke.py --playwright
```

On Windows, `browser-smoke.py` uses subprocess workers (chromium → msedge → firefox). On **Python 3.14+** preview builds, Playwright Chromium may crash (`0xC0000005`); use **CPython 3.12.x** for Playwright or HTTP-only + Cursor Browser MCP. Exit code **2** = soft pass in release gate when no parseable JSON from workers.

## MCP requirements

- **GitHub MCP:** `GITHUB_TOKEN` for repo metadata.
- **Custom AKOS MCP:** `pip install mcp httpx` (bootstrap resolves path).
- **Finance Research MCP:** `pip install mcp yfinance`; optional `ALPHA_VANTAGE_KEY`, `FINNHUB_API_KEY`.
- **HLK Registry MCP:** `pip install mcp` — 8 read-only tools over canonical CSVs.
- **cursor-ide-browser:** optional in Cursor Settings.

## If the gateway seems unhealthy

1. `py scripts/doctor.py`
2. `py scripts/check-drift.py`
3. `openclaw gateway status`
4. `py scripts/doctor.py --repair-gateway` (Windows: may clear stale listeners on 18789)
5. `py scripts/bootstrap.py --skip-ollama` if MCP looks stale
