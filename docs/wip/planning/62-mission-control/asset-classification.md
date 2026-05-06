---
language: en
status: active
initiative: 62-mission-control
report_kind: asset-classification
last_review: 2026-05-06
---

# I62 Asset Classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). Every asset touched in this initiative classified into canonical / mirrored-or-derived / ERP-canonical / reference-only.

## Canonical (AKOS-side, edit here first)

| Asset | Where it lives | Authoring path |
|:---|:---|:---|
| **NEW** `SUBDOMAINS_REGISTRY.md` | `docs/references/hlk/v3.0/Envoy Tech Lab/Repositories/SUBDOMAINS_REGISTRY.md` | I62 P0 ships row schema + initial rows; `validate_subdomains_registry.py` enforces; `release-gate.py` step added |
| `baseline_organisation.csv` (no row changes; consumed by ERP RBAC mapping) | `docs/references/hlk/compliance/baseline_organisation.csv` | AKOS PR + `validate_hlk.py`; ERP reads via `compliance.baseline_organisation_mirror` |
| `process_list.csv` (no row changes in I62; ERP reads only) | `docs/references/hlk/compliance/process_list.csv` | AKOS PR + `validate_hlk.py` |
| All 16 `compliance.*_mirror` source CSVs (read-only consumed) | `docs/references/hlk/compliance/**` | AKOS PR + `validate_hlk.py` |
| `INITIATIVE_REGISTRY.csv` (1 new row for I62) | `docs/references/hlk/compliance/INITIATIVE_REGISTRY.csv` | I62 P0 appends one row; `scripts/validate_initiative_registry.py` enforces |
| `OPS_REGISTER.csv` (rows minted as gates flip) | `docs/references/hlk/compliance/OPS_REGISTER.csv` | I62 P11 closure; `scripts/render_operator_inbox.py` re-renders OPERATOR_INBOX.md |
| `DECISION_REGISTER.csv` (D-IH-62-A..R rows) | `docs/references/hlk/compliance/DECISION_REGISTER.csv` | I62 P0 + ongoing as decisions land; `scripts/validate_decision_register.py` enforces |
| `CYCLE_REGISTER.csv` (1 new row for I62) | `docs/references/hlk/compliance/CYCLE_REGISTER.csv` | I62 P0 + I62 P11 closure |

## Mirrored / derived (consumed read-only by ERP)

| Asset | Where it lives | Owner |
|:---|:---|:---|
| **NEW** `erp` Postgres schema | Supabase (proposed via SQL gate, P2.3) | ERP application owns lifecycle |
| **NEW** `erp.vw_three_lights_status` view | Supabase | Joins eval_run + dossier_run + skills + repo_health |
| **NEW** `erp.vw_mission_control_today` view | Supabase | Aggregates 7 cards' worth of summarized data |
| **NEW** `erp.vw_operator_inbox_top` view | Supabase | Top-N OPS rows by RICE, joined to initiative |
| **NEW** `erp.vw_initiative_pulse` view | Supabase | Counts by status + 30-day closure sparkline |
| **NEW** `erp.vw_mirror_health` view | Supabase | 16/16 green + last-sync per mirror |
| **NEW** `erp.vw_public_health` view | Supabase (`SELECT` granted to `anon`) | Status page; no PII |
| **NEW** `erp._mode()` SQL function | Supabase | Reads session GUC `app.data_mode` |
| 16 `compliance.*_mirror` tables | Supabase (already exist) | Sync from canonical CSVs by `scripts/sync_compliance_mirrors_from_csv.py` |
| `validation_runs` mirror | Supabase (already exists, I32 P5) | Append-only validator dispatch history |
| `repo_health_snapshot_mirror` | Supabase (already exists, I32) | 4-week cross-repo health |

## ERP-canonical (operational facts ERP owns; write-side)

