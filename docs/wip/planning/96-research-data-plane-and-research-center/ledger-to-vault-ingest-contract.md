---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
handoff_to: INIT-OPENCLAW_AKOS-83
---

# Ledger → vault ingest contract

Handoff contract from I96 Track C to **I83 KiRBe ingestor** (P2/P3 implementation). I96 defines; I83 implements.

## Scope v1

| Pack | Path | Priority |
|:---|:---|:---|
| Automation OS | `docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv` | P1 |
| Methodology vault | `docs/references/hlk/v3.0/Research/Methodology/**` | P1 |
| Holistic-agentic | `docs/wip/intelligence/holistic-agentic-capability-orchestration-2026-06-10/source-ledger.csv` | P2 (post-D4) |

## Column mapping

| Ledger column | KiRBe metadata key | Required |
|:---|:---|:---:|
| `source_id` | `src_id` + tag `SRC-{pack}-{suffix}` | yes |
| `url` | fetch URL or repo-relative path | yes |
| `prong` | `bl_prong` (normalized BL-*) | yes |
| `source_category` | `corpint_osint` | yes |
| `control_confidence_level` | `confidence` | yes |
| `notes` | `operator_notes` | no |
| `impacts` | `impact_tags` | no |
| `ics_tier` | `ics` | no |

See [`src-tagging-contract.md`](src-tagging-contract.md) for tag format.

## Ingest endpoints (KiRBe)

| Operation | KiRBe surface | Idempotency |
|:---|:---|:---|
| Document fetch | FastAPI ingest job + WebSocket status | `source_id` replaces prior version |
| Vault path bulk | LlamaIndex reader on `docs/references/hlk/v3.0/` | path + mtime hash |
| Re-embed on stale | Triggered by staleness loop | job id logged |

Exploration E1 inventory: `root_cd/kirbe/app/api/main.py`, `/health`, task status routes.

## Neo4j boundary (D-IH-32-M)

| Instance | Owner | Purpose |
|:---|:---|:---|
| AKOS / I95 Neo4j | HCAM enterprise graph | Compliance articulation |
| KiRBe local Neo4j | KiRBe ops | Vault hybrid search |

**No merge.** KiRBe ingest must not write to AKOS graph projection.

## Holistika vault read-only

Per [`config/sync/kirbe-sync-contract.md`](../../../config/sync/kirbe-sync-contract.md): 16 compliance mirrors are read-only in KiRBe. Canonical edits remain in AKOS git.

## Acceptance (I83)

1. Ingest Automation OS ledger rows with SRC tags visible in search metadata
2. Re-ingest on radar STALE signal (see [`staleness-loop-spec.md`](staleness-loop-spec.md))
3. Health probe wired to ERP freshness badge

## Verification

- KiRBe `/health` ok in operator environment
- No secret values in ingest logs
- I96 evidence-matrix row when I83 acknowledges handoff
