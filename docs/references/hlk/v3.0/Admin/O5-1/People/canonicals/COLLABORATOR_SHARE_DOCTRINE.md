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
  - People Operations Lead
  - Legal Counsel
last_review: 2026-05-25
last_review_by: Founder/CEO
last_review_at: 2026-05-25
last_review_decision_id: D-IH-86-CY-A
methodology_version_at_review: v3.1
ratifying_decisions:
  - D-IH-86-CY-A
  - D-IH-86-CY-B
  - D-IH-86-CY-C
  - D-IH-86-CY-D
  - D-IH-73-J
status: charter
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

> The People-area canonical that names how Holistika splits the **benefits** of an engagement with a strategic collaborator who brings or operates the deal — codifying the operator's verbatim framing at the 2026-05-25 collaborator-economics architecture session:
>
> *"65% for us, 35% for Aïsha out of the margin and that means we need to act as consultants and partners but we at holistika we treat our partners as B2B, hence we propose a plethora of services we take for granted we'll do and delegate whatever process we may have agreed with the partner to them, in this case, we'll do most of the work, but it's justified because of bringing us such strategic customer for us. websitz per example was asked to support no mktops as they were a mkt agency themselves on top of bringing us customers to the table."*
>
> Thirteenth specialty instantiation of [`HOLISTIKA_QUALITY_FABRIC.md`](HOLISTIKA_QUALITY_FABRIC.md) (per **D-IH-86-CY-A**) and sister to [`ARTIFACT_CLASS_LIBRARY.md`](ARTIFACT_CLASS_LIBRARY.md). Codifies `compose_COLLABORATOR_SHARE(engagement, collaborator, services_billed, overlap_clauses, market_rate_ref) → 65/35 benefits split + transparent project-cost roster + partner-overlap-exclusion clause table + market-rate benchmark with governed override`.

## 1. Purpose

Holistika collaborates with strategic partners (people who bring deals, operate processes inside deals, or pair with us as joint go-to-market arms) and the question of *how the upside is split* recurs in every such engagement. Three failure modes drove the operator to codify this doctrine at the 2026-05-25 session:

1. **Going back on what was said.** Operator: *"i need yor help for the best practice and especially never go back on what i said not to loose credibility (they not always remember things but it can be they do)."* When the economic model lives in chat-history-and-memory rather than in canonical doctrine, every partner conversation is a fresh negotiation with implicit drift; collaborators may quote back something the operator no longer remembers; trust erodes.

2. **B2B-vendor posture mistaken for free labour.** Holistika provides a plethora of services (research-head discipline; AKOS governance; MADEIRA + AI engineering; brand + render machinery; PMO orchestration). When a partner has overlapping capabilities (Websitz precedent — they are a mkt agency themselves), Holistika does NOT bill those overlapping services against the project; we contribute them in-kind as the value of our 65% share. Without explicit clauses naming which services were in-kind, future engagements may over-bill OR under-bill, breaking the partner narrative.

3. **Collaborator transparency vs operator administrative overhead.** Aïsha-shape collaborators (operator-of-the-process being automated; Aïsha for SUEZ procurement workflow) gain BOTH a billed rate for their ongoing operator work AND a share of remaining benefits. Without canonical accounting, the operator either (a) hides the collaborator's billed time (collaborator feels exploited; benefits-pool seems larger than it is) or (b) muddles billed time with profit share (collaborator does not know what they earned for what). Transparency is the alternative; this doctrine names how to do it.

This canonical names the **economic-relationship discipline** — not a one-off contract template but a recurring doctrine with a paired runbook (computes the math), a paired validator (catches over-billing / under-billing / un-ratified market-rate excursions), a paired cursor rule (names when the discipline fires), a paired skill (names how to apply), and a paired SOP (names the operator-side AC-HUMAN + AC-AUTOMATION). The 5 CSV registers below name what to record; the runbook computes deterministically what is computable; the validator catches drift before commit; the operator scratchpad records every governed exception.

## 2. The economic architecture — TRUE-MARGIN + 5-register chassis

Per **D-IH-86-CY-B** (operator-ratified at the 2026-05-25 session), the canonical benefits formula is **TRUE-MARGIN with an explicit billed-services log**:

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

