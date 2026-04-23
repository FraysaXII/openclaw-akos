# delete-legal-transcripts — legal call staging (non-canonical)

**Purpose:** Temporary in-repo holding area for **raw legal and adviser call transcripts** (and related exports) used to extract questions, actions, and facts for founder incorporation / ENISA / constitution work.

**Not canonical HLK knowledge.** Do not treat this folder as the vault SSOT. For promotion rules and binding vs narrative, see [FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md](../../v3.0/Admin/O5-1/People/Compliance/FOUNDER_GOVERNANCE_DOCUMENT_LIFECYCLE.md). For counsel-facing packaging and read order, see [EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md](../../v3.0/Admin/O5-1/People/Legal/EXTERNAL_COUNSEL_HANDOFF_PACKAGE.md) and [FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md](../../v3.0/Admin/O5-1/People/Legal/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md).

## Retention

After structured items are captured in Legal vault or `docs/wip/`, **prefer removing** transcript copies from git or replacing them with **redacted summaries** (operator / Legal decision). Binary `.docx` exports are convenience mirrors; markdown transcripts are the usual ingestion source.

## Contents (expected)

- Pre-kick-off and kick-off calls (constitution, fiscal, ENISA / startup plan).
- Optional Word exports alongside `.md` transcripts.

`py scripts/validate_hlk.py` does not lint binaries; keep markdown paths valid when linking from vault docs.
