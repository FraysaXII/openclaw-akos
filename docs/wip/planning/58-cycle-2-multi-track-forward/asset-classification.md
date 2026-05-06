---
language: en
status: active
initiative: 58-cycle-2-multi-track-forward
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-05
---

# Initiative 58 — Asset classification

Per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). Cycle-2 ships P0 + B + C + D + E (engineering); A may fire inside this window or forward as OPS-58-1. The rows below describe what each phase actually touches.

## Canonical (edit here first)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `scripts/preflight_g58_1.py` (NEW) | [`scripts/preflight_g58_1.py`](../../../../scripts/preflight_g58_1.py) | A.0 — asserts 11/11 env vars + spend ceiling + alarm wiring before A.* fires | `tests/test_preflight_g58_1.py` regression test |
| `akos/runpod_provider.py` (MODIFIED) | [`akos/runpod_provider.py`](../../../../akos/runpod_provider.py) | D.2 — `RUNPOD_ENDPOINT_URL` + `KALAVAI_ENDPOINT_URL` read aliases; `VLLM_*` wins precedence | `tests/test_runpod_provider.py` precedence assertion |
| `config/environments/dev-local.env.example` | [`config/environments/dev-local.env.example`](../../../../config/environments/dev-local.env.example) | D.2 — comment block describing alias seam | Manual visual review |
| `docs/wip/planning/28-investor-style-company-dossier/master-roadmap.md` | [link](../28-investor-style-company-dossier/master-roadmap.md) | B.1 — frontmatter `In execution` → `closed` after I28 verification matrix re-run | `wip_dashboard_render_smoke` |
| `docs/wip/planning/29-multi-phase-consolidation/master-roadmap.md` | [link](../29-multi-phase-consolidation/master-roadmap.md) | B.2 — frontmatter `In execution` → `closed` after I29 verification matrix re-run | `wip_dashboard_render_smoke` |
| `docs/wip/planning/30-deck-moat-surgery/master-roadmap.md` | [link](../30-deck-moat-surgery/master-roadmap.md) | B.3 — frontmatter `Open` → `closed` after I30 verification matrix re-run | `wip_dashboard_render_smoke` |
| `docs/wip/planning/31-holistik-ops-discovery/master-roadmap.md` | [link](../31-holistik-ops-discovery/master-roadmap.md) | B.4 — frontmatter `Open` → `closed` after I31 verification matrix re-run; G-58-3 founder ratify | `wip_dashboard_render_smoke` |
| `docs/wip/planning/05-hlk-vault-envoy-repos/master-roadmap.md` (NEW) | [link](../05-hlk-vault-envoy-repos/master-roadmap.md) | D.1 — minimal frontmatter `status: archived` + one-paragraph history reason | `wip_dashboard_render_smoke` |
| `docs/wip/planning/20-kalavai-shadow-llamacpp-trial/master-roadmap.md` (NEW) | [link](../20-kalavai-shadow-llamacpp-trial/master-roadmap.md) | D.1 — minimal frontmatter `status: archived` + one-paragraph history reason | `wip_dashboard_render_smoke` |
| `docs/wip/planning/WIP_DASHBOARD.md` | [link](../WIP_DASHBOARD.md) | P0, B.1, B.2, B.3, B.4, D.1, E.0 — re-render via `scripts/render_wip_dashboard.py` (sha256 stable across two consecutive runs per the determinism gate) | `wip_dashboard_render_smoke` |
| `docs/wip/planning/README.md` | [link](../README.md) | P0 — add row 58 between I57 and `99-proposals` | manual visual review |
| `CHANGELOG.md` | [link](../../../../CHANGELOG.md) | P0 — `[Unreleased]` / Added entry; E.0 — closure entry | manual visual review |

## Modified canonical (B.4 dimension CSV tranches; G-58-2 per-tranche operator approval)

