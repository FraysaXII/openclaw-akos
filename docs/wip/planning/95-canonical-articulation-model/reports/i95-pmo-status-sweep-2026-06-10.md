---
report_type: pmo-status-sweep
parent_initiative: INIT-OPENCLAW_AKOS-95
authored: 2026-06-10
authored_by: Execution seat (Composer)
audience: J-OP
status: active
ratifying_decisions:
  - D-IH-95-M
  - D-IH-95-G
  - D-IH-73-D
linked_runbooks:
  - scripts/validate_hlk.py
  - scripts/verify.py
  - scripts/neo4j_connectivity_probe.py
---

# I95 PMO status sweep — 2026-06-10 (post-tranche-6)

**Initiative:** INIT-OPENCLAW_AKOS-95 — the **Canonical Articulation Model** (HCAM enterprise ontology + governed Neo4j graph over CSV SSOT)  
**Sweep scope:** Tranches 1–6 outcomes (2026-06-10 cluster burndown wave) + refreshed master queue  
**Cluster map SSOT:** [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md)  
**Prior sweep:** [`i95-pmo-status-sweep-2026-06-09.md`](i95-pmo-status-sweep-2026-06-09.md)

---

## 1. Where we are

| Surface | Status | Plain language |
|:---|:---|:---|
| **P95-GOV wave** | **Closed** (PASS) | Universal canonical governance registry + Plane-1 hardening + mirror emit contract |
| **Neo4j graph harness** | **PASS** (F6 closed) | Instance `6c0d76bf`; dual-emit sync + CQ UAT PASS |
| **L3 FK→verb tranches** | **Bindings complete** | Bundles A+B+C done; 44 L3 bindings; TRP-030/036 stay **planned** |
| **L1 Supabase EG-2 + EG-3** | **Done** | API exposure doc + edge-fn / cron / extension registries minted 2026-06-10 |
| **OPS-95-2 engagement backfill** | **Done** (Tranche 6) | 6/7 `engagement_model_id` populated; archived Rushly NULL intentional |
| **I95 initiative** | **Active** | ~**62%** engineering complete (see §3); HCAM P3–P7 + L4–L6 lanes open |

**Validator bar this sweep:** `py scripts/validate_hlk.py` **OVERALL PASS**; `py scripts/verify.py pre_commit_fast` **PASS** (post OPS-95-2 CSV apply).

---

## 2. Tranche outcomes (1–6)

| Tranche | Rank | Functional scope | Verdict | Evidence |
|:---:|:---:|:---|:---:|:---|
| **T1** | — | Pre-burndown baseline (GOV close + full regression 2026-06-09) | **PASS-WITH-FOLLOWUP** | [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md) |
| **T2** | **1** | INDEX_INTEGRITY Wave N — planning README + INITIATIVE_DEPENDENCIES I90–I95 edges | **DONE** | [`i95-tranche2-session-doctrine-2026-06-10.md`](i95-tranche2-session-doctrine-2026-06-10.md); sweep `index-sweep-2026-06-10-tranche2-wave-n.md` |
| **T3** | **2** | I91 P1–P2 — Neo4j preflight + store-coverage matrix v1 | **DONE** | [`i95-tranche3-session-doctrine-2026-06-10.md`](i95-tranche3-session-doctrine-2026-06-10.md); [`store-coverage-matrix-2026-06-10.md`](../../91-enterprise-graph-store-coverage/reports/store-coverage-matrix-2026-06-10.md) |
| **T4** | **3** | I95 L3 Bundle C — TRP-030/036 charter disposition (keep planned) | **DONE** | [`i95-tranche4-session-doctrine-2026-06-10.md`](i95-tranche4-session-doctrine-2026-06-10.md); [`i95-l3-bundle-c-disposition-2026-06-10.md`](i95-l3-bundle-c-disposition-2026-06-10.md) |
| **T5** | **3b** | I95 L1 EG-3 — edge-fn / cron / extension registries + validators | **DONE** | [`i95-tranche5-session-doctrine-2026-06-10.md`](i95-tranche5-session-doctrine-2026-06-10.md); D-IH-95-G |
| **T6** | **4** | OPS-95-2 — `engagement_model_id` backfill (7 engagements) | **DONE** | [`i95-tranche6-session-doctrine-2026-06-10.md`](i95-tranche6-session-doctrine-2026-06-10.md); [`i95-ops95-2-proposals.csv`](i95-ops95-2-proposals.csv) |

### OPS-95-2 mapping summary (operator-ratified)

| Engagement | `engagement_model_id` | `status` |
|:---|:---|:---|
| SUEZ × WeBuy | `eng_model_milestone_consultant` | active |
| EFA cobranding | `eng_model_percentage_collaborator` | active |
| Asesoría Hostelería | `eng_model_milestone_consultant` | active |
| ShadowGPU advisory | `eng_model_outsourced_helper` | active |
| Internal SMO SSOT | `eng_model_operator_self` | active |
| Websitz Shopify | `eng_model_percentage_collaborator` | active |
| Websitz Rushly (archived) | **NULL** (intentional) | archived |

