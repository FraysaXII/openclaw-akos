# delete-legal-transcripts — legal call staging (non-canonical, redacted)

**Purpose:** Temporary in-repo holding area for **adviser call transcripts** (constitution / fiscal / ENISA work). Files in this folder are **redacted forward-only** per [SOP-HLK_TRANSCRIPT_REDACTION_001](../../v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md): private organisations and persons are referenced by `GOI-*` / `POI-*` `ref_id` from [GOI_POI_REGISTER.csv](../../compliance/GOI_POI_REGISTER.csv); raw originals and unredacted markdown are kept off-repo by Compliance.

**Not canonical HLK knowledge.** Do not treat this folder as the vault SSOT. For promotion rules and binding vs narrative, see [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../../v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md). For counsel-facing packaging and read order, see [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](../../v3.0/Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) and [FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md](../../v3.0/Admin/O5-1/People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).

## Redaction posture (Initiative 21 / P2, decision D-CH-2)

- **Forward-only:** Current tip is redacted using the GOI/POI register; commit history is **not** rewritten. Re-evaluation triggers are documented in [decision-log.md](../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/decision-log.md).
- **Helper:** `py scripts/redact_transcripts_p2.py --apply --report <path>` (idempotent).
- **Substitutions** applied to existing transcripts include the adviser firm (→ `GOI-ADV-ENTITY-2026`), the ENISA-track adviser (→ `POI-LEG-ENISA-LEAD-2026`), the intake-stage contact (→ `POI-ADV-INTAKE-LEAD-2026`), and personal `source:` paths in YAML frontmatter.

## Retention

After structured items are captured in Legal vault, the [adviser open questions register](../../v3.0/Admin/O5-1/People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md), or `docs/wip/`, **prefer removing** transcript copies from git or replacing them with concise **redacted summaries** (Compliance + Legal decision). Binary `.docx` exports are convenience mirrors; markdown transcripts are the usual ingestion source.

A small number of legacy files in this folder have `.md` extensions but are actually `.docx` zip archives (detected by the redaction script's encoding probe). Operator may rename or remove them; either action must be documented in the next P-2 redaction report.

## Contents (expected, redacted)

- Pre-kick-off and kick-off call transcripts (constitution, fiscal, ENISA / startup plan) — all real names substituted by `POI-*` / `GOI-*` `ref_id`.
- Optional Word exports alongside `.md` transcripts (operator-managed).

`py scripts/validate_hlk.py` does not lint these files directly; keep markdown internal links valid when linking from vault docs.
