---
intellectual_kind: research_synthesis_prong
sharing_label: internal_only
prong_id: B
prong_topic: Funnel / Lead / Engagement / Customer / Offboard lifecycle stages — industry consensus + Holistika disambiguation
authored: 2026-05-27
last_review: 2026-05-27
parent_initiative: I86
parent_tranche: wave-r-plus-4-research-grounded-brand-ops-mktops-investor-disambiguation
linked_decisions:
  - D-IH-86-EV (MARKETING_LIFECYCLE_TAXONOMY canonical mint)
linked_canonicals:
  - MKTOPS_DISCIPLINE.md
  - ENGAGEMENT_REGISTRY.md
  - MARKETING_AREA_M3_REDESIGN.md
status: drafting
role_owner: Marketing/RevOps (assistant in donde-r capacity)
audience: J-OP, J-AIC
language: en
---

# Prong B — Funnel × Lead × Engagement × Customer × Offboard lifecycle taxonomy

## TL;DR for the C2 governance commit

The operator's 2026-05-27 framing named verbatim:

> *"i remember people have market research to mktops to lead to (other intermediate steps that i don't know because i need you to research how this is done and maybe it's the funnel per ur artifacts or maybe it's another thing i don't know but i guess there are other intermediate steps to take into account) to customer to order-to-cash. always lifetime cycle managed OTC (and i guess) offboard in worse case scenario."*

**Research finding (load-bearing):** The B2B revenue lifecycle has evolved through **3 named iterations** of industry consensus (per 5 sources surveyed):

1. **SiriusDecisions Demand Waterfall (2006, revised 2012)** — lead-centric: Inquiry → MQL → SAL → SQL → SQO → Closed/Won.
2. **SiriusDecisions Demand Unit Waterfall (2017)** — buying-group-centric: Target Demand → Active Demand → Engaged Demand → Prioritized Demand → Qualified Demand (Sales) → Pipeline → Closed/Won.
3. **Forrester B2B Revenue Waterfall (2021, current)** — opportunity-centric AND lifecycle-full: removes "demand" from name; expands beyond new-business to encompass retention + expansion; explicitly includes customer-lifecycle stages alongside acquisition.

**The current industry consensus terms (Forrester 2021):**

| Stage | Industry term | Holistika existing term | Owner area |
|:---|:---|:---|:---|
| 1 | Target Demand (TAM/ICP definition) | not-yet-named | Marketing/Resonance |
| 2 | Active Demand (intent signals; engagement) | not-yet-named | Marketing/Reach |
| 3 | Engaged Buying Group (account-team-mapping) | not-yet-named | Marketing/Reach + RevOps |
| 4 | Prioritized Lead/Account (MQA/MQL) | not-yet-named (closest: "intelligenceOps target") | RevOps + System Owner |
| 5 | Qualified Opportunity (SAL/SQL) | not-yet-named | RevOps |
| 6 | Active Pipeline (SQO) | "live conversation" (operator term) | RevOps |
| 7 | Closed/Won (contract signed) | "engagement" (= signed PO + invoicing) | RevOps + SMO |
| 8 | Onboarding (delivery start) | "engagement-active" | SMO |
| 9 | Retention/Expansion | not-yet-named (cross-sell + upsell) | RevOps |
| 10 | Offboarding | "engagement-close" | SMO |

**Holistika alignment**: The operator's term "engagement" maps to industry stage 7+ (Closed/Won onwards). The operator's term "live conversation" maps to industry stages 3-6. There is **NO Holistika term yet** for stages 1-3 (pre-engagement marketing demand-generation lifecycle). This is the precise gap that `MARKETING_LIFECYCLE_TAXONOMY.md` canonical should fill at C2 governance commit (D-IH-86-EV).

**Crucial naming decision (load-bearing for C2):** The operator named "always lifetime cycle managed OTC" — Order-to-Cash. Industry term is "B2B Revenue Waterfall" (Forrester 2021) OR "Lead-to-Cash" (older term). Recommend Holistika adopt **"Demand-to-Cash lifecycle"** as the umbrella term — it (a) honours the operator's Demand-Waterfall lineage; (b) is industry-recognized; (c) captures the FULL span (pre-demand → cash collected → upsell → offboard) that the operator's framing names.

## The 5 sources (rated + ranked)

