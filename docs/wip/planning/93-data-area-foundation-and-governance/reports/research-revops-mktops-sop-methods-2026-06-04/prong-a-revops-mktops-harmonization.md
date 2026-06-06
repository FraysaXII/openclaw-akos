---
intellectual_kind: research_prong_synthesis
parent_pack: research-revops-mktops-sop-methods-2026-06-04
prong: A
feeds_decision: RevOps org placement + MKTOPS naming harmonization
authored: 2026-06-04
sources: SRC-I93-RSM-001..005
---

# Prong A — RevOps vs MKTOPS vs MarTech harmonization

## Question

Are RevOps and MKTOPS duplicates? Should RevOps move from Operations to Marketing? How does Holistika nomenclature map to industry?

## Internal evidence (repo state)

| Construct | Type | Location | Function |
|:---|:---|:---|:---|
| **MKTOPS** | Quality Fabric **discipline** (7th specialty) | `MKTOPS_DISCIPLINE.md` | Campaign lifecycle quality MKT-01..07; compose_MKTOPS rule |
| **RevOps** | Operations **area charter** | `REVOPS_AREA_CHARTER.md` | Value-mapping spine; engagement templates; 8 adapter registries; QBR |
| **MarTech** | Implicit in adapter registries | CRM/EMAIL/ATTRIBUTION CSVs | Tooling layer — not a separate Holistika discipline name |

**Critical distinction already minted:** `MKTOPS_DISCIPLINE.md` §1 names Marketing/Reach **primary** and Operations/RevOps **co-owner**. The vault never equated the two — the operator's confusion is **naming collision** (both end in "Ops") not duplicate charters.

**RevOps charter boundary (SRC-I93-RSM-001):**

- RevOps **integrates** cross-area revenue data; does **not** own Marketing SSOT.
- RevOps **primary author** of DAMA alignment for adapter/integration posture (not all of DATA governance).
- RevOps sits under **Operations / COO** until CRO activates.

**MKTOPS scope (SRC-I93-RSM-002):**

- Outbound campaign artefacts: brief → creative → launch → measure.
- Enforces attribution trail (MKT-04) against `ATTRIBUTION_ADAPTER_REGISTRY.csv` owned under RevOps path.

## External evidence (industry)

Per SRC-I93-RSM-004..005:

| Industry term | Scope | Typical reports to |
|:---|:---|:---|
| **Marketing Operations (MOps)** | Marketing department execution, campaigns, martech stack | CMO |
| **Revenue Operations (RevOps)** | Full GTM lifecycle Marketing + Sales + CS integration | CRO / COO / CEO |
| **MarTech** | Tooling layer (not an org function) | Embedded in MOps + RevOps |

**Model gaining traction at growth stage (RevenueTools Model 2):** Unified RevOps leader with **embedded MOps specialist** — deep marketing execution inside a cross-functional RevOps umbrella.

**Failure mode (Landbase):** RevOps strategy without solid Marketing Ops **execution** foundations collapses — strategy on broken campaigns.

## Holistika fit assessment

| Option | Description | Pros | Cons |
|:---|:---|:---|:---|
| **A1 — Keep current split** | MKTOPS discipline (People/Marketing quality) + RevOps area (Operations integration) | Matches existing mint; charter boundaries clear; RevOps already owns adapter SSOT | Operator naming fatigue; "two Ops" sounds redundant |
| **A2 — Rename MKTOPS → MOps discipline** | Align external vocabulary; keep RevOps area | Easier operator communication | Large rename sweep; MKTOPS already wired in Quality Fabric |
| **A3 — Move RevOps area under Marketing** | Single GTM tree under CMO | Matches some MOps-central orgs | Breaks RevOps charter (Finance spine, COO reporting); Finance adapter ownership awkward |
| **A4 — Unified RevOps umbrella (Model 2)** | RevOps area absorbs **Marketing Ops execution** as embedded discipline; MKTOPS becomes **quality bar** RevOps enforces on Marketing output | Industry-aligned; clarifies "MKTOPS = quality, RevOps = spine" | Requires charter amend + decision register; not a DATA-only change |
| **A5 — RevOps coordination layer only** | MOps fully under Marketing; tiny RevOps owns cross-area data only | Minimal Ops headcount | Underpowers adapter registries already minted under RevOps |

## Recommended default (for master synthesis)

**Do not merge or relocate RevOps to Marketing without a People/Ops decision register row.**

**Clarify nomenclature instead:**

| Holistika name | Plain language | Industry alias |
|:---|:---|:---|
| **MKTOPS discipline** | Marketing campaign quality bar | MOps quality / campaign governance |
| **RevOps area** | Revenue integration spine | RevOps |
| **MarTech** | Adapter registries (CRM, email, attribution…) | Tooling — not a job title |

**Interim BI stewardship (until A4 ratified):** Marketing Analytics Manager + CMO chain = primary campaign/ads analytics consumer; RevOps Manager = attribution + revenue rollup consumer (Operations adapters).

## Open ratification

Operator must pick **A1, A2, A4, or A3** before P5c mints org-sensitive BI consumer `owner_role` rows tied to RevOps placement.
