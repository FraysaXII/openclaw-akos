---
language: en
status: active
intellectual_kind: active_research_radar
sharing_label: internal_only
audience: J-OP;J-AIC
role_owner: Research Director
steward_role: KM Officer
authored: 2026-06-11
last_review: 2026-06-11
linked_initiatives:
  - INIT-OPENCLAW_AKOS-95
  - INIT-OPENCLAW_AKOS-94
  - INIT-OPENCLAW_AKOS-83
linked_canonicals:
  - docs/references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md
  - docs/references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md
  - docs/references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv
  - docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/dimensions/TOPIC_REGISTRY.csv
  - docs/wip/planning/_candidates/i-nn-research-data-management-and-feed-delivery.md
  - docs/wip/planning/86-initiative-cluster-execution-coordinator/composer-packets/packet-c2-multi-channel-feed-delivery.md
worked_example_target:
  register_id: IO-PRJ-HOL-DENOM-2026-001
  topic_id: topic_external_adviser_handoff
  engagement_tracker: docs/references/hlk/v3.0/Think Big/Advisers/2026-holistika-incorporation/00-internal/portal-expediente-tracker-2026-06-10.md
---

# Agnostic topic watch — design note for I95 / I94 / I83 AIC sessions

> **For the other Madeira-Cursor AIC:** this is the **agnostic** pattern the operator wants — not an Ayuda-T-Pymes one-off script. Any future topic (incorporation, ENISA, competitor, regulator, engagement) registers as a **watch target** and reuses the same sweep → diff → Research Action ingest → optional digest path. **Priority:** defer full feed delivery to I95/I94 articulation work; ship **Tier A-lite** first (register + email-native signals + daily artifact sweep).

## 1. Problem statement (plain language)

The operator needs a **daily (or per-target) watch** that answers: *"Did anything change that I should act on?"* — for incorporation today, for articulation/I95 decisions tomorrow, and for topics not yet imagined. The watch must be **topic-agnostic**: same machinery, different register rows.

**What we must not build:** a bespoke scraper per portal (Ayuda login, etc.) as the default. Email + public sources first; authenticated RPA only when no API/RSS/email exists and operator explicitly approves SOC cost.

## 2. Where this lives in Research (CORPINT lifecycle)

| Lifecycle stage | Owner | This design |
|:---|:---|:---|
| **ACQUIRE** | Research/Intelligence (OSINT) | Source adapters fetch or receive deltas |
| **PROCESS** | Research Action + Validation | Ingest → rate → rank → synthesize |
| **STORE** | Tech (Supabase/artifacts) | Raw capture + hash in `artifacts/intelligence-watch/` |
| **RECALL** | Research/Methodology | `INTELLIGENCEOPS_REGISTER` + `TOPIC_REGISTRY` FK |
| **SHARE** | Marketing/External-render + **future I83 C2 feed** | Digest to inbox/Slack — **deferred** until OPS-86-32 mirror freshness fixed |
| **PROTECT** | Compliance access levels | No secrets in repo; Gmail tokens in env/Secret Manager only |

Doctrine anchors: [`RESEARCH_AREA_CHARTER.md`](../../references/hlk/v3.0/Research/canonicals/RESEARCH_AREA_CHARTER.md), [`RESEARCH_RADAR_DISCIPLINE.md`](../../references/hlk/v3.0/Research/Methodology/canonicals/RESEARCH_RADAR_DISCIPLINE.md).

## 3. Agnostic register pattern (mint target — not yet in CSV)

Each watch target = **one row** on [`INTELLIGENCEOPS_REGISTER.csv`](../../references/hlk/v3.0/Research/Intelligence/canonicals/dimensions/INTELLIGENCEOPS_REGISTER.csv) + optional **TOPIC_REGISTRY** link:

| Column / field | Agnostic rule |
|:---|:---|
| `register_id` | `IO-<SCOPE>-<SLUG>-<YYYY>-<seq>` |
| `target_id` | GOI/POI ref, `topic_id`, or `program_id` — not a hardcoded script name |
| `target_class` | `regulator` \| `media` \| `competitor_intelligence_target` \| **`process_watch`** (proposed) \| `recommendation` |
| `source_type` | `OSINT` \| `HUMINT` \| **`email`** (proposed) \| `portal_snapshot` (proposed, last resort) |
| `volatility_class` / `staleness_days` | Per-target only (Research Radar RULE 1 — no global "daily" constant in doctrine) |
| `linked_runbook_path` | Future: `scripts/intelligence_publication_watch_sweep.py` |
| `output_artifact` | `artifacts/intelligence-watch/<register_id>/` + human tracker MD when engagement-bound |

**Worked example (incorporation, not yet minted as IO row):**

- `register_id`: `IO-PRJ-HOL-DENOM-2026-001`
- `target_id`: `PRJ-HOL-FOUNDING-2026` / `GOI-LEG-CONST-2026`
- `source_type`: `email` (primary) + `portal_snapshot` (manual/optional)
- `volatility_class`: `fast` (~1–7d during active constitution)
- Human tracker: [`portal-expediente-tracker-2026-06-10.md`](../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/00-internal/portal-expediente-tracker-2026-06-10.md)

