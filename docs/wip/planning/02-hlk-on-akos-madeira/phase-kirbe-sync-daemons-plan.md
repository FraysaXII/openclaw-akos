# Phase plan — KiRBe sync daemons (mirrored automation)

**Initiative:** `02-hlk-on-akos-madeira` (execution handoff from NBT proposal)  
**Status:** Planned  
**Date:** 2026-04-15  

**Upstream design:** [reports/next-baseline-kirbe-sync-boundary-proposal.md](reports/next-baseline-kirbe-sync-boundary-proposal.md)

---

## Asset classification (per [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Rule |
|:------|:-----|
| **Canonical** | `docs/references/hlk/compliance/` and approved `v3.0/` vault markdown |
| **Mirrored / derived** | KiRBe, Supabase, Drive — **subordinate** to canonical; automation must replay and surface drift evidence |

---

## Decision log

| ID | Question | Decision |
|:---|:-----------|:---------|
| D-KSD-1 | Authority | Canonical wins on conflict; daemons never silently overwrite canonical CSVs without approval-gated job design |

---

## Verification matrix

- Implementation under `scripts/` / `akos/`: full [DEVELOPER_CHECKLIST.md](../../../docs/DEVELOPER_CHECKLIST.md).
- Vault doc-only updates: `py scripts/validate_hlk.py` minimum.

---

## Action IDs (from NBT)

Align implementation tasks with `NBT.1`–`NBT.5` in the boundary proposal; add phase reports under `reports/` as work starts.

**Registry:** [REG.005](../06-planning-backlog-registry/master-roadmap.md).
