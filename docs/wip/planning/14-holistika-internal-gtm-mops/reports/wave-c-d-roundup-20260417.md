# Initiative 14 — Waves C–D round-up (2026-04-17)

**Purpose:** What landed in git for **Waves C–D** vs what stays **operator-run** (calendar, meetings, live UAT).

## Delivered in repository

| Wave | ID | Artifact |
|------|-----|----------|
| **C1** | SLA decision | [decision-log.md](../decision-log.md) **D-GTM-C1**; [SOP-GTM_INBOUND_SLA_001.md](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Growth/SOP-GTM_INBOUND_SLA_001.md) references D-GTM-C1 (**4 business hours**) |
| **C2** | CRM → Supabase | [crm-minimum-fields-supabase.md](crm-minimum-fields-supabase.md); decision **D-GTM-C2** |
| **C3** | Weekly metrics forum | [wave-c-weekly-metrics-forum-log.md](wave-c-weekly-metrics-forum-log.md) — fill 4 weeks, then mark C3 `done` in [EXECUTION-BACKLOG.md](EXECUTION-BACKLOG.md) |
| **D1** | Contact funnel UAT | [uat-holistika-contact-funnel-20260417.md](uat-holistika-contact-funnel-20260417.md) — public URL + process anchors; operator fills PASS/FAIL |
| **D2** | Vault / KM | [gtm-sop-vault-index.md](gtm-sop-vault-index.md); [phase-5-km-checklist.md](phase-5-km-checklist.md) Initiative 14 note; **D-GTM-D2** |

## Operator-only (not closed by commit alone)

- **C1:** Copy **4 business hours** into Notion / team calendar if not already there.
- **C3:** Run four weekly forums; paste minutes or links into the log.
- **D1:** Execute rows in the UAT stub in a real browser (qualitative sign-off per `.cursor/rules/akos-planning-traceability.mdc`).

**Governance gates:** When editing `process_list.csv` / canonical CSVs or `v3.0/**/*.md` links, run `py scripts/validate_hlk.py` and `py scripts/validate_hlk_vault_links.py` per [docs/DEVELOPER_CHECKLIST.md](../../../DEVELOPER_CHECKLIST.md).
