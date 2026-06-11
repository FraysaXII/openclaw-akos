---
title: Holistic agentic capability orchestration — research charter + execution plan
language: en
status: charter-ratified-2026-06-11-v2
intellectual_kind: research_action_charter
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: Research Director + KM Officer
authored: 2026-06-10
last_review: 2026-06-10
linked_decisions:
  - D-IH-94-A
linked_canonicals:
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_ACTION_DISCIPLINE.md
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/RESEARCH_HEAD_DISCIPLINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_AGENTIC_DOCTRINE.md
  - docs/references/hlk/v3.0/Admin/O5-1/Envoy Tech Lab/canonicals/AGENTIC_FRAMEWORK_LANDSCAPE.md
linked_research_sources:
  - docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/research-action-pack.md
  - docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/source-ledger.csv
  - docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/master-synthesis.md
upstream_session_learnings:
  - MainThreadCursor disposed mid-session (operator-reported 2026-06-10 I94 ops session)
  - AskQuestion ratification loss when parent stream terminates before operator answers
register_id: IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001
---

# Holistic agentic capability orchestration — research charter + execution plan

> **Purpose:** Governed research action for **capability-agnostic** agentic orchestration —
> MADEIRA mindset, plug-and-play primitives (UI / API / serverless), state-of-the-art harness
> design, and multi-framework coverage (voice, geospatial, music, infra, granular UX such as
> app-building flows). **Cursor is the immediate AKOS substrate**, not the research scope
> boundary. Applies the **research-to-decision discipline** and **research radar discipline**.

## 1. Why this research exists

Holistika's **agentic OS + AIC taxonomy** research (2026-05-29) established category boundaries
between AKOS, MADEIRA, substrates, and non-AIC workers. Live I94 Operations sweep sessions
surfaced **runtime friction** that taxonomy alone does not resolve:

| Failure mode | Operator signal (2026-06-10) |
|:---|:---|
| Stream disposal | Parent agent stream ends before child work completes |
| AskQuestion loss | Inline-ratify gates posted but answers never bind when parent stream ends |
| Subprocess lifecycle | Executor subagents + background shells lack durable handoff markers |
| Token economics | No governed attribution of thinking-seat vs execution-seat spend |
| DAMA metadata gap | Agent events not yet lineage-tagged for MADEIRA AIC registry rows |
| Capability gaps | Hooks, verification profiles, and seat routing lack orchestration SOP |

## 2. Research question (one sentence)

*What holistic agentic capability orchestration contracts (primitives, harness design, metadata,
and human-in-the-loop durability) must Holistika adopt so multi-framework agent sessions remain
governable, ratifiable, and cost-attributed — without silent loss of operator decisions or
subprocess evidence — regardless of which IDE or substrate executes the work today?*

## 3. Eight prongs (mapped to Holistika areas)

| Prong ID | Holistika area | Primary question | Downstream consumer |
|:---|:---|:---|:---|
| **P1-DATA** | Data | What DAMA metadata fields must agent session events carry (lineage, actor, seat, token class)? | DataOps mirror + `SUBSTRATE_REGISTRY` audit stamps |
| **P2-FINANCE** | Finance | How do we attribute token spend to initiative / phase / seat without finance-policy drift? | FINOPS registered_fact + rev-rec policy hooks |
| **P3-LEGAL** | Legal | What audit-trail bar makes inline-ratify (`AskQuestion`) decisions legally durable? | Adviser engagement + external render discipline |
| **P4-MARKETING** | Marketing | Which operator-facing surfaces (inbox, WIP, statusline) must reflect live agent state? | PMO renders + brand dual-register copy |
| **P5-OPS-PEOPLE** | Operations + People | Subprocess / handoff markers + AIC seat rules + stream-recovery when parent disposes (I94 AskQuestion-loss learnings + agentic-OS pack) | I94 handoffs doc + two-seat routing + `HOLISTIKA_AGENTIC_DOCTRINE` |
| **P6-TECH-SUBSTRATE** | Tech | What substrate facts (MCP, observability, hooks, verification profiles) are authoritative for event plumbing? Cursor documented as **current AKOS substrate**, not scope limit | `AGENTIC_FRAMEWORK_LANDSCAPE` + config surfaces |
| **P7-RESEARCH** | Research | What orchestration doctrine belongs in Research Methodology (capability-agnostic framing)? | Methodology canonical section or specialty forward-charter |
| **P8-MADEIRA** | People (MADEIRA) | How do MADEIRA mindset + plug-and-play primitives compose across voice / geo / music / infra / UX harnesses? | MADEIRA AIC metadata profile + gap matrix |

