---
language: en
status: active
intellectual_kind: incident_diagnosis
role_owner: System Owner
area: Tech / Holistik Ops
entity: Holistika Research
authority: System Owner
last_review: 2026-05-01
artifact_role: governed_evidence
topic_ids:
  - topic_holistik_ops_discovery
parent_topic: topic_holistik_ops_discovery
---

# Neo4j Aura authentication failure — diagnosis

**Incident id:** INC-NEO4J-AURA-AUTH-2026-05-01
**Blocks:** D-IH-32-Q (Neo4j live sync mandatory for P6 closure)
**State:** ROOT CAUSE CONFIRMED — operator-side credential mismatch
**Operator:** `User`
**Aura instance:** `neo4j+s://d7e409b4.databases.neo4j.io` (created 2026-04-30)

## Symptom

`py scripts/sync_hlk_neo4j.py` consistently returns `neo4j.exceptions.AuthError: {neo4j_code: Neo.ClientError.Security.Unauthorized}`. Operator reports the same error after:

1. Resetting the Aura password and re-saving `NEO4J_PASSWORD` in `~/.openclaw/.env`.
2. Provisioning a brand-new Aura instance from scratch and re-saving credentials.

## Diagnosis path

Three orthogonal layers tested:

### Layer 1 — Env loader (ruled out)

`akos.io.load_env_file` strips surrounding `'` and `"` quotes (line 102 of `akos/io.py`). Diagnostic:

```text
URI:      'neo4j+s://d7e409b4.databases.neo4j.io'
USER:     'neo4j'
TRUST:    'all'
PWD len:  43
PWD head: '87-4G'
PWD tail: 'qfBUk'
Has any whitespace: False
Has any quote: False
```

Env loads cleanly. `NEO4J_TRUST=all` correctly rewrites `neo4j+s://` → `neo4j+ssc://` at driver-init.

### Layer 2 — Bolt driver, 3 URI variants (ruled out)

| URI scheme | Result |
|---|---|
| `neo4j+s://` | `ServiceUnavailable: Unable to retrieve routing information` (TLS chain — known, that's why we ship `NEO4J_TRUST=all`) |
| `neo4j+ssc://` | `AuthError: Invalid credential` |
| `bolt+ssc://` | `AuthError: Invalid credential` |

TLS path is healthy (with `+ssc`). Auth fails identically on both bolt and routing-driver paths.

### Layer 3 — Aura HTTP Query API direct (root cause)

Bypasses the entire local stack. Raw HTTP POST with Basic auth straight to `https://d7e409b4.databases.neo4j.io/db/neo4j/query/v2`:

```text
HTTP 401 Unauthorized
{"errors":[{"code":"Neo.ClientError.Security.Unauthorized","message":"Invalid credential."}]}
```

This is **the Aura instance itself** rejecting the password. No code, driver, SSL, or env-loader layer is in between.

## Root cause

The password value stored in `~/.openclaw/.env` (`87-...-qfBUk`, length 43) is not the password the Aura instance has on file. Three things this can be in practice:

1. **Copy-paste truncation** — the Aura console "Reset password" modal renders the new password in a field that some browsers visually truncate. If you copy from the field instead of from the modal's "Copy" button, you may miss head or tail characters. The 43-character length matches the typical Aura format, so truncation isn't the most likely — but this would be invisible on inspection.
2. **Reset modal not confirmed** — Aura's reset-password modal requires clicking "Yes, reset". If the operator copied the new password from the modal but closed without confirming, Aura keeps the old one.
3. **Different account / region / orphaned instance** — if the Aura console shows multiple instances (a paused one + a new one), the URI may point at the wrong one. The `d7e409b4` host string in the URI must match the host string shown next to the new instance in the console.

## Recommended remediation (operator action, ~5 min)

1. Open `https://console.neo4j.io/`.
2. Confirm the visible Aura instance ID matches `d7e409b4.databases.neo4j.io` (compare to `NEO4J_URI` in `~/.openclaw/.env`).
3. If they don't match: update `NEO4J_URI` to `neo4j+s://<actual-id>.databases.neo4j.io`.
4. Click the instance → **Reset password** → wait for the modal → click the dedicated **Copy** button (not field-select-Ctrl+C) → paste into `NEO4J_PASSWORD` in `~/.openclaw/.env` (without surrounding quotes, but quotes also work — the loader strips them).
5. Confirm the modal's "Yes, save" / "Reset" button.
6. Re-run the diagnostic: `py c:\Users\Shadow\AppData\Local\Temp\neo4j_diag.py`. The `neo4j+ssc://` row should print `OK: x=1`.

## What I did NOT do (and why)

I did not attempt to reset the Aura password from this side. Aura console requires interactive auth (Google/GitHub/email-link), which is not safely automatable from this agent. The operator's Aura account credentials are not in scope.

## Once auth is fixed (one-shot, ~30s)

```powershell
py scripts/sync_hlk_neo4j.py        # idempotency proof — first run
py scripts/sync_hlk_neo4j.py        # idempotency proof — second run, must match
```

Then promote this evidence note's twin: `reports/p6-neo4j-live-sync-evidence-2026-05-01.md` with the two Cypher count outputs side-by-side. That closes D-IH-32-Q.

## Cross-references

- Original 5-phase Neo4j P6 plan: `master-roadmap.md` § P6
- Decision context: D-IH-32-Q in `decision-log.md`
- Code paths exercised: `akos/hlk_neo4j.py` `_resolve_driver`, `akos/io.py` `load_env_file`
- Diagnostic script: `c:\Users\Shadow\AppData\Local\Temp\neo4j_diag.py` (3-variant prober)
