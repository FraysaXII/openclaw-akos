---
intellectual_kind: research_master_synthesis
parent_initiative: INIT-OPENCLAW_AKOS-95
authored: 2026-06-06
status: active
language: en
control_confidence_level: Keter
note: Round-2 multi-agent research synthesis (4 parallel agents) - integrated into the KB per operator directive "recycle + integrate so we don't lose those things again". Feeds the 2026-06-06 decision batch Round 2.
agents:
  - 765aa76c (intelligence-corpus open-decision inventory)
  - cf03d241 (Supabase ecosystem governance inventory)
  - db9d6473 (process<->capability fusion)
  - aa9278a5 (Knowledge Management home)
---

# Round 2 — multi-agent research synthesis (2026-06-06)

> Four parallel research agents, dispatched per the operator's "cover my back + use several agents +
> integrate into the KB" directive. This artifact is the durable record so the reasoning is not
> re-lost. Each section ends with the decision it resolves.

## 1. Process ↔ Capability — KEEP SEPARATE BUT LINKED; de-densify (do NOT fuse)

**Finding (agent db9d6473):** the operator's fusion instinct detects a *real* redundancy but
mis-diagnoses it. Cause: `CAPABILITY_REGISTRY` was seed-cloned ~1:1 off `process_list` (1,119 rows,
~1,019 kb-integrity seeds) → it reads as a process-shadow. **Cure = de-densification, not fusion.**

- EA doctrine is unanimous: a **capability = stable WHAT** (sellable), a **process = volatile HOW**;
  kept as distinct element types linked by **realization** (which HCAM already has: `HCAM-TRP-006`,
  N:N, active). TOGAF G189, ArchiMate strategy layer, BIZBOK, Ardoq (N:N: one process spans many
  capabilities), LeanIX/Gartner.
- **Collapse the registry to a coarse, stable map** (~50–150 capabilities, 2–4 levels; activate the
  `planned` `HCAM-TRP-014` capability→capability composition). Many processes realize one capability.
- **Killer Holistika reason:** the Talent-H→Talent-A (human→AIC) migration *requires* the capability
  to be the invariant while the realizing process swaps bearer. Fusing breaks the agentic/Singularity
  continuity + makes competency-questions CQ1/CQ3 unanswerable.
- **Confidence workload:** rating ~150 stable capabilities is tractable; rating 1,119 process-shadows
  is why it's 100% unrated. De-densification makes PC-01's value-triaged rating *structural*.

**Resolves:** PC-01 (rate ~150 not 1,119), PC-02 (gold-layer join, no FK on process_list), PC-03
(lifecycle maturation gate on real capabilities). **Decision → R2-01.**

## 2. Knowledge Management — 3-way split; sellable-CI-quality → Research; NO new role

**Finding (agent aa9278a5):** "KM" hides three functions with three correct homes:
1. **Knowledge architecture** (the HCAM enterprise ontology/metamodel) → **Data, Semantic Council** —
   already ratified `D-IH-95-A/C`; leave it.
