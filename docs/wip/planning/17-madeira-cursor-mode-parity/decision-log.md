# Decision log — Initiative 17

| ID | Question | Options | Decision | Date |
|:---|:---------|:--------|:---------|:-----|
| D1 | Where to persist interaction mode? | openclaw.json only; `.akos-state.json` | **`.akos-state.json`** (`AkosState.madeiraInteractionMode`) — same lifecycle as model switch, no OpenClaw schema churn | 2026-04-21 |
| D2 | How to apply Plan draft without new global prompt tier? | New variant in model-tiers; append overlay after deploy | **Append** `OVERLAY_MADEIRA_PLAN_DRAFT.md` to Madeira `SOUL.md` when mode is `plan_draft`, base assembly = `standard`; Ask uses `compact` | 2026-04-21 |
| D3 | Gateway WebChat native mode picker? | Fork OpenClaw; AKOS companion page | **Companion page** on AKOS (`GET /madeira/control`) until gateway exposes metadata | 2026-04-21 |
| D4 | Plan handoff validation in CI? | Hand-rolled checks; `jsonschema` | **`jsonschema`** against `madeira-plan-handoff.schema.json` (SSOT) | 2026-04-21 |
| D5 | SWE-bench analogue for AKOS? | Simulate on Madeira; skip | **Optional `executor_harness` marker** + ephemeral patch + pytest oracle (swarm scope only) | 2026-04-21 |
| D6 | LLM-as-judge for HLK facts? | Primary gate | **No** — oracles (CSV, schema, routing) + rubrics | 2026-04-21 |
| D7 | Release gate eval scope? | pathc only | **`AKOS_EVAL_RUBRIC=1` runs `pathc-research-spine` + `madeira-operator-coverage`** | 2026-04-21 |
| D8 | Golden manifest hygiene? | Ad hoc | **`schema_version` + `last_reviewed` on suite manifests** | 2026-04-21 |
