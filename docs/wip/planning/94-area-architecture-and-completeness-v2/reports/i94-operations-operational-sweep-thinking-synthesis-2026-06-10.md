---
parent_initiative: INIT-OPENCLAW_AKOS-94
authored: 2026-06-10
source: thinking-seat c4097ca4
status: ratified-input
linked_decisions:
  - D-IH-94-A
ratifying_decisions:
  - D-IH-94-A
linked_canonicals:
  - ../../../references/hlk/v3.0/Admin/O5-1/People/canonicals/AREA_GOVERNANCE_DISCIPLINE.md
  - ../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md
cross_links:
  - ../95-canonical-articulation-model/i95-initiative-cluster-map.md
  - ../95-canonical-articulation-model/reports/i95-pmo-status-sweep-2026-06-10.md
---

# I94 Operations operational sweep — thinking-seat synthesis

> **Durable SSOT** for executor packets. The operational sweep charter, research
> synthesis, and P1 doctrine mints MUST cite this file as upstream authority.
> Readonly thinking seat (`c4097ca4`); ratified by operator 2026-06-10.

Mode: Readonly planner (no files minted, no commit). Burndown rank 5 in the
[cluster map](../95-canonical-articulation-model/i95-initiative-cluster-map.md)
is **I94 P3 Operations PMBOK reframe** — this sweep is the design + research +
charter tranche that must precede canonical CSV edits.

## Step 0 — Operator actions & CI

### Terminal 16 (post-push)

| Field | Value |
|:---|:---|
| Command | `py scripts/sync_compliance_mirrors_from_csv.py` |
| Exit | 0 (success) |
| Output | Long stream of INSERT … ON CONFLICT … `component_service_matrix_mirror` upserts (I93 P5b/c BI components: Sentry, Analytics Buckets, GA4, Meta Business Manager), ending in COMMIT |

Plain language: After push, you regenerated compliance mirror DML for the
component/service matrix — git SSOT → SQL batches for operator apply via the
Holistika two-plane mirror gate. No errors.

### GitHub Actions (main, last ~10 runs)

| Workflow | Latest | Verdict |
|:---|:---|:---:|
| pre-commit-fast | Run 27241907607 — docs(i95): PMO status sweep post-tranche-6 | PASS (~1m12s) |
| supabase-mirror-sync | Same push 27241907620 | PASS (~5m) |
| neo4j-aura-keepalive | Scheduled 27190189096 (2026-06-09) | PASS |
| neo4j-aura-keepalive | Manual dispatches 2026-06-08 | FAIL (3 runs — pre-F6 auth fix era) |

Note: pre-commit-fast shows a Node 20 deprecation annotation only — not a gate failure.

## Step 1 — Operational lens synthesis

### Cluster position (I95 burndown rank 5)

Operations is next after Tranches 1–6 closed (INDEX_INTEGRITY, I91 matrix, L3
Bundle C, EG-3, OPS-95-2). I94 P3 is the unlock: PMBOK delivery-capacity
reframe + IntelligenceOps eviction (research-application, not delivery).

Cross-link: [I95 PMO status sweep 2026-06-10](../95-canonical-articulation-model/reports/i95-pmo-status-sweep-2026-06-10.md).

### Area completeness (live, 2026-06-10)

`py scripts/validate_area_completeness.py --matrix`

| Metric | Operations |
|:---|:---|
| Kind | delivery_capacity (Think Big, COO) |
| Score | 70% |
| crit@L3 | 9/10 — INCOMPLETE |
| Blocking critical | AREA-03 — no area-level discipline/governance canonical |

Worklist (`--area Operations --next`):

- AREA-03 (CRIT, L0→L3) — mint delivery doctrine
- AREA-11 (enh) — cursor rule + skill pair
- AREA-13 (enh) — area README.md
- AREA-16 (enh) — orphan subfolders Engagement, IntelligenceOps

Partials (not blocking tier alone but ops-critical):

- AREA-09: paired SOP+runbook 0/46 processes
- AREA-12: no discipline canonical for Quality Fabric cross-check
- AREA-16: sub-folder=role match 3/5

