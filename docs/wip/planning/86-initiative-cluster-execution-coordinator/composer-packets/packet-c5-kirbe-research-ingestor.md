---
intellectual_kind: composer_bounded_packet
packet_id: C5-kirbe-research-ingestor
target_seat: Composer (execution)
owning_initiative: INIT-OPENCLAW_AKOS-83
authored: 2026-05-29
status: ready
---

# Composer packet — C5 KiRBe research-ingestor wiring

## Objective

Wire Research output (WIP synthesis folders + source ledgers) into KiRBe as an ingestible product
per I83 master-roadmap.

## Read first

- `docs/wip/planning/83-ai-archivist-and-kirbe-ingestor/master-roadmap.md`
- `docs/wip/planning/_candidates/i-nn-research-data-management-and-feed-delivery.md` §C5
- `KNOWLEDGE_PAIRING_REGISTRY.csv` (pairing rows if any)

## Deliverables

| Location | Work |
|:---|:---|
| `kirbe-platform/` | Ingestor route or worker: accept Research pack JSON + source-ledger sidecar |
| `openclaw-akos/` | `scripts/export_research_pack_for_kirbe.py` — emits bundle from `docs/wip/intelligence/<slug>/` |
| `openclaw-akos/tests/` | Fixture pack in + schema validation out |

## Bundle schema (minimum)

```json
{
  "pack_id": "research-<slug>-<date>",
  "source_ledger_path": "...",
  "synthesis_paths": ["..."],
  "access_level": "AL4",
  "topic_ids": []
}
```

## Validators

- `py scripts/validate_research_action.py --source-ledger <path>` on each exported ledger
- KiRBe-side schema test in sibling repo CI

## Acceptance

- Export script runs on one WIP folder (e.g. `topic-ai-landscape-research`) without secrets in output.
- KiRBe ingestor accepts bundle in staging; idempotent re-ingest documented.

## Escalate to Opus if

- Billing plane / `hlk_billing_plane` routing touched.
- New Supabase DDL required (operator SQL gate).
