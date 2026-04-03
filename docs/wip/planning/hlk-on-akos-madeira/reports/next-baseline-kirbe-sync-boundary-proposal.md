# Next Baseline / KiRBe Sync Boundary Proposal

**Source program**: Madeira Flagship Hardening
**Date**: 2026-04-03
**Status**: Draft for next tranche

---

## 1. Purpose

Define what belongs in the next baseline/compliance tranche and what does not. This keeps the flagship Madeira UX program from silently expanding into a second stream while still capturing the governance and sync lessons needed for KiRBe-from-scratch work.

## 2. What The Next Tranche Owns

- Stable key policy for canonical HLK assets and KiRBe sync targets.
- Canonical-to-derived sync ownership between `docs/references/hlk/compliance/`, `docs/references/hlk/v3.0/`, KiRBe tables, and Drive mirrors.
- Formal propagation workflow for canonical CSV/vault changes into KiRBe and other mirrors.
- Approval-gated canonical enrichment of `baseline_organisation.csv`, `process_list.csv`, and active `v3.0/` assets.
- Higher-assurance admin workflow execution once the Madeira admin branch residual is paired with a runtime/model decision.

## 3. What Stays Out Of Scope For The Flagship Program

- Bulk canonical CSV edits without explicit operator approval.
- Larger KiRBe automation, sync daemons, or mirror-write services.
- `hlk_doc_search` beyond design/prototype as a downstream derived layer.
- A dedicated finance specialist subagent.
- A second parallel telemetry framework outside `akos/telemetry.py` + `scripts/log-watcher.py`.

## 4. Stable Boundary Decisions

- **Canonical truth stays here**: `docs/references/hlk/compliance/` and approved `v3.0/` assets.
- **Mirrors stay downstream**: KiRBe/Supabase, Drive hierarchy, session/local telemetry mirrors.
- **Secrets stay out of repo**: runtime credentials belong in process env or `~/.openclaw/.env`.
- **Operator-visible telemetry stays local-first**: `~/.openclaw/telemetry/` is the immediate evidence surface even when external Langfuse visibility lags.

## 5. Recommended Next Action IDs

- `NBT.1` Freeze stable machine-key policy for role/process sync.
- `NBT.2` Define canonical-to-KiRBe propagation ownership and conflict resolution.
- `NBT.3` Decide which `v3.0/` enrichments are safe before canonical CSV edits.
- `NBT.4` Design approval-gated KiRBe sync automation with deterministic replay and drift evidence.
- `NBT.5` Revisit Madeira admin escalation after model/runtime calibration, not as ad-hoc prompt churn.

## 6. Acceptance For The Next Tranche

- Every sync target has an explicit owner and direction of authority.
- Canonical asset edits remain gated by operator approval plus `py scripts/validate_hlk.py`.
- KiRBe automation is replayable, traceable, and subordinate to canonical HLK assets.
- Madeira flagship telemetry remains the evidence source for whether admin/runtime calibration is actually improving operator outcomes.