Compare to Data (I93 closed): 90%, crit@L3 10/10 COMPLETE — Operations needs
the same operational rigor, not just registry rows.

### DO vs REGISTER (binding lens)

| Class | What Operations must **do** (execute) | What it **registers** (govern) |
|:---|:---|:---|
| PMO | Initiative/program cadence, WIP/inbox renders, vault promotion, adviser plane routing | INITIATIVE_REGISTRY anchors, program portfolio SSOT, cohesion routing |
| RevOps | Engagement scaffolding, template promotion, QBR, cross-area revenue spine | REVOPS_* adapters, REVOPS_PROCESS_CATALOG.yaml, billing bridges |
| SMO | Service catalog + SLA operational rhythm | SERVICE_CATALOG.csv, SLA_MATRIX |
| Engagement | Discovery → proposal → estimation → delivery SOPs | Engagement templates, handoffs to People/Finance |
| IntelligenceOps | **Misplaced** — DO moves to Research | Counterparty/reliability SOPs belong under Research/Intelligence, not delivery |

Operator intent encoded: Other areas govern their domains; Operations runs the
delivery spine so solo operator + AIC don't touch mechanics. That implies
executable process catalog density (SOP + runbook + cadence), not more strategy
markdown under PMO.

### Cross-initiative wiring