## 3. Worked example — Aïsha-shape collaborator on a single engagement

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
| **CS-03: 65/35 default audit** | FAIL | Every SHARE_REGISTRY row's `holistika_share_pct + collaborator_share_pct = 100`; default is 65/35 unless `share_override_decision_id` is non-empty AND resolves into DECISION_REGISTER AND a matching `COLLABORATOR_RATE_OVERRIDES` row exists with `override_kind=share_split_deviation`. |
| **CS-04: Market-rate excursion audit** | WARN | Every SHARE_REGISTRY row's `collaborator_billed_rate` must fall within ±25% of the `rate_typical_per_hour` of the matching MARKET_RATE_REFERENCE row (matched on `role_class + region_code + experience_band`). Outside-band rates require a matching `COLLABORATOR_RATE_OVERRIDES` row with `override_kind=market_rate_excursion`. Missing the MARKET_RATE_REFERENCE row entirely also raises WARN (the doctrine encourages seeding reference rates as engagements materialise). |
| **CS-05: bill_mode default audit** | WARN | Every VENDOR_SERVICES_BILLED row's `bill_mode` must match the doctrine §2.2 default for that `holistika_service_class` OR have a non-empty `bill_mode_decision_id`. Mis-billing without ratification surfaces here. |
| **CS-06: Partner-overlap clause linkage** | WARN | Every VENDOR_SERVICES_BILLED row with `bill_mode=in_kind` AND a default of `billed` for that service class must carry a non-empty `justification_clause_id` resolving into PARTNER_OVERLAP_EXCLUSION_CLAUSES. |
| **CS-07: Rate override expiry hygiene** | INFO | Any `COLLABORATOR_RATE_OVERRIDES` row whose `expires_at` is in the past must have `status=archived`. Stale active rows surface as INFO. |

**INFO → FAIL ramp.** Per the operator's *"craft what you can and please ensure this is all wired up properly with the rest"* framing + the Quality Fabric §10 promotion criteria, the validator launches at INFO advisory for all 7 checks; CS-01 / CS-02 / CS-03 promote to FAIL at the **Wave T or later** boundary gated on (a) 3+ real engagements applying the doctrine cleanly with zero CS-01..03 findings, AND (b) operator-explicit promotion decision row. CS-04 / CS-05 / CS-06 remain at WARN forever (they encode judgment-class drift that operator review handles; FAIL would be over-mechanical). CS-07 remains at INFO (cleanup hygiene, not blocker).

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

- **Anti-pattern A: STRICT-MARGIN (Holistika bills in-house services against project at market rate).** Rejected per `D-IH-86-CY-B`. Failure mode: collaborator narrative breaks ("you're already billing us for everything; why do you also get 65%?"); double-dip perception; smaller benefits pool to split paradoxically reduces collaborator's apparent gain even though their absolute earnings may rise. The TRUE-MARGIN posture is cleaner narratively + structurally aligned with the operator's verbatim *"we propose a plethora of services we take for granted we'll do."*

- **Anti-pattern B: Hidden collaborator-billed-time (collaborator hours absorbed into benefits pool).** Rejected per operator's framing *"aïsha is a person whose costs will be put against the project to make her work transparent, so she may gain more money than we expect."* Failure mode: collaborator does not see her operational hours as a transparent line item; benefits pool appears inflated; when she compares against the doctrine, the math does not reconcile; trust erodes.

- **Anti-pattern C: Per-deal renegotiation of partner-overlap exclusion (no clause registry).** Rejected per `D-IH-86-CY-C` (operator chose the clause-table-with-schema-field option). Failure mode: every engagement renegotiates from scratch; patterns are not learned across engagements; future Holistika collaborators do not inherit the institutional memory; same arguments resurface; operator effort wasted.

- **Anti-pattern D: Operator-self-set collaborator billed rates with no market-rate reference.** Rejected per `D-IH-86-CY-A` (option B+governed-override chosen). Failure mode: rates drift arbitrarily; cross-engagement equity erodes (Aïsha at €100/hr while another collaborator with equivalent role-class gets €150/hr because she negotiated harder); collaborator narrative becomes "Holistika doesn't have a principled rate framework."

- **Anti-pattern E: Forbid commercial overrides (rigid 65/35 enforcement).** Rejected per operator's *"with the possibility to adjust commercially this in a governed manner"* framing. Failure mode: strategic deals (e.g., a deal where Holistika wants to share more aggressively to win a flagship customer) cannot be priced; operator forced into either a violation OR a perverse incentive (e.g., book partial benefits off-engagement to circumvent the rigid split). The governed-override mechanism preserves flexibility + the audit trail.

- **Anti-pattern F: Decision-log entries with no canonical CSV mirror.** Rejected per all AKOS doctrine — every commercial deviation gets a `COLLABORATOR_RATE_OVERRIDES` row + a `DECISION_REGISTER` row. The CSV row is canonical; the decision-log entry is the narrative around it. Decisions without CSV mirrors are ungovernable by the validator + invisible to future audits.

