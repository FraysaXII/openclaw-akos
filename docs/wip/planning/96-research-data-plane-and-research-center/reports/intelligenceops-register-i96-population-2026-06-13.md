---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: population-pack
authored: 2026-06-13
audience: J-OP;J-AIC
status: draft
requires_operator_gate: yes
canonical_target: docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
---

# IntelligenceOps register — I96 population pack (2026-06-13)

> **Functional name:** The IntelligenceOps register — the canonical CSV that lists live intelligence targets, their verify-by dates, and staleness posture for the research radar sweep.
>
> **Current state:** 5 rows (3 placeholders with `TODO[OPERATOR-*]` targets). Radar sweep shows **1 DUE** (`IO-CIT-COMPETITOR-PLACEHOLDER-001`, `next_verify_by` 2026-06-15, `block_govern`).

## Research Center consumption map

| Register signal | RC surface | Lens |
|:---|:---|:---|
| `staleness_posture=block_govern` | Staleness insight cards · freshness strip severity | Operator · Compliance |
| `next_verify_by` overdue | Radar queue panel · "re-verify" micro-CTA | Operator |
| `output_artifact` path | Navigate CTA destination | All |
| Empty / scaffold row | Honest empty queue — **not** topic_cluster substitute | Operator |

## Placeholder disposition — IO-CIT-COMPETITOR-PLACEHOLDER-001

| Field | Value |
|:---|:---|
| **Sweep signal** | DUE 2026-06-15 (`volatility_class=fast`, `staleness_posture=block_govern`) |
| **Disposition** | **Replace** — supersede placeholder with `IO-I96-GOV-ANALYTICS-001` (governed analytics pack) OR **archive** placeholder if competitor intel deferred to brand tranche |
| **Recommended** | Replace with I96 pack target (row below); set placeholder `lifecycle_status=archived` with `notes` pointing to successor `register_id` |
| **Owner** | Operator inline-ratify at CSV gate |
| **Carryover** | **Scheduled** — fires at P-G2 CSV tranche (not dropped) |

## Draft CSV rows (operator ratify — do not commit without gate)

Schema header (existing):

```csv
register_id,target_id,target_class,cadence,source_type,reliability,output_artifact,responsible_role,lifecycle_status,intro_decision_id,linked_sop_path,linked_runbook_path,notes,last_review_at,last_review_by,last_review_decision_id,methodology_version_at_review,volatility_class,staleness_days,staleness_posture,next_verify_by
```

### New I96-relevant rows

