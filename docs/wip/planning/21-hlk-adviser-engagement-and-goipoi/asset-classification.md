# Initiative 21 — Asset classification

Classification per [`PRECEDENCE.md`](../../../references/hlk/compliance/PRECEDENCE.md). All paths relative to repo root.

## Canonical (edit here first)

| Asset | Path | Validator | Notes |
|:------|:-----|:----------|:------|
| GOI/POI register | `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` | `scripts/validate_goipoi_register.py` | Knowledge-architecture dimension; obfuscation source-of-truth |
| Adviser engagement disciplines lookup | `docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | `scripts/validate_adviser_disciplines.py` | Small lookup; FK target for questions and filed instruments |
| Adviser open questions | `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv` | `scripts/validate_adviser_questions.py` | Replaces markdown queue as SSOT |
| Founder filed instruments | `docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv` | `scripts/validate_founder_filed_instruments.py` | Replaces markdown register as SSOT |
| GOI/POI maintenance SOP | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md` | doc lint | Compliance role |
| Transcript redaction SOP | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md` | doc lint | Compliance role |
| External adviser engagement SOP | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md` | doc lint | PMO role |
| External adviser router | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md` | vault links | PMO role |
| KM Topic-Fact-Source manifest | `docs/references/hlk/v3.0/_assets/<area>/topic_external_adviser_handoff.manifest.md` | `scripts/validate_hlk_km_manifests.py` | Output 1 |
| `PRECEDENCE.md` updates | `docs/references/hlk/compliance/PRECEDENCE.md` | doc lint | New canonical + mirror rows |
| `process_list.csv` tranche | `docs/references/hlk/compliance/process_list.csv` | `scripts/validate_hlk.py` | Operator-gated |

## Mirrored / derived (do not hand-edit without canonical update)

| Asset | Path / table | Sync direction |
|:------|:-------------|:---------------|
| GOI/POI mirror | `compliance.goipoi_register_mirror` | CSV → mirror; `service_role` only |
| Adviser disciplines mirror | `compliance.adviser_engagement_disciplines_mirror` | CSV → mirror |
| Adviser open questions mirror | `compliance.adviser_open_questions_mirror` | CSV → mirror |
| Filed instruments mirror | `compliance.founder_filed_instruments_mirror` | CSV → mirror |
| Existing legal vault MD (open questions, filed instruments, fact pattern) | `docs/references/hlk/v3.0/Admin/O5-1/People/Legal/*.md` | CSV → human read-out (manual P4 / P5) |
| PMO hub stakeholder index | [`TOPIC_PMO_CLIENT_DELIVERY_HUB.md`](../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) | GOI/POI CSV → manual view |

## Reference-only (non-canonical, do not hand-edit as source of truth)

| Asset | Path | Notes |
|:------|:-----|:------|
| Redacted legal transcripts | `docs/references/hlk/business-intent/delete-legal-transcripts/*.md` | Use `POI-*`/`GOI-*` ids only after P2 |
| `.docx` mirrors | same folder | Convenience copies; raw originals off-repo |

## Out-of-repo (operator-managed)

| Asset | Storage | Owner |
|:------|:--------|:------|
| Raw adviser call recordings and unredacted transcripts | Operator-managed Drive (or private store) | Compliance |
| Real identity ↔ POI/GOI mapping | Operator-managed off-repo register | Compliance |
| Filed legal instruments (signed PDFs) | Drive / deal room | Legal Counsel |
