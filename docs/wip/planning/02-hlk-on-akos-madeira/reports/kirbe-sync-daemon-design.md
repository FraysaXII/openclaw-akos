# KiRBe sync daemon — design (K0)

**Initiative:** `02-hlk-on-akos-madeira`  
**Date:** 2026-04-14  
**Upstream:** [next-baseline-kirbe-sync-boundary-proposal.md](next-baseline-kirbe-sync-boundary-proposal.md)  
**Phase plan:** [phase-kirbe-sync-daemons-plan.md](../phase-kirbe-sync-daemons-plan.md)

---

## Authority flow (NBT.1 / NBT.2)

```text
Canonical CSV + v3.0 vault (repo) ──► drift evidence JSON / operator review
        │                                      │
        │                                      ▼
        └────────────────────────────► KiRBe / Supabase / Drive (mirrors only)
```

- **Canonical wins** on conflict (D-KSD-1). Mirrors never silently overwrite canonical rows.
- **Direction:** promotion flows canonical → mirror; reverse flow requires explicit operator approval and replay logs.

## Replay / drift artifact

- **Producer:** `scripts/kirbe_sync_daemon.py` (default dry-run).
- **Payload:** SHA-256 fingerprints and line counts for `baseline_organisation.csv` and `process_list.csv`; optional embedded result of `py scripts/validate_hlk.py`.
- **Storage:** operator-chosen path (stdout or `--output`). No secrets.

## Conflict policy

1. Detect drift (hash or structural diff vs last approved mirror snapshot).  
2. If mirror disagrees with canonical → **canonical wins**; open incident, resync mirror.  
3. Bulk CSV merge → follow [phase-canonical-csv-tranche-plan.md](../phase-canonical-csv-tranche-plan.md) approval gate.

## Action ID mapping

| Proposal ID | Design element |
|:------------|:---------------|
| NBT.1 | Stable machine-key policy for role/process sync (fingerprints + validate_hlk) |
| NBT.2 | Canonical-to-mirror ownership (this doc + daemon default dry-run) |
| NBT.3 | Safe `v3.0/` enrichments before CSV bulk (out of scope for daemon; tracked in CSV tranche) |
| NBT.4 | Approval-gated automation with deterministic replay (dry-run JSON; `--apply` gated, no in-repo writes) |
| NBT.5 | Madeira admin escalation timing (program dependency; not automated here) |

## K1 / K2 implementation notes

- **K1 (shipped):** dry-run CLI + tests (`tests/test_kirbe_sync_daemon.py`, `py scripts/test.py kirbe`).  
- **K2:** `--apply` requires `--i-approve-canonical-writes` **and** `KIRBE_SYNC_APPLY=1`; current build prints guidance and **does not** write canonical CSVs or external systems — operator performs mirror updates via approved runbooks.
