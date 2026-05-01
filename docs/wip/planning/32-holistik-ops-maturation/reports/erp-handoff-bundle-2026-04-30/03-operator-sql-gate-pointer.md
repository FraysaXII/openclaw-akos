---
language: en
status: draft
initiative: 32-holistik-ops-maturation
report_kind: external-team-pointer
program_id: shared
plane: ops
authority: System Owner
last_review: 2026-04-30
audience: ERP team engineering
---

# Operator SQL gate — pointer

ERP team must follow the operator SQL gate workflow for any DDL change that touches Supabase (including new `compliance.*` views or new `holistika_ops.*` tables for ERP-specific operational data).

## The runbook

`docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md` in the AKOS repo.

GitHub link: `https://github.com/FraysaXII/openclaw-akos/blob/main/docs/wip/planning/14-holistika-internal-gtm-mops/reports/operator-sql-gate.md`

## The 5 steps

1. **Discover** — read-only MCP / SQL exploration; classify what already exists.
2. **Propose** — DDL + rollback + RLS + PII notes in `reports/sql-proposal-*.md`; operator approval in initiative `decision-log.md`.
3. **Execute DDL** — stage under `scripts/sql/<initiative>_staging/`, then promote to `supabase/migrations/<timestamp>_description.sql`, update parity map.
4. **Pre-push** — `supabase migration list` shows local + remote in parity; then `supabase db push` (or CI).
5. **Break-glass** — Dashboard / MCP `apply_migration` only in emergencies; afterward `db pull` / `migration repair` until git and ledger align.

## Forbidden for routine work

Mutating `execute_sql` or ad-hoc production DDL without a matching migration file.

## Cross-references

- AKOS rule: `.cursor/rules/akos-holistika-operations.mdc` §"Operator SQL gate"
- ERP team's existing infrastructure rules (Supabase + Next.js) are unchanged; this gate is the AKOS-side discipline they must respect when their DDL changes touch shared schemas.
