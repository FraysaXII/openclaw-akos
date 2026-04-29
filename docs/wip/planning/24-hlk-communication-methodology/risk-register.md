# Initiative 24 — Risk Register

## Active risks

| ID | Description | Mitigation | Owner | Status |
|:---|:-----------|:-----------|:-----:|:------:|
| **PR-24-1** | GOI/POI mirror ALTER drift if local migration filename diverges from remote `schema_migrations` ledger after MCP apply (Initiative 22 P7 precedent). | Rename local migration to match remote timestamp on first apply; document in `reports/p2-mirror-alter-evidence.md`. | Agent (P2) | OPEN |
| **PR-24-2** | Real-email leak (PII in artifacts/exports/) — operator forgets to redact recipient before sharing the archive copy. | Composer NEVER writes a real recipient address into git artifacts (only `ref_id`); operator inlines at SMTP step. Pre-flight checklist (G-24-3) requires `--include-restricted=false` exit code 0. Archive copy is gitignored under `artifacts/exports/`. | Agent + Operator (P6) | OPEN |
| **PR-24-3** | Composer drift between formats (MD vs HTML vs text vs PDF) — same source produces inconsistent body across formats. | Multi-format body parity test in `tests/test_compose_adviser_message.py`; verify-profile smokes for each format. | Agent (P4 + P5) | OPEN |
| **PR-24-4** | Brand foundation drift if operator's lived brand voice evolves faster than the SOP. | Annual Brand Manager review row in `process_list.csv` and `decision-log.md` rotation reminder; D-IH-17 re-evaluation trigger. | Operator | OPEN |
| **PR-24-5** | Scaffold-staged brand foundation MDs ship with placeholder content; downstream consumers (composer) might use placeholder tokens silently. | Validator emits warning per scaffold-staged file; composer refuses to resolve a brand-foundation token when the source MD is `status: scaffold-awaiting-discovery`. Operator override flag `--allow-scaffold-tokens` for early dry-run. | Agent (P0a + P4) | OPEN |
| **PR-24-6** | Real-email-send pre-flight checklist (G-24-3) gets skipped under time pressure. | Checklist is in `decision-log.md` not in YAML — every box must be ticked in PR description; founder sign-off captured in YAML Section 5 + UAT report; sent timestamp captured in UAT report at send time. | Operator | OPEN |
| **PR-24-7** | Voice register taxonomy doesn't match a real recipient (e.g. need a 4th register the enum doesn't capture). | `voice_register` is enum-bounded; validator catches non-enum values; operator adds new register via amend-CSV + amend-validator + ALTER mirror (one-row change). | Operator | OPEN |
| **PR-24-8** | `process_list.csv` tranche row for "Communication methodology maintenance" forgotten — no maintenance discipline; SOP rots. | G-24-2 operator approval gate captures the tranche-row add at P1; named tranche `thi_mkt_dtp_NN` "Communication methodology maintenance"; cursor-rules-hygiene checkbox at I24 closure. | Agent + Operator (P1) | OPEN |

## Closed risks

(none yet)

## Cross-references

- Wave-2 plan §"Risk and rollback"
- [`akos-adviser-engagement.mdc`](../../../../.cursor/rules/akos-adviser-engagement.mdc) — adviser engagement discipline
- Initiative 22 closure note (precedent for risk-register-style documentation)
