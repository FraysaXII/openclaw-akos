---
intellectual_kind: capability_collapse_map
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L2 — Capability de-densify (R2-01)
area: Marketing
authored: 2026-06-08
status: proposed
related_decisions:
  - D-IH-95-H   # keep-separate + de-densify, area-by-area, organic count
  - D-IH-82-P   # CAPABILITY_REGISTRY seed mint (the 1:1 process-shadow source)
language: en
audience: J-OP;J-AIC
register: internal
control_confidence_level: Euclid
note: >
  Proposed de-densified capability map for the Marketing area (area in
  ('MKT','Marketing') = 117 process-shadow rows). Applies the 6-step collapse
  method from l2-capability-densify-findings. This is a PROPOSAL: the one-time
  rewrite of CAPABILITY_REGISTRY is a gated canonical-CSV change requiring
  operator approval (per akos-baseline-governance.mdc). No canonical CSV is
  modified by this doc.
---

# L2 collapse map — Marketing area (117 process-shadows → 11 stable capabilities)

> **One-line result:** The 117 Marketing rows are a 1:1 shadow of `process_list`
> (seeded per D-IH-82-P), heavily inflated by ~60 bilingual brand to-dos and
> ~14 web-build tasks. They collapse to **11 stable, bearer-agnostic, outcome-named
> capabilities** under one Level-1 domain (**Go-to-Market & Brand**), plus **3 evictions**
> (tools/code-symbols that are not capabilities) and **2 rows rehomed** to other
> areas' maps. Every one of the 117 rows is accounted for. **117 → 11.**

