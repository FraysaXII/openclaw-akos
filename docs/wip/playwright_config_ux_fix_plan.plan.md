# Playwright, Config Schema, and UX Fix Plan

**Scope:** Fix failing Playwright Phase 2 checks, resolve Config "Invalid" schema errors, and document/troubleshoot Version display and "No nodes with system.exe available" issues.

---

## 1. Config Schema Fix (Code Changes)

OpenClaw v2026.2.17 schema ([config.clawi.sh](https://config.clawi.sh/v2026.2.17)) uses different key names than our `openclaw.json.example`. The gateway validates deployed config and reports "Unrecognized key" for our keys.

### Exact Key Mappings (from schema inspection)

| Our Key (invalid) | OpenClaw Schema Key (valid) | Location |
|-------------------|----------------------------|----------|
| `tools.agentToAgent.targetAllowlist` | `tools.agentToAgent.allow` | tools |
| `session.agentToAgent.pingPongTurns` | `session.agentToAgent.maxPingPongTurns` | session |
| `session.typing.mode` | `session.typingMode` | session (flat) |
| `messages.suppressToolErrorWarnings` | `messages.suppressToolErrors` | messages |

### Task 1.1: Update `config/openclaw.json.example`

**File:** [config/openclaw.json.example](config/openclaw.json.example)

- Line 165–168: Change `targetAllowlist` to `allow` inside `tools.agentToAgent`.
- Line 173: Change `pingPongTurns` to `maxPingPongTurns` inside `session.agentToAgent`.
- Line 174: Remove `"typing": {"mode": "thinking"}`; add `"typingMode": "thinking"` at `session` level.
- Line 184: Change `suppressToolErrorWarnings` to `suppressToolErrors` inside `messages`.

**Before (snippet):**
```json
"agentToAgent": {
  "enabled": true,
  "targetAllowlist": ["orchestrator", "architect", "executor", "verifier"]
}
...
"session": {
  "scope": "per-sender",
  "reset": {"mode": "idle", "idleMinutes": 60},
  "agentToAgent": {"pingPongTurns": 3},
  "typing": {"mode": "thinking"}
}
...
"messages": {
  "statusReactions": {"enabled": true},
  "suppressToolErrorWarnings": false
}
```

**After (snippet):**
```json
"agentToAgent": {
  "enabled": true,
  "allow": ["orchestrator", "architect", "executor", "verifier"]
}
...
"session": {
  "scope": "per-sender",
  "reset": {"mode": "idle", "idleMinutes": 60},
  "agentToAgent": {"maxPingPongTurns": 3},
  "typingMode": "thinking"
}
...
"messages": {
  "statusReactions": {"enabled": true},
  "suppressToolErrors": false
}
```

### Task 1.2: Update `akos/models.py`

**File:** [akos/models.py](akos/models.py)

- `AgentToAgentConfig` (line 147–152): Change `targetAllowlist` to `allow` for schema alignment. Add `Field(alias="targetAllowlist")` for backward compatibility when reading legacy configs.
- `SessionConfig` (line 154–161): Change `agentToAgent` default from `{"pingPongTurns": 3}` to `{"maxPingPongTurns": 3}`. Remove `typing` dict; add `typingMode: str = "thinking"` at top level. Add `Field(alias="typing")` on typingMode if we ever need to read `session.typing.mode` from old configs — for now, keep models aligned with new schema only.

**Exact edits:**
```python
# AgentToAgentConfig
allow: list[str] = Field(default_factory=list, alias="targetAllowlist")

# SessionConfig
agentToAgent: dict = Field(default_factory=lambda: {"maxPingPongTurns": 3})
typingMode: str = "thinking"  # was typing: dict
# Remove: typing: dict = ...
```
Use `model_config = ConfigDict(populate_by_name=True)` if using alias for reads.

---

## 2. Playwright Phase 2 Fix (Already Scoped)

**File:** [scripts/browser-smoke.py](scripts/browser-smoke.py)

- Navigate to `GATEWAY_URL + "/agents"` instead of `GATEWAY_URL`.
- Wait for agent cards; use text-based locators for Architect and Executor cards.
- Click cards; optionally open Tools tab for architect_tools_ui and executor_approval_hint.

(Details in prior plan summary.)

---

## 3. Version Display (Document Only – Not Fixable in AKOS)

**Cause:** OpenClaw dashboard header and update banner may show different version strings (e.g. "Version 2026.2.19-2" vs "running v2026.2.26"). This is OpenClaw dashboard/gateway logic; AKOS does not control it.

**Task 3.1:** Add a short note in [docs/uat/dashboard_smoke.md](docs/uat/dashboard_smoke.md) under "Known issues":

> **Version display mismatch:** The header version and the update banner may show different values. This comes from OpenClaw gateway/dashboard; AKOS has no control. For UAT, treat both as informational.

---

## 4. "No nodes with system.exe available" (Document + Troubleshooting)

**Cause:** Nodes settings page shows this when `tools.exec.host` can use nodes but no paired node offers exec capability (`system.exe` on Windows). Per [OpenClaw exec docs](https://docs.clawd.bot/tools/exec-approvals) and node troubleshooting.

**Task 4.1:** Add troubleshooting entry in [docs/USER_GUIDE.md](docs/USER_GUIDE.md) Section 17 (Troubleshooting):

> **"No nodes with system.exe available" (Nodes page)**  
> This appears when the dashboard expects an exec-capable node but none is paired. Options:
> 1. **Local exec only:** Set `tools.exec.host` to `"sandbox"` or `"gateway"` (AKOS default is `sandbox`).
> 2. **Use a node:** Pair an exec-capable node (`openclaw node install`, `openclaw nodes status`) and ensure it has `system.exe` (Windows) or equivalent for command execution.

**Task 4.2:** Add a one-line note in [docs/uat/dashboard_smoke.md](docs/uat/dashboard_smoke.md) known issues:

> **No nodes with system.exe:** Expected when no exec-capable node is paired. Use `tools.exec.host: sandbox` for local-only exec, or pair a node per USER_GUIDE §17.

---

## 5. Documentation Updates (Per CONTRIBUTING)

| File | Change |
|------|--------|
| [CHANGELOG.md](CHANGELOG.md) | Add entry: config schema alignment (targetAllowlist→allow, pingPongTurns→maxPingPongTurns, typing→typingMode, suppressToolErrorWarnings→suppressToolErrors); Playwright Phase 2 fix; known-issues docs |
| [docs/SOP.md](docs/SOP.md) | §9.11 lines 1267–1268: Use `tools.agentToAgent.allow`, `session.typingMode`, `session.agentToAgent.maxPingPongTurns` |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Table row Session Policy: `session.reset.*`, `session.typingMode` (not typing) |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | §17: Add "No nodes with system.exe" troubleshooting |
| [docs/uat/dashboard_smoke.md](docs/uat/dashboard_smoke.md) | Add "Known issues" with version display, no-nodes, and config schema (now resolved) |

---

## 6. Execution Order

1. **Config schema:** Edit `config/openclaw.json.example` and `akos/models.py`.
2. **Tests:** Run `py scripts/test.py all`; fix any failures (e.g. `test_akos_models` if it asserts old keys).
3. **Playwright:** Edit `scripts/browser-smoke.py`; run `py scripts/browser-smoke.py --playwright`.
4. **Docs:** Update CHANGELOG, SOP, ARCHITECTURE, USER_GUIDE, dashboard_smoke.
5. **Gate:** `py scripts/release-gate.py`.
6. **Commit:** Follow CONTRIBUTING pre-commit checklist.

---

## 7. Verification

- Config page in dashboard no longer shows "Unrecognized key" for the four keys.
- Playwright Phase 2 (architect_tools_ui, executor_approval_hint) passes.
- `py scripts/test.py all` passes.
- Existing validation tests (`tests/validate_configs.py`, `tests/test_akos_models.py`) pass.