```mermaid
flowchart LR
  subgraph prongs [8 prongs]
    P1[P1 Data DAMA]
    P2[P2 Finance tokens]
    P3[P3 Legal audit]
    P4[P4 Marketing UX]
    P5[P5 Ops People handoff]
    P6[P6 Tech substrate]
    P7[P7 Research doctrine]
    P8[P8 MADEIRA primitives]
  end
  subgraph govern [Research Action govern]
    Ledger[source-ledger.csv]
    Synth[master-synthesis.md]
    Ratify[inline-ratify AskQuestion]
  end
  subgraph outputs [Deliverables]
    Gap[AKOS capability gap matrix]
    Meta[MADEIRA AIC metadata profile]
    Fwd[forward charters]
  end
  prongs --> Ledger --> Synth --> Ratify --> outputs
```

## 4. Source budget (amended 2026-06-11 — operator scope upgrade v2)

**Total: 1,000 sources** — **350 CORPINT** (internal) + **650 OSINT** (external).

> Operator override: prefer **more than target** over less. Supersedes 120+250 (batch 2) and 240+500 (v1 amendment).
> **R1 delivered 120 CORPINT** (`65fc3b8f`) with no OSINT — **R2 backfills R1 OSINT debt** (context/KM voices).
> **Rule:** every tranche **R2–R12 ingests both CORPINT and OSINT** — we research holistically; vault processes
> that impact or are impacted by agent orchestration are first-class CORPINT rows in *every* relevant tranche.

### 4.0 Dual-source principle (CORPINT + OSINT every tranche)

| Principle | Functional meaning |
|:---|:---|
| **No OSINT-free tranches after R1** | Even “internal substrate” work needs external voices (Obsidian/Excalidraw/LlamaIndex/KM creators, prompt-engineering craft) |
| **No CORPINT-free tranches** | Every OSINT category pairs with **v3.0 vault** rows — SOPs, process_list lines, doctrines that will change or constrain orchestration |
| **Impact / impacted-by tagging** | Each CORP-VAULT row notes `impacts` or `impacted-by` orchestration contract in `notes` |

### Internal budget (350 CORPINT) — vault + repo lattice