2. **Sellable corporate-intelligence quality** (the SOTA bar on what the dossiers contain — the
   operator's real concern) → **Research**, as a named workstream: Research Director accountable;
   **activate the dormant KM Officer seat** already defined in the Research charter; Lead Researcher
   already owns "quality + methodology compliance of research outputs"; Research/Validation is the
   truth-gate. **NOT People-because-of-talent** (that relegates KM to a support function — APQC,
   Enterprise Knowledge). Tipping reason: per the **corporate-intelligence CNAE identity + ENISA
   innovation narrative**, intelligence IS the product → the quality bar IS the product → a
   Research/Validation competence, not HR.
3. **Knowledge curation/plumbing** (Topic-Fact-Source contract, access/confidence, store+retrieval)
   → stays **federated** (People/Compliance + Tech), unchanged.

No new "Knowledge Manager" title (re-fuses what should stay split). Citations: APQC, Enterprise
Knowledge, SCIP/Crayon, Valona, productized-IP literature. **Resolves HC-05 + sharpens it.
Decision → R2-02.**

## 3. Supabase ecosystem governance — govern the whole stack, not just tables

**Finding (agent cf03d241):** the repo governs **T2 tables/mirrors + the one FINOPS pipeline well**
(82 migrations, 50+ compliance mirrors, pgmq + 3 Edge Functions + 2 cron). But **doctrine names 9
modules and only governs tables/mirrors/one-Edge-pattern/pgmq/partial-cron**. Ungoverned / live-only:
**Auth, Storage, Realtime, pg_vector, complete Edge-function registry, extension manifest
(pg_cron/pg_net/wrappers), cron registry, FDW `stripe_gtm` DDL, RLS-as-a-system (100+ scattered
policies; adapter + collaborator mirrors RLS-on-but-no-policy), PostgREST exposure SSOT (config drift:
hosted exposes holistika_ops+finops; config.toml lists only public).**

Plus the live-assessment (this turn) confirmed: mirror staleness (decision -54, process -20, ops -11)
+ 16 RLS-disabled `public.*` tables (critical) + ~30 untracked legacy `public.*`/`kirbe.*` tables.

**Data-Architect ownership targets (mint):** `SUPABASE_MODULE_REGISTRY`, `SUPABASE_EDGE_FUNCTION_REGISTRY`,
`SUPABASE_EXTENSION_MANIFEST`, `SUPABASE_CRON_REGISTRY`, `SUPABASE_API_EXPOSURE`, `SUPABASE_RLS_POSTURE`
+ validator, FDW inventory runbook. **Resolves DB-01/DB-02. Decision → R2-03.**

## 4. Open-decision inventory — 40+ threads, 9 themes (the backlog SSOT)

**Finding (agent 765aa76c):** 40+ unresolved threads across the linking model (P5 FK→verb tail not
done), the 22 planned triples / orphan worklist, I91 cutover, I94 drift moves (DRIFT-1..9) + pending
phases (P3 Operations, P4 People/Compliance, P5 Envoy, P6 Legal, P7 subfolder, P8 DATA regression, P9
closure), the "what is an area" residuals, and cross-cutting "craft again / AskQuestion-before-A+D"
markers. Plus **index-integrity drift** (not decisions, just stale text to correct):
- `canonical-articulation-model-2026-06-05/README.md` still says "Knowledge Manager under People"
  (contradicts the ratified Data-federated finding).
- `95.../master-roadmap.md` still lists D-IH-95-B/C/E "pending" though ratified.
- `hcam-catalog-and-verbs-for-signoff.md` frontmatter still `awaiting_operator_signoff` (superseded
  by D-IH-95-B).

**Resolves:** adopt the inventory as the I94/I95 backlog; fix the drift. **Decision → R2-04.**

## 5. Web-grounded (already in the decision-batch doc)
- **HC-03 Neo4j:** Aura Free auto-pauses after 3 days of no *writes*; keep-alive write ping (free) +
  budget $65 Professional. Graph fits free limits. I91 cutover runnable while online.
- **HC-01 verbs:** FREEZE the 11; extend by **specialization + SHACL**, never new top-level verbs
  (ArchiMEO, Mendoza ArchiMate-3.2 RDF/OWL, NILUS).

## 6. Round-2 decision set (ratifiable; see the AskQuestion batch)
R2-01 fusion (keep-separate + de-densify) · R2-02 KM (3-way split + Research KM Officer) ·
R2-03 Supabase ecosystem governance (mint the registries) · R2-04 inventory-as-backlog + index-fix ·
R2-05 P5 FK→verb order · R2-06 orphan burn-down order · R2-07 IntelligenceOps landing zone ·
R2-08 DRIFT business-strategy moves · R2-09 Neo4j keep-alive mechanism.
