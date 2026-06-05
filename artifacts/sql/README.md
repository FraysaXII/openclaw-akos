# Generated SQL (gitignored)

Emit step writes upsert SQL here for operator review. **Do not commit `*.sql`.**

## Apply (after emit)

**Preferred (linked repo):** [`docs/guides/holistika-mirror-dml-apply.md`](../../docs/guides/holistika-mirror-dml-apply.md)

```powershell
# Full bundle emit
py scripts/verify.py compliance_mirror_emit

# Apply chunk directory (example: dated mirror-batches folder)
pwsh -File scripts/apply_mirror_batches.ps1 -BatchDir "artifacts/sql/mirror-batches/20260504"
```

**OPS-86-15 five-table gap:**

```powershell
py scripts/verify.py ops8615_mirror_emit
pwsh -File scripts/apply_mirror_batches.ps1 -Preset ops8615
```
