---
intellectual_kind: evidence_sweep_report
sharing_label: internal_only
parent_initiative: INIT-OPENCLAW_AKOS-86
sweep_topic: operator visibility concern (scratchpad L66)
authored: 2026-05-19
last_review: 2026-05-19
linked_decisions:
  - D-IH-86-U   # hybrid-by-wave + scratchpad drain protocol
status: active
language: en
role_owner: System Owner
co_owner_role: PMO
audience: J-OP
access_level: 3
purpose: evidence base for inline-ratify gate on operator's visibility/rework concern; no canonical decisions land in this report
---

# Lane VISIBILITY-SWEEP — evidence report

## §1 — Operator concern (verbatim) + four-axis parse

### Verbatim (scratchpad L66)

> "I'm getting lost on visibility. I know we're doing an excelent job but I don't know where how what it gives, etc. We worked on visibility for the - HUMAN OPERATOR and anyone we can have interested on this and we decide too work on the ERP-HLK. I don't remember where we are but it would be nice to visit OPS side. This is not only for AKOS visibility, but also for HLK visibility, operational cohesion and tracking. I know this seems vague but we have tons on docs and work on the ERP and the audiences and expeccted UX, amongst other related applicable disciplines. We may require a rework."

Source: [`docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md`](../operator-scratchpad.md) (line 66; processed marker not yet applied per lane charter).

### Parse — four axes (not one problem)

| Axis | Operator phrase | What they are really asking |
|:---|:---|:---|
| **1 — AKOS internal** | "where how what it gives" | Day-to-day: **which artifact tells me initiative/wave/OPS status?** How many clicks from "open repo" to "what do I do next?" |
| **2 — HLK external** | "HLK visibility" + "audiences and expected UX" | **Which J-* audiences have real shipped surfaces** (PDF/web/ERP) vs markdown-only vault? |
| **3 — HLK-ERP status** | "decide to work on the ERP-HLK" + "don't remember where we are" | **What landed in `hlk-erp` vs what is still charter/spec?** Is ERP the operator home or a parallel experiment? |
| **4 — Operational cohesion** | "operational cohesion and tracking" + "may require a rework" | **One narrative** tying AKOS planning, ERP panels, boilerplate/web, registers, and render pipelines — or explicit admission they are fragmented |

**Cross-cutting diagnosis:** Excellent **governance SSOT** (registers, validators, wave discipline) without a **cognitive map** that answers "if I have 15 minutes, where do I look?" The operator is not asking for more docs; they are asking for **legible routing** between existing docs and systems.

---

## §2 — Axis 1: AKOS internal visibility

### 2.1 Is there a single pane of glass?

**No.** There is a **deliberate multi-surface design** (I59 governance clean-slate) but no unified index that links them.

