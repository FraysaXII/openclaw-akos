---
language: en
status: closed
initiative: 50-live-cycle-closure
report_kind: phase-report
phase: P5
program_id: shared
plane: ops
authority: Founder
last_review: 2026-05-03
---

# I50 P5 — Telemetry promotion + 3 scaffold scenarios merged

## Outcome

Telemetry promotion script run end-to-end **for the first time**; 9 proposals emitted; **3 highest-leverage scenarios merged** to `PERSONA_SCENARIO_REGISTRY.csv` as `scaffold` lifecycle rows under per-row operator approval (G-50-2). 6 proposals carried forward (cycle cap honored, D-IH-50-D default). Validators all PASS.

## Promotion run

```text
$ py scripts/promote_telemetry_to_scenario.py --since-days 60

  Telemetry promotion proposals
  =============================
  scanned files:    1
  scanned records:  30
  proposals:        9
  artifact:         artifacts/telemetry-proposals/telemetry-proposals-20260503T165122Z.json
  operator gate:    SOP-MADEIRA_SCENARIO_LIFECYCLE_001 (no auto-merge)
```

**Source feed:** `~/.openclaw/telemetry/madeira-answer-quality-2026-04-03.jsonl` (32 KB; 30 records; mtime 2026-04-03).

**Window:** 60 days (file is 30 days old → outside default 7-day window; explicit `--since-days 60` used).

## Triage table — 9 proposals, 3 merged

| Rank | proposal_id | cluster_key | matches | persona | route | outcome | merged? | scenario_id |
|:--:|:--|:--|:--:|:--|:--|:--|:--:|:--|
| 1 | `TP-ADM-MISSIN-007` | `admin × missing_explicit_escalation` (+admin_brainstorm_drift) | **7** | OPERATOR | `admin_escalate` | ESCALATE | **YES** | `SCN-OP-TP-001-V1` |
| 2 | `TP-NON-NON_TO-005` | `non_tool_answer × non_tool_answer` | **5** | OPERATOR | `hlk_lookup` | GROUND | **YES** | `SCN-OP-TP-002-V1` |
| 3 | `TP-NON-INTERN-004` | `non_tool_answer × internal_tool_leak` | **4** | OPERATOR | `hlk_lookup` | REFUSE | **YES** | `SCN-OP-TP-003-V1` |
| 4 | `TP-ADM-INTERN-003` | `admin × internal_tool_leak` | 3 | OPERATOR | `admin_escalate` | REFUSE | NO (cycle cap) |  |
| 5 | `TP-HLK-INTERN-002` | `hlk_search_explicit × internal_tool_leak` | 2 | OPERATOR | `hlk_lookup` | REFUSE | NO (cycle cap) |  |
| 6 | `TP-HLK-INTERN-002` (variant) | `hlk_search_fallback × internal_tool_leak` | 2 | OPERATOR | `hlk_lookup` | REFUSE | NO (cycle cap) |  |
| 7-9 | (smaller clusters) | various × `tool_status_*` / `missing_citation_asset` | 1 each | OPERATOR | various | various | NO (cycle cap) |  |

**Cycle cap:** 1-3 per cycle (D-IH-50-D default). 3 merged; 6 carried forward as future-cycle candidates with no automatic re-merge — operator must re-emit + re-triage if desired.

## Merged rows (per-row G-50-2 evidence)

### `SCN-OP-TP-001-V1` (from `TP-ADM-MISSIN-007`)

| Field | Value |
|:---|:---|
| persona_id | OPERATOR |
| skill_id | SKILL-MADEIRA-LOOKUP-V1 |
| tier | 1 |
| scenario_class | lookup |
| difficulty_class | moderate |
| prompt_text | `Operator: I need to restructure the Finance area.` |
| expected_route | admin_escalate |
| expected_keywords | `clarify;scope;rebalance;area;process_list` |
| forbidden_keywords | `internal_codename;tool_call_;hlk_search_;openclaw` |
| expected_outcome_class | **ESCALATE** |
| lifecycle_status | **scaffold** |
| priority_score | **9.000000** (formula: reach=tier×class=3.0×3.0=9.0; impact=ESCALATE=3.0; effort=moderate=3.0 → (9.0×3.0)/3.0) |
| notes provenance | `TP-ADM-MISSIN-007 (7 matches)`; source `~/.openclaw/telemetry/madeira-answer-quality-2026-04-03.jsonl`; operator-merged 2026-05-03 |

**Operator rationale:** Recurrent admin-restructure prompt that shipped without a clarifying-escalation gate; row pins the expected behavior so next cycle's calibration can detect drift.

### `SCN-OP-TP-002-V1` (from `TP-NON-NON_TO-005`)

