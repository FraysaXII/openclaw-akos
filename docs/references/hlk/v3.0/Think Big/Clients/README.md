---
language: en
status: active
role_owner: PMO
area: PMO
entity: Holistika Research SL
last_review: 2026-05-10
---

# Think Big — Clients

This is the canonical home for **outbound** engagement documentation where Holistika provides — the engagement-types matrix in [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §3 maps customer (type 1), partner (type 2), product (type 3), and internal-capacity (type 5) engagements to this root. Inbound engagements where Holistika is the customer (type 4 — advisers) live under [`../Advisers/`](../Advisers/) instead.

Each engagement gets its own folder under this directory, named with an ISO-prefixed slug that encodes the start year and a short identifier.

## Naming convention

```
<YYYY>-<short-slug>/             external outbound (types 1 / 2 / 3)
<YYYY>-internal-<short-slug>/    internal capacity (type 5) — reserved prefix
```

Examples:

- `2026-suez-webuy/` — SUEZ WeBuy procure-to-pay automation (external customer + EFA partner)
- `2026-asesoria-hosteleria/` — Asesoría Hostelería (related-party SME; lands at P13.4)
- `2026-internal-trainee-cohort-01/` — hypothetical internal trainee cohort (illustrative)

The slug is **lowercased**, **hyphen-separated**, and **redaction-safe** (no surnames, no client confidential identifiers, no internal codenames). The `internal-` prefix is **reserved** for internal-capacity engagements per blueprint §3 (D-W13-I) — never use it for external engagements.

## Per-engagement shape (minimum-viable)

Each engagement folder has the following sub-folders:

| Folder | Purpose | Audience |
|:---|:---|:---|
| `00-internal/` | Operator-only companions: objection banks, counterparty briefs, checkpoints, internal review notes | operator + agent only |
| `01-operator-pack/` | Operator-and-collaborator pack: proposal, deck, CDC feasibility shape, discovery questionnaire, READMEs | operator + collaborator (named partner / guest) |
| `02-customer-pack/` | Customer-facing pack: customer-segmented proposal, deck, tarification | customer (with optional named host / guest header) |
| `_external_marks/` | Guest / partner brand assets (logos, color palettes, typography references) used in co-branded surfaces — usually empty for `internal-` slug engagements | render pipeline |
| `_archive/` | Dated snapshots of prior versions (one sub-folder per archive event, named `<YYYY-MM-DD>-<reason>/`) | rollback only |
| `_exports/` | Rendered branded PDFs (tracked per 2026-05-11 `.gitignore` policy reversal) + `render-manifest.json` audit trail | distribution to Drive readers |

For `<YYYY>-internal-<slug>/` engagements, the same skeleton applies with two interpretive shifts: `02-customer-pack/` becomes the **stakeholder / board / internal-review pack** (no external customer); `_external_marks/` is usually empty (no guest brand). Tooling parity is preserved — the renderer, manifest, and archive conventions are identical.

## Cross-references

- [`../README.md`](../README.md) — Think Big vault purpose and folder conventions
- [`../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement-types matrix, per-root folder shape, file-tracking policy
- [`../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) — PMO hub indexing all active engagements
- [`_engagement-template/`](_engagement-template/) — literal copy-target template for new outbound engagements (created in P13.3)
- [`../Advisers/`](../Advisers/) — inbound root for engagements where Holistika is the customer of external advisers (created in P13.5)

## What does NOT live here

- **Code repositories**, including platform products (KiRBe, MADEIRA stack, ENVOY) and client-delivery code repos. Those are indexed under `Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md`.
- **Internal admin documents** (founder bio, brand canonicals, operational SOPs). Those live under `Admin/O5-1/`.
- **Cross-engagement shared assets** (proposal templates, sequence templates, press kit, email signatures). Those live under `_assets/advops/shared/`.

## Active engagements

| Slug | Start | Status | Customer | Partner / guest | Notes |
|:---|:---|:---|:---|:---|:---|
| `2026-suez-webuy/` | 2026-05 | active (proposal stage) | SUEZ (procurement) | EFA Académie | Co-branded; volume framing 20-50 demands/day; litige reframe per D-12-15 |

End.