| Category code | Functional name | Target | Example v3.0 vault anchors (non-exhaustive) |
|:---|:---|---:|:---|
| **CORP-CANON** | Repo canon (disciplines, crafts, rules) | 55 | `RESEARCH_ACTION_DISCIPLINE`, `akos-inline-ratification.mdc`, two-seat guide |
| **CORP-VAULT-KM** | KM / context / recall doctrine | 40 | `HLK_KM_TOPIC_FACT_SOURCE.md`, `KB_HUMAN_READABILITY_CHARTER.md`, `DERIVED_RECALL_DISCIPLINE.md`, `KM_CHANNEL_VALUE_NARRATIVE.md` |
| **CORP-VAULT-AGENTIC** | Agentic + MADEIRA operations | 40 | `HOLISTIKA_AGENTIC_DOCTRINE.md`, `SOP-PEOPLE_AGENTIC_OPERATIONS_001`, `MADEIRA_AIC_PER_TASK_REGISTRY.csv` |
| **CORP-VAULT-TECH** | Tech / substrate / graph / runtime | 40 | `AGENTIC_FRAMEWORK_LANDSCAPE.md`, `SUBSTRATE_LANDSCAPE_DOCTRINE.md`, `NEO4J_STRATEGY.md`, `SOP-OPENCLAW_RUNTIME_HEALTH_TRIAGE_001` |
| **CORP-VAULT-DATA** | DataOps / contracts / mirror | 30 | `DATAOPS_DISCIPLINE.md`, `DATA_CONTRACT_STANDARD.md`, `DATA_INTEGRATION_PLANE.md` |
| **CORP-VAULT-OPS** | Operations / handoffs / PMO | 35 | `OPERATIONS_CROSS_AREA_HANDOFFS.md`, `OPERATIONS_PROCESS_CATALOG.yaml`, `WORKSPACE_BLUEPRINT_HOLISTIKA.md` |
| **CORP-VAULT-PEOPLE** | UAT / regression / synthesis | 30 | `INTER_WAVE_REGRESSION_DISCIPLINE.md`, `SYNTHESIS_BEFORE_TRANCHE_DISCIPLINE.md`, `HOLISTIKA_QUALITY_FABRIC.md` |
| **CORP-VAULT-UX** | UX / brand surfaces | 25 | `UX_DISCIPLINE.md`, `SOP-BRAND_VOICE_DRIFT_TRIAGE_001` |
| **CORP-VAULT-LEGAL-ETHICS** | Legal access + ethics boundaries | 25 | `access_levels.md`, `ETHICAL_AGENTIC_BOUNDARIES.md`, `source_taxonomy.md` |
| **CORP-VAULT-FIN** | FinOps / rev-rec | 20 | `FINOPS_REVENUE_RECOGNITION_POLICY.md`, FINOPS registers |
| **CORP-VAULT-PROC** | process_list rows (agentic impact) | 25 | `process_list.csv` lines referencing agentic, research, mirror, UAT, MCP, KiRBe |
| **CORP-I94** | I94 session artefacts | 15 | P4–P6 session doctrines, closure UAT |
| **CORP-INCIDENT** | Stream / AskQuestion incidents | 10 | Transcript learnings, executor tranche-closure rule |
| **CORP-LINEAGE** | Initiative + decision lineage | 15 | I80/I90 planning, `DECISION_REGISTER.csv` D-IH-90-* / D-IH-94-* |
| | **Subtotal** | **350** | R1 delivered **120**; R2–R12 deliver **230** |

### External budget (650 OSINT) — perspective + regression lattice

