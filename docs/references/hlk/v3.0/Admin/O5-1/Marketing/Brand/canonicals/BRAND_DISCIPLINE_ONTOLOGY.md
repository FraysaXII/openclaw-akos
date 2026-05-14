---
language: en
status: active
canonical: true
role_owner: Brand Manager + Founder
classification: way_of_working
intellectual_kind: ontology_specification
ssot: true
authored: 2026-05-12
last_review: 2026-05-12
companion_to:
  - BRAND_VISION.md
  - BRAND_ARCHITECTURE.md
  - BRAND_VOICE_FOUNDATION.md
  - BRAND_COPYWRITING_DISCIPLINE.md
  - ../AV/canonicals/BRAND_AV_CHARTER.md
  - ../Copywriter/canonicals/BRAND_COPYWRITING_DISCIPLINE.md
  - ../Design/canonicals/BRAND_DESIGN_CHARTER.md
  - "../UX Designer/canonicals/BRAND_UX_DESIGNER_CHARTER.md"
  - "../UX Designer/canonicals/BRAND_GANTT_DISCIPLINE.md"
---

# BRAND_DISCIPLINE_ONTOLOGY — Brand sub-discipline parent canonical

> Authored I70 P5 per plan section 5. Parent canonical for the four brand sub-disciplines (AV / Copywriter / Design / UX-Designer). Mirrors the Research area's 4-discipline structure (Methodology / Intelligence / Diagnosis / Validation per RESEARCH_AREA_CHARTER.md). Codifies single-ownership boundaries, the per-discipline craft, the cross-cutting render-pipeline ownership (cross-link to P10 §16), and the **Storytelling-authors / Resonance-consumes** boundary contract from P2.5 D-IH-70-X (forward-context for P8 §8.4 Marketing M3 redesign).

## 1. Why a parent ontology

Pre-I70, Brand was a single role under Marketing with all primitives bundled (visual + voice + register + canon-drift gates). The SUEZ engagement (I12 P12 + I70 P0) revealed that the four primitive families (audio-visual / copy / visual-design / UX-design) need separate doctrine homes:

- **AV** owns audio + video primitives — voiceover, podcast, video-deck transitions, audio-cue patterns. Today: empty scaffold; future: founder-bio-podcast variant + investor-pitch video render path.
- **Copywriter** owns prose register at the sentence level — anti-AI-tone tics, X-pas-Y removal, triadic-noun cleanup, "Impeccable for copywriting" discipline.
- **Design** owns visual-systems primitives — color tokens, typography, spacing, illustrations, brand mark application.
- **UX-Designer** owns interaction patterns + information-architecture primitives — slide layouts (`.host-card`, `.method-anchors`, `.grid-3x2`, `.three-lines`, `.timeline-5`), Gantt-discipline (P6), counterparty-README contract patterns (P7).

Each sub-discipline gets its own canonicals/ folder + role + charter. The parent ontology (this file) codifies how they relate.

## 2. The four sub-disciplines

| Sub-discipline | Owns | Primary craft | Active SOPs/canonicals |
|:---|:---|:---|:---|
| **AV** (Brand/AV) | audio + video primitives | recording cadence; voice consistency (founder + advisor); transition-cue catalog | reserved (P5 charter stub) |
| **Copywriter** (Brand/Copywriter) | sentence-level prose register | anti-AI-tone tic catalog; positive-claim register; "Impeccable for copywriting" discipline | BRAND_COPYWRITING_DISCIPLINE.md (this commit) |
| **Design** (Brand/Design) | visual-systems primitives | color tokens (BRAND_VISUAL_PATTERNS §1); typography scale; brand mark application | reserved (P5 charter stub); cross-link to BRAND_VISUAL_PATTERNS |
| **UX-Designer** (Brand/UX Designer) | interaction patterns + information architecture | slide layout primitives; Gantt discipline (P6); counterparty-README pattern (P7); slide-legibility QA | reserved (P5 charter stub); BRAND_GANTT_DISCIPLINE.md (P6) |

## 3. Single-ownership rule (mirrors P2.5 D-IH-70-X Storytelling/Resonance pattern)

To prevent dilution between sub-disciplines:

- **AV authors audio-visual artifacts** (founder podcast cuts, investor-pitch video). Copywriter authors prose; AV records prose.
- **Copywriter authors prose register** (BRAND_COPYWRITING_DISCIPLINE.md). Design authors visual register; Copywriter never overrides visual layout.
- **Design authors visual primitives** (color, typography, illustrations). UX-Designer authors interaction patterns; Design owns the "what it looks like at rest".
- **UX-Designer authors interaction patterns** (slide layouts, Gantt, counterparty-README structure). Design + Copywriter feed UX-Designer; UX-Designer owns the integration.

**Cross-cutting render-pipeline ownership** (cross-linked from WORKSPACE_BLUEPRINT §16 + Phase 10):

The render pipeline (`scripts/render_*_engagement_pdfs.py` + `akos/hlk_pdf_render.py`) is jointly owned by Brand sub-disciplines (4 voices in the room) + PMO + RevOps (future I72) + HLK Tech Lab + SMO + Account Management. Per P10 the full ownership matrix table is authored; this ontology asserts the Brand-side claim.

## 4. Marketing M3 redesign cross-references (P8 §8.4 forward-link)

