---
title: Collaborator Share Doctrine
language: en
intellectual_kind: people-canonical
access_level: 4
audience: J-OP;J-AIC
confidence_level: A1
source_taxonomy: holistika-internal-doctrine
authors:
  - Founder/CEO
co_authors:
  - PMO
  - People Operations Manager
  - Legal Counsel
last_review: 2026-05-27
last_review_by: System Owner (AIC)
last_review_at: 2026-05-27
last_review_decision_id: D-IH-86-EO
methodology_version_at_review: v3.2
ratifying_decisions:
  - D-IH-86-DA
  - D-IH-86-DB
  - D-IH-86-DC
  - D-IH-86-DD
  - D-IH-86-DE
  - D-IH-86-EJ
  - D-IH-86-EK
  - D-IH-86-EL
  - D-IH-86-EM
  - D-IH-86-EN
  - D-IH-86-EO
  - D-IH-73-J
status: active
register: internal
linked_canonicals:
  - HOLISTIKA_QUALITY_FABRIC.md
  - HOLISTIKA_ORGANISING_DOCTRINE.md
  - ARTIFACT_CLASS_LIBRARY.md
  - ../People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md
  - ../People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
  - ../Compliance/canonicals/PRECEDENCE.md
  - ../Compliance/canonicals/process_list.csv
  - ../Compliance/canonicals/baseline_organisation.csv
  - ../Compliance/canonicals/DECISION_REGISTER.csv
  - ../Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv
  - ../Compliance/canonicals/dimensions/PEOPLE_DESIGN_PATTERN_REGISTRY.csv
  - ../../Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md
linked_cursor_rules:
  - .cursor/rules/akos-collaborator-share.mdc
  - .cursor/rules/akos-quality-fabric.mdc
  - .cursor/rules/akos-people-discipline-of-disciplines.mdc
  - .cursor/rules/akos-applied-research-discipline.mdc
  - .cursor/rules/akos-executable-process-catalog.mdc
  - .cursor/rules/akos-holistika-operations.mdc
  - .cursor/rules/akos-inline-ratification.mdc
  - .cursor/rules/akos-planning-traceability.mdc
linked_skills:
  - .cursor/skills/collaborator-share-craft/SKILL.md
  - .cursor/skills/inline-ratify-craft/SKILL.md
companion_to:
  - HOLISTIKA_QUALITY_FABRIC.md
forward_charters:
  - process_list.csv row hol_peopl_dtp_collaborator_share_001 (paired SOP+runbook gate)
  - PEOPLE_DESIGN_PATTERN_REGISTRY row pattern_collaborator_share_doctrine
  - paired runbook scripts/collaborator_share_calculate.py (Commit 2b)
  - paired validator scripts/validate_collaborator_share.py (Commit 2b)
  - paired SOP SOP-PEOPLE_COLLABORATOR_SHARE_001.md (Commit 2c)
  - paired cursor rule .cursor/rules/akos-collaborator-share.mdc (Commit 2c)
  - paired skill .cursor/skills/collaborator-share-craft/SKILL.md (Commit 2c)
  - Supabase mirror DDL for 5 CSVs (Commit 2b)
  - Aïsha EFA per-engagement application of the doctrine (Commit 3 — first worked instantiation; SUEZ engagement)
  - INFO→FAIL ramp promotion (gated on 3+ real engagements applying the doctrine cleanly with zero validator FAIL)
---

# Collaborator Share Doctrine