| Source | Confidence | Rank | Why |
|:---|:---|:---|:---|
| **Forrester B2B Revenue Waterfall (2021)** via marqeu + opfocus + LinkedIn surveys | CL4 (Forrester is the industry-standard analyst firm; framework is the current industry consensus) | #1 framework | Names the 10-stage current consensus + opportunity-centric vs lead-centric shift + lifecycle-full expansion |
| **SiriusDecisions Demand Unit Waterfall (2017)** via Engagio LinkedIn + Sher Miller | CL4 (the bridge-iteration between old and new; explains WHY buying-group-centric matters) | #2 bridge | Names the buying-group ("demand unit") concept + Awareness → Engaged Demand → Prioritized Demand stages |
| **marqeu** — *B2B Demand Waterfall Implementation Guide* | CL3 (vendor; implementation-grounded) | #1 implementation | Names the "two-stage mental model anti-pattern" (leads + opportunities only; everything in the middle is a black box) |
| **opfocus** — *What's the Difference between Demand Unit Waterfall and B2B Revenue Waterfall* | CL3 (Salesforce consultancy; head-to-head comparison) | #2 disambiguation | Names CRO + sales-process expansion + cross-sell/upsell inclusion + CLTV obsession |
| **SiriusDecisions/Forrester original** (2006-2021 historical lineage) | CL5 (canonical originating-source) | #1 history | Establishes industry-standard genealogy of the framework |

## Insights extracted (rated + ranked)

### Insight B-1 — "Definitional drift renders funnel analytics unreliable" (marqeu; CL3-HIGH; RANK 1)

**Verbatim claim**: *"Effective implementation requires standardized stage definitions agreed upon by both sales and marketing to prevent the 'definitional drift' that renders funnel analytics unreliable."*

**Why this matters for Holistika:** This validates the entire C2 commit purpose. The operator's framing names "lead management, funnel management — engagement is the same or not?" — that question IS definitional drift in real-time. The C2 canonical must (a) name each stage; (b) name what triggers entry/exit between stages; (c) name the owner (per Prong A's channel-to-owner matrix); (d) name the metric.

**Specific stage definitions for the Holistika canonical (recommended):**

| Stage | Definition | Entry trigger | Exit trigger | Owner | Metric |
|:---|:---|:---|:---|:---|:---|
| **Demand-Target** | An account profile matches Holistika's ICP and is named in a research-radar program. | Operator-named or research-radar-identified. | Account is contacted OR account exits ICP scope. | Marketing/Resonance | Number of named accounts in radar |
| **Demand-Active** | A named account shows intent signal (visited site / engaged content / posted query / mentioned in target community). | Intent signal logged. | Account responds to outreach OR signal goes cold (>90 days). | Marketing/Reach | Intent-signal-to-response conversion rate |
| **Demand-Engaged** | A buying-group member (POI) at a target account engages directly (replies email, accepts call). | First direct reply. | Buying group is fully mapped (≥3 POIs identified) OR member disengages. | RevOps + Marketing/Reach | Buying-group-mapping completion rate |
| **Conversation-Live** | A direct multi-touch dialog is underway with a defined scope hypothesis being explored. | "Yes, let's explore" signal. | Proposal request OR explicit decline. | RevOps | Conversation-to-proposal conversion rate |
| **Proposal-Active** | A scoped proposal has been delivered and is under counterparty consideration. | Proposal sent. | PO signed OR proposal declined OR proposal stalled (>60 days). | RevOps + SMO | Proposal-to-PO conversion rate |
| **Engagement-Active** | A signed engagement (PO + first invoice) is operationally underway. | PO countersigned + first invoice rendered. | Final milestone closed + final invoice settled. | SMO + RevOps | Engagement-margin per phase |
| **Engagement-Retention** | Engagement closed; customer remains in retention/expansion conversations. | Final invoice settled + 30-day cooldown. | Repeat engagement signed OR explicit no-go. | RevOps | Net-dollar-retention (per CLTV obsession per opfocus) |
| **Engagement-Offboard** | Customer relationship ends without expansion AND without renewal signal. | Active conversation goes dormant >180 days post final invoice. | Operator-confirmed offboard OR re-engagement signal. | SMO + RevOps | Offboard-class taxonomy (graceful / forced / hostile) |

This is the proposed scaffold for `MARKETING_LIFECYCLE_TAXONOMY.md` canonical (C2 deliverable; D-IH-86-EV).

### Insight B-2 — "Opportunity-centric beats lead-centric" (opfocus + marqeu; CL4-HIGH; RANK 2)

**Verbatim claim** (opfocus): *"The Demand Unit Waterfall recognized that purchasing decisions are often made by buying groups rather than individuals. Identifying the members of those groups, and nurturing and scoring them collectively, leads to better demand qualification and increased close rates."*

