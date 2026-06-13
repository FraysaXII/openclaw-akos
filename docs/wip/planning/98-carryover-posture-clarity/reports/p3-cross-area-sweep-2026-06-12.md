# I98 P3 — Cross-area vault + WIP sweep (2026-06-12)

Synthesis of five area-batch explore passes + parent grep across `docs/references/hlk/v3.0/Admin/O5-1/` and `docs/wip/planning/`.

## Executive summary

| Posture | Count (sampled) | Top mislabel pattern |
|:---|:---|:---|
| scheduled | 41 | bare "deferred until P{N}" without index row |
| forward_charter | 28 | "forward-charter" prose without successor_ref |
| overlap_pending | 6 | scope-overlap trackers using "deferred to phase" |
| blocked | 9 | blocker trackers + deferred-funding |
| dropped | 12 | explicit "out of scope" / DECOMMISSIONED |
| monitoring | 4 | PWF followup_class rows |

**Top mislabel:** `deferred` used where work is **scheduled** (will fire at evidence gate) — e.g. I96 D-IH-96-D, I81 audience_tags, DataOps SOP pairing.

**Top collision:** `forward-charter` vs `scheduled-in-place` — e.g. I80→I81 retrofit (forward_charter) vs I97 vault (scheduled P6).

## Batch findings (abbreviated)

### Batch A — Admin, People, Compliance

| File | Snippet | Posture | Gap |
|:---|:---|:---|:---|
| PEOPLE_AREA_RESTRUCTURE.md | CSV split deferred to migration session | scheduled | target_phase missing |
| PASS_WITH_FOLLOWUP_GOVERNANCE | deferred-work-with-tracker | monitoring | linked UAT |
| SSOT_REGISTRY_AUDIT | deferred queue | scheduled | owner initiative |
| AREA_GOVERNANCE | defer-OPS disposition | forward_charter | OPS row |
| i11-i13-i17 tracker | deferred to per-phase gates | overlap_pending | indexed CO-76-001 |

### Batch B — Data, Tech, AI

| File | Snippet | Posture | Gap |
|:---|:---|:---|:---|
| DATA_CONTRACT_REGISTRY | Mirror DDL forward-charter | forward_charter | I93 closed |
| TECHOPS_DISCIPLINE | forward_charters: [] | — | clean |
| SUBSTRATE_REGISTRY | forecasted→pilot deferred I85 | scheduled | |
| CANONICAL_REGISTRY data_contract | forward-charter mirror | forward_charter | |

### Batch C — Finance, Ops, Marketing

| File | Snippet | Posture | Gap |
|:---|:---|:---|:---|
| REVOPS_AREA_CHARTER | CRO forward-charter P4 | forward_charter | |
| SLA_MATRIX | on-call deferred I72 | scheduled | |
| INVESTMENT_THESIS | deferred decision month 6 | scheduled | operator gate |
| BRAND_MULTILINGUAL | footer deferred I71 | forward_charter | closed I71 |
| ENGAGEMENT_MODEL rpp | FORWARD-CHARTER resolver | forward_charter | |

### Batch D — Research, Legal, Ethics, Intelligence

| File | Snippet | Posture | Gap |
|:---|:---|:---|:---|
| RESEARCH_ACTION_DISCIPLINE | iterate: deferring topic | forward_charter | radar row |
| METHODOLOGY_IP | deferred-at-filing-time | scheduled | D-IH-73-F |
| TRADEMARK M6 KiRBe | defer next wave | scheduled | budget gate |
| intelligence synthesis tables | "3 deferred" POV rows | scheduled | UAT POV |

### Batch E — Think Big, Envoy, UX

| File | Snippet | Posture | Gap |
|:---|:---|:---|:---|
| MADEIRA elevation scratchpad | I65 flip deferred | scheduled | |
| COMPONENT_PRIMITIVE_LIBRARY | forward-charter Shadcn | forward_charter | I-NN-OUTPUT |
| BRAND_ENGLISH_PATTERNS §10 | Open follow-ups deferred | forward_charter | |
| external-render-pending tracker | render-pending | scheduled | |

