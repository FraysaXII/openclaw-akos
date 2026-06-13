---
intellectual_kind: research_prong
prong: BL-LEGAL
topic_cluster: legal-ip-data
parent_pack: infonomics-holistika-data-economics-2026-06-12
authored: 2026-06-13
status: active
language: en
linked_decisions:
  - D-INF-ECON
---

# Prong BL-LEGAL — Legal consumer

> **Baseline prong:** `BL-LEGAL` (O5-1 Legal)  
> **Ledger coverage:** 30 rows (15 CORPINT + 15 OSINT); **1 skeptic** voice  
> **Downstream decision:** **D-INF-ECON** (P5 govern)  
> **Coverage note:** thinnest OSINT band among P4 tranche-1 prongs (15 external rows); infonomics-core cluster **empty** — legal economics inferred from IP/access templates + compliance OSINT.

## Narrative findings

### 1. Legal templates define the economic boundary of data sharing

Holistika's **DPA** (`SRC-INF-INT-165`), **MSA** (`SRC-INF-INT-166`), **NDA** (`SRC-INF-INT-167`), and **SOW** (`SRC-INF-INT-168`) templates are the **price list of permitted information flows** — what can be copied, to whom, for how long, and under which liability cap. **SOP-LEGAL_IP_REGISTER_MAINTENANCE_001** (`SRC-INF-INT-163`) and **trademark monitoring SOP** (`SRC-INF-INT-164`) treat brand and methodology IP as defendable assets. **Methodology IP minting path** (`SRC-INF-INT-138`) links research outputs to ownership before they become billable.

Without these boundaries, Infonomics valuation is fiction — Laney's "measure" step (`SRC-INF-EXT-477`) assumes definable property rights.

### 2. Trademark and entity structure anchor brand-data value

**Brand Hierarchy and Trademark Scope** (`SRC-INF-INT-064`), **Trademark Filing Strategy** (`SRC-INF-INT-140`), and external Nice Classification / EUIPO-WIPO tools (`SRC-INF-EXT-230`, `SRC-INF-EXT-226`, `SRC-INF-EXT-227`) show that **marketing data and brand surfaces** carry registrable economic value separate from raw CRM rows. **Founder entity formation memo** (`SRC-INF-INT-065`) and **related-entities fact pattern** (`SRC-INF-INT-139`) affect which entity holds data assets on balance sheet.

### 3. GDPR and SOX set the penalty floor for mis-valuation

ICO GDPR legal-basis guide (`SRC-INF-EXT-241`) and SOX overview (`SRC-INF-EXT-240`) price **non-compliance** — the downside case for treating personal or financial data as low-cost inventory. Holistika access levels (Compliance prong) must stay aligned with DPA clauses (`SRC-INF-INT-165`) before any external data product monetization.

### 4. Legal ops technology surveys show tooling cost — skeptic warns hype

Legal ops technology survey (`SRC-INF-EXT-245`) documents CLM and matter-management spend; CLM Gartner note (`SRC-INF-EXT-242`) and trademark clearance limits (`SRC-INF-EXT-231`) caution that **automation does not eliminate lawyer hours**. **Legal tech hype cycle skeptic** (`SRC-INF-EXT-495`) argues vendors oversell ROI on "AI for contracts" — Holistika should not justify Infonomics tooling with legal-tech marketing curves alone.

### 5. External counsel handoff packages information as deliverable

**External Counsel Handoff Package** (`SRC-INF-INT-184`) and **SOP-LEGAL_TEMPLATE_FIRE_001** (`SRC-INF-INT-063`) treat legal work product as **metered packages** — a precedent for pricing research packs and compliance mirror evidence bundles similarly.

## PESTEL — six viewpoints

