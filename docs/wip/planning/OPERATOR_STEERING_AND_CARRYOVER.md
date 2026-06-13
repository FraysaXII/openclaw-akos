# Operator steering + carryover execution (plain contract)

> **Ratified by operator 2026-06-12** — recovery from multithreaded drift.  
> **Goal:** MADEIRA / AIC does the work you *can* delegate; you keep **decisions and steering** only.

---

## Who does what

| You (operator) | AIC (MADEIRA / agent) |
|:---|:---|
| Pick **one active spine** initiative at a time | Execute phases on that spine (research, validators, docs, index rows) |
| Answer **inline ratify** gates (yes/no/options with evidence) | Prepare evidence packets; never invent ratifications |
| Approve **registry / canonical CSV** rows when required | Draft rows + run validators; stop at the gate |
| Say **do or don't** — no optional middle | Disposition parked items as scheduled / done elsewhere / dropped |
| Steer when parallel work would split attention | Refuse new cross-cutting governance threads while spine is open |

**Not optional:** If work is parked, it must have **what unlocks it**, **who owns it**, and **when we review it if still open**. Otherwise it is invalid — treat as a planning bug, not a note.

---

## Three rules (order of execution)

### 1. Single spine first

**Now:** **Infonomics / data economics research program** phase 0 — registry approval + first research tranche on the **full planning bar** (roadmap, decision log, verification, pause at registry gate).

**Do not** open new cross-cutting governance initiatives until that pause clears — unless you explicitly redirect.

### 2. No parked work without a gate

Every item in the [carryover index](_trackers/carryover-posture-index.md) must have:

- **Activation trigger** — what must be true before work starts  
- **Owner** — role who moves it (not “the team”)  
- **Next review** — when we re-check if the row is still true (staleness guard)

Bare “later” or “deferred” in **new** artifacts is invalid.

### 3. Closure updates the index

When **any** initiative closes, the agent must answer in the closure UAT:

> Did this closure **satisfy**, **supersede**, or **leave unchanged** any carryover index row?

If satisfied elsewhere → update the index and any old parked prose **in the same closure pass**. No silent completion in another thread.

---

## How you act on the old cleanup backlog (~75 catalogued spots)

You do **not** grind through all of them.

| When | You do |
|:---|:---|
| **Starting the spine initiative** | Skim index + sweep report rows for **that** program only |
| **Closing any initiative** | Rule 3 — index propagation checklist |
| **Weekly or when confused** | Open index; any row missing **next review** → fix or disposition |
| **Otherwise** | Ignore the backlog until a file is touched |

The P3 area sweep report is a **map of suspects**, not homework due tomorrow.

---

## Where this lives mechanically

- Posture list + required fields: `akos/planning/carryover_posture.py`  
- Index: `docs/wip/planning/_trackers/carryover-posture-index.md`  
- Row template: `docs/wip/planning/_templates/carryover-posture-row.md`  
- Closure checklist: `docs/wip/planning/_templates/uat-closure-template.md` §10  
- Agent rules: `.cursor/rules/akos-operator-communication.mdc` RULE 6–7, `akos-planning-traceability.mdc` carryover execution contract  

---

## Recovery decision record

Operator chose **all three rules** (spine → gate → closure propagation) on 2026-06-12 after clarifying that vocabulary alone did not fix stale or silently completed parked work. Recorded in I98 decision log as steering recovery.
