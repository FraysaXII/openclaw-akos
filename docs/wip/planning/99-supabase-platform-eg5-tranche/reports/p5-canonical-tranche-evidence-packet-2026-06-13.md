---
language: en
status: active
initiative: 99-supabase-platform-eg5-tranche
report_kind: inline-ratify-evidence-packet
phase: P5
gate_type: inline-ratify
parent_initiative: INIT-OPENCLAW_AKOS-99
authority: System Owner + Data Steward
last_review: 2026-06-13
audience: J-OP;J-AIC
ratifying_decisions_pending: []
ratifying_decisions: [D-IH-99-J]
---

# I99 P5 — canonical CSV tranche evidence packet (2026-06-13)

> **Status: EXECUTED** (Option A ratified 2026-06-13). Holistika closed the EG-5 Supabase platform gap: three vault registries, eight module flips, `DATA_ARCHITECTURE.md` §9 reconcile. **Harmonization (same day):** I96 domain SSOT + three-plane mapping point at canonical registry paths; Realtime publication migration minted for operator SQL gate.

**Operator choice (2026-06-13):** Full P5 tranche — registries + eight modules + §9 reconcile — then mint gate.

---

## 1. Evidence sweep (repo state)

### Draft registries (unique IDs verified)

| Draft | Rows | Spec |
|:---|:---|:---|
| [`SUPABASE_AUTH_REGISTRY.draft.csv`](../drafts/SUPABASE_AUTH_REGISTRY.draft.csv) | 16 | [`auth-registry-and-i96-consumer-spec-2026-06-13.md`](auth-registry-and-i96-consumer-spec-2026-06-13.md) |
| [`SUPABASE_REALTIME_REGISTRY.draft.csv`](../drafts/SUPABASE_REALTIME_REGISTRY.draft.csv) | 18 | [`realtime-publication-and-i96-freshness-spec-2026-06-13.md`](realtime-publication-and-i96-freshness-spec-2026-06-13.md) |
| [`SUPABASE_STORAGE_REGISTRY.draft.csv`](../drafts/SUPABASE_STORAGE_REGISTRY.draft.csv) | 25 | [`storage-bucket-and-gtm-asset-spec-2026-06-13.md`](storage-bucket-and-gtm-asset-spec-2026-06-13.md) |

Includes **Analytics/Iceberg** (ST-20, ST-25) and **Storage Vector** (ST-21, ST-26) per **D-IH-99-I** — [`multi-store-data-plane-alignment-2026-06-13.md`](multi-store-data-plane-alignment-2026-06-13.md).

### Validators (pre-mint baseline)

```text
py scripts/validate_supabase_module_registry.py  → PASS (27 modules; ungoverned=8; critical: SUPA-MOD-22)
py scripts/validate_bi_consumer_registry.py      → PASS (16 rows)
py scripts/validate_hlk.py                       → PASS (2026-06-13 session)
```

### Multi-store governance answer (vs Data Governance Policy)

