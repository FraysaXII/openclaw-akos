---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-schema-map
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-04-30
audience: ERP team engineering
---

# 16 compliance mirrors — schema map for the ERP team

This document is the read-side map. ERP screens that display org / process / role / dimension data must read from the appropriate `compliance.*_mirror` table (or a dedicated Supabase view that projects it).

## Read posture (governance)

- Every `compliance.*_mirror` table denies `anon` and `authenticated`. Reads happen via a `service_role`-scoped sync job on the ERP side or via dedicated views with explicit grants.
- ERP is a **read-only consumer**. Never write to `compliance.*_mirror`.
- The git CSV is canonical SSOT. The mirror is a derived projection. Drift is resolved canonical-side.

## The 16 mirrors

### Foundation (always present, since I14)

```sql
SELECT * FROM compliance.process_list_mirror LIMIT 5;
-- 1093 rows. Hierarchical process tree. PK item_id.
```

```sql
SELECT * FROM compliance.baseline_organisation_mirror WHERE area = 'Tech' LIMIT 5;
-- 65 rows. Org structure. PK org_id.
```

### FINOPS (since I18)

```sql
SELECT * FROM compliance.finops_counterparty_register_mirror;
-- 2 rows. Counterparty metadata only — NO monetary amounts in git (POL-PII-FINOPS-NO-AMOUNTS-IN-GIT).
```

### ADVOPS (since I21)

```sql
SELECT ref_id, display_name, distance_band, current_distance_band
FROM compliance.goipoi_register_mirror
WHERE distance_band = 'N1';
-- 6 rows post-I31 distance schema bump. Display names obfuscated for confidential entities.
```

```sql
SELECT * FROM compliance.adviser_engagement_disciplines_mirror;
-- 6 rows. Lookup: Legal / Fiscal / IP / Banking / Certification / Notary.
```

```sql
SELECT * FROM compliance.adviser_open_questions_mirror WHERE owner_role = 'Compliance';
-- 12 rows. PMO/Legal-chain SSOT for adviser-facing questions across disciplines.
```

```sql
SELECT * FROM compliance.founder_filed_instruments_mirror;
-- 1 row (founder incorporation seed). Tracks legal/fiscal/IP/banking instruments.
```

### Cross-cutting dimensions (since I23/I25/I31/I32)

```sql
SELECT program_id, program_name, lifecycle_status FROM compliance.program_registry_mirror;
-- 12 rows. PRJ-HOL-* programs with cycle dependencies + cross-program edges.
```

```sql
SELECT topic_id, title, primary_owner_role FROM compliance.topic_registry_mirror ORDER BY title;
-- 27 rows post-I32 P7. Cross-program topics with parent / depends_on / related edges.
```

```sql
SELECT persona_id, name, direction, typical_distance_band FROM compliance.persona_registry_mirror
WHERE direction = 'inbound';
-- 16 rows. Persona archetypes; routing axis 1 of the 6-axis Holistik Ops doctrine.
```

```sql
SELECT channel_id, name, response_owner_role, response_sla_band
FROM compliance.channel_touchpoint_registry_mirror ORDER BY name;
-- 10 rows. Where humans physically reach Holistika; routing axis 2.
```

```sql
SELECT vendor_id, discipline, current_distance_band FROM compliance.sourcing_register_mirror;
-- 1 row (seed). External vendor sourcing; distance migration tracking.
```

### Initiative 32 new (skill / cell / policy / repo health)

```sql
SELECT skill_id, agents_supported, axes_consumed, owner_role, eval_baseline_pct
FROM compliance.skill_registry_mirror WHERE lifecycle_status = 'active';
-- 5 rows post-I32 P2. The MADEIRA-SaaS substrate. tenant_scope='shared' until I34.
```

```sql
SELECT cell_id, persona_id, channel_id, language, template_path
FROM compliance.touchpoint_kit_cell_mirror WHERE persona_id = 'PERSONA-INVESTOR-COLD';
-- 15 rows post-I32 P3. (persona x channel x language) cells; FS-vs-CSV drift enforced canonical-side.
```

```sql
SELECT policy_id, policy_class, applies_to_schema, cadence, next_review
FROM compliance.policy_register_mirror WHERE policy_class = 'rls';
-- 14 rows post-I32 P4. RLS + service_role rotation + redaction + PII scope.
```

### Initiative 32 operational mirrors (audit history)

```sql
SELECT validator_name, status, started_at, error_count
FROM compliance.validation_runs WHERE status <> 'pass'
ORDER BY started_at DESC LIMIT 10;
-- Append-only validator dispatch history (D-IH-32-F). Indexes optimised for "last failure" queries.
```

```sql
SELECT repo_slug, snapshot_date, has_external_repo_contract, language_frontmatter_compliance_pct
FROM compliance.repo_health_snapshot_mirror WHERE snapshot_date >= CURRENT_DATE - 28
ORDER BY snapshot_date DESC, repo_slug;
-- 4-week window of cross-repo health. ERP itself is one of the 3 tracked repos.
```

## Cross-references

- AKOS PRECEDENCE.md: full mirror inventory + sync direction + DDL pointers
- KiRBe sync contract §2: mirror enumeration with consumer-role detail (rewritten in I32 P7)
- Operator SQL gate runbook: `03-operator-sql-gate-pointer.md` (sibling file)
