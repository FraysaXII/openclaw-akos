# Initiative 10 — Madeira Path B+C, SOTA quality, eval harness

**Status:** execution in progress.  
**Canonical plan source (read-only reference):** Cursor plan `madeira_b+c_and_sota_eval` (do not treat this folder as replacing that file).

## Asset classification (HLK)

Per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../references/hlk/compliance/PRECEDENCE.md):

| Class | In scope for this initiative |
|-------|------------------------------|
| **Canonical** | No edits to `baseline_organisation.csv` / `process_list.csv` without operator approval. |
| **Mirrored / derived** | `config/openclaw.json.example`, `config/agent-capabilities.json`, prompts, eval fixtures. |
| **Reference-only** | PMO Trello / [`RESEARCH_BACKLOG_TRELLO_REGISTRY.md`](../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/RESEARCH_BACKLOG_TRELLO_REGISTRY.md) for topic alignment only. |

## Decision log (summary)

| ID | Decision |
|----|----------|
| D-B | Path B SSOT: `agents.defaults.sandbox.mode` + `tools.exec.host: sandbox` in `openclaw.json.example` where supported; Windows operators use Docker Desktop sandboxes and/or WSL2 per USER_GUIDE / SECURITY. |
| D-C | Path C: remove `web_search` / `web_fetch` from orchestrator and architect `alsoAllow`; keep `browser` on architect; research spine = HLK MCP → optional graph → browser → escalation. |
| D-UI | Remove `gateway.controlUi` from SSOT (upstream schema rejection on some CLI versions). |
| D-EVAL | Suite manifests under `tests/evals/suites/<name>/`, rubric mode, Langfuse v4 via `akos.telemetry.LangfuseReporter` patterns; metadata includes categorical `research_surface` on `LangfuseTraceContext`. |

## Governed verification matrix

Full gate set: [`docs/DEVELOPER_CHECKLIST.md`](../../DEVELOPER_CHECKLIST.md) — including `py scripts/legacy/verify_openclaw_inventory.py`, `py scripts/check-drift.py`, `py scripts/test.py all`, `py scripts/browser-smoke.py --playwright`, `py -m pytest tests/test_api.py -v`, `py scripts/release-gate.py`, and when compliance assets change: `py scripts/validate_hlk.py`, `py scripts/validate_hlk_km_manifests.py`.

## Appendices (mirrors of plan narrative)

### A — Windows strict sandbox (Phase 2c)

OpenClaw strict sandbox + exec sandbox may be unsupported on native Windows without an isolation backend. Operators should prefer **Docker Desktop 4.58+** with [Docker Desktop sandboxes](https://docs.docker.com/ai/sandboxes/docker-desktop/) (microVM, isolated daemon, workspace sync, network proxy CLI) and/or **WSL2** for a Linux gateway. Verify File Sharing includes `~/.openclaw` and repo root; use `docker sandbox ls` when applicable; `py scripts/doctor.py` emits non-fatal WARNs for Docker/WSL probes.

### B — Path C research load (SOTA mitigation)

Contracted retrieval first (`hlk_*` ladder, optional `hlk_graph_*`), then architect **`browser`** for public verification under Path B, then orchestrator for side effects. USER_GUIDE documents the decision tree; eval suites cover spine steps; Langfuse metadata may include `research_surface` (categorical, SOC-safe).

### C — Eval SOTA upgrades

Suite `manifest.json` (version, dimension coverage), exclusion policy, optional `--trials`, Tier A (pytest + dry-run) vs Tier B (Playwright) CI split. See `tests/evals/README.md`.

### D — External lane reference (α–η)

Lane codenames in the Cursor plan (`Amber`, `Basalt`, …) are **due diligence** mirrors outside repo SSOT; use codenames in workspace docs only.
