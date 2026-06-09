---
report_type: neo4j-backup-retention-process
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Execution seat (Composer) — PKT-I95-F6-DOCS per thinking-seat 7b6fffee
status: active
stability_doctrine: neo4j_backup_governance
linked_charters:
  - i95-neo4j-free-backup-restore-charter-2026-06-09.md
  - i95-neo4j-credential-recovery-2026-06-09.md
ratifying_decisions:
  - D-IH-95-L
---

# I95 Neo4j Aura backup retention process (2026-06-09)

Governed backup handling for Aura graph exports — **stability doctrine**, not ad-hoc repo-root drops.

---

## Where backups live

| Rule | Binding |
|:---|:---|
| **Primary store** | Encrypted operator vault: `%USERPROFILE%\.openclaw\vault\neo4j-backups\` |
| **NOT git** | `*.backup` in `.gitignore`; never commit binaries |
| **NOT repo root** | Repo-root exports are incident-only staging; move in F6-R0 |
| **NOT unencrypted Drive** | Unless operator BitLocker/encrypted container path is documented |

---

## Naming convention

```
{instanceId}-{ISO8601UTC}-{instanceId}.backup
```

Example: `b6d76b10-2026-06-09T14-30-52-b6d76b10.backup`

---

## Retention policy

| Tier | Policy |
|:---|:---|
| **Rolling** | Keep last **3** exports after successful verify |
| **Annual** | Keep **1** archive export per calendar year |
| **Deletion** | Remove older exports only after SHA256 verify + restore-drill note |

---

## Manifest sidecar (required)

For each `.backup`, write `{basename}.sha256.json`:

```json
{
  "captured_at": "2026-06-09T14:30:52Z",
  "size_bytes": 315550,
  "source_instance_id": "b6d76b10",
  "sha256": "<hex>"
}
```

---

## Export triggers

Export **before**:

- Destroy / recreate Free instance
- Tier change (Free → Professional — funding-gated)
- Major dual-emit cutover when live graph state must be preserved beyond CSV projection

---

## Restore drill cadence

| Cadence | Action |
|:---|:---|
| **Quarterly** | Dry restore to scratch Free instance **or** doc-only drill when no Free slot |
| **Post-incident** | After any F6 restore, log drill outcome in initiative `reports/` |

---

## Cross-links

| Artifact | Link |
|:---|:---|
| F6 restore charter | [`i95-neo4j-free-backup-restore-charter-2026-06-09.md`](i95-neo4j-free-backup-restore-charter-2026-06-09.md) (F6-R0) |
| Credential recovery F5/F6 | [`i95-neo4j-credential-recovery-2026-06-09.md`](i95-neo4j-credential-recovery-2026-06-09.md) |
| Rebuildable projection | [`NEO4J_STRATEGY.md`](../../../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md) |
| Console restore limit | SRC-N4J-09 (<4 GB file upload) |

---

## Verification (operator)

```powershell
# After vault move — confirm not tracked
git status

# Optional SHA256 (PowerShell)
Get-FileHash -Path "$env:USERPROFILE\.openclaw\vault\neo4j-backups\b6d76b10-2026-06-09T14-30-52-b6d76b10.backup" -Algorithm SHA256
```
