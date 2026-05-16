---
language: en
status: active
authored: 2026-05-15
last_review: 2026-05-16
role_owner: PMO
classification: fact
ssot: true
---

# Initiative dependency map (I59..I80)

> **Purpose.** Single visual + tabular source of truth for how Holistika initiatives block, unblock, or loosely couple to each other. Companion to [`PLANNING_COMPENDIUM.md`](PLANNING_COMPENDIUM.md) and entry point for the agent during compendium §3.2 read-pass.
>
> **When to update.** Every initiative promotion (candidate → active); every TRIGGER-watch resolution (TRIGGER fired or formally retired); every phase commit that closes a hold-gate; every initiative closure (active → closed).
>
> **Authority.** State truth comes from [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv). This file mirrors `status` + `gated_on` + closure dependencies into a readable form. If they disagree, the CSV is correct; update this file.

---

## 1. Mermaid map

```mermaid
flowchart LR
    %% Closed initiatives (gold-standard reference shape)
    i59[I59 - HLK Governance Clean Slate]:::closed
    i63[I63 - External Repo Governance Codification]:::closed
    i64[I64 - Governance Mission Control]:::closed
    i65[I65 - AKOS Planning Workspace Panel]:::closed
    i66[I66 - Brand Vision Ops Sweep]:::closed
    i67[I67 - RevOps Discovery]:::closed
    i68[I68 - CICD Discipline and Observability Maturity]:::closed
    i70[I70 - Holistika OS Self-Governance Foundation]:::closed
    i71[I71 - CICD Discipline and AIOps Baseline Maturity]:::closed
    i72[I72 - Marketing Area Governance and Persona Registry Expansion]:::closed
    i73[I73 - People Operations + Engagement Models + Methodology IP]:::closed
    i79[I79 - People Manifesto + Pattern Library + AI Governance + Knowledge Hygiene]:::closed
    i80[I80 - I79 Lessons-Learned SOP Body/Addendum + Lenses + Inline-Ratify Skill]:::closed

    %% Active initiatives
    i77[I77 - Impeccable Brand-Bridge Refresh and Drift Gate]:::active

    %% Candidate initiatives (promotable when hold-gates clear)
    i75[I75 - Research Area Governance]:::candidate
    i76[I76 - MADEIRA Elevation]:::candidate
    i81[I81 - KB integrity + Compliance layout + SOP retrofit]:::candidate
    i82[I82 - Holistika Capability Doctrine and Commercial Readiness]:::candidate
    i83[I83 - AI Archivist and KiRBe Ingestor]:::candidate

    %% TRIGGER-watch candidates (dormant by design)
    i74[I74 - Brand-Tooling Productization]:::trigger
    i78[I78 - Brand-Voice LLM-as-Judge]:::trigger

    %% Hard blocks (prior must close before successor starts)
    i59 --> i63
    i63 --> i64
    i64 --> i65
    i65 --> i66
    i66 --> i70
    i67 --> i70
    i68 --> i71
    i70 --> i71
    i70 --> i73
    i70 --> i75
    i70 --> i76
    i71 --> i73
    i71 --> i77
    i72 --> i73
    i72 --> i76
    i73 --> i79
    i79 --> i80
    i80 --> i81
    i80 --> i82
    i82 --> i83

    %% Soft / strand-level cross-links (dotted)
    i71 -.->|review-stamp dimension| i73
    i71 -.->|brand canonicals lib| i77
    i72 -.->|adapter pattern| i76
    i72 -.->|paired SOP rule| i73
    i73 -.->|HR curriculum| i75
    i75 -.->|methodology pillars| i73
    i76 -.->|AIC role_owner| i72
    i79 -.->|design pattern library| i75
    i79 -.->|design pattern library| i77
    i79 -.->|agentic doctrine input| i76
    i80 -.->|inline-ratify skill| i76
    i80 -.->|SOP body/addendum pattern| i75
    i80 -.->|SOP body/addendum pattern| i77
    i80 -.->|KNOWLEDGE_PAIRING_REGISTRY| i82
    i80 -.->|KNOWLEDGE_PAIRING_REGISTRY| i83
    i82 -.->|capability surfacing capability| i76
    i82 -.->|use case archive consumed by KiRBe| i83
    i81 -.->|kb-integrity-matrix feeds Capability registry mint| i82

    %% TRIGGER-watch hold-gates (dashed)
    i74 -.->|TRIGGER-2: >=2 external requests| extReq[External org consumption requests]
    i78 -.->|TRIGGER: >=2 regex pushback signals| extReg[Regex pushback signals]

    classDef closed stroke-width:2px,stroke-dasharray: 0
    classDef active stroke-width:3px,stroke-dasharray: 0
    classDef candidate stroke-width:1px,stroke-dasharray: 4 2
    classDef trigger stroke-width:1px,stroke-dasharray: 8 4
```

