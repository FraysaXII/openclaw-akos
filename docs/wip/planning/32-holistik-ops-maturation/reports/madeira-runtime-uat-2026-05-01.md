---
language: en
status: active
intellectual_kind: phase_evidence
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: Founder + System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# MADEIRA runtime UAT — post-I32 SKILL_REGISTRY landing

**Evidence id:** UAT-MADEIRA-RUNTIME-2026-05-01
**Closes:** D-IH-32-Q9 ("Live MADEIRA runtime UAT confirms no regression after SKILL_REGISTRY landed")
**Run by:** AKOS executor on operator's local machine (gateway live at `http://127.0.0.1:18789`)
**Branch:** `i32-holistik-ops-maturation` (pushed to remote `2026-05-01` 02:55 UTC)

## Method

Two complementary smoke layers:

### Layer 1 — Live HTTP probes (auth-open endpoints only)

| Endpoint | Result | Latency | Body shape |
|---|---|---|---|
| `GET /healthz` | HTTP 200 | < 30 ms | `{"ok":true,"status":"live"}` |
| `GET /diag/process_status` | HTTP 200 | ~ 20 ms | full diag JSON |

Authenticated endpoints (`/agents`, `/status`, `/routing/classify`) returned the OpenClaw Control SPA shell rather than JSON because no `AKOS_API_KEY` is set in `~/.openclaw/.env`. This is **gateway-correct behavior** (`_check_api_key` falls back to the static index for browser flows). To exercise the actual code paths without auth, Layer 2 was added.

### Layer 2 — In-process exerciser (`madeira_uat_inproc.py`)

Imports the same modules the gateway uses, no HTTP middleware in the loop. 8 checks:

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | env bootstrap | PASS (35 ms) | `akos.io.bootstrap_openclaw_process_env` clean |
| 2 | SKILL_REGISTRY load | PASS | 5 rows / 14 fields enforced |
| 3 | TOUCHPOINT_KIT_CELL_REGISTRY load | PASS | 15 rows / 10 fields |
| 4 | POLICY_REGISTER load | PASS | 14 rows / 11 fields |
| 5 | REPO_HEALTH_SNAPSHOT load | PASS | 3 rows / 10 fields |
| 6 | `classify_request` smoke | PASS (757 ms cold) | keys = `route, confidence, method, must_escalate, reason` |
| 7 | 5 intent probes (1 per skill) | PASS (174 ms total, ~35 ms each) | `orchestrator-fallback = 0/5` (canary 5 condition) |
| 8 | `validate_hlk` dispatcher full vault | PASS (3033 ms) | `OVERALL: PASS` |

**Total: 8/8 green.**

### The 5 intent probes (canary 5)

These are the queries that, before I32, would be the most likely to fall through to "ask Orchestrator". After SKILL_REGISTRY landing, all 5 classify cleanly without fallback:

1. "Need a quick lookup on Madeira's lore" → mapped to `skill_madeira_lookup_v1`
2. "Plan a 5-phase rollout for the new persona" → `skill_architect_plan_v1`
3. "Run the test suite and report failures" → `skill_executor_run_v1`
4. "Verify the patch matches the spec" → `skill_verifier_check_v1`
5. "Detect the language of this French paragraph" → `skill_shared_locale_detect_v1`

`orchestrator-fallback = 0/5` confirms canary 5 ("UAT smoke detects 'ask Orchestrator' fallback") is currently quiet.

## Verdict

**D-IH-32-Q9: PASS.** Runtime is unchanged after the SKILL_REGISTRY (and 4 new mirror) landing. No latency regression detected (cold classify ~ 0.75 s, warm probes ~ 35 ms each — within the I27 baseline envelope). No fallback-to-orchestrator regression. Validator and dispatcher remain green on the full vault (the vault now includes 4 new I32 dimensions).

## What this UAT does NOT cover

- The MADEIRA observation dashboard rendered in a browser (would need an `AKOS_API_KEY` set + the operator clicking through). This is light to set up if needed (Q10): set `AKOS_API_KEY=<random>` in `~/.openclaw/.env`, restart the gateway, hit `http://127.0.0.1:18789/madeira/control` with `Authorization: Bearer <key>`.
- Live Langfuse trace shape validation (canary 3). Defers to Initiative 45 if approved.
- Live Neo4j projection counts. Blocked on Aura `AuthError` (separate evidence note: `neo4j-aura-auth-diagnosis-2026-05-01.md`).

## Reproduction

```powershell
# From AKOS repo root, with gateway running:
py c:\Users\Shadow\AppData\Local\Temp\madeira_uat_inproc.py
```

(Script source recorded in operator's local `%TEMP%` folder; promote into
`tests/test_madeira_runtime_uat.py` if D-IH-45-* approves keeping it.)
