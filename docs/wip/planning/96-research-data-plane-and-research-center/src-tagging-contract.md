---
initiative_id: INIT-OPENCLAW_AKOS-96
authored: 2026-06-11
---

# SRC tagging contract

Maps Research Action ledger rows to KiRBe vault metadata for ingest and re-embed.

## Tag format

```
SRC-{PACK_SLUG}-{source_id suffix}
```

Examples:

- `SRC-AOS-R6E-012` — Automation OS R6 OSINT row 12
- `SRC-HOL-R3I-005` — Holistic-agentic R3 CORPINT row 5

`source_id` column in ledger remains SSOT; KiRBe stores tag as metadata facet.

## Required ledger columns for ingest

| Column | KiRBe metadata |
|:---|:---|
| `source_id` | Primary key / tag |
| `url` | Fetch target or repo path |
| `prong` | BL-* normalized via `research_ledger_ops` |
| `source_category` | CORPINT vs OSINT routing |
| `control_confidence_level` | Access / filtering |
| `notes` | ICS tier, impacts, CON markers |

## Idempotency

Re-ingest with same `source_id` replaces prior vault document version (KiRBe task model).

## Scope v1

1. `docs/wip/intelligence/akos-automation-os-governance-2026-06-10/source-ledger.csv`
2. Methodology canonicals under `docs/references/hlk/v3.0/Research/Methodology/`
3. Expand to holistic-agentic pack after D4

Handoff: [`ledger-to-vault-ingest-contract.md`](ledger-to-vault-ingest-contract.md) → I83 P2/P3.
