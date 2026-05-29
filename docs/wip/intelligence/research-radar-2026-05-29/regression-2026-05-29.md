---
title: Research Radar — regression report (the honest "what exists / what is stale / what composes" map)
language: en
intellectual_kind: wip_intelligence_synthesis
sharing_label: internal_only
audience: J-OP
authored: 2026-05-29
last_review: 2026-05-29
status: draft
linked_research_sources:
  - docs/wip/intelligence/research-radar-2026-05-29/source-ledger.csv
---

# Research Radar — Stage A regression report

> **Why this exists.** A stale platform claim ("Cursor can't switch models / subagents
> are the only lever") reached governed doctrine without ever being date-checked. The
> operator named the real failure: *overestimating research for lack of rigour — not
> checking source dates / current product state.* The instruction: regress the research
> discipline **and** the agent's understanding of the apparatus, to a bar of
> **flexible / novel / robust / usable / scalable / DAMA-governed / product-managed /
> not-hardcoded / holistik**, then design a functional radar (Stage B charter), then ratify.
> This report is Stage A. Every claim is tagged **[verified]** (read/checked this session),
> **[proposed]** (design intent, not built), or **[unverified]** (flagged for the radar).

## 0. Method

Four streams: three read-only apparatus sweeps + one self-run verification stream.
This report applies the research-to-decision discipline to itself — it carries its own
[`source-ledger.csv`](source-ledger.csv) and is validated by `scripts/validate_research_action.py`.
That recursion is deliberate: the regression that feeds the radar charter is itself a
governed research action.

## 1. The original failure [verified]

- The claim "Cursor can't switch the foreground model; subagents are the only lever" was
  **never a sourced ledger row** — it was asserted from model-training memory as a stable
  platform fact and propagated into a cursor rule + skill + routing map.
- **Dates that condemn it:** Cursor `/multitask` shipped in **3.2 on 2026-04-24**; Plan Mode
  carries its own planning-model selector. The model-selection research is dated
  **2026-05-28** — the feature predated the research by **~5 weeks**. A "what changed in the
  last 60 days" check would have caught it. None ran.
- **Root cause:** the source ledger rates *reliability / credibility / confidence* but has
  **no time axis** — no `as_of` date, no volatility class, no re-verify deadline. A May claim
  is treated as true forever. Platform/tooling claims weren't even ledger rows.

## 2. The discipline gap [verified]

`RESEARCH_ACTION_DISCIPLINE.md` is **intake-shaped**: ingest → rate → rank → synthesize →
govern → implement → test → iterate. Loop step 8 literally says *"keep the topic on radar"*
and §5 says it prevents findings that *"cannot become a radar"* — but **"radar" is a word in
the doctrine with no mechanism.** The 13-field ledger schema
(`akos/hlk_research_action.py`) has **no freshness / decay / as-of / next-verify field**.

## 3. What already exists — the GOOD precedent to build on [verified]

The not-hardcoded pattern is **already in your KB**:

| Precedent | Mechanism | Path |
|:---|:---|:---|
| **Persistence vehicle registry** (strongest) | per-row **`read_cadence` + `staleness_days` + `staleness_posture`**, read by a runbook (`scripts/madeira_persistence_check.py`) — cadence + decay are **data**, not constants | `…/Envoy Tech Lab/canonicals/dimensions/MADEIRA_PERSISTENCE_VEHICLE_REGISTRY.csv` |
| **IntelligenceOps register** | per-row **`cadence`** + owner + linked SOP/runbook (no decay window yet) | `…/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv` |
| **Policy register** | per-row **`cadence` + `next_review`** | `…/People/Compliance/canonicals/dimensions/POLICY_REGISTER.csv` |
| **Process list** | per-row **`cadence_type`** (on_demand / scheduled / event_triggered / gated_operator) | `…/People/Compliance/canonicals/process_list.csv` |

**Design anchor [proposed]:** the radar mirrors the persistence-vehicle pattern — cadence +
decay window + posture as **governed columns**, read by a runbook. No magic numbers in code.

## 4. The hardcoded offenders — what NOT to copy [verified]

| Constant | Where | Value |
|:---|:---|:---|
| Canonical freshness tiers | `akos/canonical_freshness.py` | 3 / 30 / 90 days |
| Substrate audit staleness | `scripts/peopl_research_substrate_audit_cadence.py` | `STALENESS_THRESHOLD_DAYS = 90` |
| Substrate audit cadence | `SOP-RESEARCH_SUBSTRATE_AUDIT_CADENCE_001.md` | `cadence_schedule: quarterly` |
| Review-stamp sweep | `scripts/validate_review_stamps.py` | 180 days |
| Index drift (IDX-04) | `scripts/baseline_index_sweep.py` | 7 days |

The substrate audit is the worked anti-pattern: **quarterly in the SOP + `last_audit_date` in
the register + 90 in the script** — three places, one drifts. The operator's objection
("hardcoding quarterly contradicts what I've built") is exactly right.

## 5. The ironic finding — the one radar isn't switched on [verified]

The single domain radar you have (substrate-audit cadence) is **chartered but not firing**:
its `process_list.csv` row **`env_tech_dtp_substrate_landscape_mtnce_001` does not exist**
(grep returned no matches), so the SOP is stuck at `status: review`. So even where a radar
exists, its beam is (a) scoped to AI models only and (b) **off**.

## 6. Volatile-claim re-verification [verified] — the audit caught real drift

| Claim in the routing map | Verdict (2026-05-29) | Evidence |
|:---|:---|:---|
| DeepSeek V4 / Kimi K2.6 / Qwen 3.6 / GLM 5.1 | **VERIFIED** real, current | OpenLM, Codersera, Kilo, MindStudio (May 2026) |
| DeepSeek V4-Pro pricing | **DRIFTED** — permanent cut 2026-05-22 ($0.435/$0.87) | Codersera |
| **Wan 2.2** (video) | **STALE → Wan 2.7** (shipped 2026-05-25) | technology.org |
| **Hunyuan3D 2.1** | **STALE → Hunyuan3D 3.1** | search |
| HunyuanImage 3.0 | **VERIFIED** | Tencent GH / HF |
| FLUX.2 klein | **UNVERIFIED** — flag for radar | not confirmed in sweep |

The model **names** held; the **video/3D versions were stale within weeks** and **pricing
moved**. This is the fast-volatility class — concrete proof the radar is needed, not theory.

## 7. KiRBe + scale reality [verified]

KiRBe is a **separate SaaS product** (`kirbe-platform` v1.2 + `kirbe.*` Supabase schema),
reframed as the "AI Archivist / universal ingestor" under **I83 (active, not fully wired)**.
It already has a `yt_transcript` connector. **Today's intake is metadata-first**: ~60–80
rated sources across 3 `source-ledger.csv` folders + Trello playlist *indexes* (not video
bodies). **No 2,000-video corpus lives in git yet.** Implication: the radar is the
**intake + freshness contract**; KiRBe is the **execution substrate** that fulfils it at
media scale. Deferring storage pending confidence in the contract is coherent, not avoidance.

## 8. Compose-with map [verified] — what the radar must plug into, not duplicate

- **Research Action discipline** — the radar **feeds** its `govern` stage (prioritised, fresh
  topics); it does not replace the ledger + 8-stage loop.
- **IntelligenceOps register** — the per-target tracking spine (extend beyond its 4 seed rows).
- **Topic–Fact–Source + `TOPIC_REGISTRY`** — stable IDs for playlists/clusters.
- **`source_taxonomy.md` + `confidence_levels.md`** — reuse OSINT/HUMINT/CORPINT + Safe/Euclid/Keter.
- **PRECEDENCE + compliance mirrors** — git canonical wins; KiRBe reads mirrors.
- **Overlap to resolve [proposed]:** I75 research-area governance plans a `SOURCE_RELIABILITY_REGISTRY`
  (P4); I83 owns KiRBe ingestion. The charter must de-conflict scope with both, and with the
  MADEIRA `gtm_ws_madeira_radar` workstream + the investor `program-radar` brief (same word,
  different things).

## 9. Mint surface if ratified as 16th specialty [verified]

A Quality-Fabric specialty mint is a **15-surface contract** (canonical doctrine + Pydantic +
validator + runbook + cursor rule + skill + paired SOP + pattern-registry row + PRECEDENCE +
QF §6 row + CHANGELOG + process row + validate_hlk + verification-profiles + release-gate).
The charter (Stage B) will decide whether Research Radar is the **16th QF specialty** or a
Research-area discipline composed into the 15th (Research Action).

## 10. Honest confidence verdict

- **What's now grounded [verified]:** the failure mechanism; the not-hardcoded precedent
  (persistence-vehicle registry); the hardcoded offenders; the radar-not-switched-on fact;
  real volatile drift (Wan, Hunyuan3D, pricing); KiRBe's true nature + scale; the compose-with
  surface; the mint contract.
- **What's open for the charter [proposed]:** the decay/volatility taxonomy (data-driven, no
  magic numbers); 16th-specialty vs Research-area-discipline; scope de-confliction with I75 +
  I83; whether KiRBe is the execution substrate now or later.
- **What stays unverified [unverified]:** FLUX.2 klein; exact current pricing across all lanes —
  these become the **first radar intake targets**, which is the point: the system, not me,
  keeps them fresh.

**Bottom line:** the design *direction* — register-driven cadence + per-target decay window +
media-agnostic intake, composing your own proven patterns — can hold the Trello / CHANGELOG /
2k-video / 20-source corpus **only because it is not hardcoded**. That is now evidenced, not
asserted. Stage B turns it into a charter at your bar; nothing canonical is written until you
ratify.
