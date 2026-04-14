# Changelog

All notable changes to the OpenCLAW-AKOS project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Madeira read-only hardening** — Compact-tier overlays `OVERLAY_HLK_COMPACT.md` and `OVERLAY_STARTUP_COMPACT.md` for Madeira; `execution_escalate` intent for code/browser/MCP/multi-step execution via `akos_route_request` / `akos/intent.py`; `sequential_thinking` on Madeira allowlist; workspace scaffold `madeira/memory/README.md` and recursive scaffold deploy for `memory/`; log-watcher grounding flags and real-time eval alerts (`madeira_internal_tool_leak`, `madeira_pseudo_hlk_path_leak`, `madeira_suspect_uuid_hallucination`); USER_GUIDE security audit subsection and multi-model HLK admin smoke matrix. Traceability: `docs/wip/planning/02-hlk-on-akos-madeira/reports/madeira-readonly-hardening.md`.
- **HLK Envoy repository hub** — Canonical registry `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md` with policy README and `platform/`, `internal/`, `client-delivery/` stubs; `Think Big/README.md` for non-repo client artifacts; PMO pilot topic `TOPIC_PMO_CLIENT_DELIVERY_HUB.md`; vault `index.md` entity-placement guidance; `TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md` “Linked Git repositories” section; `PRECEDENCE.md` canonical/mirrored rows and “GitHub repositories vs vault authority”; planning traceability `docs/wip/planning/05-hlk-vault-envoy-repos/phase-1-plan.md`.
- **HLK KM follow-up (hygiene + UAT)** — Reconciled PMO Trello registry ids to the primary board export; added `PMO/imports/` with `trello_board_67697e19_primary.json`, `trello_board_67697e19_archive_slice.json`, and full formatted export; moved wip KM syntheses to `docs/wip/hlk-km/`; added `docs/wip/README.md` and `docs/wip/planning/99-proposals/` for loose plan files; relocated repo-root `_*.py` scratch scripts to `scripts/adhoc/`; HLK admin smoke **Scenario 8** for KM validators and registry checks; [km-plan-followup-checklist.md](docs/wip/planning/03-hlk-km-knowledge-base/reports/km-plan-followup-checklist.md) for incremental work without redoing the baseline rollout.
- **HLK governed KM (Topic–Fact–Source)** — Canonical contract `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md`, vault index updates, topic template and visual manifest example under Compliance, PMO `RESEARCH_BACKLOG_TRELLO_REGISTRY.md`, Output 1 pilot bundle under `v3.0/_assets/km-pilot/`, workspace roadmap `docs/wip/planning/03-hlk-km-knowledge-base/`, five `docs/wip/hlk-km/research-synthesis-*.md` stubs linked from the registry; Trello exports under PMO `imports/` with primary/archive split, and `scripts/validate_hlk_km_manifests.py` for manifest frontmatter and raster path checks.
- **HLK founder-governance case layer** — Add canonical case docs for entity-formation decisions, capitalization posture, ENISA evidence, trademark scope, Research-vs-Tech-Lab separation, and the founder-governance lifecycle/promotion ladder under role-owned `v3.0` paths.
- **HLK founder-governance SOPs** — Add canonical `v3.0` drafts for `Founder Entity Formation Readiness`, `Trademark and Naming Governance`, `Founder-to-Company Funding Path`, and `ENISA Readiness and Evidence Pack` under the role-owned Legal, Finance/Taxes, and Compliance paths.
- **HLK founder-governance registry rows** — Register matching workstreams/processes in `docs/references/hlk/compliance/process_list.csv` for founder entity formation, trademark control, founder funding, and ENISA readiness, increasing the canonical process inventory to 324 items.
- **Windows gateway port recovery** — `akos.runtime.recover_gateway_service()` now clears stale TCP listeners on port `18789` via `netstat`/`taskkill` after `gateway stop` on Windows, aligning with the `py scripts/doctor.py --repair-gateway` operator path and reducing post-reboot manual rescue.
- **Planning traceability** — `docs/wip/planning/02-hlk-on-akos-madeira/phase-7-plan.md` and `reports/phase-7-report.md` record the Gateway and GPU Recovery Hardening rollout (env contract, Windows supervision, operator runbooks).
- **ShadowPC OpenStack GPU provider** -- `akos/openstack_provider.py` provides full lifecycle management (instance creation, floating IP, security groups, teardown, spot termination detection) for Shadow's OpenStack GPU infrastructure (RTX A4500/RTX 2000 Ada). Config: `gpu-shadow.json` overlay, `gpu-shadow.env.example`, `OpenStackInstanceConfig` Pydantic model in `akos/models.py`.
- **`deploy-shadow` GPU CLI subcommand** -- `scripts/gpu.py deploy-shadow` provisions a vLLM instance on ShadowPC OpenStack with cloud-init bootstrapping, health polling, and `switch-model.py gpu-shadow` integration. Interactive menu updated with ShadowPC as option 3.
- **`vllm-shadow` gateway provider** -- `openclaw.json.example` now declares a `vllm-shadow` provider block with `${VLLM_SHADOW_URL}` env substitution, parallel to `vllm-runpod`.
- **AWQ weight quantization support** -- `PodConfig.build_vllm_command()` now emits `--quantization`, `--enforce-eager`, and `--max-num-batched-tokens` flags when configured via `envVars`. `CatalogEntry` gains a `quantization` field.
- **DeepSeek R1 70B AWQ catalog entry** -- `config/model-catalog.json` adds `casperhansen/deepseek-r1-distill-llama-70b-awq` (70GB VRAM at AWQ vs 140GB at bf16), making 70B inference feasible on 2x A100-80GB with KV cache headroom.
- **HLK branding** -- Gateway control UI title set to "HLK Intelligence Platform" via `gateway.controlUi.title`. Agent identity blocks renamed to "HLK Orchestrator", "HLK Architect", etc. FastAPI title changed to "HLK Operations Platform". Placeholder HLK logo generated at `static/hlk-logo.png`.

### Changed

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
