---
title: SOP — OpenClaw runtime health triage
language: en
intellectual_kind: tech-lab-canonical-sop
sop_id: SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001
access_level: 4
confidence_level: A1
source_taxonomy: holistika-internal-sop
authors:
  - System Owner
last_review: 2026-05-19
last_review_by: System Owner
ratifying_decisions:
  - D-IH-87-A
  - D-IH-87-B
  - D-IH-87-C
  - D-IH-87-CLOSURE
status: active
register: internal
linked_canonicals:
  - OPS_REGISTER.csv
  - INITIATIVE_REGISTRY.csv
linked_runbooks:
  - scripts/openclaw_health_escalate.py
  - scripts/openclaw_gateway_repair.py
  - scripts/validate_openclaw_plugin_pinning.py
linked_processes:
  - env_tech_dtp_openclaw_runtime_health_triage_001
cadence: event_triggered
cadence_secondary: on_demand
cadence_secondary_trigger: operator-observed runtime symptom outside the five known classes
---

# SOP — OpenClaw runtime health triage

> **Status: `active`** (promoted `review` → `active` 2026-05-19 at I87 P6 closure UAT per D-IH-87-CLOSURE; UAT report at [`docs/wip/planning/87-openclaw-operator-runtime-hardening/reports/uat-i87-closure-2026-05-19.md`](../../../../../wip/planning/87-openclaw-operator-runtime-hardening/reports/uat-i87-closure-2026-05-19.md) — synthetic 3-symptom-class dry-run drill PASS for ws-token-expiration + docker-sandbox-churn + low-context-warning).

## 1. Purpose

