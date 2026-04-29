# Initiative 26 — Asset classification

Per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md).

## Canonical (edit here first)

| Asset | Path | Authored under |
|:------|:-----|:---------------|
| Master roadmap | `master-roadmap.md` | This initiative |
| Decision log | `decision-log.md` | This initiative |
| Risk register | `risk-register.md` | This initiative |
| Re-eval-trigger templates (3) | `reports/re-eval-trigger-{finops-techops-second-csv,compliance-plane-relocation,graph-mcp-tooling-promotion}.md` | This initiative — persistent until trigger fires |

## Mirrored / derived (this initiative does not introduce new mirrors)

None. I26 is doc + runbook scope. The `compliance/<plane>/` physical relocation (P4) is **deferred**; if it fires, it becomes a `git mv` cascade — not a new mirror.

## Reference-only

| Asset | Path |
|:------|:-----|
| Phase reports | `reports/phase-*-report.md` |
| Dated UAT reports | `reports/uat-i26-*.md` |

## Touched (cross-cutting docs)

These docs are owned outside I26 and updated as part of P1/P2/P3 deliverables:

| Path | Section touched | Phase |
|:-----|:----------------|:-----:|
| [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) | mmdc CI install runbook | P1 |
| [`CONTRIBUTING.md`](../../../../CONTRIBUTING.md) | WeasyPrint GTK3 install runbook (Windows) | P3 |
| [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md) | §6 service_role quarterly rotation procedure | P2 |
| [`CHANGELOG.md`](../../../../CHANGELOG.md) | `[Unreleased]` entry | P0/P1/P2/P3 |

## SOC

- Re-eval-trigger templates carry **no secrets**. They describe trigger conditions + remediation scope; no API keys, no row-level PII.
- `service_role` rotation runbook references the Supabase dashboard path; **does not embed the key value**. Per [`akos-governance-remediation.mdc`](../../../../.cursor/rules/akos-governance-remediation.mdc) §"SOC / Security": never log secret values.

## Out of scope (explicit)

- Anything in I23 / I24 / I25.
- `git filter-repo` history rewrite (I21 D-CH-2 trigger lives in `22-…/reports/re-eval-trigger.md`, not here).
