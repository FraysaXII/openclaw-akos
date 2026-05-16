---
initiative_id: I87
language: en
last_review: 2026-05-16
---

# I87 — Evidence matrix

Closure criteria each phase must satisfy. I86 D-IH-86-D mechanical cross-check before sibling closure ratifies cross-references rows below as `INITIATIVE_REGISTRY.evidence_*` columns + `validate_hlk` + `release-gate` PASS.

| Phase | Deliverable | Verification | Artefact |
|:---|:---|:---|:---|
| **P0** | Initiative folder + 6 planning files + INIT/DEC/OPS rows + INITIATIVE_DEPENDENCIES + planning README | `py scripts/validate_hlk.py` PASS; `py scripts/verify.py pre_commit` PASS; `validate_review_stamps.py` PASS | This commit; `files-modified.csv` rows phase=P0 |
| **P1** | Health monitor emits OPS row on N=3 cycles; `OPERATOR_INBOX.md` re-renders with new row | Synthetic failure-cycle script produces row; renderer output matches; manual review of inbox markdown | `reports/p1-escalation-uat-<date>.md` |
| **P2** | `plugins.allow` template + `scripts/validate_openclaw_plugin_pinning.py` + tests | `pytest tests/test_validate_openclaw_plugin_pinning.py` GREEN; `release-gate.py` INFO row green | `reports/p2-plugin-pinning-uat-<date>.md` |
| **P3** | `ollama/qwen3:8b` removed from modelsConfig template; rollback one-liner documented | `py scripts/doctor.py` no longer warns about Ollama context; bonjour self-heal path documented | `reports/p3-modelsconfig-hygiene-uat-<date>.md` |
| **P4** | Gateway-token RCA memo; either upstream ticket reference OR operator-config SOP entry | Memo committed; ticket URL OR `SOP-*.md` cross-reference present | `reports/p4-gateway-token-rca-<date>.md` |
| **P5** | `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001.md` at `status: review`; `scripts/openclaw_health_triage.py` paired runbook; `process_list.csv` row | `py scripts/validate_hlk.py` PASS with new SOP row; `pytest tests/test_openclaw_health_triage.py` GREEN; SOP+runbook cross-references each other | `reports/p5-sop-runbook-uat-<date>.md` |
| **P6 (closure)** | UAT on synthetic 3-failure-cycle exercising end-to-end rails; SOP promotion to `status: active` | UAT report PASS; release-gate 8/8; `validate_hlk` PASS; SOP frontmatter `status: active`; `INITIATIVE_REGISTRY.csv` flip `active → closed`; I86 D-IH-86-D mechanical cross-check PASS | `reports/uat-i87-closure-<date>.md` |

## I86 mechanical cross-check (D-IH-86-D) ordered list

Before flipping `INIT-OPENCLAW_AKOS-87` to `status: closed`, the closure UAT report must demonstrate:

1. All six phases above show row in `files-modified.csv` with `change_kind` matching deliverable.
2. `validate_hlk.py` PASS in P6 transcript.
3. `release-gate.py` 8/8 PASS in P6 transcript.
4. `pytest` GREEN across all I87 tests (test files: `tests/test_validate_openclaw_plugin_pinning.py` + `tests/test_openclaw_health_triage.py`).
5. SOP+runbook pair both present (per `akos-executable-process-catalog.mdc` Rule 1).
6. UAT report present at `reports/uat-i87-closure-<date>.md` with row outcomes per phase table above.
7. R-IH-87-1..5 status reviewed; any remaining `Open` items forwarded as fresh OPS rows.
