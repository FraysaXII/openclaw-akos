---
report_type: neo4j-credential-recovery
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Execution seat (Composer)
status: active
verdict: OPERATOR-ACTION-REQUIRED
---

# I95 Neo4j Aura credential recovery (2026-06-09)

**Symptom:** `py artifacts/sql/run_cq_uat.py` and `py scripts/sync_hlk_neo4j.py` return `AuthError: Unauthorized` after operator re-saved `~/.openclaw/.env`.

**Probe:** `py scripts/neo4j_connectivity_probe.py` → **FAIL** (`classification: wrong_password_or_user`).

---

## Env loading trace (all entrypoints)

| Script / module | Bootstrap | Env file read | Repo `.env` | Process env precedence |
|:---|:---|:---|:---|:---|
| `artifacts/sql/run_cq_uat.py` | `bootstrap_openclaw_process_env()` | `~/.openclaw/.env` | not used | Neo4j keys from file **override** stale shell values (2026-06-09 fix in `akos/io.py`) |
| `scripts/sync_hlk_neo4j.py` | same | same | not used | same |
| `akos/hlk_neo4j.py` | none (reads `os.environ` after bootstrap) | — | — | uses `NEO4J_URI`, `NEO4J_USERNAME` (optional), `NEO4J_PASSWORD`, `NEO4J_TRUST`, `NEO4J_CA_BUNDLE` |
| `scripts/serve-api.py` | `load_runtime_env` + `set_process_env_defaults` | `~/.openclaw/.env` | not used | unset keys only (no Neo4j force override) |

**This session:** `~/.openclaw/.env` exists; repo root `.env` absent. All four Neo4j vars present in file. No stale process env blocked file load.

---

## Root cause (confirmed)

| Layer | Finding |
|:---|:---|
| Env loader | **Ruled out** — file loads; password length 43; no stray quotes/whitespace |
| TLS | **Ruled out** — `NEO4J_TRUST=all` rewrites `neo4j+s` → `neo4j+ssc`; Bolt reaches Aura |
| Username | **Misconfigured** — `NEO4J_USERNAME=b6d76b10` is the Aura **instance id**, not a DB user. Code now auto-heals to `neo4j` with a warning (`akos/hlk_neo4j._resolve_neo4j_username`). |
| Password | **Primary blocker** — Bolt auth fails for both `neo4j` and `b6d76b10`; Aura rejects the password on file (same pattern as INC-NEO4J-AURA-AUTH-2026-05-01). |

N3 dual-emit success at `2802ef8` likely used a **valid password at that time**; current `~/.openclaw/.env` password does not match what Aura has on file (reset not confirmed, copy-paste error, or wrong instance).

---

## Code fixes landed (2026-06-09)

1. **`scripts/neo4j_connectivity_probe.py`** — leak-safe env trace + `RETURN 1` + Aura HTTP probe + classification.
2. **`akos/io.py`** — Neo4j keys in `~/.openclaw/.env` override stale process env when non-empty.
3. **`akos/hlk_neo4j.py`** — heal instance-id-as-username misconfiguration.

---

## GitHub Actions secret alignment

| Workflow | Secrets / env | Code expectation | Gap |
|:---|:---|:---|:---|
| [`neo4j-aura-keepalive.yml`](../../../../.github/workflows/neo4j-aura-keepalive.yml) | `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` | matches `get_neo4j_driver` | none — keepalive uses inline Python, not `bootstrap_openclaw_process_env`; defaults username to `neo4j` if secret empty |
| [`neo4j-graph-integration.yml`](../../../../.github/workflows/neo4j-graph-integration.yml) | inline `bolt://127.0.0.1:7687` + `neo4j` / `neo4jintegrationci` | local Docker only | N/A for Aura |
| CQ UAT | no dedicated workflow | operator `~/.openclaw/.env` | by design |

**Operator:** after fixing local `.env`, update repo secrets **`NEO4J_URI`**, **`NEO4J_USERNAME`** (use `neo4j` unless custom user), **`NEO4J_PASSWORD`** so keepalive does not silently skip or fail.

---

## Operator recovery — Option 1 (Aura console)

Per [Neo4j Aura connect docs](https://neo4j.com/docs/aura/getting-started/connect-instance/#_instance_credentials):

1. Open [Neo4j Aura console](https://console.neo4j.io/).
2. Confirm instance host matches `NEO4J_URI` host (`b6d76b10.databases.neo4j.io` in this session).
3. **Reset password** → use modal **Copy** button → paste into `NEO4J_PASSWORD` in `~/.openclaw/.env` (quotes optional; loader strips them).
4. Set `NEO4J_USERNAME=neo4j` (or create a dedicated user below).
5. Re-run: `py scripts/neo4j_connectivity_probe.py` → expect exit **0**.
6. Then: `py artifacts/sql/run_cq_uat.py` → expect exit **0**.

### Optional: dedicated CI user (Aura Query UI)

When authenticated as an admin user, run in Aura **Query**:

```cypher
CREATE USER cicd-akos SET PASSWORD 'REPLACE_WITH_STRONG_PASSWORD' CHANGE NOT REQUIRED;
```

Or `aic-madeira` if that naming fits your RBAC plan. Then set:

- `~/.openclaw/.env`: `NEO4J_USERNAME=cicd-akos`, `NEO4J_PASSWORD=…`
- GitHub repo secrets: `NEO4J_USERNAME`, `NEO4J_PASSWORD` (names only in audit; values in secret store)

Agent cannot create Aura users without working auth — steps are operator-only until probe passes.

---

## Verification commands

```powershell
py scripts/neo4j_connectivity_probe.py
py artifacts/sql/run_cq_uat.py
py scripts/sync_hlk_neo4j.py --dry-run --dual-emit
```

---

## Cross-references

- Prior incident: [`neo4j-aura-auth-diagnosis-2026-05-01.md`](../../32-holistik-ops-maturation/reports/neo4j-aura-auth-diagnosis-2026-05-01.md)
- CQ UAT: [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md)