| Surface | Path | Render script | Primary audience | Status | "What it gives" |
|:---|:---|:---|:---|:---|:---|
| **WIP Dashboard** | `docs/wip/planning/WIP_DASHBOARD.md` | `scripts/render_wip_dashboard.py` | PMO / operator | **Live** (auto; 15 active shown 2026-05-19) | Initiative **status taxonomy** across ~70 folders |
| **Operator Action Inbox** | `docs/wip/planning/OPERATOR_INBOX.md` | `scripts/render_operator_inbox.py` | Operator | **Live** (29 open rows) | **RICE-ranked OPS tasks** needing operator/mixed action |
| **Review-stamp inbox** | `docs/wip/planning/REVIEW_STAMP_INBOX.md` | `scripts/validate_review_stamps.py` | PMO / governance | **Live** (sidecar to inbox) | Stale/missing **review stamps** on mirrored governance CSVs |
| **I86 cluster burndown** | `docs/wip/planning/86-initiative-cluster-execution-coordinator/cluster-burndown-plan.md` + `cluster-burndown-inventory.md` | (manual + inventory) | Operator / PMO | **Live** (2026-05-19) | **Current wave lens**: 5 active siblings + 3 blocker-trackers + 9 OPS rows |
| **I86 master-roadmap** | `docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md` | — | PMO | **Live** | Ten-sibling checklist + wave spotlight roster |
| **Per-initiative roadmaps** | `docs/wip/planning/<NN>-*/master-roadmap.md` (70 folders) | — | Role owners | **Mixed freshness** | Phase detail, decisions, verification |
| **Planning README index** | `docs/wip/planning/README.md` | — | Operator | **Live** | Initiative index with one-line blurbs |
| **OpenClaw control dashboard** | `http://127.0.0.1:18789` (local) | — | Operator + Madeira | **Runtime** (separate product) | Agent health, WebChat — **not** initiative portfolio |
| **UAT dossier render** | `artifacts/uat-dossier/` via `scripts/render_uat_dossier.py` | `render_uat_dossier.py` | Operator / UAT | **On demand** | Packaged verification evidence |
| **PMO hub autogen** | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md` | `scripts/render_pmo_hub.py` | PMO / delivery | **Partial** | Stakeholder index slice only |
| **Topic graph** | (output varies) | `scripts/render_topic_graph.py` | KM / Tech | **Specialized** | Topic-Fact-Source graph |
| **KM diagrams** | `_assets/**/<topic>/*.png` | `scripts/render_km_diagrams.py` | KM | **Batch** | Diagram assets |
| **Impeccable UAT HTML** | `docs/presentations/*/index.html` | `scripts/render_impeccable_uat.py` | Brand / UAT | **Episodic** | Branded UAT HTML |
| **Unified operator dashboard dir** | `docs/wip/planning/dashboards/` | — | — | **Does not exist** | Option A in §6 proposes creating it |

`RENDERING_PIPELINE_REGISTRY.csv` explicitly registers `wip_dashboard_render` and `operator_inbox_render` as separate pipelines (rows 9–10); there is **no** `unified_operator_dashboard` pipeline row.

### 2.2 How does the operator find "where am I in I76 / Wave H / next move?"

**Today: multi-hop (roughly 5–10 intentional navigations), not 1 click.**

| Question | Fastest path today | Clicks / friction |
|:---|:---|:---:|
| **Wave H status** | `cluster-burndown-plan.md` §6 + scratchpad drain notes | Open I86 folder → burndown doc |
| **I76 phase** | `docs/wip/planning/76-madeira-elevation/master-roadmap.md` + `INITIATIVE_REGISTRY.csv` | Folder + optional CSV |
| **What needs me now** | `OPERATOR_INBOX.md` (top RICE rows) | One file; **but** 20+ seed rows lack RICE (`—`) |
| **All active initiatives** | `WIP_DASHBOARD.md` § Active | One file |
| **Cluster remaining work** | `cluster-burndown-inventory.md` table §2 | One file; **does not** deep-link ERP |

**USER_GUIDE** (`docs/USER_GUIDE.md` ~L2269) states OPERATOR_INBOX is the operator's **primary triage view** for `gated_operator` initiatives — that is **OPS-centric**, not **wave-centric** or **ERP-centric**.

### 2.3 Stale vs fresh (AKOS planning surfaces)

| Artifact | `last_review` / evidence | Freshness judgment |
|:---|:---|:---|
| `WIP_DASHBOARD.md` | Auto-rendered on initiative changes | **Fresh** when render run after commits |
| `OPERATOR_INBOX.md` | 29 rows; mixed RICE | **Content drift**: many seeded OPS rows need triage |
| `I86 cluster-burndown-*` | 2026-05-19 | **Fresh** for cluster lens |
| `01-akos-full-roadmap` | 2026-04-15 | **Stale** as "program view" vs current I86 cluster |
| Per-initiative roadmaps | `last_review` varies in frontmatter | Use `WIP_DASHBOARD` as aggregate |

### 2.4 Render-script fragmentation

**Ten** `scripts/render_*.py` scripts; **no orchestrator** that runs all and emits one landing `index.md` / HTML.

Registered in [`docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv`](../../../references/hlk/v3.0/Envoy%20Tech%20Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv):

- `operator_inbox_render`, `wip_dashboard_render` — operator daily-touch
- `pmo_hub_render`, `km_diagrams_batch_render`, `topic_graph_render` — domain-specific
- `uat_dossier_render`, `generic_dossier_render`, `impeccable_uat_visual_render` — evidence packs
- `company_dossier_*`, `branded_dossier_pdf_render`, `suez_*` — external delivery

**Drift finding:** `render_wip_dashboard.py` docstring still says it reads registries (I59 P2 narrative); implementation reads **master-roadmap frontmatter** — functionally correct but **mental model** in registry text lags.

### 2.5 Axis 1 coverage map

| Need | Covered today? | Gap |
|:---|:---:|:---|
| Initiative portfolio status | Yes (`WIP_DASHBOARD`) | No wave overlay |
| Operator task queue | Yes (`OPERATOR_INBOX`) | Noisy seeds; not ERP-linked |
| Cluster/wave progress | Yes (I86 burndown only) | Not linked from inbox/dashboard |
| Canonical freshness | Partial (`REVIEW_STAMP_INBOX`) | Area canonicals use separate Lane E validator |
| Runtime/agent health | Yes (OpenClaw dashboard) | Disconnected from planning SSOT |
| **One landing page** | **No** | **Primary gap** |

---

## §3 — Axis 2: HLK external visibility

### 3.1 Audience registry baseline

Source: [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv) (I85 closure).

| Code | Status | Promised surfaces (registry `typical_surfaces`) | Shipped vs placeholder |
|:---|:---|:---|:---|
| **J-IN** | active | ENISA company dossier decks + advops dossiers | **Partial** — deck HTML/PDF pipeline exists (`build_company_deck`, `export_company_deck_pdf`); investor-specific surfaces vary by engagement |
| **J-CU** | active | touchpoint-kit + advops proposals | **Partial** — touchpoint-kit markdown; many sends still manual per rendering registry `planned` rows |
| **J-PT** | active | touchpoint-kit + partner docs | **Partial** |
| **J-ENISA** | active | enisa_* dossiers | **Partial** — PDF discipline strong post Wave F; historical BBR leaks triaged under OPS-86-5 |
| **J-AD** | active | adviser handoffs | **Partial** — hybrid register; ERP adviser rollup **not built** (I89) |
| **J-RC** | **inactive** | recruiter presentations | **Placeholder** — "flips when first hire pipeline" |
| **J-CO** | **planned** | touchpoint-kit + README | **Placeholder** — post-I74 |
| **J-OP** | active | vault + `docs/wip/planning/**` | **Live** (markdown SSOT) |

### 3.2 External-render trail (mechanical)

Per [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/uat-render-quality-2026-05-19.md`](uat-render-quality-2026-05-19.md):

- `validate_external_render_trail.py --strict --strict-freshness` → **PASS**
- **6** external-tagged surfaces with paired render artifacts; **0** pending tracker rows (Wave F closure)

**Important limitation:** This gate proves **render parity for tagged external markdown**, not that **every audience has a browsable product surface**. Most vault prose remains **authoring SSOT**, not delivery.

### 3.3 Boilerplate vs hlk-erp vs AKOS exports

| Surface | Role per governance | Live for externals? |
|:---|:---|:---|
| **boilerplate** (`holistikaresearch.com`) | **Reference-only** web (D-IH-32-N); brand/i18n | **Yes** for public marketing DOM — **not** operator portfolio |
| **hlk-erp public/advops routes** | Adviser-external rollup (I89) | **Not shipped** — charter only |
| **AKOS `docs/presentations/**/index.html`** | Broadcast/slide surfaces | **At least 2** HTML decks (company dossier, impeccable UAT) |
| **`artifacts/exports/*.pdf`** | PDF delivery | Repo search found **no** committed PDFs under `artifacts/exports/` at sweep time — PDFs may be gitignored or generated locally |

**Drift (promised UX vs shipped UX):** I29/I28 invested in **investor-grade deck + PDF**; I85 wired **audience tags**; Wave F wired **render discipline**. There is **no single external "status page"** for "what Holistika shows each audience" — only scattered assets + validators.

### 3.4 Initiatives that named audience / UX visibility

| Initiative | Visibility / UX promise | Delivery state |
|:---|:---|:---|
| **I85** | Audience-tag canonicalization + drift gate | **Closed** 2026-05-19 — registry + frontmatter |
| **I66** | BBR dual register + external prose | **Closed** — matrix + drift gate FAIL |
| **I77** | Impeccable bridges + UAT surfaces | **Closed** — bridge refresh |
| **I70** | `HLK_ERP_ARCHITECTURE` operator-facing ERP vision | **Doctrine shipped**; panels mostly reserved |
| **I65** | AKOS planning visible in ERP | **Active** — **not implemented** in sibling repo |
| **I89** | Six persona rollup panels | **Active P0**; P1–P5 **pending** |
| **I82** | Capability doctrine + audience-aware surfacing | **Active P0** — forward |

### 3.5 BBR / brand findings

- `validate_brand_baseline_reality_drift.py` at **FAIL** (D-IH-89-E) — blocks internal-register leakage to external bodies.
- Operator metadata exemption for J-OP does **not** reduce "where is the external site?" confusion.

---

## §4 — Axis 3: HLK-ERP work status

### 4.1 Sibling repo + registry

| Source | Fact |
|:---|:---|
| `REPOSITORY_REGISTRY.csv` / `REPOSITORIES_REGISTRY.md` | `hlk-erp` — platform, System Owner, GitHub `FraysaXII/hlk-erp` |
| `HLK_ERP_ARCHITECTURE.md` frontmatter | `sibling_repo: C:\Users\Shadow\cd_shadow\root_cd\hlk-erp` |
| I32 P7 | Registered ERP; noted **13 local cursor rules without AKOS SSOT cross-ref** (E12) |

### 4.2 Initiatives touching hlk-erp

| INIT | Status (registry) | ERP promise | Shipped? |
|:---|:---|:---|:---|
| **I62** Mission Control | **active** | 12-phase transform; Mission Control Today; kill mocks | **Partial** — AKOS-side SQL migrations + UAT report 2026-05-06; UAT frontmatter `status: closed` **conflicts** with INIT row still **active**; shape docs say dashboard still on **mock `lib/data.ts`** |
| **I63** External repo governance | active | Bless/drift automation | **AKOS scripts**; ERP integration via I64 |
| **I64** Governance Mission Control | active | `/operator/governance/external-repos/` 6-panel | **Spec v2** promoted; implementation **pending** in sibling |
| **I65** Planning workspace panel | active | `/operator/planning/` — "see what we do in docs/wip/planning" | **Charter 2026-05-07**; **not shipped** — directly addresses operator visibility into planning |
| **I70** Holistika OS self-governance | closed | Minted `HLK_ERP_ARCHITECTURE.md` | **Canonical only** |
| **I86 P3** | I86 anchor work closed | `governance.initiative_program_rollup_view` + persona spec | **Data layer in Supabase** — **no TSX** |
| **I89** ERP program rollup | active; **P0 in_progress** | Six `program-rollup` routes + REDACTED adviser | **Not shipped** — P1–P5 pending; master-roadmap todos show P0 charter in_progress |

**No** dedicated `I-NN-visibility-audit` or `I-NN-ERP-rework` in `_candidates/` grep (visibility only on i78 "score dashboard" forward-charter mention).

### 4.3 `HLK_ERP_ARCHITECTURE.md` panel inventory (reality check)

§4 table (authored 2026-05-13, updated for I86/I89 forward-charter):

- **~30+ panel routes** listed.
- **Vast majority:** `reserved (P10.5)` or `partially exists`.
- **Program rollup six routes:** explicitly **reserved** → implementation **forward-chartered to I89**.
- **Partially exists:** e.g. I65 initiatives/decisions routes "partial"; InfraMonitor (I62); planning index **not** done.

**Operator-intended single pane?** Doctrine says yes — §1: *"HLK-ERP is the operator-facing surface of the Holistika OS."* Implementation says **not yet** — I62 shape doc (2026-05-06) still describes **greenfield Mission Control** on mocked data.

### 4.4 Parallel system or intended home?

| Model | Evidence |
|:---|:---|
| **Intended long-term home** | `HLK_ERP_ARCHITECTURE.md` + I62 charter + I65 user quote |
| **Parallel AKOS markdown ops** | I59 deliberately minted `WIP_DASHBOARD` + `OPERATOR_INBOX` in **AKOS repo** because ERP was not ready |
| **I62 impeccable-shape-operator-inbox** | Explicitly designs **ERP inbox** with snooze/drawer **alongside** AKOS `OPERATOR_INBOX.md` — **two surfaces, same SSOT**, different affordances |

**Cohesion gap:** SSOT is unified (CSVs); **operator UX is bifurcated** (markdown in AKOS vs Next.js in hlk-erp) without a **routing doctrine** telling the operator which to open when.

### 4.5 Promised vs shipped (ERP-specific)

| Promised (I62/I65/I89) | Shipped evidence in AKOS repo |
|:---|:---|
| Mission Control 7 tiles | SQL views proposed/applied per migration reports; **ERP UI** not verifiable from AKOS-only sweep |
| Planning workspace panel | Page spec + data model **only** |
| Persona program rollup | Supabase view + `persona-view-spec-2026-05-19.md` |
| Governance 6-panel | Page spec v2 **only** |

### 4.6 Lane E freshness (area canonicals — ERP-adjacent)

From I86 Wave H Lane E landing evidence (`files-modified.csv` row H-lane-e, **not re-run in this sweep**):

| Metric | Count |
|:---|:---:|
| Surfaces scanned | **148** |
| fresh (≤3d) | **28** |
| medium (≤30d) | **98** |
| long_term (≤90d) | **0** |
| stale | **22** (all **missing** `last_review` / `last_review_at` frontmatter) |

`HLK_ERP_ARCHITECTURE.md` has `last_review: 2026-05-13` → **medium** tier at sweep date. **Not stale**, but panel table is **ahead of implementation** (spec freshness ≠ product freshness).

---

## §5 — Axis 4: Operational cohesion

### 5.1 Existing "how it fits together" canonicals

| Document | Role | Answers cohesion? |
|:---|:---|:---:|
| [`WORKSPACE_BLUEPRINT_HOLISTIKA.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md) | Four-channel persistence, engagement folders | **Partial** — vault/engagement shape, not ERP/dashboard routing |
| [`HLK_ERP_ARCHITECTURE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md) | Mirror→view→panel triplets | **Partial** — architecture **contract**, mostly **unbuilt** panels |
| [`KM_CHANNEL_VALUE_NARRATIVE.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/KM_CHANNEL_VALUE_NARRATIVE.md) | Customer-facing KM story | External narrative, not operator routing |
| [`HOLISTIKA_ORGANISING_DOCTRINE.md`](../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/HOLISTIKA_ORGANISING_DOCTRINE.md) | People / DoD | Discipline, not surface map |
| [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) | Two-plane Supabase, mirrors | **Ops data** discipline |
| [`akos-external-render-discipline.mdc`](../../../../.cursor/rules/akos-external-render-discipline.mdc) | Audience × format × channel | **Delivery** axis, not portfolio visibility |
| **OPERATIONAL_COHESION_DOCTRINE** | — | **Does not exist** (Option D proposes minting) |

### 5.2 Latest cross-area visibility artifact

| Artifact | Date | Scope |
|:---|:---|:---|
| `cluster-burndown-inventory.md` | 2026-05-19 | **Best current** "what's left" for I86 cluster |
| `HLK_ERP_ARCHITECTURE.md` | 2026-05-13 | ERP contract |
| `lane-f-app-governance-inventory-2026-05-19.md` | 2026-05-19 | GitHub app inventory — **adjacent** to visibility, not operator map |
| I62 `impeccable-shape-operator-inbox-2026-05-06.md` | 2026-05-06 | ERP inbox **shape** — pre-dates I65/I89 |

**Nothing ≤30 days** answers: *"Open this first for AKOS vs ERP vs external."*

### 5.3 Wave-level cohesion (I86)

- **5/10** cluster siblings closed (I85, I87, I84, I79, I80 per burndown narrative).
- **Active:** I76, I78, I81, I82, I89 — **all** visible in separate folders; **no** single ERP rollup UI.
- **OPS-86-1** remains open until all ten siblings closed — operator may perceive "endless cluster" without a **progress bar** surface.

### 5.4 Minimum vs maximum rework option-space

| Scope | What changes | Effort | Risk |
|:---|:---|:---:|:---|
| **Minimum** | Re-render dashboards + 1-page `OPERATIONAL_VISIBILITY_MAP.md` (planning-only) + README links | 1–2d | Low; doesn't fix ERP |
| **Medium** | Option A + new initiative: top-5 gap fixes (I65 stub route, inbox triage, cluster landing) | 1–2wk | Medium |
| **Maximum** | Full ERP rework: I62 completion + I65 + I64 + I89 + retire duplicate markdown surfaces | 1–2mo+ | High; supersede conflicts |

---

## §6 — Ranked options for inline-ratify

### Option A — Status-quo + dashboard render refresh (smallest)

**Scope:** Run `render_wip_dashboard.py`, `render_operator_inbox.py`; add **one** static landing `docs/wip/planning/dashboards/2026-05-19/index.md` linking WIP + Inbox + I86 burndown + USER_GUIDE §; refresh OPERATOR_INBOX copy for Wave H.

| Pros | Cons | Risk |
|:---|:---|:---|
| Hours–2d; no new INIT | **Does not** answer ERP confusion | Operator still two-system |
| Uses existing scripts | No doctrine for routing | Fatigue if inbox still noisy |

**Files touched:** `WIP_DASHBOARD.md`, `OPERATOR_INBOX.md`, new `dashboards/.../index.md` only.
**Decisions affected:** none new; supports D-IH-86-U drain.
**Ratify gates:** 0–1 (whether to create dashboards folder).

---

### Option B — Visibility audit + targeted gap fixes (medium) **(recommended component)**

**Scope:** Mint **I-NN-VISIBILITY-AUDIT** (or fold into I86 Wave I lane): inventory all operator surfaces; rank top-5 gaps; forward-charter ERP work; **no** preemptive ERP rewrite.

| Pros | Cons | Risk |
|:---|:---|:---|
| Names gaps with evidence | +1 initiative folder | Audit without fixes may feel hollow |
| De-risks Option C | 1–2 weeks | Scope creep into I62 |

**Typical top-5 from this sweep:** (1) no landing page, (2) I65 not built, (3) I89 rollups not built, (4) inbox seed noise, (5) I62/registry status drift.
**Decisions:** D-IH-NN-A..C likely.
**Ratify gates:** 2–3 (charter scope, top-5 priority, ERP vs AKOS-first).

---

### Option C — HLK-ERP rework + audience UX phase (large)

**Scope:** Treat I62+I65+I64+I89 as **one program**; pause new AKOS markdown surfaces; finish Mission Control + planning panel + rollups.

| Pros | Cons | Risk |
|:---|:---|:---|
| Delivers doctrine vision | 1–2 months | PMO bandwidth (R-IH-86-1) |
| True single pane in ERP | Supersedes I62/I65 partial work | Cross-repo bless overhead |

**Decisions affected:** D-IH-62-* closure, D-IH-65-*, D-IH-89-*; may conflict with I81/I82 parallel work.
**Ratify gates:** 4+ (architecture, pause markdown expansion, Vercel topology).

---

### Option D — Operational doctrine canonical first (governance-first)

**Scope:** Mint `OPERATIONAL_COHESION_DOCTRINE.md` under PMO canonicals: AKOS markdown surfaces vs ERP routes vs external render vs OpenClaw; **then** B or C.

| Pros | Cons | Risk |
|:---|:---|:---|
| Directly answers "how fit together" | 3–5d before visible UI | Doctrine without enforcement ignored |
| Low blast radius | Another canonical to maintain | Needs pairing registry row |

**Paired:** SOP + `scripts/render_operational_cohesion_index.py` per executable-process-catalog.
**Ratify gates:** 1–2 (doctrine scope; audience J-OP only vs broader).

---

### Option E — Multi-lane wave: A + D + B, defer C (combo) **(recommended)**

**Scope:** Wave I: (1) dashboard refresh (A), (2) doctrine mint (D), (3) charter visibility audit (B); **defer** full ERP rework (C) until audit ranks whether I62 completion or I65-only gives 80% value.

| Pros | Cons | Risk |
|:---|:---|:---|
| Fast visible win + narrative | 1–2 weeks across lanes | Three parallel threads |
| Matches L65–L66 scratchpad cluster | Still not full ERP | Needs explicit "ERP deferred" comms |

**Forward-charters:** I-NN-VISIBILITY-AUDIT; optionally absorb into I86 as Wave I (not new cluster).
**Ratify gates:** 2 (Wave I composition; ERP deferral).

---

## §7 — Recommendation

**Option E (recommended — doctrine + dashboard refresh + audit; defer ERP mega-rework until audit).**

Rationale: The repo already has **strong SSOT and validators**; the operator pain is **routing and implementation lag** between AKOS markdown ops (live) and ERP doctrine (mostly reserved). A **1–2 day** dashboard landing (A) plus a **short cohesion doctrine** (D) gives immediate legibility; a **bounded audit** (B) prevents Option C from becoming an unscoped rewrite. **I65** is the highest-leverage ERP slice for "where is planning?" — not a full I62 P4–P11 replay.

---

## §8 — Open questions for operator (≤5)

1. **Primary daily surface:** Markdown in AKOS (`OPERATOR_INBOX` + burndown) vs browser ERP — which should win when both exist?
2. **Rework appetite:** Is **I65 planning panel only** (2–3 weeks) acceptable as "visibility fix," or is full **I62 Mission Control** completion mandatory first?
3. **Audience scope:** Is visibility **J-OP only**, or do cleared collaborators need read-only ERP/dashboard access soon?
4. **Cluster vs new INIT:** Should visibility work stay **inside I86 Wave I**, or mint standalone **I-NN-VISIBILITY-AUDIT**?
5. **I62 status truth:** Should `INITIATIVE_REGISTRY` row for I62 flip to **closed** (UAT suggests closure) or stay **active** until ERP deploy proves P4+?

---

## §9 — Evidence appendix

### 9.1 Lane E freshness validator (baseline from Wave H landing; re-run locally)

Command for parent:

```powershell
py scripts/validate_canonical_enrichment_freshness.py
```

**Recorded baseline** (I86 `files-modified.csv`, Lane E, 2026-05-19):

```
Thresholds: fresh ≤3d | medium ≤30d | long_term ≤90d | stale >90d or missing review date
Total surfaces: 148
fresh: 28 | medium: 98 | long_term: 0 | stale: 22 (missing frontmatter review date)
```

Per-area table was emitted at validator mint time; refresh by re-running the command for current-day numbers.

### 9.2 External render trail (reference)

From `uat-render-quality-2026-05-19.md`:

```
validate_external_render_trail — PASS (strict=True, strict_freshness=True)
external-tagged: 6 | with trail: 6 | pending: 0 | stale renders: 0
```

### 9.3 Key file list (grep anchors)

- Scratchpad L66: `docs/wip/planning/86-initiative-cluster-execution-coordinator/operator-scratchpad.md`
- Cluster inventory: `docs/wip/planning/86-initiative-cluster-execution-coordinator/cluster-burndown-inventory.md`
- ERP architecture: `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/HLK_ERP_ARCHITECTURE.md`
- I89 charter: `docs/wip/planning/89-hlk-erp-program-rollup-implementation/master-roadmap.md`
- I65 charter: `docs/wip/planning/65-akos-planning-workspace-panel/master-roadmap.md`
- I62 charter: `docs/wip/planning/62-mission-control/master-roadmap.md`
- Rendering registry: `docs/references/hlk/v3.0/Envoy Tech Lab/canonicals/dimensions/RENDERING_PIPELINE_REGISTRY.csv`
- Audience registry: `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/AUDIENCE_REGISTRY.csv`

### 9.4 Evidence-gathering completeness

| Axis | Completeness |
|:---|:---|
| 1 AKOS internal | **Complete** for repo-local surfaces |
| 2 HLK external | **Complete** for registry + render gate; **boilerplate deploy state** not browser-verified |
| 3 HLK-ERP | **Complete** for AKOS planning evidence; **sibling `hlk-erp` UI** not inspected (path outside repo) |
| 4 Cohesion | **Complete** for doctrine gap analysis |
