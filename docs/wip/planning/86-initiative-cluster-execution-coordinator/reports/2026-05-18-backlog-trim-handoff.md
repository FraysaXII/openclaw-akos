---
status: active
role_owner: PMO
co_owner_role: Founder
area: PMO
plane: governance
authored: 2026-05-18
last_review: 2026-05-18
intellectual_kind: chat_session_handoff
sharing_label: internal_only
linked_decisions:
  - D-IH-89-A
  - D-IH-89-B
  - D-IH-89-C
  - D-IH-89-D
  - D-IH-89-E
  - D-IH-89-G
  - D-IH-89-H
  - D-IH-89-I
  - D-IH-89-J
  - D-IH-89-K
  - D-IH-89-L
  - D-IH-89-M
  - D-IH-89-N
linked_ops_actions:
  - OPS-86-5
linked_initiatives:
  - INIT-OPENCLAW_AKOS-86
  - INIT-OPENCLAW_AKOS-89
  - INIT-OPENCLAW_AKOS-66
  - INIT-OPENCLAW_AKOS-56
---

# 2026-05-18 Backlog-trim chat — closure handoff + rankings + next-chat brief

> **Purpose.** Persistent record of the 2026-05-18 multi-lane backlog-trim chat. Three deliverables: (1) ADVOPS plane integrity + completion ranking versus the post-I72 / v3.1 doctrine; (2) every-active-initiative integrity + completion ranking; (3) full context-pack for the next chat to continue with Lanes 2-5 without losing momentum.
>
> **Why a file (not just chat output).** The next chat starts fresh; this file is the operator-and-agent-readable handoff that survives the context reset.

---

## 1. ADVOPS plane integrity + completion ranking (vs v3.1 doctrine)

**Headline.** ADVOPS as a plane is **structurally pre-I72-doctrine** — it shipped 24+ canonicals fast under the 2026-04-25 → 2026-05-10 rush to support the Holistika incorporation engagement, before the I72 process-catalog architecture + akos-executable-process-catalog.mdc rule + cross-area Data-Owner discipline + akos-people-discipline-of-disciplines.mdc rule ratified. The plane works for its immediate purpose (unblocking the founder vis-a-vis legal + ENISA + bank advisers) but the **structural retrofit** to fit the v3.1 architecture has not happened.

> **Decision ratified this chat (D-IH-89-I):** the ADVOPS harmonization sweep is folded into **I56 P5+** rather than spawned as a new initiative. I56 already owns the adviser-engagement charter at the canonical-CSV layer; ADVOPS is structurally a P5+ extension of I56, not a new architecture.

### 1.1 Per-dimension ranking (1 = lowest integrity; 10 = doctrinally clean)