These three new dimension CSVs ship inside Initiative 31 closure (B.4). Each ships its own `validate_*.py` + `compliance.*_mirror` row in the same commit per `.cursor/rules/akos-governance-remediation.mdc`.

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `PERSONA_REGISTRY.csv` | (under `docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv`) | B.4 P2 — Persona archetype registry (~16 archetypes) | New `validate_persona_registry.py` + `compliance_mirror_emit` row |
| `CHANNEL_TOUCHPOINT_REGISTRY.csv` | (under `docs/references/hlk/compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv`) | B.4 P3 — Channel touchpoint registry (~10 channels) | New `validate_channel_touchpoint_registry.py` + `compliance_mirror_emit` row |
| `SOURCING_REGISTER.csv` | (under `docs/references/hlk/compliance/dimensions/SOURCING_REGISTER.csv`) | B.4 P5 — External vendor / sourcing register (with distance fields) | New `validate_sourcing_register.py` + `compliance_mirror_emit` row |
| `GOI_POI_REGISTER.csv` (MODIFIED) | [link](../../../references/hlk/compliance/GOI_POI_REGISTER.csv) | B.4 P2 — +3 distance columns (`distance`, `bridge_via`, `assessed_date`); +6 row backfill | Existing `validate_goipoi_register.py` extended with new invariants |
| `TOPIC_REGISTRY.csv` (MODIFIED) | [link](../../../references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv) | B.3 (+2 from I30: `topic_madeira_platform`, `topic_governance_moat`); B.4 (+4 from I31: `topic_persona_registry`, `topic_channel_touchpoint_registry`, `topic_sourcing_register`, `topic_holistik_ops_discovery`) | `validate_topic_registry.py` + `compliance_mirror_emit` |

## Mirrored / derived (Phase A only; gated by `AKOS_RECORD_LIVE=1`)

| Asset | Path | Touch point |
|:------|:-----|:------------|
| `artifacts/dossier-i58-live-cycle/` | gitignored under `artifacts/` | A.4 — live `--filter madeira` dossier emit; manifest sha256 recorded in A.4 phase report |
| `tests/evals/cassettes/<persona_id>/` | per-persona cassette folders | A.2 — OPS-50-1/51-1 persona-keyed cassette dispatch in multi-judge harness mode; recorded under `AKOS_RECORD_LIVE=1` |
| `tests/evals/cassettes/graph_rag/` | existing GraphRAG cassettes folder | A.3 — OPS-53-1 GraphRAG A/B run cassettes; preserved as ship-ready (per [I53 P6](../53-graphrag-poc-closure/master-roadmap.md)) |
| `compliance.eval_run` | Supabase mirror (DDL from [I45 P4](../45-live-eval-harness/master-roadmap.md)) | A.1 + A.2 + A.3 — write events that fill the mirror so A.4 dossier reads real Section 3 / 5 / 7 rows |
| `compliance.dossier_run` | Supabase mirror (DDL from [I48](../48-operator-dossier/master-roadmap.md)) | A.4 — `dossier_run_writer` records the live emit |

Mirror DML uses `compliance_mirror_emit`; **no megabyte migration files**. Per `.cursor/rules/akos-holistika-operations.mdc` §"Two-plane model".

## Conditional new canonical (only if A.3 = GO)

| Asset | Path | Trigger |
|:------|:-----|:--------|
| `docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv` `retrieval_mode` flip | [link](../../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv) | A.3 GO; `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` flips from `vector_only` to `graph_rag` (or `hybrid`) |
| `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` new `pol_neo4j_graph_rag_eligibility` row | [link](../../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv) | A.3 GO; POLICY clone per [I46 P5](../46-neo4j-strategic-posture/master-roadmap.md) infrastructure |
| Mirror reseed SQL stub | gitignored under `artifacts/sql/` | A.5 — staged for operator-applied `compliance_mirror_emit` |

**A.5 is conditional.** If A.3 returns NO-SHIP, A.5 is SKIPPED and I46 P5 stays deferred per D-IH-58-C. The infrastructure was preserved ship-ready by I53; this is a one-commit follow-on, not a new initiative.

## Operator-loaded (off-repo)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `~/.openclaw/.env` (long-lived block) | `~/.openclaw/.env` (gitignored; resolved by [`akos/io.py`](../../../../akos/io.py) `resolve_openclaw_home()`) | P0 — agent writes structure (Supabase URL + alias-seam stubs + commented Phase A flags + empty placeholders); operator pastes secret values | D-IH-58-F (D-IH-17 invariance forbids agent fabrication of secret values) |

## Reference-only

