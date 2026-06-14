---
report_type: closure-uat
intellectual_kind: closure_uat
parent_initiative: INIT-OPENCLAW_AKOS-96
phase: P0
sharing_label: internal_only
authored: 2026-06-11
authored_by: PMO
last_review: 2026-06-11
audience: J-OP
language: en
status: review
verdict: PASS-WITH-FOLLOWUP
closure_decision_source: agent_inline_default
verdict_followup_rationale:
  followup_class: deferred-work-with-tracker
  closure_target: Browser + Impeccable experiential UAT for Track D (Research Center)
  owner: System Owner + operator
  tracker_path: docs/wip/planning/96-research-data-plane-and-research-center/reports/uat-i96-research-center-browser-2026-06-11.md
  notes: >-
    P0 structural/mechanical gates PASS. Track D browser UAT **PASS-WITH-FOLLOWUP** (2026-06-12; `d6bcab24`) —
    dev-password experiential walk + manifest + Impeccable KiRBe relabel disposition complete; open follow-ups:
    magic-link allow-list, axe on Python 3.12, KiRBe env, page-spec sync — see
    [`uat-i96-research-center-browser-2026-06-11.md`](uat-i96-research-center-browser-2026-06-11.md) §10.
ratifying_decisions:
  - D-IH-96-A
  - D-IH-96-E
linked_canonicals:
  - INITIATIVE_REGISTRY.csv
  - DECISION_REGISTER.csv
  - INITIATIVE_DEPENDENCIES.md
linked_runbooks:
  - scripts/validate_hlk.py
  - scripts/validate_research_action.py
  - scripts/validate_index_freshness.py
  - scripts/baseline_index_sweep.py
---

# UAT — I96 P0 program mint (2026-06-11)

## Section 1 — Closure summary (TL;DR)

> I96 (Research Data Plane + Research Center program) is minted as an **active program_line**
> under I86. Registry, dependency graph, planning README, and cluster-map wiring are in place.
> Track A ledger closed at **949/950** rows. HLK-ERP Research Center v1 four-panel page ships
> read-only. **Initiative stays ACTIVE** — P0 program mint only (`D-IH-96-E`).

| Dimension | Target | Actual | Status |
|:---|:---|:---|:---:|
| **Verdict** | PASS-WITH-FOLLOWUP | PASS-WITH-FOLLOWUP | ⏳ |
| **Closure-criteria met** | 6/6 P0 mechanical | 6/6 mechanical | ✓ |
| **Mechanical gates green** | 4/4 | 4/4 | ✓ |
| **Browser UAT evidence** | **required** (sibling-repo UI) | **PWF** — walk complete; follow-ups open (see browser UAT) | ⏳ |
| **Risks closed** | 0 P0-critical | 0 open P0 | ✓ |
| **Operator sign-off** | optional P0 | pending | ⏳ |
| **Outstanding items** | tracks B-D open | 3 tracks open | ⏳ |

**Closure decision:** n/a at P0 — full closure deferred to P12 (`D-IH-96-E`). Reversibility: **low**.

## Section 2 — Closure-criteria verification

| # | Closure criterion | Verification | Expected | Actual | Status |
|:---|:---|:---|:---|:---|:---:|
| 1 | INITIATIVE_REGISTRY row | `grep INIT-OPENCLAW_AKOS-96` | 1 row active | 1 row | PASS |
| 2 | Decision register FK | `grep D-IH-96-A DECISION_REGISTER.csv` | ≥1 row | 2 rows (A+E) | PASS |
| 3 | INITIATIVE_DEPENDENCIES I96 node | file read §I96 | node + 6 edges | present | PASS |
| 4 | Planning README row 96 | grep `**96**` README | 1 row | 1 row | PASS |
| 5 | Candidate promoted | candidate frontmatter | promoted_active | promoted_active | PASS |
| 6 | Automation OS ledger | `validate_research_action.py` | PASS | PASS 949 rows | PASS |

## Section 3 — Mechanical evidence

### 3.1 Validator runs

```text
py scripts/validate_hlk.py
  OVERALL: PASS

py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv
  PASS: 949 rows; Euclid 550 / Safe 399

py scripts/validate_index_freshness.py
  total=8 fresh=7 drift=0 gap=0 blocked=0 skip=1

py scripts/baseline_index_sweep.py
  total=8 fresh=7 drift=0 gap=0 blocked=0 skip=1
```

### 3.4 Browser-evidence pattern

**Track D — PASS-WITH-FOLLOWUP (2026-06-12; `d6bcab24`).** Sibling-repo UI (HLK-ERP `/research-center`) experiential bar cleared on dev-password path — panels, multi-viewport manifest, Impeccable KiRBe relabel disposition. Open follow-ups: magic-link allow-list, axe on Python 3.12, KiRBe env, page-spec sync — [`uat-i96-research-center-browser-2026-06-11.md`](uat-i96-research-center-browser-2026-06-11.md) §10. Localhost workflow: `http://localhost:3010/sign-in?next=%2Fresearch-center`.