## Operator ratify recommendations (fed to P4)

1. **Backfill aggressiveness:** index + decision-log annotations (not mass vault rewrite).
2. **Vault promotion:** stay planning-only until I97 P6 proves doctrine shape.
3. **Next mechanical step:** optional `--strict` on new planning files in pre_commit_fast (forward OPS row).

## Cross-initiative overlap collisions

| Edge | Risk | Mitigation |
|:---|:---|:---|
| I97 ↔ I96 | doctrine duplication | CO-97-004 overlap_pending P5 |
| I98 ↔ I97 | vocabulary adoption | I97 decision-log uses scheduled rows |
| I81 deferred → I85 | audience_tags | CO-81-001 scheduled |

## Batch annex — expanded subagent passes (2026-06-12)

Five parallel explore passes ([Batch A Admin/People/Compliance](713291c4-663f-4e90-a93a-772ac14044b0), [Batch B Data/Tech/AI](edca10ff-d512-45b2-89d5-1b1bd2fbac4c), [Batch C Finance/Ops/Marketing](4494d26e-f844-438a-97bb-4c54f171012d), [Batch D Research/Legal/Intel](6777fe92-dd74-4ffb-a6b1-559b7309e7bd), [Batch E Think Big/UX/engagement](d90a52bf-3fd8-4c4e-b5af-621321e8b995)) each catalogued **15 high-signal hits** (~75 total). Abbreviated tables above remain the operator skim; this annex captures cross-batch conclusions for P4 ratify + future backfill when files are touched.

| Batch | Dominant posture | Cross-cutting theme | Index coverage |
|:---|:---|:---|:---|
| A | scheduled + forward_charter | I73/I75 vault prose + PRECEDENCE mirror cluster still bare "deferred" | CO-73-001 partial; vault rows unindexed |
| B | forward_charter + scheduled | Data mirror DDL + KiRBe/BI edges cluster on I93/I96 | CO-88-001 only |
| C | forward_charter (8/15) | Ops forward-charters without `successor_ref`; I71-closed Marketing collisions | CO-95-001 indexed |
| D | forward_charter → I75 P1–P4 | Methodology README family shares one successor gate | CO-75-001 prose-only |
| E | forward_charter (SUEZ pack) | UX/MADEIRA monitoring vs scheduled; CO-91-001 stale vs superseded tracker | CO-96-002 related |

### Cross-batch conclusions (fed P4 — now ratified)

1. **Mislabel pattern holds:** bare `deferred` almost always means **`scheduled`** or **`forward_charter`** — rarely **`dropped`** (explicit decommission only, e.g. BRAND_VISUAL_PATTERNS browser recon).
2. **Discoverability gap:** ~60 of ~75 sampled hits lack index rows; P4 chose **index + annotate on touch**, not mass vault rewrite — consistent with I98 closure (planning-only SSOT).
3. **Successor collisions:** I71-closed + I73-closed initiatives still carry forward-charter prose — disposition **`forward_charter`** with refreshed `successor_ref` or **`superseded`** when doctrine landed elsewhere (SEMANTIC_LAYER BI gate vs I93 P5b).
4. **Blocked overlay:** OPS-86-26 (I75), neo4j ADR triggers, I75-gated ERP panels — use **`blocked`**, not bare deferred.
5. **Priority index candidates** (mint when next editing parent artifact): CO-TB-001 (SUEZ pre-send regression), CO-UX-001 (operator journey discipline), CO-MAD-001 (MADEIRA dossier hook), I75 methodology SOP family edge (single CO row covering P1–P4 README cluster).

### Post-closure follow-up (scheduled — not I98 scope)

- Refresh **CO-91-001** discoverability when UX discipline row is next touched (tracker superseded by D-IH-90-AD).
- Wire carryover index as DIM-02 signal per **D-IH-98-D** (inter-wave regression disposition).
- Vault posture discipline remains **forward-chartered** per **D-IH-98-C**.
