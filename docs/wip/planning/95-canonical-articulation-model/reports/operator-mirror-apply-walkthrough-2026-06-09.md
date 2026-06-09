---
report_type: operator-walkthrough
parent_initiative: INIT-OPENCLAW_AKOS-95
phase: P95-GOV-5+7-mirror-apply
authored: 2026-06-09
authored_by: System Owner (execution seat)
status: walkthrough-only
mirror_apply_status: PENDING-OPERATOR
base_commit: 1bc2d1d
ratifying_decisions:
  - D-IH-95-B
linked_runbooks:
  - docs/guides/holistika-mirror-dml-apply.md
  - docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md
  - docs/wip/planning/95-canonical-articulation-model/reports/sql-proposal-p95-gov-7-2026-06-09.md
---

# Operator mirror apply walkthrough — P95 GOV-5 + GOV-7 (2026-06-09)

**Purpose:** Step-by-step prod apply for the universal canonical governance wave mirror follow-up.
**Git base:** `1bc2d1d` (P95-GOV-8 closure UAT).
**Session outcome:** **Walkthrough-only** — Supabase auth token and database URL were not present in this
environment; prod DDL push and DML apply were **not executed**.

## Credential preflight (this session)

| Check | Result |
|:---|:---|
| `.env` at repo root | absent |
| `SUPABASE_ACCESS_TOKEN` | unset |
| `DATABASE_URL` | unset |
| `supabase/.temp/project-ref` (linked project) | present |

**Operator must** run `npx supabase login` and confirm link before Phase B.

---

## Scope inventory

### Phase A — GOV-5 emit surfaces (DML only; DDL already on prod from I72/I70/I86)

| Git CSV / surface | Mirror table | Expected rows (git @ `1bc2d1d`) |
|:---|:---|---:|
| 8 Reach/RevOps/Billing adapters | `compliance.{crm,revops,email,attribution,billing,communication,scheduling,contract}_adapter_registry_mirror` | 11 / 4 / 3 / 3 / 3 / 2 / 3 / 3 |
| `ENGAGEMENT_TEMPLATE_REGISTRY.csv` | `compliance.engagement_template_registry_mirror` | 6 |
| `ENGAGEMENT_REGISTRY.csv` | `compliance.engagement_registry_mirror` | 7 |
| Output architecture L1–L3 | `compliance.output_type_registry_mirror` | 17 |
| | `compliance.artifact_class_registry_mirror` | 21 |
| | `compliance.component_primitive_registry_mirror` | 25 |

DDL source: `supabase/migrations/20260514260000_i72_adapter_registries_mirrors.sql` (adapters) +
prior I70/I86 output-arch + engagement DDL (verify with read-only `list_tables` before apply).

### Phase B — GOV-7 forward-charter mirrors (DDL push **then** DML)

| Migration file | Mirror table(s) |
|:---|:---|
| `20260609120000_p95_gov7_finance_registry_mirrors.sql` | `pricing_tier_registry_mirror`, `finops_performance_obligation_registry_mirror`, `finops_tax_calendar_mirror` |
| `20260609120100_p95_gov7_data_contract_registry_mirror.sql` | `data_contract_registry_mirror` |
| `20260609120200_p95_gov7_rpa_adapter_registry_mirror.sql` | `rpa_adapter_registry_mirror` |
| `20260609120300_p95_gov7_component_service_matrix_mirror.sql` | `component_service_matrix_mirror` |

| Mirror table | Expected rows |
|:---|---:|
| `compliance.pricing_tier_registry_mirror` | 6 |
| `compliance.finops_performance_obligation_registry_mirror` | 5 |
| `compliance.finops_tax_calendar_mirror` | 8 |
| `compliance.data_contract_registry_mirror` | 14 |
| `compliance.rpa_adapter_registry_mirror` | 5 |
| `compliance.component_service_matrix_mirror` | 110 |

---

## Step 0 — Read-only discover (operator SQL gate)

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos

# Ledger parity — Local and Remote must match before push
npx supabase migration list --linked

# Confirm GOV-7 tables absent OR empty pre-push (MCP list_tables or):
npx supabase db query --linked --output table "
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'compliance'
  AND table_name IN (
    'pricing_tier_registry_mirror',
    'finops_performance_obligation_registry_mirror',
    'finops_tax_calendar_mirror',
    'data_contract_registry_mirror',
    'rpa_adapter_registry_mirror',
    'component_service_matrix_mirror'
  )
ORDER BY 1;"
```

Record outcome in **Evidence log** (template below).

---

## Step 1 — Phase B DDL push (GOV-7 four migrations)

Only after operator approval of [`sql-proposal-p95-gov-7-2026-06-09.md`](sql-proposal-p95-gov-7-2026-06-09.md).

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos
npx supabase db push --linked
```

**Expected:** four `2026060912*` versions appear on remote `schema_migrations`.

**Rollback (break-glass):** see SQL proposal § Rollback; then `supabase migration repair` if needed.

---

## Step 2 — Emit mirror DML from git CSVs

```powershell
cd c:\Users\Shadow\cd_shadow\openclaw-akos
py scripts/verify.py compliance_mirror_emit
```

