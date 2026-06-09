---
report_type: operator-ratification
parent_initiative: INIT-OPENCLAW_AKOS-95
phase: P95-R2-AskQuestion-2
authored: 2026-06-09
authored_by: Execution seat (Composer)
closure_decision_source: operator_explicit
ratifying_decisions:
  - D-IH-95-G
  - D-IH-95-H
  - D-IH-95-I
status: ratified
---

# I95 Round-2 — AskQuestion #2 operator ratification (2026-06-09)

Binding operator choices for post-GOV-8 Round-2 execution. Supersedes phasing ambiguity in [`i95-round2-operator-ratification-2026-06-09.md`](i95-round2-operator-ratification-2026-06-09.md) §"All bundles" with explicit per-lane dispositions.

---

## Ratified choices

| Question | Choice | Plain-language disposition |
|:---|:---|:---|
| **L2** | **B** | Audit-only — run HLK + capability + mirror validators; **no CSV re-collapse** unless drift found |
| **L3** | **A** | Single tranche-4 commit for **bundles A+B** (~12 net-new bindings); **Bundle C** (TRP-030/036) charter only — no promotion |
| **Neo4j** | **A** | Implement dual-emit path in `sync_hlk_neo4j` (code); live sync only if `NEO4J_*` in `~/.openclaw/.env` else document **BLOCKED-ENV** |
| **Hygiene C** | **C** | Full settlement tranche scope — defer to separate packet if >1 commit; mint charter only this session if too large |
| **Master seq** | **A** | Mirror (operator) → L3 A+B → L1 EG → Neo4j; **L2 audit now** |

---

## This session execution map

| Packet | Status @ commit | Notes |
|:---|:---|:---|
| L2 audit | **DONE** | [`i95-l2-audit-2026-06-09.md`](i95-l2-audit-2026-06-09.md) — PASS-WITH-FOLLOWUPS |
| L3 tranche-4 A+B | **DONE** | 12 bindings; `L3_FK_BINDINGS` 22→34; TRP-008 deduped (tranche-1) |
| L3 Bundle C | **CHARTER ONLY** | TRP-030/036 stay **planned** per [`l3-trp-030-036-ratification-2026-06-09.md`](l3-trp-030-036-ratification-2026-06-09.md) |
| L1 EG-2 doc | **DEFERRED** | `SUPABASE_API_EXPOSURE.md` skeleton — next L1 packet after mirror walkthrough |
| Neo4j dual-emit | **FORWARD** | Separate execution packet per Neo4j choice A |
| Hygiene C settlement | **FORWARD** | Charter-only if scope exceeds one commit |

---

## L3 tranche-4 binding inventory

### Bundle A (data-plane) — 6 bindings

| CSV column | Triple |
|:---|:---|
| `aic_capability_implementation_matrix.capability_id` | TRP-038 |
| `aic_capability_implementation_matrix.aic_id` | TRP-038 |
| `data_contract_registry.producer_process_id` | TRP-045 |
| `data_contract_registry.consumer_area_ids` | TRP-046 |
| `data_contract_registry.data_surface` | TRP-047 |
| `topic_registry.parent` | TRP-021 |

### Bundle B (engagement cluster) — 6 bindings

| CSV column | Triple |
|:---|:---|
| `engagement_registry.counterparty_org_id` | TRP-012 |
| `use_case_archive.capability_id` | TRP-029 |
| `use_case_archive.engagement_id` | TRP-042 |
| `initiative_registry.program_anchors` | TRP-015 |
| `goi_poi_register.process_item_id` | TRP-043 |
| `goi_poi_register.program_id` | TRP-044 |

**Deduped:** `process_list.engagement_template_id` → TRP-008 already in tranche-1.

**Registry `current_fk` normalization:** Uppercase slugs (`ENGAGEMENT_REGISTRY`, `USE_CASE_ARCHIVE`, etc.) → lowercase registry slugs; TRP-038 bare registry → column-level FK.

---

## Verification @ commit

| Gate | Result |
|:---|:---|
| `py scripts/validate_fk_verb_coverage.py` | PASS (34 bindings) |
| `py scripts/validate_hlk.py` | PASS |
| `py scripts/verify.py pre_commit_fast` | PASS |

---

## Cross-references

- Bundle charters: [`i95-l3-parallel-bundles-charter-2026-06-09.md`](i95-l3-parallel-bundles-charter-2026-06-09.md)
- L2 state (pre-audit): [`i95-l2-state-audit-2026-06-09.md`](i95-l2-state-audit-2026-06-09.md)
- Mirror walkthrough: [`operator-mirror-apply-walkthrough-2026-06-09.md`](operator-mirror-apply-walkthrough-2026-06-09.md)
