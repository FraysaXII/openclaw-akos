---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
phase: P4-P6-execution-spec
intellectual_kind: execution_spec
operator_ratification:
  q2: sequential_P4_P5_P6_after_Research
---

# I94 Operations P4–P6 execution spec (2026-06-10)

Mechanical execution packet for Composer seat — **queued after Research Session 1**.
Upstream: [`i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md`](i94-operations-operational-sweep-thinking-synthesis-2026-06-10.md).

## Phase P4 — Cross-area handoffs mint

### Scope

Mint `OPERATIONS_CROSS_AREA_HANDOFFS.md` as a **register-only** canonical under
`Admin/O5-1/Operations/canonicals/`. Documents execution contracts to Data, People,
Finance, Tech, and Research — no file moves.

### Files

| Action | Path |
|:---|:---|
| create | `docs/references/hlk/v3.0/Admin/O5-1/Operations/canonicals/OPERATIONS_CROSS_AREA_HANDOFFS.md` |
| modify | `docs/references/hlk/v3.0/Admin/O5-1/Operations/README.md` (index link) |
| modify | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md` (one row) |
| modify | `docs/wip/planning/94-area-architecture-and-completeness-v2/files-modified.csv` |

### Verification

```powershell
py scripts/validate_hlk.py
py scripts/validate_hlk_vault_links.py
```

### Pause-point

`gate_type: ratified-at-planning` — no new `process_list` rows.

---

## Phase P5 — I88 Operations 10-pillar wiring report

### Scope

Deep slice for Operations in the I88 cross-area Ops wiring initiative. Updates §1.4
Operations paragraph to reflect IntelligenceOps eviction + Research ownership.

### Files

| Action | Path |
|:---|:---|
| create | `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/reports/i94-operations-10-pillar-wiring-2026-06-10.md` |
| modify | `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/master-roadmap.md` §1.4 |
| modify | `docs/wip/planning/88-cross-area-ops-wiring-review-discipline/files-modified.csv` |

### Content bar (10 pillars)

Each pillar row: wiring density (Tier 1/2/3), most-active cross-area touchpoint,
evidence path, cadence (`on_demand` / `scheduled` / `event_triggered`).

### Verification

```powershell
py scripts/validate_area_completeness.py --area Operations --matrix
```

---

## Phase P6 — Operations sweep closure UAT

### Scope

11-section closure UAT per `uat-closure-template.md` for the I94 Operations
operational sweep (P0–P5). Verdict target: PASS or PASS-WITH-FOLLOWUP with tracker.

### Files

| Action | Path |
|:---|:---|
| create | `docs/wip/planning/94-area-architecture-and-completeness-v2/reports/uat-i94-operations-sweep-closure-2026-06-10.md` |
| modify | `docs/wip/planning/94-area-architecture-and-completeness-v2/master-roadmap.md` (P6 status) |

### Verification matrix (full)

```powershell
py scripts/validate_area_completeness.py --area Operations --matrix
py scripts/validate_area_completeness.py --area Operations --next
py scripts/validate_hlk.py
py scripts/verify.py pre_commit_fast
py scripts/validate_uat_report.py --report docs/wip/planning/94-area-architecture-and-completeness-v2/reports/uat-i94-operations-sweep-closure-2026-06-10.md
```

### Operator sign-off

§10 seven-item checklist — required before INITIATIVE_REGISTRY flip (not in Session 1).

---

## Commit discipline

| Commit | Message shape |
|:---|:---|
| P4 | `docs(i94): P4 Operations cross-area handoffs canonical` |
| P5 | `docs(i88/i94): P5 Operations 10-pillar wiring report` |
| P6 | `docs(i94): P6 Operations sweep closure UAT` |

One phase per commit per `akos-baseline-governance.mdc`.

## Cross-references

- Handoffs narrative: [`i94-p0-research-p4-p6-handoffs-2026-06-10.md`](i94-p0-research-p4-p6-handoffs-2026-06-10.md)
- I94 master-roadmap: [`../master-roadmap.md`](../master-roadmap.md)
