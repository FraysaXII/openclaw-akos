# Contributing to OpenCLAW-AKOS

Thank you for your interest in contributing. This document provides guidelines to ensure a smooth collaboration process.

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

## Architecture

The system uses a **4-agent model** (Orchestrator, Architect, Executor, Verifier) with tiered prompt assembly, a FastAPI control plane, and RunPod GPU integration. Read `docs/ARCHITECTURE.md` and `docs/USER_GUIDE.md` before contributing to agent prompts, overlays, or the `akos/` library.

## Documentation Standards

This is primarily a documentation and configuration repository. Contributions should:

- Use clear, precise technical language
- Maintain the existing document structure and heading hierarchy
- Include version and date metadata where applicable
- Cite sources using numbered references consistent with the SOP format

### Config Metadata Keys

Keys starting with `_` (e.g. `_note`, `_comment`) in JSON config files are **documentation-only metadata**. Tooling must preserve them when generating or copying configs and must ignore them during validation and comparison.

### SOP Modifications

Changes to the Standard Operating Procedure (`docs/SOP.md`) require:

- A clear rationale in the PR description
- Verification that step-by-step procedures are accurate and reproducible
- Security impact assessment if the change touches sandboxing, networking, or credential management

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
  - `runpod>=1.7.0` -- RunPod GPU provider; graceful no-op without API key.
  - `fastapi>=0.115.0` -- Control plane API; only needed for `scripts/serve-api.py`.
  - `uvicorn>=0.32.0` -- ASGI server for FastAPI.
  - `httpx>=0.27.0` -- Async HTTP client for API tests.
  - `playwright>=1.40` -- Browser smoke DOM mode (optional; HTTP-only path when not installed).
  - `mcp>=1.0.0` -- Custom AKOS MCP server (`scripts/mcp_akos_server.py`).

## Testing Standards

- All Pydantic models must have corresponding tests in `tests/test_akos_models.py` covering both valid and invalid input.
- Alert conditions must have tests in `tests/test_akos_alerts.py` with synthetic log entries.
- RunPod provider operations must have mocked SDK tests in `tests/test_runpod_provider.py`.
- FastAPI endpoints must have TestClient tests in `tests/test_api.py`.
- New agent prompts/overlays must be covered by `tests/test_e2e_pipeline.py`.
- Role capability changes must update `config/agent-capabilities.json` and be tested via `/agents/{id}/policy` endpoint. Changes to `agent-capabilities.json` are automatically translated to OpenClaw tool profiles by bootstrap; do not hand-edit the `tools`, `session`, or `browser` sections in `openclaw.json.example` — they are generated from AKOS config.
- New workflow definitions go in `config/workflows/` as markdown files following the existing format.
- New overlay files must be registered in `config/model-tiers.json` `variantOverlays` section.
- Run the full suite before submitting: `py scripts/test.py` (193+ tests expected)
- Run specific groups: `py scripts/test.py api`, `py scripts/test.py security`, `py scripts/test.py browser`, etc.
- See all available groups: `py scripts/test.py --list`
- New test groups added in v0.4.0: `drift` (runtime drift detection), `live` (opt-in live provider smoke tests requiring `AKOS_LIVE_SMOKE=1`)
- Live smoke tests use `@pytest.mark.live` and are skipped by default
- Before releases, run the full verification matrix and release gate:
  - `py scripts/legacy/verify_openclaw_inventory.py`
  - `py scripts/check-drift.py`
  - `py scripts/test.py all`
  - `py scripts/browser-smoke.py --playwright`
  - `py -m pytest tests/test_api.py -v`
  - `py scripts/release-gate.py`
- Browser smoke tests: `py scripts/browser-smoke.py` (HTTP-only) or `py scripts/browser-smoke.py --playwright` (DOM mode; requires `pip install playwright && playwright install chromium`). On Windows crash-prone hosts, Playwright worker crashes are surfaced as `SKIP` outcomes.
- Agent evals: `py scripts/run-evals.py --dry-run` (5 canonical tasks)
- Checkpoint management: `py scripts/checkpoint.py create|list|restore`
- New eval tasks go in `tests/evals/tasks.json` following the existing schema.
- New session templates go in `config/templates/` as markdown files.
- New memory domain templates go in `config/memory-templates/`.
- New governance policy packs go in `config/policies/`.
- Rollback procedures are documented in `docs/uat/rollback_guide.md`.

## Pre-commit Checklist

Before every commit that touches features or tooling, run:

```
[ ] py scripts/legacy/verify_openclaw_inventory.py # Strict full inventory contract passes
[ ] py scripts/check-drift.py                      # No drift (repo vs runtime)
[ ] py scripts/test.py all                         # Full regression suite passes
[ ] py scripts/browser-smoke.py --playwright       # Browser smoke (SKIP allowed on Windows crash-prone hosts)
[ ] py -m pytest tests/test_api.py -v              # FastAPI control plane smoke
[ ] py scripts/release-gate.py                     # Unified release gate PASS
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
