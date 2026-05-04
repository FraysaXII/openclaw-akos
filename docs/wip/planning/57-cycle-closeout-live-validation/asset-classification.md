---
language: en
status: active
initiative: 57-cycle-closeout-live-validation
report_kind: asset-classification
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-04
---

# Initiative 57 — Asset classification

Per [`docs/references/hlk/compliance/PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). Cycle-1 ships P0 + P1 + P2 + P3 + P6 (engineering); P4 forwards as OPS-57-1; P5 forwards as OPS-57-2. The rows below describe what each phase actually touches.

## Canonical (edit here first)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `scripts/sync_compliance_mirrors_from_csv.py` | [`scripts/sync_compliance_mirrors_from_csv.py`](../../../../scripts/sync_compliance_mirrors_from_csv.py) | P1 — F-22a-EMIT-1 DATE NULL coercion in `_emit_sourcing_register_upserts` (line 384+) and F-22a-EMIT-2 NOT NULL bool default in `_emit_skill_registry_upserts` (line 434+) | Per-fix regression test in `tests/test_compliance_mirror_emit.py` |
| `static/madeira_control.html` | [`static/madeira_control.html`](../../../../static/madeira_control.html) | P1 — OPS-54-1.a CSS contrast on `button[data-locale-set="en\|es\|fr"]` (WCAG 1.4.3); OPS-54-1.b `tabindex` on `#handoff-example` (WCAG 2.1.1 + 2.1.3) | `browser-smoke.py --playwright --axe` returns 0 Critical / 0 Serious |
| `docs/wip/planning/45-live-eval-harness/master-roadmap.md` | [link](../45-live-eval-harness/master-roadmap.md) | P2 — frontmatter `status: active` → `status: closed` (UAT 2026-05-01 already declares closure) | `wip_dashboard_render_smoke` |
| `docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md` | [link](../32-holistik-ops-maturation/master-roadmap.md) | P3 — frontmatter `status: active` → `status: closed` (UAT 2026-04-30 already declares closure) | `wip_dashboard_render_smoke` |
| `docs/wip/planning/WIP_DASHBOARD.md` | [link](../WIP_DASHBOARD.md) | P0, P2, P3, P6 — re-render via `scripts/render_wip_dashboard.py` (sha256 stable across two consecutive runs per the determinism gate) | `wip_dashboard_render_smoke` |
| `docs/wip/planning/README.md` | [link](../README.md) | P0 — add row 57 between I55 and `99-proposals` | manual visual review |
| `CHANGELOG.md` | [link](../../../../CHANGELOG.md) | P0 — `[Unreleased]` / Added entry; P6 — closure entry | manual visual review |

## Modified canonical (status flip only — content already shipped)

These two master-roadmap files are content-complete (UAT reports declare closure) but the master-roadmap frontmatter still reads `status: active`. P2 and P3 flip the frontmatter and refresh `last_review` after re-running the verification matrix.

- [`docs/wip/planning/45-live-eval-harness/master-roadmap.md`](../45-live-eval-harness/master-roadmap.md) — closes via [`reports/uat-i45-live-eval-harness-2026-05-01.md`](../45-live-eval-harness/reports/uat-i45-live-eval-harness-2026-05-01.md) which already carries `status: closed`.
- [`docs/wip/planning/32-holistik-ops-maturation/master-roadmap.md`](../32-holistik-ops-maturation/master-roadmap.md) — closes via [`reports/uat-i32-holistik-ops-maturation-2026-04-30.md`](../32-holistik-ops-maturation/reports/uat-i32-holistik-ops-maturation-2026-04-30.md) which already carries `status: closed`.

## Mirrored / derived (P4 OPS-57-1 only)

| Asset | Path | Touch point |
|:------|:-----|:------------|
| `artifacts/dossier-i57-live-cycle/` | gitignored under `artifacts/` | P4 (d) — live `--filter madeira` dossier emit; manifest sha256 recorded in P4 phase report |
| `tests/evals/cassettes/<persona_id>/` | per-persona cassette folders | P4 (b) — OPS-50-1/51-1 persona-keyed cassette dispatch in multi-judge harness mode; recorded under `AKOS_RECORD_LIVE=1` |
| `tests/evals/cassettes/graph_rag/` | existing GraphRAG cassettes folder | P4 (c) — OPS-53-1 GraphRAG A/B run cassettes; preserved as ship-ready (per [I53 P6](../53-graphrag-poc-closure/master-roadmap.md)) |
| `compliance.eval_run` | Supabase mirror (DDL from [I45 P4](../45-live-eval-harness/master-roadmap.md)) | P4 (a) + (b) + (c) — write events that fill the mirror so P4 (d) dossier reads real Section 3 / 5 / 7 rows |
| `compliance.dossier_run` | Supabase mirror (DDL from [I48](../48-operator-dossier/master-roadmap.md)) | P4 (d) — `dossier_run_writer` records the live emit |

Mirror DML uses `compliance_mirror_emit`; **no megabyte migration files**. Per the AKOS governance remediation rule §"Supabase DDL vs mirror DML".

## Operator-authored canonical (P5 OPS-57-2 only)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml` Section 3 | [link](../22a-i22-post-closure-followups/operator-answers-wave2.yaml) | P5 — six GOI/POI voice profiles (operator-authored per D-IH-17) | `wave2_backfill.py --check-only --section goipoi_voice` |
| `docs/wip/planning/22a-i22-post-closure-followups/operator-answers-wave2.yaml` Section 5 | [link](../22a-i22-post-closure-followups/operator-answers-wave2.yaml) | P5 — `process_list.csv` tranche `thi_mkt_dtp_NN` rows (operator-authored per CSV-before-SOP / SOP-META) | `wave2_backfill.py --check-only --section process_list` |
| `docs/references/hlk/compliance/process_list.csv` | derived from Section 5 commit | P5 — CSV tranche merged via the YAML writer | `validate_hlk.py` (HLK gate) |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` | I24 P1 — finalizes once Section 5 process_list rows merge | downstream of P5 | I24-owned gate |

## Conditional new canonical (only if GraphRAG P4 (c) returns GO)

| Asset | Path | Trigger |
|:------|:-----|:--------|
| `docs/references/hlk/compliance/dimensions/SKILL_REGISTRY.csv` `retrieval_mode` column flip | [link](../../../references/hlk/compliance/dimensions/SKILL_REGISTRY.csv) | GraphRAG GO at P4 (c); `SKILL-MADEIRA-LOOKUP-V1.retrieval_mode` flips from `vector_only` to `graph_rag` (or `hybrid`) |
| `docs/references/hlk/compliance/dimensions/POLICY_REGISTER.csv` new `pol_neo4j_graph_rag_eligibility` row | [link](../../../references/hlk/compliance/dimensions/POLICY_REGISTER.csv) | GraphRAG GO at P4 (c); POLICY clone per [I46 P5](../46-neo4j-strategic-posture/master-roadmap.md) infrastructure |

**Out-of-scope for I57.** If P4 (c) returns GO, spawn a small follow-on task (not a new initiative; the infrastructure was preserved ship-ready by I53).

## Reference-only

| Asset | Path | Touch point |
|:------|:-----|:------------|
| I57 phase reports | `reports/p<N>-*-2026-05-DD.md` | P0 + P1 + P2 + P3 + P6 (P4 + P5 phase reports written when OPS items fire) |
| I57 closure UAT | `reports/uat-i57-cycle-closeout-2026-05-DD.md` | P6 |
| I22a [`reports/uat-i24-supabase-apply-20260504.md`](../22a-i22-post-closure-followups/reports/uat-i24-supabase-apply-20260504.md) | (read-only) | P1 references the in-batch patches that motivated F-22a-EMIT-1 + F-22a-EMIT-2 |
| I54 [`reports/uat-i54-live-a11y-audit-20260504.md`](../54-surface-test-hardening/reports/uat-i54-live-a11y-audit-20260504.md) | (read-only) | P1 references the OPS-54-1 axe findings (F-1 color-contrast, F-2 scrollable-region-focusable) |
| I46 [`reports/uat-i46-i53-graphrag-2026-05-03.md`](../53-graphrag-poc-closure/reports/uat-i46-i53-graphrag-2026-05-03.md) | (read-only) | P4 (c) cites the I53 dispatcher-validation baseline that OPS-53-1 will validate live against |
| I52 [`reports/uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md`](../52-multi-model-judge-and-cost-discipline/reports/uat-i52-multi-model-judge-and-cost-discipline-2026-05-03.md) | (read-only) | P4 (a) cites the dispatcher-validation calibration baseline that OPS-52-1 will validate live against |

## Scripts (no new scripts in I57)

| Script | Path | Touch point |
|:-------|:-----|:------------|
| `scripts/sync_compliance_mirrors_from_csv.py` | [link](../../../../scripts/sync_compliance_mirrors_from_csv.py) | P1 — modified (two value-coercion fixes) |
| `scripts/render_wip_dashboard.py` | [link](../../../../scripts/render_wip_dashboard.py) | P0 + P2 + P3 + P6 — re-render after each status flip |
| `scripts/render_uat_dossier.py` | [link](../../../../scripts/render_uat_dossier.py) | P4 (d) + P6 — `--filter madeira --mode live` (P4) and snapshot (P6) |
| `scripts/judge_calibration_burn.py` | [link](../../../../scripts/judge_calibration_burn.py) | P4 (a) — `--live` for OPS-52-1 |
| `scripts/graphrag_poc.py` | [link](../../../../scripts/graphrag_poc.py) | P4 (c) — `--live --golden-set` for OPS-53-1 |
| `scripts/endpoint_envelope_alarm.py` | [link](../../../../scripts/endpoint_envelope_alarm.py) | P4 — abort threshold $40 wired (G-57-2) |
| `scripts/wave2_backfill.py` | [link](../../../../scripts/wave2_backfill.py) | P5 — `--check-only` sentinel scan |
| `scripts/browser-smoke.py` | [link](../../../../scripts/browser-smoke.py) | P1 + P6 — `--playwright --axe` |
| `scripts/release-gate.py` | [link](../../../../scripts/release-gate.py) | P6 — 8/8 closure gate |
| `scripts/validate_hlk.py` | [link](../../../../scripts/validate_hlk.py) | P1 + P3 + P5 + P6 |
| `scripts/legacy/verify_openclaw_inventory.py` | [link](../../../../scripts/legacy/verify_openclaw_inventory.py) | every phase |
| `scripts/check-drift.py` | [link](../../../../scripts/check-drift.py) | every phase |
| `scripts/test.py` | [link](../../../../scripts/test.py) | every phase (`all` mode) |

Per the master-roadmap "asset classification → no new scripts in I57". This list is the read-side of that contract.
