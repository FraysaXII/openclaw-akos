---
language: en
status: active
canonical: true
role_owner: Founder
classification: fact
intellectual_kind: corpus_inventory
ssot: true
confidentiality: confidential
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - FOUNDER_METHODOLOGY_VERSIONING.md
  - LOGIC_CHANGE_LOG.md
  - ../FOUNDER_TRAJECTORY_INTERNAL.md
  - ../FOUNDER_BIO.md
---

# FOUNDER_CORPUS_INVENTORY — 8-section non-git-native artifact registry

> Authored I70 P9 (§9.7) per plan section 9. Codifies founder personal artifacts (notebooks, self-audios, R&L spreadsheets, CVs, epistemology images, Bâtard organigram) as **first-class governed entities** with retention class + confidentiality + digitization status. Per **H3 ratification**: this is the **only** operator-internal canonical where the founder name `Fayçal Njoya` appears explicitly — because the corpus inventories CV files where the name is on the artifact, and anonymizing there would be performative.

> **Confidentiality:** `confidential` (access_level 5). This canonical lives at `People/canonicals/` (not customer-facing); never reproduced verbatim on customer-facing surfaces; never quoted in proposals or rendered to investor pack body prose.

## 1. Why a corpus inventory

Pre-I70, founder personal artifacts existed across the operator's local filesystem + Drive + paper notebooks + audio recordings on phone, with no governance. Three signals motivated formal inventory:

1. **Disaster-recovery property** (per `WORKSPACE_BLUEPRINT_HOLISTIKA.md` §14 + F-72 disaster-recovery claim): the founder corpus is the substrate that the AKOS canonicals reference. Without inventory, recovery is impossible after device-loss / data-corruption.
2. **MADEIRA productization vector** (per D-IH-70-V + HLK_ERP_ARCHITECTURE §8 trigger): when the L6 founder-companion AI agent productizes, it needs auditable training corpus. The inventory IS the audit trail.
3. **v3.0 doctrinal substrate** (per `FOUNDER_METHODOLOGY_VERSIONING.md` §2): v0 corpus + v1 corpus + v2.x corpus must be accounted for. The lineage's authority depends on the corpus being inventoried.

## 2. The 8 sections (artifact families)

### Section 1 — Notebooks (paper + digital)

Per-notebook inventory: notebook_id + date_range + topic_areas + storage_location + digitization_status + retention_class.

Per H3: **founder name `Fayçal Njoya`** appears on most notebook covers. Inventory rows cite the literal cover marking.

Reserved for full enumeration during operator-driven corpus session. Initial seed rows expected: ~6-12 notebooks spanning v0-to-v3.0.

### Section 2 — Self-audios (operator voice memos + dictations)

Per-recording inventory: recording_id + date + topic_summary + duration + storage_location + transcription_status + retention_class.

Many self-audios are stored in `temp-move-or-delete-hlk-business-context/` under engagement-specific sub-folders (Asesoria Hosteleria, EFA, Websitz, ShadowGPU, Think Big — Service Management SSOT) per the existing untracked-folder pattern from session-start git status.

Reserved for full enumeration. Initial seed rows expected: ~30-50 recordings.

### Section 3 — Research and Logic spreadsheets (R&L corpus)

Per-spreadsheet inventory: spreadsheet_id + date + topic + storage_location + relevance_to_methodology + retention_class.

Lives at `docs/references/hlk/Research & Logic/` (per WORKSPACE_BLUEPRINT_HOLISTIKA §14 agent-only content channel pattern). Currently a sparse-mirror per D-IH-70-D.

Reserved for full enumeration. Initial seed rows expected: ~5-10 spreadsheets.

### Section 4 — CV files

Per-CV inventory: file_path + name (literal, including founder name `Fayçal Njoya`) + date + audience + storage_location + retention_class.

