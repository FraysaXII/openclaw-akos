---
report_type: pmo-status-sweep
parent_initiative: INIT-OPENCLAW_AKOS-95
authored: 2026-06-09
authored_by: Execution seat (Composer)
audience: J-OP
status: active
ratifying_decisions:
  - D-IH-95-M
  - D-IH-95-L
  - D-IH-95-B
  - D-IH-95-G
  - D-IH-95-J
linked_runbooks:
  - scripts/validate_hlk.py
  - scripts/neo4j_connectivity_probe.py
  - scripts/verify.py
---

# I95 PMO status sweep — 2026-06-09

**Initiative:** INIT-OPENCLAW_AKOS-95 — the **Canonical Articulation Model** (HCAM + governed knowledge graph over CSV SSOT)  
**Base commit:** `bab57c2` (sweep originally cut at `b052174`; refreshed after the full regression)  
**Funding closure:** **D-IH-95-M** ratified (see [`i95-fq2-ratification-2026-06-09.md`](i95-fq2-ratification-2026-06-09.md))  
**Full regression (end-of-day):** **PASS-WITH-FOLLOWUP** — [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md). Two scopes (today's 13-commit chain + initiative-wide intent-ranked sweep): **0 doctrine-level regressions**; 9 hygiene fixes applied in the regression commit (decision-log parity for `D-IH-95-J`/`D-IH-95-K`, CHANGELOG back-coverage, stale "draft" claims on `D-IH-95-M`, 12 broken links, backup-path drift); 3 tracked deferrals — **OPS-95-2** (engagement-model linkage backfill), **OPS-95-3** (I95 file-change ledger backfill), **L3 tranche-5** (10 active relationship triples still without FK bindings).

---

## 1. Where we are

| Surface | Status | Plain language |
|:---|:---|:---|
| **P95-GOV wave** | **Closed** (PASS) | Universal canonical governance registry + Plane-1 hardening + mirror emit contract landed; Neo4j N4 CQ blocker cleared 2026-06-09 |
| **Prod mirror** | **APPLIED** | Compliance mirror DML applied to MasterData; GOV-7 DDL pushed; 171 batches succeeded after FK fix |
| **Row-count parity** | **PASS** @ 2026-06-09 | CSV emit row counts match prod mirror tables (post pooler recovery) |
| **Neo4j graph harness** | **PASS** (F6 closed) | Instance `6c0d76bf`; username `6c0d76bf`; dual-emit sync + probe + CQ UAT PASS |
| **L3 FK→verb tranches** | **Bindings complete** | Bundles A+B+C done; 44 L3 bindings; TRP-030/036 stay **planned** (charter disposition 2026-06-10) |
| **L1 Supabase EG-2 doc** | **Done** | [`SUPABASE_API_EXPOSURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_API_EXPOSURE.md) minted; EG-3..5 still open |
| **Full back-covering regression** | **PASS-WITH-FOLLOWUP** @ `bab57c2` | [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md) — chain audit + intent-ranked sweep; fix-now batch applied; OPS-95-2/3 + L3 tranche-5 tracked |
| **I95 initiative** | **Active** | GOV closed; HCAM / graph / articulation lanes remain |

---

## 2. What we achieved (by audience)

### For you (operator)

- **Governance inventory is now explicit** — 73 vault surfaces registered with Plane-1 validator + Plane-2 mirror posture in one registry you can query and extend.
- **Prod mirror truth restored** — after migration drift repair, live Supabase mirrors match git-canonical CSVs again (emit contract PASS).
- **Capability + process singularity** — ~1,119 seed-cloned capabilities collapsed to **93** stable maps; process list curated to **496** with task-grain work demoted to a backlog registry (not deleted).
- **Funding posture decided** — no ~$65/mo Aura Professional in 2026 unless funding gate reopens; clear ordered path: restore graph → spike self-host → EU + vendor applications.

### For Holistika internal

- **HCAM doctrine home** — entity catalog, relationship registry, and articulation validators wired into the daily HLK gate (`validate_hlk.py`).
- **Two-plane integrity** — CSV column alignment, Pydantic↔mirror enum SSOT, and emit-contract checks prevent "green validators + silent mirror drift."
- **Collaborator-share strict gate** — settlement tranche (Hygiene C) aligned live engagement reality; `--strict` collaborator-share runs inside the HLK umbrella.
- **Semantic Council SOP** — federated area authorship model for wiring orphans and triple activation.

### For external allies and market

- **EU funding narrative anchored** — **EIC Accelerator Open** as primary public track; LOI/application work sequenced after graph restore (credible ops before grant prose).
- **Vendor credits path** — Neo4j Startup application (up to ~$16K credits) paired with Pre-Accelerator screen — framed as **AI knowledge infrastructure for regulated SME engagements**, not generic database spend.
- **Self-hosted escalation default** — post-credits ops target ~$30/mo Community Edition VM preserves Cypher portability and doctrine fit vs Aura Pro as default.

---

## 3. Value strategy sweep

| Strategy lane | What it buys | Current posture |
|:---|:---|:---|
| **Governance KG** | Queryable inventory of what the vault validates and what mirrors to Supabase | **Live** — GOV registry + validators |
| **Mirror truth** | Operators and ERP consumers read the same rows as git CSVs | **Live** — prod apply + parity PASS |
| **Capability collapse** | Stable WHAT (capabilities) decoupled from volatile HOW (processes) | **Done** — D-IH-95-I; rating cadence follow-up open |
| **Share settlement** | Partner/vendor economics match live engagements under strict audit | **Done** — Hygiene C; strict gate active |
| **Graph harness** | HCAM verb-typed edges + competency questions over Neo4j read index | **Live** — F6 restore + dual-emit + CQ UAT PASS on `6c0d76bf` |
| **Funding radar** | Ranked 2026 economics (Free → credits → EU → self-host) | **Closed** — D-IH-95-M |

Evidence synthesis: [`neo4j-graph-infrastructure-funding-research-area-2026-06-09.md`](../../../intelligence/neo4j-graph-infrastructure-funding-research-area-2026-06-09.md).

---

## 4. Master execution queue (ordered)

| # | Work item | Owner posture | Exit gate |
|:---|:---|:---|:---|
| **1** | ~~**F6 Neo4j restore** F6-R0..R7~~ | **DONE** 2026-06-09 | Instance `6c0d76bf`; backup vaulted; dual-emit + CQ PASS |
| **2** | ~~**Connectivity probe**~~ | **DONE** | `py scripts/neo4j_connectivity_probe.py` exit **0** |
| **3** | ~~**CQ UAT**~~ | **DONE** | [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md) PASS |
| **4** | **Self-hosted spike charter** | Thinking → execution | I07 `neo4j+s` contract preserved; TCO ~$30/mo documented |
| **5** | **EIC Pre-Accelerator screen + Open LOI draft** | Operator + Research | Eligibility checked; LOI draft ready for review |
| **6** | **Neo4j Startup application pack** | Operator + Research | Application submitted or explicitly deferred with reason |
| **7** | ~~**L3 bundle C** (TRP-030/036)~~ **+ tranche-5** | Semantic Council + CSV gate | **DONE** 2026-06-10 — Bundle C charter disposition; tranche-5 = 44 bindings |
| **8** | **EG-3** (edge-fn / cron / extension registries) | Data architecture | Three registries minted + validators |
| **9** | **Orphan burn-down** | Semantic Council | `--matrix` wiring % rises area-by-area |
| **10** | **Full verification bar** | CI + operator | `py scripts/verify.py pre_commit` PASS |

Charter: [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](i95-neo4j-free-backup-restore-charter-2026-06-09.md).

**Regression deltas (small, non-blocking — queue alongside, not ahead of, F6):**

- **OPS-95-2** — link each engagement to its engagement-model class (the 7-class taxonomy that says how a collaborator is engaged: hourly, milestone, percentage…). The prod mirror apply had to blank three values that pointed at the wrong registry (template IDs); the column is now empty on all 7 engagements. One small operator-gated CSV pass fixes it.
- **OPS-95-3** — backfill I95's per-initiative file-change ledger (`files-modified.csv`, the traceability CSV every initiative folder carries). Header + current-commit rows seeded by the regression; history backfill is mechanical.
- **Pending operator CSV gate (unchanged from D-IH-95-M):** the funding research area proposes 1 topic row + 2 intelligence-radar rows (appendices A/B of the synthesis). They stay proposal-only until you approve the registry edits.
- **Backup retention process** — F6-R0 **DONE**: repo-root export moved to `%USERPROFILE%\.openclaw\vault\neo4j-backups\` with SHA256 sidecar. Optional: consolidate older export in `Downloads\` into vault. Vault SOP + process-list row still forward-chartered post first restore drill.

---

## 5. What you do this week (operator)

### 1. ~~F6-R0 — Move backup to operator vault~~ **DONE** (execution seat 2026-06-09)

Vault path: `%USERPROFILE%\.openclaw\vault\neo4j-backups\b6d76b10-2026-06-09T14-30-52-b6d76b10.backup` + `.sha256.json` sidecar. Repo root clean.

**Optional:** move `Downloads\b6d76b10-2026-05-22T13-13-10-b6d76b10.backup` into the same vault if you want both exports under retention policy.

### 2. ~~F6-R1..R4 — Restore + rewire + probe~~ **DONE**

Live instance **`6c0d76bf`**; username **`6c0d76bf`**; dual-emit sync PASS; CQ UAT PASS.

### 3. Parallel — EIC Pre-Accelerator eligibility screen (≈20 min)

Skim EIC Pre-Accelerator 2026 criteria against Holistika TRL/legal entity posture; note blockers for LOI step (no submission required this week unless you choose to).

### 5. Optional sanity — fast HLK gate (≈3 min)

After any local CSV edits only:

```powershell
cd "$env:USERPROFILE\cd_shadow\openclaw-akos"
py scripts/verify.py pre_commit_fast
```

---

## 7. Cluster dependencies

**Burndown SSOT (I95 lens):** [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) — I86 portfolio coordinator + I90 routing ordnance + I91 graph handoff after F6 unblocked Neo4j. Official deps: [`INITIATIVE_DEPENDENCIES.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md) (refreshed 2026-06-10).

**Top 3 cluster-efficiency actions** (full ranked queue in cluster map §Burndown):

1. ~~**I86 Wave N INDEX_INTEGRITY**~~ — **DONE** 2026-06-10 (I95 Tranche 2): planning README + INITIATIVE_DEPENDENCIES I90–I95 edges + IDX-02/06/08 gap fixes; sweep [`index-sweep-2026-06-10-tranche2-wave-n.md`](index-sweep-2026-06-10-tranche2-wave-n.md).
2. ~~**I91 P1–P2** — Neo4j preflight + store-coverage matrix v1~~ — **DONE** 2026-06-10 (I95 Tranche 3): probe exit 0; [`store-coverage-matrix-2026-06-10.md`](../../91-enterprise-graph-store-coverage/reports/store-coverage-matrix-2026-06-10.md).
3. ~~**I95 L3 Bundle C ratify** (TRP-030/036)~~ — **DONE** 2026-06-10 (Tranche 4): keep planned; [`i95-l3-bundle-c-disposition-2026-06-10.md`](i95-l3-bundle-c-disposition-2026-06-10.md).
4. **I95 L1 EG-3** registries — **next** operator tranche (edge-fn / cron / extension).

**Registry gap:** ~~`INITIATIVE_DEPENDENCIES.md` stale vs I90–I95~~ — **cleared** 2026-06-10 (`last_generated` bumped; I90–I95 section added).

## 6. Cross-references

- Cluster map: [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md)
- Full regression (verdict + findings): [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md)
- FQ ratification: [`i95-fq2-ratification-2026-06-09.md`](i95-fq2-ratification-2026-06-09.md)
- GOV closure UAT: [`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md)
- Mirror apply evidence: [`operator-mirror-apply-execution-2026-06-09.md`](operator-mirror-apply-execution-2026-06-09.md)
- Master roadmap queue: [`master-roadmap.md`](../master-roadmap.md)
