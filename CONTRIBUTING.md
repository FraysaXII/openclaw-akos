# Contributing to OpenCLAW-AKOS

Thank you for your interest in contributing. This document provides guidelines to ensure a smooth collaboration process.

**New here?** See the [documentation map](docs/README.md) and the [first-time contributor guide](docs/guides/first_time_contributor.md) (tutorial-style path); then this file and [DEVELOPER_CHECKLIST](docs/DEVELOPER_CHECKLIST.md) for every-commit expectations.

## How to Contribute

### Reporting Issues

- Use GitHub Issues for bug reports, feature requests, and documentation improvements
- Search existing issues before creating a new one to avoid duplicates
- Provide clear reproduction steps, expected behavior, and actual behavior

### Submitting Changes

1. **Fork** the repository
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code and documentation standards below
4. **Commit** with clear, descriptive messages
5. **Push** to your fork and open a **Pull Request** against `main`

### Pull Request Guidelines

- Keep PRs focused on a single concern
- Reference related issues using `Closes #<issue-number>`
- Update documentation if your changes affect any SOP procedures, architecture descriptions, or configuration examples
- All MCP server configurations must include valid JSON syntax — validate before submitting
- **Governed multi-phase work** (runtime, inventory, Neo4j graph stack, etc.): land changes as **one atomic git commit per phase** with tests and required docs for that phase—see `.cursor/rules/akos-governance-remediation.mdc` and the verification matrix in `docs/DEVELOPER_CHECKLIST.md`

## Architecture

The system uses a **5-agent model** (Madeira, Orchestrator, Architect, Executor, Verifier) with tiered prompt assembly, a FastAPI control plane, and RunPod GPU integration. Read `docs/ARCHITECTURE.md` and `docs/USER_GUIDE.md` before contributing to agent prompts, overlays, or the `akos/` library.

## Documentation Standards

This is primarily a documentation and configuration repository. Contributions should:

- Use clear, precise technical language
- Maintain the existing document structure and heading hierarchy
- Include version and date metadata where applicable
- Cite sources using numbered references consistent with the SOP format

### Environment profiles (`config/environments/`)

Operative runtime inputs are the real `*.env` files paired with each `*.json` overlay. The `*.env.example` files are **reference-only** templates; `scripts/switch-model.py`, `scripts/gpu.py`, and other runtime paths must not fall back to them. First-run materialization of `~/.openclaw/.env` uses the shared `RUNTIME_ENV_PLACEHOLDERS` contract in `akos/io.py` (via `scripts/bootstrap.py`), not a silent copy of an example file.

### Config Metadata Keys

Keys starting with `_` (e.g. `_note`, `_comment`) in JSON config files are **documentation-only metadata**. Tooling must preserve them when generating or copying configs and must ignore them during validation and comparison.

### SOP Modifications

Changes to the Standard Operating Procedure (`docs/SOP.md`) require:

- A clear rationale in the PR description
- Verification that step-by-step procedures are accurate and reproducible
- Security impact assessment if the change touches sandboxing, networking, or credential management

## OpenClaw CLI upgrades (operator maintenance)

The OpenClaw npm package updates independently of this repo. When an upgrade is available (`openclaw status` shows a newer channel build):

1. Pick a maintenance window and run **`openclaw update`** (or the documented package manager equivalent).
2. **`openclaw gateway restart`** (or `openclaw gateway stop` / `start` on Windows Scheduled Task installs).
3. **`openclaw status --all`** — confirm gateway reachability and agent rows; prefer this over pasting secrets to chat.
4. **`py scripts/doctor.py`** — AKOS runtime and schema signals.
5. **AKOS gates:** at minimum `py scripts/legacy/verify_openclaw_inventory.py`, `py scripts/check-drift.py`, and `py scripts/release-gate.py`; full matrix in [docs/DEVELOPER_CHECKLIST.md](docs/DEVELOPER_CHECKLIST.md).

Upstream JSON schema may reject keys present in older templates; if `openclaw doctor` or gateway logs report **Unrecognized key**, align `config/openclaw.json.example` with the installed CLI and re-run **`py scripts/bootstrap.py`** (or `switch-model.py`) so `~/.openclaw/openclaw.json` merges the corrected shape.

## Python Code Standards

The `akos/` orchestration library and all scripts under `scripts/` follow these conventions:

- **Type hints required** on all function signatures and return types.
- **Pydantic models** for all configuration schemas -- never hand-write `assert` chains for JSON validation. Define a model in `akos/models.py` and call `Model.model_validate(data)`.
- **Shared utilities** live in `akos/io.py`. Never duplicate `load_json`, `deep_merge`, `resolve_openclaw_home`, or similar helpers in scripts.
- **Structured logging** via `akos/log.py`. All scripts call `setup_logging(json_output=args.json_log)` at startup and use `logging.getLogger(__name__)` instead of `print()`.
- **Subprocess calls** go through `akos/process.run()` with explicit timeouts. Never use bare `subprocess.run()` or `os.system()`.
- **Cross-platform**: use Python `pathlib.Path` and `os.environ` instead of shell-specific constructs. All scripts must work on Windows, macOS, and Linux without modification.

## Dependency Policy

- **Prefer stdlib.** Only add third-party packages when they eliminate significant complexity or duplication.
- **Security justification required.** Every new dependency must have a rationale documented in the PR description, per [SECURITY.md](SECURITY.md).
- **Current dependencies and justification:**
  - `pydantic>=2.0` -- Runtime type safety for all config schemas, Rust-backed core.
  - `langfuse>=2.0` -- Observability backend; graceful no-op when unconfigured.
  - `pytest>=7.0` -- Test runner.
  - `runpod>=1.7.0` (in `requirements-gpu.txt`) -- RunPod GPU provider; graceful no-op without API key or without installing the extra file.
  - `openstacksdk>=4.0.0` (in `requirements-openstack.txt`) -- ShadowGPU (OpenStack) provider; graceful no-op when the SDK is not installed.
  - `fastapi>=0.115.0` -- Control plane API; only needed for `scripts/serve-api.py`.
  - `neo4j>=5.14.0` -- Optional HLK graph mirror (`scripts/sync_hlk_neo4j.py`, `scripts/hlk_graph_mcp_server.py`, `/hlk/graph/*`); no-op when `NEO4J_*` unset.
  - `streamlit>=1.28.0`, `streamlit-agraph>=0.0.45`, `networkx>=3.2` -- Optional operator graph UI (`scripts/hlk_graph_explorer.py`; vis physics by default, NetworkX optional initial seed / static layout). Optional env **`AKOS_WEB_DASHBOARD_URL`** adds a shell link when WebChat is not on the API host.
  - `uvicorn>=0.32.0` -- ASGI server for FastAPI.
  - `httpx>=0.27.0` -- Async HTTP client for API tests.
  - `playwright>=1.40` -- Browser smoke DOM mode (optional; HTTP-only path when not installed). **Supported interpreters:** use **CPython 3.12.x** (or 3.11) for the environment that runs `py scripts/browser-smoke.py --playwright`; **Python 3.14** preview builds have been observed to crash Playwright’s bundled Chromium on Windows (`0xC0000005`). HTTP-only smoke and **Cursor IDE Browser** MCP remain valid for gates and UAT when Playwright is unstable.
  - `mcp>=1.0.0` -- Custom AKOS MCP servers (`scripts/mcp_akos_server.py`, `scripts/finance_mcp_server.py`).
  - `yfinance>=0.2.36` -- Finance research data (optional; finance MCP degrades gracefully without it).

## Testing Standards

