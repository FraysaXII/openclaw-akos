---
report_type: l3-ratification
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L3-4 (R2-05)
authored: 2026-06-09
authored_by: PMO (execution seat)
closure_decision_source: agent_inline_default
ratifying_decisions:
  - D-IH-95-B
verdict: PASS
disposition_summary: TRP-030 and TRP-036 remain planned; forward-charter until FK surfaces exist
---

# L3 TRP-030 / TRP-036 ratification — 2026-06-09

**Lane:** L3 FK→verb tranches (R2-05). **Prior tranche:** L3-3 at `bfe48ca` promoted TRP-031/032 only.
**Operator posture:** Per-triple inline-ratify; no bulk promote; do not invent FK columns.

## Evidence sweep

### TRP-030 — AIC assignment → process (`HCAM-TRP-030`)

| Signal | Finding |
|:---|:---|
| Registry `current_fk` | `new` (no populated CSV FK) |
| `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` columns | `matrix_id`, `capability_id`, `aic_id`, … — **no `process_id` or `process_item_id`** |
| Matrix row count | 2 data rows (both `CAP-MADEIRA-SCENARIO-LIFECYCLE` × two AICs) |
| Related active triple | **TRP-038** — `aic_capability_implementation_matrix` binds AIC→capability (`REALIZES`) |
| Indirect path | AIC→capability (TRP-038) → process via TRP-006 (`capability_registry.originating_process_ids`) — advisory, not assignment FK |
| `validate_fk_verb_coverage.py` registry map | `aic_capability_implementation_matrix` allows only `matrix_id`, `capability_id`, `aic_id` |

**Conclusion:** No direct FK surface for assignment verb to process. Promotion would require a **new**
canonical-CSV column or dedicated AIC↔process register — canonical-CSV operator gate.

### TRP-036 — initiative composition → workstream (`HCAM-TRP-036`)

| Signal | Finding |
|:---|:---|
| Registry `current_fk` | `process_list.item_granularity;process_list.item_parent_1_id` (documented paths; **not initiative-scoped**) |
| `INITIATIVE_REGISTRY.csv` columns | `program_anchors` (semicolon program IDs) — **no `workstream_item_id` or initiative→process_list FK** |
| I95 row example | `INIT-OPENCLAW_AKOS-95` has `program_anchors=PRJ-HOL-PGF-2026;PRJ-HOL-OPS-2026` — narrative link only |
| TRP-031 (active) | program→workstream via `process_list` parent/granularity — **different source entity** (program layer, not initiative registry) |
| `validate_fk_verb_coverage.py` | `initiative_registry` map: `initiative_id`, `program_anchors`, `status` only |

**Conclusion:** Initiative→workstream is charter-documented but **not FK-populated**. Promotion without a
new `INITIATIVE_REGISTRY` anchor column would falsely claim CSV-backed composition.

---

## Inline-ratify options (operator not in session — documented)

### TRP-030

| Option | Action | When to pick |
|:---|:---|:---|
| **A — Keep planned (recommended)** | No registry/bindings change; forward-charter mint `process_item_id` on matrix or new register | FK evidence absent (current state) |
| **B — Promote with `new` FK token only** | Set `status=active` leaving `current_fk=new` | **Rejected** — violates no-invent-FKs + validator would not gain L3 bindings |
| **C — Scope-extend OPS row** | OPS-95-L3-030: design AIC↔process join surface + canonical-CSV gate | Operator wants explicit tracker before CSV mint |

### TRP-036

| Option | **A — Keep planned + forward-charter (recommended)** | **B — Promote using process_list paths** | **C — Mint `workstream_anchors` column** |
|:---|:---|:---|:---|
| Action | Status stays `planned`; document resolution in tracker | **Rejected** — conflates initiative entity with program-layer TRP-031 | Add `INITIATIVE_REGISTRY` column + populate + re-ratify (canonical-CSV gate) |
| FK honesty | Honest | Would imply initiative FK exists today | Clean promotion path |

**Agent inline default (24h+ reversible):** Option A for both triples — matches L3-3 conservative deferral
and operator no-deferrals posture **only where FK evidence supports promotion** (it does not here).

---

## Disposition (this session)

| Triple | Plain language | Disposition | Registry `status` | `L3_FK_BINDINGS` change |
|:---|:---|:---|:---:|:---:|
| **TRP-030** | AI collaborator performs a process | **Keep planned** | `planned` | none |
| **TRP-036** | Initiative composed of workstreams | **Keep planned** | `planned` | none |

No edits to `akos/hlk_canonical_articulation.py` or `CANONICAL_RELATIONSHIP_REGISTRY.csv` — promotion
would be dishonest without new FK columns.

---

## Forward-charter resolution conditions

### TRP-030 closes when

1. A governed CSV (matrix extension or new register) carries a resolvable `process_item_id` (or successor) FK column.
2. `validate_fk_verb_coverage.py` `_FK_REGISTRY_COLUMNS` includes the new column.
3. `L3_FK_BINDINGS` adds `(registry, column, HCAM-TRP-030)` tuple(s).
4. Operator inline-ratify promotes registry row `planned` → `active`.

### TRP-036 closes when

1. `INITIATIVE_REGISTRY.csv` gains a populated workstream anchor column (or charter-approved join table).
2. FK token updates from `new` / process_list-only paths to initiative-scoped paths.
3. L3 bindings + validator map extended; per-tranche ratification re-run.

**Tracker suggestion:** `docs/wip/planning/_trackers/i95-trp-036-initiative-workstream-fk-tracker.md` at
next Semantic Council slice (L4 orphan burn-down) — not minted this session (docs-only ratification pass).

---

## Verification (unchanged bindings)

```text
py scripts/validate_fk_verb_coverage.py
  PASS: FK->verb L3 - 22 bindings, 17 registry column maps

py scripts/validate_hlk.py
  (no change expected — relationship registry is Data/Architecture git SSOT)
```

---

## Cross-references

- Prior tranche: [`l3-fk-verb-tranche3-2026-06-08.md`](l3-fk-verb-tranche3-2026-06-08.md)
- Registry SSOT: `CANONICAL_RELATIONSHIP_REGISTRY.csv` rows HCAM-TRP-030 / HCAM-TRP-036
- Bindings SSOT: `akos/hlk_canonical_articulation.py` `L3_FK_BINDINGS` (22 tuples)
- Master roadmap L3 lane: [`master-roadmap.md`](../master-roadmap.md) § Round-2 L3
