---
initiative_id: INIT-OPENCLAW_AKOS-94
phase: P1
intellectual_kind: wrap_regression
authored: 2026-06-05
status: active
language: en
---

# I94 P1 — activation-kit wrap: golden-path + regression (operator step 3)

> Operator workplan step 3: *"do a regression over the SOP/Skill/rule/templates, how they
> worked, what did not work as intended and revisit this topic to enhance it."* This report
> covers the **kit wrap** (SOP v2 + skill v2 + rule v2 + templates) + the **golden-path** + the
> **regression** of how the wrap performed.

## 1. The kit wrap (what shipped)

| Artifact | v2 change | Activation role |
|:---|:---|:---|
| `SOP-PEOPLE_AREA_GOVERNANCE_001.md` | 16-component grid + `--next` worklist steps + AC-HUMAN/AC-AUTOMATION rewrite | the human runbook |
| `area-governance-craft/SKILL.md` | worklist-over-matrix; critical-vs-enhancing; kind/entity; placement; file-plan | the AIC HOW |
| `akos-area-governance.mdc` | v2 model summary + RULE 1 worklist + RULE 3 kind/entity/file-plan/placement | the WHEN |
| `_templates/AREA_CHARTER_TEMPLATE.md` | NEW — fill-in for AREA-02 at L3 | "raise to L3 = fill template" |
| `_templates/AREA_README_TEMPLATE.md` | NEW — fill-in for AREA-13 at L3 | same |

## 2. Golden path — Finance + Data as the copy-me reference

Both are **COMPLETE for tier** (all 10 critical components at L3+). Their `--area <X> --next`
worklists are now **one enhancing item each** — the proof that the activation loop converges:

```
Finance --next  (items=1)
| Finance | AREA-16-FILE-PLAN | enh | L1 -> L2 | CFO | Rename orphan sub-folders to role names: ['Governance'] |

Data --next  (items=1)
| Data | AREA-16-FILE-PLAN | enh | L1 -> L2 | CDO | Rename orphan sub-folders: ['Architecture','Governance','Science'] |
```

Contrast People (the drift the model exists to catch) — the worklist **names the fix**:

```
People --next  (items=3)
| People | AREA-15-PLACEMENT-INTEGRITY | CRIT | L0 -> L3 | CPO | git mv the 4 drifted *_DISCIPLINE.md out of People to their area |
| People | AREA-13-AREA-README       | enh  | L0 -> L2 | CPO | Add README.md at area root |
| People | AREA-16-FILE-PLAN          | enh  | L1 -> L2 | CPO | Rename orphan sub-folders: ['Legal','Talent'] |
```

**Activation verdict:** a human or AIC runs `--area <X> --next` and executes top-down. The tool
emits the worklist (incl. the literal `git mv` for drift). AC-HUMAN + AC-AUTOMATION both met.

## 3. Regression — what worked / what did NOT work as intended

| # | Signal | Verdict | Disposition |
|:--|:---|:---|:---|
| W-1 | `--next` worklist emits owner + exact next action | **worked** — this is the activation lever; converges Finance/Data to 1 item | keep |
| W-2 | critical-vs-enhancing split keeps closures (Data/Finance COMPLETE) | **worked** | keep |
| W-3 | AREA-15 names the drifted files + the `git mv` (People) | **worked** — the placement check earns its keep | keep |
| W-4 | **AREA-16 over-flags `Governance`/`Architecture`/`Science`** as orphans | **did NOT work as intended** — these are legitimate *functional sub-areas* (Data Architect, Data Governance Lead are the roles; folders use the short functional form), and Data/Finance roles carry **empty `sub_area`** so there is nothing to match | **defer-OPS / forward-charter** — AREA-16 matcher needs keyword/substring tolerance OR a functional-sub-area allowlist; it is **enhancing** so it does not block closure (no harm, only noise) |
| W-5 | Templates resolve from the SOP `linked_canonicals` | **worked** | keep |

**Key revisit (W-4):** the "sub-folder = role" doctrine is right for **role-organized** areas
(People: Compliance/Ethics/Learning) but areas organized by **functional sub-area** (Data:
Architecture/Governance; Finance: Business Controller) need the matcher to accept a
`sub_area`/role **keyword** match, not exact equality. Forward-charter to a P7 refinement
(AREA-16 matcher v2) — explicitly **not** over-engineered now since AREA-16 is enhancing.

## 4. P1 status

- **Done:** doctrine v2 + LOGIC_CHANGE_LOG BT-07 + SSOT v2 + scorer v2 (action worklist) + tests
  (15 pass) + SOP v2 + skill v2 + rule v2 + 2 templates + proving on Finance/Data + this wrap
  regression.
- **Forward (P7 refinement):** AREA-16 matcher keyword tolerance (W-4).
- **Next phases:** P2 (improve affected plans) → P3 Operations → P4 People/Compliance + drift
  moves → P5 entity/Envoy (research-first) → P6 Legal (research-first) → P7 subfolder remediation
  → P8 DATA regression → P9 closure.

## 5. Cross-references

- Proving: [`p1-proving-finance-data-2026-06-05.md`](p1-proving-finance-data-2026-06-05.md)
- Doctrine: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) v2
- SOP: [`SOP-PEOPLE_AREA_GOVERNANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SOP-PEOPLE_AREA_GOVERNANCE_001.md) v2
