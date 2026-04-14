# Madeira read-only hardening — traceability mirror

**Cursor plan (active):** `.cursor/plans/madeira_hardening_consolidated_0cd9482e.plan.md` — consolidated runbook (governance + UAT + debugging). Legacy snapshot: `harden_madeira_read-only_375b110e.plan.md` (superseded).

**Scope recap:** Madeira stays a **read-only** gateway router with HLK/finance tools, compact-tier invariant overlays, `sequential_thinking` only after tool results, `execution_escalate` alongside `admin_escalate`, workspace startup/memory scaffold, log-watcher grounding signals + eval alerts, docs and security audit runbook. **Out of scope:** full-profile Madeira with broad write/browser/MCP at the gateway (contradicts read-only boundary).

## Decision log (summary)

| ID | Decision |
|----|----------|
| D1 | Swarm escalation for writes/execution; Madeira read-only at gateway. |
| D2 | Org facts via `hlk_*` tools only; cite canonical asset names. |
| D3 | `sequential_thinking` enabled on Madeira; use after tool results, not instead of HLK retrieval. |
| D4 | Log-watcher + `config/eval/alerts.json` for grounding observability. |
| D5 | Document `openclaw security audit` / `--deep` in USER_GUIDE; **SECURITY.md** §5 SOC links to USER_GUIDE §14.3. |
| D6 | Pydantic `RoutingClassificationResponse` for `/routing/classify`; alerts already schema-validated via `Alert`. |

## Verification matrix (2026-04-09, Windows dev host)

| Command | Result |
|---------|--------|
| `py scripts/assemble-prompts.py` | PASS |
| `py scripts/legacy/verify_openclaw_inventory.py` | PASS |
| `py scripts/check-drift.py` | **FAIL** (local `~/.openclaw/openclaw.json` missing `sequential_thinking` on madeira; plugin `index.ts` not yet redeployed — run `py scripts/bootstrap.py` to sync template) |
| `py scripts/test.py all` | PASS |
| `py scripts/browser-smoke.py --playwright` | SKIP (Playwright workers unavailable on this host; release-gate treated as SKIP) |
| `py -m pytest tests/test_api.py -v` | PASS |
| `py scripts/release-gate.py` | **FAIL** (only due to drift check above; other gates PASS) |
| `py scripts/validate_hlk.py` | PASS (run via release-gate) |
| `py scripts/validate_hlk_km_manifests.py` | N/A (no manifest changes) |

## Verification matrix (2026-04-14, post-bootstrap + consolidated plan closure)

| Command | Result |
|---------|--------|
| `py scripts/bootstrap.py --skip-ollama` | PASS (agents + providers + plugin `akos-runtime-tools` synced; OpenCLaw home `~/.openclaw`) |
| `py scripts/check-drift.py` | **PASS** (no drift) |
| `py scripts/release-gate.py` | **PASS** (inventory, `test.py all`, drift, browser smoke, `pytest tests/test_api.py`, `validate_hlk.py`) |

**Post-implementation:** After pulls that change `config/openclaw.json.example`, plugins, or prompts, re-run `py scripts/bootstrap.py` then `py scripts/check-drift.py` and `py scripts/release-gate.py`.

## Phase → commit mapping (Madeira read-only initiative)

Work landed primarily as feature + docs commits (not every original lettered phase is an isolated git commit):

| Plan phase / theme | Representative commit | Notes |
|--------------------|----------------------|--------|
| P1–P6 (overlays, routing, scaffold, log-watcher, capabilities) | `e8a2250` — `feat(madeira): harden read-only router and grounding telemetry` | Core implementation batch |
| P7 (UAT parity docs) | `5cd44ca` — `docs(uat): add no-browser Scenario 0 parity checklist` | Pytest matrix in `hlk_admin_smoke.md` |
| P7 (browser UAT path) | `71f66d7` — `docs(uat): document browser UAT path and tool-capable model gate` | WebChat + model gate + port 8420 |
| Cross-stack §8 (SECURITY ↔ USER_GUIDE) | Working tree / follow-up | `SECURITY.md` now links to USER_GUIDE §14.3 OpenClaw gateway security audit |

Operators needing strict **one commit per phase** for audit should cherry-pick or use this table as the authoritative mapping for this rollout.

## Scenario 0 UAT — model lanes (2026-04-14)

| Lane | Model / surface | Scope | Result |
|------|-----------------|-------|--------|
| **A — Contract / REST** | N/A (no LLM) | `py scripts/serve-api.py --port 8420`; `GET /health` → `status: ok`; `GET /hlk/roles/CTO` → `access_level` 5, `reports_to` O5-1, canonical role fields | **PASS** (validates registry + API; subfields on `/health` may show degraded gateway/RunPod/vLLM per env) |
| **B — WebChat (operator)** | Tool-capable default, e.g. `ollama/qwen3:8b` | Dashboard `…/chat?session=agent:madeira:main`; **Settings → AI & Agents** `agents.defaults.model` JSON if header picker is not a native select; `/new` then Scenario 0 steps 4–7 in [hlk_admin_smoke.md](../../../../uat/hlk_admin_smoke.md) | **Operator sign-off** (repeat on a second medium+ lane, e.g. cloud/RunPod, to meet exit “≥2 lanes”) |

Lane B remains human-in-the-loop for full tool-trace verification; Lane A locks vault-backed answers independent of gateway model choice.

## Files touched (high level)

- Prompts: `prompts/base/MADEIRA_BASE.md`, `prompts/overlays/OVERLAY_HLK.md`, `OVERLAY_HLK_COMPACT.md`, `OVERLAY_STARTUP_COMPACT.md`, assembled outputs under `prompts/assembled/`, `prompts/MADEIRA_PROMPT.md`
- Config: `config/model-tiers.json`, `config/openclaw.json.example`, `config/agent-capabilities.json`, `config/intent-exemplars.json`, `config/eval/alerts.json`
- Runtime: `akos/intent.py`, `akos/models.py` (`RoutingClassificationResponse`), `akos/api.py`, `akos/io.py`, `scripts/log-watcher.py`, `openclaw-plugins/akos-runtime-tools/index.ts`
- Scaffold: `config/workspace-scaffold/madeira/memory/README.md`
- Tests: `tests/test_intent.py`, `tests/test_api.py`, `tests/test_log_watcher.py`, `tests/test_e2e_pipeline.py`, `tests/test_akos_models.py`, `tests/validate_configs.py`
- Docs: `docs/USER_GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/SECURITY.md` (§5 SOC + USER_GUIDE §14.3 cross-link), `docs/uat/hlk_admin_smoke.md`, `CHANGELOG.md`, this mirror (verification + UAT lanes + phase mapping)
