# I70 P8 §8.17 (P8.5) — GOI/POI class regression hunt + inline-ratify report

**Date:** 2026-05-13
**Initiative:** I70 (Holistika OS Self-Governance Foundation)
**Phase:** P8 §8.17 (P8.5 — GOI class hunt)
**Decisions referenced:** D-IH-70-G, D-IH-70-N (P3 GOI hunt deferred), D-IH-70-AC (this report).
**Discipline:** A14 + H1 inline-ratify gate (evidence sweep → ranked options → `AskQuestion` → operator-pick → enum extension).

---

## 1. Why this hunt

`GOI_POI_REGISTER.csv` currently has 4 distinct `class` values (`banking_channel`, `client_org`, `external_adviser`, `partner`) drawn from 11 seed rows. The original Phase 8 §8.7 plan flagged that this list is **incomplete** — operator's working surface (operator briefs, customer engagements, methodology-coaching corpus, internal hiring, cobranding partner relationships, ENISA dossier audience) implies several relationship classes that don't yet have a slot in the enum, which forces ad-hoc text in `notes` and prevents the goipoi mirror from indexing those rows for governance queries.

This report executes the deferred §8.7 sweep + inline-ratify gate per A14 (run full sweep + distill + surface options + operator-picks; do not pause-and-wait).

---

## 2. Six-source evidence sweep

Pattern searched (case-insensitive): `legal counsel | regulator | investor | recruiter | competitor | media | press | partner | advisor | adviser | trainee | business developer | notary | inversor | competitor | journalist`.

| Source | Evidence count | Top file paths |
|:---|---:|:---|
| **1. Temp-context dump** (`temp-move-or-delete-hlk-business-context/`) | ~50 hits across 8 files | `Asesoria Hosteleria/2026-12-04 - Admin Course - 1.md` (10 hits — notary + asesoria legal); `EFA/2026-12-12 - Business Developer Onboarding.md` (1 hit — biz-dev); `Websitz/Use case 2/Rushly_Cahier_des_charges_v2.docx.md` (competitor refs); `ShadowGPU/27-02-2026 15.11 shadow gpu meeting.md` (9 hits — partner-investor blur) |
| **2. Research & Logic** | (advisory; not exhaustively swept — `docs/references/hlk/Research & Logic/` is reference-only per akos-mirror governance) | n/a |
| **3. Previous-project example** | (advisory; reference-only per same governance) | n/a |
| **4. Current engagement folders** (`docs/references/hlk/v3.0/Think Big/Clients/`) | 6 files with `legal counsel | adviser | recruiter` matches | `_engagement-template/README.md`; `2026-suez-webuy/01-operator-pack/cdc-feasibility-shape.fr.md`; `2026-suez-webuy/_external_marks/README.md`; `Clients/README.md` |
| **5. baseline_organisation** | 5 hits | `Legal Counsel`, `Legal Consumer Specialist`, `Legal Collaborator Specialist` (active roles); `Holistik Researcher Trainee` (P13.4 D-W13-E); CPO role-description references "Legal Counsel" + post-restructure landscape |
| **6. DECISION_REGISTER + INITIATIVE_REGISTRY** | (no new candidate-class evidence beyond what is already in the CSVs above) | n/a |

The temp-context corpus (~9 audio transcripts) is the strongest candidate-class signal because it captures the **operator's actual working network**: legal advisors at the constitution-desk bank (notary + asesoría legal), the EFA business-developer collaborator, ShadowGPU as a potential GPU-supplier-partner, market-survey signals from PESTEL studies, and rival app reviews from Websitz.

---

## 3. Ranked candidate-class table

