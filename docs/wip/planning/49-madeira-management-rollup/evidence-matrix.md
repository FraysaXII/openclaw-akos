---
language: en
status: active
initiative: 49-madeira-management-rollup
report_kind: evidence-matrix
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# Initiative 49 — Evidence matrix

Structured observations that justified this initiative before and during execution.

| ID | Observation | Source | Impact |
|:---|:------------|:-------|:-------|
| E1 | MADEIRA infra (I47 personas, I48 dossier) lacks a bounded **process tier** tying SOP ↔ process_list ↔ dossier verdict | Operator feedback 2026-05-02 | Canonical tranche plus four SOPs |
| E2 | Tier-3 WebChat UAT recurrently BLOCKED on Docker sandbox preflight (`npipe` on Windows) | [`uat-madeira-uc-20260425.md`](../17-madeira-cursor-mode-parity/reports/uat-madeira-uc-20260425.md) | `doctor.py --docker-sandbox` gate |
| E3 | Backlog sorting at 326+ scenarios requires deterministic rank, not intuition | PERSONA_SCENARIO_REGISTRY growth | priority_score formula + safety_lane |
| E4 | Third light **Surface UX** absent from dossier executive logic | Gap vs three-light verdict | Section 8 Surface sub-section + Impeccable artefacts |
| E5 | Flaky eval scenarios need lifecycle state without deleting history | Canary noise | quarantined + quarantine CLI |
| E6 | External prose drifts toward stack jargon between brand audits | I27 / I31 closure observations | `scripts/lint_brand_voice_offline.py` wired into `pre_commit` |
| E7 | Telemetry signal dies in `~/.openclaw/telemetry/` jsonl | I46 P4 deferred KG; no proposal pathway | `scripts/promote_telemetry_to_scenario.py` emits proposal JSON for operator review |
| E8 | Operators kept the surface in English-only despite multilingual audience (I31 D-IH-31-D) | I31 closure follow-up | en/es/fr dictionary + locale toggle in redesigned control plane |
| E9 | Three-light dossier verdict needs to roll into trend storage cleanly | I48 D-IH-48-D ordering invariant | `flavor='madeira'` field in `compliance.dossier_run.section_metrics`; preserves 12-section order |
| E10 | UAT closure needs evidence trail proving SOP execution | I29 / I32 patterns | First MADEIRA dossier emit at closure, paths cited in the closure UAT report |