```csv
IO-I96-RESEARCH-CENTER-001,I96-research-data-plane,recommendation,scheduled,CORPINT,B,docs/wip/planning/96-research-data-plane-and-research-center/,Lead Researcher,active,D-IH-96-A,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,I96 Research Center + data plane — BFF insights staleness consumer; RC Operator/Director lenses.,2026-06-13,Lead Researcher,D-IH-96-A,v3.2,fast,30,block_govern,2026-07-13
IO-I96-GOV-ANALYTICS-001,governed-actionable-analytics-surfaces-2026-06-12,recommendation,scheduled,CORPINT,B,docs/wip/intelligence/governed-actionable-analytics-surfaces-2026-06-12/,Lead Researcher,active,D-IH-96-B,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,Governed actionable analytics surfaces pack — insight card taxonomy + BFF schema for RC v2.,2026-06-12,Lead Researcher,D-IH-96-B,v3.2,fast,30,block_govern,2026-07-12
IO-I96-GOJ-UX-001,governed-operator-journey-ux-uat-2026-06-12,recommendation,scheduled,CORPINT,B,docs/wip/intelligence/governed-operator-journey-ux-uat-2026-06-12/,Lead Researcher,active,D-IH-96-F,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,GOJ UX pack — journey matrix T0-T3 copy + per-lens UAT LOOP; RC page spec v2 consumer.,2026-06-12,Lead Researcher,D-IH-96-F,v3.2,medium,45,cite_and_flag,2026-07-27
IO-I96-KIRBE-DATA-001,kirbe-research-ingest-contract,recommendation,scheduled,CORPINT,B,docs/wip/planning/96-research-data-plane-and-research-center/ledger-to-vault-ingest-contract.md,Lead Researcher,active,D-IH-96-C,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,KiRBe ingest + ledger-to-vault contract — Operator KiRBe env card + search health on RC.,2026-06-11,Lead Researcher,D-IH-96-C,v3.2,fast,30,block_govern,2026-07-11
IO-I96-AOS-GOV-001,akos-automation-os-governance-2026-06-10,recommendation,scheduled,CORPINT,B,docs/wip/intelligence/akos-automation-os-governance-2026-06-10/,Lead Researcher,active,D-IH-90-A,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,Automation OS governance pack — executable process catalog + adapter registry crosswalk for RC navigate CTAs.,2026-06-10,Lead Researcher,D-IH-90-A,v3.2,fast,30,block_govern,2026-07-10
IO-I96-MADEIRA-UAT-001,aic-madeira-experiential-uat-2026-06-11,recommendation,scheduled,CORPINT,B,docs/wip/intelligence/aic-madeira-experiential-uat-2026-06-11/,Lead Researcher,active,D-IH-96-A,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,MADEIRA experiential UAT charter — sibling-repo browser manifest bar feeding RC UAT ladder.,2026-06-11,Lead Researcher,D-IH-96-A,v3.2,medium,60,cite_and_flag,2026-08-10
IO-I96-INFONOMICS-REF-001,infonomics-holistika-data-economics-2026-06-12,recommendation,scheduled,CORPINT,C,docs/wip/intelligence/infonomics-holistika-data-economics-2026-06-12/,Lead Researcher,scaffold,D-IH-97-P0,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,Infonomics data economics WIP — reference-only for RC until I97 P5 ratify (overlap tracker CO-97-004); cite_and_flag not block_govern.,2026-06-12,Lead Researcher,D-IH-97-P0,v3.2,slow,90,cite_and_flag,2026-09-12
IO-I96-HACO-001,holistic-agentic-capability-orchestration-2026-06-10,recommendation,scheduled,CORPINT,B,docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/,Lead Researcher,active,D-IH-94-A,docs/references/hlk/v3.0/Research/Methodology/canonicals/SOP-RESEARCH_RADAR_001.md,scripts/research_radar_sweep.py,Holistic agentic orchestration — supersedes IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001 scaffold target_id.,2026-06-10,Lead Researcher,D-IH-94-A,v3.2,fast,30,block_govern,2026-07-10
```

### Existing rows — disposition

| register_id | Action |
|:---|:---|
| `IO-CAP-HOLISTIC-AGENTIC-ORCHESTRATION-2026-001` | **Supersede** → `IO-I96-HACO-001`; archive scaffold row |
| `IO-REG-ENISA-2026-001` | **Keep** — slow regulator; unchanged |
| `IO-CIT-COMPETITOR-PLACEHOLDER-001` | **Archive** after `IO-I96-GOV-ANALYTICS-001` lands OR replace `target_id` inline at ratify |
| `IO-MED-PLACEHOLDER-001` | **Keep scaffold** until media watch chartered — or archive at operator choice |
| `IO-REC-PLACEHOLDER-001` | **Keep scaffold** until recruiter tracker chartered |

## Prong / topic_cluster linkage

See [`topic-cluster-intelligenceops-harmonization-2026-06-13.md`](topic-cluster-intelligenceops-harmonization-2026-06-13.md) — `topic_cluster` in source ledgers does **not** become `target_id`; mapping table links packs to register rows.

## Verification (post-CSV commit)

```powershell
py scripts/validate_intelligenceops_register.py
py scripts/research_radar_sweep.py
py scripts/validate_hlk.py
py scripts/verify.py compliance_mirror_emit   # if mirror sync in scope
```

## Cross-references

- Staleness loop: [`../staleness-loop-spec.md`](../staleness-loop-spec.md)
- Research radar discipline: `RESEARCH_RADAR_DISCIPLINE.md`
- Master tranche P-G2: [`research-center-gap-closure-deploy-uat-tranche-2026-06-13.md`](research-center-gap-closure-deploy-uat-tranche-2026-06-13.md)
