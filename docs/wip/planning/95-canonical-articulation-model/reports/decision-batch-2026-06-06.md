# Consolidated decision batch — 2026-06-06 (MADEIRA "cover my back" sweep)

> Operator ask: *"cover my back, check other answers I gave + other brainstorms… use + expand the
> resources in docs/wip/intelligence, gather scattered logic, decide on each via a lengthy intense
> AskQuestion-ratified batch with you always proposing a grounded solution. ≥12 such decisions."*
>
> Each item below: **what's unresolved → my MADEIRA proposal (grounded) → options for ratify.**
> Sourced from: the live Supabase assessment (this turn), the process↔capability↔confidence reality,
> the I95 articulation arc (`canonical-articulation-model-2026-06-05/` + planning `95/`), the
> area-completeness research (`area-completeness-doctrine-2026-06-05/`), and prior brainstorms.

## A. Data reality / Supabase (from the live MCP assessment)

### DB-01 — Mirror re-sync cadence (T2 lapsed behind T1)
**Unresolved:** live mirrors are materially behind the CSV SSOT (decision_register 468/522, process
1187/1207, ops 139/150, initiative 74/80; baseline 77/70 stale-ahead). The re-sync isn't just the
rename — the cadence lapsed. **Proposal:** expand `OPS-95-1` to a **full re-sync now** + add an
**automated emit on every canonical-CSV commit** (CI), keeping the *apply* operator-gated (creds).
*Grounded:* two-plane doctrine says mirror follows CSV; drift this size means manual cadence failed →
automate the emit, gate the apply. **Options:** A manual-now+quarterly · B CI-emit+gated-apply (rec) · C cron nightly.

### DB-02 — Legacy `public.*` schema disposition (~30 untracked tables)
**Unresolved:** the live DB has ~30 `public.*` tables not in the governed three-tier (`test_aapl`
1258 rows, `test_*`, `rag_2`, `standard_process`, `research_process`, `nods_page`, old
`public.baseline_organisation` 49 rows, KiRBe-era `data_*`/`madeira_*`). **Proposal:** one-time
**inventory → drop the dead `test_*`/duplicate tables (operator-confirmed), document KiRBe-era as
reference-only legacy** (out of the governed schema), and register the decision. *Grounded:* "clean
KB not bloated" applies to the DB too; untracked tables are drift + the RLS risk surface.
**Options:** A inventory+drop-dead+document-legacy (rec) · B leave as-is · C bring all under governance.

### DB-03 — 🔴 RLS on the 16 exposed tables (CRITICAL)
**Unresolved:** 16 `public.*` tables have RLS disabled (anon key can read/write). **Proposal:** after
DB-02 drops the dead ones, **enable RLS + service-role-only (deny-by-default) policies** on the
survivors; never leave anon-writable. *Grounded:* Supabase advisory flags it critical; SOC posture.
**Options:** A drop-then-RLS-survivors (rec) · B RLS-deny-all-now · C defer (not recommended).

## B. Human workflow process-engineering (process ↔ capability ↔ confidence)

### PC-01 — Capability confidence is 100% seed-unrated (1119/1119 at 1.0)
**Unresolved:** the 5-dimension confidence layer was seeded once (I81 kb-integrity) and **never
rated** — it reflects nothing. **Proposal:** operationalize a **value-triaged quarterly rating
workflow** (Capability Curator): rate the ~100 active/engagement-bearing capabilities first (by
intent-ranked value), leave kb-integrity seeds as `seed` until their capability matures; surface the
real scores in the gold layer. *Grounded:* rating all 1119 is waste; value-first mirrors the
intent-ranked discipline; an unrated layer is worse than an honest "unrated" badge. **Options:**
A rate-all · B value-triaged (rec) · C deprecate the confidence registry.

