---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-integration-spec
program_id: shared
plane: ops
authority: PMO + System Owner
last_review: 2026-04-30
audience: ERP team engineering
---

# 5-axis integration spec for ERP screens (one-pager)

This is the prescriptive guide for how ERP screens consume the new I31 / I32 governance mirrors. The 6-axis Holistik Ops doctrine (HOLISTIK_OPS_DISCOVERY.md v2 in AKOS) names 6 axes: Persona × Channel × Distance × Language × Artifact-class × Topic. ERP screens consume axes 1, 2, 3, and 4 most — axes 5 and 6 are agent-side concerns.

## Pattern: persona-aware screen filter

Every ERP screen that shows a list of humans (contacts, leads, vendors, advisers) gains an optional persona filter sourced from `compliance.persona_registry_mirror`.

```typescript
// Server component example (Next.js App Router; per ERP architecture rule)
const personas = await supabase
  .from('persona_registry_mirror')   // RLS read-only
  .select('persona_id, name, direction, typical_distance_band')
  .order('name');
// Render as <Select> filter; default unset.
```

## Pattern: channel-tagged inbound view

Every ERP inbound view (lead intake, contact form responses, partner referrals, ad campaign submissions) joins `compliance.channel_touchpoint_registry_mirror` to display the channel name + response SLA + owner role per inbound row.

```typescript
const inbound = await supabase.rpc('inbound_with_channel_metadata', { since: '7 days' });
// RPC joins holistika_ops.lead_intake to channel_touchpoint_registry_mirror by channel_id.
```

The RPC is operator-defined; ERP team proposes the SQL via the `operator-sql-gate.md` workflow (see sibling `03-operator-sql-gate-pointer.md`).

## Pattern: distance-band column on every "humans list" screen

Wherever ERP shows a contact / adviser / vendor row, the `current_distance_band` from `compliance.goipoi_register_mirror` (named individuals) or `compliance.sourcing_register_mirror` (vendors) is one of the columns. Sortable. Filterable.

```typescript
const contacts = await supabase
  .from('goipoi_register_mirror')
  .select('ref_id, display_name, class, distance_band, bridge_via, distance_assessed_date')
  .order('distance_band', { ascending: true });
// 6 rows today; dashboard renders as a sortable table.
```

## Pattern: locale-aware UI + audience-canonical exception

Per `SOP-HLK_LOCALISATION_001.md` (relocated to Marketing/Brand in I32 P7), every UI string is i18n-keyed and supports `en | es | fr`. Audience-canonical exception: ERP screens whose specific use case is single-locale (e.g., a Spanish founder-incorporation dashboard) ship in the audience language only and document the deviation in the screen's frontmatter.

ERP already has solid i18n infrastructure per its architecture rule; this just formalises the rule in the cross-repo contract.

## Pattern: do NOT denormalise mirror data into local SSOT

Today's HLK-ERP `data-ssot.mdc` rule says "Centralize in `lib/*`". For HLK doctrine **this rule does not apply** — see Q10 supersession in the architecture audit. `lib/types.ts` and `lib/safe-number.ts` keep their non-HLK utility role; HLK org / process / persona / channel / etc. read from mirrors, not from `lib/`.

Concretely: `lib/supabase-types.ts` should mirror the canonical schema (auto-regenerated; treat as snapshot per AKOS PRECEDENCE.md "Mirrored / derived assets" §`supabase.ts` typings); ERP screens query the views, not the local types as SSOT.

## Pattern: chart wrapper enforcement (preserved)

The existing `chart-wrapper-enforcement` rule in HLK-ERP's architecture rule (`use ChartContainer/Tooltip/Legend from components/ui/chart.tsx`) is preserved. AKOS does not override visual or interaction conventions.

## Cross-references

- 6-axis Holistik Ops doctrine: AKOS `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md`
- Mirror schema map: `01-mirror-schema-map.md` (sibling file)
- Operator SQL gate: `03-operator-sql-gate-pointer.md` (sibling file)
- Localisation policy: `04-localisation-policy-pointer.md` (sibling file)
