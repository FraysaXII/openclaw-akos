---
status: draft
classification: working
access_level: 5
language: en
register: internal
artifact_kind: counterparty_brief
counterparty_org_ref: GOI-CUS-SUEZ-2026
counterparty_lead_ref: POI-CUS-SUEZ-LEAD-2026
bridge_ref: GOI-PRT-EFA-2026
governance: SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001
recorded_at: 2026-05-10
---

# Counterparty brief — `GOI-CUS-SUEZ-2026` / WeBuy procure-to-pay

> Internal working brief. Operator-private (access_level 5). Internal register is permitted here per the dual-register contract (counterparty / elicitation / baseline reality assessment vocabulary stays in this folder; outward-facing register lives under `docs/references/hlk/v3.0/Think Big/Clients/2026-suez-webuy/` per the P12.3 migration to the canonical client-engagement home).

## 1. Counterparty baseline reality

| Field | Value |
|:---|:---|
| Counterparty (anonymised) | `GOI-CUS-SUEZ-2026` — French enterprise, waste-and-resource-management subsidiary running the WeBuy procurement platform; specifically the **Service Engins TP / Approvisionnements** unit. |
| Stage | Mature enterprise (parent group is publicly traded). The buying unit is small relative to the group but has its own procurement-operations decision authority. |
| Sector | Industrial — civil-works fleet management (engins de chantier). |
| Geography | France (delivery + invoicing addresses in Île-de-France + Lyon). |
| Operator profile (sponsor) | Procurement-operations lead (`POI-CUS-SUEZ-LEAD-2026`) — mid-management; not a CFO/CIO sale. Reaches us via the EFA bridge (`GOI-PRT-EFA-2026` / `POI-PRT-EFA-LEAD-2026`). |
| Pain-trigger (declared) | "Manual data entry into WeBuy creates litigation-grade invoices when the PO number is missed or mistyped; the 5-part naming rule for the libellé is hard to apply without errors." |
| Pain-trigger (inferred) | Procurement-operator throughput is bounded by a single human re-keying every demande d'achat from email + Excel + supplier devis. The litigation tax (factures sans PO → blocked payments → supplier-relationship friction) is large enough that an outsider has been invited to write the CDC. |
| Decision-maker shape | Sponsor + DSI SUEZ (IT). Sponsor approves the operational solution; DSI gates hosting + integration paths + RGPD posture + access governance. |
| Time-to-engage urgency | Active — they have produced a v1.0 CDC for validation. The window is the next 2-6 weeks for shaping; Phase 1 delivery (Excel/Power Query short-term) is targeted at ~4 weeks. |
| Budget reality (declared) | Not declared. Internal CFO/CIO chain has not surfaced. |
| Budget reality (inferred) | Enterprise-scale procurement project. Comparable mid-market BPO/automation projects in France: €40–120k for a Phase-1 Excel + Phase-2 web-app sequence; €80–200k+ if Phase-3 RPA/API is added. Validated by the estimation discipline (P3) using the Madrid-SME consulting base × FR enterprise + first-of-kind multipliers. |
| Anti-patterns (their stated) | "Pas d'API publique documentée" → no expectation of a clean WeBuy API in the short term. "Pas d'installation requise côté poste utilisateur" → no fat client. RGPD-aware data handling (article 20 of CGA SUEZ). |
| Anti-patterns (inferred) | Enterprise procurement frequently bounces against internal-IT governance: any solution that **stores supplier PII outside SUEZ-homologated systems** is dead on arrival. Cloud hosting will need an explicit data-residency answer. RPA proposals tend to be killed by DSI on fragility grounds. |

## 2. WeBuy domain shape (from CDC + mode opératoire)

