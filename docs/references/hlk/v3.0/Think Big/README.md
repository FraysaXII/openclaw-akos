---
language: en
---

# Think Big — entity scope (Holistika)

**Governance:** [PRECEDENCE.md](../../compliance/PRECEDENCE.md), [v3.0/index.md](../index.md)

---

## Purpose

Think Big is the vault home for **client and program documentation that is not a GitHub repository root**: statements of work, commercials, engagement memos, deliverable PDFs/decks, and other artifacts where the **canonical file** lives in the vault (or Drive mirror), not in a separate code repo.

**Codebases** — including platform products (KiRBe, MADEIRA stack) and client-delivery repositories — are indexed under **Envoy Tech Lab**:

- [Envoy Tech Lab/Repositories/REPOSITORIES_REGISTRY.md](../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md)
- [Envoy Tech Lab/Repositories/README.md](../Envoy%20Tech%20Lab/Repositories/README.md)

Use **topic knowledge indexes** (PMO or owning role) to tie Think Big folders to registry rows and to Admin-side SOPs or case docs.

---

## Folder conventions

Think Big has **two physical roots** corresponding to the two engagement directions encoded in [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md):

| Folder | Direction | Use |
|--------|-----------|-----|
| `Clients/` | Outbound — Holistika provides | Customer, partner, product, and **internal** engagements. External slugs use `<YYYY>-<slug>/`; internal-capacity engagements (trainee cohorts, internal research sprints, related-party advisory) use the reserved prefix `<YYYY>-internal-<slug>/` with the same folder template. |
| `Advisers/` | Inbound — Holistika contracts | Engagements where Holistika is the customer of external advisers (legal, fiscal, banking, certification). Folder shape is the inbound template (`00-internal/` + `01-our-pack/` + `02-adviser-pack/` + `_archive/` + `_exports/`; no `_external_marks/`). |

`Think Big/Projects/` was retired per D-W13-I (P13.5, 2026-05-11): everything at Think Big is a project-shaped engagement; the previous `Projects/` placeholder is replaced by the `Clients/<YYYY>-internal-<slug>/` convention for internal programs.

When a deliverable is **only** in GitHub, do not duplicate the tree here: register the repo in [`REPOSITORIES_REGISTRY.md`](../Envoy%20Tech%20Lab/Repositories/REPOSITORIES_REGISTRY.md) and link from a topic index.

---

## Example cross-links

- Workspace blueprint canonical: [WORKSPACE_BLUEPRINT_HOLISTIKA.md](../Admin/O5-1/Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) — engagement-types matrix, per-root folder shape, sub-mark functional split, four-channel persistence doctrine
- PMO hub topic: [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md)
- Topic template: [TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md](../Admin/O5-1/People/Compliance/TOPIC_KNOWLEDGE_INDEX_TEMPLATE.md)
