# Gateway repair evidence — post-reboot (2026-06-15)

**Proof class:** automated JSON  
**Artifact:** `artifacts/gateway-repair-post-reboot-2026-06-15.json`

## Outcome

- First single-attempt repairs after reboot: **FAIL** (~585s; http+rpc false)
- `--check-only` probes: **FAIL** when run too early
- **2-attempt** governed repair: **PASS** — warm path, `http_ready=true`, `rpc_ready=true`
- Follow-up `--check-only`: **PASS** (~14s)

## Governance binding

- Closes **CO-90-004** / **CO-MBH-005** at adapter layer only
- Does **not** close MADEIRA α0 (master synthesis anti-pattern #1)
- Week-2 mint target: PROOF_ADAPTER row `proof-openclaw-gateway-repair-json`
