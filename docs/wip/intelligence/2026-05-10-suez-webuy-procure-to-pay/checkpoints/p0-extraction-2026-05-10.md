---
status: complete
classification: working
access_level: 5
language: en
register: internal
phase: P0
phase_name: Text extraction (engagement docs + inspiration sources)
recorded_at: 2026-05-10
---

# P0 — Text extraction self-checkpoint

## Inputs processed

| Source | Destination | Mode | Status |
|:---|:---|:---|:---|
| `CDC_WeBuy_SUEZ.docx` (operator-supplied; staged off-repo, deleted post-extraction) | `docs/wip/intelligence/2026-05-10-suez-webuy-procure-to-pay/extracts/cdc_webuy_suez.txt` | engagement (committed) | ok — 16,242 chars |
| `Mode opératoire - Process de passage de commande WeBuy.pdf` (operator-supplied; staged off-repo, deleted post-extraction) | `extracts/mode_ope_ratoire_-_process_de_passage_de_commande_webuy.txt` | engagement (committed) | ok — 32,999 chars |
| 3× operator-supplied competitor methodology decks | off-repo inspiration cache | inspiration (off-repo) | ok |
| operator-supplied competitor cost-model workbook + JSON dump | off-repo inspiration cache | inspiration (off-repo) | ok |

## Redaction tokens applied

* Engagement extracts (in-repo): bridge-collaborator real name (case-insensitive).
* Inspiration extracts (off-repo): operator-stripped competitor organisation name, internal cost-model code, end-client name, and any specific named individuals; email + phone masking applied to all extracts via the canonical `redact_text` helper. Source identifiers operator-supplied at runtime via `--redact-token`; nothing competitor-specific entered the in-repo trail.

## Tooling

* New script: `scripts/extract_engagement_pdfs.py` — Pydantic-style `ExtractionConfig` + path-discipline via `akos.io.REPO_ROOT` + `akos.log.setup_logging`. Two modes: `engagement` (in-repo intelligence) and `inspiration` (off-repo cache). NFD/NFC unicode-tolerant filename resolver for accented PDFs.
* Tests: `tests/test_extract_engagement_pdfs.py` — 13 cases covering email/phone redaction, operator tokens, accent normalisation, JSON / XLSX / passthrough roundtrips, missing-input error path, and end-to-end redacted-write.

## Verification

```
py -m pytest tests/test_extract_engagement_pdfs.py -v
==> 13 passed in 0.47s
```

## Notes

* Phone-redaction false-positive on long PO numbers (e.g. `PO01791818` → `PO[REDACTED-PHONE]`). Acceptable: downstream phases describe PO format, not specific values.
* SUEZ employee names in engagement extracts are preserved (working-space access_level 5; internal-register surface). They will be paraphrased to role-neutral language when authoring P5 (questionnaire) and P6 (proposal) external deliverables.
* Inspiration sources will be deleted at end of P3 once distillation lands in `SOP-ENG_ESTIMATION_DISCIPLINE_001.md` rate magnitudes + multipliers (no client/competitor identifiers to flow through).

## Next

P1 — Engagement folders + GOI/POI rows.