| Category code | Functional name (stakeholder lens) | Target | Primary prongs |
|:---|:---|---:|:---|
| **OSINT-CTX** | **Context / PKM / prompt engineering / NLP** *(operator add)* | 65 | P1, P7 |
| **OSINT-PLAT** | Agent platform docs (substrate-agnostic) | 45 | P6 |
| **OSINT-SYS** | System Owner — infra, performance, reliability | 42 | P6 |
| **OSINT-OBS** | Observability / tracing / session replay | 38 | P1, P6 |
| **OSINT-SEC** | Security / adversarial / SOC buyer | 32 | P3, P6 |
| **OSINT-INTEROP** | Protocol interop — MCP, A2A, ACP *(regression #4)* | 32 | P6 |
| **OSINT-ORCH** | Orchestration + human-in-the-loop gates | 42 | P5, P7 |
| **OSINT-OPS** | Operational impact — ROI, effort saved, process quality | 42 | P5 |
| **OSINT-EVAL** | Agent evaluation / benchmarking / quality bars *(regression #5)* | 38 | P5, P7 |
| **OSINT-DAMA** | DAMA / metadata / event lineage | 28 | P1 |
| **OSINT-FIN** | Token economics / FinOps AI | 32 | P2 |
| **OSINT-REG** | EU AI Act / GDPR / LOPD / ISO / NIST AI RMF | 48 | P3 |
| **OSINT-ETHICS** | AI ethics beyond legal compliance *(regression #6)* | 28 | P3, P5 |
| **OSINT-RPA** | RPA + agency hype vs governed reality | 38 | P5, P8 |
| **OSINT-UX** | Pure UX/UI — agentic surfaces, conversational IA | 42 | P4 |
| **OSINT-INV** | Investor / market narrative | 32 | P2, P7 |
| **OSINT-PO** | Product owner — discovery, PRD, roadmap | 32 | P4, P7 |
| **OSINT-PUB** | Public opinion — audiences, use cases, practitioner voices | 42 | P4, P8 |
| **OSINT-HV** | Harness — voice / multimodal realtime | 14 | P8 |
| **OSINT-HG** | Harness — geospatial / spatial / embodied | 14 | P8 |
| **OSINT-HC** | Harness — creative / music / media | 12 | P8 |
| **OSINT-HI** | Harness — infra / DevOps automation | 14 | P8, P6 |
| **OSINT-HA** | Harness — app-builder / compositional UX | 14 | P4, P8 |
| **OSINT-SKEP** | Skeptic / failure postmortems | 28 | P5, P3 |
| **OSINT-ACA** | Academic / peer-reviewed rigor | 28 | P7 |
| **OSINT-CHG** | Workforce adoption / change management | 22 | P5 |
| | **Subtotal** | **650** | |

> **OSINT-CTX examples (operator-named):** Obsidian / Excalidraw / LLMWiki creators; Zettelkasten / PKM
> practitioners; LlamaIndex / LangChain context patterns; prompt-engineering craft; NLP context-window economics.
>
> **Regression adds (6 beyond your 8 lenses):** SEC, ACA, CHG (prior) + **INTEROP**, **EVAL**, **ETHICS** (vault-anchored).

### 4.1 Stakeholder lens map (operator intent → category codes)

| Your lens | CORPINT vault codes | OSINT codes |
|:---|:---|:---|
| Investor | CORP-VAULT-FIN, CORP-LINEAGE | OSINT-INV, OSINT-FIN |
| System Owner / infra & performance | CORP-VAULT-TECH, CORP-VAULT-DATA | OSINT-SYS, OSINT-PLAT, OSINT-HI, OSINT-INTEROP |
| **Context / KM / prompt craft** | **CORP-VAULT-KM**, CORP-CANON | **OSINT-CTX** |
| Public opinion / audiences | CORP-VAULT-PROC | OSINT-PUB, OSINT-RPA |
| Product owner | CORP-VAULT-OPS | OSINT-PO, OSINT-HA |
| Operational ROI | CORP-VAULT-OPS, CORP-VAULT-PEOPLE | OSINT-OPS, OSINT-ORCH, OSINT-EVAL, OSINT-CHG |
| EU AI Act / GDPR / LOPD / ISO | CORP-VAULT-LEGAL-ETHICS | OSINT-REG, OSINT-SEC |
| RPA / agency competitive | CORP-VAULT-PROC | OSINT-RPA, OSINT-PUB |
| Pure UX/UI | CORP-VAULT-UX | OSINT-UX, OSINT-HA |
| MADEIRA / harness | CORP-VAULT-AGENTIC | OSINT-HV/HG/HC/HI/HA |

## 5. Twelve-tranche ingest plan (R1–R12) — dual CORPINT + OSINT

Each tranche ends with **tranche regression** (§5.1) then **AskQuestion → commit**. No tranche after R1 may show `0` in either column.

| Tranche | Functional name | CORPINT | OSINT | Primary categories | Vault + external pairing |
|:---|:---|---:|---:|:---|:---|
| **R1** | Substrate SSOT phase I | 120 | 0 | CORP-CANON, RUNTIME, REG | **DONE** `65fc3b8f` — OSINT debt → R2 |
| **R2** | Vault process harvest + **context/KM voices** | 50 | 58 | CORP-VAULT-* breadth + **OSINT-CTX** | `HLK_KM_*`, `DERIVED_RECALL` + Obsidian/Excalidraw/LlamaIndex voices; **includes 30 R1-debt OSINT** |
| **R3** | Platform + infra + performance | 18 | 59 | CORP-VAULT-TECH + OSINT-PLAT, SYS, INTEROP | OpenClaw/Neo4j SOPs + platform docs |
| **R4** | Observability + security | 18 | 59 | CORP-VAULT-DATA + OSINT-OBS, SEC | DATAOPS + Langfuse/OTel + red-team |
| **R5** | Orchestration + operational ROI | 18 | 59 | CORP-VAULT-OPS, PEOPLE + OSINT-ORCH, OPS, EVAL | Handoffs + process catalog + ROI patterns |
| **R6** | DAMA + FinOps | 18 | 59 | CORP-VAULT-DATA, FIN + OSINT-DAMA, FIN | Mirror discipline + token economics |
| **R7** | Regulatory + ethics stack | 18 | 59 | CORP-VAULT-LEGAL-ETHICS + OSINT-REG, ETHICS | `access_levels`, `ETHICAL_AGENTIC_BOUNDARIES` + EU AI Act/GDPR/LOPD |
| **R8** | RPA hype + agency competitive | 18 | 59 | CORP-VAULT-PROC + OSINT-RPA, PUB | process_list agentic rows + RPA creator voices |
| **R9** | Pure UX/UI agent surfaces | 18 | 59 | CORP-VAULT-UX + OSINT-UX, HA | `UX_DISCIPLINE` + agentic IA patterns |
| **R10** | Investor + PO + public audience | 18 | 59 | CORP-LINEAGE, FIN + OSINT-INV, PO, PUB | touchpoint-kit + market narrative |
| **R11** | Multi-harness + MADEIRA | 18 | 59 | CORP-VAULT-AGENTIC + OSINT-HV/HG/HC/HI/HA | MADEIRA registry + harness specialists |
| **R12** | Skeptic + academic + workforce + close | 18 | 63 | CORP-INCIDENT + OSINT-SKEP, ACA, CHG | AskQuestion-loss incidents + `master-synthesis.md`, gap matrix, hooks amendments |
| | **Totals** | **350** | **650** | | Cumulative ledger **1,000 rows** |

### 5.1 Per-tranche regression standards

Before each tranche commit, author `tranche-rN-regression.md` checking **all seven**:

| # | Standard | Functional name | Pass criterion |
|---:|:---|:---|:---|
| 1 | **Coverage** | Category quota | Assigned §4 categories meet tranche row targets |
| 2 | **Dual-source** | CORPINT + OSINT pairing | Both columns >0 (except R1 legacy); ≥1 vault CORPINT cites impact/impacted-by |
| 3 | **Voice diversity** | Stakeholder mix | ≥3 source levels per tranche OSINT |
| 4 | **Prong binding** | Holistika area map | Every row tagged to ≥1 prong (§3) |
| 5 | **KiRBe schema** | Research Action discipline | `validate_research_action.py` PASS on cumulative ledger |
| 6 | **Skeptic balance** | Hype resistance | ≥10% tranche OSINT rows with explicit CON in `notes` |
| 7 | **Downstream hook** | Consumer traceability | Names deliverable (D3–D8) fed by this tranche |

```powershell
# Per-tranche gate (repeat after R2–R12)
py scripts/validate_research_action.py --source-ledger docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/source-ledger.csv
```

**R1 completed actions:**

1. Bootstrap `source-ledger.csv` with 8 prong header rows + agentic-OS CORPINT seeds.
2. Ingest substrate + orchestration docs into P6 prong (Cursor as AKOS substrate fact, not title scope).
3. Document MainThreadCursor / AskQuestion loss as CORPINT incident row (P5 Ops/People prong).

## 6. INTELLIGENCEOPS_REGISTER row (minted R1 — operator ratified 2026-06-10)

Row in [`INTELLIGENCEOPS_REGISTER.csv`](../../../references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv):

| Field | Value |
|:---|:---|
| `register_id` | `IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001` |
| `target_id` | `TODO[OPERATOR-holistic-agentic-orchestration-2026]` (GOI/POI row at govern) |
| `target_class` | `recommendation` |
| `cadence` | `scheduled` |
| `source_type` | `CORPINT` |
| `reliability` | `B` |
| `output_artifact` | `docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/` |
| `responsible_role` | Lead Researcher |
| `lifecycle_status` | `scaffold` |
| `intro_decision_id` | `D-IH-94-A` |
| `volatility_class` | `fast` |
| `staleness_days` | `30` |
| `staleness_posture` | `block_govern` |
| `next_verify_by` | `2026-07-10` |

## 7. Deliverables index

| # | Artifact | Path | Tranche |
|---:|:---|:---|:---:|
| D1 | This charter + execution plan | `RESEARCH_CHARTER_AND_EXECUTION_PLAN.md` | R0 |
| D2 | Source ledger (1,000-row budget) | `source-ledger.csv` | R1–R12 |
| D2b | Per-tranche regression reports | `tranche-r3-regression.md` … `tranche-r12-regression.md` | R3–R12 |
| D3 | Per-prong synthesis | `prong-p1-data.md` … `prong-p8-madeira.md` | R5–R11 |
| D4 | Master synthesis | `master-synthesis.md` | R12 |
| D5 | AKOS capability gap matrix | `akos-capability-gap-matrix-2026-06-10.md` | R12 |
| D6 | MADEIRA AIC metadata profile | `madeira-aic-event-metadata-profile-2026-06-10.md` | R12 |
| D7 | Research action pack | `research-action-pack.md` | R12 |
| D8 | Forward charters (if deferred) | `forward-charter-*.md` | R12 |

Folder root: `docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/`

## 8. Cross-links

### Agentic-OS prior art (2026-05-29)

- Pack: [`docs/wip/intelligence/agentic-os-and-aic-taxonomy-2026-05-29/research-action-pack.md`](../agentic-os-and-aic-taxonomy-2026-05-29/research-action-pack.md)
- **Inheritance rule:** Narrows taxonomy into **operational orchestration contracts**; does not re-litigate AOS category.

### I94 Operations session learnings (2026-06-10) — P5 Ops/People prong

| Learning | Research prong | Planning artefact |
|:---|:---|:---|
| Stream disposal mid-session | P5 Ops/People + P6 Tech | [`i94-operations-master-sweep-design-2026-06-10.md`](../../planning/94-area-architecture-and-completeness-v2/reports/i94-operations-master-sweep-design-2026-06-10.md) |
| AskQuestion ratification loss | P5 Ops/People + P3 Legal | [`akos-inline-ratification.mdc`](../../../.cursor/rules/akos-inline-ratification.mdc) |
| Two-seat executor packet bound | P5 Ops/People | [`docs/guides/cursor-two-seat-routing.md`](../../../docs/guides/cursor-two-seat-routing.md) |

## 9. Verification matrix

```powershell
py scripts/validate_research_action.py --self-test
py scripts/validate_research_radar.py --self-test
py scripts/validate_intelligenceops_register.py
py scripts/validate_hlk.py
```

## 10. Operator ratification log

### Batch 2 (2026-06-10)

| Gate | Decision |
|:---|:---|
| Source budget (original) | 120 internal + 250 external — approved |
| INTELLIGENCEOPS row | Mint `IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001` at R1 |
| Implementation scope | R12 includes hooks.json + two-seat guide amendments (Q3-B) |

### Batch 3 (2026-06-11 — pending commit v2)

| Gate | Decision |
|:---|:---|
| Source budget (upgrade v2) | **350 CORPINT + 650 OSINT** (1,000 total); prefer over-target — pending |
| Dual-source rule | Every R2–R12 tranche ingests **both** vault CORPINT + OSINT — pending |
| OSINT-CTX category | Context / PKM / prompt engineering / NLP (Obsidian, Excalidraw, LlamaIndex voices) — pending |
| Regression adds | SEC, ACA, CHG, INTEROP, EVAL, ETHICS — pending |
| Tranche shape | **12 tranches** with §5.1 seven-point regression — pending |
| Next execution | **R2** vault harvest + OSINT-CTX (+50 CORPINT, +58 OSINT incl. R1 debt) — pending |

---

*R1 complete (`65fc3b8f`) — 120/350 CORPINT, 0/650 OSINT. Charter v2+bump amended 2026-06-11; awaiting operator ratify + commit.*
