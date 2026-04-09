# Madeira read-only hardening — traceability mirror

**Cursor plan (reference):** workspace plan *Harden Madeira read-only* (do not edit the plan file in `.cursor/plans/`).

**Scope recap:** Madeira stays a **read-only** gateway router with HLK/finance tools, compact-tier invariant overlays, `sequential_thinking` only after tool results, `execution_escalate` alongside `admin_escalate`, workspace startup/memory scaffold, log-watcher grounding signals + eval alerts, docs and security audit runbook. **Out of scope:** full-profile Madeira with broad write/browser/MCP at the gateway (contradicts read-only boundary).

## Decision log (summary)

| ID | Decision |
|----|----------|
| D1 | Swarm escalation for writes/execution; Madeira read-only at gateway. |
| D2 | Org facts via `hlk_*` tools only; cite canonical asset names. |
| D3 | `sequential_thinking` enabled on Madeira; use after tool results, not instead of HLK retrieval. |
| D4 | Log-watcher + `config/eval/alerts.json` for grounding observability. |
| D5 | Document `openclaw security audit` / `--deep` in USER_GUIDE; pointer in SECURITY. |
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

**Post-implementation:** Operators should re-run `py scripts/bootstrap.py` after pulling so live OpenClaw config and plugins match `config/openclaw.json.example` and `openclaw-plugins/akos-runtime-tools/`, then re-run `py scripts/check-drift.py` and `py scripts/release-gate.py`.

## Files touched (high level)

- Prompts: `prompts/base/MADEIRA_BASE.md`, `prompts/overlays/OVERLAY_HLK.md`, `OVERLAY_HLK_COMPACT.md`, `OVERLAY_STARTUP_COMPACT.md`, assembled outputs under `prompts/assembled/`, `prompts/MADEIRA_PROMPT.md`
- Config: `config/model-tiers.json`, `config/openclaw.json.example`, `config/agent-capabilities.json`, `config/intent-exemplars.json`, `config/eval/alerts.json`
- Runtime: `akos/intent.py`, `akos/models.py` (`RoutingClassificationResponse`), `akos/api.py`, `akos/io.py`, `scripts/log-watcher.py`, `openclaw-plugins/akos-runtime-tools/index.ts`
- Scaffold: `config/workspace-scaffold/madeira/memory/README.md`
- Tests: `tests/test_intent.py`, `tests/test_api.py`, `tests/test_log_watcher.py`, `tests/test_e2e_pipeline.py`, `tests/test_akos_models.py`, `tests/validate_configs.py`
- Docs: `docs/USER_GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/SECURITY.md`, `docs/uat/hlk_admin_smoke.md`, `CHANGELOG.md`
