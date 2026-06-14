---
parent_initiative: INIT-OPENCLAW_AKOS-96
report_kind: implementation-note
authored: 2026-06-14
status: active
audience: J-OP;J-AIC
related_repo: hlk-erp
---

# Research Center B2.4 — Realtime freshness subscribe (2026-06-14)

## Wired (hlk-erp main)

| Surface | Channel | Table | Behavior |
|:---|:---|:---|:---|
| Freshness strip — **Radar** badge | `hol.i96.freshness.radar` | `compliance.intelligenceops_register_mirror` | `postgres_changes` → invalidate React Query `research-center/*` keys (60s polling fallback retained) |

**Code:** `lib/research-center/realtime/use-radar-freshness-realtime.ts` + `FreshnessStrip` mount.

**Prerequisites (live):** I99 migration `20260613150000_i99_realtime_publication_i96_i62.sql` applied MasterData; publication + `REPLICA IDENTITY FULL` verified 2026-06-13.

## Not wired (honest posture)

| Badge / widget | Transport | Posture |
|:---|:---|:---|
| Ledger | Git reader poll | polling_only (govern plane) |
| KiRBe | HTTP health poll | polling_only |
| Mirrors heartbeat | `holistika_ops.mirror_freshness_heartbeat` | **scheduled** — SUPA-RT-04 |
| Preview env UAT | Vercel Preview matrix | **deferred** — production UAT (P-G6) is bar |
| Notifications drawer | `hol.i62.drawer.notifications` | already wired I62; separate surface |

## Verification (hlk-erp)

- `npm run typecheck` — PASS
- `npm run lint` — PASS (pre-existing command-palette hook warning)

## Followups

1. **P-G6 production UAT** on `erp.holistikaresearch.com` after merge deploy — validate radar badge updates without reload when mirror emit runs.
2. **Tier 2 panels** (radar queue, ledger summary) inherit invalidation via shared query keys; no separate channel needed until mirrors heartbeat lands.