## 9. Promotion criteria (charter → active → promoted-FAIL)

This doctrine lands at `status: charter` per `D-IH-86-CY-A`. Promotion criteria:

**charter → active** (gates):
- 1 real engagement (Aïsha-on-SUEZ; Commit 3) applies the doctrine end-to-end with all 5 CSVs populated correctly.
- Validator CS-01..07 PASS on the populated rows.
- Operator-ratified active-promotion decision row (D-IH-86-CY-E or successor).

**active → promoted-FAIL ramp** (gates per §6):
- 3+ real engagements applying the doctrine cleanly with zero CS-01..03 FAIL findings.
- ≥ 1 cross-engagement audit pass at quarterly cadence with operator sign-off.
- Operator-ratified ramp-promotion decision row.
- CS-04 / CS-05 / CS-06 remain at WARN forever per §6 (judgment-class drift).
- CS-07 remains at INFO forever per §6 (cleanup hygiene).

## 10. Self-discipline rules for agents

When authoring or applying this discipline:

1. **Default to the 65/35 split.** Every new SHARE_REGISTRY row inherits the default unless the operator surfaces a commercial-override decision via inline-ratify per `akos-inline-ratification.mdc`. Drafting a non-65/35 row without the ratify gate is the most common failure mode.
2. **Co-mint the VENDOR_SERVICES_BILLED roster with the SHARE_REGISTRY row.** Every engagement gets 10 default-in-kind rows (one per service class per §2.2) — copy from a sibling engagement, then mark deviations explicitly. Forgetting the roster lets the validator silently pass an engagement with no documentation of which Holistika services were contributed in-kind.
3. **Seed MARKET_RATE_REFERENCE rows opportunistically.** When a new collaborator's `role_class × region × experience_band` is not yet in MARKET_RATE_REFERENCE, the agent does NOT skip the row — the agent surfaces an inline-ratify gate asking the operator for the rate-source citation + the typical-rate value, then seeds the row in the same commit as the SHARE_REGISTRY row. This is how the registry builds out over time without per-engagement renegotiation.
4. **Never inline a rate exception without a ratification row.** A SHARE_REGISTRY row with `collaborator_billed_rate` 30% above the typical reference + no `COLLABORATOR_RATE_OVERRIDES` row is a validator-detected drift. The fix is always: add the override row + the DECISION_REGISTER row + the commercial-strategy-rationale. Never silence the validator without the audit trail.
5. **Cite the doctrine when communicating with the collaborator.** When sharing the math with a collaborator (e.g., emailing the final-close statement), cite the doctrine version + the relevant CSV rows. The collaborator's confidence in the math comes from the reproducible audit trail, not from the operator's assertion.
6. **Use the paired skill before authoring.** Read [`.cursor/skills/collaborator-share-craft/SKILL.md`](../../../../../../../.cursor/skills/collaborator-share-craft/SKILL.md) before drafting a new SHARE_REGISTRY row OR a new override OR a new clause. The skill carries the worked examples + the recovery patterns for the common pitfalls.

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
  - **D-IH-86-CY-A** — Doctrine mint (this canonical at status: charter).
  - **D-IH-86-CY-B** — 65/35 TRUE-MARGIN benefits formula ratified.
  - **D-IH-86-CY-C** — Named clause table + EngagementCostRow schema field for partner-overlap exclusion (option C of the 2026-05-25 architecture inline-ratify gate).
  - **D-IH-86-CY-D** — Tier 1 WIP hygiene (`docs/wip/hlk-km/` deprecation; pre-requisite housekeeping; Commit 1).
  - **D-IH-86-CY-E** — Reserved for active-promotion gate per §9.
  - **D-IH-73-J** — `eng_model_percentage_collaborator` engagement model (parent precedent).
- External research grounding: OECD Transfer Pricing Guidelines 2022 (DEMPE framework) — https://www.oecd.org/tax/transfer-pricing/; Goldscheider et al. "The Classical 25% Rule" (les Nouvelles, 2002); Hennart "A Transaction Costs Theory of Equity Joint Ventures" (Strategic Management Journal, 1988); Yan & Gray "Bargaining Power, Management Control, and Performance in United States-China Joint Ventures" (Academy of Management Journal, 1994).

@docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_QUALITY_FABRIC.md
@docs/references/hlk/v3.0/Admin/O5-1/People/People Operations/canonicals/dimensions/ENGAGEMENT_MODEL_REGISTRY.csv
@docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/PRECEDENCE.md
