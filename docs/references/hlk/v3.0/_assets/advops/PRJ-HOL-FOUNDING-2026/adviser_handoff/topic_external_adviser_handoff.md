# Topic: External Adviser Engagement (Founder Incorporation)

**source_id**: `topic_external_adviser_handoff`  
**topic_id**: `topic_external_adviser_handoff`  
**program_id**: `PRJ-HOL-FOUNDING-2026`  
**plane**: `advops`  
**primary_owner_role**: PMO (External Adviser Engagement plane)  
**access_level**: 2 (Internal Use)  
**output_type**: 2 (text — companion to `topic_external_adviser_handoff.manifest.md`)

---

## Scope

The KM Topic for managing **all** external adviser engagements across disciplines (Legal, Fiscal, IP, Banking, Certification, Notary) for the founder incorporation program `PRJ-HOL-FOUNDING-2026`. Future programs reuse the same plane (`advops`) under a different `program_id` subfolder. The plane is governed by:

- Plane SOP — [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- Router — [`EXTERNAL_ADVISER_ROUTER.md`](../../../../Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md)
- Cursor rule — [`.cursor/rules/akos-adviser-engagement.mdc`](../../../../../../../../.cursor/rules/akos-adviser-engagement.mdc)
- Initiative 21 — [`docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md`](../../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)
- Initiative 22 (this restructure) — [`docs/wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md`](../../../../../../../wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md)

---

## Facts (atomic claims)

Each fact references **at least one source_id** below. Facts must use **GOI/POI ref_ids only**; raw names of private parties stay off-repo.

- **F-001** — The program `PRJ-HOL-FOUNDING-2026` is engaged with `GOI-ADV-ENTITY-2026` (third-party startup-certification adviser firm) for ENISA-track entity readiness. Sources: `S-CSV-GOIPOI-2026`, `S-MD-PMOHUB-2026`.
- **F-002** — `POI-LEG-ENISA-LEAD-2026` is the primary adviser lead for the ENISA / entity-readiness lens. Sources: `S-CSV-GOIPOI-2026`, `S-MEMO-2026-04`, `S-TRANSCRIPT-KICKOFF-2026-08-04-1`.
- **F-003** — `POI-LEG-FISCAL-LEAD-2026` is the fiscal-track contact at `GOI-ADV-ENTITY-2026`. Sources: `S-CSV-GOIPOI-2026`, `S-TRANSCRIPT-FISCAL-2026-04-06`.
- **F-004** — `POI-ADV-INTAKE-LEAD-2026` is the intake contact at `GOI-ADV-ENTITY-2026` (pre-kick-off). Sources: `S-CSV-GOIPOI-2026`, `S-TRANSCRIPT-PRE-2026-04-06`.
- **F-005** — `GOI-BNK-INC-2026` is the constitution-desk bank for the program; `POI-BNK-DESK-LEAD-2026` is the named desk lead. Sources: `S-CSV-GOIPOI-2026`.
- **F-006** — Six adviser disciplines are recognised in canonical scope: `legal`, `fiscal`, `ip`, `banking`, `certification`, `notary`. Source: `S-CSV-DISCIPLINES-2026`.
- **F-007** — Twelve open questions/actions span the disciplines (`Q-LEG-001..009`, `Q-FIS-001..003`) as of 2026-04-28. Source: `S-CSV-QUESTIONS-2026`.
- **F-008** — One legal instrument is currently tracked in `draft` status: `INST-LEG-ESCRITURA-DRAFT-2026` (escritura de constitución, ES). Counterparty `GOI-ADV-ENTITY-2026`. Source: `S-CSV-INSTRUMENTS-2026`.
- **F-009** — Privacy posture is **redact-forward** per [D-CH-2](../../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/decision-log.md): canonical text uses GOI/POI ref_ids; raw history is not rewritten. Sources: `S-MD-DECISIONLOG-2026`, `S-SOP-REDACTION-2026`.
- **F-010** — Open questions and filed instruments are **graduated to canonical CSVs**; the corresponding vault MDs are derived per-discipline views. Sources: `S-CSV-QUESTIONS-2026`, `S-CSV-INSTRUMENTS-2026`, `S-PRECEDENCE-2026`.
- **F-011** — As of Initiative 22 P2, this Topic asset bundle lives under the **`<plane>/<program_id>/<topic_id>/`** convention; the prior flat `_assets/advopps/` location is retired. Sources: `S-MD-COMPLIANCE-README-2026`, `S-MD-KM-CONTRACT-2026`.
- **F-012** — As of Initiative 22 P5, the raster is **derived from a Mermaid source-of-truth** (`topic_external_adviser_handoff.mmd`) rendered via [`scripts/render_km_diagrams.py`](../../../../../../../../scripts/render_km_diagrams.py); the manifest's `paths.mermaid` slot points at the editable SSOT. Source: `S-MD-KM-CONTRACT-2026`.
- **F-013** — As of Initiative 22 P7, the four `compliance.*_mirror` tables are **applied** on the live Supabase project with row counts matching the canonical CSVs (6 / 6 / 12 / 1). Source: `S-RPT-SUPABASE-APPLY-2026`.

---

## Sources

| `source_id` | `output_type` | `location` | `access_level` | Notes |
|:------------|:--------------|:-----------|:---------------|:------|
| `S-CSV-GOIPOI-2026` | 3 | `docs/references/hlk/compliance/GOI_POI_REGISTER.csv` | 2 | Canonical groups/persons-of-interest register |
| `S-CSV-DISCIPLINES-2026` | 3 | `docs/references/hlk/compliance/ADVISER_ENGAGEMENT_DISCIPLINES.csv` | 2 | Canonical adviser disciplines lookup |
| `S-CSV-QUESTIONS-2026` | 3 | `docs/references/hlk/compliance/ADVISER_OPEN_QUESTIONS.csv` | 2 | Canonical adviser open questions register |
| `S-CSV-INSTRUMENTS-2026` | 3 | `docs/references/hlk/compliance/FOUNDER_FILED_INSTRUMENTS.csv` | 2 | Canonical filed instruments register |
| `S-PRECEDENCE-2026` | 2 | `docs/references/hlk/compliance/PRECEDENCE.md` | 2 | Authority precedence ledger |
| `S-MD-COMPLIANCE-README-2026` | 2 | `docs/references/hlk/compliance/README.md` | 2 | Initiative 22 forward layout convention |
| `S-MD-KM-CONTRACT-2026` | 2 | `docs/references/hlk/compliance/HLK_KM_TOPIC_FACT_SOURCE.md` | 2 | KM contract incl. directory convention + `paths.mermaid` slot |
| `S-MD-PMOHUB-2026` | 2 | `docs/references/hlk/v3.0/Admin/O5-1/Operations/PMO/TOPIC_PMO_CLIENT_DELIVERY_HUB.md` | 2 | PMO hub stakeholder index (derived view of GOI/POI) |
| `S-MD-DECISIONLOG-2026` | 2 | `docs/wip/planning/21-hlk-adviser-engagement-and-goipoi/decision-log.md` | 2 | Initiative 21 decision log |
| `S-MEMO-2026-04` | 2 | `docs/references/hlk/v3.0/Admin/O5-1/People/Legal/FOUNDER_ENTITY_FORMATION_DECISION_MEMO_2026-04.md` | 2 | Entity formation decision memo |
| `S-SOP-REDACTION-2026` | 2 | `docs/references/hlk/v3.0/Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md` | 2 | Transcript redaction SOP |
| `S-TRANSCRIPT-PRE-2026-04-06` | 2 | `docs/references/hlk/business-intent/delete-legal-transcripts/2026-04-06 - Pre-Kick-Off - Constitución Sociedad - Reunión inicial.m4a.md` | 2 | Redacted transcript (intake) |
| `S-TRANSCRIPT-FISCAL-2026-04-06` | 2 | `docs/references/hlk/business-intent/delete-legal-transcripts/2026-04-06 - Pre-Kick-Off - Constitución Sociedad - Fiscal.m4a.md` | 2 | Redacted transcript (fiscal pre-kick-off) — see notes |
| `S-TRANSCRIPT-KICKOFF-2026-08-04-1` | 2 | `docs/references/hlk/business-intent/delete-legal-transcripts/2026-08-04 - Kick-Off - Constitución Sociedad - Plan de Negocio Startup y ENISA_1.mp3.md` | 2 | Redacted transcript (kick-off, part 1) |
| `S-RPT-SUPABASE-APPLY-2026` | 2 | `docs/wip/planning/22-hlk-scalability-and-i21-closures/reports/p7-supabase-apply-evidence.md` | 2 | Live Supabase apply evidence (Initiative 22 P7) |

> **Notes** — Some redacted transcripts originated as binary masquerading as `.md`; see [`SOP-HLK_TRANSCRIPT_REDACTION_001.md`](../../../../Admin/O5-1/People/Compliance/SOP-HLK_TRANSCRIPT_REDACTION_001.md) and the P2 redaction report for handling. Raw originals are retained off-repo (operator-managed Drive).

---

## Refresh hooks

- After any change to the canonical CSVs (`GOI_POI_REGISTER.csv`, `ADVISER_ENGAGEMENT_DISCIPLINES.csv`, `ADVISER_OPEN_QUESTIONS.csv`, `FOUNDER_FILED_INSTRUMENTS.csv`), update the **Facts** list above to keep claim counts and ref_ids in sync.
- After any new redacted transcript or report is added under the initiative folder, append a new `S-*` row in the **Sources** table.
- After any change to the diagram source, regenerate the raster: `py scripts/render_km_diagrams.py <topic>.mmd` and refresh `file_sha256` in the manifest.
- Validate manifests with `py scripts/validate_hlk_km_manifests.py` before commit.

## Related

- [HLK_KM_TOPIC_FACT_SOURCE.md](../../../../../compliance/HLK_KM_TOPIC_FACT_SOURCE.md) — schema authority for Topic / Fact / Source.
- [Initiative 21 master-roadmap](../../../../../../../wip/planning/21-hlk-adviser-engagement-and-goipoi/master-roadmap.md)
- [Initiative 22 master-roadmap](../../../../../../../wip/planning/22-hlk-scalability-and-i21-closures/master-roadmap.md)
- [`SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md`](../../../../Admin/O5-1/Operations/PMO/SOP-EXTERNAL_ADVISER_ENGAGEMENT_001.md)
- [`EXTERNAL_ADVISER_ROUTER.md`](../../../../Admin/O5-1/Operations/PMO/EXTERNAL_ADVISER_ROUTER.md)
- [`compliance/README.md`](../../../../../compliance/README.md) — forward layout convention.

### Topic graph (Initiative 25 P4 — Obsidian wikilinks as secondary nav)

Markdown links above are **primary** (Git/GitHub + `validate_hlk_vault_links.py`). Wikilinks below are **secondary** Obsidian convention (out-of-scope for the link validator per D-IH-12).

- Child topic (depends-on): [[topic_enisa_evidence]] — ENISA evidence pack derived from this ADVOPS plane (Initiative 25 P6).
- Related topic (KiRBe consumes the same legal/fiscal foundation): [[topic_kirbe_billing_plane_routing]].
- Cross-program governance: [[topic_km_governance]] (KM pilot bundle).
