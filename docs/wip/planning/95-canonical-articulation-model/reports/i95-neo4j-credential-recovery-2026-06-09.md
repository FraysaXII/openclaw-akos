---
report_type: neo4j-credential-recovery
parent_initiative: INIT-OPENCLAW_AKOS-95
lane: L4-HCAM-P2-Neo4j
authored: 2026-06-09
authored_by: Execution seat (Composer) — RA-1 rewrite per thinking-seat 5b1b3f98
status: active
verdict: OPERATOR-ACTION-REQUIRED
aura_tier: free
incident_class: aura_free_credential_misguidance
linked_research_sources:
  - docs/wip/planning/95-canonical-articulation-model/reports/i95-neo4j-aura-free-recovery-source-ledger.csv
---

# I95 Neo4j Aura Free credential recovery (2026-06-09)

**Symptom:** `py artifacts/sql/run_cq_uat.py` and `py scripts/sync_hlk_neo4j.py` return `AuthError: Unauthorized` after operator re-saved `~/.openclaw/.env`.

**Probe:** `py scripts/neo4j_connectivity_probe.py` → **FAIL** (`classification: wrong_password_or_user`).

**Instance tier (operator-confirmed):** **Aura Free** — single `neo4j` user only; no RBAC / user-management Cypher; trial-expired UI; **one Free instance per account**.

**Research action:** [`i95-neo4j-aura-free-recovery-research-2026-06-09.md`](i95-neo4j-aura-free-recovery-research-2026-06-09.md) (source ledger + synthesis; governs paths below).

---

## Operator correction — prior guidance was wrong (research gap)

The 2026-06-09 first draft of this report cited generic Aura docs (**Option 1: console password reset** + **optional `CREATE USER` for a dedicated CI user**) and later recommended **Clone instance** as Path A **without a paid-tier warning**. The operator proved all three are **misleading on Aura Free**:

| Prior claim | Operator finding |
|:---|:---|
| Reset password in Aura console | Aura Free has **no in-console DB password reset** for the live instance |
| **Clone instance (recommended)** | Clone-to-new targets **Professional** (~**$65/mo** minimum); accounts allow **only one Free instance** — not a $0 recovery path |
| Run `CREATE USER` in Query tab | Returns **`42NFF` access denied** — user management blocked on Free tier |
| Use instance id as username | Wrong — username is always lowercase **`neo4j`** on Aura |

**Apology / doctrine gap:** Those drafts did not meet the **research-to-decision bar** (external sources + tier-specific verification before operator-facing recovery steps ship). Generic Neo4j Aura connect docs describe paid-tier RBAC; they do **not** state Aura Free blocks `CREATE USER` / `SHOW USERS` or that clone implies Professional billing. This rewrite incorporates operator findings + applied research (RA-1/RA-2) as binding doctrine. Future recovery edits must cite **tier** (Free vs Enterprise) before recommending Cypher, console, or clone actions.

**Incident class (future validator hook):** `aura_free_credential_misguidance` — recommend paid clone/upgrade without opt-in; cite CREATE USER on Free; cite May 2026 paid-tier console-reset advice for Free instances.

---

## DO NOT on Aura Free without explicit operator opt-in

> **STOP — these paths are NOT Free-tier recovery. Do not recommend without the cost disclosure + operator billing opt-in.**

