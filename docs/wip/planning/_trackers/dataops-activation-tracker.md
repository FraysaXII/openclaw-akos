---
status: closed
classification: governance-shape
intellectual_kind: dataops-activation-tracker
authority: System Owner (Tech) + PMO (joint)
artifact_role: durable
ratifying_decisions: [D-IH-86-CR, D-IH-86-BU, D-IH-90-AA]
parent_canonical: docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md
parent_rules:
  - .cursor/rules/akos-executable-process-catalog.mdc
  - .cursor/rules/akos-quality-fabric.mdc
paired_runbook: scripts/dataops_quality_check.py
paired_sop: docs/references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/SOP-TECH_DATAOPS_QUALITY_001.md
linked_ops: [OPS-86-9, OPS-86-19]
closure_decision: D-IH-90-AA
closure_date: 2026-06-04
language: en
audience: J-OP
last_review: 2026-06-04
authored: 2026-05-23
---

# DataOps activation tracker

> **CLOSED 2026-06-04** per D-IH-90-AA (I90 P3c). All five activation criteria met.
> Evidence: [`p3c-dataops-activation-2026-06-04.md`](../90-routing-and-wiring/reports/p3c-dataops-activation-2026-06-04.md).

## Closure record

1. `DATAOPS_DISCIPLINE.md` → `status:active` ✓
2. `SOP-TECH_DATAOPS_QUALITY_001.md` minted ✓
3. `scripts/dataops_quality_check.py` minted ✓
4. `thi_data_*` placeholders accept-as-canon; umbrella `env_tech_dtp_dataops_quality_001` ✓
5. OPS-86-19 closed ✓

---

## Historical context (pre-closure)
> currently-placeholder state of the 8 `process_list.csv` rows under the
> `thi_data_*` DataOps prefix. These rows surface as DIM-05
> SOP-RUNBOOK-PAIRING gap findings in the wave-close regression sweep
> because no paired SOP under `<area>/<role>/canonicals/` and no paired
> runbook under `scripts/` carry token-matching names. Per the
> [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc)
> Rule 1, those pairings are required for every executable process row
> — BUT the DataOps doctrine itself currently sits at
> [`status: active`](../../../references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md)
> per the Wave M D-IH-86-BU engrave-properly OVERRIDE mint. While the
> doctrine remains at charter, the rows under `thi_data_*` are
> doctrine-aware placeholders, not active processes; the pairing rule
> does not apply at the unit level until the parent doctrine activates.
> This tracker:
>
> 1. **Documents** the 8 rows as known, intentional placeholders (drift
>    is NOT silent).
> 2. **Names** the activation gate (when DataOps doctrine flips to
>    `status:active`, the pairing requirement fires for every row).
> 3. **Cross-references** the existing forward-charter (`OPS-86-9` covers
>    the runbook side; `OPS-86-19` minted here covers the full doctrine
>    activation including SOP+runbook+area+role assignments).
> 4. **Surfaces** the contra-precedent ratification mechanism — Wave R
>    Lane B drain accepted these 8 findings as canon per `D-IH-86-CR`
>    rather than minting 8 throwaway SOPs against an unactivated
>    doctrine.

## Why this tracker exists (operator-facing rationale)

The Wave-Q regression sweep (`regression-sweep-2026-05-22.md`) surfaced
**8 DIM-05 SOP-RUNBOOK-PAIRING findings** under `process_list:thi_data_*`:

- `thi_data_prj_1` (DataOps project; placeholder for DataOps program scope)
- `thi_data_ws_1` (DataOps workstream 1)
- `thi_data_ws_2` (DataOps workstream 2)
- `thi_data_dtp_31` (DataOps task)
- `thi_data_dtp_32` (DataOps task)
- `thi_data_dtp_33` (DataOps task)
- `thi_data_dtp_34` (DataOps task)
- `thi_data_dtp_72` (DataOps task)

Each row triggers the heuristic because the row body mentions "data" but no
SOP exists at `<area>/<role>/canonicals/SOP-*data*` and no runbook exists at
`scripts/*data*` matching the row's `item_id` tokens.

The discipline tension surfaced at drain3-clarified (Wave R Lane B drain
2026-05-23):

- **Option A** (Accept-as-canon all 8 under contra-precedent): clean
  shape, but no durable handle for future agents to find the placeholders.
- **Option C** (Forward-charter per row): preserves visibility per row,
  but produces 8 throwaway forward-charter rows when DataOps doctrine
  itself is the single root cause.
