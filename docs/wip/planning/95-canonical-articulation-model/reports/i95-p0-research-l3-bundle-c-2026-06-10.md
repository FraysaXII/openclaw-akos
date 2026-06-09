---
parent_initiative: INIT-OPENCLAW_AKOS-95
authored: 2026-06-10
audience: J-OP
lane: L3-Bundle-C
ratifying_decisions:
  - D-IH-95-B
linked_canonicals:
  - CANONICAL_RELATIONSHIP_REGISTRY.csv
  - l3-trp-030-036-ratification-2026-06-09.md
---

# P0 research — I95 L3 Bundle C (TRP-030 / TRP-036)

Planner-quality evidence packet before Bundle C disposition.

## Internal evidence sweep

| Source | Trust | Finding |
|:---|:---|:---|
| [`CANONICAL_RELATIONSHIP_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/CANONICAL_RELATIONSHIP_REGISTRY.csv) L31/L37 | SSOT | TRP-030 `current_fk=new`, `status=planned`; TRP-036 paths cite `process_list` layers only — **not initiative-scoped** |
| [`AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv) header | SSOT | Columns: `matrix_id`, `capability_id`, `aic_id`, … — **no `process_id` / `process_item_id`** (2 data rows) |
| [`INITIATIVE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) header | SSOT | `program_anchors` present; **no `workstream_anchors` or workstream FK column** |
| [`akos/hlk_canonical_articulation.py`](../../../../akos/hlk_canonical_articulation.py) | SSOT | `L3_FK_BINDINGS` = 44 tuples (tranches 1–5); **no TRP-030/036 tuples** |
| [`scripts/validate_fk_verb_coverage.py`](../../../../scripts/validate_fk_verb_coverage.py) `_FK_REGISTRY_COLUMNS` | Validator | `aic_capability_implementation_matrix`: `matrix_id`, `capability_id`, `aic_id` only; `initiative_registry`: `initiative_id`, `program_anchors`, `status` |
| **TRP-038** (active) | Related triple | AIC→capability via same matrix — covers REALIZES, not assignment→process |
| **TRP-031** (active) | Related triple | program→workstream via `process_list` — different source entity than initiative |
| [`l3-trp-030-036-ratification-2026-06-09.md`](l3-trp-030-036-ratification-2026-06-09.md) | High | Prior sweep identical conclusion; agent inline default = keep planned |
| [`i95-l3-parallel-bundles-charter-2026-06-09.md`](i95-l3-parallel-bundles-charter-2026-06-09.md) §Bundle C | Charter | Both triples need new CSV columns before promotion |

## FK column discovery (2026-06-10 re-check)

| Triple | Target CSV | Required FK column | Present? |
|:---|:---|:---|:---:|
| TRP-030 | `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` | `process_item_id` (or successor) | **No** |
| TRP-036 | `INITIATIVE_REGISTRY.csv` | `workstream_anchors` (or successor) | **No** |

**Conclusion:** Bundle C cannot ship bindings this session. Disposition = **charter-only** (keep `planned`).

## Novelty test (applied-research RULE 2)

**Refinement** of ratified R2-05 Semantic Council + FK-evidence bar (D-IH-95-B, D-IH-95-D). No novel framing. External research sweep **not required**.

## Semantic Council disposition pattern

Per [`master-roadmap.md`](../master-roadmap.md) P3 + L4 lane: triples without FK surfaces stay **planned** until area-federated authorship mints the join surface. Bundle C documents the blocker; L4 orphan burn-down is the next Semantic Council slice for tracker mint (forward-charter).

## Inline-ratify options (pre-digested — evidence packet)

### TRP-030 — AIC assignment → process

| Option | Action | When to pick |
|:---|:---|:---|
| **A — Keep planned (recommended)** | No registry/bindings change; forward-charter join surface | FK evidence absent (current state) |
| **B — Mint `process_item_id` on matrix** | Canonical-CSV gate + populate + re-ratify | Operator approves AIC↔process direct FK |
| **C — Dedicated AIC↔process register** | New dimension CSV + mirror | Operator prefers separate register over matrix extension |

### TRP-036 — initiative composition → workstream

| Option | Action | When to pick |
|:---|:---|:---|
| **A — Keep planned (recommended)** | Charter-only; no dishonest promotion via program-layer TRP-031 | FK evidence absent (current state) |
| **B — Mint `workstream_anchors` on INITIATIVE_REGISTRY** | Canonical-CSV gate + populate + bindings | Operator approves initiative-scoped workstream FK |
| **C — Charter join table** | New register linking `initiative_id` → `process_list.item_id` | Operator prefers join table over registry column |

## Execution plan (this tranche)

1. Mint disposition report — no `CANONICAL_RELATIONSHIP_REGISTRY.csv` or `L3_FK_BINDINGS` edits.
2. Update cluster map + PMO sweep (rank 3 DONE).
3. Validators unchanged — expect 44 bindings PASS.

## Verification commands

```powershell
py scripts/validate_fk_verb_coverage.py
py scripts/validate_canonical_articulation.py
py scripts/verify.py pre_commit_fast
```
