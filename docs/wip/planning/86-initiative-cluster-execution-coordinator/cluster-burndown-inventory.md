---
intellectual_kind: cluster_inventory
parent_initiative: INIT-OPENCLAW_AKOS-86
sharing_label: internal_only
authored: 2026-05-19
last_review: 2026-05-19
linked_decisions:
  - D-IH-86-O  # Option 5 default posture
  - D-IH-86-T  # cluster burndown plan ratification (will be minted by B-G3b)
purpose: anchored evidence for B-G3b cluster burndown plan authoring
language: en
status: active
role_owner: System Owner
co_owner_role: PMO
---

# I86 cluster — burndown inventory (B-G3a anchored evidence)

## 1. Purpose

This document captures the comprehensive remaining-work inventory in the [I86 cluster](master-roadmap.md) as of 2026-05-19, immediately after [Wave G commit `893c486`](https://github.com/FraysaXII/openclaw-akos/commit/893c486) (D-IH-86-R + D-IH-86-S closure of Strands 3b + 4 follow-ups from Wave F). It exists so the B-G3b authoring pass (cluster burndown plan, ~11 sections to plan-quality bar) has **anchored evidence** rather than re-reading 14 source files. Single source-of-truth inventory: every other cluster-coordination planning artifact should defer here for the "what's left" answer.

## 2. Comprehensive inventory table

Total: 17 items (5 active initiatives + 3 blocker-tracked candidates + 9 open OPS rows).

### 2.1 Active initiatives

| Item ID | Type | Current status | Owner role | Co-owner | Effort (d) | Dependencies | Closure criteria | Operator-gate requirements |
|:---|:---|:---|:---|:---|:---:|:---|:---|:---|
| **[I76](../76-madeira-elevation/master-roadmap.md)** | initiative | active; P0 closed 2026-05-18 (`D-IH-76-A`); P1..P6 pending | System Owner | PMO | 10-15d | I84 P4 (closed; AICs F5 inherited via `D-IH-84-C`); I86 (parent orchestrator); I79 (People-DoD doctrine); scope-overlap-tracker for I11/I13/I17 governs consolidation at P1/P3/P4 entries | All 6 phases land per shape table; 5-mode parity SOPs (Ask/Plan/Agent/Debug/Methodology) + tool catalog + per-mode RBAC + AICs F5 dispatcher + 5-engagement UAT; D-IH-76-CLOSURE minted; I11/I13/I17 consolidation gates closed (or forward-chartered to I76b) | **MANDATORY canonical-CSV pause at P4** (`MADEIRA_AIC_PER_TASK_REGISTRY` mint; per `OPS-76-1` notes); inline-ratify gates at P1/P3/P4 scope-overlap entries; standard inline-ratify at closure |
| **[I78](../78-brand-voice-llm-as-judge/master-roadmap.md)** | initiative | active; P0 done 2026-05-14; P1 engineering pending; activated `D-IH-78-A` 2026-05-17 | Brand & Narrative Manager | (none) | 3-5d (P1 only; strict-mode promotion deferred) | I71 closed (deterministic Pack A1 + Vale floor); bias-audit gate for strict-mode promotion (Strand D) | P1 judge Pydantic chassis + CLI + release-gate INFO advisory wiring landed; strict-mode promotion remains TRIGGER-watch behind bias audit | Standard inline-ratify (no canonical-CSV gates expected at P1) |
| **[I81](../81-vault-integrity-layout-milestones-retrofit/master-roadmap.md)** | initiative | active; P0 closed 2026-05-16 (`D-IH-81-A`..E + H); P1..P9 pending (absorbed mode) | PMO | System Owner | 10-25d (absorbed across waves) | I85 P1 (closed; provides `audience_tags_coverage` column for P1 matrix); blocks I82 P2 via `kb-integrity-matrix-<date>.csv`; cross-repo coordination with `hlk-erp` for P2 layout tranches | All 10 phases land per shape table; vault-integrity matrix PASS ≥ 95% on `process_list → SOP → addendum → runbook → KNOWLEDGE_PAIRING → mirror` chain; legacy Compliance canonicals migrated to I22 forward layout; ~40 SOPs body/addendum retrofit; `validate_planning_cross_refs.py` GREEN | **MANDATORY canonical-CSV operator pause per tranche at P2** (layout migration; `D-IH-81-G`); standard inline-ratify at P1/P3 closes; per-pair author sign-off at P4-P8 retrofits; operator approval at P9 closure |
| **[I82](../82-holistika-capability-doctrine/master-roadmap.md)** | initiative | active; P0 charter in_progress (`D-IH-82-A`..F/G/H); P0 doctrine mint planned; P1..P7 pending | PMO | Brand & Narrative Manager | 7-10d | I81 P1 `kb-integrity-matrix` (gates P2; OR `D-IH-82-PREREQ` waiver); I85 P1 `AUDIENCE_REGISTRY` (closed; consumed at P5); I66 `BRAND_BASELINE_REALITY_MATRIX` (consumed at P5); blocks I83 promotion via P4 `USE_CASE_ARCHIVE` mint | All 7 phases land; `HOLISTIKA_CAPABILITY_DOCTRINE.md` paired body+addendum at `status: active`; Talent activated in `baseline_organisation.csv`; 3 capability registers minted (`CAPABILITY_REGISTRY` + `CAPABILITY_CONFIDENCE_REGISTRY` + `USE_CASE_ARCHIVE`); BBR matrix §N capability-messaging extension; ≥ 1 live UAT rehearsal OR explicit waiver | **MANDATORY canonical-CSV pause at P1** (Talent activation in `baseline_organisation.csv`); **MANDATORY canonical-CSV pause at P2** (`CAPABILITY_REGISTRY` mint); operator approval at P3/P4/P7 |
| **[I89](../89-hlk-erp-program-rollup-implementation/master-roadmap.md)** | initiative | active; P0 in_progress (`D-IH-89-A`..E ratified 2026-05-17); P1..P5 pending | PMO | System Owner; Brand & Narrative Manager | 15-25d (~3-5 calendar weeks; cross-repo) | I86 P3 data layer (closed; `governance.initiative_program_rollup_view` shipped); I66 BBR matrix (consumed at P3); `OPS-86-5` ADVOPS triage (closed 2026-05-18; un-blocks BBR gate state) | All 6 routes ship in sibling `hlk-erp` repo (5 internal + Adviser-external REDACTED); RLS policies + JWT claims for 6 personas; redaction matrix at TS layer; Adviser-external PDF export pipeline; `D-IH-89-CLOSURE` + browser-smoke evidence | **MANDATORY public-prose pauses at P3 + P4** (Adviser-external panel + PDF export; per `akos-agent-checkpoint-discipline.mdc`); BBR drift-gate runs at FAIL from P0 (per `D-IH-89-E`); inline-ratify at P1 §P1.7 RLS policy + P2 §P2.6 component shape + P5 closure |

### 2.2 Blocker-tracked candidates (governance-shape artifacts; not promoted)

| Item ID | Type | Current status | Owner role | Co-owner | Effort (d) | Dependencies (blockers) | Closure criteria | Operator-gate requirements |
|:---|:---|:---|:---|:---|:---:|:---|:---|:---|
| **[BT-I74](../_blockers/i74-promotion-blocker-tracker.md)** | blocker-tracker | active; promotion blocked | PMO | System Owner | 0.1d ongoing review | TRIGGER-2 (≥2 external requests; count=0); I71 closure (PENDING ~80%); I72 closure (candidate); I73 closure (candidate); I76 P3 closure (P1-P3 pending); Founder + Brand Manager approval; HLK Tech Lab capacity | Tracker closes when I74 is promoted active in `INITIATIVE_REGISTRY.csv` (7 conditions §3 all met); promotion via fresh A1-equivalent ratify gate | Quarterly review minimum; promotion gate requires Founder + Brand Manager approval recorded |
| **[BT-I75](../_blockers/i75-promotion-blocker-tracker.md)** | blocker-tracker | active; promotion blocked (most constraint-blocked of Lane 5) | PMO | Research Director (interim Founder) | 0.1d ongoing review | I72 P0 (PENDING); I73 P0 (PENDING); Research Director hire OR founder formally takes role (PENDING — no `baseline_organisation.csv` row activation); Lane 1 promotion (conditional per handoff §2.2) | Tracker closes when I75 is promoted active; 4 conditions §2 all met | Hiring decision may take quarters; Research Director activation requires `baseline_organisation.csv` row (canonical-CSV gate) |
| **[BT-I83](../_blockers/i83-promotion-blocker-tracker.md)** | blocker-tracker | active; promotion blocked (two-stage: I82 P4 then I76 P3) | PMO | System Owner | 0.1d ongoing review | I82 P4 USE_CASE_ARCHIVE mint (not started; I82 ~20%); I76 P3 closure (operator UX SOPs + AICs F5 substrate); Founder approval; HLK Tech Lab capacity | Tracker closes when I83 is promoted active; promotion gated on §2 1-4 met | Founder approval required; capacity assessment post-I76 elevation |

### 2.3 Open OPS rows

| Item ID | Type | Current status | Owner role | Co-owner | Effort (d) | Dependencies | Closure criteria | Operator-gate requirements |
|:---|:---|:---|:---|:---|:---:|:---|:---|:---|
| **OPS-86-1** | OPS row | open; continuous master coordination | PMO | System Owner | ongoing | All 10 cluster siblings status:closed in INITIATIVE_REGISTRY; OPS-86-1 closure decision (future `D-IH-86-CLOSURE`) | Closes when all 10 cluster siblings reach status:closed + `D-IH-86-D` cross-check recorded for each + I86 closure decision minted | Closure ratify gate (operator approval) |
| **OPS-86-3** | OPS row | open; I86 P2 Stage B residual (8 unanchored mirror-reseed rows) | PMO | (none) | ~3d | Operator MasterData `compliance_mirror_emit` run for 8 unanchored INIT rows still tracked as residual operator work per I86 master-roadmap preamble | Closes when 8 unanchored INIT rows seeded with `program_anchors` via mirror-reseed; rollup view returns ≥27 anchored rows | **MANDATORY canonical-CSV operator pause** on `compliance_mirror_emit` apply per `akos-holistika-operations.mdc` two-plane model; pause-record required |
| **OPS-76-1** | OPS row | open; I76 P0..P6 execution coordination | System Owner | (none) | tied to I76 closure | I76 P0..P6 phase execution; consolidation gates at P1/P3/P4 per scope-overlap-tracker §3.1/3.2/3.3 | Closes when `D-IH-76-CLOSURE` mints | **MANDATORY canonical-CSV pause at P4** (`MADEIRA_AIC_PER_TASK_REGISTRY` mint) |
| **OPS-76-2** | OPS row | open; quarterly review cadence for BT-I74 | PMO | (none) | 0.1d/quarter | TRIGGER-2 fire OR I71/I72/I73 closure (whichever later) | Closes when I74 promoted active + tracker archive disposition | Promotion ratify gate when conditions met |
| **OPS-76-3** | OPS row | open; quarterly review cadence for BT-I75 | PMO | (none) | 0.1d/quarter | I72 P0 closure OR I73 P0 closure OR Research Director hire (whichever first) | Closes when I75 promoted active + tracker archive disposition | Promotion ratify gate |
| **OPS-76-4** | OPS row | open; review cadence for BT-I83 | PMO | (none) | 0.1d/trigger | I82 P4 closure ratified (then re-check I76 P3 closure) | Closes when I83 promoted active + tracker archive disposition | Promotion ratify gate |
| **OPS-81-1** | OPS row | open; I81 P1 vault integrity + P2 layout-migration coordination | PMO | (none) | tied to I81 closure | I81 P1+P2+P3 execution; cross-repo `hlk-erp` coordination for layout tranches | Closes at `D-IH-81-CLOSURE` (P9) | **MANDATORY canonical-CSV pause per tranche at P2** |
| **OPS-82-1** | OPS row | open; I82 doctrine + Talent + 3 registries + live UAT | PMO | (none) | tied to I82 closure | I82 P0..P7 execution; live external-stakeholder rehearsal OR waiver | Closes at I82 closure | **MANDATORY canonical-CSV pauses at P1 (Talent) + P2 (`CAPABILITY_REGISTRY`)**; operator approval at P3/P4/P7 |
| **OPS-89-1** | OPS row | open; I89 P0..P5 cross-cutting rollout (tri-co-owned) | PMO | System Owner; Brand & Narrative Manager | tied to I89 closure (~3-5 weeks) | I89 P0..P5 phase execution; sibling-repo `hlk-erp` bless coordination per [`SOP-EXTERNAL_REPO_BLESSING_001.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) | Closes when `D-IH-89-CLOSURE` mints | **MANDATORY public-prose pauses at P3 + P4** (Adviser-external panel + PDF export) |

## 3. Cross-cutting observations

- **Critical-path chain (longest dependency line)**: I76 P3 closure → unblocks BT-I83 (Strand A AICs F5 substrate dependency) AND unblocks BT-I74 (per BT-I74 condition #5 "I76 P3 closure"); separately, I82 P4 `USE_CASE_ARCHIVE` mint → unblocks BT-I83 first-stage (then BT-I83 awaits I76 P3 second-stage). **Closing I76 P3 + I82 P4 jointly unlocks BT-I83 promotion** — highest-leverage milestone for the cluster.
- **Parallel-safe lanes (no dependency conflicts)**: I76, I81, I82, I78, I89 can all advance independently. I81 P1 feeds I82 P2 (soft gate via `D-IH-82-PREREQ` waiver), but I82 can proceed in parallel with waiver or wait for matrix evidence. I89 is downstream of closed I86 P3 and has its own pace (cross-repo bless cadence governs).
- **Canonical-CSV operator-pause concentration**: I76 P4 (`MADEIRA_AIC_PER_TASK_REGISTRY`), I81 P2 (per-tranche layout migration; potentially N tranches), I82 P1 (Talent activation in `baseline_organisation.csv`), I82 P2 (`CAPABILITY_REGISTRY` mint), OPS-86-3 (`compliance_mirror_emit` for 8 unanchored INIT rows). **Total: ≥ 5 mandatory canonical-CSV pause-points** across the active cluster (more if I81 P2 splits into many tranches).
- **MANDATORY public-prose pauses**: I89 P3 (Adviser-external REDACTED panel) + I89 P4 (Adviser-external PDF export). Two MANDATORY pauses concentrated in I89.
- **Ratify-density risk per `akos-agent-checkpoint-discipline.mdc` pause-fatigue avoidance**: I81 has the highest pause-density (P2 layout migration is N-tranche operator gate; absorbed-mode means each per-area retrofit at P4-P8 also has per-pair sign-off). Mitigation: front-load substantive operator review at I81 P1 + P2 wave-1; allow batched approvals for tightly-coupled tranches; soft-pause auto-clear if operator silent ≥ 24h on non-canonical retrofit pairs.
- **Blocker-trackers (BT-I74, BT-I75, BT-I83) are governance-shape artifacts, NOT remaining engineering work**: they require **only** quarterly review cadence (OPS-76-2, OPS-76-3, OPS-76-4 each 0.1d/quarter). Promotion to active is forward work whose cost lands on the promoted initiative's P0 charter, not on the cluster burndown.
- **Closure that unlocks the most downstream work**: **I76 P3 closure** unlocks 2 blocker-trackers (BT-I83 via AICs F5 substrate; BT-I74 via condition #5). Followed by **I82 P4 closure** which unlocks BT-I83 first-stage. Together these two milestones are the **2-of-many leverage points** for shrinking the cluster faster than linear.
- **Cross-repo coordination cost**: I81 P2 (`hlk-erp` consumer paths per layout migration tranche) + I89 (sibling-repo TSX panels + browser smoke). Both require [`SOP-EXTERNAL_REPO_BLESSING_001.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/External%20Repos/SOP-EXTERNAL_REPO_BLESSING_001.md) + [`SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md`](../../references/hlk/v3.0/Admin/O5-1/Envoy%20Tech%20Lab/Cross%20Repo/SOP-CROSS_REPO_SCHEMA_PROPAGATION_001.md) cadence per tranche/commit.
- **I86 itself stays active until cluster burndown completes**: per [I86 master-roadmap](master-roadmap.md) §7 closure criterion (10 siblings closed + OPS-86-1 closed + closure cross-check). I86 P3 effective-closure landed 2026-05-17 but `INITIATIVE_REGISTRY.csv` row keeps `status: active` because operational cluster orchestration continues.
- **I78 is the lightest-touch active sibling**: P0 done; P1 only requires Pydantic chassis + CLI + INFO-advisory wiring. No canonical-CSV gates expected. Could close in a focused 3-5d block if Brand & Narrative Manager prioritises it.
- **Owner-role distribution across remaining work**: PMO owns or co-owns 13 of 17 items (every initiative + 6 of 9 OPS rows); System Owner owns or co-owns 7 (I76 primary; I81 co-owner; I89 co-owner; OPS-86-1 co-owner; OPS-76-1 primary; plus 2 blocker-tracker co-ownerships); Brand & Narrative Manager owns or co-owns 3 (I78 primary; I82 co-owner; I89 co-owner). **PMO bandwidth is the load-bearing constraint** (matches R-IH-86-1 risk). Spotlight roster per `D-IH-86-A` distributes facilitation but does not redistribute INIT-row authority.
- **Validators newly minted in cluster execution**: Wave 1-G shipped at least 6 (`validate_audience_registry.py`, `validate_audience_tags.py`, `validate_openclaw_plugin_pinning.py`, `validate_initiative_program_anchors.py`, `validate_external_render_trail.py`, `validate_locale_orthography.py`). Forward work mints more (`validate_capability_registry.py` + `validate_use_case_archive.py` at I82 P2/P4; `validate_planning_cross_refs.py` at I81 P3). Each new validator must follow [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) §"Python Code Standards" + wire into [`scripts/release-gate.py`](../../../../scripts/release-gate.py) + [`config/verification-profiles.json`](../../../../config/verification-profiles.json) `pre_commit`.
- **Wave G baseline state at this inventory authoring**: working tree clean at commit `893c486`; D-IH-86-R + D-IH-86-S closed Wave F follow-ups; external-render gate flipped to FAIL with strict freshness checks; `validate_locale_orthography.py` runs INFO advisory; 5 of 10 cluster siblings closed per §1.5 (informal accounting; see open question #2).

### 3.1 At-a-glance tally

| Dimension | Count | Notes |
|:---|:---:|:---|
| Active initiatives remaining | 5 | I76, I78, I81, I82, I89 |
| Blocker-tracked candidates | 3 | BT-I74, BT-I75, BT-I83 (governance-shape only) |
| Open OPS rows | 9 | 7 PMO-owned; 1 System Owner-owned (OPS-76-1); 1 tri-co-owned (OPS-89-1) |
| MANDATORY canonical-CSV pause-points (forward) | ≥ 5 | I76 P4; I81 P2 (N-tranche); I82 P1; I82 P2; OPS-86-3 |
| MANDATORY public-prose pause-points (forward) | 2 | I89 P3 + I89 P4 |
| Closures that unlock blocker-tracker promotions | 2 | I76 P3 (unlocks BT-I83 + BT-I74); I82 P4 (unlocks BT-I83 first-stage) |
| Cross-repo coordination cost | 2 | I81 P2 (`hlk-erp` consumer paths); I89 (full `hlk-erp` TSX implementation) |
| Estimated cluster burndown effort (active initiatives only; excludes blocker-tracker review cadence) | 45-75d | Heavily compressible via I81 absorbed-mode parallelism + I78 lightweight close |

## 4. Source files cited

For B-G3b traceability:

1. [`docs/wip/planning/86-initiative-cluster-execution-coordinator/master-roadmap.md`](master-roadmap.md) — I86 charter, sibling table §1.3, Bundle D push status §1.5
2. [`docs/wip/planning/86-initiative-cluster-execution-coordinator/reports/2026-05-19-wave-f-external-render-doctrine-closure.md`](reports/2026-05-19-wave-f-external-render-doctrine-closure.md) — Wave F closure context (5-of-10 cluster siblings closed snapshot)
3. [`docs/wip/planning/76-madeira-elevation/master-roadmap.md`](../76-madeira-elevation/master-roadmap.md) — I76 charter, 7-phase shape, scope-overlap-tracker governance for I11/I13/I17
4. [`docs/wip/planning/81-vault-integrity-layout-milestones-retrofit/master-roadmap.md`](../81-vault-integrity-layout-milestones-retrofit/master-roadmap.md) — I81 charter, 10-phase shape, layout migration tranche gating
5. [`docs/wip/planning/82-holistika-capability-doctrine/master-roadmap.md`](../82-holistika-capability-doctrine/master-roadmap.md) — I82 charter, 8-milestone shape, doctrine + 3 capability registers + live UAT
6. [`docs/wip/planning/89-hlk-erp-program-rollup-implementation/master-roadmap.md`](../89-hlk-erp-program-rollup-implementation/master-roadmap.md) — I89 charter, 6-phase cross-repo TSX implementation
7. [`docs/wip/planning/_blockers/i74-promotion-blocker-tracker.md`](../_blockers/i74-promotion-blocker-tracker.md) — BT-I74 7-condition activation gate
8. [`docs/wip/planning/_blockers/i75-promotion-blocker-tracker.md`](../_blockers/i75-promotion-blocker-tracker.md) — BT-I75 4-condition activation gate
9. [`docs/wip/planning/_blockers/i83-promotion-blocker-tracker.md`](../_blockers/i83-promotion-blocker-tracker.md) — BT-I83 4-condition activation gate (two-stage I82 P4 then I76 P3)
10. [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/INITIATIVE_REGISTRY.csv) — confirmed status (I76/I78/I81/I82/I89 active; I84/I85/I87 closed; I86 active)
11. [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv`](../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/OPS_REGISTER.csv) — confirmed 9 open OPS rows tied to I86 cluster work (OPS-86-1/3, OPS-76-1..4, OPS-81-1, OPS-82-1, OPS-89-1)

## 5. Cross-references

- **Parent**: [I86 master-roadmap](master-roadmap.md) — orchestration charter; this inventory is its operational evidence layer.
- **Sibling artifacts in I86 folder**: [`decision-log.md`](decision-log.md); [`risk-register.md`](risk-register.md); [`evidence-matrix.md`](evidence-matrix.md); [`files-modified.csv`](files-modified.csv).
- **Governing rules**:
  - [`akos-planning-traceability.mdc`](../../../../.cursor/rules/akos-planning-traceability.mdc) §"Plan-quality bar" — inherited by B-G3b's burndown plan.
  - [`akos-conflict-surfacing-and-blocker-trackers.mdc`](../../../../.cursor/rules/akos-conflict-surfacing-and-blocker-trackers.mdc) — Option 5 default posture (D-IH-86-O) authorising the 3 blocker-trackers.
  - [`akos-agent-checkpoint-discipline.mdc`](../../../../.cursor/rules/akos-agent-checkpoint-discipline.mdc) — pause-fatigue avoidance + MANDATORY public-prose pause-point category.
  - [`akos-holistika-operations.mdc`](../../../../.cursor/rules/akos-holistika-operations.mdc) §"New git-canonical compliance registers" — canonical-CSV gate discipline for I81 P2 + I82 P1+P2 + I76 P4 + OPS-86-3.
- **Downstream**: B-G3b authoring pass — consumes this inventory to author the full 11-section cluster burndown plan with `D-IH-86-T` ratification.

---

## Open questions for B-G3b to resolve

1. **I78 effort scoping not fully read** — task description listed I76+I81+I82+I89 as files to read; I78 was inferred from I86 charter sibling list (where it appears as "active; P1 engineering pending"). B-G3b should read [`docs/wip/planning/78-brand-voice-llm-as-judge/master-roadmap.md`](../78-brand-voice-llm-as-judge/master-roadmap.md) to verify the 3-5d P1-only effort estimate before authoring its risk register and effort-rollup table.
2. **I79 + I80 retro-count discrepancy** — I86 master-roadmap §1.5 says "5 of 10 cluster siblings closed: I79 + I80 + I84 + I85 + I87", but the original I86 charter title lists 10 siblings as `I81 I84 I85 I82 I83 I74 I75 I76 I87 I78`. I79 + I80 were not in the original 10; they appear to be retro-counted. B-G3b should clarify whether the cluster scope formally expanded (a `D-IH-86-*` decision should document) or whether §1.5 is informal accounting and the canonical scope remains the original 10. This affects closure-criterion arithmetic ("10 siblings closed").
3. **I86 self-closure vs cluster closure** — I86 master-roadmap preamble says "I86 CLOSES at end of P3 per D-IH-86-N" but `INITIATIVE_REGISTRY.csv` row keeps `status: active` and §7 closure criterion requires "10 siblings closed + OPS-86-1 closed". B-G3b should ratify whether the cluster burndown plan targets (a) `D-IH-86-CLOSURE` mint when all 10 close (current §7 criterion), or (b) reconciles the P3-effective-closure framing with the operational-coordinator framing.