### PC-02 — process ↔ capability link direction + human visibility
**Unresolved:** the link is one-way (`CAPABILITY_REGISTRY.originating_process_ids`); a role owner
can't easily see "my processes → capabilities → confidence." **Proposal:** keep capability→process
as SSOT (no duplicate FK on `process_list`); **surface the chain in the gold layer** (a per-role /
per-area "process→capability→confidence" view) using the existing HCAM triples (TRP-006/039/040).
*Grounded:* no schema duplication; the gold layer is the right consumption surface. **Options:**
A gold-layer-join-only (rec) · B add capability_id to process_list · C leave unlinked.

### PC-03 — Capability lifecycle maturation (most rows are seeds, not active)
**Unresolved:** ~1019 of 1119 capabilities lack an active lifecycle; they're kb-integrity seeds.
**Proposal:** a **maturation gate** (seed→registered→active) requiring a real process owner + a
confidence rating + a paired SOP — value-triaged with PC-01. *Grounded:* a capability isn't "real"
until owned + rated + exercised. **Options:** A value-triaged maturation (rec) · B bulk-activate · C leave seeded.

## C. Articulation model / the linking problem (I95 arc)

### HC-01 — Freeze the closed verb set, or allow domain verbs?
**Unresolved:** is the ArchiMate 10+association set final? **Proposal:** **freeze it**; extend only via
Semantic Council + a `D-IH` gate with strong justification. *Grounded:* closed set de-forks + is
learnable; local verb invention is how the graph forked originally. **Options:** A freeze (rec) · B add domain verbs · C per-area sets.

### HC-02 — Orphan worklist burn-down (AMBER→GREEN; 22 planned triples)
**Unresolved:** enterprise is 69% wired / AMBER; which orphans first? **Proposal:** burn down by
**intent-ranked value** (ICS) — the Data data_product/contract chain + engagement links first;
Council-dispositioned; target GREEN. *Grounded:* value-first; the gold layer already lists them.
**Options:** A value-ranked (rec) · B by-area · C defer to I91.

### HC-03 — I91 graph cutover (D-IH-95-F): wait for Neo4j, or unblock now?
**Unresolved:** the 13→6 edge unify is mapped but gated on Neo4j (`NEO4J_*` absent; I91 preflight-
blocked). **Proposal:** **provision an ephemeral/CI Neo4j to unblock the cutover now** (dual-emit one
cycle → retire legacy), rather than waiting indefinitely. *Grounded:* the operator's goal is
*automated layers*; an indefinitely-blocked cutover leaves the fork half-resolved. **Options:**
A keep waiting · B CI/ephemeral Neo4j to unblock now (rec) · C drop Neo4j → RDF.

### HC-04 — "The Singularity" / DTO — doctrine home + audience register
**Unresolved:** the operator coined "Singularity"; how is it carried? **Proposal:** keep **DTO** as
the technical/external register + **"the Singularity"** as the internal/vision register
(Quality-Fabric audience-resolved), documented in the HCAM canonical; optionally a short vision
one-pager. *Grounded:* dual-register per brand-baseline-reality discipline. **Options:**
A dual-register-in-canon (rec) · B pick one · C + separate Singularity vision doc.

### HC-05 — Knowledge Manager / Research — contributor or owner?
**Unresolved:** resolved Data-federated; should KM/Research be formalized? **Proposal:** **no new KM
role**; formalize Research (+ optional KM) as named **contributor seats** on the Semantic Council
(area reps), not owners. *Grounded:* the DG-ownership findings (53 sources) put the metamodel in
Data; KM/Research feed concepts. **Options:** A contributor-only (rec) · B mint KM role · C Research co-owns.

## D. Area-completeness / scope

### AC-01 — Promote v3 articulation to a scored component, or keep advisory?
**Unresolved:** articulation completeness is advisory (non-gating). **Proposal:** **stay advisory now
→ promote to a scored *enhancing* AREA-17 after the 8-area sweep raises coverage** (operator
sign-off), mirroring the v2 INFO→FAIL ramp. *Grounded:* don't gate on a layer that's 69% wired;
ramp like v2. **Options:** A advisory-now→enhancing-later (rec) · B enhancing now · C critical.

