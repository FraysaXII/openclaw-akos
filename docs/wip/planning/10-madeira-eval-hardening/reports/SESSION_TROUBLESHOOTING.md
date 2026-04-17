# Initiative 10 — Madeira WebChat session troubleshooting

Use this when [`uat-madeira-path-bc-browser-20260416.md`](uat-madeira-path-bc-browser-20260416.md) rows are **SKIP** or **PARTIAL** due to dashboard behaviour (not pytest/API contracts).

## 1. Stuck queue / “Remove queued message” / no reply

| Symptom | Action |
|:--------|:-------|
| Prompt stuck after **Enter** | Click **Stop generating**, then **New session** (or open `/chat?session=agent:madeira:main` and **New session**) so the gateway queue is empty before the next prompt. |
| **Remove queued message** visible | Click it, then re-type a **single** prompt (avoid stacking prompts while the model is still generating). |
| Prior UAT used **browser_wait_for** too short | Allow **120s+** for local Ollama on cold load; or run **HTTP** `py scripts/browser-smoke.py` (includes `scenario0_*`) while WebChat is flaky. |

## 2. `All models failed … ollama/… timeout`

This is **host inference**, not AKOS registry logic.

| Check | Command / note |
|:------|:----------------|
| Ollama running | OS service / `ollama serve` (see upstream docs). |
| Model pulled | `ollama pull qwen3:8b` (and any fallbacks in `~/.openclaw/openclaw.json`). |
| Warm-up | `ollama run qwen3:8b "ping"` once before WebChat UAT. **PowerShell:** no trailing comma after the prompt (`,` is not like bash’s command separator). |
| Load | Close other GPU-heavy apps; `ollama ps` to see concurrent runs. |
| Fallback order | If qwen3 times out, fallbacks (`llama3.1:8b`, `deepseek-r1:14b`) may also queue — fix **first** model health before re-testing WebChat. |

## 3. Playwright SKIP (`0xC0000005` on Windows)

Use **CPython 3.12.x** for the venv running `py scripts/browser-smoke.py --playwright`, or rely on **HTTP** smoke + **Cursor IDE Browser** MCP for dashboard rows. See [`docs/DEVELOPER_CHECKLIST.md`](../../../../DEVELOPER_CHECKLIST.md) and [`.cursor/rules/akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc).

## 4. When WebChat is down but gates must stay green

- **Registry parity (Scenario 0 steps 4–7 data plane):** `py scripts/browser-smoke.py` (HTTP) — scenarios `scenario0_hlk_cto`, `scenario0_hlk_research_area`, `scenario0_hlk_kirbe_children`, `scenario0_admin_escalation`.
- **Pytest:** [`docs/uat/hlk_admin_smoke.md`](../../../../uat/hlk_admin_smoke.md) automated parity table.

## Governance (SOC)

Do not paste API keys, bearer tokens, or full assistant transcripts into this folder; outcome tables only.
