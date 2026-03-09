---
name: AKOS v0.4 Improvement Proposal
overview: Close remaining gaps between OpenCLAW-AKOS and SOTA agentic systems (Windsurf Cascade, Cursor, Claude Code Agentic RAG, OpenClaw live testing) by deploying the full 4-agent experience in the browser, adding Windsurf-style UX (plans/todos, checkpoints, memories), cross-platform MCP paths, and live model smoke tests.
todos:
  - id: four-agent-deploy
    content: "Phase 1: Deploy Orchestrator + Verifier workspaces so all 4 agents appear in OpenClaw dashboard"
    status: pending
  - id: mcp-crossplatform
    content: "Phase 2: Fix MCP paths for Windows (playwright/filesystem use /opt/openclaw; need resolve_openclaw_home)"
    status: pending
  - id: windsurf-ux
    content: "Phase 3: Add Windsurf-style UX (plan/todo lists in prompts, named checkpoints in UI, queued messages pattern)"
    status: pending
  - id: agentic-rag
    content: "Phase 4: Agentic RAG pattern for codebase retrieval (optional; Claude Code series, SOTA repo patterns)"
    status: pending
  - id: live-smoke
    content: "Phase 5: Live model smoke tests (OpenClaw-style; optional env-gated pytest for real provider smoke)"
    status: pending
  - id: memories-rules
    content: "Phase 6: User-facing Memories & Rules (Windsurf-style; leverage MCP Memory + workspace files)"
    status: pending
isProject: false
---

# AKOS v0.4 Improvement Proposal — Composer

**Signature:** `composer`  
**Date:** March 2026

---

## End Goal

OpenCLAW-AKOS should deliver a **production-grade, end-user-testable** agentic system that:

1. **Runs as intended in the browser** — All 4 agents (Orchestrator, Architect, Executor, Verifier) visible and usable in the OpenClaw dashboard.
2. **Matches SOTA UX** — Plans/todos, checkpoints, memories, and progress feedback comparable to Windsurf Cascade, Cursor, Manus.
3. **Works across platforms** — MCP paths resolve correctly on Windows, macOS, Linux.
4. **Is verifiable end-to-end** — User can run a browser smoke test and a live model smoke test (when credentials exist).
5. **Supports agentic RAG** — Optional codebase/document retrieval for deep research and planning (inspired by Claude Code Agentic RAG series and SOTA system prompts).

---

## As-Is Analysis (post v0.3.0)

### What Works

| Component | Status |
|:----------|:-------|
| 4-agent architecture | Designed; Orchestrator + Verifier prompts and scaffolds exist |
| RunPod integration | Full SDK, health, scaling, auto-provision on switch |
| FastAPI control plane | 12 endpoints, Swagger UI, `/agents` returns 4 agents |
| MCP ecosystem | 6 servers (sequential-thinking, playwright, github, memory, filesystem, fetch) |
| HITL permissions | 15 autonomous + 18 approval-gated tools |
| Checkpoints API | Create, restore, list via REST |
| Test runner | `py scripts/test.py` with friendly subcommands |
| Browser smoke test docs | Section 16.3 in USER_GUIDE.md |

### Gaps vs SOTA (Windsurf, Cursor, Claude Code RAG, OpenClaw)

| Gap | SOTA Reference | Current State |
|:----|:---------------|:--------------|
| **4 agents in dashboard** | All agents visible and selectable | Only Architect + Executor show; Orchestrator/Verifier workspaces not created |
| **MCP paths Windows** | Cross-platform paths | `mcporter.json` uses `/opt/openclaw/workspace` — fails on Windows |
| **Plan/todo lists** | Windsurf Cascade, Cursor | Progress bullets in prompts; no explicit todo list structure |
| **Named checkpoints in UI** | Windsurf reverts, Replit forks | API exists; no dashboard integration |
| **Memories & rules** | Windsurf Memories, Cursor rules | MCP Memory server; no user-facing rules UI |
| **Agentic RAG** | Claude Code RAG series, SOTA repo | No codebase retrieval or document chunking for planning |
| **Live model smoke** | OpenClaw Vitest live suites | Pytest only; no opt-in live provider smoke |
| **Queued messages** | Windsurf queue | Sequential only |
| **Send problems to agent** | Windsurf Send to Cascade | Not implemented |
| **@-mention prev convos** | Windsurf | Langfuse traces exist; no @-mention retrieval |

