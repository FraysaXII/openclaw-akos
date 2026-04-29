# Program — `PRJ-HOL-KIR-2026` (People / Legal chain)

**Owner role**: Legal Counsel (CPO chain via Legal sub-area)  
**Program registry**: [`PROGRAM_REGISTRY.csv`](../../../../../../../compliance/dimensions/PROGRAM_REGISTRY.csv) → `PRJ-HOL-KIR-2026`.  
**Scope**: All Legal casework specifically scoped to KiRBe (subscription terms, LOA, IP, licensing, regulated jurisdictions).

This folder is the **program-scoped landing point** for Legal casework on KiRBe. Created **2026-04-29** as a cascade of `operator-answers-wave2.yaml` Section 4 `kirbe_duality.has_paying_customers_today: true` per **D-IH-16** — paying customers means Legal moves from on-demand to **required** for KiRBe. Sister to the Compliance folder created in the same cascade.

> **Process-list anchors** — Think Big Legal Compliance workstream `thi_legal_ws_2` (Founder Entity and IP Governance); filed instruments register maintenance `thi_legal_dtp_304`. KiRBe-specific legal casework adds new `process_list.csv` rows under `thi_legal_*` as it surfaces (subscription agreement template, IP assignment, regulator-licensing per jurisdiction, customer LOA flow).

## Casework scope (incoming)

- **KiRBe Subscription Agreement** — master terms + per-customer side letters, tracked as filed instruments under `discipline_id=legal` in `FOUNDER_FILED_INSTRUMENTS.csv` (or a new program-scoped instruments register if volume warrants — cf. Initiative 27 reserved slot).
- **IP assignment + licensing** for KiRBe-derived models, embeddings, prompt templates.
- **Customer Letter of Authorisation (LOA)** flow for client engagements that grant KiRBe ingestion access to off-Holistika sources.
- **Regulator licensing** by jurisdiction when KiRBe enters a regulated market (e.g. financial AI advisory in jurisdictions where that is a licensed activity).
- **Adviser engagement** via ADVOPS plane (Initiative 21) using `discipline_id=legal` (and new disciplines as KiRBe-specific legal questions arrive).

## Cross-references

- Tech KiRBe folder: [`Admin/O5-1/Tech/System Owner/programs/PRJ-HOL-KIR-2026/`](../../../../Tech/System%20Owner/programs/PRJ-HOL-KIR-2026/README.md)
- Compliance KiRBe folder (sister; same cascade): [`Admin/O5-1/People/Compliance/programs/PRJ-HOL-KIR-2026/`](../../Compliance/programs/PRJ-HOL-KIR-2026/README.md)
- Finance / Business Controller KiRBe folder (Stripe billing): [`Admin/O5-1/Finance/Business Controller/programs/PRJ-HOL-KIR-2026/`](../../../../Finance/Business%20Controller/programs/PRJ-HOL-KIR-2026/README.md)
- PMO KiRBe folder: [`Admin/O5-1/Operations/PMO/programs/PRJ-HOL-KIR-2026/`](../../../../Operations/PMO/programs/PRJ-HOL-KIR-2026/README.md)
- ADVOPS plane router: [`EXTERNAL_ADVISER_ROUTER.md`](../../../../Operations/PMO/EXTERNAL_ADVISER_ROUTER.md)
- Adviser engagement SOP: [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../../Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- Founder filed instruments register: [`FOUNDER_FILED_INSTRUMENTS.csv`](../../../../../../../compliance/FOUNDER_FILED_INSTRUMENTS.csv)
- Initiative 23 master roadmap: [`docs/wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/master-roadmap.md)
- D-IH-16 (KiRBe duality + on-demand → required cascade): see Initiative 23 [`decision-log.md`](../../../../../../../../wip/planning/23-hlk-program-registry-and-program-2/decision-log.md).