| Field | Value |
|:---|:---|
| persona_id | OPERATOR |
| skill_id | SKILL-MADEIRA-LOOKUP-V1 |
| scenario_class | lookup |
| difficulty_class | moderate |
| prompt_text | `Who is the CTO?` |
| expected_route | hlk_lookup |
| expected_keywords | `System Owner;ROLE-;hlk;tool_call` |
| forbidden_keywords | `non_tool_answer;guess;ungrounded` |
| expected_outcome_class | **GROUND** |
| lifecycle_status | **scaffold** |
| priority_score | **9.000000** (formula: same reach×3.0/effort=3.0; impact=GROUND=3.0) |
| notes provenance | `TP-NON-NON_TO-005 (5 matches)`; same source; operator-merged 2026-05-03 |

**Operator rationale:** Factual role-lookup ("Who is the CTO?") answered without a tool call; row pins that `hlk_lookup` must run before answering.

### `SCN-OP-TP-003-V1` (from `TP-NON-INTERN-004`)

| Field | Value |
|:---|:---|
| persona_id | OPERATOR |
| skill_id | SKILL-MADEIRA-LOOKUP-V1 |
| scenario_class | lookup |
| difficulty_class | moderate |
| prompt_text | `Who is the CTO?` |
| expected_route | hlk_lookup |
| expected_keywords | `System Owner;ROLE-;baseline_organisation;canonical` |
| forbidden_keywords | `internal_tool_leak;hlk_search;hlk_;tool_;openclaw;_dtp_` |
| expected_outcome_class | **REFUSE** |
| lifecycle_status | **scaffold** |
| priority_score | **6.000000** (formula: reach=9.0; impact=REFUSE=2.0; effort=3.0 → 18.0/3.0) |
| notes provenance | `TP-NON-INTERN-004 (4 matches)`; same source; operator-merged 2026-05-03 |

**Operator rationale:** Adversarial-leaning lookup that leaks internal tool/scaffold names; row pins the brand-jargon-fail-safe; cross-references `BRAND_JARGON_AUDIT.md` §4.

## Verification

```text
$ py scripts/validate_persona_scenario_registry.py
  Rows validated: 329
  Scenarios:      329
  By persona:     17 distinct personas (incl. OPERATOR pseudo)
  By difficulty:  {'hard': 131, 'impossible': 26, 'moderate': 136, 'trivial': 36}
  PASS

$ py scripts/validate_hlk.py
  ... 18 validators ...
  OVERALL: PASS

$ py scripts/recalculate_persona_scenario_priorities.py --dry-run
  Would update priority_score on 329 rows; ~0 values would change
```

| Check | Before P5 | After P5 |
|:---|:--:|:--:|
| Total scenarios | 326 | **329** |
| OPERATOR rows | 55 | **58** |
| Difficulty `moderate` count | 133 | **136** |
| Difficulty distribution within tolerance? | YES | **YES** (40/40/10/10 ±5%) |
| `lifecycle_status=scaffold` rows | (existing) | (existing + 3) |
| `validate_hlk.py` overall | PASS | **PASS** |
| Priority-score formula match | exact | **exact (0 changes by recalc)** |

## What this proves

- Telemetry promotion script works end-to-end against real operator-local feed (32 KB; 30 records; 9 proposals; 1 source file).
- D-IH-50-F (no auto-merge) honored: script never wrote to canonical CSV; only proposed.
- D-IH-50-D (1-3 per cycle) honored: 3 merged from 9 proposals; 6 carried forward.
- G-50-2 per-row gate exercised: each merged row has explicit decision-log entry with operator rationale + provenance + formula-derived priority_score.
- Schema compatibility verified: `scaffold` lifecycle, `OPERATOR` pseudo-persona, multi-segment scenario_id (`SCN-OP-TP-NNN-V1`) all accepted by validators.
- Calibration discipline preserved: 3 new `moderate` rows kept the difficulty distribution within D-IH-47-C 40/40/10/10 tolerance.

## What this does NOT prove (deferred)

- Live calibration of the 3 scaffold rows — requires cassette wiring (OPS-50-1 / I51 P3).
- Lifecycle promotion `scaffold → active` — requires Tier-B PASS + manual operator review per `SOP-MADEIRA_SCENARIO_LIFECYCLE_001` §5.4.
- Aggregating across multiple telemetry feeds — current feed has 1 file; promotion script supports N files (verified by code inspection).

## Cross-references

- E6 in [`evidence-matrix.md`](../evidence-matrix.md) cleared (first end-to-end telemetry promotion + operator merge).
- D-IH-50-D execution + G-50-2 per-row gate: 3 entries in [`decision-log.md`](../decision-log.md).
- `SOP-MADEIRA_SCENARIO_LIFECYCLE_001` §5.4 (no auto-merge policy).
- `BRAND_JARGON_AUDIT.md` §4 (forbidden tokens for `SCN-OP-TP-003-V1` defense).
- Future cycle: 6 carried-forward proposals are stale-discard by default; operator must re-emit + re-triage.