* **System of record**: WeBuy — internal procurement platform (no public API).
* **Process**: gestionnaire de commandes receives an email from a Responsable d'Intervention (R.I.); composes a demande d'achat in WeBuy by hand, picking from supplier devis + an Excel parc-engins reference + a 5-part naming rule (`[Initiales] - [N° parc] - [Code intervention] - [Fournisseur] - [N° devis]`).
* **Categories**: CAPEX (CAP), Maintenance (PMR/PMC/PMS/PMV/FSC/FSR), Fournitures pièces (PMF), Transport (FST/PMT), Location (FSL/PML), Pneus.
* **PO lifecycle**: WeBuy auto-generates a PO number (e.g. `PO0179xxxx`) that is transmitted to the supplier with the BC and must reappear on every facture. Missing → automatic litigation classification.
* **Counterparty's recommended technical posture (CDC §5)**: Option B = lightweight web app, optional Phase-1 Excel/Power-Query interim; Phase-3 RPA only as a feasibility study.
* **KPIs declared (CDC §11)**: −70% saisie time / month, ≥99% conformity of libellé, <2% factures-en-litige, <5 jours ouvrés to resolve a litige, ≥80% gestionnaire satisfaction quarterly, 100% PO traceability weekly.

## 3. Approach posture (planned)

| Technique | Use? | Rationale |
|:---|:---|:---|
| Direct interrogation | NO | Reads as adversarial in an enterprise procurement-CDC review. |
| Direct elicitation (substantive discovery) | YES — primary | Sponsor expects substantive feedback on the CDC itself in exchange for their time. |
| Indirect elicitation (peer-anchored) | YES — secondary | "Other procurement teams running WeBuy-class platforms tend to discover X around the time their litigation tax crosses Y" — useful for surfacing the unstated DSI constraints. |
| Provocation | NO | Inappropriate at this stage; we are bridge-introduced, not battle-tested. |
| Reverse-elicitation | YES — late in the call | After the CDC walkthrough, "where are we mis-naming the friction points?" surfaces internal political constraints. |

## 4. Open placeholders to confirm with the bridge before Monday

1. **Decision-authority confirmation** — Is `POI-CUS-SUEZ-LEAD-2026` the budget owner, or does sign-off escalate to a category manager / DSI sponsor / CFO chain? Bridge to confirm.
2. **DSI posture on hosting** — Has DSI pre-cleared external hosting (boilerplate-Vercel + Supabase) or is on-premise / SUEZ-internal-cloud the only acceptable option? Bridge to flag the data-residency answer the proposal must include.
3. **WeBuy integration aperture** — Is there *any* documented import path (CSV/Excel import, RFC, internal RPC) that the sponsor knows about, beyond the public surface? The CDC says "pas d'API publique"; bridge to test if there's a less-public one.
4. **Existing supplier list** — Is the Excel parc-engins reference + the supplier base authoritative, or are there shadow Excel files or shared inboxes feeding the gestionnaire? Bridge to characterise the data-feed reality so we don't propose an integration on a phantom source.

## 5. Recommended next action

* **Today (Sunday 2026-05-10)** — confirm the four placeholders with the bridge during today's prep call. Re-grade source `S2` (bridge interview reliability) accordingly.
* **Monday 2026-05-11** — meet `POI-CUS-SUEZ-LEAD-2026`. Frame: "We have read the CDC; we want to confirm our understanding before we propose anything." Use the FR elicitation plan (12 questions) as a deck-of-cards, not a script.
* **Within the week** — deliver the external pack: discovery questionnaire (FR, recap), CDC feasibility shape (FR, point-by-point), proposal (FR, 8 sections), deck (FR, 8 slides). Pricing + Gantt grounded in `SOP-ENG_ESTIMATION_DISCIPLINE_001` (P3 output).

## 6. Cross-references

* CDC extract: `extracts/cdc_webuy_suez.txt` (16,242 chars).
* Mode opératoire extract: `extracts/mode_ope_ratoire_-_process_de_passage_de_commande_webuy.txt` (32,999 chars).
* Source grading: `source-grade.csv` (this folder).
* Elicitation plan: `elicitation-plan.md` (this folder).
* SOPs: `SOP-IO_COUNTERPARTY_BASELINE_ASSESSMENT_001`, `SOP-IO_ELICITATION_DISCIPLINE_001`, `SOP-IO_INTELLIGENCE_REPORT_001`.
