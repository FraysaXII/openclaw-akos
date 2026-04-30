---
language: en
---

# Initiative 31 — Asset classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). Lifecycle status of every asset created or modified.

## New canonical assets (planning)

| Path | Class | Owner | Lifecycle |
|:-----|:------|:------|:----------|
| `docs/wip/planning/31-holistik-ops-discovery/master-roadmap.md` | Planning canonical | PMO | Closes when initiative ends |
| `docs/wip/planning/31-holistik-ops-discovery/decision-log.md` | Planning canonical | PMO | Permanent (audit trail) |
| `docs/wip/planning/31-holistik-ops-discovery/asset-classification.md` | Planning canonical | PMO | Permanent (this file) |
| `docs/wip/planning/31-holistik-ops-discovery/evidence-matrix.md` | Planning canonical | PMO | Permanent |
| `docs/wip/planning/31-holistik-ops-discovery/risk-register.md` | Planning canonical | PMO | Permanent |
| `docs/wip/planning/31-holistik-ops-discovery/discovery-taxonomy.md` | Planning canonical (NEW shape) | PMO | Permanent (seeds the registers; cross-referenced by HOLISTIK_OPS_DISCOVERY.md) |

## New canonical assets (governance SOPs + meta-doc)

| Path | Class | Owner | Lifecycle |
|:-----|:------|:------|:----------|
| `docs/references/hlk/v3.0/Admin/O5-1/Tech/System Owner/SOP-HLK_LOCALISATION_001.md` | Governance SOP | System Owner + Brand Manager | Quarterly review; updated when locale-derivation pipeline evolves |
| `docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_FRENCH_PATTERNS.md` | Brand SSOT (stub) | Brand Manager | `status: stub` until first FR external deliverable lands |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md` | Meta-methodology canonical | PMO + Founder | Updated whenever a new axis or registry joins the operating system |

## New canonical assets (registries)

| Path | Class | Owner | Lifecycle |
|:-----|:------|:------|:----------|
| `docs/references/hlk/compliance/dimensions/PERSONA_REGISTRY.csv` | Dimension CSV (canonical) | PMO | Live; `last_review` per row |
| `docs/references/hlk/compliance/dimensions/CHANNEL_TOUCHPOINT_REGISTRY.csv` | Dimension CSV (canonical) | PMO + System Owner | Live |
| `docs/references/hlk/compliance/dimensions/SOURCING_REGISTER.csv` | Dimension CSV (canonical) | PMO + Business Controller | Live; updated each engagement |

## New canonical assets (templates + touchpoint kit)

| Path | Class | Owner | Lifecycle |
|:-----|:------|:------|:----------|
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_en.md` | Template (canonical) | PMO + Brand Manager | Updated when SOP-HLK_LOCALISATION evolves |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_es.md` | Template (locale-derived) | Same | Mirrors EN structure |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/sourcing-briefs/TEMPLATE_OUTBOUND_BRIEF_fr.md` | Template (locale-derived, stub-grade per FR) | Same | First exercise of FR variant |
| `docs/references/hlk/v3.0/_assets/touchpoint-kit/<persona_id>/<channel_id>/intro_message_<lang>.md` | Touchpoint asset (canonical) | PMO + Brand Manager | Updated when persona / channel / brand voice evolves |
| `docs/references/hlk/v3.0/_assets/touchpoint-kit/<persona_id>/<channel_id>/intro_pack_<lang>.md` | Same | Same | Same |
| `docs/references/hlk/v3.0/_assets/touchpoint-kit/<persona_id>/<channel_id>/followup_<lang>.md` | Same | Same | Same |

## Modified canonical assets (cross-board impact)

| Path | Change | Drift risk |
|:-----|:-------|:-----------|
| `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` | +3 columns (`distance_band`, `bridge_via`, `distance_assessed_date`); backfill 6 rows | **Medium** — only schema bump on a pre-existing canonical CSV in this initiative. Validator + migration + render script all updated in same PR. |
| `akos/hlk_goipoi_csv.py` | +3 fields with enum + FK contract | Low (additive) |
| `scripts/validate_goipoi_register.py` | +4 invariants (enum, FK self-resolution, non-null when N≠N1, not-self) | Low |
| `scripts/sync_compliance_mirrors_from_csv.py` | `--goipoi-register-only` emit gains 3 columns | Low |
| `scripts/render_pmo_hub.py` | Auto-render gains a `distance` column; sha256 in END_AUTOGEN updates | Low — autogen is deterministic |
| `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md` | Auto-render output diff (new column) | Auto |
| `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` | New §4.X distance-assessment subsection; quarterly cadence aligned with §6 | Low (additive) |
| `docs/references/hlk/compliance/dimensions/TOPIC_REGISTRY.csv` | +4 rows | Low |

## Re-rendered (deterministic from canonicals)

| Path | Source | Trigger |
|:-----|:-------|:--------|
| `artifacts/sql/i31_persona_channel_sourcing_topic_upsert.sql` | `scripts/sync_compliance_mirrors_from_csv.py --topic-registry-only --persona-registry-only --channel-touchpoint-registry-only --sourcing-register-only` | Operator applies via `npx supabase db push` or MCP `execute_sql` |
| `supabase/migrations/<ts>_i31_goipoi_distance_extension.sql` | Hand-authored DDL ALTER + UPDATE backfill | Operator applies via `npx supabase db push` |

## Reference-only

| Path | Purpose |
|:-----|:--------|
| `docs/wip/planning/31-holistik-ops-discovery/reports/uat-i31-holistik-ops-discovery-2026-04-30.md` | UAT closure report (P7) |

## Out of scope

- Figma file at `https://www.figma.com/design/yiPav7BLxUulNFrrsoKJqW` — no deck content changes, no Figma backport
- Existing 11 TODO[OPERATOR-x] markers from I29 + I30 — founder-decision territory, untouched
- Naming partners (Websitz, Rushly) — keeps I28 D-IH-28 rule
- Productizing Holistik Ops as a Holistika-external offering — later, after founder review of the meta-doc
