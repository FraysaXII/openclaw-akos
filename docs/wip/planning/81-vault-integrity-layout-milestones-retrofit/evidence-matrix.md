# I81 — Evidence matrix

What evidence each phase produces and what verifier validates it.

| Phase | Evidence artefact | Validator | Manual review? |
|:---|:---|:---|:---|
| **P0 — Charter** | `master-roadmap.md` + 5 sibling planning files + INIT/DEC/OPS canonical rows | `py scripts/validate_hlk.py` | Inline-ratify (operator skip 2026-05-16 → `agent_inline_default`) |
| **P1 — Vault integrity baseline** | `reports/i81/kb-integrity-audit-<date>.md` + `reports/i81/kb-integrity-matrix-<date>.csv` + KNOWLEDGE_PAIRING gap register + mirror-emit coverage checklist | `py scripts/validate_hlk.py` (umbrella: includes `validate_process_list_pairing.py`, `validate_knowledge_pairing_registry.py`); `py scripts/verify.py compliance_mirror_emit` profile | Operator inline-ratify (D-IH-81-F close) — PASS threshold + waiver narrative for any FAIL rows |
| **P2 — Layout migration** (per tranche) | `git mv` commits + `PRECEDENCE.md` diffs + validator Path-constant diffs + `sync_compliance_mirrors_from_csv.py` diffs + `hlk-erp` route diffs + `validate_hlk.py` GREEN | `py scripts/validate_hlk.py`; `py scripts/verify.py compliance_mirror_emit`; sibling repo CI on `hlk-erp` PR | **Operator approval per tranche** (canonical-CSV gate; D-IH-81-G per-tranche) |
| **P3 — Named-milestone schema** | `akos/hlk_planning_milestone.py` + `scripts/validate_planning_cross_refs.py` + `tests/test_planning_cross_refs.py` + `reports/p3-class-b-regression-sweep-<date>.md` + cursor-rule extension + migration commits for active candidates + dep map + active master-roadmaps | New validator GREEN; `py scripts/validate_hlk.py`; `py scripts/test.py governance`; `py scripts/release-gate.py` | Inline-ratify (D-IH-81-I + D-IH-81-J close) |
| **P4-P8 — Retrofit strands** | Per-strand retrofit log + paired body+addendum commits + KNOWLEDGE_PAIRING row appends + `addendum_needed: false` decisions where applicable | `py scripts/validate_knowledge_pairing_registry.py`; `py scripts/validate_process_list_pairing.py`; jargon-scan on People-area bodies | Per-strand author judgement; role_owner sign-off per pair |
| **P9 — Closure UAT** | `reports/p9-uat-<date>.md` with integrity regression GREEN + spot-check DQ row PASS rate + mirror smoke + named-milestone validator GREEN on full active surface | `py scripts/verify.py pre_commit`; `py scripts/release-gate.py`; new class-B validator GREEN | Operator approval (closure gate) |

## Acceptance threshold

- **P1 PASS bar**: ≥ 95% of executable `process_list.csv` rows resolve cleanly through `item_id → SOP → addendum → runbook → KNOWLEDGE_PAIRING → mirror coverage`. FAIL rows must be tracked as OPS rows + remediation plan in audit narrative.
- **P3 PASS bar**: `validate_planning_cross_refs.py` GREEN on full active planning surface; transition allowlist empty at P3 close (per D-IH-81-I).
- **P9 PASS bar**: all earlier phase PASS bars green + ~40 SOPs retrofitted (or `addendum_needed: false` documented) + cluster cross-check D-IH-86-D GREEN.

## Out-of-band evidence (operator-side)

- Operator confirms layout migration `hlk-erp` consumer parity per tranche (P2).
- Operator confirms each P4-P8 strand's role_owner sign-off (per area).
- Closure UAT operator narrative attached to `reports/p9-uat-<date>.md`.
