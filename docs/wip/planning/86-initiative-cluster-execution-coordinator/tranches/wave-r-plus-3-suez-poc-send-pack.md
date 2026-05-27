---
tranche_id: wave-r-plus-3-suez-poc-send-pack
tranche_class: engagement
tranche_title: SUEZ POC SEND PACK — cover-email follow-up + 2 deep demos (libellé generator + dispute-litigation register) + addendum cleanup
audiences_named:
  - J-OP
  - J-AIC
  - J-CU
  - J-PT
channels_named:
  - CHAN-EMAIL-OUTBOUND
  - CHAN-EMAIL-INBOUND
  - CHAN-EVENT-MEETING
scenarios_named:
  - suez_technical_interlocutor_reads_follow_up_email_post_13_05_meeting_skims_2_deep_demos_within_5_minutes_and_forwards_to_m_regal_decision_maker
  - m_regal_decision_maker_reads_2_deep_demos_understands_libelle_generator_and_dispute_litigation_module_anonymized_examples_and_pencils_a_september_decision_window
  - suez_dsi_briefed_by_technical_interlocutor_via_june_meeting_intro_reads_demos_validates_microsoft_power_platform_stack_compatibility_with_existing_suez_az_tenant
  - aisha_continuity_partner_reviews_cobranded_posture_in_cover_email_and_demos_validates_no_premature_commercial_commitment_visible_to_customer_per_stream_a_vs_stream_b_clean_separation
  - operator_uses_demo_specs_in_own_microsoft_azure_tenant_to_build_actual_power_apps_excel_po_and_power_automate_flows_anonymized_examples_serve_as_blueprint_for_real_build
  - operator_inline_ratify_resolution_picking_among_4_demo_artifact_shapes_at_pre_send_quality_gate_application
brand_register: external-translated
ratifying_decisions:
  - D-IH-86-EP
  - D-IH-86-EQ
  - D-IH-86-ER
  - D-IH-86-ES
  - D-IH-86-ET
  - D-IH-86-EJ
  - D-IH-86-EK
  - D-IH-86-EL
  - D-IH-86-EM
  - D-IH-86-EN
  - D-IH-86-EH
  - D-IH-86-EF
  - D-IH-86-EG
  - D-IH-86-DA
  - D-IH-86-DB
  - D-IH-82-V
erp_surface_citations:
  - customer_dashboard_suez_purchase_order_creation_form_libelle_generator_power_apps_canvas_surface
  - customer_dashboard_suez_dispute_intake_form_and_litigation_dashboard_power_apps_canvas_surface
  - erp_workflow_join_suez_po_to_accounting_backbone_export_via_power_automate_flow_to_excel_template_to_suez_existing_finance_system
