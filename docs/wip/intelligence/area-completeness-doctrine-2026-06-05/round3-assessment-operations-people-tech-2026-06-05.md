---
intellectual_kind: research_assessment
parent_initiative: INIT-OPENCLAW_AKOS-93
related_initiatives: [88, 86, 79, 02]
authored: 2026-06-05
status: active
language: en
named_decision: D-AREA-DEF (round 3 — Operations / People-methodology / Tech-Envoy / subfolder-role)
source_ledger: source-ledger.csv (131 sources)
control_confidence_level: Keter
---

# Round-3 assessment — my answers to the four hard questions

> The operator asked me to *research and come back with my own assessment + AskQuestion again*
> on Operations (O-1), People-methodology (O-2), Envoy/Tech (O-4), and the sub-folder=role
> drift (O-3). This is that assessment. Grounded in the role roster
> ([`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv)),
> PMBOK/ITIL/APQC (`SRC-AREA-EXT-63..76`), and the org doctrine. **Still gated — nothing minted/moved until you pick.**

## A. The roster reveals the *real* model (and two things the scorer gets wrong)

Reading `baseline_organisation.csv` end-to-end changed my picture. The org is **area × entity**, not just area:

| Layer | What the roster actually says |
|:---|:---|
| **Areas (by C-level)** | People (CPO), Finance (CFO), Operations (COO), Marketing (CMO), Data (CDO), Tech (CTO), Research (Holistik Researcher) — **+ Legal** (Legal Counsel, reports to CPO, carries its own `area=Legal`) |
| **Entities** | **Holistika** (parent/governance), **Think Big** (business/ops/marketing/finance), **HLK Tech Lab** (Tech + half of Data — the engineering entity) |
| **Sub-areas** | the `sub_area` column: Compliance, Organisation, Ethics, Learning, People Operations, Talent-H, Talent-A (People); SMO, RevOps (Operations); Brand & Narrative, Reach, Resonance, Experimentation (Marketing); Legal |

**Two scorer bugs this exposes:**
- **BUG-1 — Legal is invisible.** `VALID_SCORED_AREAS` in `hlk_area_completeness.py` scores **7** areas and omits **Legal**, which is a first-class `area` in the roster. Legal is governed nowhere in the matrix.
- **BUG-2 — the entity axis is unmodeled.** The matrix treats `Tech/` and `Envoy Tech Lab/` as folder noise, but the roster says **HLK Tech Lab is an entity** — Tech Lead, DevOPS, Front/Back-End, Domain Specialist, AI Engineer, Database Owner all carry `entity=HLK Tech Lab`. Envoy Tech Lab is **the HLK Tech Lab entity's home**, not a stray folder. This is your "closed-off tech brand, contracts flow from Think Big" — and it's already in the data.

## B. Operations (O-1) — my assessment

**What the research says.** PMBOK 7/8 (`SRC-AREA-EXT-71/72/73`) frame project work as **principles + performance domains** (Governance, Scope, Schedule, Finance, Stakeholders, Resources, Risk) — outcome-focused, tailorable, *not* a rigid process list (exactly your "a place to understand where you are and where to go, without overengineering"). ITIL 4 (`SRC-AREA-EXT-74/76`) puts project + service management inside one **Service Value System** feeding **value streams**. The bright line (`SRC-AREA-EXT-75`): **projects end; operations continue.**

**Your definition is the correct one.** "Remove Ops and you keep all the know-how but lose the capacity to *move*." That is the textbook definition of operations as the **delivery/execution layer** — the verb that converts know-how into tangible motion. Operations is **definitionally cross-cutting**; that is *why* it feels blurry — it is not a sibling function to Finance/Marketing, it is the **delivery spine** that runs *across* them.

**My recommendation (challenges the current shape):** stop trying to make Operations a peer "topic" area. Re-frame it as the **delivery/execution capacity area**, organized by **PMBOK performance domains** (the operator's native lens), with sub-areas = **delivery modes**:

| Operations sub-area | Delivery mode | APQC / framework anchor |
|:---|:---|:---|
| **PMO** | project delivery (temporary) | PMBOK; "projects end" |
| **SMO** | service delivery (ongoing/BAU) | ITIL 4 SVS; "operations continue" |
| **RevOps** | revenue delivery | BizOps→RevOps (`EXT-67`) |
| **Engagement** | client/engagement delivery | RevOps + delivery |
| **IntelligenceOps** | **MOVE OUT** → it's research-application, not delivery (your "misleading with Research") |

The unifying doctrine: **one Operations area, PMBOK-domains as the maturity dimensions, project-vs-service as a tag not a split** (you said it: "I don't care if it's project or service, I run it all that way"). This *keeps* Operations as one area but gives it a **non-blurry internal spine** (the 7 PMBOK domains) and evicts the one genuinely misplaced sub-area (IntelligenceOps).

## C. People-methodology (O-2) — my assessment (you were right about Compliance)

The roster settles your question. Three roles each own a *different verb* on "methodology":

| Role | `role_description` (verbatim) | The verb |
|:---|:---|:---|
| **Research** (Holistik Researcher) | governs "the four Holistika methodology pillars (Process Engineering, Business Engineering, Factor Combination, Foresight)" | **authors** the methodology (R&D) |
| **Compliance** (People) | "Policy and Methodology **Enforcement** … the methodology is the product" | **enforces** the methodology in BAU |
| **People** (manifesto / discipline-of-disciplines) | "mints the patterns; other areas author their own processes" | **mints** the cross-area patterns |

**So "methodology" is not one thing in one place — it is a three-stage pipeline:** Research *invents* it → People *patternizes* it → Compliance *enforces* it. That is coherent, not drift.

**Where the cross-area quality disciplines belong** (UAT, inter-wave/intent-ranked/index/synthesis regressions, PWF, area-governance, Quality Fabric): these are **enforcement + pattern** artifacts, so their home is **People/Compliance** (the methodology-enforcement sub-area) — **not** a new "People/Methodology" sub-area (you were right to question my §5.1 proposal). Today they sit *flat* in `People/canonicals/` while the registries they govern sit correctly in `People/Compliance/canonicals/`. **The fix is to consolidate the disciplines under Compliance**, where the roster already says methodology-enforcement lives.

**Revised recommendation (replacing my earlier "People/Methodology"):** do **not** invent a new sub-area. **Compliance is the methodology sub-area** — move the flat `People/canonicals/*DISCIPLINE*` + Quality Fabric there (or formally designate `People/canonicals/` as the manifesto-tier and `People/Compliance/` as the methodology-tier). And the area-operational disciplines still drift out (MKTOPS→Marketing, TECHOPS→Tech, DATAOPS→Data, UX→Marketing) because those are *area BAU*, not cross-area methodology.

## D. Tech / Envoy Tech Lab (O-4) — my assessment

**What happened (from the roster + your context + I02 lineage):** you created **HLK Tech Lab as a distinct entity** — a closed-off engineering brand so the business (Think Big) could say "we've got tech to spare," with all contracts flowing from Think Big/Holistika. At the time, **there was no Tech area and no Data area** — so "Envoy Tech Lab" became the catch-all home for *all* engineering + the KB-as-lab. Since then Tech (CTO) and Data (CDO) areas were minted, but the **folder tree never caught up** — so Envoy Tech Lab now overlaps the Tech area it should sit *inside* (your "tech which should govern Envoy Tech Lab — it's in the name").

**My assessment:** this is an **entity-vs-area** confusion, not an area-boundary error. The clean model:
- **Tech (area, CTO)** governs the *discipline* — it is the platform area.
- **HLK Tech Lab (entity)** is *where the engagement-intensive engineering executes* — a Team-Topologies **platform + complicated-subsystem** entity (`SRC-AREA-EXT-32`) that the Tech area governs.
- **`Envoy Tech Lab/` folder** should become the **HLK Tech Lab entity's tree _under_ Tech's governance**, made **matrix-visible** as part of Tech (BUG-2 fix), not a separate unscored island.
- **IntelligenceOps / RevOps / SMO / Engagement** confusion is the *same disease in Operations* — entities/sub-areas that were minted before the area model matured. Same cure: map each to its area + entity explicitly.

**Recommendation:** keep HLK Tech Lab as an entity (it's strategically real and the brand is clear), fold the `Envoy Tech Lab/` **folder** under Tech-area governance + make it matrix-visible, and add an **entity axis** to the area model so "which entity executes this" is a governed field (it already is, in `baseline_organisation.entity` — the scorer just ignores it).

## E. Sub-folder = role (O-3) — the drift map + the standard

Your doctrine — **area sub-folder = role name** (so RACI is intuitive and drift is obvious) — is **sound and matches the roster's `sub_area` column**. But the tree does **not** currently obey it:

| Area | Roster sub-areas/roles | Folder reality | Verdict |
|:---|:---|:---|:---|
| People | Compliance, Organisation, Ethics, Learning, People Operations, Legal | `People/Compliance`, `Ethics`, `Learning`, `People Operations`, `Legal` exist; **Organisation missing**; disciplines sit flat at root | partial |
| Operations | PMO, SMO, RevOps + (Engagement, IntelligenceOps) | `PMO`, `RevOps`, `SMO`, `Engagement`, `IntelligenceOps` folders exist | mostly OK but IntelligenceOps misplaced |
| Finance | Business Controller, Financial Controller, Pricing, Taxes, Front Office, O2C, PTP | `Governance/`, `Business Controller/` — **role-named subfolders mostly absent** | drift |
| Marketing | Brand & Narrative, Reach, Resonance, Experimentation | `Brand/`, `Reach/`, `Resonance/` — **"Brand & Narrative" vs folder "Brand"; Experimentation missing** | drift |
| Data | Architecture, Governance, (Data Science, Data Eng) | `Architecture/`, `Governance/` — role-named subfolders partial | partial |
| Tech | DevOPS, System Owner, AI Engineer, Tech Lead, … | `DevOPS/`, `System Owner/` + Envoy split | drift (entity confusion) |
| Research | Methodology + (Lead/Analyst roles) | `Methodology/` only | thin |

**This is the missing AREA-16 (file-plan) component made concrete: sub-folder names must FK to `baseline_organisation.role_name` / `sub_area`.** That is mechanically checkable — a validator can assert every area sub-folder maps to a role/sub-area and flag orphans (drift). It makes "where is what" deterministic and RACI intuitive, exactly as you said.

## F. What this changes in the model (vs the §4 brainstorm)

- **AREA-14 KIND** stays, **+ add ENTITY** (Holistika / Think Big / HLK Tech Lab) as a governed field (fixes BUG-2).
- **AREA-15 placement-integrity** now also checks **sub-folder = role/sub-area FK** (the O-3 doctrine).
- **Legal becomes the 8th scored area** (fixes BUG-1) — or an explicit, ratified People sub-area, but *scored either way*.
- **Operations** = delivery-capacity area scored on **PMBOK performance domains**; IntelligenceOps evicted.
- **People methodology** home = **Compliance** (not a new sub-area); area-ops disciplines drift out.

## G. Open questions for round-3 ratification

- **Q-OPS:** adopt "Operations = delivery-capacity area, scored on PMBOK 7 domains, project/service as a tag" + move IntelligenceOps out?
- **Q-PEOPLE:** consolidate the cross-area disciplines under **People/Compliance** (methodology-enforcement) rather than a new sub-area?
- **Q-ENTITY:** add an **entity axis** (Holistika/Think Big/HLK Tech Lab) + fold `Envoy Tech Lab/` under Tech governance + make it matrix-visible?
- **Q-LEGAL:** promote **Legal to the 8th scored area** (it's a first-class `area` in the roster)?
- **Q-SUBFOLDER:** ratify **sub-folder = role/sub-area FK** as AREA-16 (validator-enforced)?

## H. Cross-references

- [`area-architecture-redesign-2026-06-05.md`](area-architecture-redesign-2026-06-05.md) (round-2 brainstorm this revises)
- [`master-synthesis.md`](master-synthesis.md) · [`baseline-state-2026-06-05.md`](baseline-state-2026-06-05.md)
- Roster: [`baseline_organisation.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/baseline_organisation.csv)
- Ops doctrine: [`HOLISTIK_OPS_DISCOVERY.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/HOLISTIK_OPS_DISCOVERY.md) · [`OPERATIONAL_COHESION_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md)
- Ledger: [`source-ledger.csv`](source-ledger.csv) (131 sources; validator PASS)