- All Pydantic models must have corresponding tests in `tests/test_akos_models.py` covering both valid and invalid input.
- Alert conditions must have tests in `tests/test_akos_alerts.py` with synthetic log entries.
- RunPod provider operations must have mocked SDK tests in `tests/test_runpod_provider.py`.
- PodManager (dedicated pod lifecycle) must have tests in `tests/test_pod_manager.py`.
- GPU CLI, model catalog, and deploy flow must have tests in `tests/test_gpu_cli.py` (catalog validation, VRAM-driven GPU selection, vLLM command generation, deploy/teardown mocked, env propagation, overlay JSON wiring).
- Environment/profile activation changes must have tests in `tests/test_switch_model.py`.
- Bootstrap inventory/env-materialization changes must have tests in `tests/test_bootstrap_full_inventory.py`.
- Gateway runtime normalization and recovery changes must have tests in `tests/test_runtime_contract.py`.
- Strict inventory verifier changes must have tests in `tests/test_verify_openclaw_inventory.py`.
- FastAPI endpoints must have TestClient tests in `tests/test_api.py`.
- Langfuse telemetry changes must have tests in `tests/test_telemetry.py` (init, trace paths, metadata contract, sampling, env normalization, flush/shutdown). See `docs/ARCHITECTURE.md` § Langfuse metadata contract for allowed keys.
- Failover router changes must have tests in `tests/test_router.py` (10 tests covering failover threshold, recovery, and multi-provider routing).
- Finance service changes must have tests in `tests/test_finance.py` (normalization, caching, missing API key degradation, error states).
- HLK domain changes must have tests in `tests/test_hlk.py` (model parsing, registry lookups, chain traversal, gap detection, API endpoints).
- `scripts/browser-smoke.py` Scenario 0 evaluators must stay covered by `tests/test_browser_smoke_scenario0_evaluators.py` when golden expectations change.
- Intent routing / `config/intent-exemplars.json`: run `py scripts/test.py intent` (or `py -m pytest -m intent`); optional before/after table via `py scripts/intent_benchmark.py` (requires repo root on `PYTHONPATH`; uses live Ollama embeddings when available).
- OpenStack provider request-shape changes must have tests in `tests/test_openstack_provider.py`.
- New agent prompts/overlays must be covered by `tests/test_e2e_pipeline.py`.
- Role capability changes must update `config/agent-capabilities.json` and be tested via `/agents/{id}/policy` endpoint. Bootstrap derives each agent's runtime `tools.profile` from the capability matrix, while `config/openclaw.json.example` remains the SSOT for curated gateway `alsoAllow` / `deny`, session, and browser semantics. Keep those layers aligned; do not treat the gateway template as disposable generated output.
- New workflow definitions go in `config/workflows/` as markdown files following the existing format.
- New overlay files must be registered in `config/model-tiers.json` `variantOverlays` section.
- Changes to `config/model-catalog.json` or `scripts/gpu.py` must be covered by `tests/test_gpu_cli.py`.
- Run the full suite before submitting: `py scripts/test.py` (300+ tests expected, including `test_pod_manager.py`, `test_gpu_cli.py`, `test_finance.py`)
- Run specific groups: `py scripts/test.py api`, `py scripts/test.py security`, `py scripts/test.py browser`, etc.
- See all available groups: `py scripts/test.py --list`
- New test groups added in v0.4.0: `drift` (runtime drift detection), `live` (opt-in live provider smoke tests requiring `AKOS_LIVE_SMOKE=1`)
- New test groups added in RunPod+Langfuse overhaul: `telemetry` (Langfuse reporter lifecycle, trace taxonomy, env normalization), `router` (FailoverRouter threshold, recovery, multi-provider)
- New test group added in HLK Phase 2: `hlk` (HLK domain models, registry service, API endpoints)
- `madeira` and `intent` groups: `py scripts/test.py madeira` / `py scripts/test.py intent` (`@pytest.mark.madeira` / `intent`)
- Graph lane: `graph` (`pytest -m graph` via `py scripts/test.py graph`); live Bolt tests use `@pytest.mark.neo4j` (`python -m pytest -m "graph and neo4j"` when `NEO4J_*` is set)
- Live smoke tests use `@pytest.mark.live` and are skipped by default
- Default pre-commit chain (orchestrated from [config/verification-profiles.json](config/verification-profiles.json)): `py scripts/verify.py pre_commit` (see `py scripts/verify.py --list`). **Holistika compliance mirror SQL emit (not part of pre-commit):** `py scripts/verify.py compliance_mirror_emit` after HLK gates when CSVs change. For releases, also run the full `release-gate` (below).
- Before releases, run the full verification matrix and release gate (equivalent to `pre_commit` profile plus final checks):
  - `py scripts/verify.py pre_commit` **or** the same steps listed in `config/verification-profiles.json` / [docs/DEVELOPER_CHECKLIST.md](docs/DEVELOPER_CHECKLIST.md)
