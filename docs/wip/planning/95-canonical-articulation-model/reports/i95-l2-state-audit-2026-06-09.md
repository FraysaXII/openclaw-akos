---
report_type: l2-state-audit
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2-capability-de-densify
authored: 2026-06-09
authored_by: Thinking seat (Opus) → execution seat mint
verdict: DONE-with-followups
ratifying_decisions:
  - D-IH-95-H
  - D-IH-95-I
evidence_commit: 2026-06-08
---

# I95 L2 — Capability de-densification state audit (2026-06-09)

**Operator question:** "Didn't we do that already?"  
**Answer:** **Yes.** The capability de-densification lane (Round-2 L2, decision **D-IH-95-I**) landed **2026-06-08** in a single milestone tranche — not just the Data+Finance+Legal pilot.

> **Supersedes** the Lane 2 section in [`i95-round2-lanes-research-synthesis-2026-06-09.md`](i95-round2-lanes-research-synthesis-2026-06-09.md), which still cited **1,119** capability rows. That was true before 2026-06-08; current SSOT is **93** capabilities.

---

## Verdict summary

| Verdict | Meaning |
|:---|:---|
| **DONE** | Foundation schema, full area collapse, evictions, `process_list` cleanup |
| **PENDING** | Hybrid rating cadence, TRP-014, graph bearer edge, prod mirror re-emit, orphan burn-down |

**Recommendation for L2 ratification A ("if not done"):** **Do not re-execute collapse.** Treat L2 as **closure + follow-ups only**.

---

## Work-item matrix

| Work item | Planned (D-IH-95-I synthesis) | Actual state @ repo | Verdict |
|:---|:---|:---|:---:|
| Foundation schema: drop `bearer_class`, add `l1_domain` + `definition` + `capability_tier` | Step 1 before slices | CSV header + [`akos/hlk_capability_registry_csv.py`](../../../../akos/hlk_capability_registry_csv.py) + mirror [`20260608002412_i95_i_capability_registry_mirror_collapse_schema.sql`](../../../../supabase/migrations/20260608002412_i95_i_capability_registry_mirror_collapse_schema.sql) | **DONE** |
| D+F+L pilot 44→11 | Step 2 | **11** Data/Finance/Legal rows in 93-cap registry | **DONE** |
| Remaining area slices (Mkt/Research/People/Ops/Tech) | Steps 3–4 | Full collapse in same wave: **93 caps** (~12:1 from 1,119) per [`decision-log.md`](../decision-log.md) D-IH-95-I + [`CHANGELOG.md`](../../../../CHANGELOG.md) | **DONE** |
| Cross-area reconciliation (~80 target) | Step 4 | Net **93** (slightly above ~80 — acceptable per organic-count ratification) | **DONE** |
| Evictions (tools→substrate, code-symbols→component matrix) | Step 5 | Routed in same tranche per decision log | **DONE** |
| `process_list` radical cleanup | Step 6 (separate gate) | **496** processes + **583** rows in [`BUILDOUT_BACKLOG.csv`](../../../../docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/BUILDOUT_BACKLOG.csv) | **DONE** |
| Hybrid weekly-cron capability rating (~8/wk) | D-IH-95-H | No evidence of activated cadence process beyond `capability_tier` column | **PENDING** |
| TRP-014 (capability composition) promotion | L2 follow-on | Still **planned** in relationship registry | **PENDING** |
| `bearer_class` on **realization edge** (graph, not CSV) | Collapse mechanic | CSV bearer removed; **Neo4j still legacy edges** — no realization-edge bearer migration | **PENDING** (Neo4j lane) |
| Prod mirror re-emit (`process_list` + `buildout_backlog`) | D-IH-95-I obligation | **PENDING-OPERATOR** (same as GOV-5/7 walkthrough) | **PENDING** |
| 8-area articulation orphan burn-down (`--matrix` AMBER→GREEN) | L4 / Council | Still ahead per decision log | **PENDING** |

---

## Evidence anchors

```1:2:docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/CAPABILITY_REGISTRY.csv
capability_id,capability_name,area,role_owner,originating_process_ids,substrate_id,skill_ids,lifecycle_status,i81_verdict,i81_gap_summary,external_register_summary,last_review_at,last_review_by,last_review_decision_id,methodology_version_at_review,notes,capability_tier,l1_domain,definition
CAP-LEGAL-INSTRUMENT-LIFECYCLE,Legal Instrument Lifecycle Management,Legal,Legal Counsel Specialist,thi_legal_dtp_21;thi_legal_dtp_22;thi_legal_dtp_23;thi_legal_dtp_26;thi_legal_dtp_27,,,planned,,,,2026-06-08,Data Governance Office,D-IH-95-I,v3.1,Collapsed from 5 shadows (D-IH-95-I); ...
```

Decision log excerpt (D-IH-95-I execution):

- **CAPABILITY_REGISTRY 1,119 → 93** — capability collapse COMPLETE @ 2026-06-08
- **`process_list` radical cleanup COMPLETE** — 496 processes; BUILDOUT_BACKLOG 583 rows

---

## Verification gates (follow-up audit — no CSV rewrite)

```powershell
py scripts/validate_hlk.py
py scripts/validate_canonical_articulation.py
py scripts/validate_area_completeness.py --matrix
py scripts/validate_mirror_emit_contract.py
```

---

## Cross-references

- Collapse maps: [`docs/wip/intelligence/canonical-articulation-model-2026-06-05/l2-collapse-maps/_SYNTHESIS-2026-06-08.md`](../../../../wip/intelligence/canonical-articulation-model-2026-06-05/l2-collapse-maps/_SYNTHESIS-2026-06-08.md)
- Operator ratification: [`i95-round2-operator-ratification-2026-06-09.md`](i95-round2-operator-ratification-2026-06-09.md)
- Mirror walkthrough: [`operator-mirror-apply-walkthrough-2026-06-09.md`](operator-mirror-apply-walkthrough-2026-06-09.md)