| Initiative | Operations implication |
|:---|:---|
| I94 P3 | PMBOK 7 domains as maturity spine; project/service = tag; evict IntelligenceOps |
| I88 | Cross-area ops wiring — Operations gets full 10-pillar ReOps review (Finance was deep example) |
| I89 | ERP persona rollup panels consume OPERATIONAL_COHESION_DOCTRINE routing |
| I86 | Cluster burndown; wave-close regression cadence applies at Operations closure |
| I92 | ERP reassess stub — Operations surfaces feed store-coverage / mission-control gaps |
| I95 L6 | PMO/canonicals/business-strategy/* re-home overlaps Marketing/Finance placement |
| I93 pattern | Mirror emit, component matrix, validators — Operations inherits execution hooks, not re-inventing Data governance |

## Step 2 — Canonical inventory (Operations tree)

63 files under `docs/references/hlk/v3.0/Admin/O5-1/Operations/`. Condensed inventory:

| Asset | Classification | Gap | Ops implication |
|:---|:---|:---|:---|
| PMO/canonicals/OPERATIONAL_COHESION_DOCTRINE.md | Canonical doctrine | Strong on routing; weak on execution | Names AKOS vs ERP vs render vs runtime — needs PMBOK domain map |
| PMO/canonicals/HLK_ERP_ARCHITECTURE.md | Canonical | ERP panels mostly forward-charter | Operations consumes I89/I92 delivery |
| PMO/canonicals/WORKSPACE_BLUEPRINT_HOLISTIKA.md | Canonical | — | Engagement folder DO pattern |
| PMO/canonicals/business-strategy/* (10+ files) | Canonical but misplaced | I95 L6 / AREA-15 | Register strategy; execute elsewhere |
| RevOps/canonicals/REVOPS_AREA_CHARTER.md | Sub-area charter | RevOps only — no Operations root charter | AREA-02 partial at sub-area level |
| RevOps/canonicals/REVOPS_PROCESS_CATALOG.yaml | Canonical catalog | Many entries scaffold; runbook pointers thin | Executable catalog spine exists, pairing cliff |
| RevOps/canonicals/dimensions/*_ADAPTER_REGISTRY.csv | Canonical dimensions | Status metadata present | Cross-area handoff contracts |
| SMO/canonicals/SERVICE_CATALOG.csv, SLA_MATRIX | Canonical | Thin automation | Service DO loop under-specified |
| Engagement/** SOPs | Canonical SOPs | Subfolder orphan (AREA-16) | Client delivery DO |
| IntelligenceOps/SOP-IO_* | Canonical SOPs | Wrong area + orphan folder | Evict to Research; stop scoring as Operations delivery |
| PMO/SOP-* (10+ root SOPs) | SOP | 0/46 paired runbooks in scorer | Biggest automation gap |
| process_list.csv (~76 Operations rows) | Canonical SSOT | Many without SOP/runbook linkage | Registry rich, execution poor |
| scripts/render_wip_dashboard.py, render_operator_inbox.py, render_operational_cohesion_index.py | Mirrored automation | Not unified in ops catalog | Already almost automate PMO loops |
| scripts/sync_compliance_mirrors_from_csv.py | Runbook | Operator-gated apply | Data handoff — Operations triggers, Data owns schema |
| .github/workflows/neo4j-aura-keepalive.yml | Derived CI | Was failing pre-F6 | Graph ops hook for I91/I95 |
| Trello JSON imports under PMO/imports/ | Reference | — | Not operational SSOT |

Existing automation hooks (reuse, don't fork):

- PMO: `render_wip_dashboard`, `render_operator_inbox`, `render_operational_cohesion_index`
- RevOps: `revops_dispatch.py`, `scaffold_engagement.py` (per catalog)
- Cluster: `validate_area_completeness.py`, `verify.py pre_commit_fast`, mirror emit profile
- Holistika: `stripe_audit_metadata.py`, `pmo_program_anchor_backfill.py`

## Step 3 — Research bar (executor must mint)

This thinking seat did not mint ledgers (readonly). Reuse + extend:

| Source pack | Rows | Reuse for Operations |
|:---|:---:|:---|
| I94 area-completeness doctrine | 131 (55 int + 76 ext) | PMBOK/ITIL/bounded-context — Round 3 Q-OPS |
| I88 Finance research | 100+ | Executable catalog + FINOPS handoff pattern |
| I93 Data closure | extensive | Area buildout + mirror discipline template |
| Operations vault + scripts + planning grep | target ≥120 internal | New ledger rows |
| PMBOK 7/8, ITIL 4 SVS, solo-founder ops, AIOps, ERP ops | target ≥120 external | New ledger rows |

Mint paths (executor):

- `docs/wip/planning/94-area-architecture-and-completeness-v2/reports/i94-operations-area-source-ledger.csv`
- `…/i94-operations-area-research-synthesis-2026-06-10.md`
- `…/i94-operations-operational-sweep-charter-2026-06-10.md` (the plan)
- `…/i94-p3-session-doctrine-2026-06-10.md`

Validators: `validate_research_action.py` PASS on ledger; `validate_hlk.py` after any canonical touch.

## Step 4 — Charter design (mint spec for executor)

### 16-component matrix — current vs target

| Component | Now | Target (Operations COMPLETE tier) | Primary deliverable |
|:---|:---|:---|:---|
| AREA-01 Parent redesign | pass | hold | — |
| AREA-02 Area charter | partial (RevOps only) | L3 | OPERATIONS_AREA_CHARTER.md |
| AREA-03 Discipline charters | gap | L3 | OPERATIONS_DELIVERY_DOCTRINE.md (PMBOK 7 domains) |
| AREA-04 Process list | pass | hold | 76 rows — trim/migrate IntelligenceOps processes |
| AREA-05 Baseline roles | pass | hold | COO, PMO, RevOps sub-areas |
| AREA-06 Capability/confidence | partial | L3 | Ops capability rows in registry |
| AREA-07 PRECEDENCE | pass | hold | — |
| AREA-08 Dimension registries | partial | L3 | Adapter + service registries wired |
| AREA-09 Paired SOP+runbook | partial 0/46 | L2+ (enhancing) | Tranched pairing — top 12 critical processes first |
| AREA-10 Mirrors | skip | skip | Conservative — operator SQL gate |
| AREA-11 Rule+skill | gap | L2 | akos-operations-delivery.mdc + operations-delivery-craft |
| AREA-12 Quality Fabric | partial | L3 | Doctrine cites compose_* + ERP surfaces |
| AREA-13 README | gap | L2 | Operations/README.md |
| AREA-14 Kind+entity | pass | hold | delivery_capacity / Think Big |
| AREA-15 Placement integrity | partial | L3 | Evict IntelligenceOps; L6 biz-strategy tracker |
| AREA-16 File plan | partial | L2 | Rename/relocate orphans; FK subfolders to roster |

Tier gate: crit@L3 10/10 — unblock is AREA-03 (+ charter README/rule for completeness).

### Phased execution (charter body)

| Phase | Scope | Automates vs human-gated |
|:---|:---|:---|
| P0 Research | ≥120+120 ledger + synthesis + charter + session doctrine | Human: scope ratification only |
| P1 Doctrine mint | Operations area charter + PMBOK delivery doctrine + README + rule/skill | Human: doctrine review (D-IH-94-C) |
| P2 Executable catalog T1 | Pair top 12 processes (PMO inbox/WIP, cohesion review, initiative anchors, external adviser, engagement scaffold, mirror emit trigger, area completeness sweep) | Automate: runbooks in verify.py; Gate: CSV rows if new item_ids |
| P3 Placement | IntelligenceOps → Research; Engagement subfolder FK; biz-strategy forward tracker (I95 L6) | Hard gate: file moves + operator approval |
| P4 Cross-area handoffs | Document+wire: Data mirror, People compliance, Finance FINOPS, Tech Envoy/CICD | Mostly register; execution via existing scripts |
| P5 I88 deep slice | Operations 10-pillar wiring review report | Scheduled + on_demand cadence |
| P6 Regression + UAT slice | --matrix crit@L3 10/10; synthesis-before-tranche; optional PASS-WITH-FOLLOWUP on AREA-09 cliff | validate_area_completeness.py, validate_hlk.py, verify.py pre_commit_fast |

### Architecture (Operations as delivery spine)

| Register layer | Execute layer | Operator surfaces |
|:---|:---|:---|
| process_list.csv | RevOps + SMO registries | Operational Cohesion Doctrine |
| render wip + inbox + cohesion | revops_dispatch + scaffold | compliance_mirror_emit |
| validate_area_completeness | AKOS markdown | hlk-erp panels I89 |
| OpenClaw dashboard | | |

## Top 10 operational gaps (priority order)

1. No Operations root delivery doctrine (AREA-03) — blocks crit@L3 tier
2. 0/46 SOP+runbook pairs — registry without executable catalog
3. IntelligenceOps in Operations tree — wrong bounded context (I94 P3)
4. No Operations/README.md — operator navigation gap
5. No Operations cursor rule+skill — agents improvise ops mechanics
6. Engagement subfolder orphan — AREA-16 RACI drift
7. business-strategy under PMO — placement debt (I95 L6)
8. RevOps catalog mostly scaffold — value-mapping spine not operationalized
9. ERP execution surfaces forward-charter — Operations doctrine references panels not live
10. Mirror parity lag — git correct, Supabase apply operator-dependent (OPS-95-2 pattern)

## Ratification record

Pre-digested evidence supports three scope forks. **Operator ratified 2026-06-10:**

| Question | Ratified option | Binding label |
|:---|:---|:---|
| **Q1 — Scope** | **B** | **Full sweep** — P0–P6 including 12-process pairing + I88 Ops slice + placement moves (~2–3 week calendar) |
| **Q2 — Priority** | **automation-first** | Inbox/WIP/cohesion/mirror loops hands-off first in pairing tranche |
| **Q3 — Capacity** | **6–8h/day until GTM** | Substantive execution capacity; not design-only |

Executor packets MUST honour Q1=B + automation-first + 6–8h/day capacity when
scoping P2 pairing and P3 placement gates.

## Executor packet order (from thinking seat)

1. **i94-ops-P0-research** — Mint ≥120+120 source ledger, synthesis, operational-sweep charter, session doctrine; `validate_research_action` PASS
2. **i94-ops-P1-doctrine** — Operations area charter + PMBOK delivery doctrine + README + akos-operations-delivery rule/skill
3. **i94-ops-P2-exec-catalog-T1** — Pair 12 critical SOP+runbook processes
4. **i94-ops-P3-placement** — IntelligenceOps eviction + Engagement subfolder FK (file-move gate)
5. **i94-ops-P4-verify** — `validate_area_completeness` crit@L3 10/10; `validate_hlk`; `pre_commit_fast`

Hard gates: operator scope ratification (Q1) before P2 CSV or file moves.

=== OPUS DONE -> SWITCH TO COMPOSER ===
