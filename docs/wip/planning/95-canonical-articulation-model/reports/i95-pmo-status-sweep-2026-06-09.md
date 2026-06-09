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
**Base commit:** `b052174`  
**Funding closure:** **D-IH-95-M** ratified (see [`i95-fq2-ratification-2026-06-09.md`](i95-fq2-ratification-2026-06-09.md))

---

## 1. Where we are

| Surface | Status | Plain language |
|:---|:---|:---|
| **P95-GOV wave** | **Closed** (PASS-WITH-FOLLOWUP) | Universal canonical governance registry + Plane-1 hardening + mirror emit contract landed across seven GOV tranches |
| **Prod mirror** | **APPLIED** | Compliance mirror DML applied to MasterData; GOV-7 DDL pushed; 171 batches succeeded after FK fix |
| **Row-count parity** | **PASS** @ 2026-06-09 | CSV emit row counts match prod mirror tables (post pooler recovery) |
| **Neo4j graph harness** | **BLOCKED-AUTH** | Connectivity probe fails (`wrong_password_or_user`); GHA keepalive returns `42NFF` — pending **F6 restore** (F6-R0..R7) |
| **L3 FK→verb tranches** | **Tranche-4 done** | Bundles A+B committed (12 bindings); **Bundle C** (TRP-030/036) charter-only |
| **L1 Supabase EG-2 doc** | **Done** | [`SUPABASE_API_EXPOSURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/SUPABASE_API_EXPOSURE.md) minted; EG-3..5 still open |
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
| **Graph harness** | HCAM verb-typed edges + competency questions over Neo4j read index | **Blocked** — F6 restore first |
| **Funding radar** | Ranked 2026 economics (Free → credits → EU → self-host) | **Closed** — D-IH-95-M |

Evidence synthesis: [`neo4j-graph-infrastructure-funding-research-area-2026-06-09.md`](../../../intelligence/neo4j-graph-infrastructure-funding-research-area-2026-06-09.md).

---

## 4. Master execution queue (ordered)

| # | Work item | Owner posture | Exit gate |
|:---|:---|:---|:---|
| **1** | **F6 Neo4j restore** F6-R0..R7 | Operator + execution seat | Backup in vault; Aura Free restore complete |
| **2** | **Connectivity probe** | Operator env | `py scripts/neo4j_connectivity_probe.py` exit **0** |
| **3** | **CQ UAT** | Execution seat | `run_cq_uat.py` PASS (competency questions live) |
| **4** | **Self-hosted spike charter** | Thinking → execution | I07 `neo4j+s` contract preserved; TCO ~$30/mo documented |
| **5** | **EIC Pre-Accelerator screen + Open LOI draft** | Operator + Research | Eligibility checked; LOI draft ready for review |
| **6** | **Neo4j Startup application pack** | Operator + Research | Application submitted or explicitly deferred with reason |
| **7** | **L3 bundle C** (TRP-030/036) | Semantic Council + CSV gate | Charter ratified → promotion commit if FK columns exist |
| **8** | **EG-3** (edge-fn / cron / extension registries) | Data architecture | Three registries minted + validators |
| **9** | **Orphan burn-down** | Semantic Council | `--matrix` wiring % rises area-by-area |
| **10** | **Full verification bar** | CI + operator | `py scripts/verify.py pre_commit` PASS |

Charter: [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](i95-neo4j-free-backup-restore-charter-2026-06-09.md).

---

## 5. What you do this week (operator)

### 1. F6-R0 — Move backup to operator vault (≈10 min)

Confirm the export exists (~308 KB), then vault it (never commit):

```powershell
$vault = "$env:USERPROFILE\.openclaw\vault\neo4j-backups"
New-Item -ItemType Directory -Force -Path $vault | Out-Null
Move-Item -Force "$env:USERPROFILE\cd_shadow\openclaw-akos\b6d76b10-2026-06-09T14-30-52-b6d76b10.backup" $vault\
git -C "$env:USERPROFILE\cd_shadow\openclaw-akos" status --short
```

Expect: backup **absent** from repo root; `git status` clean of `.backup` files.

### 2. F6-R1..R2 — Aura Free restore (≈30–45 min)

In Neo4j Aura console: ensure a **Free** instance slot → **Restore from backup file** using the vaulted `.backup` (<4 GB). Save new credentials securely.

### 3. F6-R3..R4 — Rewire AKOS + probe (≈15 min)

Update `~/.openclaw/.env` (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`) and matching GitHub Actions secrets, then:

```powershell
cd "$env:USERPROFILE\cd_shadow\openclaw-akos"
py scripts/neo4j_connectivity_probe.py
```

Expect: exit code **0**.

### 4. Parallel — EIC Pre-Accelerator eligibility screen (≈20 min)

Skim EIC Pre-Accelerator 2026 criteria against Holistika TRL/legal entity posture; note blockers for LOI step (no submission required this week unless you choose to).

### 5. Optional sanity — fast HLK gate (≈3 min)

After any local CSV edits only:

```powershell
cd "$env:USERPROFILE\cd_shadow\openclaw-akos"
py scripts/verify.py pre_commit_fast
```

---

## 6. Cross-references

- FQ ratification: [`i95-fq2-ratification-2026-06-09.md`](i95-fq2-ratification-2026-06-09.md)
- GOV closure UAT: [`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md)
- Mirror apply evidence: [`operator-mirror-apply-execution-2026-06-09.md`](operator-mirror-apply-execution-2026-06-09.md)
- Master roadmap queue: [`master-roadmap.md`](../master-roadmap.md)