### AC-02 — Remaining area sweep (Operations/Legal/Envoy) + I94 interleave
**Unresolved:** I94 has unswept areas; sequencing. **Proposal:** **interleave** — run the area-v3
articulation sweep on the remaining areas now (verbs exist), value-ranked. *Grounded:* operator chose
interleave earlier; the verbs unblock it. **Options:** A interleave-now (rec) · B finish I95 cutover first · C defer.

### AC-03 — Entity axis in the gold layer (Holistika / Think Big / HLK Tech Lab)
**Unresolved:** the scorecard is area-only; the enterprise is multi-entity. **Proposal:** **add an
entity breakdown** to the gold layer so the DGO sees per-entity wiring. *Grounded:* cheap; the entity
axis already exists in the area model + baseline_organisation. **Options:** A add entity breakdown (rec) · B area-only · C defer.

---

**Count: 14 decisions** (≥12 ask satisfied). The background intelligence-corpus exploration is
cross-checking for any missed thread; additions fold into execution or a follow-up round.

---

## Round 1 outcomes (operator ratify 2026-06-06)

**Banked (actionable now):** DB-03 drop-then-RLS · HC-04 Singularity **vision doc** + dual-register ·
AC-01 **ramp** (advisory→enhancing later) · AC-02 **interleave** the area sweep.

**A + expanded scope (operator amendments):**
- **DB-01** A + *global drift-prevention*: Data Architect moves the missing tables, ensures integrity
  for present+future use cases, "never happens again". Method: **multi-agent research, recycled +
  integrated into the KB** (operator loved the subagent pattern — apply to all deep topics).
- **DB-02** A + *govern the FULL Supabase ecosystem* (not just tables — functions, edge functions,
  extensions, pgmq, cron, vault, FDW, RLS, storage, realtime). Data Architect owns it ASAP. Drop
  legacy; prioritise present+future if up to standard.
- **PC-01** A + **weekly cron** rating + the deep **fusion question** (fuse process_list +
  CAPABILITY_REGISTRY? operator suspects separate registries backfire on the Singularity; "a lot of
  DOING") → research agent R1.
- **AC-03** A + *careful entity tree/matrix design* (entities are umbrellas for scattered intel).

**Deferred to Round 2 (research-then-propose):** PC-02 + PC-03 (depend on the fusion decision R1) ·
HC-02 orphans (my grounded choice, likely value-ranked) · HC-05 KM home (R2 agent).

## Round 1 research findings (grounded)

- **HC-03 Neo4j (assessed):** Aura **Free auto-pauses after 3 days of no *write* activity**; 30 days
  paused → permanent deletion; no native keep-alive; no auto-backup. **Plan:** (a) free + a scheduled
  **write keep-alive ping** (GitHub Action or `pg_cron`→`pg_net`); (b) budget **~$65/mo Professional**
  for production. Graph fits free limits (200k nodes/400k rels). I91 cutover can run while online.
  Sources: support.neo4j.com Aura Free FAQ; neo4j.com Aura pause docs; assay.tools Aura API notes.
- **HC-01 verbs (grounded → FREEZE):** the **11 ArchiMate relationship types are the standard
  enterprise-ontology core**; domain needs are met by **specialization (sub-properties) + SHACL
  constraints, never new top-level verbs** (ArchiMEO; A. Mendoza ArchiMate-3.2 RDF/OWL + SHACL; NILUS
  "stable core + governed specialization"). → freeze; specialize via the Semantic Council.

## Round 2 (in flight — multi-agent research, to be integrated into KB)
- R1 fusion (process↔capability) · R2 KM home (People vs Research vs new; sellable-intelligence angle)
  · R3 full Supabase-ecosystem governance inventory · intelligence-corpus open-thread inventory.
- Each agent's findings → a durable KB artifact (research-action style) so the logic isn't re-lost.
