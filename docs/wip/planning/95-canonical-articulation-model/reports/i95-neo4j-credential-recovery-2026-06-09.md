---
report_type: neo4j-credential-recovery
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Execution seat (Composer)
status: active
verdict: OPERATOR-ACTION-REQUIRED
aura_tier: free
---

# I95 Neo4j Aura credential recovery (2026-06-09)

**Symptom:** `py artifacts/sql/run_cq_uat.py` and `py scripts/sync_hlk_neo4j.py` return `AuthError: Unauthorized` after operator re-saved `~/.openclaw/.env`.

**Probe:** `py scripts/neo4j_connectivity_probe.py` → **FAIL** (`classification: wrong_password_or_user`).

**Instance tier (operator-confirmed):** **Aura Free** — single `neo4j` user only; no RBAC / user-management Cypher.

---

## Operator correction — prior guidance was wrong (research gap)

The 2026-06-09 first draft of this report cited generic Aura docs (**Option 1: console password reset** + **optional `CREATE USER` for a dedicated CI user**). The operator proved both paths are **misleading on Aura Free**:

| Prior claim | Operator finding |
|:---|:---|
| Reset password in Aura console | Aura Free has **no in-console password reset** for the live instance; clone is the supported recovery path |
| Run `CREATE USER` in Query tab | Returns **`42NFF` access denied** — user management blocked on Free tier |
| Use instance id as username | Wrong — username is always lowercase **`neo4j`** on Aura |

**Apology / doctrine gap:** That draft did not meet the **research-to-decision bar** (the discipline that requires external sources and tier-specific verification before operator-facing recovery steps ship). Generic Neo4j Aura connect docs describe paid-tier RBAC; they do **not** state Aura Free blocks `CREATE USER` / `SHOW USERS`. This rewrite incorporates operator findings as binding doctrine. Future recovery edits must cite **tier** (Free vs Enterprise) before recommending Cypher or console actions.

---

## Aura Free tier doctrine (binding — operator findings)

### 1. User management is blocked

On **Aura Free**, the following return **`42NFF` access denied**:

- `CREATE USER`
- `DROP USER`
- `SHOW USERS`

There is **no system database access**. The instance exposes a **single** database user: **`neo4j`**. Multi-user RBAC requires **paid Aura Enterprise** (or self-hosted Neo4j Enterprise).

**Do not** recommend `CREATE USER`, dedicated CI users, or Option-1-style generic Aura password-reset flows for **Free** instances.

### 2. Connection rules (all Aura tiers)

| Setting | Correct value | Wrong value |
|:---|:---|:---|
| URI scheme | `neo4j+s://` | `bolt://` (TLS mismatch on Aura) |
| Username | lowercase `neo4j` | Aura **instance id** (e.g. `b6d76b10`) |
| Password | From credentials file or **clone** output | Stale copy, wrong instance, or post-reset mismatch |

Optional: `NEO4J_TRUST=all` rewrites `neo4j+s` → `neo4j+ssc` when corporate TLS inspection requires it (see env trace below).

### 3. Aura Free recovery paths only

Use **one** of these — in order of preference:

#### Path A — Clone instance (recommended password reset)

