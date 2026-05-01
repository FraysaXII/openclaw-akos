---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-changelog
program_id: shared
plane: ops
authority: Founder + System Owner
last_review: 2026-04-30
audience: ERP team engineering
---

# I31 + I32 highlights for the ERP team (jargon-audit clean)

This is a curated, jargon-audit-clean changelog of what AKOS shipped recently that materially affects the ERP team's read-side. Internal codenames stripped per `BRAND_JARGON_AUDIT.md`.

## Initiative 31 (closed 2026-04-30) — Holistik Ops Discovery

Holistika now operates a 5-axis system for human interactions: Persona × Channel × Distance × Language × Artifact-class. Every axis is backed by a governed CSV and a Postgres mirror table.

What's new for the ERP team:

- 16 persona archetypes available as a queryable dimension (previously implicit in operator memory)
- 10 channel touchpoints registered (LinkedIn DM, email, web form, Cal scheduling, etc.) with response SLA + owner role per channel
- Distance band (N1 / N2 / N3 / N4) on every named individual in the contact register; queryable as a sortable column
- Language declaration (`language: en | es | fr`) on every internal document
- 8 highest-leverage touchpoint kit cells seeded across persona × channel combinations

## Initiative 32 (closed today) — Holistik Ops Maturation

Initiative 31's substrate matures into a production-ready, multi-tenant, multi-agent platform. Three new governed dimensions: skill registry, touchpoint kit cell registry, policy register. Topic promoted to axis 6.

What's new for the ERP team:

- Skill registry — versioned skill bundles that agents invoke (5 seed skills covering all 5 documented agents); tenant-aware schema for future productisation
- Touchpoint kit cell registry — every (persona × channel × language) template file is now a queryable row; filesystem-vs-registry drift detected automatically
- Policy register — security and access policies as a queryable CSV (was paragraphs in 5+ separate documents); 14 seed rows covering schema-level posture, the quarterly key rotation cadence, and the brand-jargon redaction policy
- Cross-repo discipline — ERP is now formally tracked as one of three Holistika-tracked repositories with a 1-page contract that pins it to the canonical knowledge dimensions
- Topic axis 6 — every dimension row carries a topic linkage; routing flow now resolves topic explicitly instead of guessing

## What the ERP team needs to know in one paragraph

Read the new dimensions read-only via Supabase (mirror tables in the compliance schema; access-controlled to the service role). Display persona, channel, distance, and language wherever your ERP screens show humans or inbound. Adopt the language declaration on new internal documents. The new contract at the ERP repository root captures everything in one page; a small companion cursor rule keeps every cursor session aware of the AKOS canonical sources. Three things stay yours: Next.js patterns, theme tokens, the chart wrapper enforcement.

## Cross-references

- 6-axis Holistik Ops doctrine: AKOS `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md`
- Schema map (16 mirrors): `01-mirror-schema-map.md` (sibling file)
- Integration spec: `02-five-axis-integration-spec.md` (sibling file)
- Architecture audit (separate): `../erp-architecture-audit-2026-04-30.md`
