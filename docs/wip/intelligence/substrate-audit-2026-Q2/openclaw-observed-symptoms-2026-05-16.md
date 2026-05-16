---
evidence_id: openclaw-observed-symptoms-2026-05-16
captured_at: 2026-05-16
captured_by: operator (gateway log paste during I77 P4 follow-up chat)
target_initiatives: [INIT-OPENCLAW_AKOS-84, INIT-OPENCLAW_AKOS-87 (proposed)]
target_strands:
  - I84 P1 Track 1 (agent-SDK comparison matrix — observed reliability surface for OpenClaw row)
  - I84 P3 §7 (OpenClaw/LlamaIndex/Cursor-SDK retrospective)
  - I87 P0 charter (5-strand scope; this file IS the scope reference)
classification: intelligence (working-space; not canonical SSOT)
access_level: 5 (operator + cleared collaborators)
language: en
---

# OpenClaw observed reliability symptoms — 2026-05-16

> **Source**: gateway log paste from operator during I77 P4 follow-up chat session (2026-05-16 evening). Six-hour silent-fail window observed from 14:37 → 20:34 with no operator escalation despite 13 consecutive 30-minute health-monitor cycles failing the same way. Fallback (Ollama → vLLM) masked the symptom; system continued running on the fallback model.
>
> **Why this file exists**: real-world field data is the strongest form of substrate-audit evidence. Synthetic comparison matrices read as marketing; observed reliability symptoms read as ground truth. This evidence anchors I84 P1 Track 1 (agent-SDK comparison matrix → OpenClaw row → `reliability_observed_symptoms` field) AND I87 P0 charter scope (the 5 distinct failure classes below are I87's 5 strands).

## Section 1 — Five distinct failure classes observed

| # | Symptom | Frequency | Severity | Self-healing? | Routes to |
|:-:|:---|:---|:---|:---|:---|
| 1 | `Failed to inspect sandbox image: failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine` | every 30min for 6+ hours (13 consecutive cycles) | **HIGH** (silent multi-hour outage) | NO — fallback works (Ollama → vLLM) but the underlying Docker daemon never recovers; no operator escalation | **I87 P1** (health-monitor escalation patch) + I84 P1 Track 1 (evidence) |
| 2 | `low context window: ollama/qwen3:8b ctx=16384 (warn<32000) source=modelsConfig` | every 30min (paired with #1) | LOW | NO — model registered with under-spec'd ctx; config drift | **I87 P3** (modelsConfig hygiene) + I84 P3 §7 (operator-config-burden axis) |
| 3 | `[ws] unauthorized ... reason=token_missing` + `[ws] closed before connect ... code=1008 reason=unauthorized: gateway token missing` | sporadic (control UI reconnects at 17:10, 18:48, 20:09) | MED | NO — operator UX bug (token not auto-applied / rotated stale) | **I87 P4** (token-rotation UX investigation) + I84 P3 §7 (operator-DX evidence) |
| 4 | `akos-runtime-tools: loaded without install/load-path provenance ... pin trust via plugins.allow` | once at 14:30:19 (startup) | LOW | NO — AKOS-authored plugin not pinned in OpenClaw's `plugins.allow` | **I87 P2** (one-line pin + optional `scripts/validate_openclaw_plugin_pinning.py` validator) |
| 5 | `bonjour watchdog detected non-announced service; attempting re-advertise` | once at 14:27:32 | NIL | YES — self-healed | none (informational only) |

## Section 2 — Proposed I87 charter scope (5 strands; ~5-7d total)

**I87 — OpenClaw Operator-Runtime Hardening** sits as the operational sibling to I84 (research). Same domain (OpenClaw), different angle: I84 decides which substrate AKOS commits to long-term; I87 makes the currently-deployed substrate stop bleeding silently.

| Strand | Scope | Effort | Cursor-rule operationalised |
|:---|:---|:---|:---|
| **P1 — Health-monitor escalation patch** | After N (default 3) consecutive 30-min cycles failing the same way, emit operator-visible escalation (Slack? toast? `OPERATOR_INBOX.md` row?). Closes the "silent multi-hour outage" failure mode. | ~1-2d | [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract" verbatim: *"Treat `Runtime: unknown` as an observability contract bug, not a healthy state."* |
| **P2 — `plugins.allow` AKOS plugin pinning** | One-line config in `~/.openclaw/openclaw.json` to explicitly trust `akos-runtime-tools` (and any future AKOS-authored OpenClaw plugins). Optional: `scripts/validate_openclaw_plugin_pinning.py` validator (mirrors I77 P4.C wiring pattern in miniature). | ~0.5d | [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 2 (adapter/integration registry status metadata pattern adapted to plugin trust) |
| **P3 — modelsConfig hygiene patch** | Bump `ollama/qwen3:8b` ctx in the modelsConfig where it's registered (raise to 32K+ to clear the warn threshold) OR remove the model entry if unused since fallback to vLLM is happening anyway. Decide via inline-ratify. | ~0.5d | none-rule-specific; standard config hygiene |
| **P4 — Gateway-token auto-paste UX investigation** | Root cause Class #3 (control UI repeatedly losing the gateway token between sessions). Either OpenClaw upstream bug (file ticket; defer) OR operator-config issue (document the rotation flow in SOP). | ~1d (mostly investigation) | none-rule-specific; UX investigation |
| **P5 — `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` + paired runbook** | New SOP at `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/` documenting the 5 symptom classes + triage decision tree (start Docker Desktop / disable Docker-dependent agent in modelsConfig / rotate gateway token / pin `akos-runtime-tools`). Paired `scripts/openclaw_health_triage.py` runbook that scans the gateway log + reports symptom class + recommended action per class. | ~2-3d | [`akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (SOP+runbook pairing — every executable process needs both surfaces) |

**Cross-cluster wiring**: I87 has no hard-blockers. Can run in any wave. **Recommended slot**: before I84 P4 ratification (Wave 3) so the `D-IH-84-B` substrate decision (OpenClaw vs Cursor-SDK vs hybrid) compares against the *patched* OpenClaw baseline, not the bleeding one. Otherwise OpenClaw looks worse than it deserves in the substrate-ratification table.

## Section 3 — Triage routing summary (where each class lands in the I86 cluster)

| Class | Primary home | Secondary home |
|:-:|:---|:---|
| #1 Docker sandbox | I87 P1 (operational fix) | I84 P1 evidence (substrate reliability symptom) |
| #2 low ctx | I87 P3 (operational fix) | I84 P3 §7 (operator-config-burden axis) |
| #3 ws auth | I87 P4 (operational fix) | I84 P3 §7 (operator-DX axis) |
| #4 plugins.allow | I87 P2 (operational fix) | — |
| #5 bonjour | none — self-healed | — |

## Section 4 — Operator triage actions taken 2026-05-16

| Time | Action | Outcome |
|:---|:---|:---|
| ~20:46 (during I77 P4 follow-up chat) | Started Docker Desktop via `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"` | Cascade expected to clear within 30-60s once Docker daemon is fully initialized; next health-monitor cycle should succeed. **Pending operator confirmation post-init.** |
| 2026-05-16 same chat | Saved this evidence file at canonical I84 P1 evidence path | Routed for I84 P1 Track 1 consumption + I87 P0 scope reference |

## Section 5 — Raw gateway log (verbatim; for I84 P1 evidence quality)

> Header observed at startup:
>
> `OpenClaw 2026.4.14 (323493f) — Shell yeah—I'm here to pinch the toil and leave you the glory.`
>
> Operating model: `vllm-shadow/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf` (fallback target during the 6h cascade)
> Originally-requested model: `ollama/qwen3:8b` (Docker-sandbox-dependent)
>
> Health-monitor: started 14:23:06 (interval: 300s, startup-grace: 60s, channel-connect-grace: 120s)
> Total cycles failing with class #1 cascade: 13 (14:37 / 15:04 / 15:34 / 16:04 / 16:34 / 17:04 / 17:34 / 18:04 / 18:34 / 19:04 / 19:34 / 20:04 / 20:34)

### Class #1 (Docker sandbox) — representative cycle (14:37:19)

```text
14:37:14 [agent/embedded] low context window: ollama/qwen3:8b ctx=16384 (warn<32000) source=modelsConfig; OpenClaw is using the configured model context limit for this model, so raise contextWindow/contextTokens if it is set too low
14:37:19 [diagnostic] lane task error: lane=main durationMs=149120 error="Error: Failed to inspect sandbox image: failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified."
14:37:19 [diagnostic] lane task error: lane=session:agent:orchestrator:main durationMs=149130 error="Error: Failed to inspect sandbox image: failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified."
14:37:19 [model-fallback/decision] model fallback decision: decision=candidate_failed requested=ollama/qwen3:8b candidate=ollama/qwen3:8b reason=unknown next=vllm-shadow/DeepSeek-R1-Distill-Llama-70B-Q4_K_M.gguf detail=Failed to inspect sandbox image: failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
14:37:28 Embedded agent failed before reply: Failed to inspect sandbox image: failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; check if the path is correct and if the daemon is running: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
```

This pattern repeats verbatim at 15:04, 15:34, 16:04, 16:34, 17:04, 17:34, 18:04, 18:34, 19:04, 19:34, 20:04, 20:34 — twelve more times.

### Class #3 (ws auth) — three reconnect attempts

```text
17:10:09 [ws] unauthorized conn=6323d168-... client=openclaw-control-ui webchat v2026.4.14 role=operator scopes=5 auth=none ... reason=token_missing
17:10:09 [ws] closed before connect conn=6323d168-... code=1008 reason=unauthorized: gateway token missing (open the dashboard URL and paste the token in Control UI settings)
17:10:36 [ws] unauthorized conn=8abb40ae-... (same pattern)
18:48:31 [ws] unauthorized conn=29ea3648-... (same pattern)
20:09:11 [ws] unauthorized conn=b6457843-... (same pattern)
20:09:38 [ws] unauthorized conn=76781ae8-... (same pattern)
```

### Class #4 (plugins.allow) — startup-time warning

```text
14:30:14 [plugins] plugins.allow is empty; discovered non-bundled plugins may auto-load: akos-runtime-tools (C:\Users\Shadow\.openclaw\extensions\akos-runtime-tools\index.ts). Set plugins.allow to explicit trusted ids.
14:30:19 [plugins] akos-runtime-tools: loaded without install/load-path provenance; treat as untracked local code and pin trust via plugins.allow or install records (C:\Users\Shadow\.openclaw\extensions\akos-runtime-tools\index.ts)
```

### Class #5 (bonjour) — self-healed

```text
14:27:32 [bonjour] watchdog detected non-announced service; attempting re-advertise (gateway fqdn=SHADOW-9H7SPBV9 (OpenClaw)._openclaw-gw._tcp.local. host=openclaw.local. port=18789 state=probing)
```

(Self-healed — no subsequent bonjour failures observed in 6h log window.)

## Section 6 — Cross-references

- I84 master-roadmap (substrate doctrine): [`docs/wip/planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md`](../../planning/84-substrate-doctrine-and-commercial-readiness/master-roadmap.md)
- AKOS runtime-contract rule: [`.cursor/rules/akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract"
- AKOS executable-process-catalog rule: [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 (SOP+runbook pairing) + Rule 2 (status enum)
- I77 P4.C wiring pattern to mirror for I87 P2 validator: [`scripts/validate_rendering_pipeline_registry.py`](../../../../scripts/validate_rendering_pipeline_registry.py) + [`akos/hlk_rendering_pipeline_csv.py`](../../../../akos/hlk_rendering_pipeline_csv.py)
- I77 P4 closure narrative (operational-style closure precedent): [`docs/wip/planning/77-impeccable-brand-bridge-refresh/reports/p4-brand-canon-collapse-remediation-2026-05-16.md`](../../planning/77-impeccable-brand-bridge-refresh/reports/p4-brand-canon-collapse-remediation-2026-05-16.md)