- **Option A-plus** (operator-ratified at drain3-clarified): one tracker
  file + one OPS row (`OPS-86-19`) covering DataOps doctrine activation;
  the 8 process rows are accepted-as-canon as placeholders pending
  doctrine flip. This is the durable shape minted here.

## Activation criteria (when this tracker closes)

The tracker closes when ALL of the following are TRUE:

1. `DATAOPS_DISCIPLINE.md` flips from `status:charter` to `status:active`
   (operator ratification at the activating decision row).
2. `SOP-TECH_DATAOPS_QUALITY_001.md` is minted at
   `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/canonicals/`
   per the doctrine's forward_charter row.
3. `scripts/dataops_quality_check.py` (the paired runbook) is minted per
   the canonical's forward_charter + `OPS-86-9` rolllup.
4. Each of the 8 `thi_data_*` `process_list.csv` rows is reviewed and
   either (a) rewritten to point to a real SOP+runbook pair OR (b)
   formally removed from `process_list.csv` if the placeholder turns out
   to be redundant after doctrine activation.
5. The Wave-X regression sweep at the activation commit emits
   `gap_count == 0` for DIM-05 against the `thi_data_*` prefix.

When all 5 conditions are TRUE, append a closure decision row (e.g.
`D-IH-NN-X`) and flip this tracker's frontmatter `status` to `closed`.

## Pre-activation contra-precedent (Wave R Lane B drain, 2026-05-23)

Per [`akos-inter-wave-regression.mdc`](../../../.cursor/rules/akos-inter-wave-regression.mdc)
RULE 2 option 4 (accept-as-canon): the 8 DIM-05 findings are accepted as
intentional drift, ratified by `D-IH-86-CR`. Future regression sweeps
should treat these specific 8 rows as known-placeholder UNTIL this
tracker closes per the activation criteria above.

The 8 affected rows + their accepted-as-canon disposition rationale:

| process_list row | Disposition | Rationale |
|:---|:---|:---|
| `thi_data_prj_1` | accept-as-canon | DataOps program scope placeholder; SOP+runbook deferred until doctrine activates |
| `thi_data_ws_1` | accept-as-canon | DataOps workstream 1 placeholder; same |
| `thi_data_ws_2` | accept-as-canon | DataOps workstream 2 placeholder; same |
| `thi_data_dtp_31` | accept-as-canon | DataOps task placeholder; same |
| `thi_data_dtp_32` | accept-as-canon | DataOps task placeholder; same |
| `thi_data_dtp_33` | accept-as-canon | DataOps task placeholder; same |
| `thi_data_dtp_34` | accept-as-canon | DataOps task placeholder; same |
| `thi_data_dtp_72` | accept-as-canon | DataOps task placeholder; same |

## Optional future regression-sweep heuristic enhancement

A future improvement to `scripts/inter_wave_regression_sweep.py` DIM-05
heuristic: read the parent canonical's `status:` field — if `charter`,
suppress per-row pairing findings AND emit a single placeholder advisory
naming the tracker file. This would close the loop mechanically and
reduce the contra-precedent burden in subsequent waves. Out of scope
for the Wave R Lane B drain; forward-charter via `OPS-86-19` notes.

## Cross-references

- [`DATAOPS_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATAOPS_DISCIPLINE.md) — parent canonical (Data/Governance; re-homed I93 P1).
- [`akos-executable-process-catalog.mdc`](../../../.cursor/rules/akos-executable-process-catalog.mdc) Rule 1 — the pairing rule this tracker contra-precedents against.
- [`akos-quality-fabric.mdc`](../../../.cursor/rules/akos-quality-fabric.mdc) — parent fabric (DataOps is one of the 4 charter specialties from Wave M).
- [`akos-inter-wave-regression.mdc`](../../../.cursor/rules/akos-inter-wave-regression.mdc) RULE 2 — 5-option disposition enum (this tracker = option 4 accept-as-canon at scale).
- `OPS-86-9` (Wave M Cluster B paired-runbook minting for 4 specialty canonicals).
- `OPS-86-19` (this tracker's activation-rollup OPS row).
- `D-IH-86-CR` (Wave R Lane B drain closure umbrella; ratifying decision).
- `D-IH-86-BU` (Wave M engrave-properly OVERRIDE that minted DATAOPS_DISCIPLINE at status:charter).
- `regression-sweep-2026-05-22.md` (originating gap findings).
