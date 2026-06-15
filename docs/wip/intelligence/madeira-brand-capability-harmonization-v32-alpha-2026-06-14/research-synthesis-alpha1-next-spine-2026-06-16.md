---
intellectual_kind: research_synthesis
authored: 2026-06-16
parent_pack: madeira-brand-capability-harmonization-v32-alpha-2026-06-14
control_confidence: Euclid
decision_use: α1 spine selection + ratify gates (post LangGraph recovery)
method: internal evidence sweep + external OSINT sweep (research-action discipline)
---

# Research synthesis — next spine after LangGraph spike PASS (2026-06-16)

## Why this document exists

The LangGraph spike failed HLK bar initially by **claiming proof without observable evidence** and **misattributing root cause**. This synthesis applies the research-action loop *before* the next operator spine choice: internal inventory → external OSINT → ranked findings → explicit proof classes → ratify options.

## Ranked findings

| Rank | Finding | Sources | Confidence | Proof class required |
|:---:|:---|:---|:---|:---|
| 1 | **α1 is not the same as α0** — annex defines 5–10 external design partners on Scenarios A+B; opening α1 means support + NDA + cohort + finops attribution, not “internal green = invite outsiders” | INT: v32-closed-alpha-program-annex; alpha-1-readiness-forward-charter | Safe | Operator ratify gate distinct from α0 PASS |
| 2 | **Scenario B α1 gate is partially open** — L3 8/8 journeys PASS; L4 PWF on prod signed-in PNGs (CO-MBH-010). Annex text says “Research Center experiential PASS” — L4 PWF may suffice for α0 but α1 charter marks criterion 2 **partial** | INT: uat-i96 L4 2026-06-16; annex § Alpha phases | Euclid | Close L4 OR explicit operator accept PWF for α1 open |
| 3 | **CO-MBH-010 blocker is I99 Resend SMTP, not “Windows auth”** — prod magic-link pain = Supabase demo mail rate limits + redirect fallback; fix path is OPS-99-1 (Resend custom SMTP + domain verify), status **scheduled** in SUPABASE_AUTH_REGISTRY row SUPA-AUTH-09 | INT: i96-auth RCA; SUPABASE_AUTH_REGISTRY; auth-email tranche | Euclid | Supabase dashboard + Cloudflare DNS + smoke magic link |
| 4 | **α0 closure UAT has registry WARN** — `D-IH-76-ALPHA0` inline-ratified but **absent** from DECISION_REGISTER.csv (validator WARN). Hygiene fix is single-row CSV mint — separate gate from α1 open | INT: uat-i76-v32-alpha0-closure §6 | Safe | `validate_hlk.py` after CSV append |
| 5 | **α1 prep gaps (human/process)** — cohort list, NDA/MOU posture, support channel undefined per forward charter rows 3 & 5 | INT: alpha-1-readiness-forward-charter | Safe | Draft artifacts; Legal/People for NDA |
| 6 | **Design partner industry norm** — 5–10 cohort, mutual NDA, weekly 30-min feedback, dedicated support channel, production use case expected | EXT-041..042 | Euclid | Cohort intake template + support spec before invite |
| 7 | **LangGraph spike PASS ≠ pilot promotion** — CI proved real graph on fixture (run 27520939620); SUBSTRATE row still **candidate** and name implies **Postgres checkpointer** — promoting to pilot without PostgresSaver CI would repeat “claim > proof” | INT: SUBSTRATE_REGISTRY; spike closure; EXT-043 | Euclid | PostgresSaver smoke before pilot mint |
| 8 | **LangGraph PostgresSaver prod class** — official docs require `checkpointer.setup()`, connection pool, durable Postgres; Memory/Sqlite ≠ prod parity | EXT-043..044 | Euclid | New CI job or docker-compose smoke — not bundled in spike |

## What is NOT a blocker (parallel lanes)

| Lane | Posture |
|:---|:---|
| LangGraph portfolio | Spike **closed PASS**; pilot mint **scheduled** after Postgres proof |
| I97 infonomics join | Forward charter only — CSV gates D-IH-97-F/G separate |
| CO-MBH-008 multi-tenant voice | Post-α2 per annex |
| Python 3.13 on shadow box | Local dev parity only; CI already proves langgraph on 3.13 |

## Proof-class matrix (avoid last issue)

| Work item | Acceptable proof | Unacceptable proof |
|:---|:---|:---|
| LangGraph evaluation | Green `langgraph-spike-smoke` + `engine=langgraph` | Mock graph PASS |
| Resend SMTP live | Smoke magic link received at operator inbox; SUPA-AUTH-09 → live | “Will configure later” |
| α1 open | Ratify gate + cohort doc + support channel + finops cohort tags | α0 PASS alone |
| Substrate pilot | PostgresSaver CI + spike CI both green | Spike CI only |
| D-IH-76-ALPHA0 | Row in DECISION_REGISTER + validate_hlk PASS | Inline ratify in UAT only |

## Recommended spine order (AIC recommendation — operator ratifies)

1. **Registry hygiene** — `D-IH-76-ALPHA0` CSV row (small, closes UAT WARN)
2. **I99 OPS-99-1** — Resend SMTP (unblocks CO-MBH-010 / Scenario B L4)
3. **α1 prep pack** — cohort intake + support + finops cohort spec (no invites yet)
4. **α1 open ratify gate** — only after 1–3 evidence packet complete
5. **LangGraph pilot mint** — only after PostgresSaver proof class

Cross-ref: [`alpha-1-readiness-forward-charter-2026-06-16.md`](../../planning/76-madeira-elevation/reports/alpha-1-readiness-forward-charter-2026-06-16.md)
