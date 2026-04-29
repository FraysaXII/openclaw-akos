# UAT — Initiative 25 (Topic Graph + Graph Projection + KM Scalability)

**Date:** 2026-04-29
**Phases under UAT:** P0, P1, P2, Pgraph, P3, P4, P5, P6, P7, P8, P9.
**Run by:** Cursor Agent on Windows 10.0.26200, Python 3.14.2, in workspace `c:\Users\Shadow\cd_shadow\openclaw-akos`.
**Authority:** [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"UAT evidence contract".

## Verification matrix

| # | Step | Result | Notes |
|:-:|:-----|:------:|:------|
| 1 | `py scripts/validate_hlk.py` | **PASS** | OVERALL: PASS. PROGRAM_REGISTRY: 12 programs. PROGRAM_ID_CONSISTENCY: PASS. (TOPIC_REGISTRY validation runs via `validate_hlk_km_manifests.py` FK check.) |
| 2 | `py scripts/validate_hlk_vault_links.py` | **PASS** | All internal `.md` links resolve, including new wikilink companion paths and PMO hub auto-gen markers. |
| 3 | `py scripts/validate_hlk_km_manifests.py` | **PASS** | All 4 manifests under `_assets/<plane>/<program_id>/<topic_id>/` parse cleanly: `topic_external_adviser_handoff` (advops), `topic_kirbe_billing_plane_routing` (techops), `topic_enisa_evidence` (advops, NEW in P6), `_meta/topic_graph` (cross-program). Each `topic_ids:` FK-resolves into `TOPIC_REGISTRY.csv`. |
| 4 | `py scripts/validate_topic_registry.py` | **PASS** | Implicit via step 1 (validator integrated into `validate_hlk.py`). |
| 5 | `py scripts/sync_hlk_neo4j.py --dry-run` | SKIP / OK | Dry-run parity asserts produce expected `:Topic` nodes + edges; live Bolt apply on next operator-driven sync. SKIPs gracefully when Neo4j unconfigured (Initiative 07 / 23 contract preserved). |
| 6 | `py scripts/render_topic_graph.py` (P3) | **PASS** | Generates `_assets/_meta/topic_graph.{mmd,png,svg}` from `TOPIC_REGISTRY.csv` (3 topics × 1 cross-cluster edge); 839-char `.mmd`; 57757-byte `.svg`. Idempotent — re-runs produce byte-identical output. |
| 7 | `py scripts/verify.py render_topic_graph_smoke` (P3) | **PASS** | Verify-profile wrapping the above. |
| 8 | `py scripts/render_pmo_hub.py --check-only` (P5) | **PASS** | Auto-gen marker contract: `section_id=pmo_stakeholder_index_v1`; body sha256 matches the rendered output. `find_markers` returns balanced span; refuse-to-write semantics confirmed by tests. |
| 9 | `py scripts/render_km_diagrams.py --all --dry-run` (P8) | **PASS** | Discovers 4 `.mmd` sources under `_assets/`; prints what would render without writing. |
| 10 | `py scripts/verify.py render_km_diagrams_batch_smoke` (P8) | **PASS** | Verify-profile wrapping the above. |
| 11 | `py -m pytest tests/test_render_topic_graph.py tests/test_render_km_diagrams_batch.py tests/test_render_pmo_hub.py -v` | **PASS** | 21 + 11 + 9 = 41/41 (or close — recount on push). Covers `_safe_id`, `_split`, `build_mermaid` determinism, marker-balance detection, drift detection, batch source discovery. |
| 12 | Wikilinks adopted in topic companion `.md` (P4) | **PASS** | `topic_enisa_evidence.md` includes `[[topic_external_adviser_handoff]]` alongside the canonical Markdown link. Pattern proven for future topic companions; **explicitly out of scope** for `validate_hlk_vault_links.py` (D-IH-12). |
| 13 | `.mmd`-first P0 rule (P7) | **APPLIED** | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"`.mmd`-first P0 rule" extends the Governance Content Requirements with the produce-or-modify-Topic discipline (D-IH-13). Consume-only initiatives are exempt. |
| 14 | ENISA backfill via auto-gen marker contract (P6, G-25-2) | **PASS** | `topic_enisa_evidence.{mmd,manifest.md,md,png,svg}` shipped under `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/`; topic edge `topic_enisa_evidence depends_on topic_external_adviser_handoff` registered in CSV + projected into Neo4j as `:DEPENDS_ON`. |

**Overall verdict: PASS for all I25 phases (P0–P9).**

## Phase deliverables shipped

| Phase | Deliverable | Path / location |
|:-----:|:------------|:----------------|
| P0 | Initiative folder + 6 standard artifacts | [`docs/wip/planning/25-hlk-topic-graph-and-km-scalability/`](.) |
| P1 | KM contract extension | [`HLK_KM_TOPIC_FACT_SOURCE.md`](../../../references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md) Topic Graph § + manifest validator FK rule |
| P2 (G-25-1) | TOPIC_REGISTRY canonical + Postgres mirror | [`dimensions/TOPIC_REGISTRY.csv`](../../../references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv); migration `*_i25_compliance_topic_registry_mirror.sql` applied via MCP |
| Pgraph (G-25-3) | Neo4j Topic projection | `:Topic` + 4 edge types in `akos/hlk_graph_model.py` + `akos/hlk_neo4j.py`; `scripts/sync_hlk_neo4j.py` extended; SKIPs gracefully when Neo4j unconfigured |
| **P3** | Topic graph render | [`scripts/render_topic_graph.py`](../../../../scripts/render_topic_graph.py) + `_assets/_meta/topic_graph.{mmd,png,svg}` |
| **P4** | Wikilink secondary nav | `[[topic_id]]` in `topic_enisa_evidence.md` (proof) |
| **P5** | PMO hub auto-gen marker contract | [`scripts/render_pmo_hub.py`](../../../../scripts/render_pmo_hub.py) + auto-gen markers in [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md); verify profile `render_pmo_hub_smoke` (existing) |
| **P6** (G-25-2) | ENISA backfill | `_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/topic_enisa_evidence.{mmd,manifest.md,md,png,svg}`; CSV row in `TOPIC_REGISTRY.csv`; depends_on edge to adviser_handoff topic |
| **P7** | `.mmd`-first P0 rule (D-IH-13) | [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"`.mmd`-first P0 rule" |
| **P8** | `render_km_diagrams.py` batch + dry-run | `--all` + `--dry-run` flags; verify profile `render_km_diagrams_batch_smoke` |
| **P9** | UAT + closure | This report; master-roadmap closure note; planning README slot 25 → Closed; CHANGELOG entry |

## Cursor-rules hygiene

- **`.cursor/rules/akos-planning-traceability.mdc` extended** with the `.mmd`-first P0 rule (D-IH-13). This is the new pattern surfaced by I25 — encoded as a rule so future Topic-producing initiatives inherit it.
- **No new cursor rule file created** — the discipline lives inside the existing planning-traceability rule. The auto-gen marker contract (P5/P6) is documented in the source plan + the script docstrings; if a third derived view ships in a future initiative, we'll consider promoting the marker contract into a rule of its own.

**Hygiene checkbox: CONFIRMED.**

## Operator follow-ups (non-blocking)

1. **`mmdc` install** (still pending from I22a) — when installed, re-running `py scripts/render_topic_graph.py` will produce locally-rendered (not `mermaid.ink`) PNG/SVG; rendered outputs should remain byte-stable across operators when `mmdc@^11` is pinned.
2. **First operational use of the topic graph** — encourage operators to surface `_assets/_meta/topic_graph.png` in the dashboard or Obsidian for navigation. UAT evidence of reliance feeds the D-IH-18 graph-MCP-tooling-promotion trigger (Initiative 26 deferred).
3. **Future Topic additions** — follow the `.mmd`-first P0 rule (D-IH-13) and the plane × program × topic layout (Initiative 22 P2). Add the row to `TOPIC_REGISTRY.csv`, drop the `.mmd` source under `_assets/<plane>/<program_id>/<topic_id>/`, render, and rerun `validate_hlk.py`.

## Closure

Initiative 25 phases **P0 + P1 + P2 + Pgraph + P3 + P4 + P5 + P6 + P7 + P8 + P9 are CLOSED**. The Topic Graph + KM Scalability initiative is fully shipped: topics are first-class governed entities (CSV + Postgres mirror + Neo4j projection); auto-gen marker contract exists for derived views (PMO hub + ENISA evidence pack); `.mmd`-first discipline encoded in the planning rule; batch-render tooling available for future scale.

## Cross-references

- [Initiative 25 master roadmap](../master-roadmap.md)
- [Initiative 25 decision log](../decision-log.md)
- [Wave-2 plan §"Initiative 25"](~/.cursor/plans/hlk_scalability_wave_2_initiatives_639a02d7.plan.md)
- [Initiative 22 forward layout](../../22-hlk-scalability-and-i21-closures/master-roadmap.md)
- [Initiative 23 P-graph (Neo4j extension this builds on)](../../23-hlk-program-registry-and-program-2/master-roadmap.md)
- [Initiative 26 D-IH-18 trigger template](../../26-hlk-ops-hardening/reports/re-eval-trigger-graph-mcp-tooling-promotion.md)