1. Open [Neo4j Aura console](https://console.neo4j.io/).
2. Select the instance whose host matches `NEO4J_URI` (this session: `b6d76b10.databases.neo4j.io`).
3. **Clone** the instance → Aura issues a **new credentials file** (this is the supported way to obtain a fresh password on Free tier).
4. Copy password from the credentials file into `NEO4J_PASSWORD` in `~/.openclaw/.env` (loader strips optional quotes).
5. Set `NEO4J_USERNAME=neo4j`.
6. Update GitHub repo secrets (names only here): `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`.
7. Re-run: `py scripts/neo4j_connectivity_probe.py` → expect exit **0**.

After clone, update `NEO4J_URI` if the clone’s host differs from the old instance.

#### Path B — Browser password test (confirm password before env edit)

1. In Aura **Browser** → **Query** tab, run `:server disconnect`.
2. Manually log in with username **`neo4j`** and the password you believe is correct (from credentials file or clone).
3. If login fails, password is wrong — use **Path A (clone)**; do not attempt `CREATE USER`.

#### Path C — NOT valid on Aura Free

- **`CREATE USER`** in Query tab
- Generic Aura docs **Option 1** “reset password” / “create dedicated user” without tier check

---

## Root cause (confirmed — env + auth)

| Layer | Finding |
|:---|:---|
| Env loader | **Ruled out** — `~/.openclaw/.env` loads; password length 43; no stray quotes/whitespace |
| TLS | **Ruled out** — `NEO4J_TRUST=all` rewrites `neo4j+s` → `neo4j+ssc`; Bolt reaches Aura |
| Username | **Misconfigured** — `NEO4J_USERNAME=b6d76b10` is the Aura **instance id**, not a DB user. Code auto-heals to `neo4j` with a warning (`akos/hlk_neo4j._resolve_neo4j_username`). |
| Password | **Primary blocker** — Bolt auth fails for both `neo4j` and `b6d76b10`; password on file does not match Aura (stale credentials, wrong instance, or never refreshed via clone). |
| Tier | **Aura Free** — no in-console password reset; clone or credentials-file password is the recovery surface |

N3 dual-emit success at `2802ef8` likely used a **valid password at that time**; current `~/.openclaw/.env` password does not match what Aura accepts now.

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

## AKOS wiring (after recovery)

| Surface | Variables | Notes |
|:---|:---|:---|
| Local operator env | `~/.openclaw/.env` | `NEO4J_URI`, `NEO4J_USERNAME=neo4j`, `NEO4J_PASSWORD` |
| GitHub Actions | Secrets `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` | Keepalive workflow; values in secret store only — never log |
| Probe | `py scripts/neo4j_connectivity_probe.py` | Exit **0** required before CQ UAT or live sync |

---

## Code fixes landed (2026-06-09)

1. **`scripts/neo4j_connectivity_probe.py`** — leak-safe env trace + `RETURN 1` + Aura HTTP probe + classification.
2. **`akos/io.py`** — Neo4j keys in `~/.openclaw/.env` override stale process env when non-empty.
3. **`akos/hlk_neo4j.py`** — heal instance-id-as-username misconfiguration.

---

## GitHub Actions secret alignment

| Workflow | Secrets / env | Code expectation | Gap |
|:---|:---|:---|:---|
| [`neo4j-aura-keepalive.yml`](../../../../.github/workflows/neo4j-aura-keepalive.yml) | `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` | matches `get_neo4j_driver` | none — keepalive defaults username to `neo4j` if secret empty |
| [`neo4j-graph-integration.yml`](../../../../.github/workflows/neo4j-graph-integration.yml) | inline `bolt://127.0.0.1:7687` + `neo4j` / `neo4jintegrationci` | local Docker only | N/A for Aura |
| CQ UAT | no dedicated workflow | operator `~/.openclaw/.env` | by design |

---

## Appendix — paid tier / self-hosted / Enterprise only

**Not applicable to Aura Free.** Use only when the instance is **Aura Enterprise**, **Aura Professional** with RBAC enabled, or **self-hosted Neo4j Enterprise**.

### Correct Cypher syntax (hyphenated usernames need backticks)

```cypher
CREATE USER `aic-madeira` IF NOT EXISTS
SET PASSWORD 'password'
CHANGE NOT REQUIRED;
```

Notes:

- `IF NOT EXISTS` follows the username.
- Hyphenated usernames **must** be backtick-quoted.
- Requires admin privileges and a tier that allows user management.

Example dedicated CI user (paid/self-hosted only):

```cypher
CREATE USER `cicd-akos` IF NOT EXISTS
SET PASSWORD 'REPLACE_WITH_STRONG_PASSWORD'
CHANGE NOT REQUIRED;
```

Then set `NEO4J_USERNAME=cicd-akos` in `~/.openclaw/.env` and matching GitHub secrets.

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
- CQ UAT (blocked on auth): [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md)
- E2e cutover charter: [`i95-neo4j-e2e-cutover-charter-2026-06-09.md`](i95-neo4j-e2e-cutover-charter-2026-06-09.md)