| Action | Why blocked on Free | Cost signal |
|:---|:---|:---|
| **Clone → new instance** | Official migration tutorial: clone works for **AuraDB Professional**; one Free instance per account → clone-to-new cannot stay Free | **~$65/mo** minimum (1 GB Professional; [Neo4j pricing](https://neo4j.com/pricing/)) |
| **Upgrade instance** (Free → Professional) | Console **Upgrade** button changes billing tier | Same **~$65/mo+** |
| **`CREATE USER` / dedicated CI user** | `42NFF` access denied on Free | Requires **paid RBAC** tier for production multi-user patterns |
| **Console DB password reset** (from [`INC-NEO4J-AURA-AUTH-2026-05-01`](../../32-holistik-ops-maturation/reports/neo4j-aura-auth-diagnosis-2026-05-01.md)) | That incident doc assumed paid-tier UI — **superseded for Free** by this report | N/A — UI absent on Free |
| **Support ticket password reset** | Neo4j KB: *“Aura Support cannot recover or reset an Aura Instance password”* | No recovery path |

**Mandatory disclosure before any clone/upgrade recommendation:** estimated **$65–66/mo** + new URI + explicit operator opt-in. Never label clone as “recommended” without this box.

---

## Aura Free tier doctrine (binding)

### User management is blocked

On **Aura Free**, the following return **`42NFF` access denied**:

- `CREATE USER`
- `DROP USER`
- `SHOW USERS`

There is **no system database access**. The instance exposes a **single** database user: **`neo4j`**. Multi-user RBAC requires **paid Aura Enterprise / Business Critical** (or self-hosted Neo4j Enterprise).

### Connection rules (all Aura tiers)

| Setting | Correct value | Wrong value |
|:---|:---|:---|
| URI scheme | `neo4j+s://` | `bolt://` (TLS mismatch on Aura) |
| Username | lowercase `neo4j` | Aura **instance id** (e.g. `b6d76b10`) |
| Password | From credentials file, Browser change, or F5 rebuild output | Stale copy, wrong instance, or post-reset mismatch |

Optional: `NEO4J_TRUST=all` rewrites `neo4j+s` → `neo4j+ssc` when corporate TLS inspection requires it.

### Free-tier recovery paths only (F1–F5)

Use **one** of these — in order of preference. All are **$0** on Free tier.

#### F1 — Resume paused instance (same credentials)

Aura Free **auto-pauses after 72 hours with no writes**. Reads do not prevent pause.

1. Open [Neo4j Aura console](https://console.neo4j.io/).
2. If instance status is **Paused**, click **Resume**.
3. Re-use password from the **original credentials file** (F2) — pause does not rotate password.
4. Re-run: `py scripts/neo4j_connectivity_probe.py` → expect exit **0**.

Source: [Aura Free FAQ](https://support.neo4j.com/s/article/16094506528787-Support-resources-and-FAQ-for-Aura-Free-Tier).

#### F2 — Recover one-time credentials file

Neo4j shows the DB password **once** at instance creation. It is **never stored** by Neo4j.

1. Search operator machine / password manager for the `.txt` credentials file from instance creation.
2. Copy password into `NEO4J_PASSWORD` in `~/.openclaw/.env`; set `NEO4J_USERNAME=neo4j`.
3. Sync GitHub secrets: `NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD`.
4. Re-probe.

Source: [Aura DB authentication KB](https://support.neo4j.com/s/article/6787460237843-Neo4j-Aura-Database-Authentication-Neo4j-Database-Username-Password).

#### F3 — Browser password test (confirm before env edit)

1. In Aura **Browser** → **Query** tab, run `:server disconnect`.
2. Log in with username **`neo4j`** and the password you believe is correct (from F2).
3. If login fails, password is wrong — proceed to F5 (or operator AskQuestion if non-CSV graph state must be preserved); **do not** attempt `CREATE USER` or clone without opt-in.

#### F4 — Change password when current password is known

When F3 login **succeeds** but env file is stale:

1. In Aura Browser/Query: `:server change-password` (set new password per prompt).
2. Update `NEO4J_PASSWORD` in `~/.openclaw/.env` + GitHub secrets.
3. Re-probe.

This is **not** a console “Reset password” button — it requires knowing the current DB password.

Sources: [Aura DB authentication KB](https://support.neo4j.com/s/article/6787460237843-Neo4j-Aura-Database-Authentication-Neo4j-Database-Username-Password); [Browser `:server change-password`](https://neo4j.com/docs/browser/legacy/reference-commands/).

#### F5 — AKOS CSV projection rebuild ($0; loses non-CSV graph state)

When password is **lost** and F2/F3 fail — Neo4j has **no Free-tier support/console reset** ([KB 360037061874](https://support.neo4j.com/s/article/360037061874-How-to-recover-a-lost-Aura-Instance-s-password-in-Neo4j-Aura)).

Holistika doctrine: Neo4j is a **rebuildable projection**; git-canonical CSVs are SSOT ([`NEO4J_STRATEGY.md`](../../../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md)). N3 dual-emit at `2802ef8` proved live sync when auth worked.

1. **Destroy** the current Free instance in Aura console (or create account slot — only one Free instance allowed).
2. **Create** a new Aura Free instance → **Download** credentials file before Continue (F2 window).
3. Set `NEO4J_URI`, `NEO4J_USERNAME=neo4j`, `NEO4J_PASSWORD` in `~/.openclaw/.env` + GitHub secrets.
4. Re-probe → `py scripts/sync_hlk_neo4j.py --dual-emit` (or `--dry-run` first).
5. Re-run CQ UAT: `py artifacts/sql/run_cq_uat.py`.

**Data loss scope:** Only graph state **not** in CSV projection (e.g. `_KeepAlive` keepalive nodes, ad-hoc Cypher). Governance CSVs + sync script restore the governed graph.

---

## Root cause (confirmed — env + auth)

| Layer | Finding |
|:---|:---|
| Env loader | **Ruled out** — `~/.openclaw/.env` loads; password length 43; no stray quotes/whitespace |
| TLS | **Ruled out** — `NEO4J_TRUST=all` rewrites `neo4j+s` → `neo4j+ssc`; Bolt reaches Aura |
| Username | **Misconfigured** — `NEO4J_USERNAME=b6d76b10` is the Aura **instance id**, not a DB user. Code auto-heals to `neo4j` with a warning (`akos/hlk_neo4j._resolve_neo4j_username`). |
| Password | **Primary blocker** — Bolt auth fails for both `neo4j` and `b6d76b10`; password on file does not match Aura (stale credentials, wrong instance, or never refreshed). |
| Tier | **Aura Free** — no in-console DB password reset; F1–F5 are the only AKOS-governed recovery surface |

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

Keepalive is **architecturally correct** for Free pause doctrine (writes prevent 72h pause); **operational PASS unverified** in-repo — workflow skips if secrets unset. Check GitHub Actions history for `neo4j-aura-keepalive` after recovery.

---

## Research provenance

### Internal precedents

| ID | Artifact | Relevant finding |
|:---|:---------|:-----------------|
| **INC-NEO4J-AURA-AUTH-2026-05-01** | [`neo4j-aura-auth-diagnosis-2026-05-01.md`](../../32-holistik-ops-maturation/reports/neo4j-aura-auth-diagnosis-2026-05-01.md) | HTTP 401 = password mismatch; recommended console Reset — **paid-tier only; superseded for Free** |
| **p1-neo4j-preflight** | [`p1-neo4j-preflight-blocked-2026-06-01.md`](../../91-enterprise-graph-store-coverage/reports/p1-neo4j-preflight-blocked-2026-06-01.md) | BLOCKED-ENV |
| **I95 cutover** | [`i95-neo4j-cutover-execution-2026-06-09.md`](i95-neo4j-cutover-execution-2026-06-09.md) | N3 dual-emit APPLIED when auth worked |
| **D-IH-95-G R2-09** | [`decision-log.md`](../decision-log.md) | Free keepalive + budget ~$65/mo Professional |
| **NEO4J_STRATEGY** | [`NEO4J_STRATEGY.md`](../../../../../docs/references/hlk/v3.0/Envoy%20Tech%20Lab/Neo4j/NEO4J_STRATEGY.md) | Rebuildable projection — F5 doctrine |

### External sources (ledger IDs)

Full ratings in [`i95-neo4j-aura-free-recovery-source-ledger.csv`](i95-neo4j-aura-free-recovery-source-ledger.csv). Load-bearing URLs:

- [Lost password KB](https://support.neo4j.com/s/article/360037061874-How-to-recover-a-lost-Aura-Instance-s-password-in-Neo4j-Aura) — no support reset
- [Aura DB auth KB](https://support.neo4j.com/s/article/6787460237843-Neo4j-Aura-Database-Authentication-Neo4j-Database-Username-Password) — one-time credentials
- [Aura Free FAQ](https://support.neo4j.com/s/article/16094506528787-Support-resources-and-FAQ-for-Aura-Free-Tier) — pause/resume
- [migration-free](https://neo4j.com/docs/aura/tutorials/migration-free/) — clone = Professional
- [Neo4j pricing](https://neo4j.com/pricing/) — ~$65/mo Professional floor

---

## Appendix — paid tier / self-hosted / Enterprise only

**Not applicable to Aura Free.** Use only when the instance is **Aura Enterprise**, **Aura Professional** with RBAC enabled, or **self-hosted Neo4j Enterprise** — and only after operator billing opt-in where applicable.

```cypher
CREATE USER `cicd-akos` IF NOT EXISTS
SET PASSWORD 'REPLACE_WITH_STRONG_PASSWORD'
CHANGE NOT REQUIRED;
```

Hyphenated usernames **must** be backtick-quoted. Requires admin privileges and a tier that allows user management.

---

## Verification commands

```powershell
py scripts/neo4j_connectivity_probe.py
py artifacts/sql/run_cq_uat.py
py scripts/sync_hlk_neo4j.py --dry-run --dual-emit
```

---

## Cross-references

- Research action: [`i95-neo4j-aura-free-recovery-research-2026-06-09.md`](i95-neo4j-aura-free-recovery-research-2026-06-09.md)
- Prior incident (paid-tier advice superseded for Free): [`neo4j-aura-auth-diagnosis-2026-05-01.md`](../../32-holistik-ops-maturation/reports/neo4j-aura-auth-diagnosis-2026-05-01.md)
- CQ UAT (blocked on auth): [`i95-neo4j-cq-uat-2026-06-09.md`](i95-neo4j-cq-uat-2026-06-09.md)
- E2e cutover charter: [`i95-neo4j-e2e-cutover-charter-2026-06-09.md`](i95-neo4j-e2e-cutover-charter-2026-06-09.md)
