---
initiative_id: INIT-OPENCLAW_AKOS-94
phase: P1
intellectual_kind: proving_evidence
authored: 2026-06-05
status: active
language: en
---

# I94 P1 — v2 scorer proving + calibration evidence (Finance/Data)

> Operator workplan: *"Option B [full kit] then prove it on Finance/Data, then do a regression
> over the SOP/Skill/rule/templates, how they worked, what did not work as intended and revisit
> this topic to enhance it."* This report covers the **prove + first-regression** step on the
> code core (SSOT + scorer). The SOP/skill/rule/templates wrap is the next P1 increment.

## 1. v2 matrix (8 areas × 16 components × L0–L5; `py scripts/validate_area_completeness.py --matrix`)

| area | kind | score | crit@L3 | tier |
|:---|:---|---:|:---:|:---|
| **Data** | platform | 90% | **10/10** | **COMPLETE** |
| **Finance** | stream_aligned | 91% | **10/10** | **COMPLETE** |
| Marketing | stream_aligned | 77% | 10/10 | COMPLETE* |
| Operations | delivery_capacity | 70% | 9/10 | INCOMPLETE |
| Tech | platform | 67% | 8/10 | INCOMPLETE |
| People | capability_meta | 73% | 8/10 | INCOMPLETE |
| Research | stream_aligned | 67% | 7/10 | INCOMPLETE |
| Legal | stream_aligned | 53% | 6/10 | INCOMPLETE |

The **`crit@L3` tier** (all critical components at "governed") is the real closure gate; the
`%` is now a secondary maturity badge.

## 2. Closure preserved (the key proof)

**Data (90%) and Finance (91%) are COMPLETE for tier** — all 10 critical components at L3+.
v2 did **not** break the I93/Finance closures (D-IH-94-A promise held). Both gained the maturity
badge + the AREA-15 placement-integrity check.

\*Marketing reaches critical-tier too — a finding: its remaining gaps (README, rule+skill) are
**enhancing**, not critical. Whether Marketing is "done" is now an explicit operator call, not a
% artifact.

## 3. Findings surfaced (the model earning its keep)

- **People crit@L3 = 8/10** — AREA-15 fires **gap** because People hosts the 4 drifted
  disciplines (MKTOPS/TECHOPS/DATAOPS/UX → their areas). The scorer *sees the drift the operator
  named.*
- **Legal 6/10** — newly scored (BUG-1 fix); surfaces the real LegalOps build (charter,
  discipline, dimensions, README all gap). Matches the operator's "I don't know how to articulate
  Legal."
- **Research / Tech 7–8/10** — charter + discipline + placement gaps, as expected.

## 4. Calibration findings (the first regression — what did NOT work as intended)

| # | What broke | Root cause | Fix |
|:--|:---|:---|:---|
| CAL-1 | Data/Finance dropped below closure (87/88%, INCOMPLETE) | **AREA-09 paired-SOP+runbook** was made *critical-must-pass-L3*, but it is `partial` for **every** area (the pairing cliff = forward debt; never `pass` in v1) | **Reclassified AREA-09 → enhancing** (weighted badge + tracked, not a closure gate). Doctrine note added in SSOT. |
| CAL-2 | AREA-15 stuck at L2 for all areas (no contract detected) | `DATA_CONTRACT_PATH` mis-resolved (pointed under People/Compliance) **and** contract search used the bare area name (missed `DC-HOL-FINOPS-*`) | Fixed the path + added **area-name aliases** (Finance↔finops, Data↔dc-hol, etc.) |

Both are **calibration, not design errors** — exactly the signal the "prove then regress" step
exists to catch. Post-fix, Data/Finance return to COMPLETE.

## 5. Activation evidence (humans + AICs)

The **action-emitting worklist** (`--area <X> --next`) is the activation lever — the tool emits
the do-this-next list, not just a diagnosis. Example (`--area Finance --next`):

| component | crit | now → tgt | owner | next_action |
|:---|:---|:---|:---|:---|
| AREA-15-PLACEMENT-INTEGRITY | CRIT | L2 → L3 | CFO | (resolved post CAL-2 fix) |
| AREA-16-FILE-PLAN | enh | L1 → L2 | CFO | Rename orphan sub-folder `Governance` to a role name |

## 6. What worked / what's next (regression on the code kit so far)

- **Worked:** deterministic scoring preserved; 16×8 grid runs in ~2s; `crit@L3` tier is a clean
  closure gate; worklist is genuinely actionable; 15/15 tests pass; `validate_hlk` OVERALL PASS.
- **Next P1 increment (the kit wrap):** SOP v2 (AC-HUMAN + AC-AUTOMATION) + `area-governance-craft`
  skill v2 + `akos-area-governance.mdc` rule v2 + templates (charter/README/sub-folder scaffold) +
  one golden-path area taken to fully-COMPLETE. Then regress the wrap (operator's step 3) + revisit.

## 7. Cross-references

- SSOT: [`akos/hlk_area_completeness.py`](../../../../akos/hlk_area_completeness.py) (v2)
- Scorer: [`scripts/validate_area_completeness.py`](../../../../scripts/validate_area_completeness.py) (v2)
- Doctrine: [`AREA_GOVERNANCE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md) v2
- Tests: [`tests/test_validate_area_completeness.py`](../../../../tests/test_validate_area_completeness.py) (15 pass)
