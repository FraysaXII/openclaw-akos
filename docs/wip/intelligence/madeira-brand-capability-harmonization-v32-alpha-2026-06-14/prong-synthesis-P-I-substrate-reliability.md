---
intellectual_kind: research_synthesis_prong
prong_id: P-I
prong_topic: Substrate reliability — Windows gateway + multi-method portfolio
authored: 2026-06-15
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
decision_use: D-MBH-W1-01 mint gate + OpenClaw portfolio posture
---

# Prong P-I — Substrate reliability (refresh tranche R1)

## Executive outcome (plain language)

The **10-minute repair script is not the Holistika product** — it is the **AKOS adapter** on top of **upstream OpenClaw**, which on Windows has **known scheduled-task and health-probe bugs** (SRC-MBH-EXT-027..030). Post-reboot failure-then-PASS on 2026-06-14/15 matches upstream symptom class: **ready in logs but RPC/HTTP flaky**, **CLOSE_WAIT zombie listeners**, **probe too early during channel-connect grace**.

Research was sufficient to **name** substrate agnosticism (P-A); refresh tranche R1 adds **reliability evidence** so mint rows don't pretend OpenClaw is production-grade without proof-class binding.

## Ranked findings

| Rank | Finding | Sources | Confidence |
|:---:|:---|:---|:---|
| 1 | **Upstream owns root cause** — Windows schtasks races, WS 1008 misread as down, post-ready HTTP hang | EXT-027, EXT-028, EXT-029, EXT-030 | Euclid |
| 2 | **AKOS adapter is correctly tiered** — SOP §4.6 + repair script + `--check-only` post-reboot; operator RACI = escalate only | INT-041..043 | Safe |
| 3 | **Repair PASS ≠ MADEIRA α0** — anti-pattern #1 from master synthesis; closes CO-90-004 adapter proof only | INT-040, master § anti-patterns | Safe |
| 4 | **Portable alternative (LangGraph OSS)** — MIT library + self-host needs Postgres checkpointer, FastAPI health, OTEL; no built-in Windows tray gateway | EXT-031..033 | Euclid |
| 5 | **Multi-method portfolio is coherent** — primary OpenClaw + hardening + Scenario B without local gateway + time-boxed second substrate spike | Operator ratify 2026-06-15 | Safe |

## Upstream vs AKOS boundary

| Symptom | Owner | Holistika action |
|:---|:---|:---|
| schtasks `/Run` queued never Running | OpenClaw | Track version; upgrade when fixes land |
| WS 1008 treated as unhealthy | OpenClaw | Upstream probe fix (issue 48771) |
| Duplicate gateway windows on restart | OpenClaw | PR 52487 class |
| Post-reboot probe too early | **AKOS** | `--check-only --wait 180`; no stop/start after login |
| Zombie LISTEN + CLOSE_WAIT | **AKOS** | `ensure_gateway_port_free()` in runtime |
| No registry FK for gateway health | **Holistika vault** | PROOF_ADAPTER + SUBSTRATE row (mint gate) |

## Multi-method portfolio (operator-aligned)

All four postures from steering — **not contradictory** if each maps to a capability outcome:

| Posture | α0 role | Same outcome if done properly? |
|:---|:---|:---|
| Adapter band-aid + govern | Daily hygiene; OPS escalation | **Health probe PASS** with proof artifact |
| Hardening tranche (I87/I90) | Auto stale-listener, Langfuse trace on repair | **Faster deterministic PASS** |
| De-emphasize Scenario A | Prioritize Research Center (B) for experiential α0 | **Vault UI proof** without local gateway |
| Evaluation spike | LangGraph or LlamaIndex worker hits CAP-M* subset | **Same capability rows** with different `substrate_id` |

If a method cannot hit the same CAP-M* outcome row, it is **suboptimal** until DATA_CONTRACT defines a narrower scope.

## Gaps updated

| Gap | R1 disposition |
|:---|:---|
| GAP-MBH-03 (adapter registry not minted) | Mint gate packet drafted — Week-2 ratify |
| GAP-MBH-05 (gateway live PASS) | **Satisfied** with post-reboot evidence artifact — bind to PROOF_ADAPTER on mint |
| OpenClaw version pin vs upstream fixes | **Scheduled** — INTELLIGENCEOPS volatility row on next radar sweep |

## Mint gate inputs (for operator ratify Week-2)

See [`mint-gate-packet-draft-2026-06-15.md`](mint-gate-packet-draft-2026-06-15.md):

1. SUBSTRATE_REGISTRY — confirm `openclaw-local-windows` row + draft Make/n8n gaps
2. DATA_CONTRACT — `DC-HOL-SUBSTRATE-ADAPTER-001` fields from substrate audit
3. PROOF_ADAPTER — `proof-openclaw-gateway-repair-json` + `proof-openclaw-check-only-post-reboot`
4. CAPABILITY_REGISTRY — backfill CAP-M* seeds tied to adapter health (not net-new product capabilities)

## Anti-patterns this prong refuses

- Treating script duration (10 min) as architecture failure without separating upstream cold-start
- Minting SUBSTRATE rows without PROOF_ADAPTER pairing
- Abandoning OpenClaw before upstream fix + AKOS hardening tranche complete
- Declaring research "insufficient" — gap is **mint + proof**, not missing P-A..P-H