## 4. Activation tiers (operator priority = I95/I94 first)

| Tier | What | When | Owner initiative |
|:---|:---|:---|:---|
| **A-lite (ship first)** | Register row + daily GitHub Action or Cloud Scheduler running sweep; **Gmail label/filter** on `*@ayudatpymes.es` → parse subject/body for estado keywords; public RSS/API for regulators; artifacts-only output | Now (minimal) | I94 P4+ / Research Intelligence |
| **A** | Tier A-lite + `research_radar_sweep.py` integration + Research Action govern queue on delta | After IO row mint | I75 / Wave R+5 |
| **B** | Authenticated portal adapters (RPA/Composio) | Operator-gated per target | ENVOY / Composio |
| **C** | Multi-channel feed (`packet-c2-multi-channel-feed-delivery.md`) | After OPS-86-32 + C1 inventory | I83 |

**Operator instruction (2026-06-11):** Q1 tier choice **defers to I95/I94 AIC** — do not block articulation batch on feed product. Digest channel = same priority (artifact-first until C2).

## 5. Gmail / Gemini / Google Cloud — recommended RPA posture

Operator has: personal Gmail + Gemini; Google Cloud (personal + Workspace `admin@holistikaresearch.com`).

| Approach | Fit | Notes |
|:---|:---|:---|
| **Gmail filter + label `holistika/watch`** | Best near-term | Zero code; Gemini can summarize labeled threads in inbox |
| **Gmail API + Cloud Function (Pub/Sub push)** | Best durable | Watch `ayudatpymes.es`, `registradores.org`, ENISA; write JSON to GCS or Supabase; no credentials in repo |
| **Google Apps Script** | Fast prototype | Same as above; operator-owned; migrate to Cloud Function when stable |
| **Composio Gmail MCP** | Agent-assisted | Good for ad-hoc sweeps in Cursor; not SSOT cron — pair with scheduled script |
| **Portal login RPA** | Last resort | Ayuda portal has no public API; email track (`POI-LEG-DENOM-ADV-2026`) is the native channel for denomination |

**Security:** tokens in GCP Secret Manager or GitHub Actions secrets; never commit. Redact DNI/address in automated logs — store full text only in operator-controlled mail + engagement tracker.

## 6. What the other AIC should **not** duplicate

Already exists — **extend**, do not fork:

- `scripts/research_radar_sweep.py` — freshness/staleness queue (WHEN to verify)
- `scripts/agent_memory_trigger_watcher.py` — cron-ready pattern (artifact JSON + exit code)
- `INTELLIGENCEOPS_REGISTER.csv` — target SSOT
- `TOPIC_REGISTRY.csv` — topic FK spine (HCAM / I95 linking)
- `packet-c2-multi-channel-feed-delivery.md` — SHARE layer (later)
- `CAP-HOL-RESEA-DTP-324` Publication Monitoring — planned OSINT capability; this design **is** the SOP/runbook target for that process row

## 7. Suggested mint sequence (for Composer packet)

1. Add `process_watch` + `email` enums to `validate_intelligenceops_register.py` (if missing).
2. Mint `IO-PRJ-HOL-DENOM-2026-001` row (incorporation worked example).
3. Add `scripts/intelligence_publication_watch_sweep.py` — reads register, runs adapters, writes `artifacts/intelligence-watch/<id>/YYYY-MM-DD.json`, exits 1 on delta.
4. Add `.github/workflows/intelligence-watch-daily.yml` — cron 07:00 UTC (mirror `neo4j-aura-keepalive.yml` pattern).
5. Document Gmail setup stub in `docs/USER_GUIDE.md` §research watch (env vars only).
6. Wire delta → Research Action WIP folder under `docs/wip/intelligence/` (Tier 1).

## 8. Link to I95 decision batch

This design **does not resolve** HCAM P5 FK→verb mapping or Neo4j cutover — it **consumes** those registers once wired. Relevant batch lines:

- Orphan-worklist / ICS ordering (Theme 2) — watch targets should rank by ICS when multiple deltas fire.
- IntelligenceOps landing zone (Theme 5.4) — `process_watch` rows live under Research/Intelligence register (already relocated OPS-86-26).
- I83 C2 feed — SHARE output; blocked on mirror freshness (OPS-86-32).

## 9. Cross-references

- Incorporation tracker (worked example): [`portal-expediente-tracker-2026-06-10.md`](../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/00-internal/portal-expediente-tracker-2026-06-10.md)
- I95 articulation corpus: [`docs/wip/intelligence/canonical-articulation-model-2026-06-05/`](canonical-articulation-model-2026-06-05/)
- I94 Operations master roadmap: [`docs/wip/planning/94-area-architecture-and-completeness-v2/master-roadmap.md`](../planning/94-area-architecture-and-completeness-v2/master-roadmap.md)
