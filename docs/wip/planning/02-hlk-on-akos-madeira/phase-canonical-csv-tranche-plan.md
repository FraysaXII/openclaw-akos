# Phase plan — Canonical CSV bulk tranche (approval-gated)

**Initiative:** `02-hlk-on-akos-madeira` / compliance program  
**Status:** Planned  
**Date:** 2026-04-15  

---

## Asset classification (per [PRECEDENCE.md](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths |
|:------|:------|
| **Canonical** | `docs/references/hlk/compliance/baseline_organisation.csv`, `process_list.csv`, taxonomy companions |

---

## Decision log

| ID | Question | Decision |
|:---|:-----------|:---------|
| D-CSV-1 | Gate | **No bulk CSV merge** without explicit operator approval recorded in plan/report or commit message reference |
| D-CSV-2 | Docs | Update [docs/USER_GUIDE.md](../../../USER_GUIDE.md) HLK Operator Model and [docs/ARCHITECTURE.md](../../../ARCHITECTURE.md) HLK sections when role/process counts change |

---

## Verification matrix

- `py scripts/validate_hlk.py` **mandatory** on every CSV or compliance taxonomy edit.
- Full [DEVELOPER_CHECKLIST.md](../../../docs/DEVELOPER_CHECKLIST.md) when paired code or registry readers change.
- `py scripts/validate_hlk_km_manifests.py` if Output 1 manifests are touched in the same tranche.

---

## Phased actions (outline)

1. Operator approval artifact (link or id) for batch scope — **template:** [reports/canonical-csv-tranche-operator-approval-template.md](reports/canonical-csv-tranche-operator-approval-template.md).
2. Dry-run diff + KiRBe impact note.
3. Apply CSV edits + validate + doc sync.
4. Release gate on branch.

**Registry:** [REG.006](../06-planning-backlog-registry/master-roadmap.md).