This is a Tier-1 Research-area WIP finding (correct home: `docs/wip/intelligence/`,
internal register permitted). It feeds the L2 lane (R2-01) of the I95 master-roadmap
and applies the method ratified in
[`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md).

## 0. What I inspected (so this is falsifiable)

| Evidence | What it told me |
|:---|:---|
| 117 filtered `CAPABILITY_REGISTRY.csv` rows (`area in ('MKT','Marketing')`) | Pure process-shadow: `capability_id` = `CAP-`+uppercased `process` id; `capability_name` = process name verbatim; one `originating_process_id` each. Inflation sources: **49** `gtm_brand_dtp_1..49` Spanish/English brand to-dos + **11** `gtm_cl_*` hash-ID Spanish brand-channel tasks + **~14** web-build tasks tagged MKT. |
| `role_owner` column | Marketing's sub-area managers (**Brand & Narrative**, **Reach**, **Resonance**, **Account Management**, **PR**, **Experimentation**, **Marketing Analytics**) and **CMO** pre-cluster the rows — they are a ready-made signal for the L2 capability boundaries. |
| `lifecycle_status` | 14 rows are `active` (the TBI brand-governance set + 2 Reach GTM rows + comms-methodology + founder-bio + proposal + RevOps template); the rest `planned`. |
| `COMPONENT_PRIMITIVE_REGISTRY.csv` (the named eviction target) | **Schema mismatch finding (§3):** this registry holds **deliverable render-primitives** (`CP-COVER-PAGE`, `CP-HOOK`, `CP-CTA`, `CP-SLIDE-HERO` …), NOT software tools / code symbols. Marketing's non-capabilities (Mailchimp, Calendly, a MADEIRA API symbol) do **not** fit its schema and must evict elsewhere. |

---

## 1. Proposed capabilities (the stable WHAT)

All 11 sit under the single Level-1 domain **Go-to-Market & Brand** (per method §3.3
worked clusters #4 + #5). Names are nouns/gerunds, outcome-oriented, technology-neutral,
**bearer-agnostic** — the `CAP-ENV-*` / `CAP-THI-*` / `CAP-GTM-*` / `CAP-TBI-*` convention
variants of the same ability are merged into one capability (method §2.3 / Q3). IDs are
proposals; final IDs are set at the gated write.

| # | Proposed `capability_id` | Capability (stable WHAT) | One-line definition | Tier | Primary `role_owner` | Lifecycle | Rolls up |
|:--|:--|:--|:--|:--|:--|:--|:--:|
| C1 | `CAP-MKT-BRAND-NARRATIVE` | **Brand & Narrative Management** | The ability to own a coherent brand voice, message, manifesto, visual identity, founder narrative, and positioning story. | differentiating | Brand & Narrative Manager | active | 23 |
| C2 | `CAP-MKT-BRAND-GOVERNANCE` | **Brand Governance & Drift Control** | The ability to keep the brand canon true over time — canon maintenance, voice-drift triage, register/jargon/audience-tag audits, drift gates, brand-asset & domain stewardship. | differentiating | Brand & Narrative Manager | active | 12 |
| C3 | `CAP-MKT-EDITORIAL` | **Editorial & Content Production** | The ability to plan, produce, and route content across channels — editorial calendar, content templates, copy pipeline, newsletter, thought-leadership. | utility | Brand & Narrative Manager | planned | 26 |
| C4 | `CAP-MKT-CREATIVE-WEB` | **Creative, Web & Experience Design** | The ability to produce brand-grade creative + web/landing experiences — design, UX, multimedia, animation, landing pages. *(Engineering realization shared with Tech — see §4.)* | utility | Brand & Narrative Manager | planned | 14 |
| C5 | `CAP-MKT-DEMAND-GEN` | **Digital Demand Generation** | The ability to generate qualified demand — SEO, paid media, campaigns, funnel, audiences, events, social channels, partner-channel acquisition. | utility | Reach Manager | active | 20 |
| C6 | `CAP-MKT-ANALYTICS` | **Marketing Analytics & Attribution** | The ability to measure and attribute marketing performance — analytics, dashboards, attribution models, traffic research. | utility (enabler) | Marketing Analytics Manager | planned | 3 |
| C7 | `CAP-MKT-EXPERIMENTATION` | **Marketing Experimentation & Growth** | The ability to run a disciplined experiment loop — variant hypotheses, A/B testing, experiment registry, growth hacking. | differentiating | Experimentation Manager | planned | 3 |
| C8 | `CAP-MKT-PR-MEDIA` | **PR & Media Relations** | The ability to earn media — press releases, media pitches, journalist relations. | utility | PR Manager | planned | 1 |
| C9 | `CAP-MKT-RESONANCE` | **Community & Audience Resonance** | The ability to build and sustain community — ambassador program, resonance pulse, social-channel support. | differentiating | Resonance Manager | planned | 3 |
| C10 | `CAP-MKT-ACCOUNT-LIFECYCLE` | **Account & Lifecycle Marketing** | The ability to nurture known contacts across the lifecycle — account engagement cadence, email/scheduling-driven nurture. *(Tools evicted — see §3.)* | utility | Account Management Manager | planned | 1 |
| C11 | `CAP-MKT-PRODUCT-LAUNCH` | **Product & Launch Marketing** | The ability to bring products to market — ASO/app-store, battlecards/messaging matrix, launch content packs, sales-enablement collateral. | utility | Brand & Narrative Manager | planned | 6 |

**Domain note:** `CMO` is the area lead (accountable across all 11); the sub-area managers
above are the per-capability `role_owner`. The 60 Spanish brand to-dos (`gtm_brand_dtp_*`,
`gtm_cl_*`) are all currently owned by `CMO` and redistribute to the sub-area managers on collapse.

---

## 2. Rollup (every old row → its destination capability)

Old rows are listed by their `originating_process_id` suffix for brevity (the full
`capability_id` is `CAP-`+uppercased id). Each row appears **exactly once**. The
`process` rows are **not deleted** — they stay in `process_list.csv` and link to the
capability via the `realization` verb (TRP-006, N:N); only the duplicate *capability-shadow*
rows collapse.

| Capability | Rolls up these process-shadow rows (by id) | n |
|:--|:--|:--:|
| **C1 Brand & Narrative Management** | `thi_mkt_dtp_65` (Voice), `thi_mkt_dtp_66` (Message), `thi_mkt_dtp_293` (Communication methodology), `thi_marke_dtp_109` (Identify Personal Discourse); `gtm_cl_4b1030b0ba2d8f`, `gtm_cl_735c01230d82a4`, `gtm_cl_776150a9cd31ed`, `gtm_cl_d6af33605daf86`, `gtm_cl_f5b16f89f8a884` (brand messaging/discovery); `gtm_brand_dtp_1,3,5,6,7,8,9,10,11,12,14,15,47` (manifesto, message plan, corporate colors, brand/buyer/competitor research, voice spectrum, marca y mensajes); `tbi_ppl_prc_founder_bio_mtnce_001` (founder bio — cross-entity flag §4) | 23 |
| **C2 Brand Governance & Drift Control** | `tbi_mkt_prc_brand_canon_mtnce_001`, `tbi_mkt_prc_voice_drift_triage_001`, `tbi_mkt_prc_register_matrix_review_001`, `tbi_mkt_prc_jargon_audit_review_001`, `tbi_mkt_prc_template_registry_mtnce_001`, `tbi_mkt_prc_drift_gate_ops_001`, `tbi_mkt_prc_audience_tag_governance_001`, `tbi_mkt_prc_brand_domain_naming_001`; `gtm_brand_dtp_16,17,18,19` (access unify / device enrol / domain-payment continuity / access registry — brand-asset stewardship) | 12 |
| **C3 Editorial & Content Production** | `thi_mkt_dtp_67` (Editorial Calendar), `thi_mkt_dtp_59` (Newsletter), `thi_mkt_dtp_212` (Content Calendar & Template Library), `thi_mkt_dtp_291` (Editorial Calendar Coherence), `thi_mkt_dtp_304` (Storytelling Artifact Authoring), `thi_mkt_dtp_306` (Thought Leadership Editorial); `gtm_cl_f3265c7b665852`, `gtm_cl_f8c52621706eb9`; `gtm_brand_dtp_2,4,13,25,26,27,28,30,31,34,39,40,41,42,43,44,45,46` (copy, blog/channel messages, content-type lists, calendar template, copy process/format, content pipeline) | 26 |
| **C4 Creative, Web & Experience Design** | `thi_mkt_dtp_2` (Storytelling web), `thi_mkt_dtp_3` (Media Edition — tool names → substrate §4), `thi_mkt_dtp_4` (Layout), `thi_mkt_dtp_9` (Components UX design), `thi_mkt_dtp_40` (Layout marketing pod), `thi_mkt_dtp_60` (Animations), `thi_mkt_dtp_62` (Landing page design), `env_mkt_dtp_7` (High-Level Web design); `gtm_cl_a427f4b0dd3c83` (web codebase); `gtm_brand_dtp_20,21,22,23,24` (code-structure SOP, web categorization, codebase SOPs, Tech handoff/maintenance) | 14 |
| **C5 Digital Demand Generation** | `thi_mkt_dtp_20` (Buyer Funnel), `thi_mkt_dtp_39` (Audiences), `thi_mkt_dtp_41` (Events), `thi_mkt_dtp_42` (Campaign Management), `thi_mkt_dtp_50` (LinkedIn — channel §4), `thi_mkt_dtp_51` (Instagram — channel §4), `thi_mkt_dtp_290` (Multi-Channel Paid Media), `thi_mkt_dtp_300` (Reach Quarterly Review — cadence), `thi_mkt_dtp_301` (Demand Gen Funnel Ops), `env_mkt_dtp_47` (SEO OnPage), `env_mkt_dtp_48` (SEO OffPage); `holistika_reach_dtp_001` (GTM Proof Run), `holistika_reach_dtp_002` (Agency Partner Intake); `gtm_cl_585c46c9150e93`, `gtm_cl_bd461617be6692`, `gtm_cl_d277fd4bde7e85` (channels / organic-paid flow / buyer personas); `gtm_brand_dtp_32,35,48,49` (audience dimensions, FBM+SEM, web/LinkedIn channels, paid media & positioning) | 20 |
| **C6 Marketing Analytics & Attribution** | `thi_mkt_dtp_19` (Analytics), `thi_mkt_dtp_309` (Analytics Dashboard & Attribution Model); `gtm_brand_dtp_29` (traffic research) | 3 |
| **C7 Marketing Experimentation & Growth** | `thi_mkt_dtp_61` (A-Z Test), `thi_mkt_dtp_307` (Experiment Registry Maintenance), `thi_mkt_dtp_308` (Growth Hacker Variant Hypothesis) | 3 |
| **C8 PR & Media Relations** | `thi_mkt_dtp_305` (PR Press Release & Media Pitch) | 1 |
| **C9 Community & Audience Resonance** | `thi_mkt_dtp_213` (Community & Ambassador Program), `thi_mkt_dtp_287` (ITIL Support on Social Channels), `thi_mkt_dtp_302` (Resonance Pulse Review) | 3 |
| **C10 Account & Lifecycle Marketing** | `thi_mkt_dtp_303` (Account Management Engagement Pulse Cadence) | 1 |
| **C11 Product & Launch Marketing** | `thi_mkt_dtp_211` (App Store Listing & ASO), `thi_mkt_dtp_231` (Battlecards & Messaging Matrix), `thi_mkt_dtp_254` (Migration Guide & Launch Content Pack); `gtm_brand_dtp_33` (match to capabilities/products), `gtm_brand_dtp_36` (sales documentation for buyers), `gtm_brand_dtp_37` (Pitch) | 6 |
| **— evicted (not capabilities) →** | `thi_mkt_dtp_57` (Mailchimp), `thi_mkt_dtp_58` (Calendly), `gtm_brand_dtp_38` (MADEIRA API surface item) — see §3 | 3 |
| **— rehomed to other areas →** | `hol_eng_prc_proposal_001` (Proposal generation → Delivery), `tbi_mkt_dtp_revops_template_promotion_001` (RevOps template promotion → RevOps/PMO) — see §4 | 2 |
| | **Total accounted** | **117** |

Collapse arithmetic: 23+12+26+14+20+3+3+1+3+1+6 = **112** rows fold into 11 capabilities; **+3** evictions **+2** rehomed = **117**. ✓

---

## 3. Evictions (rows that are not capabilities) + a registry-target finding

Per method step 1 (strip non-capabilities) + Q2: rows named after a **system/tool** or a
**code/API symbol** are not capabilities — *"naming capabilities after systems defeats the
purpose"* (method §2.2). Three Marketing rows qualify:

| Row | Why not a capability | The real capability it serves | Correct destination |
|:--|:--|:--|:--|
| `thi_mkt_dtp_57` **Mailchimp** | SaaS email/automation **tool**, not an ability. | C10 Account & Lifecycle Marketing / C3 Editorial (email delivery is realized *using* Mailchimp). | tool/substrate registry |
| `thi_mkt_dtp_58` **Calendly** | SaaS scheduling **tool**. | C10 Account & Lifecycle Marketing (meeting booking). | tool/substrate registry |
| `gtm_brand_dtp_38` **"MADEIRA API surface item"** | A **code/API symbol** mis-seeded into the brand workstream — same class as the method's `LLMConfig`/`Sentiment Analyzer` examples. | MADEIRA delivery (Applied-AI area), not Marketing. | component/service matrix |

> **Registry-target finding (important — surfaced because I read the target).** The task named
> `COMPONENT_PRIMITIVE_REGISTRY.csv` as the eviction target, but on inspection that registry holds
> **deliverable render-primitives** (`CP-COVER-PAGE`, `CP-EXECUTIVE-SUMMARY`, `CP-HOOK`, `CP-CTA`,
> `CP-SLIDE-HERO`, `CP-DATA-TABLE` …) keyed by `parent_artifact_class_codes` (AC-DOSSIER, AC-DECK-*,
> AC-COVER-EMAIL). **Mailchimp / Calendly (tools) and a MADEIRA API symbol do NOT fit its schema.**
> The method doc's "evict code-symbols to `COMPONENT_PRIMITIVE_REGISTRY`" assumption holds for the
> **MADEIRA/Applied-AI** area's code symbols only loosely, and **not at all** for Marketing's
> tool/SaaS rows. **Recommendation:** route the two SaaS tools to a tool/substrate registry (e.g.
> the substrate registry / `COMPONENT_SERVICE_MATRIX`) and the API symbol to the component/service
> matrix — *not* `COMPONENT_PRIMITIVE_REGISTRY`. Confirm the canonical tool-registry target at the
> gated write (inline-ratify). Marketing contributes **zero** true render-primitive rows.

Note: tool names embedded *inside* otherwise-valid capability rows are not evicted — e.g.
`thi_mkt_dtp_3` "Media Edition (Final Cut, Premiere, etc)" folds into **C4** as the ability
"multimedia production"; the named editors (Final Cut, Premiere) are substrate, registered once
in the tool registry, not 117-style shadows.

---

## 4. Cross-area flags

### 4.1 MKT / Marketing area-naming normalization (the operator-requested flag)
Of the 117 rows, **116 are tagged `MKT`** and exactly **1 is tagged `Marketing`** —
`thi_marke_dtp_109` "Identify Personal Discourse" (`CAP-THI-MARKE-DTP-109`). This is a single
mis-tagged row, not a second area. **Recommendation: normalize to `MKT`** (the dominant value,
and the value `process_list.csv` already uses — `akos-area-governance.mdc` RULE 2 states
*"Marketing: `process_list.csv` uses area code `MKT`, not `Marketing`"*). The fix is a one-cell
edit on `thi_marke_dtp_109` (and its capability shadow) at the gated write; it folds into **C1**
regardless. No other Marketing row carries the `Marketing` spelling.

### 4.2 Rows that belong to another area's capability map (rehomed, not Marketing capabilities)
| Row | Tagged | Real owner area / capability | Disposition |
|:--|:--|:--|:--|
| `hol_eng_prc_proposal_001` **Proposal generation** (active; owner Brand & Narrative Manager) | MKT | **Delivery & Client Engagement Ops** — method cluster #12 "Engagement Design, Estimation & Proposal". Marketing contributes the *content/messaging*; the proposal *capability* is Delivery-owned. | Rehome to Delivery map; Marketing keeps a realization edge (sales-enablement content). |
| `tbi_mkt_dtp_revops_template_promotion_001` **RevOps engagement template promotion** (active; owner PMO) | MKT | **RevOps / PMO** (Delivery domain) — engagement-template lifecycle, not a marketing ability. | Rehome to RevOps/PMO map. |

### 4.3 Shared-realization (N:N) flags — capability is Marketing's, but a realizing process is another area's
- **C4 Creative, Web & Experience Design** ↔ **Tech "Web Experience Engineering"** (method cluster #6,
  Product & Platform Eng L1). The *design* intent (look, story, UX, landing CRO) is Marketing's; the
  *engineering* (codebase, components, DNS/deploy) is Tech's. Rows `gtm_brand_dtp_20,22,23,24`,
  `gtm_cl_a427f4b0dd3c83`, `env_mkt_dtp_7` explicitly straddle this. Keep as **one capability per area**,
  linked by N:N `realization` — do **not** duplicate the row in both maps.
- **C1 brand/market research rows** (`gtm_brand_dtp_10,11,12`) ↔ **Research / CorpInt** area. Competitor/
  buyer/trend research realized for brand positioning overlaps the Research area's market-intel capability;
  keep in C1 with a realization edge to Research (bearer-agnostic — the same research process can realize both).
- **C1 `tbi_ppl_prc_founder_bio_mtnce_001`** carries a **`ppl` (People) prefix** but is owned by the
  Brand & Narrative Manager and tagged MKT. The founder bio is a brand/narrative asset → keep in **C1**;
  flag the prefix as cosmetic (the bearer-agnostic ID at the gated write drops the `ppl`/`thi`/`tbi` prefix).

### 4.4 Channel-vs-capability naming
`thi_mkt_dtp_50` **LinkedIn** and `thi_mkt_dtp_51` **Instagram** are **channels/touchpoints**, not
capabilities (same class as the technology-neutral rule). They fold into **C5 Digital Demand
Generation** (and Resonance for organic) as channel-specific *process* realizations; the channels
themselves belong in a **channel/touchpoint registry** (`CHANNEL_TOUCHPOINT_REGISTRY`), not the
capability map. No separate eviction needed — they remain accounted under C5.

---

## 5. Count summary

| Bucket | Count |
|:--|:--:|
| Old Marketing process-shadow rows (`area in ('MKT','Marketing')`) | **117** |
| → fold into stable capabilities | 112 |
| → evicted (tools / code-symbol; §3) | 3 |
| → rehomed to other areas' maps (§4.2) | 2 |
| **Proposed stable Marketing capabilities** | **11** |
| Level-1 domains spanned | 1 (Go-to-Market & Brand) |
| of which `active` lifecycle | 3 (C1, C2, C5) |
| of which `differentiating` tier | 4 (C1, C2, C7, C9) |

**117 → 11** (≈ 10.6:1 de-densification), landing the Marketing slice well inside the
40–100 strategic L2 band the method targets, while keeping every row traceable to a destination.

### Next gates (inline-ratify at the canonical write, per method §5)
1. Confirm the **11-capability count + boundaries** (esp. C1↔C2↔C3 brand/governance/editorial split).
2. Ratify the **tool-eviction target registry** (substrate/tool registry vs `COMPONENT_SERVICE_MATRIX`) — *not* `COMPONENT_PRIMITIVE_REGISTRY` (§3 finding).
3. Approve the **`Marketing`→`MKT` normalization** of `thi_marke_dtp_109` (§4.1).
4. Confirm the **2 cross-area rehomes** land in the Delivery / RevOps maps when those areas are processed.

> **Gate boundary:** this proposal modifies no canonical CSV. The one-time rewrite of
> `CAPABILITY_REGISTRY.csv` (117 → 11 for Marketing) is a **gated canonical-CSV change** requiring
> explicit operator approval, ideally as a per-area slice (method §5 Q7).

## Cross-references
- Method: [`l2-capability-densify-findings-2026-06-07.md`](../l2-capability-densify-findings-2026-06-07.md) (6-step collapse; worked clusters #4 #5 #6 #12).
- Ratifying decision: **D-IH-95-H** (keep-separate + de-densify, area-by-area, organic count).
- Sibling collapse-maps (forthcoming): other areas under `l2-collapse-maps/`.
- Governing rules: `akos-baseline-governance.mdc` (canonical-CSV gate), `akos-area-governance.mdc` RULE 2 (`MKT` not `Marketing`), `akos-inline-ratification.mdc` (the §5 gates).