**Legend (style encoding only; no explicit fill colours per `PLANNING_COMPENDIUM.md` §10.3).**

- **Solid border, thick stroke** = closed (gold-standard reference shape).
- **Solid border, extra-thick stroke** = active (in flight).
- **Dashed border, short dashes** = candidate (promotable when hold-gates clear).
- **Dashed border, long dashes** = TRIGGER-watch (dormant by design; waits on external signal).
- **Solid arrow** = hard block (prior must close before successor starts).
- **Dotted arrow with label** = soft / strand-level cross-link (dependency exists but doesn't gate the whole initiative).

---

## 2. Per-initiative blocker table

| Initiative | State | Blockers (hard) | Blocked-by | Unblocks | TRIGGER conditions | Current phase |
|:---|:---|:---|:---|:---|:---|:---|
| **I59** — HLK Governance Clean Slate | closed | — | — | I63 | — | closed |
| **I63** — External Repo Governance Codification | closed | I59 closed | I59 | I64 | — | closed |
| **I64** — Governance Mission Control | closed | I63 closed | I63 | I65 | — | closed |
| **I65** — AKOS Planning Workspace Panel | closed | I64 closed | I64 | I66 | — | closed |
| **I66** — Brand Vision Ops Sweep | closed | I65 closed | I65 | I70 | — | closed |
| **I67** — RevOps Discovery | closed | — | — | I70 (RevOps strand input) | — | closed |
| **I68** — CICD Discipline + Observability Maturity | closed | — | — | I71 (CICD baseline + Observability evolution) | — | closed |
| **I70** — Holistika OS Self-Governance Foundation | closed | I66 + I67 closed | I66 + I67 | I71 + I73 + I75 + I76 | — | closed |
| **I71** — CICD Discipline + AIOps Baseline Maturity | closed | I68 + I70 closed | I68 + I70 | I73 (review-stamp dimension) + I77 (brand canonicals lib) | — | closed |
| **I72** — Marketing Area Governance + Persona Registry + IntelligenceOps + RevOps + Process Catalog | closed | — | — | I73 (paired SOP rule) + I76 (adapter pattern) | — | closed |
| **I73** — People Ops + Engagement Models + Methodology IP (mega-initiative) | closed | I70 + I71 + I72 closed (MET) | I70 + I71 + I72 | I75 (HR curriculum cross-link) | — | **CLOSED 2026-05-15** (`INIT-OPENCLAW_AKOS-73`; `D-IH-73-CLOSURE`) — P7–P11 kb-readability + methodology IP + UAT + integration |
| **I74** — Brand-tooling productization | TRIGGER-watch | TRIGGER-2: ≥2 external orgs request AKOS doctrine consumption without source-fork (0 today) | external market signal | (none yet) | TRIGGER-2 = ≥2 external requests | dormant |
| **I75** — Research area governance | candidate | I70 closed (MET); I71 + I72 + I73 P0 (I73 PENDING); Research Director commit (PENDING) | I73 + founder approvals | I76 (cross-strand methodology pillars) | — | candidate |
| **I76** — MADEIRA elevation | candidate | I70 + I72 closed (MET); Strand A external research on AIC F1-F5 completes (PENDING) | external research + operator ratification | (forward-charter linkage to I72 RevOps roles) | — | candidate |
| **I77** — Impeccable Brand-Bridge Refresh + Drift Gate | active | I71 P1 Pack A1 ship (MET — I71 fully closed) | I71 closed | (forward — Impeccable v3.1 chassis stays operational across all initiatives) | — | P0 charter ratified 2026-05-14; P1 Strand A pending |
| **I78** — Brand-voice LLM-as-judge advisory | TRIGGER-watch | TRIGGER: ≥2 regex pushback signals on I71 deterministic gate (0 today) | external regex pushback | (forward — advisory layer to I71's deterministic gate) | TRIGGER = ≥2 pushback signals | dormant |
| **I79** — People Manifesto + Pattern Library + AI Governance + Knowledge Hygiene (mega-initiative) | closed | I73 closed (MET 2026-05-15) | I73 | I75 (design pattern library input) + I77 (design pattern library input) + I76 (agentic doctrine input) + I80 (lessons-learned input) | — | **CLOSED 2026-05-15** (`INIT-OPENCLAW_AKOS-79`; `D-IH-79-CLOSURE`) — P0–P8 mega-initiative six strands + UAT + integration verification; 24/1165 process_list FK seeds; anti-jargon drift gate operational |
| **I80** — I79 Lessons-Learned (SOP Body/Addendum + Stakeholder Lenses + Inline-Ratify Skill) | closed | I79 closed (MET 2026-05-15) | I79 | I81 (full-vault SOP body/addendum retrofit forward-charter) + I76 (inline-ratify skill consumed) + I75/I77 (SOP body/addendum pattern adopted) | — | **CLOSED 2026-05-16** (`INIT-OPENCLAW_AKOS-80`; `D-IH-80-CLOSURE`) — 8 atomic commits P0..P7; 3 tracks delivered: stakeholder lenses paired files + SOP body/addendum pattern (8 paired-file instantiations) + inline-ratify craft skill |
| **I81** — Vault integrity + Compliance layout reorganisation + full-vault SOP retrofit | candidate | Operator charter + **baseline/process approval** gates for CSV path migrations; I80 P6 forward-charter MET | **I80 P7 closed** (`D-IH-80-CLOSURE`) **+ KNOWLEDGE_PAIRING pattern live** (`D-IH-80-H`) | **I82** (consumes integrity matrix + unlocks Confidence in folder layout hygiene) **+ downstream mirror/ERP path consumers** | — | candidate (scope expanded operator 2026-05-16) |
| **I82** — Holistika Capability Doctrine + Commercial Readiness | candidate | Doctrine name + sequencing ratified; **`baseline` Talent row gate** optional defer documented; **recommended:** **I81 P1 integrity CLOSED** before Capability registry merges | **I80 closed** (`D-IH-80-CLOSURE`) · optional **parallel I81 integrity sprint** · **Talent CSV approval queued** | **I83** (Archivist ingestor consumes registries once I82 facets land) **+ Investor/collateral surfaces** | — | candidate (**phase table + Talent gate refreshed 2026-05-16**) |
| **I83** — AI Archivist + KiRBe Ingestor | candidate | I82 P4 closed (use case archive minted); Tech Lab Lead bandwidth | I82 P4 + Tech Lab capacity | (forward — knowledge surfacing system consuming I82 + I80 P6.5 registries) | — | candidate (Tech-area-led product-shaped; 9-12d MVP estimate) |

State truth: row 56 of [`INITIATIVE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) (I70), row 57 (I71), row 58 (I72), row 59 (I77), row 60 (I73 — **closed 2026-05-15**), row 61 (I79 — **closed 2026-05-15**), row 62 (I80 — **closed 2026-05-16**). I74/I75/I76/I78/I81/I82/I83 have no INIT row yet; state is read from candidate files under [`docs/wip/planning/_candidates/`](../_candidates/).

---

## 3. Cross-strand linkages

Some initiatives are loose-coupled to others via specific strands, where the dependency is real but does not block the whole initiative. These are the dotted arrows in §1.

### 3.1 I71 P4 review-stamp dimension → I73 P1 curriculum versioning

I71 P4 (closed 2026-05-14) added a `methodology_version_at_review` column to 4 mirrored canonicals + minted [`validate_review_stamps.py`](../../../../scripts/validate_review_stamps.py) + the [`REVIEW_STAMP_INBOX.md`](../REVIEW_STAMP_INBOX.md) sidecar + reserved an ERP freshness-dashboard panel slot. I73 candidate conundrum C-73-2 (curriculum versioning anchor — methodology-anchor vs own cadence) resolves toward methodology-anchor because the I71 P4 column makes drift detection automatic for methodology-anchored content. See [`docs/wip/planning/71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md`](../71-cicd-discipline-and-aiops-baseline-maturity/master-roadmap.md) §P4 and [`docs/wip/planning/_candidates/i73-people-operations-and-learning-curriculum.md`](../_candidates/i73-people-operations-and-learning-curriculum.md) §4 C-73-2.

### 3.2 I71 P1 Pack A1 brand canonicals → I77 P1 bridge refresh

I71 P1 Pack A1 landed [`BRAND_ENGLISH_PATTERNS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_ENGLISH_PATTERNS.md) + [`BRAND_LLM_TONE_TELLS.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/BRAND_LLM_TONE_TELLS.md) as part of the 10-layer brand-DNA chassis. I77 P1 Strand A bridge refresh cross-references both into the new `BASELINE_REALITY.md` bridge. The dependency is structural (P1 cannot start before I71 P1 lands; MET), not gating (I77 P0 charter ratified 2026-05-14 regardless).

### 3.3 I72 P9 adapter pattern → I76 cross-area handoff

I72 P9 shipped 8 adapter registries (CRM / REVOPS / EMAIL / ATTRIBUTION / BILLING / COMMUNICATION / SCHEDULING / CONTRACT) under the Normalized Adapter Pattern (per Truto + Unified.to + Apideck industry consensus). I76 MADEIRA elevation will extend the REVOPS_ADAPTER_REGISTRY pattern for cross-area handoff bridges (Finance / Data / Tech / GTM-CRM / People / Legal / Research / MADEIRA). The pattern is the SSOT; I76 consumes it rather than mints a parallel system. See I72 P9 commit `297d6b7` and [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 2.

### 3.4 I72 paired SOP rule → I73 P3 People Ops SOPs

I72 P9 ratified [`.cursor/rules/akos-executable-process-catalog.mdc`](../../../../.cursor/rules/akos-executable-process-catalog.mdc) RULE 1: every executable process needs a paired human-readable SOP AND an agent-facing executable runbook AND both `acceptance_criteria_human` + `acceptance_criteria_automation` declared per catalog entry. I73 P3 People Operations SOPs (hiring + onboarding + payroll + offboarding) inherit this rule — each SOP carries a paired runbook (likely `scripts/<purpose>.py` or YAML in a sibling catalog).

### 3.5 I73 HR curriculum ↔ I75 Research methodology pillars

I73 P1 authors the Holistik Researcher onboarding curriculum (per-discipline reading list + per-pillar exercises). The pillar list is defined by I75 (Research area governance). The two initiatives co-evolve: I73 P1 lands a stub curriculum with placeholder pillars; I75 P2 (when it ships) fills the pillar definitions and triggers a curriculum revision. This is bidirectional loose-coupling, not a block.

### 3.6 I76 AIC role_owner → I72 D-IH-72-S binary AC axis

I76 candidate conundrum C-76-1 (AIC SOP-consumption posture) builds on I72's `D-IH-72-S` (Round 6): the binary AC axis classifies AIC SOP consumption on the AC-HUMAN side (humans + AIC are SOP-readers) while AC-AUTOMATION covers unattended runbook firing. I76 may extend this axis or split it; the conundrum is the architectural fork.

---

## 4. Hold-gate quick-check at a glance

For the agent: when promoting any candidate to active, confirm these gates via the per-initiative checklist below.

### I73 promotion gates (ALL MET 2026-05-15; promoted to active)

- [x] I70 closing UAT — MET 2026-05-13.
- [x] I71 P0 charter — MET (I71 fully closed 2026-05-14).
- [x] I72 P0 charter — MET (I72 fully closed 2026-05-14).
- [x] First Holistik Researcher hired (or hiring window committed) — **MET via charter-satisfies-gate reframe** per **D-IH-73-B** (bootstrapping reality: operator + Madeira AI O5-1 + ad-hoc collaborators; founder's own paid employment per [`FOUNDER_TRAJECTORY_INTERNAL.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/FOUNDER_TRAJECTORY_INTERNAL.md) §2 funds Holistika bootstrap; designing the 7-class engagement-model taxonomy IS the unblock, not a traditional hire).
- [x] Founder approval to formally onboard People Operations Lead — **MET via charter-satisfies-gate reframe** per **D-IH-73-B** (same rationale; People Operations Lead role minted in [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv) at I70 P8.3 per `PEOPLE_AREA_RESTRUCTURE.md`; engagement-model-registry execution drives the role even before traditional hire).

### I75 promotion gates

- [x] I70 closing UAT — MET 2026-05-13.
- [x] I71 P0 charter — MET.
- [x] I72 P0 charter — MET.
- [ ] I73 P0 charter — **MET** (I73 **closed** 2026-05-15 per `INIT-OPENCLAW_AKOS-73`; see **D-IH-73-CLOSURE**).
- [ ] Research Director commitment — PENDING (operator decision).

### I76 promotion gates

- [x] I70 closing UAT — MET.
- [x] I72 P0 charter — MET.
- [ ] Strand A external research on AIC F1-F5 framings — PENDING.
- [ ] Operator ratification of AIC architecture (C-76-1) — PENDING (planning-time conundrum).

### I74 TRIGGER-watch

- [ ] TRIGGER-2: ≥2 external orgs request AKOS doctrine consumption without source-fork — **NOT FIRED** (0 requests as of 2026-05-15).

### I78 TRIGGER-watch

- [ ] TRIGGER: ≥2 regex pushback signals on I71 deterministic gate — **NOT FIRED** (0 signals as of 2026-05-15; I71 just closed).

---

## 5. Update history

| Date | Change | Author |
|:---|:---|:---|
| 2026-05-15 | Initial authoring. Covers I59..I78 with state truth from `INITIATIVE_REGISTRY.csv` + `_candidates/` files. I71, I72 closed reflected. | PMO |
| 2026-05-15 | I73 promoted from candidate to active (P0 charter shipped 2026-05-15; `INIT-OPENCLAW_AKOS-73` minted). Mega-initiative absorbing 8 strands (Learning + Ethics+Learning + People Ops engagement-lifecycle + Compliance/Ethics boundary + ENGAGEMENT_MODEL_REGISTRY + Historical case-law + KB human-readability + Methodology IP minting) across 11 phases. Hold-gate reframing per **D-IH-73-B** (charter-satisfies-gate; bootstrapping reality). 7 charter-time decisions ratified (D-IH-73-A..G). 10 OPS-73-* rows minted. Mermaid classDef flipped candidate → active; blocker table row updated; §4 hold-gates flipped to MET with footnote on reframe; §5 history extended. | PMO |
| 2026-05-15 | I73 **`INIT-OPENCLAW_AKOS-73` closed** — P11; **`D-IH-73-CLOSURE`** minted; **`INITIATIVE_REGISTRY.csv`** row 60 `status=closed` + `closed_at=2026-05-15`. Mermaid `i73` → `:::closed`. Blocker table + I75 promotion gate **I73 P0** → **MET**. All **`OPS-73-*`** rows closed. Carry-over: **`hlk-erp`** kb-views as sibling PR; **`release-gate.py`** environmental FAIL lanes per triage unchanged. | PMO |
| 2026-05-15 | I79 **`INIT-OPENCLAW_AKOS-79`** P0 charter ratified — Holistika People Manifesto + Knowledge Hygiene + Cross-area Design Patterns + AI Governance (mega-initiative; follow-up to closed I73 doctrinal layer). Mega-initiative absorbing 6 strands (A Manifesto + B Pattern Library + C-People AI Doctrine + Ethics Anchor + C-TechLab Framework Landscape + D Cross-area Breakthrough Propagation + E Orphan Hygiene + F process_list 8th-col FK) across 10 phases (P0..P8 with P3a/P3b split). 14 charter-time decisions ratified (D-IH-79-A..N) per round 1 + round 3 inline-ratify gates. 10 OPS-79-* rows minted. New always-applied Cursor rule [`.cursor/rules/akos-people-discipline-of-disciplines.mdc`](../../../../.cursor/rules/akos-people-discipline-of-disciplines.mdc) ratified at P0 per `D-IH-79-H`. Mermaid `i79` node added (active); `i73 --> i79` hard-block edge added; soft-link arrows `i79 -.-> i75/i77/i76` added; blocker table row added; §5 history extended. Authoritative Cursor plan: `~/.cursor/plans/i79_people_doctrine_4e309f45.plan.md`. Workspace mirror at [`docs/wip/planning/79-people-manifesto-and-pattern-library/`](../79-people-manifesto-and-pattern-library/). | PMO |
| 2026-05-15 | I79 **`INIT-OPENCLAW_AKOS-79` closed** — P8; **`D-IH-79-CLOSURE`** minted; **`INITIATIVE_REGISTRY.csv`** row 61 `status=closed` + `closed_at=2026-05-15` + `closure_decision_id=D-IH-79-CLOSURE`. Mermaid `i79` → `:::closed` (moved from active set to closed set). Blocker table row updated to **CLOSED**. All **`OPS-79-1..OPS-79-10`** rows closed. 18 D-IH-79-* decisions ratified across 7 rounds (charter A-N + runtime O-R + closure). Phase ship SHAs: P0 `f88d600` + P1 `c1c4ab6` + P2 `b91ed97` + P3a `081614b` + P3b `b248057` + P4 `79149f6` + P5 (4-cluster atomic) `55bfaed`/`c0c74d0`/`0501420`/`83ac4f1` + P6 (4-step atomic) `38256cb`/`68dcc3f`/`cb4d7cc`/`9de986a` + P7 `1117b99` + P8 closure (this commit). Process-singularity FK adoption surface seeded: 24/1165 rows; 8 of 12 patterns adopted. Anti-jargon drift gate operational. Forward-charters carried: `pattern_classification_lattice` + `pattern_dual_register_internal_external` + `pattern_inline_ratify_via_askquestion` + `pattern_program_topic_layout` zero-adoption (universal canonicals; per-row seeding judgement-rich; deferred to future tranches per Round 7 closure rationale); SOP-PEOPLE_ORPHAN_FOLDER_AUDIT_001 mint deferred to a future I-NN per `D-IH-79-Q` cadence ratification. | PMO |
| 2026-05-16 | I80 **`INIT-OPENCLAW_AKOS-80`** P0 charter ratified — I79 lessons-learned follow-up: 3-track absorption (Track 1 stakeholder lenses paired files + agent reflection; Track 2 SOP body/addendum pattern mint + retrofit pilot; Track 3 inline-ratify craft skill + Cursor rule extension) across 8 phases (P0..P7). Charter-satisfies-gate inherits from I79 D-IH-79-A (which inherited I73 D-IH-73-B). 7 charter-time decisions ratified (D-IH-80-A..G) per round 1 inline-ratify gates: A mega-charter scope + B SOP body/addendum paired-file default for DAMA-readiness + C stakeholder lenses paired-files (level 4 body + level 5 addendum) + D retrofit Option-B pilot at I80 with Option-C forward-charter to I81 + E inline-ratify craft skill home + F jargon-gate `*.addendum.md` glob exclusion + G pattern_class taxonomy extension `documentation_layering` as 11th class. 7 OPS-80-* rows minted. Mermaid `i80` node added (active); `i79 --> i80` hard-block edge added; `i80 --> i81` forward-charter edge added; soft-link arrows `i80 -.-> i75/i76/i77` added; blocker table row added; I81 candidate row added; §5 history extended. Authoritative plan: in-repo at [`docs/wip/planning/80-i79-lessons-learned/master-roadmap.md`](../80-i79-lessons-learned/master-roadmap.md) (no out-of-repo Cursor plan companion needed for I80 — small-initiative posture). | PMO |
| 2026-05-16 | I80 **`INIT-OPENCLAW_AKOS-80` closed** — P7; **`D-IH-80-CLOSURE`** minted; **`INITIATIVE_REGISTRY.csv`** I80 row `status=closed` + `closed_at=2026-05-16` + `closure_decision_id=D-IH-80-CLOSURE`. Mermaid `i80` → `:::closed` (moved from active set to closed set). Blocker table row updated to **CLOSED 2026-05-16**. All **`OPS-80-1..OPS-80-7`** rows closed. 8 D-IH-80-* decisions total (charter A-G + closure). Phase ship SHAs across P0-P6 (P7 = this commit). 8 paired-file instantiations of `pattern_sop_addendum_split` shipped (P2 stakeholder lenses + P4 2 I79 SOPs + P5 5 I73 lifecycle SOPs). I81 candidate stub minted at P6 per `D-IH-80-D` Option C forward-charter (~40 SOP bodies remaining; non-time-pressured). DAMA-DMBOK 2.0 alignment thread woven through every architectural decision. Inline-ratify craft skill operational at `.cursor/skills/inline-ratify-craft/SKILL.md` (per `D-IH-80-E`). | PMO |
| 2026-05-16 | **I80 P6.5 follow-on** + **I81/I82 candidate stub expansion**. Minted [`KNOWLEDGE_PAIRING_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/KNOWLEDGE_PAIRING_REGISTRY.csv) (16 cols, 10 seed rows; Pydantic SSOT [`akos/hlk_knowledge_pairing_csv.py`](../../../../akos/hlk_knowledge_pairing_csv.py); validator [`scripts/validate_knowledge_pairing_registry.py`](../../../../scripts/validate_knowledge_pairing_registry.py); 11 governance tests; wired into `validate_hlk.py`; `D-IH-80-H` + `OPS-80-8`). Per operator directive 2026-05-16, **expanded I81 scope** from "full-vault SOP retrofit" to **3-strand foundation work**: (1) **P1 KB integrity + DQ baseline run** (matrix CSV + audit narrative + pairing-registry gap list + `compliance_mirror_emit` coverage checklist); (2) **P2 Compliance vault layout reorganisation** per Initiative 22 forward layout (advops/finops/techops/dimensions wave-by-plane migrations with PRECEDENCE + validators + sync-script + ERP-route synchronisation); (3) **P3-P7 retrofit strands** unchanged. **Refreshed I82 phasing**: P0 doctrine charter → **P1 Talent activation** (`baseline_organisation.csv` operator gate) → **P2 `CAPABILITY_REGISTRY` mint** (gated on I81 P1 integrity CLOSED OR `D-IH-82-PREREQ` waiver) → P3 confidence rating → **P4 use case archive** → P5 eloquence translation → P6 ERP/mirrors → P7 UAT/closure. New dotted edge `i81 -.->|integrity matrix prerequisite for Capability registry| i82` added to mermaid. Blocker table I81/I82/I83 rows refreshed (I83 prerequisite shifted I82 P3 → **I82 P4** to match the new use-case-archive phase position). _templates/README per-initiative state table refreshed in lockstep. Regression sweep this turn fixed 4 phase-numbering drifts (I81 cross-refs to I82 P1 → P2; I83 prerequisite refs I82 P3 → P4 in dep map + README) plus 1 cosmetic typo in I82 §2a. | PMO |