| Asset | Path | Touch point |
|:------|:-----|:------------|
| I58 phase reports | `reports/p<N>-*-2026-05-DD.md` | P0 + B.1 + B.2 + B.3 + B.4 + C.1 + D.1 + D.2 + E.0 (A.* phase reports written when OPS items fire) |
| I58 closure UAT | `reports/uat-i58-cycle-2-closure-2026-05-DD.md` | E.0 |
| I58 browser MCP UAT | `reports/uat-i58-cycle-2-browser-2026-05-DD.md` | E.0 (qualitative pass per `.cursor/rules/akos-planning-traceability.mdc`) |
| I57 [`reports/uat-i57-cycle-closeout-2026-05-04.md`](../57-cycle-closeout-live-validation/reports/uat-i57-cycle-closeout-2026-05-04.md) | (read-only) | P0 cites the I57 engineering closure as the predecessor state |
| I57 [`reports/p4-live-cycle-forward-2026-05-04.md`](../57-cycle-closeout-live-validation/reports/p4-live-cycle-forward-2026-05-04.md) | (read-only) | A.0 + A.* reuses the runbook verbatim if Phase A fires |
| I46 + I53 [`uat-i46-i53-graphrag-2026-05-03.md`](../53-graphrag-poc-closure/reports/uat-i46-i53-graphrag-2026-05-03.md) | (read-only) | A.3 cites the I53 dispatcher-validation baseline that OPS-53-1 will validate live against |
| I52 [`uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md`](../52-multi-model-judge-and-cost-discipline/reports/uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md) | (read-only) | A.1 cites the dispatcher-validation calibration baseline that OPS-52-1 will validate live against |

## Scripts (one new + one modified)

| Script | Path | Touch point |
|:-------|:-----|:------------|
| `scripts/preflight_g58_1.py` (NEW) | [link](../../../../scripts/preflight_g58_1.py) | A.0 — asserts 11/11 env vars + spend ceiling + alarm wiring; exits non-zero with checklist on miss |
| `akos/runpod_provider.py` (MODIFIED) | [link](../../../../akos/runpod_provider.py) | D.2 — alias seam reads `RUNPOD_ENDPOINT_URL` + `KALAVAI_ENDPOINT_URL` |
| `scripts/render_wip_dashboard.py` | [link](../../../../scripts/render_wip_dashboard.py) | P0 + B.* + D.1 + E.0 — re-render after each status flip |
| `scripts/render_uat_dossier.py` | [link](../../../../scripts/render_uat_dossier.py) | A.4 — `--filter madeira --mode live` (operator-funded) |
| `scripts/judge_calibration_burn.py` | [link](../../../../scripts/judge_calibration_burn.py) | A.1 — `--n 50 --persona founder --target-pp 80` for OPS-52-1 (operator-funded) |
| `scripts/graphrag_poc.py` | [link](../../../../scripts/graphrag_poc.py) | A.3 — `--max-spend 20 --golden-set` for OPS-53-1 (operator-funded) |
| `scripts/endpoint_envelope_alarm.py` | [link](../../../../scripts/endpoint_envelope_alarm.py) | A.* — abort threshold $40 wired (G-58-1) |
| `scripts/browser-smoke.py` | [link](../../../../scripts/browser-smoke.py) | E.0 — `--playwright --axe` (verify no regression on OPS-54-1.c fix) |
| `scripts/release-gate.py` | [link](../../../../scripts/release-gate.py) | E.0 — 8/8 closure gate |
| `scripts/validate_hlk.py` | [link](../../../../scripts/validate_hlk.py) | After every B.* + A.5 + D.1 |
| `scripts/validate_hlk_km_manifests.py` | [link](../../../../scripts/validate_hlk_km_manifests.py) | After B.4 (touchpoint kit manifests) |
| `scripts/legacy/verify_openclaw_inventory.py` | [link](../../../../scripts/legacy/verify_openclaw_inventory.py) | every phase |
| `scripts/check-drift.py` | [link](../../../../scripts/check-drift.py) | every phase |
| `scripts/test.py` | [link](../../../../scripts/test.py) | every phase (`all` mode) |

The new + modified scripts (`preflight_g58_1.py` + `akos/runpod_provider.py`) are the only application-code surface this initiative ships; B.1–B.4 reuse existing strategy initiative scripts; A.* reuses existing eval/dossier scripts.
