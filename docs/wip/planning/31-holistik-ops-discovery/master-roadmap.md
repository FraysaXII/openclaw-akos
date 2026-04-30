---
language: en
---

# Initiative 31 — Holistik Ops Discovery: 5-axis operating system for human interactions

**Folder:** `docs/wip/planning/31-holistik-ops-discovery/`
**Status:** Open (started 2026-04-30)
**Authoritative Cursor plan:** `~/.cursor/plans/holistik_ops_discovery_3b68fd00.plan.md`

## Outcome

Discover and codify "Holistik Ops" — the missing operational interface layer between AKOS canonicals and the messy real world of multilingual (EN/ES/FR), multi-channel (LinkedIn, email, web, ads, search, referrals, scheduled calls), multi-stakeholder, **multi-distance** (N1/N2/N3/N4 social-graph reach) human interactions. Foundation for everything that talks to humans outside the repo.

The 5-axis Holistik Ops operating system: **Persona × Channel × Distance × Language × Artifact-class**. Each axis is a governed registry; cross-axis routing happens via a touchpoint kit + brand-voice rules.

## Why now

- Founder is **already operating multilingually** (EN/ES/FR) across 8+ channels (LinkedIn DMs, email, web form, future ads, organic search, advisor referrals, partner joint-equity inquiries, hourly-rate vendor sourcing).
- Initiative 30 surfaced a real inconsistency: 2 strategy artifacts in Spanish, 8 in English — no codified rule yet.
- Existing GOI/POI register tracks named individuals but **does not record distance** — there is no current way to query "who do I know at N1 in the investor world?" or "which N2 bridges can warm-intro me?".
- Founder said: "we're close to discovering our holistik ops, i can feel it."

## Scope decisions

| In scope | Out of scope |
|:---|:---|
| Frontmatter `language:` policy + validator + migration of canonical MDs | Auto-translation tooling (manual rewrite per BRAND_*_PATTERNS) |
| Persona registry (~16 archetypes) | Mapping every named individual (GOI/POI register stays canonical for that — extended with distance) |
| Distance dimension on GOI/POI register (N1/N2/N3/N4 + bridge_via FK + assessed_date) | Full social-graph database (CSV + FK column is enough for today) |
| Channel touchpoint registry (~10 channels) | Building a CRM (lean on existing canonicals) |
| Per-persona × per-channel touchpoint kit (8 high-leverage seeds; rest staged as TODO[OPERATOR-x]) | All 16 × 10 × 4 × 3 = 1.920 cells (over-engineered for today) |
| Outbound brief template + sourcing register (with distance fields) | Filling the actual hourly-rate bands per discipline (founder-decision territory) |
| HOLISTIK_OPS_DISCOVERY.md meta-pattern document (5-axis) | Productizing Holistik Ops as a Holistika-external offering (later) |
| French brand-voice rules placeholder | Full BRAND_FRENCH_PATTERNS.md authoring (deferred until first FR external deliverable) |

## Asset classification (per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md))

| Class | Paths | Rule |
|:------|:------|:-----|
| **New canonical (planning)** | `docs/wip/planning/31-holistik-ops-discovery/{master-roadmap,decision-log,asset-classification,evidence-matrix,risk-register,discovery-taxonomy}.md` | Standard six-artifact contract + discovery-taxonomy seed |
| **New canonical (governance SOP)** | `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-HLK_LOCALISATION_001.md` | Localisation policy SOP |
| **New canonical (registry)** | `docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv` | Archetype people-axis |
| **New canonical (registry)** | `docs/references/hlk/compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | Channel-axis (operational touchpoints, distinct from CHANNEL_STRATEGY acquisition hypotheses) |
| **New canonical (registry)** | `docs/references/hlk/compliance/dimensions/SOURCING_REGISTER.csv` | External vendor register (with distance fields) |
| **New canonical (template)** | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_{en,es,fr}.md` | Outbound brief template, locale-derived |
| **New canonical (touchpoint kit)** | `docs/references/hlk/v3.0/_assets/touchpoint-kit/<persona_id>/<channel_id>/*` | Per-persona × per-channel × per-language templates with in-file distance variants |
| **New canonical (meta-doc)** | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md` | The 5-axis operating system doctrine |
| **Modified canonical** | `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` (+3 columns; backfill 6 rows) | Schema bump — only modification of pre-existing canonical CSV in this initiative |
| **Modified canonical** | `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` (+4 rows) | `topic_persona_registry` + `topic_channel_touchpoint_registry` + `topic_sourcing_register` + `topic_holistik_ops_discovery` |
| **Modified canonical** | `akos/hlk_goipoi_csv.py` (3 new fields) + `scripts/validate_goipoi_register.py` (4 new invariants) + `scripts/sync_compliance_mirrors_from_csv.py` (3 new columns in goipoi emit) + `scripts/render_pmo_hub.py` (distance column in autogen) + `SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` (§4.X distance assessment) | Cross-board impact of GOI/POI schema bump |
| **New (mirror migration)** | `supabase/migrations/<ts>_i31_goipoi_distance_extension.sql` | DDL ALTER + UPDATE backfill; operator applies via `npx supabase db push` |
| **Mirror reseed (operator-applied)** | `artifacts/sql/i31_persona_channel_sourcing_topic_upsert.sql` | Staged for operator |
| **Reference-only** | Phase reports under `reports/` | Standard initiative artifact |

## Phase dependency

```mermaid
flowchart TD
    P0[P0_bootstrap_discovery_taxonomy]
    P1[P1_localisation_foundation]
    P2["P2_people_axes_persona_distance_GOIPOI"]
    P3[P3_channel_touchpoint_registry]
    P4[P4_touchpoint_kit_5axis]
    P5[P5_outbound_brief_sourcing]
    P6[P6_holistik_ops_discovery_5axis_doc]
    P7[P7_tests_changelog_uat_pr]
    P0 --> P1
    P0 --> P2
    P0 --> P3
    P1 --> P4
    P2 --> P4
    P3 --> P4
    P1 --> P5
    P2 --> P5
    P4 --> P6
    P5 --> P6
    P6 --> P7