is_atomic_commit: false
closing_loop_test: py scripts/synthesis_before_tranche_check.py --check-charter docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-3-suez-poc-send-pack.md PASS + py scripts/validate_brand_baseline_reality_drift.py PASS (zero internal-register tokens in the 2 demo files + rewritten cover email) + py scripts/validate_hlk.py OVERALL PASS + py scripts/validate_collaborator_share.py PASS (SUEZ rows still consulting_direct + bd_commission_overlay; no commercial-close drift yet) + py scripts/validate_decision_register.py PASS (5 new EP/EQ/ER/ES/ET rows + zero collision with prior ranges) + manual brand-jargon sweep of the 2 demos + cover email confirms zero forbidden tokens (Madeira / AKOS / share_pattern / counterparty / elicitation per BRAND_BASELINE_REALITY_MATRIX) + manual cobranding-posture sweep confirms Aïsha named in continuity-role footer of demos AND cover email (J-PT visibility) but NOT in commercial-commitment posture (Stream A invoicing remains Holistika-direct per D-IH-86-EL) + manual visual-richness check confirms each demo carries ≥ 1 wireframe ascii-art OR mermaid flow + ≥ 1 Excel-template snippet OR Power Automate flow pseudocode + 3-5 anonymized worked examples per demo (Fournisseur-Alpha-001 et al; never real SUEZ supplier names per no-client-screenshot IP principle) + manual recipient-fallback check confirms cover email mentions phone follow-up option (CHAN-EVENT-MEETING fallback for J-CU recipients not accessing email).
recipient_fallback_channel: J-CU SUEZ recipients (technical interlocutor + M. Régal + DSI) — cover email offers (a) 30min phone follow-up Cal.com link in signature + (b) June DSI intro meeting (CHAN-EVENT-MEETING) for live walkthrough. J-PT Aïsha (continuity partner) — direct Slack/WhatsApp out-of-AKOS-scope. Demos at stable git paths; any later re-share via Drive/OneDrive/SharePoint reuses same SSOT.
reversibility_class: medium
reversibility_rationale: Wave R+3 SEND PACK is medium-reversibility because all 4 in-scope artifacts (tranche charter + 2 demo specs + rewritten cover email + architecture-addendum deletion) are reversible via git revert until the cover email is physically sent to SUEZ via the operator's mail client (irreversibility crystallises at send-action OUTSIDE the AKOS repo — the SEND ACTION itself is not what this tranche commits; it commits the SEND-PACK artifacts in a ready-to-send state). Demo specs are reversible (deletion + git revert returns prior state); cover email is reversible until send-action (operator-side; not auto-triggered); architecture-addendum deletion is reversible (git revert restores the file). The DECISION_REGISTER rows EP/EQ/ER/ES/ET are one-way at the row level (supersede rows stay in history) but their content effects are reversible via successor decision rows + content amendments. CRITICAL non-reversibility: the SUEZ commercial close itself (collaborator share final values + pricing variant election + Phase 1 PO sign) is NOT in this tranche scope — that crystallises at a separate post-send commercial-negotiation cycle when SUEZ responds + M. Régal decides + Phase 1 PO is signed. This tranche commits the PRE-COMMERCIAL-CLOSE state of the send-pack only; post-commercial-close artifacts (signed PO + final SHARE_REGISTRY status flip from draft to active + commercial-schedule final variant + Power Apps + Excel real .xlsx + Loom recording) ship in a future post-commercial-close tranche per D-IH-86-EH artifact-shape ratification.
---

# Wave R+3 — SUEZ POC SEND PACK (cover-email rewrite + 2 deep use-case demos + architecture-addendum cleanup)

## Purpose

Execute the SUEZ POC **SEND PACK** ratified at the operator's `Q1-post-transcript=b_doctrine_first_suez_after` + `Q2-post-transcript=c_two_deep_demos` ratification gates (2026-05-26, post-13/05-meeting-transcript substrate audit + post-Wave-R+2-doctrine-rewrite + post-handshake debrief absorption). The doctrine layer is now correct (4-base + 1-overlay model per D-IH-86-EJ landed at sha 5cd9793..b7af78e tranche close); the SUEZ rows are now structurally-correct (`consulting_direct + bd_commission_overlay` per D-IH-86-EL); the path forward is to ship the customer-facing send-pack itself: rewrite the cover email as a FOLLOW-UP referencing the 13/05 meeting + attach the deck + CDC + 2 NEW deep use-case demos showing the libellé generator (CDC F-05) + the dispute register with litigation detection (CDC §11; F-25 to F-29).

Per the operator's verbatim framing from the post-handshake debrief (2026-05-26):

> *"on est dans la création des cas d'usage plutôt"* — create new anonymized use cases from the operator's own Microsoft Azure tenant rather than extract historic SUEZ data (no-client-screenshot IP principle).

