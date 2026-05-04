---
language: en
status: bootstrapped-pending-first-advisor-reply
initiative: 56-first-response-cycle
report_kind: asset-classification
program_id: shared
plane: advops
authority: Founder
last_review: 2026-05-03
---

# Initiative 56 — Asset classification

Per `docs/references/hlk/compliance/PRECEDENCE.md`. Cycle-1 ships P0 only; the rows below describe the assets that **will** be touched as P1–P8 execute under OPS-56-1.

## Canonical (edit here first)

| Asset | Path | Touch point | Gate |
|:------|:-----|:------------|:-----|
| `ADVISER_OPEN_QUESTIONS.csv` | [`docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv`](../../../references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv) | P2 — answered Q-rows | G-56-1a |
| `FOUNDER_FILED_INSTRUMENTS.csv` | [`docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv`](../../../references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv) | P2 — only if instruments committed | G-56-1b |
| `GOI_POI_REGISTER.csv` | [`docs/references/hlk/compliance/GOI_POI_REGISTER.csv`](../../../references/hlk/compliance/GOI_POI_REGISTER.csv) | P2 — only if previously-unknown participants | G-56-1c |
| `ADVISER_ENGAGEMENT_DISCIPLINES.csv` | [`docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv`](../../../references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv) | Read-only (referenced from P2 rows) | — |

## Mirrored / derived

| Asset | Path | Touch point |
|:------|:-----|:------------|
| `compliance.adviser_open_questions_mirror` | Supabase | P3 mirror sync |
| `compliance.founder_filed_instruments_mirror` | Supabase | P3 mirror sync |
| `compliance.goipoi_register_mirror` | Supabase | P3 mirror sync |
| `compliance.adviser_engagement_disciplines_mirror` | Supabase | P3 mirror sync (parity check only) |

Mirror DML uses `compliance_mirror_emit`; **no megabyte migration files**. Per the AKOS governance remediation rule §"Supabase DDL vs mirror DML".

## Reference-only

| Asset | Path | Touch point |
|:------|:-----|:------------|
| Redacted transcript MD | [`docs/references/hlk/business-intent/delete-legal-transcripts/`](../../../references/hlk/business-intent/delete-legal-transcripts/) (or current canonical home per [I22 layout](../22-hlk-scalability-and-i21-closures/master-roadmap.md)) | P1 — committed AFTER redaction per `SOP-HLK_TRANSCRIPT_REDACTION_001.md` |
| `EXTERNAL_ADVISER_ROUTER.md` | I21-canonical (read-only) | Cite-only from P5 + P7 reports |
| Raw original transcripts | **OFF-REPO** (operator's identity store) | Never committed |

## Vault SOPs (canonical, edit if cycle-1 surfaces a gap)

| SOP | Path | Touch point |
|:----|:-----|:------------|
| `SOP-HLK_TRANSCRIPT_REDACTION_001.md` | [`docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) | P1 (read); P7 (extend if R-56-1 fired) |
| `SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md` | [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_REGRESSION_TO_ADVISOR_LOOP_001.md) | P4 (cite); P7 (refine if cycle-1 lessons warrant) |
| `SOP-HLK_COMMUNICATION_METHODOLOGY_001.md` | [`docs/references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_COMMUNICATION_METHODOLOGY_001.md`](../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/SOP-HLK_COMMUNICATION_METHODOLOGY_001.md) | P4 (cite for response-message composer; if I55 P5 has landed by then) |
| `SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md` (if exists) | I21 canonical | P7 — refine based on cycle-1 lessons |

## Scripts (no new scripts in I56)

| Script | Path | Touch point |
|:-------|:-----|:------------|
| `scripts/export_adviser_handoff.py` | [`scripts/export_adviser_handoff.py`](../../../../scripts/export_adviser_handoff.py) | P4 (export the handoff packet that the response cycle's followup, if any, would attach) |
| `scripts/compose_adviser_message.py` | [`scripts/compose_adviser_message.py`](../../../../scripts/compose_adviser_message.py) | P4 (compose any followup draft; only if I55 loop proposes one) |
| `scripts/validate_adviser_questions.py` | [`scripts/validate_adviser_questions.py`](../../../../scripts/validate_adviser_questions.py) | P2 (G-56-1a verification) |
| `scripts/validate_founder_filed_instruments.py` | [`scripts/validate_founder_filed_instruments.py`](../../../../scripts/validate_founder_filed_instruments.py) | P2 (G-56-1b verification) |
| `scripts/validate_goipoi_register.py` | [`scripts/validate_goipoi_register.py`](../../../../scripts/validate_goipoi_register.py) | P2 (G-56-1c verification) |
| `scripts/regression_artifact_diff.py` | [`scripts/regression_artifact_diff.py`](../../../../scripts/regression_artifact_diff.py) | P4 (cite — response feeds I55 L1 → next regression cycle) |
| `scripts/propose_advisor_update.py` | [`scripts/propose_advisor_update.py`](../../../../scripts/propose_advisor_update.py) | P6 (only if loop proposes a follow-up) |

Per the master-roadmap "asset classification → New scripts: None expected. I56 is rails-exercise, not new tooling." This list is the read-side of that contract.