Output: `artifacts/sql/compliance_mirror_upsert.sql` (gitignored; ~5.5 MB full bundle).

**Scoped smoke (optional — one GOV-7 table):**

```powershell
py scripts/sync_compliance_mirrors_from_csv.py --pricing-tier-registry-only
```

---

## Step 3 — Apply DML to linked remote

**Method A (preferred):** split + batch apply per [`holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md).

For the full bundle (GOV-5 + GOV-7 + existing mirrors), either:

1. Use initiative 22a chunk pattern under `scripts/sql/mirror-batches/`, **or**
2. Apply monolith via psql (Method B) if Editor/CLI size limits bite.

**CI alternative (when gh auth available):**

```powershell
gh workflow run supabase-mirror-sync.yml -f apply=true
```

**Single-table linked apply (smoke after DDL):**

```powershell
# After emitting a scoped SQL file to artifacts/sql/
npx supabase db query --linked --file artifacts/sql/<scoped-upsert>.sql
```

---

## Step 4 — Row-count parity verification

### 4.1 Mechanical (git SSOT)

```powershell
py scripts/validate_mirror_emit_contract.py
```

Expected: `PASS: mirror emit contract — 47 tables, CSV row counts match emitted INSERTs`.

### 4.2 Prod (linked query)

```powershell
npx supabase db query --linked --output table "
SELECT 'pricing_tier' t, count(*)::int n FROM compliance.pricing_tier_registry_mirror
UNION ALL SELECT 'finops_perf_obl', count(*)::int FROM compliance.finops_performance_obligation_registry_mirror
UNION ALL SELECT 'finops_tax', count(*)::int FROM compliance.finops_tax_calendar_mirror
UNION ALL SELECT 'data_contract', count(*)::int FROM compliance.data_contract_registry_mirror
UNION ALL SELECT 'rpa_adapter', count(*)::int FROM compliance.rpa_adapter_registry_mirror
UNION ALL SELECT 'component_svc', count(*)::int FROM compliance.component_service_matrix_mirror
UNION ALL SELECT 'engagement_tpl', count(*)::int FROM compliance.engagement_template_registry_mirror
UNION ALL SELECT 'engagement_reg', count(*)::int FROM compliance.engagement_registry_mirror
UNION ALL SELECT 'output_type', count(*)::int FROM compliance.output_type_registry_mirror
UNION ALL SELECT 'artifact_class', count(*)::int FROM compliance.artifact_class_registry_mirror
UNION ALL SELECT 'component_prim', count(*)::int FROM compliance.component_primitive_registry_mirror
UNION ALL SELECT 'crm_adapter', count(*)::int FROM compliance.crm_adapter_registry_mirror
UNION ALL SELECT 'rpa_adapter_gov5', count(*)::int FROM compliance.rpa_adapter_registry_mirror;"
```

Compare every `n` to the **Expected rows** tables above. Mismatch → stop; do not mark APPLIED.

### 4.3 Drift probe (optional)

```powershell
py scripts/probe_compliance_mirror_drift.py --emit-sql
# apply SELECT bundle via MCP or db query --linked
py scripts/probe_compliance_mirror_drift.py --verify
```

---

## Evidence logging template

Copy into synthesis stubs + UAT §4.3 when complete.

```markdown
| Step | Status | Evidence |
|:---|:---:|:---|
| Prod DDL inventory (read-only) | PASS / FAIL | `migration list` screenshot or pasted output @ <ISO time> |
| `npx supabase db push --linked` (GOV-7) | APPLIED / SKIP | Remote versions: 20260609120000..20260609120300 |
| `compliance_mirror_emit` + apply | APPLIED / SKIP | apply path: CLI batch / gh workflow / psql |
| Post-apply row-count parity | PASS / FAIL | Query output pasted; validator PASS @ <SHA> |
| Operator | <name> | <date> |
```

---

## Status after this session

| Phase | Scope | Status |
|:---|:---|:---:|
| **A** | GOV-5 emit (adapters, templates, engagement, output-arch) | **PENDING-OPERATOR** |
| **B** | GOV-7 DDL push + six new mirrors | **PENDING-OPERATOR** |

**Next operator action:** Steps 0→4 in order; update
[`synthesis-p95-gov-5-2026-06-09.md`](synthesis-p95-gov-5-2026-06-09.md),
[`synthesis-p95-gov-7-2026-06-09.md`](synthesis-p95-gov-7-2026-06-09.md), and
[`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md) §4.3
to **APPLIED** when parity PASS.

## Cross-references

- Holistika mirror DML guide: [`docs/guides/holistika-mirror-dml-apply.md`](../../../../guides/holistika-mirror-dml-apply.md)
- Operator SQL gate: [`operator-sql-gate.md`](../../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md)
- GOV-7 SQL proposal: [`sql-proposal-p95-gov-7-2026-06-09.md`](sql-proposal-p95-gov-7-2026-06-09.md)
- Closure UAT PWF tracker: [`uat-universal-canonical-governance-2026-06-09.md`](uat-universal-canonical-governance-2026-06-09.md)