> *"tu vends de la capacité de Holistika de les faire"* — sell capability + methodology, not finished products (the demos showcase the operator's ability to build these systems quickly + cleanly, NOT a finished SUEZ-ready SaaS).

> *"On est à plusieurs"* — Aïsha continuity partner named in cobranded footer of demos + cover email, BUT Stream A invoicing remains Holistika-direct per D-IH-86-EL clean separation from Stream B (Aïsha's separate EFA Académie maintenance scope outside this engagement).

> *"litige c'est un coup caché"* — disputes are a hidden-cost category at SUEZ; the dispute-register-with-litigation-detection module is a confirmed CORE ASK from M. Régal's framing (decision-maker), not a nice-to-have.

And per the 13/05 customer-meeting transcript substrate (load-bearing for cover-email tone):

- M. Régal is the decision-maker; technical interlocutor is the gatekeeper who briefs M. Régal + the DSI; September decision window with **a tight before-summer deliverable bar to give M. Régal something to study over the August break**.
- DSI needs a June intro meeting (CHAN-EVENT-MEETING) to validate Microsoft Power Platform stack compatibility with SUEZ existing Azure tenant.
- SUEZ already acknowledged cobranding posture (Aïsha-with-Holistika); no commercial concern raised about the dual party.
- Customer perceives Holistika as **external prestation B2B vendor** — Holistika own-bills, NOT a 3-way revenue split with EFA as commercial party.

### Artifact shape rationale (Q2-post-transcript=c_two_deep_demos ratify)

The operator ratified `c_two_deep_demos` over `a_no_new_artifacts` (just rewrite the cover email) and `b_one_deep_demo_only` (cover + 1 demo) because:

1. **Two demos cover both stream halves** — libellé generator covers the deterministic Phase-1 PO-creation core (CDC F-05); dispute register covers the differentiating Phase-2 litigation-detection module that M. Régal pre-confirmed as core ask (CDC §11). Single-demo coverage would leave one of the two stream halves un-illustrated.

2. **Two anonymized demos respect the no-client-screenshot IP principle** — both demos are built from the operator's own Microsoft Azure tenant with anonymized supplier names (Fournisseur-Alpha-001 / Beta-002 / Gamma-003), never real SUEZ supplier data. The demos are blueprints showing CAPABILITY, not finished SUEZ deliverables (per `vends le savoir-faire` framing).

3. **Two demos fit the before-summer deliverable bar** — the SUEZ technical interlocutor reads the email + skims the 2 demos within 5 minutes; M. Régal reads the 2 demos in-depth over the August break (CDC + deck already shown in 13/05 meeting; this is the supplementary read for decision-maker). One demo would feel thin; three+ demos would overload the August reading capacity.

4. **Two demos serve the operator's own POC build path** — after send, the operator uses the demo specs themselves as blueprints to build the actual Power Apps + Excel templates in own Microsoft Azure tenant (operator-led; out-of-scope for this tranche but unblocked by this tranche). Each demo's wireframe + flow + worked-examples become the spec for the actual build.

### Architecture-addendum cleanup rationale (B1 ratified per scratchpad L1716)

`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/architecture-addendum.fr.md` is staged for deletion (already `D` in git status at session start). Operator ratified at scratchpad L1716 that the addendum's content (Phase 1/2/3 + Aïsha continuity + SUEZ CTO office replicability + ERP-engagement-governance UX shape 3-surface citation) is now **fully redundant** with:

- The customer-pack proposal (`proposal.customer.fr.md`) — covers Phase 1/2/3 architecture narrative already.
- The CDC (`cdc-feasibility-shape.fr.md` in 01-operator-pack/) — covers ERP-engagement-governance UX shape via F-NN functional decomposition.
- The customer deck (referenced in proposal cross-references) — already shown in the 13/05 meeting; covers Aïsha continuity posture.

The addendum was an artifact-shape compromise from the Commit-4 (Wave R+1) D-IH-86-EH ratify when the 13/05 transcript hadn't been re-read; with the transcript now absorbed, the redundancy is visible + the addendum carries no incremental information for the customer. Deletion is reversible (git revert) but preferred over reuse because the 2 deep demos (this tranche) cover the same SUEZ-actionable surface area with the visual richness the customer needs to envision the build.

## Scope (in scope for this multi-commit tranche; 4 commits expected)

### Commit 1 — Tranche charter + architecture-addendum cleanup (~30min; this commit)

1. **Author this tranche charter** at `docs/wip/planning/86-initiative-cluster-execution-coordinator/tranches/wave-r-plus-3-suez-poc-send-pack.md` per `akos-synthesis-before-tranche.mdc` RULE 4 paired-SOP-runbook gate.
2. **Run `py scripts/synthesis_before_tranche_check.py --check-charter <this-file>`** — engagement-class fires all 10 SYN dimensions; expect PASS=10 (or PASS=9 + WARN=1 with SYN-07 atomicity dispositioned scope-extend at charter time per RULE 2 of synthesis-before-tranche, mirroring Wave R+2 7-commit precedent).
3. **Delete `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/architecture-addendum.fr.md`** — already staged as `D` in git status; this commit formalises the deletion per B1 ratify.
4. **Append `D-IH-86-EP` (SUEZ POC SEND PACK tranche scope) + `D-IH-86-EQ` (architecture-addendum deletion ratify)** to `DECISION_REGISTER.csv` at status=active.
5. **CHANGELOG.md `[Unreleased]` entry** with Commit 1 scope contract + forward-pointers to Commits 2/3/4.
6. **86-cluster `files-modified.csv` +N rows** (tranche charter + addendum deletion + DECISION_REGISTER + CHANGELOG + self-row).
7. **Atomic commit.**

### Commit 2 — Deep demo 1: générateur de libellé (~60min)

1. **Author `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/demo-libelle-generator.fr.md`** (~3-4 pages FR; external register per BBR; status=draft; intellectual_kind=use-case-demo-spec; brand_voice_register=peer_consulting matching proposal):
   - **§1 Contexte** — what the libellé (description naming rule) does + why it matters for SUEZ supplier-PO traceability (CDC F-05 rationale).
   - **§2 Règle de nommage en 5 composants** — the 5-component naming rule (e.g., `[DATE]-[FOURNISSEUR-CODE]-[CATEGORIE]-[SITE]-[INTITULE-COURT]`) with each component sourced from a deterministic dropdown / typeahead / free-text field as specified in CDC F-05.
   - **§3 Wireframe Power Apps formulaire de saisie** — ASCII-art or markdown-table mockup of the Power Apps canvas form: 5 input fields + auto-generated libellé preview + save button + cancel button + breadcrumb back to PO list. Show field validation states (empty / valid / invalid) and the auto-generated libellé preview updating in real-time.
   - **§4 Power Automate flow de génération** — pseudocode / mermaid flow showing: form-submit event → fetch supplier code from supplier registry → concatenate 5 components per format string → write to Excel PO template (column G "Libellé") → log to operator dashboard → return success / error to form.
   - **§5 Template Excel PO** — markdown table snippet showing the 8-column PO Excel template (Date / Fournisseur-Code / Fournisseur-Nom / Catégorie / Site / Libellé / Montant-HT / TVA) with 3 sample rows fully populated using anonymized supplier names.
   - **§6 5 cas usage anonymisés** — 5 worked examples with realistic-feeling supplier names (Fournisseur-Alpha-001 / Beta-002 / Gamma-003 / Delta-004 / Epsilon-005) + realistic categories (CONSOMMABLE / SERVICE-MAINT / EQUIPEMENT / PRESTATION-CONSEIL / TRANSPORT) + realistic sites (PARIS-NORD / LYON-SUD / MARSEILLE-EST / NANTES-OUEST / STRASBOURG-CENTRE) showing the libellé that each composition generates.
   - **§7 Cobranding footer** — "Démo conçue par Holistika en collaboration avec Aïsha (continuité opérationnelle post-projet)" — Aïsha named in continuity-role posture per cobranded posture acknowledged by SUEZ in 13/05 meeting; commercial commitment posture is Holistika-direct per D-IH-86-EL (Stream A clean separation).
2. **Append `D-IH-86-ER` (demo-libelle-generator content ratify)** to `DECISION_REGISTER.csv` at status=active.
3. **CHANGELOG.md `[Unreleased]` entry** with Commit 2 scope contract.
4. **86-cluster `files-modified.csv` +N rows.**
5. **Atomic commit.**

### Commit 3 — Deep demo 2: registre des litiges avec détection (~60min)

1. **Author `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/02-customer-pack/demo-dispute-register-litigation-detection.fr.md`** (~3-4 pages FR; external register per BBR; status=draft; intellectual_kind=use-case-demo-spec):
   - **§1 Contexte** — what the dispute register module does + why it matters for SUEZ supplier-litigation pre-detection (CDC §11; F-25 to F-29 rationale; operator framing *"litige c'est un coup caché"* — hidden cost category M. Régal pre-confirmed as core ask).
   - **§2 Formulaire de saisie litige Power Apps** — ASCII-art / markdown-table wireframe of the dispute intake canvas form: supplier dropdown + PO reference number lookup + dispute category dropdown (12-class taxonomy) + dispute description free-text + amount-at-stake numeric + opening-date datepicker + assigned-handler dropdown + initial-severity dropdown (low / medium / high / critical) + supporting-docs attach button + save button.
   - **§3 Taxonomie 12 catégories** — markdown table of the 12 dispute categories (DELAI-LIVRAISON / QUALITE-PRODUIT / QUALITE-SERVICE / FACTURATION-ERREUR / NON-CONFORMITE-COMMANDE / SAV-INSUFFISANT / RUPTURE-CONTRAT / GARANTIE-NON-RESPECTEE / DOCUMENT-MANQUANT / TVA-ANOMALIE / TRANSPORT-ENDOMMAGE / AUTRE) with one-line description per category + typical amount-at-stake range + typical resolution-time-days range.
   - **§4 Power Automate flow de classification** — mermaid flow showing: form-submit event → category-FK lookup → severity-recompute heuristic (amount-at-stake × resolution-time-days × supplier-history-weight) → write to dispute register Dataverse table → trigger litigation-detection heuristic IF severity ≥ high → notify operator dashboard + Aïsha (continuity partner) IF litigation-detection fires → return success / error to form.
   - **§5 Heuristique de détection litige** — pseudocode showing the litigation-detection heuristic: `IF (severity == critical) OR (severity == high AND amount-at-stake > 5000€) OR (supplier-history-disputes-90-days >= 3) OR (category in {RUPTURE-CONTRAT, GARANTIE-NON-RESPECTEE}) THEN flag_for_litigation_review` + Power Automate flow notifies operator + creates Cal.com 30min review meeting slot + emails draft mise-en-demeure template to operator for review.
   - **§6 Wireframe dashboard operator de pilotage** — ASCII-art / markdown-table mockup of the operator dashboard Power Apps canvas: top KPI cards (disputes-open-count / disputes-overdue-count / amount-at-stake-total / litigation-flagged-count) + middle table of disputes-sorted-by-severity-DESC with inline actions (open / close / escalate) + bottom chart of disputes-by-category-stacked-bar + filter bar (date-range / supplier / category / severity / handler).
   - **§7 3 cas usage anonymisés** — 3 worked examples with realistic-feeling supplier-dispute scenarios (Fournisseur-Alpha-001 DELAI-LIVRAISON severity=medium amount=1200€ → routine handling; Fournisseur-Beta-002 RUPTURE-CONTRAT severity=critical amount=15000€ → litigation flag fires + Cal.com slot booked + mise-en-demeure draft emailed; Fournisseur-Gamma-003 supplier-history=4-disputes-90-days QUALITE-PRODUIT severity=high → litigation flag fires on history-weight even though single-dispute amount is low).
   - **§8 Cobranding footer** — identical to demo 1.
2. **Append `D-IH-86-ES` (demo-dispute-register content ratify)** to `DECISION_REGISTER.csv` at status=active.
3. **CHANGELOG.md `[Unreleased]` entry** with Commit 3 scope contract.
4. **86-cluster `files-modified.csv` +N rows.**
5. **Atomic commit.**

### Commit 4 — Cover-email rewrite + closing-loop verification + tranche close (~45min)

1. **Rewrite `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/01-operator-pack/cover-email-2026-05-27.fr.md`** as a FOLLOW-UP email (NOT a first-contact email — first contact was the 13/05 in-person meeting):
   - **Objet** — explicit reference to 13/05 meeting + 2 deep demos preview.
   - **§1 Récap 13/05** — 2-3 sentences reaffirming the operator's understanding of M. Régal's framing (no-client-screenshot IP principle respected; high-level only).
   - **§2 Pack envoyé** — bulleted list of attachments: (a) proposal customer pack (already known); (b) CDC feasibility shape (already known); (c) NEW demo 1 libellé generator; (d) NEW demo 2 dispute register with litigation detection.
   - **§3 Promotion module litige** — 1-2 sentences explicitly promoting the dispute-litigation module as a core differentiating value (per *"litige c'est un coup caché"* M. Régal framing).
   - **§4 Confirmation rendez-vous DSI juin** — 1-2 sentences confirming the operator's availability for a 30-45min Cal.com slot in early June to brief the DSI on Microsoft Power Platform stack compatibility.
   - **§5 Mention Aïsha 1-ligne** — 1-line cobranded footer mentioning Aïsha continuity-role posture (per Stream A clean separation; NOT positioning Aïsha as commercial party).
   - **§6 Stream B 1-line** — 1-line acknowledgement that EFA Académie's separate maintenance scope at SUEZ (Stream B) is out-of-scope for this engagement + operator-stays-in-touch for any cross-pollination relevance.
   - **§7 Recipient fallback** — phone follow-up Cal.com link in signature + commitment to send the demo specs again in any alternate format (Drive / OneDrive / SharePoint) on request.
2. **Run closing-loop verification (5 probes per pre-send regression gate informal application):**
   - (a) `py scripts/synthesis_before_tranche_check.py --check-charter <this-tranche-charter>` — expect PASS=10 (engagement class fires all dimensions; conditional triggers re-evaluated post-cover-email-author).
   - (b) `py scripts/validate_brand_baseline_reality_drift.py` — expect zero internal-register tokens in the 2 demos + rewritten cover email.
   - (c) `py scripts/validate_hlk.py` OVERALL PASS — full umbrella validator green (or pre-existing INFO advisories only).
   - (d) `py scripts/validate_collaborator_share.py` PASS — SUEZ rows still at `consulting_direct + bd_commission_overlay` (no commercial-close drift; status=draft preserved).
   - (e) `py scripts/validate_decision_register.py` PASS — 5 new EP/EQ/ER/ES/ET rows lint clean.
3. **Mint closing-loop verification report** at `docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/wave-r-plus-3-suez-poc-send-pack-closing-loop-2026-05-27.md` (mirror Wave R+2 closing-loop report shape).
4. **Append `D-IH-86-ET` (Wave R+3 SUEZ POC SEND PACK tranche close + 5-probe closing-loop verdict)** to `DECISION_REGISTER.csv` at status=active.
5. **CHANGELOG.md `[Unreleased]` entry** with Commit 4 scope contract + tranche-close marker.
6. **86-cluster `files-modified.csv` +N rows + operator-scratchpad.md drain entry covering all 4 commits.**
7. **Atomic commit.**

## Out of scope (deferred to post-commercial-close cycle OR parallel tracks)

- **Actual Microsoft Azure POC build** — operator-led (operator builds Power Apps + Excel + Power Automate flows in own tenant from the 2 demo specs); not auto-executed by AKOS commits. Tracked as `suez-microsoft-poc-build` PENDING todo.
- **Working Excel `.xlsx` file + Loom screen recording** — deferred to post-commercial-close cycle per D-IH-86-EH artifact-shape ratification.
- **WeasyPrint render of cover email + demos to PDF** — deferred to post-commercial-close cycle; markdown source is canonical SSOT for now; PDF render can happen on operator demand using existing `scripts/render_suez_engagement_pdfs.py`.
- **SUEZ commercial close (signed Phase 1 PO + final SHARE_REGISTRY status flip from draft to active + final commercial-schedule variant election)** — happens AFTER SUEZ responds to send pack + M. Régal decides + DSI validates stack + September decision window. Separate post-commercial-close tranche.
- **Stream B (EFA Académie's separate maintenance contract at SUEZ)** — Aïsha's sole-trader scope; NOT in this engagement; named 1-line in cover email §6 + 2-deep-demo cobranded footers but no commercial commitment posture from Holistika.
- **13th specialty COLLABORATOR_SHARE Stage-1 re-promotion (D-IH-86-EO reserved)** — happens AFTER SUEZ commercial close at status=active + 2+ additional engagements exercise the 4-base + 1-overlay model cleanly. Separate forward tranche.

## Closing-loop verification (the closing_loop_test field above)

Codified in the frontmatter `closing_loop_test` field. Five probes:

1. **synthesis_before_tranche_check --check-charter** — engagement-class fire-set (all 10 SYN dims) PASS at Commit 4 close.
2. **validate_brand_baseline_reality_drift** — zero internal-register tokens in the 3 customer-pack artifacts (2 demos + cover email).
3. **validate_hlk OVERALL** — full umbrella validator green.
4. **validate_collaborator_share** — CS-01..CS-09 PASS; SUEZ rows still at `consulting_direct + bd_commission_overlay` draft status.
5. **validate_decision_register** — 5 new rows (EP/EQ/ER/ES/ET) lint clean.

Plus 3 manual judgment-class checks at Commit 4:

- Manual brand-jargon sweep of the 2 demos + cover email confirms zero forbidden tokens (Madeira / AKOS / share_pattern / counterparty / elicitation per `BRAND_BASELINE_REALITY_MATRIX.md`).
- Manual cobranding-posture sweep confirms Aïsha named in continuity-role footer (J-PT visibility) but NOT in commercial-commitment posture (Stream A invoicing remains Holistika-direct per D-IH-86-EL).
- Manual visual-richness check confirms each demo carries ≥ 1 wireframe ascii-art OR mermaid flow + ≥ 1 Excel-template snippet OR Power Automate flow pseudocode + 3-5 anonymized worked examples (Fournisseur-Alpha-001 et al; never real SUEZ supplier names per no-client-screenshot IP principle).

## Decision lineage table (preview)

| ID | Decision | Status | Commit minted |
|:---|:---|:---|:---|
| **D-IH-86-EP** | Wave R+3 SUEZ POC SEND PACK tranche scope ratification (4-commit lineage; engagement-class; fires all 10 SYN dimensions; methodology-spine-first posture preserved from Wave R+2) | active | Commit 1 (this commit) |
| **D-IH-86-EQ** | Architecture-addendum.fr.md deletion ratification (B1 already-ratified at scratchpad L1716; content fully redundant with proposal + CDC + customer deck; formal deletion via Commit 1 atomic) | active | Commit 1 |
| **D-IH-86-ER** | Demo libellé generator content ratification (5-component naming rule + Power Apps wireframe + Power Automate flow + Excel template + 5 anonymized worked examples; external register per BBR; cobranding footer) | active | Commit 2 |
| **D-IH-86-ES** | Demo dispute register with litigation detection content ratification (12-category taxonomy + intake form wireframe + classification flow + litigation-detection heuristic + operator dashboard mockup + 3 anonymized worked examples; external register; cobranding footer) | active | Commit 3 |
| **D-IH-86-ET** | Wave R+3 SUEZ POC SEND PACK tranche close + 5-probe closing-loop verification verdict (cover email rewritten as follow-up + demos attached + closing-loop verification PASS) | active | Commit 4 |

## Cross-references

- Parent initiative: [`86 — initiative cluster execution coordinator`](../master-roadmap.md).
- Parent canonical: [`SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md) — the 14th Quality Fabric specialty whose 3rd worked-example gate this tranche extends (already MET at Wave R+1 Commit 4; this tranche is a 4th application not a gating mint).
- Companion canonical: [`COLLABORATOR_SHARE_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/COLLABORATOR_SHARE_DOCTRINE.md) — 4-base + 1-overlay model; SUEZ rows at `consulting_direct + bd_commission_overlay` draft status (this tranche commits the customer-pack send-pack; SUEZ commercial close happens later).
- Companion canonical: [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_BASELINE_REALITY_MATRIX.md) — dual-register CORPINT-internal vs translated-external; this tranche ships 3 customer-pack artifacts in translated-external register (zero internal tokens).
- Sister rules:
  - [`akos-synthesis-before-tranche.mdc`](../../../../.cursor/rules/akos-synthesis-before-tranche.mdc) — 14th specialty; RULE 1 + RULE 2 disposition; engagement-class fires all 10 SYN dims.
  - [`akos-collaborator-share.mdc`](../../../../.cursor/rules/akos-collaborator-share.mdc) — 13th specialty; SUEZ rows compliance (RULE 1 triple-resolution + RULE 3 CS-01..CS-09).
  - [`akos-brand-baseline-reality.mdc`](../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — dual-register; customer-pack artifacts in translated-external register (RULE 1 default-to-external rule).
  - [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) — 6-surface delivery contract; cover email = mail surface; demos = pdf surface (defer to post-commercial-close cycle).
  - [`akos-inline-ratification.mdc`](../../../../.cursor/rules/akos-inline-ratification.mdc) — Wave R+3 has zero inline-ratify gates planned at charter time (all 5 decisions are ratified-at-charter via this charter file; commit-time work is mechanical execution).
  - [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) — Wave R+3 mints zero new blockers; preserves 4 named PENDING todos from prior cycle as forward-pointers.
- Operator framing source: post-handshake debrief (`docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-grounding-post-handshake-2026-05-26.md`) — 440 lines; load-bearing for Stream A vs Stream B clean separation + no-client-screenshot IP principle + cobranding-acknowledged + dispute-litigation core ask.
- 13/05 customer-meeting transcript: `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/00-internal/source-materials/transcripts/2026-05-13-suez-customer-meeting.mp3.md` — load-bearing for cover-email tone + M. Régal decision-maker positioning + DSI June intro meeting confirmation.
- Pre-send regression gate spec (forward-charter as candidate 15th Quality Fabric specialty): [`docs/wip/planning/86-initiative-cluster-execution-coordinator/pre-send-regression-gate-spec-2026-05-26.md`](../pre-send-regression-gate-spec-2026-05-26.md) — Commit 4 5-probe closing-loop verification is the first informal application of this spec; full specialty mint deferred to next maintenance window.