```

## Phase at a glance

| Phase | Deliverable | Acceptance |
|:------|:------------|:-----------|
| **P0** | Initiative folder + 5 standard artifacts + discovery-taxonomy.md + reports/ | Folder exists; decision-log carries D-IH-31-A..H |
| **P1** | SOP-HLK_LOCALISATION_001.md + frontmatter validator + ~80 file migration | `validate_hlk_language_frontmatter.py` PASS; every canonical MD declares `language:` |
| **P2** | PERSONA_REGISTRY.csv (~16 rows) + GOI/POI schema bump + akos updates + 4 validators + mirror DDL + sync flags + 2 topics + SOP §4.X + render_pmo_hub extension | `validate_goipoi_register.py` PASS at new schema; `validate_topic_registry.py` PASS at 21 |
| **P3** | CHANNEL_TOUCHPOINT_REGISTRY.csv (~10 rows) + akos + validator + mirror + sync + topic | `validate_channel_touchpoint_registry.py` PASS; topic_registry at 22 |
| **P4** | Touchpoint kit folder + 8 high-leverage cells with N1/N2/N3+ in-file variants + placeholders | Folder structure resolves all FK; 8 real templates ship |
| **P5** | TEMPLATE_OUTBOUND_BRIEF_{en,es,fr}.md + SOURCING_REGISTER.csv + akos + validator + mirror + topic | First exercise of locale-derivation pipeline; topic_registry at 23 |
| **P6** | HOLISTIK_OPS_DISCOVERY.md (5-axis meta-doc) + topic_holistik_ops_discovery row | Doc names what we built; reach-map property is queryable |
| **P7** | 5 new test suites + extended tests + CHANGELOG + UAT + mirror reseed SQL + DDL migration + commit + PR + merge | `pytest tests/` 0 new failures (excluding pre-existing config drift); PR squash-merged |

## Drift-handling rule (carried forward)

YAML / Markdown SSOT wins for content; Figma wins for visual layout; HTML preview is fast iteration; PDF is disposable. The deck Figma file at `https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW` is **not modified** by this initiative (no deck content changes — I31 is operations-layer, not deck-layer).

## Estimated effort

6-8 hours of focused execution. The migration in P1.3 (~80 MD files) is the biggest mechanical chunk; the GOI/POI distance extension in P2.2 is the highest-risk part of the regression because it modifies a pre-existing canonical CSV.

## Clean-slate criterion (post-merge)

1. `py scripts/validate_hlk.py` — PASS at 23 topics
2. `py scripts/validate_goipoi_register.py` — PASS at 6 rows × new schema
3. `py scripts/validate_hlk_language_frontmatter.py` — PASS (every canonical MD declares `language:`)
4. `py scripts/probe_compliance_mirror_drift.py --verify` after operator applies migration — PASS at 4 mirrors with new schema (3 new + GOI/POI upgraded)
5. `pytest tests/` — same posture as I29/I30 (the 2 sandbox-config failures excluded)
6. `git status` clean; deck rebuild deterministic (HTML + PDF reproduce I30 sha256s — I31 doesn't touch deck content)
