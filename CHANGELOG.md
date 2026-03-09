# Changelog

All notable changes to the OpenCLAW-AKOS project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

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
- **Multi-provider config**: 5 provider blocks in `openclaw.json.example` (ollama-local, ollama-gpu, openai, anthropic, vllm-runpod).
- **Environment profiles**: `dev-local`, `gpu-runpod`, `prod-cloud` with `.env.example` + `.json` overlay pairs.
- **Cross-platform switch-model**: `scripts/switch-model.py` with atomic config merge, prompt deploy, gateway restart, rollback safety.
- **Cross-platform bootstrap**: `scripts/bootstrap.py` (Python, any OS) complementing `bootstrap.ps1`.
- **Langfuse telemetry**: `scripts/log-watcher.py` with `--env-file`, `--dry-run`, `--once` flags.
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
