# I95 L3 FK→verb tranche-3 — per-TRP inline ratification (workstream layers)

**Date:** 2026-06-08  
**Lane:** L3-3 (R2-05)  
**Verdict:** PASS (partial tranche — 2 promoted, 2 deferred)  
**Operator posture:** Per-triple inline-ratify (option D); mirror-before-merge gate (operator verifies sync)

## Per-TRP ratification table

| Triple | Relationship (plain language) | Evidence summary | Ratification | `current_fk` after |
|:---|:---|:---|:---|:---|
| **TRP-030** | AI collaborator performs a process | `AIC_CAPABILITY_IMPLEMENTATION_MATRIX.csv` has only `capability_id` + `aic_id` (2 rows). No `process_id` column. **TRP-038** already active: same matrix links AIC→capability (`REALIZES`). Indirect path AIC→capability→process exists via TRP-006 but is not a direct FK for assignment. | **Keep planned** | `new` |
| **TRP-031** | Program composed of workstreams | `process_list.csv`: 72 `workstream` rows; **100%** have `item_parent_1_id` populated. 3 program-pattern rows (`hlk_prog_*`) per PRECEDENCE §program layer. `current_fk` paths set in tranche-1. | **Promote → active** | `process_list.item_granularity;process_list.item_parent_1_id` |
| **TRP-032** | Workstream composed of processes | `process_list.csv`: 303 `process` rows; **100%** have `item_parent_1_id` pointing at workstream parents (e.g. `env_tech_ws_madeira_quality` → MADEIRA child processes). | **Promote → active** | `process_list.item_granularity;process_list.item_parent_1_id` |
| **TRP-036** | Initiative composed of workstreams | Registry notes say *charter FK forward-charter*. `INITIATIVE_REGISTRY.csv` has `program_anchors` but **no** workstream FK column to `process_list`. Initiative→workstream link is narrative, not a populated CSV FK. | **Keep planned** | `process_list.item_granularity;process_list.item_parent_1_id` (paths documented; status stays planned) |

### TRP-030 vs TRP-038 (related triple)

| Triple | Verb | Target | Matrix role |
|:---|:---|:---|:---|
| TRP-038 (active) | realization | capability | `aic_capability_implementation_matrix` — SSOT for which AIC implements which capability |
| TRP-030 (planned) | assignment | process | Would need a new FK surface (e.g. `process_item_id` on matrix or a dedicated AIC↔process register) — not in scope without canonical-CSV operator gate |

## Deliverables (this commit)

| Artifact | Change |
|:---|:---|
| `akos/hlk_canonical_articulation.py` `L3_TRANCHE3_FK_BINDINGS` | 4 bindings (TRP-031 + TRP-032 × `item_granularity` + `item_parent_1_id`) |
| `L3_FK_BINDINGS` | 18 → **22** total |
| `CANONICAL_RELATIONSHIP_REGISTRY.csv` | TRP-031/032 `planned` → `active` |
| `scripts/validate_fk_verb_coverage.py` | Tranche-3 docstring + self-test floor 22 |

## L3 tranche-3 bindings (4)

| CSV column | Triple | Verb semantics |
|:---|:---|:---|
| `process_list.item_granularity` | TRP-031 | disambiguates program-layer workstream rows |
| `process_list.item_parent_1_id` | TRP-031 | program → child workstream parent FK |
| `process_list.item_granularity` | TRP-032 | disambiguates process-under-workstream rows |
| `process_list.item_parent_1_id` | TRP-032 | workstream → child process parent FK |

## Verification matrix

```powershell
py scripts/validate_fk_verb_coverage.py
py scripts/validate_hlk.py
py scripts/verify.py pre_commit_fast --dry-run
```

## Mirror-before-merge checklist (operator gate)

Before closing L3-3 phase on a machine with Supabase credentials:

1. **Emit** — `py scripts/verify.py compliance_mirror_emit` (or scoped profile) after CSV changes land.
2. **Apply** — `pwsh -File scripts/apply_mirror_batches.ps1` (or manual `supabase db query --linked -f` per batch).
3. **Verify** — `compliance_mirror_drift_probe` / DATA-02 row-count parity for `canonical_relationship_registry_mirror` (if mirrored).
4. **Record** — Note apply date + batch SHA in initiative decision log or next pause record.

*This executor run did not apply live Supabase DML (no creds assumed). Git-canonical SSOT is authoritative; mirror is operator-verified per locked gate.*

## Deferred to L3-4+

- **TRP-030** — mint `process_item_id` (or successor FK) on AIC↔process join surface; re-ratify with matrix/process_list evidence.
- **TRP-036** — mint `INITIATIVE_REGISTRY` workstream anchor column (or charter FK) before promotion.