---

## To-Be Architecture (Target State)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     OPENCLAW GATEWAY DASHBOARD                       │
│                   http://127.0.0.1:18789                             │
│                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │
│  │Orchestrator │ │  Architect  │ │  Executor   │ │  Verifier   │    │
│  │   visible   │ │  visible    │ │  visible   │ │  visible   │    │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘    │
│                                                                      │
│  Plan/Todo list in chat · Named checkpoints · Memories & rules      │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MCP SERVERS (cross-platform paths)                │
│  workspace_root = resolve_openclaw_home() / "workspace"              │
│  Windows: C:\Users\<user>\.openclaw\workspace                        │
│  Linux:   ~/.openclaw/workspace or /opt/openclaw/workspace           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI CONTROL PLANE (8420)                       │
│  /health · /agents · /checkpoints · /prompts/assemble · /metrics     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Full 4-Agent Dashboard Deployment

**Goal:** All 4 agents appear in the OpenClaw dashboard and are selectable for chat.

### 1.1 Root Cause

The dashboard shows only agents whose workspace directories exist and contain `SOUL.md`. Orchestrator and Verifier scaffolds exist in `config/workspace-scaffold/` but are not deployed to `~/.openclaw/workspace-orchestrator` and `~/.openclaw/workspace-verifier` during bootstrap.

### 1.2 Extend Bootstrap to Deploy All 4 Agents

Update `scripts/bootstrap.py` (or `akos/io.py` `deploy_soul_prompts`):

- Ensure `deploy_soul_prompts` writes to all 4 agent workspaces, not just Architect and Executor.
- Create workspace directories for Orchestrator and Verifier if missing.
- Copy `ORCHESTRATOR_PROMPT.md` → `workspace-orchestrator/SOUL.md`, `VERIFIER_PROMPT.md` → `workspace-verifier/SOUL.md`.
- Mirror the scaffold files (IDENTITY.md, MEMORY.md, HEARTBEAT.md) into each workspace.

### 1.3 Extend `switch-model.py` / Deploy Logic

When switching environment, deploy SOUL.md for all 4 agents. The current logic may only deploy Architect and Executor.

### 1.4 Verification

- Run bootstrap (or `py scripts/switch-model.py dev-local`).
- Open `http://127.0.0.1:18789/agents`.
- **Expected:** 4 agents listed (Orchestrator, Architect, Executor, Verifier).
- Run `py scripts/test.py api` and ensure `/agents` returns `soul_md_exists: true` for all 4.

---

## Phase 2: Cross-Platform MCP Paths

**Goal:** Playwright and Filesystem MCP servers work on Windows without manual path edits.

### 2.1 Problem

`config/mcporter.json.example` has:

```json
"args": ["-y", "@playwright/mcp@latest", "--output-dir", "/opt/openclaw/workspace/exports"]
"args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/openclaw/workspace"]
```

