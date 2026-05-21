---
intellectual_kind: kb_integrity_audit
parent_initiative: INIT-OPENCLAW_AKOS-81
parent_phase: P1
sharing_label: internal_only
authored: 2026-05-21
last_review: 2026-05-21
linked_decisions:
  - D-IH-81-F  # integrity matrix methodology + PASS threshold (ratified at this phase close)
  - D-IH-81-K  # I81 P1 phase ratification (this commit)
  - D-IH-86-T  # I86 cluster burndown plan (parent context)
status: active
role_owner: PMO
co_owner_role: System Owner
language: en
---

# I81 P1 — KB integrity baseline audit (2026-05-21)

> Wave H lane-2 (subagent stream) of the [I86 cluster burndown plan](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md). Authored 2026-05-19 in parallel with parent agent's foreground I76 P2 work. Paired with [`kb-integrity-matrix-2026-05-21.csv`](kb-integrity-matrix-2026-05-21.csv); see `akos/hlk_kb_integrity.py` for the row + summary schemas.

## §1 Baseline snapshot

| Metric | Value |
|:---|---:|
| Executable rows scanned | **1092** |
| PASS verdict | **0** (0.0%) |
| PARTIAL verdict | 1092 (100.0%) |
| FAIL verdict | 0 |
| Pass rate | **0.00%** |
| Pass threshold (D-IH-81-F) | 95% |
| Meets threshold? | NO |

## §2 Per-signal coverage

| Signal | Matched / Declared | Total | Coverage |
|:---|---:|---:|---:|
| `knowledge_pairing_status` | 0 | 1092 | 0.00% |
| `paired_sop_status` | 92 | 1092 | 8.42% |
| `mirror_coverage_status` | 1092 | 1092 | 100.00% |
| `audience_tags_status` | 0 | 1092 | 0.00% (P1 baseline: deferred for all) |
| `cadence_status` | 34 | 1092 | 3.11% |

## §3 Per-area distribution

| Area | Total | PASS | PARTIAL | FAIL |
|:---|---:|---:|---:|---:|
| Data | 10 | 0 | 10 | 0 |
| Finance | 16 | 0 | 16 | 0 |
| Legal | 11 | 0 | 11 | 0 |
| MKT | 115 | 0 | 115 | 0 |
| Marketing | 1 | 0 | 1 | 0 |
| Operations | 404 | 0 | 404 | 0 |
| People | 84 | 0 | 84 | 0 |
| Research | 80 | 0 | 80 | 0 |
| Tech | 371 | 0 | 371 | 0 |

## §4 Top 5 gap signals (most-frequent shortfalls)

- `knowledge_pairing(1092)`
- `audience_tags_deferred(1092)`
- `cadence_undeclared(1058)`
- `paired_sop(1000)`

## §5 Reading guide + caveats (P1 baseline)

The P1 baseline pass-rate is **0.00%** — well below the 95% threshold. This is **expected** and not a regression: the `audience_tags_status` signal is `deferred` for every row at P1, pulling 100% of rows below `pass` on that signal alone. The metric becomes meaningful once two follow-ups land:

1. **I85 audience-tag wire** (I81 P1 follow-up commit): join `audience_tags_status` from `AUDIENCE_REGISTRY.csv` via role_owner → audience tag mapping. When this lands, audience_tags_deferred → audience_tags_matched for every row whose role_owner has a registered audience tag.
2. **I81 P4-P8 SOP body/addendum retrofit waves**: lift `paired_sop_status` from baseline (currently `8.42%` matched) toward 70-90% as each area's SOPs land per `pattern_sop_addendum_split`.

The P1 baseline records the **starting point**; P4-P8 record progress against it. P9 closure UAT re-runs this audit and verifies pass_rate ≥ 95%.

## §6 Next actions (routing)

- **KNOWLEDGE_PAIRING gaps**: 1092 executable rows have no pairing registry entry. Top per-area gaps shipped in the matrix CSV; PMO + per-area role_owner can mint missing pairs as the SOP retrofits land in P4-P8.
- **Paired-SOP gaps**: 1000 executable rows have no detectable v3.0 SOP reference. Per-area retrofit waves (P4 RevOps, P5 Marketing, P6 Tech, P7 Research/Compliance/Ethics, P8 Operations remainder) close these in scoped tranches.
- **Cadence gaps**: 1058 executable rows have no `cadence_type` declared per `akos-executable-process-catalog.mdc` RULE 3. The cadence taxonomy is fully expressible; missing rows are operator-side backfill.
- **Audience-tag deferred**: ALL rows. Forward-charter to I81 P1 follow-up wire commit.

## §7 Cross-references

- [I81 master-roadmap](../master-roadmap.md) — P1 phase shape per §3.
- [`kb-integrity-matrix-2026-05-21.csv`](kb-integrity-matrix-2026-05-21.csv) — row-level data.
- [`akos/hlk_kb_integrity.py`](../../../../akos/hlk_kb_integrity.py) — Pydantic chassis (row + summary models).
- [`scripts/audit_kb_integrity.py`](../../../../scripts/audit_kb_integrity.py) — paired runbook per `akos-executable-process-catalog.mdc` RULE 1.
- [I86 cluster burndown plan §6 Wave H](../../86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md) — parent wave context.
- [`process_list.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/process_list.csv) — executable-row source-of-truth.
- [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) — pairing source-of-truth.
- D-IH-81-F (ratified at this phase close per the methodology + threshold values used above).
- D-IH-81-K (I81 P1 phase ratification — this commit).

## §8 Notes

P1 baseline snapshot per D-IH-81-F. audience_tags_status is deferred for every row pending I85 P1 wire (audience_tags_coverage column join). pass_rate at baseline is expected to be near-zero because of the audience_tags_deferred floor; the metric becomes meaningful once that wire lands.
