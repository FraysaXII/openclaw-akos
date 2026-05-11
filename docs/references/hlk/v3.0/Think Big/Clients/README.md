---
language: en
status: active
role_owner: PMO
area: PMO
entity: Holistika Research SL
last_review: 2026-05-10
---

# Think Big — Clients

This is the canonical home for client-engagement documentation that lives in the vault (and Drive mirror) rather than in a code repository. Each engagement gets its own folder under this directory, named with an ISO-prefixed slug that encodes the start year and a short identifier.

## Naming convention

```
<YYYY>-<short-slug>/
```

Examples:

- `2026-suez-webuy/` — SUEZ WeBuy procure-to-pay automation engagement, started 2026
- `2026-asesoria-hosteleria/` — Asesoría Hostelería (placeholder for P13.4 placement decision)

The slug is **lowercased**, **hyphen-separated**, and **redaction-safe** (no surnames, no client confidential identifiers, no internal codenames).

## Per-engagement shape (minimum-viable)

Each engagement folder has the following sub-folders:

| Folder | Purpose | Audience |
|:---|:---|:---|
| `00-internal/` | Operator-only companions: objection banks, counterparty briefs, checkpoints, internal review notes | operator + agent only |
| `01-operator-pack/` | Operator-and-collaborator pack: proposal, deck, CDC feasibility shape, discovery questionnaire, READMEs | operator + collaborator (named partner / guest) |
| `02-customer-pack/` | Customer-facing pack: customer-segmented proposal, deck, tarification | customer (with optional named host / guest header) |
| `_external_marks/` | Guest / partner brand assets (logos, color palettes, typography references) used in co-branded surfaces | render pipeline |
| `_archive/` | Dated snapshots of prior versions (one sub-folder per archive event, named `<YYYY-MM-DD>-<reason>/`) | rollback only |
| `_exports/` | Rendered PDFs (generated from markdown, deterministic; not committed to git per `.gitignore`) | distribution |

The `_engagement-template/` skeleton (P13.3) extends this minimum-viable shape with optional sub-folders for full-scope engagements (`05_partner_bridge/`, `06_research_intel_feeds/`, `07_tech_touchpoints/`). The minimum-viable shape is a strict subset; expansion does not require restructuring.

## Cross-references

- [`../README.md`](../README.md) — Think Big vault purpose and folder conventions
- [`../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — PMO hub indexing all active engagements
- `WORKSPACE_BLUEPRINT_HOLISTIKA.md` (P13.1) — engagement-types matrix and full folder-shape spec
- `_engagement-template/` (P13.3) — reusable template skeleton for new engagements

## What does NOT live here

- **Code repositories**, including platform products (KiRBe, MADEIRA stack, ENVOY) and client-delivery code repos. Those are indexed under `Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md`.
- **Internal admin documents** (founder bio, brand canonicals, operational SOPs). Those live under `Admin/O5-1/`.
- **Cross-engagement shared assets** (proposal templates, sequence templates, press kit, email signatures). Those live under `_assets/advops/shared/`.

## Active engagements

| Slug | Start | Status | Customer | Partner / guest | Notes |
|:---|:---|:---|:---|:---|:---|
| `2026-suez-webuy/` | 2026-05 | active (proposal stage) | SUEZ (procurement) | EFA Académie | Co-branded; volume framing 20-50 demands/day; litige reframe per D-12-15 |

End.
