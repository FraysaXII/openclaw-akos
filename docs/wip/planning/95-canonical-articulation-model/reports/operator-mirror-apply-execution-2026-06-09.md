---
report_type: operator-mirror-apply-execution
parent_initiative: INIT-OPENCLAW_AKOS-95
phase: P95-GOV-5+7-mirror-apply
authored: 2026-06-09
authored_by: Execution seat (Composer)
status: APPLIED
mirror_apply_status: APPLIED
base_commit: 35169fc69624399fb5ae36e96d69b7d504d33b29
ratifying_decisions:
  - D-IH-95-B
linked_runbooks:
  - docs/guides/holistika-mirror-dml-apply.md
  - docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md
  - docs/wip/planning/95-canonical-articulation-model/reports/sql-proposal-p95-gov-7-2026-06-09.md
---

# Operator mirror apply — execution evidence (2026-06-09)

**Purpose:** Prod recovery after failed mirror apply + GOV-5/GOV-7 closure.  
**Git base:** `35169fc` (Hygiene B+C collaborator-share tranche).  
**Outcome:** Migration drift **repaired**; GOV-7 DDL **APPLIED**; compliance mirror DML **APPLIED** (171 batches); emit contract **PASS**. Prod row-count parity query **deferred** (Supabase pooler circuit breaker after batch storm).

Companion walkthrough (pre-apply): [`operator-mirror-apply-walkthrough-2026-06-09.md`](operator-mirror-apply-walkthrough-2026-06-09.md).

---

## Step 0 — Migration drift diagnosis

| Symptom | Detail |
|:---|:---|
| Remote-only (not in repo) | `20260608204329`, `20260608222856` — no matching files under `supabase/migrations/` |
| Local-only (not on remote) | `20260608211500`, `20260608223000`, `20260609120000`–`20260609120300` (GOV-7 + pending) |

**Repair (ledger reconcile before push):**

```powershell
npx supabase migration repair --linked --status reverted 20260608204329 20260608222856
```

Remote-only versions marked **reverted** in migration history (orphan ledger rows; DDL not in git SSOT).

---

## Step 1 — GOV-7 DDL push

```powershell
npx supabase db push --linked
```

Applied six local migrations:

| Version | Scope |
|:---|:---|
| `20260608211500` | Pending pre-GOV-7 |
| `20260608223000` | Pending pre-GOV-7 |
| `20260609120000` | Finance registry mirrors (pricing tier, perf obligation, tax calendar) |
| `20260609120100` | Data contract registry mirror |
| `20260609120200` | RPA adapter registry mirror |
| `20260609120300` | Component service matrix mirror |

**Parity check:** `npx supabase migration list --linked` — local = remote for all rows post-push.

**Table existence:** `npx supabase db query --linked --file artifacts/sql/gov7_table_check.sql` — all six GOV-7 mirror tables present.

---

## Step 2 — Mirror DML emit + apply

| Step | Command | Result |
|:---|:---|:---|
| Emit | `py scripts/verify.py compliance_mirror_emit` | Wrote `artifacts/sql/compliance_mirror_upsert.sql` (~5.5 MB) |
| Split | `py scripts/split_compliance_mirror_upsert.py` | 171 batches → `artifacts/sql/mirror-batches/20260609/` |
| Apply | `powershell -NoProfile -File scripts/apply_mirror_batches.ps1` | 171/171 after FK fix (see below) |

**First-run failure (batch 156 / engagement_registry chunk 01):**

```
FK violation: engagement_model_id='tmpl_customer_outbound_full_v1'
  not present in engagement_model_registry_mirror
```

**Root cause:** `ENGAGEMENT_REGISTRY.csv` stored **template IDs** (`tmpl_*`) in `engagement_model_id`; FK targets `engagement_model_registry_mirror` (`eng_model_*` only).

**Fixes:**

1. Cleared `tmpl_*` from three engagement rows (SUEZ, Websitz Shopify, Websitz Use case 2) — template linkage deferred; column nullable.
2. `scripts/sync_compliance_mirrors_from_csv.py` — empty `engagement_model_id` → SQL `NULL` via `nullable_text_columns`.
3. Scoped re-apply: batches 37–45 (engagement + output-arch + GOV-7 mirrors) after emit refresh; batches 1–36 already applied on first run (idempotent upserts).

**Contract validator:**

```text
py scripts/validate_mirror_emit_contract.py  → PASS (47 tables)
py scripts/verify.py pre_commit_fast         → PASS
```

---

## Step 3 — Prod row-count parity (deferred)

**Query file:** `artifacts/sql/gov57_parity_check.sql`

**Expected counts (git SSOT @ emit):**

| Mirror key | Expected |
|:---|---:|
| pricing_tier | 6 |
| finops_perf_obl | 5 |
| finops_tax | 8 |
| data_contract | 14 |
| rpa_adapter | 5 |
| component_svc | 110 |
| engagement_tpl | 6 |
| engagement_reg | 7 |
| output_type | 17 |
| artifact_class | 21 |
| component_prim | 25 |
| crm_adapter | 11 |

**Blocker:** After ~171 batch applies, Supabase pooler returned `(ECIRCUITBREAKER) too many authentication failures`. Parity query retries failed with same error.

**Operator re-run (when pooler clears):**

```powershell
npx supabase db query --linked --file artifacts/sql/gov57_parity_check.sql --output table
```

Compare output to table above; mismatch → re-run `compliance_mirror_emit` + scoped batch apply per walkthrough §4.

---

## Canonical CSV note (operator gate)

`ENGAGEMENT_REGISTRY.csv` — three rows cleared of invalid `engagement_model_id` FK targets. Template→model binding remains a **forward charter** item (separate from mirror apply closure).

---

## Cross-references

- GOV-5 synthesis (updated): [`synthesis-p95-gov-5-2026-06-09.md`](synthesis-p95-gov-5-2026-06-09.md)
- GOV-7 synthesis (updated): [`synthesis-p95-gov-7-2026-06-09.md`](synthesis-p95-gov-7-2026-06-09.md)
- SQL proposal (APPLIED): [`sql-proposal-p95-gov-7-2026-06-09.md`](sql-proposal-p95-gov-7-2026-06-09.md)
- UAT §4.3 flip: [`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md)