**Operator follow-up:** mirror re-emit for `engagement_registry_mirror` per [`holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md) (two-plane doctrine; not blocking git SSOT).

---

## 3. I95 % complete estimate

Weighted by master-roadmap lanes + cluster burndown (not calendar time):

| Lane family | Weight | Done | Notes |
|:---|:---:|:---:|:---|
| P0 research + P1 relationship SSOT | 15% | **100%** | Core validators wired |
| P2 Neo4j + CQ harness (F6) | 15% | **100%** | Instance live |
| P95-GOV universal governance | 10% | **100%** | PASS-WITH-FOLLOWUP closed |
| L2 capability de-densify | 5% | **100%** | D-IH-95-I |
| L3 FK→verb (bindings) | 10% | **100%** | 44 bindings; TRP-030/036 deferred |
| L1 Supabase EG-2..3 | 8% | **50%** | EG-2+3 done; EG-4..5 open |
| Cluster tranches T2–T6 (burndown 1–4) | 12% | **100%** | This sweep wave |
| P3 HCAM doctrine + Semantic Council | 10% | **0%** | Open |
| P4 area-completeness v3 | 8% | **0%** | Depends I94 |
| P5 repo-wide FK→verb (residual) | 5% | **30%** | 10 unbound active triples (F-11) |
| P6 lead simplification | 4% | **0%** | Canonical gate Q2 |
| L4 orphan burn-down | 4% | **0%** | `--matrix` open |
| L5 Topics + IntelligenceOps | 3% | **0%** | T1 schema tranche |
| L6 biz-strategy re-home | 3% | **0%** | I94 P7 overlap |
| P7 closure UAT | 5% | **0%** | 5 competency questions |

**Composite engineering estimate: ~62%** (governance + graph spine + L3/L1 partial + burndown wave done; doctrine home + closure + L4–L6 remain).

---

## 4. Master execution queue (updated burndown)

Authoritative ranked queue: [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md) §Burndown.

| Rank | Work item | Primary INIT | Exit gate | Status |
|:---:|:---|:---|:---|:---:|
| **1** | ~~INDEX_INTEGRITY Wave N~~ | I86 / I90 | Sweep drift 0 | **DONE** T2 |
| **2** | ~~I91 P1–P2 Neo4j + matrix~~ | I91 | Probe exit 0 + matrix v1 | **DONE** T3 |
| **3** | ~~L3 Bundle C TRP-030/036~~ | I95 | Charter disposition logged | **DONE** T4 |
| **3b** | ~~L1 EG-3 registries~~ | I95 | 3 registries + validators | **DONE** T5 |
| **4** | ~~OPS-95-2 engagement_model_id~~ | I95 | `validate_hlk.py` PASS + OPS closed | **DONE** T6 |
| **5** | **I94 P3** Operations PMBOK reframe | I94 | Doctrine section + IntelligenceOps eviction plan | **NEXT** |
| **6** | **I95 L4** equal-slice orphan burn-down | I95 | `--matrix` wiring % up | Open |
| **7** | **I92 P0** full charter (ERP reassess) | I92 | Replaces stub; links I91 matrix | Open |
| **8** | **Self-hosted spike charter** + EIC screen | I95 funding | TCO documented; no engineering block | Open |
| **9** | **`py scripts/verify.py pre_commit`** full bar | All | Release readiness | Open |

**Regression deltas (tracked, non-blocking):**

- **OPS-95-3** — I95 `files-modified.csv` historical backfill (~40 commits 2026-06-05..09)
- **L3 tranche-5** — 10 active relationship triples still without FK bindings (F-11)
- **Mirror re-emit** — engagement_registry_mirror after OPS-95-2 (operator SQL gate)
- **EG-4..5** — remaining L1 Supabase registry family

---

## 5. Cross-initiative next actions

| Initiative | Next action | Why it unlocks |
|:---|:---|:---|
| **I94** | P3 Operations PMBOK reframe | Burndown rank 5; eviction plan for IntelligenceOps from Operations area |
| **I92** | P0 full charter expansion | ERP dashboard consumes I91 store-coverage matrix |
| **I91** | Maintain matrix freshness | Neo4j + Supabase store posture as I95 articulation consumes |
| **I88** | P1–P3 discipline canonical | Cross-area wiring lens for L4 orphan burn-down |
| **I89** | P1–P5 TSX panels (sibling `hlk-erp`) | Audience/register semantics from I95 GOV |
| **I86** | Wave cadence only | Portfolio coordinator; INDEX_INTEGRITY path cleared |
| **I95** | L4 one-area orphan slice + P3 HCAM doctrine | Largest remaining engineering surface |

---

## 6. What you do this week (operator)

1. **Optional — mirror parity (~10 min):** after OPS-95-2, re-emit + apply `engagement_registry_mirror` when convenient (git SSOT already correct).

2. **Burndown rank 5 — I94 P3 kickoff:** skim Operations PMBOK reframe scope in I94 master-roadmap; no CSV gate unless charter mints new process rows.

3. **Funding parallel (~20 min):** EIC Pre-Accelerator eligibility screen (unchanged from 2026-06-09 sweep).

4. **Fast gate after local edits:**

```powershell
cd "$env:USERPROFILE\cd_shadow\openclaw-akos"
py scripts/verify.py pre_commit_fast
```

---

## 7. Cross-references

- **Cluster map (burndown SSOT):** [`i95-initiative-cluster-map.md`](../i95-initiative-cluster-map.md)
- **OPS-95-2 research:** [`i95-p0-research-ops95-2-engagement-backfill-2026-06-10.md`](i95-p0-research-ops95-2-engagement-backfill-2026-06-10.md)
- **Full regression:** [`i95-full-regression-2026-06-09.md`](i95-full-regression-2026-06-09.md)
- **Master roadmap:** [`master-roadmap.md`](../master-roadmap.md)
- **Official deps:** [`INITIATIVE_DEPENDENCIES.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_DEPENDENCIES.md)