- HLK KM visual manifests: when editing `docs/references/hlk/v3.0/_assets/**/*.manifest.md`, run `py scripts/validate_hlk_km_manifests.py`. New manifests follow the **`<plane>/<program_id>/<topic_id>/`** convention (Initiative 22 P2; see `docs/references/hlk/v3.0/_assets/README.md`). When the manifest references a `paths.mermaid` source-of-truth, regenerate the raster via `py scripts/render_km_diagrams.py <topic>.mmd --update-manifest` (uses `mmdc` if installed via `npm i -g @mermaid-js/mermaid-cli`, else falls back to the public `mermaid.ink` HTTP API).
- HLK Adviser handoff PDF rendering (Initiative 22 P6, opt-in): install with `py -m pip install --only-binary=:all: -r requirements-export.txt` (adds `weasyprint`, `fpdf2`, `markdown`). The renderer chain is WeasyPrint → fpdf2 → pandoc; on Windows without GTK3 runtime the pure-Python `fpdf2` path is used automatically. Smoke profile: `py scripts/verify.py export_adviser_handoff_pdf_smoke`.
- HLK compliance mirror **drift probe** (Initiative 23 P4, operator-pasted): `py scripts/probe_compliance_mirror_drift.py --emit-sql` prints a JSON-shaped `SELECT` covering all 8 compliance mirrors. Run it via the `user-supabase` MCP `execute_sql` tool, save the JSON result into `artifacts/probes/mirror-drift-<YYYYMMDD>.json` (gitignored; only the README is tracked), then `py scripts/probe_compliance_mirror_drift.py --verify` (or the verify profile `compliance_mirror_drift_probe`). PASSes when canonical CSV row counts match live mirror counts; FAILs row-by-row on drift; **SKIPs gracefully (exit 0) when no fresh artifact exists** — CI never red on a probe operators have not refreshed. Cross-program glossary at [`docs/reference/glossary-cross-program.md`](docs/reference/glossary-cross-program.md) (Initiative 23 P5) is the SSOT for program codes, discipline codes, sensitivity bands, sharing labels, GOI/POI class taxonomy, status enums, and voice registers.
- Browser smoke tests: `py scripts/browser-smoke.py` (HTTP-only) or `py scripts/browser-smoke.py --playwright` (DOM mode; requires `pip install playwright && playwright install chromium`). On Windows crash-prone hosts, Playwright worker crashes are surfaced as `SKIP` outcomes. **`release-gate.py` browser-smoke exit 1** with failures in `architect_tools_ui` / `executor_approval_hint` usually means **control plane `/agents` or Playwright env drift**, not a regression in the graph stack—Phase 2 asserts against the same **FastAPI** `/agents` SSOT as `agent_visibility` (not OpenClaw gateway card copy). Exit **2** (no parseable JSON from workers) is treated as a soft pass in `release-gate.py`.
- Agent evals: `py scripts/run-evals.py list` — list includes governance rubric suite ids from the verification config. **Governance rubric (all offline suites, same as `AKOS_EVAL_RUBRIC=1` in release gate):** `py scripts/run-evals.py run --governance-rubric`. **Single suite:** `py scripts/run-evals.py run --suite <suite_id> --mode rubric` (suites under `tests/evals/suites/<id>/`; legacy `tests/evals/tasks.json` for optional smoke). Optional Executor oracle: `AKOS_EXECUTOR_HARNESS=1` and `py scripts/verify.py optional_executor_harness` (or `py -m pytest tests/test_executor_harness_optional.py -m executor_harness`).
- Optional release gate slice: set `AKOS_EVAL_RUBRIC=1` when running `py scripts/release-gate.py` to include the offline rubric pass.
- **Path B on Windows:** Install **Docker Desktop 4.58+** (sandboxes) and/or **WSL2** for a Linux gateway; ensure Docker **File Sharing** includes `~/.openclaw` and your repo root. `py scripts/doctor.py` emits non-fatal Docker/WSL hints on Windows.
- Checkpoint management: `py scripts/checkpoint.py create|list|restore`
- New eval suites: add `manifest.json` + `tasks.json` under `tests/evals/suites/<suite_id>/` per `tests/evals/README.md`.
- New session templates go in `config/templates/` as markdown files.
- New memory domain templates go in `config/memory-templates/`.
- New governance policy packs go in `config/policies/`.
- Rollback procedures are documented in `docs/uat/rollback_guide.md`.

## Pre-commit Checklist

Before every commit that touches features or tooling, run:

```
[ ] py scripts/verify.py pre_commit                # One entry: full chain from config/verification-profiles.json
# Or `--dry-run` to print steps; for targeted work use `py scripts/test.py <group>` and see docs/DEVELOPER_CHECKLIST.md
[ ] py scripts/validate_hlk_km_manifests.py     # If HLK v3.0/_assets manifests changed
```

Update documentation as needed:

- [ ] CHANGELOG.md — Add entry under [Unreleased] or version
- [ ] README.md — Version refs, new capabilities
- [ ] docs/ARCHITECTURE.md — New components, diagrams
- [ ] docs/SOP.md — New procedures (e.g., 9.12 Browser UAT)
- [ ] docs/USER_GUIDE.md — New sections, UX changes
- [ ] SECURITY.md — New deps, controls
- [ ] config/workspace-scaffold/README.md — If scaffold changes
- [ ] CONTRIBUTING.md — New test groups, deps

See [docs/DEVELOPER_CHECKLIST.md](docs/DEVELOPER_CHECKLIST.md) for the full phase checklist.

## Security Contributions

Given the Zero-Trust posture of this project:

- **Never** commit API keys, tokens, or credentials
- **Never** add dependencies without a security justification
- All new skill integrations must pass `skillvet` scanning
- Review [SECURITY.md](SECURITY.md) before proposing changes to security-related procedures

## Code of Conduct

- Be respectful and constructive in all interactions
- Focus on technical merit when reviewing contributions
- Assume good intent from fellow contributors

## Questions?

Open a GitHub Discussion or reach out via the issue tracker.
