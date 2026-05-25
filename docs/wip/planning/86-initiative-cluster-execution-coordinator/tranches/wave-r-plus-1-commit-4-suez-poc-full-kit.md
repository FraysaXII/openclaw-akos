---
tranche_id: wave-r-plus-1-commit-4-suez-poc-full-kit
tranche_class: engagement
tranche_title: SUEZ POC FULL KIT — first engagement-class application of both 13th + 14th Quality Fabric specialties
audiences_named:
  - J-CU
  - J-PT
  - J-OP
  - J-AIC
channels_named:
  - CHAN-EMAIL-OUTBOUND
  - CHAN-DRIVE-SHARE
scenarios_named:
  - suez_proc_ops_lead_reviewing_cover_mail_and_arch_addendum_27_28_05
  - efa_academie_partner_cross_checking_cobranded_posture
  - aisha_continuity_role_recipient_reading_arch_addendum_replicability_section
  - operator_internal_post_dispatch_self_audit
brand_register: mixed
ratifying_decisions:
  - D-IH-86-DF
  - D-IH-86-EF
  - D-IH-86-EG
  - D-IH-86-EH
  - D-IH-86-DA
  - D-IH-86-DB
  - D-IH-86-DC
  - D-IH-86-DD
  - D-IH-86-DE
  - D-IH-86-EA
  - D-IH-86-EB
  - D-IH-86-EC
  - D-IH-86-ED
  - D-IH-86-EE
  - D-IH-82-T
  - D-IH-82-U
  - D-IH-82-V
erp_surface_citations:
  - operator_dashboard
  - customer_dashboard
  - erp_workflow_join
is_atomic_commit: true
reversibility_class: medium
reversibility_rationale: SUEZ POC FULL KIT artifacts (cover-mail draft + arch-addendum markdown + render-script extension) are reversible via git revert; COLLABORATOR_SHARE_REGISTRY rows are authored at status=draft (NOT signed with collaborator yet) so per-row split adjustments remain reversible until operator signs at SUEZ commercial-close 2026-XX-XX; D-IH-86-DF active-promotion of 13th specialty is one-way once active rows accumulate (3+ engagement gate would prevent re-charter; reversal cost = full doctrine-state-rollback + DECISION_REGISTER superseded row + scratchpad lessons-learned); D-IH-86-EF/EG/EH ratifications are governance-class (medium reversibility) — operator override via successor decision row + DECISION_REGISTER superseded marker reverts; arch-addendum + cover-mail are draft customer-facing artifacts requiring operator final-review before SMTP send (no irreversible send-class commitment lands at this commit).
closing_loop_test: py scripts/validate_collaborator_share.py PASS (5 CSVs with seeded SUEZ rows) + py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-1-commit-4-suez-poc-full-kit.md PASS + py scripts/validate_decision_register.py PASS (433 + 4 new = 437 rows) + py scripts/validate_hlk.py OVERALL PASS + py scripts/render_suez_engagement_pdfs.py --smoke PASS (render-pipeline soft-success or full render of 9 surfaces: 7 existing + 2 new = cover-mail + arch-addendum) + py -m pytest tests/test_hlk_collaborator_share.py tests/test_validate_collaborator_share.py tests/test_hlk_synthesis_before_tranche.py tests/test_validate_synthesis_before_tranche.py -v PASS + grep architecture-addendum.fr.md to verify the 3 ERP-surface citation triple present in body
recipient_fallback_channel: Google Drive PDF distribution from artifacts/exports/ to engagement-shared Drive folder when SUEZ proc-ops lead OR EFA Académie partner cannot access mail attachment due to enterprise-MIME filtering; per operator framing on traditional-means SYN-10 intent (drives + manual handoff outside dashboard surfaces)
---

# Wave R+1 Commit 4 — SUEZ POC FULL KIT (first engagement-class worked example for both 13th + 14th specialties)

## Purpose

Ship the SUEZ POC FULL KIT artifacts (27-28/05 target per operator slip from initial 26/05) AND simultaneously land the **first engagement-class application** of both Quality Fabric specialties minted in the preceding wave:

1. **13th specialty COLLABORATOR_SHARE_DOCTRINE** — first real (non-self-test) engagement to populate the 5 CSV registers. SUEZ POC is the first commercial-economic application. Two-pattern engagement per Q-B ratify:
   - **Aïsha @ `deep_partner_65_35`** — continuity revenue stream row; Holistika 65 / Aïsha 35 default split; collaborator_id = POI-PRT-EFA-LEAD-2026 per GOI_POI_REGISTER. Aïsha is the EFA Académie partner lead AND the SUEZ-process operator AND the post-launch maintenance lead (per proposal §3 Continuité posture A); the 35% pool compensates her continuity role beyond per-hour billed time.
   - **SUEZ deal economics @ `orchestration_broker_thin_margin`** — across-rows sum-to-100 with Holistika-corporate ~6% (broker margin = the AKOS governance + methodology IP value) + Founder Mark-I + EFA Académie organisation. Interim defaults: Holistika 6 / Founder 47 / EFA 47 per operator's "two people sharing the deal" framing; operator finalizes exact split at SUEZ commercial-close 2026-XX-XX via DECISION_REGISTER row amendment (rows stay status=draft until signed).

2. **14th specialty SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE** — first engagement-class worked example (worked-example #3 overall after self-mint #1 + I82 P1 canonical_csv_mint #2; per doctrine §5 Stage 1 charter→active promotion gate). The engagement-class fires ALL 10 SYN dimensions per `DIMENSION_FIRE_RULES['engagement']` — making this the broadest synthesis-sweep application to date. The ERP-engagement-governance UX shape (operator dashboard / customer dashboard / ERP workflow join) materialises across all SUEZ artifacts per Q-A ratify.

Per the operator's 2026-05-25 Q-A framing ratified inline (also cited in Commit 3 charter):

> *"the main goal is to properly govern our engagements via cleverly crafting erp workflow and UX just like i want my dashboard they would also like to have it (even if they don't log so much or see it that much and i send them info via traditional means or drives) we need this kind of thinking to ensure we scale and don't find false scope creep that we knew was a logical tactical move and design from our part but we're not taking the full design in mind of these processes, why we're doing what we're doing."*

Per the operator's 2026-05-25 Q-B framing on Aïsha:

> *"aisha asked me to make her ongoing maintenance/operator administrative work (as she is the operator of the process we aim to automate, we also spoke about that, so please look it up)"*

And on the SUEZ commercial shape:

> *"we could even hire with still nice margin for two people sharing the deal and Holistika has 6%"*

## Scope (in scope for this commit)

### A. SUEZ POC FULL KIT artifacts (operator-named at slip)

1. **Cobranded cover mail FR** at `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/01-operator-pack/cover-email-2026-05-27.fr.md`:
   - Addresses SUEZ proc-ops lead with `[NOM_LECTEUR]` placeholder (operator fills at SMTP-send time per operator-private identity discipline).
   - Cobranded Holistika + EFA Académie posture per `BRAND_COBRANDING_PATTERN.md` host=Holistika / guest=EFA Académie.
   - References Aïsha role-class explicitly with AL-restricted-access framing — names her function (`notre opératrice partenaire en continuité`) per BRAND_BASELINE_REALITY_MATRIX external register translation; first-name reveal deferred to operator's final-pass per BBR identity discipline.
   - Forwards POC scope from existing `proposal.customer.fr.md` (Variant B recommendation) + `cdc-feasibility-shape.fr.md` + `commercial-schedule-c.md` — explicitly does NOT re-elicit per operator directive.
   - Audience tag `J-CU` (SUEZ procurement-operations lead = customer-enterprise) + `J-PT` (EFA Académie partner cobranded recipient).
   - Channel `CHAN-EMAIL-OUTBOUND` per `CHANNEL_TOUCHPOINT_REGISTRY`.
   - Render target: `mail` surface per `akos-external-render-discipline.mdc` RULE 1 — rendered to HTML body at SMTP-send time via downstream tooling (NOT this commit; the markdown is the source-of-truth; .md is NEVER sent externally per RULE 1 forbidden-mail-attachment).

2. **2-page architecture addendum FR** at `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/architecture-addendum.fr.md`:
   - Page 1: Phase 1 (Excel + Power Query libellé generator) + Phase 2 (lightweight web app multi-catégories) + Phase 3 (intégration feasibility avec portail WeBuy + couche reporting).
   - Page 2: **Aïsha-led continuity** (posture A from proposal §3 referenced explicitly; AL-restricted access level posture documented) + **SUEZ CTO office replicability** narrative (the methodology replicates beyond this engagement to other SUEZ CTO procurement workflows) + **ERP-engagement-governance UX shape citation** (the 3-surface model from D-IH-82-V; operator dashboard for Holistika audit-trail + customer dashboard for SUEZ proc-ops visibility + ERP workflow join for Power Platform integration).
   - Microsoft Power Platform stack named per operator ratify (Power Query for Phase 1, Power Apps + Power Automate + SharePoint for Phase 2, Power BI for Phase 3 reporting layer).
   - Audience `J-CU` (SUEZ DSI + procurement) + `J-PT` (EFA Académie partner).
   - Render target: `pdf` (via extended `render_suez_engagement_pdfs.py`) + manifest sidecar.

3. **`render_suez_engagement_pdfs.py` extension** — add the 2 new surfaces (cover-mail OPTIONAL via the existing renderer's mail-rendering pipeline OR separate; arch-addendum as customer-pack 4th surface) to the existing 7-surface render set. Maintains existing soft-success behaviour.

### B. COLLABORATOR_SHARE 5-CSV first-engagement population (13th specialty worked example #1)

Per `akos-collaborator-share.mdc` RULE 2 atomic-5-CSV co-mint contract:

4. **`COLLABORATOR_MARKET_RATE_REFERENCE.csv`** — seed 4 FR market rates:
   - `rate_fr_founder_lead_consulting` — Founder-role-class senior consulting rate FR (€/h band based on Madeira-island + Spain-incorporation context; operator-private rate-source citation).
   - `rate_fr_partner_operator_continuity_mid` — Partner-role-class operator-continuity mid-tier rate FR (Aïsha shape).
   - `rate_fr_partner_business_development_senior` — Partner-role-class business-development senior rate FR (EFA Académie deal-bringer shape).
   - `rate_fr_holistik_researcher_senior` — Holistik-Researcher-role senior rate FR (covers founder side execution work + general consulting band).
   - Rate-source citations point to industry-survey references (operator confirms private sources at next session; placeholder citations cite the doctrine §2.4 ±25% market-rate band convention).

5. **`PARTNER_OVERLAP_EXCLUSION_CLAUSES.csv`** — no new clauses needed for SUEZ; EFA Académie is a coaching/bilingual-bridge firm without overlap with Holistika's research-head / dataops / mktops capability — all 10 Holistika service classes remain at their doctrine §2.2 default `bill_mode`. No clause linkage emerges at this engagement.

6. **`HOLISTIKA_VENDOR_SERVICES_BILLED.csv`** — 10 rows for engagement_id=`2026-suez-webuy`, one per service class, all at doctrine §2.2 default `bill_mode` (in_kind for 8 service classes + billed for 2: `dataops_engineering` + `madeira_ai_orchestration` carry billed-against-project hours per the Variant C scope's Phase 1 Excel/Power Query prototype + Phase 2 web app build):
   - 8 in_kind: `research_head_discipline`, `mktops_marketing`, `brand_render_machinery`, `pmo_orchestration`, `finops_governance`, `legal_governance`, `compliance_governance`, `talent_governance`.
   - 2 billed (with billed_hours/billed_rate populated from commercial-schedule-c.md Variant C estimates): `dataops_engineering` (Phase 1+2 build hours), `madeira_ai_orchestration` (Phase 2 web app AI integration hours, IF Phase 2 elected per recommendation).

7. **`COLLABORATOR_SHARE_REGISTRY.csv`** — 4 rows for engagement_id=`2026-suez-webuy`:
   - Row 1 (`deep_partner_65_35`): collaborator_id=POI-PRT-EFA-LEAD-2026 (Aïsha); holistika_share_pct=65; collaborator_share_pct=35; engagement_model_id=`eng_model_percentage_collaborator`; collaborator_role_class per baseline_organisation; status=draft (un-signed; awaits operator commercial-close ratify).
   - Row 2 (`orchestration_broker_thin_margin`): collaborator_id=`HOLISTIKA-CORPORATE` (broker margin row; the AKOS governance + methodology IP value); holistika_share_pct=6; collaborator_share_pct=0 (Holistika is the broker; this row records Holistika's broker margin only).
   - Row 3 (`orchestration_broker_thin_margin`): collaborator_id=`FOUNDER-MARK-I-2026`-shape (Founder personal-billing row); collaborator_share_pct=47 (interim default per "two people sharing the deal" framing; operator finalizes split at commercial-close).
   - Row 4 (`orchestration_broker_thin_margin`): collaborator_id=GOI-PRT-EFA-2026 (EFA Académie organisation); collaborator_share_pct=47 (interim default; operator finalizes).
   - Across-rows for orchestration_broker pattern: 6 + 47 + 47 = 100 (CS-03 across-rows PASS).
   - Per-row for deep_partner pattern: 65 + 35 = 100 (CS-03 per-row PASS).

8. **`COLLABORATOR_RATE_OVERRIDES.csv`** — no overrides at this commit. All rows use defaults (Aïsha 65/35 default; orchestration_broker no per-row default to deviate from; market rates within ±25% band so no market_rate_excursion rows). If operator's commercial-close adjusts orchestration_broker splits away from 47/47, the override rows land at that future commit.

### C. SUEZ-specific CAPABILITY_REGISTRY rows (engagement-class capabilities the SUEZ POC delivers)

9. **5 SUEZ-specific operational capability rows** appended to `CAPABILITY_REGISTRY.csv` (1097 → 1102):
   - `CAP-HOL-DATAOPS-SUEZ-LIBELLE-GENERATOR-001` — Phase 1 Excel/Power Query libellé generator covering 5-component naming rule across 6 categories (CAPEX / maintenance / pneus / fournitures / transport / location) per cdc-feasibility-shape.fr.md §0 + §6.
   - `CAP-HOL-DATAOPS-SUEZ-CATEGORY-ACCOUNT-MAPPING-001` — déterministic catégorie ↔ compte comptable mapping referenced in proposal.customer.fr.md §"Cinq fonctionnalités, parmi les vingt-quatre identifiées".
   - `CAP-HOL-MADEIRA-SUEZ-EMAIL-EXTRACTION-001` — Phase 2 lightweight web app email-to-structured-PR extraction module per cdc-feasibility-shape.fr.md §1 F-01.
   - `CAP-HOL-DATAOPS-SUEZ-DISPUTE-REGISTER-001` — module de prévention et gestion des litiges per proposal.customer.fr.md §"Cinq fonctionnalités".
   - `CAP-HOL-DATAOPS-SUEZ-USAGE-DASHBOARD-001` — tableau de bord d'usage mensuel auto-généré par catégorie/fournisseur/engin/centre de coût per proposal.customer.fr.md §"Cinq fonctionnalités".
   - Each row's `notes:` field carries the `surface=` triple per D-IH-82-V convention.
   - `originating_process_ids` field: links to existing `hol_eng_prc_*` engagement-process rows in `process_list.csv` (no new process_list rows minted at this commit; SUEZ-specific engagement-class processes inherit from the existing engagement-process catalog).

### D. Decision rows

10. **D-IH-86-DF mint** — 13th specialty COLLABORATOR_SHARE_DOCTRINE Stage 1 active-promotion:
    - Aïsha-on-SUEZ deep_partner_65_35 worked-example #1 (1 real engagement applying the doctrine with all 5 CSVs populated correctly + CS-01..CS-08 PASS).
    - 13th specialty status flip charter → active in HOLISTIKA_QUALITY_FABRIC §6 row + doctrine frontmatter.
    - Reversibility: medium-high (Stage 1 promotion is reversible via successor decision row + status downgrade; rows would stay populated as historical record).

11. **D-IH-86-EF mint** — 14th specialty SYNTHESIS_BEFORE_TRANCHE engagement-class worked-example #3 ratification:
    - SUEZ POC engagement-class application closes gate 3 of 3 for charter→active promotion at next maturation gate.
    - 14th specialty Stage 1 active-promotion candidate (separate decision when first 2 consecutive subsequent tranches PASS per doctrine §5.2 gate; deferred to a future commit).
    - Reversibility: medium (doctrine-application reversal does not deprecate the doctrine itself).

12. **D-IH-86-EG mint** — SUEZ orchestration_broker_thin_margin commercial-architecture interim-defaults ratification:
    - Records the Holistika 6 / Founder 47 / EFA 47 interim default + operator's "two people sharing the deal" verbatim framing.
    - Per-row status=draft preserves reversibility until operator commercial-close signs with collaborators.
    - Reversibility: high (split changes via row-amendment + COLLABORATOR_RATE_OVERRIDES row with override_kind=share_split_deviation + ratifying_decision_id pointing at successor D-IH-86-* row).

13. **D-IH-86-EH mint** — SUEZ POC FULL KIT artifact shape ratification:
    - Authorises the cover-mail + arch-addendum + render-script-extension shape as canon for the SUEZ engagement (future SUEZ-class engagements inherit the shape).
    - Documents the deferral of .xlsx libellé generator authoring (operator-side Microsoft-Excel workflow; NOT a markdown-authoring task) + Loom screen-recording deferral (operator-side; out-of-scope for this commit).
    - Reversibility: medium (artifact-shape reversal requires render-script-extension revert + 2 artifacts unpublish; medium cost).

### E. Closing surfaces

14. **CHANGELOG entry** prepended under `[Unreleased]` documenting Commit 4.
15. **86-cluster `files-modified.csv` rows** appended (~15 rows expected).
16. **Operator-scratchpad drain entry** appended.

## Out of scope for this commit (forward-charters)

- **Working .xlsx Excel + Power Query libellé generator attachment** — operator-side Microsoft-Excel workflow; NOT a markdown-authoring task; operator builds + tests + attaches at SMTP-send time; tracker row added to `_trackers/` if needed.
- **60-90s Loom screen recording** — operator-side; out-of-scope for this commit.
- **SUEZ commercial-close final-ratify of orchestration_broker splits** — deferred to commercial-close date 2026-XX-XX when operator signs with EFA + (potentially) Aïsha; lands as COLLABORATOR_RATE_OVERRIDES + DECISION_REGISTER amendment.
- **I82 P2 capability registry full population** — cross-pollination from BOTH SUEZ + Websitz engagements; Commit 5 post-26/05-ship.
- **14th specialty Stage 1 active-promotion** — requires 2 consecutive subsequent tranches PASS post-Commit 4; lands at a future commit after natural traffic.
- **Investor stability dossier** — parallel non-blocking; lands as I86 wave-deliverable in a separate commit per Q-C ratify.
- **Aïsha named introduction at customer side** — first-name reveal deferred per BBR identity discipline; cover-mail uses role reference; operator final-pass at SMTP-send time fills in identity if appropriate.

## Decision lineage table

| Decision ID | Purpose | Reversibility | Carries |
|:---|:---|:---|:---|
| D-IH-86-DF | 13th specialty Stage 1 active-promotion + Aïsha-on-SUEZ deep_partner_65_35 worked example #1 | medium-high | doctrine status flip + 1 SHARE_REGISTRY row + 1 VENDOR_SERVICES_BILLED roster + MARKET_RATE rows |
| D-IH-86-EF | 14th specialty SUEZ POC engagement-class worked-example #3 ratification | medium | tranche charter + synthesis sweep + 10-dim fire-set PASS evidence |
| D-IH-86-EG | SUEZ orchestration_broker interim-defaults (6/47/47) commercial-architecture | high | 3 SHARE_REGISTRY rows status=draft + operator-final-ratify deferred to commercial-close |
| D-IH-86-EH | SUEZ POC FULL KIT artifact shape canon (cover-mail + arch-addendum + render extension) | medium | 2 new artifacts + render script extension |

## Closing-loop test (SYN-09)

The commit is verified PASS when ALL of:

1. `py scripts/validate_collaborator_share.py` PASS — all 8 checks (CS-01..CS-08); 5 CSVs populated with SUEZ rows.
2. `py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-1-commit-4-suez-poc-full-kit.md` PASS (engagement-class 10-dim fire-set; ≥ 8 PASS, ≤ 2 WARN/INFO acceptable per D-IH-86-ED broad-fire INFO ramp).
3. `py scripts/validate_capability_registry.py` PASS on all 1102 rows.
4. `py scripts/validate_decision_register.py` PASS (433 → 437 rows).
5. `py scripts/validate_hlk.py` OVERALL PASS.
6. `py -m pytest tests/test_hlk_collaborator_share.py tests/test_validate_collaborator_share.py tests/test_hlk_synthesis_before_tranche.py tests/test_validate_synthesis_before_tranche.py -v` ALL PASS (91+ tests).
7. `py scripts/render_suez_engagement_pdfs.py --smoke` PASS (render-pipeline soft-success acceptable when WeasyPrint not installed; manifest sidecars verify source_sha256 matches authored markdown).
8. Grep `surface=` triple present on every new CAPABILITY_REGISTRY row + present in arch-addendum body.

## Cross-references

- Doctrine 13th: [`COLLABORATOR_SHARE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md).
- Doctrine 14th: [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md).
- Sister 13th specialty mint trail: Commits 2a (4d564c0) + 2b+2b-ext (47977f7) + 2c-a (0ed0e40) + 2c-b (0cb4e61).
- Sister 14th specialty mint trail: Commits 2a (e4148d6) + 2b (42ef2f1) + 2c-a (c825a03) + 2c-b (cbe7f51).
- Sister application precedent: Commit 3 I82 P1 capability extension (ee8493f) — first non-self 14th-specialty application (canonical_csv_mint class).
- SUEZ engagement home: [`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/).
- SUEZ proposal customer-facing: [`proposal.customer.fr.md`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/02-customer-pack/proposal.customer.fr.md).
- SUEZ proposal operator-pack: [`proposal.fr.md`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/01-operator-pack/proposal.fr.md).
- SUEZ CDC feasibility shape: [`cdc-feasibility-shape.fr.md`](../../../references/hlk/v3.0/Think%20Big/Clients/2026-suez-webuy/01-operator-pack/cdc-feasibility-shape.fr.md).
- SUEZ commercial schedule Variant C: [`commercial-schedule-c.md`](../../../intelligence/2026-05-10-suez-webuy-procure-to-pay/commercial-schedule-c.md).
- SUEZ render pipeline: [`scripts/render_suez_engagement_pdfs.py`](../../../../scripts/render_suez_engagement_pdfs.py).
- GOI/POI register for Aïsha + EFA + SUEZ: [`GOI_POI_REGISTER.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv) — POI-PRT-EFA-LEAD-2026 + GOI-PRT-EFA-2026 + GOI-CUS-SUEZ-2026 + POI-CUS-SUEZ-LEAD-2026 all already canonical.
- Cursor rules: [`akos-collaborator-share.mdc`](../../../../.cursor/rules/akos-collaborator-share.mdc) + [`akos-synthesis-before-tranche.mdc`](../../../../.cursor/rules/akos-synthesis-before-tranche.mdc) + [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) + [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) + [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) (Aïsha role-class is partner-class, not adviser-class; rule cross-referenced for clean separation only).
- Paired skills: [`collaborator-share-craft`](../../../../.cursor/skills/collaborator-share-craft/SKILL.md) + [`synthesis-before-tranche-craft`](../../../../.cursor/skills/synthesis-before-tranche-craft/SKILL.md) + [`external-render-craft`](../../../../.cursor/skills/external-render-craft/SKILL.md).
- Operator-scratchpad drain entry: appended at this commit; cites the SUEZ 27-28/05 ship target + 13th specialty Stage 1 active-promotion + 14th specialty 3-of-3 worked-example gates MET + interim commercial defaults pending operator commercial-close ratify + forward-pointer to Commit 5 I82 P2 + Investor stability dossier I86 wave-deliverable.
