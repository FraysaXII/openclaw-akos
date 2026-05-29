---
intellectual_kind: composer_bounded_packet
packet_id: C2-multi-channel-feed-delivery
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-83
ops_forward: OPS-86-30
authored: 2026-05-29
status: ready
depends_on_packet: C1-data-consumer-inventory
---

# Composer packet — C2 Multi-channel research-feed delivery

## Objective

Implement the **SHARE data-product** path: research radar / IntelligenceOps stale queue pushed to
operator inbox + Discord + Slack + Telegram (channel adapters per normalized adapter pattern).

## Preconditions

- C1 inventory complete (consumer_id FK for each channel).
- Prod mirror re-sync applied (`OPS-86-32`) so register rows are live.

## Deliverables (sibling repos — gate already approved)

| Repo | Path / artefact |
|:---|:---|
| `openclaw-akos` | `scripts/research_feed_dispatch.py` (runbook skeleton) |
| `openclaw-akos` | `akos/hlk_research_feed.py` (Pydantic message envelope) |
| `kirbe-platform` | Ingest webhook or worker hook (bounded — cite I83 master-roadmap) |
| `hlk-erp` | Optional operator inbox row (defer to E2 if scope tight) |

## Message envelope (minimum fields)

`feed_id`, `register_id`, `staleness_posture`, `title`, `summary`, `source_url`, `confidence`,
`audience`, `channel`, `render_format` (`mail` | `slack` | `discord` | `telegram`)

## Validators / tests

- `tests/test_hlk_research_feed.py` — valid + invalid envelope pairs
- Wire self-test into `config/verification-profiles.json` when stable

## Acceptance

- Dry-run mode prints formatted payload without sending secrets.
- One channel (mail OR slack) end-to-end in dev with env vars documented in `docs/USER_GUIDE.md` §research feed (stub section OK).

## Escalate to Opus if

- Channel choice affects external-render discipline (external audience).
- New `process_list.csv` row required.