Per Conundrum 12 + D-IH-70-T (Marketing area redesign at P8 §8.4):

- **Brand (saying)** — owns the four sub-disciplines above. This ontology lives here.
- **Reach (extending)** — acquisition + Demand Generation + Paid Media. Cross-references Brand for voice/visual register but doesn't author it.
- **Resonance (deepening)** — Resonance Manager (generalist holding Community-Management discipline per D-IH-72-AN) + Account Management Manager (kept). **CONSUMES** Brand-authored artifacts in 1:1 relationship contexts (per D-IH-70-X forward-context).
- **Storytelling (conveying)** — Storytelling Manager (generalist holding Thought-Leadership-Editorial + Corporate-Marketing disciplines per D-IH-72-AN) + PR Manager (kept). **AUTHORS** narrative artifacts that integrate Brand sub-discipline outputs (case studies, press releases, employer-brand collateral). Single-ownership boundary: Storytelling integrates Brand voice; Brand never authors the integrated narrative. **MERGES with Brand at R-E into Brand & Narrative sub-area per D-IH-72-AO** (regression-amend 2026-05-15).
- **Experimentation (testing)** — Experimentation Manager (generalist holding Growth-Hacker discipline per D-IH-72-AN) + Marketing Analytics Manager (kept). Tests Brand-authored prose/visual variants against engagement metrics; never authors register itself.

The Storytelling-authors / Resonance-consumes boundary (D-IH-70-X) extends here:

- Brand sub-disciplines AUTHOR primitives (voice, visual, interaction, AV).
- Storytelling INTEGRATES primitives into narrative artifacts.
- Resonance DEPLOYS narrative artifacts in 1:1 contexts.
- Reach AMPLIFIES narrative artifacts via channels.
- Experimentation MEASURES variant performance.

## 5. Slide-legibility QA discipline (UX-Designer owns; cross-cutting concern)

Per plan section 5 §4: every customer-facing deck slide passes slide-legibility QA before render. The UX-Designer charter (reserved, P5 stub) codifies the gates:

- **Headline gate**: H2 must be ≤ 60 characters; not start with internal-jargon-tokens (per BRAND_JARGON_AUDIT §4); pass anti-AI-tone tic regex (per BRAND_COPYWRITING_DISCIPLINE).
- **Body gate**: paragraph max 4 sentences; no triadic noun-phrase stacks (per BRAND_COPYWRITING_DISCIPLINE §3); no `X, pas Y` AI-tic.
- **Visual gate**: contrast ratio ≥ 4.5:1 for body text (WCAG 2.2 AA); no overlapping interactive regions; cover-strip carries 4 fields max.
- **Multilingual gate** (per P7 BRAND_MULTILINGUAL_CONTRACT): per-language register matches per-engagement language declaration.
- **Counterparty gate** (per P7 BRAND_COUNTERPARTY_README_CONTRACT): no operator-jargon visible to counterparty; proper register tier per BRAND_REGISTER_MATRIX.

Slide-legibility QA runs as part of `scripts/render_suez_engagement_pdfs.py --check` (or equivalent per-engagement render script) before PDF emission.

## 6. External research brief — Impeccable-copywriting prior art (Tier 3 WIP)

Per plan section 5: external research on the "Impeccable for copywriting" prior art lives at `Marketing/Brand/Copywriter/wip/2026-impeccable-copywriting/` (Tier 3 per blueprint §17 — area-scoped, role-owned). The brief surveys public copywriting craft (David Ogilvy, Joseph Sugarman, Eugene Schwartz, modern long-form newsletter craft) and named-AI-tone catalogs (Reddit /r/COPYWRITING anti-tic threads, recent academic pieces on LLM-prose detection markers). The brief feeds BRAND_COPYWRITING_DISCIPLINE.md (this commit's sibling) and the copywriting rule pack on `validate_brand_voice_register.py` (deferred to I71 implementation).

## 7. Cross-references

- BRAND_VISION.md (Marketing/Brand/canonicals/) — outward-facing vision; sub-disciplines serve this vision.
- BRAND_ARCHITECTURE.md (Marketing/Brand/canonicals/) — Branded House structure; sub-disciplines operate at the Holistika sub-mark.
- BRAND_VOICE_FOUNDATION.md (Marketing/Brand/canonicals/) — voice charter; Copywriter sub-discipline operates the discipline below it.
- BRAND_REGISTER_MATRIX.md (Marketing/Brand/canonicals/) — relationship × channel → register matrix; UX-Designer + Copywriter both consume this.
- BRAND_COPYWRITING_DISCIPLINE.md (this commit) — the Copywriter sub-discipline canonical with the 7 tic families.
- BRAND_GANTT_DISCIPLINE.md (P6 forward-link, UX-Designer/canonicals/).
- BRAND_MULTILINGUAL_CONTRACT.md (P7 forward-link).
- BRAND_COUNTERPARTY_README_CONTRACT.md (P7 forward-link).
- WORKSPACE_BLUEPRINT_HOLISTIKA §16 (render pipeline ownership matrix; cross-link to P10).
- D-IH-70-X (P2.5 audit sub-decision: Corporate Marketing -> Marketing/Storytelling; Storytelling-authors / Resonance-consumes boundary).
- D-IH-70-T (Conundrum 12 ratification: Marketing M3 redesign).
- I70 plan section 5 — full P5 deliverable spec.