| Asset | Where it lives | Owner |
|:---|:---|:---|
| **NEW** `holistika_ops.user_role_mapping` | Supabase (proposed via SQL gate, P1.3) | ERP application; mirrors `auth.users` to AKOS roles |
| **NEW** `holistika_ops.audit_log` | Supabase | Every confidential read + impersonation start/stop |
| **NEW** `holistika_ops.user_preferences` | Supabase | Theme / density / locale / saved_views / starred_ids |
| **NEW** `holistika_ops.notifications` | Supabase | Realtime subscription source for in-app drawer |
| **NEW** `demo.*` schema (5+ tables mirroring source schemas) | Supabase | Idempotent seed via `scripts/seed-demo.ts` |

## Reference-only (initiative artefacts)

| Asset | Where it lives | Lifecycle |
|:---|:---|:---|
| `master-roadmap.md` | This folder | Updated as plan evolves; mirrors `~/.cursor/plans/hlk-erp_mission_control_magnificent_5aa05486.plan.md` |
| `decision-log.md` | This folder | Append-only as new D-IH-62-* decisions land |
| `asset-classification.md` (this file) | This folder | Updated when new assets touched |
| `evidence-matrix.md` | This folder | Audit-finding → resolution rows from the I32 P8 architecture audit |
| `risk-register.md` | This folder | R-62-* rows + mitigations |
| `reports/impeccable-shape-mission-control-today-2026-05-06.md` | This folder | One per surface; operator approval line |
| `reports/impeccable-shape-operator-inbox-2026-05-06.md` | This folder | Operator approval before P5 starts |
| `reports/impeccable-shape-initiatives-2026-05-06.md` | This folder | Operator approval before P5 starts |
| `reports/sql-discovery-2026-05-06.md` | This folder | `list_schemas` evidence; informs P2.3 SQL proposal |
| `reports/sql-proposal-mission-control-<date>.md` | This folder (added in P1.3 + P2.3) | Operator approval per [operator-sql-gate.md](../14-holistika-internal-gtm-mops/reports/operator-sql-gate.md) |
| `reports/uat-mission-control-<phase>-<date>.md` | This folder (added per phase) | Per-phase UAT evidence per [.cursor/rules/akos-planning-traceability.mdc](../../../../.cursor/rules/akos-planning-traceability.mdc) |
| `reports/dr-runbook.md` | This folder (added in P10.4) | Disaster recovery RTO 4h / RPO 24h |

## ERP-side (external repo) — read-only AKOS view

These live in `https://github.com/FraysaXII/hlk-erp` and are referenced from this initiative but authored externally. Per [`EXTERNAL_REPO_CONTRACT.md`](https://github.com/FraysaXII/hlk-erp/blob/main/EXTERNAL_REPO_CONTRACT.md), AKOS does not author them; the ERP application owns them.

- `app/(operator)/mission-control/**` — operator surface routes.
- `app/showcase/**` — public showcase routes.
- `app/sign-in`, `app/auth/**`, `app/forbidden` — auth surfaces.
- `lib/supabase/{server,client,admin}.ts` — split clients.
- `lib/auth/policy.ts` — RBAC primitives.
- `middleware.ts` — route gating.
- `scripts/seed-demo.ts` — idempotent demo seed.
- `scripts/lint-jargon.ts` — brand-voice fast-lint port.
- `.cursor/rules/hlk-erp-mission-control.mdc` — captures the Mission Control contract on the ERP side.
- `.github/workflows/ci.yml` — CI pipeline.
- `next.config.js` — security headers.
- `tsconfig.json` — strict TS settings.

## Drift detection

When canonical and mirrored / derived assets disagree, **canonical wins**. Investigate the propagation path, resync the mirror, and document the incident in `reports/`. Specific drift probes:

- `scripts/check-drift.py` — existing AKOS gate.
- `scripts/validate_subdomains_registry.py` — NEW; cross-checks `SUBDOMAINS_REGISTRY.md` rows against Vercel project domain attachments via Vercel MCP (manual cross-check P10; automated later).
- ERP `npm run db:types` — regenerates `lib/supabase-types.ts`; CI fails on diff.
- ERP `npm run lint:jargon` — brand-voice fast-lint on `app/showcase/**` and `app/(marketing)/**`.