`/opt/openclaw/workspace` does not exist on Windows. The OpenClaw home on Windows is typically `C:\Users\<user>\.openclaw\`.

### 2.2 Solution Options

**A. Env var substitution in mcporter.json**

OpenClaw/mcporter may support `${OPENCLAW_HOME}` or similar. Check OpenClaw docs and `mcporter.json` schema.

**B. Bootstrap writes resolved mcporter.json**

- `scripts/bootstrap.py` reads `mcporter.json.example`.
- Resolves paths using `akos.io.resolve_openclaw_home()`.
- Writes `~/.mcporter/mcporter.json` (or project-local) with actual paths.
- Example: `resolve_openclaw_home() / "workspace" / "exports"` for Playwright.

**C. Symlink or junction on Windows**

Create `C:\Users\<user>\.openclaw\workspace` → equivalent of `/opt/openclaw/workspace`. Not ideal for portability.

**Recommendation:** B — bootstrap generates a resolved `mcporter.json` from the example, using `resolve_openclaw_home()`.

### 2.3 Implementation

- Add `akos.io.resolve_workspace_path(subpath: str) -> Path`.
- In bootstrap, after MCP config step, generate `mcporter.json` with resolved paths.
- Document in USER_GUIDE that `mcporter.json` is generated; users should not hand-edit for path changes.

---

## Phase 3: Windsurf-Style UX Patterns

**Goal:** Bring key Windsurf Cascade UX patterns into AKOS prompts and docs.

### 3.1 Plan / Todo Lists in Prompts

Windsurf: "Cascade has built-in planning capabilities... Todo list within the conversation."

- Add to Orchestrator and Architect base prompts: When decomposing a task, emit a **numbered todo list** (e.g., `1. [ ] Sub-task A`, `2. [ ] Sub-task B`).
- Executor: Before each action, reference the todo item being executed (e.g., `Executing step 2: ...`).
- Verifier: On completion of a step, suggest marking it done (e.g., `1. [x] Sub-task A`).
- Store in `OVERLAY_REASONING.md` or new `OVERLAY_PLAN_TODOS.md`.

### 3.2 Named Checkpoints (User-Facing)

We have `akos/checkpoints.py` and `/checkpoints` API. Expose to users:

- Add to USER_GUIDE: "Create a checkpoint before risky operations: `POST /checkpoints` with `workspace=executor` and `name=before-refactor`."
- Optional: Add a small script `scripts/checkpoint.py create|restore|list` for CLI users.
- Future: If OpenClaw dashboard supports custom actions, hook checkpoint create/restore there.

### 3.3 Queued Messages Pattern (Documentation)

Windsurf allows queueing messages while the agent works. OpenClaw may not support this natively. Document the limitation and suggest workarounds (e.g., "Wait for the agent to finish before sending the next message").

### 3.4 Progress Summaries (Already Partially There)

Prompt directives already require progress sentences. Consider structured format (e.g., JSON) for FastAPI WebSocket to parse and render rich progress in a future UI.

---

## Phase 4: Agentic RAG (Optional)

**Goal:** Enable codebase and document retrieval for planning and research tasks.

**Reference:** Claude Code Agentic RAG series (theaiautomators), SOTA system prompts (FraysaXII repo).

### 4.1 Options

| Approach | Complexity | UX Value |
|:---------|:-----------|:---------|
| **MCP codebase server** | Medium | High — search, read files, list dirs |
| **Custom RAG pipeline** | High | High — embeddings, chunking, retrieval |
| **GitHub MCP + read_file** | Low (already have) | Medium — repo metadata, file read |
| **Defer** | None | — |

### 4.2 Recommendation

**Defer full RAG.** We already have:
- GitHub MCP (repo metadata, code search)
- Filesystem MCP (read, list)
- Fetch MCP (HTTP)

For v0.4, enhance the Architect prompt to **explicitly use** these tools for "research" and "codebase analysis" tasks. Add an overlay `OVERLAY_RESEARCH.md` that instructs the Architect to:
1. Use `list_directory` and `read_file` (filesystem) for local codebase.
2. Use GitHub MCP for repo structure and search.
3. Use `fetch` for external docs when URLs are provided.

No new infra. Prompt-level improvement only.

---

## Phase 5: Live Model Smoke Tests (Optional)

**Goal:** Opt-in pytest tests that hit real providers (Ollama, OpenAI, etc.) when credentials exist.

**Reference:** OpenClaw testing docs — Vitest live suites, `OPENCLAW_LIVE_TEST=1`, `OPENCLAW_LIVE_MODELS`.

### 5.1 Design

- Add `tests/test_live_smoke.py` (or under `tests/live/`).
- Use pytest markers: `@pytest.mark.live` and `@pytest.mark.skipif(not os.getenv("AKOS_LIVE_SMOKE"), reason="AKOS_LIVE_SMOKE not set")`.
- Tests:
  - Health check: Call `GET /health` (no provider needed).
  - Ollama smoke (if `ollama` running): `POST /switch` with `dev-local`, then verify status.
  - Optional: Single completion via a minimal prompt (requires API key or Ollama).
- Add to `scripts/test.py`: `py scripts/test.py live` → runs only `-m live` tests.
- Document in USER_GUIDE and CONTRIBUTING: "Set `AKOS_LIVE_SMOKE=1` to enable live tests."

### 5.2 Scope

Keep live tests minimal — 2–3 smoke checks. No full agent loop against real models (too flaky, costs credits).

---

## Phase 6: Memories & Rules (Windsurf-Style)

**Goal:** User-facing "Memories" and "Rules" that persist and influence agent behavior.

**Reference:** Windsurf Memories & Rules, Cursor Rules.

### 6.1 Current State

- MCP Memory server: `memory_store`, `memory_retrieve` for key-value.
- Workspace files: `MEMORY.md`, `IDENTITY.md`, `USER.md` in each agent scaffold.

### 6.2 Enhancement

**Rules:**

- Add `RULES.md` to workspace scaffold. Content: "User-defined rules that MUST be followed. Examples: 'Always use TypeScript for new files', 'Never commit without running tests'."
- Architect and Executor base prompts: "Read RULES.md if present and apply rules to all outputs."
- Bootstrap: Create empty `RULES.md` with placeholder text.

**Memories:**

- `MEMORY.md` already exists. Strengthen prompt directive: "After each session, append lessons learned to MEMORY.md. Use concise bullet format."
- Optional: MCP Memory keys like `user_preference:theme` or `project:stack` that the agent can read at session start.

### 6.3 Implementation

- Add `config/workspace-scaffold/architect/RULES.md` (and for other agents).
- Update `deploy_soul_prompts` to copy RULES.md.
- Add to Architect/Executor base: "If RULES.md exists in workspace, read it and apply all rules."
- Update USER_GUIDE: "Customize RULES.md in each agent's workspace to enforce project conventions."

---

## Files Changed/Created Summary

| File | Action |
|:-----|:-------|
| `scripts/bootstrap.py` | Deploy all 4 agents; generate resolved mcporter.json |
| `akos/io.py` | `resolve_workspace_path()`, `deploy_soul_prompts` for 4 agents |
| `config/mcporter.json.example` | Document env var or templating for paths (if supported) |
| `config/workspace-scaffold/*/RULES.md` | New file for user rules |
| `prompts/base/ORCHESTRATOR_BASE.md` | Todo list format |
| `prompts/base/ARCHITECT_BASE.md` | Todo list format, RULES.md directive |
| `prompts/base/EXECUTOR_BASE.md` | Todo refs, RULES.md directive |
| `prompts/overlays/OVERLAY_RESEARCH.md` | Optional research tool usage |
| `scripts/checkpoint.py` | Optional CLI for checkpoints |
| `tests/test_live_smoke.py` | Optional live smoke tests |
| `scripts/test.py` | Add `live` group |
| `docs/USER_GUIDE.md` | Checkpoint CLI, RULES.md, live tests, MCP path notes |

---

## Priority Order

| Phase | Priority | Effort | Impact |
|:-----|:---------|:-------|:-------|
| 1. Four-agent deploy | **P0** | Low | High — unblocks end-user testing |
| 2. MCP cross-platform | **P0** | Medium | High — Windows usability |
| 3. Windsurf UX | **P1** | Low–Medium | Medium — better UX |
| 6. Memories & rules | **P1** | Low | Medium — customization |
| 4. Agentic RAG | **P2** | Low (prompt-only) | Medium |
| 5. Live smoke | **P2** | Low | Low — niche DX |

---

## Verification Checklist

After implementing:

- [ ] All 4 agents visible in `http://127.0.0.1:18789/agents`
- [ ] Chat works for Orchestrator and Verifier (not just Architect/Executor)
- [ ] Playwright MCP works on Windows (output-dir resolves)
- [ ] Filesystem MCP works on Windows (workspace path resolves)
- [ ] `py scripts/test.py` passes (191+ tests)
- [ ] `py scripts/test.py live` runs when `AKOS_LIVE_SMOKE=1` (if Phase 5 done)
- [ ] Browser smoke test (USER_GUIDE 16.3.2) passes for all 4 agents
- [ ] RULES.md is read and applied (manual spot check)

---

*Proposal by Composer. Run `py scripts/test.py --list` to see current test groups.*