## Section 4 — Per-dimension findings

| # | Dimension | Expected | Actual | Class | Severity |
|:---|:---|:---|:---|:---|:---:|
| 1 | Registry wiring | INIT row + decisions | minted | aligned | n/a |
| 2 | Three-plane specs | P1–P3 artifacts | minted | aligned | n/a |
| 3 | Track A ledger | ~950 rows | 949 rows | neutral | low |
| 4 | ERP Research Center | four panels read-only | shipped hlk-erp | aligned | n/a |
| 5 | Holistic lane | R4–R12 | blocked D4 | neutral | medium |

## Section 5 — D-IH-86-D mechanical cross-check

| Signal | Source | Result |
|:---|:---|:---:|
| `validate_hlk.py` OVERALL PASS | 2026-06-11 run | ✓ |
| I86 `files-modified.csv` session backfill | 23 rows appended | ✓ |
| UAT report present | this file | ✓ |
| Initiative stays active (not sibling closure) | D-IH-96-E | ✓ |

## Section 6 — SOP + runbook pairs

N/A at P0 — no new SOP+runbook pair minted. Existing research-action runbooks exercised:

| Surface | Path | Status |
|:---|:---|:---:|
| Research action validator | `scripts/validate_research_action.py` | active |
| HLK umbrella validator | `scripts/validate_hlk.py` | active |
| Index freshness sweep | `scripts/validate_index_freshness.py` | active |

## Section 7 — Risk-register closure

| Risk ID | Summary | Status | Note |
|:---|:---|:---:|:---|
| R-IH-96-1 | Ledger drift | MITIGATED | validator PASS at 949 |
| R-IH-96-3 | KiRBe ingest scope creep | OPEN | contract draft only |
| R-IH-96-7 | D4 synthesis delay | OPEN | blocks holistic R4–R12 |

## Section 8 — Decision close-outs

- **D-IH-96-A** — RATIFIED 2026-06-11; registry + planning folder minted.
- **D-IH-96-E** — RATIFIED; program_line status until P12.
- **D-IH-96-B..D** — Proposed; gates at P6/P10.

## Section 9 — Closure registry edits

**Applied 2026-06-11** (P0 program mint — initiative **stays active**).

- **INITIATIVE_REGISTRY**: `INIT-OPENCLAW_AKOS-96` — `status` `active`; `inception_decision_id` **D-IH-96-A**; program anchors `PRJ-HOL-DAT-2026;PRJ-HOL-PGF-2026`.
- **DECISION_REGISTER**: **D-IH-96-A**, **D-IH-96-E** appended.
- **INITIATIVE_DEPENDENCIES**: I96 section + edges to I86, I75, I83, I88, I92, I95.
- **planning README** §96 row added.
- **Candidate**: `i-nn-research-data-management-and-feed-delivery.md` → `promoted_active`.

## Section 10 — Verdict

**Verdict:** **PASS-WITH-FOLLOWUP** — P0 mechanical mint complete; Track D browser UAT **PWF** (experiential walk done; env/auth follow-ups open).

1. ✓ **P0 closure-criteria** — §2 shows 6/6 PASS.
2. ✓ **Mechanical evidence reproducible** — §3 commands re-run yield same outputs.
3. **Browser UAT** — **required** for Track D; **PWF** — walk + manifest + Impeccable disposition on file; follow-ups in [`uat-i96-research-center-browser-2026-06-11.md`](uat-i96-research-center-browser-2026-06-11.md) §10.
4. ✓ **D-IH-86-D cross-check** — §5 satisfied for program mint scope.
5. N/A **SOP+runbook pair** — none minted at P0.
6. ✓ **Risk + decision audit** — §7–§8; no P0-critical open risks.
7. ⏳ **Operator sign-off** — optional at P0; full P12 closure is separate gate.

## Section 11 — Cross-references

- Master roadmap: [`master-roadmap.md`](../master-roadmap.md)
- Decision log: [`decision-log.md`](../decision-log.md)
- Evidence matrix: [`evidence-matrix.md`](../evidence-matrix.md)
- Files modified: [`files-modified.csv`](../files-modified.csv)
- Page spec: [`research-center-page-spec-2026-06-11.md`](research-center-page-spec-2026-06-11.md)
- Cluster map: [`i96-initiative-cluster-map.md`](../i96-initiative-cluster-map.md)
- I95 cluster map (I96 columns): [`../../95-canonical-articulation-model/i95-initiative-cluster-map.md`](../../95-canonical-articulation-model/i95-initiative-cluster-map.md)
- Template: [`docs/wip/planning/_templates/uat-closure-template.md`](../../_templates/uat-closure-template.md)