Codifies the operator-facing triage tree for the five OpenClaw runtime symptom classes surfaced during the substrate audit on 2026-05-16 ([`openclaw-observed-symptoms-2026-05-16.md`](../../../../../../wip/intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md) §2). Each class routes to a governed action — emission to `OPS_REGISTER.csv`, validator invocation, or upstream-ticket workflow — so the runtime contract violation flagged by [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract" (`Runtime: unknown` treated as healthy) stays falsifiable.

## 2. Scope

In scope:

- Operator triage of OpenClaw control-plane health symptoms.
- Emission to `OPS_REGISTER.csv` via [`scripts/openclaw_health_escalate.py`](../../../../../../../scripts/openclaw_health_escalate.py) (D-IH-87-A escalation contract).
- Plugin allow-list policy validation via [`scripts/validate_openclaw_plugin_pinning.py`](../../../../../../../scripts/validate_openclaw_plugin_pinning.py) (D-IH-87-B).
- modelsConfig hygiene posture (D-IH-87-C).
- Gateway-token UX workaround until upstream OpenClaw bug fix lands.

Out of scope:

- Substrate-doctrine decisions (I84 owns; this SOP triages on the **currently deployed** substrate).
- OpenClaw upstream code changes (file via upstream issue tracker; this SOP records the workaround, not the fix).
- Operator-local credential management (covered by [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §SOC).

## 3. Inputs

- Operator-visible OpenClaw control UI or terminal output.
- `~/.openclaw/openclaw.json` (operator-local config; not git-canonical).
- `config/openclaw.json.example` (git-canonical example).
- `config/environments/dev-local.json` (git-canonical environment overlay).
- The five symptom classes named in I87 P0 charter.

## 4. The five symptom classes — triage tree

### 4.1 Docker sandbox churn

**Signature.** Container restart loop in OpenClaw sandbox provisioning; log messages reference container ID regeneration faster than 30s intervals.

**Triage steps.**

1. Observe ≥ 3 churn cycles within a 5-minute window.
2. Invoke `py scripts/openclaw_health_escalate.py --symptom-class docker-sandbox-churn --consecutive-failures <N> --evidence-path <log-path>`.
3. The runbook appends one OPS-87-N row with `status=open` + `owner_class=operator`.
4. `scripts/render_operator_inbox.py` surfaces the row at the next render (manual or release-gate-triggered).
5. Operator reviews and either (a) restarts the OpenClaw sandbox host, (b) escalates to upstream OpenClaw issue tracker, (c) marks the OPS row `status=closed` if churn stops.

### 4.2 Low LLM context warning

**Signature.** Gateway log warns about `qwen3:8b` context window; despite the warning, requests succeed via the vLLM fallback path.

**Triage steps.**

1. Per **D-IH-87-C** the canonical fix is to remove `qwen3:8b` from `ollama.models` (already landed in P3).
2. If the warning persists in a deployed environment, verify the deployment's modelsConfig matches the canonical `config/openclaw.json.example` (no `qwen3:8b` row; fallback chain ends at `llama3.1:8b`).
3. If deployment diverges, file an OPS row via the escalation helper with `--symptom-class low-context-warning`.

### 4.3 Gateway WebSocket auth churn (ws-token-expiration)

**Signature.** Repeated `[ws] unauthorized` events at irregular intervals; first failure ~2.5h after session start, then every ~1.5h.

**Triage steps.**

1. Per the P4 RCA memo ([`reports/p4-gateway-token-rca-2026-05-16.md`](../../../../../../wip/planning/87-openclaw-operator-runtime-hardening/reports/p4-gateway-token-rca-2026-05-16.md)) the root cause is **server-side TTL expiration** (upstream OpenClaw bug, Class A).
2. **Workaround.** Operator re-authenticates the gateway session via the OpenClaw control UI when the symptom appears. No code action required from AKOS.
3. File an OPS row with `--symptom-class ws-token-expiration` when the pattern recurs ≥ 3 times in a single working day, so the upstream ticket carries cumulative evidence.
4. **Upstream action.** File an issue at the OpenClaw repository linking to the RCA memo. Until upstream lands a fix, the workaround stands.

### 4.4 plugins.allow trust posture

**Signature.** Operator review of `~/.openclaw/openclaw.json` reveals plugins outside the AKOS-curated allow-list, or required AKOS-pinned plugins missing.

**Triage steps.**

1. Run `py scripts/validate_openclaw_plugin_pinning.py` against `config/openclaw.json.example`.
2. Per **D-IH-87-B** the validator enforces: (a) `akos-runtime-tools` MUST be present and pinned, (b) third-party entries warn if not in the known-third-party list, (c) orphan entries (declared but never used) fail.
3. The validator is wired into `release-gate.py` as INFO; failures surface but never block.
4. For operator-local config drift, the operator manually reconciles `~/.openclaw/openclaw.json` against the canonical example.

### 4.5 Bonjour self-heal (modelsConfig fallback chain)

**Signature.** OpenClaw silently routes to a fallback model when the primary is unavailable, without an operator-visible signal.

**Triage steps.**

1. Per **D-IH-87-C** the fallback chain is canonical at `agents.defaults.model.fallbacks: ["ollama/llama3.1:8b"]` (P3 deliverable; `qwen3:8b` removed since the bonjour fallback to vLLM was already happening).
2. If a self-heal event is suspected (e.g., responses arrive but from a different model than configured), check gateway logs for fallback-route markers.
3. File an OPS row with `--symptom-class bonjour-self-heal` when fallback events are observed but not desired (the canonical posture is to honor the explicit fallback chain; silent re-routing outside the chain is a bug).

### 4.6 Gateway schema drift, cold start, and stale listeners (Windows)

**RACI (binding for AKOS).** Gateway repair is **AIC / Envoy Tech Lab execution** — not operator manual ops. The operator does **not** run `netstat`, `taskkill`, or PID hunting. Routine recovery is one governed command (`py scripts/openclaw_gateway_repair.py`); the agent or automation runs it. The operator’s only action on persistent failure is **escalation** via `py scripts/openclaw_health_escalate.py --symptom-class gateway-cold-start` (OPS row + inbox), per **D-IH-87-A** and operator steering **RULE 6**.

**Signature.** `openclaw gateway start` or `doctor --repair-gateway` exits non-zero; port `18789` shows LISTENING but HTTP/RPC probes time out; config validation rejects legacy `sandbox.mode: strict`; gateway log shows **ready** only after 45–90s of plugin load; RPC may stay unavailable for up to **120s** after ready (OpenClaw `channel-connect-grace`); many `CLOSE_WAIT` sockets on Windows.

**Triage steps (AIC-run).**

0. After reboot, prefer **`py scripts/openclaw_gateway_repair.py --check-only --json`** first — probes HTTP+RPC without stopping the Windows scheduled-task auto-start.
1. Run `py scripts/openclaw_gateway_repair.py` (pairs with this SOP; normalizes `~/.openclaw/openclaw.json`, warm-path skip when already healthy, Windows scheduled-task stop + stale listener release, **two automated attempts** by default).
2. Allow the **full cold-start window**: plugin load (45–90s) **plus** channel-connect grace (**120s** after HTTP ready on Windows). AKOS waits **130s** post-ready before judging RPC failure.
3. If repair still fails after automated retries, AIC inspects the log path from `openclaw gateway status` for pricing/bootstrap **TimeoutError** (see USER_GUIDE §17) or invalid config lines — still **not** operator netstat surgery.
4. File an OPS row with `--symptom-class gateway-cold-start` when the pattern recurs ≥ 3 times in one working day after the repair runbook (operator ratifies closure of the OPS row only).

**AKOS posture.** Upstream OpenClaw owns WebSocket/RPC semantics; AKOS supplies config normalization (`akos/openclaw_config.py`), recovery timing (`akos/runtime.py`), and this runbook so the operator stack adapts without forking the gateway.

**Upstream issue cross-links (v3.2 alpha substrate reliability).** Source ledger IDs **SRC-MBH-EXT-027..030** — GitHub **#63491** (post-ready HTTP hang / stale cron), **#48771** (schtasks WS 1008 probe misread), **#49871** (Run Queued never Running), **#41804** / **#61579** (Session 0 / schtasks races). Research pack: [`madeira-brand-capability-harmonization-v32-alpha-2026-06-14`](../../../../../../wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/openclaw-hardening-tranche-charter.md). Repair JSON may include `langfuse_trace_logged` when Langfuse credentials are configured (H3).

## 5. Outputs

- One OPS-87-N row in `OPS_REGISTER.csv` per escalation event (status:open at emission; status:closed by operator after action).
- `OPERATOR_INBOX.md` auto-refresh (via `scripts/render_operator_inbox.py`) surfacing the row.
- Upstream OpenClaw ticket reference (when applicable; recorded in the OPS row's `notes` field).
- `validate_openclaw_plugin_pinning.py` INFO row in `release-gate.py` output.

## 6. Failure modes

| Failure | Detection | Recovery |
|:---|:---|:---|
| Idempotency guard fires false-positive (e.g., transient closed-then-reopened state) | Operator sees no new OPS row after re-running the helper | Manually amend the prior open row's `notes` to record the recurrence; do not bypass the guard |
| Escalation helper run with bad symptom-class slug | `ValueError: symptom_class must match` | Re-run with a valid slug from §4.x or invent a new slug matching `[a-z][a-z0-9-]{2,40}` |
| `OPS_REGISTER.csv` not found | `FileNotFoundError` | Repository is not a fresh AKOS checkout; verify cwd; restore from git |
| validate_hlk fails on the appended OPS row | release-gate output | Inspect the row for schema mismatches (RICE impact tier; date format); fix manually then re-validate |

## 7. Cross-references

- **Initiative 87 charter.** [`master-roadmap.md`](../../../../../../wip/planning/87-openclaw-operator-runtime-hardening/master-roadmap.md).
- **Charter decisions.** D-IH-87-A (escalation sink), D-IH-87-B (plugin pinning), D-IH-87-C (modelsConfig hygiene).
- **Paired runbooks.** [`scripts/openclaw_health_escalate.py`](../../../../../../../scripts/openclaw_health_escalate.py) (escalation); [`scripts/openclaw_gateway_repair.py`](../../../../../../../scripts/openclaw_gateway_repair.py) (repair §4.6). Per [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1.
- **P4 RCA memo.** [`reports/p4-gateway-token-rca-2026-05-16.md`](../../../../../../wip/planning/87-openclaw-operator-runtime-hardening/reports/p4-gateway-token-rca-2026-05-16.md).
- **Substrate audit evidence.** [`openclaw-observed-symptoms-2026-05-16.md`](../../../../../../wip/intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md).
- **Process registration.** `process_list.csv` row `env_tech_dtp_openclaw_runtime_health_triage_001`.
- **Governance rules.** [`akos-governance-remediation.mdc`](../../../../../../../.cursor/rules/akos-governance-remediation.mdc) §"Runtime contract"; [`akos-executable-process-catalog.mdc`](../../../../../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 pairing.

## 8. Promotion criteria (status:review → status:active)

This SOP is at `status: review` until **all** of the following hold:

1. I87 P6 closure UAT executes a synthetic three-failure-cycle scenario end-to-end (operator runs the escalation helper; OPS row appears; OPERATOR_INBOX renders; row closed by operator).
2. The UAT report at `reports/p6-closure-uat-<date>.md` records PASS for all five symptom classes (at least one event per class, or a documented N/A reason).
3. `validate_hlk.py` PASS over the canonical CSVs after the UAT (OPS_REGISTER, INITIATIVE_REGISTRY, DECISION_REGISTER).
4. Operator approval (inline-ratify) of the promotion commit.

Per [`SOP-META_PROCESS_MGMT_001.md`](../../People/canonicals/SOP-META_PROCESS_MGMT_001.md) §4.3 lifecycle.
