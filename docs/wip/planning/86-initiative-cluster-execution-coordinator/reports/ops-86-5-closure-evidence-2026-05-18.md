---
language: en
status: active
role_owner: Brand & Narrative Manager
co_owner_role: PMO
area: Operations / Marketing
entity: Holistika Research SL
program_id: PRJ-HOL-FOUNDING-2026
authored: 2026-05-18
last_review: 2026-05-18
linked_ops_action_ids:
  - OPS-86-5
linked_decisions:
  - D-IH-89-G
  - D-IH-86-L
  - D-IH-86-N
  - D-IH-89-E
linked_initiatives:
  - INIT-OPENCLAW_AKOS-86
  - INIT-OPENCLAW_AKOS-89
---

# OPS-86-5 closure evidence — ADVOPS harmonization sweep (2026-05-18)

> **OPS row.** `OPS-86-5` (Brand & Narrative Manager + PMO co-owned). Originally opened 2026-05-17 by I86 P3 closure with 0.2 person-week estimated effort. Closed 2026-05-18 with 0.5 person-week actual effort (expanded scope per operator instruction in same chat session).

## Scope summary (what shipped)

Seven concrete deliverables across two work-classes (content rewrite + cross-area governance wiring):

| # | Deliverable | File(s) | Effect |
|:--:|:---|:---|:---|
| 1 | **BBR drift gate cleared** | [`dossier_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md) (6 leaks fixed); [`deck_slides.yaml`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_slides.yaml) (1 leak fixed) | `py scripts/validate_brand_baseline_reality_drift.py` PASS (zero leaks across all in-scope adviser surfaces); unblocks `pre_commit` profile per `D-IH-89-E` |
| 2 | **Operator-internal questions purged from external prose** | [`dossier_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md) | Apéndice A (12 operator-internal questions Q-LEG / Q-FIS / Q-IPT / Q-BNK / Q-CRT) removed; their canonical home is [`FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/FOUNDER_OPEN_QUESTIONS_EXTERNAL_COUNSEL.md) (not the ENISA dossier) |
| 3 | **TODO[OPERATOR] markers replaced** | [`dossier_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md) | 4 markers (objeto social options + ruta de constitución choice + capital social options + PESTEL factors + plan de personal) → external-register prose carrying the resolved positions |
| 4 | **Entity name alignment** | [`dossier_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/dossier_es.md), [`deck_story_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/deck_story_es.md), [`cover_email_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_evidence/cover_email_es.md), [`cover_email_company_dossier_es.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/enisa_company_dossier/cover_email_company_dossier_es.md) | Holistika Research → Holistika Research SL consistently |
| 5 | **Legal-constitutor handoff minted** | [`legal-constitutor-handoff-2026-05-18.md`](../../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/01-our-pack/legal-constitutor-handoff-2026-05-18.md) | 5 SL name candidates (SET A: Holistika Research SL primary + Holistika Research Lab SL / Holistika Sistemas SL / Holistika Métodos SL / Holistika Aplicada SL); 3 K€ tribute breakdown table; in-kind asset contribution table (operator-fill slots for PC + phone + 3 additional); cash transfer slot; per-share structure; cross-links to all founder-incorporation canonicals |
| 6 | **Cross-area governance README minted** | [`_assets/advops/PRJ-HOL-FOUNDING-2026/README.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/README.md) (was absent) | Explains program_id (`PRJ-HOL-FOUNDING-2026`) vs engagement_slug (`2026-holistika-incorporation`) split; cross-wires both folders; documents BBR posture for the asset bucket; tracks the `adviser_handoff/` vs `adviser-handoff/` validator-glob-vs-folder-naming gap for follow-up |
| 7 | **Engagement README reciprocal cross-link** | [`Think Big/Advisers/2026-holistika-incorporation/README.md`](../../../../references/hlk/v3.0/Think%20Big/Advisers/2026-holistika-incorporation/README.md) | New `linked_program_asset_bucket:` frontmatter field; `01-our-pack/` row promoted from "placeholder" to "populated (2026-05-18)"; new "program asset bucket" cross-reference section; `last_review` bumped to 2026-05-18 |

## Validator evidence (mechanical PASS rows)

```
py scripts/validate_brand_baseline_reality_drift.py
→ BRAND_BASELINE_REALITY OK — dual-register contract holds; 8 internal token(s) checked
   Exit 0

py scripts/validate_hlk.py
→ OVERALL: PASS
   (Decision register: PASS; Master-roadmap frontmatter: PASS; Language frontmatter: PASS;
    OPS register: PASS; Initiative registry: PASS; all other umbrella validators: PASS)
   Exit 0

py scripts/validate_hlk_vault_links.py
→ validate_hlk_vault_links: PASS (no broken internal .md links)
   Exit 0
```

## Validator-evidence pivot (why we did NOT rename the directory)

The original operator answer to the metadata-strategy ratify (2026-05-17 chat) selected `meta-b` (FULL METADATA TRANSLATION), which I had originally framed as including a literal rename of `_assets/advops/PRJ-HOL-FOUNDING-2026/` → `_assets/advops/2026-holistika-incorporation/` (aligning with the Think Big/Advisers engagement slug).

On re-reading [`scripts/validate_brand_baseline_reality_drift.py`](../../../../../scripts/validate_brand_baseline_reality_drift.py) L160-185 + L197-207 with the actual leak text in hand:

- The validator scans **file content** (regex `\bPRJ-HOL-\b` against the full text body) — **not directory paths**.
- The glob set targets `**/deck/*.yaml`, `**/dossier_*.md`, `**/deck_slides.yaml`, `**/founder-filed/**/*.md`, `**/adviser-handoff/*.md` — the directory name `_assets/advops/PRJ-HOL-FOUNDING-2026/` itself is **not** what the validator measures.

A literal directory rename would therefore:
- NOT fix any of the 7 BBR leaks (those are text-body content hits, fixed by content rewrite per Deliverable 1 above).
- Break ~30 cross-references across canonicals, manifests, manifest-mmd sources, planning docs, decision logs, and frontmatter `program_id:` slots that all reference the program-id-anchored path.
- Decouple the asset-bucket folder name from the PMO program-id discipline (`PRJ-HOL-*` is the PMO portfolio key; every PMO-tracked program asset bucket lives at `_assets/advops/<program_id>/`).

The operator's deeper instruction — *"properly wire everything up and activate cross area"* — was governance cross-wiring, not literal folder rename. The chosen path (content rewrite + cross-area README minting + reciprocal engagement-README link) delivers the operator's intent without breaking the program-id discipline.

**Decision logged:** `D-IH-89-G` (`decision_source: agent_inline_default_accepted_via_explicit_skip 2026-05-18` + `validator_evidence_pivot`). Operator may override the pivot and request the literal rename in a follow-up ratify if the program-id-vs-engagement-slug architecture should be revisited at the asset-bucket level.

## Deliverable narrative (operator-visible summary)

**Sub-lane A — ADVOPS prose harmonization** (Deliverables 1-4)

The ENISA evidence dossier (`dossier_es.md`) and its visual companion (`deck_slides.yaml`) were carrying operator-internal vocabulary that would have read as "tradecraft jargon" to an ENISA reviewer (the `PRJ-HOL-FOUNDING-2026` program identifier) and operator-internal task markers (the `TODO[OPERATOR]` blocks + the 12-question appendix that duplicated the canonical FOUNDER_OPEN_QUESTIONS register). The rewrite preserves the dossier's substantive content (Pillars I-IV + apéndices for filed instruments + capabilities + glosario + trazabilidad) while translating it consistently to the external register per [`BRAND_BASELINE_REALITY_MATRIX.md`](../../../../references/hlk/v3.0/Admin/O5-1/Marketing/Brand/canonicals/BRAND_BASELINE_REALITY_MATRIX.md). The "el primer vehículo legal" framing (operator-flagged as unclear) was rewritten to explicit "Holistika Research SL es la primera sociedad operativa del grupo".

Cover-emails were refreshed to: (a) anchor recipient via ref_id (`POI-LEG-ENISA-LEAD-2026`) with the real name resolved off-repo at SMTP send time per [`SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/SOP-HLK_GOIPOI_REGISTER_MAINTENANCE_001.md); (b) remove operator-internal CNAE recommendations from the body (they belong in the dossier, not the cover note); (c) wrap operator-internal notes in HTML-comment-fenced "NOTAS INTERNAS (no enviar)" sections clearly separated from the send-as-is body.

**Sub-lane B — Legal-constitutor handoff bundle** (Deliverable 5)

The legal constitutor was waiting on four operator-side inputs (5 SL name candidates + tribute breakdown + asset contribution table + cash contribution amount) to unblock the constitution filing. The new handoff bundle scaffolds all four with operator-fill slots for the data only the founder can provide (asset serial numbers + estimated values + cash amount + SL name order confirmation). The 5 SL name proposals (SET A — methodology-anchored: "Holistika Research SL" primary; "Holistika Research Lab SL" / "Holistika Sistemas SL" / "Holistika Métodos SL" / "Holistika Aplicada SL" as backups in descending preference) balance brand-voice fit + Spanish-market resonance + low Registro-Mercantil collision risk per [`BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md`](../../../../references/hlk/v3.0/Admin/O5-1/People/Legal/canonicals/BRAND_HIERARCHY_AND_TRADEMARK_SCOPE_2026-04.md).

**Sub-lane C — Cross-area governance wiring** (Deliverables 6-7)

The `_assets/advops/PRJ-HOL-FOUNDING-2026/` folder previously had no README, leaving the relationship between (a) the PMO program-id-anchored asset bucket + (b) the Think Big/Advisers engagement-slug-anchored inbound bundle implicit. The new asset-bucket README makes the two-slug architecture explicit + cross-wires both folders + documents the BBR posture for prose authored under the bucket. The engagement README now reciprocally links to the asset bucket via a new `linked_program_asset_bucket:` frontmatter field + a new "Cross-references — program asset bucket" section. Operators and advisers can now navigate seamlessly between canonical narrative + machine-readable registers + engagement scaffold + rendered external collateral.

## Known follow-up items (not in OPS-86-5 scope; routed to other OPS rows)

| Follow-up | Status | Owner | Routing |
|:---|:---|:---|:---|
| Validator glob naming mismatch: `adviser_handoff/` (underscore, current folder) vs `adviser-handoff/` (hyphen, validator glob) | Tracked in [`_assets/advops/PRJ-HOL-FOUNDING-2026/README.md`](../../../../references/hlk/v3.0/_assets/advops/PRJ-HOL-FOUNDING-2026/README.md) §"Folder shape" note | System Owner | Future OPS row when the operator decides whether to rename the folder or extend the validator glob |
| Operator-side data fill in the legal-constitutor handoff (asset serial numbers + valuations + cash amount + SL name order confirmation) | Pending operator | Founder | Operator action item; legal-constitutor sends back confirmation under `02-adviser-pack/legal-constitutor-confirmation-<date>.md` |
| Trademark filings (umbrella "Holistika" + design mark + product brands) | Separate engagement | Legal Counsel (trademark-track) | Mint future engagement folder `Think Big/Advisers/2026-trademark-counsel/` when the legal-constitutor confirms the SL name + filing strategy |
| ENISA-track adviser handoff package | Pending mint | Compliance | Future `01-our-pack/enisa-handoff-<date>.md` mint when business plan + PESTEL closure decisions are operator-ratified |
| Banking & KYC handoff package | Pending mint | Legal Counsel | Future `01-our-pack/banking-kyc-handoff-<date>.md` mint when `GOI-BNK-INC-2026` constitution-desk opens the constitution-account |

## Cross-references

- Closing decision: `D-IH-89-G` in [`DECISION_REGISTER.csv`](../../../../references/hlk/v3.0/Admin/O5-1/People/Compliance/canonicals/DECISION_REGISTER.csv).
- Operator instruction trail (2026-05-17 + 2026-05-18): see I86 master-roadmap §"Round 4 — I89 promotion + BBR gate flip" + I89 decision-log.
- Original OPS row mint: [I86 P3 closure pause record](../reports/p3-closure-pause-record-2026-05-17.md).
- Governing cursor rules: [`akos-brand-baseline-reality.mdc`](../../../../../.cursor/rules/akos-brand-baseline-reality.mdc), [`akos-adviser-engagement.mdc`](../../../../../.cursor/rules/akos-adviser-engagement.mdc), [`akos-planning-traceability.mdc`](../../../../../.cursor/rules/akos-planning-traceability.mdc).