| candidate_class | evidence_count | top_3_citations | confidence (0-5) | recommended_action | rationale |
|:---|---:|:---|---:|:---|:---|
| **`legal-counsel-external`** | 10+ (Asesoría Hostelería notary + Spanish constitution-desk attorney + Legal Counsel role role_description) | `Asesoria Hosteleria/2026-12-04 - Admin Course - 1.md` lines 156-176; `baseline_organisation.csv` row 60 (Legal Counsel role); `_engagement-template/README.md` | **5** | **add-to-enum** | Spanish notary + constitution-desk legal advisor evidenced. Currently mapped under `external_adviser` (overlapping with ENISA-track advisers). Splitting `external_adviser` → `external_adviser` (business/strategy advisers) + `legal-counsel-external` (legal-track advisers) clarifies governance and aligns with the existing Legal Counsel role hierarchy. |
| **`investor-inbound`** | 6+ (PRJ-HOL-FOUNDING-2026 dossier audience; ShadowGPU meeting partner-investor framing; ENISA dossier README investor_like_reader) | `deck_slides.yaml` (audience: ["enisa_adviser", "startup_certification_reader", "investor_like_reader"]); `ShadowGPU/27-02-2026 15.11 meeting.md` (partner+investor signals); `docs/references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/README.md` | **4** | **add-to-enum** | Clearly established audience for the company dossier. Materializes a real relationship class (capital provider) distinct from `external_adviser` (paid services) and `partner` (revenue-share collaboration). |
| **`business-developer-collaborator`** | 8+ (EFA Business Developer Onboarding transcript; EFA partner-lead two-hat posture; researcher-onboarding transcript) | `EFA/2026-12-12 - Holistika Research - Business Developer Onboarding.m4a.md`; `EFA/2026-04-17 - Researcher Onboarding.mp3.md`; `GOI-PRT-EFA-2026` notes |  **3** | **defer-to-I72** | Currently absorbed by `partner` (the EFA cobranding row). The "business-developer" sub-role inside a partner org is real but not a distinct relationship class; it is a **persona** within the partner relationship. Defer to I72 persona registry rather than enum-extending GOI class. |
| **`supplier-infrastructure`** | 9+ (ShadowGPU meeting; SaaS hosting; cloud bill discussions) | `ShadowGPU/27-02-2026 15.11 meeting.md` (9 hits); cost-of-goods discussion in Asesoría Hostelería transcripts | **3** | **add-to-enum** | GPU/cloud/hosting suppliers are a distinct relationship class (operator engages on commercial terms; not a partner, not a customer, not an adviser). Pre-empts I72 sourcing register schema friction. |
| **`recruiter-counterparty`** | 1 (HR-ops transcripts mention candidate sourcing but no third-party recruiter relationship) | Asesoría Hostelería 2026-30-04 m4a (passing reference); `baseline_organisation.csv` (no recruiter role); People Operations Lead role-description owns hiring directly | **1** | **reject (notes-only)** | Operator owns recruiting directly; no third-party recruiter relationships evidenced. Document in notes if/when a recruiter engagement materializes. |
| **`competitor-intelligence-target`** | 4 (Websitz Cart Bundle App review = competitor analysis; Rushly cahier des charges; PESTEL studies in Asesoría) | `Websitz/Use case 1/23-03-2026 Cart Bundle App review.mp3.md`; `Websitz/Use case 2/Rushly_Cahier_des_charges_v2.docx.md`; `Asesoria Hosteleria/2026-12-04 - PESTEL.md` | **2** | **reject (notes-only)** | Competitive intelligence targets are not a relationship class — the operator does not have a relationship with them; they are an audit subject. Best modeled as a `topic_id` or `intelligence_target` field, not a GOI class. Defer infrastructure to I72 IntelligenceOps register. |
| **`media-counterparty`** | 0 (no PR/journalist contacts evidenced) | (none) | **0** | **reject (notes-only)** | No current media relationships. Activates with Marketing/Storytelling PR Manager (already in baseline post-P8.2); when a real journalist relationship lands, document in notes first, promote to enum if pattern recurs. |
| **`regulatory-body`** | 1 (ENISA references; speculative EU AI Act counterparty mentions) | `ENISA_EVIDENCE_PACK_HOLISTIKA_RESEARCH_2026-04.md`; deck_slides audience `enisa_adviser` | **2** | **defer-to-I72** | ENISA itself is the regulator; current `external_adviser` row (`GOI-ADV-ENTITY-2026`) is the firm that interfaces with ENISA. The regulator is a step removed; modeling ENISA as a GOI row is premature until direct interaction (e.g., site visit, formal correspondence) occurs. Defer to I72 regulatory-relationship roadmap. |
| **`internal-trainee`** | 1 (`Holistik Researcher Trainee` role added P13.4 D-W13-E) | `baseline_organisation.csv` row 63 (Holistik Researcher Trainee) | **2** | **reject (notes-only)** | Trainees are internal employees, not external relationships. Already covered by `entity_kind=person` + `class=internal_employee` (currently absent because no internal-employee rows; that's because GOI/POI is for **external** relationships per dimension definition). Internal employees belong in `baseline_organisation.csv` only. |

---

## 4. Inline-ratify gate

Per A14 + H1, the agent surfaces these candidates via `AskQuestion` (next step in the same chat). Operator picks one of 3 actions per candidate:

- `add-to-enum`: agent extends the GOI_POI_REGISTER `class` enum (no DDL since the column is plain `TEXT`; CSV-level + downstream consumers).
- `defer-to-I72`: agent records the deferral in `INITIATIVE_REGISTRY.csv` (under I72) without enum extension.
- `reject (notes-only)`: agent documents the candidate in this report's §6 audit log; future occurrences go in `notes` field of existing row classes.

---

## 5. Post-ratify execution plan

After operator response:

1. **For each `add-to-enum` candidate**:
   - Add a concrete row in `GOI_POI_REGISTER.csv` if a real instance exists today (e.g., the Spanish constitution-desk legal counsel; the ShadowGPU GPU supplier).
   - Update `ENGAGEMENT_REGISTRY.csv` `engagement_class` enum if applicable.
   - No supabase migration required (the `class` column is plain `TEXT` per `20260429081728_i21_compliance_goipoi_register_mirror.sql`).

2. **For each `defer-to-I72` candidate**:
   - Add a row in `INITIATIVE_REGISTRY.csv` linking to I72 (Marketing area governance + persona registry expansion).
   - No CSV mutation here.

3. **For each `reject (notes-only)` candidate**:
   - Document in §6 of this report (audit log).

4. **D-IH-70-AC** (this decision): record ratification outcomes in `DECISION_REGISTER.csv`.

5. **Validators**: `py scripts/validate_hlk.py`, `py scripts/test.py all`.

6. **Commit**: atomic single-commit per A5 discipline.

---

## 6. Audit log — ratification outcomes

Operator response received inline 2026-05-13 (interrupted-and-resumed AskQuestion). Decisions ratified at the second-pass synthesis turn.

| candidate_class | operator_decision | decision_source | timestamp | notes |
|:---|:---|:---|:---|:---|
| `legal_counsel_external` | **add-to-enum + concrete row** | `q1=A` (inline) | 2026-05-13 | New class added; concrete `GOI-LEG-CONST-2026` row added (Spanish constitution-desk legal counsel firm, `is_public_entity=false`, stance=ally, distance_band=N1). |
| `investor` (was `investor-inbound`) | **add-to-enum + concrete row + e2e sweep** | `q2=A`+ (inline) | 2026-05-13 | Class already in validator enum (I22 P4 D-IH-5); concrete `GOI-INV-ENISA-2026` row added (Spanish state-backed startup investor, `is_public_entity=true`, stance=neutral, distance_band=N2 bridged through GOI-ADV-ENTITY-2026). E2E sweep covered ENISA + CDTI + fondos europeos + ShadowGPU partner-investor blur + dossier audience targeting. |
| `supplier_infrastructure` | **add-to-enum + concrete row** | `q3=A` (inline) | 2026-05-13 | New class added; concrete `GOI-SUP-SHGPU-2026` row added (GPU/cloud supplier candidate per 27-02-2026 meeting transcript, `is_public_entity=false`, stance=neutral pending commercial-terms ratification, distance_band=N1). |
| `business-developer-collaborator` | **defer to I72** | `q4=A` (inline) | 2026-05-13 | Best modeled as persona within existing `partner` class. INITIATIVE_REGISTRY row added for `INIT-OPENCLAW_AKOS-72` (Marketing area governance + persona registry expansion + IntelligenceOps register expansion). |
| `competitor_intelligence_target` | **add-to-enum (operator override)** | `q5` (inline, operator override) | 2026-05-13 | Operator surfaced v2.7 ally/neutral/enemy doctrine during Q5 deliberation; recommended A (reject as audit-subject) was overridden with "we are researching having GOI/POI competitors too will help our intel ops across the board". Class added; concrete competitor rows deferred to I72 IntelligenceOps register schema work. **Sister event**: ratifying the new schema dimension `stance` (D-IH-70-AD) which encodes the v2.7 doctrine as a first-class column. See `docs/references/hlk/v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md`. |
| `recruiter` | **add-to-enum (pre-emptive)** | `q6=C` (inline) | 2026-05-13 | New class added pre-emptively; no concrete row yet (revisit when operator engages a third-party recruiter). |
| `media` | **already in enum (no-op)** | `q6=C` (inline) | 2026-05-13 | Class already in validator enum since I22 P4 D-IH-5. Pre-emptive Q6 selection lands as a no-op for class addition; concrete row deferred until first PR/journalism relationship lands (post-Marketing/Storytelling PR Manager activation). |
| `regulator` | **already in enum (no-op)** | `q6=C` (inline) | 2026-05-13 | Class already in validator enum since I22 P4 D-IH-5. Pre-emptive Q6 selection lands as a no-op; ENISA itself currently captured as `investor` (capital-flow is the operative relationship); regulator-relationship roadmap deferred to I72 when ENISA correspondence becomes direct. |
| `internal-trainee` | (not asked; resolved during table authoring) | report §3 | 2026-05-13 | Trainees are internal employees → covered by `baseline_organisation.csv` only; outside GOI/POI scope. No action. |

**Schema extensions ratified** (operator-prompted Q5 surfacing → D-IH-70-AD):

- New column `stance` on GOI_POI_REGISTER.csv with enum `ally / neutral / enemy / unknown / empty`.
- All 14 existing rows backfilled with operator-judgment stance values (8 ally, 5 neutral, 1 ally Asesoría related-party).
- Validator (`scripts/validate_goipoi_register.py`) extended with `STANCES` enum constant.
- Mirror DDL (`supabase/migrations/20260513150000_i70_p85_goipoi_stance_and_class_enum_extension.sql`): adds stance column + CHECK constraint + covering index; tightens class enum CHECK to the documented 19-value superset.
- Test (`tests/test_validate_goipoi_register.py`) updated: header `[-1] == "stance"` invariant replaces former `[-1] == "related_party"`; new test for stance enum validity.
- Canonical doctrine doc: `docs/references/hlk/v3.0/Research/Intelligence/canonicals/GOI_POI_STANCE_DOCTRINE.md`.

---

## 7. Cross-references

- `D-IH-70-G` (P3 GOI/POI register seed-rows ratification — supersedes by extending enum at P8.5)
- `D-IH-70-N` (P3 GOI hunt deferral with inline-ratify discipline)
- `D-IH-70-AC` (this hunt's ratification record — to be added)
- `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/GOI_POI_REGISTER.csv` — target CSV
- `supabase/migrations/20260429081728_i21_compliance_goipoi_register_mirror.sql` — mirror DDL (no enum CHECK on `class`)
- `.cursor/rules/akos-inline-ratification.mdc` — A14 inline-ratify pattern
