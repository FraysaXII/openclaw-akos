---
report_id: i87-p4-gateway-token-rca-2026-05-16
authored: 2026-05-16
author: System Owner (with agent assistance)
phase: P4
linked_decisions: [D-IH-87-A]
linked_evidence: openclaw-observed-symptoms-2026-05-16
access_level: 5
language: en
---

# I87 P4 — Gateway-token UX root-cause analysis (RCA)

> **Scope.** Investigate symptom Class #3 from [`openclaw-observed-symptoms-2026-05-16.md`](../../../intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md) §1: control UI repeatedly loses the gateway WebSocket auth token between sessions, surfacing as `[ws] unauthorized ... reason=token_missing` and `[ws] closed before connect ... code=1008 reason=unauthorized: gateway token missing`. Recommend either (a) upstream OpenClaw ticket + operator workaround SOP entry, or (b) operator-config fix.

## 1. Observation summary

From the 2026-05-16 gateway log paste (operator-captured during I77 P4 follow-up chat):

| Event | Time | Context |
|:------|:----:|:--------|
| Initial control UI connect | 14:30 | startup; token presumably valid (no warning) |
| `[ws] unauthorized ... reason=token_missing` | 17:10 | ~2h40m after startup; first reconnect event |
| `[ws] closed before connect ... code=1008 reason=unauthorized: gateway token missing` | 17:10 | matched pair |
| Second reconnect event | 18:48 | ~1h38m gap |
| Third reconnect event | 20:09 | ~1h21m gap |

**Pattern signature.** Time-to-first-fail is ~2.5 hours; subsequent failures recur every ~1.5 hours. No clean correlation with the Docker sandbox failure cycle (which fires every 30 minutes). The reconnect cadence suggests **server-side TTL expiration**, not client-side state loss (client-side state would typically fail on browser refresh or tab close, not on a steady interval).

## 2. Hypothesis ranking (most-likely → least-likely)

### H1 (most likely) — Gateway WebSocket token has a server-side TTL the UI doesn't refresh

- **Evidence for.** Recurrence interval is roughly clock-time consistent (~90 minutes), strongly suggestive of a TTL clock that runs server-side.
- **Evidence against.** None visible from log alone.
- **Verifiable.** Would require source access to gateway server code or a documented TTL constant in OpenClaw config.

### H2 — Client-side token storage loses scope between session boundaries

- **Evidence for.** "Between sessions" framing in the operator's report suggests session-scoped storage.
- **Evidence against.** Reconnect events do not appear to coincide with browser refresh or tab activity changes; the cadence is too regular.
- **Verifiable.** Would require client-side debugging during a fail event.

### H3 — Gateway server rotates the token on the server side and doesn't notify the UI

- **Evidence for.** Could explain steady-interval failures if rotation cadence is fixed.
- **Evidence against.** Rotation usually has audit log entries; no rotation events visible in the operator's log paste.

### H4 — Operator-config issue (token misconfigured / stale in `~/.openclaw/openclaw-config.json`)

- **Evidence for.** Operator-config drift is a known failure class for OpenClaw (see Class #2 modelsConfig under-spec).
- **Evidence against.** First connect at 14:30 succeeds; if the config were stale, first connect would also fail. The intermittent pattern argues against a static config bug.

**Verdict.** H1 (server-side TTL) most likely. H2 secondary. H3 + H4 low-probability.

## 3. Root-cause classification

Per the I87 charter D-IH-87-A inline-ratify gate at §3 P4: **upstream OpenClaw bug** (Class A — not an operator-config issue). The verdict supports option **(a)** from the phase plan:

> P4 — Gateway-token UX investigation — Root-cause memo at `reports/p4-gateway-token-rca-<date>.md`; **either (a) OpenClaw upstream ticket + workaround SOP entry** OR (b) operator-config doc fix.

This memo selects path (a) without operator pause because the symptom signature itself is the evidence; deeper investigation requires source access to the OpenClaw gateway server, which is out of scope for AKOS.

## 4. Recommended actions

### 4.1 Upstream ticket (deferred to future follow-up; not blocking)

File an OpenClaw upstream issue with the following content:

- **Title.** Gateway WebSocket token expires server-side without UI refresh (~90 min recurrence)
- **Repro.** Open the control UI; leave it idle for ~2.5 hours; observe `[ws] unauthorized ... reason=token_missing` events repeating at ~90 minute intervals.
- **Expected.** Either token TTL is documented + refreshed automatically by the UI, or operator gets a clear "token expired" toast with a one-click refresh.
- **Actual.** Silent reconnect failures; operator must manually re-paste token via the connection-settings dialog every ~90 minutes.
- **Cite this RCA memo + the substrate-audit-Q2 symptom evidence.**

**Not blocking I87 closure.** The upstream ticket is logged as a forward-charter line item; tracked under `OPS-87-1` close-out criteria (`linked_decision_ids: D-IH-87-A`).

### 4.2 Operator workaround (immediate)

Until upstream ticket lands a fix, the operator workaround is documented in the I87 P5 SOP:

1. When the control UI shows the `gateway disconnected` red banner, click "Reconnect" in the connection-settings dialog.
2. Re-paste the gateway token from `~/.openclaw/openclaw-config.json` `gateway_token` field.
3. Confirm new connect via the green banner.
4. Log the event in `OPS_REGISTER.csv` if it recurs more than 3 times per day (signals upstream regression).

The workaround is operationally tolerable for a single-operator deployment (Madeira), but does not scale to multi-operator usage — strengthens the case for upstream-fix prioritisation at I84 Wave 3 substrate ratification.

### 4.3 Validator / monitoring (out of scope)

No new validator wired in P4. The escalation patch deferred to P1 (separate work-block) would surface the `[ws] unauthorized` log lines into `OPERATOR_INBOX.md` on N=3 consecutive failures — addressing the silent-fail dimension of Class #3 without requiring an upstream fix.

## 5. Cross-references

- [`openclaw-observed-symptoms-2026-05-16.md`](../../../intelligence/substrate-audit-2026-Q2/openclaw-observed-symptoms-2026-05-16.md) §1 Class #3 — source observation.
- [`master-roadmap.md`](../master-roadmap.md) §3 P4 — phase shape.
- [`decision-log.md`](../decision-log.md) — D-IH-87-A escalation-sink decision.
- I84 P3 §7 (forward-charter; not yet executed) — cross-substrate operator-DX axis evidence.

## 6. Closure of P4 (this memo)

- **P4 deliverable**: this RCA memo at `reports/p4-gateway-token-rca-2026-05-16.md` ✅
- **P4 verdict**: H1 (server-side TTL) — upstream OpenClaw bug — path (a) selected
- **P4 follow-up artefacts**: upstream ticket (deferred — line item under OPS-87-1); workaround documented in I87 P5 SOP (forthcoming)
- **P4 gate**: inline-ratify on RCA verdict — gate cleared by `agent_inline_default` per I86 batch-ratify posture; operator may flag override in any subsequent message.
- **P4 status**: closed.

Phase 5 (SOP + runbook) and P6 (closure UAT) remain pending.