| # | Dimension | Score | What is present | What is missing (folded into I56 P5+) |
|:-:|:---|:-:|:---|:---|
| 1 | **Canonical CSV register integrity** (ADVISER_ENGAGEMENT_DISCIPLINES / ADVISER_OPEN_QUESTIONS / FOUNDER_FILED_INSTRUMENTS / GOI_POI_REGISTER) | **7/10** | 17 ADVOPS-adjacent canonical CSVs exist + Pydantic models + `validate_hlk.py` reads them. | No Supabase mirror tables for the 4 ADVOPS-specific CSVs (`compliance.adviser_engagement_disciplines_mirror`, `..._open_questions_mirror`, `founder_filed_instruments_mirror`, `goipoi_register_mirror`) per I21 design. |
| 2 | **Process catalog integrity** (process_list.csv rows for ADVOPS-authored processes) | **3/10** | Some PMO processes exist (`hol_opera_dtp_311..312`, `hol_peopl_dtp_303..304`, `thi_legal_dtp_304`, `hol_opera_ws_5`) referenced by SOP-EXTERNAL_ADVISER_ENGAGEMENT_001. | Most ADVOPS-author processes (dossier-mint, deck-sync, cover-email-mint, handoff-mint, Q-row maintenance, instrument-filing) are NOT registered in process_list.csv. Owner: I56 P5+. |
| 3 | **SOP + runbook pairing** (per `akos-executable-process-catalog.mdc` RULE 1) | **4/10** | SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md exists at status: active. `scripts/export_adviser_handoff.py` exists as paired runbook for that SOP. | Most ADVOPS SOPs have NO paired runbook (dossier-rendering, deck-sync-from-strategy, cover-email-compose, Q-row-maintenance). Owner: I56 P5+. |
| 4 | **Asset-bucket layout** (per I22 + D-IH-89-H) | **9/10** | Post-D-IH-89-H rename: `_assets/advops/2026-holistika-incorporation/` reads cleanly in Obsidian + GitHub trees; cross-area README documents the engagement-slug-vs-program_id convention; PROGRAM_ID_CONSISTENCY validator updated; BBR validator exempts frontmatter. | Sub-folder name `adviser_handoff` (underscore) vs BBR validator glob `adviser-handoff` (hyphen) — known governance gap; resolution in I56 P5+ (either rename folder or widen glob). |
| 5 | **Dual-register integrity** (BBR contract per `akos-brand-baseline-reality.mdc`) | **9/10** | All BBR-scoped ADVOPS surfaces (dossier_*.md, deck/*.yaml, deck_slides.yaml, founder-filed/**, adviser-handoff/*.md) PASS the drift gate. Companion files (.objections.md, .counterparty-brief.md) intentionally exempt. | Validator glob doesn't yet cover `adviser_handoff/` (underscore) folder — see #4. |
| 6 | **External-register prose quality** (handoff + cover emails + dossier) | **8/10** | Legal-constitutor handoff rewritten with 6-name list + CIRCE/AT-Pymes + uncapped asset table + joint-confirm CNAE framing. Three cover emails (Noelia + Guillermo-dossier + Guillermo-evidence) carry consistent voice + decision-trail. Dossier has Q-citation appendix. | Dossier still uses the legacy 4-ENISA-pillar structure (Mercantil/Mercado/Financiacion/Operativa). Full KILLER 5-pillar re-architecture (WHO/WHAT/WHY-DIFFERENT/TRACTION/ASK + executive summary + PDF-export-ready visual system) deferred to next chat as Wave 2m+ — see §3.4. |
| 7 | **Recipient-name discipline** (per D-IH-89-N) | **10/10** | All committed cover emails use `Hola [nombre del asesor],` placeholder pattern; SMTP-send hook resolves real names off-repo. Tests updated to accept new pattern alongside legacy for backward-compat. | None. |
| 8 | **Cross-area governance wiring** (PMO + Compliance + Legal + Brand) | **6/10** | Cross-area README at the asset-bucket root documents the wiring; reciprocal cross-link from engagement-folder README; frontmatter `linked_decisions` + `linked_canonicals` consistent across the rewritten artifacts. | RevOps + Marketing/Reach + Operations/SMO adapters NOT yet wired (per akos-executable-process-catalog.mdc RULE 4 DAMA-DMBOK alignment). Owner: I56 P5+. |
| 9 | **Decision-trail completeness** | **10/10** | All decisions taken in this chat minted in DECISION_REGISTER.csv with full `linked_*` cross-references (D-IH-89-A through -N, excluding -F). | None. |
| 10 | **Test coverage** | **9/10** | 53 ADVOPS-touching tests all green (`test_render_dossier`, `test_company_deck`, `test_deck_slides_schema`, `test_deck_jargon`). Two tests updated to ratify the D-IH-89-N ref-placeholder doctrine. | No test yet enforces that every `cc_ref_ids:` entry resolves to a row in `GOI_POI_REGISTER.csv` — defer to I56 P5+ as a 1-hour validator-mint task. |

### 1.2 Aggregate ADVOPS integrity score

**7.5 / 10** — high enough to ship the founder's immediate adviser-unblock work safely; low enough to demand the I56 P5+ structural retrofit. ADVOPS is **not** broken — it is **load-bearing for the founding engagement** — but its structure was minted before the v3.1 doctrine and needs to absorb the post-I72 patterns (process catalog + SOP-runbook pairing + Data Owner per DAMA + cross-area integration spine) to scale beyond this single engagement.

### 1.3 What "superseded" means for ADVOPS

ADVOPS is **not deprecated** and **not superseded** in the registry-status sense. The word "superseded" the operator used refers to the **architectural layer underneath ADVOPS** — specifically:

- The cross-area integration pattern that I72 introduced (Normalized Adapter Pattern per Truto/Unified.to consensus 2026; akos-executable-process-catalog.mdc RULE 2 adapter status metadata).
- The process-list discipline that I72 P8 + akos-executable-process-catalog.mdc RULE 1 pairing rule introduced.
- The Data Owner discipline (DAMA-DMBOK 2.0) that I72 P9 + akos-people-discipline-of-disciplines.mdc surfaced.

ADVOPS was minted **before** those rules ratified, so it doesn't follow them yet. That's the "superseded" — the architecture has moved on; ADVOPS hasn't been retrofitted. **D-IH-89-I folds the retrofit into I56 P5+** so it happens inside a governed initiative with proper decision-log + risk-register + plan-quality bar.

---

## 2. Active-initiative integrity + completion ranking (18 active)

**Method.** Score each active initiative on (a) decision-trail completeness, (b) phase-execution velocity, (c) verification-matrix coverage, (d) cross-area harmonization. Aggregate is qualitative (1-10), not arithmetic — execution context matters.

| ID | Title (truncated) | Owner | Anchor | Cycle / Cadence | Integrity | Completion | Next move |
|:--:|:---|:---|:---|:---|:-:|:-:|:---|
| **I03** | HLK governed KM — workspace master roadmap | PMO | PGF-2026 | continuous | 8/10 | rolling | Continuous; no scheduled phase. |
| **I11** | MADEIRA day-to-day ops copilot | PMO | MAD-2026 | program-line | 7/10 | 60% | Awaits I76 elevation; co-evolves with KB stewardship. |
| **I17** | MADEIRA Cursor mode parity (Ask / Plan / Run) | PMO | MAD-2026 | program-line | 6/10 | 40% | Lower priority; resumes when MADEIRA Mission Control (I62) lands. |
| **I24** | Communication Methodology + Eloquence-Layer Composer | PMO | MKT-2026 | program-line | 9/10 | 75% | Continuous refinement; the cover-email rewrites this chat consume it. |
| **I56** | First-response cycle (Adviser engagement operations) | PMO | OPS-2026 | program-line | 7/10 | 50% | **HIGH PRIORITY — P5+ charter expansion needed** for ADVOPS retrofit per D-IH-89-I. Owner picks up in next chat. |
| **I62** | MADEIRA Mission Control on hlk-erp | System Owner | INF-2026 | program-line | 7/10 | 55% | Sibling-repo execution; awaits Mission-Control panel rollout. |
| **I63** | External Repo Governance Codification | DevOps | INF-2026 | continuous | 9/10 | rolling | Continuous; mirror-template rule already cursor-loaded across sibling repos. |
| **I64** | Governance Mission Control on hlk-erp | System Owner | PGF-2026 | program-line | 8/10 | 70% | Sibling-repo execution; Mission Control surfaces I86 cluster status. |
| **I65** | AKOS Planning Workspace Panel | System Owner | PGF-2026 | program-line | 8/10 | 65% | Sibling-repo execution. |
| **I67** | RevOps Discovery | Brand & Narrative Mgr | MKT-2026 | program-line | 8/10 | 60% | Co-evolves with I72-promoted REVOPS_PROCESS_CATALOG; expands with first paying engagement. |
| **I68** | CICD Discipline + Observability Maturity + InfraMonitor | System Owner | INF-2026 | program-line | 9/10 | 80% | Round 2 plan in execution; on track. |
| **I78** | Brand-voice LLM-as-judge advisory layer (Tier 2) | Brand & Narrative Mgr | MKT-2026 | program-line | 8/10 | 30% | Lane-2 closure-sweep candidate; check P1-P3 status next chat. |
| **I81** | Vault integrity sweep + Compliance layout reorg | PMO | PGF-2026 | program-line | 7/10 | 15% | **HEAVY long-pole (Lane 3a-3c).** Heavy canonical-CSV gate; needs P1-P4 first half in next chat. |
| **I82** | Holistika Capability Doctrine and Commercial Readiness | PMO | PEO-2026 | program-line | 7/10 | 20% | **Lane 3b** — interleaves with I81; P1-P4 + closure in weeks 2-5. |
| **I85** | Audience-tag canonicalization (J-* codes from brand matrix) | Brand & Narrative Mgr | MKT-2026 | program-line | 9/10 | 90% | **Lane 2 closure-sweep candidate** — should be the FIRST closure to advance the I86 burndown 1/10 → 2/10. |
| **I86** | Initiative Cluster Execution Coordinator (Waves 1-5 burndown) | PMO | PGF-2026 | event-driven | 9/10 | 35% | **Cluster orchestrator** — closes when all 10 siblings close. Currently 1/10 closed (I88). |
| **I87** | OpenClaw operator-runtime hardening | System Owner | INF-2026 | program-line | 7/10 | 60% | **Lane 2 closure-sweep candidate**. |
| **I89** | HLK-ERP persona-rollup panel implementation (six routes) | PMO | INF-2026 | program-line | 8/10 | 20% | **Lane 4** — Wave-2 promoted this chat (D-IH-89-A); P1-P5 sibling-repo execution in weeks 2-5. |

### 2.1 Aggregate active-cluster integrity

**7.8 / 10** — strong; reflects the I72 + I79 + I80 governance ratifications that hardened the base. The **completion** distribution is the real signal:

- **Near-closure** (≥ 80%): I85 (90%), I68 (80%) → closure-sweep candidates this week.
- **Mid-execution** (50-79%): I03 (rolling), I24 (75%), I64 (70%), I65 (65%), I67 (60%), I87 (60%), I62 (55%), I56 (50%) → continuous polish; I56 needs the explicit P5+ expansion (D-IH-89-I).
- **Early execution** (15-49%): I11 (60% — older), I17 (40%), I78 (30%), I82 (20%), I89 (20%), I81 (15%) → Lane 3a/3b/4 candidates.

### 2.2 Recommended sequencing for the next 2 weeks (per backlog plan ratified earlier this chat)

| Lane | What | Initiatives | Weeks | Priority signal |
|:---|:---|:---|:---|:---|
| **2** | Closure-sweep (move I86 burndown 1/10 → 4/10) | I85 + I87 + I78 | Week 1 (next chat) | High — closing 3 siblings unlocks I86 cluster-closure trajectory. |
| **3a** | I81 P1-P4 long-pole first half (canonical-CSV gate) | I81 | Weeks 1-3 | Critical — vault integrity sweep is overdue. |
| **3b** | I82 P1-P4 + closure (interleaves with I81) | I82 | Weeks 2-5 | High — Holistika Capability Doctrine + Commercial Readiness gates inbound investor / partner conversations. |
| **4** | I89 P1-P5 sibling-repo execution (6 panel routes in hlk-erp) | I89 | Weeks 2-5 | High — promotes the persona-rollup UX surface that I64 + I65 + I62 + I68 all consume. |
| **5** | Newly-promoted execution | I76 + I74 + I83 (and I75 if Lane 1 promoted) | Weeks 3-6 | Medium — start when Lane 3a clears. |
| **3c** | I81 P5-P8 tail (per-area background retrofit) | I81 | Weeks 4-6 | Medium — extends after I81 P1-P4 closes. |
| **closure** | I86 cluster-closure | I86 | Weeks 7-8 | Terminal — closes the orchestrator once 10/10 siblings closed. |

---

## 3. Next-chat context-pack (everything needed to resume Lanes 2-5)

> **Goal.** A new chat starts; the operator types something like *"continue from last chat"*. The next agent reads THIS section first and has everything needed to make the right next move.

### 3.1 Where the founding-engagement work stopped (Lane 1 status)

**SUBSTANTIALLY COMPLETE.** The legal-constitutor handoff is unblocked for sending. The dossier carries the Q-citation appendix (all 12 Q-IDs cited). The decision trail is fully minted (D-IH-89-A through -N, excluding -F). All validators (BBR, HLK, vault-links) PASS. 53 ADVOPS-touching tests PASS.

**WHAT THE OPERATOR CAN SEND NOW:**

- [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md`](../../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md) — handoff doc, PDF-exportable, complete with 6-name list + CNAE 7219 joint-confirm + CIRCE/AT-Pymes route + 3k/5k capital + uncapped asset template.
- [`docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md`](../../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/cover_email_legal_constitutor_es.md) — cover email for Noelia (legal); CC's Guillermo (ENISA) for the joint-confirm + AT-Pymes AM (operational coordination).
- [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md`](../../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_company_dossier/cover_email_company_dossier_es.md) — cover email for Guillermo (dossier); now references the joint-confirm CNAE 7219 framing.
- [`docs/references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md`](../../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/enisa_evidence/cover_email_es.md) — cover email for Guillermo (evidence appendix); same joint-confirm posture.

**WHAT THE OPERATOR STILL OWES THE NEXT CHAT:**

1. **Asset inventory close-out** (serial numbers + purchase year + purchase price + estimated current value) — the legal handoff §5.1 has 20 placeholder rows; founder fills rows 1-2 (PC + phone) as mandatory + however many of rows 3-20 are real.
2. **Cash transfer amount decision** — within [3,000 − in-kind, 5,000 − in-kind] EUR band; decided as late as signing-day − 7.
3. **Real recipient-names** — resolved at SMTP-send time from GOI_POI off-repo (per D-IH-89-N); the operator already knows Noelia (legal) and Guillermo (ENISA) and the AT-Pymes AM Javier.
4. **Portal field-map (Wave 2q)** — if the operator wants the agent to map the Ayuda-T-Pymes portal fields, the next chat needs the portal URL + auth method (browser MCP cannot survive auth from one chat to another).

### 3.2 What changed in this chat (the audit trail)

**13 decisions minted** (D-IH-89-A through -N, F skipped):

| ID | Class | Title |
|:---|:---|:---|
| D-IH-89-A | architecture | I89 promotion from candidate to active |
| D-IH-89-B | scope | I89 scope = all six persona panel routes |
| D-IH-89-C | architecture | I89 cadence = six-phase cross-cutting (concern-sliced) |
| D-IH-89-D | governance | I89 ownership = tri-co-owned (System Owner + PMO + Brand) |
| D-IH-89-E | governance | BBR drift-gate severity flip INFO → FAIL |
| D-IH-89-G | closure | OPS-86-5 closed — ADVOPS harmonization sweep COMPLETE |
| D-IH-89-H | architecture | ADVOPS asset-bucket dirname = engagement-slug (operator override) |
| D-IH-89-I | scope | ADVOPS harmonization sweep folded into I56 P5+ |
| D-IH-89-J | governance | SL six-name candidate list (Research/Studio/Works/Lab/Logos/Compass) |
| D-IH-89-K | execution | CNAE 7219-primary joint-confirm with ENISA-track |
| D-IH-89-L | execution | CIRCE telematic via Ayuda-T-Pymes + BBVA partnership |
| D-IH-89-M | execution | Capital 3k floor / 5k stretch + uncapped asset table |
| D-IH-89-N | governance | Ref-placeholder doctrine (cover emails) |

**Key file changes (broad strokes — see `git status` for the canonical list):**

- Directory rename: `_assets/advops/PRJ-HOL-FOUNDING-2026/` → `_assets/advops/2026-holistika-incorporation/` (33 active files updated; 41 historical files preserved per audit-trail).
- 2 validator upgrades: `validate_program_id_consistency.py` (engagement-slug-aware), `validate_brand_baseline_reality_drift.py` (frontmatter-exempt).
- 1 script upgrade: `render_dossier.py` (program_id → engagement-slug lookup map for ADVOPS).
- 6 cover-email + handoff rewrites (legal-constitutor + 2 ENISA + Q-citation appendix).
- 2 test files patched (D-IH-89-N pattern accepted).
- DECISION_REGISTER.csv += 7 rows (H, I, J, K, L, M, N).

### 3.3 Open questions deferred to operator (not blocking but pending)

| Q | Topic | Owner | Recommended next move |
|:---|:---|:---|:---|
| Q-CRT-001..003 | ENISA reparto documental + plan-de-negocio + financiación | Guillermo (ENISA-track) | Send dossier + apéndice de evidencias; cover email already routes the question. |
| Q-LEG-001 | Objeto social + CNAE primario joint-confirm | Noelia + Guillermo | Send the handoff + cover email (legal-constitutor); operator available for 3-way call. |
| Q-LEG-002..005 | CIRCE template fit + capital legal basis + holding-forward considerations | Noelia | Bundled in same handoff send. |
| Q-FIS-001..002 | Pluriactividad + pre-incorporation infrastructure tax treatment | AT-Pymes gestoría (post-constitution) | First post-constitution monthly call. |
| Q-IPT-001 | EUIPO + OEPM trademark filing plan | Future trademark-track adviser | Post-constitution; out of this engagement's scope. |
| Q-BNK-001 | KYC + constitution-account opening | BBVA partner (operationally handled by AT-Pymes AM) | Triggered automatically by the AT-Pymes bundle. |

### 3.4 Wave 2m+ — KILLER dossier full re-architecture (deferred to next session)

**Spec.** The current dossier is structurally a 4-ENISA-pillar evidence appendix (Mercantil / Mercado / Financiación / Operativa). The KILLER rewrite reorganizes around 5 PITCH pillars while keeping ENISA-pillar mapping visible:

| Pillar | Reads to | Maps to ENISA |
|:---|:---|:---|
| **WHO** — Quiénes somos | Founder + investor + partner | ENISA Pilar I (Mercantil) — quién es la empresa registrada |
| **WHAT** — Qué hacemos | Founder + investor + partner | ENISA Pilar I+II — actividad económica + innovación scope |
| **WHY-DIFFERENT** — Por qué somos diferentes | Investor + partner | ENISA Pilar II — diferenciación / innovación |
| **TRACTION** — Tracción y momentum | Investor + ENISA | ENISA Pilar III + IV — Financiación + Operativa (evidencia) |
| **ASK** — Pedida / qué ofrecemos | Each audience | ENISA Pilar I (certificación) + investor / partner framing |

**Acceptance criteria for the KILLER rewrite:**

1. Executive summary front-page (one page, scannable, 6 rows + small stat-grid).
2. 5 pillars in order WHO → WHAT → WHY-DIFFERENT → TRACTION → ASK; each pillar explicitly names which ENISA pillar(s) it maps to.
3. Q-citation appendix preserved (per test_dossier_cites_every_active_q_row).
4. PDF-export-ready visual system (clean print layout; consistent typographic hierarchy; one stat-grid per pillar; one pull-quote per pillar; no operator-internal language).
5. Web-export-ready (could become a landing page or one-pager) — Markdown semantics survive PDF + HTML render.
6. BBR-compliant (no `PRJ-HOL-*` tokens in body; frontmatter exempt per D-IH-89-H).
7. Voice-aligned with the BRAND_VOICE_FOUNDATION + BRAND_SPANISH_PATTERNS + ANTI-jargon mandate per People-as-DoD rule.
8. ENISA evaluator can read it in 5 minutes; investor in 3 minutes; partner in 4 minutes.

**Companion deliverables for the same wave:**

- `deck_slides.yaml` re-architected to match the 5 pillars (12 slides → 8-10 slides; slide 11 governance-metrics quote already up-to-date with 28 / 1.169 / 67).
- `deck_story_es.md` re-written.
- `deck-visual-system.md` updated to reflect the new pillar-aligned visual grammar.
- Tests updated to assert the new structure (test_dossier_pillars_present + test_dossier_executive_summary_present).

**Estimated effort.** 0.5-1.0 person-week for the rewrite + 0.2 person-week for the test refresh + 0.1 person-week for the deck sync.

### 3.5 Concrete next-chat opening prompts (operator picks one)

| Prompt | Triggers | Estimated chat shape |
|:---|:---|:---|
| *"continue from last chat — close Lane 2 (I85 + I87 + I78)"* | Lane 2 closure-sweep | 1-2 hours; 3 sibling closures; I86 burndown moves 1/10 → 4/10 |
| *"do the KILLER dossier rewrite per Wave 2m spec"* | Wave 2m+ | 2-3 hours; dossier + deck + tests; ENISA-ready output |
| *"start I81 P1 — vault integrity sweep"* | Lane 3a long-pole | 2-4 hours; heavy canonical-CSV gate; needs operator approval at the P1 commit |
| *"start I89 P1 — hlk-erp persona-rollup"* | Lane 4 sibling-repo | 2-3 hours; bless_external_repo flow + 6 panel routes |
| *"promote I76 + I74 + I83"* | Lane 5 promotion | 1 hour; charter mint + frontmatter + planning folder stubs |
| *"map the Ayuda-T-Pymes portal"* | Wave 2q | 1-2 hours; requires portal URL + browser MCP auth |

### 3.6 Files the next agent should read first (in priority order)

1. **This file** (`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/2026-05-18-backlog-trim-handoff.md`) — the handoff.
2. [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](../master-roadmap.md) — cluster orchestrator.
3. [`docs/wip/planning/86-initiative-cluster-execution-coordinator/decision-log.md`](../decision-log.md) — cluster decision log.
4. [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) — full canonical decision register (tail rows: D-IH-89-H through -N this chat).
5. [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) — 18 active initiatives.
6. Then: whichever Lane the operator picks (Lane 2 → I85 + I87 + I78 master-roadmaps; Lane 3a → I81 master-roadmap + plan; Lane 4 → I89 master-roadmap + plan).

### 3.7 Cursor rules the next agent inherits (always-applied)

- [`akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc) — initiative discipline.
- [`akos-people-discipline-of-disciplines.mdc`](../../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) — People as DoD.
- [`akos-mirror-template.mdc`](../../../../../.cursor/rules/akos-mirror-template.mdc) — AKOS as SSOT for sibling repos.
- [`akos-inline-ratification.mdc`](../../../../../.cursor/rules/akos-inline-ratification.mdc) — inline-ratify pattern.
- [`akos-holistika-operations.mdc`](../../../../../.cursor/rules/akos-holistika-operations.mdc) — Supabase + compliance ops.
- [`akos-governance-remediation.mdc`](../../../../../.cursor/rules/akos-governance-remediation.mdc) — guardrails.
- [`akos-executable-process-catalog.mdc`](../../../../../.cursor/rules/akos-executable-process-catalog.mdc) — SOP+runbook pairing.
- [`akos-brand-baseline-reality.mdc`](../../../../../.cursor/rules/akos-brand-baseline-reality.mdc) — dual-register (CRITICAL for any external prose).
- [`akos-agent-checkpoint-discipline.mdc`](../../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — pause-point + self-checkpoint cadence.

### 3.8 Two principles to carry forward from this chat (operator-emphasized)

1. **"It's no use to be indefinitely horizontal. Clever designs are what really makes us governed and scalable but holistik."** — The 6-name SL list + the 5-pillar dossier spec + the engagement-slug dirname convention all embody this: pick the clever design, then make it holistik in the small choices that follow. Don't conflate horizontal-scope with shapelessness.
2. **"Every initiative makes us stronger and any artifact I send carries our best and updated quality."** — The Q-citation discipline + the cover-email joint-confirm framing + the recipient-name placeholder pattern (D-IH-89-N) all serve this: any send-ready artifact reflects current governance, not the governance of the day it was first drafted.

---

## 4. Clean-git posture for this chat

This file is the closure record for the 2026-05-18 backlog-trim chat. The git commit posture (3 commits, logical chunks):

1. **Chore: ADVOPS asset-bucket directory rename + validator + script upgrades + dossier surgical fixes (D-IH-89-H + D-IH-89-N)**
   - `git mv _assets/advops/PRJ-HOL-FOUNDING-2026 _assets/advops/2026-holistika-incorporation`
   - 33 active-file path-reference updates (bulk script ran + deleted).
   - `validate_program_id_consistency.py` engagement-slug-aware.
   - `validate_brand_baseline_reality_drift.py` frontmatter-exempt.
   - `render_dossier.py` engagement-slug mapping.
   - `sync_deck_from_strategy.py` / `build_company_deck.py` / `lint_brand_voice_offline.py` path updates.
   - Cross-area README rewrite at `_assets/advops/2026-holistika-incorporation/README.md`.
   - Dossier surgical fixes: Q-citation appendix + CIRCE route corrections + appendix renumbering.
   - Test patches: D-IH-89-N placeholder pattern + slide 11 governance count (1.168 → 1.169).
   - Asset-bucket README + reciprocal cross-link.
2. **Feat: Legal-constitutor handoff rework + cover-email mint (D-IH-89-J/K/L/M)**
   - `legal-constitutor-handoff-2026-05-18.md` rewritten end-to-end (6 names, CNAE 7219 joint-confirm, CIRCE/AT-Pymes route, 3k/5k capital, uncapped asset table).
   - NEW `cover_email_legal_constitutor_es.md` (Noelia primary; Guillermo + AT-Pymes AM in CC).
   - Existing ENISA cover emails updated for joint-confirm framing.
3. **Chore: Decision-register mint (D-IH-89-H through -N) + planning handoff record (THIS FILE)**
   - DECISION_REGISTER.csv += 7 rows.
   - `2026-05-18-backlog-trim-handoff.md` (this file).
   - `release-gate.py` comment refresh (OPS-86-5 closure).

---

## 5. Cross-references

- Parent initiative: [`INIT-OPENCLAW_AKOS-86`](../master-roadmap.md) — initiative cluster execution coordinator.
- Pre-cursor: [`reports/ops-86-5-closure-evidence-2026-05-18.md`](./ops-86-5-closure-evidence-2026-05-18.md) — OPS-86-5 closure record (the trigger for this chat).
- Decision register: [`DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv) rows D-IH-89-A through D-IH-89-N.
- Initiative register: [`INITIATIVE_REGISTRY.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) — 18 active.
- OPS register: [`OPS_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) — OPS-86-5 closed; future OPS rows for Wave 2q + I56 P5+ at next chat.
- Founding-engagement bundle: [`Think Big/Advisers/2026-holistika-incorporation/`](../../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/) — operator-facing engagement folder (where the next chat's "send to advisers" action runs from).
- ADVOPS asset bucket: [`_assets/advops/2026-holistika-incorporation/`](../../../../references/hlk/v3.0/_assets/advops/2026-holistika-incorporation/) — external-facing collateral.