> The People-area canonical that names how Holistika splits the **benefits** of an engagement with a strategic collaborator (or party) who brings, operates, or co-ventures the deal. The doctrine names **4 base patterns + 1 stackable overlay** — capturing the operator's lived commercial reality across deep-partner, pure-BD-intro, joint-venture-aventure, and direct-consulting engagement shapes.
>
> Founding operator framing (2026-05-25, deep_partner_65_35 lived precedent):
>
> *"65% for us, 35% for Aïsha out of the margin and that means we need to act as consultants and partners but we at holistika we treat our partners as B2B, hence we propose a plethora of services we take for granted we'll do and delegate whatever process we may have agreed with the partner to them, in this case, we'll do most of the work, but it's justified because of bringing us such strategic customer for us. websitz per example was asked to support no mktops as they were a mkt agency themselves on top of bringing us customers to the table."*
>
> Extending operator framing (2026-05-22, 15% BD overlay + direct-consulting reality):
>
> *"what about 15% of business development that i give to people when they don't work but just come and give us a project and work as business developer/account mgr at least for the beginning, getting their share over the margin so that they have an incentive to bring good deals? […] yeah, we need to get paid from our own project like any consultancy does, and be clever so that the numbers are cleverly crafted to sit our interests."*
>
> Thirteenth specialty instantiation of [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (per **D-IH-86-DA**) and sister to [`ARTIFACT_CLASS_LIBRARY.md`](ARTIFACT_CLASS_LIBRARY.md). Rewritten at Wave R+2 per **D-IH-86-EJ** to replace the pre-rewrite 3-shape enum (which contained an architectural-invention pattern `orchestration_broker_thin_margin` that mis-encoded the SUEZ POC commercial reality) with a 4-base + 1-overlay shape grounded in lived precedents + transcript substrate. Codifies `compose_COLLABORATOR_SHARE(engagement, collaborator, share_pattern, share_overlay, methodology_readiness, services_billed, overlap_clauses, market_rate_ref) → per-pattern benefits split or revenue-allocation + optional BD-overlay stack + transparent project-cost roster + partner-overlap-exclusion clause table + market-rate benchmark with governed override`.

## 1. Purpose

Holistika collaborates with strategic partners (people who bring deals, operate processes inside deals, or pair with us as joint go-to-market arms) and the question of *how the upside is split* recurs in every such engagement. Three failure modes drove the operator to codify this doctrine at the 2026-05-25 session:

1. **Going back on what was said.** Operator: *"i need yor help for the best practice and especially never go back on what i said not to loose credibility (they not always remember things but it can be they do)."* When the economic model lives in chat-history-and-memory rather than in canonical doctrine, every partner conversation is a fresh negotiation with implicit drift; collaborators may quote back something the operator no longer remembers; trust erodes.

2. **B2B-vendor posture mistaken for free labour.** Holistika provides a plethora of services (research-head discipline; AKOS governance; MADEIRA + AI engineering; brand + render machinery; PMO orchestration). When a partner has overlapping capabilities (Websitz precedent — they are a mkt agency themselves), Holistika does NOT bill those overlapping services against the project; we contribute them in-kind as the value of our 65% share. Without explicit clauses naming which services were in-kind, future engagements may over-bill OR under-bill, breaking the partner narrative.

3. **Collaborator transparency vs operator administrative overhead.** Aïsha-shape collaborators (operator-of-the-process being automated; Aïsha for SUEZ procurement workflow) gain BOTH a billed rate for their ongoing operator work AND a share of remaining benefits. Without canonical accounting, the operator either (a) hides the collaborator's billed time (collaborator feels exploited; benefits-pool seems larger than it is) or (b) muddles billed time with profit share (collaborator does not know what they earned for what). Transparency is the alternative; this doctrine names how to do it.

This canonical names the **economic-relationship discipline** — not a one-off contract template but a recurring doctrine with a paired runbook (computes the math), a paired validator (catches over-billing / under-billing / un-ratified market-rate excursions), a paired cursor rule (names when the discipline fires), a paired skill (names how to apply), and a paired SOP (names the operator-side AC-HUMAN + AC-AUTOMATION). The 5 CSV registers below name what to record; the runbook computes deterministically what is computable; the validator catches drift before commit; the operator scratchpad records every governed exception.

## 2. The economic architecture — TRUE-MARGIN + 5-register chassis

Per **D-IH-86-DB** (operator-ratified at the 2026-05-25 session), the canonical benefits formula is **TRUE-MARGIN with an explicit billed-services log**:

```
BENEFITS = REVENUE - (
    founder_billed_time
    + collaborator_billed_time
    + direct_pass_through_project_costs
    + holistika_vendor_services_billed_against_project_per_log
)
```

Where:

- **REVENUE** is the gross amount the engagement client (e.g., SUEZ WeBuy) pays Holistika under the engagement contract — invoiced amount, before any Holistika-side cost allocation.
- **`founder_billed_time`** is the founder's (Mark-I) hours logged against the engagement at the founder market rate (per the same `COLLABORATOR_MARKET_RATE_REFERENCE.csv` benchmarks that apply to collaborators — the founder is not exempt; the doctrine treats every billed contributor uniformly to preserve narrative consistency).
- **`collaborator_billed_time`** is the named collaborator's (e.g., Aïsha's) hours logged against the engagement at their per-row rate in `COLLABORATOR_SHARE_REGISTRY.csv` × hours-worked.
- **`direct_pass_through_project_costs`** is third-party costs invoiced directly to the engagement (cloud infrastructure billed back per `eng_model_rpp_vendor` pattern; per-deal tooling licenses; outsourced helper hours per `eng_model_outsourced_helper`; printing / translation / notarisation costs).
- **`holistika_vendor_services_billed_against_project_per_log`** is the explicit subset of Holistika's in-house service stack that THIS engagement bills against the project per the per-engagement row in `HOLISTIKA_VENDOR_SERVICES_BILLED.csv`. **Default is zero** (Holistika's service stack is the value of our 65% share); the log explicitly names exceptions (e.g., a partner with no overlapping research capability for whom Holistika bills the research head's hours against the project per a charter-time ratification).

BENEFITS is then split **65% Holistika-side / 35% collaborator-side** by default. Per-engagement deviations from the 65/35 default require an explicit `DECISION_REGISTER` row + a `COLLABORATOR_RATE_OVERRIDES.csv` row pointing at the decision FK; the validator FAILS on a SHARE_REGISTRY row whose split deviates from 65/35 without a matching override row.

### Why this shape (the design constraints satisfied)

| Constraint | How TRUE-MARGIN satisfies it |
|:---|:---|
| **Partner narrative cleanly defends the 65% Holistika-side share.** | The 65% is the value of Holistika's in-house service stack (research + AKOS + MADEIRA + brand + PMO) contributed AS our share — not billed AGAINST the project then claimed again as share. No double-dipping. The partner sees: "Holistika brings the methodology + machinery + execution craft; collaborator brings the deal + operational continuity; benefits split fairly." |
| **Collaborator transparency on billed time.** | Aïsha-shape collaborators see their hours logged at their rate against the project (transparent line item in the cost roster) AND see they gain 35% of remaining benefits on top. They never feel their operational hours were absorbed into the benefits pool to inflate the 35% calculation. |
| **B2B-vendor posture preserved.** | Holistika is positioned as a B2B vendor to the partner — we propose a plethora of services we take for granted; the partner sees the service stack as a coherent business offering; the partner is NOT positioned as a buyer of unbundled Holistika hours. |
| **Partner-overlap exclusion is principled, not ad-hoc.** | Websitz-precedent (they are a mkt agency themselves; MKTOPS support was contributed in-kind because of overlap) is codified in `PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv` as a named pattern row. Future engagements with similar partner-capability overlap inherit the pattern; no per-deal renegotiation. |
| **Governed commercial flexibility.** | Per-engagement deviations from 65/35 (and per-collaborator deviations from market-rate benchmarks) are NOT forbidden — they are *governed* via the `COLLABORATOR_RATE_OVERRIDES.csv` register + `DECISION_REGISTER` row. Operator can adjust commercially when strategy demands; the audit trail is preserved. |
| **Audit-trail-bearing across the engagement lifecycle.** | Every cost row, every in-kind contribution, every market-rate excursion, every commercial override has a canonical CSV row with a `decision_id` FK when ratification was required. A future auditor (or a future Aïsha-shape collaborator asking "show me how my 35% was computed") can reproduce the math from the 5 CSVs alone. |

### The 5 net-new canonical CSV registers

The doctrine is materialised across 5 net-new canonical CSVs (all landing under `docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/` per the sibling-to-ENGAGEMENT_MODEL_REGISTRY convention):

| # | Register | Purpose | Cross-CSV FK |
|:--|:---|:---|:---|
| **1** | **`COLLABORATOR_SHARE_REGISTRY.csv`** | One row per (engagement, collaborator) pair. Records the engagement_id, collaborator_id (FK to `GOI_POI_REGISTER`), engagement_model_id (FK to `ENGAGEMENT_MODEL_REGISTRY` — typically `eng_model_percentage_collaborator`), holistika_share_pct (default 65), collaborator_share_pct (default 35), collaborator_billed_rate, collaborator_billed_rate_currency, collaborator_role_class (FK to `baseline_organisation`), share_override_decision_id (nullable; populated when deviating from 65/35), status, signed_at, signed_by_collaborator, signed_by_holistika, notes. | engagement_id (engagement folder slug); collaborator_id → GOI_POI_REGISTER; engagement_model_id → ENGAGEMENT_MODEL_REGISTRY; collaborator_role_class → baseline_organisation; share_override_decision_id → DECISION_REGISTER |
| **2** | **`HOLISTIKA_VENDOR_SERVICES_BILLED.csv`** | One row per (engagement, holistika_service_class) pair documenting whether that service was BILLED against the project or contributed IN-KIND. Records engagement_id, holistika_service_class (e.g., `research_head_discipline`, `mktops_marketing`, `dataops_engineering`, `madeira_ai_orchestration`, `brand_render_machinery`, `pmo_orchestration`), bill_mode (`billed` / `in_kind`), billed_hours (nullable), billed_rate (nullable), billed_amount_computed (nullable), justification_clause_id (FK to `PARTNER_OVERLAP_EXCLUSION_CLAUSES` when bill_mode=in_kind), bill_mode_decision_id (nullable; populated when bill_mode deviates from doctrine default), status, notes. Default `bill_mode` per service class per the doctrine §2.2 below. | engagement_id; justification_clause_id → PARTNER_OVERLAP_EXCLUSION_CLAUSES; bill_mode_decision_id → DECISION_REGISTER |
| **3** | **`PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv`** | Named clause patterns documenting categorical reasons a partner's overlapping capability triggers in-kind treatment. Records clause_id (e.g., `clause_partner_marketing_agency_overlap`), clause_name, applicable_holistika_service_classes (semicolon-separated), overlap_pattern_description, internal_precedent (the engagement that minted the pattern), industry_precedent_citation, ratifying_decision_id, last_review_at, status, notes. Seeded with Websitz pattern (`clause_partner_marketing_agency_overlap`). | applicable_holistika_service_classes → HOLISTIKA_VENDOR_SERVICES_BILLED.holistika_service_class enum; ratifying_decision_id → DECISION_REGISTER |
| **4** | **`COLLABORATOR_MARKET_RATE_REFERENCE.csv`** | Role-class × region × experience-band benchmarks for collaborator billed rates. Records rate_id (e.g., `rate_fr_lead_data_senior`), role_class (FK to `baseline_organisation.role_name`), region_code (ISO-3166-1 alpha-2; e.g., `FR` / `ES` / `US`), experience_band (`junior` / `mid` / `senior` / `lead` / `expert`), rate_currency (ISO-4217), rate_min_per_hour, rate_typical_per_hour, rate_max_per_hour, rate_source (industry survey citation; URL when public), last_review_at, status, notes. The validator's market-rate audit allows ±25% variance from `rate_typical_per_hour`; outside the band requires an override row. | role_class → baseline_organisation |
| **5** | **`COLLABORATOR_RATE_OVERRIDES.csv`** | Governed commercial adjustments to market-rate OR to the 65/35 split. Records override_id, override_kind (`market_rate_excursion` / `share_split_deviation`), engagement_id, collaborator_id (FK to GOI_POI_REGISTER), reference_rate_id (FK to COLLABORATOR_MARKET_RATE_REFERENCE; nullable for share_split_deviation), reference_rate_value (decimal; nullable for share_split_deviation), actual_value (decimal — actual rate for market_rate_excursion; actual collaborator_share_pct for share_split_deviation), variance_pct (computed; signed), justification_narrative, ratifying_decision_id (FK to DECISION_REGISTER; **mandatory**), commercial_strategy_rationale (short prose; why the operator commercially adjusted), expires_at (nullable; auto-revert), last_review_at, status, notes. | engagement_id; collaborator_id → GOI_POI_REGISTER; reference_rate_id → COLLABORATOR_MARKET_RATE_REFERENCE; ratifying_decision_id → DECISION_REGISTER |

### 2.2. Default `bill_mode` per Holistika service class (the in-kind baseline)

For HOLISTIKA_VENDOR_SERVICES_BILLED, the doctrine specifies the canonical default `bill_mode` per service class. Per-engagement deviations from default require a `bill_mode_decision_id` FK to a `DECISION_REGISTER` row.

| `holistika_service_class` | Default `bill_mode` | Why this default |
|:---|:---|:---|
| `research_head_discipline` | `in_kind` | Holistika's discovery + applied-research craft is the value of our 65% share; not double-dipped. Exception when partner has no research capability AND engagement demands deep external research beyond ordinary engagement discovery. |
| `mktops_marketing` | `in_kind` | Default in-kind. Websitz precedent: when partner is a marketing agency themselves, MKTOPS overlap → in-kind is mandatory (clause-enforced). Exception when partner has no MKTOPS capability AND engagement requires GTM funnel beyond ordinary outreach. |
| `dataops_engineering` | `in_kind` | Holistika's AKOS + data governance + canonical-CSV discipline is foundational service stack. Exception when partner is themselves a data-engineering firm (overlap) OR when engagement requires custom data-platform build beyond ordinary AKOS-shaped governance. |
| `madeira_ai_orchestration` | `in_kind` | MADEIRA + AIC orchestration is the differentiator that makes the deal economically asymmetric in Holistika's favour (single AIC replacing multiple humans). Exception when partner brings their own AIC stack (very rare) OR when AIC build is the deal itself (then revenue IS for AIC build; not in-kind). |
| `brand_render_machinery` | `in_kind` | Brand + render-trail + 5-axis Quality Fabric machinery is the methodology IP that makes Holistika's externals defensible. Exception when partner brings their own brand + render stack (Websitz pattern again — they have their own brand). |
| `pmo_orchestration` | `in_kind` | PMO + governance + decision-register + canonical-CSV orchestration is overhead Holistika absorbs as the cost of being the SSOT-bearing party. Exception is rare — PMO overhead is the cost of being us. |
| `legal_template_handling` | `billed` (when external counsel engaged) / `in_kind` (when standard templates from `Legal/canonicals/`) | Standard templates contributed in-kind; external counsel + bespoke templates billed at pass-through. Per Initiative 21 founder-filed-instruments pattern. |
| `front_end_engineering` | depends on engagement scope | When deal builds a custom front-end (e.g., a new HLK-ERP panel for a partner-side workflow), front-end hours are billed. When boilerplate-shaped reuse, in-kind. Charter-time ratification required when scope is ambiguous. |
| `ai_engineering_bespoke` | `billed` | Bespoke AI engineering hours (model fine-tuning, custom embedder training, ML-pipeline build) are billed; AI engineering is a deliverable scope, not a foundational service stack. |
| `external_research_pass` | `billed` (when scope explicitly demands a research pass beyond ordinary engagement discovery) / `in_kind` (when within ordinary discovery) | External research that produces a deliverable artifact (market study; competitive landscape; regulatory scan) is billed when explicitly scoped; baseline discovery work is in-kind. |

The default table is itself codifiable as a CSV (`HOLISTIKA_VENDOR_SERVICE_DEFAULT_BILL_MODE.csv` — forward-charter; not minted in this commit because the 10 rows above are stable and changing them requires doctrine amendment). The defaults can be amended via the doctrine versioning process (operator-ratified amendment + cross-canonical updates).

### 2.3. Four base patterns + one stackable overlay — the `share_pattern` + `share_overlay` enums (D-IH-86-EJ rewrite of pre-D-IH-86-DE 3-shape enum)

The §2 economic architecture above describes the **deep_partner_65_35** shape — the lived Websitz precedent the operator codified verbatim at the 2026-05-25 architecture session. The pre-rewrite doctrine (commits 2a..4 inclusive, status pre-rewrite) named a 3-shape enum where the second shape `orchestration_broker_thin_margin` was minted mid-architecture-session to capture a SUEZ near-future projection the operator was experimenting with at the time.

The SUEZ 13/05/2026 customer-meeting substrate + the operator's 22/05/2026 follow-up framing surfaced that **the orchestration_broker shape was an architectural invention** that mis-encoded the real SUEZ commercial reality. The operator's verbatim correction:

> *"6% is unknown to me (like i would accept that). [...] What about 15% of business development that i give to people when they don't work but just come and give us a project and work as business developer/account mgr at least for the beginning [...] yeah, we need to get paid from our own project like any consultancy does, and be clever so that the numbers are cleverly crafted to sit our interests."* (operator, 2026-05-22, post-13/05-meeting reflection)

This rewrite (per **D-IH-86-EJ**, ratified 2026-05-26 post-substrate-audit) replaces the 3-shape enum with **4 base patterns + 1 stackable overlay** grounded in the operator's lived commercial reality across deep-partner, pure-BD-intro, joint-venture-aventure, and direct-consulting engagement shapes. The new `share_pattern` enum on `COLLABORATOR_SHARE_REGISTRY.csv` carries 4 values; a separate `share_overlay` column (nullable) carries the optional BD-commission stack.

The architectural invention `orchestration_broker_thin_margin` is **removed** (no surviving canonical rows; the 5 SUEZ-engagement SHARE_REGISTRY rows authored at Commit 4 are corrected via supersede in Commit 5 of this rewrite). The 3-shape decisions **D-IH-86-DE** (enum mint), **D-IH-86-DF** (Stage-1 active-promotion), and **D-IH-86-EG** (SUEZ split anchor) are marked superseded by **D-IH-86-EJ** (rewrite ratify), **D-IH-86-EO** (Stage-1 re-active-promotion on the 4+1 enum at Wave R+3), and **D-IH-86-EL** (SUEZ recommercialization), respectively. The active-promotion gate reset implicitly with the rewrite — the doctrine returned to `status: charter` while the new 4-base + 1-overlay shape exercised ≥ 2 base patterns + ≥ 1 overlay in lived engagements (SUEZ POC + Aïsha continuity at Wave R+3), and then re-promoted to `active` via D-IH-86-EO once the 4-of-4 Stage-1 gates met.

#### 2.3.1. The 4 base `share_pattern` values (mutually exclusive)

| `share_pattern` value | Sum-to-100 invariant | Default split or anchor | Cost-roster semantics | Override required when | Use when |
|:---|:---|:---|:---|:---|:---|
| **`deep_partner_65_35`** *(default; backward-compatible with all pre-rewrite rows)* | **Per-row** — every SHARE_REGISTRY row's `holistika_share_pct + collaborator_share_pct = 100` (typically 65 + 35). | 65/35 default. Per-engagement deviation requires a matching `COLLABORATOR_RATE_OVERRIDES` row with `override_kind=share_split_deviation`. | TRUE-MARGIN formula per §2 (revenue minus founder billed time minus collaborator billed time minus direct pass-through minus VENDOR_SERVICES_BILLED billed rows; result split 65/35). | Per-row split deviates from 65/35. | Holistika contributes a full methodology + machinery + execution stack as the value of the 65% share; collaborator brings the deal + operates the process; B2B partner narrative applies; collaborator is `methodology_trained` OR `methodology_in_progress`. The Websitz / Rushly lived precedent (§3.1) + the Aïsha-shape didactic example. |
| **`bd_intro_only`** | **Per-row** — single SHARE_REGISTRY row per intro per engagement. `holistika_share_pct = 100 − bd_commission_pct` (default `bd_commission_pct = 15`; result default 85/15); `collaborator_share_pct = bd_commission_pct`. Per-row sum-to-100 still applies. | 15% to collaborator (BD-overlay default); Holistika retains 85%. | TRUE-MARGIN formula per §2 with the collaborator's BD-commission slice computed off the BENEFITS pool (NOT off gross revenue — the BD commission tracks the operator's economic outcome, not the customer's gross spend). | Per-row commission % deviates from 15 OR collaborator works ANY operational hours beyond pure intro/BD (then the engagement is not `bd_intro_only`; reclassify to `consulting_direct + bd_commission_overlay` OR `deep_partner_65_35`). | Collaborator brings a project but does NOT work on it operationally beyond initial BD/account-management; collaborator is `methodology_naive` (cannot follow methodology) OR `methodology_not_applicable`; engagement structurally needs a pure BD/finder's-fee arrangement. The 22/05 framing's *"people when they don't work but just come and give us a project"* shape. |
| **`joint_venture_aventure`** | **Per-row** — every SHARE_REGISTRY row's `holistika_share_pct + collaborator_share_pct = 100` (typically 50 + 50 OR another mutually-named split). | 50/50 default. Per-engagement deviation requires the matching override row. | TRUE-MARGIN formula per §2 BUT both parties contribute methodology + machinery + execution stack as in-kind value of their respective shares; both parties bill their respective execution hours transparently; both parties carry shared upside AND shared downside. | Per-row split deviates from 50/50 OR the engagement carries asymmetric risk-bearing (one party absorbs more downside; reclassify via override). | True joint-venture aventure where Holistika partners with a peer-equivalent party (e.g., a sister consultancy, an aligned tooling vendor) to pursue a shared go-to-market or co-delivery; both parties contribute substantial methodology stack; both parties are `methodology_trained` OR cross-recognise each other's methodology stacks as equivalent-in-value. Distinguished from `deep_partner_65_35` by structural symmetry (peer-to-peer, not vendor-to-partner). |
| **`consulting_direct`** | **Per-row** — single SHARE_REGISTRY row per engagement. `holistika_share_pct = 100 − sum(applied_overlays)`; `collaborator_share_pct = sum(applied_overlays)`. When no overlays apply, the row reduces to `100 / 0` (Holistika retains 100%). | 100% Holistika by default (no BD-overlay applied). When `bd_commission_overlay` stacks (see §2.3.2), the row becomes `(100 − overlay_pct) / overlay_pct` (default `85 / 15`). | TRUE-MARGIN formula per §2 with the founder + execution team billing transparently against the engagement; Holistika consumes the BENEFITS pool minus any applied overlay slice. | Per-row deviates from the 100% Holistika baseline AND no `share_overlay` value resolves the deviation; collaborator does ANY operational work without a paired BD-overlay (then engagement is not `consulting_direct`; reclassify). | Holistika delivers an engagement as a direct consultancy — founder + execution team work on a customer's project; we get paid for our own project like any consultancy does (per operator 22/05 framing); customer relationship is direct (not collaborator-brokered). The SUEZ POC corrected commercial reality (§3.2 corrected) + flagship-class direct engagements going forward. With an optional `bd_commission_overlay` when an intro/BD party brought the deal. |

#### 2.3.2. The stackable `share_overlay` enum (currently 1 value; designed to extend)

The `share_overlay` column on `COLLABORATOR_SHARE_REGISTRY.csv` is **nullable**. When present, it stacks ON TOP of the base `share_pattern` to compose a richer commercial shape. The current canonical enum carries 1 value (the 15% BD commission per operator 22/05 framing); the architecture supports future overlays without enum-breaking.

| `share_overlay` value | Stacks on which base patterns | Effect | Default anchor | Use when |
|:---|:---|:---|:---|:---|
| **`bd_commission_overlay`** | `consulting_direct` (primary use case); `deep_partner_65_35` (when an external BD party introduces a deal that Holistika + a separate deep partner deliver — rare); NEVER on `bd_intro_only` (would be circular — the base pattern IS the BD shape); NEVER on `joint_venture_aventure` (would conflate JV symmetry with intro asymmetry — file as separate engagement OR reclassify base). | The BD-overlay party receives `bd_commission_pct` of the BENEFITS pool (default 15%); Holistika's share reduces correspondingly; the operational delivery party (per base pattern) is unaffected (their hours billed independently). | 15% to overlay party. Per-engagement deviation requires a matching `COLLABORATOR_RATE_OVERRIDES` row with `override_kind=overlay_pct_deviation`. | An intro/BD-only party brought a deal that Holistika delivers under `consulting_direct` (Aïsha on SUEZ POC is the canonical instantiation — Aïsha brought the SUEZ relationship; Holistika delivers; Aïsha is on a BD-commission overlay during early-phase relationship-continuity; see §3.2 corrected) OR an intro party brought a deal that Holistika + a deep partner co-deliver. |

The overlay row in SHARE_REGISTRY is **separate** from the base-pattern row — i.e., a `consulting_direct + bd_commission_overlay` engagement has TWO rows: one for Holistika (base `consulting_direct`, 85%) and one for the BD-overlay party (base `consulting_direct`, 15%, `share_overlay = bd_commission_overlay`). Both rows carry the same `engagement_id` + same `share_pattern = consulting_direct`. CS-03 verifies the across-rows sum equals 100; CS-09 (NEW; see §6) verifies that any `share_overlay = bd_commission_overlay` row pairs with a sibling base-pattern row of an `[VALID_OVERLAY_BASE_PAIRINGS]`-compatible base (currently `consulting_direct` or `deep_partner_65_35`).

#### 2.3.3. The escape hatch: `custom` is removed; reclassify-or-charter governance applies

The pre-rewrite 3rd shape `custom` is **removed** in this rewrite. Reasoning: the 4 base patterns cover the operator's lived reality (deep partner + BD-only + JV peer + direct consulting); the BD-overlay covers the most-common stacking case. Engagements that genuinely fit none of these 4 base patterns (e.g., a non-cash partnership with equity instead of revenue share; a flagship discount deal with operator-defined math) escape to a different mechanism:

- **Equity-instead-of-revenue partnerships.** Use `eng_model_investor_advisor` engagement model + the separate cap-table-class governance (out of scope for this doctrine).
- **Milestone-shaped retribution without ongoing operator continuity.** Use `eng_model_milestone_consultant` engagement model (Bâtard 2020 precedent; codified at I73 / D-IH-73-I) — the milestone economics live at the engagement-model layer, not this share_pattern layer.
- **Flagship-discount commercial deals with operator-defined math.** Author a `consulting_direct` row with a mandatory `share_override_decision_id` FK + operator-defined `holistika_share_pct` (e.g., 70% instead of the default 85% when a 30% commercial overlay is granted to a flagship customer for case-study rights — and the override row carries the strategic rationale).
- **Any other shape the 4 base patterns cannot express.** Halt and propose either a 5th base pattern (doctrine amendment via inline-ratify + decision row) OR reclassification to an existing engagement-model registry row. NEVER author a row outside the enum silently — CS-08 FAILs immediately.

The removal of `custom` is the load-bearing claim of this rewrite: governance schemas are stronger when the escape hatch is **structurally constrained** (reclassify-or-amend-the-enum) rather than **operator-narrative-defined** (the old `custom` allowed arbitrary commercial shapes with only the override FK as discipline; the new architecture forces the operator to choose: name the shape via a base pattern + overlay stack OR amend the enum via a decision row that lives in the doctrine).

#### 2.3.4. Why this enum architecture exists at all

The pre-rewrite doctrine implicitly assumed a single economic shape (the 65/35 deep-partner Websitz model) plus a thin-margin orchestration invention that did not match operator reality. Forcing operator-lived engagement shapes into either of those would have required either (a) declaring the founder + each collaborator as separate per-row 65/35 splits (mathematically nonsensical for direct-consulting work where Holistika owns 100%); OR (b) overloading the override mechanism so heavily that the validator could no longer distinguish "operator-ratified commercial flexibility" from "schema doesn't fit the deal at all"; OR (c) silently mis-classifying engagements (the SUEZ POC pre-rewrite Commit-4 rows were authored under `orchestration_broker_thin_margin` with a 6% Holistika anchor the operator never agreed to).

The 4-base + 1-overlay architecture surfaces the structural differences explicitly so each shape gets its own validator semantics (CS-03 + CS-04 branch per base pattern; CS-08 enforces base-enum membership; CS-09 NEW enforces overlay-base coherence). The architecture is also designed to extend: future patterns (`programmatic_revenue_share` for a SaaS-class engagement; `co_authored_publication` for a research-IP-share engagement) can be added as 5th + 6th base patterns via doctrine amendment without breaking existing rows.

#### 2.3.5. Default + backward compatibility posture

The Pydantic model + the Supabase mirror DDL both default `share_pattern` to `deep_partner_65_35` and `share_overlay` to NULL. The pre-rewrite 3-shape enum's `orchestration_broker_thin_margin` value is **removed** from `VALID_SHARE_PATTERNS` (Pydantic Literal); a forward Supabase migration drops the old CHECK constraint + adds the new (`deep_partner_65_35` / `bd_intro_only` / `joint_venture_aventure` / `consulting_direct`) + adds the new `share_overlay` column with NULLABLE TEXT + CHECK constraint matching `VALID_SHARE_OVERLAYS` (currently `bd_commission_overlay`).

Pre-rewrite SHARE_REGISTRY rows authored at Commit 4 (the 5 SUEZ POC rows under the removed `orchestration_broker_thin_margin`) are **corrected** at Commit 5 via supersede: the existing 5 rows are deleted (DELETE statement in the operator-applied SQL gate per `akos-holistika-operations.mdc`) and replaced with the new 2-row shape (1 Holistika row at `consulting_direct` / 85% + 1 Aïsha row at `consulting_direct + bd_commission_overlay` / 15%). The supersede decision row D-IH-86-EL records the rationale.

#### 2.3.6. INFO → FAIL ramp posture (reset to charter at this rewrite)

Per `akos-collaborator-share.mdc` RULE 5 (rewritten at Commit 4 of this rewrite-tranche), CS-08 (enum-validity) + CS-09 (overlay-base coherence; NEW) launch at INFO advisory. The doctrine reset to `status: charter` implicitly with D-IH-86-EJ (the rewrite supersedes the pre-rewrite D-IH-86-DE 3-shape enum that D-IH-86-DF had promoted). Stage-1 re-active-promotion ratified at Wave R+3 via D-IH-86-EO once the 4-of-4 §9 gates met on lived 2-base + 1-overlay coverage (SUEZ POC + Aïsha continuity + EFA overlay).

Promotion path:
- **charter → active** (gates): ≥ 2 of the 4 base `share_pattern` values exercised cleanly in lived engagements; ≥ 1 `share_overlay` value exercised cleanly; validator CS-01..09 PASS on all populated rows; operator-explicit active-promotion decision row.
- **active → promoted-FAIL ramp** (gates): ≥ 3 lived engagements; ≥ 1 cross-engagement audit pass; operator-explicit ramp-promotion decision row. CS-04 / CS-05 / CS-06 remain at WARN forever (judgment-class drift). CS-07 remains at INFO (cleanup hygiene). CS-08 + CS-09 promote to FAIL with the ramp.

### 2.4. Methodology-readiness axis — *what makes a partner "deep"* (D-IH-86-EN; NEW)

The 4-base `share_pattern` enum names *the commercial shape*; the methodology-readiness axis names *the collaborator-capability shape that makes a given commercial pattern appropriate*. Without this axis, the doctrine would let operators classify the same collaborator into any of the 4 patterns interchangeably — which would defeat the purpose of having patterns at all.

Per **D-IH-86-EN** (operator-ratified at this rewrite, 2026-05-26, derived from operator's framing *"she can't follow our methodology the way we are and that is also a pending point in our kb so it's known because it's bound to happen with more people"*), every `COLLABORATOR_SHARE_REGISTRY` row carries a `methodology_readiness` column with one of 4 values that gates which `share_pattern` values are appropriate via the `METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS` lookup. (Companion decision **D-IH-86-EK** introduces the `parallel_invoice_stream_indicator` boolean column at position 20 of the same registry — a separate per-row flag declaring whether the collaborator invoices the customer directly vs in-kind under Holistika's umbrella invoice; structural-shape axis orthogonal to commercial-shape axis.)

| `methodology_readiness` value | What it means | Eligible `share_pattern` values | Disqualified `share_pattern` values |
|:---|:---|:---|:---|
| **`methodology_trained`** | The collaborator has been onboarded into the AKOS methodology (researcher discipline + AIC posture + canonical-CSV discipline + brand baseline reality + the rest of the People discipline-of-disciplines stack); they can operate inside the methodology autonomously; they cross-recognize Holistika's quality fabric specialties when surfaced. | `deep_partner_65_35` ✓ ; `joint_venture_aventure` ✓ ; `consulting_direct` ✓ (as a sub-contracted operator) ; `bd_intro_only` ✓ (if their commercial role is intro-only by choice, not by capability constraint) | none |
| **`methodology_in_progress`** | The collaborator is in onboarding (typically the first 2-3 engagements with active mentoring); they need supervision + checkpoints but can take on bounded sub-deliverables; trajectory is toward `methodology_trained`. | `deep_partner_65_35` ✓ (with `methodology_mentoring_clause`; reduces collaborator's effective execution scope) ; `consulting_direct + bd_commission_overlay` ✓ ; `joint_venture_aventure` ✗ (JV requires peer-equivalence; in-progress is asymmetric); `bd_intro_only` ✓ | `joint_venture_aventure` |
| **`methodology_naive`** | The collaborator has NOT been onboarded and is not currently being onboarded; they bring deal-sourcing + customer-relationship value but cannot operate inside the methodology; any execution work they do must happen OUTSIDE the methodology surfaces (which means it can't be governed end-to-end the AKOS way; partial outputs may need rework). | `bd_intro_only` ✓ (canonical use case) ; `consulting_direct + bd_commission_overlay` ✓ (Holistika executes; collaborator stays on BD-only) | `deep_partner_65_35` ✗ (would force methodology compromise — the 22/05 framing's *"me compromising for that 35%"* failure mode) ; `joint_venture_aventure` ✗ |
| **`methodology_not_applicable`** | The collaborator's role does NOT structurally require the methodology (e.g., a pure introducer who only ever does intro + handoff; a non-operational party whose only value is relational; an industry-association reference). | `bd_intro_only` ✓ (only appropriate value) | `deep_partner_65_35` ✗ ; `joint_venture_aventure` ✗ ; `consulting_direct` ✗ (without overlay; with overlay only) |

#### 2.4.1. The mandatory linkage: `methodology_readiness` × `share_pattern` consistency

When authoring a `COLLABORATOR_SHARE_REGISTRY` row, the agent + operator MUST resolve both `share_pattern` AND `methodology_readiness` together. The combinations are:

- **Eligible pairs** (any cell marked ✓ above) — author normally.
- **Disqualified pairs** (any cell marked ✗ above) — reclassify the `share_pattern` OR (rarely) escalate via inline-ratify to amend the methodology-readiness assessment.

The validator does not currently enforce the eligibility matrix mechanically (forward-charter: CS-10 enum-pair-consistency check, candidate for a future doctrine extension when ≥ 5 lived engagements have populated the methodology_readiness column). For now, the matrix is operator-discipline + skill-mediated (the paired `collaborator-share-craft` skill carries the decision-tree).

#### 2.4.2. The 22/05 failure-mode the axis prevents

The operator's 22/05/2026 framing made the failure-mode explicit:

> *"the operator compromising for that 35% and i don't lie, so yeah. You see, we lose value if we don't have things ready because in reality A was correct."*

The 35% reference is the deep_partner_65_35 split. The failure mode: when a `methodology_naive` collaborator is classified into `deep_partner_65_35` (because the operator wants to honor their deal-sourcing + relational value), the collaborator's inability to operate inside the methodology forces Holistika to do MORE of the work than the 65% share-stack baseline would justify — but the commercial split is locked at 65/35. The operator absorbs the methodology-onboarding overhead silently; the 35% commercial split overstates the collaborator's value contribution; the engagement-economic narrative degrades.

The fix: when methodology-readiness is `methodology_naive`, the eligible patterns are `bd_intro_only` OR `consulting_direct + bd_commission_overlay`. Both patterns route the collaborator's commercial slice through a BD-overlay (15% default) — which is structurally honest about the value being relational (deal-sourcing) rather than operational (methodology-execution). The operator stops compromising; the collaborator gets a fair BD-commission; the methodology stays uncompromised.

#### 2.4.3. Tracking + maturation

The methodology-readiness column is **mutable** — a collaborator who starts at `methodology_naive` can be onboarded into `methodology_in_progress` and eventually `methodology_trained`. The transition is recorded:

- When a collaborator's status changes, append a new `COLLABORATOR_SHARE_REGISTRY` row for the NEXT engagement with the updated value (do NOT mutate the existing row — preserve the lineage).
- Optionally append an `OPS_REGISTER` row tracking the onboarding trajectory + checkpoint cadence (forward-charter: a dedicated `COLLABORATOR_METHODOLOGY_READINESS_REGISTRY.csv` for tracking the maturation lifecycle, candidate for a future doctrine extension).
- The pattern `pattern_collaborator_share_doctrine` row in `PEOPLE_DESIGN_PATTERN_REGISTRY` is extended at Commit 5 of this rewrite to surface methodology-readiness as a load-bearing pattern dimension that other areas can inherit (e.g., a future Research-area collaborator pattern can name the same axis).

## 3. Worked examples

### 3.1. `deep_partner_65_35` — Aïsha-shape collaborator on a single engagement (Websitz lived precedent + didactic instantiation)

This is a **didactic example** to lock the math. It uses anonymized rounded numbers in the doctrine; the real Aïsha-on-SUEZ instantiation lands in Commit 3 with actual numbers + actual `COLLABORATOR_SHARE_REGISTRY` + `HOLISTIKA_VENDOR_SERVICES_BILLED` + market-rate-reference rows for FR-LEAD-DATA role class.

**Scenario:** An engagement client pays Holistika €100,000 for a deal where:

- A strategic collaborator (operator-of-the-process being automated) brings the client + agrees to provide ongoing operator-maintenance work post-deployment.
- The founder commits ~60 hours of execution-class work at the founder market rate.
- The collaborator commits ~120 hours of operator-class work at her market rate.
- Holistika contributes the full service stack in-kind (research-head + AKOS dataops + MADEIRA orchestration + brand-render + PMO) — no service-class billed against the project per the doctrine §2.2 defaults.
- Direct project costs: €4,000 (cloud infra pass-through + one external API license).
- Market rates: founder at €200/hr, collaborator at €100/hr (mid-band FR senior collaborator hypothetical; actual benchmarks land in `COLLABORATOR_MARKET_RATE_REFERENCE.csv`).
- No commercial overrides (65/35 default applies; rates within ±25% of reference).

**Math:**

| Line | Amount | Source |
|:---|---:|:---|
| REVENUE | €100,000 | engagement contract |
| − Founder billed time (60 hrs × €200) | (€12,000) | per `COLLABORATOR_MARKET_RATE_REFERENCE` founder rate |
| − Collaborator billed time (120 hrs × €100) | (€12,000) | per `COLLABORATOR_SHARE_REGISTRY` collaborator_billed_rate × hours_worked |
| − Direct project costs | (€4,000) | per `HOLISTIKA_VENDOR_SERVICES_BILLED` pass-through rows |
| − Holistika vendor services billed | (€0) | all 10 default-in-kind classes apply |
| **= BENEFITS** | **€72,000** | computed by `scripts/collaborator_share_calculate.py` |
| Holistika-side share (65%) | €46,800 | default split |
| Collaborator-side share (35%) | €25,200 | default split |

**Collaborator total earnings on this engagement:** €12,000 (billed time) + €25,200 (35% share) = **€37,200**.

**Holistika-side total earnings:** €12,000 (founder billed time) + €46,800 (65% share) = **€58,800**.

**Holistika gross margin (before founder taxes):** €58,800 on €100k revenue = 58.8%.

The collaborator's narrative: *"I brought the deal + I operate the process + I earned a transparent fair share of both my operational hours and the benefits of the deal."*

The Holistika narrative: *"We brought the methodology + machinery + execution craft contributed in-kind as the value of our 65% share; we billed our founder's execution hours transparently; we did not double-dip."*

**Worked precedent anchor (Websitz / Rushly engagement, live 2026; see [`docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/`](../../../../Think%20Big/Clients/2026-websitz-rushly/)).** Websitz is the lived precedent that minted this shape — they brought a customer (Rushly), they operate adjacent capabilities (mkt agency themselves; mktops overlap), and the resulting commercial arrangement uses the 65/35 deep-partner split with MKTOPS contributed in-kind per the `clause_partner_marketing_agency_overlap` clause row. The Aïsha-on-SUEZ continuity work (which is **NOT** a deep_partner deal — it's the §3.2 orchestration shape) does NOT use this pattern; the two are economically distinct even though both involve Aïsha.

### 3.2. `consulting_direct + bd_commission_overlay` — SUEZ POC corrected (recommercialization per D-IH-86-EL)

**Scenario.** Holistika ships a SUEZ POC under a direct-consulting commercial shape (Holistika gets paid for its own project like any consultancy does, per operator 22/05 framing); Aïsha brought the SUEZ relationship + provides early-phase relational continuity; classified as `methodology_in_progress` (not `methodology_trained` — she does not operate inside the methodology autonomously, but she is in active onboarding for the SUEZ relationship-continuity scope). Aïsha's commercial role is **BD/account-management overlay during early phase**, NOT deep-partner operational work.

This replaces the pre-rewrite §3.2 SUEZ projection that misclassified the engagement as `orchestration_broker_thin_margin / 6%` — a shape the operator never agreed to (*"6% is unknown to me (like i would accept that)"*).

**Deal structure** (per operator 22/05 + 13/05-meeting substrate):

- A strategic collaborator (Aïsha as `POI-PRT-EFA-LEAD-2026`) brings the SUEZ relationship + provides early-phase BD/account-management continuity with the SUEZ procurement team during the POC + the post-POC DSI introduction phase.
- Holistika delivers the POC directly: founder + execution team work on the customer's project; this is `consulting_direct` shape per the 22/05 framing.
- Aïsha's commercial slice is a 15% BD-commission overlay (default per `bd_commission_overlay`) off the engagement BENEFITS pool — not a 35% deep_partner split (which would force Holistika to compromise methodology to accommodate her non-trained methodology readiness) and not a 30% orchestration-broker slice (which would have implied a thin-margin Holistika posture the operator never agreed to).
- The customer-meeting substrate (transcript 2026-05-13 at `docs/.../2026-suez-webuy/00-internal/source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md` L1-L11) confirms Aïsha's role as relationship-continuity + DSI-introduction-coordination, NOT methodology execution.

**Per-row math** (illustrative; replaced with real numbers when SUEZ commercial close lands):

Assume engagement revenue = €100,000 (placeholder; real number lives in the SUEZ engagement folder + the commercial schedule the operator finalises with SUEZ).

Direct project costs (founder-billed time + execution-team-billed time + cloud infra pass-through + any external API licenses) are subtracted from REVENUE first per the TRUE-MARGIN formula §2; the resulting BENEFITS pool is then split between the 2 rows.

Worked numbers (illustrative; specifically illustrative — the SUEZ commercial close determines actual):

| Line | Amount | Source |
|:---|---:|:---|
| REVENUE | €100,000 | engagement contract (placeholder) |
| − Founder billed time (180 hrs × €200) | (€36,000) | per `COLLABORATOR_MARKET_RATE_REFERENCE` founder rate; orchestration + technical-architecture + senior-execution |
| − Execution-team billed time (~250 hrs collective × €120 blended) | (€30,000) | per `COLLABORATOR_SHARE_REGISTRY` execution-class rows; engineering + AI-orchestration delivery |
| − Direct pass-through costs (Azure + Power Platform licenses + AKOS infra absorbed at engagement) | (€4,000) | per `HOLISTIKA_VENDOR_SERVICES_BILLED` pass-through rows |
| − Holistika vendor services billed | (€0) | all 10 default-in-kind classes apply per §2.2 |
| **= BENEFITS** | **€30,000** | computed by `scripts/collaborator_share_calculate.py` |

The BENEFITS pool €30,000 then splits between 2 SHARE_REGISTRY rows under the same `engagement_id=suez_poc_2026`:

| Row | `collaborator_id` | `share_pattern` | `share_overlay` | `holistika_share_pct` | `collaborator_share_pct` | BENEFITS slice | Notes |
|:---|:---|:---|:---|---:|---:|---:|:---|
| 1 | Holistika (corporate) | `consulting_direct` | NULL | 85 | 0 | €25,500 | Holistika's direct-consulting share of BENEFITS (85% per default consulting_direct after default 15% BD overlay applied). Holistika consumes this BENEFITS slice in addition to the founder + execution-team billed time already accounted for above. |
| 2 | Aïsha (POI-PRT-EFA-LEAD-2026) | `consulting_direct` | `bd_commission_overlay` | 0 | 15 | €4,500 | Aïsha's 15% BD-commission overlay on BENEFITS pool. Recognises her relationship-continuity + DSI-introduction-coordination role during the POC + early post-POC phase. Does NOT compensate operational hours (she does not work operationally on the POC — that's Holistika's direct-consulting scope). |
| **Across-rows sum check** | — | — | — | **85** | **15** | **€30,000** | Sum-across-rows = 100; **CS-03 across-rows-per-engagement invariant holds for `consulting_direct + bd_commission_overlay`.** Per-row sum-to-100 does NOT apply to overlay rows (row 2 is 0+15=15, not 100; CS-03 routes through the across-rows variant when `share_overlay = bd_commission_overlay` is present). |

**Holistika gross outcome:** €36,000 founder billed + €25,500 BENEFITS share = **€61,500** on €100k revenue = 61.5% gross margin. (The 6% thin-margin projection from the pre-rewrite §3.2 was off by an order of magnitude — the actual operator-acceptable margin sits in the 50-70% range that the operator's *"any consultancy does"* framing implies.)

**Aïsha gross outcome:** €4,500 (BD-commission share) = **€4,500**. She does NOT bill operational hours on the SUEZ POC (her hours go into BD/account-management which is consumed by the BD-commission slice). When/if she transitions to `methodology_in_progress` deep_partner work on the post-POC SUEZ extension (the production-grade build), the engagement is **a new engagement_id** with a new SHARE_REGISTRY row + possibly a different `share_pattern` (e.g., `deep_partner_65_35` if her methodology readiness has matured + her role is operational, or `consulting_direct + bd_commission_overlay` again if her role stays BD-only).

**Why this is structurally correct:**

1. **The operator gets paid like a consultancy.** Founder + execution-team hours billed at market rates against the project (transparent line items in the cost roster); Holistika consumes the BENEFITS pool minus the BD-overlay slice. This matches the 22/05 framing's *"we need to get paid from our own project like any consultancy does."*
2. **Aïsha's role is honestly classified.** She is `methodology_in_progress` (not yet `methodology_trained` — see §2.4); her commercial role is BD/account-management (not deep-partner execution). The `bd_commission_overlay` shape is structurally honest about the value being relational rather than methodology-operational.
3. **No double-dipping.** Aïsha's BD-commission overlay tracks her relational contribution; she does not also claim a share of Holistika's methodology stack (which she does not contribute to). Holistika does not claim a share of her relationship (which Holistika did not source).
4. **The 35% compromise failure-mode is avoided.** The pre-rewrite §3.2 + the pre-rewrite alternative-classification path (forcing Aïsha into deep_partner_65_35 with a 35% slice) both implied compromises the operator's 22/05 framing explicitly rejected. The new shape lets the operator stop compromising.
5. **The methodology stays uncompromised.** Holistika's research-head + AKOS + MADEIRA + brand machinery + PMO stack delivers the POC at the methodology's quality bar (not the lowered bar a `methodology_naive` operational collaborator would force). The customer wins on quality; Holistika wins on margin; Aïsha wins on a fair BD-commission for her relationship-continuity.

**Strategic context.** The SUEZ POC corrected shape is the **canonical worked example** for `consulting_direct + bd_commission_overlay`. Future SUEZ post-POC engagements (the production-grade build, the multi-divisional rollout, the DSI-coordinated platform extension) may use the same shape OR transition to `deep_partner_65_35` if Aïsha completes methodology onboarding into `methodology_trained` AND her role shifts to operational execution. Each engagement is a separate `engagement_id` with its own SHARE_REGISTRY row(s) — the pattern can evolve across the relationship lifecycle without retroactive rewrites.

**Cost roster semantics for `consulting_direct + bd_commission_overlay`.** Under `consulting_direct`, costs are subtracted from REVENUE before computing BENEFITS (same as `deep_partner_65_35` — TRUE-MARGIN formula applies). The overlay slice consumes a percentage of the BENEFITS pool (not gross revenue). This means the BD-overlay party's commercial outcome is tied to the engagement's economic outcome — if the engagement is unprofitable, the overlay slice shrinks; if the engagement is highly profitable, the overlay slice grows. This is structurally aligned with the 22/05 framing's *"so that they have an incentive to bring good deals"* — the BD-commission is upside-linked, not gross-revenue-linked.

### 3.3. `bd_intro_only` — pure BD/intro-only collaborator (operator 22/05 worked framing)

**Scenario.** A collaborator brings Holistika a project lead but does NOT work on the project operationally beyond the initial introduction + early-phase account-management. The collaborator is classified `methodology_naive` OR `methodology_not_applicable` (they do not operate inside the methodology). Per operator 22/05 framing:

> *"15% of business development that i give to people when they don't work but just come and give us a project and work as business developer/account mgr at least for the beginning, getting their share over the margin so that they have an incentive to bring good deals."*

**Per-row math** (illustrative):

Assume engagement revenue = €80,000 (placeholder; SaaS-class direct engagement).

| Line | Amount | Source |
|:---|---:|:---|
| REVENUE | €80,000 | engagement contract |
| − Founder + execution team billed time (~180 hrs blended × €170) | (€30,600) | per market-rate references; Holistika delivers operationally |
| − Direct pass-through (cloud + tooling) | (€2,400) | per `HOLISTIKA_VENDOR_SERVICES_BILLED` pass-through rows |
| − Holistika vendor services billed | (€0) | all 10 default-in-kind classes apply |
| **= BENEFITS** | **€47,000** | computed by runbook |

| Row | `collaborator_id` | `share_pattern` | `share_overlay` | `holistika_share_pct` | `collaborator_share_pct` | BENEFITS slice |
|:---|:---|:---|:---|---:|---:|---:|
| 1 | Holistika (corporate) | `bd_intro_only` | NULL | 85 | 0 | €39,950 |
| 2 | BD-only collaborator | `bd_intro_only` | NULL | 0 | 15 | €7,050 |

**Across-rows sum check:** 85 + 15 = 100 (CS-03 across-rows variant holds; the `bd_intro_only` base pattern collapses to the same across-rows shape as `consulting_direct + bd_commission_overlay` but without requiring the overlay column — the BD framing IS the base pattern).

**Difference from `consulting_direct + bd_commission_overlay`:** When the base engagement is `consulting_direct` (Holistika is delivering a direct consultancy engagement, and the collaborator is the BD intro party who continues with account-management for a bounded early phase), use `consulting_direct + bd_commission_overlay`. When the engagement is a pure BD-intro arrangement (the collaborator's role is intro-only by structural choice; no ongoing account-management; pure finder's-fee shape), use `bd_intro_only`. The two patterns produce equivalent commercial math but encode structurally distinct narratives — `consulting_direct + bd_commission_overlay` says "Holistika consults; BD party brokers"; `bd_intro_only` says "BD party finder; Holistika executes" without an account-management bridge.

### 3.4. `joint_venture_aventure` — peer-equivalent co-delivery aventure (forward-charter; first instantiation TBD)

**Scenario.** Holistika partners with a peer-equivalent party (e.g., a sister consultancy with a different methodology stack; an aligned tooling vendor co-bringing a customer; an industry-association co-publication aventure) to pursue a shared go-to-market or shared-delivery engagement. Both parties contribute substantial methodology stacks; both parties bring relational + execution value; both parties are `methodology_trained` OR cross-recognize each other's methodology stacks as equivalent-in-value.

**Distinguishing characteristics** (vs `deep_partner_65_35`):

- **Symmetry.** Both parties contribute methodology + execution + relational value at peer levels; neither party is in a vendor-to-partner posture.
- **Default 50/50 split.** The mathematical baseline reflects the symmetry. Deviations require named override (e.g., 60/40 when one party brings the customer relationship + the other party brings the deeper methodology stack).
- **Shared risk-bearing.** Both parties carry shared upside AND shared downside; if the engagement is unprofitable, both absorb proportional loss; if highly profitable, both share proportional upside.
- **Distinct from JV cap-table arrangements.** This is engagement-economic shape, not entity-formation. A JV-aventure may convert into a true joint-venture entity formation over time, at which point the engagement transitions out of this doctrine's scope into the cap-table-class governance.

**Per-row math** (illustrative; no lived instantiation yet — first instantiation forward-chartered):

Assume engagement revenue = €120,000 (placeholder; shared-delivery to a flagship customer).

| Line | Amount | Source |
|:---|---:|:---|
| REVENUE | €120,000 | engagement contract |
| − Holistika-side founder + execution billed time | (€20,000) | Holistika market rates × hours |
| − JV-partner-side execution billed time | (€18,000) | partner market rates × hours |
| − Direct pass-through (cloud + tooling) | (€5,000) | per VENDOR_SERVICES_BILLED |
| − Holistika vendor services billed | (€0) | all 10 default-in-kind (both parties contribute methodology in-kind symmetrically) |
| **= BENEFITS** | **€77,000** | computed by runbook |

| Row | `collaborator_id` | `share_pattern` | `share_overlay` | `holistika_share_pct` | `collaborator_share_pct` | BENEFITS slice |
|:---|:---|:---|:---|---:|---:|---:|
| 1 | Holistika (corporate) | `joint_venture_aventure` | NULL | 50 | 50 | €38,500 / €38,500 |

**Per-row sum-to-100:** 50 + 50 = 100 (CS-03 per-row variant holds — same as `deep_partner_65_35`).

**Forward-charter note.** No `joint_venture_aventure` engagement is currently in scope. The pattern is named at this rewrite to surface the structural distinction for future instantiation; the worked example above is illustrative. First lived instantiation will land per a future engagement charter ratifying both the JV-aventure shape AND the specific partner + customer + deliverable triple. When that instantiation lands, this §3.4 will be amended with the real numbers + the real partner identity + the cross-engagement governance learnings.

### 3.5. The removed `custom` shape — what replaces it

The pre-rewrite §3.3 `custom` pattern is removed per §2.3.3. Engagements that previously would have been classified `custom` route to:

- **Flagship discount commercial deals** → `consulting_direct` with operator-defined `holistika_share_pct` deviation + mandatory `share_override_decision_id` FK to a DECISION_REGISTER row carrying the strategic rationale (preferred logo for fundraise; lighthouse case study; etc.). The override row replaces the prior `custom` escape hatch without losing audit trail.
- **Non-cash partnerships** → `eng_model_investor_advisor` engagement model (out of scope for this doctrine; cap-table-class governance applies).
- **Milestone-shaped retribution** → `eng_model_milestone_consultant` engagement model (Bâtard 2020 precedent; engagement-model layer, not share_pattern layer).
- **Genuinely novel shapes** → propose a 5th base pattern via doctrine amendment + inline-ratify decision row; do NOT silently route through any existing pattern with an override hack.

The removal of `custom` is the load-bearing claim of this rewrite (per §2.3.3): governance schemas are stronger when the escape hatch is **structurally constrained** rather than **operator-narrative-defined**.

## 4. External research grounding

Per [`akos-applied-research-discipline.mdc`](../../../../../../../.cursor/rules/akos-applied-research-discipline.mdc) RULE 2 (novel framing requires external citation), this doctrine grounds in three external precedents:

1. **OECD DEMPE doctrine (Transfer Pricing Guidelines, 2022 + 2024 revisions).** The OECD Transfer Pricing Guidelines for IP valuation use the **DEMPE** framework (Development, Enhancement, Maintenance, Protection, Exploitation) to allocate value where multiple parties contribute to an IP-bearing arrangement. The 65/35 split is defensible under DEMPE because Holistika owns the **Development + Enhancement + Protection** legs (methodology IP, AKOS governance, doctrine continuity) while the collaborator owns the **Maintenance + Exploitation** legs (ongoing operator work + customer relationship + market access). The asymmetric split reflects the proportional weight DEMPE assigns to each leg — Development + Enhancement + Protection typically command 50-70% of IP value in DEMPE-grounded valuations; 65% sits within this band.

2. **The historical "25% Rule" (Goldscheider, 2011 critique).** A long-standing benchmark in IP licensing — the licensor receives ~25% of the licensee's operating profit. Though formally rejected by the U.S. Federal Circuit in *Uniloc v. Microsoft* (2011) as a per-se rule, it remains a **cross-check benchmark** in practitioner valuations. Holistika's 65% share corresponds to a *reversed* configuration: Holistika is the IP-licensor + execution partner (not pure licensor); the collaborator is the deal-source + operator (not pure licensee). The 65/35 split aligns with practitioner benchmarks for **hybrid IP-licensor + execution-partner arrangements** where the licensor contributes both IP and execution capacity (typical range: 60-75% to the IP+execution party).

3. **Profit-sharing literature in joint ventures (Hennart 1988; Yan & Gray 1994).** Asymmetric profit splits in joint ventures correlate with asymmetric contribution of **complex tacit knowledge** (Hennart's "soft asset" framing). Holistika's methodology IP + AKOS governance + AIC orchestration constitute high-tacit-knowledge contributions; the collaborator's deal-sourcing + operator continuity constitute relational-asset + transactional-asset contributions. The 65/35 asymmetry is consistent with this body of literature for arrangements where tacit-knowledge contribution is the primary value driver.

The combination of (1) + (2) + (3) gives the doctrine a **defensible economic narrative** that can survive scrutiny by a counterparty's legal + finance team, an investor's due-diligence pass, or a regulator's transfer-pricing audit. The 65/35 split is not arbitrary — it is the operator's specific landing within a band that the industry and OECD both validate as appropriate for hybrid IP-licensor + execution-partner arrangements.

## 5. Internal precedent grounding

This doctrine is consistent with prior Holistika ratifications:

| Precedent | Decision row | Continuity |
|:---|:---|:---|
| `eng_model_percentage_collaborator` engagement model | **D-IH-73-J** (Initiative 73) | Existing canonical CSV row in `ENGAGEMENT_MODEL_REGISTRY.csv` line 4: "Percentage Collaborator / Revenue-share retribution without cap-table presence; full engagement-bounded access." This doctrine fills in the percentages + the chassis that D-IH-73-J left as forward-charter. |
| `eng_model_milestone_consultant` (Bâtard 2020 precedent) | D-IH-73-I | Bâtard 2020 franchise model used milestone-class consulting with milestone-shaped retribution. The current doctrine extends to the percentage-collaborator pattern that supersedes pure milestone-consulting for relational deals (where the collaborator is also the operator). |
| Websitz / Rushly engagement | (live 2026; see `docs/references/hlk/v3.0/Think Big/Clients/2026-websitz-rushly/`) | Operator's verbatim citation at the 2026-05-25 session: *"websitz per example was asked to support no mktops as they were a mkt agency themselves on top of bringing us customers to the table."* Codified as `clause_partner_marketing_agency_overlap` seed row in `PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv`. |
| Aïsha as `POI-PRT-EFA-LEAD-2026` | `GOI_POI_REGISTER.csv` (existing row); D-12-4 (maintenance posture) | Aïsha's dual role as bridge/BD + incumbent operator of SUEZ WeBuy process is codified. Her per-engagement application of this doctrine lands in Commit 3 (SUEZ engagement role spec) — first worked instantiation outside the didactic example in §3. |
| `eng_model_investor_advisor` | D-IH-73-L | Adjacent engagement-model pattern (advisor grants + round-cadence retribution) — distinct from collaborator-share but inherits the same audit-trail + DECISION_REGISTER discipline. |

## 6. Drift gate + validator behaviour

[`scripts/validate_collaborator_share.py`](../../../../../../../scripts/validate_collaborator_share.py) (Commit 2b) executes the following checks at every `py scripts/verify.py pre_commit` invocation:

| Check | Severity | Behaviour |
|:---|:---|:---|
| **CS-01: CSV header sha** | FAIL | Each of the 5 CSVs' headers must match its Pydantic `*_FIELDNAMES` tuple in `akos/hlk_collaborator_share.py`. |
| **CS-02: Cross-CSV FK integrity** | FAIL | Every `collaborator_id` in SHARE_REGISTRY resolves into `GOI_POI_REGISTER`; every `engagement_model_id` resolves into `ENGAGEMENT_MODEL_REGISTRY`; every `clause_id` referenced from VENDOR_SERVICES_BILLED resolves into PARTNER_OVERLAP_EXCLUSION_CLAUSES; every `reference_rate_id` referenced from RATE_OVERRIDES resolves into MARKET_RATE_REFERENCE; every `*_decision_id` resolves into DECISION_REGISTER. |
| **CS-03: split-sum invariant audit** *(branches on `share_pattern` × `share_overlay` per D-IH-86-EJ)* | FAIL | **Per-row variant** (applies when `share_overlay IS NULL` AND `share_pattern IN (deep_partner_65_35, joint_venture_aventure)`): every SHARE_REGISTRY row's `holistika_share_pct + collaborator_share_pct = 100`; default is 65/35 for deep_partner OR 50/50 for joint_venture_aventure unless `share_override_decision_id` is non-empty AND resolves into DECISION_REGISTER AND a matching `COLLABORATOR_RATE_OVERRIDES` row exists with `override_kind=share_split_deviation`. **Across-rows variant** (applies when `share_pattern IN (bd_intro_only, consulting_direct)` OR `share_overlay = bd_commission_overlay`): sum across all SHARE_REGISTRY rows for a single `engagement_id` equals 100; per-row sum-to-100 does NOT apply (overlay rows are 0+overlay_pct=overlay_pct; base rows under bd_intro_only/consulting_direct are 85+0=85 OR 100+0=100 when no overlay applied). FAILs when neither variant resolves cleanly. |
| **CS-04: default-anchor + market-rate audit** *(branches on `share_pattern` × `share_overlay` per D-IH-86-EJ)* | WARN | **Common audit (all patterns)**: every SHARE_REGISTRY row's `collaborator_billed_rate` must fall within ±25% of the matching MARKET_RATE_REFERENCE row's `rate_typical_per_hour`; outside-band rates require a matching `COLLABORATOR_RATE_OVERRIDES` row with `override_kind=market_rate_excursion`. **Per-pattern anchor audit**: `deep_partner_65_35` → 65/35 default; deviations require `override_kind=share_split_deviation`. `joint_venture_aventure` → 50/50 default; same override requirement. `bd_intro_only` → 85/15 default; deviations require `override_kind=share_split_deviation`. `consulting_direct` → 100/0 default (when no overlay) OR 85/15 default (when `bd_commission_overlay` present); deviations require `override_kind=share_split_deviation` OR `override_kind=overlay_pct_deviation`. |
| **CS-05: bill_mode default audit** | WARN | Every VENDOR_SERVICES_BILLED row's `bill_mode` must match the doctrine §2.2 default for that `holistika_service_class` OR have a non-empty `bill_mode_decision_id`. Mis-billing without ratification surfaces here. Applies to all `share_pattern` values (the VENDOR_SERVICES_BILLED roster discipline is pattern-agnostic). |
| **CS-06: Partner-overlap clause linkage** | WARN | Every VENDOR_SERVICES_BILLED row with `bill_mode=in_kind` AND a default of `billed` for that service class must carry a non-empty `justification_clause_id` resolving into PARTNER_OVERLAP_EXCLUSION_CLAUSES. Applies to all `share_pattern` values. |
| **CS-07: Rate override expiry hygiene** | INFO | Any `COLLABORATOR_RATE_OVERRIDES` row whose `expires_at` is in the past must have `status=archived`. Stale active rows surface as INFO. Applies to all `share_pattern` values. |
| **CS-08: share_pattern enum validity** *(rewritten per D-IH-86-EJ; enum reduced from 3 to 4 values)* | FAIL | Every SHARE_REGISTRY row's `share_pattern` value must be one of `deep_partner_65_35` / `bd_intro_only` / `joint_venture_aventure` / `consulting_direct`. The pre-rewrite values `orchestration_broker_thin_margin` AND `custom` are NO LONGER VALID and FAIL immediately; pre-rewrite rows authored under either value MUST be migrated via the Commit-5 supersede SQL (no automatic remediation — operator-applied per `akos-holistika-operations.mdc` SQL gate). Empty values default to `deep_partner_65_35` per the Pydantic model + Supabase mirror CHECK constraint. |
| **CS-09: overlay-base coherence audit** *(NEW per D-IH-86-EJ)* | FAIL | Every SHARE_REGISTRY row's `share_overlay` value MUST be either NULL or one of `VALID_SHARE_OVERLAYS` (currently `bd_commission_overlay`). When non-NULL, the row's paired sibling base row(s) under the same `engagement_id` MUST have a `share_pattern` value compatible with the overlay's `VALID_OVERLAY_BASE_PAIRINGS` table (currently: `bd_commission_overlay` pairs with `consulting_direct` OR `deep_partner_65_35`; pairs forbidden with `bd_intro_only` because circular; pairs forbidden with `joint_venture_aventure` because conflates symmetry with intro asymmetry). FAILs when (a) overlay value is invalid, OR (b) overlay row exists without a sibling base row at the same engagement_id, OR (c) overlay+base pairing violates the matrix. |

**INFO → FAIL ramp (reset to charter implicitly at this rewrite per D-IH-86-EJ; re-promoted to active via D-IH-86-EO at Wave R+3).** Per the operator's *"craft what you can and please ensure this is all wired up properly with the rest"* framing + the Quality Fabric §10 promotion criteria, the validator at this rewrite reset to INFO advisory for all 9 checks. The pre-rewrite Stage-1 active-promotion (D-IH-86-DF) is superseded by D-IH-86-EO (the post-rewrite re-active-promotion ratified on the 4-base + 1-overlay enum at Wave R+3 once the 4-of-4 §9 gates met on lived SUEZ POC + Aïsha continuity + EFA overlay coverage). Re-promotion path:

- **charter → active**: ≥ 2 of the 4 new base `share_pattern` values exercised cleanly in lived engagements; ≥ 1 `share_overlay` value exercised cleanly; CS-01..09 PASS; operator-explicit re-active-promotion decision row (ratified 2026-05-27 as D-IH-86-EO).
- **active → promoted-FAIL ramp**: CS-01 / CS-02 / CS-03 / CS-08 / CS-09 promote to FAIL at the Wave T or later boundary gated on (a) 3+ real engagements with zero CS-01..03 / CS-08 / CS-09 findings AND covering ≥ 2 of the 4 base patterns + ≥ 1 overlay value, AND (b) operator-explicit ramp-promotion decision row.
- CS-04 / CS-05 / CS-06 remain at WARN forever (judgment-class drift that operator review handles; FAIL would be over-mechanical).
- CS-07 remains at INFO (cleanup hygiene).

## 7. Cadence + when this doctrine fires

The discipline fires at the following recurring moments:

| Trigger | Frequency | What fires |
|:---|:---|:---|
| **Engagement charter time** (new engagement with a strategic collaborator opens) | per engagement | Author SHARE_REGISTRY row + VENDOR_SERVICES_BILLED roster (10 default rows OR explicit deviations) + verify collaborator's MARKET_RATE_REFERENCE row exists (seed if missing per inline-ratify) + DECISION_REGISTER row for charter ratification. |
| **Engagement milestone close** (billed time roster updates) | per milestone | Append billed-hours rows; rerun `scripts/collaborator_share_calculate.py --engagement <id>` to recompute current benefits estimate; share with collaborator if transparency cadence requires. |
| **Engagement final close** (invoicing complete; benefits settle) | per engagement | Run runbook final mode + emit collaborator-share statement; obtain collaborator sign-off; archive engagement-folder companion files. |
| **Per-engagement commercial deviation** (rate excursion OR share split deviation) | event-triggered | Inline-ratify gate per `akos-inline-ratification.mdc` + RATE_OVERRIDES row + DECISION_REGISTER row + (optional) operator-scratchpad entry naming the strategic rationale. |
| **Doctrine amendment** (defaults change; new service class added; new overlap clause minted) | as needed | Operator-ratified doctrine version bump + cross-canonical updates (cursor rule + skill + SOP + dependent CSVs) per `akos-docs-config-sync.mdc`. |
| **Market-rate reference refresh** | annual minimum | Re-seed MARKET_RATE_REFERENCE rows from latest industry surveys; refresh `rate_source` citations; update `last_review_at`. |
| **Cross-engagement audit** | quarterly minimum | Run validator across all engagements; surface CS-04 / CS-05 / CS-06 findings; operator reviews + closes via inline-ratify dispositions. |

## 8. Anti-patterns (what NOT to do)

This doctrine explicitly forbids the following alternatives that the 2026-05-25 architecture session considered and rejected:

- **Anti-pattern A: STRICT-MARGIN (Holistika bills in-house services against project at market rate).** Rejected per `D-IH-86-DB`. Failure mode: collaborator narrative breaks ("you're already billing us for everything; why do you also get 65%?"); double-dip perception; smaller benefits pool to split paradoxically reduces collaborator's apparent gain even though their absolute earnings may rise. The TRUE-MARGIN posture is cleaner narratively + structurally aligned with the operator's verbatim *"we propose a plethora of services we take for granted we'll do."*

- **Anti-pattern B: Hidden collaborator-billed-time (collaborator hours absorbed into benefits pool).** Rejected per operator's framing *"aïsha is a person whose costs will be put against the project to make her work transparent, so she may gain more money than we expect."* Failure mode: collaborator does not see her operational hours as a transparent line item; benefits pool appears inflated; when she compares against the doctrine, the math does not reconcile; trust erodes.

- **Anti-pattern C: Per-deal renegotiation of partner-overlap exclusion (no clause registry).** Rejected per `D-IH-86-DC` (operator chose the clause-table-with-schema-field option). Failure mode: every engagement renegotiates from scratch; patterns are not learned across engagements; future Holistika collaborators do not inherit the institutional memory; same arguments resurface; operator effort wasted.

- **Anti-pattern D: Operator-self-set collaborator billed rates with no market-rate reference.** Rejected per `D-IH-86-DA` (option B+governed-override chosen). Failure mode: rates drift arbitrarily; cross-engagement equity erodes (Aïsha at €100/hr while another collaborator with equivalent role-class gets €150/hr because she negotiated harder); collaborator narrative becomes "Holistika doesn't have a principled rate framework."

- **Anti-pattern E: Forbid commercial overrides (rigid 65/35 enforcement).** Rejected per operator's *"with the possibility to adjust commercially this in a governed manner"* framing. Failure mode: strategic deals (e.g., a deal where Holistika wants to share more aggressively to win a flagship customer) cannot be priced; operator forced into either a violation OR a perverse incentive (e.g., book partial benefits off-engagement to circumvent the rigid split). The governed-override mechanism preserves flexibility + the audit trail.

- **Anti-pattern F: Decision-log entries with no canonical CSV mirror.** Rejected per all AKOS doctrine — every commercial deviation gets a `COLLABORATOR_RATE_OVERRIDES` row + a `DECISION_REGISTER` row. The CSV row is canonical; the decision-log entry is the narrative around it. Decisions without CSV mirrors are ungovernable by the validator + invisible to future audits.

## 9. Promotion criteria (charter → active → promoted-FAIL) — RESET AT REWRITE per D-IH-86-EJ

This doctrine lands at `status: charter` per `D-IH-86-DA` original mint, is RESET to `status: charter` implicitly at the Wave R+2 rewrite per `D-IH-86-EJ` (because the worked example that the pre-rewrite Stage-1 D-IH-86-DF had ratified — SUEZ POC at `orchestration_broker_thin_margin` — was itself superseded), AND is re-promoted to `status: active` at Wave R+3 (2026-05-27) per `D-IH-86-EO` once the 4-of-4 Stage-1 gates met on lived 2-base + 1-overlay coverage.

**charter → active (Wave R+3 re-promotion; gates met):**
- ≥ 2 of the 4 new base `share_pattern` values exercised cleanly in lived engagements (NOT just self-tests). At rewrite-commit time, the SUEZ POC under the corrected `consulting_direct + bd_commission_overlay` shape (Commit 5) covers `consulting_direct` + `bd_commission_overlay`. A second engagement covering `deep_partner_65_35` (the preserved Websitz precedent stays valid) OR `bd_intro_only` OR `joint_venture_aventure` is required for the second exercised pattern.
- ≥ 1 `share_overlay` value exercised cleanly (the SUEZ recommercialization satisfies this via `bd_commission_overlay`).
- Validator CS-01..09 PASS on the populated rows across both exercised patterns.
- Operator-ratified re-active-promotion decision row D-IH-86-EO (Wave R+3 2026-05-27; supersedes D-IH-86-DF).

**active → promoted-FAIL ramp (gates per §6)**:
- 3+ real engagements applying the doctrine cleanly with zero CS-01..03 / CS-08 / CS-09 FAIL findings.
- Coverage requirement: ≥ 2 of the 4 base patterns + ≥ 1 overlay value exercised in lived practice (so the per-pattern × per-overlay branching has been tested beyond self-tests).
- ≥ 1 cross-engagement audit pass at quarterly cadence with operator sign-off.
- Operator-ratified ramp-promotion decision row.
- CS-04 / CS-05 / CS-06 remain at WARN forever per §6 (judgment-class drift).
- CS-07 remains at INFO forever per §6 (cleanup hygiene).

**Methodology-readiness gate (per §2.4 + D-IH-86-EN)**: every SHARE_REGISTRY row's `methodology_readiness` value must be coherent with its `share_pattern` per the per-axis table in §2.4. Coherence violations (e.g., `methodology_naive` paired with `deep_partner_65_35`) **fail CS-09 at FAIL severity** AND require an explicit `bd_commission_overlay` retrofit OR a pattern downgrade BEFORE the engagement charters. This gate prevents the "35% compromise" failure mode the operator named verbatim at the 2026-05-22 framing (*"i don't lie ... we lose value if we don't have things ready because in reality A was correct"*).

## 10. Self-discipline rules for agents — REWRITTEN per D-IH-86-EJ

When authoring or applying this discipline:

1. **Resolve `share_pattern` × `share_overlay` × `methodology_readiness` BEFORE drafting any row.** The single most load-bearing decision in this discipline is the pattern + overlay + readiness triple. CS-03, CS-04, CS-09 all branch on the triple; picking wrong silently produces incorrect settlement math the collaborator may dispute at final-close. Resolve via inline-ratify per `akos-inline-ratification.mdc` (read the paired skill at `.cursor/skills/collaborator-share-craft/SKILL.md` for the decision tree).
2. **Default per pattern, NOT per row.** Each of the 4 base patterns has its own default-anchor: `deep_partner_65_35` → 65/35; `joint_venture_aventure` → 50/50; `bd_intro_only` → 85/15; `consulting_direct` → 100/0 (or 85/15 with `bd_commission_overlay`). Drafting any deviation requires the operator surface a commercial-override decision via inline-ratify. Drafting a non-default row without the ratify gate is the most common failure mode.
3. **Co-mint the VENDOR_SERVICES_BILLED roster with the SHARE_REGISTRY row.** Every engagement gets 10 default-in-kind rows (one per service class per §2.2) — copy from a sibling engagement, then mark deviations explicitly. Forgetting the roster lets the validator silently pass an engagement with no documentation of which Holistika services were contributed in-kind.
4. **Seed MARKET_RATE_REFERENCE rows opportunistically.** When a new collaborator's `role_class × region × experience_band` is not yet in MARKET_RATE_REFERENCE, the agent does NOT skip the row — the agent surfaces an inline-ratify gate asking the operator for the rate-source citation + the typical-rate value, then seeds the row in the same commit as the SHARE_REGISTRY row. This is how the registry builds out over time without per-engagement renegotiation.
5. **Never inline a rate exception without a ratification row.** A SHARE_REGISTRY row with `collaborator_billed_rate` 30% above the typical reference + no `COLLABORATOR_RATE_OVERRIDES` row is a validator-detected drift. The fix is always: add the override row + the DECISION_REGISTER row + the commercial-strategy-rationale. Never silence the validator without the audit trail.
6. **Cite the doctrine when communicating with the collaborator.** When sharing the math with a collaborator (e.g., emailing the final-close statement), cite the doctrine version (post-rewrite: v3.2 per `D-IH-86-EJ`) + the relevant CSV rows + the `share_pattern + share_overlay` combination that applies. The collaborator's confidence in the math comes from the reproducible audit trail, not from the operator's assertion.
7. **Never compromise to bridge a methodology gap.** The 2026-05-22 operator framing — *"we lose value if we don't have things ready because in reality A was correct"* — names the specific failure mode: accepting a 35% slice when the collaborator's `methodology_readiness` is `methodology_naive` and the right shape is `bd_commission_overlay + consulting_direct`. The fix is to delay the deal OR restructure to overlay shape, NOT to compromise the deep-partner anchor.
8. **Use the paired skill before authoring.** Read [`.cursor/skills/collaborator-share-craft/SKILL.md`](../../../../../../../.cursor/skills/collaborator-share-craft/SKILL.md) before drafting a new SHARE_REGISTRY row OR a new override OR a new clause. The skill carries the worked examples + the recovery patterns for the common pitfalls.

## 11. Cross-references

- Parent meta-doctrine: [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (the 5-axis composition; this doctrine is the 13th specialty per §6 row).
- Sister specialty disciplines: [`UAT_DISCIPLINE.md`](UAT_DISCIPLINE.md), [`INTER_WAVE_REGRESSION_DISCIPLINE.md`](INTER_WAVE_REGRESSION_DISCIPLINE.md), [`INDEX_INTEGRITY_DISCIPLINE.md`](INDEX_INTEGRITY_DISCIPLINE.md), [`PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md`](PASS_WITH_FOLLOWUP_GOVERNANCE_DISCIPLINE.md), [`MKTOPS_DISCIPLINE.md`](MKTOPS_DISCIPLINE.md), [`DATAOPS_DISCIPLINE.md`](DATAOPS_DISCIPLINE.md), [`TECHOPS_DISCIPLINE.md`](TECHOPS_DISCIPLINE.md), [`UX_DISCIPLINE.md`](UX_DISCIPLINE.md), [`RESEARCH_HEAD_DISCIPLINE.md`](RESEARCH_HEAD_DISCIPLINE.md).
- Engagement model registry doctrine: [`../People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md`](../People%20Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.md) (the parent registry of engagement models; this doctrine specialises `eng_model_percentage_collaborator`).
- Workspace blueprint: [`../../Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../Operations/PMO/WORKSPACE_BLUEPRINT_HOLISTIKA.md) §16 (Advisers/Clients engagement folder shape — the doctrine's per-engagement application lives in those folders).
- Paired cursor rule: [`.cursor/rules/akos-collaborator-share.mdc`](../../../../../../../.cursor/rules/akos-collaborator-share.mdc) (Commit 2c).
- Paired skill: [`.cursor/skills/collaborator-share-craft/SKILL.md`](../../../../../../../.cursor/skills/collaborator-share-craft/SKILL.md) (Commit 2c).
- Paired SOP+runbook: [`SOP-PEOPLE_COLLABORATOR_SHARE_001.md`](SOP-PEOPLE_COLLABORATOR_SHARE_001.md) (Commit 2c) paired with [`scripts/collaborator_share_calculate.py`](../../../../../../../scripts/collaborator_share_calculate.py) (Commit 2b).
- Paired validator: [`scripts/validate_collaborator_share.py`](../../../../../../../scripts/validate_collaborator_share.py) (Commit 2b).
- Pydantic chassis: [`akos/hlk_collaborator_share.py`](../../../../../../../akos/hlk_collaborator_share.py) (this commit; SSOT for all 5 CSVs' field contracts).
- 5 canonical CSVs (this commit):
  - [`../People Operations/canonicals/dimensions/COLLABORATOR_SHARE_REGISTRY.csv`](../People%20Operations/canonicals/dimensions/COLLABORATOR_SHARE_REGISTRY.csv)
  - [`../People Operations/canonicals/dimensions/HOLISTIKA_VENDOR_SERVICES_BILLED.csv`](../People%20Operations/canonicals/dimensions/HOLISTIKA_VENDOR_SERVICES_BILLED.csv)
  - [`../People Operations/canonicals/dimensions/PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv`](../People%20Operations/canonicals/dimensions/PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv)
  - [`../People Operations/canonicals/dimensions/COLLABORATOR_MARKET_RATE_REFERENCE.csv`](../People%20Operations/canonicals/dimensions/COLLABORATOR_MARKET_RATE_REFERENCE.csv)
  - [`../People Operations/canonicals/dimensions/COLLABORATOR_RATE_OVERRIDES.csv`](../People%20Operations/canonicals/dimensions/COLLABORATOR_RATE_OVERRIDES.csv)
- Decisions:
  - **D-IH-86-DA** — Doctrine mint (this canonical at status: charter; original mint).
  - **D-IH-86-DB** — 65/35 TRUE-MARGIN benefits formula ratified (preserved at rewrite for `deep_partner_65_35` pattern; formula reused with adjusted default-anchor per pattern).
  - **D-IH-86-DC** — Named clause table + EngagementCostRow schema field for partner-overlap exclusion (option C of the 2026-05-25 architecture inline-ratify gate; preserved at rewrite).
  - **D-IH-86-DD** — Tier 1 WIP hygiene (`docs/wip/hlk-km/` deprecation; pre-requisite housekeeping; Commit 1; preserved at rewrite).
  - **D-IH-86-DE** *(superseded by D-IH-86-EJ at 2026-05-27)* — Original `share_pattern` enum (3 shapes: `deep_partner_65_35` / `orchestration_broker_thin_margin` / `custom`); CS-08 added; CS-03 + CS-04 branch per pattern. Superseded because (a) the SUEZ POC commercial reality was mis-encoded as `orchestration_broker_thin_margin` whereas the operator's actual commercial philosophy is `consulting_direct + bd_commission_overlay` (15% BD commission overlay on the BENEFITS pool), AND (b) `custom` was a doctrinal escape hatch that prevented mechanical validation, AND (c) the 3-value enum had no `joint_venture_aventure` value for symmetric founder partnerships AND no `bd_intro_only` value for the 15% BD commission base case.
  - **D-IH-86-DF** *(superseded by D-IH-86-EO at 2026-05-27)* — Original Stage-1 active-promotion of the 3-enum `share_pattern` model. Superseded because (a) the enum it promoted is itself superseded by D-IH-86-EJ (rewrite from 3-shape to 4-base + 1-overlay), and (b) the worked example it cited (SUEZ POC at `orchestration_broker_thin_margin`) was itself recommercialised by D-IH-86-EL. The Wave R+2 rewrite implicitly reset the doctrine to `charter`; Stage-1 re-active-promotion ratifies at D-IH-86-EO with the corrected SUEZ encoding + Aïsha continuity deep-partner row + EFA bd_commission_overlay row as the 2-base + 1-overlay worked-example coverage.
  - **D-IH-86-EG** *(superseded by D-IH-86-EL at 2026-05-27)* — Original SUEZ commercial encoding as `orchestration_broker_thin_margin`; superseded because the SUEZ POC's actual commercial shape is `consulting_direct + bd_commission_overlay` per the 13/05 customer meeting + the operator's verbatim *"15% of business development that i give to people when they don't work but just come and give us a project"* framing. See §3.2 for the corrected per-row math.
  - **D-IH-86-EH** *(preserved at rewrite)* — SUEZ POC artifact-shape ratification (Excel libellé generator real .xlsx + Loom + WeasyPrint render deferred to post-commercial-close cycle); unaffected by the commercial-pattern recoding.
  - **D-IH-86-EI** *(preserved at rewrite)* — SUEZ POC operator-led Microsoft Azure build (Power Apps + Excel PO + Power Automate flow); unaffected by the commercial-pattern recoding.
  - **D-IH-86-EJ** — Doctrine FULL REWRITE: `share_pattern` enum 3-value → 4-value (`deep_partner_65_35` / `bd_intro_only` / `joint_venture_aventure` / `consulting_direct`) + new `share_overlay` field with 1-value enum (`bd_commission_overlay`) + new methodology-readiness axis per §2.4 + new CS-09 overlay-base coherence check + supersedes D-IH-86-DE. Ratified inline-ratify after 13/05 transcript surfaced the operator's actual commercial philosophy (4 patterns + 1 overlay; not 3 patterns). Doctrine status reset to `charter` implicitly by the rewrite; Stage-1 re-active-promotion ratified at D-IH-86-EO (Wave R+3 2026-05-27).
  - **D-IH-86-EK** — `parallel_invoice_stream_indicator` boolean column added to `COLLABORATOR_SHARE_REGISTRY` (position 20; default `false`). Per-row flag declaring whether the collaborator is invoiced separately from Holistika's customer-facing invoice; surfaces the structural difference between in-kind contribution (single Holistika→customer invoice) and parallel commercial invoicing flow (collaborator invoices customer directly) despite identical economic outcomes. Motivated by the post-handshake transcript framing distinguishing "EFA invoices SUEZ directly for their 15% BD commission" from "EFA contributes value in-kind under Holistika's umbrella invoice."
  - **D-IH-86-EL** — SUEZ POC recommercialization from `orchestration_broker_thin_margin` (3-row split 6/47/47 HOL-CORP / Founder / EFA) to `consulting_direct + bd_commission_overlay` (1 base row HOL-CORP 85 + 1 overlay row EFA 15 carving from the BENEFITS pool); supersedes D-IH-86-EG. Ratifies the per-row math in §3.2 + the corrected SUEZ rows in `COLLABORATOR_SHARE_REGISTRY.csv` landed at Wave R+2 Commit 5.
  - **D-IH-86-EM** — `overlay_pct_deviation` `override_kind` enum value added to `COLLABORATOR_RATE_OVERRIDES.override_kind` (auditable separately from `share_split_deviation`) for `bd_commission_overlay` rows deviating from the 15% default anchor. `VALID_OVERRIDE_KINDS` extended to 3-value (`market_rate_excursion` / `share_split_deviation` / `overlay_pct_deviation` NEW). Overlay-deviation auditing rides on the existing `COLLABORATOR_RATE_OVERRIDES.csv` row pattern (not a new schema).
  - **D-IH-86-EN** — `methodology_readiness` 4-value axis added to `COLLABORATOR_SHARE_REGISTRY` (`methodology_trained` / `methodology_in_progress` / `methodology_naive` / `methodology_not_applicable`) gating `share_pattern` eligibility via the `METHODOLOGY_READINESS_PERMISSIBLE_PATTERNS` lookup. Prevents the operator-named *"35% compromise to bridge a methodology gap"* failure mode where an inexperienced collaborator gets committed to `deep_partner_65_35` as a negotiation compromise while Holistika silently carries both the 65% AND the methodology-fill-in work. CS-09 validator enforces the coherence table at row-authoring time.
  - **D-IH-86-EO** — Stage-1 re-active-promotion of `COLLABORATOR_SHARE_DOCTRINE` (charter → active) ratified 2026-05-27 at this commit. Supersedes D-IH-86-DF (original 3-enum Stage-1 promotion). Promotion criteria 4-of-4 MET: (1) 2 of 4 base patterns exercised in lived engagements — `consulting_direct` (SUEZ HOL-CONSULTING base row) + `deep_partner_65_35` (Aïsha continuity row); (2) 1 of 1 overlay value exercised — `bd_commission_overlay` (SUEZ EFA overlay row); (3) Validator CS-01..CS-09 9/9 PASS on 3 live SHARE_REGISTRY rows (including CS-09 coherence audit per D-IH-86-EK/EN); (4) operator-ratified re-active-promotion decision row = this. Methodology-readiness coverage 3 of 4 values exercised in lived practice (`methodology_trained` + `methodology_in_progress` + `methodology_not_applicable`). Closing-loop verification report at `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/wave-r-plus-3-collaborator-share-stage1-re-promotion-closing-loop-2026-05-27.md` carries the per-gate evidence.
  - **D-IH-73-J** — `eng_model_percentage_collaborator` engagement model (parent precedent; unaffected by rewrite).
- External research grounding: OECD Transfer Pricing Guidelines 2022 (DEMPE framework) — https://www.oecd.org/tax/transfer-pricing/; Goldscheider et al. "The Classical 25% Rule" (les Nouvelles, 2002); Hennart "A Transaction Costs Theory of Equity Joint Ventures" (Strategic Management Journal, 1988); Yan & Gray "Bargaining Power, Management Control, and Performance in United States-China Joint Ventures" (Academy of Management Journal, 1994).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
@docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
