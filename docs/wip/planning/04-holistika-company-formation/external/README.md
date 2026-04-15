# External incorporation / certification sources (UTF-8 markdown only)

**Status**: Non-canonical operator mirror.  
**Governance**: Raw audio and vendor **`.docx`** files stay **outside** this repository or in secure storage. This folder holds **one-time exports** to **real UTF-8 `.md`** so operators are not misled by `.md` filenames that actually contain binary Office XML.

## Export rule

1. Open each `.docx` (or mislabeled “`.m4a.md`” that is actually a ZIP) in an editor that can export **plain UTF-8 markdown**, or run a local script to extract `word/document.xml` and strip tags.  
2. Save here as `*.md` with ASCII filenames (e.g. `pre-kickoff-fiscal-2026-04-06.md`).  
3. **Redact** personal names and direct identifiers of external individuals before committing.  
4. Link paths from [TOPIC_PMO_CLIENT_DELIVERY_HUB.md](../../../../references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md) portfolio row `external_sources` column.

## Current exports (UTF-8)

| File | Notes |
|:-----|:------|
| `pre-kickoff-alcance-2026-04-02.md` | Scope pre-kick (from vendor `.docx`) |
| `pre-kickoff-fiscal-2026-04-06.md` | Fiscal pre-kick (from mislabeled zip-as-`.md`) |
| `pre-kickoff-fiscal-2026-04-06-part2.md` | Fiscal pre-kick duplicate thread export |
| `founder-incorporation-report-export.md` | Working notes export |
| `kick-off-enisa-2026-08-04-part1.md` | Main ENISA / plan kick-off transcript |
| `kick-off-enisa-2026-08-04-part2.md` | Short follow-on fragment |

External individual names are genericized to `[bank desk contact]` where they appeared in source text.

Do not commit **binary** `.docx` into this repo unless policy explicitly allows; prefer markdown exports only.