| Letter | Viewpoint | Finding (cite `SRC-*`) |
|:---|:---|:---|
| **P** | Political | Trademark jurisdictions (EUIPO `SRC-INF-EXT-226`, INPI `SRC-INF-EXT-229`) and entity formation (`SRC-INF-INT-065`) follow political trade and tax treaties — data residency choices have legal-political cost. |
| **E** | Economic | CLM and legal ops surveys (`SRC-INF-EXT-245`, `SRC-INF-EXT-242`) show legal spend as **fixed overhead** on every data deal; mis-priced DPA scope (`SRC-INF-INT-165`) converts information revenue into liability. |
| **S** | Social | Ethics boundary doc under Compliance (`SRC-INF-INT-025`, cross-prong) sets social license above legal minimum; Open Data Institute responsible use (`SRC-INF-EXT-486`, ethics prong) parallels GDPR spirit (`SRC-INF-EXT-241`). |
| **T** | Technological | Legal tech hype (`SRC-INF-EXT-495`) warns that AI contract review does not replace register maintenance (`SRC-INF-INT-163`); tooling TCO must sit in Infonomics, not vanish in "efficiency" claims. |
| **E** | Environmental | Low direct environmental force; indirect via data-center clauses in MSAs (`SRC-INF-INT-166`) if clients demand green hosting attestations. |
| **L** | Legal | Core prong force: GDPR (`SRC-INF-EXT-241`), SOX (`SRC-INF-EXT-240`), IP registers (`SRC-INF-INT-163`), and template fire SOP (`SRC-INF-INT-063`) define **lawful monetization envelope** for information assets. |

## Porter — four forces + competition synthesis

| Force | Finding (cite `SRC-*`) |
|:---|:---|
| **Supplier power** | External counsel packages (`SRC-INF-INT-184`) and trademark agents (filing strategy `SRC-INF-INT-140`) set professional-services rates; CLM vendors (`SRC-INF-EXT-242`) lock contract metadata schemas. |
| **Buyer power** | Clients negotiate DPA/MSA terms (`SRC-INF-INT-165`, `SRC-INF-INT-166`); GDPR (`SRC-INF-EXT-241`) empowers data subjects to withdraw consent — buyers of Holistika insights inherit that power downstream. |
| **Threat of substitutes** | Template fire SOP (`SRC-INF-INT-063`) enables rapid substitute contracts; over-customized data deals substitute **legal risk** for **speed** if templates are bypassed. |
| **Threat of new entrants** | Legal-tech AI entrants (skeptic `SRC-INF-EXT-495`) promise cheaper contract review; entrants may underprice diligence if Holistika prices full governed trail. |
| **Competition synthesis** | Holistika competes on **defensible, template-governed information exchange** — not on avoiding legal cost. Economic advantage comes from reusing fired templates and IP registers so each new data product does not pay full greenfield legal cost. |

## Infonomics hook

**Economic levers for Legal:** IP register as asset catalog; DPA/MSA as transfer-pricing rules; trademark scope as brand-data valuation anchor; compliance penalty models (`SRC-INF-EXT-241`) as risk-adjusted discount rate; counsel handoff as unit-of-sale precedent.

**Holistika delta vs external Infonomics posture:** strong on **ownership definition** (templates, IP SOPs); weak on **quantified legal COGS per information product** and **risk-adjusted asset carrying value**. Skeptic (`SRC-INF-EXT-495`) limits legal-tech as valuation shortcut.

**Govern options (ranked):**

1. **Add `linked_legal_instruments` column to DATA_CONTRACT_REGISTRY** (Data prong) pointing to DPA/SOW template IDs (`SRC-INF-INT-165`, `SRC-INF-INT-168`) — couples economics to lawful basis without new Legal canonical. *(recommended)*
2. **Extend IP register with `economic_use_class` enum** (internal product / external license / defensive) per methodology mint path (`SRC-INF-INT-138`) — CSV gate on Legal.
3. **Legal-only narrative appendix in Infonomics discipline** — documents penalty floors; no register automation.
4. **Defer legal-economic columns until external counsel ratifies** — scheduled after P5 if operator wants counsel review; not dropped.

## Cross-references

- [`source-ledger-prong-ssot-2026-06-12.md`](source-ledger-prong-ssot-2026-06-12.md) · [`charter.md`](charter.md)
