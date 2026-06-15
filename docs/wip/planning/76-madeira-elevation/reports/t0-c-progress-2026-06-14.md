# T0-C progress — v3.2 closed alpha foundation (2026-06-14)

**Initiative:** I76 Madeira elevation annex  
**Operator ratification:** 2026-06-14 (full pack + BT-12 Option 6)

## Lane status

| Lane | Deliverable | Status |
|:---|:---|:---|
| **1 — I76 program** | `v32-closed-alpha-program-annex-2026-06-14.md` | **Done** — ratified + BT-12 linked |
| **2 — DG-A** | `substrate-data-governance-audit-2026-06-14.md` | **Done** (WIP; CSV mint gated) |
| **2 — DG-B** | `infonomics-substrate-join-2026-06-14.md` | **Done** (WIP) |
| **3 — Context** | `context-economics-wip-spec-outline.md` | **Done** (Keter gaps named) |
| **3 — I96 manifest** | Browser walk `localhost:3010` | **Scheduled** — dev server not up post-reboot; folder + plan minted |
| **4 — Gateway** | CO-90-004 / CO-MBH-005 | **Satisfied** pre-reboot; post-reboot re-verify in flight |
| **4 — Carryover** | CO-MBH-001..008 | **Minted**; CO-MBH-007 satisfied (BT-12) |
| **Logic** | LOGIC_CHANGE_LOG BT-12 | **Appended** `BT-12-madeira-alpha-governed-and-metered` |

## Post-reboot gateway note

Windows scheduled task auto-starts OpenClaw on login. **Check path:** `py scripts/openclaw_gateway_repair.py --check-only --json` (no restart). **Repair path:** full script when check-only fails. Operator does not run netstat/taskkill — SOP §4.6 RACI.

## I96 T0 blocker (CO-MBH-006)

| Blocker | Posture | Next |
|:---|:---|:---|
| `localhost:3010` not responding | **Scheduled** (not dropped) | AIC starts `hlk-erp` dev server + dev sign-in path when consumer repo available on host |
| Auth | Use `/api/dev/sign-in?next=/research-center` per B1.5 ladder | Magic link remains operator UAT path |

## Week-1 refresh (started 2026-06-15)

| Item | Status |
|:---|:---|
| Charter + P-I synthesis | **Done** |
| Source ledger +12 rows (78 total) | **PASS** validator |
| Mint gate packet draft | Ready for Week-2 ratify |
| Carryover **CO-MBH-W1** | **Scheduled** → review 2026-06-22 |

See `week-1-substrate-reliability-refresh-charter.md` in research pack.

```powershell
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/madeira-brand-capability-harmonization-v32-alpha-2026-06-14/source-ledger.csv
py scripts/verify.py pre_commit_fast
```

## T1 carryover (scheduled)

- I96 manifest captures complete (CO-MBH-006)
- Canonical CSV mint gates (SUBSTRATE gaps, DATA_CONTRACT DC-HOL-SUBSTRATE-ADAPTER-001)
- FOUNDER_METHODOLOGY_VERSIONING §2 lineage row for v3.2 (companion to LOGIC_CHANGE_LOG §3)