The founder-name appears literally on these files (anonymizing is performative; per H3 they're the exception).

Known existing files (pre-I70):
- `temp-move-or-delete-hlk-business-context/CV LinkedinProfile.pdf`
- `temp-move-or-delete-hlk-business-context/Fayçal Njoya CV - EN.pdf`

Both currently untracked at session-start; migration target deferred to operator-driven temp-folder migration session.

### Section 5 — Epistemology images (visual frameworks)

Per-image inventory: image_id + date + topic + storage_location + relevance + retention_class.

Hand-drawn / hand-edited diagrams the founder uses to think. Examples (placeholder — full inventory at corpus session):
- v0/v1 mental-model sketches.
- Holistik Ops 6-axis discovery framework (per HOLISTIK_OPS_DISCOVERY.md cross-reference).
- v2.x AKOS canonicals mental architecture.

Reserved for full enumeration.

### Section 6 — Bâtard organigram (founder-brand precedent)

Per founder principle 2.4 (Brand-as-authority-shield): the **first Bâtard organigram already carried the Holistika logo**. This is the v1 era artifact that proves the brand-precedes-substance pattern.

Inventory:
- `bâtard-organigram-v1` — date: TBD (operator confirms); storage: TBD (likely paper + scan); retention_class: confidential + permanent.
- Historical note: the organigram represents the founder's pre-Holistika-company brand-positioning thought experiment that crystallized into Holistika the company.

Reserved for operator-confirmed scan + cataloging.

### Section 7 — Operator-private decision log (informal)

Per-decision inventory beyond the canonical `DECISION_REGISTER.csv`. The founder maintains an informal "thinking-out-loud" log that captures decisions BEFORE they reach DECISION_REGISTER (which only tracks ratified decisions).

Reserved for operator-driven inventory + decision-on-promotion pattern (some informal decisions promote to DECISION_REGISTER per §13 4-step ladder; most stay private).

### Section 8 — Cross-area knowledge fragments

Per-fragment inventory: fragment_id + date + cross-area-tags + storage_location + retention_class.

Catch-all for founder-private knowledge fragments that don't fit sections 1-7: post-its, voice-memo snippets, drawing-on-napkin photos, conversation transcript excerpts.

Reserved for ongoing operator curation. KM Officer (post-Research area activation per P4.7) curates Tier 1 promotion candidates from this section.

## 3. Retention class taxonomy

Per the v3.0 governance:

| Retention class | Definition | Examples |
|:---|:---|:---|
| **permanent** | Never delete; archive at OS-migration trigger | Bâtard organigram (§6); founder-CV-files (§4); v0-v2.7 lineage notebooks |
| **engagement-tied** | Retain for engagement duration + 24 months post-engagement | Per-engagement self-audios (§2); per-engagement R&L spreadsheets (§3) |
| **review-quarterly** | Founder reviews quarterly; promote to permanent OR delete | Cross-area knowledge fragments (§8); informal decision log (§7) |
| **scratchpad** | Auto-delete after 30 days unless promoted | Voice memos used for in-the-moment thinking (§2 sub-class); not yet enumerated |

## 4. Confidentiality posture

- **All Section 1-8 inventories are `confidential` access_level 5.**
- This canonical itself is `confidential` and never rendered to customer-facing surfaces.
- Per H3: the founder name `Fayçal Njoya` is allowed in this canonical specifically because §4 inventories CV files where the name is on the artifact (anonymizing is performative).
- Section 7 (informal decision log) is the highest-sensitivity sub-section; access requires founder explicit consent for any agent-read operation beyond inventory metadata.

## 5. OS-migration implications

When TRIGGER-1 fires (MADEIRA productizes per WORKSPACE_BLUEPRINT_HOLISTIKA §15.2 + MADEIRA-AKOS/STATUS.md §3):
- Section 4 CV files travel with the founder; never become library content.
- Sections 1-3, 5-8 require operator-driven decision per artifact: keep operator-private OR migrate to library form (Scenario B / B').
- This canonical's section structure remains; the inventory's content gets per-section visibility decisions.

## 6. Cross-references

- Parent canonical: [`FOUNDER_METHODOLOGY_VERSIONING.md`](FOUNDER_METHODOLOGY_VERSIONING.md) §2 (v0-v2.7 corpus is materialized in §1-§5 below).
- Sister: [`LOGIC_CHANGE_LOG.md`](LOGIC_CHANGE_LOG.md) — version-driving insight register.
- WORKSPACE_BLUEPRINT_HOLISTIKA.md §14 (agent-only content channel pattern; R&L spreadsheets per §3 here).
- WORKSPACE_BLUEPRINT_HOLISTIKA.md §15.1 (founder-corpus registry hook; points here).
- FOUNDER_TRAJECTORY_INTERNAL.md (People/) — operator-internal full personal trajectory; confidential access_level 5; cross-references this inventory.
- FOUNDER_BIO.md (People/) — external canonical (anonymized public-facing variants); does NOT cross-reference this confidential inventory.
- D-IH-70-V — AIC-as-category framing; MADEIRA productization gates corpus visibility decisions.
- H3 ratification (Pre-handoff) — founder name `Fayçal Njoya` allowed in this canonical specifically.
- H4 ratification — the `temp-move-or-delete-hlk-business-context/` folder enumeration (deferred to operator-driven temp-folder migration session per P9 §9.8 inline-ratify gate; deferred per chat-budget realities).
- I70 plan §9.7 — full P9.7 deliverable spec.