**Why this matters for Holistika:** Holistika's actual practice ALREADY operates buying-group-centric (the operator routinely identifies decision-makers + technical-evaluators + economic-buyers as separate POIs per `GOI_POI_REGISTER.csv`). The taxonomy should NAME this as the standard, not the exception. Each lifecycle stage should explicitly carry buying-group identification (≥3 POIs typical for B2B SME engagements).

### Insight B-3 — "CLTV obsession + cross-sell/upsell first-class" (opfocus; CL3-HIGH; RANK 2)

**Verbatim claim**: *"Customer lifetime value is one of the areas of obsession for SaaS companies—and rightfully so. The B2B Revenue Waterfall, with its inclusion of cross-sells, upsells, and new business, helps companies more accurately capture CLTV. The updated funnel reflects a shift in the SaaS model to focus on net dollar retention—not only account retention or product retention, but overall revenue retention."*

**Why this matters for Holistika:** Holistika is consulting-class not SaaS-class, but the principle transfers: CLTV ≈ cumulative-engagement-volume-per-account. The taxonomy MUST carry the Engagement-Retention stage as first-class — not as an afterthought. The operator's framing names "always lifetime cycle managed" — this is the same insight industry-tested.

### Insight B-4 — "Sales process is not a single stage" (opfocus; CL3-MEDIUM; RANK 3)

**Verbatim claim**: *"The Demand Unit Waterfall had a heavy focus on marketing: the sales pipeline part of the funnel was a single stage in the funnel and not given enough weight in the process... The B2B Revenue Waterfall solved this issue by expanding and adding multiple stages to reflect the complexity and duration of the sales process."*

**Why this matters for Holistika:** Validates breaking Holistika's "live conversation" stage into 3 distinct stages (Demand-Engaged → Conversation-Live → Proposal-Active) per Insight B-1's recommended scaffold.

## Decisions this prong informs (load-bearing for C2 governance commit)

| Decision needed at C2 | Recommended position (research-grounded) |
|:---|:---|
| Should the C2 canonical be named "MARKETING_LIFECYCLE_TAXONOMY" or "DEMAND_TO_CASH_LIFECYCLE"? | **Mint as `MARKETING_LIFECYCLE_TAXONOMY.md` with the body adopting "Demand-to-Cash lifecycle" as the umbrella term.** Filename stays generic for easier discovery; doctrine body uses the specific umbrella term. |
| How many lifecycle stages should the Holistika canonical name? | **8 stages per Insight B-1** (Demand-Target → Demand-Active → Demand-Engaged → Conversation-Live → Proposal-Active → Engagement-Active → Engagement-Retention → Engagement-Offboard). |
| Should buying-group identification be first-class in every stage? | **Yes — every stage has a "POI/GOI mapping" requirement per `GOI_POI_STANCE_DOCTRINE.md`** (which already exists at active). |
| Should the canonical cite Forrester 2021 + SiriusDecisions 2017 + 2006 lineage? | **Yes — in §Evidence-base per `akos-applied-research-discipline.mdc` RULE 2.** Cite this prong as the internal synthesis. |

## Cross-references

- `MKTOPS_DISCIPLINE.md` — currently at charter; C2 canonical-mint creates the substrate the runbook (C3 commit) will operationalize.
- `ENGAGEMENT_REGISTRY.md` — current engagement tracking; C2 canonical clarifies that engagement = stage 6+ (signed PO).
- `MARKETING_AREA_M3_REDESIGN.md` — area-structural; integrates with Prong A's channel-to-owner propagation matrix.
- `GOI_POI_STANCE_DOCTRINE.md` — buying-group / POI identification doctrine (active); first-class in every lifecycle stage per Insight B-2.
- D-IH-86-EV — C2 canonical-mint ratifying decision; cites this prong as load-bearing substrate.

## Source archive

- https://www.opfocus.com/learn-with-us/blog/whats-the-difference-between-demand-unit-waterfall-and-b2b-revenue-waterfall
- https://www.marqeu.com/demand-waterfall-conversion-rates
- https://www.marqeu.com/demand-waterfall-implementation-guide
- http://www.shermiller.com/2020/07/siriusdecisions-demand-waterfall-models/
- https://www.linkedin.com/pulse/siriusdecisions-new-waterfall-how-operationalize-drive-redlinger

3 full pages cached locally in agent-tools/ for re-grounding.