[`DATA_GOVERNANCE_POLICY.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Governance/canonicals/DATA_GOVERNANCE_POLICY.md) §1 already covers **git CSVs**, **Supabase mirrors/FDW**, and **graph representations**. Before **D-IH-99-I**, I99 P4 under-represented Analytics and Vector as `out_of_scope`; that gap is closed in the Storage draft. **Neo4j (T3)** is properly governed under I91/I93 — not a Supabase module — with I99 coordination via ST-27 only.

| Store | Tier | Governance home after P5 |
|:---|:---|:---|
| Git vault CSVs | T1 | Data Steward (unchanged) |
| Supabase Postgres + Auth + Realtime + Storage | T2 | I99 registries + `SUPABASE_MODULE_REGISTRY` |
| Analytics Iceberg | T2 OLAP | I93 BI (`BI-HOL-ANALYTICS-BUCKETS`) + I99 Storage link rows |
| pg_vector / storage.vector | T2 extension | I99 `partial` MOD-17 + KiRBe/I83 boundary |
| Neo4j graph index | T3 | I91 + I93 (`BI-HOL-NEO4J`, `sync_hlk_neo4j.py`) |

---

## 2. Module registry flips (D-IH-99-D — eight rows)

| module_id | Today | P5 target | repo_artifact after mint |
|:---|:---|:---|:---|
| **SUPA-MOD-22** Auth | ungoverned | **governed** | `dimensions/SUPABASE_AUTH_REGISTRY.csv` |
| **SUPA-MOD-21** Realtime | ungoverned | **governed** | `dimensions/SUPABASE_REALTIME_REGISTRY.csv` |
| **SUPA-MOD-23** Storage | ungoverned | **governed** | `dimensions/SUPABASE_STORAGE_REGISTRY.csv` |
| **SUPA-MOD-17** pg_vector | ungoverned | **partial** | `SUPABASE_EXTENSION_MANIFEST.md` + ST-21/26 link |
| **SUPA-MOD-12** Edge secrets | ungoverned | **partial** | paths-only manifest note (no secret values) |
| **SUPA-MOD-20** DB Webhooks | ungoverned | **partial** | explicit zero-def row; pg_net forward |
| **SUPA-MOD-07** kirbe schema | ungoverned | **reference-only** | gap text: KiRBe app-owned DDL |
| **SUPA-MOD-26** seed SQL | ungoverned | **partial** | stub `supabase/seed.sql` or documented defer |

**Scorecard after mint (expected):** governed **18** · partial **8** · ungoverned **0** · forward **0** (critical Auth hole closed).

---

## 3. Atomic commit inventory (single phase-scoped commit)

### 3a. New vault CSVs (promote drafts → canonical)

| Target path | Source |
|:---|:---|
| `docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_AUTH_REGISTRY.csv` | P2 draft |
| `docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_REALTIME_REGISTRY.csv` | P3 draft |
| `docs/references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/dimensions/SUPABASE_STORAGE_REGISTRY.csv` | P4 draft |

### 3b. Validators + Pydantic helpers (mirror I95 EG-3 pattern)

| New script | Wired in `validate_hlk.py` |
|:---|:---|
| `scripts/validate_supabase_auth_registry.py` | yes |
| `scripts/validate_supabase_realtime_registry.py` | yes |
| `scripts/validate_supabase_storage_registry.py` | yes |
| `akos/hlk_supabase_auth_registry_csv.py` | — |
| `akos/hlk_supabase_realtime_registry_csv.py` | — |
| `akos/hlk_supabase_storage_registry_csv.py` | — |

### 3c. Registry governance rows (same commit)

- `CANONICAL_REGISTRY.csv` — 3 rows (`supabase_auth_registry`, `supabase_realtime_registry`, `supabase_storage_registry`)
- `CANONICAL_GOVERNANCE_REGISTRY.csv` — 3 rows (git_only validators)
- `PRECEDENCE.md` — 3 mirror rows
- `SUPABASE_MODULE_REGISTRY.csv` — eight row updates (§2)
- `SUPABASE_ECOSYSTEM_GOVERNANCE.md` — baseline scorecard line refresh

### 3d. Vault doctrine touch (scheduled — same commit)

**File:** [`DATA_ARCHITECTURE.md`](../../../../references/hlk/v3.0/Admin/O5-1/Data/Architecture/canonicals/DATA_ARCHITECTURE.md) §9

**Replace line 197:**

```markdown
Forward: Analytics Buckets (Iceberg) — **non-goal until GA** per `D-IH-93-I`.
```

**With:**

```markdown
| Analytics Buckets (Iceberg) | Marketing OLAP / campaign aggregates | `storage.analytics` + BI registry | `BI-HOL-ANALYTICS-BUCKETS` (operator production per `D-IH-93-J`) |
```

And add to module table row for Auth/Storage: registry SSOT pointers (`SUPABASE_AUTH_REGISTRY.csv`, `SUPABASE_STORAGE_REGISTRY.csv`).

**Rationale:** BI consumer is **active** since I93 P5c; Supabase alpha label is not a Holistika blocker per `SOP-DATA_PRODUCTION_READINESS_001.md`. Stale §9 text contradicted `DATA_BI_GOVERNANCE.md` and the Storage draft absorption.

### 3e. process_list rows (SOP-META §4.2 order — before SOP promotion)

Proposed **one umbrella + three specialty** rows under Data / System Owner:

| process_id | Title | Owner | Paired SOP (forward in same or follow commit) |
|:---|:---|:---|:---|
| `hol_data_dtp_supabase_eg5_registry_001` | Supabase EG-5 registry maintenance (umbrella) | System Owner | `SOP-SUPABASE_EG5_REGISTRY_MAINTENANCE_001.md` (mint at P5) |
| `hol_data_dtp_supabase_auth_registry_001` | Supabase Auth registry maintenance | System Owner | section in umbrella SOP |
| `hol_data_dtp_supabase_realtime_registry_001` | Supabase Realtime publication maintenance | System Owner | section in umbrella SOP |
| `hol_data_dtp_supabase_storage_registry_001` | Supabase Storage bucket/path maintenance | System Owner | section in umbrella SOP |

**Note:** Canonical CSV rows may land in the same commit as process rows per SOP-META when the process describes the registry being minted (I95 EG-3 precedent).

### 3f. Optional DDL (operator SQL gate — **not** blocking registry mint)

| Artifact | Posture |
|:---|:---|
| Realtime `ALTER PUBLICATION` migration | **APPLIED 2026-06-14** — `20260613150000_i99_realtime_publication_i96_i62.sql` on MasterData; MCP verified publication + REPLICA IDENTITY FULL |
| Storage bucket `INSERT` + RLS policies | **scheduled** — apply after registry mint; rows SUPA-ST-22 |
| Auth hook migration / retire | **M2** — document in SUPA-AUTH-11/12; not P5 blocker |

Registry mint **does not require** hosted DDL apply — two-plane discipline: git SSOT first, then operator apply.

---

## 4. Risks and mitigations

| Risk | Mitigation |
|:---|:---|
| Canonical CSV gate without operator read | This packet + AskQuestion before any vault write |
| SOP missing at mint | Mint umbrella SOP stub or full SOP in same commit (I95 precedent) |
| Hosted drift vs publication DDL | RT-01 row marks `drift`; reconcile at SQL gate |
| KiRBe embedding DDL in AKOS | MOD-07 `reference-only` — platform partial only |
| Neo4j duplicate registry | No Neo4j rows in Supabase registries — ST-27 link only |

---

## 5. Verification matrix (post-commit)

```powershell
py scripts/validate_supabase_auth_registry.py
py scripts/validate_supabase_realtime_registry.py
py scripts/validate_supabase_storage_registry.py
py scripts/validate_supabase_module_registry.py
py scripts/validate_hlk.py
py scripts/validate_initiative_registry_frontmatter_sync.py
py scripts/verify.py pre_commit_fast
```

---

## 6. Inline-ratify options (operator gate)

### Option A — Mint full tranche now (Recommended)

Promote all three draft CSVs, flip all eight module rows, add validators + governance registry rows, reconcile `DATA_ARCHITECTURE.md` §9, add process_list rows + umbrella SOP. **DDL apply remains a separate operator SQL gate.**

**Tradeoff:** Largest single canonical commit; requires ~45 min execution seat time. **Benefit:** Closes critical SUPA-MOD-22 hole; unblocks I96 B2.4 Realtime wiring spec against canonical rows.

### Option B — Mint registries only; defer five non-EG-5 module flips

Mint Auth + Realtime + Storage CSVs and flip MOD-21/22/23 only. Leave MOD-07/12/17/20/26 ungoverned for P5b.

**Tradeoff:** Violates **D-IH-99-D** operator ratification. **Benefit:** Smaller diff if time-boxed.

### Option C — Registry mint without §9 vault touch

Same as A but skip `DATA_ARCHITECTURE.md` edit; track §9 reconcile as carryover.

**Tradeoff:** Leaves documented doctrine drift (BI active vs §9 non-goal). **Not recommended** — contradicts **D-IH-99-I** scheduled posture.

### Option D — Hold mint; evidence packet only

No vault writes; continue I96 B2 product work first.

**Tradeoff:** I96 BFF continues binding to wip drafts, not canonical paths.

---

## 7. Recommended default

**Option A** — full tranche per operator selection and **D-IH-99-D** / **D-IH-99-I**. Registry mint and §9 reconcile are low-risk, high-signal; DDL stays gated.

---

## Cross-references

- Multi-store alignment: [`multi-store-data-plane-alignment-2026-06-13.md`](multi-store-data-plane-alignment-2026-06-13.md) (**D-IH-99-I**)
- Implementation order: [`implementation-spec-2026-06-13.md`](implementation-spec-2026-06-13.md)
- Master roadmap P5: [`../master-roadmap.md`](../master-roadmap.md)
- Operator SQL gate: [`../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
- Pending decision: **D-IH-99-J** (P5 canonical mint ratification)
